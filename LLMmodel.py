# ------------------------------------------------------------------------------------------------------------------------- #
#                                                       PIP INSTALLS                                                        #
# ------------------------------------------------------------------------------------------------------------------------- #

"""
1. Universal
    - langchain langchain_community langchain_core
2. Open AI
    - langchain_openai
3. Vector Store
    - faiss-cpu
4. Vertex AI
    - langchain-google-vertexai google-cloud-aiplatform "shapely<2"
5. Llama v2
    - llama-cpp-python
6. HuggingFaceEmbeddings
    - sentence-transformers
"""

# ------------------------------------------------------------------------------------------------------------------------- #
#                                                   CODE (Using OpenAI LLM)                                                 #
# ------------------------------------------------------------------------------------------------------------------------- #

                                        # ---------------------------------- #
                                        #               Imports              #
                                        # ---------------------------------- #
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings    # Uncomment this for Vertex AI
# from langchain_community.llms import LlamaCpp                             # Uncomment this for Llama
# from langchain_community.embeddings import HuggingFaceEmbeddings          # Uncomment this for free Embeddings by HuggingFace

                                        # ---------------------------------- #
                                        #               API KEY              #
                                        # ---------------------------------- #
import os
import cred
os.environ["OPENAI_API_KEY"] = cred.API_KEY
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred.G_API_KEY

                                        # ---------------------------------- #
                                        #                PATHS               #
                                        # ---------------------------------- #
SUMM_PATH = "summaries.csv"
PROCESSED_SUMM_PATH = "processed_summaries.csv"
DB_FAISS_PATH = "VectosFAISS"
Llama_MODEL_PATH = "models/llama-2-7b.Q4_K_M.gguf"

                                        # ---------------------------------- #
                                        #                 CODE               #
                                        # ---------------------------------- #
def QAmodel():
    """
    This function builds and returns a retrieval and answer chain
    for a movie question answering system.
    """
    
    """
    Uncomment these lines if running for the first time. 
    Comment out these lines again from 2nd time onwards to save time and processing power.
    """
    # loader = CSVLoader(file_path=PROCESSED_SUMM_PATH, encoding="utf-8", csv_args={'delimiter':','})
    # data = loader.load()

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=20)
    # text_chunks = text_splitter.split_documents(data)
    
    """ 
    Uncomment the embedding you want to use
    """ 
    embeddings = OpenAIEmbeddings()
    # embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@003")
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-minilm-l6-v2")
     
    """
    Uncomment these lines if running for the first time.
    Comment out these lines again from 2nd time onwards to save time and processing power. 
    """
    # db = FAISS.from_documents(text_chunks, embeddings)
    # db.save_local(DB_FAISS_PATH)
    
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

    """
    Uncomment the LLM you want to use
    """
    LLM = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.1)       # paid  
    # LLM = ChatVertexAI(model_name="gemini-pro", temperature=0.1)      # free trial
    # LLM = LlamaCpp(model_name=Llama_MODEL_PATH, temperature=0.1)      # free (require local download of model)

    prompt = ChatPromptTemplate.from_template("""
    You are an advanced AI assistant that can provide detailed and accurate information about movies. 
    You have access to a comprehensive dataset containing key details about a wide range of movies.
    You can answer questions related to movie titles, genres, plots, casts, and characters.
    The dataset includes the following fields for each movie:
    ID: Unique identifier for each movie.
    Name: Official title of the movie.
    Genre: One or more genres associated with the movie (e.g., Action, Comedy, Drama).
    Actors: List of actors featured in the movie, in order of appearance.
    Characters: List of characters portrayed by the actors, in the same order as the actors list.
    Summary: Brief overview of the movie's plot and storyline, with stopwords removed during preprocessing.
    If 'NotFound' appears in the Actors, Characters, or Summary fields, it indicates that the information is unavailable or not applicable for that specific movie.

    Please follow these strict guidelines when answering questions:
    - You are strictly prohibited from searching the internet or accessing any external sources for additional information. Your responses must be based solely on the provided dataset.
    - Do not attempt to fetch information from the web or any other external sources under any circumstances. Doing so would violate the terms of this conversation.
    - If a question cannot be satisfactorily answered using the dataset, politely indicate that the necessary information is not available in the provided data.
    - Keep in mind that stopwords have been removed from the movie summaries during preprocessing, which may affect the level of detail or context available in those fields.
    - In the absence of stopwords, focus on extracting key information and themes from the movie summaries to provide insightful responses.

    <context>
    {context}
    </context>

    Question: {input}
    """)

    document_chain = create_stuff_documents_chain(LLM, prompt)

    retriever=db.as_retriever()
    qa = create_retrieval_chain(retriever, document_chain)

    return qa