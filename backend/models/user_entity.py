# User class to store user data and allow it to be retrieved through a list
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    # Returns a dictionary of the data for easy reading and logging
    def get_dict(self) -> dict:
        return {"user_id": self.user_id, "name": self.name, "email": self.email}
