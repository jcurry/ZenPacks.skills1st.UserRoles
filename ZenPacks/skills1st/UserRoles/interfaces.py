from Products.ZenUI3.navigation.interfaces import IZenossNav
from Products.Zuul.interfaces import IFacade


class IUserRoleSkin(IZenossNav):
    """
    Marker interface for User Role nav layer
    """

# The name of the IFacade class here ( IupdateDevsFacade ) must match what is defined in an
#   adapter stanza's provides=".interfaces. this_is_the_bit_that_must_match"
#   ie. IupdateDevsFacade in configure.zcml
# The method name and parameters must match those defined for the facade that implements
#   IupdateDevsFacade in facades.py (ie. updateDevsFacadeFunc )

class IupdateDevsFacade(IFacade):
    def updateDevsFacadeFunc(self, ob):
        """ Modify admin roles for an organizer object"""



