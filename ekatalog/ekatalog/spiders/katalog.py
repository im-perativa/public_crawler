import logging
import scrapy


class KatalogSpider(scrapy.Spider):
    name = 'katalog'
    allowed_domains = ['e-katalog.lkpp.go.id']
    start_urls = ['https://e-katalog.lkpp.go.id/id/search-produk?cat=5590&order=maxPrice&limit=1000']

    headers = {
        'Host': "e-katalog.lkpp.go.id",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv':'91.0) Gecko/20100101 Firefox/91.0",
        'Accept': "text/html, */*; q=0.01",
        'Accept-Language': "en-US,en;q=0.5",
        'Accept-Encoding': "gzip, deflate, br",
        'X-Requested-With': "XMLHttpRequest",
        'DNT': "1",
        'Connection': "keep-alive",
        'Referer': "https':'//e-katalog.lkpp.go.id/katalog/produk/detail/1470775?lang=id&type=general",
        'Cookie': "E_KATALOG_5_SESSION=e4804d3eece4abaf0bb671c6ee18744653a16fa3-___AT=9774e430348ee0128d2297e32fc71c25775e0165&___TS=1631097163369&___ID=3e2f6483-5c33-4a3c-bd04-cfdafd7e4b82; TS01db93b1=01661f96477e9c44e06bceee2d2a81d6bc5afacd1da7c186757d8bbeea79257bdd1a004b022518ccd369166e199f5ea0677e0ab251e7eacde0a64e3d28a1ed6d691c3c7924a841cf1da9480b7f3e3cbe1f140d250243f229ba2ecb7f890455dcbaa5af761d",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'Pragma': "no-cache",
        'Cache-Control': "no-cache",
    }
    
    def __init__(self,  *args, **kwargs):

        super(KatalogSpider, self).__init__(*args, **kwargs)

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
        product_link = response.css('.card-item .card-item-image a::attr(href)')

        for product in product_link:
            api_link = product.get().replace('?lang=id&type=general', '').replace(
                'katalog/produk/detail/', 'katalog.produkctr/getdetailproductcenter?id=')
            yield response.follow(api_link, self.parse_product, headers=self.headers)

    def parse_product(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        detail = response.css('.detail-description::text').getall()

        try:
            yield {
                'nama': detail[0].strip(),
                'merk': detail[1].strip(),
                'harga': extract_with_css('#detailhargaChange::text').replace('Rp ', '').replace('.', '').replace(',00', ''),
                'prosesor': detail[7].strip(),
                'type_model': detail[8].strip(),
                'ram': detail[9].strip(),
                'storage': detail[10].strip(),
                'vga': detail[11].strip(),
                'display': detail[12].strip(),
                'connectivity': detail[13].strip(),
                'description': detail[14].strip(),
                'url': response.url
            }
        except IndexError:
            pass
