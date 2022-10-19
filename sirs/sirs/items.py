# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RsItem(scrapy.Item):
    kode = scrapy.Field()
    nama = scrapy.Field()
    kabupaten = scrapy.Field()
    alamat = scrapy.Field()
    telepon = scrapy.Field()
    pemilik = scrapy.Field()
    kelas = scrapy.Field()
    
    jenis = scrapy.Field()
    status_blu = scrapy.Field()
    direktur = scrapy.Field()
    luas_tanah = scrapy.Field()
    luas_bangunan = scrapy.Field()

class TempatTidurItem(scrapy.Item):
    kode = scrapy.Field()
    kelas = scrapy.Field()
    jumlah = scrapy.Field()

class LayananItem(scrapy.Item):
    kode = scrapy.Field()
    layanan = scrapy.Field()

class TenagaItem(scrapy.Item):
    kode = scrapy.Field()
    grup = scrapy.Field()
    sdm = scrapy.Field()
    jumlah = scrapy.Field()



