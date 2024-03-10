class Document(BaseModel):
    page_content: str
    metadata: dict = Field(default_factory=dict)

    def to_dict(self):
        return self.dict(by_alias=True, exclude_unset=True)


@app.route('/process', methods=['POST'])
def process_text():
    # Get the raw data from the request
    data = request.get_data()

    # Assuming data is a dictionary-like object that may contain 'source_documents'
    if 'source_documents' in data and isinstance(data['source_documents'], list):
        # Convert each Document in 'source_documents' to a dictionary
        data['source_documents'] = [doc.to_dict() for doc in data['source_documents'] if isinstance(doc, Document)]

    # Serialize the data to JSON
    json_data = json.dumps(data, ensure_ascii=False, indent=4)  
    print("Final result to be returned:", json_data)

    # Return the JSON data
    return json_data




@app.route('/process', methods=['POST'])
def process_text():

    # get the data from wherever it comes from don't treat is specially. 
    data = data.get('query')
    
    # Convert each Document to a dictionary before serialization
    data['source_documents'] = [doc.to_dict() for doc in data['source_documents']]

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data, ensure_ascii=False, indent=4)  
    print("Final result to be returned:", json_data)
    return json_data
