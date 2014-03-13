from .base import EditorTests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from django.test.utils import IgnoreDeprecationWarningsMixin

class EditorViewsTest(IgnoreDeprecationWarningsMixin, EditorTests):

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
		self.assertIn('Edit Story', self.browser.find_element_by_tag_name('h2').text)

		# Anthony clicks Published Stories Tab again
		self.browser.find_element_by_link_text('Published Stories').click()

		# Anthony clicks on the second story's title
		# ToDo: This only works locally, on server this story doesn't exist.
		self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[3]/td[1]/a').click()
		self.assertIn('Edit Story', self.browser.find_element_by_tag_name('h2').text)

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
		self.assertIn('Edit Story Front Page', self.browser.find_element_by_tag_name('h2').text)

		# Anthony clicks Stories in progress Tab again
		self.browser.find_element_by_link_text('Stories in progress').click()

		# Anthony clicks on the second story's title
		self.browser.find_element_by_link_text('About Us').click()
		self.assertIn('Edit Story About Us', self.browser.find_element_by_tag_name('h2').text)

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

	def test_editor_can_add_new_story(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony clicks on the add story button
		self.browser.get(self.test_server + '/story/add/article')

		# Anthony clicks submit without filling out the form, which fials
		self.browser.find_element_by_name('submit').click()
		self.assertIn('This field is required.', self.browser.find_elements_by_class_name('help-block')[0].text)

		# Anthony adds title, text, and author to story form
		self.browser.find_element_by_name('title').send_keys('Add new story test title')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('Add new story test text')
		author = Select(self.browser.find_element_by_id('id_author'))
		author.select_by_visible_text('anthony')

		# Anthony clicks save.
		self.browser.find_element_by_name('submit').click()

		# Anthony sees two success messages.
		self.assertIn('Article saved successfully', self.browser.find_elements_by_class_name('alert-success')[0].text)
		self.assertIn('Add new story test title', self.browser.find_element_by_tag_name('h2').text)


	def test_editor_can_send_story_to_all_clients_on_add_new_story(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony clicks on the add story button
		self.browser.get(self.test_server + '/story/add/article')

		# Anthony clicks submit without filling out the form, which fials
		self.browser.find_element_by_name('submit').click()

		# Anthony adds title, text, and author to story form
		self.browser.find_element_by_name('title').send_keys('Add new story test title')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('Add new story test text')
		author = Select(self.browser.find_element_by_id('id_author'))
		author.select_by_visible_text('anthony')
		mediaitem = Select(self.browser.find_element_by_id('id_mediaitems'))
		mediaitem.select_by_visible_text('Make some media 1')
		mediaitem.select_by_visible_text('Another Media Item')

		# Anthony clicks publsih story and send now, then clicks save.
		self.browser.find_element_by_name('is_published').click()
		self.browser.find_element_by_name('send_now').click()
		self.browser.find_element_by_name('submit').click()

		# Anthony sees two success messages.
		self.assertIn('Article saved successfully', self.browser.find_elements_by_class_name('alert-success')[0].text)
		self.assertIn('Article published successfully', self.browser.find_elements_by_class_name('alert-success')[1].text)
		self.assertIn('Add new story test title', self.browser.find_element_by_tag_name('h2').text)

	def test_editor_can_send_story_to_all_clients(self):

		# Anthony logs into the site
		self.log_in_editor()

		self.browser.get(self.test_server + '/story/inprogress/')
		# Anthony clicks on the Front Page story's title

		self.browser.find_element_by_link_text('Front Page').click()
		self.assertIn('Edit Story Front Page', self.browser.find_element_by_tag_name('h2').text)

		# Anthony clicks publsih story and send now, then clicks save.
		self.browser.find_element_by_name('is_published').click()
		self.browser.find_element_by_name('send_now').click()
		self.browser.find_element_by_name('submit').click()

		# Anthony sees two success messages.
		self.assertIn('Article updated successfully', self.browser.find_elements_by_class_name('alert-success')[0].text)
		self.assertIn('Article published successfully', self.browser.find_elements_by_class_name('alert-success')[1].text)
		self.assertIn('Front Page', self.browser.find_element_by_tag_name('h2').text)

	def test_editor_can_send_story_to_only_addition_recipients(self):

		# Anthony logs into the site
		self.log_in_editor()

		self.browser.get(self.test_server + '/story/inprogress/')
		# Anthony clicks on the Front Page story's title

		self.browser.find_element_by_link_text('About Us').click()
		self.assertIn('Edit Story About Us', self.browser.find_element_by_tag_name('h2').text)

		# Anthony clicks publsih story and send now, then clicks save.
		self.browser.find_element_by_name('is_published').click()
		self.browser.find_element_by_name('send_now').click()
		self.browser.find_element_by_name('add_recipients_only').click()
		self.browser.find_element_by_name('submit').click()

		# Oops, Anthony forgot to add an email to the recipient list
		self.assertIsNotNone(self.browser.find_elements_by_class_name('alert-error'))

		# Anthony adds an email address to the field
		self.browser.find_element_by_name('add_recipients').send_keys('nns.aroberts@gmail.com')
		self.browser.find_element_by_name('submit').click()

		# Anthony sees two success messages.
		self.assertIn('Article updated successfully', self.browser.find_elements_by_class_name('alert-success')[0].text)
		self.assertIn('Article published successfully', self.browser.find_elements_by_class_name('alert-success')[1].text)
		self.assertIn('About Us', self.browser.find_element_by_tag_name('h2').text)

	def test_editor_can_send_story_to_only_broadcasters(self):

		# Anthony logs into the site
		self.log_in_editor()

		self.browser.get(self.test_server + '/story/inprogress/')
		# Anthony clicks on the Front Page story's title

		self.browser.find_element_by_link_text('About Us').click()
		self.assertIn('Edit Story About Us', self.browser.find_element_by_tag_name('h2').text)

		# Anthony clicks publsih story and send now, then clicks save.
		self.browser.find_element_by_name('is_published').click()
		self.browser.find_element_by_name('send_now').click()
		self.browser.find_element_by_name('broadcast_only').click()
		self.browser.find_element_by_name('submit').click()

		# Anthony sees two success messages.
		self.assertIn('Article updated successfully', self.browser.find_elements_by_class_name('alert-success')[0].text)
		self.assertIn('Article published successfully', self.browser.find_elements_by_class_name('alert-success')[1].text)
		self.assertIn('About Us', self.browser.find_element_by_tag_name('h2').text)

	def test_editor_can_create_new_media_item(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony goes to the add new story page
		self.browser.get(self.test_server + '/story/add/media')

		# Anthony tries to save the media item without a title, but can't 
		self.browser.find_element_by_id('id_title').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('This field is required.', self.browser.find_element_by_class_name('help-block').text)

		# Anthony makes some changes and saves.
		self.browser.find_element_by_id('id_title').send_keys('Functional Test Add Media Title')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('This is an added paragraph to the create new story test.')
		author = Select(self.browser.find_element_by_id('id_author'))
		author.select_by_visible_text('anthony')
		self.browser.find_element_by_id('id_tags').send_keys(', Tags, Media')

		self.browser.find_element_by_name('submit').click()

		# Anthony sees two success messages, saved and editor notified
		self.assertIn('Media saved successfully', 
						self.browser.find_elements_by_class_name('alert-success')[0].text)
		self.assertIn('Functional Test Add Media Title',
						self.browser.find_element_by_tag_name('h2').text)

	def test_editor_can_edit_and_send_published_media_items(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony goes to the media list and clicks on the first media item in the list
		self.browser.get(self.test_server + '/story/media')
		self.browser.find_element_by_link_text('test new media item error text 2').click()
		self.assertIn('test new media item error text 2', self.browser.find_element_by_name('title').get_attribute('value'))

		# Anthony makes some changes and saves.
		self.browser.find_element_by_id('id_title').send_keys('Functional Test Add Media Title 2')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('This is an added paragraph to the create new media test.')
		self.browser.find_element_by_id('id_tags').send_keys(', Anthonys_new_tag')
		self.browser.find_element_by_name('send_now').click()
		self.browser.find_element_by_name('submit').click()

		# Anthony sees two success messages, updated and published
		self.assertIn('Media updated successfully', 
					self.browser.find_elements_by_class_name('alert-success')[0].text)
		self.assertIn('Media published successfully', 
					self.browser.find_elements_by_class_name('alert-success')[1].text)

	def test_editor_can_edit_and_send_media_items_inprogress(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony goes to the media list and clicks on the first media item in the list
		self.browser.get(self.test_server + '/story/media/inprogress')
		self.browser.find_element_by_link_text('test new media item error text').click()
		self.assertIn('test new media item error text', self.browser.find_element_by_name('title').get_attribute('value'))


		# Anthony makes some changes and saves.
		self.browser.find_element_by_id('id_title').send_keys('Functional Test Add Media Title 2')
		self.browser.find_element_by_class_name('redactor_editor').send_keys('This is an added paragraph to the create new media test.')
		self.browser.find_element_by_id('id_tags').send_keys(', Anthonys_new_tag')
		self.browser.find_element_by_id('id_is_published').click()
		self.browser.find_element_by_id('id_send_now').click()
		self.browser.find_element_by_name('submit').click()

		# Anthony sees two success messages, updated and published
		self.assertIn('Media updated successfully', 
					self.browser.find_element_by_class_name('alert-success').text)
		self.assertIn('Media published successfully', 
					self.browser.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]').text)


class EditorProfileTest(IgnoreDeprecationWarningsMixin, EditorTests):

	def test_editor_can_view_and_edit_profile(self):

		# Anthony logs into the site
		self.log_in_editor()

		# Anthony clicks the Account Settings button, to see if this is his account.
		self.browser.find_element_by_link_text('Account Settings').click()
		self.assertIn('Anthony', self.browser.find_element_by_name('first_name').get_attribute('value'))
		self.assertIn('Roberts, Technology Consultant', self.browser.find_element_by_name('last_name').get_attribute('value'))

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
		self.browser.find_element_by_link_text('Account Settings').click()

		# Anthony decides to try to delete some required info, which he's not allowed to do.
		self.browser.find_element_by_id('id_email').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('Primary email', self.browser.find_element_by_class_name('error').text)

		#Anthony clicks on Stories, then goes back to Account Settings, then tries to edit the form again.
		self.browser.find_element_by_link_text('Stories').click()
		self.browser.find_element_by_link_text('Account Settings').click()
		self.browser.find_element_by_id('id_first_name').clear()
		self.browser.find_element_by_name('submit').click()
		self.assertIn('First name', self.browser.find_element_by_class_name('error').text)

		# self.fail('As Samuel L. Jackson: Say FAIL one more god-damn time, I dare you mutha-fucka!')