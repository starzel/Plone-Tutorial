# encoding=utf-8
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

class TalkDefaultView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
