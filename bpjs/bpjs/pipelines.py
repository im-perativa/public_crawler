# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class BpjsPipeline:
    def process_item(self, item, spider):
        return item


class CSVperItemPipeline:

    def open_spider(self, spider):
        self.itemTypeToExport = {}
        if not os.path.exists('result'):
            os.makedirs('result')

    def process_item(self, item, spider):
        itemType = type(item).__name__ 
        if itemType not in self.itemTypeToExport:
            csvFile = open(os.path.join('result', f'{itemType}.csv'), 'wb')
            exporter = CsvItemExporter(csvFile)
            exporter.start_exporting()
            self.itemTypeToExport[itemType] = (exporter, csvFile)
        exporter = self.itemTypeToExport[itemType][0]
        exporter.export_item(item)
        return item

    def close_spider(self, spider):
        for exporter, csvFile in self.itemTypeToExport.values():
            exporter.finish_exporting()
            csvFile.close()