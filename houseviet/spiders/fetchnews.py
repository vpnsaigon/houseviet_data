import scrapy


class FetchnewsSpider(scrapy.Spider):
    name = "fetchnews"
    allowed_domains = ["houseviet.vn"]
    start_urls = ["https://houseviet.vn"]
    titles = set()

    def start_requests(self):
        # urls list
        base_url = "https://houseviet.vn/nha-dat-ban"
        urls = [base_url]
        for i in range(1, 10): # max = 8000
            urls.append(base_url + f"/p{i}")
        
        # follow link
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        links = response.xpath('//div[@class="property-body"]/a')
        for link in links:
            link = link.xpath('./@href').get()
            yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):
        title = response.xpath('//h1/text()').get().strip()        
        date = response.xpath('//div[@class="d-flex align-items-center justify-content-between mt-3"]/div[4]/span/text()').get().strip()
        price = response.xpath('//div[@class="highlight-info pe-3"]/div/div/text()').get().strip()
        erea = response.xpath('//div[@class="highlight-info border-start ps-3"]/div[2]/text()').get().strip()
        address = response.xpath('//div[@class="article-overview"]/div[1]/span/text()').get().strip()

        if title and price and erea and address:
            # check note same title (same data)
            if title not in self.titles:
                self.titles.add(title) 

                yield {
                    'title': title,
                    'date': date,
                    'price': price,
                    'erea': erea,
                    'address': address
                }
