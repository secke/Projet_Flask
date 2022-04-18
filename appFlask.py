from flask import Flask, url_for,render_template, redirect
# from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test_123@localhost/flask_project'

@app.route('/')
def principal():
    return render_template('principal.html')

@app.route('/adduser')
def adduser():
    return render_template('adduser.html')

if __name__=='__main__':
    app.run(debug=True)

