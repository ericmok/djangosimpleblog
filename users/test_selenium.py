from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse_lazy

from selenium.webdriver.firefox.webdriver import WebDriver


class SeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SeleniumTests, cls).tearDownClass()

    def test_register_view(self):
        self.browser.get('%s/%s' % (self.live_server_url, reverse_lazy('users-register')))
        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('secret')
        #self.browser.find_element_by_xpath('//input[@value="Register"]').click()
        self.browser.find_element_by_id('button')

        self.assertIn('Register', self.browser.find_element_by_tag_name('body'))