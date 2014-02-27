from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test.utils import IgnoreDeprecationWarningsMixin

class ReporterViewsTest(IgnoreDeprecationWarningsMixin, FunctionalTest):

	def test_reporter_can_view_user_lists(self):

		# Joe logs into the site
		self.log_in_reporter()

		# Joe goes to client list
		self.browser.get(self.test_server + '/profiles/')
		self.assertIn('Clients', self.browser.find_element_by_tag_name('h2').text)

		# Joe goes to reporter list
		self.browser.get(self.test_server + '/reporters/')
		self.assertIn('Reporters', self.browser.find_element_by_tag_name('h2').text)

		# Joe goes to editor list
		self.browser.get(self.test_server + '/editors/')
		self.assertIn('Editors', self.browser.find_element_by_tag_name('h2').text)

	def test_reporter_can_view_published_story_list(self):

		# Joe logs into the site
		self.log_in_reporter()

		# Joe clicks Published Stories Tab, sees a list of stories
		self.browser.find_element_by_link_text('Published Stories').click()
		self.assertIsNotNone(
			self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[2]/td[1]/a'))

	def test_reporter_can_edit_published_stories(self):

		# Joe logs into the site
		self.log_in_reporter()
		self.browser.get(self.test_server + '/story/')

		# Joe clicks on the fist story's title
		self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[2]/td[1]/a').click()

		# ToDo: This only works locally, on server this story doesn't exist.
		self.assertIn('Edit Story', self.browser.find_element_by_tag_name('h1').text)

		# Joe clicks Published Stories Tab again
		self.browser.find_element_by_link_text('Published Stories').click()

		# Joe clicks on the second story's title
		# ToDo: This only works locally, on server this story doesn't exist.
		self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[3]/td[1]/a').click()
		self.assertIn('Edit Story', self.browser.find_element_by_tag_name('h1').text)

		# Joe tries to save the story without a title, but can't 
		self.browser.find_element_by_id('id_title').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('This field is required.', self.browser.find_element_by_class_name('help-block').text)

		# Joe makes some changes and saves.
		self.browser.find_element_by_id('id_title').send_keys('Edited Test Story Title')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('This is an added paragraph to the test story.')
		self.browser.find_element_by_id('id_tags').send_keys(', Joes_new_tag')
		self.browser.find_element_by_name('submit').click()

		# Joe sees his changes to the story.
		self.assertIn('Edited Test Story Title', self.browser.find_element_by_tag_name('h2').text)
		ptext = self.browser.find_elements_by_tag_name('p')
		try:
			for p in ptext:
				if 'This is an added paragraph to the test story.' in p.text:
					self.assertIn('This is an added paragraph to the test story.', p.text)
		except:
			self.fail('The text did not get added to the story')


	def test_reporter_can_view_inprogress_story_list(self):

		# Joe logs into the site
		self.log_in_reporter()

		# Joe clicks Stories in progress Tab, sees a list of stories
		self.browser.find_element_by_link_text('Stories in progress').click()
		self.assertIsNotNone(
			self.browser.find_element_by_xpath('//*[@id="tab2"]/table/tbody/tr[3]/td[1]/a'))

	def test_reporter_can_edit_inprogress_story(self):

		# Joe logs into the site
		self.log_in_reporter()

		self.browser.get(self.test_server + '/story/inprogress/')
		# Joe clicks on the Front Page story's title

		self.browser.find_element_by_link_text('Front Page').click()
		self.assertIn('Edit Story Front Page', self.browser.find_element_by_tag_name('h1').text)

		# Joe clicks Stories in progress Tab again
		self.browser.find_element_by_link_text('Stories in progress').click()

		# Joe clicks on the second story's title
		self.browser.find_element_by_link_text('About Us').click()
		self.assertIn('Edit Story About Us', self.browser.find_element_by_tag_name('h1').text)

		# Joe tries to save the story without a title, but can't 
		self.browser.find_element_by_id('id_title').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('This field is required.', self.browser.find_element_by_class_name('help-block').text)

		# Joe makes some changes and saves.
		self.browser.find_element_by_id('id_title').send_keys('Edited Published Story Title')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('This is an added paragraph to the published test story.')
		self.browser.find_element_by_id('id_tags').send_keys(', Joes_new_tag')
		self.browser.find_element_by_name('submit').click()

		# Joe sees his changes to the story.
		self.assertIn('Edited Published Story Title', self.browser.find_element_by_tag_name('h2').text)
		ptext = self.browser.find_elements_by_tag_name('p')
		try:
			for p in ptext:
				if 'This is an added paragraph to the published test story.' in p.text:
					self.assertIn('This is an added paragraph to the published test story.', p.text)
		except:
			self.fail('The text did not get added to the story')

	def test_reporter_can_create_new_story(self):

		# Joe logs into the site
		self.log_in_reporter()

		# Joe goes to the add new story page
		self.browser.get(self.test_server + '/story/add/article')

		# Joe tries to save the story without a title, but can't 
		self.browser.find_element_by_id('id_title').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('This field is required.', self.browser.find_element_by_class_name('help-block').text)

		# Joe makes some changes and saves.
		self.browser.find_element_by_id('id_title').send_keys('Functional Test Add Story Title')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('This is an added paragraph to the create new story test.')
		self.browser.find_element_by_id('id_tags').send_keys(', Joes_new_tag')
		self.browser.find_element_by_name('submit').click()

		# Joe sees his changes to the story.
		self.assertIn('Functional Test Add Story Title', self.browser.find_element_by_tag_name('h2').text)
		ptext = self.browser.find_elements_by_tag_name('p')
		try:
			for p in ptext:
				if 'This is an added paragraph to the create new story test.' in p.text:
					self.assertIn('This is an added paragraph to the create new story test.', p.text)
		except:
			self.fail('The text did not get added to the story')

class ReporterProfileTest(IgnoreDeprecationWarningsMixin, FunctionalTest):

	def test_reporter_can_view_and_edit_profile(self):

		# Joe logs into the site
		self.log_in_reporter()

		# Joe clicks the My Profile button, to see if this is his account.
		self.browser.find_element_by_link_text('My Profile').click()
		self.assertIn('Welcome Joseph Moore', self.browser.find_element_by_tag_name('h3').text)

		# Joe clicks the Edit my profile button, to edit his account info.
		self.browser.find_element_by_link_text('Edit my profile').click()
		self.assertIn('Edit Profile', self.browser.find_element_by_tag_name('h2').text)

		# Joe changes some information
		self.browser.find_element_by_id('id_phone').clear()
		self.browser.find_element_by_id('id_phone').send_keys('402-555-5555')
		self.browser.find_element_by_id('id_byline').clear()
		self.browser.find_element_by_id('id_byline').send_keys('By Joseph Moore, NNS')
		self.browser.find_element_by_id('id_email').clear()
		self.browser.find_element_by_id('id_email').send_keys('nns.jmoore@gmail.com')
		
		# Joe clicks the Save button.
		self.browser.find_element_by_name('submit').click()
		
		# Joe sees his profile with the new data.
		self.assertIn('Welcome Joseph Moore', self.browser.find_element_by_tag_name('h3').text)
		self.assertIn('(402) 555-5555', self.browser.find_element_by_xpath('//*[@id="tab5"]/div/div[1]/ul/li[2]').text)
		self.assertIn('nns.jmoore@gmail.com', self.browser.find_element_by_xpath('//*[@id="tab5"]/div/div[1]/ul/li[1]').text)


	def test_reporter_cant_delete_required_profile_data(self):

		# Joe logs into the site
		self.log_in_reporter()
		self.browser.find_element_by_link_text('My Profile').click()

		# Joe decides to try to delete some required info, which he's not allowed to do.
		self.browser.find_element_by_link_text('Edit my profile').click()
		self.browser.find_element_by_id('id_email').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('Primary email', self.browser.find_element_by_class_name('error').text)

		#Joe clicks on Stories, then goes back to My Profile, then tries to edit the form again.
		self.browser.find_element_by_link_text('Stories').click()
		self.browser.find_element_by_link_text('My Profile').click()
		self.browser.find_element_by_link_text('Edit my profile').click()
		self.browser.find_element_by_id('id_first_name').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('First name', self.browser.find_element_by_class_name('error').text)

		# self.fail('As Samuel L. Jackson: Say FAIL one more god-damn time, I dare you mutha-fucka!')