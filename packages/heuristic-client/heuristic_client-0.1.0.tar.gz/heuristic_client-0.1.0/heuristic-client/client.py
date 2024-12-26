import requests

class HeuristicSearch:
    """
    A client to interact with the search API.
    """

    BASE_URL = "http://34.47.147.97:3000/search"

    def __init__(self, api_key):
        """
        Initialize the client with an API key.

        :param api_key: API key for authorization.
        """
        self.api_key = api_key

    def search(self, query, num_results=10, date_range=None, engine=None):
        """
        Perform a search query.

        :param query: Search query string.
        :param num_results: Number of results to return (default: 10).
        :param date_range: Optional date range filter ('day', 'week', 'month', 'year').
        :param engine: Optional list of search engines to use.
        :return: List of search results.
        """
        params = {
            "query": query,
            "num_results": num_results,
            "api_key": self.api_key,
        }
        if date_range:
            params["date_range"] = date_range
        if engine:
            params["engine"] = engine

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()["results"]
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch search results: {e}")
