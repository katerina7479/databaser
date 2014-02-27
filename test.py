from database import Database
import unittest
import os

tables = {'tables': {'legs': 'integer', 'material': 'text'},
          'clients': {'name': 'text', 'address': 'text', 'phone': 'integer'}}


class DbTest(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.db.create_tables(tables)
        self.tablename = 'tables'

    def tearDown(self):
        os.remove('database.sqlite')

    def test_exists(self):
        test = os.path.isfile('database.sqlite')
        self.assertEqual(test, True)

    def test_add(self):
        row = self.db.add(self.tablename, {'legs': 4, 'material': 'wood'})
        self.assertEqual(row, 1)

        test = self.db.delete(self.tablename, row)
        self.assertEqual(test, True)

    def test_copy(self):
        row = self.db.add(self.tablename, {'legs': 4, 'material': 'wood'})
        self.assertEqual(row, 1)

        row2 = self.db.copy(self.tablename, row)
        self.assertEqual(row2, 2)

        data = self.db.query(self.tablename, row=row2)
        self.assertEqual(data['material'], 'wood')

        test = self.db.delete(self.tablename, row)
        self.assertEqual(test, True)

        test = self.db.delete(self.tablename, row2)
        self.assertEqual(test, True)

    def test_tables(self):
        table_list = self.db.get_table_list()
        self.assertIn(self.tablename, table_list)

    def test_query(self):
        row = self.db.add(self.tablename, {'legs': 4, 'material': 'wood'})
        self.assertEqual(row, 1)

        result = self.db.query(self.tablename)[0]
        self.assertEqual(result['legs'], 4)
        self.assertEqual(result['material'], 'wood')

        test = self.db.delete(self.tablename, row)
        self.assertEqual(test, True)

    def test_query_table_row(self):
        row = self.db.add('clients', {'name': 'Fischer', 'address': 'Next door', 'phone': 23645})
        self.assertEqual(row, 1)
        row = self.db.add('clients', {'name': 'Tolouse', 'address': '55th st', 'phone': 8928384})
        self.assertEqual(row, 2)

        result = self.db.query('clients', row=2)
        self.assertEqual(result['id'], 2)
        self.assertEqual(result['name'], 'Tolouse')

    def test_query_cols_all(self):
        row = self.db.add('clients', {'name': 'Fischer', 'address': 'Next door', 'phone': 23645})
        self.assertEqual(row, 1)
        row = self.db.add('clients', {'name': 'Tolouse', 'address': '55th st', 'phone': 8928384})
        self.assertEqual(row, 2)

        result = self.db.query('clients', cols=['id', 'name'])

        index = 1
        for row in result:
            self.assertEqual(row[0], index)
            index += 1

    def test_query_cols_where(self):
        row = self.db.add('clients', {'name': 'Fischer', 'address': 'Next door', 'phone': 23645})
        self.assertEqual(row, 1)
        row = self.db.add('clients', {'name': 'Tolouse', 'address': '55th st', 'phone': 8928384})
        self.assertEqual(row, 2)

        result = self.db.query('clients', cols=['id', 'phone'], wcol='phone', wval=23645)
        result = result[0]
        self.assertEqual(result[0], 1)

    def test_query_where(self):
        row = self.db.add('clients', {'name': 'Fischer', 'address': 'Next door', 'phone': 23645})
        self.assertEqual(row, 1)
        row = self.db.add('clients', {'name': 'Tolouse', 'address': '55th st', 'phone': 8928384})
        self.assertEqual(row, 2)

        result = self.db.query('clients', wcol='phone', wval=23645)
        result = result[0]
        self.assertEqual(result['id'], 1)

if __name__ == '__main__':
    unittest.main()
