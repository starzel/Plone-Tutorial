# encoding=utf-8
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from plonekonf.talk.interfaces import IVoting

class TalkDefaultView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')

class TalkListView(grok.View):
    grok.context(Interface)
    grok.require("zope2.View")

    @property
    def talks(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        talks = portal_catalog(portal_type="talk",
                               path="/".join(self.context.getPhysicalPath()))
        for brain in talks:
            # Achtung, wir wecken Objekte auf, das kann teuer sein.
            talk = brain.getObject()
            voting = IVoting(talk)
            yield {
                # Was passiert bei brain.title?
                # talk.title
                'title': brain.Title,
                # talk.absolute_url()
                'absolute_url': brain.getURL(),
                'average_rating': voting.average_vote(),
                'audience': talk.audience,
                'uuid': brain.UID,
                }
