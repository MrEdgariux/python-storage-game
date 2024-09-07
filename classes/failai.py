from datetime import datetime
class Failas():
    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file_size = len(content)

    def read(self):
        return self.content

    def write(self, tekstas):
        self.content = tekstas
        self.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file_size = len(self.content)

    def __str__(self):
        return f"{self.name} {self.file_size}B {self.last_modified}"
    
    def __dict__(self):
        return {
            "name": self.name,
            "content": self.content,
            "last_modified": self.last_modified,
            "file_size": self.file_size
        }
    
    @classmethod
    def from_dict(cls, data):
        file = cls(data["name"], data["content"])
        file.last_modified = data["last_modified"]
        file.file_size = data["file_size"]
        return file