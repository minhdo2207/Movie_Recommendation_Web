import scrapy
import pandas as pd
from imdb.items import ImdbItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import HtmlResponse

class UserRatingSpider(scrapy.Spider):
    name = 'user_rating1'
    df = pd.read_csv("./movies_data.csv", low_memory=False)
    df['title_id'] = df['url'].str.extract(r'/title/([^/]+)')
    title_id_list = df['title_id'].unique()
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/title/{}/reviews'.format(title_id) for title_id in title_id_list]

    def parse(self, response):
        user_urls = response.xpath("//span[@class='display-name-link']/a/@href").getall()
        ratings = response.xpath("//span[@class='rating-other-user-rating']/span[1]/text()").getall()

        for user_url, rating in zip(user_urls, ratings):
            user_id = user_url.split('/')[-2]
            movie_id = response.url.split('?')[0].split('/')[-2]

            yield {
                'user_id': user_id,
                'movie_id': movie_id,
                'rating': rating
            }