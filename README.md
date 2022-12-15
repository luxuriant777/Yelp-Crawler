# Yelp-Crawler

This script can scrape information, related to different businesses, listed on Yelp website.

### Crawler accepts as an input:

1. Category name, ie - contractors
2. Location, ie - San Francisco, CA

It returns a file with json objects, each json representing a business from the
given search results.

## Each business has the following data:

- Business name
- Business rating
- Number of reviews
- Business yelp url
- Business website
- List of first 5 reviews, for each review:
    * Reviewer name
    * Reviewer location
    * Review date

### Installation
```shell
Get API key on this page https://fusion.yelp.com/
Create .env file in project's directory and put there your API_KEY in next format:
API_KEY=<YOUR_API_KEY>
python -m venv venv
source venv/bin/activate (Linux and macOS) or venv\Scripts\activate (Windows)
pip install -r requirements.txt
run main.py
```

### Please pay attention

The script can be run without a proxy, but sometimes it does not parse all the necessary information due to blocking.
Currently it uses free proxy package, so it may work slowly. If you have access to premium proxies, you can significantly increase the speed of parsing.
