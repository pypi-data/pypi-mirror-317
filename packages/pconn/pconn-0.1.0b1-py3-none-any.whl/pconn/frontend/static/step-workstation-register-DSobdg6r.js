import { k as h, i as f, r as d, a as g, h as m, b as p, x as a, s as u, t as v } from "./index-Bs6A-haP.js";
import "./filled-button-DK7nEDMp.js";
import "./filled-text-field-qW71ccQt.js";
import "./pc-circular-progress-CXHtR8Ql.js";
import { c as _ } from "./styles-CmkOrDPY.js";
var w = Object.defineProperty, y = Object.getOwnPropertyDescriptor, c = (t, e, s, o) => {
  for (var r = o > 1 ? void 0 : o ? y(e, s) : e, n = t.length - 1, l; n >= 0; n--)
    (l = t[n]) && (r = (o ? l(e, s, r) : l(r)) || r);
  return o && r && w(e, s, r), r;
};
let i = class extends g {
  constructor() {
    super(...arguments), this._loading = !1, this._fetchData = new m(
      this,
      async () => {
        await p.getRequest("/config/workstation/verify").catch((t) => {
          var e;
          throw new Error((e = t.response) == null ? void 0 : e.data.detail);
        });
      },
      () => []
    );
  }
  _preventClose(t) {
    t.preventDefault();
  }
  render() {
    return a`<pc-dialog open @close=${this._preventClose}>
      ${this._fetchData.render({
      pending: () => a`<div slot="content" class="content">
            Verifying workstation...
          </div>`,
      complete: () => a` <div slot="headline">Select your machine name</div>
            <div slot="content" class="content">
              ${this._errorMsg ? a`<pc-alert
                    alert-type="error"
                    .header=${this._errorMsg}
                  ></pc-alert>` : ""}
              <p>Please enter a name for this workstation</p>
              <md-filled-text-field
                label="Name"
                .value=${this.workstationName || ""}
                @input=${this._valueChanged}
              >
              </md-filled-text-field>
            </div>
            <div slot="actions" class="buttons">
              ${this._loading ? a`<pc-circular-progress
                    indeterminate
                  ></pc-circular-progress>` : a` <md-filled-button @click=${this._handleSubmit}
                    >SUBMIT
                  </md-filled-button>`}
            </div>`,
      error: (t) => a`<pc-alert
            slot="content"
            class="content"
            alert-type="error"
            .header=${t}
          >
          </pc-alert>`
    })}</pc-dialog
    >`;
  }
  _valueChanged(t) {
    this.workstationName = t.target.value;
  }
  async _handleSubmit(t) {
    t.stopPropagation(), this._loading = !0, await p.postRequest("/config/workstations", {
      action: "register",
      data: { name: this.workstationName }
    }).then(() => {
      u(this, "config-updated");
    }).catch((e) => {
      var s;
      this._errorMsg = (s = e.response) == null ? void 0 : s.data.detail;
    }).finally(() => {
      this._loading = !1;
    });
  }
};
i.styles = [
  h,
  _,
  f`
      md-filled-text-field {
        display: block;
      }
    `
];
c([
  d()
], i.prototype, "_errorMsg", 2);
c([
  d()
], i.prototype, "_loading", 2);
i = c([
  v("step-workstation-register")
], i);
