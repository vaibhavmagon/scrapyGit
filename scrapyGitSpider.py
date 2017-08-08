import scrapy

class LoginSpider(scrapy.Spider):
    name = 'ScrapyGit'
    start_urls = ['https://github.com/login']
    allowed_domains = ['github.com']

    def parse(self, response):
        ele = scrapy.FormRequest.from_response(
            response,
            formdata={'login': 'USER_NAME', 'password': 'PASSWORD'},
            callback=self.after_login
        )
        return ele


    def after_login(self, response):
        if "Incorrect username or password" in response.body:
            self.logger.error("Login failed")
            return
        else:
            myList = []
            for x in response.css('ul#repo_listing li'):
                ele = x.css('a::attr(data-ga-click)')[0].extract()
                fork = ele.split(" ")[9].split(":")[1]
                if fork == "false":
                    repo =  x.css('span.repo::text')[0].extract()
                    link = 'https://github.com' + x.css('a::attr(href)')[0].extract()
                    type = ele.split(" ")[8].split(":")[1]
                    myList.append(dict(repo=repo, link=link, type=type))

            return myList


