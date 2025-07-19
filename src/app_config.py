# src/app_config.py
config = {
    "openai_api_key": "sk_907dda2a5ae5653c63278c4418d845c91e4cedf171772f78d906cfad2e2f4db4",
     "sqlite_path": "os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'movies.sqlite'))",
    "neo4j_uri": "neo4j://localhost:7687",
    "neo4j_username": "neo4j",
    "neo4j_password": "projectdatabase",  # Replace with your actual password
}