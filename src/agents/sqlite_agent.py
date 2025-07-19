import ssl, httpx, os
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase  # Updated import
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent


def get_sqlite_agent(openai_api_key, db_path):
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_base="https://llm-proxy-api.ai.eng.netapp.com",
        openai_api_key=openai_api_key,
        model_kwargs={'user': "ak16683"},
        http_client=httpx.Client(verify=False)
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(llm=llm, toolkit=toolkit)
    return agent


# # Verification code
# if __name__ == "__main__":
#     # Configuration
#     config = {
#         "openai_api_key": "sk_986e96a6aa3c463da735f7e1cefc345a8e3f33f0fa2c33a00e4b879c9b7a6f44",  # Load from environment variable
#          "sqlite_path": os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'movies.sqlite'))  # Correct path to your SQLite database
#     }
#
#     openai_api_key = config["openai_api_key"]
#     db_path = config["sqlite_path"]
#
#     # Ensure the database file exists
#     if not os.path.exists(db_path):
#         print(f"Error: The database file at {db_path} does not exist.")
#         exit(1)
#
#     # Initialize the SQLite agent
#     sqlite_agent = get_sqlite_agent(openai_api_key, db_path)
#
#     # Define a sample question
#     question = "Movies with the highest ratings in the year 2010."
#
#     # Run the sample query
#     response = sqlite_agent.invoke(question)
#     print(f"Question: {question}")
#     print(f"Response: {response}")
