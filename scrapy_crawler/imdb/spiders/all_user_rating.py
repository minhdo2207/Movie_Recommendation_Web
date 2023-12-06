import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class MoviesByYearSpider(CrawlSpider):
    name = 'user_rating'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?title_type=feature&release_date=1960-01-01,2022-12-31']
    # start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_movie', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"))
    )

    def parse_movie(self, response):
        for review_link in response.xpath("//div[@data-testid='reviews-header']//a/@href").getall():
            review_url = response.urljoin(review_link)
            yield scrapy.Request(review_url, callback=self.parse_review)


    def parse_review(self, response):
        user_urls = response.xpath("//span[@class='display-name-link']/a/@href").getall()
        ratings = response.xpath("//span[@class='rating-other-user-rating']/span[1]/text()").getall()

        for user_url, rating in zip(user_urls, ratings):
            user_id = user_url.split('/')[-2]
            movie_id = response.url.split('?')[0].split('/')[-2]

            item = {
                'user_id': user_id,
                'movie_id': movie_id,
                'rating': rating,
            }
            yield item
