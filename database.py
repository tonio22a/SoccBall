import sqlite3
from config import DB_NAME

class DB_Manager:
    def __init__(self, database):
        self.database = database
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                country TEXT DEFAULT 'Unknown',
                city TEXT DEFAULT 'Unknown',
                stadium TEXT DEFAULT 'Unknown'
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                team_id INTEGER,
                position TEXT DEFAULT 'Player',
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )''')

            conn.execute('''CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                date TEXT DEFAULT CURRENT_DATE,
                home_team_id INTEGER,
                away_team_id INTEGER,
                home_score INTEGER DEFAULT 0,
                away_score INTEGER DEFAULT 0,
                status TEXT DEFAULT 'scheduled',
                FOREIGN KEY (home_team_id) REFERENCES teams(id),
                FOREIGN KEY (away_team_id) REFERENCES teams(id)
            )''')
            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
    
    def populate_teams(self):
        """Заполняем таблицу команд"""
        teams_data = [
            (1, 'Реал Мадрид', 'Испания', 'Мадрид', 'Сантьяго Бернабеу'),
            (2, 'Барселона', 'Испания', 'Барселона', 'Камп Ноу'),
            (3, 'Интер', 'Италия', 'Милан', 'Джузеппе Меацца'),
            (4, 'Милан', 'Италия', 'Милан', 'Сан Сиро'),
            (5, 'ПСЖ', 'Франция', 'Париж', 'Парк де Пренс'),
            (6, 'Ливерпуль', 'Англия', 'Ливерпуль', 'Энфилд')
        ]
        
        sql = '''INSERT OR IGNORE INTO teams (id, name, country, city, stadium) 
                 VALUES (?, ?, ?, ?, ?)'''
        self.__executemany(sql, teams_data)
        print("Таблица teams заполнена!")
    
    def populate_matches(self):
        """Заполняем таблицу матчей"""
        matches_data = [
            (1, '2024-01-15', 1, 2, 3, 2, 'completed'),  # Реал vs Барса
            (2, '2024-01-16', 3, 4, 1, 1, 'completed'),  # Интер vs Милан
            (3, '2024-01-17', 5, 6, 2, 2, 'completed'),  # ПСЖ vs Ливерпуль
            (4, '2024-02-01', 2, 1, 1, 4, 'scheduled'),  # Барса vs Реал
            (5, '2024-02-02', 4, 3, 0, 0, 'scheduled'),  # Милан vs Интер
            (6, '2024-02-03', 6, 5, 0, 0, 'scheduled')   # Ливерпуль vs ПСЖ
        ]
        
        sql = '''INSERT OR IGNORE INTO matches (id, date, home_team_id, away_team_id, 
                 home_score, away_score, status) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.__executemany(sql, matches_data)
        print("Таблица matches заполнена!")
    
    def populate_players(self):
        """Заполняем таблицу игроков (по 2 игрока на команду для примера)"""
        players_data = [
            # Реал Мадрид
            (1, 'Бензема', 1, 'Нападающий'),
            (2, 'Модрич', 1, 'Полузащитник'),
            
            # Барселона
            (3, 'Левандовски', 2, 'Нападающий'),
            (4, 'Педри', 2, 'Полузащитник'),
            
            # Интер
            (5, 'Лаутaро', 3, 'Нападающий'),
            (6, 'Барелла', 3, 'Полузащитник'),
            
            # Милан
            (7, 'Леao', 4, 'Нападающий'),
            (8, 'Тонали', 4, 'Полузащитник'),
            
            # ПСЖ
            (9, 'Мбаппе', 5, 'Нападающий'),
            (10, 'Мessi', 5, 'Нападающий'),
            
            # Ливерпуль
            (11, 'Салах', 6, 'Нападающий'),
            (12, 'Ван Дейк', 6, 'Защитник')
        ]
        
        sql = '''INSERT OR IGNORE INTO players (id, name, team_id, position) 
                 VALUES (?, ?, ?, ?)'''
        self.__executemany(sql, players_data)
        print("Таблица players заполнена!")
    
    def show_all_data(self):
        """Показать все данные из базы"""
        print("\n=== КОМАНДЫ ===")
        teams = self.__select_data("SELECT * FROM teams ORDER BY id")
        for team in teams:
            print(f"{team[0]}: {team[1]} | {team[2]} | {team[3]} | {team[4]}")
        
        print("\n=== ИГРОКИ ===")
        players = self.__select_data('''
            SELECT p.id, p.name, t.name, p.position 
            FROM players p 
            JOIN teams t ON p.team_id = t.id 
            ORDER BY t.name, p.name
        ''')
        for player in players:
            print(f"{player[0]}: {player[1]} | {player[2]} | {player[3]}")
        
        print("\n=== МАТЧИ ===")
        matches = self.__select_data('''
            SELECT m.id, m.date, t1.name, t2.name, m.home_score, m.away_score, m.status
            FROM matches m
            JOIN teams t1 ON m.home_team_id = t1.id
            JOIN teams t2 ON m.away_team_id = t2.id
            ORDER BY m.date
        ''')
        for match in matches:
            status = "✅" if match[6] == 'completed' else "⏰"
            print(f"{match[0]}: {match[1]} {status} {match[2]} {match[4]}-{match[5]} {match[3]}")

if __name__ == '__main__':
    manager = DB_Manager(DB_NAME)
    manager.create_tables()
    
    # Заполняем базу данных
    manager.populate_teams()
    manager.populate_players()
    manager.populate_matches()
    
    # Показываем все данные
    manager.show_all_data()