"""
    Email notification
    ~~~~~~~~~~~~~~~~~~
    
    Using threading to send email and sms notifications async_chat
    
"""

from ext.app.responseless_decorators import async
from flask import current_app as app
from jinja2 import Environment, FileSystemLoader
from ext.notifications.jinja2_filters import nl2br
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..scf import Scf, NOTIFICATION_SEND_EMAIL


class Email():

    def __init__(self):

        config = Scf()
        self.config = config.get_email()
        self.prod = config.is_production()

        self.recepients = []
        self.message = False
        self.prefix = 'F/NLF'
        self.subject = ''
        self.message_plaintext = False
        self.message_html = False

        # Init template
        self.template_dir = os.path.dirname(os.path.abspath(__file__)) + '/templates/'
        self.j2env = Environment(loader=FileSystemLoader(self.template_dir), trim_blocks=True)
        self.j2env.filters['nl2br'] = nl2br

    @async
    def send_async(self, recepient, prefix, subject, instance):

        # Now we build the message part!
        if self.message_html and self.message_plaintext:
            message = MIMEMultipart('alternative')
            # Last is considered prioritized
            message.attach(MIMEText("""%s""" % self.message_plaintext, 'plain'))
            message.attach(MIMEText("""%s""" % self.message_html, 'html'))

        elif self.message_html and not self.message_plaintext:
            message = MIMEText(self.message_html, 'html')

        elif not self.message_html and self.message_plaintext:
            message = MIMEText(self.message_plaintext, 'plain')

        elif not self.message_html and not self.message_plaintext:
            # print("No message body!")
            return False

        message.preamble = 'NLF Notification'
        message['From'] = 'NLF OBSREG <%s>' % self.config['from']

        if instance in ['dev', 'local', 'beta']:
            message['Subject'] = '[%s TEST] %s' % (prefix, subject)
        else:
            message['Subject'] = '[%s] %s' % (prefix, subject)

        message['To'] = '%s <%s>' % (recepient['full_name'], recepient['email'])

        s = smtplib.SMTP(self.config['smtp'], self.config['smtp_port'])
        s.ehlo()
        s.starttls()
        s.ehlo()

        # s.login(self.config['username'], self.config['password'])

        s.send_message(message)
        s.quit()

    def send(self, recepients, subject, prefix='OBSREG'):  # , recepients, subject, message, message_html=None, prefix=None
        """ Sends email via async after setting some values
        @todo: check length of message
        @todo: check recepients as list and length > 0
        @todo: check that list of dicts with keys name, email
        """
        if NOTIFICATION_SEND_EMAIL is True:
            for i, r in enumerate(recepients):
                self.send_async(recepient=r, prefix=prefix, subject=subject, instance=app.config.get('APP_INSTANCE'))

    def get_username(self):
        return self.config.get('username')

    def get_password(self):
        return self.config.get('password')

    def get_smtp_port(self):
        return self.config.get('smtp_port')

    def get_smtp(self):
        return self.config.get('smtp')

    def get_from(self):
        return self.config.get('from')

    def set_recepients(self, recepients):
        """Set to a list of dicts
        (name, email)
        """
        self.recepients = recepients

    def add_recepient(self, email, name=False):
        """Adds recepient dict to recepients list
        """
        if name:
            self.recepients.push({'name': name, 'email': email})
        else:
            self.recepients.push({'name': email, 'email': email})

    def add_message(self, message, type='plain'):

        if type == 'plain':
            self.message_plaintext = message

        elif type == 'html':
            self.message_html = message

    def add_message_plain(self, data, template):

        data.update({'instance': app.config.get('APP_INSTANCE')})
        template = '%s.txt' % template
        r = self.j2env.get_template(template).render(data)
        self.add_message(r, 'plain')

    def get_message_plain(self):
        return self.message_plaintext

    def add_message_html(self, data, template):

        data.update({'instance': app.config.get('APP_INSTANCE')})
        template = '%s.html' % template
        r = self.j2env.get_template(template).render(data)
        self.add_message(r, 'html')

    def get_message_html(self):
        return self.message_html

    """
    def alertsomething(self):
        # Safety! Should be to admin!
        if len(recepients) > 50:
            recepients = self.helper.get_melwin_users_email([45199])
            subject = "Too many recepients!"
            message = "Safety measure when too many recepient"
            message += "Recepients: %i" % len(recepient)
        
        send_email(recepients, subject, message)
    """


"""
mail = Email()

# recepients = get_recepients(
recepients = [{'name': 'Einar Huseby', 'email': 'einar.huseby@gmail.com', 'id': 301041}]
message = {}

action = ''
if self.action is not None:
    action = self._trigger_attrs[self.action]['descr']
else:
    action = 'Opprettet'

subject = 'Observasjon #%s %s' % (int(self.db_wf.get('id')), action)

message.update({'observation_id': self.db_wf['id']})
message.update({'action_by': get_person_name_text(app.globals['id'])})
message.update({'action': action})
message.update({'title': '%s' % ' '.join(self.db_wf.get('tags'))})
message.update({'wf_from': self._state_attrs[self.initial_state]['description']})
message.update({'wf_to': self._state_attrs[self.state]['description']})
message.update({'club': get_org_name_text(self.db_wf.get('discipline'))})
message.update({'date': datetime.today().strftime('%Y-%m-%d %H:%M')})
message.update({'url': 'ors/fallskjerm/edit/%i\n' % int(self.db_wf.get('id'))})
message.update({'url_root': request.url_root})
message.update({'comment': self.comment})
message.update({'context': context})

mail.add_message_html(message, 'ors')
mail.add_message_plain(message, 'ors')

mail.send(recepients, subject, prefix='OBSREG')
    
"""
