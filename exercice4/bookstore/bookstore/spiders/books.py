# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from bookstore.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    page_count = 1
    max_pages =3
    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            item = BookItem()
            item["title"] = book.css("h3 a::attr(title)").get()
            item["price"] = float(book.css(".price_color::text").get().replace('£',''))
            item["rating"] = book.css("p::attr(class)").get()
            item["availability"] = book.css(".availability::text").re_first(r"\S.*\S")

            yield item

        if self.page_count < self.max_pages:
            next_page = response.css("li.next a::attr(href)").get()
            if next_page:
                self.page_count += 1
                yield response.follow(next_page, callback=self.parse)