import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MoviesByYearSpider(CrawlSpider):
    name = 'movies_by_year'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?title_type=feature&release_date=1960-01-01,2022-12-31']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"))
    )

    def parse_item(self, response):
        yield {
            'title': response.xpath("//h1[@data-testid='hero__pageTitle']/span/text()").get(),
            'img_url': response.xpath("//meta[@property='og:image']/@content").get(),
            'year': response.xpath("//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt']/li/a/text()").get(),
            'director': response.xpath("//li[contains(.//text(), 'Director')]//ul/li/a/text()").get(),
            'stars': [item.xpath(".//text()").get() for item in response.xpath("//li[contains(.//text(), 'Stars')]//ul/li/a")],
            'duration': response.xpath("//li[@class='ipc-inline-list__item']/text()").get(),
            'genres': [item.xpath(".//span/text()").get() for item in response.xpath("//div[@data-testid='genres']//a")],
            'overview': response.xpath("//span[@data-testid='plot-xl']/text()").get(),
            'rating': response.xpath("(//div[@data-testid='hero-rating-bar__aggregate-rating__score'])[1]/span/text()").get(),
            'num_rating': response.xpath("//div[@class='sc-bde20123-3 bjjENQ'][1]/text()").get(),
            'num_user_review': response.xpath("(//span[contains(@class, 'three-Elements')])[1]/span/text()").get(),
            'num_critic_review': response.xpath("(//span[contains(@class, 'three-Elements')])[2]/span/text()").get(),
            'budget': response.xpath("//li[@data-testid='title-boxoffice-budget']/div/ul/li/span/text()").get(),
            'gross': response.xpath("//li[@data-testid='title-boxoffice-cumulativeworldwidegross']/div/ul/li/span/text()").get(),
            'country': response.xpath("//li[@data-testid='title-details-origin']//a/text()").get(),
            'metascore': response.xpath("//span[contains(@class, 'metacritic-score-box')]/text()").get(),
            'oscar': response.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-none sc-fcdc3619-2 oEiKO ipc-metadata-list--base']/li/a/text()").get(),
            'win_and_nomination': response.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-none sc-fcdc3619-2 oEiKO ipc-metadata-list--base']/li/div/ul/li/span/text()").get(),
            'url': response.url,
        }
