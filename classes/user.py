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
        """
        Finds user objects stored in DB.
        :param user_id: User id
        :return: User object if it exists in DB otherwise returns None
        """
        user = database_cursor(
            sql='''SELECT * FROM users WHERE user_id=%s;''',
            variable=(user_id,),
            cursor_type='fetchone')

        return cls(**user) if user else None

    @classmethod
    def get_all(cls):
        """
        Finds all active users stored in DB.
        :return: List of all active users
        """
        users = database_cursor(
            sql='''SELECT * FROM users WHERE active=%s;''',
            variable=(1,),
            cursor_type='fetchall')

        return list(users)

    def update(self, first_name, last_name, email):
        """
        Updates user object stored in DB.
        :param first_name: User new first name
        :param last_name: User new last name
        :param email: User new email
        :return: None
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        database_cursor(
            sql='''UPDATE users SET first_name=%s, last_name=%s, email=%s WHERE user_id=%s;''',
            variable=(self.first_name, self.last_name, self.email, self.id))

    def set_inactive(self):
        """
        Sets user object stored in DB to inactive.
        :return: None
        """
        database_cursor(
            sql='''UPDATE users SET active=%s WHERE user_id=%s;''',
            variable=(0, self.id))
