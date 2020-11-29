import unittest

from jinja2 import FileSystemLoader, Environment, select_autoescape

class MyWebpage:
    def __init__(self, filename="default.html", input_=None):
        self.filename = ''.join(filename.split('.')[:-1]) + '.html'
        template_loader = FileSystemLoader(searchpath="./")
        template_env = Environment(loader=template_loader,
            autoescape=select_autoescape(['html', 'xml']))
        self.template = template_env.get_template("template.html")
        if not input_ is None:
            self.input_ = input_
        else:
            self.input_ = {
                "title": "Webpage",
                "body": {
                    "navigation": [{
                        "href": "http://www.example.com", "caption": "EXAMPLE"
                    }]
                }
            }

    def render_webpage(self):
        self.template_rendered = self.template.render(data=self.input_)
    
    def save_webpage(self):
        with open(self.filename, 'w') as f:
            f.write(self.template_rendered)
        print("Saved webpage!")

class TestWebpageJinja(unittest.TestCase):
    def setUp(self):
        self.webpage = MyWebpage()

    def test_render_webpage(self):
        default_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <title>Webpage</title>
            </head>
            <body>
            <h1>Navigation</h1>
            <ul id="navigation">
            <li><a href="http://www.example.com">EXAMPLE</a></li>
            </ul>
            </body>
            </html>
        """
        default_html = [line.strip() for line in default_html.split("\n")]
        default_html = [line for line in default_html if not line == ""]
        self.webpage.render_webpage()
        test_html = [line.strip() for line in self.webpage.template_rendered.split("\n")]
        test_html = [line for line in test_html if not line == ""]
        self.assertEqual(len(default_html), len(test_html))

        for i in range(len(test_html)):
            with self.subTest(i=i):
                self.assertEqual(default_html[i], test_html[i])

if __name__ == "__main__":
    unittest.main()
