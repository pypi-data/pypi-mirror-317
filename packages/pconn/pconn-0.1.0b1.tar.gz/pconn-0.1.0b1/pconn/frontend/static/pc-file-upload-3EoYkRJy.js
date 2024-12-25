import { _ as v, c as t, L as _, i as h, t as b, r as x, l as k, a as $, x as c, A as w, ar as p, R as f, s as m } from "./index-Bs6A-haP.js";
import { o as g } from "./style-map-8seGJ4i8.js";
import { P as z } from "./progress-CmTEcoJs.js";
import { e as D } from "./ensure-array-ILKxE5fq.js";
import "./filled-button-DK7nEDMp.js";
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
class y extends z {
  constructor() {
    super(...arguments), this.buffer = 0;
  }
  // Note, the indeterminate animation is rendered with transform %'s
  // Previously, this was optimized to use px calculated with the resizeObserver
  // due to a now fixed Chrome bug: crbug.com/389359.
  renderIndicator() {
    const e = {
      transform: `scaleX(${(this.indeterminate ? 1 : this.value / this.max) * 100}%)`
    }, n = this.buffer ?? 0, s = n > 0, l = {
      transform: `scaleX(${(this.indeterminate || !s ? 1 : n / this.max) * 100}%)`
    }, d = this.indeterminate || !s || n >= this.max || this.value >= this.max;
    return _`
      <div class="dots" ?hidden=${d}></div>
      <div class="inactive-track" style=${g(l)}></div>
      <div class="bar primary-bar" style=${g(e)}>
        <div class="bar-inner"></div>
      </div>
      <div class="bar secondary-bar">
        <div class="bar-inner"></div>
      </div>
    `;
  }
}
v([
  t({ type: Number })
], y.prototype, "buffer", void 0);
/**
 * @license
 * Copyright 2024 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const P = h`:host{--_active-indicator-color: var(--md-linear-progress-active-indicator-color, var(--md-sys-color-primary, #6750a4));--_active-indicator-height: var(--md-linear-progress-active-indicator-height, 4px);--_four-color-active-indicator-four-color: var(--md-linear-progress-four-color-active-indicator-four-color, var(--md-sys-color-tertiary-container, #ffd8e4));--_four-color-active-indicator-one-color: var(--md-linear-progress-four-color-active-indicator-one-color, var(--md-sys-color-primary, #6750a4));--_four-color-active-indicator-three-color: var(--md-linear-progress-four-color-active-indicator-three-color, var(--md-sys-color-tertiary, #7d5260));--_four-color-active-indicator-two-color: var(--md-linear-progress-four-color-active-indicator-two-color, var(--md-sys-color-primary-container, #eaddff));--_track-color: var(--md-linear-progress-track-color, var(--md-sys-color-surface-container-highest, #e6e0e9));--_track-height: var(--md-linear-progress-track-height, 4px);--_track-shape: var(--md-linear-progress-track-shape, var(--md-sys-shape-corner-none, 0px));border-radius:var(--_track-shape);display:flex;position:relative;min-width:80px;height:var(--_track-height);content-visibility:auto;contain:strict}.progress,.dots,.inactive-track,.bar,.bar-inner{position:absolute}.progress{direction:ltr;inset:0;border-radius:inherit;overflow:hidden;display:flex;align-items:center}.bar{animation:none;width:100%;height:var(--_active-indicator-height);transform-origin:left center;transition:transform 250ms cubic-bezier(0.4, 0, 0.6, 1)}.secondary-bar{display:none}.bar-inner{inset:0;animation:none;background:var(--_active-indicator-color)}.inactive-track{background:var(--_track-color);inset:0;transition:transform 250ms cubic-bezier(0.4, 0, 0.6, 1);transform-origin:left center}.dots{inset:0;animation:linear infinite 250ms;animation-name:buffering;background-color:var(--_track-color);background-repeat:repeat-x;-webkit-mask-image:url("data:image/svg+xml,%3Csvg version='1.1' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 5 2' preserveAspectRatio='xMinYMin slice'%3E%3Ccircle cx='1' cy='1' r='1'/%3E%3C/svg%3E");mask-image:url("data:image/svg+xml,%3Csvg version='1.1' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 5 2' preserveAspectRatio='xMinYMin slice'%3E%3Ccircle cx='1' cy='1' r='1'/%3E%3C/svg%3E");z-index:-1}.dots[hidden]{display:none}.indeterminate .bar{transition:none}.indeterminate .primary-bar{inset-inline-start:-145.167%}.indeterminate .secondary-bar{inset-inline-start:-54.8889%;display:block}.indeterminate .primary-bar{animation:linear infinite 2s;animation-name:primary-indeterminate-translate}.indeterminate .primary-bar>.bar-inner{animation:linear infinite 2s primary-indeterminate-scale}.indeterminate.four-color .primary-bar>.bar-inner{animation-name:primary-indeterminate-scale,four-color;animation-duration:2s,4s}.indeterminate .secondary-bar{animation:linear infinite 2s;animation-name:secondary-indeterminate-translate}.indeterminate .secondary-bar>.bar-inner{animation:linear infinite 2s secondary-indeterminate-scale}.indeterminate.four-color .secondary-bar>.bar-inner{animation-name:secondary-indeterminate-scale,four-color;animation-duration:2s,4s}:host(:dir(rtl)){transform:scale(-1)}@keyframes primary-indeterminate-scale{0%{transform:scaleX(0.08)}36.65%{animation-timing-function:cubic-bezier(0.334731, 0.12482, 0.785844, 1);transform:scaleX(0.08)}69.15%{animation-timing-function:cubic-bezier(0.06, 0.11, 0.6, 1);transform:scaleX(0.661479)}100%{transform:scaleX(0.08)}}@keyframes secondary-indeterminate-scale{0%{animation-timing-function:cubic-bezier(0.205028, 0.057051, 0.57661, 0.453971);transform:scaleX(0.08)}19.15%{animation-timing-function:cubic-bezier(0.152313, 0.196432, 0.648374, 1.00432);transform:scaleX(0.457104)}44.15%{animation-timing-function:cubic-bezier(0.257759, -0.003163, 0.211762, 1.38179);transform:scaleX(0.72796)}100%{transform:scaleX(0.08)}}@keyframes buffering{0%{transform:translateX(calc(var(--_track-height) / 2 * 5))}}@keyframes primary-indeterminate-translate{0%{transform:translateX(0px)}20%{animation-timing-function:cubic-bezier(0.5, 0, 0.701732, 0.495819);transform:translateX(0px)}59.15%{animation-timing-function:cubic-bezier(0.302435, 0.381352, 0.55, 0.956352);transform:translateX(83.6714%)}100%{transform:translateX(200.611%)}}@keyframes secondary-indeterminate-translate{0%{animation-timing-function:cubic-bezier(0.15, 0, 0.515058, 0.409685);transform:translateX(0px)}25%{animation-timing-function:cubic-bezier(0.31033, 0.284058, 0.8, 0.733712);transform:translateX(37.6519%)}48.35%{animation-timing-function:cubic-bezier(0.4, 0.627035, 0.6, 0.902026);transform:translateX(84.3862%)}100%{transform:translateX(160.278%)}}@keyframes four-color{0%{background:var(--_four-color-active-indicator-one-color)}15%{background:var(--_four-color-active-indicator-one-color)}25%{background:var(--_four-color-active-indicator-two-color)}40%{background:var(--_four-color-active-indicator-two-color)}50%{background:var(--_four-color-active-indicator-three-color)}65%{background:var(--_four-color-active-indicator-three-color)}75%{background:var(--_four-color-active-indicator-four-color)}90%{background:var(--_four-color-active-indicator-four-color)}100%{background:var(--_four-color-active-indicator-one-color)}}@media(forced-colors: active){:host{outline:1px solid CanvasText}.bar-inner,.dots{background-color:CanvasText}}
`;
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
let u = class extends y {
};
u.styles = [P];
u = v([
  b("md-linear-progress")
], u);
const X = (r = 0, e = 2) => {
  if (r === 0)
    return "0 Bytes";
  const n = 1024;
  e = e < 0 ? 0 : e;
  const s = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"], o = Math.floor(Math.log(r) / Math.log(n));
  return `${parseFloat((r / n ** o).toFixed(e))} ${s[o]}`;
};
var B = Object.defineProperty, F = Object.getOwnPropertyDescriptor, a = (r, e, n, s) => {
  for (var o = s > 1 ? void 0 : s ? F(e, n) : e, l = r.length - 1, d; l >= 0; l--)
    (d = r[l]) && (o = (s ? d(e, n, o) : d(o)) || o);
  return s && o && B(e, n, o), o;
};
let i = class extends $ {
  constructor() {
    super(...arguments), this.multiple = !1, this.disabled = !1, this.uploading = !1, this.autoOpenFileDialog = !1, this._drag = !1;
  }
  firstUpdated(r) {
    super.firstUpdated(r), this.autoOpenFileDialog && this._openFilePicker();
  }
  render() {
    return c`
      ${this.uploading ? c`<div class="container">
            <div class="row">
              <span class="header">${this.value ?? "uploading"} ></span>
              ${this.progress ? c`<span class="progress">${this.progress}%</span>` : ""}
            </div>
            <md-linear-progress
              .indeterminate=${!this.progress}
              .progress=${this.progress ? this.progress / 100 : void 0}
            ></md-linear-progress>
          </div>` : c`<label
            for=${this.value ? "" : "input"}
            class="container ${w({
      dragged: this._drag,
      multiple: this.multiple,
      value: !!this.value
    })}"
            @drop=${this._handleDrop}
            @dragenter=${this._handleDragStart}
            @dragover=${this._handleDragStart}
            @dragleave=${this._handleDragEnd}
            @dragend=${this._handleDragEnd}
            >${this.value ? typeof this.value == "string" ? c`<div class="row">
                    <div class="value" @click=${this._openFilePicker}>
                      <pc-svg-icon
                        .path=${this.icon || p}
                      ></pc-svg-icon>
                      ${this.value}
                    </div>
                    <pc-icon-button
                      @click=${this._clearValue}
                      label="Delete"
                      .path=${f}
                    ></pc-icon-button>
                  </div>` : (this.value instanceof FileList ? Array.from(this.value) : D(this.value)).map(
      (r) => c`<div class="row">
                        <div class="value" @click=${this._openFilePicker}>
                          <pc-svg-icon
                            .path=${this.icon || p}
                          ></pc-svg-icon>
                          ${r.name} - ${X(r.size)}
                        </div>
                        <pc-icon-button
                          @click=${this._clearValue}
                          label="Delete"
                          .path=${f}
                        ></pc-icon-button>
                      </div>`
    ) : c`<pc-svg-icon
                    class="big-icon"
                    .path=${this.icon || p}
                  ></pc-svg-icon>
                  <md-filled-button unelevated @click=${this._openFilePicker}>
                    ${this.label}
                  </md-filled-button>
                  <span class="secondary">${this.secondary}</span>
                  <span class="supports">${this.supports}</span>`}
            <input
              id="input"
              type="file"
              class="file"
              .accept=${this.accept}
              .multiple=${this.multiple}
              @change=${this._handleFilePicked}
          /></label>`}
    `;
  }
  _openFilePicker() {
    var r;
    (r = this._input) == null || r.click();
  }
  _handleDrop(r) {
    var e;
    r.preventDefault(), r.stopPropagation(), (e = r.dataTransfer) != null && e.files && m(this, "file-picked", {
      files: this.multiple || r.dataTransfer.files.length === 1 ? Array.from(r.dataTransfer.files) : [r.dataTransfer.files[0]]
    }), this._drag = !1;
  }
  _handleDragStart(r) {
    r.preventDefault(), r.stopPropagation(), this._drag = !0;
  }
  _handleDragEnd(r) {
    r.preventDefault(), r.stopPropagation(), this._drag = !1;
  }
  _handleFilePicked(r) {
    var e;
    ((e = r.target.files) == null ? void 0 : e.length) !== 0 && (this.value = r.target.files, m(this, "file-picked", {
      files: Array.from(r.target.files)
    }));
  }
  _clearValue(r) {
    r.preventDefault(), this._input.value = "", this.value = void 0, m(this, "change");
  }
  static get styles() {
    return h`
      :host {
        display: block;
        height: 240px;
      }
      :host([disabled]) {
        pointer-events: none;
        color: var(--disabled-text-color);
      }
      .container {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: solid 1px rgba(0, 0, 0, 0.42);
        border-radius: var(--mdc-shape-small, 4px);
        height: 100%;
      }
      label.container {
        border: dashed 1px rgba(0, 0, 0, 0.42);
        cursor: pointer;
      }
      :host([disabled]) .container {
        border-color: var(--disabled-color);
      }
      label.dragged {
        border-color: var(--primary-color);
      }
      .dragged:before {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: var(--primary-color);
        content: "";
        opacity: var(--dark-divider-opacity);
        pointer-events: none;
        border-radius: var(--mdc-shape-small, 4px);
      }
      label.value {
        cursor: default;
      }
      label.value.multiple {
        justify-content: unset;
        overflow: auto;
      }
      .highlight {
        color: var(--primary-color);
      }
      .row {
        display: flex;
        width: 100%;
        align-items: center;
        justify-content: space-between;
        padding: 0 16px;
        box-sizing: border-box;
      }
      pc-button {
        margin-bottom: 4px;
      }
      .supports {
        color: var(--secondary-text-color);
        font-size: 12px;
      }
      :host([disabled]) .secondary {
        color: var(--disabled-text-color);
      }
      input.file {
        display: none;
      }
      .value {
        cursor: pointer;
      }
      .value pc-svg-icon {
        margin-right: 8px;
        margin-inline-end: 8px;
        margin-inline-start: initial;
      }
      .big-icon {
        --md-icon-button-icon-size: 48px;
        margin-bottom: 8px;
      }
      pc-button {
        --md-icon-button-outline-color: var(--primary-color);
        --md-icon-button-icon-size: 24px;
      }
      md-linear-progress {
        width: 100%;
        padding: 16px;
        box-sizing: border-box;
      }
      .header {
        font-weight: 500;
      }
      .progress {
        color: var(--secondary-text-color);
      }
    `;
  }
};
a([
  t()
], i.prototype, "accept", 2);
a([
  t()
], i.prototype, "icon", 2);
a([
  t()
], i.prototype, "label", 2);
a([
  t()
], i.prototype, "secondary", 2);
a([
  t()
], i.prototype, "supports", 2);
a([
  t({ type: Object })
], i.prototype, "value", 2);
a([
  t({ type: Boolean })
], i.prototype, "multiple", 2);
a([
  t({ type: Boolean, reflect: !0 })
], i.prototype, "disabled", 2);
a([
  t({ type: Boolean })
], i.prototype, "uploading", 2);
a([
  t({ type: Number })
], i.prototype, "progress", 2);
a([
  t({ type: Boolean, attribute: "auto-open-file-dialog" })
], i.prototype, "autoOpenFileDialog", 2);
a([
  x()
], i.prototype, "_drag", 2);
a([
  k("#input")
], i.prototype, "_input", 2);
i = a([
  b("pc-file-upload")
], i);
