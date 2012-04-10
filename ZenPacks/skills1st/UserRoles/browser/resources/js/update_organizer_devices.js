// New menu option on the device list cog wheel menu, context-configure-menu

Ext.ComponentMgr.onAvailable('context-configure-menu', function(config) {
  var origOnGet = config.onGetMenuItems;
  config.onGetMenuItems = function(uid) {
    var result = origOnGet.call(this, uid) || [];
    // Menu item only shows up when certain device class is selected
    if( uid.match('^/zport/dmd/Locations/') || uid.match('^/zport/dmd/Systems/') || uid.match('^/zport/dmd/Groups/')) {
        result.push( {
            text: _t('Update organizer devices with Administrative Roles'),
            hidden: Zenoss.Security.doesNotHavePermission('Administrators Edit'),
            handler: function() {
                var win = new Zenoss.dialog.CloseDialog({
                    width: 600,
                    title: _t('Update organizer devices with Administrative Roles'),
                    items: [{
                        buttons: [{
                            xtype: 'DialogButton',
                            id: 'updateDevice-submit',
                            text: _t('Modify'),
                            handler: function(b) {

                                //  Following line must match the class defined in routers.py
                                //    and the last part must match the method defined on that class
                                //    ie. router class = updateDevsRouter, method = updateDevsFunc

                                Zenoss.remote.updateDevsRouter.updateDevsFunc(
                                            function(response) {
                                                if (response.success) {
                                                    new Zenoss.dialog.SimpleMessageDialog({
                                                        title: _t(' Device modified'),
                                                        message: response.msg,
                                                        buttons: [{
                                                            xtype: 'DialogButton',
                                                            text: _t('OK')
                                                        }]
                                                    }).show();
                                                }
                                                else {
                                                    new Zenoss.dialog.SimpleMessageDialog({
                                                        message: response.msg,
                                                        buttons: [{
                                                            xtype: 'DialogButton',
                                                            text: _t('OK')
                                                        }]
                                                    }).show();
                                                }
                                            });
                            }
                        }, Zenoss.dialog.CANCEL]
                     }]
                });
                win.show();
            }
        });
    }
    return result;
  };
});


