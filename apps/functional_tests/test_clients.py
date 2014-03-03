from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from django.contrib.auth.models import User
from django.test.utils import IgnoreDeprecationWarningsMixin

class NewCientRegistrationTest(IgnoreDeprecationWarningsMixin, FunctionalTest):

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
		self.assertIn('Please click the link in this email to activate your NNS account.', reg_success_message[2].text)

		# Rod sees a message thanking him for registering.
		self.assertEqual('Thank you for becoming a client of the Nebraska News Service', reg_success_message[0].text)

		# Rod clicks the link to activate his account.
		# ToDo: get the activation key and go to the activation url for this new account.


class ClientSigninTest(IgnoreDeprecationWarningsMixin, FunctionalTest):

	def test_client_login(self):
		self.browser.get(self.test_server)

		# Rod clicks login.
		self.browser.find_element_by_link_text('Login').click()
		
		# Rod fills the form out wrong
		self.browser.find_element_by_id('id_username').clear()
		self.browser.find_element_by_id('id_username').send_keys('bad_email')
		self.browser.find_element_by_id('id_password').clear()
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)
		self.assertIn('Please enter a correct username and password.', 
						self.browser.find_element_by_class_name('errorlist').text)

		self.browser.find_element_by_id('id_username').clear()
		self.browser.find_element_by_id('id_username').send_keys('anthony@lincolnultimate.com')
		self.browser.find_element_by_id('id_password').clear()
		self.browser.find_element_by_id('id_password').send_keys('bad-password')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)
		self.assertIn('Please enter a correct username and password.', 
						self.browser.find_element_by_class_name('errorlist').text)

		# Rod fills out the form correctly.
		self.browser.find_element_by_id('id_username').clear()
		self.browser.find_element_by_id('id_password').clear()

		self.browser.find_element_by_id('id_username').send_keys('anthony@lincolnultimate.com')
		self.browser.find_element_by_id('id_password').send_keys('anthony')
		self.browser.find_element_by_id('id_password').send_keys(Keys.RETURN)

		#self.assertIn('Published Stories', self.browser.find_element_by_tag_name('h2').text)
		self.assertIn('Published Stories', self.browser.find_element_by_tag_name('h2').text)

class ClientProfileTest(IgnoreDeprecationWarningsMixin, FunctionalTest):

	def test_client_can_view_and_edit_profile(self):

		# Rod logs into the site
		self.log_in_client()

		# Rod clicks the Account Settings button, to see if this is his account.
		self.browser.find_element_by_link_text('Account Settings').click()
		self.assertIn('Anthony', self.browser.find_element_by_name('first_name').get_attribute('value'))
		self.assertIn('Roberts', self.browser.find_element_by_name('last_name').get_attribute('value'))

		# Rod changes some information
		self.browser.find_element_by_id('id_facebook').send_keys('ainsworthnews')
		self.browser.find_element_by_id('id_pub_area').send_keys('Northern Central Nebraska')
		self.browser.find_element_by_id('id_phone').clear()
		self.browser.find_element_by_id('id_phone').send_keys('402-555-5555')

		# Rod clicks the Save button.
		self.browser.find_element_by_name('submit').click()

		# Are there error messages? Let's fill out the required fields this time.
		try:
			errors = self.browser.find_elements_by_class_name('error')
		except:
			pass
		if errors:
			self.assertIn('This field is required.', self.browser.find_elements_by_class_name('error')[0].text)
			# Rod fills in the required fields.
			pub_area = self.browser.find_element_by_id('id_pub_area')
			pub_area.send_keys('Northern Central Nebraska')
			# Rod clicks the Save button.
			self.browser.find_element_by_name('submit').click()
		
		# Rod sees his profile with the new data.
		self.assertIn('Welcome Anthony Roberts', self.browser.find_element_by_tag_name('h3').text)
		self.assertIn('ainsworthnews', self.browser.find_element_by_xpath('//*[@id="tab5"]/div/div[1]/ul[2]/li[2]').text)
		self.assertIn('Northern Central Nebraska', self.browser.find_element_by_xpath('//*[@id="tab5"]/div/div[1]/ul[1]/li[5]').text)

	def test_client_cant_delete_required_profile_data(self):

		# Rod logs into the site
		self.log_in_client()
		self.browser.find_element_by_link_text('Account Settings').click()

		# Rod decides to try to delete some required info, which he's not allowed to do.
		self.browser.find_element_by_id('id_pub_area').send_keys('Northern Central Nebraska')
		self.browser.find_element_by_id('id_phone').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('Phone', self.browser.find_element_by_class_name('error').text)

		#Rod clicks on Stories, then goes back to Account Settings, then tries to edit the form again.
		self.browser.find_element_by_link_text('Stories').click()
		self.browser.find_element_by_link_text('Account Settings').click()
		self.browser.find_element_by_id('id_pub_area').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('Circulation or Broadcast Area', self.browser.find_element_by_class_name('error').text)

