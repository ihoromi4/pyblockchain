import unittest

import tests
#from tests import *


suite = tests.test_suite()
runner = unittest.TextTestRunner()
runner.run(suite)

#unittest.main()

