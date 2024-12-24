import psycopg2
from config.db_config import DB_CONFIG
from src.timer import Timer

class UserManager:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def create_temp_user(self, user, pwd):
        self.drop_temp_user(user)  # Drop existing user if it exists
        create_user_sql = f"CREATE USER {user} WITH PASSWORD '{pwd}';"
        self.cursor.execute(create_user_sql)
        # Grant permissions to the user
        self.grant_permissions(user)
        
    def drop_temp_user(self, user):
        drop_user_sql = f"DROP USER IF EXISTS {user};"
        self.cursor.execute(drop_user_sql)

    def grant_permissions(self, user):
        # Grant SELECT permission on a specific table
        grant_permission_sql = f"GRANT SELECT ON TABLE admin_users TO {user};"  # Adapt as needed
        self.cursor.execute(grant_permission_sql)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    manager = UserManager()
    temp_user = 'temp_user'
    temp_password = 'temp_password'
    
    print(f"Attempting to create temporary user '{temp_user}'...")
    manager.create_temp_user(temp_user, temp_password)
    print(f"Temporary user '{temp_user}' created. It will be deleted after 10 minutes.")

    # Initialize timer for 10 minutes
    print("Starting timer for 10 minutes...")
    t = Timer(10, manager.drop_temp_user, args=(temp_user,))
    t.start()

    print("You can now use this user for database operations.")
    print("The program will exit, but the timer will continue to delete the user after the time expires.")
