from email import header
from scraper_helper import headers
import scrapy


class TinydealspiderSpider(scrapy.Spider):
    name = 'tinydealspider'
    allowed_domains = [
        'www.tinydeals.co']
    start_urls = [
        'https://www.tinydeals.co/product-category/smart-phones-tablets']
    header = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"

    def start_requests(self):
        return scrapy.Request(url="https://www.tinydeals.co/product-category/smart-phones-tablets", callback=self.parse, headers={header})

    def parse(self, response):
        main_div = response.xpath("//ul[@data-view='grid']/li")
        for item in main_div:
            yield {
                "product_url": item.xpath('//*[@id="main"]/ul/li[1]/div/div/div[1]/a/@href').get(),
                "product_title": item.xpath('//*[@id="main"]/ul/li[1]/div/div/div[1]/a/h2/text()').get(),
                "product_price": item.xpath('.//span[@class="woocommerce-Price-amount amount"]/bdi/text()').get()

            }
        current_page = response.xpath(
            '//span[@class="page-numbers current"]/text()').get()
        next_page = int(current_page) + 1
        home_url = "https://www.tinydeals.co/product-category/smart-phones-tablets/page/"
        next_page_url = f'{home_url}{next_page}'
        if int(current_page) != next_page:
            yield response.follow(next_page_url, callback=self.parse, headers={header})
