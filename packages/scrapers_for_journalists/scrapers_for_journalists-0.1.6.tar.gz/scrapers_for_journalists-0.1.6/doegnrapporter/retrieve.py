from argparse import ArgumentParser
import json
import re

import pandas as pd
import requests
from base import BaseScraper
from bs4 import BeautifulSoup
from tqdm import tqdm


class DoegnRapportScraper(BaseScraper):
    """
    Scraper af døgnrapporter fra politi.dk
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"
        }

    def get_pages(self, publish_date_from: str, publish_date_to: str) -> list[dict]:
        """
        getting links to scrape
        """
        max_pages = 10
        links = []

        publish_date_from = publish_date_from.replace("-", "/")
        publish_date_to = publish_date_to.replace("-", "/")

        for page_no in tqdm(range(1, max_pages)):
            response = requests.get(
                "https://politi.dk/doegnrapporter"
                + f"?fromDate={publish_date_from}"
                + f"&toDate={publish_date_to}"
                + f"&newsType=Doegnrapporter&page={page_no}",
                headers=self.headers,
            )

            soup = BeautifulSoup(response.text, features="html.parser")
            content = soup.select_one("section.newsList")
            content = json.loads(re.findall(r"init\((.+)\)", content.get("ng-init"))[0])
            new_links = content["AllNews"]["NewsList"]
            print(f"... Found {len(new_links)} links")

            if len(new_links) == 0:
                print(f"Got to the last page: {page_no}")
                return links
            else:
                links = links + new_links

        return links

    def parse_page(self, soup: BeautifulSoup) -> dict:
        text = soup.select_one("article.newsArticle").text
        headings = [
            h2.text for h2 in soup.select("article.newsArticle h2") if h2.text != ""
        ]

        return {"rapport": text, "overskrifter i rapport": ", ".join(headings)}

    def execute(self, publish_date_from: str, publish_date_to: str) -> pd.DataFrame:
        print(
            f"***Looking through police reports from {publish_date_from} to {publish_date_to}"
        )

        # Get links and save locally
        print("*** Getting links for pages ***")
        pages = self.get_pages(
            publish_date_from=publish_date_from, publish_date_to=publish_date_to
        )

        # Scrape pages
        print("*** Scraping pages ***")
        reports = []
        for page in tqdm(pages):
            response = requests.get(page["Link"], headers=self.headers)
            soup = BeautifulSoup(response.text, features="html.parser")
            data = self.parse_page(soup)
            data.update(page)
            reports.append(data)

        print("*** -> DONE <- ***")
        return pd.DataFrame(reports)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="DomStolScraper", description="Scrapes rapporter from politi.dk"
    )
    parser.add_argument(
        "--outfile", help="the path to save the Excel-file. Must end with .xlsx"
    )
    parser.add_argument(
        "--from_date", help="filter only ads published from, format. YYYY-mm-dd"
    )
    parser.add_argument(
        "--to_date", help="filter only ads published to, format. YYYY-mm-dd"
    )
    args = parser.parse_args()
    print(args.from_date)
    scraper = DoegnRapportScraper()
    df = scraper.execute(publish_date_from=args.from_date, publish_date_to=args.to_date)

    df.to_excel(args.outfile, engine="openpyxl", index=False)
