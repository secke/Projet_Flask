# ############### IMPORTATION DES MODULES ET FONCTIONS #####################
from flask import Flask, redirect, url_for,render_template,request,flash


#############################################################################

############## APPLICATION FLASK ET SES FONCTIONS DE NAVIGATION ###################

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

############ PAGE DE CONNEXION ###################################################
@app.route('/login', methods=('GET','POST'))
def connexion():
    if request.method=='POST':
        mail=request.form['connect']
        motPass=request.form['secur']
        if not mail:
            flash('Ce champ est requis!')
        else:
            redirect(url_for('user'))
    return render_template('connexion.html')

############## DEBOGUER #############################################################
if __name__=='__main__':
    app.run(debug=True) 

