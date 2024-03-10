import json
from pydantic import BaseModel, Field

# Define the Document class
class Document(BaseModel):
    page_content: str
    metadata: dict = Field(default_factory=dict)

    # Method to convert to a dictionary
    def to_dict(self):
        return self.dict(by_alias=True, exclude_unset=True)

    # Method to convert to a JSON string
    def to_json(self):
        return self.json(by_alias=True, exclude_unset=True)

# Define the dictionary with the provided data
data = {'question': 'gastritits', 'chat_history': [('gastritits', 'response of last querry'), ('querry before that', 'response of querry before that')], 'answer': 'answer to current question', 'source_documents': [Document(page_content=' content of source', metadata={'source': 'nameofpdf.pdf', 'page': 56, 'Gültigkeit': 'Gültig'}), Document(page_content=' content of source 2', metadata={'source': 'name pdf source 2.pdf', 'page': 8, 'Gültigkeit': 'Abgelaufen'}), Document(page_content=' content source 3', metadata={'source': 'pdfnamesource3.pdf', 'page': 7, 'Gültigkeit': 'Gültig'})]}

# Convert each Document to a dictionary before serialization
data['source_documents'] = [doc.to_dict() for doc in data['source_documents']]

# Convert the dictionary to a JSON string
json_data = json.dumps(data, ensure_ascii=False, indent=4)

# Print the JSON string
print(json_data)