#########################################################################################
#
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 June 24th, 2011
# Revised:		June 28th, 2011		Added ZEN_COMMON role
#
# ZenPack to overcome issues with Administered Objects code in Core
#
# It create a new role, ZenOperator on install which has the same
#  permissions as the standard ZenUser but also has "Manage Events" permission.
#  This means users with ZenOperator role can Close / Ack events that they
#  have access to.
#  The role is deleted again when the ZenPack is removed.
#
# A second role,ZEN_COMMON is also created / removed.  This role ONLY has 
#  the ZEN_COMMON premission.
#
# Administered Objects configurations for Organizers (device classes, locations,
#  systems and groups) are not propagated to the contained devices, in the standard code.
#  This is logged as a bug in ticket 7848.
#
#  This ZenPack monkey patches (overrides) the methods in 
#   $ZENHOME/Products/ZenModel/AdministrativeRoleable.py so that propagation of
#  extra roles to contained devices DOES take place.
#
#  NOTE that you should modify the Role applied to an Administered Object
#   from the Organizers DETAILS -> Administration menu.  If you do it from
#   the User or group menu, you will need to modify the role for ALL devices,
#   not just Organizers (the panel will implement exactly what you see on that panel).
#
#  NOTE that code in this ZenPack could provide a separate Role menu, in addition
#   to the standard Administrators / Administered Objects menus.  In the future,
#   we may want different menus and actions for roles.  Currently the Roles
#   menu stuff is commented out.
#
# There is a bug currently, documented as ticket 7837, whereby deleting a user
#  group that has Administered Objects configured, does NOT properly delete
#  the Administered Object relationship and leaves your Zope Database in a 
#  nasty inconsistent state.  The manage_deleteGroups method at the end of
#  this ZenPack monkey patches the code in UserSettings so that group
#  deletion also clears up the relationships with Administerd Objects.
#
#  There are various logging hooks around the code - all are currently
#   commented out.
#
# This ZenPack has been tested with a user that has NO global role.  They are
#   added to a group which has Administered Objects configured with the
#   ZenOperator role.  The result is that the user ONLY sees those devices and
#   Organizers for which Administered Objects are configured.  The user can Ack
#   and Close events from those devices.  By default, you get to see the usual
#   View stuff for such devices but you will NOT see any graphs (for the
#   device or its components).  Graphs are deliverd by the RenderServer in
#   $ZENHOME/Products/ZenRRD/RenderServer.py.  Although the user's role is
#   augmented by the Administered Object, this is only for a device and the 
#   RenderService is not of class Device- hence no role applies (and View is
#   required).  To fix this, modify the RenderServer.py code to comment out
#   the 5 occurrences of security.declareProtected . zenhub and zopectl will
#   need to be recycled.
#   NOTE that this last kludge will not be upgrade-proof.

#   This is now done by self.allowAuthenticatedRender(app.zport.RenderServer)
#        in this file
#

# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

import logging
log = logging.getLogger('zen.ZenPack')

import Globals
import os.path

import os
zenhome = os.environ['ZENHOME']
logfileBaseName = zenhome + '/log'

import types
from AccessControl import ClassSecurityInfo
from Products.ZenModel.AdministrativeRole import AdministrativeRole
from Products.ZenModel.UserSettings  import *
from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from Products.ZenWidgets import messaging
from Products.ZenModel.ZenPack import ZenPackBase

from AccessControl import Permissions
from Products.ZenModel.UserSettings import *
from Products.ZenModel.DeviceOrganizer import DeviceOrganizer
from Products.ZenModel.Location import Location
from Products.ZenModel.System import System
from Products.ZenWidgets.ZenossPortlets import ZenossPortlets


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

