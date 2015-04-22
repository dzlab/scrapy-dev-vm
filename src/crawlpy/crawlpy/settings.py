# -*- coding: utf-8 -*-

# Scrapy settings for logement project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'logement'

SPIDER_MODULES = ['logement.spiders']
NEWSPIDER_MODULE = 'logement.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'logement (+http://www.yourdomain.com)'

# configuring splash
DOWNLOADER_MIDDLEWARES = {
    'scrapyjs.SplashMiddleware': 725,
}
SPLASH_URL = 'http://localhost:8050/'
DUPEFILTER_CLASS = 'scrapyjs.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapyjs.SplashAwareFSCacheStorage'