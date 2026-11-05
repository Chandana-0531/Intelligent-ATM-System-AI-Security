from flask import Flask, render_template, request, redirect, url_for, session,flash,jsonify,render_template_string,Response
import mysql.connector
import random
import string
import os
import serial
import time
import smtplib
from email.mime.text import MIMEText
from pyfingerprint.pyfingerprint import PyFingerprint
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import base64
from PIL import Image
import numpy as np
import io
import face_recognition
import pickle
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

MYCOM = "COM3"
# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="bank_system"
    )



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE email=%s AND password=%s", (email, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['admin'] = admin['email']
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/manage-profile', methods=['GET', 'POST'])
def manage_profile():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    admin_email = session['admin']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        new_password = request.form['password']
        # Update password in database
        cursor.execute("UPDATE admin SET password = %s WHERE email = %s", (new_password, admin_email))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Password updated successfully!", "success")
        return redirect(url_for('manage_profile'))

    # Fetch admin details
    cursor.execute("SELECT * FROM admin WHERE email = %s", (admin_email,))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('manage_profile.html', admin=admin)



'''@app.route('/admin/create-customer', methods=['GET', 'POST'])
def create_customer():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        dob = request.form['dob']
        aadhar = request.form['aadhar']
        pan = request.form['pan']
        picture = request.files['picture']

        # Generate account number
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(account_number) FROM customers")
        last_acc = cursor.fetchone()[0]
        if last_acc is None:
            account_number = 7654321
        else:
            account_number = int(last_acc) + 1

        # Create a unique filename using account number + original extension
        ext = os.path.splitext(picture.filename)[1]  # Get file extension
        unique_filename = f"{account_number}{ext}"
        picture_path = os.path.join("static/customer_pics", unique_filename)

        # Save picture to folder
        picture.save(picture_path)

       

        # Insert into DB (removed extra %s you had in your query)
        cursor.execute("""
            INSERT INTO customers 
            (full_name, email, phone, gender, dob, aadhar, pan, picture, fingerprint_id, account_number)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (full_name, email, phone, gender, dob, aadhar, pan, unique_filename, 1, account_number))

        conn.commit()
        cursor.close()
        conn.close()

        # Send email with account number
        #send_email(email, account_number)

        flash("Account created successfully!", "success")
        return redirect(url_for('create_customer'))

    return render_template('create_customer.html')'''


