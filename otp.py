"""
Adapted from:
https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py
https://developers.google.com/identity/protocols/OAuth2

1. Generate and authorize an OAuth2 (generate_oauth2_token)
2. Generate a new access tokens using a refresh token(refresh_token)
3. Generate an OAuth2 string to use for login (access_token)
"""

import base64
import imaplib
import json
import urllib.parse
import urllib.request
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itertools import chain
import lxml.html
import time

IMP_SSL_HOST = 'imap.gmail.com'  # imap.mail.yahoo.com
IMP_SSL_PORT = 993

GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

with open('oauthcredentials.txt') as credentials:
    credentials = list(credentials.readlines())
    GOOGLE_CLIENT_ID = credentials[0].split('=')[-1].strip(' ').replace('\n', '')
    GOOGLE_CLIENT_SECRET = credentials[1].split('=')[-1].strip(' ').replace('\n', '')
    GOOGLE_REFRESH_TOKEN = credentials[2].split('=')[-1].strip(' ').replace('\n', '')

if GOOGLE_REFRESH_TOKEN in ['', ' ', '\n']:
    GOOGLE_REFRESH_TOKEN = None

def command_to_url(command):
    return '%s/%s' % (GOOGLE_ACCOUNTS_BASE_URL, command)


def url_escape(text):
    return urllib.parse.quote(text, safe='~-._')


def url_unescape(text):
    return urllib.parse.unquote(text)


def url_format_params(params):
    param_fragments = []
    for param in sorted(params.items(), key=lambda x: x[0]):
        param_fragments.append('%s=%s' % (param[0], url_escape(param[1])))
    return '&'.join(param_fragments)


def generate_permission_url(client_id, scope='https://mail.google.com/'):
    params = {}
    params['client_id'] = client_id
    params['redirect_uri'] = REDIRECT_URI
    params['scope'] = scope
    params['response_type'] = 'code'
    return '%s?%s' % (command_to_url('o/oauth2/auth'), url_format_params(params))


def call_authorize_tokens(client_id, client_secret, authorization_code):
    params = {}
    params['client_id'] = client_id
    params['client_secret'] = client_secret
    params['code'] = authorization_code
    params['redirect_uri'] = REDIRECT_URI
    params['grant_type'] = 'authorization_code'
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def call_refresh_token(client_id, client_secret, refresh_token):
    params = {}
    params['client_id'] = client_id
    params['client_secret'] = client_secret
    params['refresh_token'] = refresh_token
    params['grant_type'] = 'refresh_token'
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def generate_oauth2_string(username, access_token, as_base64=False):
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if as_base64:
        auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    return auth_string


def test_imap(user, auth_string):
    imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_conn.debug = 4
    imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
    imap_conn.select('INBOX')



def get_authorization(google_client_id, google_client_secret):
    scope = "https://mail.google.com/"
    print('Navigate to the following URL to auth:', generate_permission_url(google_client_id, scope))
    authorization_code = input('Enter verification code: ')
    response = call_authorize_tokens(google_client_id, google_client_secret, authorization_code)
    return response['refresh_token'], response['access_token'], response['expires_in']


def refresh_authorization(google_client_id, google_client_secret, refresh_token):
    response = call_refresh_token(google_client_id, google_client_secret, refresh_token)
    return response['access_token'], response['expires_in']

def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()

def get_otp(fromaddr):
    if GOOGLE_REFRESH_TOKEN is None:
        print('No refresh token found, obtaining one')
        refresh_token, access_token, expires_in = get_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
        print('Set the following as your GOOGLE_REFRESH_TOKEN in oauthcredentials.txt:', refresh_token)
        exit()
    access_token, expires_in = refresh_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)
    auth_string = generate_oauth2_string(fromaddr, access_token)

    server = imaplib.IMAP4_SSL(IMP_SSL_HOST, IMP_SSL_PORT)
    server.authenticate('XOAUTH2', lambda x: auth_string)
    server.select('INBOX')
    msg = None
    
    while True:
        try:
            result, data = server.fetch('1', '(RFC822)')  # fetch entire message
            msg = email.message_from_bytes(data[0][1])
            break
        except:
            time.sleep(1)
            server.recent()
            #print('Waiting on the email forward')
            continue
    #print(data)
    
    

    text = get_first_text_block(msg)
    words = list(x.decode('utf-8') for x in base64.b64decode(text).split())
    OTP = words[words.index('is')+1][:-1]
    typ, data = server.search(None, 'ALL')
    for num in data[0].split():
        server.store(num, '+FLAGS', '\\Deleted')
    server.expunge()
    server.logout()
    return OTP
