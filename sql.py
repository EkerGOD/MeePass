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
        INSERT INTO passwords (title, username, password, url, notes, group_id) 
        VALUES (?, ?, ?, ?, ?, ?)
    '''

SELECT_PASSWORDS = '''
        SELECT password FROM passwords WHERE username = ?
'''

SELECT_GROUPS = '''
SELECT * FROM groups'''

SELECT_PASSWORDS_BY_GROUP = '''
SELECT title, username, password, url, notes FROM passwords WHERE group_id = ?
'''