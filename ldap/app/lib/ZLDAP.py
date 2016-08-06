import ldap


class ZLDAP:
    def __init__(self, app):
        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None


    # Set default configure value for ldap
    def init_app(self, app ):
        app.config.setdefault('LDAP_HOST', '127.0.0.1')
        app.config.setdefault('LDAP_PORT', 389)
        app.config.setdefault('LDAP_VER', 3)
        app.config.setdefault('LDAP_BASE_DN', None)
        app.config.setdefault('LDAP_ROOT_DN', None)
        app.config.setdefault('LDAP_ROOT_PASSWORD', None)

    # Connect LDAP server use root user
    def connectRootDN(self):
        host = self.app.config['LDAP_HOST']
        port = self.app.config['LDAP_PORT']
        root_dn = self.app.config['LDAP_ROOT_DN']
        root_password = self.app.config['LDAP_ROOT_PASSWORD']

        try:
            self.conn = ldap.initialize('ldap://' + host + ":" + port)
            ver = self.app.config['LDAP_VER']
            if ver == 1:
                self.conn.protocol_version = ldap.VERSION1
            elif ver == 2:
                self.conn.protocol_version = ldap.VERSION2
            else:
                self.conn.protocol_version = ldap.VERSION3

            self.conn.simple_bind_s(root_dn, root_password)
        except ldap.LDAPError, e:
            raise Exception(e)


    # Check user exist by uid
    # return 1 if exist. 0 none exist
    def checKExistByUID(self, uid):
        base_dn = self.app.config['LDAP_BASE_DN']
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        searchFilter = "(uid=" + uid + ")"
        try:
            ldap_result_id = self.conn.search_s(base_dn, searchScope, searchFilter, retrieveAttributes)
        except ldap.LDAPError, e:
            raise Exception(e)
        if len(ldap_result_id) == 0:
            return 0
        else:
            return 1

    # Set pasword for user
    # return 1 is sucess, 0 none unsuccess
    def setPasswordByUID(self, user, password):
        base_dn = self.app.config['LDAP_BASE_DN']
        user_dn = "uid=" + user + "," + base_dn
        try:
            self.conn.passwd_s(user_dn, None, password)
        except ldap.LDAPError, e:
            # raise Exception()
            return 0
        return 1


    # Change pasword for user
    # Return 1 if change password success else return 0.
    def changePasswordByUID(self, uid , oldPassword, newPassword):
        base_dn = self.app.config['LDAP_BASE_DN']
        user_dn = "uid=" + uid + "," + base_dn
        #user_dn = "uid=kaonhan,ou=People,dc=zamba,dc=vn"
        try:
            self.conn.passwd_s(user_dn,oldPassword, newPassword)
        except Exception, e:
            # raise Exception(e)
            return 0
        return 1

    # Get email user by uid
    # Return email if user is exist else return 0
    def getEmailByUID(self, user):
        base_dn = self.app.config['LDAP_BASE_DN']
        filter = "(uid=" + user + ")"
        results = self.conn.search_s(base_dn, ldap.SCOPE_SUBTREE, filter)
        if len(results) <= 0:
            return
        else:
            return results[0][1]['mail'][0]

    def close(self):
        self.conn.unbind()