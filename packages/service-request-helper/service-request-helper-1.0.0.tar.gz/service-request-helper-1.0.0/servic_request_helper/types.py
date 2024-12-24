class ResponseFile:
    content = None
    filename = None
    mimetype = None

    def __init__(self, content, filename=None, mimetype=None):
        self.content = content
        self.filename = filename
        self.mimetype = mimetype

    @property
    def size_in_bytes(self):
        return len(self.content)


    def save(self, path):
        with open(path, 'wb') as file:
            result = file.write(self.content)
        return result