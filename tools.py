import MySQLdb


def database_cursor(sql, variable=None, cursor_type=None):
    """Connects to DB and executes given sql command"""

    db = MySQLdb.connect(host='localhost',
                         user='lottery',
                         passwd='LoTteRyPsW134!',
                         db='lottery',
                         charset='utf8')

    db.autocommit(True)
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    if variable:
        cursor.execute(sql, variable)
    if not variable:
        cursor.execute(sql)
    search_result = None
    if cursor_type:
        if cursor_type == 'fetchone':
            search_result = cursor.fetchone()
        if cursor_type == 'fetchall':
            search_result = cursor.fetchall()
        if cursor_type == 'last_id':
            search_result = cursor.lastrowid
    cursor.close()
    db.close()
    return search_result
