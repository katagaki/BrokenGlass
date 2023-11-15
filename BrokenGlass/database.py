import hashlib
import pymysql


def init_database(cursor):
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            Username VARCHAR(255) PRIMARY KEY NOT NULL,
            Password TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserProfile (
            Username VARCHAR(255) NOT NULL,
            Name TEXT NOT NULL,
            LastSignIn DATE NULL,
            FOREIGN KEY (Username) REFERENCES User(Username) ON DELETE CASCADE
        );
    """)
    # Create initial data
    admin_password = hashlib.sha256(b"password").hexdigest()
    justin_password = hashlib.sha256(b"rosebud2").hexdigest()
    cursor.execute("INSERT IGNORE INTO User VALUES (%s, %s);", ["admin", admin_password])
    cursor.execute("INSERT IGNORE INTO User VALUES (%s, %s);", ["justin", justin_password])
    cursor.execute("INSERT IGNORE INTO UserProfile VALUES (%s, %s, NULL);", ["admin", "System Admin"])
    cursor.execute("INSERT IGNORE INTO UserProfile VALUES (%s, %s, NULL);", ["justin", "Katagaki Shintaro"])


conn = pymysql.connect(host='localhost', port=3306, user='root', password='P@ssw0rd!', db='broken_glass')
cursor = conn.cursor()
init_database(cursor)
conn.commit()
