import httpx
from langchain.schema import HumanMessage
from langchain_neo4j import Neo4jGraph
from langchain_openai import ChatOpenAI


def get_neo4j_agent(openai_api_key, uri, username, password):
    graph = Neo4jGraph(
        url=uri,
        username=username,
        password=password
    )

    http_client = httpx.Client(verify=False)
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_base="https://llm-proxy-api.ai.eng.netapp.com",
        openai_api_key=openai_api_key,
        model_kwargs={'user': "ak16683"},
        http_client=http_client
    )

    def retrieve(question):
        # Step 1: Get node labels
        label_result = graph.query("CALL db.labels()")
        node_labels = [row['label'] for row in label_result]

        # Step 2: Get relationships with direction
        relationships_query = """
        MATCH (start)-[r]->(end)
        RETURN DISTINCT type(r) AS relationship_type, start AS start_node, end AS end_node
        LIMIT 100
        """
        relationships_result = graph.query(relationships_query)
        # print("Relationship Result:", relationships_result)

        def infer_label(node):
            if 'title' in node:
                return 'Movie'
            elif 'name' in node:
                # You can refine this further if needed
                return 'Actor'  # or Director, Genre, Certificate
            else:
                return 'Unknown'

        relationships = []
        for rel in relationships_result:
            start_label = infer_label(rel['start_node'])
            end_label = infer_label(rel['end_node'])
            rel_type = rel['relationship_type']
            relationships.append(f"(:{start_label})-[:{rel_type}]->(:{end_label})")

        # Step 3: Get property keys for each node label
        property_keys = {}
        for label in node_labels:
            try:
                result = graph.query(f"MATCH (n:{label}) RETURN keys(n) AS props LIMIT 1")
                property_keys[label] = result[0]['props'] if result else []
            except Exception:
                property_keys[label] = []

        # Step 4: Format schema for LLM
        schema_info = f"Nodes: {', '.join(node_labels)}\n"
        schema_info += "Relationships:\n" + "\n".join(relationships) + "\n"
        schema_info += "Properties:\n"
        for label, props in property_keys.items():
            schema_info += f"{label}: {', '.join(props)}\n"

        # Step 5: Prompt the LLM
        prompt = f"""
You are a Cypher expert. Based on the following Neo4j schema, generate ONLY the Cypher query to answer the question.

Schema:
{schema_info}

Question: {question}

Only return the Cypher query. Do not include any explanation or formatting.
"""

        message = HumanMessage(content=prompt)
        response = llm.invoke([message])
        cypher_query = response.content.strip()

        if "```cypher" in cypher_query:
            cypher_query = cypher_query.split("```cypher")[1].split("```")[0].strip()

        print(f"Generated Cypher Query:\n{cypher_query}")

        # Step 6: Execute the query
        result = graph.query(cypher_query)

        print(f"Query Result:\n{result}")
        if not result:
            result = "Unable to determine"
            print(result)
        return result

    return retrieve

    # Example usage


# openai_api_key = "sk_986e96a6aa3c463da735f7e1cefc345a8e3f33f0fa2c33a00e4b879c9b7a6f44"  # Use environment variable for safety
# uri = "neo4j://localhost:7687"
# username = "neo4j"
# password = "projectdatabase"
#
# get_neo4j_agent(openai_api_key, uri, username, password)("scifi movies with high ratings")
