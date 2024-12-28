import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cur = self.conn.cursor()
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS bdd_moves(command, action, bdd_script)")


    def insert_into_table(self, command, action, bdd_script):
        res = self.cur.execute("SELECT 1 FROM bdd_moves WHERE command = ?", (command,))
        if res.fetchone() is None:
            self.cur.execute("INSERT INTO bdd_moves VALUES (?, ?, ?)", (command, action, bdd_script))
            self.save_database()


    def get_all_actions(self):
        res = self.cur.execute("SELECT command, action, bdd_script FROM bdd_moves")
        return res.fetchall()


    def get_specific_action(self, command):
        res = self.cur.execute("SELECT command, action, bdd_script FROM bdd_moves WHERE command = ?", (command,))
        return res.fetchone()


    def destroy_table(self):
        self.cur.execute("DROP TABLE bdd_moves")
        self.save_database()


    def save_database(self):
        self.conn.commit()

# conn = sqlite3.connect("database.db")
# database = Database()
# # database.destroy_table()
# # database.save_database()

# database.insert_into_table("command", "action", "bdd_script")
# database.insert_into_table("command2", "action3", "bdd_script4")
# # # # conn.commit()
# # database.save_database()
# print(database.get_all_actions())
# print(database.get_specific_action("command"))
# print(Database().destroy_table())
database = Database()
# # database.destroy_table()
# # database.save_database()

database.insert_into_table("command", "action", "bdd_script")
# database.insert_into_table("command2", "action3", "bdd_script4")
# # # # conn.commit()
# # database.save_database()
# print(database.get_all_actions())
print(database.get_specific_action("command"))