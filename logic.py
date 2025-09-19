import sqlite3
import random

class FootballLogic:
    def __init__(self, db_name):
        self.db_name = db_name
    
    def get_teams(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("SELECT id, name, country, city, stadium FROM teams ORDER BY id")
        teams = cur.fetchall()
        conn.close()
        return teams
    
    def update_team(self, team_id, new_name, new_stadium):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("UPDATE teams SET name=?, stadium=? WHERE id=?", (new_name, new_stadium, team_id))
        conn.commit()
        conn.close()
    
    def simulate_match(self, home_id, away_id):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("SELECT name, stadium FROM teams WHERE id=?", (home_id,))
        home_team, stadium = cur.fetchone()
        cur.execute("SELECT name FROM teams WHERE id=?", (away_id,))
        away_team = cur.fetchone()[0]
        conn.close()
        
        home_score = random.randint(0, 4)
        away_score = random.randint(0, 4)
        return home_team, away_team, stadium, home_score, away_score
    
    def get_stats(self):
        return {
            'удары': f"{random.randint(10, 20)}-{random.randint(8, 18)}",
            'владение': f"{random.randint(45, 65)}%-{random.randint(35, 55)}%",
            'угловые': f"{random.randint(3, 8)}-{random.randint(2, 7)}",
            'фолы': f"{random.randint(8, 15)}-{random.randint(7, 14)}"
        }