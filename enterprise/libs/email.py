'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: email.py
# Project: core.wecare.id
# File Created: Wednesday, 20th February 2019 3:30:08 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 20th February 2019 3:30:08 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love
# Copyright - 2018 Wecare.Id, wecare.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import json
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings


def send_mail(subject_template_name, email_template_name, html_email_template_name,
              context, to_email, from_email=None, mandrill_template=None, mandrill_variables=None,
              cc=[]):
    """
    Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    if not from_email:
        from_email = getattr(settings, 'FROM_EMAIL')

    subject = loader.render_to_string(subject_template_name, context)

    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    headers = {}

    if mandrill_template:
        headers["X-MC-Template"] = mandrill_template

    if mandrill_variables:
        headers["X-MC-MergeVars"] = json.dumps(mandrill_variables)

    email_message = EmailMultiAlternatives(
        subject, body, from_email, [to_email], headers=headers, cc=cc)

    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    try:
        email_message.send()
    except Exception as e:
        if settings.DEBUG:
            print (str(e))
        else:
            raise e