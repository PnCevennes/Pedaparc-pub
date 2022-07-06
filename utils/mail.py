"""
Envoi de mails
"""
import threading

from flask_mail import Message

import config
from server import mail


def _send_async(msg):
    # TODO utiliser backends authentif pour gérer les envois mails

    from utils.auth import get_members_mails
    from server import app
    with app.app_context():
        for mail_addr in get_members_mails(config.ADMIN_GROUPS):
            msg.add_recipient(mail_addr)
        mail.send(msg)


def send_mail(
        subject, msg_body,
        add_dests=None, sendername='Pedaparc'):
    '''
    envoie un mail aux administrateurs de l'application
    '''
    if add_dests is None:
        add_dests = []

    # supprimer chaines vides dans listes email
    add_dests = list(filter(lambda x: len(x), add_dests))

    if not config.SEND_MAIL:
        return

    dests = add_dests

    msg = Message(
        '[%s] %s' % (sendername, subject),
        sender=config.MAIL_SENDER,
        recipients=dests)
    msg.html = msg_body

    thr = threading.Thread(target=_send_async, args=[msg])
    thr.start()

