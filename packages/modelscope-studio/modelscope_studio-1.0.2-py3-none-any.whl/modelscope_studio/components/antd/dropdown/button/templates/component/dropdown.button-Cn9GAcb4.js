import { g as re, w as R, d as oe, a as I } from "./Index-C8tL3xS6.js";
const y = window.ms_globals.React, k = window.ms_globals.React.useMemo, q = window.ms_globals.React.useState, J = window.ms_globals.React.useEffect, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, T = window.ms_globals.ReactDOM.createPortal, se = window.ms_globals.antd.Dropdown;
var Y = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var le = y, ce = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ue = Object.prototype.hasOwnProperty, ae = le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Q(n, e, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (l in e) ue.call(e, l) && !de.hasOwnProperty(l) && (o[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) o[l] === void 0 && (o[l] = e[l]);
  return {
    $$typeof: ce,
    type: n,
    key: t,
    ref: s,
    props: o,
    _owner: ae.current
  };
}
O.Fragment = ie;
O.jsx = Q;
O.jsxs = Q;
Y.exports = O;
var b = Y.exports;
const {
  SvelteComponent: fe,
  assign: N,
  binding_callbacks: D,
  check_outros: pe,
  children: X,
  claim_element: Z,
  claim_space: _e,
  component_subscribe: W,
  compute_slots: me,
  create_slot: he,
  detach: E,
  element: K,
  empty: B,
  exclude_internal_props: M,
  get_all_dirty_from_scope: ge,
  get_slot_changes: we,
  group_outros: be,
  init: ye,
  insert_hydration: S,
  safe_not_equal: ve,
  set_custom_element_data: $,
  space: Ee,
  transition_in: C,
  transition_out: F,
  update_slot_base: xe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ie,
  getContext: Re,
  onDestroy: Se,
  setContext: Ce
} = window.__gradio__svelte__internal;
function z(n) {
  let e, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = he(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = K("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = Z(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = X(e);
      o && o.l(s), s.forEach(E), this.h();
    },
    h() {
      $(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      S(t, e, s), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && xe(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? we(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : ge(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (C(o, t), r = !0);
    },
    o(t) {
      F(o, t), r = !1;
    },
    d(t) {
      t && E(e), o && o.d(t), n[9](null);
    }
  };
}
function ke(n) {
  let e, r, l, o, t = (
    /*$$slots*/
    n[4].default && z(n)
  );
  return {
    c() {
      e = K("react-portal-target"), r = Ee(), t && t.c(), l = B(), this.h();
    },
    l(s) {
      e = Z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), X(e).forEach(E), r = _e(s), t && t.l(s), l = B(), this.h();
    },
    h() {
      $(e, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      S(s, e, i), n[8](e), S(s, r, i), t && t.m(s, i), S(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && C(t, 1)) : (t = z(s), t.c(), C(t, 1), t.m(l.parentNode, l)) : t && (be(), F(t, 1, 1, () => {
        t = null;
      }), pe());
    },
    i(s) {
      o || (C(t), o = !0);
    },
    o(s) {
      F(t), o = !1;
    },
    d(s) {
      s && (E(e), E(r), E(l)), n[8](null), t && t.d(s);
    }
  };
}
function G(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Oe(n, e, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const i = me(t);
  let {
    svelteInit: c
  } = e;
  const w = R(G(e)), a = R();
  W(n, a, (d) => r(0, l = d));
  const f = R();
  W(n, f, (d) => r(1, o = d));
  const u = [], p = Re("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: h,
    subSlotIndex: m
  } = re() || {}, g = c({
    parent: p,
    props: w,
    target: a,
    slot: f,
    slotKey: _,
    slotIndex: h,
    subSlotIndex: m,
    onDestroy(d) {
      u.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", g), Ie(() => {
    w.set(G(e));
  }), Se(() => {
    u.forEach((d) => d());
  });
  function v(d) {
    D[d ? "unshift" : "push"](() => {
      l = d, a.set(l);
    });
  }
  function P(d) {
    D[d ? "unshift" : "push"](() => {
      o = d, f.set(o);
    });
  }
  return n.$$set = (d) => {
    r(17, e = N(N({}, e), M(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, e = M(e), [l, o, a, f, i, c, s, t, v, P];
}
class Pe extends fe {
  constructor(e) {
    super(), ye(this, e, Oe, ke, ve, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, j = window.ms_globals.tree;
function je(n) {
  function e(r) {
    const l = R(), o = new Pe({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? j;
          return i.nodes = [...i.nodes, s], U({
            createPortal: T,
            node: j
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), U({
              createPortal: T,
              node: j
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
function Le(n) {
  const [e, r] = q(() => I(n));
  return J(() => {
    let l = !0;
    return n.subscribe((t) => {
      l && (l = !1, t === e) || r(t);
    });
  }, [n]), e;
}
function Te(n) {
  const e = k(() => oe(n, (r) => r), [n]);
  return Le(e);
}
const Fe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const l = n[r];
    return typeof l == "number" && !Fe.includes(r) ? e[r] = l + "px" : e[r] = l, e;
  }, {}) : {};
}
function A(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(T(y.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: y.Children.toArray(n._reactElement.props.children).map((o) => {
        if (y.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = A(o.props.el);
          return y.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...y.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: s,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = A(t);
      e.push(...i), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Ne(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const x = te(({
  slot: n,
  clone: e,
  className: r,
  style: l
}, o) => {
  const t = ne(), [s, i] = q([]);
  return J(() => {
    var f;
    if (!t.current || !n)
      return;
    let c = n;
    function w() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Ne(o, u), r && u.classList.add(...r.split(" ")), l) {
        const p = Ae(l);
        Object.keys(p).forEach((_) => {
          u.style[_] = p[_];
        });
      }
    }
    let a = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var m, g, v;
        (m = t.current) != null && m.contains(c) && ((g = t.current) == null || g.removeChild(c));
        const {
          portals: _,
          clonedElement: h
        } = A(n);
        return c = h, i(_), c.style.display = "contents", w(), (v = t.current) == null || v.appendChild(c), _.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", w(), (f = t.current) == null || f.appendChild(c);
    return () => {
      var u, p;
      c.style.display = "", (u = t.current) != null && u.contains(c) && ((p = t.current) == null || p.removeChild(c)), a == null || a.disconnect();
    };
  }, [n, e, r, l, o]), y.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function De(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function We(n, e = !1) {
  try {
    if (e && !De(n))
      return;
    if (typeof n == "string") {
      let r = n.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function L(n, e) {
  return k(() => We(n, e), [n, e]);
}
function H(n, e) {
  const r = k(() => y.Children.toArray(n).filter((t) => t.props.node && (!e && !t.props.nodeSlotKey || e && e === t.props.nodeSlotKey)).sort((t, s) => {
    if (t.props.node.slotIndex && s.props.node.slotIndex) {
      const i = I(t.props.node.slotIndex) || 0, c = I(s.props.node.slotIndex) || 0;
      return i - c === 0 && t.props.node.subSlotIndex && s.props.node.subSlotIndex ? (I(t.props.node.subSlotIndex) || 0) - (I(s.props.node.subSlotIndex) || 0) : i - c;
    }
    return 0;
  }).map((t) => t.props.node.target), [n, e]);
  return Te(r);
}
function ee(n, e, r) {
  const l = n.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, t) => {
      var w;
      if (typeof o != "object")
        return e != null && e.fallback ? e.fallback(o) : o;
      const s = {
        ...o.props,
        key: ((w = o.props) == null ? void 0 : w.key) ?? (r ? `${r}-${t}` : `${t}`)
      };
      let i = s;
      Object.keys(o.slots).forEach((a) => {
        if (!o.slots[a] || !(o.slots[a] instanceof Element) && !o.slots[a].el)
          return;
        const f = a.split(".");
        f.forEach((m, g) => {
          i[m] || (i[m] = {}), g !== f.length - 1 && (i = s[m]);
        });
        const u = o.slots[a];
        let p, _, h = (e == null ? void 0 : e.clone) ?? !1;
        u instanceof Element ? p = u : (p = u.el, _ = u.callback, h = u.clone ?? h), i[f[f.length - 1]] = p ? _ ? (...m) => (_(f[f.length - 1], m), /* @__PURE__ */ b.jsx(x, {
          slot: p,
          clone: h
        })) : /* @__PURE__ */ b.jsx(x, {
          slot: p,
          clone: h
        }) : i[f[f.length - 1]], i = s;
      });
      const c = (e == null ? void 0 : e.children) || "children";
      return o[c] && (s[c] = ee(o[c], e, `${t}`)), s;
    });
}
function Be(n, e) {
  return n ? /* @__PURE__ */ b.jsx(x, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function V({
  key: n,
  setSlotParams: e,
  slots: r
}, l) {
  return r[n] ? (...o) => (e(n, o), Be(r[n], {
    clone: !0,
    ...l
  })) : void 0;
}
const ze = je(({
  getPopupContainer: n,
  slots: e,
  menuItems: r,
  children: l,
  dropdownRender: o,
  buttonsRender: t,
  setSlotParams: s,
  value: i,
  ...c
}) => {
  var _, h, m;
  const w = L(n), a = L(o), f = L(t), u = H(l, "buttonsRender"), p = H(l);
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [/* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: p.length > 0 ? null : l
    }), /* @__PURE__ */ b.jsx(se.Button, {
      ...c,
      buttonsRender: u.length ? (...g) => (s("buttonsRender", g), u.map((v, P) => /* @__PURE__ */ b.jsx(x, {
        slot: v
      }, P))) : f,
      menu: {
        ...c.menu,
        items: k(() => {
          var g;
          return ((g = c.menu) == null ? void 0 : g.items) || ee(r, {
            clone: !0
          }) || [];
        }, [r, (_ = c.menu) == null ? void 0 : _.items]),
        expandIcon: e["menu.expandIcon"] ? V({
          slots: e,
          setSlotParams: s,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) : (h = c.menu) == null ? void 0 : h.expandIcon,
        overflowedIndicator: e["menu.overflowedIndicator"] ? /* @__PURE__ */ b.jsx(x, {
          slot: e["menu.overflowedIndicator"]
        }) : (m = c.menu) == null ? void 0 : m.overflowedIndicator
      },
      getPopupContainer: w,
      dropdownRender: e.dropdownRender ? V({
        slots: e,
        setSlotParams: s,
        key: "dropdownRender"
      }) : a,
      icon: e.icon ? /* @__PURE__ */ b.jsx(x, {
        slot: e.icon
      }) : c.icon,
      children: p.length > 0 ? l : i
    })]
  });
});
export {
  ze as DropdownButton,
  ze as default
};
