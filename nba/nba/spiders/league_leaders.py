import scrapy
from sys import exit


class LeagueLeadersSpider(scrapy.Spider):
    name = 'league_leaders'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://basketball-reference.com/']

    def __init__(self, year, statistic=None):
        self.year = year
        self.statistic = statistic


    def start_requests(self):
        start_url = f'https://www.basketball-reference.com/leagues/NBA_{self.year}_leaders.html'
        yield scrapy.Request(start_url, self.parse)
    
    def parse(self, response):
        self.stats_available = sorted(response.xpath('//table/caption/text()').extract())
        
        if self.statistic is None or self.statistic not in self.stats_available:
            self.show_stat_list(response)

        table = response.xpath(f'//table/caption[@data-tip="{self.statistic}"]/parent::table')

        for tr in table.xpath('./tr'):
            rank = tr.xpath('./td[@class="rank"]/text()').extract_first()
            player_name = tr.xpath('./td[@class="who"]/a/text()').extract_first()
            team_id = tr.xpath('./td[@class="who"]/span/text()').extract_first()
            value = tr.xpath('./td[@class="value"]/text()').extract_first()

            yield dict(
                statistic=self.statistic,
                rank=rank,
                player_name=player_name,
                team_id=team_id,
                value=value,
            )
    
    def show_stat_list(self, response):
        print("\n\nPlease choose one of the following statistics")
        print('*' * 80)

        for stat in self.stats_available:
            print(stat)
        
        print('*' * 80)

        self.statistic = input("Please enter stat from list above here (enter q to quit): ")

        while self.statistic not in self.stats_available:
            if self.statistic == 'q':
                exit(0)

            self.statistic = input("Statistic not found. Please enter stat here (enter q to quit): ")








