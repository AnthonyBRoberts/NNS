from pyvirtualdisplay import Display
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys


class FunctionalTest(LiveServerTestCase):
	display = Display(visible=0, size=(1920, 1080))
	fixtures = ['testdata.json']

	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.test_server = 'http://' + arg.split('=')[1]
				return
		LiveServerTestCase.setUpClass()
		cls.test_server = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.test_server == cls.live_server_url:
			LiveServerTestCase.tearDownClass()

	def setUp(self):
		self.display.start()
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()
		self.display.stop()

	def log_in_client(self):
		self.browser.get(self.test_server)
		self.browser.find_element_by_link_text('Login').click()
		self.browser.find_element_by_id('id_username').send_keys('anthony@lincolnultimate.com')
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)

	def log_in_reporter(self):
		self.browser.get(self.test_server)
		self.browser.find_element_by_link_text('Login').click()
		self.browser.find_element_by_id('id_username').send_keys('nns.jmoore@gmail.com')
		self.browser.find_element_by_id('id_password').send_keys('jmoore')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)

	def log_in_editor(self):
		self.browser.get(self.test_server)
		self.browser.find_element_by_link_text('Login').click()
		self.browser.find_element_by_id('id_username').send_keys('nns.aroberts@gmail.com')
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)