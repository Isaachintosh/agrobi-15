/** @odoo-module **/
import {registry} from "@web/core/registry";
import {debounce} from "@web/core/utils/timing";
import config from "web.config";
import core from "web.core";

import LegacyControlPanel from "web.ControlPanel";
import {ControlPanel} from "@web/search/control_panel/control_panel";
import SearchPanel from "@web/legacy/js/views/search_panel";
import {patch} from "web.utils";

const {useState, useContext} = owl.hooks;
const {Context} = owl;

export const deviceContext = new Context({
    isSmall: config.device.isMobile,
    size: config.device.size_class,
    SIZES: config.device.SIZES,
});
const uiContextService = {
    dependencies: ["ui"],
    start(env, {ui}) {
        window.addEventListener(
            "resize",
            debounce(() => {
                const state = deviceContext.state;
                if (state.size !== ui.size) {
                    state.size = ui.size;
                }
                if (state.isSmall !== ui.isSmall) {
                    state.isSmall = ui.isSmall;
                    config.device.isMobile = state.isSmall;
                    config.device.size_class = state.size;
                    core.bus.trigger("UI_CONTEXT:IS_SMALL_CHANGED");
                }
            }, 150) // UIService debounce for this event is 100
        );

        return deviceContext;
    },
};

patch(LegacyControlPanel.prototype, "spiffy_theme_backend.LegacyControlPanelMobile", {
    setup() {
        this._super();
        this.state = useState({
            mobileSearchMode: this.props.withBreadcrumbs ? "" : "quick",
        });
        this.ui = useContext(deviceContext);
    },
    setMobileSearchMode(ev) {
        this.state.mobileSearchMode = ev.detail;
    },
});

patch(ControlPanel.prototype, "spiffy_theme_backend.ControlPanelMobile", {
    setup() {
        this._super();
        this.state = useState({
            mobileSearchMode: "",
        });
        this.ui = useContext(deviceContext);
    },
    setMobileSearchMode(ev) {
        this.state.mobileSearchMode = ev.detail;
    },
});

patch(SearchPanel.prototype, "spiffy_theme_backend.SearchPanelMobile", {
    setup() {
        this._super();
        this.state.mobileSearch = false;
        this.ui = useContext(deviceContext);
    },
    getActiveSummary() {
        const selection = [];
        for (const filter of this.model.get("sections")) {
            let filterValues = [];
            if (filter.type === "category") {
                if (filter.activeValueId) {
                    const parentIds = this._getAncestorValueIds(
                        filter,
                        filter.activeValueId
                    );
                    filterValues = [...parentIds, filter.activeValueId].map(
                        (valueId) => filter.values.get(valueId).display_name
                    );
                }
            } else {
                let values = [];
                if (filter.groups) {
                    values = [
                        ...[...filter.groups.values()].map((g) => g.values),
                    ].flat();
                }
                if (filter.values) {
                    values = [...filter.values.values()];
                }
                filterValues = values
                    .filter((v) => v.checked)
                    .map((v) => v.display_name);
            }
            if (filterValues.length) {
                selection.push({
                    values: filterValues,
                    icon: filter.icon,
                    color: filter.color,
                    type: filter.type,
                });
            }
        }
        return selection;
    },
});


registry.category("services").add("ui_context", uiContextService);
// odoo.define("spiffy_theme_backend.responsive", function (require) {
    // const config = require("web.config");
    // const ControlPanel = require("web.ControlPanel");
    // const SearchPanel = require("web/static/src/js/views/search_panel.js");
    // const {QWeb, Context} = owl;
    // const {useState, useContext} = owl.hooks;

    // const deviceContext = new Context({
    //     isMobile: config.device.isMobile,
    //     size_class: config.device.size_class,
    //     SIZES: config.device.SIZES,
    // });

    // ControlPanel.patch("spiffy_theme_backend.ControlPanelMobile", (T) => {
    //     class ControlPanelPatchResponsive extends T {
    //         constructor() {
    //             super(...arguments);
    //             this.state = useState({
    //                 mobileSearchMode: "",
    //             });
    //             this.device = useContext(deviceContext);
    //         }
    //     }
    //     return ControlPanelPatchResponsive;
    // });

    // // Patch search panel to add functionality for mobile view
    // SearchPanel.patch("spiffy_theme_backend.SearchPanelMobile", (T) => {
    //     class SearchPanelPatchResponsive extends T {
    //         constructor() {
    //             super(...arguments);
    //             this.state.mobileSearch = false;
    //             this.device = useContext(deviceContext);
    //         }
    //         getActiveSummary() {
    //             const selection = [];
    //             for (const filter of this.model.get("sections")) {
    //                 let filterValues = [];
    //                 if (filter.type === "category") {
    //                     if (filter.activeValueId) {
    //                         const parentIds = this._getAncestorValueIds(
    //                             filter,
    //                             filter.activeValueId
    //                         );
    //                         filterValues = [...parentIds, filter.activeValueId].map(
    //                             (valueId) => filter.values.get(valueId).display_name
    //                         );
    //                     }
    //                 } else {
    //                     let values = [];
    //                     if (filter.groups) {
    //                         values = Array.from(
    //                             filter.groups.values(),
    //                             (g) => g.values
    //                         ).flat();
    //                     }
    //                     if (filter.values) {
    //                         values = [...filter.values.values()];
    //                     }
    //                     filterValues = values
    //                         .filter((v) => v.checked)
    //                         .map((v) => v.display_name);
    //                 }
    //                 if (filterValues.length) {
    //                     selection.push({
    //                         values: filterValues,
    //                         icon: filter.icon,
    //                         color: filter.color,
    //                         type: filter.type,
    //                     });
    //                 }
    //             }
    //             return selection;
    //         }
    //     }
    //     return SearchPanelPatchResponsive;
    // });

    // return {
    //     deviceContext: deviceContext,
    // };
// });