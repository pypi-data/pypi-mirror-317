var Pt = typeof global == "object" && global && global.Object === Object && global, sn = typeof self == "object" && self && self.Object === Object && self, S = Pt || sn || Function("return this")(), A = S.Symbol, wt = Object.prototype, an = wt.hasOwnProperty, un = wt.toString, H = A ? A.toStringTag : void 0;
function fn(e) {
  var t = an.call(e, H), n = e[H];
  try {
    e[H] = void 0;
    var r = !0;
  } catch {
  }
  var i = un.call(e);
  return r && (t ? e[H] = n : delete e[H]), i;
}
var ln = Object.prototype, cn = ln.toString;
function dn(e) {
  return cn.call(e);
}
var gn = "[object Null]", pn = "[object Undefined]", qe = A ? A.toStringTag : void 0;
function N(e) {
  return e == null ? e === void 0 ? pn : gn : qe && qe in Object(e) ? fn(e) : dn(e);
}
function j(e) {
  return e != null && typeof e == "object";
}
var _n = "[object Symbol]";
function Ae(e) {
  return typeof e == "symbol" || j(e) && N(e) == _n;
}
function xt(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = Array(r); ++n < r; )
    i[n] = t(e[n], n, e);
  return i;
}
var w = Array.isArray, yn = 1 / 0, Ye = A ? A.prototype : void 0, Xe = Ye ? Ye.toString : void 0;
function St(e) {
  if (typeof e == "string")
    return e;
  if (w(e))
    return xt(e, St) + "";
  if (Ae(e))
    return Xe ? Xe.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -yn ? "-0" : t;
}
function z(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function $t(e) {
  return e;
}
var bn = "[object AsyncFunction]", hn = "[object Function]", mn = "[object GeneratorFunction]", vn = "[object Proxy]";
function Ct(e) {
  if (!z(e))
    return !1;
  var t = N(e);
  return t == hn || t == mn || t == bn || t == vn;
}
var ge = S["__core-js_shared__"], Je = function() {
  var e = /[^.]+$/.exec(ge && ge.keys && ge.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function Tn(e) {
  return !!Je && Je in e;
}
var On = Function.prototype, An = On.toString;
function D(e) {
  if (e != null) {
    try {
      return An.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var Pn = /[\\^$.*+?()[\]{}|]/g, wn = /^\[object .+?Constructor\]$/, xn = Function.prototype, Sn = Object.prototype, $n = xn.toString, Cn = Sn.hasOwnProperty, jn = RegExp("^" + $n.call(Cn).replace(Pn, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function En(e) {
  if (!z(e) || Tn(e))
    return !1;
  var t = Ct(e) ? jn : wn;
  return t.test(D(e));
}
function In(e, t) {
  return e == null ? void 0 : e[t];
}
function K(e, t) {
  var n = In(e, t);
  return En(n) ? n : void 0;
}
var be = K(S, "WeakMap"), Ze = Object.create, Mn = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!z(t))
      return {};
    if (Ze)
      return Ze(t);
    e.prototype = t;
    var n = new e();
    return e.prototype = void 0, n;
  };
}();
function Ln(e, t, n) {
  switch (n.length) {
    case 0:
      return e.call(t);
    case 1:
      return e.call(t, n[0]);
    case 2:
      return e.call(t, n[0], n[1]);
    case 3:
      return e.call(t, n[0], n[1], n[2]);
  }
  return e.apply(t, n);
}
function Fn(e, t) {
  var n = -1, r = e.length;
  for (t || (t = Array(r)); ++n < r; )
    t[n] = e[n];
  return t;
}
var Rn = 800, Nn = 16, Dn = Date.now;
function Kn(e) {
  var t = 0, n = 0;
  return function() {
    var r = Dn(), i = Nn - (r - n);
    if (n = r, i > 0) {
      if (++t >= Rn)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function Un(e) {
  return function() {
    return e;
  };
}
var oe = function() {
  try {
    var e = K(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), Gn = oe ? function(e, t) {
  return oe(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: Un(t),
    writable: !0
  });
} : $t, Bn = Kn(Gn);
function zn(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r && t(e[n], n, e) !== !1; )
    ;
  return e;
}
var Hn = 9007199254740991, qn = /^(?:0|[1-9]\d*)$/;
function jt(e, t) {
  var n = typeof e;
  return t = t ?? Hn, !!t && (n == "number" || n != "symbol" && qn.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function Pe(e, t, n) {
  t == "__proto__" && oe ? oe(e, t, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : e[t] = n;
}
function we(e, t) {
  return e === t || e !== e && t !== t;
}
var Yn = Object.prototype, Xn = Yn.hasOwnProperty;
function Et(e, t, n) {
  var r = e[t];
  (!(Xn.call(e, t) && we(r, n)) || n === void 0 && !(t in e)) && Pe(e, t, n);
}
function J(e, t, n, r) {
  var i = !n;
  n || (n = {});
  for (var o = -1, s = t.length; ++o < s; ) {
    var a = t[o], u = void 0;
    u === void 0 && (u = e[a]), i ? Pe(n, a, u) : Et(n, a, u);
  }
  return n;
}
var We = Math.max;
function Jn(e, t, n) {
  return t = We(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var r = arguments, i = -1, o = We(r.length - t, 0), s = Array(o); ++i < o; )
      s[i] = r[t + i];
    i = -1;
    for (var a = Array(t + 1); ++i < t; )
      a[i] = r[i];
    return a[t] = n(s), Ln(e, this, a);
  };
}
var Zn = 9007199254740991;
function xe(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= Zn;
}
function It(e) {
  return e != null && xe(e.length) && !Ct(e);
}
var Wn = Object.prototype;
function Se(e) {
  var t = e && e.constructor, n = typeof t == "function" && t.prototype || Wn;
  return e === n;
}
function Qn(e, t) {
  for (var n = -1, r = Array(e); ++n < e; )
    r[n] = t(n);
  return r;
}
var Vn = "[object Arguments]";
function Qe(e) {
  return j(e) && N(e) == Vn;
}
var Mt = Object.prototype, kn = Mt.hasOwnProperty, er = Mt.propertyIsEnumerable, $e = Qe(/* @__PURE__ */ function() {
  return arguments;
}()) ? Qe : function(e) {
  return j(e) && kn.call(e, "callee") && !er.call(e, "callee");
};
function tr() {
  return !1;
}
var Lt = typeof exports == "object" && exports && !exports.nodeType && exports, Ve = Lt && typeof module == "object" && module && !module.nodeType && module, nr = Ve && Ve.exports === Lt, ke = nr ? S.Buffer : void 0, rr = ke ? ke.isBuffer : void 0, se = rr || tr, ir = "[object Arguments]", or = "[object Array]", sr = "[object Boolean]", ar = "[object Date]", ur = "[object Error]", fr = "[object Function]", lr = "[object Map]", cr = "[object Number]", dr = "[object Object]", gr = "[object RegExp]", pr = "[object Set]", _r = "[object String]", yr = "[object WeakMap]", br = "[object ArrayBuffer]", hr = "[object DataView]", mr = "[object Float32Array]", vr = "[object Float64Array]", Tr = "[object Int8Array]", Or = "[object Int16Array]", Ar = "[object Int32Array]", Pr = "[object Uint8Array]", wr = "[object Uint8ClampedArray]", xr = "[object Uint16Array]", Sr = "[object Uint32Array]", v = {};
v[mr] = v[vr] = v[Tr] = v[Or] = v[Ar] = v[Pr] = v[wr] = v[xr] = v[Sr] = !0;
v[ir] = v[or] = v[br] = v[sr] = v[hr] = v[ar] = v[ur] = v[fr] = v[lr] = v[cr] = v[dr] = v[gr] = v[pr] = v[_r] = v[yr] = !1;
function $r(e) {
  return j(e) && xe(e.length) && !!v[N(e)];
}
function Ce(e) {
  return function(t) {
    return e(t);
  };
}
var Ft = typeof exports == "object" && exports && !exports.nodeType && exports, q = Ft && typeof module == "object" && module && !module.nodeType && module, Cr = q && q.exports === Ft, pe = Cr && Pt.process, B = function() {
  try {
    var e = q && q.require && q.require("util").types;
    return e || pe && pe.binding && pe.binding("util");
  } catch {
  }
}(), et = B && B.isTypedArray, Rt = et ? Ce(et) : $r, jr = Object.prototype, Er = jr.hasOwnProperty;
function Nt(e, t) {
  var n = w(e), r = !n && $e(e), i = !n && !r && se(e), o = !n && !r && !i && Rt(e), s = n || r || i || o, a = s ? Qn(e.length, String) : [], u = a.length;
  for (var f in e)
    (t || Er.call(e, f)) && !(s && // Safari 9 has enumerable `arguments.length` in strict mode.
    (f == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    i && (f == "offset" || f == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    o && (f == "buffer" || f == "byteLength" || f == "byteOffset") || // Skip index properties.
    jt(f, u))) && a.push(f);
  return a;
}
function Dt(e, t) {
  return function(n) {
    return e(t(n));
  };
}
var Ir = Dt(Object.keys, Object), Mr = Object.prototype, Lr = Mr.hasOwnProperty;
function Fr(e) {
  if (!Se(e))
    return Ir(e);
  var t = [];
  for (var n in Object(e))
    Lr.call(e, n) && n != "constructor" && t.push(n);
  return t;
}
function Z(e) {
  return It(e) ? Nt(e) : Fr(e);
}
function Rr(e) {
  var t = [];
  if (e != null)
    for (var n in Object(e))
      t.push(n);
  return t;
}
var Nr = Object.prototype, Dr = Nr.hasOwnProperty;
function Kr(e) {
  if (!z(e))
    return Rr(e);
  var t = Se(e), n = [];
  for (var r in e)
    r == "constructor" && (t || !Dr.call(e, r)) || n.push(r);
  return n;
}
function je(e) {
  return It(e) ? Nt(e, !0) : Kr(e);
}
var Ur = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, Gr = /^\w*$/;
function Ee(e, t) {
  if (w(e))
    return !1;
  var n = typeof e;
  return n == "number" || n == "symbol" || n == "boolean" || e == null || Ae(e) ? !0 : Gr.test(e) || !Ur.test(e) || t != null && e in Object(t);
}
var Y = K(Object, "create");
function Br() {
  this.__data__ = Y ? Y(null) : {}, this.size = 0;
}
function zr(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var Hr = "__lodash_hash_undefined__", qr = Object.prototype, Yr = qr.hasOwnProperty;
function Xr(e) {
  var t = this.__data__;
  if (Y) {
    var n = t[e];
    return n === Hr ? void 0 : n;
  }
  return Yr.call(t, e) ? t[e] : void 0;
}
var Jr = Object.prototype, Zr = Jr.hasOwnProperty;
function Wr(e) {
  var t = this.__data__;
  return Y ? t[e] !== void 0 : Zr.call(t, e);
}
var Qr = "__lodash_hash_undefined__";
function Vr(e, t) {
  var n = this.__data__;
  return this.size += this.has(e) ? 0 : 1, n[e] = Y && t === void 0 ? Qr : t, this;
}
function R(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
R.prototype.clear = Br;
R.prototype.delete = zr;
R.prototype.get = Xr;
R.prototype.has = Wr;
R.prototype.set = Vr;
function kr() {
  this.__data__ = [], this.size = 0;
}
function fe(e, t) {
  for (var n = e.length; n--; )
    if (we(e[n][0], t))
      return n;
  return -1;
}
var ei = Array.prototype, ti = ei.splice;
function ni(e) {
  var t = this.__data__, n = fe(t, e);
  if (n < 0)
    return !1;
  var r = t.length - 1;
  return n == r ? t.pop() : ti.call(t, n, 1), --this.size, !0;
}
function ri(e) {
  var t = this.__data__, n = fe(t, e);
  return n < 0 ? void 0 : t[n][1];
}
function ii(e) {
  return fe(this.__data__, e) > -1;
}
function oi(e, t) {
  var n = this.__data__, r = fe(n, e);
  return r < 0 ? (++this.size, n.push([e, t])) : n[r][1] = t, this;
}
function E(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
E.prototype.clear = kr;
E.prototype.delete = ni;
E.prototype.get = ri;
E.prototype.has = ii;
E.prototype.set = oi;
var X = K(S, "Map");
function si() {
  this.size = 0, this.__data__ = {
    hash: new R(),
    map: new (X || E)(),
    string: new R()
  };
}
function ai(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function le(e, t) {
  var n = e.__data__;
  return ai(t) ? n[typeof t == "string" ? "string" : "hash"] : n.map;
}
function ui(e) {
  var t = le(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function fi(e) {
  return le(this, e).get(e);
}
function li(e) {
  return le(this, e).has(e);
}
function ci(e, t) {
  var n = le(this, e), r = n.size;
  return n.set(e, t), this.size += n.size == r ? 0 : 1, this;
}
function I(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
I.prototype.clear = si;
I.prototype.delete = ui;
I.prototype.get = fi;
I.prototype.has = li;
I.prototype.set = ci;
var di = "Expected a function";
function Ie(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(di);
  var n = function() {
    var r = arguments, i = t ? t.apply(this, r) : r[0], o = n.cache;
    if (o.has(i))
      return o.get(i);
    var s = e.apply(this, r);
    return n.cache = o.set(i, s) || o, s;
  };
  return n.cache = new (Ie.Cache || I)(), n;
}
Ie.Cache = I;
var gi = 500;
function pi(e) {
  var t = Ie(e, function(r) {
    return n.size === gi && n.clear(), r;
  }), n = t.cache;
  return t;
}
var _i = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, yi = /\\(\\)?/g, bi = pi(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(_i, function(n, r, i, o) {
    t.push(i ? o.replace(yi, "$1") : r || n);
  }), t;
});
function hi(e) {
  return e == null ? "" : St(e);
}
function ce(e, t) {
  return w(e) ? e : Ee(e, t) ? [e] : bi(hi(e));
}
var mi = 1 / 0;
function W(e) {
  if (typeof e == "string" || Ae(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -mi ? "-0" : t;
}
function Me(e, t) {
  t = ce(t, e);
  for (var n = 0, r = t.length; e != null && n < r; )
    e = e[W(t[n++])];
  return n && n == r ? e : void 0;
}
function vi(e, t, n) {
  var r = e == null ? void 0 : Me(e, t);
  return r === void 0 ? n : r;
}
function Le(e, t) {
  for (var n = -1, r = t.length, i = e.length; ++n < r; )
    e[i + n] = t[n];
  return e;
}
var tt = A ? A.isConcatSpreadable : void 0;
function Ti(e) {
  return w(e) || $e(e) || !!(tt && e && e[tt]);
}
function Oi(e, t, n, r, i) {
  var o = -1, s = e.length;
  for (n || (n = Ti), i || (i = []); ++o < s; ) {
    var a = e[o];
    n(a) ? Le(i, a) : i[i.length] = a;
  }
  return i;
}
function Ai(e) {
  var t = e == null ? 0 : e.length;
  return t ? Oi(e) : [];
}
function Pi(e) {
  return Bn(Jn(e, void 0, Ai), e + "");
}
var Fe = Dt(Object.getPrototypeOf, Object), wi = "[object Object]", xi = Function.prototype, Si = Object.prototype, Kt = xi.toString, $i = Si.hasOwnProperty, Ci = Kt.call(Object);
function ji(e) {
  if (!j(e) || N(e) != wi)
    return !1;
  var t = Fe(e);
  if (t === null)
    return !0;
  var n = $i.call(t, "constructor") && t.constructor;
  return typeof n == "function" && n instanceof n && Kt.call(n) == Ci;
}
function Ei(e, t, n) {
  var r = -1, i = e.length;
  t < 0 && (t = -t > i ? 0 : i + t), n = n > i ? i : n, n < 0 && (n += i), i = t > n ? 0 : n - t >>> 0, t >>>= 0;
  for (var o = Array(i); ++r < i; )
    o[r] = e[r + t];
  return o;
}
function Ii() {
  this.__data__ = new E(), this.size = 0;
}
function Mi(e) {
  var t = this.__data__, n = t.delete(e);
  return this.size = t.size, n;
}
function Li(e) {
  return this.__data__.get(e);
}
function Fi(e) {
  return this.__data__.has(e);
}
var Ri = 200;
function Ni(e, t) {
  var n = this.__data__;
  if (n instanceof E) {
    var r = n.__data__;
    if (!X || r.length < Ri - 1)
      return r.push([e, t]), this.size = ++n.size, this;
    n = this.__data__ = new I(r);
  }
  return n.set(e, t), this.size = n.size, this;
}
function x(e) {
  var t = this.__data__ = new E(e);
  this.size = t.size;
}
x.prototype.clear = Ii;
x.prototype.delete = Mi;
x.prototype.get = Li;
x.prototype.has = Fi;
x.prototype.set = Ni;
function Di(e, t) {
  return e && J(t, Z(t), e);
}
function Ki(e, t) {
  return e && J(t, je(t), e);
}
var Ut = typeof exports == "object" && exports && !exports.nodeType && exports, nt = Ut && typeof module == "object" && module && !module.nodeType && module, Ui = nt && nt.exports === Ut, rt = Ui ? S.Buffer : void 0, it = rt ? rt.allocUnsafe : void 0;
function Gi(e, t) {
  if (t)
    return e.slice();
  var n = e.length, r = it ? it(n) : new e.constructor(n);
  return e.copy(r), r;
}
function Bi(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = 0, o = []; ++n < r; ) {
    var s = e[n];
    t(s, n, e) && (o[i++] = s);
  }
  return o;
}
function Gt() {
  return [];
}
var zi = Object.prototype, Hi = zi.propertyIsEnumerable, ot = Object.getOwnPropertySymbols, Re = ot ? function(e) {
  return e == null ? [] : (e = Object(e), Bi(ot(e), function(t) {
    return Hi.call(e, t);
  }));
} : Gt;
function qi(e, t) {
  return J(e, Re(e), t);
}
var Yi = Object.getOwnPropertySymbols, Bt = Yi ? function(e) {
  for (var t = []; e; )
    Le(t, Re(e)), e = Fe(e);
  return t;
} : Gt;
function Xi(e, t) {
  return J(e, Bt(e), t);
}
function zt(e, t, n) {
  var r = t(e);
  return w(e) ? r : Le(r, n(e));
}
function he(e) {
  return zt(e, Z, Re);
}
function Ht(e) {
  return zt(e, je, Bt);
}
var me = K(S, "DataView"), ve = K(S, "Promise"), Te = K(S, "Set"), st = "[object Map]", Ji = "[object Object]", at = "[object Promise]", ut = "[object Set]", ft = "[object WeakMap]", lt = "[object DataView]", Zi = D(me), Wi = D(X), Qi = D(ve), Vi = D(Te), ki = D(be), P = N;
(me && P(new me(new ArrayBuffer(1))) != lt || X && P(new X()) != st || ve && P(ve.resolve()) != at || Te && P(new Te()) != ut || be && P(new be()) != ft) && (P = function(e) {
  var t = N(e), n = t == Ji ? e.constructor : void 0, r = n ? D(n) : "";
  if (r)
    switch (r) {
      case Zi:
        return lt;
      case Wi:
        return st;
      case Qi:
        return at;
      case Vi:
        return ut;
      case ki:
        return ft;
    }
  return t;
});
var eo = Object.prototype, to = eo.hasOwnProperty;
function no(e) {
  var t = e.length, n = new e.constructor(t);
  return t && typeof e[0] == "string" && to.call(e, "index") && (n.index = e.index, n.input = e.input), n;
}
var ae = S.Uint8Array;
function Ne(e) {
  var t = new e.constructor(e.byteLength);
  return new ae(t).set(new ae(e)), t;
}
function ro(e, t) {
  var n = t ? Ne(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.byteLength);
}
var io = /\w*$/;
function oo(e) {
  var t = new e.constructor(e.source, io.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var ct = A ? A.prototype : void 0, dt = ct ? ct.valueOf : void 0;
function so(e) {
  return dt ? Object(dt.call(e)) : {};
}
function ao(e, t) {
  var n = t ? Ne(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.length);
}
var uo = "[object Boolean]", fo = "[object Date]", lo = "[object Map]", co = "[object Number]", go = "[object RegExp]", po = "[object Set]", _o = "[object String]", yo = "[object Symbol]", bo = "[object ArrayBuffer]", ho = "[object DataView]", mo = "[object Float32Array]", vo = "[object Float64Array]", To = "[object Int8Array]", Oo = "[object Int16Array]", Ao = "[object Int32Array]", Po = "[object Uint8Array]", wo = "[object Uint8ClampedArray]", xo = "[object Uint16Array]", So = "[object Uint32Array]";
function $o(e, t, n) {
  var r = e.constructor;
  switch (t) {
    case bo:
      return Ne(e);
    case uo:
    case fo:
      return new r(+e);
    case ho:
      return ro(e, n);
    case mo:
    case vo:
    case To:
    case Oo:
    case Ao:
    case Po:
    case wo:
    case xo:
    case So:
      return ao(e, n);
    case lo:
      return new r();
    case co:
    case _o:
      return new r(e);
    case go:
      return oo(e);
    case po:
      return new r();
    case yo:
      return so(e);
  }
}
function Co(e) {
  return typeof e.constructor == "function" && !Se(e) ? Mn(Fe(e)) : {};
}
var jo = "[object Map]";
function Eo(e) {
  return j(e) && P(e) == jo;
}
var gt = B && B.isMap, Io = gt ? Ce(gt) : Eo, Mo = "[object Set]";
function Lo(e) {
  return j(e) && P(e) == Mo;
}
var pt = B && B.isSet, Fo = pt ? Ce(pt) : Lo, Ro = 1, No = 2, Do = 4, qt = "[object Arguments]", Ko = "[object Array]", Uo = "[object Boolean]", Go = "[object Date]", Bo = "[object Error]", Yt = "[object Function]", zo = "[object GeneratorFunction]", Ho = "[object Map]", qo = "[object Number]", Xt = "[object Object]", Yo = "[object RegExp]", Xo = "[object Set]", Jo = "[object String]", Zo = "[object Symbol]", Wo = "[object WeakMap]", Qo = "[object ArrayBuffer]", Vo = "[object DataView]", ko = "[object Float32Array]", es = "[object Float64Array]", ts = "[object Int8Array]", ns = "[object Int16Array]", rs = "[object Int32Array]", is = "[object Uint8Array]", os = "[object Uint8ClampedArray]", ss = "[object Uint16Array]", as = "[object Uint32Array]", h = {};
h[qt] = h[Ko] = h[Qo] = h[Vo] = h[Uo] = h[Go] = h[ko] = h[es] = h[ts] = h[ns] = h[rs] = h[Ho] = h[qo] = h[Xt] = h[Yo] = h[Xo] = h[Jo] = h[Zo] = h[is] = h[os] = h[ss] = h[as] = !0;
h[Bo] = h[Yt] = h[Wo] = !1;
function ne(e, t, n, r, i, o) {
  var s, a = t & Ro, u = t & No, f = t & Do;
  if (n && (s = i ? n(e, r, i, o) : n(e)), s !== void 0)
    return s;
  if (!z(e))
    return e;
  var d = w(e);
  if (d) {
    if (s = no(e), !a)
      return Fn(e, s);
  } else {
    var _ = P(e), y = _ == Yt || _ == zo;
    if (se(e))
      return Gi(e, a);
    if (_ == Xt || _ == qt || y && !i) {
      if (s = u || y ? {} : Co(e), !a)
        return u ? Xi(e, Ki(s, e)) : qi(e, Di(s, e));
    } else {
      if (!h[_])
        return i ? e : {};
      s = $o(e, _, a);
    }
  }
  o || (o = new x());
  var b = o.get(e);
  if (b)
    return b;
  o.set(e, s), Fo(e) ? e.forEach(function(c) {
    s.add(ne(c, t, n, c, e, o));
  }) : Io(e) && e.forEach(function(c, m) {
    s.set(m, ne(c, t, n, m, e, o));
  });
  var l = f ? u ? Ht : he : u ? je : Z, p = d ? void 0 : l(e);
  return zn(p || e, function(c, m) {
    p && (m = c, c = e[m]), Et(s, m, ne(c, t, n, m, e, o));
  }), s;
}
var us = "__lodash_hash_undefined__";
function fs(e) {
  return this.__data__.set(e, us), this;
}
function ls(e) {
  return this.__data__.has(e);
}
function ue(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.__data__ = new I(); ++t < n; )
    this.add(e[t]);
}
ue.prototype.add = ue.prototype.push = fs;
ue.prototype.has = ls;
function cs(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r; )
    if (t(e[n], n, e))
      return !0;
  return !1;
}
function ds(e, t) {
  return e.has(t);
}
var gs = 1, ps = 2;
function Jt(e, t, n, r, i, o) {
  var s = n & gs, a = e.length, u = t.length;
  if (a != u && !(s && u > a))
    return !1;
  var f = o.get(e), d = o.get(t);
  if (f && d)
    return f == t && d == e;
  var _ = -1, y = !0, b = n & ps ? new ue() : void 0;
  for (o.set(e, t), o.set(t, e); ++_ < a; ) {
    var l = e[_], p = t[_];
    if (r)
      var c = s ? r(p, l, _, t, e, o) : r(l, p, _, e, t, o);
    if (c !== void 0) {
      if (c)
        continue;
      y = !1;
      break;
    }
    if (b) {
      if (!cs(t, function(m, T) {
        if (!ds(b, T) && (l === m || i(l, m, n, r, o)))
          return b.push(T);
      })) {
        y = !1;
        break;
      }
    } else if (!(l === p || i(l, p, n, r, o))) {
      y = !1;
      break;
    }
  }
  return o.delete(e), o.delete(t), y;
}
function _s(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r, i) {
    n[++t] = [i, r];
  }), n;
}
function ys(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r) {
    n[++t] = r;
  }), n;
}
var bs = 1, hs = 2, ms = "[object Boolean]", vs = "[object Date]", Ts = "[object Error]", Os = "[object Map]", As = "[object Number]", Ps = "[object RegExp]", ws = "[object Set]", xs = "[object String]", Ss = "[object Symbol]", $s = "[object ArrayBuffer]", Cs = "[object DataView]", _t = A ? A.prototype : void 0, _e = _t ? _t.valueOf : void 0;
function js(e, t, n, r, i, o, s) {
  switch (n) {
    case Cs:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case $s:
      return !(e.byteLength != t.byteLength || !o(new ae(e), new ae(t)));
    case ms:
    case vs:
    case As:
      return we(+e, +t);
    case Ts:
      return e.name == t.name && e.message == t.message;
    case Ps:
    case xs:
      return e == t + "";
    case Os:
      var a = _s;
    case ws:
      var u = r & bs;
      if (a || (a = ys), e.size != t.size && !u)
        return !1;
      var f = s.get(e);
      if (f)
        return f == t;
      r |= hs, s.set(e, t);
      var d = Jt(a(e), a(t), r, i, o, s);
      return s.delete(e), d;
    case Ss:
      if (_e)
        return _e.call(e) == _e.call(t);
  }
  return !1;
}
var Es = 1, Is = Object.prototype, Ms = Is.hasOwnProperty;
function Ls(e, t, n, r, i, o) {
  var s = n & Es, a = he(e), u = a.length, f = he(t), d = f.length;
  if (u != d && !s)
    return !1;
  for (var _ = u; _--; ) {
    var y = a[_];
    if (!(s ? y in t : Ms.call(t, y)))
      return !1;
  }
  var b = o.get(e), l = o.get(t);
  if (b && l)
    return b == t && l == e;
  var p = !0;
  o.set(e, t), o.set(t, e);
  for (var c = s; ++_ < u; ) {
    y = a[_];
    var m = e[y], T = t[y];
    if (r)
      var L = s ? r(T, m, y, t, e, o) : r(m, T, y, e, t, o);
    if (!(L === void 0 ? m === T || i(m, T, n, r, o) : L)) {
      p = !1;
      break;
    }
    c || (c = y == "constructor");
  }
  if (p && !c) {
    var $ = e.constructor, C = t.constructor;
    $ != C && "constructor" in e && "constructor" in t && !(typeof $ == "function" && $ instanceof $ && typeof C == "function" && C instanceof C) && (p = !1);
  }
  return o.delete(e), o.delete(t), p;
}
var Fs = 1, yt = "[object Arguments]", bt = "[object Array]", te = "[object Object]", Rs = Object.prototype, ht = Rs.hasOwnProperty;
function Ns(e, t, n, r, i, o) {
  var s = w(e), a = w(t), u = s ? bt : P(e), f = a ? bt : P(t);
  u = u == yt ? te : u, f = f == yt ? te : f;
  var d = u == te, _ = f == te, y = u == f;
  if (y && se(e)) {
    if (!se(t))
      return !1;
    s = !0, d = !1;
  }
  if (y && !d)
    return o || (o = new x()), s || Rt(e) ? Jt(e, t, n, r, i, o) : js(e, t, u, n, r, i, o);
  if (!(n & Fs)) {
    var b = d && ht.call(e, "__wrapped__"), l = _ && ht.call(t, "__wrapped__");
    if (b || l) {
      var p = b ? e.value() : e, c = l ? t.value() : t;
      return o || (o = new x()), i(p, c, n, r, o);
    }
  }
  return y ? (o || (o = new x()), Ls(e, t, n, r, i, o)) : !1;
}
function De(e, t, n, r, i) {
  return e === t ? !0 : e == null || t == null || !j(e) && !j(t) ? e !== e && t !== t : Ns(e, t, n, r, De, i);
}
var Ds = 1, Ks = 2;
function Us(e, t, n, r) {
  var i = n.length, o = i;
  if (e == null)
    return !o;
  for (e = Object(e); i--; ) {
    var s = n[i];
    if (s[2] ? s[1] !== e[s[0]] : !(s[0] in e))
      return !1;
  }
  for (; ++i < o; ) {
    s = n[i];
    var a = s[0], u = e[a], f = s[1];
    if (s[2]) {
      if (u === void 0 && !(a in e))
        return !1;
    } else {
      var d = new x(), _;
      if (!(_ === void 0 ? De(f, u, Ds | Ks, r, d) : _))
        return !1;
    }
  }
  return !0;
}
function Zt(e) {
  return e === e && !z(e);
}
function Gs(e) {
  for (var t = Z(e), n = t.length; n--; ) {
    var r = t[n], i = e[r];
    t[n] = [r, i, Zt(i)];
  }
  return t;
}
function Wt(e, t) {
  return function(n) {
    return n == null ? !1 : n[e] === t && (t !== void 0 || e in Object(n));
  };
}
function Bs(e) {
  var t = Gs(e);
  return t.length == 1 && t[0][2] ? Wt(t[0][0], t[0][1]) : function(n) {
    return n === e || Us(n, e, t);
  };
}
function zs(e, t) {
  return e != null && t in Object(e);
}
function Hs(e, t, n) {
  t = ce(t, e);
  for (var r = -1, i = t.length, o = !1; ++r < i; ) {
    var s = W(t[r]);
    if (!(o = e != null && n(e, s)))
      break;
    e = e[s];
  }
  return o || ++r != i ? o : (i = e == null ? 0 : e.length, !!i && xe(i) && jt(s, i) && (w(e) || $e(e)));
}
function qs(e, t) {
  return e != null && Hs(e, t, zs);
}
var Ys = 1, Xs = 2;
function Js(e, t) {
  return Ee(e) && Zt(t) ? Wt(W(e), t) : function(n) {
    var r = vi(n, e);
    return r === void 0 && r === t ? qs(n, e) : De(t, r, Ys | Xs);
  };
}
function Zs(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function Ws(e) {
  return function(t) {
    return Me(t, e);
  };
}
function Qs(e) {
  return Ee(e) ? Zs(W(e)) : Ws(e);
}
function Vs(e) {
  return typeof e == "function" ? e : e == null ? $t : typeof e == "object" ? w(e) ? Js(e[0], e[1]) : Bs(e) : Qs(e);
}
function ks(e) {
  return function(t, n, r) {
    for (var i = -1, o = Object(t), s = r(t), a = s.length; a--; ) {
      var u = s[++i];
      if (n(o[u], u, o) === !1)
        break;
    }
    return t;
  };
}
var ea = ks();
function ta(e, t) {
  return e && ea(e, t, Z);
}
function na(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function ra(e, t) {
  return t.length < 2 ? e : Me(e, Ei(t, 0, -1));
}
function ia(e) {
  return e === void 0;
}
function oa(e, t) {
  var n = {};
  return t = Vs(t), ta(e, function(r, i, o) {
    Pe(n, t(r, i, o), r);
  }), n;
}
function sa(e, t) {
  return t = ce(t, e), e = ra(e, t), e == null || delete e[W(na(t))];
}
function aa(e) {
  return ji(e) ? void 0 : e;
}
var ua = 1, fa = 2, la = 4, Qt = Pi(function(e, t) {
  var n = {};
  if (e == null)
    return n;
  var r = !1;
  t = xt(t, function(o) {
    return o = ce(o, e), r || (r = o.length > 1), o;
  }), J(e, Ht(e), n), r && (n = ne(n, ua | fa | la, aa));
  for (var i = t.length; i--; )
    sa(n, t[i]);
  return n;
});
function ca(e) {
  return e.replace(/(^|_)(\w)/g, (t, n, r, i) => i === 0 ? r.toLowerCase() : r.toUpperCase());
}
const Vt = ["interactive", "gradio", "server", "target", "theme_mode", "root", "name", "visible", "elem_id", "elem_classes", "elem_style", "_internal", "props", "value", "_selectable", "loading_status", "value_is_output"], da = Vt.concat(["attached_events"]);
function ga(e, t = {}) {
  return oa(Qt(e, Vt), (n, r) => t[r] || ca(r));
}
function pa(e, t) {
  const {
    gradio: n,
    _internal: r,
    restProps: i,
    originalRestProps: o,
    ...s
  } = e, a = (i == null ? void 0 : i.attachedEvents) || [];
  return Array.from(/* @__PURE__ */ new Set([...Object.keys(r).map((u) => {
    const f = u.match(/bind_(.+)_event/);
    return f && f[1] ? f[1] : null;
  }).filter(Boolean), ...a.map((u) => u)])).reduce((u, f) => {
    const d = f.split("_"), _ = (...b) => {
      const l = b.map((c) => b && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
        type: c.type,
        detail: c.detail,
        timestamp: c.timeStamp,
        clientX: c.clientX,
        clientY: c.clientY,
        targetId: c.target.id,
        targetClassName: c.target.className,
        altKey: c.altKey,
        ctrlKey: c.ctrlKey,
        shiftKey: c.shiftKey,
        metaKey: c.metaKey
      } : c);
      let p;
      try {
        p = JSON.parse(JSON.stringify(l));
      } catch {
        p = l.map((c) => c && typeof c == "object" ? Object.fromEntries(Object.entries(c).filter(([, m]) => {
          try {
            return JSON.stringify(m), !0;
          } catch {
            return !1;
          }
        })) : c);
      }
      return n.dispatch(f.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
        payload: p,
        component: {
          ...s,
          ...Qt(o, da)
        }
      });
    };
    if (d.length > 1) {
      let b = {
        ...s.props[d[0]] || (i == null ? void 0 : i[d[0]]) || {}
      };
      u[d[0]] = b;
      for (let p = 1; p < d.length - 1; p++) {
        const c = {
          ...s.props[d[p]] || (i == null ? void 0 : i[d[p]]) || {}
        };
        b[d[p]] = c, b = c;
      }
      const l = d[d.length - 1];
      return b[`on${l.slice(0, 1).toUpperCase()}${l.slice(1)}`] = _, u;
    }
    const y = d[0];
    return u[`on${y.slice(0, 1).toUpperCase()}${y.slice(1)}`] = _, u;
  }, {});
}
function re() {
}
function _a(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function ya(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return re;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function F(e) {
  let t;
  return ya(e, (n) => t = n)(), t;
}
const U = [];
function M(e, t = re) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function i(a) {
    if (_a(e, a) && (e = a, n)) {
      const u = !U.length;
      for (const f of r)
        f[1](), U.push(f, e);
      if (u) {
        for (let f = 0; f < U.length; f += 2)
          U[f][0](U[f + 1]);
        U.length = 0;
      }
    }
  }
  function o(a) {
    i(a(e));
  }
  function s(a, u = re) {
    const f = [a, u];
    return r.add(f), r.size === 1 && (n = t(i, o) || re), a(e), () => {
      r.delete(f), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: s
  };
}
const {
  getContext: ba,
  setContext: Wa
} = window.__gradio__svelte__internal, ha = "$$ms-gr-loading-status-key";
function ma() {
  const e = window.ms_globals.loadingKey++, t = ba(ha);
  return (n) => {
    if (!t || !n)
      return;
    const {
      loadingStatusMap: r,
      options: i
    } = t, {
      generating: o,
      error: s
    } = F(i);
    (n == null ? void 0 : n.status) === "pending" || s && (n == null ? void 0 : n.status) === "error" || (o && (n == null ? void 0 : n.status)) === "generating" ? r.update(({
      map: a
    }) => (a.set(e, n), {
      map: a
    })) : r.update(({
      map: a
    }) => (a.delete(e), {
      map: a
    }));
  };
}
const {
  getContext: Ke,
  setContext: de
} = window.__gradio__svelte__internal, va = "$$ms-gr-slots-key";
function Ta() {
  const e = M({});
  return de(va, e);
}
const Oa = "$$ms-gr-context-key";
function ye(e) {
  return ia(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const kt = "$$ms-gr-sub-index-context-key";
function Aa() {
  return Ke(kt) || null;
}
function mt(e) {
  return de(kt, e);
}
function Pa(e, t, n) {
  var y, b;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = tn(), i = Sa({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), o = Aa();
  typeof o == "number" && mt(void 0);
  const s = ma();
  typeof e._internal.subIndex == "number" && mt(e._internal.subIndex), r && r.subscribe((l) => {
    i.slotKey.set(l);
  }), wa();
  const a = Ke(Oa), u = ((y = F(a)) == null ? void 0 : y.as_item) || e.as_item, f = ye(a ? u ? ((b = F(a)) == null ? void 0 : b[u]) || {} : F(a) || {} : {}), d = (l, p) => l ? ga({
    ...l,
    ...p || {}
  }, t) : void 0, _ = M({
    ...e,
    _internal: {
      ...e._internal,
      index: o ?? e._internal.index
    },
    ...f,
    restProps: d(e.restProps, f),
    originalRestProps: e.restProps
  });
  return a ? (a.subscribe((l) => {
    const {
      as_item: p
    } = F(_);
    p && (l = l == null ? void 0 : l[p]), l = ye(l), _.update((c) => ({
      ...c,
      ...l || {},
      restProps: d(c.restProps, l)
    }));
  }), [_, (l) => {
    var c, m;
    const p = ye(l.as_item ? ((c = F(a)) == null ? void 0 : c[l.as_item]) || {} : F(a) || {});
    return s((m = l.restProps) == null ? void 0 : m.loading_status), _.set({
      ...l,
      _internal: {
        ...l._internal,
        index: o ?? l._internal.index
      },
      ...p,
      restProps: d(l.restProps, p),
      originalRestProps: l.restProps
    });
  }]) : [_, (l) => {
    var p;
    s((p = l.restProps) == null ? void 0 : p.loading_status), _.set({
      ...l,
      _internal: {
        ...l._internal,
        index: o ?? l._internal.index
      },
      restProps: d(l.restProps),
      originalRestProps: l.restProps
    });
  }];
}
const en = "$$ms-gr-slot-key";
function wa() {
  de(en, M(void 0));
}
function tn() {
  return Ke(en);
}
const xa = "$$ms-gr-component-slot-context-key";
function Sa({
  slot: e,
  index: t,
  subIndex: n
}) {
  return de(xa, {
    slotKey: M(e),
    slotIndex: M(t),
    subSlotIndex: M(n)
  });
}
function $a(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var nn = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function n() {
      for (var o = "", s = 0; s < arguments.length; s++) {
        var a = arguments[s];
        a && (o = i(o, r(a)));
      }
      return o;
    }
    function r(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return n.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var s = "";
      for (var a in o)
        t.call(o, a) && o[a] && (s = i(s, a));
      return s;
    }
    function i(o, s) {
      return s ? o ? o + " " + s : o + s : o;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(nn);
var Ca = nn.exports;
const ja = /* @__PURE__ */ $a(Ca), {
  getContext: Ea,
  setContext: Ia
} = window.__gradio__svelte__internal;
function Ma(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(i = ["default"]) {
    const o = i.reduce((s, a) => (s[a] = M([]), s), {});
    return Ia(t, {
      itemsMap: o,
      allowedSlots: i
    }), o;
  }
  function r() {
    const {
      itemsMap: i,
      allowedSlots: o
    } = Ea(t);
    return function(s, a, u) {
      i && (s ? i[s].update((f) => {
        const d = [...f];
        return o.includes(s) ? d[a] = u : d[a] = void 0, d;
      }) : o.includes("default") && i.default.update((f) => {
        const d = [...f];
        return d[a] = u, d;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: r
  };
}
const {
  getItems: La,
  getSetItemFn: Fa
} = Ma("mentions"), {
  SvelteComponent: Ra,
  assign: vt,
  check_outros: Na,
  component_subscribe: G,
  compute_rest_props: Tt,
  create_slot: Da,
  detach: Ka,
  empty: Ot,
  exclude_internal_props: Ua,
  flush: O,
  get_all_dirty_from_scope: Ga,
  get_slot_changes: Ba,
  group_outros: za,
  init: Ha,
  insert_hydration: qa,
  safe_not_equal: Ya,
  transition_in: ie,
  transition_out: Oe,
  update_slot_base: Xa
} = window.__gradio__svelte__internal;
function At(e) {
  let t;
  const n = (
    /*#slots*/
    e[25].default
  ), r = Da(
    n,
    e,
    /*$$scope*/
    e[24],
    null
  );
  return {
    c() {
      r && r.c();
    },
    l(i) {
      r && r.l(i);
    },
    m(i, o) {
      r && r.m(i, o), t = !0;
    },
    p(i, o) {
      r && r.p && (!t || o & /*$$scope*/
      16777216) && Xa(
        r,
        n,
        i,
        /*$$scope*/
        i[24],
        t ? Ba(
          n,
          /*$$scope*/
          i[24],
          o,
          null
        ) : Ga(
          /*$$scope*/
          i[24]
        ),
        null
      );
    },
    i(i) {
      t || (ie(r, i), t = !0);
    },
    o(i) {
      Oe(r, i), t = !1;
    },
    d(i) {
      r && r.d(i);
    }
  };
}
function Ja(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[0].visible && At(e)
  );
  return {
    c() {
      r && r.c(), t = Ot();
    },
    l(i) {
      r && r.l(i), t = Ot();
    },
    m(i, o) {
      r && r.m(i, o), qa(i, t, o), n = !0;
    },
    p(i, [o]) {
      /*$mergedProps*/
      i[0].visible ? r ? (r.p(i, o), o & /*$mergedProps*/
      1 && ie(r, 1)) : (r = At(i), r.c(), ie(r, 1), r.m(t.parentNode, t)) : r && (za(), Oe(r, 1, 1, () => {
        r = null;
      }), Na());
    },
    i(i) {
      n || (ie(r), n = !0);
    },
    o(i) {
      Oe(r), n = !1;
    },
    d(i) {
      i && Ka(t), r && r.d(i);
    }
  };
}
function Za(e, t, n) {
  const r = ["gradio", "props", "_internal", "value", "label", "disabled", "key", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let i = Tt(t, r), o, s, a, u, f, d, {
    $$slots: _ = {},
    $$scope: y
  } = t, {
    gradio: b
  } = t, {
    props: l = {}
  } = t;
  const p = M(l);
  G(e, p, (g) => n(23, d = g));
  let {
    _internal: c = {}
  } = t, {
    value: m
  } = t, {
    label: T
  } = t, {
    disabled: L
  } = t, {
    key: $
  } = t, {
    as_item: C
  } = t, {
    visible: Q = !0
  } = t, {
    elem_id: V = ""
  } = t, {
    elem_classes: k = []
  } = t, {
    elem_style: ee = {}
  } = t;
  const Ue = tn();
  G(e, Ue, (g) => n(22, f = g));
  const [Ge, rn] = Pa({
    gradio: b,
    props: d,
    _internal: c,
    visible: Q,
    elem_id: V,
    elem_classes: k,
    elem_style: ee,
    as_item: C,
    value: m,
    disabled: L,
    key: $,
    label: T,
    restProps: i
  });
  G(e, Ge, (g) => n(0, u = g));
  const Be = Ta();
  G(e, Be, (g) => n(21, a = g));
  const on = Fa(), {
    default: ze,
    options: He
  } = La(["default", "options"]);
  return G(e, ze, (g) => n(19, o = g)), G(e, He, (g) => n(20, s = g)), e.$$set = (g) => {
    t = vt(vt({}, t), Ua(g)), n(28, i = Tt(t, r)), "gradio" in g && n(7, b = g.gradio), "props" in g && n(8, l = g.props), "_internal" in g && n(9, c = g._internal), "value" in g && n(10, m = g.value), "label" in g && n(11, T = g.label), "disabled" in g && n(12, L = g.disabled), "key" in g && n(13, $ = g.key), "as_item" in g && n(14, C = g.as_item), "visible" in g && n(15, Q = g.visible), "elem_id" in g && n(16, V = g.elem_id), "elem_classes" in g && n(17, k = g.elem_classes), "elem_style" in g && n(18, ee = g.elem_style), "$$scope" in g && n(24, y = g.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    256 && p.update((g) => ({
      ...g,
      ...l
    })), rn({
      gradio: b,
      props: d,
      _internal: c,
      visible: Q,
      elem_id: V,
      elem_classes: k,
      elem_style: ee,
      as_item: C,
      value: m,
      disabled: L,
      key: $,
      label: T,
      restProps: i
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots, $options, $items*/
    7864321 && on(f, u._internal.index || 0, {
      props: {
        style: u.elem_style,
        className: ja(u.elem_classes, "ms-gr-antd-mentions-option"),
        id: u.elem_id,
        value: u.value,
        label: u.label,
        disabled: u.disabled,
        key: u.key,
        ...u.restProps,
        ...u.props,
        ...pa(u)
      },
      slots: a,
      options: s.length > 0 ? s : o.length > 0 ? o : void 0
    });
  }, [u, p, Ue, Ge, Be, ze, He, b, l, c, m, T, L, $, C, Q, V, k, ee, o, s, a, f, d, y, _];
}
class Qa extends Ra {
  constructor(t) {
    super(), Ha(this, t, Za, Ja, Ya, {
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 10,
      label: 11,
      disabled: 12,
      key: 13,
      as_item: 14,
      visible: 15,
      elem_id: 16,
      elem_classes: 17,
      elem_style: 18
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), O();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), O();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), O();
  }
  get value() {
    return this.$$.ctx[10];
  }
  set value(t) {
    this.$$set({
      value: t
    }), O();
  }
  get label() {
    return this.$$.ctx[11];
  }
  set label(t) {
    this.$$set({
      label: t
    }), O();
  }
  get disabled() {
    return this.$$.ctx[12];
  }
  set disabled(t) {
    this.$$set({
      disabled: t
    }), O();
  }
  get key() {
    return this.$$.ctx[13];
  }
  set key(t) {
    this.$$set({
      key: t
    }), O();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), O();
  }
  get visible() {
    return this.$$.ctx[15];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), O();
  }
  get elem_id() {
    return this.$$.ctx[16];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), O();
  }
  get elem_classes() {
    return this.$$.ctx[17];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), O();
  }
  get elem_style() {
    return this.$$.ctx[18];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), O();
  }
}
export {
  Qa as default
};
