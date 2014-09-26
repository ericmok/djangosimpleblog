from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse_lazy, reverse
from users.models import User

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

class SeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SeleniumTests, cls).tearDownClass()

    def xtest_register_view(self):
        self.browser.get('%s%s' % (self.live_server_url, reverse('users-register')))
        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.browser.find_element_by_name("password1")
        password_input.send_keys('secret')
        password_input = self.browser.find_element_by_name("password2")
        password_input.send_keys('not matching secret')
        
        self.assertIn('Register', self.browser.find_element_by_tag_name('body').text)
        button = self.browser.find_element_by_css_selector('form input[type="submit"]')
        button.click()
        
        self.assertEqual(User.objects.count(), 0)

        self.browser.get('%s%s' % (self.live_server_url, reverse('users-register')))
        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys('myuser')

        self.browser.find_element_by_name("email").send_keys("tim@google.com")

        password_input = self.browser.find_element_by_name("password1")
        password_input.send_keys('secret')
        password_input = self.browser.find_element_by_name("password2")
        password_input.send_keys('secret')
        
        self.assertIn('Register', self.browser.find_element_by_tag_name('body').text)
        button = self.browser.find_element_by_css_selector('form input[type="submit"]')
        button.click()

        WebDriverWait(self.browser, 50)
        self.assertEqual(User.objects.count(), 1)