# Importing necessary modules and classes from the langchain package and others
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.elasticsearch import ElasticsearchStore
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
import param  # A library for defining parameters in classes
from dotenv import load_dotenv  # A utility to load environment variables from .env files
import os  # Standard library for interacting with the operating system
import openai  # OpenAI's Python client library
# import json

# Setting up environment variables
dotenv_path = 'KEYs.env'  # Defining the path to the .env file containing your environment variables
_ = load_dotenv(os.path.join(os.path.dirname(__file__), '../KEYs.env'))  # Loading the environment variables

# Setting API keys and Elasticsearch credentials from environment variables
openai.api_key = os.environ['OPENAI_API_KEY']
_es_cloud_id = os.environ['es_cloud_id']
_es_user = os.environ['es_user']
_es_password = os.environ['es_password']

# Initializing OpenAI embeddings for use in Elasticsearch
embedding = OpenAIEmbeddings()

# Setting up Elasticsearch vector search
elastic_vector_search = ElasticsearchStore(
    es_cloud_id=_es_cloud_id,
    index_name="leitliniengpt",
    embedding=embedding,
    es_user=_es_user,
    es_password=_es_password,
)

# A fallback message if no documents are found
No_Doc = "Die hinterlegten Leitlinien Dokumente enthalten keine Informationen zu Ihrer Frage."

# Defining a prompt template for use in the ConversationalRetrievalChain
template = """
Only base your response on the context. 
The answer should not exceed 8 sentences.
Memorize the language I ask you in my question.
context: {context}
question: {question}
Answer in the same language which I requested you to memorize.
:"""
# Format the output as a JSON with the following keys: 
#question:
#answer:
#source page:
#source Title of page:

prompt = PromptTemplate.from_template(template)  # Creating a PromptTemplate object from the defined template

# Function to initialize the ConversationalRetrievalChain model
def Init_model():
    qa = ConversationalRetrievalChain.from_llm(
        # The temperature=0 parameter implies deterministic, less-random responses.
        llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"),
        retriever=elastic_vector_search.as_retriever(search_kwargs={"k": 3}),
        # This defines the retriever to be used along with the language model. 
        # Here, it uses Elasticsearch as a retriever (set up earlier in your code), configured to return the top 3 ("k": 3) relevant documents for a given query.
        combine_docs_chain_kwargs={"prompt": prompt},
        response_if_no_docs_found=No_Doc,
        return_source_documents=True,
        chain_type='stuff'
    )
    return qa 


# Defining a class 'cbfs' with methods for model loading, query processing, and chat history management
class cbfs(param.Parameterized):
    chat_history = param.List([])  # Chat history as a list of tuples (query, response)
    count = param.List([])  # A list for keeping count, purpose not specified in the snippet

    def __init__(self, **params):
        super(cbfs, self).__init__(**params)
        self.qa = Init_model()  # Initializing the model on creation of an instance of cbfs

    # Method to load the model based on the specified database
    def load_model(self, Database):
        if Database == "Nur aktuell gültige Leitlinien":
            # Specific configuration for "Nur aktuell gültige Leitlinien"
            self.qa = ConversationalRetrievalChain.from_llm(...)
            self.count.append(1)
        else:
            # Default model initialization
            self.qa = Init_model()

    # Method to process a query and update chat history
    def convchain(self, query):
        result = self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        print("Received result:", result)

        return result



    # Method to clear the chat history
    def clr_history(self):
        self.chat_history = []  # Resetting chat history to an empty list