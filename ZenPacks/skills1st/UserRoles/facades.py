import os
import logging
log = logging.getLogger('zen.ExampleDeviceFacade')

from zope.interface import implements

from Products.Zuul.facades import ZuulFacade
from Products.Zuul.utils import ZuulMessageFactory as _t
from ZenPacks.skills1st.UserRoles import *

from .interfaces import IupdateDevsFacade

class updateDevsFacade(ZuulFacade):
    implements(IupdateDevsFacade)


    def updateDevsFacadeFunc(self, ob):
        """ Modifies admin roles for an organizer """

        update_organizer_devices_with_adminRole(ob)
 
        return True, _t(" Admin roles updated for organizer %s" % (ob.id))

