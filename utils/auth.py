'''
Fonctions relatives à l'authentification LDAP
'''

from functools import wraps

import ldap3
from ldap3.core.exceptions import LDAPUnknownAuthenticationMethodError
from flask import redirect, url_for, g, abort

import config

from flask import request

class AuthUser:
    '''
    Classe représentant un utilisateur avec son nom et les groupes auxquels il appartient
    '''
    def __init__(self, data=None):
        try:
            self.name = data['name']
            self.groups = data['groups']
            self.is_valid = True
        except TypeError:
            self.name = None
            self.groups = []
            self.is_valid = False

    def has_group(self, group):
        return group in self.groups

    @property
    def is_admin(self):
        return any([x in self.groups for x in config.ADMIN_GROUPS])

    def as_dict(self):
        return {
                'name': self.name,
                'groups': self.groups,
                'is_valid': self.is_valid
                }


class InvalidAuthError(Exception):
    '''
    Exception levée en cas d'erreur d'authentification
    '''
    pass


def ldap_connect(login, passwd):
    '''
    fonction de connexion au LDAP pour vérification des logins utilisateurs
    '''
    ldap_srv = ldap3.Server(
            config.LDAP_HOST,
            get_info=ldap3.ALL)

    ldap_cnx = ldap3.Connection(
            ldap_srv,
            user= config.LDAP_PREFIX % login,
            password=passwd,
            authentication=ldap3.NTLM)

    if ldap_cnx.bind():
        return ldap_cnx

    raise InvalidAuthError


def get_user_groups(user_data):
    '''
    Retourne la liste des groupes de l'utilisateur.
    '''
    user_groups = []
    if 'memberOf' in str(user_data):
        for grp in user_data['memberOf']:
            user_groups.append(
                [gr[1] for gr in ldap3.utils.dn.parse_dn(grp)][0]
            )
    return user_groups


def get_members(groups):
    '''
    Retourne la liste des membres d'un groupe
    '''
    ldap_cnx = ldap_connect(
        config.LDAP_USER,
        config.LDAP_PASS)
    ldap_cnx.search(
        'ou=Personnel,dc=pnc,dc=int',
        '(sn=*)',
        attributes=['cn', 'mail', 'memberOf'])
    for entry in ldap_cnx.entries:
        user_groups = get_user_groups(entry)
        for grp in groups:
            if grp in user_groups:
                yield entry
                break


def get_members_mails(groups):
    '''
    Retourne l'adresse email des membres d'un groupe
    '''
    yield from [str(member.mail) for member in get_members(groups)]


def check_ldap_auth(login, passwd):
    '''
    Vérifie les informations d'authentification et renvoie un objet AuthUser
    '''
    try:
        ldap_cnx = ldap_connect(login, passwd)
    except LDAPUnknownAuthenticationMethodError as err:
        raise InvalidAuthError
    ldap_cnx.search(
            config.LDAP_BASE_PATH,
            '(sAMAccountName=%s)' % login,
            attributes=['cn', 'memberOf'])
    user_data = ldap_cnx.entries[0]
    user_name = str(user_data.cn)
    user_groups = []
    if 'memberOf' in str(user_data):
        for grp in user_data['memberOf']:
            user_groups.append(
                    [gr[1] for gr in ldap3.utils.dn.parse_dn(grp)][0])
    user = AuthUser({
            'name': user_name,
            'groups': user_groups
            })

    return user


def require_valid_user(view):
    '''
    Décorateur pour les vues qui nécéssitent l'authentification préalable de l'utilisateur.
    '''
    @wraps(view)
    def _require_valid_user(*args, **kwargs):
        if not g.user.is_valid:
            return redirect(url_for('main.login_view', url=request.url))
        return view(*args, **kwargs)
    return _require_valid_user


def require_admin_user(view):
    '''
    Décorateur pour les vues qui nécéssitent un administrateur.
    '''
    @wraps(view)
    def _require_admin_user(*args, **kwargs):
        if not g.user.is_admin:
            return abort(403)
        return view(*args, **kwargs)
    return _require_admin_user