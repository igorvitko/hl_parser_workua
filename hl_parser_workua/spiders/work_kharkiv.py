import scrapy


class WorkKharkivSpider(scrapy.Spider):
    name = 'work_kharkiv'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    def parse(self, response):

        for item in response.css('div#pjax-resume-list div.card.resume-link'):

            card_uri = item.css('h2 a::attr(href)').get()

            result = {
                'name': item.css('div b::text').get().strip(),
                'age': None,
                # 'link': card_uri,
                'position': item.css('h2 a::text').get()
            }

            yield response.follow(card_uri, self.parse_person, meta={
                'result': result
                })

    def parse_person(self, response):

        age = response.css('div.card dd::text').get()[:2]
        description = ' '.join(response.css('div.card > p::text').getall())
        description = ' '.join(description.split())

        people_info = response.meta['result']
        people_info['description'] = description
        people_info['age'] = age

        yield people_info