#
# Need to change permissions on the GoogleMapsPortlet to ZEN_COMMON
# Next few lines sets up the new permissions list
# updatePortletPermissions method (see later) then registers those permissions
# This affects what you see in Advanced -> Portlets GUI
#
new_portlets = []
for portlet in ZenossPortlets.portlets:
    if portlet['id'] == 'GoogleMapsPortlet':
        portlet['permission'] = ZEN_COMMON
    new_portlets.append(portlet)
ZenossPortlets.portlets = new_portlets

ZEN_OP_ROLE = 'ZenOperator'
ZEN_COMMON_ROLE = 'ZenCommon'

class ZenPack(ZenPackBase):

    def install( self, app):
        super(ZenPack, self).install(app)
    #
    # Fix security tag limitation on RenderServer - default permission is VIEW
    #  this changes it to any Authenticated user
    #
        self.allowAuthenticatedRender(app.zport.RenderServer)
        self.allowAuthenticatedReport(app.zport.ReportServer)

    # Fix portlet permissions so that GoogleMapsPortlet has ZEN_Common
    #  permission, not ZEN_VIEW
    #
        self.updatePortletPermissions(app.zport.ZenPortletManager)
    #
    # On ZenPack install, create a new role called ZenOperator with ZenUser roles plus 'Manage Events'
    #
        self.addZenOperatorRole(app.zport)
    #
    # Add ZenCommon role
    #
        self.addZenCommonRole(app.zport)

# No upgrade needed - upgrade for ZenPacks now deprecated
# Since Zenoss 2.5, upgrade calls remove with leaveObjects = True, then calls install

