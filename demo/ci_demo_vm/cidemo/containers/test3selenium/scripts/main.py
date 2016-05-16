from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
import unittest

NODE_ADDRESS = 'http://' + os.environ['SELENIUMHUB_PORT_4444_TCP_ADDR'] + ":" + str(os.environ['SELENIUMHUB_PORT_4444_TCP_PORT']) + '/wd/hub'

APP_ADDRESS='http://' + os.environ['WEB_PORT_80_TCP_ADDR'] + ":" + str(os.environ['WEB_PORT_80_TCP_PORT'])

class WebpageTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		print("Set up class")
		cls.driver = webdriver.Remote(
			command_executor=NODE_ADDRESS,
			desired_capabilities=DesiredCapabilities.FIREFOX
		)

	@classmethod
	def tearDownClass(cls):
		print("Tear down class")
		cls.driver.close()

	def tearDown(self):
		print("Tear down")
		# If an error has occurred, take a screen capture of the browser state
		for method, error in self._outcome.errors:
			if error:
				screenshot_name = '/workspace/failed-{}.png'.format(str(method).split()[0])
				print("Saving screen shot to {}".format(screenshot_name))
				self.driver.save_screenshot(screenshot_name)

	##############################################
	# All tests defined below this point
	def testIndexExists(self):
		self.driver.get(APP_ADDRESS + "/index.html")
		assert "Index" in self.driver.title

	def testAExists(self):
		self.driver.get(APP_ADDRESS + "/a.html")
		assert "A" in self.driver.title

	def testBExists(self):
		self.driver.get(APP_ADDRESS + "/b.html")
		assert "B" in self.driver.title
