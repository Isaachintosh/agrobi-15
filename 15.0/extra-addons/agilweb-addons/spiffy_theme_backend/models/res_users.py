# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class User(models.Model):
    _inherit = "res.users"

    app_ids = fields.One2many('favorite.apps', 'user_id',string="Favorite Apps")
    bookmark_ids = fields.One2many('bookmark.link', 'user_id',string="Bookmark Links")
    multi_tab_ids = fields.One2many('biz.multi.tab', 'user_id',string="Multi Tabs")
    dark_mode = fields.Boolean(string="Is dark Mode Active", default=False)
    vertical_sidebar_pinned = fields.Boolean(string="Pinned Sidebar", default=True)
    backend_theme_config = fields.Many2one('backend.config', string="Backend Config", copy=False)
	# multi_tab = fields.Boolean(related="backend_theme_config.multi_tab", string="Enable Multi Tab?")