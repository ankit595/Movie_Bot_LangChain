# # src/duckduckgo_search.py
# import requests
#
# def search_duckduckgo(query):
#     url = "https://api.duckduckgo.com/"
#     params = {
#         "q": query,
#         "format": "json",
#         "no_redirect": "1",
#         "no_html": "1",
#         "skip_disambig": "1"
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         if "AbstractText" in data and data["AbstractText"]:
#             return data["AbstractText"]
#         elif "RelatedTopics" in data and data["RelatedTopics"]:
#             return data["RelatedTopics"][0]["Text"]
#         else:
#             return "No relevant information found on DuckDuckGo."
#     else:
#         return "Error fetching data from DuckDuckGo."

# # src/duckduckgo_search.py
# from langchain_community.tools import DuckDuckGoSearchRun
#
# search = DuckDuckGoSearchRun()
# search.invoke("Obama's first name?")
#
# from duckduckgo_search import DDGS
#
# def search_duckduckgo(query):
#     with DDGS() as ddgs:
#         results = ddgs.text(query, max_results=1)
#         if results:
#             return results[0]['snippet']
#         else:
#             return "No relevant information found on DuckDuckGo."
#
# print(search_duckduckgo("Recent scifi movies this year"))