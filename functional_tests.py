from pyvirtualdisplay import Display
from pyvirtualdisplay.smartdisplay import SmartDisplay
from easyprocess import EasyProcess
from selenium import webdriver
import unittest

class NewCientTest(unittest.TestCase):
	display = Display(visible=0, size=(1920, 1080))

	def setUp(self):

		self.display.start()
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()
		self.display.stop()

	def test_new_client_registration(self):
		# Rod visits nebraskanewsservice.net, and is interested in being a client.
		self.browser.get('http://0.0.0.0:5000')

		# Rod says, "yup, there's NNS in the title"

		self.assertIn('Nebraska News Service', self.browser.title)
		self.fail('Say FAIL one more god-damn time, I dare you mutha-fucka!')

		# Rod sees the Nav bar items, and the register today button.

		# Rod clicks the register today button.

		# Rod Enters his email address and a password.

		# Rod is redirected to a page that tells him 
		# to check his email for an activation link.

		# Rod clicks the link to activate his account.



if __name__ == '__main__':
	unittest.main()