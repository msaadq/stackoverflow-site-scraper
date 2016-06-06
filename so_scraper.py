import requests
from lxml import html


class so_scraper:
    base_url = "https://stackoverflow.com"
    login_url = base_url + "/users/login"
    session_request = []
    credentials = []
    main_page = []
    questions = []

    def __init__(self, email, password):
        self.session_request = requests.session()
        result = self.session_request.get(self.login_url)
        login_page = html.fromstring(result.text)
        token = list(set(login_page.xpath("//input[@name='fkey']/@value")))[0]

        self.credentials = {
            "email": email,
            "password": password,
            "fkey": token
        }

        result = self.session_request.post(
            self.login_url,
            data=self.credentials,
            headers=dict(referer=self.login_url)
        )

        self.main_page = html.fromstring(result.content)
        self.questions = self.main_page.xpath("//div[@id='question-mini-list']")[0]

    def get_reputation(self):
        return int(str(self.main_page.xpath('//span[@class="reputation"]/text()')[0]).strip())

    def get_ques_titles(self):
        return self.questions.xpath("//a[@class='question-hyperlink']/text()")

    def get_ques_links(self):
        return [self.base_url + link for link in self.questions.xpath("//a[@class='question-hyperlink']/@href")]

    def display_data(self):
        print "Reputation: " + str(self.get_reputation()) + "\n"

        ques_titles = self.get_ques_titles()
        ques_links = self.get_ques_links()

        for i in xrange(len(ques_titles)):
            print "Question: " + str(i + 1)
            print ques_titles[i]
            print ques_links[i] + "\n"
