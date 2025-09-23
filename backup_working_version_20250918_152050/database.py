import os, psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        self.dsn = os.getenv("DATABASE_DSN")
    
    def get_connection(self):
        return psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)
    
    def get_user(self, user_id: str):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
                return cur.fetchone()
    
    def get_user_courses(self, user_id: str):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT course_id FROM user_courses WHERE user_id = %s", (user_id,))
                return [row['course_id'] for row in cur.fetchall()]
    
    def get_all_courses(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM courses")
                return cur.fetchall()
    
    def assign_course(self, user_id: str, course_id: str):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (user_id, course_id)
                )
                conn.commit()
    
    def get_assignment_history(self, user_id: str, course_id: str):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM user_courses WHERE user_id = %s AND course_id = %s",
                    (user_id, course_id)
                )
                return cur.fetchone()