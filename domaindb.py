import sqlite3

# Create connection to database domaindb.sqlite
conn = sqlite3.connect('domaindb.sqlite')

# Create a database cursor to execute SQL queries
cur = conn.cursor()

# Deletes Counts table if already exists in the database
cur.execute('''
            DROP TABLE IF EXISTS Counts
            ''')

# Create Counts table in the database
cur.execute('''
            CREATE TABLE Counts (
                org TEXT, 
                count INTEGER)
            ''')

# Open a file from user input
fname = input("Enter file name: ")

if(len(fname) < 1):
    fname = "mbox.txt"

fh = open(fname)

# Reads lines from the file that stars with 'From'
for line in fh:
    if not line.startswith('From: '):
        continue

# Looks for emails domains
    domainpos = line.find('@')
    domain = line[domainpos+1:].strip()

# Looks for the domain in the table Counts
    cur.execute(
                '''
                SELECT count
                FROM Counts
                WHERE org = ?
                ''', (domain,)
                )
    row = cur.fetchone()

    if row is None:
        cur.execute(
                    '''
                    INSERT INTO Counts (org, count)
                    VALUES (?, 1)
                    ''', (domain,)
                    )
    else:
        cur.execute('''
                    UPDATE Counts
                    SET count = count + 1
                    WHERE org = ?
                    ''', (domain,))

    # Saves new updates in the database    
    conn.commit()


#https://www.sqlite.org/lang_select.html
sqltr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqltr):
    print(str(row[0]), row[1])

# Closes connection to database
cur.close()
    
