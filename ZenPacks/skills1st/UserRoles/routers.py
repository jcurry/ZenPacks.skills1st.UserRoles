from Products.ZenUtils.Ext import DirectRouter, DirectResponse
from Products import Zuul
import Globals
import logging
log = logging.getLogger('zen.ZenPack')

import os
zenhome = os.environ['ZENHOME']
logfileBaseName = zenhome + '/log'

class updateDevsRouter(DirectRouter):

    def _getFacade(self):

        # The parameter in the next line - updateDevsAdapter - must match with 
        #   the name field in an adapter stanza in configure.zcml

        return Zuul.getFacade('updateDevsAdapter', self.context)

    # The method name - myRouterFunc - and its parameters - must match with 
    #   the last part of the call for Zenoss.remote.updateDevsRouter.updateDevsFunc
    #   in the javascript file update_organizer_devices.js .

    def updateDevsFunc(self):
        logfile_rou=open(logfileBaseName+'/logfile_rou', 'a')
        logfile_rou.write('In updateDevsFunc \n')
        facade = self._getFacade()

        # The object that is being operated on is in self.context

        ob = self.context
        logfile_rou.write('In updateDevsFunc - ob is %s \n' % (ob))

        # The facade name in the next line & its parameters must match with a method defined
        #   in facades.py (ie. updateDevsFacadeFunc(ob) )

        success, message = facade.updateDevsFacadeFunc(ob)

        if success:
            return DirectResponse.succeed(message)
        else:
            return DirectResponse.fail(message)

        logfile_rou.close()

