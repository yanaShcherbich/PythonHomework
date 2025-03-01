"""Module contains class related to news."""

import json
import logging
import sys
import datetime

import feedparser
from bs4 import BeautifulSoup

from rss.cache import Cache


class News:
    """This class parses, processes and outputs news."""

    def __init__(self, url: str, limit=None):
        logging.info('News initialization')

        self.url = url
        logging.info('Parsing url')
        self.feeds = feedparser.parse(self.url)
        self._check_url()

        self.feed_title = self.feeds.feed.get('title')
        self.list_of_news = []
        self.list_of_row_descriptions = []

        self._check_limit(limit)
        self.make_list_of_news()

    def _check_url(self):
        """Check if the url is valid."""

        logging.info('Check URL')
        if self.feeds['bozo'] or self.feeds.status != 200:
            raise Exception('Something wrong with URL or Internet connection')

    def _check_limit(self, limit):
        """Check if the limit > 0."""

        logging.info('Check limit')
        if limit is not None and limit <= 0:
            raise ValueError('Invalid limit: limit <= 0')

    def print_news(self, limit):
        """Print news in human-readable format."""

        logging.info("Start printing news")
        print('\nFeed:', self.feed_title, "\n\n")

        news_number = 1
        # check if self.list_of_news consists of 1 element
        if type(self.list_of_news) == dict:
            print('№', news_number)
            self._print_entries(self.list_of_news)
        else:
            for news in self.list_of_news[:limit]:
                print('№', news_number)
                news_number += 1
                self._print_entries(news)

    def _print_entries(self, news: dict):
        """Print one news."""

        logging.info('Print one news')
        print('Title:', news['title'])
        print('Date:', news['date'])
        print('Link:', news['link'], '\n')

        if news['description']['text'] != 'Nothing':
            print(news['description']['text'], '\n')

        if news['description']['images']:
            print('Images:')
            for item in news['description']['images']:
                print(item['src'])

        if news['description']['links']:
            print('Links:')
            for item in news['description']['links']:
                print(item)

        print('-' * 50)

    def _find_date_tag(self, news: dict) -> str:
        """
        Find date tag and return its value,
        or return the current local date if tag not found.
        """

        logging.info('Find date tag')

        if news.get('published'):
            return news['published']
        elif news.get('pubDate'):
            return news['pubDate']
        elif news.get('Date:'):
            return news['Date']
        else:
            date = datetime.datetime.now()
            return date.isoformat()

    def make_list_of_news(self):
        """Make a list of news.

        type of news: dict
         """

        logging.info('Make a list of news')

        cache = Cache()
        for news in self.feeds['entries']:
            title = news.get('title', 'Unknown')
            one_news = {'title': title.replace('&#39;', "'"),
                        'link': news.get('link', 'Unknown'),
                        'date': self._find_date_tag(news)}
            one_news.update(self._read_description(news))

            self.list_of_news.append(one_news)
            cache.insert_news(one_news, self.list_of_row_descriptions[-1], self.url)

    def _read_description(self, news: dict) -> dict:
        """Return dict with keys 'text', 'images', 'links'.

        'text' value is description(str)
        'images' value is a dict
        'links' value is a list of urls
        """

        logging.info('Get information from description')
        soup = BeautifulSoup(news.description, features="html.parser")

        logging.info('Get text of description')
        text = soup.text.replace('&#39;', "'")
        if not text:
            text = 'Nothing'

        self.list_of_row_descriptions.append(news.description)
        return {'description': {'text': text, 'images': self._get_img_list(soup),
                'links': self._get_links_list(soup)}}

    def _get_img_list(self, soup) -> list:
        """Get images src and alt from soup object.
        Return list of dicts.
        """

        logging.info('Get images')
        list_of_images = []
        images = soup.findAll('img')
        for image in images:
            if image.get('src'):
                list_of_images.append({'src': image['src'], 'alt': image['alt']})
        return list_of_images if list_of_images else None

    def _get_links_list(self, soup):
        """Get links from soup object."""

        logging.info('Get set of links')
        set_of_links = set()
        for tag in soup.findAll():
            if tag.get('href'):
                set_of_links.add(tag['href'])
            if tag.get('url'):
                set_of_links.add(tag['url'])
        return list(set_of_links) if set_of_links else None

    def convert_to_json(self, limit=None):
        """Return news in JSON format."""

        logging.info('Convert news into JSON format')
        result = json.dumps({'news': {'feed': self.feed_title, 'items': self.list_of_news[:limit]}},
                            indent=4, ensure_ascii=False)
        return result
