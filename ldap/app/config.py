import os
basedir = os.path.abspath(os.path.dirname(__file__))

TOOL_TITLE="Welcome to my company"

# configure for sqlite
SQLALCHEMY_DATABASE_URI='sqlite:////tmp/clgt.db'

#configure for LDAP
LDAP_HOST='172.16.2.3'
LDAP_PORT='389'
LDAP_VER=3
LDAP_BASE_DN='ou=People,dc=company,dc=vn'
LDAP_ROOT_DN='cn=Manager,dc=company,dc=vn'
LDAP_ROOT_PASSWORD='passWord'

#Configure for email
MAIL_SERVER="mailserver.com"
MAIL_PORT=587
MAIL_USERNAME="system"
MAIL_PASSWORD="MhxOIROxVu9UBBrmIQN"
MAIL_DEFAULT_SENDER="sysadmin@company.com"
MAIL_USE_TLS=False
MAIL_USE_SSL=False
# extends
NOTIFY_EMAIL=0
MANGER_EMAIL='sysadmin@company.com'
