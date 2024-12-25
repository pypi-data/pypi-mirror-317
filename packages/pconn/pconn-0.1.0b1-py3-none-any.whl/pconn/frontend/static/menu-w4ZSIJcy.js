import { i as V, $ as S, _ as r, l as j, c as u, W as J, r as ee, K as te, a0 as ie, a1 as ne, a2 as se, a3 as oe, a4 as ae, L as z, M as re, N as le, a5 as M, t as ce } from "./index-Bs6A-haP.js";
import { o as de } from "./style-map-8seGJ4i8.js";
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
function he(g, e) {
  return new CustomEvent("close-menu", {
    bubbles: !0,
    composed: !0,
    detail: { initiator: g, reason: e, itemPath: [g] }
  });
}
const Y = he, W = {
  SPACE: "Space",
  ENTER: "Enter"
}, q = {
  CLICK_SELECTION: "click-selection",
  KEYDOWN: "keydown"
}, pe = {
  ESCAPE: "Escape",
  SPACE: W.SPACE,
  ENTER: W.ENTER
};
function Z(g) {
  return Object.values(pe).some((e) => e === g);
}
function we(g) {
  return Object.values(W).some((e) => e === g);
}
function G(g, e) {
  const t = new Event("md-contains", { bubbles: !0, composed: !0 });
  let i = [];
  const s = (p) => {
    i = p.composedPath();
  };
  return e.addEventListener("md-contains", s), g.dispatchEvent(t), e.removeEventListener("md-contains", s), i.length > 0;
}
const B = {
  NONE: "none",
  LIST_ROOT: "list-root",
  FIRST_ITEM: "first-item",
  LAST_ITEM: "last-item"
};
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
class Ce {
  /**
   * @param host The MenuItem in which to attach this controller to.
   * @param config The object that configures this controller's behavior.
   */
  constructor(e, t) {
    this.host = e, this.internalTypeaheadText = null, this.onClick = () => {
      this.host.keepOpen || this.host.dispatchEvent(Y(this.host, {
        kind: q.CLICK_SELECTION
      }));
    }, this.onKeydown = (i) => {
      if (this.host.href && i.code === "Enter") {
        const n = this.getInteractiveElement();
        n instanceof HTMLAnchorElement && n.click();
      }
      if (i.defaultPrevented)
        return;
      const s = i.code;
      this.host.keepOpen && s !== "Escape" || Z(s) && (i.preventDefault(), this.host.dispatchEvent(Y(this.host, {
        kind: q.KEYDOWN,
        key: s
      })));
    }, this.getHeadlineElements = t.getHeadlineElements, this.getSupportingTextElements = t.getSupportingTextElements, this.getDefaultElements = t.getDefaultElements, this.getInteractiveElement = t.getInteractiveElement, this.host.addController(this);
  }
  /**
   * The text that is selectable via typeahead. If not set, defaults to the
   * innerText of the item slotted into the `"headline"` slot, and if there are
   * no slotted elements into headline, then it checks the _default_ slot, and
   * then the `"supporting-text"` slot if nothing is in _default_.
   */
  get typeaheadText() {
    if (this.internalTypeaheadText !== null)
      return this.internalTypeaheadText;
    const e = this.getHeadlineElements(), t = [];
    return e.forEach((i) => {
      i.textContent && i.textContent.trim() && t.push(i.textContent.trim());
    }), t.length === 0 && this.getDefaultElements().forEach((i) => {
      i.textContent && i.textContent.trim() && t.push(i.textContent.trim());
    }), t.length === 0 && this.getSupportingTextElements().forEach((i) => {
      i.textContent && i.textContent.trim() && t.push(i.textContent.trim());
    }), t.join(" ");
  }
  /**
   * The recommended tag name to render as the list item.
   */
  get tagName() {
    switch (this.host.type) {
      case "link":
        return "a";
      case "button":
        return "button";
      default:
      case "menuitem":
      case "option":
        return "li";
    }
  }
  /**
   * The recommended role of the menu item.
   */
  get role() {
    return this.host.type === "option" ? "option" : "menuitem";
  }
  hostConnected() {
    this.host.toggleAttribute("md-menu-item", !0);
  }
  hostUpdate() {
    this.host.href && (this.host.type = "link");
  }
  /**
   * Use to set the typeaheadText when it changes.
   */
  setTypeaheadText(e) {
    this.internalTypeaheadText = e;
  }
}
/**
 * @license
 * Copyright 2024 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const Te = V`:host{display:flex;--md-ripple-hover-color: var(--md-menu-item-hover-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--md-ripple-hover-opacity: var(--md-menu-item-hover-state-layer-opacity, 0.08);--md-ripple-pressed-color: var(--md-menu-item-pressed-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--md-ripple-pressed-opacity: var(--md-menu-item-pressed-state-layer-opacity, 0.12)}:host([disabled]){opacity:var(--md-menu-item-disabled-opacity, 0.3);pointer-events:none}md-focus-ring{z-index:1;--md-focus-ring-shape: 8px}a,button,li{background:none;border:none;padding:0;margin:0;text-align:unset;text-decoration:none}.list-item{border-radius:inherit;display:flex;flex:1;max-width:inherit;min-width:inherit;outline:none;-webkit-tap-highlight-color:rgba(0,0,0,0)}.list-item:not(.disabled){cursor:pointer}[slot=container]{pointer-events:none}md-ripple{border-radius:inherit}md-item{border-radius:inherit;flex:1;color:var(--md-menu-item-label-text-color, var(--md-sys-color-on-surface, #1d1b20));font-family:var(--md-menu-item-label-text-font, var(--md-sys-typescale-body-large-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-menu-item-label-text-size, var(--md-sys-typescale-body-large-size, 1rem));line-height:var(--md-menu-item-label-text-line-height, var(--md-sys-typescale-body-large-line-height, 1.5rem));font-weight:var(--md-menu-item-label-text-weight, var(--md-sys-typescale-body-large-weight, var(--md-ref-typeface-weight-regular, 400)));min-height:var(--md-menu-item-one-line-container-height, 56px);padding-top:var(--md-menu-item-top-space, 12px);padding-bottom:var(--md-menu-item-bottom-space, 12px);padding-inline-start:var(--md-menu-item-leading-space, 16px);padding-inline-end:var(--md-menu-item-trailing-space, 16px)}md-item[multiline]{min-height:var(--md-menu-item-two-line-container-height, 72px)}[slot=supporting-text]{color:var(--md-menu-item-supporting-text-color, var(--md-sys-color-on-surface-variant, #49454f));font-family:var(--md-menu-item-supporting-text-font, var(--md-sys-typescale-body-medium-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-menu-item-supporting-text-size, var(--md-sys-typescale-body-medium-size, 0.875rem));line-height:var(--md-menu-item-supporting-text-line-height, var(--md-sys-typescale-body-medium-line-height, 1.25rem));font-weight:var(--md-menu-item-supporting-text-weight, var(--md-sys-typescale-body-medium-weight, var(--md-ref-typeface-weight-regular, 400)))}[slot=trailing-supporting-text]{color:var(--md-menu-item-trailing-supporting-text-color, var(--md-sys-color-on-surface-variant, #49454f));font-family:var(--md-menu-item-trailing-supporting-text-font, var(--md-sys-typescale-label-small-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-menu-item-trailing-supporting-text-size, var(--md-sys-typescale-label-small-size, 0.6875rem));line-height:var(--md-menu-item-trailing-supporting-text-line-height, var(--md-sys-typescale-label-small-line-height, 1rem));font-weight:var(--md-menu-item-trailing-supporting-text-weight, var(--md-sys-typescale-label-small-weight, var(--md-ref-typeface-weight-medium, 500)))}:is([slot=start],[slot=end])::slotted(*){fill:currentColor}[slot=start]{color:var(--md-menu-item-leading-icon-color, var(--md-sys-color-on-surface-variant, #49454f))}[slot=end]{color:var(--md-menu-item-trailing-icon-color, var(--md-sys-color-on-surface-variant, #49454f))}.list-item{background-color:var(--md-menu-item-container-color, transparent)}.list-item.selected{background-color:var(--md-menu-item-selected-container-color, var(--md-sys-color-secondary-container, #e8def8))}.selected:not(.disabled) ::slotted(*){color:var(--md-menu-item-selected-label-text-color, var(--md-sys-color-on-secondary-container, #1d192b))}@media(forced-colors: active){:host([disabled]),:host([disabled]) slot{color:GrayText;opacity:1}.list-item{position:relative}.list-item.selected::before{content:"";position:absolute;inset:0;box-sizing:border-box;border-radius:inherit;pointer-events:none;border:3px double CanvasText}}
`;
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const X = {
  END_START: "end-start",
  END_END: "end-end",
  START_START: "start-start",
  START_END: "start-end"
};
class ue {
  /**
   * @param host The host to connect the controller to.
   * @param getProperties A function that returns the properties for the
   * controller.
   */
  constructor(e, t) {
    this.host = e, this.getProperties = t, this.surfaceStylesInternal = {
      display: "none"
    }, this.lastValues = {
      isOpen: !1
    }, this.host.addController(this);
  }
  /**
   * The StyleInfo map to apply to the surface via Lit's stylemap
   */
  get surfaceStyles() {
    return this.surfaceStylesInternal;
  }
  /**
   * Calculates the surface's new position required so that the surface's
   * `surfaceCorner` aligns to the anchor's `anchorCorner` while keeping the
   * surface inside the window viewport. This positioning also respects RTL by
   * checking `getComputedStyle()` on the surface element.
   */
  async position() {
    const { surfaceEl: e, anchorEl: t, anchorCorner: i, surfaceCorner: s, positioning: n, xOffset: p, yOffset: a, disableBlockFlip: o, disableInlineFlip: m, repositionStrategy: v } = this.getProperties(), I = i.toLowerCase().trim(), w = s.toLowerCase().trim();
    if (!e || !t)
      return;
    const b = window.innerWidth, C = window.innerHeight, c = document.createElement("div");
    c.style.opacity = "0", c.style.position = "fixed", c.style.display = "block", c.style.inset = "0", document.body.appendChild(c);
    const f = c.getBoundingClientRect();
    c.remove();
    const x = window.innerHeight - f.bottom, d = window.innerWidth - f.right;
    this.surfaceStylesInternal = {
      display: "block",
      opacity: "0"
    }, this.host.requestUpdate(), await this.host.updateComplete, e.popover && e.isConnected && e.showPopover();
    const E = e.getSurfacePositionClientRect ? e.getSurfacePositionClientRect() : e.getBoundingClientRect(), y = t.getSurfacePositionClientRect ? t.getSurfacePositionClientRect() : t.getBoundingClientRect(), [h, R] = w.split("-"), [k, L] = I.split("-"), F = getComputedStyle(e).direction === "ltr";
    let { blockInset: P, blockOutOfBoundsCorrection: A, surfaceBlockProperty: H } = this.calculateBlock({
      surfaceRect: E,
      anchorRect: y,
      anchorBlock: k,
      surfaceBlock: h,
      yOffset: a,
      positioning: n,
      windowInnerHeight: C,
      blockScrollbarHeight: x
    });
    if (A && !o) {
      const _ = h === "start" ? "end" : "start", U = k === "start" ? "end" : "start", O = this.calculateBlock({
        surfaceRect: E,
        anchorRect: y,
        anchorBlock: U,
        surfaceBlock: _,
        yOffset: a,
        positioning: n,
        windowInnerHeight: C,
        blockScrollbarHeight: x
      });
      A > O.blockOutOfBoundsCorrection && (P = O.blockInset, A = O.blockOutOfBoundsCorrection, H = O.surfaceBlockProperty);
    }
    let { inlineInset: N, inlineOutOfBoundsCorrection: D, surfaceInlineProperty: K } = this.calculateInline({
      surfaceRect: E,
      anchorRect: y,
      anchorInline: L,
      surfaceInline: R,
      xOffset: p,
      positioning: n,
      isLTR: F,
      windowInnerWidth: b,
      inlineScrollbarWidth: d
    });
    if (D && !m) {
      const _ = R === "start" ? "end" : "start", U = L === "start" ? "end" : "start", O = this.calculateInline({
        surfaceRect: E,
        anchorRect: y,
        anchorInline: U,
        surfaceInline: _,
        xOffset: p,
        positioning: n,
        isLTR: F,
        windowInnerWidth: b,
        inlineScrollbarWidth: d
      });
      Math.abs(D) > Math.abs(O.inlineOutOfBoundsCorrection) && (N = O.inlineInset, D = O.inlineOutOfBoundsCorrection, K = O.surfaceInlineProperty);
    }
    v === "move" && (P = P - A, N = N - D), this.surfaceStylesInternal = {
      display: "block",
      opacity: "1",
      [H]: `${P}px`,
      [K]: `${N}px`
    }, v === "resize" && (A && (this.surfaceStylesInternal.height = `${E.height - A}px`), D && (this.surfaceStylesInternal.width = `${E.width - D}px`)), this.host.requestUpdate();
  }
  /**
   * Calculates the css property, the inset, and the out of bounds correction
   * for the surface in the block direction.
   */
  calculateBlock(e) {
    const { surfaceRect: t, anchorRect: i, anchorBlock: s, surfaceBlock: n, yOffset: p, positioning: a, windowInnerHeight: o, blockScrollbarHeight: m } = e, v = a === "fixed" || a === "document" ? 1 : 0, I = a === "document" ? 1 : 0, w = n === "start" ? 1 : 0, b = n === "end" ? 1 : 0, c = (s !== n ? 1 : 0) * i.height + p, f = w * i.top + b * (o - i.bottom - m), x = w * window.scrollY - b * window.scrollY, d = Math.abs(Math.min(0, o - f - c - t.height));
    return { blockInset: v * f + I * x + c, blockOutOfBoundsCorrection: d, surfaceBlockProperty: n === "start" ? "inset-block-start" : "inset-block-end" };
  }
  /**
   * Calculates the css property, the inset, and the out of bounds correction
   * for the surface in the inline direction.
   */
  calculateInline(e) {
    const { isLTR: t, surfaceInline: i, anchorInline: s, anchorRect: n, surfaceRect: p, xOffset: a, positioning: o, windowInnerWidth: m, inlineScrollbarWidth: v } = e, I = o === "fixed" || o === "document" ? 1 : 0, w = o === "document" ? 1 : 0, b = t ? 1 : 0, C = t ? 0 : 1, c = i === "start" ? 1 : 0, f = i === "end" ? 1 : 0, d = (s !== i ? 1 : 0) * n.width + a, E = c * n.left + f * (m - n.right - v), y = c * (m - n.right - v) + f * n.left, h = b * E + C * y, R = c * window.scrollX - f * window.scrollX, k = f * window.scrollX - c * window.scrollX, L = b * R + C * k, F = Math.abs(Math.min(0, m - h - d - p.width)), P = I * h + d + w * L;
    let A = i === "start" ? "inset-inline-start" : "inset-inline-end";
    return (o === "document" || o === "fixed") && (i === "start" && t || i === "end" && !t ? A = "left" : A = "right"), {
      inlineInset: P,
      inlineOutOfBoundsCorrection: F,
      surfaceInlineProperty: A
    };
  }
  hostUpdate() {
    this.onUpdate();
  }
  hostUpdated() {
    this.onUpdate();
  }
  /**
   * Checks whether the properties passed into the controller have changed since
   * the last positioning. If so, it will reposition if the surface is open or
   * close it if the surface should close.
   */
  async onUpdate() {
    const e = this.getProperties();
    let t = !1;
    for (const [p, a] of Object.entries(e))
      if (t = t || a !== this.lastValues[p], t)
        break;
    const i = this.lastValues.isOpen !== e.isOpen, s = !!e.anchorEl, n = !!e.surfaceEl;
    t && s && n && (this.lastValues.isOpen = e.isOpen, e.isOpen ? (this.lastValues = e, await this.position(), e.onOpen()) : i && (await e.beforeClose(), this.close(), e.onClose()));
  }
  /**
   * Hides the surface.
   */
  close() {
    this.surfaceStylesInternal = {
      display: "none"
    }, this.host.requestUpdate();
    const e = this.getProperties().surfaceEl;
    e != null && e.popover && (e != null && e.isConnected) && e.hidePopover();
  }
}
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const T = {
  INDEX: 0,
  ITEM: 1,
  TEXT: 2
};
class me {
  /**
   * @param getProperties A function that returns the options of the typeahead
   * controller:
   *
   * {
   *   getItems: A function that returns an array of menu items to be searched.
   *   typeaheadBufferTime: The maximum time between each keystroke to keep the
   *       current type buffer alive.
   * }
   */
  constructor(e) {
    this.getProperties = e, this.typeaheadRecords = [], this.typaheadBuffer = "", this.cancelTypeaheadTimeout = 0, this.isTypingAhead = !1, this.lastActiveRecord = null, this.onKeydown = (t) => {
      this.isTypingAhead ? this.typeahead(t) : this.beginTypeahead(t);
    }, this.endTypeahead = () => {
      this.isTypingAhead = !1, this.typaheadBuffer = "", this.typeaheadRecords = [];
    };
  }
  get items() {
    return this.getProperties().getItems();
  }
  get active() {
    return this.getProperties().active;
  }
  /**
   * Sets up typingahead
   */
  beginTypeahead(e) {
    this.active && (e.code === "Space" || e.code === "Enter" || e.code.startsWith("Arrow") || e.code === "Escape" || (this.isTypingAhead = !0, this.typeaheadRecords = this.items.map((t, i) => [
      i,
      t,
      t.typeaheadText.trim().toLowerCase()
    ]), this.lastActiveRecord = this.typeaheadRecords.find((t) => t[T.ITEM].tabIndex === 0) ?? null, this.lastActiveRecord && (this.lastActiveRecord[T.ITEM].tabIndex = -1), this.typeahead(e)));
  }
  /**
   * Performs the typeahead. Based on the normalized items and the current text
   * buffer, finds the _next_ item with matching text and activates it.
   *
   * @example
   *
   * items: Apple, Banana, Olive, Orange, Cucumber
   * buffer: ''
   * user types: o
   *
   * activates Olive
   *
   * @example
   *
   * items: Apple, Banana, Olive (active), Orange, Cucumber
   * buffer: 'o'
   * user types: l
   *
   * activates Olive
   *
   * @example
   *
   * items: Apple, Banana, Olive (active), Orange, Cucumber
   * buffer: ''
   * user types: o
   *
   * activates Orange
   *
   * @example
   *
   * items: Apple, Banana, Olive, Orange (active), Cucumber
   * buffer: ''
   * user types: o
   *
   * activates Olive
   */
  typeahead(e) {
    if (e.defaultPrevented)
      return;
    if (clearTimeout(this.cancelTypeaheadTimeout), e.code === "Enter" || e.code.startsWith("Arrow") || e.code === "Escape") {
      this.endTypeahead(), this.lastActiveRecord && (this.lastActiveRecord[T.ITEM].tabIndex = -1);
      return;
    }
    e.code === "Space" && e.preventDefault(), this.cancelTypeaheadTimeout = setTimeout(this.endTypeahead, this.getProperties().typeaheadBufferTime), this.typaheadBuffer += e.key.toLowerCase();
    const t = this.lastActiveRecord ? this.lastActiveRecord[T.INDEX] : -1, i = this.typeaheadRecords.length, s = (o) => (o[T.INDEX] + i - t) % i, n = this.typeaheadRecords.filter((o) => !o[T.ITEM].disabled && o[T.TEXT].startsWith(this.typaheadBuffer)).sort((o, m) => s(o) - s(m));
    if (n.length === 0) {
      clearTimeout(this.cancelTypeaheadTimeout), this.lastActiveRecord && (this.lastActiveRecord[T.ITEM].tabIndex = -1), this.endTypeahead();
      return;
    }
    const p = this.typaheadBuffer.length === 1;
    let a;
    this.lastActiveRecord === n[0] && p ? a = n[1] ?? n[0] : a = n[0], this.lastActiveRecord && (this.lastActiveRecord[T.ITEM].tabIndex = -1), this.lastActiveRecord = a, a[T.ITEM].tabIndex = 0, a[T.ITEM].focus();
  }
}
/**
 * @license
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const fe = 200, Q = /* @__PURE__ */ new Set([
  S.ArrowDown,
  S.ArrowUp,
  S.Home,
  S.End
]), ye = /* @__PURE__ */ new Set([
  S.ArrowLeft,
  S.ArrowRight,
  ...Q
]);
function ge(g = document) {
  var t;
  let e = g.activeElement;
  for (; e && ((t = e == null ? void 0 : e.shadowRoot) != null && t.activeElement); )
    e = e.shadowRoot.activeElement;
  return e;
}
class l extends te {
  /**
   * Whether the menu is animating upwards or downwards when opening. This is
   * helpful for calculating some animation calculations.
   */
  get openDirection() {
    return this.menuCorner.split("-")[0] === "start" ? "DOWN" : "UP";
  }
  /**
   * The element which the menu should align to. If `anchor` is set to a
   * non-empty idref string, then `anchorEl` will resolve to the element with
   * the given id in the same root node. Otherwise, `null`.
   */
  get anchorElement() {
    return this.anchor ? this.getRootNode().querySelector(`#${this.anchor}`) : this.currentAnchorElement;
  }
  set anchorElement(e) {
    this.currentAnchorElement = e, this.requestUpdate("anchorElement");
  }
  constructor() {
    super(), this.anchor = "", this.positioning = "absolute", this.quick = !1, this.hasOverflow = !1, this.open = !1, this.xOffset = 0, this.yOffset = 0, this.noHorizontalFlip = !1, this.noVerticalFlip = !1, this.typeaheadDelay = fe, this.anchorCorner = X.END_START, this.menuCorner = X.START_START, this.stayOpenOnOutsideClick = !1, this.stayOpenOnFocusout = !1, this.skipRestoreFocus = !1, this.defaultFocus = B.FIRST_ITEM, this.noNavigationWrap = !1, this.typeaheadActive = !0, this.isSubmenu = !1, this.pointerPath = [], this.isRepositioning = !1, this.openCloseAnimationSignal = ie(), this.listController = new ne({
      isItem: (e) => e.hasAttribute("md-menu-item"),
      getPossibleItems: () => this.slotItems,
      isRtl: () => getComputedStyle(this).direction === "rtl",
      deactivateItem: (e) => {
        e.selected = !1, e.tabIndex = -1;
      },
      activateItem: (e) => {
        e.selected = !0, e.tabIndex = 0;
      },
      isNavigableKey: (e) => {
        if (!this.isSubmenu)
          return ye.has(e);
        const i = getComputedStyle(this).direction === "rtl" ? S.ArrowLeft : S.ArrowRight;
        return e === i ? !0 : Q.has(e);
      },
      wrapNavigation: () => !this.noNavigationWrap
    }), this.lastFocusedElement = null, this.typeaheadController = new me(() => ({
      getItems: () => this.items,
      typeaheadBufferTime: this.typeaheadDelay,
      active: this.typeaheadActive
    })), this.currentAnchorElement = null, this.internals = // Cast needed for closure
    this.attachInternals(), this.menuPositionController = new ue(this, () => ({
      anchorCorner: this.anchorCorner,
      surfaceCorner: this.menuCorner,
      surfaceEl: this.surfaceEl,
      anchorEl: this.anchorElement,
      positioning: this.positioning === "popover" ? "document" : this.positioning,
      isOpen: this.open,
      xOffset: this.xOffset,
      yOffset: this.yOffset,
      disableBlockFlip: this.noVerticalFlip,
      disableInlineFlip: this.noHorizontalFlip,
      onOpen: this.onOpened,
      beforeClose: this.beforeClose,
      onClose: this.onClosed,
      // We can't resize components that have overflow like menus with
      // submenus because the overflow-y will show menu items / content
      // outside the bounds of the menu. Popover API fixes this because each
      // submenu is hoisted to the top-layer and are not considered overflow
      // content.
      repositionStrategy: this.hasOverflow && this.positioning !== "popover" ? "move" : "resize"
    })), this.onWindowResize = () => {
      this.isRepositioning || this.positioning !== "document" && this.positioning !== "fixed" && this.positioning !== "popover" || (this.isRepositioning = !0, this.reposition(), this.isRepositioning = !1);
    }, this.handleFocusout = async (e) => {
      const t = this.anchorElement;
      if (this.stayOpenOnFocusout || !this.open || this.pointerPath.includes(t))
        return;
      if (e.relatedTarget) {
        if (G(e.relatedTarget, this) || this.pointerPath.length !== 0 && G(e.relatedTarget, t))
          return;
      } else if (this.pointerPath.includes(this))
        return;
      const i = this.skipRestoreFocus;
      this.skipRestoreFocus = !0, this.close(), await this.updateComplete, this.skipRestoreFocus = i;
    }, this.onOpened = async () => {
      this.lastFocusedElement = ge();
      const e = this.items, t = se(e);
      t && this.defaultFocus !== B.NONE && (t.item.tabIndex = -1);
      let i = !this.quick;
      switch (this.quick ? this.dispatchEvent(new Event("opening")) : i = !!await this.animateOpen(), this.defaultFocus) {
        case B.FIRST_ITEM:
          const s = ae(e);
          s && (s.tabIndex = 0, s.focus(), await s.updateComplete);
          break;
        case B.LAST_ITEM:
          const n = oe(e);
          n && (n.tabIndex = 0, n.focus(), await n.updateComplete);
          break;
        case B.LIST_ROOT:
          this.focus();
          break;
        default:
        case B.NONE:
          break;
      }
      i || this.dispatchEvent(new Event("opened"));
    }, this.beforeClose = async () => {
      var e, t;
      this.open = !1, this.skipRestoreFocus || (t = (e = this.lastFocusedElement) == null ? void 0 : e.focus) == null || t.call(e), this.quick || await this.animateClose();
    }, this.onClosed = () => {
      this.quick && (this.dispatchEvent(new Event("closing")), this.dispatchEvent(new Event("closed")));
    }, this.onWindowPointerdown = (e) => {
      this.pointerPath = e.composedPath();
    }, this.onDocumentClick = (e) => {
      if (!this.open)
        return;
      const t = e.composedPath();
      !this.stayOpenOnOutsideClick && !t.includes(this) && !t.includes(this.anchorElement) && (this.open = !1);
    }, this.internals.role = "menu", this.addEventListener("keydown", this.handleKeydown), this.addEventListener("keydown", this.captureKeydown, { capture: !0 }), this.addEventListener("focusout", this.handleFocusout);
  }
  /**
   * The menu items associated with this menu. The items must be `MenuItem`s and
   * have both the `md-menu-item` and `md-list-item` attributes.
   */
  get items() {
    return this.listController.items;
  }
  willUpdate(e) {
    if (e.has("open")) {
      if (this.open) {
        this.removeAttribute("aria-hidden");
        return;
      }
      this.setAttribute("aria-hidden", "true");
    }
  }
  update(e) {
    e.has("open") && (this.open ? this.setUpGlobalEventListeners() : this.cleanUpGlobalEventListeners()), e.has("positioning") && this.positioning === "popover" && // type required for Google JS conformance
    !this.showPopover && (this.positioning = "fixed"), super.update(e);
  }
  connectedCallback() {
    super.connectedCallback(), this.open && this.setUpGlobalEventListeners();
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this.cleanUpGlobalEventListeners();
  }
  getBoundingClientRect() {
    return this.surfaceEl ? this.surfaceEl.getBoundingClientRect() : super.getBoundingClientRect();
  }
  getClientRects() {
    return this.surfaceEl ? this.surfaceEl.getClientRects() : super.getClientRects();
  }
  render() {
    return this.renderSurface();
  }
  /**
   * Renders the positionable surface element and its contents.
   */
  renderSurface() {
    return z`
      <div
        class="menu ${re(this.getSurfaceClasses())}"
        style=${de(this.menuPositionController.surfaceStyles)}
        popover=${this.positioning === "popover" ? "manual" : le}>
        ${this.renderElevation()}
        <div class="items">
          <div class="item-padding"> ${this.renderMenuItems()} </div>
        </div>
      </div>
    `;
  }
  /**
   * Renders the menu items' slot
   */
  renderMenuItems() {
    return z`<slot
      @close-menu=${this.onCloseMenu}
      @deactivate-items=${this.onDeactivateItems}
      @request-activation=${this.onRequestActivation}
      @deactivate-typeahead=${this.handleDeactivateTypeahead}
      @activate-typeahead=${this.handleActivateTypeahead}
      @stay-open-on-focusout=${this.handleStayOpenOnFocusout}
      @close-on-focusout=${this.handleCloseOnFocusout}
      @slotchange=${this.listController.onSlotchange}></slot>`;
  }
  /**
   * Renders the elevation component.
   */
  renderElevation() {
    return z`<md-elevation part="elevation"></md-elevation>`;
  }
  getSurfaceClasses() {
    return {
      open: this.open,
      fixed: this.positioning === "fixed",
      "has-overflow": this.hasOverflow
    };
  }
  captureKeydown(e) {
    e.target === this && !e.defaultPrevented && Z(e.code) && (e.preventDefault(), this.close()), this.typeaheadController.onKeydown(e);
  }
  /**
   * Performs the opening animation:
   *
   * https://direct.googleplex.com/#/spec/295000003+271060003
   *
   * @return A promise that resolve to `true` if the animation was aborted,
   *     `false` if it was not aborted.
   */
  async animateOpen() {
    const e = this.surfaceEl, t = this.slotEl;
    if (!e || !t)
      return !0;
    const i = this.openDirection;
    this.dispatchEvent(new Event("opening")), e.classList.toggle("animating", !0);
    const s = this.openCloseAnimationSignal.start(), n = e.offsetHeight, p = i === "UP", a = this.items, o = 500, m = 50, v = 250, I = (o - v) / a.length, w = e.animate([{ height: "0px" }, { height: `${n}px` }], {
      duration: o,
      easing: M.EMPHASIZED
    }), b = t.animate([
      { transform: p ? `translateY(-${n}px)` : "" },
      { transform: "" }
    ], { duration: o, easing: M.EMPHASIZED }), C = e.animate([{ opacity: 0 }, { opacity: 1 }], m), c = [];
    for (let d = 0; d < a.length; d++) {
      const E = p ? a.length - 1 - d : d, y = a[E], h = y.animate([{ opacity: 0 }, { opacity: 1 }], {
        duration: v,
        delay: I * d
      });
      y.classList.toggle("md-menu-hidden", !0), h.addEventListener("finish", () => {
        y.classList.toggle("md-menu-hidden", !1);
      }), c.push([y, h]);
    }
    let f = (d) => {
    };
    const x = new Promise((d) => {
      f = d;
    });
    return s.addEventListener("abort", () => {
      w.cancel(), b.cancel(), C.cancel(), c.forEach(([d, E]) => {
        d.classList.toggle("md-menu-hidden", !1), E.cancel();
      }), f(!0);
    }), w.addEventListener("finish", () => {
      e.classList.toggle("animating", !1), this.openCloseAnimationSignal.finish(), f(!1);
    }), await x;
  }
  /**
   * Performs the closing animation:
   *
   * https://direct.googleplex.com/#/spec/295000003+271060003
   */
  animateClose() {
    let e;
    const t = new Promise((h) => {
      e = h;
    }), i = this.surfaceEl, s = this.slotEl;
    if (!i || !s)
      return e(!1), t;
    const p = this.openDirection === "UP";
    this.dispatchEvent(new Event("closing")), i.classList.toggle("animating", !0);
    const a = this.openCloseAnimationSignal.start(), o = i.offsetHeight, m = this.items, v = 150, I = 50, w = v - I, b = 50, C = 50, c = 0.35, f = (v - C - b) / m.length, x = i.animate([
      { height: `${o}px` },
      { height: `${o * c}px` }
    ], {
      duration: v,
      easing: M.EMPHASIZED_ACCELERATE
    }), d = s.animate([
      { transform: "" },
      {
        transform: p ? `translateY(-${o * (1 - c)}px)` : ""
      }
    ], { duration: v, easing: M.EMPHASIZED_ACCELERATE }), E = i.animate([{ opacity: 1 }, { opacity: 0 }], { duration: I, delay: w }), y = [];
    for (let h = 0; h < m.length; h++) {
      const R = p ? h : m.length - 1 - h, k = m[R], L = k.animate([{ opacity: 1 }, { opacity: 0 }], {
        duration: b,
        delay: C + f * h
      });
      L.addEventListener("finish", () => {
        k.classList.toggle("md-menu-hidden", !0);
      }), y.push([k, L]);
    }
    return a.addEventListener("abort", () => {
      x.cancel(), d.cancel(), E.cancel(), y.forEach(([h, R]) => {
        R.cancel(), h.classList.toggle("md-menu-hidden", !1);
      }), e(!1);
    }), x.addEventListener("finish", () => {
      i.classList.toggle("animating", !1), y.forEach(([h]) => {
        h.classList.toggle("md-menu-hidden", !1);
      }), this.openCloseAnimationSignal.finish(), this.dispatchEvent(new Event("closed")), e(!0);
    }), t;
  }
  handleKeydown(e) {
    this.pointerPath = [], this.listController.handleKeydown(e);
  }
  setUpGlobalEventListeners() {
    document.addEventListener("click", this.onDocumentClick, { capture: !0 }), window.addEventListener("pointerdown", this.onWindowPointerdown), document.addEventListener("resize", this.onWindowResize, { passive: !0 }), window.addEventListener("resize", this.onWindowResize, { passive: !0 });
  }
  cleanUpGlobalEventListeners() {
    document.removeEventListener("click", this.onDocumentClick, {
      capture: !0
    }), window.removeEventListener("pointerdown", this.onWindowPointerdown), document.removeEventListener("resize", this.onWindowResize), window.removeEventListener("resize", this.onWindowResize);
  }
  onCloseMenu() {
    this.close();
  }
  onDeactivateItems(e) {
    e.stopPropagation(), this.listController.onDeactivateItems();
  }
  onRequestActivation(e) {
    e.stopPropagation(), this.listController.onRequestActivation(e);
  }
  handleDeactivateTypeahead(e) {
    e.stopPropagation(), this.typeaheadActive = !1;
  }
  handleActivateTypeahead(e) {
    e.stopPropagation(), this.typeaheadActive = !0;
  }
  handleStayOpenOnFocusout(e) {
    e.stopPropagation(), this.stayOpenOnFocusout = !0;
  }
  handleCloseOnFocusout(e) {
    e.stopPropagation(), this.stayOpenOnFocusout = !1;
  }
  close() {
    this.open = !1, this.slotItems.forEach((t) => {
      var i;
      (i = t.close) == null || i.call(t);
    });
  }
  show() {
    this.open = !0;
  }
  /**
   * Activates the next item in the menu. If at the end of the menu, the first
   * item will be activated.
   *
   * @return The activated menu item or `null` if there are no items.
   */
  activateNextItem() {
    return this.listController.activateNextItem() ?? null;
  }
  /**
   * Activates the previous item in the menu. If at the start of the menu, the
   * last item will be activated.
   *
   * @return The activated menu item or `null` if there are no items.
   */
  activatePreviousItem() {
    return this.listController.activatePreviousItem() ?? null;
  }
  /**
   * Repositions the menu if it is open.
   *
   * Useful for the case where document or window-positioned menus have their
   * anchors moved while open.
   */
  reposition() {
    this.open && this.menuPositionController.position();
  }
}
r([
  j(".menu")
], l.prototype, "surfaceEl", void 0);
r([
  j("slot")
], l.prototype, "slotEl", void 0);
r([
  u()
], l.prototype, "anchor", void 0);
r([
  u()
], l.prototype, "positioning", void 0);
r([
  u({ type: Boolean })
], l.prototype, "quick", void 0);
r([
  u({ type: Boolean, attribute: "has-overflow" })
], l.prototype, "hasOverflow", void 0);
r([
  u({ type: Boolean, reflect: !0 })
], l.prototype, "open", void 0);
r([
  u({ type: Number, attribute: "x-offset" })
], l.prototype, "xOffset", void 0);
r([
  u({ type: Number, attribute: "y-offset" })
], l.prototype, "yOffset", void 0);
r([
  u({ type: Boolean, attribute: "no-horizontal-flip" })
], l.prototype, "noHorizontalFlip", void 0);
r([
  u({ type: Boolean, attribute: "no-vertical-flip" })
], l.prototype, "noVerticalFlip", void 0);
r([
  u({ type: Number, attribute: "typeahead-delay" })
], l.prototype, "typeaheadDelay", void 0);
r([
  u({ attribute: "anchor-corner" })
], l.prototype, "anchorCorner", void 0);
r([
  u({ attribute: "menu-corner" })
], l.prototype, "menuCorner", void 0);
r([
  u({ type: Boolean, attribute: "stay-open-on-outside-click" })
], l.prototype, "stayOpenOnOutsideClick", void 0);
r([
  u({ type: Boolean, attribute: "stay-open-on-focusout" })
], l.prototype, "stayOpenOnFocusout", void 0);
r([
  u({ type: Boolean, attribute: "skip-restore-focus" })
], l.prototype, "skipRestoreFocus", void 0);
r([
  u({ attribute: "default-focus" })
], l.prototype, "defaultFocus", void 0);
r([
  u({ type: Boolean, attribute: "no-navigation-wrap" })
], l.prototype, "noNavigationWrap", void 0);
r([
  J({ flatten: !0 })
], l.prototype, "slotItems", void 0);
r([
  ee()
], l.prototype, "typeaheadActive", void 0);
/**
 * @license
 * Copyright 2024 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const ve = V`:host{--md-elevation-level: var(--md-menu-container-elevation, 2);--md-elevation-shadow-color: var(--md-menu-container-shadow-color, var(--md-sys-color-shadow, #000));min-width:112px;color:unset;display:contents}md-focus-ring{--md-focus-ring-shape: var(--md-menu-container-shape, var(--md-sys-shape-corner-extra-small, 4px))}.menu{border-radius:var(--md-menu-container-shape, var(--md-sys-shape-corner-extra-small, 4px));display:none;inset:auto;border:none;padding:0px;overflow:visible;background-color:rgba(0,0,0,0);color:inherit;opacity:0;z-index:20;position:absolute;user-select:none;max-height:inherit;height:inherit;min-width:inherit;max-width:inherit;scrollbar-width:inherit}.menu::backdrop{display:none}.fixed{position:fixed}.items{display:block;list-style-type:none;margin:0;outline:none;box-sizing:border-box;background-color:var(--md-menu-container-color, var(--md-sys-color-surface-container, #f3edf7));height:inherit;max-height:inherit;overflow:auto;min-width:inherit;max-width:inherit;border-radius:inherit;scrollbar-width:inherit}.item-padding{padding-block:8px}.has-overflow:not([popover]) .items{overflow:visible}.has-overflow.animating .items,.animating .items{overflow:hidden}.has-overflow.animating .items{pointer-events:none}.animating ::slotted(.md-menu-hidden){opacity:0}slot{display:block;height:inherit;max-height:inherit}::slotted(:is(md-divider,[role=separator])){margin:8px 0}@media(forced-colors: active){.menu{border-style:solid;border-color:CanvasText;border-width:1px}}
`;
/**
 * @license
 * Copyright 2022 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
let $ = class extends l {
};
$.styles = [ve];
$ = r([
  ce("md-menu")
], $);
export {
  fe as D,
  B as F,
  Ce as M,
  T,
  we as a,
  G as i,
  Te as s
};
