from flask import Flask, render_template, url_for, request
import sqlite3
import bcrypt
from data import *
conn = sqlite3.connect("data.db", check_same_thread=False)
# password = b"cba"
# salt = bcrypt.gensalt()
# print(salt)
# hashed = bcrypt.hashpw(password, salt)
# print(hashed)

cursor = conn.cursor()
# cursor.execute("DROP TABLE IF EXISTS Cards")
# cursor.execute("""CREATE TABLE Cards (
# picture_url TEXT,
# card_title TEXT,
# card_text TEXT
# );
# """)

# for info in home_page_data:
#     cursor.execute(f"""INSERT INTO Cards
#     (picture_url, card_title, card_text) VALUES {info}
#     """)

# cursor.execute("DROP TABLE IF EXISTS Students")
# cursor.execute("""CREATE TABLE Students (
# bavshvis_saxeli TEXT,
# bavshvis_gvari TEXT,
# klasi TEXT,
# bavhsvis_piradi_nomeri TEXT,
# mshoblis_piradi_nomeri TEXT,
# mshoblis_saxeli TEXT,
# mshoblis_gvari TEXT,
# mshoblis_telefonis_nomeri TEXT
# );
# """)


# conn.commit()







app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    cursor.execute("SELECT * FROM Cards")
    all_cards = cursor.fetchall()

    return render_template("home.html", all_cards=all_cards)



@app.route("/store")
def store():
    return render_template("store.html")



@app.route("/register",  methods = ["GET", "POST"])
def register():
    add = []
    if request.method == "POST":
        answer0 = request.form.get("answer0")
        answer1 = request.form.get("answer1")
        answer2 = request.form.get("answer2")
        answer3 = request.form.get("answer3")
        answer4 = request.form.get("answer4")
        answer5 = request.form.get("answer5")
        answer6 = request.form.get("answer6")
        answer7 = request.form.get("answer7")
        answer_tuple = (answer0, answer1, answer2, answer3, answer4, answer5, answer6, answer7)

        for ans in answer_tuple:
            if 0 < len(ans) <= 20:
                add.append(True)
            else:
                add.append(False)


        if False not in add:
            cursor.execute(f"""INSERT INTO Students
            (bavshvis_saxeli, bavshvis_gvari, klasi, bavhsvis_piradi_nomeri, mshoblis_piradi_nomeri, mshoblis_saxeli, mshoblis_gvari, mshoblis_telefonis_nomeri) VALUES {answer_tuple}
            """)
            conn.commit()
    return render_template("register.html", add = add)







if __name__ == "__main__":
    app.run(debug=True)