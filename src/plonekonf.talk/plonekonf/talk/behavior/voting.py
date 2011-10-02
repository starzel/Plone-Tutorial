# encoding=utf-8
from collections import defaultdict
from hashlib import md5
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations

# Der key sollte eindeutig sein, der Klassenname mit komplettem Modulpfad
# ist ein guter Ansatz, kann aber Verwirrung stiften, denn, er MUSS dem nicht
# entsprechen, und wenn man den code mal verschiebt, sollte man den Key deswegen
# nicht ändern, sonst kommt man nicht mehr an seine Altdaten ran.
KEY = "plonekonf.talk.behavior.voting.Vote"

class Vote(object):
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if KEY not in annotations.keys():
            # Was passiert, wenn man kein PersistentDict oder List verwendet?
            annotations[KEY] = PersistentDict({
                "version": 1,
                "voted": PersistentList(),
                })
        self.annotations = annotations[KEY]
        if not self.annotations.has_key('version') or self.annotations['version'] == 1:
            self.annotations['version'] = 2
            self.annotations['votes'] = PersistentDict()

    def _hash(self, request):
        """
        This hash can be tricked out by changing IP Adresses and might allow
        only a single person of a big company to vote
        """
        hash = md5()
        hash.update(request.getClientAddr())
        for key in ["User-Agent", "Accept-Language",
                    "Accept-Encoding", "Accept-Charset"]:
            hash.update(request.getHeader(key))
        return hash.hexdigest()

    def vote(self, vote, request):
        vote = int(vote)
        if self.already_voted(request):
            # Exceptions erzeugen hässliche Fehlermeldungen, diese sollte man
            # nur dann nicht abfangen, wenn ein Nutzer normalerweise keine
            # Chance hat, ihn zu sehen. Und Transaktionen?
            raise KeyError("You may not vote twice")
        self.annotations['voted'].append(self._hash(request))
        votes = self.annotations['votes']
        if vote not in votes:
            votes[vote] = 1
        else:
            votes[vote] += 1

    def average_vote(self):
        total_votes = sum(self.annotations['votes'].values())
        if total_votes == 0:
            return 0
        total_points = sum([vote * count for (vote, count) in
                            self.annotations['votes'].items()])
        return float(total_points) / total_votes

    def has_votes(self):
        return len(self.annotations['votes']) != 0

    def already_voted(self, request):
        return self._hash(request) in self.annotations['voted']

    def clear(self): 
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentDict({'voted': PersistentList()})
        self.annotations = annotations[KEY]
