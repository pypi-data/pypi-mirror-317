import { a as f, b as n, s as h, x as c, aq as _, c as o, r as d, t as v } from "./index-Bs6A-haP.js";
import "./pc-file-upload-3EoYkRJy.js";
var y = Object.defineProperty, b = Object.getOwnPropertyDescriptor, s = (e, t, a, l) => {
  for (var r = l > 1 ? void 0 : l ? b(t, a) : t, p = e.length - 1, u; p >= 0; p--)
    (u = e[p]) && (r = (l ? u(t, a, r) : u(r)) || r);
  return l && r && y(t, a, r), r;
};
let i = class extends f {
  constructor() {
    super(...arguments), this.disabled = !1, this.required = !0, this._busy = !1, this._removeFile = async () => {
      this._busy = !0, await n.postRequest("file/delete", {
        file_id: this.value
      }).finally(() => {
        this._busy = !1;
      }), this._filename = void 0, h(this, "value-changed", { value: "" });
    };
  }
  render() {
    var e, t;
    return c`
      <pc-file-upload
        .accept=${((e = this.selector.file) == null ? void 0 : e.accept) || ""}
        .icon=${_}
        .label=${this.label}
        .required=${this.required}
        .disabled=${this.disabled}
        .supports=${this.helper}
        .uploading=${this._busy}
        .value=${this.value ? (t = this._filename) == null ? void 0 : t.name : void 0}
        @file-picked=${this._uploadFile}
        @change=${this._removeFile}
      ></pc-file-upload>
    `;
  }
  willUpdate(e) {
    super.willUpdate(e), e.has("value") && this._filename && this.value !== this._filename.fileId && (this._filename = void 0);
  }
  async _uploadFile(e) {
    this._busy = !0;
    const t = e.detail.files[0];
    await n.postFile("file/upload", t).then((a) => {
      const l = a.data.result;
      this._filename = { fileId: l, name: t.name }, h(this, "value-changed", { value: l });
    }).catch((a) => {
      var l;
      alert((l = a.response) == null ? void 0 : l.data.detail);
    }).finally(() => {
      this._busy = !1;
    });
  }
};
s([
  o({ attribute: !1 })
], i.prototype, "selector", 2);
s([
  o()
], i.prototype, "value", 2);
s([
  o()
], i.prototype, "label", 2);
s([
  o()
], i.prototype, "helper", 2);
s([
  o({ type: Boolean })
], i.prototype, "disabled", 2);
s([
  o({ type: Boolean })
], i.prototype, "required", 2);
s([
  d()
], i.prototype, "_filename", 2);
s([
  d()
], i.prototype, "_busy", 2);
i = s([
  v("pc-selector-file")
], i);
export {
  i as PcFileSelector
};
