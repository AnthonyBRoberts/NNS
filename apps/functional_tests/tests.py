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

def log_out(self):
	if self.browser.find_element_by_link_text('Logout'):
		self.browser.find_element_by_link_text('Logout').click()


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


class LayoutAndStylingTest(FunctionalTest):

	def test_home_page_layout(self):

		# Rod visits nebraskanewsservice.net.
		self.browser.get(self.test_server)
		self.browser.set_window_size(1280, 900)

		# Rod says, "yup, there's NNS in the title, the big register button, and centered page layout"
		self.assertIn('Nebraska News Service', self.browser.title)
		self.assertIn('Register for the Nebraska News Service', 
						self.browser.find_element_by_xpath('//*[@id="tab1"]/div/div[1]/div/div[1]/div/a/div/h3').text)
		banner = self.browser.find_element_by_class_name('navbar-inner')
		self.assertAlmostEqual(
			banner.location['x'] + banner.size['width'] / 2, 640, delta=10)


class NewCientRegistrationTest(FunctionalTest):

	def test_new_client_registration(self):
		self.browser.get(self.test_server)

		# Rod clicks the register button.
		register = self.browser.find_element_by_link_text('Register')
		register.click()

		# Rod sees a registration form.
		self.assertIn('Become a client of the Nebraska News Service', 
						self.browser.find_element_by_tag_name('h2').text)

		# Rod fills out the form.
		email = self.browser.find_element_by_id('id_email')
		email.send_keys('selenium1@gmail.com')
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
		self.browser.find_element_by_name('register').click()

		# Rod is redirected to a page that tells him to check his email for an activation link.
		reg_success_message = self.browser.find_elements_by_tag_name('p')
		self.assertEqual('Please click the link in this email to activate your NNS account.', reg_success_message[2].text)

		# Rod sees a message thanking him for registering.
		self.assertEqual('Thank you for becoming a client of the Nebraska News Service', reg_success_message[0].text)

		# Rod clicks the link to activate his account.
		# ToDo: get the activation key and go to the activation url for this new account.


class ClientSigninTest(FunctionalTest):

	def test_client_login(self):
		self.browser.get(self.test_server)

		# Rod clicks login.
		self.browser.find_element_by_link_text('Login').click()
		
		# Rod fills the form out wrong
		self.browser.find_element_by_id('id_username').send_keys('bad_email')
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)
		self.assertIn('Please enter a correct username and password.', 
						self.browser.find_element_by_xpath('//*[@id="tab1"]/form/ul/li').text)

		self.browser.find_element_by_id('id_username').send_keys('anthony@lincolnultimate.com')
		self.browser.find_element_by_id('id_password').send_keys('bad-password')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)
		self.assertIn('Please enter a correct username and password.', 
						self.browser.find_element_by_xpath('//*[@id="tab1"]/form/ul/li').text)

		# Rod fills out the form correctly.
		self.browser.find_element_by_id('id_username').clear()
		self.browser.find_element_by_id('id_password').clear()

		self.browser.find_element_by_id('id_username').send_keys('anthony@lincolnultimate.com')
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)

		#self.assertIn('Published Stories', self.browser.find_element_by_tag_name('h2').text)
		self.assertIn('Published Stories', self.browser.find_element_by_tag_name('h2').text)

class ClientSiteUsageTest(FunctionalTest):

	def log_in(self):
		self.browser.get(self.test_server)
		self.browser.find_element_by_link_text('Login').click()
		self.browser.find_element_by_id('id_username').send_keys('anthony@lincolnultimate.com')
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)


	def test_client_can_visit_aboutus_without_logging_in(self):
		
		# Rod reads the About NNS page
		self.browser.get(self.test_server + '/about/')
		headings = self.browser.find_elements_by_tag_name('h3')
		self.assertEqual('What is the Nebraska News Service?', headings[0].text)
		self.assertEqual('Our Terms of Service', headings[1].text)
		self.assertEqual('Our Privacy Policy', headings[2].text)

	def test_client_can_read_published_stories(self):

		# Rod logs into the site
		log_in(self)

		# Rod clicks the Stories button in the nav, goes to the Published Stories list
		self.browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div/ul[1]/li[2]/a').click()
		self.assertIn('Published Stories', self.browser.find_element_by_tag_name('h2').text)
		self.browser.find_element_by_link_text('Test New Story').click()
		self.assertIn('Test New Story', self.browser.find_element_by_tag_name('h2').text)

	def test_client_cant_read_stories_inprogress(self):

		# Rod logs into the site
		self.browser.get(self.test_server)
		self.browser.find_element_by_link_text('Login').click()
		self.browser.find_element_by_id('id_username').send_keys('anthony@lincolnultimate.com')
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)

		# Rod tries to visit the inprogress list, but he's not allowed there.
		self.browser.get(self.test_server + '/story/inprogress/')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

		# Rod tries to view an in progress story, but he's not allowed to that.
		self.browser.get(self.test_server + '/story/article/front-page')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

	def test_client_cant_read_user_list_pages(self):

		# Rod logs into the site
		self.browser.get(self.test_server)
		self.browser.find_element_by_link_text('Login').click()
		self.browser.find_element_by_id('id_username').send_keys('anthony@lincolnultimate.com')
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)

		# Rod tries to visit the client list, but he's not allowed there.
		self.browser.get(self.test_server + '/profiles/')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

		# Rod tries to visit the reporter list, but he's not allowed there.
		self.browser.get(self.test_server + '/reporters/')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

		# Rod tries to visit the editor list, but he's not allowed there.
		self.browser.get(self.test_server + '/editors/')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

	def test_client_cant_add_or_edit_stories(self):

		# Rod logs into the site
		self.browser.get(self.test_server)
		self.browser.find_element_by_link_text('Login').click()
		self.browser.find_element_by_id('id_username').send_keys('anthony@lincolnultimate.com')
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)

		# Rod tries to create a new story, but he's not allowed to do that.
		self.browser.get(self.test_server + '/story/add/article')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

		# Rod tries to edit an existing story, but he's not allowed to do that.
		self.browser.get(self.test_server + '/story/edit/article/front-page')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

		# self.fail('Say FAIL one more god-damn time, I dare you mutha-fucka!')


class ReporterSiteUsageTest(FunctionalTest):

	def test_reporter_can_login(self):

		# Joe logs into the site
		self.browser.get(self.test_server)
		self.browser.find_element_by_link_text('Login').click()
		self.browser.find_element_by_id('id_username').send_keys('nns.jmoore@gmail.com')
		self.browser.find_element_by_id('id_password').send_keys('jmoore')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)

		# Joe clicks the My Profile button, to see if this is his account.
		self.browser.find_element_by_link_text('My Profile').click()
		self.assertIn('Welcome Joseph Moore', self.browser.find_element_by_tag_name('h3').text)

