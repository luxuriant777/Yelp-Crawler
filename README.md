![Screenshot_1](https://user-images.githubusercontent.com/20545475/207770520-b1262a99-182c-4ae0-b83e-35fb8c1f3eba.png)
![Screenshot_2](https://user-images.githubusercontent.com/20545475/207770523-61ed3608-4c1a-4c44-9433-f30e711b3f1f.png)
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
1. Get API key on this page https://fusion.yelp.com/
2. Create .env file in project directory and put there your API_KEY in next format:
API_KEY=YOUR_API_KEY
3. python -m venv venv
4. source venv/bin/activate (Linux and macOS) or venv\Scripts\activate (Windows)
5. pip install -r requirements.txt
6. run main.py
```

### Please pay attention

The script can work without a proxy, but sometimes it does not parse all the necessary information due to blocking.
If you have access to premium proxies, you can increase the quality of parsing.
