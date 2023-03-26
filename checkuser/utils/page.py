PAGE_FILE = './pages/client.html'


def get_page_content(path: str = PAGE_FILE) -> str:
    with open(path) as f:
        content = f.read()
        return content
