from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, img_path, is_creator, firstname, surname, email):
        self.id = id
        self.username = username
        self.password = password
        self.img_path = img_path
        self.is_creator = is_creator
        self.firstname = firstname
        self.surname = surname
        self.email = email