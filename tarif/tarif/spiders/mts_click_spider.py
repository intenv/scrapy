# -*- coding: utf-8 -*-
import scrapy
import string
from scrapy_splash import SplashRequest

# script="""
# function main(splash)
#     splash:wait(3)
#     splash:runjs("document.querySelector('div.range-slider__scale').querySelectorAll('div')[2].click()")
#     splash:wait(3)
#     return {
#         html = splash:html(),
#     }
# end
# """

script="""
function main(splash)
    splash:wait(3)
    splash:runjs("document.querySelector('div.range-slider__scale').querySelectorAll('div')[2].click()")
    splash:wait(3)
    return {
        html = splash:evaljs("document.title"),
    }
end
"""

script="""
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  assert(splash:runjs("document.querySelector('div.range-slider__scale').querySelectorAll('div')[1].click()"))
  assert(splash:wait(0.5))
  return {
    png = splash:png(),
    html = splash:html(),
  }
end
"""

# script=u"""
# function main(splash)
#   assert(splash:wait(30))
#   assert(splash:runjs("document.querySelector('div.range-slider__scale').querySelectorAll('div')[2].click()"))
#   assert(splash:wait(30))
#   return splash:html()
# end
# """
class Mts_ClickSpider(scrapy.Spider):
    name = "mts_click"

    # def start_requests(self):
    #     urls = [
    #         'https://moskva.mts.ru/personal/mobilnaya-svyaz/tarifi/vse-tarifi/tarifishhe'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.product_info_calculate)


    def start_requests(self):
        urls = [
            'https://moskva.mts.ru/personal/mobilnaya-svyaz/tarifi/vse-tarifi/tarifishhe'
        ]

        for url in urls:
            yield SplashRequest(url=url, callback=self.product_info_calculate,
                                endpoint='execute'
                                # , args={'wait': 3}
                                , args = {'lua_source': script}
                                #, meta={'yahoo_url': url}
                                )



    def product_info_calculate(self, response):
        productCalck = response.xpath('*//div[@class="product-info-calculate"]')
        # response.xpath('*//div[@class="product-info-calculate"]//div[child::span[text()="800 минут и&nbsp;800 SMS"]]')

        ttt= response.xpath('*//div[@class="product-info-calculate"]//div[child::span[text()!="800 SMS"]]/span/text()').extract()
        print ttt
        # for line in detail.xpath('*//table[@class="tariffTable"]//tr//text()').extract():
        #     if string.strip(line) not in [None, u'']:
        #         print string.strip(line)
        #     # yield item
        # result = productCalck.xpath('*[text]/text()')
        # '/html/body/div[3]/div/div[1]/div[4]/div/div/div[2]/div/div[2]/keyparameters/package-configurator/div/div[1]/optionslider/div/div[2]/div/div[2]/div[2]'
        result = productCalck.xpath('*//span[@class="js-tariff-price"]/text()')
        print result.extract_first()
        yield result.extract()

