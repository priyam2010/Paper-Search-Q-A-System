from pydantic import BaseModel
class PaperSection(BaseModel):
    section_name:str
    content:str
    
    