from email import header
from http.client import ResponseNotReady
from requests import head
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'top_movies'
    # allowed_domains = ['imbd.com']
    # start_urls = ['https://www.imdb.com/chart/top/']

    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url="https://www.imdb.com/chart/top/", headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True),)
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True, process_request='set_user_agent'))

    # def set_user_agent(self, request):
    #     request.headers['User-Agent'] = self.user_agent
    #     return request

    def parse_item(self, response):
        movie_title = response.xpath(
            '//div[@class="sc-94726ce4-2 khmuXj"]/h1/text()').get()
        year = response.xpath(
            '//span[@class="sc-8c396aa2-2 itZqyK"]/text()')[0].get()
        duration = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]/text()').getall()
        genre = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div/a/ul/li/text()').get()
        rating = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]/text()').get()
        yield {
            "movie_title": movie_title,
            "year": year,
            "duration": "".join(duration),
            "genre": genre,
            "rating": rating,
            "movie_url": response.url,


        }