#    def upgrade( self, app):
#        ZenPackBase.upgrade( self, app )

    def remove( self, app, leaveObjects=False):
    #
    # On ZenPack remove, delete role ZenOperator 
    #
        self.removeZenOperatorRole(app.zport)
    #
    # Remove ZenCommon role
    #
        self.removeZenCommonRole(app.zport)

        ZenPackBase.remove( self, app, leaveObjects=False )

    def allowAuthenticatedRender(self, renderServer):
        log.info('Allowing authenticated access to RenderServer')
        renderServer.manage_permission(ZEN_VIEW, ['Authenticated'], 0)

    def allowAuthenticatedReport(self, reportServer):
        log.info('Allowing authenticated access to reportServer')
        reportServer.manage_permission(ZEN_VIEW, ['Authenticated'], 0)

    def updatePortletPermissions(self, portletManager):
        log.info("Changing permission on GoogleMapsPortlet ")
        for portlet in ZenossPortlets.portlets:
            portletManager.register_portlet(**portlet)

    def addZenOperatorRole(self, zport):

        log.info('Adding ZenOperator role')

        #logfile_i=open(logfileBaseName+'/logfile_i', 'a')
	dmd = self.dmd
        #logfile_i.write(' In install code. zport is %s  \n ' % (zport))
	# This adds ZenOperator to the roles in http://<your zenoss>:8080/zport/manage_access
        if not ZEN_OP_ROLE in zport.__ac_roles__:
            zport.__ac_roles__ += (ZEN_OP_ROLE,)

	# Next few lines adds the ZenOperator role to the roleManager
        rms = (dmd.getPhysicalRoot().acl_users.roleManager,
                    zport.acl_users.roleManager)
        for rm in rms:
            if not ZEN_OP_ROLE in rm.listRoleIds():
                rm.addRole(ZEN_OP_ROLE)

        # Following are standard roles same as for ZenUser
        self.addPermissions(zport, ZEN_VIEW,
            [ZEN_OP_ROLE,], 0)
        self.addPermissions(zport, ZEN_VIEW_HISTORY,
            [ZEN_OP_ROLE,], 1)
        self.addPermissions(zport, ZEN_ZPROPERTIES_VIEW,
            [ZEN_OP_ROLE,], 1)
        self.addPermissions(zport, ZEN_RUN_COMMANDS,
            [ZEN_OP_ROLE,], 1)
        self.addPermissions(zport, ZEN_DEFINE_COMMANDS_VIEW,
            [ZEN_OP_ROLE,], 1)
        self.addPermissions(zport, ZEN_MAINTENANCE_WINDOW_VIEW,
            [ZEN_OP_ROLE,], 1)
        self.addPermissions(zport, ZEN_ADMINISTRATORS_VIEW,
            [ZEN_OP_ROLE,], 1)
        self.addPermissions(zport, ZEN_COMMON,
            [ZEN_OP_ROLE,], 1)
    # ZEN_MANAGE_EVENTS permission is extra to allow Ack / Close of events
        self.addPermissions(zport, ZEN_MANAGE_EVENTS,
            [ZEN_OP_ROLE,], 1)

        #logfile_i.close()

    def addZenCommonRole(self, zport):

        log.info('Adding ZenCommon role')

        #logfile_i=open(logfileBaseName+'/logfile_i', 'a')
	dmd = self.dmd
        #logfile_i.write(' In install code. zport is %s  \n ' % (zport))
	# This adds ZenCommon to the roles in http://<your zenoss>:8080/zport/manage_access
        if not ZEN_COMMON_ROLE in zport.__ac_roles__:
            zport.__ac_roles__ += (ZEN_COMMON_ROLE,)

	# Next few lines adds the ZenCommon role to the roleManager
        rms = (dmd.getPhysicalRoot().acl_users.roleManager,
                    zport.acl_users.roleManager)
        for rm in rms:
            if not ZEN_COMMON_ROLE in rm.listRoleIds():
                rm.addRole(ZEN_COMMON_ROLE)

        # ZEN_COMMON permission is only permission for the ZEN_COMMON_ROLE
        self.addPermissions(zport, ZEN_COMMON,
            [ZEN_COMMON_ROLE,], 1)

        #logfile_i.close()

    def removeZenOperatorRole(self, zport):
        #logfile_r=open(logfileBaseName+'/logfile_r', 'a')
	dmd = self.dmd
        rms = (dmd.getPhysicalRoot().acl_users.roleManager,
                    zport.acl_users.roleManager)
	# This removes the role from the roleManager
	# If a user has this role, it is simply removed from them
        for rm in rms:
            #logfile_r.write(' rm.listRoleIds() is %s  \n ' % (rm.listRoleIds()))
            if ZEN_OP_ROLE in rm.listRoleIds():
                rm.removeRole(ZEN_OP_ROLE)
	#This removes the role from the manage_access list
        if ZEN_OP_ROLE in zport.__ac_roles__:
            rolelist=list(zport.__ac_roles__)
	    rolelist.remove(ZEN_OP_ROLE)
	    zport.__ac_roles__ = tuple(rolelist)
        #logfile_r.close()

    def removeZenCommonRole(self, zport):
        #logfile_r=open(logfileBaseName+'/logfile_r', 'a')
	dmd = self.dmd
        rms = (dmd.getPhysicalRoot().acl_users.roleManager,
                    zport.acl_users.roleManager)
	# This removes the role from the roleManager
	# If a user has this role, it is simply removed from them
        for rm in rms:
            #logfile_r.write(' rm.listRoleIds() is %s  \n ' % (rm.listRoleIds()))
            if ZEN_COMMON_ROLE in rm.listRoleIds():
                rm.removeRole(ZEN_COMMON_ROLE)
	#This removes the role from the manage_access list
        if ZEN_COMMON_ROLE in zport.__ac_roles__:
            rolelist=list(zport.__ac_roles__)
	    rolelist.remove(ZEN_COMMON_ROLE)
	    zport.__ac_roles__ = tuple(rolelist)
        #logfile_r.close()

    def addPermissions(self, obj, permission, roles=None, acquire=0):
        if not roles:
            roles = []
        if not permission in obj.possible_permissions():
            obj.__ac_permissions__=(
                obj.__ac_permissions__+((permission,(),roles),))

        for permissionDir in obj.rolesOfPermission(permission):
            if permissionDir['selected']:
                if permissionDir['name'] not in roles:
                    roles.append(permissionDir['name'])
        obj.manage_permission(permission, roles, acquire)



