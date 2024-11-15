# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
# Developed by Bizople Solutions Pvt. Ltd.

from odoo import http
from odoo.http import request

class BackendConfigration(http.Controller):

    @http.route(['/color/pallet/'], type='json',auth='public')
    def get_selected_pallet(self, **kw):
        config_vals = {}
        current_user = request.env.user
        app_light_bg_image = kw.get('app_light_bg_image')

        if app_light_bg_image:
            if 'data:image/' in str(app_light_bg_image):
                light_bg_file = str(app_light_bg_image).split(',')
                app_light_bg_file_mimetype = light_bg_file[0]
                app_light_bg_image = light_bg_file[1]
            else:
                light_bg_file = str(app_light_bg_image).split("'")
                app_light_bg_image = light_bg_file[1]
        else:
            app_light_bg_image = False

        config_vals.update({
            'light_primary_bg_color': kw.get('light_primary_bg_color'),
            'light_primary_text_color': kw.get('light_primary_text_color'),
            'light_bg_image': app_light_bg_image,
            'apply_light_bg_img':kw.get('apply_light_bg_img'),
            'tree_form_split_view': kw.get('tree_form_split_view'),
            'attachment_in_tree_view': kw.get('attachment_in_tree_view'),
            'separator':kw.get('selected_separator'),
            'tab':kw.get('selected_tab'),
            'checkbox':kw.get('selected_checkbox'),
            'radio': kw.get('selected_radio'),
            'popup': kw.get('selected_popup'),
            'use_custom_colors': kw.get('custom_color_pallet'),
            'color_pallet': kw.get('selected_color_pallet'),
            'appdrawer_custom_bg_color': kw.get('custom_drawer_bg'),
            'appdrawer_custom_text_color': kw.get('custom_drawer_text'),
            'use_custom_drawer_color': kw.get('custom_drawer_color_pallet'),
            'drawer_color_pallet': kw.get('selected_drawer_color_pallet'),
            'loader_style': kw.get('selected_loader'),
            'font_family': kw.get('selected_fonts'),
            'font_size': kw.get('selected_fontsize'),
            'chatter_position': kw.get('selected_chatter_position'),
            'top_menu_position': kw.get('selected_top_menu_position'),
            'theme_style': kw.get('selected_theme_style'),
            # 'multi_tab': kw.get('multi_tab'),
        })

        if current_user.backend_theme_config:
            current_user.backend_theme_config.sudo().update(config_vals)
        else:
            backend_config_record = request.env['backend.config'].sudo().create(config_vals)
            current_user.sudo().write({
                'backend_theme_config': backend_config_record.id
            })
        
        return True

    @http.route(['/color/pallet/data/'], type='http', auth='public', sitemap=False)
    def selected_pallet_data(self, **kw):
        company = request.env.company
        user = request.env.user
        admin_users = request.env['res.users'].sudo().search([
            ('groups_id','in',request.env.ref('base.user_admin').id),
            ('backend_theme_config','!=',False),
        ], order="id asc", limit=1)

        admin_config = False
        if admin_users:
            admin_config = admin_users.backend_theme_config
        

        if company.backend_theme_level == 'user_level':
            if user.backend_theme_config:
                config_vals = user.backend_theme_config
            elif admin_config:
                config_vals = admin_config
            else:
                config_vals = request.env['backend.config'].sudo().search([], order="id asc", limit=1)
        else:
            if admin_config:
                config_vals = admin_config
            else:
                config_vals = request.env['backend.config'].sudo().search([], order="id asc", limit=1)
        
        values = {}
        separator_selection_dict = dict(config_vals._fields['separator'].selection)
        tab_selection_dict = dict(config_vals._fields['tab'].selection)
        checkbox_selection_dict = dict(config_vals._fields['checkbox'].selection)
        radio_selection_dict = dict(config_vals._fields['radio'].selection)
        popup_selection_dict = dict(config_vals._fields['popup'].selection)
        light_bg_image = config_vals.light_bg_image
        values.update({
            'config_vals': config_vals,
            'separator_selection_dict': separator_selection_dict,
            'tab_selection_dict': tab_selection_dict,
            'checkbox_selection_dict': checkbox_selection_dict,
            'radio_selection_dict': radio_selection_dict,
            'popup_selection_dict': popup_selection_dict,
            'app_background_image':light_bg_image,
        })

        response = request.render("spiffy_theme_backend.template_backend_config_data", values) 
        
        return response 

    @http.route(['/get/model/record'], type='json',auth='public')
    def get_record_data(self, **kw):
        company = request.env.company
        user = request.env.user
        admin_group_id = request.env.ref('base.user_admin').id
        is_admin = False
        if admin_group_id in user.groups_id.ids:
            is_admin = True
        admin_users = request.env['res.users'].sudo().search([
            ('groups_id','in',request.env.ref('base.user_admin').id),
            ('backend_theme_config','!=',False),
        ], order="id asc", limit=1)
        
        admin_users_ids = admin_users.ids
        admin_config = False
        if admin_users:
            admin_config = admin_users.backend_theme_config
        show_edit_mode = True
        for admin in admin_users:
            if admin.backend_theme_config:
                admin_config = admin.backend_theme_config
                break
            else:
                continue

        if company.backend_theme_level == 'user_level':
            if user.backend_theme_config:
                record_vals = user.backend_theme_config
            elif admin_config:
                record_vals = admin_config
            else:
                record_vals = request.env['backend.config'].sudo().search([], order="id asc", limit=1)
        else:
            if not user.id in admin_users_ids:
                show_edit_mode = False
            if admin_config:
                record_vals = admin_config
            else:
                record_vals = request.env['backend.config'].sudo().search([], order="id asc", limit=1)

        prod_obj = request.env['backend.config']
        record_dict = record_vals.read(set(prod_obj._fields))
        if user.dark_mode:
            darkmode = "dark_mode"
        else:
            darkmode = False
        if user.vertical_sidebar_pinned:
            pinned_sidebar = "pinned"
        else:
            pinned_sidebar = False
        record_val = {
            'record_dict': record_dict,
            'darkmode': darkmode,
            'pinned_sidebar': pinned_sidebar,
            'show_edit_mode': show_edit_mode,
            'is_admin': is_admin,
        }
        return record_val

    @http.route(['/get-favorite-apps'], type='json',auth='public')
    def get_favorite_apps(self, **kw):
        user_id = request.env.user
        app_list = []
        # user_id.sudo().write({
        #     'app_ids': False,
        # })
        if user_id.app_ids:
            for app in user_id.app_ids:
                irmenu = request.env['ir.ui.menu'].sudo().search([('id','=',app.app_id)])
                if irmenu:
                    app_dict = {
                        'name': app.name,
                        'app_id': app.app_id,
                        'app_xmlid': app.app_xmlid,
                        'app_actionid': app.app_actionid,
                        'line_id': app.id,
                        'use_icon': irmenu.use_icon,
                        'icon_class_name': irmenu.icon_class_name,
                        'icon_img': irmenu.icon_img,
                        'web_icon_data': irmenu.web_icon_data,
                    }
                    app_list.append(app_dict)
            record_val = {
                'app_list': app_list,
            }
            return record_val
        else:
            return False

    @http.route(['/update-user-fav-apps'], type='json',auth='public')
    def update_favorite_apps(self, **kw):
        user_id = request.env.user
        user_id.sudo().write({
            'app_ids': [(0, 0, {
                'name': kw.get('app_name'),
                'app_id': kw.get('app_id'),
            })]
        })
        return True

    @http.route(['/remove-user-fav-apps'], type='json',auth='public')
    def remove_favorite_apps(self, **kw):
        user_id = request.env.user

        for line in user_id.app_ids:
            if line.app_id == str(kw.get('app_id')):
                user_id.sudo().write({
                    'app_ids': [(3, line.id)]
                })
        return True

    """ @http.route(['/get/active/menu'], type='json',auth='public')
    def get_active_menu_data(self, **kw):
        menu_items = []
        menu_records = request.env['ir.ui.menu'].search([('parent_id', '=', False)])
        for menu in menu_records:
            menu_items.append({
                'menu_name': menu.complete_name,
                'menu_id':menu.id
            })
        return menu_items """

    """ @http.route(['/get/appsearch/data'], type='json',auth='public')
    def get_appsearch_data(self, menuOption=None, **kw):
        menu_items = []
        menu_records = request.env['ir.ui.menu'].search([('name', 'ilike', kw.get('searchvals'))], order ='id asc')
        if menuOption:
            for record in menu_records:
                if record.parent_path:
                    parent_record = record.parent_path.split('/')
                    parent_record_id = parent_record[0]
                    if parent_record_id == menuOption:
                        if not record.child_id:
                            menu_items.append({
                                'name': record.complete_name,
                                'menu_id':record.id
                            })
        else:
            for record in menu_records:
                if not record.child_id:
                    menu_items.append({
                        'name': record.complete_name,
                        'menu_id':record.id,
                        'previous_menu_id': record.parent_id.id,
                        'action_id': record.action.id if record.action else None,
                    })
        return menu_items """

    @http.route(['/get/tab/title/'], type='json', auth='public')
    def get_tab_title(self, **kw):
        company_id = request.env.company
        new_name = company_id.tab_name
        return new_name

    @http.route(['/get/active/lang'], type='json', auth='public')
    def get_active_lang(self, **kw):
        lang_records = request.env['res.lang'].sudo().search([('active', '=', 'True')])
        lang_list = []
        for lang in lang_records:
            lang_list.append({
                'lang_name' :lang.name,
                'lang_code': lang.code,
            })
        
        return lang_list
    
    @http.route(['/change/active/lang'], type='json', auth='public')
    def biz_change_active_lang(self, **kw):
        request.env.user.lang = kw.get('lang')
        return True

    @http.route(['/active/dark/mode'], type='json', auth='public')
    def active_dark_mode(self, **kw):
        dark_mode = kw.get('dark_mode')
        backend_theme_config = request.env['backend.config'].sudo().search([])
        user = request.env.user
        if dark_mode == 'on':
            user.update({
                'dark_mode': True,
            })
            dark_mode = user.dark_mode
            return dark_mode
        elif dark_mode == 'off':
            user.update({
                'dark_mode': False,
            })
            dark_mode = user.dark_mode
            return dark_mode

    @http.route(['/sidebar/behavior/update'], type='json', auth='public')
    def sidebar_behavior(self, **kw):
        user = request.env.user
        sidebar_pinned = kw.get('sidebar_pinned')
        user.update({
            'vertical_sidebar_pinned': sidebar_pinned,
        })
        return True

    @http.route(['/get/dark/mode/data'], type='json', auth='public')
    def dark_mode_on(self, **kw):
        user = request.env.user
        dark_mode_value = user.dark_mode

        return dark_mode_value
    
    @http.route(['/add/mutli/tab'], type='json', auth='public')
    def add_multi_tab(self, **kw):
        user = request.env.user
        # user.sudo().write({
        #     'multi_tab_ids': False,
        # })
        multi_tab_ids = user.multi_tab_ids.filtered(lambda mt: mt.name == kw.get('name'))
        if not multi_tab_ids:
            user.sudo().write({
                'multi_tab_ids': [(0, 0,  {
                    'name': kw.get('name'),
                    'url': kw.get('url'),
                    'actionId': kw.get('actionId'),
                    'menuId': kw.get('menuId'),
                    'menu_xmlid': kw.get('menu_xmlid'),
                })]
            })

        return True
    
    @http.route(['/get/mutli/tab'], type='json', auth='public')
    def get_multi_tab(self, **kw):
        obj = request.env['biz.multi.tab']
        user = request.env.user
        if user.multi_tab_ids:
            record_dict = user.multi_tab_ids.sudo().read(set(obj._fields))
            return record_dict
        else:
            return False
    
    @http.route(['/remove/multi/tab'], type='json', auth='public')
    def remove_multi_tab(self, **kw):
        multi_tab = request.env['biz.multi.tab'].sudo().search([('id','=',kw.get('multi_tab_id'))])
        multi_tab.unlink()
        user = request.env.user
        multi_tab_count = len(user.multi_tab_ids)
        values = {
            'removeTab': True,
            'multi_tab_count': multi_tab_count,
        }
        return values

    @http.route(['/update/tab/details'], type='json', auth='public')
    def update_tabaction(self, **kw):
        tabId = kw.get('tabId')
        TabTitle = kw.get('TabTitle')
        url = kw.get('url')
        ActionId = kw.get('ActionId')
        menu_xmlid = kw.get('menu_xmlid')

        multi_tab = request.env['biz.multi.tab'].sudo().search([('id', '=', tabId)])
        if multi_tab:
            multi_tab.sudo().write({
                'name': TabTitle or multi_tab.name,
                'url': url or multi_tab.url,
                'actionId': ActionId or multi_tab.ActionId,
                'menu_xmlid': menu_xmlid or multi_tab.menu_xmlid,
            })
        return True
    
    @http.route(['/add/bookmark/link'], type='json', auth='public')
    def add_bookmark_link(self, **kw):
        user = request.env.user
        bookmark_ids = user.bookmark_ids.filtered(lambda b: b.name == kw.get('name'))
        if not bookmark_ids:
            user.sudo().write({
                'bookmark_ids': [(0, 0,  {
                    'name': kw.get('name'),
                    'url': kw.get('url'),
                    'title': kw.get('title'),
                })]
            })

        return True
    
    @http.route(['/update/bookmark/link'], type='json', auth='public')
    def update_bookmark_link(self, **kw):
        bookmark = request.env['bookmark.link'].sudo().search([('id','=',kw.get('bookmark_id'))])
        updated_bookmark = bookmark.update({
            'name': kw.get('bookmark_name'),
            'title': kw.get('bookmark_title'),
        })
        return True
    
    @http.route(['/remove/bookmark/link'], type='json', auth='public')
    def remove_bookmark_link(self, **kw):
        bookmark = request.env['bookmark.link'].sudo().search([('id','=',kw.get('bookmark_id'))])
        bookmark.unlink()
        return True
    
    @http.route(['/get/bookmark/link'], type='json', auth='public')
    def get_bookmark_link(self, **kw):
        obj = request.env['bookmark.link']
        user = request.env.user
        record_dict = user.bookmark_ids.sudo().read(set(obj._fields))
        return record_dict
    
    @http.route(['/get/attachment/data'], type='json', auth='public')
    def get_attachment_data(self, **kw):
        rec_ids = kw.get('rec_ids')
        for rec in rec_ids:
            if isinstance(rec, str):
                rec_ids.remove(rec)
        if kw.get('model') and rec_ids:
            # FOR DATA SPEED ISSUE; SEARCH ATTACHMENT DATA WITH SQL QUERY
            attachments = request.env['ir.attachment'].search([
                ('res_model', '=', kw.get('model'))
            ])
            attachment_data = []
            attachment_res_id_set = set()
            for attachment in attachments:
                attachment_res_id_set.add(attachment.res_id)
            dict ={}
            for res_id in attachment_res_id_set:
                filtered_attachment_record = attachments.filtered(lambda attachment: attachment.res_id == res_id)
                for fac in filtered_attachment_record:
                    if dict.get(res_id):
                        dict[res_id].append({
                            'attachment_id': fac.id,
                            'attachment_mimetype': fac.mimetype,
                            'attachment_name': fac.name,
                        })
                    else:
                        dict[res_id] = [{
                            'attachment_id': fac.id,
                            'attachment_mimetype': fac.mimetype,
                            'attachment_name': fac.name,
                        }]
            attachment_data.append(dict)
            return attachment_data
        
    @http.route(['/get/irmenu/icondata'], type='json', auth='public')
    def get_irmenu_icondata(self, **kw):
        irmenuobj = request.env['ir.ui.menu']
        irmenu = request.env['ir.ui.menu'].sudo().search([('id','in',kw.get('menu_ids'))])

        app_menu_dict = {}
        for menu in irmenu:
            menu_dict = menu.read(set(irmenuobj._fields))
            app_menu_dict[menu.id] = menu_dict
        return app_menu_dict