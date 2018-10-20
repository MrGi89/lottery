from datetime import date, timedelta
from random import randint
from tools import database_cursor

TODAY = date.today()


class Lottery:

    def __init__(self, lottery_id, prize, lottery_date, active):
        self.id = lottery_id
        self.prize = prize
        self.lottery_date = lottery_date
        self.active = active

    @classmethod
    def create(cls, prize, lottery_date):
        """
        Creates and saves to DB lottery class object.
        :param prize: cumulated amount of money that will be divided between winners
        :param lottery_date: date of lottery draw
        :return: Lottery class object
        """
        lottery_id = database_cursor(
            sql='''INSERT INTO lottery VALUES (%s, %s, %s, %s);''',
            variable=(None, prize, lottery_date, 1),
            cursor_type='last_id')

        return cls(lottery_id, prize, lottery_date, 1)

    @classmethod
    def get(cls, lottery_id):
        """
         Select lottery class object from DB.
        :param lottery_id: ID of lottery class object stored in DB
        :return: Lottery class object if exists otherwise returns None
        """
        lottery = database_cursor(
            sql='''SELECT * FROM lottery WHERE lottery_id=%s;''',
            variable=(lottery_id,),
            cursor_type='fetchone')
        return cls(**lottery) if lottery else None

    def set_inactive(self):
        """
        Sets object of lottery class to inactive.
        :return: None
        """
        database_cursor(
            sql='''UPDATE lottery SET active=%s WHERE lottery_id=%s;''',
            variable=(0, self.id))

    def handle_lottery_draw(self):
        """
        Controls lottery draw operations from making a draw to creating another lottery.
        :return: next lottery object
        """
        # self.make_draw()
        self.set_inactive()
        divide_prize = self.divide_prize()

        # Creates new lottery
        next_lottery_date = self.lottery_date + timedelta(days=7)
        cumulation = self.prize if divide_prize is None else self.prize - sum(divide_prize.values())
        return Lottery.create(cumulation, next_lottery_date)

    def make_draw(self):
        """
        Selects 6 random numbers in range 1-49 and saves them to DB.
        :return: None
        """
        # Selects random numbers
        draw_numbers = list()
        while len(draw_numbers) < 6:
            random_number = randint(1, 49)
            if random_number in draw_numbers:
                continue
            draw_numbers.append(random_number)
        # Saves selected numbers to DB
        for number in draw_numbers:
            database_cursor(
                sql='''INSERT INTO lottery_outcomes VALUES (%s, %s, %s);''',
                variable=(None, self.id, number))

    def divide_prize(self):
        """
        Checks how many tickets had at least 3 matches and divide lottery prizes
        based on amount of matches and amount of winning tickets.
        :return:
            - None if no number from ticket matched numbers from lottery draw
            - Dictionary that stores amount of matches(keys) and amount of winning tickets(values)
        """
        outcomes = database_cursor(
            sql='''SELECT category, COUNT(category) AS winners FROM 
                        (SELECT t.user_id, tn.ticket_id, COUNT(lo.number) AS category
                         FROM tickets t 
                         LEFT JOIN ticket_numbers tn ON t.ticket_id=tn.ticket_id
                         LEFT JOIN lottery_outcomes lo ON t.lottery_id=lo.lottery_id AND tn.number=lo.number
                         WHERE t.lottery_id=%s
                         GROUP BY t.user_id, tn.ticket_id) 
                   AS lvl WHERE category > %s
                   GROUP BY category;''',
            variable=(self.id, 2),
            cursor_type='fetchall')

        if not outcomes:
            return None
        # Dictionary that stores: (keys) amount of numbers that can be matched
        #                         (values) amount of money that will be divided between winners
        prizes = {'6': self.prize * 0.4,
                  '5': self.prize * 0.1,
                  '4': self.prize * 0.05,
                  '3': self.prize * 0.02}
        # Dictionary that stores: (keys) amount of numbers that where matched
        #                         (values) amount of money that will be given to winner
        divided_prizes = dict()
        for outcome in outcomes:
            category = str(outcome['category'])
            divided_prizes[category] = prizes[category] / outcome['winners']
        self.select_winners(divided_prizes)
        return divided_prizes

    def select_winners(self, divide_prize):
        """
        Selects user that had at least one lottery ticket that matched at least 3 numbers, assigns prize
        and saves them to DB.
        :param divide_prize: Dictionary that stores amount of matches(keys) and amount of winning tickets(values)
        :return: None
        """
        winners = database_cursor(
            sql='''SELECT * FROM 
                        (SELECT t.user_id, tn.ticket_id, COUNT(lo.number) AS matching
                         FROM tickets t 
                         LEFT JOIN ticket_numbers tn ON t.ticket_id=tn.ticket_id
                         LEFT JOIN lottery_outcomes lo ON t.lottery_id=lo.lottery_id AND tn.number=lo.number
                         WHERE t.lottery_id=%s
                         GROUP BY t.user_id, tn.ticket_id) 
                   AS lvl WHERE matching > %s;''',
            variable=(self.id, 2),
            cursor_type='fetchall')

        for winner in winners:
            database_cursor(sql='''INSERT INTO lottery_winners VALUES(%s, %s, %s, %s, %s);''',
                            variable=(None,
                                      self.id,
                                      winner['ticket_id'],
                                      winner['user_id'],
                                      divide_prize[str(winner['matching'])]))
