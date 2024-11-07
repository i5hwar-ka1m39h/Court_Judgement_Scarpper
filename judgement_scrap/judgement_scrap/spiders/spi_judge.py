import scrapy



class SpiJudgeSpider(scrapy.Spider):
    name = "spi_judge"
    allowed_domains = ["indiankanoon.org"]
    start_urls = ["https://indiankanoon.org/search/?formInput=doctypes%3A%20bombay%20fromdate%3A%201-1-2024%20todate%3A%2031-12-2024&pagenum=0"]

    def parse(self, response):

      

        #get all the result on the given page it should be 10 result per page
        all_result = response.css('div.result')

        #for each result go the individual result page and extract the data from it for that use parse_result in callback
        for result in all_result:
            relative_url = result.css('div.result_title a::attr(href)').get()
            yield response.follow(relative_url, callback=self.parse_result)
                
        #check on the given page next button exists or not if exist then repeate the process by calling the parse of self
        next_page = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page:
            # Use response.follow to handle relative URLs and call parse on the next page
            yield response.follow(next_page, callback=self.parse)



    def parse_result(self, response):
        court_name = response.css('div.judgments h2.docsource_main::text').getall()
        case_name = response.css('div.judgments h2.doc_title::text').getall()
        author_name = response.css('div.judgments h3.doc_author a::text').getall()
        bench = response.css('div.judgments h3.doc_bench a::text').getall()
        html_data = response.css('div.judgments').getall()
        
        
        yield{
            'court_name': court_name,
            'case_name': case_name,
            'author_name': author_name,
            'bench': bench,
            'html_data': html_data
        }