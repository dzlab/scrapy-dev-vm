__author__ = 'dzlab'

from scrapy.link import Link

class SelogerLinkExtractor:

    def extract_links(self, response):
        hxs = HtmlXPathSelector(response)
        articles = hxs.select('//article')
        links = []
        for article in articles:
            div = article.select('./div/div/div')
            href = div.select('a[contains(@class, "listing_link slides")]/@href').extract()[0]
            link = Link(href)
            links.append(link)
        return links