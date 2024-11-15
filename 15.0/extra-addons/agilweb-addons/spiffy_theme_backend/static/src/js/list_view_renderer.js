/** @odoo-module **/
import DocumentViewer from '@mail/js/document_viewer';
import view_registry from 'web.view_registry';
import ActionMenus from 'web.ActionMenus';

    var ListRenderer = require('web.ListRenderer');
    var ajax = require("web.ajax");
    var core = require("web.core");
    var dom = require("web.dom");
    var _t = core._t;
    var { patch } = require("web.utils");

    var biz_listrenderer = ListRenderer.include({
        events: _.extend({}, ListRenderer.prototype.events, {
            "click .attachment_box": "_loadattachmentviewer",
        }),
        willStart: async function () {
            const _super = this._super.bind(this);
            var self = this;
            await ajax.jsonRpc("/get/attachment/data", "call", {
                domain: this.state.domain,
                model: this.state.model,
                rec_ids: this.state.res_ids,
            }).then(function (data) {
                if (data) {
                  self.biz_attachment_data = data;
                }
            });
            return _super(...arguments);
        },
        _loadattachmentviewer: function (ev) {
            var attachment_id = parseInt($(ev.currentTarget).data("id"));
            var rec_id = parseInt($(ev.currentTarget).data("rec_id"));
            var attachment_mimetype = $(ev.currentTarget).data("mimetype");
            var mimetype_match = attachment_mimetype.match("(image|application/pdf|text|video)");
            var attachment_data = this.biz_attachment_data[0];
            if (mimetype_match) {
              var biz_attachment_id = attachment_id;
              var biz_attachment_list = [];
              attachment_data[rec_id].forEach((attachment) => {
                if (attachment.attachment_mimetype.match("(image|application/pdf|text|video)")) {
                  biz_attachment_list.push({
                    id: attachment.attachment_id,
                    filename: attachment.attachment_name,
                    name: attachment.attachment_name,
                    url: "/web/content/"+attachment.attachment_id+"?download=true",
                    type: attachment.attachment_mimetype,
                    mimetype: attachment.attachment_mimetype,
                    is_main: false,
                  });
                }
              });
              var biz_attachmentViewer = new DocumentViewer(self,biz_attachment_list,biz_attachment_id);
              biz_attachmentViewer.appendTo($("body"));
            } else this.call("notification", "notify", {
                title: _t("File Format Not Supported"),
                message: _t("Preview for this file type can not be shown"),
                sticky: false,
            });
        },
        _renderRow: function (record) {
            var res = this._super.apply(this, arguments);
            if ($('body').hasClass('show_attachment')){
              if (this.biz_attachment_data) {
                var attachment_data = this.biz_attachment_data[0];
                if (attachment_data[record.data.id]) {
                    var $main_div = $("<div>", {
                        class: "attachment_div",
                    });
                    var $attachment_section = $("<section>", {
                      class: "biz_attachment_section d-flex align-items-center justify-content-center w-100 position-absolute flex-wrap",
                      id: record.id,
                    });
                    attachment_data[record.data.id].every((attachment, index, arr) => {
                      if (index < 5) {
                        var $attachment_box = $("<div>", {
                          class: "attachment_box border d-flex align-items-center mx-2",
                          "data-id": attachment.attachment_id,
                          "data-name": attachment.attachment_name,
                          "data-mimetype": attachment.attachment_mimetype,
                          "data-rec_id": record.data.id,
                        });
          
                        var $attachment_image = $("<span>", {
                            "data-mimetype": attachment.attachment_mimetype,
                            class: "o_image mr-2",
                        })
                        $attachment_box = $attachment_box.append($attachment_image);
          
                        var $attachment_name = $("<div>", {
                          class: "attachment-name text-nowrap",
                        }).append($("<span>").html(attachment.attachment_name));
                        $attachment_box = $attachment_box.append($attachment_name);
  
                        $attachment_section = $attachment_section.append($attachment_box);
                        $main_div = $main_div.append($attachment_section);
                        return true;
                      } else {
                        var $attachment_box = $("<div>", {
                          class: "attachment_box border attachment_box_counter d-flex align-items-center px-2 ",
                          "data-id": attachment.attachment_id,
                          "data-name": attachment.attachment_name,
                          "data-mimetype": attachment.attachment_mimetype,
                          "data-rec_id": record.data.id,
                        });
                        var $attachment_name = $("<div>", {
                          class: "attachment-name text-nowrap",
                        }).append(
                          $("<span>").html("+" + (arr.length - 5))
                        );
                        $attachment_box = $attachment_box.append($attachment_name);
                        $attachment_section = $attachment_section.append($attachment_box);
                        $main_div = $main_div.append($attachment_section);
                        return false;
                      }
                    });
                    res = res.add($main_div);
                }
              }
            }
            return res
        },

        _onRowClicked: function (ev) {
          var self = this
          var record_id = $(ev.currentTarget).attr('data-id');
          if ($('body').hasClass('tree_form_split_view') && !$(ev.target).parents('.tree-form-viewer').length && !ev.target.closest('.o_list_record_selector') && !this.editable) {
            var size = $(window).width();
            if (size <= 1200) {
              this.$el.removeClass('tree_form_split')
              $('.o_list_view').attr('style','')
              $('.tree-form-viewer').remove()
              this._super.apply(this, arguments);
            } else {
              this.split_view_controller(record_id);
            }
          } else {
            this._super.apply(this, arguments);
          }
        },

        _removeTreeFormView: function() {
          $('.tree_form_split > .o_view_controller > .o_content > #separator').remove()
          $('.tree_form_split > .o_view_controller > .o_content > .o_view_controller').remove()
          $('.tree_form_split > .o_view_controller > .o_content > .close_form_view').remove()
          $('.o_action_manager.tree_form_split').removeClass('tree_form_split')
          $('.o_list_view').attr('style','')
          $('.reload_view').click()
        },

        split_view_controller: function (record_id) {
          var self = this;
          var ListController = this.getParent();
          var AdaptView = ListController.getParent();
          var currentController = AdaptView.actionService.currentController;

          var params = {
            resModel: currentController.props.resModel,
            views: currentController.props.views,
            context: currentController.props.context,
          };
          var options = {
            actionId: currentController.action.id,
            loadActionMenus: currentController.props.loadActionMenus,
            loadIrFilters: currentController.props.loadIrFilters,
          };

          var biz_form_controller = this.biz_form_controller(record_id,ListController,AdaptView,currentController,params,options)

          biz_form_controller.then(function(formview){
            var fragment = document.createDocumentFragment();

            return formview.appendTo(fragment)
            .then(function () {
              formview.toolbarActions = {}
              $('.tree_form_split_view > .o_action_manager > .o_view_controller > .o_content > .o_view_controller').remove();
              $('#separator').remove();
              $('.close_form_view').remove();
              dom.append(self.$el.parent(), fragment, {
                  callbacks: [{widget: formview}],
                  in_DOM: true,
              })
              
              $('.tree_form_split_view > .o_action_manager').addClass('tree_form_split')
              $('.tree_form_split_view > .o_action_manager > .o_view_controller').addClass('split-screen-tree-viewer')
              $('.tree_form_split_view > .o_action_manager > .o_view_controller > .o_content > .o_view_controller').addClass('tree-form-viewer')

              $('.tree_form_split_view > .o_action_manager > .o_view_controller > .o_content > .o_list_view').before('<div class="close_form_view">X</div>')
              $('.tree_form_split_view > .o_action_manager > .o_view_controller > .o_content > .o_list_view').after('<div id="separator" class="split_view_separator"></div>')

              $('.close_form_view').unbind().click(function(e) {
                self._removeTreeFormView()
              })

              $('.o_action_manager.tree_form_split > .split-screen-tree-viewer > .o_control_panel .reload_view').click()

              var options = {
                containment: 'parent',
                helper: 'clone'
              }
              Object.assign(options, {
                axis: 'x',
                start: function(event, ui) {
                    $(this).attr('start_offset', $(this).offset().left);
                    $(this).attr('start_next_height', $(this).next().width());
                },
                drag: function(event, ui) {
                    var prev_element = $(this).prev();
                    prev_element.width(ui.offset.left - prev_element.offset().left);
                }
              })
              $('#separator').draggable(options);
              $('#separator').on("dragstop", function(event, ui) {
                  $('.custom_seperator').css({
                      'opacity': '1'
                  })
              });
            });
          })

        },

        biz_form_controller: function(record_id,ListController,AdaptView,currentController,params,options){
          var self = this;
          var FormView = view_registry.get('form');

          var fields_view_def = AdaptView.vm.loadViews(params, options);
          var rec_id = ListController.model.get(record_id, {raw: true});

          return fields_view_def.then(function (viewInfo) {
              viewInfo['form'].toolbar = viewInfo['form'].actionMenus
              var formview = new FormView(viewInfo['form'], {
                  action: currentController.action,
                  modelName: ListController.modelName,
                  context: currentController.props.context,
                  ids: rec_id.res_id ? self.state.res_ids : [],
                  currentId: rec_id.res_id || undefined,
                  index: 0,
                  mode: self.mode,
                  footerToButtons: true,
                  default_buttons: true,
                  withControlPanel: true,
                  model: ListController.model,
                  parentID: self.parentID,
                  recordID: self.recordID,
              });
              return formview.getController(AdaptView);
          })
        },
    });

    patch(ActionMenus.prototype, "spiffy_theme_backend.actionmenuinherit", {
      async willUpdateProps(nextProps) {
        nextProps.items = this.env.view.toolbar
        this.actionItems = await this._setActionItems(nextProps);
        this.printItems = await this._setPrintItems(nextProps);
        $('.o_action_manager.tree_form_split > .split-screen-tree-viewer > .o_control_panel .reload_view').click()
      }
    })

    return biz_listrenderer;