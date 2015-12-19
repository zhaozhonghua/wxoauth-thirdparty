# -*- coding: utf-8 -*-
"""
字符串 util
"""
import re
import time
import xml.etree.ElementTree as ET
from hashlib import sha1
from BeautifulSoup import BeautifulSoup, Comment

def sanitize(value, allowed_tags):
    """Argument should be in form 'tag2:attr1:attr2 tag2:attr1 tag3', where tags
    are allowed HTML tags, and attrs are the allowed attributes for that tag.
    """
    js_regex = re.compile(r'[\s]*(&#x.{1,7})?'.join(list('javascript')))
    allowed_tags = [tag.split(':') for tag in allowed_tags.split()]
    allowed_tags = dict((tag[0], tag[1:]) for tag in allowed_tags)

    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    for tag in soup.findAll(True):
        if tag.name not in allowed_tags:
            tag.hidden = True
        else:
            tag.attrs = [(attr, js_regex.sub('', val)) for attr, val in tag.attrs
                         if attr in allowed_tags[tag.name]]

    return soup.renderContents().decode('utf8')

def parse_msg(rawmsgstr):
    """
    xml转dict
    :param rawmsgstr:
    :return:
    """
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def gen_timetoken(openid):
    """
    生成timetoken
    :param openid:
    :return:
    """
    now = str(time.strftime('%Y%m%d%H',time.localtime(time.time())))
    minite = str(time.localtime(time.time()).tm_min/10)
    timetoken = ''.join([openid, now, minite])
    return sha1(timetoken).hexdigest()

def verification(signature, timestamp, nonce, token):
    """
    验证
    :return:
    """
    tmplist = [token.token, timestamp, nonce] if token else []
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = sha1(tmpstr).hexdigest()

    if hashstr == signature:
        return True

    return False

if __name__=="__main__":
    print sanitize("<script>alter(111)</script>", '')

