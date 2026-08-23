from html.parser import HTMLParser

class HTMLToText(HTMLParser):
    # Block-level tags become a line break so words either side don't run
    # together (e.g. "<p>Java</p><p>SQL</p>" -> "Java\nSQL", not "JavaSQL").
    _BLOCK_TAGS = {
        'p', 'br', 'div', 'li', 'ul', 'ol', 'tr', 'table', 'section',
        'article', 'header', 'footer', 'blockquote',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)  # decodes &amp; &nbsp; etc.
        self._parts = []

    def handle_data(self, data):
        self._parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in self._BLOCK_TAGS:
            self._parts.append('\n')

    def handle_endtag(self, tag):
        if tag in self._BLOCK_TAGS:
            self._parts.append('\n')

    def get_text(self):
        return ''.join(self._parts)