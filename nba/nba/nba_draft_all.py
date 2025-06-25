import scrapy
from scrapy.crawler import CrawlerProcess
from pathlib import Path
from nba.nba.spiders.draft import DraftSpider

downloads = Path.home() / 'Downloads'

year = '2021'
# filename = year + '.csv'
filename = 'drafts.csv'
filepath = downloads / filename
uri = 'file:///' + filename
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'CSV',
    'FEED_URI': uri,
})

dir(process)
process.crawl(DraftSpider, year=2020)
process.start()
process.stop()