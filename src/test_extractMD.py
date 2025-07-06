import re
import unittest
from md_process import extract_markdown_images, extract_markdown_links


import unittest
from md_process import extract_markdown_images, extract_markdown_links

class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png) and some text."
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt text", "http://example.com/image.png"))

        text = "No images here."
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)

        text = "Multiple images ![first](http://example.com/first.png) and ![second](http://example.com/second.png)."
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("first", "http://example.com/first.png"))
        self.assertEqual(images[1], ("second", "http://example.com/second.png"))

        text = "Image with special characters ![alt text](http://example.com/image.png?query=1&other=2)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt text", "http://example.com/image.png?query=1&other=2"))

        text = "Image links next to hyperlinks ![image](http://example.com/image.png) and [link](http://example.com)." 
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("image", "http://example.com/image.png"))

    def test_extract_markdown_links(self):
        text = "Here is a link [Boot.dev](https://boot.dev) and some text."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("Boot.dev", "https://boot.dev"))

        text = "No links here."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)

        text = "Multiple links [first](https://first.com) and [second](https://second.com)."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("first", "https://first.com"))
        self.assertEqual(links[1], ("second", "https://second.com"))

        text = "Link with special characters [Boot.dev](https://boot.dev?query=1&other=2)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("Boot.dev", "https://boot.dev?query=1&other=2"))

        text = "Links next to images ![image](http://example.com/image.png) and [link](http://example.com)." 
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link", "http://example.com"))

if __name__ == "__main__":
    unittest.main()