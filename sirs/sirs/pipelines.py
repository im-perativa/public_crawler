# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class SirsPipeline:
    def process_item(self, item, spider):
        return item


class CSVperItem_Pipeline:

    def open_spider(self, spider):
        self.itemType_to_exporterAndCsvFile = {}     

    def process_item(self, item, spider):
        itemType = type(item).__name__ #item class name as str
        if itemType not in self.itemType_to_exporterAndCsvFile:
            csvFile = open(f'{itemType}.csv', 'wb')
            exporter = CsvItemExporter(csvFile)
            exporter.start_exporting()
            self.itemType_to_exporterAndCsvFile[itemType] = (exporter, csvFile)
        exporter = self.itemType_to_exporterAndCsvFile[itemType][0]
        exporter.export_item(item)
        return item

    def close_spider(self, spider):
        for exporter, csvFile in self.itemType_to_exporterAndCsvFile.values():
            exporter.finish_exporting()
            csvFile.close()