from pyvirtualdisplay import Display
from pyvirtualdisplay.smartdisplay import SmartDisplay
from easyprocess import EasyProcess
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import unittest
from unittest import skip
import sys


class FunctionalTest(LiveServerTestCase):

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


class NewCientTest(FunctionalTest):
	display = Display(visible=0, size=(1920, 1080))
	fixtures = ['testdata.json']

	def test_home_page_layout(self):
		# Rod visits nebraskanewsservice.net, and is interested in being a client.
		self.browser.get(self.test_server)
		self.browser.set_window_size(1280, 900)

		# Rod says, "yup, there's NNS in the title, centered on the page"
		self.assertIn('Nebraska News Service', self.browser.title)
		banner = self.browser.find_element_by_class_name('navbar-inner')
		self.assertAlmostEqual(
			banner.location['x'] + banner.size['width'] / 2, 640, delta=10)

	def test_new_client_registration(self):

		self.browser.get(self.test_server)
		# Rod clicks the register button, then fills out the form and clicks Register.
		try:
			register = self.browser.find_element_by_link_text('Register')
		except:
			logout = self.browser.find_element_by_partial_link_text('Logout')
			logout.click()
			print "logging out"
			register = self.browser.find_element_by_link_text('Register')
		
		register.click()

		# Rod sees a registration form.
		self.assertIn('Become a client of the Nebraska News Service', 
						self.browser.find_element_by_tag_name('h2').text)

		# Rod fills out the form.
		email = self.browser.find_element_by_id('id_email')
		email.send_keys('test_email@gmail.com')
		pass1 = self.browser.find_element_by_id('id_password1')
		pass1.send_keys('password')
		pass2 = self.browser.find_element_by_id('id_password2')
		pass2.send_keys('password')
		pub_name = self.browser.find_element_by_id('id_pub_name')
		pub_name.send_keys("Ainsworth Star-Journal")
		pub_type = Select(self.browser.find_element_by_id('id_pub_type'))
		pub_type.select_by_visible_text("Newspaper")
		pub_area = self.browser.find_element_by_id('id_pub_area')
		pub_area.send_keys("Nebraska")
		first_name = self.browser.find_element_by_id('id_first_name')
		first_name.send_keys('Rod')
		last_name = self.browser.find_element_by_id('id_last_name')
		last_name.send_keys('Worrell')
		phone = self.browser.find_element_by_id('id_phone')
		phone.send_keys('4024723041')
		address = self.browser.find_element_by_id('id_address')
		address.send_keys('1234 Main Street')
		city = self.browser.find_element_by_id('id_city')
		city.send_keys('Ainsworth')
		state = Select(self.browser.find_element_by_id('id_state'))
		state.select_by_visible_text('Nebraska')
		zipcode = self.browser.find_element_by_id('id_zipcode')
		zipcode.send_keys('55555')
		website = self.browser.find_element_by_id('id_website')
		website.send_keys('www.ainsworthnews.com')
		facebook = self.browser.find_element_by_id('id_facebook')
		facebook.send_keys('ainsworthnews')
		twitter = self.browser.find_element_by_id('id_twitter')
		twitter.send_keys('ainsworthnews')
		about = self.browser.find_element_by_id('id_about')
		about.send_keys('rural ag news')

		# Rod clicks the Register button.
		submit = self.browser.find_element_by_name('register')
		submit.click()

		# Rod sees a message thanking him for registering.
		reg_success_message = self.browser.find_elements_by_tag_name('p')
		self.assertEqual('Thank you for becoming a client of the Nebraska News Service', reg_success_message[0].text)
						

	def test_client_login(self):
		self.browser.get(self.test_server)
		# Rod clicks login, then enters his email and password.
		try:
			login = self.browser.find_element_by_link_text('Login')
		except:
			logout = self.browser.find_element_by_partial_link_text('Logout')
			logout.click()
			print "logging out"
			login = self.browser.find_element_by_link_text('Login')

		login.click()


		# Rod fills out the form.
		self.browser.find_element_by_id('id_username').clear()
		self.browser.find_element_by_id('id_password').clear()

		self.browser.find_element_by_id('id_username').send_keys('forked5@gmail.com')
		self.browser.find_element_by_id('id_password').send_keys('forked5')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)

		#Rod clicks the Login Button
		# Rod clicks the Register button.
		#submit = self.browser.find_element_by_name('login')
		#submit.click()

		#self.assertIn('Published Stories', self.browser.find_element_by_tag_name('h2').text)
		self.assertIn('Published Stories', self.browser.find_element_by_tag_name('h2').text)



		# self.fail('Say FAIL one more god-damn time, I dare you mutha-fucka!')

		# Rod sees the Nav bar items, and the register today button.

		# Rod clicks the register today button.

		# Rod Enters his email address and a password.

		# Rod is redirected to a page that tells him 
		# to check his email for an activation link.

		# Rod clicks the link to activate his account.