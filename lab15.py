import sqlite3 as sq

    
conn=sq.connect('student_record.db')
cursor=conn.cursor()

cursor.execute('''Create table if not exists student_record
               (Enrollment_no INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                mark INTEGER NOT NULL
                )''')
conn.commit()

student_record=[
    (92301733005,'Helena Chongo','PWP',85),
    (92301733004, 'Duclas Matsinhe','PWP',100),
    (92301733003, 'Albeija Laissane','PWP',98),
    (92301733008, 'Yurica Caetano','PWP',100)
    ]
cursor.executemany('''INSERT INTO student_record (Enrollment_no, name, subject, mark)
                   VALUES (?, ?, ?, ?)''',student_record)
conn.commit()

cursor.execute('SELECT * FROM student_record')
rows=cursor.fetchall()

print("All Students Records:")
for row in rows:
    print(row)

