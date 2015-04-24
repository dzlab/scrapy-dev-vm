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

    # render starting url into splash then extract the links to companies pages
    def start_requests(self):
        log.msg('Parsing starting urls: '+str(self.start_urls), level=log.DEBUG)
        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            get_nodes_html = splash:jsfunc([[
                function(css){
                    var elems = document.querySelectorAll(css);
                    var res = [];
                    for (var i=0; i<elems.length; i++){
                        res.push(elems[i].getElementsByTagName('a')[0].getAttribute('href'));
                    }
                    return res;
                }
            ]])
            splash:wait(20.0)
            local res = get_nodes_html('p.MSMRSTSignature_FullName.MSMRSTArticleItemTitle')
            return res
        end
        """
        for url in self.start_urls:
            yield Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'execute',
                    'args': {'lua_source': script}
                }
            })
    # receives a list of urls of companies pages
    def parse(self, response):
        log.msg('Parsing company page: %s' % response.url, level=log.DEBUG)
        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            fetch = splash:jsfunc([[
                function(){
                    var res = {};
                    var elems = document.querySelectorAll('a.MSMRSTNavigationPathPage');
                    res['company'] = elems[elems.length-1].innerHTML;
                    res['address'] = document.querySelectorAll('p.MSMRSTSignature_Address')[0].innerHTML;
                    res['contacts'] = []
                    var peoplElms = document.querySelector('div.MSMRSTWidget.MSMRSTWidget_People').querySelectorAll('div.MSMRSTListTableRow');
                    for (var i=0; i<peoplElms.length; i++){
                        var contact = {};
                        contact['fullname'] = peoplElms[i].querySelector('p.MSMRSTSignature_FullName').childNodes[0].innerHTML;
                        res['contacts'].push(contact);
                    }
                    return res;
                }
            ]])
            splash:wait(20.0)
            local res = fetch()
            return res
        """
        urls = eval(response.body)
        for url in urls:
            yield Request(url, self.parse_company_page, meta={
                'splash': {
                    'endpoint': 'execute',
                    'args': {'lua_source': script}
                }
            })

    # retrieve contact information from a given company page
    def parse_company_page(self, response):
        #print response.body
        hxs = HtmlXPathSelector(response)
        listing = hxs.select('//a[contains(@class, "MSMRSTNavigationPathPage")]/href').extract()

        # use Item Loaders for removing spaces
        print listing