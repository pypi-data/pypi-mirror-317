import os
import requests
import unittest
from random import choice
from string import ascii_letters
from litter.uploader import *


def generate_random_file_content():
    result = ""
    for _ in range(30):
        result += choice(ascii_letters)

    return result


class TestUploadMethods(unittest.TestCase):
    def setUp(self):
        self.content = generate_random_file_content()
        self.filename = "testfile"
        with open(self.filename, "w") as f:
            f.write(self.content)

    def tearDown(self):
        os.remove(self.filename)

    def compare(self, url):
        r = requests.get(url)
        self.assertEqual(r.text, self.content)

    def test_catbox(self):
        uploader = CatboxUploader(self.filename)
        result = uploader.execute()
        self.compare(result)

    def test_litterbox(self):
        uploader = LitterboxUploader(self.filename, time="1h")
        result = uploader.execute()
        self.compare(result)


if __name__ == "__main__":
    unittest.main()
