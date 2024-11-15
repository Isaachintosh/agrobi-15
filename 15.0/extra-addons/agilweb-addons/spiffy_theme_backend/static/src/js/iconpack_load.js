odoo.define('spiffy_theme_backend.tree_button', function (require) {
"use strict";
   var ListController = require('web.ListController');
   var ListView = require('web.ListView');
   var viewRegistry = require('web.view_registry');

   var TreeButton = ListController.extend({
      buttons_template: 'show_icon_pack.button',
   });

   var IrUiMenuListView = ListView.extend({
      config: _.extend({}, ListView.prototype.config, {
         Controller: TreeButton,
      }),
   });
   
   viewRegistry.add('button_in_tree', IrUiMenuListView);
});