import requests


class Message:
    hook: str
    text: str = ""

    def __init__(self, hook: str):
        self.hook = hook

    def isValid(self) -> bool:
        return self.hook is not None and self.hook != ""

    def addSection(self, text: str):
        self.text += text

    def printme(self):
        print(self.hook)
        print(self.text)

    def send(self):
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self.hook,
            json={"text": self.text},
            headers=headers,
            timeout=60,
        )
        print(response.status_code)
        print(response.content)
