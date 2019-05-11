import scrapy

from database.handler import add_record


class JobSpider(scrapy.Spider):
    name = "jobs"
    start_urls = [
        'https://news.ycombinator.com/jobs',
    ]

    def parse(self, response):
        for job in response.css('a.storylink::text').getall():
            job = job.lower()

            if 'and hiring' in job and 'is ':
                description_index = job.index('is ')
                hiring_index = job.index(' and hiring')
                job = job.replace(job[description_index:hiring_index], '')

            if ' raised ' in job and ' and is ' in job:
                profit_index = job.index(' raised ')
                hiring_index = job.index(' and is ')
                job = job.replace(job[profit_index:hiring_index], '')

            job = job.replace('and is looking', 'looking')
            job = job.replace('is looking', 'looking')
            job = job.replace('is hiring', 'looking')
            job = job.replace('and hiring', 'looking')
            job = job.replace('hiring', 'looking')
            company_name = ''
            job_title = ''
            location = ''

            try:
                location_index = job.index('in ')
            except ValueError:
                location_index = -1

            if location_index != -1:
                location = job[location_index:]
                job = job.replace(location, '')
                try:
                    quality_index = location.index(':')
                    location = location.replace(location[quality_index:], '')
                except ValueError:
                    pass

                try:
                    description_index = location.index('–')
                    location = location.replace(location[description_index:], '')
                except ValueError:
                    pass

                location = location.replace('in ', '')
                location = location.replace('our ', '')
                location = location.replace(' office', '')

            if 'looking' in job:
                job_tokens = job.split('looking')
                if len(job_tokens) > 1:
                    company_name = job_tokens[0]
                    job_title = job_tokens[1]
                else:
                    company_name = ''
                    job_title = job_tokens[0]
            elif ' for ' in job:
                job_tokens = job.split(' for ')
                if len(job_tokens) > 1:
                    job_title = job_tokens[0]
                    company_name = job_tokens[1]

            add_record(company_name, job_title, location)

            # pagination
            next_page_url = response.css('a.morelink::attr(href)').extract_first()
            if next_page_url:
                next_page_url = response.urljoin(next_page_url)
                yield scrapy.Request(url=next_page_url, callback=self.parse)
