# Dependencies

`camply` is compatible with any Python version >= `3.6`. Currently, there are eight required
dependencies:

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
    -   Colorizing the CLI
-   [python-dotenv](https://github.com/theskumar/python-dotenv)
    -   The `python-dotenv` package reads key-value pairs from a `.env` file and can set them as
        environment variables - this helps with the `.camply` configuration file.
-   [pydantic](https://github.com/samuelcolvin/pydantic)
    -   The `pydantic` package performs data validation against API responses and assists with fancy
        data containers for `camply` objects.
-   [PyYAML](https://pyyaml.org/)
    -   PyYAML is a YAML parsing library - this helps with the YAML file campsite searches.
