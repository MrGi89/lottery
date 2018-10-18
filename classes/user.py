from tools import database_cursor


class User:

    def __init__(self, user_id, first_name, last_name, email, active):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.active = active

    @classmethod
    def create(cls, first_name, last_name, email):
        """
        Creates User object and saves it to DB.
        :param first_name: user first name
        :param last_name: user last name
        :param email: user email
        :return: User object
        """
        user_id = database_cursor(
            sql='''INSERT INTO users VALUES (%s, %s, %s, %s, %s);''',
            variable=(None, first_name, last_name, email, 1),
            cursor_type='last_id')
        return cls(user_id, first_name, last_name, email, 1)

    @classmethod
    def get(cls, user_id):
        user = database_cursor(
            sql='''SELECT * FROM users WHERE user_id=%s;''',
            variable=(user_id,),
            cursor_type='fetchone')
        return cls(**user) if user else None
