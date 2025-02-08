import os
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# المسار المؤقت لتخزين الصور
UPLOAD_FOLDER = 'E:/GP/test'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# التأكد من وجود المجلد
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# تحميل نموذج التعلم الآلي الخاص بك
import tensorflow as tf
model = tf.keras.models.load_model('E:/GP/Enhanced_Model.h5')  # تعديل المسار إلى الموقع الصحيح

# API للتنبؤ باستخدام الصورة
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    # حفظ الصورة في المسار المؤقت
    image_file = request.files['image']
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)

    try:
        # فتح الصورة وتحويلها إلى مصفوفة numpy
        img = Image.open(image_path).convert('RGB')
        img = img.resize((32, 32))  # تغيير حجم الصورة إلى (32, 32)
        img_array = np.array(img)  # تحويل الصورة إلى مصفوفة numpy
        img_array = np.expand_dims(img_array, axis=0)  # إضافة بعد جديد لتصبح المصفوفة (1, 32, 32, 3)

        # إجراء التنبؤ باستخدام النموذج
        prediction = model.predict(img_array)

        # معالجة نتائج التنبؤ
        predicted_class = np.argmax(prediction[0])  # استخراج الفئة المتوقعة
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    finally:
        # حذف الصورة بعد التنبؤ
        if os.path.exists(image_path):
            os.remove(image_path)

    # إرجاع النتيجة في صيغة JSON
    return jsonify({"prediction": float(predicted_class)})

# مسار للاختبار
@app.route('/')
def home():
    return "Flask App is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)