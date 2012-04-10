#########################################################################################
#
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 November 24th, 2011
# Revised:		
#
# Script to update all devices in an organizer (Location, Group, System)
#  for the Administrative Role(s) applied to the Organizer
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

import logging
log = logging.getLogger('zen.ZenPack')

import Globals
import os.path

import types
from AccessControl import ClassSecurityInfo
from Products.ZenModel.AdministrativeRole import AdministrativeRole
from Products.ZenModel.UserSettings  import *
from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from Products.ZenWidgets import messaging

from AccessControl import Permissions
from Products.ZenModel.UserSettings import *
from Products.ZenModel.DeviceOrganizer import DeviceOrganizer
from Products.ZenModel.Location import Location
from Products.ZenModel.System import System
from Products.ZenModel.DeviceGroup import DeviceGroup
from Products.ZenModel.AdministrativeRoleable import AdministrativeRoleable
from transaction import commit


def update_organizer_devices_with_adminRole(self):
    """ self is an organizer.  
        Updates all contained devices with adminRole(s) of organizer
    """
    # adminroles() actually delivers a user or group - not actually a role

    logfile_dar=open('/usr/local/zenoss/zenoss/local/ZenPacks.skills1st.UserRoles/ZenPacks/skills1st/UserRoles/logfile_dar', 'a')
    for ar in self.adminRoles():
        id = ar.id
        role = ar.role
        level = ar.level
        logfile_dar.write('self is %s, id is %s, role is %s, level is %s. \n ' % (self.id, id, role, level))
        #logfile_dar.close()

        # need to delete the ar first or it wont re-add new devices
        self.manage_deleteAdministrativeRole(id)

        # This actually updates the user / usergroup
        self.manage_addAdministrativeRole(id)
        # This updates the role
        self.manage_editAdministrativeRoles( id, role, level)
    logfile_dar.close()
    commit()