@app.route('/admin/create-customer', methods=['GET', 'POST'])
def create_customer():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        dob = request.form['dob']
        aadhar = request.form['aadhar']
        pan = request.form['pan']
        indep = request.form['indep']
        picture = request.files['picture']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Generate account number
        cursor.execute("SELECT MAX(account_number) FROM customers")
        last_acc = cursor.fetchone()[0]
        account_number = 7654321 if last_acc is None else int(last_acc) + 1

        # Save picture
        ext = os.path.splitext(picture.filename)[1]
        unique_filename = f"{account_number}{ext}"
        picture_path = os.path.join("static/customer_pics", unique_filename)
        picture.save(picture_path)

        # Insert into DB with fingerprint_id = NULL
        cursor.execute("""
            INSERT INTO customers 
            (full_name, email, phone, gender, dob, aadhar, pan, picture, fingerprint_id, account_number,balance)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (full_name, email, phone, gender, dob, aadhar, pan, unique_filename, 0, account_number,indep))
        conn.commit()

        cursor.close()
        conn.close()
        send_email(email,account_number)

        # Redirect to fingerprint enrollment page
        return redirect(url_for('enroll_fingerprint', acc=account_number))

    return render_template('create_customer.html')


@app.route('/admin/enroll-fingerprint/<int:acc>')
def enroll_fingerprint(acc):
    """Page where fingerprint enrollment happens"""
    #session["account_number"]=acc
    return render_template('enroll_fingerprint.html', account_number=acc)

####### for face below 2 functions and enroll_fingerprint.html

@app.route('/admin/face_register/<int:acc>')
def face_register(acc):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('face_enroll.html', account_number=acc)

ENCODINGS_PATH = "encodings.pkl"  
def load_encodings():
    # Check if the file exists
    if not os.path.exists(ENCODINGS_PATH):
        # If not, create an empty file with an empty dictionary
        with open(ENCODINGS_PATH, "wb") as f:
            pickle.dump({}, f)
        return {}
    
    # If file exists, load and return the encodings
    with open(ENCODINGS_PATH, "rb") as f:
        return pickle.load(f)

def save_encodings(enc):
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(enc, f)

@app.route('/admin/face-enroll/<int:acc>', methods=['POST'])
def face_enroll(acc):
    data = request.json
    image_data = data.get("image")
    if not image_data:
        return jsonify({"status": "error", "msg": "No image data received"}), 400

    # Decode base64 image
    img_bytes = base64.b64decode(image_data.split(',')[1])
    img = Image.open(io.BytesIO(img_bytes))
    img = np.array(img)

    # Convert to RGB if needed
    if img.shape[2] == 4:
        img = img[:, :, :3]

    # Detect face and encode
    face_locs = face_recognition.face_locations(img)
    if not face_locs:
        return jsonify({"status": "error", "msg": "No face detected"}), 200

    encs = face_recognition.face_encodings(img, known_face_locations=face_locs)
    if not encs:
        return jsonify({"status": "error", "msg": "Face not clear"}), 200

    enc_db = load_encodings()
    if str(acc) in enc_db:
        enc_db[str(acc)].append(encs[0])
    else:
        enc_db[str(acc)] = [encs[0]]

    save_encodings(enc_db)
    return jsonify({"status": "success", "msg": "Face captured and saved."})




@app.route("/verify_face", methods=["POST"])
def verify_face():
    with open(ENCODINGS_PATH, "rb") as f:
        encodings_db = pickle.load(f)
    accno=session["account_number"]
    #print(accno)
    data = request.json
    img_data = data['image'].split(",")[1]
    img_bytes = base64.b64decode(img_data)
    img = Image.open(BytesIO(img_bytes))
    img = np.array(img)

    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    if face_encodings:
        encoding = face_encodings[0]
        for name, enc_list in encodings_db.items():
            matches = face_recognition.compare_faces(enc_list, encoding, tolerance=0.5)
            if True in matches:
                print("accno",accno)
                print("name",name)
                if int(accno)==int(name):
                    print("face is matched")
                    return jsonify({"status":"matched", "name": name})
                else:
                    return jsonify({"status":"unmatched"})
                    
        return jsonify({"status":"unmatched"})
    else:
        return jsonify({"status":"no_face"})

# ---------------------
# Serve HTML page
# ---------------------

@app.route('/admin/fingerprint-stream/<int:acc>')
def fingerprint_stream(acc):
    """Server-Sent Events stream for fingerprint messages"""
    def generate():
        import time
        try:
            f = PyFingerprint(MYCOM, 57600, 0xFFFFFFFF, 0x00000000)
            if not f.verifyPassword():
                yield f"data: Fingerprint sensor password incorrect!\n\n"
                return

            yield f"data: Place finger on sensor...\n\n"
            while f.readImage() == False:
                time.sleep(0.2)

            f.convertImage(0x01)
            result = f.searchTemplate()
            if result[0] >= 0:
                yield f"data: Fingerprint already exists in DB!\n\n"
                return

            yield f"data: Remove finger...\n\n"
            time.sleep(2)

            yield f"data: Place the same finger again...\n\n"
            while f.readImage() == False:
                time.sleep(0.2)

            f.convertImage(0x02)
            if f.compareCharacteristics() == 0:
                yield f"data: Fingers do not match!\n\n"
                return

            f.createTemplate()
            positionNumber = f.storeTemplate()

            # Update DB
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE customers SET fingerprint_id=%s WHERE account_number=%s",
                        (positionNumber, acc))
            conn.commit()
            cur.close()
            conn.close()

            yield f"data: ✅ Fingerprint enrolled successfully! ID = {positionNumber}\n\n"

        except Exception as e:
            yield f"data: ❌ Error: {str(e)}\n\n"
        '''finally:
            if f is not None:
                try:
                    f.ledControl(False)
                except:
                    print("could not close")
                time.sleep(0.5)   # 🕒 give Windows time to flush & release port
                f.close()'''


    return Response(generate(), mimetype="text/event-stream")


def send_email(to_email, account_number):
    msg = MIMEText(f"Dear Customer,\n\nYour BankSecure account has been created.\nAccount Number: {account_number}\nfor login you need to use your face and fingerprint\n\nRegards,\nBankSecure")
    msg['Subject'] = "Your New BankSecure Account Details"
    msg['From'] = "jayanthg978@gmail.com"
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("jayanthg978@gmail.com", "nblgyetrcwrmbkni")
        server.sendmail(msg['From'], [msg['To']], msg.as_string())

@app.route("/view_customers", methods=["GET", "POST"])
def view_customers():
    customer = None
    if request.method == "POST":
        account_number = request.form.get("account_number")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM customers WHERE account_number = %s", (account_number,))
        customer = cursor.fetchone()

        cursor.close()
        conn.close()

    return render_template("view_customers.html", customer=customer)




#-------------------- atm simulation ----------------

def verify_fingerprint():
    """
    Waits for a finger, verifies against stored templates,
    and returns the matched position number (fingerprint_id).
    Returns None if no match.
    """
    try:
        # Adjust COM port and baudrate for your setup
        f = PyFingerprint(MYCOM, 57600, 0xFFFFFFFF, 0x00000000)

        if f.verifyPassword() == False:
            raise ValueError("Fingerprint sensor password is wrong!")

    except Exception as e:
        print("Sensor init failed:", e)
        return None

    try:
        print("Waiting for finger...")

        # Wait until finger is read
        while f.readImage() == False:
            pass

        # Convert image to characteristics and store in charbuffer 1
        f.convertImage(0x01)

        # Search template
        result = f.searchTemplate()
        positionNumber = result[0]

        if positionNumber == -1:
            print("No match found.")
            return None
        else:
            print(f"Found template at position #{positionNumber} with accuracy score {result[1]}")
            return positionNumber  # This is your fingerprint_id (mapped to customer_id)

    except Exception as e:
        print("Operation failed:", e)
        return None

@app.route("/atm_login")
def atm_login():
    return render_template("atm_fingerprint.html")

@app.route("/verify_fingerprint", methods=["POST"])
def verify_fingerprint_route():
    customer_finger_id = verify_fingerprint()
    if customer_finger_id is not None:
        # Lookup customer in DB using fingerprint_id
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE fingerprint_id=%s", (customer_finger_id,))
        customer = cursor.fetchone()
        conn.close()

        if customer:
            session["customer_id"] = customer["id"]
            session["account_number"] = customer["account_number"]
            return jsonify({"success": True, "redirect": url_for("liveliness_check")})
        else:
            return jsonify({"success": False, "message": "Fingerprint matched, but no customer found!"})
    else:
        return jsonify({"success": False, "message": "Fingerprint not recognized!"})

@app.route("/liveliness")
def liveliness_check():
    if "customer_id" not in session:
        return redirect(url_for("atm_login"))
    if "account_number" not in session:
        return redirect(url_for("atm_login"))
    return render_template("liveliness.html")

@app.route("/sendotp")
def sendotp():
    customer_id = session.get("customer_id")
    if not customer_id:
        return "Not logged in", 401
    
    # Fetch customer email
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not customer:
        return "User not found", 404

    # Generate OTP
    otp = str(random.randint(100000, 999999))
    session["otp"] = otp
    print("otp", otp)

    # Send OTP
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("jayanthg978@gmail.com", "nblgyetrcwrmbkni")
        message = f"Subject: Your OTP Code\n\nYour OTP is: {otp}"
        server.sendmail("jayanthg978@gmail.com", customer["email"], message)
        server.quit()
    except Exception as e:
        print("Error sending OTP:", e)

    # Directly render OTP page
    return render_template("otp.html")




@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()  # <-- parse JSON
    entered_otp = data.get("otp")
    session_otp = session.get("otp")
    customer_id = session.get("customer_id")

    if not customer_id:
        return jsonify({"status": "error", "msg": "Not logged in"}), 401

    if entered_otp == session_otp:
        # OTP is correct → fetch customer details
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT full_name, account_number FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        conn.close()

        if not customer:
            return jsonify({"status": "error", "msg": "User not found"}), 404

        # Clear OTP from session
        session.pop("otp", None)

        # Store customer data in session if you need it later
        session["customer_name"] = customer["full_name"]
        session["account_number"] = customer["account_number"]

        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "msg": "Invalid OTP"}), 400

@app.route("/resend-otp")
def resend_otp():
    customer_id = session.get("customer_id")
    if not customer_id:
        return {"status": "error", "message": "Not logged in"}, 401

    # Fetch customer email
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()

    if not customer:
        return {"status": "error", "message": "User not found"}, 404

    # Generate new OTP
    otp = str(random.randint(100000, 999999))
    session["otp"] = otp
    print("new otp", otp)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("jayanthg978@gmail.com", "nblgyetrcwrmbkni")
        message = f"Subject: Your OTP Code\n\nYour new OTP is: {otp}"
        server.sendmail("jayanthg978@gmail.com", customer["email"], message)
        server.quit()
        return {"status": "success"}
    except Exception as e:
        print("Error sending OTP:", e)
        return {"status": "success"}
        #return {"status": "error", "message": str(e)}, 500
        
        
@app.route("/profile")
def profile():
    if "customer_id" not in session:
        return redirect(url_for("login"))  # redirect if not logged in

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Fetch customer row using session customer_id
    cur.execute("SELECT full_name, email, phone, aadhar, picture, account_number FROM customers WHERE id=%s",
                (session["customer_id"],))
    customer = cur.fetchone()
    # Image path (match account number)
    
    img_filename = customer['picture']
    print(img_filename)
    cur.close()
    conn.close()

    if not customer:
        return "Customer not found"

    
    #img_path = os.path.join("customer_pics", img_filename)

    return render_template("profile.html", customer=customer, img_path=img_filename)

@app.route("/dashboard")
def dashboard():
    customer = {
        "name": session.get("customer_name"),
        "account_number": session.get("account_number")
    }
    if not customer["name"]:
        return redirect(url_for("atm_login"))  # if user not logged in
    return render_template("banking.html", customer=customer)


@app.route("/balance", methods=["GET"])
def balance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    customer_id = session.get("customer_id")  # store this when login happens
    if not customer_id:
        return jsonify({"error": "Not logged in"}), 401

    cursor.execute("SELECT balance FROM customers WHERE id = %s", (customer_id,))
    result = cursor.fetchone()

    if result:
        return jsonify({"balance": result["balance"]})
    else:
        return jsonify({"error": "Customer not found"}), 404


@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    amount = float(data.get("amount", 0))  # always integer withdrawal
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    customer_id = session.get("customer_id")
    if not customer_id:
        return jsonify({"success": False, "message": "Not logged in"})

    cursor.execute("SELECT balance FROM customers WHERE id=%s", (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        return jsonify({"success": False, "message": "Customer not found"})

    balance = float(customer["balance"])  # ✅ convert safely
    if amount > balance:
        return jsonify({"success": False, "message": "❌ Insufficient funds"})

    new_balance = balance - amount
    cursor.execute("UPDATE customers SET balance=%s WHERE id=%s", (new_balance, customer_id))
    cursor.execute(
        "INSERT INTO transactions (userid, transtype, amount, txdatetime) VALUES (%s, %s, %s, %s)",
        (customer_id, "debit", amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    return jsonify({
    "success": True,
    "message": f"✅ Withdrawal successful. New Balance ₹{new_balance:.2f}",
    "new_balance": f"{new_balance:.2f}"
})


@app.route("/transactions")
def transactions():
    cust_id = session["customer_id"]
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT transtype, amount, txdatetime FROM transactions WHERE userid=%s ORDER BY id DESC LIMIT 10",
                (cust_id,))
    rows = cur.fetchall()
    cur.close()
    return jsonify({"transactions": rows})


@app.route("/last_transactions")
def last_transactions():
    print("last tx")
    user_id = session.get("customer_id")  # assuming login stores this
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT amount 
        FROM transactions 
        WHERE userid = %s AND transtype = 'debit'
        ORDER BY id DESC 
        LIMIT 4
    """, (user_id,))
    
    transactions = cursor.fetchall()
    print(transactions)
    cursor.close()
    return jsonify({"transactions": transactions})


