from flask import Flask, render_template, request, send_file
import os
from lesson_core import extract_text_from_pdf, generate_lesson_plan, save_to_word

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'pdf' not in request.files:
        return "❌ No file uploaded."

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return "❌ No selected file."

    file_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(file_path)

    teacher_name = request.form['teacher_name']
    email = request.form['email']
    class_section = request.form['class_section']

    text = extract_text_from_pdf(file_path)
    lesson_plan = generate_lesson_plan(text, teacher_name, email, class_section)

    output_path = "Sanskriti_Lesson_Plan.docx"
    save_to_word(lesson_plan, output_path)

    return render_template("result.html", content=lesson_plan)

@app.route('/download')
def download():
    return send_file("Sanskriti_Lesson_Plan.docx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
