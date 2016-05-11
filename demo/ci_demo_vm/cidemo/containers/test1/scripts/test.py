import sys
import unittest
import os

info = sys.version_info

print("Hello world!  Python version {}.{}".format(info.major, info.minor))

class BasicTest(unittest.TestCase):
	def testTestPythonVersion(self):
		self.assertEquals(2, info.major)
		self.assertEquals(7, info.minor)

	def testBuildBroken(self):
		self.assertNotEqual("true", os.environ["BREAK_BUILD"])
