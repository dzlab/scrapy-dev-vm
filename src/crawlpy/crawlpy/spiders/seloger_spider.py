__author__ = 'dzlab'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

class SelogerSpider(CrawlSpider):
    name = "seloger"
    allowed_domains = ["seloger.com"]
    start_urls = ["http://www.seloger.com/list.htm?cp=75&idtt=1",
                  "http://www.seloger.com/list.htm?cp=93&idtt=1",
                  "http://www.seloger.com/list.htm?cp=92&idtt=1",
                  "http://www.seloger.com/list.htm?cp=94&idtt=1"]

    rules = [
        Rule(
            LxmlLinkExtractor(
                allow='http://www.seloger.com/annonces/*',
                allow_domains=['seloger.com'],
                restrict_xpaths='//article',
                tags=['a'],
                attrs=['href']),
            'parse_article')
    ]

    # http://doc.scrapy.org/en/0.18/intro/tutorial.html#intro-tutorial
    def parse_article(self, response):
        hxs = HtmlXPathSelector(response)
        listing = hxs.select('//div[contains(@class, "main listing")]')
        title = listing.select('./div/div/h1/text()').extract()
        #title = " ".join(title[0].split())
        price = listing.select('./div/section/div/div/div/span/text()').extract() #[contains(@class, "resume__prix"]
        #price = " ".join(price.split())
        # use Item Loaders for removing spaces
        print title, price