# End of class ZenPack(ZenPackBase):

# Most of the rest of the ZenPack redefines methods in $ZENHOME/Products/ZenModel/AdministrativeRoleable.py
# Standard code does not propagate user, group and role changes to individual devices in 
#   Organizer Administered Objects (ie deviceClasses, locations, groups, systems).  This code does that.

# Code is here but commented out, to create new Role menu that basically has the same effect as the 
#  Administration / administered Objects menus.  Perhaps we want different role menus eventually......

userGroupRoletab = { 'id': 'userGroupRole',
        'name' : 'Roles',
        'action' : 'roleOverview',
        'permissions' : ( Permissions.view,)
        }

# Use the standard administeredDevices page template from Products/ZenModel/skins/zenmodel
#userGroupRoletab = { 'id': 'userGroupRole',
#        'name' : 'Roles',
#        'action' : 'administeredDevices',
#        'permissions' : ( Permissions.view,)
#        }

# Uncomment next 2 lines to get Role menu for users and groups

#UserSettings.factory_type_information[0]['actions'] += (userGroupRoletab,)
#GroupSettings.factory_type_information[0]['actions'] += (userGroupRoletab,)

#deviceOrganizerRoletab = { 'id': 'deviceOrganizerRole',
#        'name' : 'Roles',
#        'action' : 'deviceRoleManagement',
#        'permissions' : ( Permissions.view,)
#        }

# Use the standard deviceManagement page template from Products/ZenModel/skins/zenmodel
deviceOrganizerRoletab = { 'id': 'deviceOrganizerRole',
        'name' : 'Roles',
        'action' : 'deviceManagement',
        'permissions' : ( Permissions.view,)
        }

# Uncomment next 3 lines to get Role menu for Groups, Locations and Systems

#DeviceOrganizer.factory_type_information[0]['actions'] += (deviceOrganizerRoletab,)
#Location.factory_type_information[0]['actions'] += (deviceOrganizerRoletab,)
#System.factory_type_information[0]['actions'] += (deviceOrganizerRoletab,)

security = ClassSecurityInfo()

#security.declareProtected(ZEN_ADMINISTRATORS_EDIT, 'manage_addRole')
def manage_addRole(self, newId=None, REQUEST=None):
    "Add a  Role to this device"

    # Note that this code actually associates users and groups with organizers and devices, NOT roles directly
    # Many of the method names are confusing in that they have "Role" in them

    logfile_a=open(logfileBaseName+'/logfile_a', 'a')
    us = self.ZenUsers.getUserSettings(newId)
    # Check whether role already exists for this object. Only add if not already there.
    selfRoles = [s.id for s in self.adminRoles() ]
    if not (us.id in selfRoles):
        AdministrativeRole(us, self)
        logfile_a.write(' In base object (including device) clause - role for object %s is %s. New us is %s \n ' % (self.id, selfRoles, us.id))
    # If the object is not a device then apply the admin role to all devices within the organizer
    if not hasattr(self,'deviceClass'):
        for dev in self.getSubDevices():
            roleNames = [r.id for r in dev.adminRoles() ]
            logfile_a.write(' roleNames for %s are %s . New user is %s \n ' % (dev.id, roleNames, us.id))
            # Check whether role already exists for this device. Only add if not already there.
            if not (us.id in roleNames):
                AdministrativeRole(us, dev)
                # Flag these devices as added as part of an organizer, by setting level=2
                dev.manage_editAdministrativeRoles(us.id, ZEN_USER_ROLE, 2)
                logfile_a.write(' In If - role for device %s is %s. New us is %s \n ' % (dev.id, roleNames, us.id))
    # setAdminLocalRoles() is a null function - simply "pass"
    self.setAdminLocalRoles()
    if REQUEST:
        if us:
            messaging.IMessageSender(self).sendToBrowser(
                'Role Added',
                'The %s role has been added.' % newId
            )
        return self.callZenScreen(REQUEST)
    logfile_a.close()


