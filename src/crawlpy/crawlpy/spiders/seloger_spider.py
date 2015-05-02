# encoding=utf8
__author__ = 'dzlab'

import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

from crawlpy.items import RentalAdItem

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
        hxs = Selector(response=response)
        # parse reference
        reference  = hxs.xpath('//span[contains(@class, "description_ref")]/text()').extract()
        reference = reference[0].encode("utf-8").split()[1]
        listing = hxs.xpath('//div[contains(@class, "main listing")]')
        # parse title
        title = listing.xpath('./div/div/h1/text()').extract()
        title = " ".join(title[0].encode("utf-8").split())
        # parse price
        price = listing.xpath('./div/section/div/div/div/span/text()').extract() #[contains(@class, "resume__prix"]
        price = price[0].encode("utf-8").split()[0].replace('\xc2\xa0', '').replace(",", ".")
        print "price: %s" % price
        # parse location
        location = hxs.xpath('//h2[contains(@class, "detail-subtitle")]/span/text()').extract()
        location = re.sub(r'[\xe0]', r' ', location[0])
        location = " ".join(location.encode("utf-8").split())
        description = hxs.xpath('//p[contains(@class, "description")]/text()').extract()
        description = " ".join(description[0].encode("utf-8").split())
        # parse the description section: surface, floor, etc.
        elms = hxs.xpath('//ol[contains(@class, "description-liste")]/li/text()').extract()
        room = None
        floor = None
        surface = None
        fees = None
        constructedIn = None
        for cell in range(len(elms)):
            encoded = elms[cell].encode("utf-8")
            if "Surface de" in encoded:
                surface = " ".join(encoded.replace("Surface de", "").split())
            elif "Honoraires ttc :" in encoded: # parse fees
                fees = encoded.replace("Honoraires ttc :", "").split()[0].replace('\xc2\xa0', '').replace(",", ".")
            elif "Etage" in encoded:
                floor = encoded.replace("Etage", "").split()[0]
            elif "Pièce" in encoded:
                room = encoded.replace("Pièce", "").split()[0]
            elif "Garantie :" in encoded:
                warranty = encoded.replace("Garantie :", "").split()[0].replace('\xc2\xa0', '').replace(",", ".")
            elif "Cave" in encoded:
                cellar = True
            elif "Année de construction"  in encoded:
                constructedIn = encoded.replace("Année de construction", "").split()[0]
                print "constructed in %s" % constructedIn

        elms = hxs.xpath('//ol[contains(@class, "description-liste")]/li/a/text()').extract()
        if len(elms) > 0:
            for i in range(len(elms)):
                if "Honoraires ttc :" in elms[i].encode("utf-8"):
                    fees = elms[i].encode("utf-8").replace("Honoraires ttc :", "").split()[0]
                    break

        yield RentalAdItem(reference=reference,
                           title=title,
                           description=description,
                           location=location,
                           surface=surface,
                           price=price,
                           fees=fees,
                           link= response.url,
                           room= room,
                           floor= floor,
                           constructedIn=constructedIn)