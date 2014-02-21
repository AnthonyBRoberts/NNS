from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ReporterSiteUsageTest(FunctionalTest):

	def test_reporter_can_login_view_profile(self):

		# Joe logs into the site
		self.log_in_reporter()

		# Joe clicks the My Profile button, to see if this is his account.
		self.browser.find_element_by_link_text('My Profile').click()
		self.assertIn('Welcome Joseph Moore', self.browser.find_element_by_tag_name('h3').text)

	def test_reporter_can_view_published_story_list(self):

		# Joe logs into the site
		self.log_in_reporter()

		# Joe clicks Published Stories Tab, sees a list of stories
		self.browser.find_element_by_link_text('Published Stories').click()
		self.assertIsNotNone(
			self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[2]/td[1]/a'))

		# Joe clicks on the fist story's title
		self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[2]/td[1]/a').click()
		self.assertIn('Test New Story', self.browser.find_element_by_tag_name('h2').text)

		# Joe clicks Published Stories Tab again
		self.browser.find_element_by_link_text('Published Stories').click()

		# Joe clicks on the second story's title
		self.browser.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[3]/td[1]/a').click()
		self.assertIn('Test Story Number One', self.browser.find_element_by_tag_name('h2').text)


	def test_reporter_can_view_inprogress_story_list(self):

		# Joe logs into the site
		self.log_in_reporter()

		# Joe clicks Stories in progress Tab, sees a list of stories
		self.browser.find_element_by_link_text('Stories in progress').click()
		self.assertIsNotNone(
			self.browser.find_element_by_xpath('//*[@id="tab2"]/table/tbody/tr[3]/td[1]/a'))

		# Joe clicks on the Front Page story's title
		self.browser.find_element_by_xpath('//*[@id="tab2"]/table/tbody/tr[3]/td[1]/a').click()
		self.assertIn('Front Page', self.browser.find_element_by_tag_name('h2').text)

		# Joe clicks Stories in progress Tab again
		self.browser.find_element_by_link_text('Stories in progress').click()

		# Joe clicks on the second story's title
		self.browser.find_element_by_xpath('//*[@id="tab2"]/table/tbody/tr[4]/td[1]/a').click()
		self.assertIn('About Us', self.browser.find_element_by_tag_name('h2').text)

		# self.fail('Say FAIL one more god-damn time, I dare you mutha-fucka!')

