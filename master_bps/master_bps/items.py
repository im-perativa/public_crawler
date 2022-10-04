# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DesaItem(scrapy.Item):
    bps_provinsi_id = scrapy.Field()
    bps_provinsi = scrapy.Field()
    bps_kabupaten_id = scrapy.Field()
    bps_kabupaten = scrapy.Field()
    bps_kecamatan_id = scrapy.Field()
    bps_kecamatan = scrapy.Field()
    bps_desa_id = scrapy.Field()
    bps_desa = scrapy.Field()
    kemendagri_provinsi_id = scrapy.Field()
    kemendagri_provinsi = scrapy.Field()
    kemendagri_kabupaten_id = scrapy.Field()
    kemendagri_kabupaten = scrapy.Field()
    kemendagri_kecamatan_id = scrapy.Field()
    kemendagri_kecamatan = scrapy.Field()
    kemendagri_desa_id = scrapy.Field()
    kemendagri_desa = scrapy.Field()
