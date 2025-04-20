from typing import Any, Dict, List, Optional
import requests
import os
import json
from urllib.parse import quote
import urllib.parse
import ir_datasets as irds


_colbert_server = {
    #'neuclir/1/zh': 'r4n20:9090',
    'neuclir/1/zh': 'r8n01:9090',
    'neuclir/1/fa': 'r8n10:9191',
    'neuclir/1/ru': 'r7n10:9292',
    #'neuclir/1/zho': 'r4n20:9090',
    'neuclir/1/zho': 'r8n01:9090',
    'neuclir/1/fas': 'r8n10:9191',
    'neuclir/1/rus': 'r7n10:9292'
}
_collection_name_mapping = {
    'neuclir/1/zh': 'neuclir/1/zh',
    'neuclir/1/fa': 'neuclir/1/fa',
    'neuclir/1/ru': 'neuclir/1/ru',
    'neuclir/1/zho': 'neuclir/1/zh',
    'neuclir/1/fas': 'neuclir/1/fa',
    'neuclir/1/rus': 'neuclir/1/ru',
    'neuclir/1/zh': 'neuclir/1/zh',

}

def get_text_from_id(docid, collection):
    global _collection_name_mapping
    d = irds.load(_collection_name_mapping[collection]).docs.lookup(docid)
    return d.title, d.text


class HLTCOESearch():
    """
    HLTCOE Search Retriever
    """

    def __init__(self, query: str, query_domains=None):
        self.endpoint = os.getenv('RETRIEVER_ENDPOINT')
        self.endpoint_collection = os.getenv('RETRIEVER_ENDPOINT_COLLECTION')

        if not self.endpoint:
            raise ValueError("RETRIEVER_ENDPOINT environment variable not set")

        self.params = self._populate_params()
        self.query = query

    def _populate_params(self) -> Dict[str, Any]:
        """
        Populates parameters from environment variables prefixed with 'RETRIEVER_ARG_'
        """
        return {
            key[len('RETRIEVER_ARG_'):].lower(): value
            for key, value in os.environ.items()
            if key.startswith('RETRIEVER_ARG_')
        }

    def search(self, max_results: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Performs the search using the custom retriever endpoint.

        :param max_results: Maximum number of results to return (not currently used)
        :return: JSON response in the format:
            [
              {
                "url": "http://example.com/page1",
                "raw_content": "Content of page 1"
              },
              {
                "url": "http://example.com/page2",
                "raw_content": "Content of page 2"
              }
            ]
        """
        try:
            print(self.query, self.params)
            print(f'curl "{self.endpoint}/query_doc?query={self.query}&content=false&limit={max_results}"')

            response = requests.get(f"{self.endpoint}/query_doc?",
                                    params={**self.params, 'query': self.query, 'content': 'false', 'limit':{max_results}})

            #print("-----")
            #print(response.request.method)
            #print(response.request.url)
            #print(response.request.headers)
            #print(response.request.body)
            #print("-----")
            
            response.raise_for_status()

            results = response.json().get("results", [])
            search_result = []

            for result in results:
                title, content = get_text_from_id(result["doc_id"], self.endpoint_collection)
                search_result.append(
                    {
                        "title": title,
                        "href": result["doc_id"],
                        "body": content,
                    }
                )

            return search_result


            return response.json()
        except requests.RequestException as e:
            print(f"Failed to retrieve search results: {e}")
            return None
        

class HLTCOESearch2():
    """
    HLTCOE Search Retriever
    """
    def __init__(self, query):
        """
        Initializes the object
        Args:
            query:
        """
        self.query = query
   

    def search(self, query: str, collection: str, max_results: int=10):
        global _colbert_server
        global _collection_name_mapping
        query = urllib.parse.quote(query)

        print(f'calling HLTCOE search: http://{_colbert_server[collection]}/query_doc?query={query}&content=false&limit={max_results} / {collection}')
        resp = requests.get(f'http://{_colbert_server[collection]}/query_doc?query={query}&content=false&limit={max_results}')
        # Preprocess the results
        if resp is None:
            return
        try:
            search_results = json.loads(resp.text)
        except Exception:
            return
        if search_results is None:
            return

        # need to save title, href, body
        return_results = []
        # print(f"Search results: {search_results['results']}")
        for result in search_results["results"]:
            title, content = get_text_from_id(result["doc_id"], collection)
            return_results.append({"title": title, "url": result["doc_id"], "raw_content": content})
        return return_results




if __name__ == "__main__":
    query = "what is the best car"
    retriever = HLTCOE(query)
    results = retriever.search(query, "neuclir/1/zh", 10)
    print(results)
