from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


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


