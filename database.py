import pymysql
from pymysql.cursors import DictCursor
import os

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME'),
        charset=os.getenv('DB_CHARSET', 'utf8mb4'),
        cursorclass=DictCursor
    )

def get_players_from_db():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT game_name as name, tag_line as tag FROM players"
            cursor.execute(sql)
            players = cursor.fetchall()
        return players
    except Exception as e:
        print(f"DB Error: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def add_player(game_name, tag_line):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO players (game_name, tag_line) VALUES (%s, %s)"
            cursor.execute(sql, (game_name, tag_line.upper()))
            conn.commit()
            return True
    except pymysql.err.IntegrityError:
        return False
    except Exception as e:
        print(f"DB Error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def remove_player(game_name, tag_line):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "DELETE FROM players WHERE game_name = %s AND tag_line = %s"
            cursor.execute(sql, (game_name, tag_line.upper()))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"DB Error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close() 