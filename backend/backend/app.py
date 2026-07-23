from flask import Flask, render_template, request, redirect
import mysql.connector
def get_db():
  return mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="2aHs1wFAJDAzGua.root",
    password="pianLC4XT5r5HcE4",
    database="blood_bank_db",
    ssl_disabled=False
)

app = Flask(__name__)

db = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="2aHs1wFAJDAzGua.root",
    password="pianLC4XT5r5HcE4",
    database="blood_bank_db",
    ssl_disabled=False
)

def get_db():
    global db
    if not db.is_connected():
        db.reconnect(attempts=3, delay=2)
    return db

@app.route("/")
def home():
    success = request.args.get("success")
    return render_template("index.html", success=success)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        age = request.form["age"]
        blood_group = request.form["blood_group"]
        phone = request.form["phone"]

        db = get_db()
        cursor = db.cursor()

        sql = """INSERT INTO donor
        (donor_name, blood_group, age, phone)
        VALUES (%s, %s, %s, %s)"""

        cursor.execute(sql, (name, blood_group, age, phone))
        db.commit()
        cursor.close()
        db.close()

        return redirect("/?success=1")

    return render_template("register.html")
    

@app.route("/donors")
def donors():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM donor")
    donors = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("donors.html", donors=donors)
@app.route("/delete/<int:donor_id>")
def delete_donor(donor_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM donor WHERE donor_id = %s", (donor_id,))
    db.commit()
    return redirect("/donors")
@app.route('/search', methods=['POST'])
def search_donor():
    search = request.form['search'].strip()

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM donor WHERE blood_group=%s",
        (search,)
    )

    donors = cursor.fetchall()

    cursor.close()
    db.close()

    if len(donors) == 0:
        return render_template("notfound.html", blood_group=search)

    return render_template("donors.html", donors=donors)

@app.route("/findblood")
def findblood():
    return render_template("findblood.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/hospital")
def hospital():
    return render_template("hospital.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    