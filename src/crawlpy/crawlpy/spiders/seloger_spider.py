__author__ = 'dzlab'

import re

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
        # parse title
        title = listing.select('./div/div/h1/text()').extract()
        title = " ".join(title[0].encode("utf-8").split())
        # parse price
        price = listing.select('./div/section/div/div/div/span/text()').extract() #[contains(@class, "resume__prix"]
        price = " ".join(price[0].encode("utf-8").split())
        # parse location
        location = hxs.select('//h2[contains(@class, "detail-subtitle")]/span/text()').extract()
        location = re.sub(r'[\xe0]', r' ', location[0])
        location = " ".join(location.encode("utf-8").split())
        # parse the description section: surface, floor, etc.
        description = hxs.select('//ol[contains(@class, "description-liste")]/li/text()').extract()
        surface = " ".join(description[0].encode("utf-8").replace("Surface de", "").split())
        floor = " ".join(description[1].encode("utf-8").replace("Surface de", "").split())
        room = " ".join(description[2].encode("utf-8").replace("Surface de", "").split())

        fees = None
        elms = hxs.select('//ol[contains(@class, "description-liste")]/li/a/text()').extract()
        if len(elms) > 0:
            for i in range(len(elms)):
                if "Honoraires ttc :" in elms[i].encode("utf-8"):
                    fees = " ".join(elms[i].encode("utf-8").replace("Honoraires ttc :", "").split())
                    break

        # use Item Loaders for removing spaces
        print "title: %s, location: %s, price: %s" % (title, location, price)
        print "surface: %s, floor: %s, room: %s, fees: %s" % (surface, floor, room, fees)