from datetime import date
from tools import database_cursor

TODAY = date.today()


class Ticket:

    def __init__(self, ticket_id, lottery_id, user_id, create_date, numbers):
        self.ticket_id = ticket_id
        self.lottery_id = lottery_id
        self.user_id = user_id
        self.create_date = create_date
        self.numbers = numbers

    @classmethod
    def create(cls, lottery_id, user_id, numbers):
        """
        Creates Ticket object and stores it in DB.
        :param lottery_id: Lottery id that indicates to which lottery ticket was bought
        :param user_id: User id that indicates to which user ticket belong
        :param numbers: List of numbers chosen by user
        :return: Ticket object saved in DB
        """
        ticket_id = database_cursor(
            sql='''INSERT INTO tickets VALUES (%s, %s, %s, %s);''',
            variable=(None, lottery_id, user_id, TODAY),
            cursor_type='last_id')

        for number in numbers:
            database_cursor(
                sql='''INSERT INTO ticket_numbers VALUES (%s, %s, %s);''',
                variable=(None, ticket_id, number))

        return cls(ticket_id, lottery_id, user_id, TODAY, numbers)

    @staticmethod
    def get_all(user_id):
        """
        Finds all user tickets stored in DB.
        :param user_id: User id
        :return: List of all user tickets and chosen numbers stored in DB
        """
        tickets = database_cursor(
            sql='''SELECT t.ticket_id, t.lottery_id, t.create_date, GROUP_CONCAT(tn.number) AS numbers
                   FROM tickets t 
                   LEFT JOIN ticket_numbers tn ON t.ticket_id=tn.ticket_id
                   WHERE t.user_id=%s
                   GROUP BY t.ticket_id
                   ORDER BY t.ticket_id DESC''',
            variable=(user_id,),
            cursor_type='fetchall')
        # For all user tickets changes founded numbers to sorted list
        for ticket in tickets:
            numbers = ticket['numbers'].split(',')
            numbers.sort()
            ticket['numbers'] = numbers
        return list(tickets)
