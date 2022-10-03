import json
import logging
import scrapy


from kpu.items import PilpresItem, PilegItem


class KpuSpider(scrapy.Spider):
    name = 'kpu'
    start_urls = [
        'https://pemilu2019.kpu.go.id/static/json/wilayah/0.json'
    ]

    def __init__(self,  *args, **kwargs):

        super(KpuSpider, self).__init__(*args, **kwargs)

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
        provinsis = json.loads(response.body)
        provinsis = {key: value['nama'] for key, value in provinsis.items()}

        for provinsi in provinsis.items():
            yield scrapy.Request('https://pemilu2019.kpu.go.id/static/json/wilayah/{}.json'.format(
                provinsi[0]),
                callback=self.parse_kabupaten,
                meta={
                        'provinsi': provinsi
                    }
            )


    def parse_kabupaten(self, response):
        kabupatens = json.loads(response.body)
        kabupatens = {key: value['nama'] for key, value in kabupatens.items()}

        for kabupaten in kabupatens.items():
            yield scrapy.Request('https://pemilu2019.kpu.go.id/static/json/wilayah/{}/{}.json'.format(
                response.meta['provinsi'][0], kabupaten[0]),
                callback=self.parse_kecamatan,
                meta={
                        'provinsi': response.meta['provinsi'],
                        'kabupaten': kabupaten
                    }
            )


    def parse_kecamatan(self, response):
        kecamatans = json.loads(response.body)
        kecamatans = {key: value['nama'] for key, value in kecamatans.items()}

        for kecamatan in kecamatans.items():
            yield scrapy.Request('https://pemilu2019.kpu.go.id/static/json/wilayah/{}/{}/{}.json'.format(
                response.meta['provinsi'][0], response.meta['kabupaten'][0], kecamatan[0]),
                callback=self.parse_kelurahan,
                meta={
                        'provinsi': response.meta['provinsi'],
                        'kabupaten': response.meta['kabupaten'],
                        'kecamatan': kecamatan
                    }
            )


    def parse_kelurahan(self, response):
        kelurahans = json.loads(response.body)
        kelurahans = {key: value['nama'] for key, value in kelurahans.items()}

        for kelurahan in kelurahans.items():
            yield scrapy.Request('https://pemilu2019.kpu.go.id/static/json/wilayah/{}/{}/{}/{}.json'.format(
                response.meta['provinsi'][0], response.meta['kabupaten'][0], response.meta['kecamatan'][0], kelurahan[0]),
                callback=self.parse_tps,
                meta={
                        'provinsi': response.meta['provinsi'],
                        'kabupaten': response.meta['kabupaten'],
                        'kecamatan': response.meta['kecamatan'],
                        'kelurahan': kelurahan,
                    }
            )


    def parse_tps(self, response):
        tpss = json.loads(response.body)
        tpss = {key: value['nama'] for key, value in tpss.items()}

        for tps in tpss.items():
            # Pilpres
            yield scrapy.Request('https://pemilu2019.kpu.go.id/static/json/hhcw/ppwp/{}/{}/{}/{}/{}.json'.format(
                response.meta['provinsi'][0], response.meta['kabupaten'][0], response.meta['kecamatan'][0], response.meta['kelurahan'][0], tps[0]),
                callback=self.parse_pilpres,
                meta={
                        'provinsi': response.meta['provinsi'],
                        'kabupaten': response.meta['kabupaten'],
                        'kecamatan': response.meta['kecamatan'],
                        'kelurahan': response.meta['kelurahan'],
                        'tps': tps
                    }
            )
            # Pileg
            for tipe in ['dprri', 'dprdprov', 'dprdkab']:
                yield scrapy.Request('https://pemilu2019.kpu.go.id/static/json/hhcw/{}/{}/{}/{}/{}/{}.json'.format(
                    tipe, response.meta['provinsi'][0], response.meta['kabupaten'][0], response.meta['kecamatan'][0], response.meta['kelurahan'][0], tps[0]),
                    callback=self.parse_pileg,
                    meta={
                            'tipe': tipe,
                            'provinsi': response.meta['provinsi'],
                            'kabupaten': response.meta['kabupaten'],
                            'kecamatan': response.meta['kecamatan'],
                            'kelurahan': response.meta['kelurahan'],
                            'tps': tps
                        }
                )


    def parse_pilpres(self, response):

        pilpres = json.loads(response.body)
        pilpres_item = PilpresItem()

        pilpres_item['url'] = response.request.url
        pilpres_item['provinsi_id'] = response.meta['provinsi'][0]
        pilpres_item['provinsi'] = response.meta['provinsi'][1]
        pilpres_item['kabupaten_id'] = response.meta['kabupaten'][0]
        pilpres_item['kabupaten'] = response.meta['kabupaten'][1]
        pilpres_item['kecamatan_id'] = response.meta['kecamatan'][0]
        pilpres_item['kecamatan'] = response.meta['kecamatan'][1]
        pilpres_item['kelurahan_id'] = response.meta['kelurahan'][0]
        pilpres_item['kelurahan'] = response.meta['kelurahan'][1]
        pilpres_item['tps_id'] = response.meta['tps'][0]
        pilpres_item['tps'] = response.meta['tps'][1]
        pilpres_item['pemilih'] = pilpres['pemilih_j'] if pilpres != {} else None
        pilpres_item['pengguna'] = pilpres['pengguna_j'] if pilpres != {} else None
        pilpres_item['suara_sah'] = pilpres['suara_sah'] if pilpres != {} else None
        pilpres_item['suara_tidak_sah'] = pilpres['suara_tidak_sah'] if pilpres != {} else None
        pilpres_item['suara_total'] = pilpres['suara_total'] if pilpres != {} else None
        pilpres_item['calon_21'] = pilpres['chart']['21'] if pilpres != {} else None
        pilpres_item['calon_22'] = pilpres['chart']['22'] if pilpres != {} else None
        pilpres_item['timestamp'] = pilpres['ts'] if pilpres != {} else None
        yield pilpres_item


    def parse_pileg(self, response):

        pileg = json.loads(response.body)
        pileg_item = PilegItem()

        pileg_item['url'] = response.request.url
        pileg_item['tipe'] = response.meta['tipe']
        pileg_item['provinsi_id'] = response.meta['provinsi'][0]
        pileg_item['provinsi'] = response.meta['provinsi'][1]
        pileg_item['kabupaten_id'] = response.meta['kabupaten'][0]
        pileg_item['kabupaten'] = response.meta['kabupaten'][1]
        pileg_item['kecamatan_id'] = response.meta['kecamatan'][0]
        pileg_item['kecamatan'] = response.meta['kecamatan'][1]
        pileg_item['kelurahan_id'] = response.meta['kelurahan'][0]
        pileg_item['kelurahan'] = response.meta['kelurahan'][1]
        pileg_item['tps_id'] = response.meta['tps'][0]
        pileg_item['tps'] = response.meta['tps'][1]
        pileg_item['pemilih'] = pileg['pemilih_j'] if pileg != {} else None
        pileg_item['pengguna'] = pileg['pengguna_j'] if pileg != {} else None
        pileg_item['suara_sah'] = pileg['suara_sah'] if pileg != {} else None
        pileg_item['suara_tidak_sah'] = pileg['suara_tidak_sah'] if pileg != {} else None
        pileg_item['suara_total'] = pileg['suara_total'] if pileg != {} else None
        for i in range(1, 21):
            # kasus partai di aceh
            try:
                pileg_item['partai_{}'.format(i)] = pileg['chart'][str(i)] if pileg != {} else None
            except:
                pass
        pileg_item['timestamp'] = pileg['ts'] if pileg != {} else None
        yield pileg_item