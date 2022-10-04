# Public Crawler
A collection of crawler project for Indonesia dataset

## Contents

- [List](#list)
- [Usage](#usage)

## List

| Crawler  |      Description      |  Website |
|----------|-------------|------|
| [bpjs](https://github.com/im-perativa/public_crawler/tree/main/bpjs) | Healthcare facilities in Indonesia | [https://faskes.bpjs-kesehatan.go.id/aplicares/](https://faskes.bpjs-kesehatan.go.id/aplicares/) |
| [ekatalog](https://github.com/im-perativa/public_crawler/tree/main/ekatalog) | Procurement of goods and services for government institution |   [https://e-katalog.lkpp.go.id/](https://e-katalog.lkpp.go.id/) |
| [jobsid](https://github.com/im-perativa/public_crawler/tree/main/jobsid) | Job vacancy | [https://www.jobs.id/](https://www.jobs.id/) |
| [kpu](https://github.com/im-perativa/public_crawler/tree/main/kpu) | 2019 general election result | [https://pemilu2019.kpu.go.id](https://pemilu2019.kpu.go.id) |
| [master_bps](https://github.com/im-perativa/public_crawler/tree/main/master_bps) | Indonesia administrative list with bridging code between Statistics Indonesia and Ministry of Internal Affairs | [https://sig.bps.go.id/bridging-kode/index](https://sig.bps.go.id/bridging-kode/index) |

## Usage

```
pip install -r requirements.txt
cd <crawler_directory>
scrapy crawl <spider_name> -o result.csv
```
