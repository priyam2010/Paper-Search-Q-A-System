from pydantic import BaseModel

class Citation(BaseModel):
    source_paper_id:str
    cited_title:str
    