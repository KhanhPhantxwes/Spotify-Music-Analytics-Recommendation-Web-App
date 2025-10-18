from website import create_App, db


app = create_App()
with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
