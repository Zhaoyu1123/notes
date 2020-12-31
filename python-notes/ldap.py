# -*- coding: utf-8 -*-
import ldap
import os
from ldap import modlist

from flask import Flask, request
import flask_restful


app = Flask(__name__)
api = flask_restful.Api(app)
ldap_admin = ""
ldap_pwd = ""
ldap_server = ""


class LDAPClient:
    def __init__(self,server,admin_user,admin_pwd):
        self.server = server
        self.admin_user = admin_user
        self.admin_pwd = admin_pwd

    def connection(self):
        conn = ldap.initialize(self.server)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.protocol_version = ldap.VERSION3
        conn.simple_bind_s(self.admin_user, self.admin_pwd)
        self.conn = conn

    def search(self,searchDN,searchFilter):
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        ldap_result_id = self.conn.search(searchDN, searchScope, searchFilter, retrieveAttributes)
        while 1:
            result_type, result_data = self.conn.result(ldap_result_id, 0)
            if result_type == ldap.RES_SEARCH_ENTRY:
                self.conn.unbind_s()
                return result_data[0][0]
            else:
                self.conn.unbind_s()
                return ''

    def searchByUID(self,searchDN,uid):
        searchFilter = "uid="+uid
        return self.search(searchDN,searchFilter)

    def validate(self,searchDN,username,password):
        target_CN = self.searchByUID(searchDN,username)
        if self.conn.simple_bind_s(target_CN, password):
            self.conn.unbind_s()
            return True
        else:
            return False

    def updatePasswd(self,uid,oldpass,newpass,department):
        target_CN = self.searchByUID("dc=100credit,dc=com", uid)
        if self.validate("ou=%sdc=100credit,dc=com"%department, uid, oldpass):
            self.conn.passwd_s(target_CN,oldpass,newpass)
            self.conn.unbind_s()
            print 'update passwd'
            return True
        else :
            return False

    def setPassWord(self, username, password, department):
        self.conn.protocal_version = ldap.VERSION3
        try:
            self.conn.modify_s("cn=%s,ou=%s,dc=100credit,dc=com" % (username, department), [(ldap.MOD_REPLACE, 'userPassword', [str(password)])])
            self.conn.unbind_s()
            print 'set passwd'
            return True
        except ldap.NO_SUCH_OBJECT:
            return self.addUser(username, password)

    def addUser(self, username, password, department):
        try:
            dn="cn=%s,ou=%s,dc=100credit,dc=com" % (username, department)
            attrs = {}
            attrs['objectclass'] = ['top','account','posixAccount']
            attrs['cn'] = [str(username)]
            attrs['uid'] = [str(username)]
            attrs['uidNumber'] = ['10000']
            attrs['gidNumber'] = ['10000']
            attrs['homeDirectory'] = [str(username)]
            attrs['userPassword'] = [str(password)]
            ldif = modlist.addModlist(attrs)
            self.conn.add_s(dn,ldif)
            self.conn.unbind_s()
            print 'add user'
            return True
        except ldap.ALREADY_EXISTS:
            self.conn.unbind_s()
            print 'user exist'
            return False

    def delUser(self, username, department):
        deleteDN = "cn=%s,ou=%s,dc=100credit,dc=com" % (username, department)
        self.conn.delete_s(deleteDN)
        return True



class LdapValidate(flask_restful.Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            client = LDAPClient(ldap_server,ldap_admin,ldap_pwd)
            client.connection()
            if client.validate("dc=100credit,dc=com", username, password):
                return {'code': 0, 'msg': 'success'}
            else:
                return {'code': 1, 'msg': 'ERROR Incorrect username or password'}
        else:
            return {'code': 2, 'msg': 'User name or password is empty'}


class UpdatePasswd(flask_restful.Resource):
    def post(self):
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        department = request.form.get('department')
        if username and password1 and password2:
            client = LDAPClient(ldap_server,ldap_admin,ldap_pwd)
            client.connection()
            if client.updatePasswd(username, password1, password2, department):
                return {'code': 0, 'msg': 'success'}
            else:
                return {'code': 1, 'msg': 'ERROR Incorrect username or password'}
        else:
            return {'code': 2, 'msg': 'User name or password is empty'}


class SetPasswd(flask_restful.Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        department = request.form.get('department')
        if username and password:
            client = LDAPClient(ldap_server,ldap_admin,ldap_pwd)
            client.connection()
            client.setPassWord(username,password,department)
            return {'code': 0, 'msg': 'success'}
        else:
            return {'code': 1, 'msg': 'User name or password is empty'}


class AddUser(flask_restful.Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        department = request.form.get('department')
        if username:
            client = LDAPClient(ldap_server,ldap_admin,ldap_pwd)
            client.connection()
            if client.addUser(username, password, department):
                return {'code': 0, 'msg': 'success'}
            else:
                return {'code': 1, 'msg': 'user is already exist'}
        else:
            return {'code': 1, 'msg': 'username is empty'}


class DelUser(flask_restful.Resource):
    def post(self):
        username = request.form.get('username')
        department = request.form.get('department')
        if username and department:
            client = LDAPClient(ldap_server,ldap_admin,ldap_pwd)
            client.connection()
            if client.delUser(username, department):
                return {'code': 0, 'msg': 'success'}
            else:
                return {'code': 1, 'msg': 'user is already exist'}
        else:
            return {'code': 1, 'msg': 'username is empty'}


api.add_resource(LdapValidate, '/validate')
api.add_resource(UpdatePasswd, '/mpasswd')
api.add_resource(SetPasswd, '/spasswd')
api.add_resource(AddUser, '/adduser')
api.add_resource(DelUser, '/deluser')


if __name__ == '__main__':
    # client = LDAPClient(ldap_server,ldap_admin,ldap_pwd)
    # client.connection()
    # print client.addUser('wang', 'wang')
    app.run(debug=True, host='0.0.0.0')
