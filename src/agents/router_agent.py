# src/agents/router_agent.py
import ssl
import httpx
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.graphs import Neo4jGraph

def get_sqlite_schema(sqlite_path):
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_info = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema_info[table_name] = [column[1] for column in columns]

    conn.close()
    return schema_info


def get_neo4j_schema(uri, username, password):
    graph = Neo4jGraph(
        url=uri,
        username=username,
        password=password,
    )
    schema_query = """
    CALL db.schema.visualization() YIELD nodes, relationships
    RETURN nodes, relationships
    """
    schema_result = graph.query(schema_query)

    nodes = [node['name'] for node in schema_result[0]['nodes']]
    relationships = [rel[1] for rel in schema_result[0]['relationships']]

    return nodes, relationships


def route_question(question, config):
    sqlite_schema = get_sqlite_schema(config["sqlite_path"])
    neo4j_nodes, neo4j_relationships = get_neo4j_schema(
        config["neo4j_uri"],
        config["neo4j_username"],
        config["neo4j_password"]
    )

    # Create an instance of httpx.Client with SSL verification disabled
    http_client = httpx.Client(verify=False)

    # Simple router using LLM classification; can later be replaced by a more advanced approach
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    prompt = f"""Classify this question as ['neo4j', 'sqlite', 'both'] based on the following schema information and whether it requires relationship/graph data, direct table lookup, or both:
    SQLite Schema: {sqlite_schema}
    Neo4j Nodes: {neo4j_nodes}
    Neo4j Relationships: {neo4j_relationships}
    Question: '{question}'
    Output ONLY one of: neo4j, sqlite, both.
    """
    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    route = response.content.strip().lower()

    if route in ["neo4j", "sqlite", "both"]:
        return route
    else:
        return "unknown"
