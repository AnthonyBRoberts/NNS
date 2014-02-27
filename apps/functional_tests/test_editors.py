from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test.utils import IgnoreDeprecationWarningsMixin

class EditorViewsTest(IgnoreDeprecationWarningsMixin, FunctionalTest):

	def test_editor_can_view_user_lists(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony goes to client list
		self.browser.get(self.test_server + '/profiles/')
		self.assertIn('Clients', self.browser.find_element_by_tag_name('h2').text)

		# Anthony goes to editor list
		self.browser.get(self.test_server + '/reporters/')
		self.assertIn('Reporters', self.browser.find_element_by_tag_name('h2').text)

		# Anthony goes to editor list
		self.browser.get(self.test_server + '/editors/')
		self.assertIn('Editors', self.browser.find_element_by_tag_name('h2').text)

	def test_editor_can_view_published_story_list(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony clicks Published Stories Tab, sees a list of stories
		self.browser.find_element_by_link_text('Published Stories').click()
		self.assertIsNotNone(
			self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[2]/td[1]/a'))

	def test_editor_can_edit_published_stories(self):

		# Anthony logs into the site
		self.log_in_editor()
		self.browser.get(self.test_server + '/story/')

		# Anthony clicks on the fist story's title
		self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[2]/td[1]/a').click()

		# ToDo: This only works locally, on server this story doesn't exist.
		self.assertIn('Edit Story', self.browser.find_element_by_tag_name('h1').text)

		# Anthony clicks Published Stories Tab again
		self.browser.find_element_by_link_text('Published Stories').click()

		# Anthony clicks on the second story's title
		# ToDo: This only works locally, on server this story doesn't exist.
		self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[3]/td[1]/a').click()
		self.assertIn('Edit Story', self.browser.find_element_by_tag_name('h1').text)

		# Anthony tries to save the story without a title, but can't 
		self.browser.find_element_by_id('id_title').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('This field is required.', self.browser.find_element_by_class_name('help-block').text)

		# Anthony makes some changes and saves.
		self.browser.find_element_by_id('id_title').send_keys('Edited Test Story Title')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('This is an added paragraph to the test story.')
		self.browser.find_element_by_id('id_tags').send_keys(', Anthonys_new_tag')
		self.browser.find_element_by_name('submit').click()

		# Anthony sees his changes to the story.
		self.assertIn('Edited Test Story Title', self.browser.find_element_by_tag_name('h2').text)
		ptext = self.browser.find_elements_by_tag_name('p')
		try:
			for p in ptext:
				if 'This is an added paragraph to the test story.' in p.text:
					self.assertIn('This is an added paragraph to the test story.', p.text)
		except:
			self.fail('The text did not get added to the story')


	def test_editor_can_view_inprogress_story_list(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony clicks Stories in progress Tab, sees a list of stories
		self.browser.find_element_by_link_text('Stories in progress').click()
		self.assertIsNotNone(
			self.browser.find_element_by_xpath('//*[@id="tab2"]/table/tbody/tr[3]/td[1]/a'))

	def test_editor_can_edit_inprogress_story(self):

		# Anthony logs into the site
		self.log_in_editor()

		self.browser.get(self.test_server + '/story/inprogress/')
		# Anthony clicks on the Front Page story's title

		self.browser.find_element_by_link_text('Front Page').click()
		self.assertIn('Edit Story Front Page', self.browser.find_element_by_tag_name('h1').text)

		# Anthony clicks Stories in progress Tab again
		self.browser.find_element_by_link_text('Stories in progress').click()

		# Anthony clicks on the second story's title
		self.browser.find_element_by_link_text('About Us').click()
		self.assertIn('Edit Story About Us', self.browser.find_element_by_tag_name('h1').text)

		# Anthony tries to save the story without a title, but can't 
		self.browser.find_element_by_id('id_title').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('This field is required.', self.browser.find_element_by_class_name('help-block').text)

		# Anthony makes some changes and saves.
		self.browser.find_element_by_id('id_title').send_keys('Edited Published Story Title')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('This is an added paragraph to the published test story.')
		self.browser.find_element_by_id('id_tags').send_keys(', Anthonys_new_tag')
		self.browser.find_element_by_name('submit').click()

		# Anthony sees his changes to the story.
		self.assertIn('Edited Published Story Title', self.browser.find_element_by_tag_name('h2').text)
		ptext = self.browser.find_elements_by_tag_name('p')
		try:
			for p in ptext:
				if 'This is an added paragraph to the published test story.' in p.text:
					self.assertIn('This is an added paragraph to the published test story.', p.text)
		except:
			self.fail('The text did not get added to the story')

class EditorProfileTest(IgnoreDeprecationWarningsMixin, FunctionalTest):

	def test_editor_can_view_and_edit_profile(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony clicks the My Profile button, to see if this is his account.
		self.browser.find_element_by_link_text('My Profile').click()
		self.assertIn('Welcome Anthony', self.browser.find_element_by_tag_name('h3').text)

		# Anthony clicks the Edit my profile button, to edit his account info.
		self.browser.find_element_by_link_text('Edit my profile').click()
		self.assertIn('Edit Profile', self.browser.find_element_by_tag_name('h2').text)

		# Anthony changes some information
		self.browser.find_element_by_id('id_phone').clear()
		self.browser.find_element_by_id('id_phone').send_keys('402-555-5555')
		self.browser.find_element_by_id('id_byline').clear()
		self.browser.find_element_by_id('id_byline').send_keys('By Anthony, NNS')
		self.browser.find_element_by_id('id_email').clear()
		self.browser.find_element_by_id('id_email').send_keys('nns.aroberts@gmail.com')
		
		# Anthony clicks the Save button.
		self.browser.find_element_by_name('submit').click()
		
		# Anthony sees his profile with the new data.
		self.assertIn('Welcome Anthony', self.browser.find_element_by_tag_name('h3').text)
		self.assertIn('(402) 555-5555', self.browser.find_element_by_xpath('//*[@id="tab5"]/div/div[1]/ul/li[2]').text)
		self.assertIn('nns.aroberts@gmail.com', self.browser.find_element_by_xpath('//*[@id="tab5"]/div/div[1]/ul/li[1]').text)


	def test_editor_cant_delete_required_profile_data(self):

		# Anthony logs into the site
		self.log_in_editor()
		self.browser.find_element_by_link_text('My Profile').click()

		# Anthony decides to try to delete some required info, which he's not allowed to do.
		self.browser.find_element_by_link_text('Edit my profile').click()
		self.browser.find_element_by_id('id_email').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('Primary email', self.browser.find_element_by_class_name('error').text)

		#Anthony clicks on Stories, then goes back to My Profile, then tries to edit the form again.
		self.browser.find_element_by_link_text('Stories').click()
		self.browser.find_element_by_link_text('My Profile').click()
		self.browser.find_element_by_link_text('Edit my profile').click()
		self.browser.find_element_by_id('id_first_name').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('First name', self.browser.find_element_by_class_name('error').text)

		# self.fail('As Samuel L. Jackson: Say FAIL one more god-damn time, I dare you mutha-fucka!')