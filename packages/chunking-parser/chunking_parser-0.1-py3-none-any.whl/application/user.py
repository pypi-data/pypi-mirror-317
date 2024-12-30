class User:
    def __init__(self, id) -> None:
        self.id = id

    def create_user(self, name): ...

    def get_user(self):
        return self

    def get_userid(self) -> str:
        return self.id

