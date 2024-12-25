import { J as v, K as g, _ as s, c as e, l as b, W as f, X as $, L as h, V as c, N as p, Y as C, M as E, t as x, a as I, x as _, i as k } from "./index-Bs6A-haP.js";
import { M as w, s as R } from "./menu-w4ZSIJcy.js";
/**
 * @license
 * Copyright 2022 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const B = v(g);
class t extends B {
  constructor() {
    super(...arguments), this.disabled = !1, this.type = "menuitem", this.href = "", this.target = "", this.keepOpen = !1, this.selected = !1, this.menuItemController = new w(this, {
      getHeadlineElements: () => this.headlineElements,
      getSupportingTextElements: () => this.supportingTextElements,
      getDefaultElements: () => this.defaultElements,
      getInteractiveElement: () => this.listItemRoot
    });
  }
  /**
   * The text that is selectable via typeahead. If not set, defaults to the
   * innerText of the item slotted into the `"headline"` slot.
   */
  get typeaheadText() {
    return this.menuItemController.typeaheadText;
  }
  set typeaheadText(o) {
    this.menuItemController.setTypeaheadText(o);
  }
  render() {
    return this.renderListItem(h`
      <md-item>
        <div slot="container">
          ${this.renderRipple()} ${this.renderFocusRing()}
        </div>
        <slot name="start" slot="start"></slot>
        <slot name="end" slot="end"></slot>
        ${this.renderBody()}
      </md-item>
    `);
  }
  /**
   * Renders the root list item.
   *
   * @param content the child content of the list item.
   */
  renderListItem(o) {
    const d = this.type === "link";
    let r;
    switch (this.menuItemController.tagName) {
      case "a":
        r = c`a`;
        break;
      case "button":
        r = c`button`;
        break;
      default:
      case "li":
        r = c`li`;
        break;
    }
    const l = d && this.target ? this.target : p;
    return C`
      <${r}
        id="item"
        tabindex=${this.disabled && !d ? -1 : 0}
        role=${this.menuItemController.role}
        aria-label=${this.ariaLabel || p}
        aria-selected=${this.ariaSelected || p}
        aria-checked=${this.ariaChecked || p}
        aria-expanded=${this.ariaExpanded || p}
        aria-haspopup=${this.ariaHasPopup || p}
        class="list-item ${E(this.getRenderClasses())}"
        href=${this.href || p}
        target=${l}
        @click=${this.menuItemController.onClick}
        @keydown=${this.menuItemController.onKeydown}
      >${o}</${r}>
    `;
  }
  /**
   * Handles rendering of the ripple element.
   */
  renderRipple() {
    return h` <md-ripple
      part="ripple"
      for="item"
      ?disabled=${this.disabled}></md-ripple>`;
  }
  /**
   * Handles rendering of the focus ring.
   */
  renderFocusRing() {
    return h` <md-focus-ring
      part="focus-ring"
      for="item"
      inward></md-focus-ring>`;
  }
  /**
   * Classes applied to the list item root.
   */
  getRenderClasses() {
    return {
      disabled: this.disabled,
      selected: this.selected
    };
  }
  /**
   * Handles rendering the headline and supporting text.
   */
  renderBody() {
    return h`
      <slot></slot>
      <slot name="overline" slot="overline"></slot>
      <slot name="headline" slot="headline"></slot>
      <slot name="supporting-text" slot="supporting-text"></slot>
      <slot
        name="trailing-supporting-text"
        slot="trailing-supporting-text"></slot>
    `;
  }
  focus() {
    var o;
    (o = this.listItemRoot) == null || o.focus();
  }
}
t.shadowRootOptions = {
  ...g.shadowRootOptions,
  delegatesFocus: !0
};
s([
  e({ type: Boolean, reflect: !0 })
], t.prototype, "disabled", void 0);
s([
  e()
], t.prototype, "type", void 0);
s([
  e()
], t.prototype, "href", void 0);
s([
  e()
], t.prototype, "target", void 0);
s([
  e({ type: Boolean, attribute: "keep-open" })
], t.prototype, "keepOpen", void 0);
s([
  e({ type: Boolean })
], t.prototype, "selected", void 0);
s([
  b(".list-item")
], t.prototype, "listItemRoot", void 0);
s([
  f({ slot: "headline" })
], t.prototype, "headlineElements", void 0);
s([
  f({ slot: "supporting-text" })
], t.prototype, "supportingTextElements", void 0);
s([
  $({ slot: "" })
], t.prototype, "defaultElements", void 0);
s([
  e({ attribute: "typeahead-text" })
], t.prototype, "typeaheadText", null);
/**
 * @license
 * Copyright 2022 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
let y = class extends t {
};
y.styles = [R];
y = s([
  x("md-menu-item")
], y);
var O = Object.defineProperty, T = Object.getOwnPropertyDescriptor, a = (n, o, d, r) => {
  for (var l = r > 1 ? void 0 : r ? T(o, d) : o, m = n.length - 1, u; m >= 0; m--)
    (u = n[m]) && (l = (r ? u(o, d, l) : u(l)) || l);
  return r && l && O(o, d, l), l;
};
let i = class extends I {
  constructor() {
    super(...arguments), this.corner = "end-start", this.menuCorner = "start-start", this.x = 0, this.y = 0, this.disabled = !1, this.fixed = !1, this.noAnchor = !1;
  }
  get items() {
    var n;
    return (n = this._menu) == null ? void 0 : n.items;
  }
  render() {
    return _`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <md-menu
        .anchorCorner=${this.corner}
        .menuCorner=${this.menuCorner}
        .positioning=${this.fixed ? "fixed" : "popover"}
        .yOffset=${this.y}
        .xOffset=${this.x}
        @opened=${this._bubbleEvent}
        @closed=${this._bubbleEvent}
      >
        <slot></slot>
      </md-menu>
    `;
  }
  _bubbleEvent(n) {
    this.dispatchEvent(new Event(n.type));
  }
  _handleClick() {
    this.disabled || (this._menu.anchorElement = this.noAnchor ? null : this, this._menu.show());
  }
  static get styles() {
    return k`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
      ::slotted(div) {
        margin-top: 8px;
      }
    `;
  }
};
a([
  e()
], i.prototype, "corner", 2);
a([
  e({ attribute: !1 })
], i.prototype, "menuCorner", 2);
a([
  e({ type: Number })
], i.prototype, "x", 2);
a([
  e({ type: Number })
], i.prototype, "y", 2);
a([
  e({ type: Boolean })
], i.prototype, "disabled", 2);
a([
  e({ type: Boolean })
], i.prototype, "fixed", 2);
a([
  e({ type: Boolean, attribute: "no-anchor" })
], i.prototype, "noAnchor", 2);
a([
  b("md-menu", !0)
], i.prototype, "_menu", 2);
i = a([
  x("pc-button-menu")
], i);