#security.declareProtected(ZEN_ADMINISTRATORS_EDIT, 'manage_editRoles')
def manage_editRoles(self, ids=(), role=(), level=(), REQUEST=None):
    """Edit list of admin roles.
    """

    # This code DOES actually manipulate roles
    #
    # Note that role changes should be performed from an Organizer or Device DETAILS menu - if you edit
    #  roles on a user / group page then it will apply whatever that panel shows (so just changing
    #  an Organizer will NOT propagate to individual devices)

    logfile_e=open(logfileBaseName+'/logfile_e', 'a')
    if type(ids) in types.StringTypes:
        ids = [ids]
        role = [role]
        level = [level]
    logfile_e.write(' object is %s ids is %s role is %s level is %s \n' % (self.id, ids, role, level ) )
    for i, id in enumerate(ids):
        ar = self.adminRoles._getOb(id)
        ar.update(role[i], level[i])
    # If the object is not a device then apply the admin role to all devices within the organizer
        if not hasattr(self,'deviceClass'):
            for dev in self.getSubDevices():
            # Check that this user / group has an Administered Object for this device
                subar = dev.adminRoles._getOb(id, None)
                if subar is not None:
                    logfile_e.write('device is %s  id is %s subar is %s role is %s level is %s \n ' % (dev.id, id, subar, role[i], level[i] ) )
                    subar.update(role[i], level[i])
    # setAdminLocalRoles() is a null function - simply "pass"
    self.setAdminLocalRoles()
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Roles Updated',
            ('The following roles have been updated: '
             '%s' % ", ".join(ids))
        )
        return self.callZenScreen(REQUEST)
    logfile_e.close()


#security.declareProtected(ZEN_ADMINISTRATORS_EDIT, 'manage_deleteRole')
def manage_deleteRole(self, delids=(), REQUEST=None):
    """Delete admin roles from this device
    """

    # Note that this code actually associates users and groups with organizers and devices, NOT roles directly
    # Many of the method names are confusing in that they have "Role" in them

    logfile_d=open(logfileBaseName+'/logfile_d', 'a')
    if type(delids) in types.StringTypes:
        delids = [delids]
	logfile_d.write(' delids is %s \n' % (delids))
    for userid in delids:
	logfile_d.write(' userid is %s \n' % (userid))
        ar = self.adminRoles._getOb(userid, None)
        if ar is not None: ar.delete()
        self.manage_delLocalRoles((userid,))
    # If the object is not a device then delete the admin role from all devices within the organizer
        if not hasattr(self,'deviceClass'):
            for dev in self.getSubDevices():
                try:
                    logfile_d.write('device is %s \n ' % (dev.id) )
                    subar = dev.adminRoles._getOb(userid, None)
                    logfile_d.write('subar is %s \n' % (subar) )
                    if subar is not None:
                        logfile_d.write(' roleNames for %s are %s . Delete user is %s \n ' % (dev.id, subar, userid))
                        subar.delete()
                    dev.manage_delLocalRoles((userid,))
                except:
                    logfile_d.write('In except clause')
                    break
    # setAdminLocalRoles() is a null function - simply "pass"
    self.setAdminLocalRoles()
    logfile_d.write('Past setAdminLocalRoles')
    if REQUEST:
        #logfile_d.write(' In if Request clause - delids is %s \n' % (delids))
        #logfile_d.write(' In if Request clause - join delids is %s \n' % ", ".join(delids))
        if delids:
            messaging.IMessageSender(self).sendToBrowser(
                'Roles Deleted',
                ('The following roles have been deleted: '
                 '%s' % ", ".join(delids))
            )
        return self.callZenScreen(REQUEST)
    logfile_d.close()


