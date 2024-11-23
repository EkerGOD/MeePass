"""
sql语句
"""
CREATE_PASSWORDS = '''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            account TEXT NOT NULL,
            password TEXT NOT NULL,
            group_id INTEGER NOT NULL,
            notes TEXT
        )
    '''
CREATE_GROUPS = '''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            parent_id INTEGER NOT NULL
        )
    '''
INSERT_PASSWORDS = '''
        INSERT INTO passwords (account, password, group_id, notes) 
        VALUES (?, ?, ?, ?)
    '''

SELECT_PASSWORDS = '''
        SELECT password FROM passwords WHERE account = ?
'''