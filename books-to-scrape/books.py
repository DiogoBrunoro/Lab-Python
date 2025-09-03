import scrapy
from scrapy.crawler import CrawlerProcess
import json

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ['http://books.toscrape.com/']


    books_list = []

    def parse(self, response):
        # Extrai os dados dos livros da página atual
        for book in response.css('article.product_pod'):
            book_data = {
                'title': book.css('h3 a::attr(title)').get(),
                'price': float(book.css('p.price_color::text').get().replace('£', '')),
                #'price': float(book.css('p.price_color::text').get().replace('£', '')),
                'availability': book.css('p.instock.availability::text').re_first('(\S+\s\S+)'),
            }
            if (book_data['price'] >= 50):
                self.books_list.append(book_data)
            


        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # Segue para a próxima página
            yield response.follow(next_page, self.parse)
        else:
            # Quando não houver mais páginas, salva os dados acumulados em um arquivo JSON
            with open('books.json', 'w', encoding='utf-8') as f:
                json.dump(self.books_list, f, ensure_ascii=False, indent=4)