def manage_deleteAdministrativeRole_UserSettings(self, delids=(), REQUEST=None):
    "Delete admin role from this device"
    logfile_u=open(logfileBaseName+'/logfile_u', 'a')
    if type(delids) in types.StringTypes:
        delids = [delids]
    logfile_u.write(' delids is %s \n' % (delids))
    for ar in self.adminRoles():
        logfile_u.write(' ar is %s \n' % (ar))
        mobj = ar.managedObject()
        logfile_u.write(' mobj is %s \n' % (mobj))
        if mobj.managedObjectName() not in delids: continue
        mobj = mobj.primaryAq()
        logfile_u.write(' mobj.primaryAq is %s \n' % (mobj))
        # If mobj is an organizer then the next line is going to delete all the
        #   Organizer's components so the next time round this loop will break as
        #   the next mobj will no longer exist.
        if not hasattr(mobj, 'deviceClass'):
            mobj.manage_deleteAdministrativeRole(self.id)
            break
        else:
            mobj.manage_deleteAdministrativeRole(self.id)
    if REQUEST:
        if delids:
            messaging.IMessageSender(self).sendToBrowser(
                'Roles Deleted',
                "Administrative roles were deleted."
            )
        return self.callZenScreen(REQUEST)
    logfile_u.close()


from itertools import imap
from Products.ZenModel.DeviceOrganizer import DeviceOrganizer
from Products.ZenModel.DeviceGroup import DeviceGroup
from Products.ZenModel.System import System
from Products.ZenModel.Location import Location
from Products.ZenModel.Device import Device


def removeDevices(self, uids, organizer):
    # Resolve target if a path
    if isinstance(organizer, basestring):
        organizer = self._getObject(organizer)
    assert isinstance(organizer, DeviceOrganizer)
    organizername = organizer.getOrganizerName()
    devs = imap(self._getObject, uids)
    if isinstance(organizer, DeviceGroup):
        for dev in devs:
            groups = dev.getDeviceGroupNames()

            newGroups = self._excludePath(organizername, groups)
            if newGroups != groups:
                dev.setGroups(newGroups)
                check_ar_for_removed_device(dev)
    elif isinstance(organizer, System):
        for dev in devs:
            systems = dev.getSystemNames()

            newSystems = self._excludePath(organizername, systems)
            if newSystems != systems:
                dev.setSystems(newSystems)
                check_ar_for_removed_device(dev)
    elif isinstance(organizer, Location):
        for dev in devs:
            dev.setLocation(None)
            check_ar_for_removed_device(dev)

def check_ar_for_removed_device(self):
    """ If device being removed has adminRole with level of 2
            then remove adminRole from device as well as removing device from organizer
    """
    logfile_c=open(logfileBaseName+'/logfile_c', 'a')
    logfile_c.write(' Going into check_ar_for_removed_device with self = %s \n' % (self.id))
    for ar in self.adminRoles():
        # if the adminRole level is set to 2, this indicates the ar was added as part of an organizer
        #   so delete the ar when you remove the device from an organizer
        if ar.level == 2:
            self.manage_deleteAdministrativeRole(ar.id)
    logfile_c.close()


from transaction import commit

def update_organizer_devices_with_adminRole(self):
    """ self is an organizer.  
        Updates all contained devices with adminRole(s) of organizer
    """
    # adminroles() actually delivers a user or group - not actually a role

    logfile_dar=open(logfileBaseName+'/logfile_dar', 'a')
    try:
        # Check that this really is an organizer
        organizername = self.getOrganizerName()
        for ar in self.adminRoles():
            id = ar.id
            role = ar.role
            level = ar.level
            logfile_dar.write('self is %s, id is %s, role is %s, level is %s. \n ' % (self.id, id, role, level))

            # need to delete the ar first or it wont re-add new devices
            self.manage_deleteAdministrativeRole(id)

            # This actually updates the user / usergroup
            self.manage_addAdministrativeRole(id)
            # This updates the role
            self.manage_editAdministrativeRoles( id, role, level)
    except:
        pass
    logfile_dar.close()
    commit()

