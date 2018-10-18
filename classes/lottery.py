from datetime import date
from random import randint
from tools import database_cursor

TODAY = date.today()


class Lottery:

    def __init__(self, lottery_id, prize, lottery_date):
        self.id = lottery_id
        self.prize = prize
        self.lottery_date = lottery_date

    @classmethod
    def create(cls, prize, lottery_date):
        lottery_id = database_cursor(
            sql='''INSERT INTO lottery VALUES (%s, %s, %s);''',
            variable=(None, prize, lottery_date),
            cursor_type='last_id')

        return cls(lottery_id, prize, lottery_date)

    def make_draw(self):
        draw_numbers = list()
        while len(draw_numbers) < 5:
            random_number = randint(1, 20)
            if random_number in draw_numbers:
                continue
            draw_numbers.append(random_number)

        for number in draw_numbers:
            database_cursor(
                sql='''INSERT INTO lottery_outcomes VALUES (%s, %s, %s);''',
                variable=(None, self.id, number))

    def find_winners(self):
        pass
