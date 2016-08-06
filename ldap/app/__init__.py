from flask import Flask, render_template, request, jsonify
from flask import json
from app.lib.ZLDAP import ZLDAP
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_pyfile('config.py')

ld = ZLDAP(app)
db = SQLAlchemy(app)

from app.modules.Staff import Staff



@app.route("/")
def index():
    #ld.connectRootDN()
    #return str(ld.checKExistByUID("toa"))
    title = app.config['TOOL_TITLE']
    return render_template("index.html", title=title)

@app.route("/change", methods=['POST'])
def changePassword():
    if request.method == "POST":
        dataDic = json.loads(request.data)
        username = dataDic['username']
        password = dataDic['password']
        newpassword = dataDic['newpassword']
        if  dataDic != "" and username != "" and password != "" and newpassword != "" and len(newpassword) >= 8:
            st = Staff()
            re, msg = st.changePassword(username, password, newpassword)
            if re == True:
                return jsonify(re='success',msg=msg)
            else:
                return jsonify(re='error', msg=msg)
    return jsonify(re='error', msg="Data is invalid")



@app.route("/reset", methods=['POST'])
def resetPassword():
    if request.method == "POST":
        dataDic = json.loads(request.data)
        username = dataDic['username']
        if username != "":
            st = Staff()
            re, msg = st.resetPassword(username)
            if re == True:
                return jsonify(re="success", msg=msg)
            else:
                return jsonify(re="error", msg=msg)
    return jsonify(re='error', msg="Data is invalid")


@app.route("/dochangepassword", methods=['GET'])
def doChangePassword():
    if request.method == "GET":
        user = request.args.get("user")
        token = request.args.get("token")
        st = Staff()
        re, msg = st.doResetPassword(user, token)
        if re == True:
            return render_template("success.html", title=msg)
        else:
            return render_template("success.html", title=msg)

    else:
        return render_template("success.html", title="Method request is invalid")

