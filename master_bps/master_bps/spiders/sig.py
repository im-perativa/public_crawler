from asyncio import constants
from master_bps.items import DesaItem

import json
import logging
import scrapy


class SigSpider(scrapy.Spider):
    name = 'sig'
    allowed_domains = ['sig.bps.go.id']
    start_urls = ['https://sig.bps.go.id/rest-bridging/getwilayah']

    def __init__(self,  *args, **kwargs):

        super(SigSpider, self).__init__(*args, **kwargs)

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        logFormatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        # file handler
        fileHandler = logging.FileHandler(f'log.txt')
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)

        # console handler
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)

    def parse(self, response):
        provinsi_list = json.loads(response.body)

        for provinsi in provinsi_list:
            print(provinsi)
            yield scrapy.Request(f'https://sig.bps.go.id/rest-bridging/getwilayah?level=kabupaten&parent={provinsi["kode_bps"]}',
                                 callback=self.parse_kabupaten,
                                 meta={'provinsi': provinsi}
                                 )

    def parse_kabupaten(self, response):
        provinsi = response.meta['provinsi']
        kabupaten_list = json.loads(response.body)

        for kabupaten in kabupaten_list:
            yield scrapy.Request(f'https://sig.bps.go.id/rest-bridging/getwilayah?level=kecamatan&parent={kabupaten["kode_bps"]}',
                                 callback=self.parse_kecamatan,
                                 meta={
                                     'provinsi': provinsi,
                                     'kabupaten': kabupaten,
                                 }
                                 )

    def parse_kecamatan(self, response):
        provinsi = response.meta['provinsi']
        kabupaten = response.meta['kabupaten']
        kecamatan_list = json.loads(response.body)

        for kecamatan in kecamatan_list:
            yield scrapy.Request(f'https://sig.bps.go.id/rest-bridging/getwilayah?level=desa&parent={kecamatan["kode_bps"]}',
                                 callback=self.parse_desa,
                                 meta={
                                     'provinsi': provinsi,
                                     'kabupaten': kabupaten,
                                     'kecamatan': kecamatan,
                                 }
                                 )

    def parse_desa(self, response):
        provinsi = response.meta['provinsi']
        kabupaten = response.meta['kabupaten']
        kecamatan = response.meta['kecamatan']
        desa_list = json.loads(response.body)

        for desa in desa_list:

            desa_item = DesaItem()
            desa_item['bps_provinsi_id'] = provinsi['kode_bps']
            desa_item['bps_provinsi'] = provinsi['nama_bps']
            desa_item['bps_kabupaten_id'] = kabupaten['kode_bps']
            desa_item['bps_kabupaten'] = kabupaten['nama_bps']
            desa_item['bps_kecamatan_id'] = kecamatan['kode_bps']
            desa_item['bps_kecamatan'] = kecamatan['nama_bps']
            desa_item['bps_desa_id'] = desa['kode_bps']
            desa_item['bps_desa'] = desa['nama_bps']
            desa_item['kemendagri_provinsi_id'] = provinsi['kode_dagri']
            desa_item['kemendagri_provinsi'] = provinsi['nama_dagri']
            desa_item['kemendagri_kabupaten_id'] = kabupaten['kode_dagri']
            desa_item['kemendagri_kabupaten'] = kabupaten['nama_dagri']
            desa_item['kemendagri_kecamatan_id'] = kecamatan['kode_dagri']
            desa_item['kemendagri_kecamatan'] = kecamatan['nama_dagri']
            desa_item['kemendagri_desa_id'] = desa['kode_dagri']
            desa_item['kemendagri_desa'] = desa['nama_dagri']

            yield desa_item
