import { g as $, w as I, d as ee, a as w } from "./Index-CyjwoADP.js";
const m = window.ms_globals.React, G = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, k = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Result;
var K = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = m, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) se.call(t, s) && !ie.hasOwnProperty(s) && (o[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: le.current
  };
}
R.Fragment = oe;
R.jsx = V;
R.jsxs = V;
K.exports = R;
var _ = K.exports;
const {
  SvelteComponent: ae,
  assign: L,
  binding_callbacks: A,
  check_outros: ce,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: N,
  compute_slots: de,
  create_slot: fe,
  detach: g,
  element: J,
  empty: D,
  exclude_internal_props: F,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: S,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: be,
  transition_in: C,
  transition_out: T,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: xe,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function M(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = fe(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = J("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = q(t);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      S(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && we(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (C(o, e), r = !0);
    },
    o(e) {
      T(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      t = J("react-portal-target"), r = be(), e && e.c(), s = D(), this.h();
    },
    l(l) {
      t = B(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(g), r = ue(l), e && e.l(l), s = D(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      S(l, t, a), n[8](t), S(l, r, a), e && e.m(l, a), S(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && C(e, 1)) : (e = M(l), e.c(), C(e, 1), e.m(s.parentNode, s)) : e && (me(), T(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      o || (C(e), o = !0);
    },
    o(l) {
      T(e), o = !1;
    },
    d(l) {
      l && (g(t), g(r), g(s)), n[8](null), e && e.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Se(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = de(e);
  let {
    svelteInit: i
  } = t;
  const b = I(W(t)), d = I();
  N(n, d, (c) => r(0, s = c));
  const h = I();
  N(n, h, (c) => r(1, o = c));
  const u = [], f = xe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: O,
    subSlotIndex: y
  } = $() || {}, x = i({
    parent: f,
    props: b,
    target: d,
    slot: h,
    slotKey: p,
    slotIndex: O,
    subSlotIndex: y,
    onDestroy(c) {
      u.push(c);
    }
  });
  ve("$$ms-gr-react-wrapper", x), ye(() => {
    b.set(W(t));
  }), Ee(() => {
    u.forEach((c) => c());
  });
  function E(c) {
    A[c ? "unshift" : "push"](() => {
      s = c, d.set(s);
    });
  }
  function Q(c) {
    A[c ? "unshift" : "push"](() => {
      o = c, h.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = L(L({}, t), F(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, l = c.$$scope);
  }, t = F(t), [s, o, d, h, a, i, l, e, E, Q];
}
class Ce extends ae {
  constructor(t) {
    super(), he(this, t, Se, Ie, ge, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, P = window.ms_globals.tree;
function Re(n) {
  function t(r) {
    const s = I(), o = new Ce({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? P;
          return a.nodes = [...a.nodes, l], z({
            createPortal: k,
            node: P
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), z({
              createPortal: k,
              node: P
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function Oe(n) {
  const [t, r] = U(() => w(n));
  return H(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function Pe(n) {
  const t = G(() => ee(n, (r) => r), [n]);
  return Oe(t);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Te(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !ke.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function j(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(k(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(o.props.el);
          return m.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...m.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = j(e);
      t.push(...a), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function je(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const v = X(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = Z(), [l, a] = U([]);
  return H(() => {
    var h;
    if (!e.current || !n)
      return;
    let i = n;
    function b() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), je(o, u), r && u.classList.add(...r.split(" ")), s) {
        const f = Te(s);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var y, x, E;
        (y = e.current) != null && y.contains(i) && ((x = e.current) == null || x.removeChild(i));
        const {
          portals: p,
          clonedElement: O
        } = j(n);
        return i = O, a(p), i.style.display = "contents", b(), (E = e.current) == null || E.appendChild(i), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", b(), (h = e.current) == null || h.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, r, s, o]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Le(n, t) {
  const r = G(() => m.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const a = w(e.props.node.slotIndex) || 0, i = w(l.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (w(e.props.node.subSlotIndex) || 0) - (w(l.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Pe(r);
}
const Ne = Re(({
  slots: n,
  children: t,
  ...r
}) => {
  const s = Le(t);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: s.length > 0 ? null : t
    }), /* @__PURE__ */ _.jsx(te, {
      ...r,
      extra: n.extra ? /* @__PURE__ */ _.jsx(v, {
        slot: n.extra
      }) : r.extra,
      icon: n.icon ? /* @__PURE__ */ _.jsx(v, {
        slot: n.icon
      }) : r.icon,
      subTitle: n.subTitle ? /* @__PURE__ */ _.jsx(v, {
        slot: n.subTitle
      }) : r.subTitle,
      title: n.title ? /* @__PURE__ */ _.jsx(v, {
        slot: n.title
      }) : r.title,
      children: s.length > 0 ? t : null
    })]
  });
});
export {
  Ne as Result,
  Ne as default
};
