# -*- coding: utf-8 -*-
## Turn simple string to html format.

def html(script): return '<html><head/><body>{}</body></html>'.format(script)

def title(name, *others): return '<h2>{}</h2>'.format(name)+('<h3>{}</h3>'.format('</h3><h3>'.join(others)) if others else '')

def content(text): return '<p>{}</p>'.format(text.replace('\n', '</p><p>'))

def orderList(*List): return '<ol><li>{}</li></ol>'.format('</li><li>'.join(List))

## Turn simple string to help text.

def help(*script):
    head = '==Help message=='
    return head+'\n'+'\n\n'.join(script)+'\n'+'='*len(head)

def argumentType(*types): return '\n\n'.join(['Arguments:', '* {}'.format('\n* '.join(types))])

def argumentList(*Args):
    maxArg = max(*[len(e) for e in Args])
    buff = [(e if len(e)==maxArg else e[:-1]+['\t']*(maxArg-len(e))+e[-1:]) for e in Args]
    return '\n'.join(['\t'.join(e) for e in buff])

def present(*part): return "Power by"+' '.join(part)+'.'
