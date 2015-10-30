#!/usr/bin/python

import urllib2
import sys
import json
import re
import HTMLParser
#import pprint

if len(sys.argv) <= 1:
    text = 'apple'
else:
    text=sys.argv[1]

print "Try '%s' for google auto-fill." % text

text = text.replace(' ','%20')

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)
class ConcatJSONDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            objs.append(obj)
        return objs

def get_google_answer(text):
    url = 'http://www.google.com/s?output=search&sclient=psy-ab&q=%s' % text
    req = urllib2.Request(url=url)
    #req.add_header( 'Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3' )
    req.add_header( 'Accept-Language', 'en-US;q=0.5,en;q=0.3' )
    response = urllib2.urlopen(req)
    answer = response.read()
    return answer

got     = get_google_answer( text )
handled = json.loads(got, cls=ConcatJSONDecoder)
final   = handled[0][1]

h = HTMLParser.HTMLParser()
for answer in final:
    str =  (answer[0].replace('<b>','')).replace('</b>','')
    print "\t", h.unescape(str) 




