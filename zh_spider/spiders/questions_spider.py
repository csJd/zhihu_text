# -*- coding: utf-8 -*-
import json
import time
import scrapy
from util.tool import get_abs_url


class QuestionsSpider(scrapy.Spider):
    name = 'questions_spider'
    allowed_domains = ['zhihu.com']

    GET_LIMIT = '100'
    DATA_DIR = get_abs_url('data')

    filename_suffix = time.strftime('%y%m%d', time.localtime()) + '.txt'
    sysu_topic_id = '19608566'
    scut_topic_id = '19599737'
    gzhemc_topic_id = '19608544'

    questions_api_url = 'https://www.zhihu.com/api/v4/topics/' \
                        + gzhemc_topic_id + '/feeds/timeline_question?offset=0&limit=' + GET_LIMIT

    qa_api_suffix = '/answers?offset=0&include=data[*].is_normal%2Ccontent&limit=' + GET_LIMIT
    qa_api_urls = []
    qa_api_titles = []

    # topic_url = 'https://www.zhihu.com/topic/19608566/top-answers'
    # topic_api_url = 'https://www.zhihu.com/api/v4/topics/19608566/feeds/essence?offset=0&limit=' + GET_LIMIT
    # qa_api_url = '/api/v4/questions/34866229/answers?limit=5&offset=0&include=data[*].is_normal%2Ccontent'
    # answer_api_url = 'https://www.zhihu.com/api/v4/answers/60198194?include=content'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                       (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.questions_api_url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        print()
        resp = response.text

        jo = json.loads(resp)
        is_end = bool(jo.get('paging').get('is_end'))
        ja_data = jo.get('data')
        for item in ja_data:
            qa_api_url = item.get('target').get('url') + self.qa_api_suffix
            qa_api_title = item.get('target').get('title')
            q_created_timestamp = item['target']['created']
            q_create_time = time.strftime('%Y-%m-%d', time.localtime(q_created_timestamp))
            q_answer_count = item['target']['answer_count']
            self.qa_api_urls.append(qa_api_url)
            self.qa_api_titles.append(q_create_time + ', ' + str(q_answer_count) + ', ' + qa_api_title)
            # "create_time, answer_count, question_title"

        if not is_end:
            next_page_url = jo.get('paging').get('next')
            yield scrapy.Request(url=next_page_url, callback=self.parse, headers=self.headers)

        else:
            print(str(len(self.qa_api_urls)) + " questions crawled")
            urls_url = self.DATA_DIR + 'question_urls_gzhemc_' + self.filename_suffix
            with open(urls_url, 'w', encoding='utf-8') as urls_file:
                for url in self.qa_api_urls:
                    urls_file.write(url + '\n')
            titles_url = self.DATA_DIR + 'question_titles_gzhemc_' + self.filename_suffix
            cnt = 0
            with open(titles_url, 'w', encoding='utf-8') as titles_file:
                for title in self.qa_api_titles:
                    titles_file.write(title + '\n')
                    cnt += 1
            print(cnt)

# process = CrawlerProcess()
# process.crawl(QuestionsSpider)
# process.start()  # the script will block here until the crawling is finished
