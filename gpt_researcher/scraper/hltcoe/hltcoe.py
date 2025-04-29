import os
import ir_datasets as irds
import requests


def get_text_from_id(docid, collection):
    d = irds.load(collection).docs.lookup(docid)
    return d.title, d.text

class HLTCOEScraper:

    def __init__(self, link, session=None):
        self.link = link
        self.session = session
        self.endpoint = os.getenv('SCRAPTER_ENDPOINT')
        self.endpoint_collection = os.getenv('RETRIEVER_ENDPOINT_COLLECTION')

    def scrape(self) -> tuple:
        """
        This function extracts content 

        Returns:
          The `scrape` method returns a tuple containing the extracted content, a list of image URLs, and
        the title of the webpage specified by the `self.link` attribute. 
        """

        try:

            response = requests.get(f"{self.endpoint}/get_passage/{self.link}")
            response.raise_for_status()

            content = response.json().get("content", "")
            docid = response.json().get("doc_id", "")
            # TODO: returning docid for title here. may need to change for other applications
            return content, [], docid

        except Exception as e:
            print("Error! : " + str(e))
            return "", [], ""

    # TODO: Need to standardize how search content is passed. This function below is the old version.        
    def scrape2(self) -> tuple:
        """
        This function extracts content 

        Returns:
          The `scrape` method returns a tuple containing the extracted content, a list of image URLs, and
        the title of the webpage specified by the `self.link` attribute. 
        """

        try:

            title, content = get_text_from_id(self.link, self.endpoint_collection)
            return content, [], title

        except Exception as e:
            print("Error! : " + str(e))
            return "", [], ""