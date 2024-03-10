# Importing necessary modules and classes
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.elasticsearch import ElasticsearchStore
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
import param  # For defining parameters in classes
from dotenv import load_dotenv  # For loading environment variables
import os  # For interacting with the operating system
import openai  # OpenAI's Python client library
from pydantic import BaseModel, Field
import json
from fastapi.encoders import jsonable_encoder

# Document class definition
class Document(BaseModel):
    """Interface for interacting with a document."""
    page_content: str
    metadata: dict = Field(default_factory=dict)

    def to_json(self):
        return self.model_dump_json(by_alias=True, exclude_unset=True)

# Environment variable setup
dotenv_path = 'KEYs.env'
_ = load_dotenv(os.path.join(os.path.dirname(__file__), '../KEYs.env'))

# API keys and Elasticsearch credentials
openai.api_key = os.environ['OPENAI_API_KEY']
_es_cloud_id = os.environ['es_cloud_id']
_es_user = os.environ['es_user']
_es_password = os.environ['es_password']

# OpenAI embeddings initialization
embedding = OpenAIEmbeddings()

# Elasticsearch vector search setup
elastic_vector_search = ElasticsearchStore(
    es_cloud_id=_es_cloud_id,
    index_name="leitliniengpt",
    embedding=embedding,
    es_user=_es_user,
    es_password=_es_password,
)

# Fallback message
No_Doc = "Die hinterlegten Leitlinien Dokumente enthalten keine Informationen zu Ihrer Frage."

# Prompt template definition
template = """
Only base your response on the context. 
The answer should not exceed 8 sentences.
Memorize the language I ask you in my question.
context: {context}
question: {question}
Answer in the same language which I requested you to memorize.
:"""

prompt = PromptTemplate.from_template(template)

# ConversationalRetrievalChain model initialization function
def Init_model():
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"),
        retriever=elastic_vector_search.as_retriever(search_kwargs={"k": 3}),
        combine_docs_chain_kwargs={"prompt": prompt},
        response_if_no_docs_found=No_Doc,
        return_source_documents=True,
        chain_type='stuff'
    )
    return qa

# cbfs class definition
class cbfs(param.Parameterized):
    chat_history = param.List([])
    count = param.List([])

    def __init__(self, **params):
        super(cbfs, self).__init__(**params)
        self.qa = Init_model()

    def load_model(self, Database):
        # Implement the specific configuration for different databases
        if Database == "Nur aktuell gültige Leitlinien":
            self.qa = ConversationalRetrievalChain.from_llm(...)
            self.count.append(1)
        else:
            self.qa = Init_model()

    def convchain(self, query):
        result = self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        
        # Convert the result to a serializable format
        serializable_result = jsonable_encoder(result)
        return serializable_result

    def clr_history(self):
        self.chat_history = []

    # Test function to demonstrate JSON serialization
    def test_default_prompt(self):
        default_prompt = "Wie behandel ich einen Patienten mit Gastritis?"
        result = self.convchain(default_prompt)
        result_json = json.dumps(result, ensure_ascii=False, indent=4)
        print(result_json)

# If this file is run as a script, execute the test function
if __name__ == "__main__":
    cbfs_instance = cbfs()
    cbfs_instance.test_default_prompt()