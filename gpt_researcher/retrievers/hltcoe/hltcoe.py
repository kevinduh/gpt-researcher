from typing import Any, Dict, List, Optional
import requests
import os
import json
import ir_datasets as irds



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
            print(f'curl "{self.endpoint}/query_passage?query={self.query}&content=true&limit={max_results}"')

            response = requests.get(f"{self.endpoint}/query_passage?",
                                    params={**self.params, 'query': self.query, 'content': 'true', 'limit': max_results})

            # print("-----")
            # print(response.request.method)
            # print(response.request.url)
            # print(response.request.headers)
            # print(response.request.body)
            # print("-----")
            
            response.raise_for_status()

            results = response.json().get("results", [])
            search_result = []

            # TODO: Need to include title and standardize how search content is passed
            for result in results:
                search_result.append(
                    {
                        "title": None,
                        "href": str(result["pid"]),
                        "body": result["content"],
                    }
                )

            return search_result

        except requests.RequestException as e:
            print(f"Failed to retrieve search results: {e}")
            return []



if __name__ == "__main__":
    query = "what is the best car"
    retriever = HLTCOE(query)
    results = retriever.search(query, "neuclir/1/zh", 10)
    print(results)
