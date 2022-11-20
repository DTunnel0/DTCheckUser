import os


def page_content():
    filename = os.path.join(os.path.dirname(__file__), 'page.html')
    with open(filename, 'r') as f:
        return f.read()
