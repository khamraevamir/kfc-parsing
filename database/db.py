import sqlite3 as sq


class Database:

    def __init__(self, **kwargs):
        self._filename = kwargs.get('filename')
        self._db = sq.connect(kwargs.get('filename'))
        self._table = kwargs.get('table')

    def create(self, sql):
        cursor = self._db.cursor()

        try:
            cursor.execute(f'''CREATE TABLE {self._table}({sql})''')
        except:
            result = input(f'This {self._table} is already exists.\nYES - DROP, NO - continue\n')
            if result.lower() == 'yes':
                cursor.execute(f"DROP TABLE IF EXISTS {self._table}")
                self._db.commit()
                print(f'Table {self._table} deleted successfully!')
            else:
                print('Try again!')
        self._db.commit()

    def post(self, **kwargs):
        keys = ', '.join([key for key in kwargs.keys()])
        values = [value for value in kwargs.values()]
        quant = ', '.join(['?' for i in range(0, len(kwargs))])
        cursor = self._db.cursor()
        sql = 'INSERT INTO {}({}) values({})'.format(self._table, keys, quant)
        cursor.execute(sql, tuple(values))
        self._db.commit()

    def delete(self, id):
        sql = 'DELETE FROM {} WHERE id = ?', format(self._table)
        cursor = self._db.cursor()
        cursor.execute(sql, tuple(str(id), ))
        self._db.commit()
        print("Record Deleted successfully ")

    def get(self, id):
        sql = 'SELECT * from {} WHERE id = ?'.format(self._table)
        cursor = self._db.cursor()
        cursor.execute(sql, tuple(str(id), ))
        return list(cursor.fetchone())

    def get_all(self):
        sql = 'SELECT * from {}'.format(self._table)
        cursor = self._db.cursor()
        cursor.execute(sql)
        return list(cursor.fetchall())

    def put(self, id, data):
        keys = ', '.join([key + ' = ?' for key in data.keys()])
        values = [value for value in data.values()]
        cursor = self._db.cursor()
        sql = 'UPDATE {} SET {} WHERE id = {}'.format(self._table, keys, id)
        cursor.execute(sql, tuple(values))
        self._db.commit()

    def close(self):
        del self._filename
