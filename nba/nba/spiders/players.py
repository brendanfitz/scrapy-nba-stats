import scrapy
from urllib.parse import quote_plus

class PlayersSpider(scrapy.Spider):
    name = 'players'
    allowed_domains = ['basketball-reference.com']
    search_url = 'https://www.basketball-reference.com/search/search.fcgi?search='

    def __init__(self, player_name):
        self.player_name = player_name
    
    def start_requests(self):
        start_url = self.search_url + quote_plus(self.player_name)
        yield scrapy.Request(start_url, self.parse_search_results)
    
    def parse_search_results(self, response):
        resource_path = response.xpath('//div[@class="search-item-url"]/text()').extract_first()
        if resource_path is None:
            raise ValueError('Player Not Found')
        url = 'https://www.basketball-reference.com' + resource_path
        yield scrapy.Request(url, callback=self.parse_per_game_stats)

    def parse_per_game_stats(self, response):
        table = response.xpath('//table[@id="per_game"]')
        thead = table.xpath('./thead/tr/th/text()').extract()

        trs = table.xpath('./tbody/tr')
        for row in trs:
            th = row.xpath('./th//text()').extract_first()
            tds = row.xpath('./td//text()').extract()
            row_data = [th] + tds 
            yield dict(zip(thead, row_data))
        

        
        