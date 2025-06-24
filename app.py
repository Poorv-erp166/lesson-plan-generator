import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from lesson_core import extract_text_from_pdf, generate_lesson_plan, save_to_word

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdf_file = request.files.get("pdf_file")
        teacher_name = request.form.get("teacher_name", "")
        email = request.form.get("email", "")
        class_section = request.form.get("class_section", "")
        chapter_text = request.form.get("chapter_text", "")
        school_name = request.form.get("school_name", "SANSKRUTI- AN ENGLISH MEDIUM SCHOOL")
        session = request.form.get("session", "SESSION-2025-2026")
        plan_title = request.form.get("plan_title", "LESSON PLAN (Chapter wise)")

        extracted_text = ""
        if pdf_file and pdf_file.filename != "":
            filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            pdf_file.save(pdf_path)
            extracted_text = extract_text_from_pdf(pdf_path)
        elif chapter_text.strip():
            extracted_text = chapter_text.strip()
        else:
            return "❌ Please provide either a PDF or text input."

        lesson_plan = generate_lesson_plan(extracted_text, teacher_name, email, class_section, school_name, session, plan_title)

        if not lesson_plan:
            return "❌ Failed to generate lesson plan."

        output_path = "Sanskriti_Lesson_Plan.docx"
        save_to_word(lesson_plan, school_name, session, plan_title, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")
