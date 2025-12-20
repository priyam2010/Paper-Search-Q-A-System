import streamlit as st
import arxiv
import os
import certifi
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where() # Ensure SSL certificates are correctly set 

# Page configuration
st.set_page_config(
    page_title="ArXiv Paper Q&A",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'papers' not in st.session_state:
    st.session_state.papers = []
if 'selected_paper' not in st.session_state:
    st.session_state.selected_paper = None
if 'retrieval_chain' not in st.session_state:
    st.session_state.retrieval_chain = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def search_arxiv(query: str, top_k: int = 5):  # Search arXiv for papers 
    """Search arXiv for papers"""
    search = arxiv.Search(
        query=query,
        max_results=top_k,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "authors": [str(a) for a in result.authors],
            "published": result.published,
            "summary": result.summary,
            "pdf_url": result.pdf_url,
        })
    return papers

@st.cache_resource # Cache the Q&A chain setup
def setup_qa_chain(pdf_url: str, _api_key: str, model_name: str = "gemini-2.5-flash"):
    """Setup the Q&A chain for a specific paper"""
    # Load PDF
    loader = PyPDFLoader(pdf_url)
    docs = loader.load()
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    documents = text_splitter.split_documents(docs)
    
    # Create embeddings
    embedding_model = HuggingFaceEmbeddings()
    
    # Build vector database
    vectordb = FAISS.from_documents(documents, embedding_model)
    retriever = vectordb.as_retriever()
    
    # Setup prompt
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert in research paper analysis. Answer the following question based only on the provided context:
        <context>
        {context}
        </context>
        
        Question: {input}
        """
    )
    
    # Setup LLM
    llm = GoogleGenerativeAI(model=model_name, google_api_key=_api_key)
    
    # Create chains
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    return retrieval_chain

# Main UI
st.title("📚 ArXiv Paper Search & Q&A System")
st.markdown("Search for research papers on arXiv and ask questions about them using AI!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Google API Key", 
        value=os.getenv('GOOGLE_API_KEY', ''),
        type="password",
        help="Enter your Google API key for Gemini"
    )
    
    # Model selection
    model_name = st.selectbox(
        "Select Model",
        options=["gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-flash-exp"
        ],
        index=0,
        help="gemini-2.5-flash is recommended for better quota limits"
    )
    
    st.divider()
    st.header("📖 About")
    st.markdown("""
    This app allows you to:
    1. Search for papers on arXiv
    2. Select a paper to analyze
    3. Ask questions about the paper
    
    The AI will answer based only on the paper's content.
    
    **Tip:** Use gemini-2.5-flash for better rate limits!
    """)
    
    st.divider()
    st.markdown("### 💡 Troubleshooting")
    st.markdown("""
    **If you see quota errors:**
    - Switch to gemini-1.5-flash model
    - Wait a few minutes before retrying
    - Check your API usage at [Google AI Studio](https://ai.google.dev)
    """)

# Main content area
tab1, tab2 = st.tabs(["🔍 Search Papers", "💬 Ask Questions"])

with tab1:
    st.header("Search ArXiv Papers")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Enter your search query",
            placeholder="e.g., machine learning in healthcare"
        )
    with col2:
        num_results = st.number_input(
            "Number of results",
            min_value=1,
            max_value=10,
            value=5
        )
    
    if st.button("🔍 Search", type="primary"):
        if search_query:
            with st.spinner("Searching arXiv..."):
                st.session_state.papers = search_arxiv(search_query, num_results)
            st.success(f"Found {len(st.session_state.papers)} papers!")
        else:
            st.warning("Please enter a search query")
    
    # Display papers
    if st.session_state.papers:
        st.divider()
        st.subheader("Search Results")
        
        for idx, paper in enumerate(st.session_state.papers):
            with st.expander(f"📄 {idx + 1}. {paper['title']}", expanded=(idx == 0)):
                st.markdown(f"**Authors:** {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
                st.markdown(f"**Published:** {paper['published'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Summary:** {paper['summary'][:300]}...")
                st.markdown(f"**PDF URL:** [{paper['pdf_url']}]({paper['pdf_url']})")
                
                if st.button(f"Select this paper for Q&A", key=f"select_{idx}"):
                    st.session_state.selected_paper = paper
                    st.session_state.chat_history = []
                    st.session_state.retrieval_chain = None
                    st.success(f"Selected: {paper['title']}")
                    st.rerun()

with tab2:
    st.header("Ask Questions About the Paper")
    
    if st.session_state.selected_paper:
        # Display selected paper info
        with st.container():
            st.info(f"**Selected Paper:** {st.session_state.selected_paper['title']}")
            
            if st.button("🔄 Change Paper"):
                st.session_state.selected_paper = None
                st.session_state.retrieval_chain = None
                st.session_state.chat_history = []
                st.rerun()
        
        st.divider()
        
        # Setup Q&A chain if not already done
        if st.session_state.retrieval_chain is None and api_key:
            with st.spinner("Loading paper and setting up Q&A system..."):
                try:
                    st.session_state.retrieval_chain = setup_qa_chain(
                        st.session_state.selected_paper['pdf_url'],
                        api_key,
                        model_name
                    )
                    st.success("Q&A system ready!")
                except Exception as e:
                    st.error(f"Error setting up Q&A system: {str(e)}")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if question := st.chat_input("Ask a question about the paper..."):
            if not api_key:
                st.error("Please enter your Google API key in the sidebar")
            elif st.session_state.retrieval_chain:
                # Add user message
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": question
                })
                
                with st.chat_message("user"):
                    st.markdown(question)
                
                # Get AI response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            response = st.session_state.retrieval_chain.invoke({
                                'input': question
                            })
                            answer = response['answer']
                            st.markdown(answer)
                            
                            # Add assistant message
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": answer
                            })
                        except Exception as e:
                            error_msg = str(e)
                            if "429" in error_msg or "quota" in error_msg.lower():
                                st.error("⚠️ **API Quota Exceeded**")
                                st.markdown("""
                                **Solutions:**
                                1. Switch to **gemini-1.5-flash** model in the sidebar (better quota limits)
                                2. Wait a few minutes before trying again
                                3. Check your usage at [Google AI Studio](https://aistudio.google.com/apikey)
                                
                                The free tier has limits on requests per minute and per day.
                                """)
                            else:
                                st.error(f"Error: {error_msg}")
        
        # Clear chat button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
    
    else:
        st.info("👈 Please search and select a paper from the 'Search Papers' tab first")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    Built with Streamlit • Powered by LangChain & Google Gemini
    </div>
    """,
    unsafe_allow_html=True
)