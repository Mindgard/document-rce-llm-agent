import os
from langchain.agents import Tool
from langchain_community.document_loaders import Docx2txtLoader
from langchain_experimental.utilities import PythonREPL
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
import gradio as gr
 

def create_agent(file_path):
    # Get prompt template from hub
    prompt = hub.pull("hwchase17/openai-functions-agent")

    # Create OpenAI model
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # Create tool to run Python code
    python_repl = PythonREPL()
    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    )

    # Create tool to load documents and create a vector store to search
    loader = Docx2txtLoader(file_path)

    docs = loader.load()

    documents = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    ).split_documents(docs)

    vector = FAISS.from_documents(documents, OpenAIEmbeddings())

    retriever = vector.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "word_document_serach",
        "Search for a word in a document.",
    )

    # Collect tools
    tools = [retriever_tool, repl_tool]

    # Create agent
    agent = create_openai_functions_agent(llm, tools, prompt)

    return AgentExecutor(agent=agent, tools=tools, verbose=True)


def predict(message, history, file):
    # Create agent
    agent = create_agent(file)

    # Invoke agent
    response = agent.invoke({"input": message})

    # Return response
    return response['output']


def run():
    # Create and launch the chat interface
    gr.ChatInterface(
        predict,
        theme="base",
        title="Internal LLM Agent",
        chatbot=gr.Chatbot(height=600),
        textbox=gr.Textbox(placeholder="Ask me a question", container=False, scale=7, lines=5),
        retry_btn=None,
        undo_btn=None,
        clear_btn=None,
        additional_inputs=[
            gr.UploadButton()
        ]
    ).launch(server_port=8999, server_name="localhost")

    
if __name__ == "__main__":
    # Set OpenAI API key
    os.environ['OPENAI_API_KEY'] = "" # Replace with your OpenAI API key

    run()
