var Ot = typeof global == "object" && global && global.Object === Object && global, ln = typeof self == "object" && self && self.Object === Object && self, E = Ot || ln || Function("return this")(), O = E.Symbol, At = Object.prototype, fn = At.hasOwnProperty, cn = At.toString, Y = O ? O.toStringTag : void 0;
function pn(e) {
  var t = fn.call(e, Y), n = e[Y];
  try {
    e[Y] = void 0;
    var r = !0;
  } catch {
  }
  var i = cn.call(e);
  return r && (t ? e[Y] = n : delete e[Y]), i;
}
var gn = Object.prototype, dn = gn.toString;
function _n(e) {
  return dn.call(e);
}
var hn = "[object Null]", bn = "[object Undefined]", He = O ? O.toStringTag : void 0;
function D(e) {
  return e == null ? e === void 0 ? bn : hn : He && He in Object(e) ? pn(e) : _n(e);
}
function x(e) {
  return e != null && typeof e == "object";
}
var mn = "[object Symbol]";
function Pe(e) {
  return typeof e == "symbol" || x(e) && D(e) == mn;
}
function Pt(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = Array(r); ++n < r; )
    i[n] = t(e[n], n, e);
  return i;
}
var P = Array.isArray, yn = 1 / 0, qe = O ? O.prototype : void 0, Ye = qe ? qe.toString : void 0;
function $t(e) {
  if (typeof e == "string")
    return e;
  if (P(e))
    return Pt(e, $t) + "";
  if (Pe(e))
    return Ye ? Ye.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -yn ? "-0" : t;
}
function q(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function St(e) {
  return e;
}
var vn = "[object AsyncFunction]", Tn = "[object Function]", wn = "[object GeneratorFunction]", On = "[object Proxy]";
function Ct(e) {
  if (!q(e))
    return !1;
  var t = D(e);
  return t == Tn || t == wn || t == vn || t == On;
}
var de = E["__core-js_shared__"], Xe = function() {
  var e = /[^.]+$/.exec(de && de.keys && de.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function An(e) {
  return !!Xe && Xe in e;
}
var Pn = Function.prototype, $n = Pn.toString;
function K(e) {
  if (e != null) {
    try {
      return $n.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var Sn = /[\\^$.*+?()[\]{}|]/g, Cn = /^\[object .+?Constructor\]$/, En = Function.prototype, In = Object.prototype, jn = En.toString, xn = In.hasOwnProperty, Fn = RegExp("^" + jn.call(xn).replace(Sn, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function Ln(e) {
  if (!q(e) || An(e))
    return !1;
  var t = Ct(e) ? Fn : Cn;
  return t.test(K(e));
}
function Mn(e, t) {
  return e == null ? void 0 : e[t];
}
function U(e, t) {
  var n = Mn(e, t);
  return Ln(n) ? n : void 0;
}
var ye = U(E, "WeakMap"), Je = Object.create, Rn = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!q(t))
      return {};
    if (Je)
      return Je(t);
    e.prototype = t;
    var n = new e();
    return e.prototype = void 0, n;
  };
}();
function Nn(e, t, n) {
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
function Dn(e, t) {
  var n = -1, r = e.length;
  for (t || (t = Array(r)); ++n < r; )
    t[n] = e[n];
  return t;
}
var Kn = 800, Un = 16, Gn = Date.now;
function Bn(e) {
  var t = 0, n = 0;
  return function() {
    var r = Gn(), i = Un - (r - n);
    if (n = r, i > 0) {
      if (++t >= Kn)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function zn(e) {
  return function() {
    return e;
  };
}
var ie = function() {
  try {
    var e = U(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), Hn = ie ? function(e, t) {
  return ie(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: zn(t),
    writable: !0
  });
} : St, qn = Bn(Hn);
function Yn(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r && t(e[n], n, e) !== !1; )
    ;
  return e;
}
var Xn = 9007199254740991, Jn = /^(?:0|[1-9]\d*)$/;
function Et(e, t) {
  var n = typeof e;
  return t = t ?? Xn, !!t && (n == "number" || n != "symbol" && Jn.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function $e(e, t, n) {
  t == "__proto__" && ie ? ie(e, t, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : e[t] = n;
}
function Se(e, t) {
  return e === t || e !== e && t !== t;
}
var Zn = Object.prototype, Wn = Zn.hasOwnProperty;
function It(e, t, n) {
  var r = e[t];
  (!(Wn.call(e, t) && Se(r, n)) || n === void 0 && !(t in e)) && $e(e, t, n);
}
function Q(e, t, n, r) {
  var i = !n;
  n || (n = {});
  for (var o = -1, a = t.length; ++o < a; ) {
    var s = t[o], u = void 0;
    u === void 0 && (u = e[s]), i ? $e(n, s, u) : It(n, s, u);
  }
  return n;
}
var Ze = Math.max;
function Qn(e, t, n) {
  return t = Ze(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var r = arguments, i = -1, o = Ze(r.length - t, 0), a = Array(o); ++i < o; )
      a[i] = r[t + i];
    i = -1;
    for (var s = Array(t + 1); ++i < t; )
      s[i] = r[i];
    return s[t] = n(a), Nn(e, this, s);
  };
}
var Vn = 9007199254740991;
function Ce(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= Vn;
}
function jt(e) {
  return e != null && Ce(e.length) && !Ct(e);
}
var kn = Object.prototype;
function Ee(e) {
  var t = e && e.constructor, n = typeof t == "function" && t.prototype || kn;
  return e === n;
}
function er(e, t) {
  for (var n = -1, r = Array(e); ++n < e; )
    r[n] = t(n);
  return r;
}
var tr = "[object Arguments]";
function We(e) {
  return x(e) && D(e) == tr;
}
var xt = Object.prototype, nr = xt.hasOwnProperty, rr = xt.propertyIsEnumerable, Ie = We(/* @__PURE__ */ function() {
  return arguments;
}()) ? We : function(e) {
  return x(e) && nr.call(e, "callee") && !rr.call(e, "callee");
};
function or() {
  return !1;
}
var Ft = typeof exports == "object" && exports && !exports.nodeType && exports, Qe = Ft && typeof module == "object" && module && !module.nodeType && module, ir = Qe && Qe.exports === Ft, Ve = ir ? E.Buffer : void 0, ar = Ve ? Ve.isBuffer : void 0, ae = ar || or, sr = "[object Arguments]", ur = "[object Array]", lr = "[object Boolean]", fr = "[object Date]", cr = "[object Error]", pr = "[object Function]", gr = "[object Map]", dr = "[object Number]", _r = "[object Object]", hr = "[object RegExp]", br = "[object Set]", mr = "[object String]", yr = "[object WeakMap]", vr = "[object ArrayBuffer]", Tr = "[object DataView]", wr = "[object Float32Array]", Or = "[object Float64Array]", Ar = "[object Int8Array]", Pr = "[object Int16Array]", $r = "[object Int32Array]", Sr = "[object Uint8Array]", Cr = "[object Uint8ClampedArray]", Er = "[object Uint16Array]", Ir = "[object Uint32Array]", y = {};
y[wr] = y[Or] = y[Ar] = y[Pr] = y[$r] = y[Sr] = y[Cr] = y[Er] = y[Ir] = !0;
y[sr] = y[ur] = y[vr] = y[lr] = y[Tr] = y[fr] = y[cr] = y[pr] = y[gr] = y[dr] = y[_r] = y[hr] = y[br] = y[mr] = y[yr] = !1;
function jr(e) {
  return x(e) && Ce(e.length) && !!y[D(e)];
}
function je(e) {
  return function(t) {
    return e(t);
  };
}
var Lt = typeof exports == "object" && exports && !exports.nodeType && exports, X = Lt && typeof module == "object" && module && !module.nodeType && module, xr = X && X.exports === Lt, _e = xr && Ot.process, H = function() {
  try {
    var e = X && X.require && X.require("util").types;
    return e || _e && _e.binding && _e.binding("util");
  } catch {
  }
}(), ke = H && H.isTypedArray, Mt = ke ? je(ke) : jr, Fr = Object.prototype, Lr = Fr.hasOwnProperty;
function Rt(e, t) {
  var n = P(e), r = !n && Ie(e), i = !n && !r && ae(e), o = !n && !r && !i && Mt(e), a = n || r || i || o, s = a ? er(e.length, String) : [], u = s.length;
  for (var f in e)
    (t || Lr.call(e, f)) && !(a && // Safari 9 has enumerable `arguments.length` in strict mode.
    (f == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    i && (f == "offset" || f == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    o && (f == "buffer" || f == "byteLength" || f == "byteOffset") || // Skip index properties.
    Et(f, u))) && s.push(f);
  return s;
}
function Nt(e, t) {
  return function(n) {
    return e(t(n));
  };
}
var Mr = Nt(Object.keys, Object), Rr = Object.prototype, Nr = Rr.hasOwnProperty;
function Dr(e) {
  if (!Ee(e))
    return Mr(e);
  var t = [];
  for (var n in Object(e))
    Nr.call(e, n) && n != "constructor" && t.push(n);
  return t;
}
function V(e) {
  return jt(e) ? Rt(e) : Dr(e);
}
function Kr(e) {
  var t = [];
  if (e != null)
    for (var n in Object(e))
      t.push(n);
  return t;
}
var Ur = Object.prototype, Gr = Ur.hasOwnProperty;
function Br(e) {
  if (!q(e))
    return Kr(e);
  var t = Ee(e), n = [];
  for (var r in e)
    r == "constructor" && (t || !Gr.call(e, r)) || n.push(r);
  return n;
}
function xe(e) {
  return jt(e) ? Rt(e, !0) : Br(e);
}
var zr = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, Hr = /^\w*$/;
function Fe(e, t) {
  if (P(e))
    return !1;
  var n = typeof e;
  return n == "number" || n == "symbol" || n == "boolean" || e == null || Pe(e) ? !0 : Hr.test(e) || !zr.test(e) || t != null && e in Object(t);
}
var J = U(Object, "create");
function qr() {
  this.__data__ = J ? J(null) : {}, this.size = 0;
}
function Yr(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var Xr = "__lodash_hash_undefined__", Jr = Object.prototype, Zr = Jr.hasOwnProperty;
function Wr(e) {
  var t = this.__data__;
  if (J) {
    var n = t[e];
    return n === Xr ? void 0 : n;
  }
  return Zr.call(t, e) ? t[e] : void 0;
}
var Qr = Object.prototype, Vr = Qr.hasOwnProperty;
function kr(e) {
  var t = this.__data__;
  return J ? t[e] !== void 0 : Vr.call(t, e);
}
var eo = "__lodash_hash_undefined__";
function to(e, t) {
  var n = this.__data__;
  return this.size += this.has(e) ? 0 : 1, n[e] = J && t === void 0 ? eo : t, this;
}
function N(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
N.prototype.clear = qr;
N.prototype.delete = Yr;
N.prototype.get = Wr;
N.prototype.has = kr;
N.prototype.set = to;
function no() {
  this.__data__ = [], this.size = 0;
}
function fe(e, t) {
  for (var n = e.length; n--; )
    if (Se(e[n][0], t))
      return n;
  return -1;
}
var ro = Array.prototype, oo = ro.splice;
function io(e) {
  var t = this.__data__, n = fe(t, e);
  if (n < 0)
    return !1;
  var r = t.length - 1;
  return n == r ? t.pop() : oo.call(t, n, 1), --this.size, !0;
}
function ao(e) {
  var t = this.__data__, n = fe(t, e);
  return n < 0 ? void 0 : t[n][1];
}
function so(e) {
  return fe(this.__data__, e) > -1;
}
function uo(e, t) {
  var n = this.__data__, r = fe(n, e);
  return r < 0 ? (++this.size, n.push([e, t])) : n[r][1] = t, this;
}
function F(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
F.prototype.clear = no;
F.prototype.delete = io;
F.prototype.get = ao;
F.prototype.has = so;
F.prototype.set = uo;
var Z = U(E, "Map");
function lo() {
  this.size = 0, this.__data__ = {
    hash: new N(),
    map: new (Z || F)(),
    string: new N()
  };
}
function fo(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function ce(e, t) {
  var n = e.__data__;
  return fo(t) ? n[typeof t == "string" ? "string" : "hash"] : n.map;
}
function co(e) {
  var t = ce(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function po(e) {
  return ce(this, e).get(e);
}
function go(e) {
  return ce(this, e).has(e);
}
function _o(e, t) {
  var n = ce(this, e), r = n.size;
  return n.set(e, t), this.size += n.size == r ? 0 : 1, this;
}
function L(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
L.prototype.clear = lo;
L.prototype.delete = co;
L.prototype.get = po;
L.prototype.has = go;
L.prototype.set = _o;
var ho = "Expected a function";
function Le(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(ho);
  var n = function() {
    var r = arguments, i = t ? t.apply(this, r) : r[0], o = n.cache;
    if (o.has(i))
      return o.get(i);
    var a = e.apply(this, r);
    return n.cache = o.set(i, a) || o, a;
  };
  return n.cache = new (Le.Cache || L)(), n;
}
Le.Cache = L;
var bo = 500;
function mo(e) {
  var t = Le(e, function(r) {
    return n.size === bo && n.clear(), r;
  }), n = t.cache;
  return t;
}
var yo = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, vo = /\\(\\)?/g, To = mo(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(yo, function(n, r, i, o) {
    t.push(i ? o.replace(vo, "$1") : r || n);
  }), t;
});
function wo(e) {
  return e == null ? "" : $t(e);
}
function pe(e, t) {
  return P(e) ? e : Fe(e, t) ? [e] : To(wo(e));
}
var Oo = 1 / 0;
function k(e) {
  if (typeof e == "string" || Pe(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -Oo ? "-0" : t;
}
function Me(e, t) {
  t = pe(t, e);
  for (var n = 0, r = t.length; e != null && n < r; )
    e = e[k(t[n++])];
  return n && n == r ? e : void 0;
}
function Ao(e, t, n) {
  var r = e == null ? void 0 : Me(e, t);
  return r === void 0 ? n : r;
}
function Re(e, t) {
  for (var n = -1, r = t.length, i = e.length; ++n < r; )
    e[i + n] = t[n];
  return e;
}
var et = O ? O.isConcatSpreadable : void 0;
function Po(e) {
  return P(e) || Ie(e) || !!(et && e && e[et]);
}
function $o(e, t, n, r, i) {
  var o = -1, a = e.length;
  for (n || (n = Po), i || (i = []); ++o < a; ) {
    var s = e[o];
    n(s) ? Re(i, s) : i[i.length] = s;
  }
  return i;
}
function So(e) {
  var t = e == null ? 0 : e.length;
  return t ? $o(e) : [];
}
function Co(e) {
  return qn(Qn(e, void 0, So), e + "");
}
var Ne = Nt(Object.getPrototypeOf, Object), Eo = "[object Object]", Io = Function.prototype, jo = Object.prototype, Dt = Io.toString, xo = jo.hasOwnProperty, Fo = Dt.call(Object);
function Lo(e) {
  if (!x(e) || D(e) != Eo)
    return !1;
  var t = Ne(e);
  if (t === null)
    return !0;
  var n = xo.call(t, "constructor") && t.constructor;
  return typeof n == "function" && n instanceof n && Dt.call(n) == Fo;
}
function Mo(e, t, n) {
  var r = -1, i = e.length;
  t < 0 && (t = -t > i ? 0 : i + t), n = n > i ? i : n, n < 0 && (n += i), i = t > n ? 0 : n - t >>> 0, t >>>= 0;
  for (var o = Array(i); ++r < i; )
    o[r] = e[r + t];
  return o;
}
function Ro() {
  this.__data__ = new F(), this.size = 0;
}
function No(e) {
  var t = this.__data__, n = t.delete(e);
  return this.size = t.size, n;
}
function Do(e) {
  return this.__data__.get(e);
}
function Ko(e) {
  return this.__data__.has(e);
}
var Uo = 200;
function Go(e, t) {
  var n = this.__data__;
  if (n instanceof F) {
    var r = n.__data__;
    if (!Z || r.length < Uo - 1)
      return r.push([e, t]), this.size = ++n.size, this;
    n = this.__data__ = new L(r);
  }
  return n.set(e, t), this.size = n.size, this;
}
function S(e) {
  var t = this.__data__ = new F(e);
  this.size = t.size;
}
S.prototype.clear = Ro;
S.prototype.delete = No;
S.prototype.get = Do;
S.prototype.has = Ko;
S.prototype.set = Go;
function Bo(e, t) {
  return e && Q(t, V(t), e);
}
function zo(e, t) {
  return e && Q(t, xe(t), e);
}
var Kt = typeof exports == "object" && exports && !exports.nodeType && exports, tt = Kt && typeof module == "object" && module && !module.nodeType && module, Ho = tt && tt.exports === Kt, nt = Ho ? E.Buffer : void 0, rt = nt ? nt.allocUnsafe : void 0;
function qo(e, t) {
  if (t)
    return e.slice();
  var n = e.length, r = rt ? rt(n) : new e.constructor(n);
  return e.copy(r), r;
}
function Yo(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = 0, o = []; ++n < r; ) {
    var a = e[n];
    t(a, n, e) && (o[i++] = a);
  }
  return o;
}
function Ut() {
  return [];
}
var Xo = Object.prototype, Jo = Xo.propertyIsEnumerable, ot = Object.getOwnPropertySymbols, De = ot ? function(e) {
  return e == null ? [] : (e = Object(e), Yo(ot(e), function(t) {
    return Jo.call(e, t);
  }));
} : Ut;
function Zo(e, t) {
  return Q(e, De(e), t);
}
var Wo = Object.getOwnPropertySymbols, Gt = Wo ? function(e) {
  for (var t = []; e; )
    Re(t, De(e)), e = Ne(e);
  return t;
} : Ut;
function Qo(e, t) {
  return Q(e, Gt(e), t);
}
function Bt(e, t, n) {
  var r = t(e);
  return P(e) ? r : Re(r, n(e));
}
function ve(e) {
  return Bt(e, V, De);
}
function zt(e) {
  return Bt(e, xe, Gt);
}
var Te = U(E, "DataView"), we = U(E, "Promise"), Oe = U(E, "Set"), it = "[object Map]", Vo = "[object Object]", at = "[object Promise]", st = "[object Set]", ut = "[object WeakMap]", lt = "[object DataView]", ko = K(Te), ei = K(Z), ti = K(we), ni = K(Oe), ri = K(ye), A = D;
(Te && A(new Te(new ArrayBuffer(1))) != lt || Z && A(new Z()) != it || we && A(we.resolve()) != at || Oe && A(new Oe()) != st || ye && A(new ye()) != ut) && (A = function(e) {
  var t = D(e), n = t == Vo ? e.constructor : void 0, r = n ? K(n) : "";
  if (r)
    switch (r) {
      case ko:
        return lt;
      case ei:
        return it;
      case ti:
        return at;
      case ni:
        return st;
      case ri:
        return ut;
    }
  return t;
});
var oi = Object.prototype, ii = oi.hasOwnProperty;
function ai(e) {
  var t = e.length, n = new e.constructor(t);
  return t && typeof e[0] == "string" && ii.call(e, "index") && (n.index = e.index, n.input = e.input), n;
}
var se = E.Uint8Array;
function Ke(e) {
  var t = new e.constructor(e.byteLength);
  return new se(t).set(new se(e)), t;
}
function si(e, t) {
  var n = t ? Ke(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.byteLength);
}
var ui = /\w*$/;
function li(e) {
  var t = new e.constructor(e.source, ui.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var ft = O ? O.prototype : void 0, ct = ft ? ft.valueOf : void 0;
function fi(e) {
  return ct ? Object(ct.call(e)) : {};
}
function ci(e, t) {
  var n = t ? Ke(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.length);
}
var pi = "[object Boolean]", gi = "[object Date]", di = "[object Map]", _i = "[object Number]", hi = "[object RegExp]", bi = "[object Set]", mi = "[object String]", yi = "[object Symbol]", vi = "[object ArrayBuffer]", Ti = "[object DataView]", wi = "[object Float32Array]", Oi = "[object Float64Array]", Ai = "[object Int8Array]", Pi = "[object Int16Array]", $i = "[object Int32Array]", Si = "[object Uint8Array]", Ci = "[object Uint8ClampedArray]", Ei = "[object Uint16Array]", Ii = "[object Uint32Array]";
function ji(e, t, n) {
  var r = e.constructor;
  switch (t) {
    case vi:
      return Ke(e);
    case pi:
    case gi:
      return new r(+e);
    case Ti:
      return si(e, n);
    case wi:
    case Oi:
    case Ai:
    case Pi:
    case $i:
    case Si:
    case Ci:
    case Ei:
    case Ii:
      return ci(e, n);
    case di:
      return new r();
    case _i:
    case mi:
      return new r(e);
    case hi:
      return li(e);
    case bi:
      return new r();
    case yi:
      return fi(e);
  }
}
function xi(e) {
  return typeof e.constructor == "function" && !Ee(e) ? Rn(Ne(e)) : {};
}
var Fi = "[object Map]";
function Li(e) {
  return x(e) && A(e) == Fi;
}
var pt = H && H.isMap, Mi = pt ? je(pt) : Li, Ri = "[object Set]";
function Ni(e) {
  return x(e) && A(e) == Ri;
}
var gt = H && H.isSet, Di = gt ? je(gt) : Ni, Ki = 1, Ui = 2, Gi = 4, Ht = "[object Arguments]", Bi = "[object Array]", zi = "[object Boolean]", Hi = "[object Date]", qi = "[object Error]", qt = "[object Function]", Yi = "[object GeneratorFunction]", Xi = "[object Map]", Ji = "[object Number]", Yt = "[object Object]", Zi = "[object RegExp]", Wi = "[object Set]", Qi = "[object String]", Vi = "[object Symbol]", ki = "[object WeakMap]", ea = "[object ArrayBuffer]", ta = "[object DataView]", na = "[object Float32Array]", ra = "[object Float64Array]", oa = "[object Int8Array]", ia = "[object Int16Array]", aa = "[object Int32Array]", sa = "[object Uint8Array]", ua = "[object Uint8ClampedArray]", la = "[object Uint16Array]", fa = "[object Uint32Array]", m = {};
m[Ht] = m[Bi] = m[ea] = m[ta] = m[zi] = m[Hi] = m[na] = m[ra] = m[oa] = m[ia] = m[aa] = m[Xi] = m[Ji] = m[Yt] = m[Zi] = m[Wi] = m[Qi] = m[Vi] = m[sa] = m[ua] = m[la] = m[fa] = !0;
m[qi] = m[qt] = m[ki] = !1;
function oe(e, t, n, r, i, o) {
  var a, s = t & Ki, u = t & Ui, f = t & Gi;
  if (n && (a = i ? n(e, r, i, o) : n(e)), a !== void 0)
    return a;
  if (!q(e))
    return e;
  var p = P(e);
  if (p) {
    if (a = ai(e), !s)
      return Dn(e, a);
  } else {
    var d = A(e), h = d == qt || d == Yi;
    if (ae(e))
      return qo(e, s);
    if (d == Yt || d == Ht || h && !i) {
      if (a = u || h ? {} : xi(e), !s)
        return u ? Qo(e, zo(a, e)) : Zo(e, Bo(a, e));
    } else {
      if (!m[d])
        return i ? e : {};
      a = ji(e, d, s);
    }
  }
  o || (o = new S());
  var b = o.get(e);
  if (b)
    return b;
  o.set(e, a), Di(e) ? e.forEach(function(c) {
    a.add(oe(c, t, n, c, e, o));
  }) : Mi(e) && e.forEach(function(c, v) {
    a.set(v, oe(c, t, n, v, e, o));
  });
  var l = f ? u ? zt : ve : u ? xe : V, g = p ? void 0 : l(e);
  return Yn(g || e, function(c, v) {
    g && (v = c, c = e[v]), It(a, v, oe(c, t, n, v, e, o));
  }), a;
}
var ca = "__lodash_hash_undefined__";
function pa(e) {
  return this.__data__.set(e, ca), this;
}
function ga(e) {
  return this.__data__.has(e);
}
function ue(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.__data__ = new L(); ++t < n; )
    this.add(e[t]);
}
ue.prototype.add = ue.prototype.push = pa;
ue.prototype.has = ga;
function da(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r; )
    if (t(e[n], n, e))
      return !0;
  return !1;
}
function _a(e, t) {
  return e.has(t);
}
var ha = 1, ba = 2;
function Xt(e, t, n, r, i, o) {
  var a = n & ha, s = e.length, u = t.length;
  if (s != u && !(a && u > s))
    return !1;
  var f = o.get(e), p = o.get(t);
  if (f && p)
    return f == t && p == e;
  var d = -1, h = !0, b = n & ba ? new ue() : void 0;
  for (o.set(e, t), o.set(t, e); ++d < s; ) {
    var l = e[d], g = t[d];
    if (r)
      var c = a ? r(g, l, d, t, e, o) : r(l, g, d, e, t, o);
    if (c !== void 0) {
      if (c)
        continue;
      h = !1;
      break;
    }
    if (b) {
      if (!da(t, function(v, w) {
        if (!_a(b, w) && (l === v || i(l, v, n, r, o)))
          return b.push(w);
      })) {
        h = !1;
        break;
      }
    } else if (!(l === g || i(l, g, n, r, o))) {
      h = !1;
      break;
    }
  }
  return o.delete(e), o.delete(t), h;
}
function ma(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r, i) {
    n[++t] = [i, r];
  }), n;
}
function ya(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r) {
    n[++t] = r;
  }), n;
}
var va = 1, Ta = 2, wa = "[object Boolean]", Oa = "[object Date]", Aa = "[object Error]", Pa = "[object Map]", $a = "[object Number]", Sa = "[object RegExp]", Ca = "[object Set]", Ea = "[object String]", Ia = "[object Symbol]", ja = "[object ArrayBuffer]", xa = "[object DataView]", dt = O ? O.prototype : void 0, he = dt ? dt.valueOf : void 0;
function Fa(e, t, n, r, i, o, a) {
  switch (n) {
    case xa:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case ja:
      return !(e.byteLength != t.byteLength || !o(new se(e), new se(t)));
    case wa:
    case Oa:
    case $a:
      return Se(+e, +t);
    case Aa:
      return e.name == t.name && e.message == t.message;
    case Sa:
    case Ea:
      return e == t + "";
    case Pa:
      var s = ma;
    case Ca:
      var u = r & va;
      if (s || (s = ya), e.size != t.size && !u)
        return !1;
      var f = a.get(e);
      if (f)
        return f == t;
      r |= Ta, a.set(e, t);
      var p = Xt(s(e), s(t), r, i, o, a);
      return a.delete(e), p;
    case Ia:
      if (he)
        return he.call(e) == he.call(t);
  }
  return !1;
}
var La = 1, Ma = Object.prototype, Ra = Ma.hasOwnProperty;
function Na(e, t, n, r, i, o) {
  var a = n & La, s = ve(e), u = s.length, f = ve(t), p = f.length;
  if (u != p && !a)
    return !1;
  for (var d = u; d--; ) {
    var h = s[d];
    if (!(a ? h in t : Ra.call(t, h)))
      return !1;
  }
  var b = o.get(e), l = o.get(t);
  if (b && l)
    return b == t && l == e;
  var g = !0;
  o.set(e, t), o.set(t, e);
  for (var c = a; ++d < u; ) {
    h = s[d];
    var v = e[h], w = t[h];
    if (r)
      var M = a ? r(w, v, h, t, e, o) : r(v, w, h, e, t, o);
    if (!(M === void 0 ? v === w || i(v, w, n, r, o) : M)) {
      g = !1;
      break;
    }
    c || (c = h == "constructor");
  }
  if (g && !c) {
    var I = e.constructor, j = t.constructor;
    I != j && "constructor" in e && "constructor" in t && !(typeof I == "function" && I instanceof I && typeof j == "function" && j instanceof j) && (g = !1);
  }
  return o.delete(e), o.delete(t), g;
}
var Da = 1, _t = "[object Arguments]", ht = "[object Array]", ne = "[object Object]", Ka = Object.prototype, bt = Ka.hasOwnProperty;
function Ua(e, t, n, r, i, o) {
  var a = P(e), s = P(t), u = a ? ht : A(e), f = s ? ht : A(t);
  u = u == _t ? ne : u, f = f == _t ? ne : f;
  var p = u == ne, d = f == ne, h = u == f;
  if (h && ae(e)) {
    if (!ae(t))
      return !1;
    a = !0, p = !1;
  }
  if (h && !p)
    return o || (o = new S()), a || Mt(e) ? Xt(e, t, n, r, i, o) : Fa(e, t, u, n, r, i, o);
  if (!(n & Da)) {
    var b = p && bt.call(e, "__wrapped__"), l = d && bt.call(t, "__wrapped__");
    if (b || l) {
      var g = b ? e.value() : e, c = l ? t.value() : t;
      return o || (o = new S()), i(g, c, n, r, o);
    }
  }
  return h ? (o || (o = new S()), Na(e, t, n, r, i, o)) : !1;
}
function Ue(e, t, n, r, i) {
  return e === t ? !0 : e == null || t == null || !x(e) && !x(t) ? e !== e && t !== t : Ua(e, t, n, r, Ue, i);
}
var Ga = 1, Ba = 2;
function za(e, t, n, r) {
  var i = n.length, o = i;
  if (e == null)
    return !o;
  for (e = Object(e); i--; ) {
    var a = n[i];
    if (a[2] ? a[1] !== e[a[0]] : !(a[0] in e))
      return !1;
  }
  for (; ++i < o; ) {
    a = n[i];
    var s = a[0], u = e[s], f = a[1];
    if (a[2]) {
      if (u === void 0 && !(s in e))
        return !1;
    } else {
      var p = new S(), d;
      if (!(d === void 0 ? Ue(f, u, Ga | Ba, r, p) : d))
        return !1;
    }
  }
  return !0;
}
function Jt(e) {
  return e === e && !q(e);
}
function Ha(e) {
  for (var t = V(e), n = t.length; n--; ) {
    var r = t[n], i = e[r];
    t[n] = [r, i, Jt(i)];
  }
  return t;
}
function Zt(e, t) {
  return function(n) {
    return n == null ? !1 : n[e] === t && (t !== void 0 || e in Object(n));
  };
}
function qa(e) {
  var t = Ha(e);
  return t.length == 1 && t[0][2] ? Zt(t[0][0], t[0][1]) : function(n) {
    return n === e || za(n, e, t);
  };
}
function Ya(e, t) {
  return e != null && t in Object(e);
}
function Xa(e, t, n) {
  t = pe(t, e);
  for (var r = -1, i = t.length, o = !1; ++r < i; ) {
    var a = k(t[r]);
    if (!(o = e != null && n(e, a)))
      break;
    e = e[a];
  }
  return o || ++r != i ? o : (i = e == null ? 0 : e.length, !!i && Ce(i) && Et(a, i) && (P(e) || Ie(e)));
}
function Ja(e, t) {
  return e != null && Xa(e, t, Ya);
}
var Za = 1, Wa = 2;
function Qa(e, t) {
  return Fe(e) && Jt(t) ? Zt(k(e), t) : function(n) {
    var r = Ao(n, e);
    return r === void 0 && r === t ? Ja(n, e) : Ue(t, r, Za | Wa);
  };
}
function Va(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function ka(e) {
  return function(t) {
    return Me(t, e);
  };
}
function es(e) {
  return Fe(e) ? Va(k(e)) : ka(e);
}
function ts(e) {
  return typeof e == "function" ? e : e == null ? St : typeof e == "object" ? P(e) ? Qa(e[0], e[1]) : qa(e) : es(e);
}
function ns(e) {
  return function(t, n, r) {
    for (var i = -1, o = Object(t), a = r(t), s = a.length; s--; ) {
      var u = a[++i];
      if (n(o[u], u, o) === !1)
        break;
    }
    return t;
  };
}
var rs = ns();
function os(e, t) {
  return e && rs(e, t, V);
}
function is(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function as(e, t) {
  return t.length < 2 ? e : Me(e, Mo(t, 0, -1));
}
function ss(e) {
  return e === void 0;
}
function us(e, t) {
  var n = {};
  return t = ts(t), os(e, function(r, i, o) {
    $e(n, t(r, i, o), r);
  }), n;
}
function ls(e, t) {
  return t = pe(t, e), e = as(e, t), e == null || delete e[k(is(t))];
}
function fs(e) {
  return Lo(e) ? void 0 : e;
}
var cs = 1, ps = 2, gs = 4, Wt = Co(function(e, t) {
  var n = {};
  if (e == null)
    return n;
  var r = !1;
  t = Pt(t, function(o) {
    return o = pe(o, e), r || (r = o.length > 1), o;
  }), Q(e, zt(e), n), r && (n = oe(n, cs | ps | gs, fs));
  for (var i = t.length; i--; )
    ls(n, t[i]);
  return n;
});
async function ds() {
  window.ms_globals || (window.ms_globals = {}), window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function _s(e) {
  return await ds(), e().then((t) => t.default);
}
function hs(e) {
  return e.replace(/(^|_)(\w)/g, (t, n, r, i) => i === 0 ? r.toLowerCase() : r.toUpperCase());
}
const Qt = ["interactive", "gradio", "server", "target", "theme_mode", "root", "name", "visible", "elem_id", "elem_classes", "elem_style", "_internal", "props", "value", "_selectable", "loading_status", "value_is_output"], bs = Qt.concat(["attached_events"]);
function ms(e, t = {}) {
  return us(Wt(e, Qt), (n, r) => t[r] || hs(r));
}
function mt(e, t) {
  const {
    gradio: n,
    _internal: r,
    restProps: i,
    originalRestProps: o,
    ...a
  } = e, s = (i == null ? void 0 : i.attachedEvents) || [];
  return Array.from(/* @__PURE__ */ new Set([...Object.keys(r).map((u) => {
    const f = u.match(/bind_(.+)_event/);
    return f && f[1] ? f[1] : null;
  }).filter(Boolean), ...s.map((u) => t && t[u] ? t[u] : u)])).reduce((u, f) => {
    const p = f.split("_"), d = (...b) => {
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
      let g;
      try {
        g = JSON.parse(JSON.stringify(l));
      } catch {
        g = l.map((c) => c && typeof c == "object" ? Object.fromEntries(Object.entries(c).filter(([, v]) => {
          try {
            return JSON.stringify(v), !0;
          } catch {
            return !1;
          }
        })) : c);
      }
      return n.dispatch(f.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
        payload: g,
        component: {
          ...a,
          ...Wt(o, bs)
        }
      });
    };
    if (p.length > 1) {
      let b = {
        ...a.props[p[0]] || (i == null ? void 0 : i[p[0]]) || {}
      };
      u[p[0]] = b;
      for (let g = 1; g < p.length - 1; g++) {
        const c = {
          ...a.props[p[g]] || (i == null ? void 0 : i[p[g]]) || {}
        };
        b[p[g]] = c, b = c;
      }
      const l = p[p.length - 1];
      return b[`on${l.slice(0, 1).toUpperCase()}${l.slice(1)}`] = d, u;
    }
    const h = p[0];
    return u[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = d, u;
  }, {});
}
function B() {
}
function ys(e) {
  return e();
}
function vs(e) {
  e.forEach(ys);
}
function Ts(e) {
  return typeof e == "function";
}
function ws(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Vt(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return B;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function R(e) {
  let t;
  return Vt(e, (n) => t = n)(), t;
}
const G = [];
function Os(e, t) {
  return {
    subscribe: C(e, t).subscribe
  };
}
function C(e, t = B) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function i(s) {
    if (ws(e, s) && (e = s, n)) {
      const u = !G.length;
      for (const f of r)
        f[1](), G.push(f, e);
      if (u) {
        for (let f = 0; f < G.length; f += 2)
          G[f][0](G[f + 1]);
        G.length = 0;
      }
    }
  }
  function o(s) {
    i(s(e));
  }
  function a(s, u = B) {
    const f = [s, u];
    return r.add(f), r.size === 1 && (n = t(i, o) || B), s(e), () => {
      r.delete(f), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: a
  };
}
function pu(e, t, n) {
  const r = !Array.isArray(e), i = r ? [e] : e;
  if (!i.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const o = t.length < 2;
  return Os(n, (a, s) => {
    let u = !1;
    const f = [];
    let p = 0, d = B;
    const h = () => {
      if (p)
        return;
      d();
      const l = t(r ? f[0] : f, a, s);
      o ? a(l) : d = Ts(l) ? l : B;
    }, b = i.map((l, g) => Vt(l, (c) => {
      f[g] = c, p &= ~(1 << g), u && h();
    }, () => {
      p |= 1 << g;
    }));
    return u = !0, h(), function() {
      vs(b), d(), u = !1;
    };
  });
}
const {
  getContext: As,
  setContext: gu
} = window.__gradio__svelte__internal, Ps = "$$ms-gr-loading-status-key";
function $s() {
  const e = window.ms_globals.loadingKey++, t = As(Ps);
  return (n) => {
    if (!t || !n)
      return;
    const {
      loadingStatusMap: r,
      options: i
    } = t, {
      generating: o,
      error: a
    } = R(i);
    (n == null ? void 0 : n.status) === "pending" || a && (n == null ? void 0 : n.status) === "error" || (o && (n == null ? void 0 : n.status)) === "generating" ? r.update(({
      map: s
    }) => (s.set(e, n), {
      map: s
    })) : r.update(({
      map: s
    }) => (s.delete(e), {
      map: s
    }));
  };
}
const {
  getContext: ge,
  setContext: ee
} = window.__gradio__svelte__internal, Ss = "$$ms-gr-slots-key";
function Cs() {
  const e = C({});
  return ee(Ss, e);
}
const Es = "$$ms-gr-render-slot-context-key";
function Is() {
  const e = ee(Es, C({}));
  return (t, n) => {
    e.update((r) => typeof n == "function" ? {
      ...r,
      [t]: n(r[t])
    } : {
      ...r,
      [t]: n
    });
  };
}
const js = "$$ms-gr-context-key";
function be(e) {
  return ss(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const kt = "$$ms-gr-sub-index-context-key";
function xs() {
  return ge(kt) || null;
}
function yt(e) {
  return ee(kt, e);
}
function Fs(e, t, n) {
  var h, b;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = Ms(), i = Rs({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), o = xs();
  typeof o == "number" && yt(void 0);
  const a = $s();
  typeof e._internal.subIndex == "number" && yt(e._internal.subIndex), r && r.subscribe((l) => {
    i.slotKey.set(l);
  }), Ls();
  const s = ge(js), u = ((h = R(s)) == null ? void 0 : h.as_item) || e.as_item, f = be(s ? u ? ((b = R(s)) == null ? void 0 : b[u]) || {} : R(s) || {} : {}), p = (l, g) => l ? ms({
    ...l,
    ...g || {}
  }, t) : void 0, d = C({
    ...e,
    _internal: {
      ...e._internal,
      index: o ?? e._internal.index
    },
    ...f,
    restProps: p(e.restProps, f),
    originalRestProps: e.restProps
  });
  return s ? (s.subscribe((l) => {
    const {
      as_item: g
    } = R(d);
    g && (l = l == null ? void 0 : l[g]), l = be(l), d.update((c) => ({
      ...c,
      ...l || {},
      restProps: p(c.restProps, l)
    }));
  }), [d, (l) => {
    var c, v;
    const g = be(l.as_item ? ((c = R(s)) == null ? void 0 : c[l.as_item]) || {} : R(s) || {});
    return a((v = l.restProps) == null ? void 0 : v.loading_status), d.set({
      ...l,
      _internal: {
        ...l._internal,
        index: o ?? l._internal.index
      },
      ...g,
      restProps: p(l.restProps, g),
      originalRestProps: l.restProps
    });
  }]) : [d, (l) => {
    var g;
    a((g = l.restProps) == null ? void 0 : g.loading_status), d.set({
      ...l,
      _internal: {
        ...l._internal,
        index: o ?? l._internal.index
      },
      restProps: p(l.restProps),
      originalRestProps: l.restProps
    });
  }];
}
const en = "$$ms-gr-slot-key";
function Ls() {
  ee(en, C(void 0));
}
function Ms() {
  return ge(en);
}
const tn = "$$ms-gr-component-slot-context-key";
function Rs({
  slot: e,
  index: t,
  subIndex: n
}) {
  return ee(tn, {
    slotKey: C(e),
    slotIndex: C(t),
    subSlotIndex: C(n)
  });
}
function du() {
  return ge(tn);
}
function Ns(e) {
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
      for (var o = "", a = 0; a < arguments.length; a++) {
        var s = arguments[a];
        s && (o = i(o, r(s)));
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
      var a = "";
      for (var s in o)
        t.call(o, s) && o[s] && (a = i(a, s));
      return a;
    }
    function i(o, a) {
      return a ? o ? o + " " + a : o + a : o;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(nn);
var Ds = nn.exports;
const vt = /* @__PURE__ */ Ns(Ds), {
  getContext: Ks,
  setContext: Us
} = window.__gradio__svelte__internal;
function Gs(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(i = ["default"]) {
    const o = i.reduce((a, s) => (a[s] = C([]), a), {});
    return Us(t, {
      itemsMap: o,
      allowedSlots: i
    }), o;
  }
  function r() {
    const {
      itemsMap: i,
      allowedSlots: o
    } = Ks(t);
    return function(a, s, u) {
      i && (a ? i[a].update((f) => {
        const p = [...f];
        return o.includes(a) ? p[s] = u : p[s] = void 0, p;
      }) : o.includes("default") && i.default.update((f) => {
        const p = [...f];
        return p[s] = u, p;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: r
  };
}
const {
  getItems: Bs,
  getSetItemFn: _u
} = Gs("color-picker"), {
  SvelteComponent: zs,
  assign: Ae,
  check_outros: Hs,
  claim_component: qs,
  component_subscribe: re,
  compute_rest_props: Tt,
  create_component: Ys,
  create_slot: Xs,
  destroy_component: Js,
  detach: rn,
  empty: le,
  exclude_internal_props: Zs,
  flush: $,
  get_all_dirty_from_scope: Ws,
  get_slot_changes: Qs,
  get_spread_object: me,
  get_spread_update: Vs,
  group_outros: ks,
  handle_promise: eu,
  init: tu,
  insert_hydration: on,
  mount_component: nu,
  noop: T,
  safe_not_equal: ru,
  transition_in: z,
  transition_out: W,
  update_await_block_branch: ou,
  update_slot_base: iu
} = window.__gradio__svelte__internal;
function wt(e) {
  let t, n, r = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: lu,
    then: su,
    catch: au,
    value: 25,
    blocks: [, , ,]
  };
  return eu(
    /*AwaitedColorPicker*/
    e[5],
    r
  ), {
    c() {
      t = le(), r.block.c();
    },
    l(i) {
      t = le(), r.block.l(i);
    },
    m(i, o) {
      on(i, t, o), r.block.m(i, r.anchor = o), r.mount = () => t.parentNode, r.anchor = t, n = !0;
    },
    p(i, o) {
      e = i, ou(r, e, o);
    },
    i(i) {
      n || (z(r.block), n = !0);
    },
    o(i) {
      for (let o = 0; o < 3; o += 1) {
        const a = r.blocks[o];
        W(a);
      }
      n = !1;
    },
    d(i) {
      i && rn(t), r.block.d(i), r.token = null, r = null;
    }
  };
}
function au(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function su(e) {
  let t, n;
  const r = [
    {
      style: (
        /*$mergedProps*/
        e[2].elem_style
      )
    },
    {
      className: vt(
        /*$mergedProps*/
        e[2].elem_classes,
        "ms-gr-antd-color-picker"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[2].elem_id
      )
    },
    /*$mergedProps*/
    e[2].restProps,
    /*$mergedProps*/
    e[2].props,
    mt(
      /*$mergedProps*/
      e[2],
      {
        change_complete: "changeComplete",
        open_change: "openChange",
        format_change: "formatChange"
      }
    ),
    {
      value: (
        /*$mergedProps*/
        e[2].props.value ?? /*$mergedProps*/
        e[2].value ?? void 0
      )
    },
    {
      slots: (
        /*$slots*/
        e[3]
      )
    },
    {
      presetItems: (
        /*$presets*/
        e[4]
      )
    },
    {
      value_format: (
        /*value_format*/
        e[1]
      )
    },
    {
      onValueChange: (
        /*func*/
        e[21]
      )
    },
    {
      setSlotParams: (
        /*setSlotParams*/
        e[9]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [uu]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let o = 0; o < r.length; o += 1)
    i = Ae(i, r[o]);
  return t = new /*ColorPicker*/
  e[25]({
    props: i
  }), {
    c() {
      Ys(t.$$.fragment);
    },
    l(o) {
      qs(t.$$.fragment, o);
    },
    m(o, a) {
      nu(t, o, a), n = !0;
    },
    p(o, a) {
      const s = a & /*$mergedProps, undefined, $slots, $presets, value_format, value, setSlotParams*/
      543 ? Vs(r, [a & /*$mergedProps*/
      4 && {
        style: (
          /*$mergedProps*/
          o[2].elem_style
        )
      }, a & /*$mergedProps*/
      4 && {
        className: vt(
          /*$mergedProps*/
          o[2].elem_classes,
          "ms-gr-antd-color-picker"
        )
      }, a & /*$mergedProps*/
      4 && {
        id: (
          /*$mergedProps*/
          o[2].elem_id
        )
      }, a & /*$mergedProps*/
      4 && me(
        /*$mergedProps*/
        o[2].restProps
      ), a & /*$mergedProps*/
      4 && me(
        /*$mergedProps*/
        o[2].props
      ), a & /*$mergedProps*/
      4 && me(mt(
        /*$mergedProps*/
        o[2],
        {
          change_complete: "changeComplete",
          open_change: "openChange",
          format_change: "formatChange"
        }
      )), a & /*$mergedProps, undefined*/
      4 && {
        value: (
          /*$mergedProps*/
          o[2].props.value ?? /*$mergedProps*/
          o[2].value ?? void 0
        )
      }, a & /*$slots*/
      8 && {
        slots: (
          /*$slots*/
          o[3]
        )
      }, a & /*$presets*/
      16 && {
        presetItems: (
          /*$presets*/
          o[4]
        )
      }, a & /*value_format*/
      2 && {
        value_format: (
          /*value_format*/
          o[1]
        )
      }, a & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          o[21]
        )
      }, a & /*setSlotParams*/
      512 && {
        setSlotParams: (
          /*setSlotParams*/
          o[9]
        )
      }]) : {};
      a & /*$$scope*/
      4194304 && (s.$$scope = {
        dirty: a,
        ctx: o
      }), t.$set(s);
    },
    i(o) {
      n || (z(t.$$.fragment, o), n = !0);
    },
    o(o) {
      W(t.$$.fragment, o), n = !1;
    },
    d(o) {
      Js(t, o);
    }
  };
}
function uu(e) {
  let t;
  const n = (
    /*#slots*/
    e[20].default
  ), r = Xs(
    n,
    e,
    /*$$scope*/
    e[22],
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
      4194304) && iu(
        r,
        n,
        i,
        /*$$scope*/
        i[22],
        t ? Qs(
          n,
          /*$$scope*/
          i[22],
          o,
          null
        ) : Ws(
          /*$$scope*/
          i[22]
        ),
        null
      );
    },
    i(i) {
      t || (z(r, i), t = !0);
    },
    o(i) {
      W(r, i), t = !1;
    },
    d(i) {
      r && r.d(i);
    }
  };
}
function lu(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function fu(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[2].visible && wt(e)
  );
  return {
    c() {
      r && r.c(), t = le();
    },
    l(i) {
      r && r.l(i), t = le();
    },
    m(i, o) {
      r && r.m(i, o), on(i, t, o), n = !0;
    },
    p(i, [o]) {
      /*$mergedProps*/
      i[2].visible ? r ? (r.p(i, o), o & /*$mergedProps*/
      4 && z(r, 1)) : (r = wt(i), r.c(), z(r, 1), r.m(t.parentNode, t)) : r && (ks(), W(r, 1, 1, () => {
        r = null;
      }), Hs());
    },
    i(i) {
      n || (z(r), n = !0);
    },
    o(i) {
      W(r), n = !1;
    },
    d(i) {
      i && rn(t), r && r.d(i);
    }
  };
}
function cu(e, t, n) {
  const r = ["gradio", "props", "_internal", "value", "value_format", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let i = Tt(t, r), o, a, s, u, {
    $$slots: f = {},
    $$scope: p
  } = t;
  const d = _s(() => import("./color-picker-CFwNzWoz.js"));
  let {
    gradio: h
  } = t, {
    props: b = {}
  } = t;
  const l = C(b);
  re(e, l, (_) => n(19, o = _));
  let {
    _internal: g = {}
  } = t, {
    value: c
  } = t, {
    value_format: v = "hex"
  } = t, {
    as_item: w
  } = t, {
    visible: M = !0
  } = t, {
    elem_id: I = ""
  } = t, {
    elem_classes: j = []
  } = t, {
    elem_style: te = {}
  } = t;
  const [Ge, an] = Fs({
    gradio: h,
    props: o,
    _internal: g,
    visible: M,
    elem_id: I,
    elem_classes: j,
    elem_style: te,
    as_item: w,
    value: c,
    restProps: i
  });
  re(e, Ge, (_) => n(2, a = _));
  const Be = Cs();
  re(e, Be, (_) => n(3, s = _));
  const sn = Is(), {
    presets: ze
  } = Bs(["presets"]);
  re(e, ze, (_) => n(4, u = _));
  const un = (_) => {
    n(0, c = _);
  };
  return e.$$set = (_) => {
    t = Ae(Ae({}, t), Zs(_)), n(24, i = Tt(t, r)), "gradio" in _ && n(11, h = _.gradio), "props" in _ && n(12, b = _.props), "_internal" in _ && n(13, g = _._internal), "value" in _ && n(0, c = _.value), "value_format" in _ && n(1, v = _.value_format), "as_item" in _ && n(14, w = _.as_item), "visible" in _ && n(15, M = _.visible), "elem_id" in _ && n(16, I = _.elem_id), "elem_classes" in _ && n(17, j = _.elem_classes), "elem_style" in _ && n(18, te = _.elem_style), "$$scope" in _ && n(22, p = _.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    4096 && l.update((_) => ({
      ..._,
      ...b
    })), an({
      gradio: h,
      props: o,
      _internal: g,
      visible: M,
      elem_id: I,
      elem_classes: j,
      elem_style: te,
      as_item: w,
      value: c,
      restProps: i
    });
  }, [c, v, a, s, u, d, l, Ge, Be, sn, ze, h, b, g, w, M, I, j, te, o, f, un, p];
}
class hu extends zs {
  constructor(t) {
    super(), tu(this, t, cu, fu, ru, {
      gradio: 11,
      props: 12,
      _internal: 13,
      value: 0,
      value_format: 1,
      as_item: 14,
      visible: 15,
      elem_id: 16,
      elem_classes: 17,
      elem_style: 18
    });
  }
  get gradio() {
    return this.$$.ctx[11];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), $();
  }
  get props() {
    return this.$$.ctx[12];
  }
  set props(t) {
    this.$$set({
      props: t
    }), $();
  }
  get _internal() {
    return this.$$.ctx[13];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), $();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
    }), $();
  }
  get value_format() {
    return this.$$.ctx[1];
  }
  set value_format(t) {
    this.$$set({
      value_format: t
    }), $();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), $();
  }
  get visible() {
    return this.$$.ctx[15];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), $();
  }
  get elem_id() {
    return this.$$.ctx[16];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), $();
  }
  get elem_classes() {
    return this.$$.ctx[17];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), $();
  }
  get elem_style() {
    return this.$$.ctx[18];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), $();
  }
}
export {
  hu as I,
  R as a,
  pu as d,
  du as g,
  C as w
};
