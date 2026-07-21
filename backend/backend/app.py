from flask import Flask, render_template, request, redirect
import mysql.connector
mydb = mysql.connector.connect(
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

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        age = request.form["age"]
        blood_group = request.form["blood_group"]
        phone = request.form["phone"]

        cursor = db.cursor()

        sql = """INSERT INTO donor
        (donor_name, blood_group, age, phone)
        VALUES (%s, %s, %s, %s)"""

        cursor.execute(sql, (name, blood_group, age, phone))
        db.commit()

        return "Donor Registered Successfully"

    return render_template("register.html")
    

@app.route("/donors")
def donors():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM donor")
    donors = cursor.fetchall()
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

    cursor = mydb.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM donor WHERE blood_group=%s",
        (search,)
    )

    donors = cursor.fetchall()
    cursor.close()

    return render_template('donors.html', donors=donors)
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
    