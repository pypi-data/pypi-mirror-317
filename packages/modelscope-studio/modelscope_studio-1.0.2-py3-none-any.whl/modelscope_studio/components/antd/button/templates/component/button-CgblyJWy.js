import { g as Z, w as x, d as $, a as b } from "./Index-BBCOjs4f.js";
const _ = window.ms_globals.React, W = window.ms_globals.React.useMemo, z = window.ms_globals.React.useState, G = window.ms_globals.React.useEffect, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, P = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Button;
var U = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = _, ne = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) re.call(t, s) && !le.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: se.current
  };
}
C.Fragment = oe;
C.jsx = H;
C.jsxs = H;
U.exports = C;
var w = U.exports;
const {
  SvelteComponent: ie,
  assign: T,
  binding_callbacks: j,
  check_outros: ae,
  children: K,
  claim_element: V,
  claim_space: ce,
  component_subscribe: A,
  compute_slots: de,
  create_slot: ue,
  detach: h,
  element: q,
  empty: N,
  exclude_internal_props: D,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: I,
  safe_not_equal: he,
  set_custom_element_data: J,
  space: ge,
  transition_in: S,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function B(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ue(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = V(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = K(t);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      I(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && we(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? pe(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (S(r, e), o = !0);
    },
    o(e) {
      k(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && B(n)
  );
  return {
    c() {
      t = q("react-portal-target"), o = ge(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      t = V(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(t).forEach(h), o = ce(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      I(l, t, a), n[8](t), I(l, o, a), e && e.m(l, a), I(l, s, a), r = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && S(e, 1)) : (e = B(l), e.c(), S(e, 1), e.m(s.parentNode, s)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      r || (S(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (h(t), h(o), h(s)), n[8](null), e && e.d(l);
    }
  };
}
function F(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ie(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = de(e);
  let {
    svelteInit: i
  } = t;
  const g = x(F(t)), u = x();
  A(n, u, (c) => o(0, s = c));
  const m = x();
  A(n, m, (c) => o(1, r = c));
  const d = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y
  } = Z() || {}, E = i({
    parent: f,
    props: g,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y,
    onDestroy(c) {
      d.push(c);
    }
  });
  ve("$$ms-gr-react-wrapper", E), be(() => {
    g.set(F(t));
  }), Ee(() => {
    d.forEach((c) => c());
  });
  function v(c) {
    j[c ? "unshift" : "push"](() => {
      s = c, u.set(s);
    });
  }
  function Y(c) {
    j[c ? "unshift" : "push"](() => {
      r = c, m.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = T(T({}, t), D(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, l = c.$$scope);
  }, t = D(t), [s, r, u, m, a, i, l, e, v, Y];
}
class Se extends ie {
  constructor(t) {
    super(), me(this, t, Ie, xe, he, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const s = x(), r = new Se({
      ...o,
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
          }, a = e.parent ?? O;
          return a.nodes = [...a.nodes, l], M({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), M({
              createPortal: P,
              node: O
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function Re(n) {
  const [t, o] = z(() => b(n));
  return G(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Oe(n) {
  const t = W(() => $(n, (o) => o), [n]);
  return Re(t);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !Pe.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function L(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(_.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: _.Children.toArray(n._reactElement.props.children).map((r) => {
        if (_.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = L(r.props.el);
          return _.cloneElement(r, {
            ...r.props,
            el: l,
            children: [..._.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = L(e);
      t.push(...a), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Le(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Te = Q(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = X(), [l, a] = z([]);
  return G(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Le(r, d), o && d.classList.add(...o.split(" ")), s) {
        const f = ke(s);
        Object.keys(f).forEach((p) => {
          d.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var y, E, v;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: R
        } = L(n);
        return i = R, a(p), i.style.display = "contents", g(), (v = e.current) == null || v.appendChild(i), p.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, o, s, r]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(n, t) {
  const o = W(() => _.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const a = b(e.props.node.slotIndex) || 0, i = b(l.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (b(e.props.node.subSlotIndex) || 0) - (b(l.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Oe(o);
}
const Ne = Ce(({
  slots: n,
  value: t,
  children: o,
  ...s
}) => {
  const r = je(o);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: r.length > 0 ? null : o
    }), /* @__PURE__ */ w.jsx(ee, {
      ...s,
      icon: n.icon ? /* @__PURE__ */ w.jsx(Te, {
        slot: n.icon
      }) : s.icon,
      children: r.length > 0 ? o : t
    })]
  });
});
export {
  Ne as Button,
  Ne as default
};
