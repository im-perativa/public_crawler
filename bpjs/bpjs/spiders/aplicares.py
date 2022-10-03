import logging
import json
import scrapy

from bpjs.items import Faskes


class AplicaresSpider(scrapy.Spider):
    name = 'aplicares'
    URL = 'https://faskes.bpjs-kesehatan.go.id'

    def __init__(self,  *args, **kwargs):

        super(AplicaresSpider, self).__init__(*args, **kwargs)

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

    def start_requests(self):
        for prov_id in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34']:
            yield scrapy.Request(f'{self.URL}/aplicares/Referensi/dati2/{prov_id}', meta={'prov_id': prov_id})

    def parse(self, response):
        res = json.loads(response.body)
        for dati2 in res:
            for jnsppk in ["R", "P", "U", "G", "S", "B", "A", "O"]:
                form_data = {'params': {'pagination': {'start': 0, 'number': 1000}}, 'jnscari': 'carifaskes',
                             'jnscari1': 'bylocation', 'dati2ppk': f'{dati2["id"]}', 'jnsppk': jnsppk}
                yield scrapy.http.JsonRequest(f'{self.URL}/aplicares/Pencarian/getList', self.parse_dati2, method='POST', data=form_data, meta={
                    'prov_id': response.meta['prov_id'], 'dati2_id': dati2['id'], 'dati2_name': dati2['name']})

    def parse_dati2(self, response):
        res = json.loads(response.body)
        if 'row' in res:
            faskes_list = res['row']
            for faskes in faskes_list:
                try:
                    faskes_item = Faskes()

                    faskes_item['prov_id'] = response.meta['prov_id']
                    faskes_item['dati2_id'] = response.meta['dati2_id']
                    faskes_item['dati2_name'] = response.meta['dati2_name']
                    faskes_item['no'] = faskes['no']
                    faskes_item['kdppk'] = faskes['kdppk']
                    faskes_item['jnsppk'] = faskes['jnsppk']
                    faskes_item['nmppk'] = faskes['nmppk']
                    faskes_item['telpppk'] = faskes['telpppk']
                    faskes_item['nmjlnppk'] = faskes['nmjlnppk']
                    faskes_item['lat'] = faskes['lat']
                    faskes_item['lng'] = faskes['lng']
                    faskes_item['distance'] = faskes['distance']
                    faskes_item['vvip'] = faskes['vvip']
                    faskes_item['vip'] = faskes['vip']
                    faskes_item['utama'] = faskes['utama']
                    faskes_item['I'] = faskes['I']
                    faskes_item['II'] = faskes['II']
                    faskes_item['III'] = faskes['III']
                    faskes_item['ICU'] = faskes['ICU']
                    faskes_item['ICCU'] = faskes['ICCU']
                    faskes_item['NICU'] = faskes['NICU']
                    faskes_item['PICU'] = faskes['PICU']
                    faskes_item['IGD'] = faskes['IGD']
                    faskes_item['UGD'] = faskes['UGD']
                    faskes_item['BERSALIN'] = faskes['BERSALIN']
                    faskes_item['HCU'] = faskes['HCU']
                    faskes_item['ISOLASI'] = faskes['ISOLASI']

                    if faskes['jnsppk'] == 'R':
                        form_data = {"kdppk": faskes['kdppk'], "jnsppk": faskes['jnsppk']}

                        yield scrapy.http.JsonRequest(f'{self.URL}/aplicares/Pencarian/getData', self.parse_rs, method='POST', data=form_data, meta={'faskes_item': faskes_item})
                    else:
                        yield faskes_item
                except:
                    pass

    def parse_rs(self, response):
        res = json.loads(response.body)
        faskes_item = response.meta['faskes_item']
        try:
            faskes_item['tglhbspksppk'] = res['profil']['tglhbspksppk']
            faskes_item['jumlah_pelayanan'] = len(res['pelayanan'])
            faskes_item['jumlah_sarana'] = len(res['sarana'])

            faskes_item['jumlah_kamar_khusus'] = sum([obj['jumlah_kamar'] for obj in res['Khusus']])
            faskes_item['jumlah_kamar_i'] = sum([obj['jumlah_kamar'] for obj in res['satu']])
            faskes_item['jumlah_kamar_ii'] = sum([obj['jumlah_kamar'] for obj in res['dua']])
            faskes_item['jumlah_kamar_iii'] = sum([obj['jumlah_kamar'] for obj in res['tiga']])
            faskes_item['jumlah_kamar_vip'] = sum([obj['jumlah_kamar'] for obj in res['vip']])
            faskes_item['jumlah_kamar_lain'] = sum([obj['jumlah_kamar'] for obj in res['Lain']])
        except:
            pass

        yield faskes_item
