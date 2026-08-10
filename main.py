import streamlit as st
import mysql.connector
import pandas as pd

# =========================================================
#  Database Connection Setup
# =========================================================
def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='', #pass
        database='software_license'
    )

st.set_page_config(page_title="Software License Management", layout="wide")
st.title("🗂️ Software License Management System")

# =========================================================
#  Database Connection
# =========================================================
db = get_db()
cursor = db.cursor(dictionary=True)

# =========================================================
#  USER OPERATIONS
# =========================================================
st.header("👤 User Operations")

# ---------- Create User ----------
with st.form("Create User"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    is_active = st.selectbox("Is Active?", [True, False])
    submitted = st.form_submit_button("Create User")
    if submitted:
        try:
            cursor.execute(
                "INSERT INTO USER (username, email, first_name, last_name, is_active) VALUES (%s, %s, %s, %s, %s)",
                (username, email, first_name, last_name, is_active)
            )
            db.commit()
            st.success("✅ User created successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ---------- View Users ----------
cursor.execute("SELECT * FROM USER")
df_users = pd.DataFrame(cursor.fetchall())
st.dataframe(df_users if not df_users.empty else pd.DataFrame(columns=["No Users Found"]))

# ---------- Update User ----------
st.subheader("✏️ Update a User")
if not df_users.empty:
    user_ids = df_users["user_id"].tolist()
    selected_user = st.selectbox("Select User ID", user_ids, key="update_user")
    new_email = st.text_input("New Email")
    new_status = st.selectbox("New Status", [True, False], key="update_user_status")
    if st.button("Update Selected User"):
        try:
            cursor.execute("UPDATE USER SET email=%s, is_active=%s WHERE user_id=%s",
                           (new_email, new_status, selected_user))
            db.commit()
            st.success(f"✅ User {selected_user} updated successfully!")
            st.rerun()
        except Exception as e:
            st.error(str(e))

# ---------- Delete User ----------
st.subheader("🗑️ Delete a User")
if not df_users.empty:
    del_user_id = st.selectbox("Select User ID to Delete", df_users["user_id"].tolist())
    if st.button("Delete Selected User"):
        try:
            cursor.execute("DELETE FROM USER WHERE user_id=%s", (del_user_id,))
            db.commit()
            st.success(f"User {del_user_id} deleted successfully!")
            st.rerun()
        except Exception as e:
            st.error(str(e))

# =========================================================
#  VENDOR CRUD
# =========================================================
st.header("🏷️ Vendor Operations")

with st.expander("➕ Add Vendor"):
    with st.form("Create Vendor"):
        vendor_name = st.text_input("Vendor Name")
        vendor_type = st.text_input("Vendor Type")
        contact_email = st.text_input("Contact Email")
        website_url = st.text_input("Website URL")
        is_active_vendor = st.selectbox("Is Active?", [True, False])
        submit_vendor = st.form_submit_button("Add Vendor")
        if submit_vendor:
            try:
                cursor.execute("""
                    INSERT INTO VENDOR (vendor_name, vendor_type, contact_email, website_url, is_active)
                    VALUES (%s, %s, %s, %s, %s)
                """, (vendor_name, vendor_type, contact_email, website_url, is_active_vendor))
                db.commit()
                st.success("✅ Vendor added successfully!")
                st.rerun()
            except Exception as e:
                st.error(str(e))

cursor.execute("SELECT * FROM VENDOR")
df_vendors = pd.DataFrame(cursor.fetchall())
st.dataframe(df_vendors if not df_vendors.empty else pd.DataFrame(columns=["No Vendors Found"]))

# ---------- Update Vendor ----------
st.subheader("✏️ Update a Vendor")
if not df_vendors.empty:
    v_id = st.selectbox("Select Vendor ID", df_vendors["vendor_id"].tolist())
    new_email = st.text_input("New Contact Email")
    new_status = st.selectbox("Active?", [True, False], key="update_vendor_status")
    if st.button("Update Vendor"):
        try:
            cursor.execute("UPDATE VENDOR SET contact_email=%s, is_active=%s WHERE vendor_id=%s",
                           (new_email, new_status, v_id))
            db.commit()
            st.success("✅ Vendor updated successfully!")
            st.rerun()
        except Exception as e:
            st.error(str(e))

# ---------- Delete Vendor ----------
st.subheader("🗑️ Delete a Vendor")
if not df_vendors.empty:
    del_vendor = st.selectbox("Select Vendor ID to Delete", df_vendors["vendor_id"].tolist())
    if st.button("Delete Vendor"):
        try:
            cursor.execute("DELETE FROM VENDOR WHERE vendor_id=%s", (del_vendor,))
            db.commit()
            st.success("Vendor deleted successfully!")
            st.rerun()
        except Exception as e:
            st.error(str(e))

# =========================================================
#  LICENSE MANAGEMENT (Trigger Demo)
# =========================================================
st.header("🔑 License Management")

with st.form("Create License"):
    license_key = st.text_input("License Key")
    license_name = st.text_input("License Name")
    purchase_date = st.date_input("Purchase Date")
    license_quantity = st.number_input("License Quantity", min_value=1, value=1)
    auto_renewal = st.selectbox("Auto Renewal?", [True, False])
    vendor_id_license = st.number_input("Vendor ID", min_value=1)
    submit_license = st.form_submit_button("Add License")

    if submit_license:
        try:
            cursor.execute("""
                INSERT INTO LICENSE (license_key, license_name, purchase_date, license_quantity, auto_renewal, vendor_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (license_key, license_name, purchase_date, license_quantity, auto_renewal, vendor_id_license))
            db.commit()

            cursor.execute("""
                SELECT license_id, license_key, license_name, purchase_date, license_status
                FROM LICENSE ORDER BY license_id DESC LIMIT 1
            """)
            st.dataframe(pd.DataFrame(cursor.fetchall()))
            st.success("✅ Trigger executed: license_status auto-updated!")
            st.rerun()
        except Exception as e:
            st.error(str(e))

cursor.execute("SELECT * FROM LICENSE")
df_license = pd.DataFrame(cursor.fetchall())
st.dataframe(df_license if not df_license.empty else pd.DataFrame(columns=["No Licenses Found"]))

# ---------- Update License ----------
st.subheader("✏️ Update License Status")
if not df_license.empty:
    lic_id = st.selectbox("Select License ID", df_license["license_id"].tolist())
    new_status = st.selectbox("New Status", ["active", "expired"])
    if st.button("Update License Status"):
        try:
            cursor.execute("UPDATE LICENSE SET license_status=%s WHERE license_id=%s", (new_status, lic_id))
            db.commit()
            st.success("✅ License status updated successfully!")
            st.rerun()
        except Exception as e:
            st.error(str(e))

# ---------- Delete License ----------
st.subheader("🗑️ Delete a License")
if not df_license.empty:
    del_lic = st.selectbox("Select License ID to Delete", df_license["license_id"].tolist())
    if st.button("Delete License"):
        try:
            cursor.execute("DELETE FROM LICENSE WHERE license_id=%s", (del_lic,))
            db.commit()
            st.success("License deleted successfully!")
            st.rerun()
        except Exception as e:
            st.error(str(e))

# =========================================================
#  PROCEDURES, TRIGGERS, FUNCTIONS
# =========================================================
st.header("⚙️ Stored Procedures / Functions")

st.subheader("🧩 Add Software Product via Stored Procedure")
p_name = st.text_input("Product Name")
p_version = st.text_input("Version")
p_category = st.text_input("Category")
p_type = st.text_input("Type")
p_end_date = st.date_input("End of Life Date")
vendor_id = st.number_input("Vendor ID for Product", min_value=1)
license_id = st.number_input("License ID for Product", min_value=1)
run_proc = st.button("Run Procedure")

if run_proc:
    try:
        cursor.callproc("add_software_product", [
            p_name, p_version, p_category, p_type, p_end_date, vendor_id, license_id
        ])
        db.commit()
        for result in cursor.stored_results():
            st.dataframe(pd.DataFrame(result.fetchall()))
        st.success("✅ Stored Procedure executed successfully!")
    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err.msg}")
    except Exception as e:
        st.error(f"Python Error: {e}")

st.subheader("🕒 Get License Days Left (Function)")
lic_id_days = st.number_input("License ID", min_value=1, key="days_left_input")
if st.button("Calculate Days Left"):
    cursor.execute("SELECT get_license_days_left(%s) AS days_left", (lic_id_days,))
    result = cursor.fetchone()
    st.write("Days left:", result["days_left"] if result else "N/A")

# =========================================================
#  SPECIAL QUERIES
# =========================================================
st.header("🔎 Special Queries")

if st.button("Show Nested Query (Products with Active Licenses)"):
    cursor.execute("""
        SELECT product_name, product_version, product_category, product_type
        FROM SOFTWARE_PRODUCT
        WHERE license_id IN (SELECT license_id FROM LICENSE WHERE license_status='active')
    """)
    st.dataframe(pd.DataFrame(cursor.fetchall()))

if st.button("Show Join Query (User's Products)"):
    cursor.execute("""
        SELECT U.username, S.product_name 
        FROM USER U
        JOIN USER_BUYS_PRODUCT B ON U.user_id=B.user_id
        JOIN SOFTWARE_PRODUCT S ON B.product_id=S.product_id
    """)
    st.dataframe(pd.DataFrame(cursor.fetchall()))

if st.button("Show Aggregate Query (License Usage)"):
    cursor.execute("""
        SELECT L.license_name, COUNT(M.user_id) AS managed_by_count
        FROM LICENSE L
        LEFT JOIN USER_MANAGES_LICENSE M ON L.license_id=M.license_id
        GROUP BY L.license_id
    """)
    st.dataframe(pd.DataFrame(cursor.fetchall()))

# =========================================================
#  CLOSE CONNECTION
# =========================================================
db.close()
