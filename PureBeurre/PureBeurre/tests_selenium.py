import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from users.models import User


class SeleniumFunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        capabilities = DesiredCapabilities().FIREFOX
        #travis
        #username = os.environ["SAUCE_USERNAME"]
        #access_key = os.environ["SAUCE_ACCESS_KEY"]
        #capabilities["tunnel-identifier"] = os.environ["TRAVIS_JOB_NUMBER"]
        #capabilities["build"] = os.environ["TRAVIS_BUILD_NUMBER"]
        #capabilities["tags"] = [os.environ["TRAVIS_PYTHON_VERSION"], "CI"]
        #hub_url = "%s:%s@localhost:4445" % (username, access_key)
        #cls.driver = webdriver.Remote(desired_capabilities=capabilities, command_executor="http://%s/wd/hub" % hub_url)
        #end travis
        capabilities["marionette"] = True
        binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        options = Options()
        options.set_headless(headless=True)
        #options.binary = binary
        cls.driver = webdriver.Firefox(options=options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_user_journey_create_an_account(self):
        driver = self.driver
        # import pdb; pdb.set_trace()
        server = self.live_server_url
        driver.get("{}".format(server))
        # check if we are at the right place
        self.assertEqual(driver.title, 'Pur Beurre - Home')
        # At this point, if user want to create an account,
        # he has to go to the login page and then to the signup page
        # user clicks to this link to go to login page
        driver.find_element_by_id('link_to_login').click()
        # check if we are inside the login page
        self.assertEqual(driver.title, 'Pur Beurre - Login')
        # user has not yet an account so he wants to go to the signup page
        # user clicks on this link to go to the signup page
        driver.find_element_by_id('link_to_register').click()
        # check user is inside the register page
        self.assertEqual(driver.title, 'Pur Beurre - Register')
        # we make sure there is no user in database
        self.assertEqual(len(User.objects.all()), 0)
        # user fills form with values
        driver.find_element_by_name('username').clear()
        driver.find_element_by_name('username').send_keys('Robert123456')
        driver.find_element_by_name('email').clear()
        driver.find_element_by_name('email').send_keys('Robert123456@test.com')
        driver.find_element_by_css_selector("input[type='password']").clear()
        driver.find_element_by_css_selector(
            "input[type='password']").send_keys('secret_password')
        # user clicks on submit button
        # import pdb; pdb.set_trace()
        driver.find_element_by_name('submit').click()
        # if everything is fine, user is redirected to Home page

        self.assertEqual(driver.title, 'Pur Beurre - Home')
        new_user = User.objects.get(username='Robert123456')
        user_attrs = ['Robert123456', 'Robert123456@test.com']
        self.assertEqual([new_user.username, new_user.email], user_attrs)
        self.assertTrue(new_user.check_password('secret_password'))
        # we check that user has received a mail with activation link to his email
        self.assertEqual(mail.outbox[0].subject,"Activez votre compte PurBeurre")
        self.assertEqual(mail.outbox[0].to[0],"Robert123456@test.com")
