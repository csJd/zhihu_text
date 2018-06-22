# -*- coding: utf-8 -*-

import scrapy
import os
from scrapy.shell import inspect_response
from scrapy.utils.conf import closest_scrapy_cfg

from util.tool import get_prot_root, get_abs_url


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/question/278969757']

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    #                     (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    #     'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    # }

    def parse(self, response):
        '''get scrapy shell in ipython

        '''
        inspect_response(response, self)
        # then in ipython
        # print(response.xpath('//strong/@title').extract())


if __name__ == '__main__':
    proj_root_dir = os.path.dirname(closest_scrapy_cfg())
    print(proj_root_dir)
    print(get_prot_root())
    print(get_abs_url('./test/ssdf'))


'''
in this folder
scrapy runspider test
'''

''' another way

# in cmd 
scrapy shell

# in pyhton
test_url = 'https://www.zhihu.com/question/275098818'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
}

req = scrapy.Request(test_url, headers=headers)
fetch(req)
# fetch a new response from the given request and update all related objects accordingly.

response.xpath('//strong/@title').extract()
'''
