import json
from typing import List, Any
from requests.exceptions import RequestException

from bs4 import BeautifulSoup, ResultSet
from sitemap import Sitemap
import requests
from pymongo import MongoClient

import sitemap

client = MongoClient("mongodb://localhost:27017")
db = client["news"]
collection = db["articles"]


class Article:
    def __init__(self, site, url, title, description, keywords, author, published_time, modified_time, article_section,
                 word_count, language, date_created):
        self.site = site
        self.url = url
        self.title = title
        self.description = description
        self.keywords = keywords
        self.author = author
        self.published_time = published_time
        self.modified_time = modified_time
        self.article_section = article_section
        self.word_count = word_count
        self.language = language
        self.date_created = date_created

    # Getters

    def get_site(self):
        return self.site

    def get_url(self):
        return self.url

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_keywords(self):
        return self.keywords

    def get_author(self):
        return self.author

    def get_published_time(self):
        return self.published_time

    def get_modified_time(self):
        return self.modified_time

    def get_article_section(self):
        return self.article_section

    def get_word_count(self):
        return self.word_count

    def get_language(self):
        return self.language

    def get_date_created(self):
        return self.date_created

    # Setters

    def set_site(self, site):
        self.site = site

    def set_url(self, url):
        self.url = url

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_keywords(self, keywords):
        self.keywords = keywords

    def set_author(self, author):
        self.author = author

    def set_published_time(self, published_time):
        self.published_time = published_time

    def set_modified_time(self, modified_time):
        self.modified_time = modified_time

    def set_article_section(self, article_section):
        self.article_section = article_section

    def set_word_count(self, word_count):
        self.word_count = word_count

    def set_language(self, language):
        self.language = language

    def set_date_created(self, date_created):
        self.date_created = date_created


class DataExtractor:
    def extract_locs_from_sitemap(self, xml_sitemaps):
        locs = []
        obj =DataExtractor()
        for sitemap_url in xml_sitemaps:
            response = requests.get(sitemap_url)
            if response.status_code == 200:
                xml_content = response.text
                soup = BeautifulSoup(xml_content, "xml")
                url_elements = soup.find_all("url")
                for url_element in url_elements:
                    loc_element = url_element.find("loc")
                    if loc_element:
                        locs.append(loc_element.get_text())
                        print(f'{loc_element.get_text()} grabbed')
                        obj.extract_mayadeen(url=loc_element.get_text())

            else:
                print(f"Failed to fetch sitemap: {sitemap_url}")
        print(f'returned loc : {locs}')
        return locs

    def extract_mayadeen(self, url):
        print('start extraction from mayadeen')
        connect_timeout = 100  # seconds
        read_timeout = 500  # seconds

        try:
            response = requests.get(url,timeout=(connect_timeout,read_timeout))
            html_content = response.content
            soup = BeautifulSoup(html_content, "lxml")
            # Find all script tags containing JSON-LD data
            script_tags = soup.find_all("script", type="application/ld+json")

            # Extract data from the first script tag
            if script_tags:
                first_script_tag = script_tags[0]
                json_ld_content = json.loads(first_script_tag.string)

                # Extract the desired data from the JSON-LD content
                data = {
                    "site": json_ld_content.get("publisher", {}).get("url", None),
                    "url": json_ld_content.get("url", None),
                    "title": json_ld_content.get("headline", None),
                    "description": json_ld_content.get("description", None),
                    'keywords': json_ld_content.get("keywords", None),
                    'author': json_ld_content.get("author", {}).get("name", None),
                    'published_time': json_ld_content.get("datePublished", None),
                    'modified_time': json_ld_content.get("dateModified", None),
                    'article_section': json_ld_content.get("articleSection", None),
                    'word_count': json_ld_content.get("wordCount", None),
                    'language': json_ld_content.get("inLanguage", None),
                    'date_created': json_ld_content.get("dateCreated", None)
                }
                collection.insert_one(data)
                print(f'inserted: {data}')
            else:
                print("JSON-LD script tag not found.")
        except RequestException as e:
            print(f"An error occurred during the request: {e} at this url : {url}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def extract_jazeera(self, url):
        print('start extraction from jazeera')
        connect_timeout = 100  # seconds
        read_timeout = 500  # seconds

        try:
            response = requests.get(url, timeout=(connect_timeout, read_timeout))
            print(response)
            html_content = response.content
            soup = BeautifulSoup(html_content, "lxml")
            # Find all script tags containing JSON-LD data
            script_tags = soup.find_all("script", type="application/ld+json")

            # Extract data from the first script tag
            if script_tags:
                first_script_tag = script_tags[0]
                json_ld_content = json.loads(first_script_tag.string)

                # Extract the desired data from the JSON-LD content
                data = {
                    "site": json_ld_content.get("name", ""),
                    "url": json_ld_content.get("mainEntityOfPage", ""),
                    "title": json_ld_content.get("headline", ""),
                    "description": json_ld_content.get("description", ""),
                    'author': json_ld_content.get("author", {}).get("name", ""),
                    'published_time': json_ld_content.get("datePublished", ""),
                    'modified_time': json_ld_content.get("dateModified", ""),
                }
                collection.insert_one(data)
                print(f'inserted: {data}')
            else:
                print("JSON-LD script tag not found.")
        except RequestException as e:
            print(f"An error occurred during the request: {e} at this url : {url}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def main():
    sitemap_extractor = Sitemap()
    data = DataExtractor()
    sitemap_url = 'https://www.almayadeen.net/sitemaps/all.xml'
    sitemaps = sitemap_extractor.process_sitemap(sitemap_url)
    article_urls = data.extract_locs_from_sitemap(xml_sitemaps=sitemaps)
    print('finished and now extracting')
    # for article in article_urls:
    #     data.extract_jazeera(url=article)

    client.close()


if __name__ == '__main__':
    main()
