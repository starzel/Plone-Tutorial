# encoding=utf-8
from five import grok

from plonekonf.talk.interfaces import IVotable, IVoting

# Wir verwenden hier den CodeView. Der normaler grok.View bietet noch ein
# paar Helferlein, die wir aber nicht nutzen. So kann man den CodeView
# aber auch als Indikator für Views nutzen die nicht für Endnutzer gedacht sind

class Vote(grok.CodeView):
    grok.context(IVotable)
    grok.require("zope2.View")

    # Dieser View hat eine Render Methode, das bedeutet, es wird kein
    # Template genutzt
    def render(self, rating):
        voting = IVoting(self.context)
        voting.vote(rating, self.request)
        return "success"

class ClearVotes(grok.CodeView):
    grok.context(IVotable)
    grok.require("zope2.ViewManagementScreens")

    def render(self):
        voting = IVoting(self.context)
        voting.clear()
        return "success"
