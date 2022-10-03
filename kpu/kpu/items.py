# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PilpresItem(scrapy.Item):
    url = scrapy.Field()
    provinsi_id = scrapy.Field()
    provinsi = scrapy.Field()
    kabupaten_id = scrapy.Field()
    kabupaten = scrapy.Field()
    kecamatan_id = scrapy.Field()
    kecamatan = scrapy.Field()
    kelurahan_id = scrapy.Field()
    kelurahan = scrapy.Field()
    tps_id = scrapy.Field()
    tps = scrapy.Field()
    timestamp = scrapy.Field()
    pemilih = scrapy.Field()
    pengguna = scrapy.Field()
    suara_sah = scrapy.Field()
    suara_tidak_sah = scrapy.Field()
    suara_total = scrapy.Field()
    calon_21 = scrapy.Field()
    calon_22 = scrapy.Field()


class PilegItem(scrapy.Item):
    url = scrapy.Field()
    tipe = scrapy.Field()
    provinsi_id = scrapy.Field()
    provinsi = scrapy.Field()
    kabupaten_id = scrapy.Field()
    kabupaten = scrapy.Field()
    kecamatan_id = scrapy.Field()
    kecamatan = scrapy.Field()
    kelurahan_id = scrapy.Field()
    kelurahan = scrapy.Field()
    tps_id = scrapy.Field()
    tps = scrapy.Field()
    timestamp = scrapy.Field()
    pemilih = scrapy.Field()
    pengguna = scrapy.Field()
    suara_sah = scrapy.Field()
    suara_tidak_sah = scrapy.Field()
    suara_total = scrapy.Field()
    partai_1 = scrapy.Field()
    partai_2 = scrapy.Field()
    partai_3 = scrapy.Field()
    partai_4 = scrapy.Field()
    partai_5 = scrapy.Field()
    partai_6 = scrapy.Field()
    partai_7 = scrapy.Field()
    partai_8 = scrapy.Field()
    partai_9 = scrapy.Field()
    partai_10 = scrapy.Field()
    partai_11 = scrapy.Field()
    partai_12 = scrapy.Field()
    partai_13 = scrapy.Field()
    partai_14 = scrapy.Field()
    partai_15 = scrapy.Field()
    partai_16 = scrapy.Field()
    partai_17 = scrapy.Field()
    partai_18 = scrapy.Field()
    partai_19 = scrapy.Field()
    partai_20 = scrapy.Field()