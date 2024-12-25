import requests
import time
import threading

class Fetcher:
    def __init__(self, base_url=None, cache_size=10, refetch_interval=None, retry_attempts=3, headers=None):
        """
        Initialize the Fetcher instance with optional configurations.
        
        :param base_url: Optional base URL for API requests.
        :param cache_size: Number of cached results.
        :param refetch_interval: Interval in seconds for automatic refetch.
        :param retry_attempts: Number of retry attempts on failure.
        :param headers: Optional custom headers (e.g., for authentication).
        """
        self.base_url = base_url
        self.cache_size = cache_size
        self.refetch_interval = refetch_interval
        self.retry_attempts = retry_attempts
        self.headers = headers if headers else {}  # Use empty dict if no headers provided
        self._cache = {}
        self._state = {
            "loading": False,
            "error": None,
            "data": None
        }

    def _make_request(self, url, retries=0):
        """Private method to make an HTTP request with retry logic."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            if retries < self.retry_attempts:
                print(f"Retrying request... ({retries+1}/{self.retry_attempts})")
                return self._make_request(url, retries + 1)
            else:
                raise e

    def fetch(self, endpoint, params=None):
        """Fetch data from the API and return the result."""
        # Update state: set loading to True when fetching
        self._set_state(loading=True)

        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        if params:
            url += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
        
        # Check cache first
        if url in self._cache:
            print("Using cached data for", url)
            self._set_state(data=self._cache[url])  # Set the cached data in state
            return self._cache[url]

        try:
            # Fetch data if not cached
            print("Fetching data from", url)
            data = self._make_request(url)
            
            # Cache the result
            if len(self._cache) >= self.cache_size:
                self._cache.pop(next(iter(self._cache)))  # Pop the oldest cached entry
            self._cache[url] = data
            
            # Update state with fetched data
            self._set_state(data=data)

            return data
        except Exception as e:
            # If an error occurs, update the state with the error
            self._set_state(error=str(e))
            raise e

    def refetch(self, endpoint, params=None):
        """Refetch the data in the background at a set interval."""
        def refetch_data():
            while True:
                print(f"Refetching data for {endpoint}")
                self.fetch(endpoint, params)
                time.sleep(self.refetch_interval)

        if self.refetch_interval:
            thread = threading.Thread(target=refetch_data, daemon=True)
            thread.start()

    def clear_cache(self):
        """Clear the cache."""
        self._cache.clear()

    def _set_state(self, loading=False, error=None, data=None):
        """Update the state with new values."""
        if loading is not None:
            self._state['loading'] = loading
        if error is not None:
            self._state['error'] = error
        if data is not None:
            self._state['data'] = data

    def get_state(self, at_once = False):
        """Return the current state."""
        if not at_once:
            return self._state["data"], self._state["error"], self._state["loading"]
        else:
            return self._state