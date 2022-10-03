# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Ads(scrapy.Item):
    url = scrapy.Field()
    industry = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    experience = scrapy.Field()
    category = scrapy.Field()
    salary_currency = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    description = scrapy.Field()
    requirement = scrapy.Field()
    ads_start = scrapy.Field()
    ads_end = scrapy.Field()
    company = scrapy.Field()
    company_industry = scrapy.Field()
    company_size = scrapy.Field()
    company_nearby_transportation = scrapy.Field()
    company_hq = scrapy.Field()
    company_web = scrapy.Field()
