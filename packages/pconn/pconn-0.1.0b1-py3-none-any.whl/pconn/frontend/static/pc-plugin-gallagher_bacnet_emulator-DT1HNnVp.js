import { w as u, y as h, z as m, T as b, a as f, h as g, b as d, x as l, A as v, B as _, C as y, D as $, E as x, F as D, p as w, i as O, c as S, r as j, t as E } from "./index-Bs6A-haP.js";
import "./filled-button-DK7nEDMp.js";
import "./pc-button-menu-BrK2NJOx.js";
import { p as I } from "./styles-COki90LR.js";
/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const p = "important", P = " !" + p, C = u(class extends h {
  constructor(t) {
    var e;
    if (super(t), t.type !== m.ATTRIBUTE || t.name !== "style" || ((e = t.strings) == null ? void 0 : e.length) > 2) throw Error("The `styleMap` directive must be used in the `style` attribute and must be the only part in the attribute.");
  }
  render(t) {
    return Object.keys(t).reduce((e, s) => {
      const i = t[s];
      return i == null ? e : e + `${s = s.includes("-") ? s : s.replace(/(?:^(webkit|moz|ms|o)|)(?=[A-Z])/g, "-$&").toLowerCase()}:${i};`;
    }, "");
  }
  update(t, [e]) {
    const { style: s } = t.element;
    if (this.ft === void 0) return this.ft = new Set(Object.keys(e)), this.render(e);
    for (const i of this.ft) e[i] == null && (this.ft.delete(i), i.includes("-") ? s.removeProperty(i) : s[i] = null);
    for (const i in e) {
      const a = e[i];
      if (a != null) {
        this.ft.add(i);
        const n = typeof a == "string" && a.endsWith(P);
        i.includes("-") || n ? s.setProperty(i, n ? a.slice(0, -11) : a, n ? p : "") : s[i] = a;
      }
    }
    return b;
  }
});
var A = Object.defineProperty, L = Object.getOwnPropertyDescriptor, c = (t, e, s, i) => {
  for (var a = i > 1 ? void 0 : i ? L(e, s) : e, n = t.length - 1, o; n >= 0; n--)
    (o = t[n]) && (a = (i ? o(e, s, a) : o(a)) || a);
  return i && a && A(e, s, a), a;
};
let r = class extends f {
  constructor() {
    super(...arguments), this._fetchData = new g(
      this,
      async () => {
        let t = 0;
        return await d.postRequest(`/plugins/${this.entry.entry_id}`, {
          action: "get_data"
        }).then((e) => {
          this._deviceId = e.data.result.id, this._objects = e.data.result.objects, t = this._objects.length;
        }), t > 0 && (this.dataStream = d.getDataStream(
          this,
          this.entry.entry_id,
          this._updateData
        )), t;
      },
      () => []
    ), this._renderItem = (t) => l`<md-list-item
      class="object ${v({
      "state-disabled": t.disabled
    })}"
      .object=${t}
    >
      <pc-svg-icon
        slot="start"
        style=${C({
      color: !t.outOfService && t.presentValue === "active" ? "yellow" : "grey"
    })}
        .path=${t.identifier[0] === "binaryInput" ? _ : y}
      ></pc-svg-icon>
      <div slot="headline">${t.name}</div>
      <div slot="supporting-text">
        ${t.identifier[0]}-${t.identifier[1]}
      </div>
      ${t.disabled ? l`<md-filled-button
            unelevated
            slot="end"
            @click=${this._handleEnable}
            >ENABLE
          </md-filled-button>` : t.outOfService ? l`<pc-icon-button
              slot="end"
              class="error"
              style="color: var(--error-color)"
              .label=${t.flags.toString()}
              .path=${$}
            ></pc-icon-button>` : l` <pc-button-menu slot="end">
              <pc-icon-button
                slot="trigger"
                label="Menu"
                .path=${x}
              ></pc-icon-button>
              ${t.disabled ? "" : l`<md-menu-item @close-menu=${this._handleDisable}>
                    <div slot="headline">Disable</div>
                    <pc-svg-icon
                      slot="start"
                      .path=${D}
                    ></pc-svg-icon>
                  </md-menu-item>`}
            </pc-button-menu>`}
    </md-list-item>`;
  }
  _updateData(t) {
    this._objects = t;
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this.dataStream && this.dataStream.close();
  }
  render() {
    return l` <div class="container">
      <pc-card .header=${this.entry.entry_id}>
        <div class="header-status">
          <span>Device ID: ${this._deviceId} </span>
        </div>
        ${this._fetchData.render({
      pending: () => l`<p>Loading data...</p>`,
      complete: (t) => {
        var e;
        return l`
            <div class="card-content">
              ${t === 0 ? l`<div>No objects configured!!</div>` : l`
                    <md-list>
                      ${(e = this._objects) == null ? void 0 : e.map(
          (s) => this._renderItem(s)
        )}
                    </md-list>
                  `}
            </div>
          `;
      }
    })}
      </pc-card>
    </div>`;
  }
  _handleEnable(t) {
    this._enableDisableObject(
      t.target.closest(".object").object,
      !1
    );
  }
  _handleDisable(t) {
    this._enableDisableObject(
      t.target.closest(".object").object,
      !0
    );
  }
  async _enableDisableObject(t, e) {
    await d.postRequest(`/plugins/${this.entry.entry_id}`, {
      action: "disable_item",
      user_input: {
        item_id: t.ftItemId,
        disabled: e
      }
    }), await this._fetchData.run();
  }
};
r.styles = [
  w,
  I,
  O`
      .state-disabled {
        --md-list-item-label-text-color: var(--disabled-text-color);
        --md-list-item-supporting-text-color: var(--disabled-text-color);
      }
      md-list-item {
        width: 100%;
        --md-list-item-supporting-text-color: var(--secondary-text-color);
      }
      .container {
        height: calc(100% - 64px);
      }
      pc-card {
        display: flex;
        flex-direction: column;
        height: calc(100% - 49px);
      }
      .card-content {
        display: flex;
        flex-direction: column;
        height: calc(100% - 49px);
      }
      md-list {
        flex-grow: 1;
      }
    `
];
c([
  S({ attribute: !1 })
], r.prototype, "entry", 2);
c([
  j()
], r.prototype, "_objects", 2);
r = c([
  E("pc-plugin-gallagher_bacnet_emulator")
], r);
export {
  r as PcPluginGallagherBacnetEmulator
};
