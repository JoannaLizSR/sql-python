import sqlite3

# Create connection to database domaindb.sqlite
conn = sqlite3.connect('emaildb.sqlite')

# Create a database cursor to execute SQL queries
cur = conn.cursor()

# Deletes Counts table if already exists in the database
cur.execute('''
            DROP TABLE IF EXISTS Counts
            ''')

# Create Counts table in the database
cur.execute('''
            CREATE TABLE Counts (
                email TEXT,
                count INTEGER
            )
            ''')

# Open a file from user input
fname = input("Enter file name: ")

if(len(fname) < 1):
    fname = "mbox-short.txt"

fh = open(fname)

# Reads lines from the file that stars with 'From' and stores email adresses
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    cur.execute(
                '''
                SELECT count
                FROM Counts
                WHERE email = ?
                ''', (email,)
                )
    row = cur.fetchone()

    if row is None:
        cur.execute(
                    '''
                    INSERT INTO Counts (email, count)
                    VALUES (?, 1)
                    ''', (email,)
                    )
    else:
        cur.execute('''
                    UPDATE Counts
                    SET count = count + 1
                    WHERE email = ?
                    ''', (email,))
    
    # Saves new updates in the database        
    conn.commit()


#https://www.sqlite.org/lang_select.html
sqltr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqltr):
    print(str(row[0]), row[1])

# Closes connection to database
cur.close()
