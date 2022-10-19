import json
import logging
import pandas as pd
import scrapy

from sirs.items import RsItem, TempatTidurItem, LayananItem, TenagaItem


class SirsKemkesSpider(scrapy.Spider):
    name = 'sirs_kemkes'
    allowed_domains = ['sirs.kemkes.go.id']
    start_urls = ['https://sirs.kemkes.go.id/fo/home/rekap_rs_all']

    def __init__(self,  *args, **kwargs):

        super(SirsKemkesSpider, self).__init__(*args, **kwargs)

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
        rs_list = json.loads(response.body)
        rs_list = rs_list['data']

        for rs in rs_list:
            rs_item = RsItem()

            rs_item['kode'] = rs['kode']
            rs_item['nama'] = rs['nama']
            rs_item['kabupaten'] = rs['kab']
            rs_item['alamat'] = rs['alamat'].strip()
            rs_item['telepon'] = rs['TELEPON']
            rs_item['pemilik'] = rs['pemilik']
            rs_item['kelas'] = rs['kelas']

            yield scrapy.Request(f'https://sirs.kemkes.go.id/fo/home/profile_rs/{rs_item["kode"]}',
                    callback=self.parse_rs_detail,
                    meta={'rs_item': rs_item})

    def parse_rs_detail(self, response):
        rs_item = response.meta['rs_item']

        rs_item['jenis'] = response.css('li.list-group-item:nth-child(2) > a:nth-child(2)::text').get()
        rs_item['status_blu'] = response.css('li.list-group-item:nth-child(4) > a:nth-child(2)::text').get()
        rs_item['direktur'] = response.css('li.list-group-item:nth-child(6) > a:nth-child(2)::text').get()
        rs_item['luas_tanah'] = response.css('li.list-group-item:nth-child(7) > a:nth-child(2)::text').get()
        rs_item['luas_bangunan'] = response.css('li.list-group-item:nth-child(8) > a:nth-child(2)::text').get()

        df_tempat_tidur = pd.DataFrame({
            'kelas': response.css('.user-block > table:nth-child(1) > tbody > tr > td:nth-child(2)::text').getall(), 
            'jumlah': response.css('.user-block > table:nth-child(1) > tbody > tr > td:nth-child(3)::text').getall() 
            })

        for i, row in df_tempat_tidur.iterrows():
            tempattidur_item = TempatTidurItem()
            tempattidur_item['kode'] = rs_item['kode']
            tempattidur_item['kelas'] = row['kelas'].strip()
            tempattidur_item['jumlah'] = row['jumlah']

            yield tempattidur_item

        df_layanan = pd.DataFrame({
            'layanan': response.css('#example6 > tbody:nth-child(2) > tr > td:nth-child(2)::text').getall()
        }) 

        for i, row in df_layanan.iterrows():
            layanan_item = LayananItem()
            layanan_item['kode'] = rs_item['kode']
            layanan_item['layanan'] = row['layanan'].strip()

            yield layanan_item
        
        df_tenaga = pd.DataFrame({
            'grup': response.css('#example7 > tbody:nth-child(2) > tr > td:nth-child(2)::text').getall(), 
            'sdm': response.css('#example7 > tbody:nth-child(2) > tr > td:nth-child(3)::text').getall(),
            'jumlah': response.css('#example7 > tbody:nth-child(2) > tr > td:nth-child(4)::text').getall(),
            })

        for i, row in df_tenaga.iterrows():
            tenaga_item = TenagaItem()
            tenaga_item['kode'] = rs_item['kode']
            tenaga_item['grup'] = row['grup'].strip()
            tenaga_item['sdm'] = row['sdm'].strip()
            tenaga_item['jumlah'] = row['jumlah']

            yield tenaga_item
        
        yield rs_item