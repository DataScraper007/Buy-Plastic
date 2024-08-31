import json
import urllib

import pandas as pd
import scrapy
from scrapy.cmdline import execute
from itertools import permutations
from itertools import product

from buyplastic.items import BplItem


class LinkExtractorSpider(scrapy.Spider):
    name = "bpl"

    def start_requests(self):
        yield scrapy.Request(
            url="https://buyplastic.com/categories",
            callback=self.extract_link
        )

    def extract_link(self, response, **kwargs):
        links = response.xpath('//ul[@class="productGrid"]//figure[@class="card-figure"]/a/@href').getall()
        for link in links:
            yield scrapy.Request(
                url="https://buyplastic.com/king-colorcore-plastic-sheet/",
                callback=self.parse
            )
            return
        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.extract_link
            )

    def parse(self, response, **kwargs):
        # get product id
        product_id = response.xpath('//input[@name="product_id"]/@value').get()

        product_name = response.xpath(
            '//div[@class="productView"]//h1[contains(@class,"productView-title")]/text()').get('')

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': 'fornax_anonymousId=a5f36f8b-a54a-4324-8a37-9d105702cb71; SF-CSRF-TOKEN=93e8344a-c8bc-473b-8fd6-5bc4bd44d4f2; XSRF-TOKEN=d6743bdff73b944cdf661cf77da14e4df9a458d1fd21799293e36c28564e7601; SHOP_SESSION_TOKEN=2fd268f1-e1dc-4b22-af6b-e39a7a6bee25; _gid=GA1.2.1368736830.1724998234; STORE_VISITOR=1; _gcl_au=1.1.1837268069.1724998236; _clck=fistk4%7C2%7Cfor%7C0%7C1703; lastVisitedCategory=0; _fbp=fb.1.1724998238982.761846094614836022; athena_short_visit_id=8358de41-7f10-4cc6-bfc5-4b637e9eddd6:1725005281; _ga=GA1.1.1126432091.1724998234; _uetsid=91ea21a0669611ef888add6ad919ac0c; _uetvid=91ea5920669611ef9cd14972e81111db; _ga_YBZ6F6339N=GS1.1.1725006041.2.1.1725009427.0.0.0; _clsk=190u0bi%7C1725011159624%7C11%7C1%7Cx.clarity.ms%2Fcollect; __cf_bm=.trtd9WI5v1zRklg2Cm7GvTJZfpwR_FdUuFE.kACbzg-1725011177-1.0.1.1-oT.bad7E_0H17Z13ZjvgUwg0KJ_1tuPhPUOCFE5x5l1ZFcPpGHJSQlCe3hBOaKf9_1iwytO4xX2jI_dnJpHR8w; _ga_50BLGJTDSB=GS1.1.1725005451.2.1.1725011284.60.0.0; Shopper-Pref=6553CB8D8DF3DB317A093EA9A457CAED310D2FF1-1725616188053-x%7B%22cur%22%3A%22USD%22%7D',
            'origin': 'https://buyplastic.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://buyplastic.com/products/multiwall-polycarbonate-sheet.html',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'stencil-config': '{}',
            'stencil-options': '{"render_with":"products/bulk-discount-rates"}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-requested-with': 'stencil-utils',
            'x-sf-csrf-token': '93e8344a-c8bc-473b-8fd6-5bc4bd44d4f2',
            'x-xsrf-token': 'd6743bdff73b944cdf661cf77da14e4df9a458d1fd21799293e36c28564e7601',
        }

        cookies = {
            'fornax_anonymousId': 'a5f36f8b-a54a-4324-8a37-9d105702cb71',
            'SF-CSRF-TOKEN': '93e8344a-c8bc-473b-8fd6-5bc4bd44d4f2',
            'XSRF-TOKEN': 'd6743bdff73b944cdf661cf77da14e4df9a458d1fd21799293e36c28564e7601',
            'SHOP_SESSION_TOKEN': '2fd268f1-e1dc-4b22-af6b-e39a7a6bee25',
            '_gid': 'GA1.2.1368736830.1724998234',
            'STORE_VISITOR': '1',
            '_gcl_au': '1.1.1837268069.1724998236',
            '_clck': 'fistk4%7C2%7Cfor%7C0%7C1703',
            'lastVisitedCategory': '0',
            '_fbp': 'fb.1.1724998238982.761846094614836022',
            'athena_short_visit_id': '8358de41-7f10-4cc6-bfc5-4b637e9eddd6:1725005281',
            '_ga': 'GA1.1.1126432091.1724998234',
            '_uetsid': '91ea21a0669611ef888add6ad919ac0c',
            '_uetvid': '91ea5920669611ef9cd14972e81111db',
            '_ga_YBZ6F6339N': 'GS1.1.1725006041.2.1.1725009427.0.0.0',
            '_clsk': '190u0bi%7C1725011159624%7C11%7C1%7Cx.clarity.ms%2Fcollect',
            '__cf_bm': '.trtd9WI5v1zRklg2Cm7GvTJZfpwR_FdUuFE.kACbzg-1725011177-1.0.1.1-oT.bad7E_0H17Z13ZjvgUwg0KJ_1tuPhPUOCFE5x5l1ZFcPpGHJSQlCe3hBOaKf9_1iwytO4xX2jI_dnJpHR8w',
            '_ga_50BLGJTDSB': 'GS1.1.1725005451.2.1.1725011284.60.0.0',
            'Shopper-Pref': '6553CB8D8DF3DB317A093EA9A457CAED310D2FF1-1725616188053-x%7B%22cur%22%3A%22USD%22%7D',
        }

        # get all variants
        variants = {}
        count = 0
        parameters_data = response.xpath(
            '//div[@data-product-option-change]/div[@class="form-field" and not (@data-product-attribute="textarea")]')

        for parameter in parameters_data:
            if parameter:
                value = parameter.xpath('./div[@class="form-option-wrapper"]/input/@name').get()
                keys = parameter.xpath('./div[@class="form-option-wrapper"]/input/@value').getall()

                variants[str(count)] = {}
                for key in keys:
                    variants[str(count)][key] = value
                count += 1

        lists = [list(values.keys()) for values in variants.values()]

        # Generate all combinations
        combinations = product(*lists)

        # Flatten the dictionary
        values_dict = {key: value for subdict in variants.values() for key, value in subdict.items()}

        for combo in list(combinations):
            payload = {}
            payload['action'] = 'add'
            payload['product_id'] = product_id
            name_with_variant = product_name
            for value in combo:
                payload[values_dict[value]] = value
                variant_name = response.xpath(
                    f'//label[contains(@data-product-attribute-value,"{value}")]//span[@class="form-option-variant"]/text() | //label[contains(@data-product-attribute-value,"{value}")]/span[contains(@class, "form-option-variant")]/@title').get()
                name_with_variant = name_with_variant + ' ' + variant_name

            if product_id:
                yield scrapy.FormRequest(
                    url=f"https://buyplastic.com/remote/v1/product-attributes/{product_id}",
                    method='POST',
                    headers=headers,
                    cookies=cookies,
                    formdata=payload,
                    callback=self.scrape_product_data,
                    dont_filter=True,
                    meta={'product_name': name_with_variant.strip(), 'page_url': response.url}
                )
            else:
                print("Product id is not found.")

    def scrape_product_data(self, response):
        page_url = response.meta['page_url']
        product_name = response.meta['product_name']
        json_data = json.loads(response.text)
        price = json_data['data']['price']['without_tax']['value']

        item = BplItem()
        item['name'] = product_name
        item['price'] = price
        item['url'] = page_url

        yield item


if __name__ == '__main__':
    execute('scrapy crawl bpl'.split())
