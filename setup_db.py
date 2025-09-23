from dotenv import load_dotenv
load_dotenv()

import csv, psycopg2
from database import Database

def setup_database():
    db = Database()
    
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            # Создаем таблицы
            cur.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    course_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    duration_minutes INTEGER,
                    url TEXT,
                    tags TEXT,
                    prerequisites TEXT,
                    provider TEXT
                )
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    role TEXT NOT NULL,
                    department TEXT
                )
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_courses (
                    user_id TEXT,
                    course_id TEXT,
                    completed_on DATE,
                    PRIMARY KEY (user_id, course_id)
                )
            """)
            
            # Загружаем данные из CSV
            with open('data/courses.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cur.execute("""
                        INSERT INTO courses VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (course_id) DO NOTHING
                    """, (row['course_id'], row['title'], row['description'], 
                         row['category'], row['duration_minutes'], row['url'],
                         row['tags'], row['prerequisites'], row['provider']))
            
            with open('data/users.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cur.execute("""
                        INSERT INTO users VALUES (%s,%s,%s,%s,%s)
                        ON CONFLICT (user_id) DO NOTHING
                    """, (row['user_id'], row['name'], row['email'], 
                         row['role'], row['department']))
            
            with open('data/user_courses.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cur.execute("""
                        INSERT INTO user_courses VALUES (%s,%s,%s)
                        ON CONFLICT (user_id, course_id) DO NOTHING
                    """, (row['user_id'], row['course_id'], row['completed_on']))
            
            conn.commit()
    
    print("База data настроена!")

if __name__ == "__main__":
    setup_database()