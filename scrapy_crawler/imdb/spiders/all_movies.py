import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class AllMoviesSpider(CrawlSpider):
    name = 'all_movies'
    allowed_domains = ['imdb.com']
    start_urls = [f'https://www.imdb.com/title/tt{str(i).zfill(7)}/' for i in range(5001, 18325)]

    def parse(self, response):
        # Check if all fields are not null before yielding
        title = response.xpath("//h1[@data-testid='hero__pageTitle']/span/text()").get()
        year = response.xpath("//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt']/li/a/text()").get()
        duration = response.xpath("//li[@class='ipc-inline-list__item']/text()").get()
        genres = response.xpath("//span[@class='ipc-chip__text']/text()").get()
        overview = response.xpath("//span[@data-testid='plot-xs_to_m']/text()").get()
        rating = response.xpath("(//div[@data-testid='hero-rating-bar__aggregate-rating__score'])[1]/span/text()").get()
        num_rating = response.xpath("//div[@class='sc-bde20123-3 bjjENQ'][1]/text()").get()
        num_user_review = response.xpath("(//span[contains(@class, 'three-Elements')])[1]/span/text()").get()
        num_critics_review = response.xpath("(//span[contains(@class, 'three-Elements')])[2]/span/text()").get()
        metascore = response.xpath("(//span[@class='three-Elements'])[3]/span/span/text()").get()

        if all([title, year, duration, genres, rating, overview, num_rating, num_user_review, num_critics_review]):
            yield {
                'title': title,
                'year': year,
                'duration': duration,
                'genres': genres,
                'rating': rating,
                'overview': overview,
                'num_rating': num_rating,
                'num_user_review': num_user_review,
                'num_critics_review': num_critics_review,
                'metascore': metascore,
                'oscar': response.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-none sc-fcdc3619-2 oEiKO ipc-metadata-list--base']/li/a/text()").get(),
                'win_and_nomination': response.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-none sc-fcdc3619-2 oEiKO ipc-metadata-list--base']/li/div/ul/li/span/text()").get(),
                'url': response.url,
            }

    def parse_start_url(self, response):
        # In this method, you can set the priority for the requests
        for i in range(5001, 18325):
            url = f'https://www.imdb.com/title/tt{str(i).zfill(7)}/'
            yield scrapy.Request(url, callback=self.parse, priority=i)
