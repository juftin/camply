# Dependencies

`camply` is compatible with any Python version >= `3.8`. Here are the current dependencies:

-   [click](https://docs.python-requests.org/en/master/)
    -   The `click` package is used to leverage it's simple Command Line Interface
        API for camply
-   [requests](https://docs.python-requests.org/en/master/)
    -   The `requests` package is used to fetch data from the APIs of Camping Booking Providers.
-   [pandas](https://pandas.pydata.org/)
    -   The `pandas` package is to group and aggregate across large data sets of campsites,
        campgrounds, and recreation areas.
-   [tenacity](https://tenacity.readthedocs.io/en/latest/)
    -   The `tenacity` package is used for retrying data searches on the underlying campsite APIs.
        This retrying methodology handles exceptions allowing for API downtime and facilitating
        exponential backoff.
-   [rich](https://github.com/textualize/rich)
    -   Colorizing the CLI (also using [rich-click](https://github.com/ewels/rich-click) to
        colorize `click`)
-   [python-dotenv](https://github.com/theskumar/python-dotenv)
    -   The `python-dotenv` package reads key-value pairs from a `.env` file and can set them as
        environment variables - this helps with the `.camply` configuration file.
-   [pydantic](https://github.com/samuelcolvin/pydantic)
    -   The `pydantic` package performs data validation against API responses and assists with fancy
        data containers for `camply` objects.
-   [PyYAML](https://pyyaml.org/)
    -   PyYAML is a YAML parsing library - this helps with the YAML file campsite searches.
-   [ratelimit](https://github.com/tomasbasham/ratelimit)
    -   The `ratelimit` package is used for limiting the frequency of our API calls to external
        APIs so we can be good partners to our friends who run the campsite booking services.
-   [fake-useragent](https://github.com/fake-useragent/fake-useragent)
    -   `fake-useragent` makes it easy for us to mock the latest browsers when interacting with
        certain API providers.
