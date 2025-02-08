import pyodbc
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# إعدادات الاتصال بقاعدة البيانات
server = 'DESKTOP-M13HNO9\\MSSQLSERVER01'
database = 'GP'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# المسار الأساسي لتخزين الصور
base_image_path = "E:/GP/Images"

# الاتصال بقاعدة البيانات
def connect_to_db():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error:
        return None

# # API لإنشاء مستخدم جديد
# @app.route('/users', methods=['POST'])
# def create_user():
#     data = request.json
#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')

#     if not name or not email or not password:
#         return jsonify({"error": "Please fill all fields."}), 400

#     if not email.endswith('@gmail.com'):
#         return jsonify({"error": "Email must end with @gmail.com."}), 400

#     if len(password) < 8:
#         return jsonify({"error": "Password must be at least 8 characters long."}), 400

#     conn = connect_to_db()
#     if conn is None:
#         return jsonify({"error": "Error connecting to database."}), 500

#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO [User] (name, email, password) VALUES (?, ?, ?)",
#             (name, email, password)
#         )
#         conn.commit()
#         return jsonify({"message": "User created successfully!"}), 201
#     except pyodbc.IntegrityError:
#         return jsonify({"error": "Email already exists."}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         conn.close()

# API للحصول على جميع المستخدمين
@app.route('/users', methods=['GET'])
def get_users():
    conn = connect_to_db()
    if conn is None:
        return jsonify({"error": "Error connecting to database."}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, email FROM [User]")
        users = cursor.fetchall()

        user_list = [{"user_id": user[0], "name": user[1], "email": user[2]} for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# # API للحصول على مستخدم معين
# @app.route('/users/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     conn = connect_to_db()
#     if conn is None:
#         return jsonify({"error": "Error connecting to database."}), 500

#     try:
#         cursor = conn.cursor()
#         cursor.execute("SELECT user_id, name, email FROM [User] WHERE user_id = ?", (user_id,))
#         user = cursor.fetchone()

#         if user:
#             return jsonify({"user_id": user[0], "name": user[1], "email": user[2]}), 200
#         else:
#             return jsonify({"error": "User not found."}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         conn.close()

# # API لتحديث معلومات مستخدم معين
# @app.route('/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     data = request.json
#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')

#     conn = connect_to_db()
#     if conn is None:
#         return jsonify({"error": "Error connecting to database."}), 500

#     try:
#         cursor = conn.cursor()

#         # التحقق من وجود المستخدم
#         cursor.execute("SELECT user_id FROM [User] WHERE user_id = ?", (user_id,))
#         user = cursor.fetchone()

#         if not user:
#             return jsonify({"error": "User not found."}), 404

#         # تحديث بيانات المستخدم
#         cursor.execute(
#             "UPDATE [User] SET name = ?, email = ?, password = ? WHERE user_id = ?",
#             (name, email, password, user_id)
#         )
#         conn.commit()
#         return jsonify({"message": "User updated successfully!"}), 200
#     except pyodbc.IntegrityError:
#         return jsonify({"error": "Email already exists."}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         conn.close()

# # API لحذف مستخدم معين
# @app.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     conn = connect_to_db()
#     if conn is None:
#         return jsonify({"error": "Error connecting to database."}), 500

#     try:
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM [User] WHERE user_id = ?", (user_id,))
        
#         if cursor.rowcount == 0:
#             return jsonify({"error": "User not found."}), 404

#         conn.commit()
#         return jsonify({"message": "User deleted successfully!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         conn.close()

# API لتسجيل مستخدم جديد (Registration)
import bcrypt

# API لتسجيل مستخدم جديد (Registration)
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Please fill all fields."}), 400

    if not email.endswith('@gmail.com'):
        return jsonify({"error": "Email must end with @gmail.com."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long."}), 400

    # Hashing the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = connect_to_db()
    if conn is None:
        return jsonify({"error": "Error connecting to database."}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO [User] (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except pyodbc.IntegrityError:
        return jsonify({"error": "Email already exists."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()




# API لتسجيل الدخول (Login)
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Please fill all fields."}), 400

    conn = connect_to_db()
    if conn is None:
        return jsonify({"error": "Error connecting to database."}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, password FROM [User] WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            stored_password_hash = user[2]

            # Verify the password by comparing the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                return jsonify({"message": "Login successful!", "user_id": user[0], "name": user[1]}), 200
            else:
                return jsonify({"error": "Invalid email or password."}), 401
        else:
            return jsonify({"error": "Invalid email or password."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# API لتحميل الصورة
@app.route('/upload-image', methods=['POST'])
def save_image():
    data = request.json
    description = data.get('description')
    user_id = data.get('user_id')
    image_path = data.get('image_path')

    if not description or not user_id or not image_path:
        return jsonify({"error": "Please fill all fields and provide an image path/URL."}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "User ID must be a valid number."}), 400

    conn = connect_to_db()
    if conn is None:
        return jsonify({"error": "Error connecting to database."}), 500

    try:
        cursor = conn.cursor()

        # التحقق من وجود المستخدم
        cursor.execute("SELECT user_id FROM [User] WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found."}), 404

        # إنشاء مجلد المستخدم إذا لم يكن موجودًا
        user_folder = os.path.join(base_image_path, f"user_{user_id}")
        os.makedirs(user_folder, exist_ok=True)

        # حساب عدد الصور للمستخدم
        cursor.execute("SELECT COUNT(*) FROM Images WHERE user_id = ?", (user_id,))
        image_count = cursor.fetchone()[0] + 1

        # إنشاء اسم ملف جديد للصورة
        image_filename = f"{user_id}.{image_count}.jpg"
        new_image_path = os.path.join(user_folder, image_filename)

        # تنزيل الصورة إذا كان الرابط من الإنترنت
        if image_path.startswith("http://") or image_path.startswith("https://"):
            response = requests.get(image_path, stream=True)
            response.raise_for_status()
            with open(new_image_path, "wb") as image_file:
                for chunk in response.iter_content(1024):
                    image_file.write(chunk)
        else:
            # نقل الصورة إذا كان المسار محليًا
            os.rename(image_path, new_image_path)

        # إدخال معلومات الصورة في جدول Images
        cursor.execute(
            "INSERT INTO Images (image_path, description, user_id) VALUES (?, ?, ?)",
            (new_image_path, description, user_id)
        )
        conn.commit()

        return jsonify({"message": "Image saved successfully!"}), 201

    except Exception as e:
        return jsonify({"error": f"Error saving image: {e}"}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)