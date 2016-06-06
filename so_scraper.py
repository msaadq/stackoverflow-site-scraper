import requests
from lxml import html


class so_scraper:
    base_url = "https://stackoverflow.com"  # Base URL for the SO website
    login_url = base_url + "/users/login"  # Login page URL
    session_request = []  # Independent instance of a web session request
    credentials = []  # Dictionary of login credentials with auth token
    main_page = []  # Main HTML page saved after successful login
    questions = []  # HTML element containing the sub elements of all the top questions belonging to class "question-mini-list"
    page_title = ""  # Title of the current page

    def __init__(self, email, password):

        """
        Initiates the session and Logs in with the provided credentials

        :param email:
        :param password:
        :return:
        """

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
        self.page_title = str(self.main_page.xpath("//title/text()")[0])

        if self.page_title == "Stack Overflow":
            print "Login Successful" + "\n"
            self.questions = self.main_page.xpath("//div[@id='question-mini-list']")[0]
        else:
            print "Invalid Credentials" + "\n"

    def _get_reputation(self):

        """
        Parses the HTML page for reputation score

        :return: reputation as int
        """

        return int(str(self.main_page.xpath('//span[@class="reputation"]/text()')[0]).strip())

    def _get_ques_titles(self):

        """
        Parses the HTML page for all "Top Questions" titles

        :return: list of titles
        """

        return self.questions.xpath("//a[@class='question-hyperlink']/text()")

    def _get_ques_links(self):

        """
        Parses the HTML page for all "Top Questions" titles

        :return: list of questions links
        """

        return [self.base_url + link for link in self.questions.xpath("//a[@class='question-hyperlink']/@href")]

    def display_data(self):

        """
        Displays the reputation score along with all top questions and links in a neat format

        :return: none
        """

        try:
            print "Reputation: " + str(self._get_reputation()) + "\n"

            ques_titles = self._get_ques_titles()
            ques_links = self._get_ques_links()

            for i in xrange(len(ques_titles)):
                print "Question: " + str(i + 1)
                print ques_titles[i]
                print ques_links[i] + "\n"

        except:
            print "You are not logged in!"
