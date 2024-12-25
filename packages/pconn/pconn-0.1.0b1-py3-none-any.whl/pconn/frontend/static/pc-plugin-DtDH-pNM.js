import { r as c, c as m, t as g, a as u, h, b as _, x as d, n as y } from "./index-Bs6A-haP.js";
import { d as f } from "./dynamic-element-directive-UOoPpDHn.js";
var v = Object.defineProperty, w = Object.getOwnPropertyDescriptor, p = (e, r, s, a) => {
  for (var t = a > 1 ? void 0 : a ? w(r, s) : r, o = e.length - 1, i; o >= 0; o--)
    (i = e[o]) && (t = (a ? i(r, s, t) : i(t)) || t);
  return a && t && v(r, s, t), t;
};
const l = {
  gallagher_demo: () => import("./pc-plugin-gallagher_demo-DlYTb5_o.js"),
  gallagher_odoo: () => import("./pc-plugin-gallagher_odoo-D73Z2PoM.js"),
  gallagher_bacnet_emulator: () => import("./pc-plugin-gallagher_bacnet_emulator-DT1HNnVp.js"),
  gallagher_ai_analyzer: () => import("./pc-plugin-gallagher_ai_analyzer-CQVqa0rY.js")
};
let n = class extends u {
  constructor() {
    super(...arguments), this._verifyPluginEntry = new h(
      this,
      async () => {
        const r = (await _.getRequest(`/plugins/${this.entryId}`).catch((s) => {
          let a = "Unknown Error";
          throw [400, 404].includes(s.response.status) && (a = s.response.data.detail), new Error(a);
        })).data.result;
        return this.domain = r.domain, r;
      },
      () => []
    );
  }
  render() {
    return d`${this._verifyPluginEntry.render({
      complete: (e) => f(`pc-plugin-${e.domain}`, {
        entry: e
      }),
      error: (e) => d`<pc-alert-dialog
          alert-type="error"
          .message=${e}
          @alert-dismissed-clicked=${this._handleClose}
        ></pc-alert-dialog>`
    })}`;
  }
  _handleClose() {
    y("/plugins", { replace: !0 });
  }
  willUpdate(e) {
    var r;
    e.has("domain") && ((r = l[this.domain]) == null || r.call(l));
  }
};
p([
  m({ attribute: "entry-id" })
], n.prototype, "entryId", 2);
p([
  c()
], n.prototype, "domain", 2);
n = p([
  g("pc-plugin")
], n);
export {
  n as Plugin
};
