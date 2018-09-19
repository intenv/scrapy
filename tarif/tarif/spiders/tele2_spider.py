# -*- coding: utf-8 -*-
import scrapy
import string

class Tele2Spider(scrapy.Spider):
    name = "tele2"

    def start_requests(self):
        urls = [
            'https://msk.shop.tele2.ru/tariff'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseTarifList)

    def parseTarifList(self, response):
        for tarif in response.xpath('/html/body/div[2]/div[2]/div/div[3]/div[2]/div[3]/div[2]/div/section'):
            tarifName = tarif.xpath('a[1]/span/div/text()').extract_first()
            tarifPage = tarif.xpath('a[1]/@href').extract_first()

            # yield scrapy.Request(response.urljoin(tarifPage), callback = self.parseTarifDetails)
            item = {
                'text': tarifName,
                'link': tarifPage,
                # 'detail': scrapy.Request(response.urljoin(tarifPage), callback = self.parseTarifDetails)
            }
            print item
            yield scrapy.Request(response.urljoin(tarifPage), callback=self.parseTarifDetails)
            # yield item

    def parseTarifDetails(self, response):
        detail = response.xpath('/html/body/div[2]/div[2]/div/div[3]/div[2]/div[2]/div[2]')
        service = detail.xpath('div[1]/table/tbody/tr/td[1]/text()').extract_first()
        quant = detail.xpath('div[1]/table/tbody/tr/td[2]/text()').extract_first()
        print {service : quant}

        # options = detail.xpath('div[2]/table[2]/tbody/tr')
        options = detail.xpath('*//table[@class="tariffTable"]//tr')
        # "/html/body/div[2]/div[2]/div/div[3]/div[2]/div[2]/div[2]/div[2]/table[2]/tbody/tr[1]"

        # for option in options:
        #     type = option.xpath('td/h3/text()').extract_first()
        #     desc = option.xpath('td[1]/text()').extract_first()
        #     value = option.xpath('td[2]/text()').extract_first()
        #     print type, desc, value
        #     yield {type : {desc : value}}

        for line in detail.xpath('*//table[@class="tariffTable"]//tr//text()').extract():
            if string.strip(line) not in [None, u'']:
                print string.strip(line)