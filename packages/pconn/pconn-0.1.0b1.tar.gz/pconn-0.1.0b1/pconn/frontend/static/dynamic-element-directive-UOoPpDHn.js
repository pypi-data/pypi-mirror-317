import { w as s, y as c, z as m, T as a } from "./index-Bs6A-haP.js";
const d = s(
  class extends c {
    constructor(e) {
      if (super(e), e.type !== m.CHILD)
        throw new Error(
          "dynamicElementDirective can only be used in content bindings"
        );
    }
    update(e, [t, n]) {
      return this._element && this._element.localName === t ? (n && Object.entries(n).forEach(([r, i]) => {
        this._element[r] = i;
      }), a) : this.render(t, n);
    }
    render(e, t) {
      return this._element = document.createElement(e), t && Object.entries(t).forEach(([n, r]) => {
        this._element[n] = r;
      }), this._element;
    }
  }
);
export {
  d
};
