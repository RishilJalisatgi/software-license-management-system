from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import mysql, init_db

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize DB
init_db(app)

# -------------------------------
# ROUTES
# -------------------------------

@app.route('/')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            COUNT(*) AS total_licenses,
            SUM(license_status='active') AS active_licenses,
            SUM(license_status='expired') AS expired_licenses
        FROM LICENSE
    """)
    stats = cur.fetchone()

    cur.execute("""
        SELECT vendor_name, COUNT(*) AS license_count 
        FROM LICENSE 
        JOIN VENDOR ON LICENSE.vendor_id = VENDOR.vendor_id
        GROUP BY vendor_name
    """)
    vendor_data = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', stats=stats, vendor_data=vendor_data)


@app.route('/licenses')
def licenses():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT l.*, v.vendor_name 
        FROM LICENSE l 
        LEFT JOIN VENDOR v ON l.vendor_id = v.vendor_id
    """)
    data = cur.fetchall()
    cur.close()
    return render_template('licenses.html', data=data)


@app.route('/add_license', methods=['GET', 'POST'])
def add_license():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        license_key = request.form['license_key']
        license_name = request.form['license_name']
        purchase_date = request.form['purchase_date']
        quantity = request.form['quantity']
        vendor_id = request.form['vendor_id']

        cur.execute("""
            INSERT INTO LICENSE (license_key, license_name, purchase_date, license_quantity, vendor_id, license_status)
            VALUES (%s, %s, %s, %s, %s, 'pending')
        """, (license_key, license_name, purchase_date, quantity, vendor_id))
        mysql.connection.commit()
        flash('✅ License added successfully!', 'success')
        return redirect(url_for('licenses'))

    cur.execute("SELECT * FROM VENDOR")
    vendors = cur.fetchall()
    cur.close()
    return render_template('add_license.html', vendors=vendors)

@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    if request.method == 'POST':
        vendor_name = request.form['vendor_name']
        vendor_type = request.form['vendor_type']
        contact_email = request.form['contact_email']
        website_url = request.form['website_url']
        is_active = 'is_active' in request.form
        
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO VENDOR (vendor_name, vendor_type, contact_email, website_url, is_active)
            VALUES (%s, %s, %s, %s, %s)
        """, (vendor_name, vendor_type, contact_email, website_url, is_active))
        mysql.connection.commit()
        cur.close()
        
        flash('✅ Vendor added successfully!', 'success')
        return redirect(url_for('vendors'))
    
    return render_template('add_vendor.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        is_active = 'is_active' in request.form
        
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO USER (username, email, first_name, last_name, is_active)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, email, first_name, last_name, is_active))
        mysql.connection.commit()
        cur.close()
        
        flash('✅ User added successfully!', 'success')
        return redirect(url_for('users'))
    
    return render_template('add_user.html')


@app.route('/vendors')
def vendors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM VENDOR")
    data = cur.fetchall()
    cur.close()
    return render_template('vendors.html', data=data)


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM USER")
    data = cur.fetchall()
    cur.close()
    return render_template('users.html', data=data)


# License renewal route (calls stored procedure)
@app.route('/renew/<int:license_id>')
def renew_license(license_id):
    cur = mysql.connection.cursor()
    try:
        cur.callproc('renew_license', [license_id])
        for result in cur.stored_results():
            flash(result.fetchall()[0]['message'], 'success')
        mysql.connection.commit()
    except Exception as e:
        flash(str(e), 'danger')
    finally:
        cur.close()
    return redirect(url_for('licenses'))


if __name__ == '__main__':
    app.run(debug=True)
