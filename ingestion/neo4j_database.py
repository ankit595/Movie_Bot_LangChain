from py2neo import Graph, Node, Relationship
import pandas as pd

def create_movie_graph():
    try:
        # Connect to Neo4j
        graph = Graph("url", auth=("username", "password"))  # user, password

        # Load CSV
        df = pd.read_csv('../data/movies.csv')

        for _, row in df.iterrows():
            # Create Movie node
            movie = Node("Movie",
                         title=row['Series_Title'],
                         year=int(row['Released_Year']),
                         runtime=str(row['Runtime']),
                         imdb_rating=float(row['IMDB_Rating']),
                         overview=row['Overview'],
                         meta_score=int(row['Meta_score']) if not pd.isnull(row['Meta_score']) else None,
                         no_of_votes=int(row['No_of_Votes']) if not pd.isnull(row['No_of_Votes']) else None,
                         gross=row['Gross'] if not pd.isnull(row['Gross']) else None
                         )
            graph.merge(movie, "Movie", "title")
            print(f"Created/merged movie: {row['Series_Title']}")

            # Director
            director = Node("Director", name=row['Director'])
            graph.merge(director, "Director", "name")
            graph.merge(Relationship(movie, "DIRECTED_BY", director))
            print(f"Created/merged director relationship: {row['Director']} -> {row['Series_Title']}")

            # Certificate
            if pd.notnull(row['Certificate']):
                certificate = Node("Certificate", name=row['Certificate'])
                graph.merge(certificate, "Certificate", "name")
                graph.merge(Relationship(movie, "HAS_CERTIFICATE", certificate))
                print(f"Created/merged certificate relationship: {row['Certificate']} -> {row['Series_Title']}")

            # Genres (split by comma)
            if pd.notnull(row['Genre']):
                genres = [g.strip() for g in row['Genre'].split(',')]
                for g in genres:
                    genre = Node("Genre", name=g)
                    graph.merge(genre, "Genre", "name")
                    graph.merge(Relationship(movie, "HAS_GENRE", genre))
                    print(f"Created/merged genre relationship: {g} -> {row['Series_Title']}")

            # Actors
            for star_col in ['Star1', 'Star2', 'Star3', 'Star4']:
                if pd.notnull(row[star_col]):
                    actor = Node("Actor", name=row[star_col])
                    graph.merge(actor, "Actor", "name")
                    graph.merge(Relationship(movie, "STARS", actor))
                    print(f"Created/merged actor relationship: {row[star_col]} -> {row['Series_Title']}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_movie_graph()
