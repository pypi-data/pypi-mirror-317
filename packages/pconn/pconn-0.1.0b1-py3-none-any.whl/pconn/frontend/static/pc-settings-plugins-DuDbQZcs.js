import { J as x, K as w, _ as i, c as p, L as d, M as $, N as f, i as v, t as _, p as E, r as g, a as z, h as R, b as s, x as o, O as D, A as P, E as C, P as k, Q as O, F as T, R as F } from "./index-Bs6A-haP.js";
import "./filled-button-DK7nEDMp.js";
import "./pc-button-menu-BrK2NJOx.js";
import "./pc-circular-progress-CXHtR8Ql.js";
import { s as L } from "./styles-BLMRQn28.js";
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const q = x(w);
class c extends q {
  constructor() {
    super(...arguments), this.size = "medium", this.label = "", this.lowered = !1;
  }
  render() {
    const { ariaLabel: a } = this;
    return d`
      <button
        class="fab ${$(this.getRenderClasses())}"
        aria-label=${a || f}>
        <md-elevation part="elevation"></md-elevation>
        <md-focus-ring part="focus-ring"></md-focus-ring>
        <md-ripple class="ripple"></md-ripple>
        ${this.renderTouchTarget()} ${this.renderIcon()} ${this.renderLabel()}
      </button>
    `;
  }
  getRenderClasses() {
    const a = !!this.label;
    return {
      lowered: this.lowered,
      small: this.size === "small" && !a,
      large: this.size === "large" && !a,
      extended: a
    };
  }
  renderTouchTarget() {
    return d`<div class="touch-target"></div>`;
  }
  renderLabel() {
    return this.label ? d`<span class="label">${this.label}</span>` : "";
  }
  renderIcon() {
    const { ariaLabel: a } = this;
    return d`<span class="icon">
      <slot
        name="icon"
        aria-hidden=${a || this.label ? "true" : f}>
        <span></span>
      </slot>
    </span>`;
  }
}
c.shadowRootOptions = {
  mode: "open",
  delegatesFocus: !0
};
i([
  p({ reflect: !0 })
], c.prototype, "size", void 0);
i([
  p()
], c.prototype, "label", void 0);
i([
  p({ type: Boolean })
], c.prototype, "lowered", void 0);
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
class u extends c {
  constructor() {
    super(...arguments), this.variant = "surface";
  }
  getRenderClasses() {
    return {
      ...super.getRenderClasses(),
      primary: this.variant === "primary",
      secondary: this.variant === "secondary",
      tertiary: this.variant === "tertiary"
    };
  }
}
i([
  p()
], u.prototype, "variant", void 0);
/**
 * @license
 * Copyright 2024 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const A = v`:host{--_container-color: var(--md-fab-container-color, var(--md-sys-color-surface-container-high, #ece6f0));--_container-elevation: var(--md-fab-container-elevation, 3);--_container-height: var(--md-fab-container-height, 56px);--_container-shadow-color: var(--md-fab-container-shadow-color, var(--md-sys-color-shadow, #000));--_container-width: var(--md-fab-container-width, 56px);--_focus-container-elevation: var(--md-fab-focus-container-elevation, 3);--_focus-icon-color: var(--md-fab-focus-icon-color, var(--md-sys-color-primary, #6750a4));--_hover-container-elevation: var(--md-fab-hover-container-elevation, 4);--_hover-icon-color: var(--md-fab-hover-icon-color, var(--md-sys-color-primary, #6750a4));--_hover-state-layer-color: var(--md-fab-hover-state-layer-color, var(--md-sys-color-primary, #6750a4));--_hover-state-layer-opacity: var(--md-fab-hover-state-layer-opacity, 0.08);--_icon-color: var(--md-fab-icon-color, var(--md-sys-color-primary, #6750a4));--_icon-size: var(--md-fab-icon-size, 24px);--_lowered-container-color: var(--md-fab-lowered-container-color, var(--md-sys-color-surface-container-low, #f7f2fa));--_lowered-container-elevation: var(--md-fab-lowered-container-elevation, 1);--_lowered-focus-container-elevation: var(--md-fab-lowered-focus-container-elevation, 1);--_lowered-hover-container-elevation: var(--md-fab-lowered-hover-container-elevation, 2);--_lowered-pressed-container-elevation: var(--md-fab-lowered-pressed-container-elevation, 1);--_pressed-container-elevation: var(--md-fab-pressed-container-elevation, 3);--_pressed-icon-color: var(--md-fab-pressed-icon-color, var(--md-sys-color-primary, #6750a4));--_pressed-state-layer-color: var(--md-fab-pressed-state-layer-color, var(--md-sys-color-primary, #6750a4));--_pressed-state-layer-opacity: var(--md-fab-pressed-state-layer-opacity, 0.12);--_focus-label-text-color: var(--md-fab-focus-label-text-color, var(--md-sys-color-primary, #6750a4));--_hover-label-text-color: var(--md-fab-hover-label-text-color, var(--md-sys-color-primary, #6750a4));--_label-text-color: var(--md-fab-label-text-color, var(--md-sys-color-primary, #6750a4));--_label-text-font: var(--md-fab-label-text-font, var(--md-sys-typescale-label-large-font, var(--md-ref-typeface-plain, Roboto)));--_label-text-line-height: var(--md-fab-label-text-line-height, var(--md-sys-typescale-label-large-line-height, 1.25rem));--_label-text-size: var(--md-fab-label-text-size, var(--md-sys-typescale-label-large-size, 0.875rem));--_label-text-weight: var(--md-fab-label-text-weight, var(--md-sys-typescale-label-large-weight, var(--md-ref-typeface-weight-medium, 500)));--_large-container-height: var(--md-fab-large-container-height, 96px);--_large-container-width: var(--md-fab-large-container-width, 96px);--_large-icon-size: var(--md-fab-large-icon-size, 36px);--_pressed-label-text-color: var(--md-fab-pressed-label-text-color, var(--md-sys-color-primary, #6750a4));--_primary-container-color: var(--md-fab-primary-container-color, var(--md-sys-color-primary-container, #eaddff));--_primary-focus-icon-color: var(--md-fab-primary-focus-icon-color, var(--md-sys-color-on-primary-container, #21005d));--_primary-focus-label-text-color: var(--md-fab-primary-focus-label-text-color, var(--md-sys-color-on-primary-container, #21005d));--_primary-hover-icon-color: var(--md-fab-primary-hover-icon-color, var(--md-sys-color-on-primary-container, #21005d));--_primary-hover-label-text-color: var(--md-fab-primary-hover-label-text-color, var(--md-sys-color-on-primary-container, #21005d));--_primary-hover-state-layer-color: var(--md-fab-primary-hover-state-layer-color, var(--md-sys-color-on-primary-container, #21005d));--_primary-icon-color: var(--md-fab-primary-icon-color, var(--md-sys-color-on-primary-container, #21005d));--_primary-label-text-color: var(--md-fab-primary-label-text-color, var(--md-sys-color-on-primary-container, #21005d));--_primary-pressed-icon-color: var(--md-fab-primary-pressed-icon-color, var(--md-sys-color-on-primary-container, #21005d));--_primary-pressed-label-text-color: var(--md-fab-primary-pressed-label-text-color, var(--md-sys-color-on-primary-container, #21005d));--_primary-pressed-state-layer-color: var(--md-fab-primary-pressed-state-layer-color, var(--md-sys-color-on-primary-container, #21005d));--_secondary-container-color: var(--md-fab-secondary-container-color, var(--md-sys-color-secondary-container, #e8def8));--_secondary-focus-icon-color: var(--md-fab-secondary-focus-icon-color, var(--md-sys-color-on-secondary-container, #1d192b));--_secondary-focus-label-text-color: var(--md-fab-secondary-focus-label-text-color, var(--md-sys-color-on-secondary-container, #1d192b));--_secondary-hover-icon-color: var(--md-fab-secondary-hover-icon-color, var(--md-sys-color-on-secondary-container, #1d192b));--_secondary-hover-label-text-color: var(--md-fab-secondary-hover-label-text-color, var(--md-sys-color-on-secondary-container, #1d192b));--_secondary-hover-state-layer-color: var(--md-fab-secondary-hover-state-layer-color, var(--md-sys-color-on-secondary-container, #1d192b));--_secondary-icon-color: var(--md-fab-secondary-icon-color, var(--md-sys-color-on-secondary-container, #1d192b));--_secondary-label-text-color: var(--md-fab-secondary-label-text-color, var(--md-sys-color-on-secondary-container, #1d192b));--_secondary-pressed-icon-color: var(--md-fab-secondary-pressed-icon-color, var(--md-sys-color-on-secondary-container, #1d192b));--_secondary-pressed-label-text-color: var(--md-fab-secondary-pressed-label-text-color, var(--md-sys-color-on-secondary-container, #1d192b));--_secondary-pressed-state-layer-color: var(--md-fab-secondary-pressed-state-layer-color, var(--md-sys-color-on-secondary-container, #1d192b));--_small-container-height: var(--md-fab-small-container-height, 40px);--_small-container-width: var(--md-fab-small-container-width, 40px);--_small-icon-size: var(--md-fab-small-icon-size, 24px);--_tertiary-container-color: var(--md-fab-tertiary-container-color, var(--md-sys-color-tertiary-container, #ffd8e4));--_tertiary-focus-icon-color: var(--md-fab-tertiary-focus-icon-color, var(--md-sys-color-on-tertiary-container, #31111d));--_tertiary-focus-label-text-color: var(--md-fab-tertiary-focus-label-text-color, var(--md-sys-color-on-tertiary-container, #31111d));--_tertiary-hover-icon-color: var(--md-fab-tertiary-hover-icon-color, var(--md-sys-color-on-tertiary-container, #31111d));--_tertiary-hover-label-text-color: var(--md-fab-tertiary-hover-label-text-color, var(--md-sys-color-on-tertiary-container, #31111d));--_tertiary-hover-state-layer-color: var(--md-fab-tertiary-hover-state-layer-color, var(--md-sys-color-on-tertiary-container, #31111d));--_tertiary-icon-color: var(--md-fab-tertiary-icon-color, var(--md-sys-color-on-tertiary-container, #31111d));--_tertiary-label-text-color: var(--md-fab-tertiary-label-text-color, var(--md-sys-color-on-tertiary-container, #31111d));--_tertiary-pressed-icon-color: var(--md-fab-tertiary-pressed-icon-color, var(--md-sys-color-on-tertiary-container, #31111d));--_tertiary-pressed-label-text-color: var(--md-fab-tertiary-pressed-label-text-color, var(--md-sys-color-on-tertiary-container, #31111d));--_tertiary-pressed-state-layer-color: var(--md-fab-tertiary-pressed-state-layer-color, var(--md-sys-color-on-tertiary-container, #31111d));--_container-shape-start-start: var(--md-fab-container-shape-start-start, var(--md-fab-container-shape, var(--md-sys-shape-corner-large, 16px)));--_container-shape-start-end: var(--md-fab-container-shape-start-end, var(--md-fab-container-shape, var(--md-sys-shape-corner-large, 16px)));--_container-shape-end-end: var(--md-fab-container-shape-end-end, var(--md-fab-container-shape, var(--md-sys-shape-corner-large, 16px)));--_container-shape-end-start: var(--md-fab-container-shape-end-start, var(--md-fab-container-shape, var(--md-sys-shape-corner-large, 16px)));--_large-container-shape-start-start: var(--md-fab-large-container-shape-start-start, var(--md-fab-large-container-shape, var(--md-sys-shape-corner-extra-large, 28px)));--_large-container-shape-start-end: var(--md-fab-large-container-shape-start-end, var(--md-fab-large-container-shape, var(--md-sys-shape-corner-extra-large, 28px)));--_large-container-shape-end-end: var(--md-fab-large-container-shape-end-end, var(--md-fab-large-container-shape, var(--md-sys-shape-corner-extra-large, 28px)));--_large-container-shape-end-start: var(--md-fab-large-container-shape-end-start, var(--md-fab-large-container-shape, var(--md-sys-shape-corner-extra-large, 28px)));--_small-container-shape-start-start: var(--md-fab-small-container-shape-start-start, var(--md-fab-small-container-shape, var(--md-sys-shape-corner-medium, 12px)));--_small-container-shape-start-end: var(--md-fab-small-container-shape-start-end, var(--md-fab-small-container-shape, var(--md-sys-shape-corner-medium, 12px)));--_small-container-shape-end-end: var(--md-fab-small-container-shape-end-end, var(--md-fab-small-container-shape, var(--md-sys-shape-corner-medium, 12px)));--_small-container-shape-end-start: var(--md-fab-small-container-shape-end-start, var(--md-fab-small-container-shape, var(--md-sys-shape-corner-medium, 12px)));cursor:pointer}:host([size=small][touch-target=wrapper]){margin:max(0px,48px - var(--_small-container-height))}.fab{cursor:inherit}.fab .icon ::slotted(*){color:var(--_icon-color)}.fab:focus{color:var(--_focus-icon-color)}.fab:hover{color:var(--_hover-icon-color)}.fab:active{color:var(--_pressed-icon-color)}.fab.primary{background-color:var(--_primary-container-color);--md-ripple-hover-color: var(--_primary-hover-state-layer-color);--md-ripple-pressed-color: var(--_primary-pressed-state-layer-color)}.fab.primary .icon ::slotted(*){color:var(--_primary-icon-color)}.fab.primary:focus{color:var(--_primary-focus-icon-color)}.fab.primary:hover{color:var(--_primary-hover-icon-color)}.fab.primary:active{color:var(--_primary-pressed-icon-color)}.fab.primary .label{color:var(--_primary-label-text-color)}.fab:hover .fab.primary .label{color:var(--_primary-hover-label-text-color)}.fab:focus .fab.primary .label{color:var(--_primary-focus-label-text-color)}.fab:active .fab.primary .label{color:var(--_primary-pressed-label-text-color)}.fab.secondary{background-color:var(--_secondary-container-color);--md-ripple-hover-color: var(--_secondary-hover-state-layer-color);--md-ripple-pressed-color: var(--_secondary-pressed-state-layer-color)}.fab.secondary .icon ::slotted(*){color:var(--_secondary-icon-color)}.fab.secondary:focus{color:var(--_secondary-focus-icon-color)}.fab.secondary:hover{color:var(--_secondary-hover-icon-color)}.fab.secondary:active{color:var(--_secondary-pressed-icon-color)}.fab.secondary .label{color:var(--_secondary-label-text-color)}.fab:hover .fab.secondary .label{color:var(--_secondary-hover-label-text-color)}.fab:focus .fab.secondary .label{color:var(--_secondary-focus-label-text-color)}.fab:active .fab.secondary .label{color:var(--_secondary-pressed-label-text-color)}.fab.tertiary{background-color:var(--_tertiary-container-color);--md-ripple-hover-color: var(--_tertiary-hover-state-layer-color);--md-ripple-pressed-color: var(--_tertiary-pressed-state-layer-color)}.fab.tertiary .icon ::slotted(*){color:var(--_tertiary-icon-color)}.fab.tertiary:focus{color:var(--_tertiary-focus-icon-color)}.fab.tertiary:hover{color:var(--_tertiary-hover-icon-color)}.fab.tertiary:active{color:var(--_tertiary-pressed-icon-color)}.fab.tertiary .label{color:var(--_tertiary-label-text-color)}.fab:hover .fab.tertiary .label{color:var(--_tertiary-hover-label-text-color)}.fab:focus .fab.tertiary .label{color:var(--_tertiary-focus-label-text-color)}.fab:active .fab.tertiary .label{color:var(--_tertiary-pressed-label-text-color)}.fab.extended slot span{padding-inline-start:4px}.fab.small{width:var(--_small-container-width);height:var(--_small-container-height)}.fab.small .icon ::slotted(*){width:var(--_small-icon-size);height:var(--_small-icon-size);font-size:var(--_small-icon-size)}.fab.small,.fab.small .ripple{border-start-start-radius:var(--_small-container-shape-start-start);border-start-end-radius:var(--_small-container-shape-start-end);border-end-start-radius:var(--_small-container-shape-end-start);border-end-end-radius:var(--_small-container-shape-end-end)}.fab.small md-focus-ring{--md-focus-ring-shape-start-start: var(--_small-container-shape-start-start);--md-focus-ring-shape-start-end: var(--_small-container-shape-start-end);--md-focus-ring-shape-end-end: var(--_small-container-shape-end-end);--md-focus-ring-shape-end-start: var(--_small-container-shape-end-start)}
`;
/**
 * @license
 * Copyright 2024 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const S = v`@media(forced-colors: active){.fab{border:1px solid ButtonText}.fab.extended{padding-inline-start:15px;padding-inline-end:19px}md-focus-ring{--md-focus-ring-outward-offset: 3px}}
`;
/**
 * @license
 * Copyright 2024 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const j = v`:host{--md-ripple-hover-opacity: var(--_hover-state-layer-opacity);--md-ripple-pressed-opacity: var(--_pressed-state-layer-opacity);display:inline-flex;-webkit-tap-highlight-color:rgba(0,0,0,0)}:host([size=medium][touch-target=wrapper]){margin:max(0px,48px - var(--_container-height))}:host([size=large][touch-target=wrapper]){margin:max(0px,48px - var(--_large-container-height))}.fab,.icon,.icon ::slotted(*){display:flex}.fab{align-items:center;justify-content:center;vertical-align:middle;padding:0;position:relative;height:var(--_container-height);transition-property:background-color;border-width:0px;outline:none;z-index:0;text-transform:inherit;--md-elevation-level: var(--_container-elevation);--md-elevation-shadow-color: var(--_container-shadow-color);background-color:var(--_container-color);--md-ripple-hover-color: var(--_hover-state-layer-color);--md-ripple-pressed-color: var(--_pressed-state-layer-color)}.fab.extended{width:inherit;box-sizing:border-box;padding-inline-start:16px;padding-inline-end:20px}.fab:not(.extended){width:var(--_container-width)}.fab.large{width:var(--_large-container-width);height:var(--_large-container-height)}.fab.large .icon ::slotted(*){width:var(--_large-icon-size);height:var(--_large-icon-size);font-size:var(--_large-icon-size)}.fab.large,.fab.large .ripple{border-start-start-radius:var(--_large-container-shape-start-start);border-start-end-radius:var(--_large-container-shape-start-end);border-end-start-radius:var(--_large-container-shape-end-start);border-end-end-radius:var(--_large-container-shape-end-end)}.fab.large md-focus-ring{--md-focus-ring-shape-start-start: var(--_large-container-shape-start-start);--md-focus-ring-shape-start-end: var(--_large-container-shape-start-end);--md-focus-ring-shape-end-end: var(--_large-container-shape-end-end);--md-focus-ring-shape-end-start: var(--_large-container-shape-end-start)}.fab:focus{--md-elevation-level: var(--_focus-container-elevation)}.fab:hover{--md-elevation-level: var(--_hover-container-elevation)}.fab:active{--md-elevation-level: var(--_pressed-container-elevation)}.fab.lowered{background-color:var(--_lowered-container-color);--md-elevation-level: var(--_lowered-container-elevation)}.fab.lowered:focus{--md-elevation-level: var(--_lowered-focus-container-elevation)}.fab.lowered:hover{--md-elevation-level: var(--_lowered-hover-container-elevation)}.fab.lowered:active{--md-elevation-level: var(--_lowered-pressed-container-elevation)}.fab .label{color:var(--_label-text-color)}.fab:hover .fab .label{color:var(--_hover-label-text-color)}.fab:focus .fab .label{color:var(--_focus-label-text-color)}.fab:active .fab .label{color:var(--_pressed-label-text-color)}.label{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-family:var(--_label-text-font);font-size:var(--_label-text-size);line-height:var(--_label-text-line-height);font-weight:var(--_label-text-weight)}.fab.extended .icon ::slotted(*){margin-inline-end:12px}.ripple{overflow:hidden}.ripple,md-elevation{z-index:-1}.touch-target{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}:host([touch-target=none]) .touch-target{display:none}md-elevation,.fab{transition-duration:280ms;transition-timing-function:cubic-bezier(0.2, 0, 0, 1)}.fab,.ripple{border-start-start-radius:var(--_container-shape-start-start);border-start-end-radius:var(--_container-shape-start-end);border-end-start-radius:var(--_container-shape-end-start);border-end-end-radius:var(--_container-shape-end-end)}md-focus-ring{--md-focus-ring-shape-start-start: var(--_container-shape-start-start);--md-focus-ring-shape-start-end: var(--_container-shape-start-end);--md-focus-ring-shape-end-end: var(--_container-shape-end-end);--md-focus-ring-shape-end-start: var(--_container-shape-end-start)}.icon ::slotted(*){width:var(--_icon-size);height:var(--_icon-size);font-size:var(--_icon-size)}
`;
/**
 * @license
 * Copyright 2022 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
let h = class extends u {
};
h.styles = [j, A, S];
h = i([
  _("md-fab")
], h);
var B = Object.defineProperty, M = Object.getOwnPropertyDescriptor, y = (r, a, e, t) => {
  for (var n = t > 1 ? void 0 : t ? M(a, e) : a, m = r.length - 1, b; m >= 0; m--)
    (b = r[m]) && (n = (t ? b(a, e, n) : b(n)) || n);
  return t && n && B(a, e, n), n;
};
let l = class extends z {
  constructor() {
    super(...arguments), this._fetchData = new R(
      this,
      async () => {
        await s.getRequest("/config/plugin_entries").then((r) => {
          this._pluginEntries = r.data.result;
        });
      },
      () => []
    );
  }
  connectedCallback() {
    super.connectedCallback(), this.addEventListener(
      "flow-updated",
      (r) => this._updateEntries(r)
    );
  }
  async _updateEntries(r) {
    this._reloadingEntry = r.detail.data.handler, await s.getRequest("/config/plugin_entries").then((a) => {
      this._pluginEntries = a.data.result;
    }).finally(() => {
      this._reloadingEntry = void 0;
    });
  }
  render() {
    return o`
      ${this._fetchData.render({
      complete: () => this._renderEntries()
    })}
      <div id="fab">
        <md-fab label="Add Plugin" @click=${this._showPlugins}
          ><pc-svg-icon slot="icon" .path=${D}></pc-svg-icon
        ></md-fab>
      </div>
    `;
  }
  _renderEntries() {
    return this._pluginEntries ? o` <div class="root">
          ${Object.entries(this._pluginEntries).map(
      ([r, a]) => o`<pc-card
                outlined
                header=${r.toUpperCase().replaceAll("_", " ")}
              >
                <div class="card-content">
                  <md-list>
                    ${a.map(
        (e) => o`<md-list-item
                          class="plugin_entry ${P({
          "state-setup-error": e.state === "setup_error",
          "state-not-loaded": e.state === "not_loaded" || e.disabled_by === "user",
          "state-setup": e.entry_id === this._reloadingEntry
        })}"
                          data-entry-id=${e.entry_id}
                          .pluginEntry=${e}
                        >
                          ${e.title}
                          ${e.ws !== null ? o`<div slot="supporting-text">
                                Related to (${e.ws})
                              </div>` : ""}
                          ${e.entry_id === this._reloadingEntry ? o`<pc-circular-progress
                                slot="end"
                                indeterminate
                              ></pc-circular-progress>` : e.disabled_by === "user" ? o`<md-filled-button
                                  id="action-btn"
                                  unelevated
                                  slot="end"
                                  @click=${this._handleEnable}
                                  >ENABLE
                                </md-filled-button>` : e.supports_options && e.state === "loaded" ? o`<md-text-button
                                    id="action-btn"
                                    slot="end"
                                    @click=${this._showOptions}
                                    >CONFIGURE
                                  </md-text-button>` : ""}
                          ${e.reason ? o`<div class="message" slot="end">
                                ${e.reason}
                              </div>` : ""}
                          <pc-button-menu slot="end">
                            <pc-icon-button
                              slot="trigger"
                              label="Menu"
                              .path=${C}
                            ></pc-icon-button>
                            ${e.disabled_by ? "" : o`<md-menu-item
                                  @close-menu=${this._handleReload}
                                >
                                  <div slot="headline">Reload</div>
                                  <pc-svg-icon
                                    slot="start"
                                    .path=${k}
                                  ></pc-svg-icon>
                                </md-menu-item>`}
                            ${e.disabled_by === "user" ? o`<md-menu-item
                                  @close-menu=${this._handleEnable}
                                >
                                  <div slot="headline">Enable</div>
                                  <pc-svg-icon
                                    slot="start"
                                    .path=${O}
                                  ></pc-svg-icon>
                                </md-menu-item>` : e.disabled_by === null ? o`<md-menu-item
                                    @close-menu=${this._handleDisable}
                                  >
                                    <div slot="headline">Disable</div>
                                    <pc-svg-icon
                                      slot="start"
                                      class="warning"
                                      .path=${T}
                                    ></pc-svg-icon>
                                  </md-menu-item>` : ""}
                            <md-menu-item @close-menu=${this._handleDelete}>
                              <div slot="headline">Delete</div>
                              <pc-svg-icon
                                slot="start"
                                class="warning"
                                .path=${F}
                              ></pc-svg-icon>
                            </md-menu-item>
                          </pc-button-menu>
                        </md-list-item>`
      )}
                  </md-list>
                </div>
              </pc-card>`
    )}
        </div>` : o`<pc-alert
          alert-type="info"
          header="No plugins configured. Try to add a plugin"
        ></pc-alert>`;
  }
  _handleEnable(r) {
    this._enableDisablePlugin(
      r.target.closest(".plugin_entry").pluginEntry,
      !1
    );
  }
  _handleDisable(r) {
    this._enableDisablePlugin(
      r.target.closest(".plugin_entry").pluginEntry,
      !0
    );
  }
  _handleDelete(r) {
    this._deletePlugin(
      r.target.closest(".plugin_entry").pluginEntry
    );
  }
  async _handleReload(r) {
    await this._reloadPlugin(
      r.target.closest(".plugin_entry").pluginEntry
    );
  }
  async _enableDisablePlugin(r, a) {
    this._reloadingEntry = r.entry_id, await s.postRequest(
      `/config/plugin_entries/${r.entry_id}`,
      {
        action: "disable",
        user_input: {
          disabled_by: a ? "user" : null
        }
      }
    ), this._reloadingEntry = void 0, await this._fetchData.run();
  }
  async _deletePlugin(r) {
    await s.postRequest(
      `/config/plugin_entries/${r.entry_id}`,
      {
        action: "delete"
      }
    ), await this._fetchData.run();
  }
  async _reloadPlugin(r) {
    this._reloadingEntry = r.entry_id, await s.postRequest(
      `/config/plugin_entries/${r.entry_id}`,
      {
        action: "reload"
      }
    ), this._reloadingEntry = void 0, await this._fetchData.run();
  }
  _showOptions(r) {
    const a = r.target.closest(".plugin_entry").pluginEntry;
    import("./dialog-data-entry-flow-BnPHFKR5.js").then(() => {
      var t;
      const e = document.createElement("dialog-data-entry-flow");
      e.handler = a.entry_id, e.domain = a.domain, e.flowType = "options", (t = this.shadowRoot) == null || t.appendChild(e);
    });
  }
  _showPlugins() {
    import("./pc-add-plugin-jKg84UC3.js").then(() => {
      var a;
      const r = document.createElement("pc-add-plugin");
      (a = this.shadowRoot) == null || a.appendChild(r);
    });
  }
};
l.styles = [
  E,
  L,
  v`
      .state-setup-error {
        --md-list-item-label-text-color: var(--error-color);
        --text-on-state-color: var(--text-primary-color);
      }
      .state-setup-error::after {
        background-color: var(--error-color);
      }
      .state-failed::after {
        background-color: var(--warning-color);
      }
      .state-not-loaded,
      .state-setup {
        --md-list-item-label-text-color: var(--disabled-text-color);
      }
      .message {
        font-weight: bold;
        align-items: center;
        max-width: 200px;
        font-size: 10px;
        margin-left: 8px;
        padding-top: 2px;
        padding-right: 2px;
        overflow-wrap: break-word;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 7;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .message pc-svg-icon {
        color: var(--md-list-item-label-text-color);
      }

      #fab {
        position: fixed;
        right: calc(24px + env(safe-area-inset-right));
        bottom: calc(60px + env(safe-area-inset-bottom));
        z-index: 1;
      }
    `
];
y([
  g()
], l.prototype, "_pluginEntries", 2);
y([
  g()
], l.prototype, "_reloadingEntry", 2);
l = y([
  _("pc-settings-plugins")
], l);
export {
  l as PluginSettings
};
