import time
from flask_mail import Mail, Message
from flask import request
import uuid
from app import ld, db, app




class Staff(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    email = db.Column(db.String(120))
    tooken = db.Column(db.String(120))
    dateCreate = db.Column(db.Integer())
    dateExpire = db.Column(db.Integer())
    status = db.Column(db.Boolean, unique=False, default=True)



    def __init__(self, username=None, email=None, token=None, dateCreat=None, dateExpire=None):
        self.username = username
        self.email = email
        self.tooken = token
        self.dateCreate = dateCreat
        self.dateExpire = dateExpire

    # parameters username, old password, new password
    # return 1 if changing password success
    # return 0 if changing password unsucess
    def changePassword(self, uid, oldPassword, newPassword):
        ld.connectRootDN()
        ret = ld.changePasswordByUID(uid, oldPassword, newPassword)
        if ret == 0:
            return False, "Password is wrong"
        else:
            mail = Mail(app)
            uid_email = [ld.getEmailByUID(uid)]
            ld.close()
            subj = "Notification change password for user: " + uid
            content = "You have just changed vpn passsword for account " + uid
            try:
                msg = Message(subj, recipients=uid_email)
                msg.body = content
                mail.send(msg)
            except Exception, e:
                print "Have error" + str(e)
            return True, "Password changed successfully"

    def resetPassword(self, uid):
        ld.connectRootDN()
        if uid != "":
            isExist = ld.checKExistByUID(uid)
            if isExist == 0:
                return False, "User is not exist"
            else:
                mail = Mail(app)
                uid_email = [ld.getEmailByUID(uid)]
                ld.close()
                subj = "Confirm reset password for user " + uid
                token = uuid.uuid4().hex
                link = "http://" + request.headers['Host'] + "/dochangepassword?user=" + uid + "&token=" + token
                content = "You have just sent a request for chaging password in our system. Please press below link to comfirm <br />" + \
                    "<a href='" + link + "'> Click here </a>"
                try:
                    msg = Message(subj, recipients=uid_email)
                    msg.html = content
                    mail.send(msg)
                except Exception, e:
                    print "Have error"
                dateCreate = int(time.time())
                dateExpire = dateCreate + 10*60 # expire sau 10 phut
                usr=Staff(uid, uid_email[0], token, dateCreate, dateExpire)
                db.session.add(usr)
                db.session.commit()
                return True, "Checking your email to confirm reset password request"
        else:
            return False, "Parameter is invalid"


    def doResetPassword(self, uid, token):
        ld.connectRootDN()
        if uid != "" and token != "":
            u = Staff.query.filter_by(username=uid).order_by("id desc").first()
            if u is not None:
                curTime = int(time.time())
                newPassword = uuid.uuid4().hex
                if u.dateCreate < curTime < u.dateExpire and u.status == True:
                    if ld.setPasswordByUID(uid, newPassword) == 1:
                        mail = Mail(app)
                        uid_email = [ld.getEmailByUID(uid)]
                        ld.close()
                        subj = "New password for user " + uid
                        content = "<h3> New password for user " + uid + " is: " + newPassword + "</h3>"
                        try:
                            msg = Message(subj, recipients=uid_email)
                            msg.html = content
                            mail.send(msg)
                        except Exception, e:
                            print "Have error"
                    u.status = False
                    db.session.commit()
                    return True, "Password reseted sucessfully"
                else:
                    return False, "Wrong token or Limit time expired"
            return False, "User is not valid"
        return False, "Data invalid"


