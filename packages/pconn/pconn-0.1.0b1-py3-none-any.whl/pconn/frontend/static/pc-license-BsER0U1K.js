import { p as r, k as d, c as u, r as f, l as g, a as h, x as n, o as _, q as v, b as y, s as C, t as b } from "./index-Bs6A-haP.js";
import "./pc-file-upload-3EoYkRJy.js";
var $ = Object.defineProperty, w = Object.getOwnPropertyDescriptor, i = (e, l, s, t) => {
  for (var a = t > 1 ? void 0 : t ? w(l, s) : l, p = e.length - 1, c; p >= 0; p--)
    (c = e[p]) && (a = (t ? c(l, s, a) : c(a)) || a);
  return t && a && $(l, s, a), a;
};
let o = class extends h {
  constructor() {
    super(...arguments), this.allowClose = !1, this._uploading = !1;
  }
  _preventClose(e) {
    e.target.returnValue !== "close" && e.preventDefault();
  }
  async _closeDialog() {
    var e;
    await ((e = this.dialog) == null ? void 0 : e.close("close"));
  }
  render() {
    return n` <pc-dialog open @close=${this._preventClose}>
      <div slot="headline">
        Select activation license.
        ${this.allowClose ? n`<pc-icon-button
              slot="headline"
              label="Close"
              .path=${_}
              @click=${this._closeDialog}
            ></pc-icon-button>` : ""}
      </div>
      <pc-file-upload
        slot="content"
        .uploading=${this._uploading}
        .icon=${v}
        accept="application/x-license"
        label="Upload license"
        supports="Supports .lic files"
        @file-picked=${this._uploadFile}
      ></pc-file-upload>
    </pc-dialog>`;
  }
  async _uploadFile(e) {
    const l = e.detail.files[0];
    this._uploading = !0, await y.postFile("license/apply", l).then(() => {
      C(this, "config-updated");
    }).catch((s) => {
      var t;
      alert((t = s.response) == null ? void 0 : t.data.detail);
    }).finally(() => {
      this._uploading = !1;
    });
  }
};
o.styles = [r, d];
i([
  u({ attribute: !1 })
], o.prototype, "allowClose", 2);
i([
  f()
], o.prototype, "_uploading", 2);
i([
  g("pc-dialog")
], o.prototype, "dialog", 2);
o = i([
  b("pc-license")
], o);
