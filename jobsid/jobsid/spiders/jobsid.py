import logging
import scrapy
import unicodedata

from jobsid.items import Ads


def clean(text):
    return unicodedata.normalize('NFKD', ' '.join(text.replace('\n', '').split()))


class JobsidSpider(scrapy.Spider):
    name = 'jobsid'
    start_urls = [
        'https://www.jobs.id/berkas/industri'
    ]

    def __init__(self,  *args, **kwargs):

        super(JobsidSpider, self).__init__(*args, **kwargs)

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
        industry_urls = response.css('ul > li > a ::attr(href)').getall()
        industry_urls = [i for i in industry_urls if 'industri=' in i]

        for industry_url in industry_urls:
            yield scrapy.Request(f'{industry_url}&halaman=1', callback=self.parse_industry, meta={'page': 1})

    def parse_industry(self, response):
        industry = response.css('h1.search-title > span ::text').get().replace('Lowongan Kerja ', '')
        ads_urls = [ads_url.css('h3 > a.bold ::attr(href)').get() for ads_url in response.css('div.single-job-ads')]
        next_page = response.meta['page'] + 1

        # recursively until no more ads found for this industry
        if len(ads_urls) > 0:
            for ads_url in ads_urls:
                yield scrapy.Request(ads_url, callback=self.parse_ads, meta={'industry': industry})

            yield scrapy.Request(f'{response.url.split("&")[0]}&halaman={next_page}', callback=self.parse_industry, meta={'page': next_page})

    def parse_ads(self, response):
        ads = Ads()
        ads['url'] = response.url
        ads['industry'] = response.meta['industry']
        # get job info
        ads['title'] = clean(response.css('h1.clear-top.bold ::text').get())
        ads['location'] = response.css('span.location ::text').get().replace(' dan ', '')
        infos = response.css('div.col-xs-12.col-sm-6.col-md-4 > h4')

        for info in infos:
            if clean(info.css('small ::text').get()) == 'Pengalaman Kerja:':
                ads['experience'] = clean(info.css('span.semi-bold ::text').get())
            elif clean(info.css('small ::text').get()) == 'Bidang Pekerjaan:':
                ads['category'] = info.css('a.cyan.semi-bold ::text').get()
            elif clean(info.css('small ::text').get()) == 'Gaji:':
                salary = info.css('span.semi-bold ::text').getall()
                if len(salary) == 1:
                    ads['salary_currency'], ads['salary_min'], ads['salary_max'] = [None, None, None]
                elif len(salary) == 3:
                    ads['salary_currency'], ads['salary_min'], ads['salary_max'] = map(
                        lambda x: x.replace('.', ''), salary)

        ads['description'] = clean('; '.join(response.css('div.job_desc > div > ul > li ::text').getall()))
        ads['requirement'] = clean('; '.join(response.css('div.job_req > ul > li ::text').getall()))
        ads_time = response.css('div.col-xs-6 > p.text-gray::text').getall()
        if ads_time:
            ads['ads_start'] = clean(ads_time[0]).replace('Diiklankan sejak ', '')
            ads['ads_end'] = clean(ads_time[1]).replace('Ditutup pada ', '')

        # get company info
        ads['company'] = response.css('a > strong.text-muted ::text').get()
        company_infos = response.css('div.company-profile > div.panel-body > p')
        for company_info in company_infos:
            if clean(company_info.css('small ::text').get()) == 'Industri:':
                ads['company_industry'] = company_info.css('a.semi-bold ::text').get()
            elif clean(company_info.css('small ::text').get()) == 'Ukuran Perusahaan:':
                ads['company_size'] = company_info.css('b.semi-bold ::text').get()
            elif clean(company_info.css('small ::text').get()) == 'Kendaraan Umum Terdekat:':
                ads['company_nearby_transportation'] = company_info.css('b.semi-bold ::text').get()
            elif clean(company_info.css('small ::text').get()) == 'Kantor Pusat:':
                ads['company_hq'] = company_info.css('b.semi-bold ::text').get()
            elif clean(company_info.css('small ::text').get()) == 'Tautan Eksternal:':
                ads['company_web'] = company_info.css('a.semi-bold ::attr(href)').get()

        yield ads
