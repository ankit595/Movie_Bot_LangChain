# src/orchestrator.py
import sys, os

import httpx
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agents.sqlite_agent import get_sqlite_agent
from agents.neo4j_agent import get_neo4j_agent
from agents.router_agent import route_question
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def format_response(response, openai_api_key):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_base="https://llm-proxy-api.ai.eng.netapp.com",
        openai_api_key=openai_api_key,
        model_kwargs={'user': "ak16683"},
        http_client=httpx.Client(verify=False)
    )

    prompt = f"Format the following response in a clean, plain text manner suitable for display in a UI and describe everything a little as per the answer don't mention that you are formatting this. Ensure the output is simple and readable:\n{response}"
    message = HumanMessage(content=prompt)
    formatted_response = llm.invoke([message]).content.strip()
    print(f"Formatted response: {formatted_response}")
    return formatted_response

def web_search(question, openai_api_key):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_base="https://llm-proxy-api.ai.eng.netapp.com",
        openai_api_key=openai_api_key,
        model_kwargs={'user': "ak16683"},
        http_client=httpx.Client(verify=False)
    )

    prompt = f"You are a movie expert so answer the question :\n{question}"
    message = HumanMessage(content=prompt)
    response = llm.invoke([message]).content.strip()
    print(f"Formatted response: {response}")
    return response

def answer_question(question, config, swarm_memory):
    route = route_question(question, config)
    sqlite_agent = get_sqlite_agent(config["openai_api_key"], config["sqlite_path"])
    neo4j_agent = get_neo4j_agent(
        config["openai_api_key"],
        config["neo4j_uri"],
        config["neo4j_username"],
        config["neo4j_password"]
    )
    swarm_memory.log_route(question, route)

    if route == "sqlite":
        response = sqlite_agent.invoke(question)
    elif route == "neo4j":
        response = neo4j_agent(question)
    elif route == "both":
        neo4j_results = neo4j_agent(question)
        sqlite_results = sqlite_agent.invoke(question)
        response = f"{neo4j_results}\n{sqlite_results}"
    # else:
    #     response = "Unable to determine the right database for this question."
    if not response or "Unable to determine" in response:
        # Fallback to DuckDuckGo search
        # search = DuckDuckGoSearchResults(output_format="list",max_results=1)
        # search_results = search.invoke(question)
        # print(search_results)
        # response = [result['snippet'] for result in search_results]
        # print(response)
        response = web_search(question, config["openai_api_key"])
        print(response)

        # response = search_results.get("snippet", "Unable to find relevant information.")

    # if not response or "Unable to determine" in response:
    #     # Fallback to DuckDuckGo search
    #     response = search_duckduckgo(question)

        # Format the response using LLM
    formatted_response = format_response(response, config["openai_api_key"])
    return formatted_response


# config = {
#     "openai_api_key": "sk_986e96a6aa3c463da735f7e1cefc345a8e3f33f0fa2c33a00e4b879c9b7a6f44",
#      "sqlite_path": "os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'movies.sqlite'))",
#     "neo4j_uri": "neo4j://localhost:7687",
#     "neo4j_username": "neo4j",
#     "neo4j_password": "projectdatabase",
# }
#
# def init_system():
#     # Initialize and return the swarm memory or any other system setup required
#     return {}
#
#
# # ui/app.py
# import os
# from langchain_setup import init_system
# from orchestrator import answer_question
#
#
# def main():
#     swarm_memory = init_system()
#     question = "What are recent drama movies in 2023?"
#     answer = answer_question(question, config, swarm_memory)
#
#     print("### Specific Question")
#     print(f"You: {question}")
#     print(f"Bot: {answer}")
#
#
# if __name__ == "__main__":
#     main()