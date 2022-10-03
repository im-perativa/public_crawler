# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Faskes(scrapy.Item):
    prov_id = scrapy.Field()
    dati2_id = scrapy.Field()
    dati2_name = scrapy.Field()
    no = scrapy.Field()
    kdppk = scrapy.Field()
    jnsppk = scrapy.Field()
    nmppk = scrapy.Field()
    telpppk = scrapy.Field()
    nmjlnppk = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    distance = scrapy.Field()
    vvip = scrapy.Field()
    vip = scrapy.Field()
    utama = scrapy.Field()
    I = scrapy.Field()
    II = scrapy.Field()
    III = scrapy.Field()
    ICU = scrapy.Field()
    ICCU = scrapy.Field()
    NICU = scrapy.Field()
    PICU = scrapy.Field()
    IGD = scrapy.Field()
    UGD = scrapy.Field()
    BERSALIN = scrapy.Field()
    HCU = scrapy.Field()
    ISOLASI = scrapy.Field()
    tglhbspksppk = scrapy.Field()
    jumlah_pelayanan = scrapy.Field()
    jumlah_sarana = scrapy.Field()
    jumlah_kamar_khusus = scrapy.Field()
    jumlah_kamar_i = scrapy.Field()
    jumlah_kamar_ii = scrapy.Field()
    jumlah_kamar_iii = scrapy.Field()
    jumlah_kamar_vip = scrapy.Field()
    jumlah_kamar_lain = scrapy.Field()
