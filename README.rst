==========================
ZenPacks.skills1st.UserRoles
==========================

Description
===========

NOTE THAT THIS IS A BETA ZENPACK AND SHOULD NOT BE INSTALLED ON A PRODUCTION SYSTEM.

Zenoss Core doesn't provide any easy way to create new roles and permissions.  Zenoss Enterprise has the Device Access Control Lists ZenPack (documented in the Extended Monitoring Guide) but I don't believe this delivers anything very sophisticated.

 

I have created a ZenPack that works with the concept of Administered Objects to:

    * Create a new role, ZenOperator, that has the normal ZenUser permissions plus "Manage Events" which lets a user Ack / Close events
    * Create a new role, ZenCommon, with very minimal permissions
    * For those devices / device organizers that are allocated as Administered Objects to a user,  devices can be viewed, their events can be Ack'ed / Closed, performance graphs are available and Locations will appear on the Dashboard GoogleMaps portlet.
    * Conversely, users ONLY see what are allocated to them as Administerd Objects
    * I have included a utility I found on the wiki (I think from cluther???) - copyDashboardState.py - that copies a model dashboard to other users - it's in the lib directory.
    * Fixes various bugs to do with Administered Objects so that Locations, Groups Systems and Device Classes can be allocated / removed successfully as Administered Objects

This is currently development code and would much appreciate other testers.  The code should be installed in a backed-up, test environment.  The ZenPack was developed in a 3.1 environment and has at least been installed on a 2.5.2 system.

    * Download the tarball
    * Untar it - I put such things into $ZENHOME/local.  Change to this directory.
    * Install in development mode, as the zenoss user, with :
        * zenpack --link --install ZenPacks.skills1st.UserRoles
        * zenhub restart
        * zopectl restart
        * Point your browser at <your zenoss>:8080/zport/manage_access and check that ZenOperator and ZenCommon roles exist
    * Read the README and the comments at the start of __init__.py
    * To test the ZenPack:
        * Create a test group
        * Allocate an Administered Object to this group - ideally a smallish Location, Group or System
        * Change the role for this Group's Administered Objects to be ZenOperator (do this starting from the Location / Group / System -> DETAILS -> Administration menu, not from ADVANCED -> Settings -> Users)
        * Create a user and give it the ZenCommon basic role.  Assign it to the test user group.
        * Logoff and log on as the new user.  Check that you see only the devices and organizers allocated as Administered Objects
        * Take care with testing - web browsers are likely to cache who you are logged on as, even if you logoff one tab

 
For more discussions around the development process have a look at http://community.zenoss.org/message/59387#59387 .

This is just a starting point.  Users authorised to see various Administered Objects don't see any reports (but they do get a blank REPORTS top-level menu).

This ZenPack creates 2 new roles; it does not look at creating any new permissions; nor does it address how to apply new roles and permissions to existing Zenoss Core code.

Organisation will want a more generic way of specifying roles and permissions.

I am actively looking for other sponsors of this work.  I am hoping that it is of interest to several organisations who would be prepared to contribute development funds and/or coding efforts - obviously they also get to help specify the requirements.
 

The Zenoss Community Alliance hopes that this will be the first example of a joint community development.


Components
==========

         

Requirements & Dependencies
===========================

    * Zenoss Versions Supported: 3.1
    * External Dependencies: 
    * ZenPack Dependencies:
    * Installation Notes: zenhub and zopectl restart after installing this ZenPack.
    * Configuration: 

Download
========
Download the appropriate package for your Zenoss version from the list
below.

* Zenoss 3.0+ `Latest Package for Python 2.6`_
* Zenoss 4.0+ `Latest Package for Python 2.7`_

Installation
============
Normal Installation (packaged egg)
----------------------------------
 
This ZenPack should probably only be installed in development mode as it is a BETA!!! ie. DON'T DO THIS YET.

Copy the downloaded .egg to your Zenoss server and run the following commands as the zenoss
user::

   zenpack --install <package.egg>
   zenhub restart
   zopectl restart

Developer Installation (link mode)
----------------------------------

    * Download the tarball
    * Untar it - I put such things into $ZENHOME/local.  Change to this directory.
    * Install in development mode, as the zenoss user, with :
        * zenpack --link --install ZenPacks.skills1st.UserRoles
        * zenhub restart
        * zopectl restart
        * Point your browser at <your zenoss>:8080/zport/manage_access and check that ZenOperator and ZenCommon roles exist
    * Read the README and the comments at the start of __init__.py

If you wish to further develop and possibly contribute back to this 
ZenPack you should clone the git repository, then install the ZenPack in
developer mode::


Configuration
=============

Tested with Zenoss 3.1 against. Installed on 2.5.2.

Change History
==============
* 1.0.1
   * Initial Release
* 1.1.1
   * Release for 4.x with fixes for ZenPack removal (_excludePath message caused by change in role attribute) 

Screenshots
===========
|myScreenshot|


.. External References Below. Nothing Below This Line Should Be Rendered

.. _Latest Package for Python 2.6: https://github.com/jcurry/ZenPacks.skills1st.UserRoles/blob/master/dist/ZenPacks.skills1st.UserRoles-1.0.1-py2.6.egg?raw=true
.. _Latest Package for Python 2.7: https://github.com/jcurry/ZenPacks.skills1st.UserRoles/blob/4.x/dist/ZenPacks.skills1st.UserRoles-1.1.1-py2.7.egg?raw=true

.. |myScreenshot| image:: http://github.com/jcurry/ZenPacks.skills1st.UserRoles/raw/master/screenshots/myScreenshot.jpg

                                                                        

