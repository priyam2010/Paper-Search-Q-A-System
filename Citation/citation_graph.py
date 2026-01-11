class CitationGraph:
    def __init__(self):
        self.graph = {}

    def add_paper(self, paper_id, references):
        self.graph[paper_id] = references

    def get_references(self, paper_id):
        return self.graph.get(paper_id, [])
    
    
    