__author__ = 'dzlab'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy import log, Request

# http://blog.scrapinghub.com/2015/03/02/handling-javascript-in-scrapy-with-splash/
class MorningstarProSpider(CrawlSpider):
    name = "morningstarpro"
    allowed_domains = ["morningstarpro.fr"]
    start_urls = ["http://www.morningstarpro.fr/fr-FR/annuaire/societes/societes-de-gestion.html"]

    """rules = [
        Rule(
            LxmlLinkExtractor(
                allow=r'http://www.morningstarpro.fr/fr-FR/annuaire/societes/societes-de-gestion/\d+/societe/*',
                allow_domains=['morningstarpro.fr'],
                #restrict_xpaths='//article',
                tags=['a'],
                attrs=['href']),
            'parse_article')
    ]"""



    def start_requests(self):
        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            splash:wait(20.0)
            return splash:evaljs("document.querySelectorAll('p.MSMRSTSignature_FullName.MSMRSTArticleItemTitle')")
        end
        """
        for url in self.start_urls:
            yield Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'execute',
                    'args': {'lua_source': script}
                }
            })

    def parse(self, response):
        #log.msg(response, level=log.DEBUG)
        filename = response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)
        hxs = HtmlXPathSelector(response)
        elements = hxs.select('//div[contains(@class, "MSMRSTListTableCell MSMRSTListTableCell_Text  MSMRSTListTableCell_Text_CompanyCard")]')
        print elements
        for elm in elements:
            url = elm.select('./a/@href').extract()[0]
            yield Request(url, self.parse_article, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 10.0}
                }
            })

    # http://doc.scrapy.org/en/0.18/intro/tutorial.html#intro-tutorial
    def parse_article(self, response):
        print response.body
        hxs = HtmlXPathSelector(response)
        listing = hxs.select('//a[contains(@class, "MSMRSTNavigationPathPage")]')

        # use Item Loaders for removing spaces
        print listing