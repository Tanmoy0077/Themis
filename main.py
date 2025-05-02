import os
from flask import Flask, render_template, request, redirect, url_for, flash
import markdown
from graphs.contract_graph import contract_graph
from graphs.court_case_graph import court_case_graph
from dotenv import load_dotenv
from util.parser import format_clauses_to_markdown
from runner import get_court_case_analysis_data

load_dotenv()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.getenv("FLASK_KEY")

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def analyze_contract(filepath):
    data = contract_graph.invoke({"document_path": filepath})
    return {
        "summary": markdown.markdown(data["summary"], extensions=["tables", "nl2br"]),
        "clauses": markdown.markdown(
            format_clauses_to_markdown(data["clauses"]),
            extensions=["tables", "nl2br"],
        ),
        "review": markdown.markdown(data["review"], extensions=["tables", "nl2br"]),
    }


def analyze_court_case(filepath):
    data = court_case_graph.invoke({"document_path": filepath})
    sample = get_court_case_analysis_data()
    return {
        "summary_markdown": markdown.markdown(
            data["summary"], extensions=["tables", "nl2br"]
        ),
        "facts_markdown": markdown.markdown(
            data["facts"], extensions=["tables", "nl2br"]
        ),
        "similar_cases": sample["similar_cases"],
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


# Route to display the upload form
@app.route("/upload", methods=["GET"])
def upload_form():
    return render_template("upload.html")


# Route to handle the file upload and processing logic
@app.route("/file-processing", methods=["POST"])
def file_processing():
    if request.method == "POST":
        # Check if the post request has the file part
        if "file_upload" not in request.files:
            flash("No file part selected.")
            return redirect(url_for("upload_form"))

        file = request.files["file_upload"]
        document_type = request.form.get("document_type")

        if file.filename == "":
            flash("No selected file.")
            return redirect(url_for("upload_form"))

        # Check if document type was selected
        if not document_type:
            flash("Please select a document type.")
            return redirect(url_for("upload_form"))

        # Check if the file is allowed (e.g., PDF) and save it
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            try:
                file.save(filepath)
                if document_type == "contract":
                    analysis_data = analyze_contract(filepath)
                    return render_template(
                        "contract.html",
                        summary_markdown=analysis_data["summary"],
                        clauses_markdown=analysis_data["clauses"],
                        review_markdown=analysis_data["review"],
                    )

                elif document_type == "court_case":
                    analysis_data = analyze_court_case(filepath)
                    # In a real scenario, you would call a function like analyze_court_case(filepath)
                    return render_template(
                        "court.html",
                        summary_markdown=analysis_data["summary_markdown"],
                        facts_markdown=analysis_data["facts_markdown"],
                        similar_cases=analysis_data["similar_cases"],
                    )

                else:
                    # Handle unexpected document type
                    flash("Invalid document type selected.")
                    return redirect(url_for("upload_form"))

            except Exception as e:
                # Log the exception e
                print(f"Error saving or processing file: {e}")
                flash("An error occurred while processing the file.")
                return redirect(url_for("upload_form"))

        else:
            flash("Invalid file type. Only PDF files are allowed.")
            return redirect(url_for("upload_form"))

    return redirect(url_for("upload_form"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
