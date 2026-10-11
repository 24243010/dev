from flask import Flask, render_template, request, redirect

app = Flask(__name__)
notes = []

@app.route("/")
def home():
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    title = request.form.get("title")
    content = request.form.get("content")
    if title and content:
        notes.append({"title": title, "content": content})
    return redirect("/")

@app.route("/delete/<int:index>")
def delete_note(index):
    if 0 <= index < len(notes):
        notes.pop(index)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
