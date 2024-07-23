import sqlite3

class PensionDatabase:
    def __init__(self, db_name='pension_schemes.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.update_schema()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS db_schemes
        (id INTEGER PRIMARY KEY, name TEXT, accrual_rate REAL)
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS dc_schemes
        (id INTEGER PRIMARY KEY, name TEXT)
        ''')
        self.conn.commit()

    def update_schema(self):
        # Update db_schemes table
        self.update_table_schema('db_schemes', [
            ('accrual_rate', 'REAL'),
            ('normal_retirement_age', 'INTEGER')
        ])
        
        # Update dc_schemes table
        self.update_table_schema('dc_schemes', [
            ('default_contribution_rate', 'REAL')
        ])

    def update_table_schema(self, table_name, columns_to_add):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        existing_columns = [column[1] for column in self.cursor.fetchall()]
        
        for column_name, column_type in columns_to_add:
            if column_name not in existing_columns:
                self.cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}')
        
        self.conn.commit()

    def add_db_scheme(self, name, accrual_rate, normal_retirement_age):
        self.cursor.execute('INSERT INTO db_schemes (name, accrual_rate, normal_retirement_age) VALUES (?, ?, ?)',
                            (name, accrual_rate, normal_retirement_age))
        self.conn.commit()

    def add_dc_scheme(self, name, default_contribution_rate):
        self.cursor.execute('INSERT INTO dc_schemes (name, default_contribution_rate) VALUES (?, ?)',
                            (name, default_contribution_rate))
        self.conn.commit()

    def get_db_schemes(self):
        self.cursor.execute('SELECT * FROM db_schemes')
        return self.cursor.fetchall()

    def get_dc_schemes(self):
        self.cursor.execute('SELECT * FROM dc_schemes')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()