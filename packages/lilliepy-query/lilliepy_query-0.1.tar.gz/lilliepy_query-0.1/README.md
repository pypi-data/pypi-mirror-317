# Lilliepy-query

this is a sub module for the lilliepy framework to be able to query and cache queries effectivly

## dependecies

* request
* time
* threading
* reactpy
* asyncio

## how to use

### Import: 

step 1:
```bash
pip install lilliepy-query
```

step 2:
```python
from lilliepy-query import Fetcher, use_query
```

### Syntax for Fetcher:
this is for the people who want to use a class, rather than a function hook

you will be using these 4 lines of code the most:

```python
from lilliepy import Fetcher

req = query.Fetcher("https://jsonplaceholder.typicode.com", refetch_interval=2) # initilizes the Fetcher class, you will now be able to start fetching and caching data, params are listed in the class comment docs
req.fetch("/todos/3") # fetches the data, since the base url is "https://jsonplaceholder.typicode.com", it will fetch from "https://jsonplaceholder.typicode.com/todos/3"
req.refetch("/todos/3") # refetches every interval stated by the Fetcher init, in this case, 2

data, err, load = req.get_state() # 3 vars are declared here: data, for the data from the fetch; error, for containing any error from preforming the fetch; and load, to indicate if the fetch is still loading or not
```

### Syntax for use_query:
this is for the people who want to have a function hook

```python
# MainPage.x.py
# the title of the page that was specified above is the file arrangement so that lilliepy-dir-router can route it correctly

from reactpy import component, html
from lilliepy-query import use_query
import httpx # if you want to use this

async def fetch_example_data(): # fetching function (pro tip: you can use the Fetcher for this part!!!)
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        response.raise_for_status()
        return response.json()


@component
def MainPage():
    query = use_query(
        query_key="example-data", # query key
        fetch_function=fetch_example_data, # query function
        enabled=True, #should it execute on mount, in this case, yes
        refetch_interval=30  # Refetch every 30 seconds
    )

    if query["is_loading"]: # if query is loading
        return html.div("Loading...")

    if query["error"]: #if query had an error
        return html.div(f"Error: {query['error']}")

    if query["data"]: #when query gets data
        return html.div(f"Data: {query['data']}")

    return html.div("No data available.") #nothing came out (shouldnt happen)
```