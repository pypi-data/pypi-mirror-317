import { p as x, i as w, c as l, a as _, x as n, s as m, t as u, r as b, k as j, l as q, h as E, b as $, o as M } from "./index-Bs6A-haP.js";
import "./pc-form-CK-FZij5.js";
import { c as K } from "./styles-CmkOrDPY.js";
import "./pc-circular-progress-CXHtR8Ql.js";
var R = Object.defineProperty, A = Object.getOwnPropertyDescriptor, P = (s, t, i, o) => {
  for (var e = o > 1 ? void 0 : o ? A(t, i) : t, a = s.length - 1, r; a >= 0; a--)
    (r = s[a]) && (e = (o ? r(t, i, e) : r(e)) || e);
  return o && e && R(t, i, e), e;
};
let y = class extends _ {
  render() {
    return n` <h2>${this.translationKeys.title}</h2>
      <div class="content">
        ${this.translationKeys[this.step.type][this.step.reason]}
      </div>
      <div class="buttons" slot="actions">
        <md-text-button @click=${this._flowDone}>CLOSE</md-text-button>
      </div>`;
  }
  _flowDone() {
    m(this, "flow-updated");
  }
};
y.styles = [
  x,
  K,
  w`
      .error {
        color: red;
      }

      .submit-spinner {
        margin-right: 16px;
      }
      pc-form {
        margin-top: 24px;
        display: block;
      }
      h2 {
        word-break: break-word;
        padding-inline-end: 72px;
        direction: var(--direction);
      }
    `
];
P([
  l({ attribute: !1 })
], y.prototype, "step", 2);
P([
  l({ attribute: !1 })
], y.prototype, "translationKeys", 2);
y = P([
  u("step-flow-abort")
], y);
var I = Object.defineProperty, L = Object.getOwnPropertyDescriptor, O = (s, t, i, o) => {
  for (var e = o > 1 ? void 0 : o ? L(t, i) : t, a = s.length - 1, r; a >= 0; a--)
    (r = s[a]) && (e = (o ? r(t, i, e) : r(e)) || e);
  return o && e && I(t, i, e), e;
};
let g = class extends _ {
  render() {
    return n` <h2>${this.translationKeys.title}</h2>
      <div class="content">
        ${this.translationKeys[this.step.type].description}
      </div>
      <div class="buttons" slot="actions">
        <md-text-button @click=${this._flowDone}>CLOSE</md-text-button>
      </div>`;
  }
  _flowDone() {
    m(this, "flow-updated", {
      data: {
        handler: this.step.handler
      }
    });
  }
};
g.styles = [
  x,
  K,
  w`
      .error {
        color: red;
      }

      .submit-spinner {
        margin-right: 16px;
      }
      pc-form {
        margin-top: 24px;
        display: block;
      }
      h2 {
        word-break: break-word;
        padding-inline-end: 72px;
        direction: var(--direction);
      }
    `
];
O([
  l({ attribute: !1 })
], g.prototype, "step", 2);
O([
  l({ attribute: !1 })
], g.prototype, "translationKeys", 2);
g = O([
  u("step-flow-create-entry")
], g);
const B = (s) => {
  const t = {};
  return s.forEach((i) => {
    var o, e;
    ((o = i.description) == null ? void 0 : o.suggested_value) !== void 0 && ((e = i.description) == null ? void 0 : e.suggested_value) !== null ? t[i.name] = i.description.suggested_value : "default" in i && i.default !== null && (t[i.name] = i.default);
  }), t;
}, T = (s, t) => {
  const i = {};
  return Object.entries(s).forEach(([o, e]) => {
    if (typeof e == "object" && !Array.isArray(e))
      i[o] = T(e, t);
    else {
      const a = /\{([^}]+)\}/g, r = e.matchAll(a);
      r && Array.from(r).forEach((S) => {
        const C = S[1];
        C in t && (e = e.replace(S[0], t[C]));
      }), i[o] = e;
    }
  }), i;
};
var H = Object.defineProperty, z = Object.getOwnPropertyDescriptor, h = (s, t, i, o) => {
  for (var e = o > 1 ? void 0 : o ? z(t, i) : t, a = s.length - 1, r; a >= 0; a--)
    (r = s[a]) && (e = (o ? r(t, i, e) : r(e)) || e);
  return o && e && H(t, i, e), e;
};
let d = class extends _ {
  constructor() {
    super(...arguments), this.loading = !1;
  }
  render() {
    const s = this._stepDataProcessed, t = this._stepTranslationKeys;
    return n` <h2>${this._renderHeader()}</h2>
      <div class="content">
        <p>${t.description}</p>
        ${this._errorMsg ? n`<pc-alert
              alert-type="error"
              .header=${this._errorMsg}
            ></pc-alert>` : ""}
        <pc-form
          .data=${s}
          .disabled=${this.loading}
          .error=${this.step.errors}
          @value-changed=${this._stepDataChanged}
          .schema=${this.step.data_schema}
          .labels=${t.data}
          .errorDescriptions=${this.translationKeys.error}
        >
        </pc-form>
      </div>
      <div class="buttons" slot="actions">
        ${this.loading ? n`<div class="submit-spinner">
              <pc-circular-progress indeterminate></pc-circular-progress>
            </div>` : n`<div>
              <md-text-button @click=${this._handleSubmit}
                >Submit
              </md-text-button>
            </div>`}
      </div>`;
  }
  _renderHeader() {
    return this.flowType === "config" ? "Setup " + this.translationKeys.title : this.flowType === "options" ? "Options" : this.translationKeys.title;
  }
  _stepDataChanged(s) {
    this._stepData = s.detail.value;
  }
  get _stepDataProcessed() {
    return this._stepData !== void 0 ? this._stepData : (this._stepData = B(this.step.data_schema), this._stepData);
  }
  get _stepTranslationKeys() {
    let s = {};
    return this.translationKeys && (s = this.translationKeys[this.flowType].step[this.step.step_id]), T(
      s,
      this.step.description_placeholders || {}
    );
  }
  async _handleSubmit(s) {
    s.stopPropagation();
    const t = this._stepData || {};
    if (!(t === void 0 ? (
      // If no data filled in, just check that any field is required
      this.step.data_schema.find((o) => o.required) === void 0
    ) : (
      // If data is filled in, make sure all required fields are
      t && this.step.data_schema.every(
        (o) => !o.required || !["", void 0].includes(t[o.name])
      )
    ))) {
      this._errorMsg = "Not all required fields are filled in.";
      return;
    }
    this._errorMsg = void 0, m(this, "flow-updated", {
      data: {
        handler: this.step.handler,
        flow_id: this.step.flow_id,
        user_input: this._stepData
      }
    });
  }
};
d.styles = [
  x,
  K,
  w`
      .submit-spinner {
        margin-right: 16px;
        margin-inline-end: 16px;
        margin-inline-start: initial;
      }
      pc-form {
        margin-top: 24px;
        display: block;
      }
      h2 {
        word-break: break-word;
        padding-inline-end: 72px;
      }
    `
];
h([
  l({ attribute: !1 })
], d.prototype, "step", 2);
h([
  l({ attribute: !1 })
], d.prototype, "flowType", 2);
h([
  l({ attribute: !1 })
], d.prototype, "translationKeys", 2);
h([
  l({ type: Boolean })
], d.prototype, "loading", 2);
h([
  b()
], d.prototype, "_errorMsg", 2);
h([
  b()
], d.prototype, "_stepData", 2);
d = h([
  u("step-flow-form")
], d);
var N = Object.defineProperty, V = Object.getOwnPropertyDescriptor, F = (s, t, i, o) => {
  for (var e = o > 1 ? void 0 : o ? V(t, i) : t, a = s.length - 1, r; a >= 0; a--)
    (r = s[a]) && (e = (o ? r(t, i, e) : r(e)) || e);
  return o && e && N(t, i, e), e;
};
let D = class extends _ {
  render() {
    const s = `Loading ${this.flowType} ...`;
    return n`
      <div class="init-spinner">
        ${s ? n`<div>${s}</div>` : ""}
        <pc-circular-progress indeterminate></pc-circular-progress>
      </div>
    `;
  }
  static get styles() {
    return w`
      .init-spinner {
        padding: 50px 100px;
        text-align: center;
      }
      pc-circular-progress {
        margin-top: 16px;
      }
    `;
  }
};
F([
  l({ attribute: !1 })
], D.prototype, "flowType", 2);
D = F([
  u("step-flow-loading")
], D);
var G = Object.defineProperty, J = Object.getOwnPropertyDescriptor, v = (s, t, i, o) => {
  for (var e = o > 1 ? void 0 : o ? J(t, i) : t, a = s.length - 1, r; a >= 0; a--)
    (r = s[a]) && (e = (o ? r(t, i, e) : r(e)) || e);
  return o && e && G(t, i, e), e;
};
let f = class extends _ {
  render() {
    const s = this.step.menu_options, t = this._stepTranslationKeys;
    return n`
      <h2>${t.title}</h2>
      <md-list class="content" role="menu">
        ${s.map(
      (i) => n`
            <md-list-item
              type="button"
              class="step"
              .step=${i}
              @click=${this._handleStep}
            >
              <span slot="headline"
                >${t.menu_options[i]}</span
              >
            </md-list-item>
          `
    )}
      </md-list>
    `;
  }
  get _stepTranslationKeys() {
    let s = {};
    return this.translationKeys && (s = this.translationKeys[this.flowType].step[this.step.step_id]), T(
      s,
      this.step.description_placeholders || {}
    );
  }
  _handleStep(s) {
    s.stopPropagation();
    const t = s.target.closest(".step").step;
    m(this, "flow-updated", {
      data: {
        handler: this.step.handler,
        flow_id: this.step.flow_id,
        user_input: { next_step_id: t }
      }
    });
  }
};
f.styles = j;
v([
  l({ attribute: !1 })
], f.prototype, "step", 2);
v([
  l({ attribute: !1 })
], f.prototype, "flowType", 2);
v([
  l({ attribute: !1 })
], f.prototype, "translationKeys", 2);
f = v([
  u("step-flow-menu")
], f);
var Q = Object.defineProperty, U = Object.getOwnPropertyDescriptor, c = (s, t, i, o) => {
  for (var e = o > 1 ? void 0 : o ? U(t, i) : t, a = s.length - 1, r; a >= 0; a--)
    (r = s[a]) && (e = (o ? r(t, i, e) : r(e)) || e);
  return o && e && Q(t, i, e), e;
};
let p = class extends _ {
  constructor() {
    super(...arguments), this._loading = !1, this._fetchData = new E(
      this,
      async () => {
        if (!this._step) {
          const t = await $.postRequest(
            `/config/plugin_entries/${this.flowType}/flow`,
            {
              handler: this.handler
            }
          );
          this._step = t.data.result;
        }
        const s = this.flowType === "options" ? this.domain : this._step.handler;
        await $.getRequest(`/translations/plugins/${s}`).then((t) => {
          this._translationKeys = t.data.result;
        });
      },
      () => [this._step]
    );
  }
  async _closeDialog() {
    var s;
    await ((s = this.dialog) == null ? void 0 : s.close("close"));
  }
  _preventClose(s) {
    s.target.returnValue !== "close" && s.preventDefault();
  }
  render() {
    return n`<pc-dialog open @close=${this._preventClose}>
      ${this._fetchData.render({
      pending: () => n`<step-flow-loading
            slot="content"
            .flowType=${this.flowType}
          ></step-flow-loading>`,
      complete: () => n`
          ${this._step === void 0 ? "" : n`
                <pc-icon-button
                  label="Close"
                  slot="content"
                  .path=${M}
                  @click=${this._closeDialog}
                ></pc-icon-button>
                ${this._step.type === "form" ? n`
                      <step-flow-form
                        slot="content"
                        .loading=${this._loading}
                        .step=${this._step}
                        .flowType=${this.flowType}
                        .translationKeys=${this._translationKeys}
                        @flow-updated=${this._handleSubmit}
                      ></step-flow-form>
                    ` : this._step.type === "menu" ? n`
                        <step-flow-menu
                          slot="content"
                          .step=${this._step}
                          .flowType=${this.flowType}
                          .translationKeys=${this._translationKeys}
                          @flow-updated=${this._handleSubmit}
                        ></step-flow-menu>
                      ` : this._step.type === "abort" ? n`
                          <step-flow-abort
                            slot="content"
                            .step=${this._step}
                            .translationKeys=${this._translationKeys}
                            @flow-updated=${this._closeDialog}
                          ></step-flow-abort>
                        ` : this._step.type === "create_entry" ? n`<step-flow-create-entry
                            slot="content"
                            .step=${this._step}
                            .translationKeys=${this._translationKeys}
                            @flow-updated=${this._closeDialog}
                          ></step-flow-create-entry>` : ""}
              `}
        `
    })}</pc-dialog
    >`;
  }
  async _handleSubmit(s) {
    s.stopPropagation(), this._loading = !0, await $.postRequest(
      `/config/plugin_entries/${this.flowType}/flow`,
      s.detail.data
    ).then((t) => {
      const i = t.data.result;
      i.type === "create_entry" && this.flowType === "options" ? (this._closeDialog(), m(this, "flow-updated", {
        data: {
          handler: i.handler
        }
      })) : this._step = i;
    }).catch((t) => {
      var i;
      this._closeDialog(), alert((i = t.response) == null ? void 0 : i.data.detail);
    }).finally(() => {
      this._loading = !1;
    });
  }
};
p.styles = [
  j,
  w`
      pc-dialog {
        --dialog-content-padding: 0;
      }
      pc-icon-button {
        position: absolute;
        right: 16px;
        top: 7px;
        text-decoration: none;
        color: inherit;
        inset-inline-start: initial;
        inset-inline-end: 16px;
        z-index: 1;
      }
      .dialog-actions {
        padding: 16px;
        position: absolute;
        top: 0;
        right: 0;
        inset-inline-start: initial;
        inset-inline-end: 0px;
        direction: var(--direction);
      }
      .dialog-actions > * {
        color: var(--secondary-text-color);
      }
    `
];
c([
  l()
], p.prototype, "domain", 2);
c([
  l()
], p.prototype, "handler", 2);
c([
  l({ attribute: !1 })
], p.prototype, "flowType", 2);
c([
  b()
], p.prototype, "_step", 2);
c([
  b()
], p.prototype, "_translationKeys", 2);
c([
  b()
], p.prototype, "_loading", 2);
c([
  q("pc-dialog")
], p.prototype, "dialog", 2);
p = c([
  u("dialog-data-entry-flow")
], p);