def setLocalRoles(self):
    """Hook for setting permissions"""
    #logfile=open(logfileBaseName+'/logfile', 'a')
    #logfile.write('Entering setAdminLocalRoles \n')
    #logfile.write(' Object is %s \n' % (self.id) )
    #logfile.write('Exiting setAdminLocalRoles \n')
    #logfile.close()

    pass

# monkey patch these methods into AdministrativeRoleable

from Products.ZenModel.AdministrativeRoleable import AdministrativeRoleable
AdministrativeRoleable.manage_addAdministrativeRole = manage_addRole
AdministrativeRoleable.manage_editAdministrativeRoles = manage_editRoles
AdministrativeRoleable.manage_deleteAdministrativeRole = manage_deleteRole
AdministrativeRoleable.setAdminLocalRoles = setLocalRoles

# monkey patch this method into UserSettings

from Products.ZenModel.UserSettings import UserSettings
UserSettings.manage_deleteAdministrativeRole = manage_deleteAdministrativeRole_UserSettings

# monkey patch this method into devicefacade

from Products.Zuul.facades.devicefacade import DeviceFacade
DeviceFacade.removeDevices = removeDevices

# Bug exists when a User group is deleted - no check made for an Administered Object relationship so
#  half a relationship is left hanging - ticket 7837

#security.declareProtected(ZEN_MANAGE_DMD, 'manage_deleteGroups')
def manage_deleteGroups(self, groupids=(), REQUEST=None):
    """ Delete a zenoss group from the system
    """
    #logfile_g=open(logfileBaseName+'/logfile_g', 'a')
    gm = self.acl_users.groupManager
    if type(groupids) in types.StringTypes:
        groupids = [groupids]
        #logfile_g.write(' Groupids is %s \n' % (groupids) )
    for groupid in groupids:

        if self._getOb(groupid):
	    us = self._getOb(groupid)
            for ar in us.adminRoles():
                #logfile_g.write(' ar is %s \n' % (ar) )
                ar.userSetting.removeRelation()
                mobj = ar.managedObject().primaryAq()
                #logfile_g.write(' mobj is %s \n' % (mobj) )
                mobj.adminRoles._delObject(ar.id)
	    self._delObject(groupid)
        try:
            #logfile_g.write(' Groupid is %s \n' % (groupid) )
            gm.removeGroup(groupid)
            self.acl_users.ZCacheable_invalidate()
        except KeyError: pass
#        except KeyError:
		#logfile_g.write(' In except KeyError  \n' )
	

    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Groups Deleted',
            "Groups were deleted: %s." % (', '.join(groupids))
        )
        return self.callZenScreen(REQUEST)
    #logfile_g.close()

# monkey patch these methods into UserSettings

from Products.ZenModel.UserSettings  import UserSettingsManager
UserSettingsManager.manage_deleteGroups = manage_deleteGroups

# Hacks for Location to make googlemaps work for authorized devices
# We CANNOT overwrite a security tag if one exists in the Core code
# (there are no tags in Core code around the following methods)
# but we CAN impose tags here if none exist in Core
#
# Next 3 imports necessary for this code but they are declared at the top of the file
#from Globals import InitializeClass
#from AccessControl import ClassSecurityInfo
#from Products.ZenModel.ZenossSecurity import ZEN_COMMON


from Products.ZenModel.Location import Location

Location.security = ClassSecurityInfo()
Location.security.declareProtected(ZEN_COMMON, 'getChildLinks')
Location.security.declareProtected(ZEN_COMMON, 'numMappableChildren')
Location.security.declareProtected(ZEN_COMMON, 'getGeomapData')
Location.security.declareProtected(ZEN_COMMON, 'getChildGeomapData')
Location.security.declareProtected(ZEN_COMMON, 'getSecondaryNodes')

Globals.InitializeClass(Location)



