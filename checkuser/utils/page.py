import logging

PAGE_FILE = './pages/client.html'


def get_page_content(path: str = PAGE_FILE) -> str:
    try:
        with open(path) as f:
            content = f.read()
            return content
    except FileNotFoundError:
        from .default_page import page

        logging.info('Could load page %s', path)
        return page
