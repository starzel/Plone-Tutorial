# encoding=utf-8
from zope.interface import Interface

# IVotable ist das Marker Interface für Contenttypen die zufällig das Behavior
# unterstützen. Siehe auch behavior/configure.zcml
class IVotable(Interface):
    pass

# IVoting wird als Adapter verwendet. Wenn man IVoting(objekt) aufruft
# bekommt man das Behavior zurück.
class IVoting(Interface):
    def vote(request):
        """
        Store the vote information, store the request hash to ensure
        that the user does not vote twice
        """
        
    def average_vote():
        """
        Return the average voting for an item
        """

    def has_votes():
        """
        Return whether anybody ever voted for this item
        """
        
    def already_voted(request):
        """
        Return the information wether a person already voted.
        This is not very high level and can be tricked out easily
        """

    def clear():
        """
        Clear the votes. Should only be called by admins
        """