class ClientContentTest(IgnoreDeprecationWarningsMixin, FunctionalTest):

	def test_client_can_visit_aboutus_without_logging_in(self):
		
		# Rod reads the About NNS page
		self.browser.get(self.test_server + '/about/')
		headings = self.browser.find_elements_by_tag_name('h3')
		self.assertEqual('What is the Nebraska News Service?', headings[0].text)
		self.assertEqual('Our Terms of Service', headings[1].text)
		self.assertEqual('Our Privacy Policy', headings[2].text)

	def test_client_can_read_published_stories(self):

		# Rod logs into the site
		self.log_in_client()

		# Rod clicks the Stories button in the nav, goes to the Published Stories list
		self.browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div/ul[1]/li[2]/a').click()
		self.assertIn('Published Stories', self.browser.find_element_by_tag_name('h2').text)

		# ToDo: This only works locally, on server this story doesn't exist.
		self.browser.find_element_by_link_text('Test New Story').click()
		self.assertIn('Test New Story', self.browser.find_element_by_tag_name('h2').text)

	def test_client_cant_read_stories_inprogress(self):

		# Rod logs into the site
		self.log_in_client()

		# Rod tries to visit the inprogress list, but he's not allowed there.
		self.browser.get(self.test_server + '/story/inprogress/')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

		# Rod tries to view an in progress story, but he's not allowed to that.
		self.browser.get(self.test_server + '/story/article/front-page')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

	def test_client_cant_read_client_list_pages(self):

		# Rod logs into the site
		self.log_in_client()

		# Rod tries to visit the client list, but he's not allowed there.
		self.browser.get(self.test_server + '/profiles/')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

	def test_client_cant_read_reporter_list_pages(self):

		# Rod logs into the site
		self.log_in_client()

		# Rod tries to visit the reporter list, but he's not allowed there.
		self.browser.get(self.test_server + '/reporters/')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

	def test_client_cant_read_editor_list_pages(self):

		# Rod logs into the site
		self.log_in_client()

		# Rod tries to visit the editor list, but he's not allowed there.
		self.browser.get(self.test_server + '/editors/')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

	def test_client_cant_add_or_edit_stories(self):

		# Rod logs into the site
		self.log_in_client()

		# Rod tries to create a new story, but he's not allowed to do that.
		self.browser.get(self.test_server + '/story/add/article')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

		# Rod tries to edit an existing story, but he's not allowed to do that.
		self.browser.get(self.test_server + '/story/edit/article/front-page')
		self.assertIn('You do not have permission to view this page', 
						self.browser.find_element_by_tag_name('h3').text)

		# self.fail('Say FAIL one more god-damn time, I dare you mutha-fucka!')

	def test_client_can_unsubscribe(self):

		# Rod logs into the site
		self.log_in_client()
		self.browser.find_element_by_link_text('Account Settings').click()
		self.browser.find_element_by_link_text('Unsubscribe from NNS emails').click()
		self.browser.find_element_by_id('id_unsubscribe').click()
		self.browser.find_element_by_name('submit').click()
		client = User.objects.get(email='anthony@lincolnultimate.com')
		self.assertEqual('InactiveClient', client.get_profile().user_type)