@app.route("/download_statement", methods=["POST"])
def download_statement():
    data = request.get_json()
    from_date = data.get("from")
    to_date = data.get("to")
    customer_id = session.get("customer_id")  # assuming login session has customer_id

    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        # fetch transactions in date range
        cur.execute("""
            SELECT transtype, amount, txdatetime 
            FROM transactions 
            WHERE userid = %s AND DATE(txdatetime) BETWEEN %s AND %s
            ORDER BY txdatetime DESC
        """, (customer_id, from_date, to_date))
        transactions = cur.fetchall()
        print("mini statement",transactions)

        # fetch customer email
        cur.execute("SELECT email, full_name FROM customers WHERE id=%s", (customer_id,))
        customer = cur.fetchone()

        cur.close()
        conn.close()

        if not transactions:
            return jsonify({"success": False, "error": "No transactions found in this range"})

        # generate PDF
        filename = f"mini_statement_{customer_id}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(f"Mini Statement for {customer['full_name']}", styles["Title"]))
        elements.append(Paragraph(f"Date Range: {from_date} to {to_date}", styles["Normal"]))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))

        table_data = [["Type", "Amount", "DateTime"]]
        for txn in transactions:
            table_data.append([txn["transtype"], str(txn["amount"]), txn["txdatetime"]])

        table = Table(table_data, colWidths=[100, 100, 200])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("GRID", (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(table)
        doc.build(elements)

        # send email with PDF
        sender_email = "jayanthg978@gmail.com"
        sender_pass = "nblgyetrcwrmbkni"
        receiver_email = customer["email"]

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Your Mini Statement"

        # attach PDF
        with open(filename, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={filename}")
            msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        os.remove(filename)  # cleanup

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/deposit/<int:customer_id>', methods=['POST'])
def deposit(customer_id):
    amount = request.form['amount']
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get current balance
        cursor.execute("SELECT balance FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            flash("Customer not found!", "danger")
            return redirect(url_for('view_customers'))

        new_balance = float(customer['balance']) + float(amount)

        # Update customer balance
        cursor.execute("UPDATE customers SET balance = %s WHERE id = %s",(new_balance, customer_id))

        # Insert into transactions
        tx_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO transactions (userid, transtype, amount, txdatetime) VALUES (%s, %s, %s, %s)",
            (customer_id, 'credit', amount, tx_time)
        )

        conn.commit()
        cursor.close()
        conn.close()
        flash("Deposit successful!", "success")
    except Exception as e:
        print("Error:", e)
        flash("Something went wrong. Try again!", "danger")

    return redirect(url_for('view_customers'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)