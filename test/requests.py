import unittest

import requests


class MyTestCase(unittest.TestCase):
    def test_something(self):
        pass


if __name__ == '__main__':
    res = requests.post('http://127.0.0.1:5000/callback?message=hoge')
    # unittest.main()
