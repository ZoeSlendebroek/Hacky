from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/bookshelf")
def bookshelf():
    return render_template("bookshelf.html")

@app.route("/popup_poem")
def popup_poem():
    return "<p>This is a poem popup content.</p>"

@app.route("/popup_quote")
def popup_quote():
    return "<p>This is a quote popup content.</p>"

if __name__ == "__main__":
    app.run(debug=True)