import requests
import asyncio
import aiohttp as aiohttp
import json
import os

from dataclasses import dataclass
from bs4 import BeautifulSoup
from urllib.parse import unquote
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.environ.get("API_KEY")

HEADERS = {"accept": "application/json", "Authorization": f"Bearer {API_KEY}"}

REVIEWER_NAME_SELECTOR = "user-passport-info border-color--default__09f24__NPAKY"
REVIEWER_LOCATION_SELECTOR = (
    "responsive-hidden-small__09f24__qQFtj border-color--default__09f24__NPAKY"
)
DATE_SELECTOR = "margin-t1__09f24__w96jn margin-b1-5__09f24__NHcQi border-color--default__09f24__NPAKY"


@dataclass
class ReviewDetails:
    reviewer_name: str
    reviewer_location: str
    review_date: str

    def __iter__(self) -> iter:
        return iter(
            (
                "reviewer_name: " + self.reviewer_name,
                "reviewer_location: " + self.reviewer_location,
                "review_date: " + self.review_date,
            )
        )


@dataclass
class Business:
    business_name: str
    business_rating: float
    number_of_reviews: int
    business_yelp_url: str
    business_website: str | None
    list_of_reviews: list[ReviewDetails]


def endpoint_creator(location: str, categories: list[str]) -> str:
    return f"https://api.yelp.com/v3/businesses/search?location={location}&categories={categories}&limit=50"


def url_with_offset(url: str, offset: int) -> str:
    return f"{url}&offset={offset}"


def get_businesses_by_api(url: str, headers: dict) -> list[Business]:
    offset = 0
    list_of_businesses = []

    # 20 is a maximum number of pages that API returns
    for i in range(0, 1):
        response = requests.get(url_with_offset(url, offset), headers=headers)
        list_of_businesses.extend(dict(response.json())["businesses"])
        offset += 50

    list_of_business_objects = []

    for business in list_of_businesses:
        business_name = business["name"]
        business_rating = business["rating"]
        number_of_reviews = business["review_count"]
        business_yelp_url = business["url"].split("?")[0].split("&")[0]
        business_website = None
        list_of_reviews = []

        list_of_business_objects.append(
            Business(
                business_name,
                business_rating,
                number_of_reviews,
                business_yelp_url,
                business_website,
                list_of_reviews,
            )
        )

    return list_of_business_objects


async def scrape_details_of_business(business: Business) -> None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(business.business_yelp_url) as resp:
                business_page = await resp.text()
                soup = BeautifulSoup(business_page, "html.parser")

                try:
                    website_tag = soup.find_all("p", string="Business website")[0].parent.findNext("a")["href"]
                    business.business_website = (
                        str(unquote(website_tag))
                        .replace("/biz_redir?url=", "")
                        .split("?")[0]
                        .split("&")[0]
                    )
                except IndexError:
                    print("Website url not found.")

                reviewer_name_tags = list(
                    soup.find_all(
                        "div",
                        {"class": REVIEWER_NAME_SELECTOR},
                    )
                )[1:6]

                reviewer_location_tags = list(
                    soup.find_all(
                        "div",
                        {"class": REVIEWER_LOCATION_SELECTOR},
                    )
                )[1:6]

                date_tags = list(
                    soup.find_all(
                        "div",
                        {"class": DATE_SELECTOR},
                    )
                )[:5]

                if len(reviewer_name_tags) > 4:
                    for i in range(0, 5):
                        reviewer_name = (
                            reviewer_name_tags[i]
                            .select_one("span", {"class": "fs-block css-ux5mu6"})
                            .text
                        )
                        reviewer_location = (
                            reviewer_location_tags[i]
                            .select_one("span", {"class": "css-qgunke"})
                            .text
                        )
                        review_date = "".join(
                            i for i in date_tags[i].text if i.isdigit() or i == "/"
                        )
                        business.list_of_reviews.append(
                            ReviewDetails(reviewer_name, reviewer_location, review_date)
                        )
    except Exception as e:
        print(e)
        print("Error occurred while scraping details of business.")


async def main() -> None:
    categories = []
    location = input("Please, enter location (for example: 'Los Angeles').\n")
    category = input("Please, enter category (for example: 'contractors').\n")
    categories.append(category)

    print("Please, wait. It may take a while...")

    endpoint = endpoint_creator(location, categories)

    list_of_business_objects = get_businesses_by_api(endpoint, HEADERS)

    tasks = []
    for business in list_of_business_objects:
        task = asyncio.create_task(scrape_details_of_business(business))
        tasks.append(task)

    await asyncio.gather(*tasks)

    for business in list_of_business_objects:
        with open("businesses.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(business, default=lambda o: o.__dict__, indent=4))
            f.write(",\n")

    print("Done. Please, check 'businesses.json' file.")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
