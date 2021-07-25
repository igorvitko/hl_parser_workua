import scrapy


class WorkKharkivSpider(scrapy.Spider):
    name = 'work_kharkiv'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    def parse(self, response):

        for item in response.css('div#pjax-resume-list div.card.resume-link'):

            card_uri = item.css('h2 a::attr(href)').get()
            # при таком запросе выборка возраста меньше из-за того, что селектор не имеет постоянного места
            # и может быть на второй или третьей позиции
            age = item.css('div > span:nth-child(3)::text').get()[:2]

            result = {
                'name': item.css('div b::text').get().strip(),
                'age': age,
                'position': item.css('h2 a::text').get()
            }

            yield response.follow(card_uri, self.parse_person, meta={
                'result': result
                })

        for page in response.css('ul.pagination li'):
            if page.css('a::text').get() == 'Наступна':
                yield response.follow(
                    page.css('a::attr(href)').get(),
                    self.parse
                )

    def parse_person(self, response):

        header = response.css('div.card > h2::text').get()
        description = ' '.join(response.css('div.card > p::text').getall())
        description = header + " " + ' '.join(description.split())

        people_info = response.meta['result']
        people_info['description'] = description

        yield people_info
