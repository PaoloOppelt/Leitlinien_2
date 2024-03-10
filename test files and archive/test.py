from cbfs import cbfs
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
    

# Create an instance of cbfs
cbfs_instance = cbfs()
data = cbfs_instance.get_data()

# Convert each Document to a dictionary before serialization
data['source_documents'] = [doc.to_dict() for doc in data['source_documents']]

# Convert the dictionary to a JSON string
json_data = json.dumps(data, ensure_ascii=False, indent=4)

# Print the JSON string
print(json_data)