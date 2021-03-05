import scrapy


class TeamsMappingSpider(scrapy.Spider):
    name = 'teams_mapping'
    allowed_domains = ['basketball-reference.com']
    start_urls = ['http://basketball-reference.com/teams/']

    def parse(self, response):
        ths = response.xpath('//th[@data-stat="franch_name"]')
        for th in ths:
            a = th.xpath('./a')
            if a:
                team_name = a.xpath('./text()').extract_first()
                href = (a.xpath('./@href').extract_first()
                    .replace('/teams/', '')
                    .replace('/', '')
                )
                yield dict(team_name=team_name, team_id=href)
