import sleekxmpp
from sleekxmpp import ClientXMPP, JID
import os
import time
import logging
import config as app_config
import json
import requests
from queries import MessageSource

log = logging.getLogger(__name__)

class Config: pass


def fix_p_tags(html_body):
    # sleekxmpp likes to wrap html_body in p tags, but that will mess up our
    # formatting
    if html_body.startswith('<p>') and \
       html_body.endswith('</p>'):
        return html_body[3:-4]
    return html_body

def push_message(config, room, sender, html_body, priority):
    data = {
        'source': config.source_id,
        'group': str(room),
        'sender': str(sender),
        'body': html_body,
        'format': 'html',
        'priority': priority,
        }
    url = config.base_url + '/messages'
    response = requests.post(url, data=json.dumps(data))

def get_config(message_source):
    json = message_source.config
    log.debug(json)
    config = Config()
    config.source_id = message_source.id
    config.base_url = 'http://'+app_config.BASE_URL
    config.username = json['username']
    config.password = json['password']
    config.nickname = json['nickname']
    config.chats = list(json['chats'])
    config.muc_domain = json['muc_domain']
    config.targets = list(json['targets'])
    return config

def join_rooms_on_connect_handler(bot, muc, muc_domain, rooms_to_join, nick):
    def join_rooms_on_connect(event):
        log.info('getting roster')
        bot.get_roster()
        log.info('sending presence')
        bot.send_presence(ppriority=0)
        log.info('joining rooms ..')
        for room in rooms_to_join:
            full_room = room + '@' + muc_domain 
            log.info(' .. joining ' + full_room)
            muc.joinMUC(full_room, nick, wait=True)
    return join_rooms_on_connect

def on_message_handler(config):
    def on_message(message_stanza):
        if message_stanza['type'] == 'error':
            log.error(message_stanza)

        if not message_stanza['body']:
            log.error('apparently empty message: '+str(message_stanza))

        if message_stanza['subject']:
            log.debug('ignoring room subject')
            return

        body = message_stanza['body']
        user = message_stanza['mucnick'] or message_stanza['from']

        log.debug('got message {} from {}'.format(body, user))

        priority = 'message'
        if any(body.lower().startswith(target) for target in config.targets):
            priority = 'ping'
        elif any(target in body.lower() for target in config.targets):
            priority = 'mention'

        html_body = message_stanza['html']['body'] or body
        html_body = fix_p_tags(html_body)
        room = JID(message_stanza['mucroom']).user
        sender = user

        push_message(config, room, sender, html_body, priority)
    return on_message
        

def xmpp_connect(config):
    bot = ClientXMPP(config.username, config.password)
    bot.register_plugin('xep_0045')
    muc = bot.plugin['xep_0045']
    bot.register_plugin('xep_0199')
    ping = bot.plugin['xep_0199']
    ping.enable_keepalive(30, 30)

    bot.add_event_handler('session_start',
            join_rooms_on_connect_handler(bot, muc, config.muc_domain,
                config.chats, config.nickname))
    bot.add_event_handler('message', on_message_handler(config))

    if not bot.connect():
        raise 'could not connect'

    # gevent should mean that we fall out of this method
    bot.process(block=True)

    return bot


def run(source):
    config = get_config(source)
    bot = xmpp_connect(config)
    return bot


