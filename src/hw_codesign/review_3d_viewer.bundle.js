/*!
 * hw-codesign interactive 3D review viewer.
 * Bundles Three.js 0.179.1 and Chevrotain 9.0.1.
 * Chevrotain is licensed under Apache-2.0; see the distribution NOTICE and LICENSE.
 *
 * Three.js MIT License:
 * The MIT License
 *
 * Copyright © 2010-2025 three.js authors
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

var HWReview3D=(()=>{var ia=Object.defineProperty;var Qu=Object.getOwnPropertyDescriptor;var eh=Object.getOwnPropertyNames;var th=Object.prototype.hasOwnProperty;var nh=(n,e)=>{for(var t in e)ia(n,t,{get:e[t],enumerable:!0})},ih=(n,e,t,i)=>{if(e&&typeof e=="object"||typeof e=="function")for(let r of eh(e))!th.call(n,r)&&r!==t&&ia(n,r,{get:()=>e[r],enumerable:!(i=Qu(e,r))||i.enumerable});return n};var rh=n=>ih(ia({},"__esModule",{value:!0}),n);var R_={};nh(R_,{mount:()=>A_});var jn={LEFT:0,MIDDLE:1,RIGHT:2,ROTATE:0,DOLLY:1,PAN:2},Jn={ROTATE:0,PAN:1,DOLLY_PAN:2,DOLLY_ROTATE:3},dl=0,za=1,fl=2;var Va=1,pl=2,Sn=3,un=0,wt=1,en=2,Nn=0,oi=1,Ga=2,Ha=3,Wa=4,ml=5,Wn=100,gl=101,_l=102,yl=103,vl=104,xl=200,El=201,Sl=202,Tl=203,Rs=204,ws=205,Ml=206,bl=207,Al=208,Rl=209,wl=210,Cl=211,Il=212,Pl=213,Ll=214,Js=0,$s=1,Qs=2,ai=3,eo=4,to=5,no=6,io=7,ro=0,Nl=1,Ol=2,On=0,Dl=1,Ul=2,Fl=3,kl=4,Bl=5,zl=6,Vl=7;var Xa=300,pi=301,mi=302,so=303,oo=304,Wr=306,Ln=1e3,Yt=1001,Cs=1002,Bt=1003,Gl=1004;var Xr=1005;var hn=1006,ao=1007;var $n=1008;var pn=1009,Ya=1010,qa=1011,Ji=1012,co=1013,Qn=1014,Tn=1015,$i=1016,lo=1017,uo=1018,Qi=1020,Ka=35902,Za=1021,ja=1022,tn=1023,Bi=1026,er=1027,Ja=1028,ho=1029,$a=1030,fo=1031;var po=1033,Yr=33776,qr=33777,Kr=33778,Zr=33779,mo=35840,go=35841,_o=35842,yo=35843,vo=36196,xo=37492,Eo=37496,So=37808,To=37809,Mo=37810,bo=37811,Ao=37812,Ro=37813,wo=37814,Co=37815,Io=37816,Po=37817,Lo=37818,No=37819,Oo=37820,Do=37821,jr=36492,Uo=36494,Fo=36495,Qa=36283,ko=36284,Bo=36285,zo=36286;var gr=2300,Is=2301,As=2302,Ra=2400,wa=2401,Ca=2402;var Hl=3200,Wl=3201;var ec=0,Xl=1,Dn="",pt="srgb",ci="srgb-linear",_r="linear",at="srgb";var si=7680;var Ia=519,Yl=512,ql=513,Kl=514,tc=515,Zl=516,jl=517,Jl=518,$l=519,Pa=35044;var nc="300 es",ln=2e3,yr=2001;var _n=class{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});let i=this._listeners;i[e]===void 0&&(i[e]=[]),i[e].indexOf(t)===-1&&i[e].push(t)}hasEventListener(e,t){let i=this._listeners;return i===void 0?!1:i[e]!==void 0&&i[e].indexOf(t)!==-1}removeEventListener(e,t){let i=this._listeners;if(i===void 0)return;let r=i[e];if(r!==void 0){let s=r.indexOf(t);s!==-1&&r.splice(s,1)}}dispatchEvent(e){let t=this._listeners;if(t===void 0)return;let i=t[e.type];if(i!==void 0){e.target=this;let r=i.slice(0);for(let s=0,o=r.length;s<o;s++)r[s].call(this,e);e.target=null}}},Ct=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Fc=1234567,pr=Math.PI/180,zi=180/Math.PI;function tr(){let n=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,i=Math.random()*4294967295|0;return(Ct[n&255]+Ct[n>>8&255]+Ct[n>>16&255]+Ct[n>>24&255]+"-"+Ct[e&255]+Ct[e>>8&255]+"-"+Ct[e>>16&15|64]+Ct[e>>24&255]+"-"+Ct[t&63|128]+Ct[t>>8&255]+"-"+Ct[t>>16&255]+Ct[t>>24&255]+Ct[i&255]+Ct[i>>8&255]+Ct[i>>16&255]+Ct[i>>24&255]).toLowerCase()}function et(n,e,t){return Math.max(e,Math.min(t,n))}function ic(n,e){return(n%e+e)%e}function sh(n,e,t,i,r){return i+(n-e)*(r-i)/(t-e)}function oh(n,e,t){return n!==e?(t-n)/(e-n):0}function mr(n,e,t){return(1-t)*n+t*e}function ah(n,e,t,i){return mr(n,e,1-Math.exp(-t*i))}function ch(n,e=1){return e-Math.abs(ic(n,e*2)-e)}function lh(n,e,t){return n<=e?0:n>=t?1:(n=(n-e)/(t-e),n*n*(3-2*n))}function uh(n,e,t){return n<=e?0:n>=t?1:(n=(n-e)/(t-e),n*n*n*(n*(n*6-15)+10))}function hh(n,e){return n+Math.floor(Math.random()*(e-n+1))}function dh(n,e){return n+Math.random()*(e-n)}function fh(n){return n*(.5-Math.random())}function ph(n){n!==void 0&&(Fc=n);let e=Fc+=1831565813;return e=Math.imul(e^e>>>15,e|1),e^=e+Math.imul(e^e>>>7,e|61),((e^e>>>14)>>>0)/4294967296}function mh(n){return n*pr}function gh(n){return n*zi}function _h(n){return(n&n-1)===0&&n!==0}function yh(n){return Math.pow(2,Math.ceil(Math.log(n)/Math.LN2))}function vh(n){return Math.pow(2,Math.floor(Math.log(n)/Math.LN2))}function xh(n,e,t,i,r){let s=Math.cos,o=Math.sin,c=s(t/2),l=o(t/2),a=s((e+i)/2),d=o((e+i)/2),p=s((e-i)/2),f=o((e-i)/2),m=s((i-e)/2),g=o((i-e)/2);switch(r){case"XYX":n.set(c*d,l*p,l*f,c*a);break;case"YZY":n.set(l*f,c*d,l*p,c*a);break;case"ZXZ":n.set(l*p,l*f,c*d,c*a);break;case"XZX":n.set(c*d,l*g,l*m,c*a);break;case"YXY":n.set(l*m,c*d,l*g,c*a);break;case"ZYZ":n.set(l*g,l*m,c*d,c*a);break;default:console.warn("THREE.MathUtils: .setQuaternionFromProperEuler() encountered an unknown order: "+r)}}function Ui(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return n/4294967295;case Uint16Array:return n/65535;case Uint8Array:return n/255;case Int32Array:return Math.max(n/2147483647,-1);case Int16Array:return Math.max(n/32767,-1);case Int8Array:return Math.max(n/127,-1);default:throw new Error("Invalid component type.")}}function Dt(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return Math.round(n*4294967295);case Uint16Array:return Math.round(n*65535);case Uint8Array:return Math.round(n*255);case Int32Array:return Math.round(n*2147483647);case Int16Array:return Math.round(n*32767);case Int8Array:return Math.round(n*127);default:throw new Error("Invalid component type.")}}var rc={DEG2RAD:pr,RAD2DEG:zi,generateUUID:tr,clamp:et,euclideanModulo:ic,mapLinear:sh,inverseLerp:oh,lerp:mr,damp:ah,pingpong:ch,smoothstep:lh,smootherstep:uh,randInt:hh,randFloat:dh,randFloatSpread:fh,seededRandom:ph,degToRad:mh,radToDeg:gh,isPowerOfTwo:_h,ceilPowerOfTwo:yh,floorPowerOfTwo:vh,setQuaternionFromProperEuler:xh,normalize:Dt,denormalize:Ui},ze=class n{constructor(e=0,t=0){n.prototype.isVector2=!0,this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){let t=this.x,i=this.y,r=e.elements;return this.x=r[0]*t+r[3]*i+r[6],this.y=r[1]*t+r[4]*i+r[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=et(this.x,e.x,t.x),this.y=et(this.y,e.y,t.y),this}clampScalar(e,t){return this.x=et(this.x,e,t),this.y=et(this.y,e,t),this}clampLength(e,t){let i=this.length();return this.divideScalar(i||1).multiplyScalar(et(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){let t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;let i=this.dot(e)/t;return Math.acos(et(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){let t=this.x-e.x,i=this.y-e.y;return t*t+i*i}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){let i=Math.cos(t),r=Math.sin(t),s=this.x-e.x,o=this.y-e.y;return this.x=s*i-o*r+e.x,this.y=s*r+o*i+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}},zt=class{constructor(e=0,t=0,i=0,r=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=i,this._w=r}static slerpFlat(e,t,i,r,s,o,c){let l=i[r+0],a=i[r+1],d=i[r+2],p=i[r+3],f=s[o+0],m=s[o+1],g=s[o+2],y=s[o+3];if(c===0){e[t+0]=l,e[t+1]=a,e[t+2]=d,e[t+3]=p;return}if(c===1){e[t+0]=f,e[t+1]=m,e[t+2]=g,e[t+3]=y;return}if(p!==y||l!==f||a!==m||d!==g){let h=1-c,u=l*f+a*m+d*g+p*y,E=u>=0?1:-1,x=1-u*u;if(x>Number.EPSILON){let A=Math.sqrt(x),N=Math.atan2(A,u*E);h=Math.sin(h*N)/A,c=Math.sin(c*N)/A}let _=c*E;if(l=l*h+f*_,a=a*h+m*_,d=d*h+g*_,p=p*h+y*_,h===1-c){let A=1/Math.sqrt(l*l+a*a+d*d+p*p);l*=A,a*=A,d*=A,p*=A}}e[t]=l,e[t+1]=a,e[t+2]=d,e[t+3]=p}static multiplyQuaternionsFlat(e,t,i,r,s,o){let c=i[r],l=i[r+1],a=i[r+2],d=i[r+3],p=s[o],f=s[o+1],m=s[o+2],g=s[o+3];return e[t]=c*g+d*p+l*m-a*f,e[t+1]=l*g+d*f+a*p-c*m,e[t+2]=a*g+d*m+c*f-l*p,e[t+3]=d*g-c*p-l*f-a*m,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,i,r){return this._x=e,this._y=t,this._z=i,this._w=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){let i=e._x,r=e._y,s=e._z,o=e._order,c=Math.cos,l=Math.sin,a=c(i/2),d=c(r/2),p=c(s/2),f=l(i/2),m=l(r/2),g=l(s/2);switch(o){case"XYZ":this._x=f*d*p+a*m*g,this._y=a*m*p-f*d*g,this._z=a*d*g+f*m*p,this._w=a*d*p-f*m*g;break;case"YXZ":this._x=f*d*p+a*m*g,this._y=a*m*p-f*d*g,this._z=a*d*g-f*m*p,this._w=a*d*p+f*m*g;break;case"ZXY":this._x=f*d*p-a*m*g,this._y=a*m*p+f*d*g,this._z=a*d*g+f*m*p,this._w=a*d*p-f*m*g;break;case"ZYX":this._x=f*d*p-a*m*g,this._y=a*m*p+f*d*g,this._z=a*d*g-f*m*p,this._w=a*d*p+f*m*g;break;case"YZX":this._x=f*d*p+a*m*g,this._y=a*m*p+f*d*g,this._z=a*d*g-f*m*p,this._w=a*d*p-f*m*g;break;case"XZY":this._x=f*d*p-a*m*g,this._y=a*m*p-f*d*g,this._z=a*d*g+f*m*p,this._w=a*d*p+f*m*g;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+o)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){let i=t/2,r=Math.sin(i);return this._x=e.x*r,this._y=e.y*r,this._z=e.z*r,this._w=Math.cos(i),this._onChangeCallback(),this}setFromRotationMatrix(e){let t=e.elements,i=t[0],r=t[4],s=t[8],o=t[1],c=t[5],l=t[9],a=t[2],d=t[6],p=t[10],f=i+c+p;if(f>0){let m=.5/Math.sqrt(f+1);this._w=.25/m,this._x=(d-l)*m,this._y=(s-a)*m,this._z=(o-r)*m}else if(i>c&&i>p){let m=2*Math.sqrt(1+i-c-p);this._w=(d-l)/m,this._x=.25*m,this._y=(r+o)/m,this._z=(s+a)/m}else if(c>p){let m=2*Math.sqrt(1+c-i-p);this._w=(s-a)/m,this._x=(r+o)/m,this._y=.25*m,this._z=(l+d)/m}else{let m=2*Math.sqrt(1+p-i-c);this._w=(o-r)/m,this._x=(s+a)/m,this._y=(l+d)/m,this._z=.25*m}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let i=e.dot(t)+1;return i<1e-8?(i=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=i):(this._x=0,this._y=-e.z,this._z=e.y,this._w=i)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=i),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(et(this.dot(e),-1,1)))}rotateTowards(e,t){let i=this.angleTo(e);if(i===0)return this;let r=Math.min(1,t/i);return this.slerp(e,r),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){let i=e._x,r=e._y,s=e._z,o=e._w,c=t._x,l=t._y,a=t._z,d=t._w;return this._x=i*d+o*c+r*a-s*l,this._y=r*d+o*l+s*c-i*a,this._z=s*d+o*a+i*l-r*c,this._w=o*d-i*c-r*l-s*a,this._onChangeCallback(),this}slerp(e,t){if(t===0)return this;if(t===1)return this.copy(e);let i=this._x,r=this._y,s=this._z,o=this._w,c=o*e._w+i*e._x+r*e._y+s*e._z;if(c<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,c=-c):this.copy(e),c>=1)return this._w=o,this._x=i,this._y=r,this._z=s,this;let l=1-c*c;if(l<=Number.EPSILON){let m=1-t;return this._w=m*o+t*this._w,this._x=m*i+t*this._x,this._y=m*r+t*this._y,this._z=m*s+t*this._z,this.normalize(),this}let a=Math.sqrt(l),d=Math.atan2(a,c),p=Math.sin((1-t)*d)/a,f=Math.sin(t*d)/a;return this._w=o*p+this._w*f,this._x=i*p+this._x*f,this._y=r*p+this._y*f,this._z=s*p+this._z*f,this._onChangeCallback(),this}slerpQuaternions(e,t,i){return this.copy(e).slerp(t,i)}random(){let e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),i=Math.random(),r=Math.sqrt(1-i),s=Math.sqrt(i);return this.set(r*Math.sin(e),r*Math.cos(e),s*Math.sin(t),s*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}},Z=class n{constructor(e=0,t=0,i=0){n.prototype.isVector3=!0,this.x=e,this.y=t,this.z=i}set(e,t,i){return i===void 0&&(i=this.z),this.x=e,this.y=t,this.z=i,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion(kc.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion(kc.setFromAxisAngle(e,t))}applyMatrix3(e){let t=this.x,i=this.y,r=this.z,s=e.elements;return this.x=s[0]*t+s[3]*i+s[6]*r,this.y=s[1]*t+s[4]*i+s[7]*r,this.z=s[2]*t+s[5]*i+s[8]*r,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){let t=this.x,i=this.y,r=this.z,s=e.elements,o=1/(s[3]*t+s[7]*i+s[11]*r+s[15]);return this.x=(s[0]*t+s[4]*i+s[8]*r+s[12])*o,this.y=(s[1]*t+s[5]*i+s[9]*r+s[13])*o,this.z=(s[2]*t+s[6]*i+s[10]*r+s[14])*o,this}applyQuaternion(e){let t=this.x,i=this.y,r=this.z,s=e.x,o=e.y,c=e.z,l=e.w,a=2*(o*r-c*i),d=2*(c*t-s*r),p=2*(s*i-o*t);return this.x=t+l*a+o*p-c*d,this.y=i+l*d+c*a-s*p,this.z=r+l*p+s*d-o*a,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){let t=this.x,i=this.y,r=this.z,s=e.elements;return this.x=s[0]*t+s[4]*i+s[8]*r,this.y=s[1]*t+s[5]*i+s[9]*r,this.z=s[2]*t+s[6]*i+s[10]*r,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=et(this.x,e.x,t.x),this.y=et(this.y,e.y,t.y),this.z=et(this.z,e.z,t.z),this}clampScalar(e,t){return this.x=et(this.x,e,t),this.y=et(this.y,e,t),this.z=et(this.z,e,t),this}clampLength(e,t){let i=this.length();return this.divideScalar(i||1).multiplyScalar(et(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){let i=e.x,r=e.y,s=e.z,o=t.x,c=t.y,l=t.z;return this.x=r*l-s*c,this.y=s*o-i*l,this.z=i*c-r*o,this}projectOnVector(e){let t=e.lengthSq();if(t===0)return this.set(0,0,0);let i=e.dot(this)/t;return this.copy(e).multiplyScalar(i)}projectOnPlane(e){return ra.copy(this).projectOnVector(e),this.sub(ra)}reflect(e){return this.sub(ra.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){let t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;let i=this.dot(e)/t;return Math.acos(et(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){let t=this.x-e.x,i=this.y-e.y,r=this.z-e.z;return t*t+i*i+r*r}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,i){let r=Math.sin(t)*e;return this.x=r*Math.sin(i),this.y=Math.cos(t)*e,this.z=r*Math.cos(i),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,i){return this.x=e*Math.sin(t),this.y=i,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){let t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){let t=this.setFromMatrixColumn(e,0).length(),i=this.setFromMatrixColumn(e,1).length(),r=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=i,this.z=r,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){let e=Math.random()*Math.PI*2,t=Math.random()*2-1,i=Math.sqrt(1-t*t);return this.x=i*Math.cos(e),this.y=t,this.z=i*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}},ra=new Z,kc=new zt,Ze=class n{constructor(e,t,i,r,s,o,c,l,a){n.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,i,r,s,o,c,l,a)}set(e,t,i,r,s,o,c,l,a){let d=this.elements;return d[0]=e,d[1]=r,d[2]=c,d[3]=t,d[4]=s,d[5]=l,d[6]=i,d[7]=o,d[8]=a,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){let t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],this}extractBasis(e,t,i){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),i.setFromMatrix3Column(this,2),this}setFromMatrix4(e){let t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){let i=e.elements,r=t.elements,s=this.elements,o=i[0],c=i[3],l=i[6],a=i[1],d=i[4],p=i[7],f=i[2],m=i[5],g=i[8],y=r[0],h=r[3],u=r[6],E=r[1],x=r[4],_=r[7],A=r[2],N=r[5],w=r[8];return s[0]=o*y+c*E+l*A,s[3]=o*h+c*x+l*N,s[6]=o*u+c*_+l*w,s[1]=a*y+d*E+p*A,s[4]=a*h+d*x+p*N,s[7]=a*u+d*_+p*w,s[2]=f*y+m*E+g*A,s[5]=f*h+m*x+g*N,s[8]=f*u+m*_+g*w,this}multiplyScalar(e){let t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){let e=this.elements,t=e[0],i=e[1],r=e[2],s=e[3],o=e[4],c=e[5],l=e[6],a=e[7],d=e[8];return t*o*d-t*c*a-i*s*d+i*c*l+r*s*a-r*o*l}invert(){let e=this.elements,t=e[0],i=e[1],r=e[2],s=e[3],o=e[4],c=e[5],l=e[6],a=e[7],d=e[8],p=d*o-c*a,f=c*l-d*s,m=a*s-o*l,g=t*p+i*f+r*m;if(g===0)return this.set(0,0,0,0,0,0,0,0,0);let y=1/g;return e[0]=p*y,e[1]=(r*a-d*i)*y,e[2]=(c*i-r*o)*y,e[3]=f*y,e[4]=(d*t-r*l)*y,e[5]=(r*s-c*t)*y,e[6]=m*y,e[7]=(i*l-a*t)*y,e[8]=(o*t-i*s)*y,this}transpose(){let e,t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){let t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,i,r,s,o,c){let l=Math.cos(s),a=Math.sin(s);return this.set(i*l,i*a,-i*(l*o+a*c)+o+e,-r*a,r*l,-r*(-a*o+l*c)+c+t,0,0,1),this}scale(e,t){return this.premultiply(sa.makeScale(e,t)),this}rotate(e){return this.premultiply(sa.makeRotation(-e)),this}translate(e,t){return this.premultiply(sa.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){let t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,i,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){let t=this.elements,i=e.elements;for(let r=0;r<9;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<9;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){let i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e}clone(){return new this.constructor().fromArray(this.elements)}},sa=new Ze;function sc(n){for(let e=n.length-1;e>=0;--e)if(n[e]>=65535)return!0;return!1}function Vi(n){return document.createElementNS("http://www.w3.org/1999/xhtml",n)}function Ql(){let n=Vi("canvas");return n.style.display="block",n}var Bc={};function li(n){n in Bc||(Bc[n]=!0,console.warn(n))}function eu(n,e,t){return new Promise(function(i,r){function s(){switch(n.clientWaitSync(e,n.SYNC_FLUSH_COMMANDS_BIT,0)){case n.WAIT_FAILED:r();break;case n.TIMEOUT_EXPIRED:setTimeout(s,t);break;default:i()}}setTimeout(s,t)})}var zc=new Ze().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),Vc=new Ze().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function Eh(){let n={enabled:!0,workingColorSpace:ci,spaces:{},convert:function(r,s,o){return this.enabled===!1||s===o||!s||!o||(this.spaces[s].transfer===at&&(r.r=Pn(r.r),r.g=Pn(r.g),r.b=Pn(r.b)),this.spaces[s].primaries!==this.spaces[o].primaries&&(r.applyMatrix3(this.spaces[s].toXYZ),r.applyMatrix3(this.spaces[o].fromXYZ)),this.spaces[o].transfer===at&&(r.r=Fi(r.r),r.g=Fi(r.g),r.b=Fi(r.b))),r},workingToColorSpace:function(r,s){return this.convert(r,this.workingColorSpace,s)},colorSpaceToWorking:function(r,s){return this.convert(r,s,this.workingColorSpace)},getPrimaries:function(r){return this.spaces[r].primaries},getTransfer:function(r){return r===Dn?_r:this.spaces[r].transfer},getLuminanceCoefficients:function(r,s=this.workingColorSpace){return r.fromArray(this.spaces[s].luminanceCoefficients)},define:function(r){Object.assign(this.spaces,r)},_getMatrix:function(r,s,o){return r.copy(this.spaces[s].toXYZ).multiply(this.spaces[o].fromXYZ)},_getDrawingBufferColorSpace:function(r){return this.spaces[r].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(r=this.workingColorSpace){return this.spaces[r].workingColorSpaceConfig.unpackColorSpace},fromWorkingColorSpace:function(r,s){return li("THREE.ColorManagement: .fromWorkingColorSpace() has been renamed to .workingToColorSpace()."),n.workingToColorSpace(r,s)},toWorkingColorSpace:function(r,s){return li("THREE.ColorManagement: .toWorkingColorSpace() has been renamed to .colorSpaceToWorking()."),n.colorSpaceToWorking(r,s)}},e=[.64,.33,.3,.6,.15,.06],t=[.2126,.7152,.0722],i=[.3127,.329];return n.define({[ci]:{primaries:e,whitePoint:i,transfer:_r,toXYZ:zc,fromXYZ:Vc,luminanceCoefficients:t,workingColorSpaceConfig:{unpackColorSpace:pt},outputColorSpaceConfig:{drawingBufferColorSpace:pt}},[pt]:{primaries:e,whitePoint:i,transfer:at,toXYZ:zc,fromXYZ:Vc,luminanceCoefficients:t,outputColorSpaceConfig:{drawingBufferColorSpace:pt}}}),n}var nt=Eh();function Pn(n){return n<.04045?n*.0773993808:Math.pow(n*.9478672986+.0521327014,2.4)}function Fi(n){return n<.0031308?n*12.92:1.055*Math.pow(n,.41666)-.055}var Ti,Ps=class{static getDataURL(e,t="image/png"){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let i;if(e instanceof HTMLCanvasElement)i=e;else{Ti===void 0&&(Ti=Vi("canvas")),Ti.width=e.width,Ti.height=e.height;let r=Ti.getContext("2d");e instanceof ImageData?r.putImageData(e,0,0):r.drawImage(e,0,0,e.width,e.height),i=Ti}return i.toDataURL(t)}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){let t=Vi("canvas");t.width=e.width,t.height=e.height;let i=t.getContext("2d");i.drawImage(e,0,0,e.width,e.height);let r=i.getImageData(0,0,e.width,e.height),s=r.data;for(let o=0;o<s.length;o++)s[o]=Pn(s[o]/255)*255;return i.putImageData(r,0,0),t}else if(e.data){let t=e.data.slice(0);for(let i=0;i<t.length;i++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[i]=Math.floor(Pn(t[i]/255)*255):t[i]=Pn(t[i]);return{data:t,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}},Sh=0,Gi=class{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:Sh++}),this.uuid=tr(),this.data=e,this.dataReady=!0,this.version=0}getSize(e){let t=this.data;return t instanceof HTMLVideoElement?e.set(t.videoWidth,t.videoHeight,0):t instanceof VideoFrame?e.set(t.displayHeight,t.displayWidth,0):t!==null?e.set(t.width,t.height,t.depth||0):e.set(0,0,0),e}set needsUpdate(e){e===!0&&this.version++}toJSON(e){let t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];let i={uuid:this.uuid,url:""},r=this.data;if(r!==null){let s;if(Array.isArray(r)){s=[];for(let o=0,c=r.length;o<c;o++)r[o].isDataTexture?s.push(oa(r[o].image)):s.push(oa(r[o]))}else s=oa(r);i.url=s}return t||(e.images[this.uuid]=i),i}};function oa(n){return typeof HTMLImageElement<"u"&&n instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&n instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&n instanceof ImageBitmap?Ps.getDataURL(n):n.data?{data:Array.from(n.data),width:n.width,height:n.height,type:n.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}var Th=0,aa=new Z,Ft=class n extends _n{constructor(e=n.DEFAULT_IMAGE,t=n.DEFAULT_MAPPING,i=Yt,r=Yt,s=hn,o=$n,c=tn,l=pn,a=n.DEFAULT_ANISOTROPY,d=Dn){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:Th++}),this.uuid=tr(),this.name="",this.source=new Gi(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=i,this.wrapT=r,this.magFilter=s,this.minFilter=o,this.anisotropy=a,this.format=c,this.internalFormat=null,this.type=l,this.offset=new ze(0,0),this.repeat=new ze(1,1),this.center=new ze(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new Ze,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=d,this.userData={},this.updateRanges=[],this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.isArrayTexture=!!(e&&e.depth&&e.depth>1),this.pmremVersion=0}get width(){return this.source.getSize(aa).x}get height(){return this.source.getSize(aa).y}get depth(){return this.source.getSize(aa).z}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.isArrayTexture=e.isArrayTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}setValues(e){for(let t in e){let i=e[t];if(i===void 0){console.warn(`THREE.Texture.setValues(): parameter '${t}' has value of undefined.`);continue}let r=this[t];if(r===void 0){console.warn(`THREE.Texture.setValues(): property '${t}' does not exist.`);continue}r&&i&&r.isVector2&&i.isVector2||r&&i&&r.isVector3&&i.isVector3||r&&i&&r.isMatrix3&&i.isMatrix3?r.copy(i):this[t]=i}}toJSON(e){let t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];let i={metadata:{version:4.7,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(i.userData=this.userData),t||(e.textures[this.uuid]=i),i}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==Xa)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Ln:e.x=e.x-Math.floor(e.x);break;case Yt:e.x=e.x<0?0:1;break;case Cs:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Ln:e.y=e.y-Math.floor(e.y);break;case Yt:e.y=e.y<0?0:1;break;case Cs:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}};Ft.DEFAULT_IMAGE=null;Ft.DEFAULT_MAPPING=Xa;Ft.DEFAULT_ANISOTROPY=1;var vt=class n{constructor(e=0,t=0,i=0,r=1){n.prototype.isVector4=!0,this.x=e,this.y=t,this.z=i,this.w=r}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,i,r){return this.x=e,this.y=t,this.z=i,this.w=r,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){let t=this.x,i=this.y,r=this.z,s=this.w,o=e.elements;return this.x=o[0]*t+o[4]*i+o[8]*r+o[12]*s,this.y=o[1]*t+o[5]*i+o[9]*r+o[13]*s,this.z=o[2]*t+o[6]*i+o[10]*r+o[14]*s,this.w=o[3]*t+o[7]*i+o[11]*r+o[15]*s,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);let t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,i,r,s,l=e.elements,a=l[0],d=l[4],p=l[8],f=l[1],m=l[5],g=l[9],y=l[2],h=l[6],u=l[10];if(Math.abs(d-f)<.01&&Math.abs(p-y)<.01&&Math.abs(g-h)<.01){if(Math.abs(d+f)<.1&&Math.abs(p+y)<.1&&Math.abs(g+h)<.1&&Math.abs(a+m+u-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;let x=(a+1)/2,_=(m+1)/2,A=(u+1)/2,N=(d+f)/4,w=(p+y)/4,O=(g+h)/4;return x>_&&x>A?x<.01?(i=0,r=.707106781,s=.707106781):(i=Math.sqrt(x),r=N/i,s=w/i):_>A?_<.01?(i=.707106781,r=0,s=.707106781):(r=Math.sqrt(_),i=N/r,s=O/r):A<.01?(i=.707106781,r=.707106781,s=0):(s=Math.sqrt(A),i=w/s,r=O/s),this.set(i,r,s,t),this}let E=Math.sqrt((h-g)*(h-g)+(p-y)*(p-y)+(f-d)*(f-d));return Math.abs(E)<.001&&(E=1),this.x=(h-g)/E,this.y=(p-y)/E,this.z=(f-d)/E,this.w=Math.acos((a+m+u-1)/2),this}setFromMatrixPosition(e){let t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=et(this.x,e.x,t.x),this.y=et(this.y,e.y,t.y),this.z=et(this.z,e.z,t.z),this.w=et(this.w,e.w,t.w),this}clampScalar(e,t){return this.x=et(this.x,e,t),this.y=et(this.y,e,t),this.z=et(this.z,e,t),this.w=et(this.w,e,t),this}clampLength(e,t){let i=this.length();return this.divideScalar(i||1).multiplyScalar(et(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this.w=e.w+(t.w-e.w)*i,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}},Ls=class extends _n{constructor(e=1,t=1,i={}){super(),i=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:hn,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1,depth:1,multiview:!1},i),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=i.depth,this.scissor=new vt(0,0,e,t),this.scissorTest=!1,this.viewport=new vt(0,0,e,t);let r={width:e,height:t,depth:i.depth},s=new Ft(r);this.textures=[];let o=i.count;for(let c=0;c<o;c++)this.textures[c]=s.clone(),this.textures[c].isRenderTargetTexture=!0,this.textures[c].renderTarget=this;this._setTextureOptions(i),this.depthBuffer=i.depthBuffer,this.stencilBuffer=i.stencilBuffer,this.resolveDepthBuffer=i.resolveDepthBuffer,this.resolveStencilBuffer=i.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=i.depthTexture,this.samples=i.samples,this.multiview=i.multiview}_setTextureOptions(e={}){let t={minFilter:hn,generateMipmaps:!1,flipY:!1,internalFormat:null};e.mapping!==void 0&&(t.mapping=e.mapping),e.wrapS!==void 0&&(t.wrapS=e.wrapS),e.wrapT!==void 0&&(t.wrapT=e.wrapT),e.wrapR!==void 0&&(t.wrapR=e.wrapR),e.magFilter!==void 0&&(t.magFilter=e.magFilter),e.minFilter!==void 0&&(t.minFilter=e.minFilter),e.format!==void 0&&(t.format=e.format),e.type!==void 0&&(t.type=e.type),e.anisotropy!==void 0&&(t.anisotropy=e.anisotropy),e.colorSpace!==void 0&&(t.colorSpace=e.colorSpace),e.flipY!==void 0&&(t.flipY=e.flipY),e.generateMipmaps!==void 0&&(t.generateMipmaps=e.generateMipmaps),e.internalFormat!==void 0&&(t.internalFormat=e.internalFormat);for(let i=0;i<this.textures.length;i++)this.textures[i].setValues(t)}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),e!==null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,t,i=1){if(this.width!==e||this.height!==t||this.depth!==i){this.width=e,this.height=t,this.depth=i;for(let r=0,s=this.textures.length;r<s;r++)this.textures[r].image.width=e,this.textures[r].image.height=t,this.textures[r].image.depth=i,this.textures[r].isArrayTexture=this.textures[r].image.depth>1;this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let t=0,i=e.textures.length;t<i;t++){this.textures[t]=e.textures[t].clone(),this.textures[t].isRenderTargetTexture=!0,this.textures[t].renderTarget=this;let r=Object.assign({},e.textures[t].image);this.textures[t].source=new Gi(r)}return this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}},yn=class extends Ls{constructor(e=1,t=1,i={}){super(e,t,i),this.isWebGLRenderTarget=!0}},vr=class extends Ft{constructor(e=null,t=1,i=1,r=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=Bt,this.minFilter=Bt,this.wrapR=Yt,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}};var Ns=class extends Ft{constructor(e=null,t=1,i=1,r=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=Bt,this.minFilter=Bt,this.wrapR=Yt,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}};var vn=class{constructor(e=new Z(1/0,1/0,1/0),t=new Z(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t+=3)this.expandByPoint(on.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,i=e.count;t<i;t++)this.expandByPoint(on.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){let i=on.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(i),this.max.copy(e).add(i),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);let i=e.geometry;if(i!==void 0){let s=i.getAttribute("position");if(t===!0&&s!==void 0&&e.isInstancedMesh!==!0)for(let o=0,c=s.count;o<c;o++)e.isMesh===!0?e.getVertexPosition(o,on):on.fromBufferAttribute(s,o),on.applyMatrix4(e.matrixWorld),this.expandByPoint(on);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),ns.copy(e.boundingBox)):(i.boundingBox===null&&i.computeBoundingBox(),ns.copy(i.boundingBox)),ns.applyMatrix4(e.matrixWorld),this.union(ns)}let r=e.children;for(let s=0,o=r.length;s<o;s++)this.expandByObject(r[s],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,on),on.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,i;return e.normal.x>0?(t=e.normal.x*this.min.x,i=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,i=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,i+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,i+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,i+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,i+=e.normal.z*this.min.z),t<=-e.constant&&i>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(cr),is.subVectors(this.max,cr),Mi.subVectors(e.a,cr),bi.subVectors(e.b,cr),Ai.subVectors(e.c,cr),Fn.subVectors(bi,Mi),kn.subVectors(Ai,bi),ti.subVectors(Mi,Ai);let t=[0,-Fn.z,Fn.y,0,-kn.z,kn.y,0,-ti.z,ti.y,Fn.z,0,-Fn.x,kn.z,0,-kn.x,ti.z,0,-ti.x,-Fn.y,Fn.x,0,-kn.y,kn.x,0,-ti.y,ti.x,0];return!ca(t,Mi,bi,Ai,is)||(t=[1,0,0,0,1,0,0,0,1],!ca(t,Mi,bi,Ai,is))?!1:(rs.crossVectors(Fn,kn),t=[rs.x,rs.y,rs.z],ca(t,Mi,bi,Ai,is))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,on).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(on).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(bn[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),bn[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),bn[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),bn[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),bn[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),bn[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),bn[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),bn[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(bn),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}toJSON(){return{min:this.min.toArray(),max:this.max.toArray()}}fromJSON(e){return this.min.fromArray(e.min),this.max.fromArray(e.max),this}},bn=[new Z,new Z,new Z,new Z,new Z,new Z,new Z,new Z],on=new Z,ns=new vn,Mi=new Z,bi=new Z,Ai=new Z,Fn=new Z,kn=new Z,ti=new Z,cr=new Z,is=new Z,rs=new Z,ni=new Z;function ca(n,e,t,i,r){for(let s=0,o=n.length-3;s<=o;s+=3){ni.fromArray(n,s);let c=r.x*Math.abs(ni.x)+r.y*Math.abs(ni.y)+r.z*Math.abs(ni.z),l=e.dot(ni),a=t.dot(ni),d=i.dot(ni);if(Math.max(-Math.max(l,a,d),Math.min(l,a,d))>c)return!1}return!0}var Mh=new vn,lr=new Z,la=new Z,Xn=class{constructor(e=new Z,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){let i=this.center;t!==void 0?i.copy(t):Mh.setFromPoints(e).getCenter(i);let r=0;for(let s=0,o=e.length;s<o;s++)r=Math.max(r,i.distanceToSquared(e[s]));return this.radius=Math.sqrt(r),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){let t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){let i=this.center.distanceToSquared(e);return t.copy(e),i>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;lr.subVectors(e,this.center);let t=lr.lengthSq();if(t>this.radius*this.radius){let i=Math.sqrt(t),r=(i-this.radius)*.5;this.center.addScaledVector(lr,r/i),this.radius+=r}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(la.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(lr.copy(e.center).add(la)),this.expandByPoint(lr.copy(e.center).sub(la))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}toJSON(){return{radius:this.radius,center:this.center.toArray()}}fromJSON(e){return this.radius=e.radius,this.center.fromArray(e.center),this}},An=new Z,ua=new Z,ss=new Z,Bn=new Z,ha=new Z,os=new Z,da=new Z,Yn=class{constructor(e=new Z,t=new Z(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,An)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);let i=t.dot(this.direction);return i<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,i)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){let t=An.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(An.copy(this.origin).addScaledVector(this.direction,t),An.distanceToSquared(e))}distanceSqToSegment(e,t,i,r){ua.copy(e).add(t).multiplyScalar(.5),ss.copy(t).sub(e).normalize(),Bn.copy(this.origin).sub(ua);let s=e.distanceTo(t)*.5,o=-this.direction.dot(ss),c=Bn.dot(this.direction),l=-Bn.dot(ss),a=Bn.lengthSq(),d=Math.abs(1-o*o),p,f,m,g;if(d>0)if(p=o*l-c,f=o*c-l,g=s*d,p>=0)if(f>=-g)if(f<=g){let y=1/d;p*=y,f*=y,m=p*(p+o*f+2*c)+f*(o*p+f+2*l)+a}else f=s,p=Math.max(0,-(o*f+c)),m=-p*p+f*(f+2*l)+a;else f=-s,p=Math.max(0,-(o*f+c)),m=-p*p+f*(f+2*l)+a;else f<=-g?(p=Math.max(0,-(-o*s+c)),f=p>0?-s:Math.min(Math.max(-s,-l),s),m=-p*p+f*(f+2*l)+a):f<=g?(p=0,f=Math.min(Math.max(-s,-l),s),m=f*(f+2*l)+a):(p=Math.max(0,-(o*s+c)),f=p>0?s:Math.min(Math.max(-s,-l),s),m=-p*p+f*(f+2*l)+a);else f=o>0?-s:s,p=Math.max(0,-(o*f+c)),m=-p*p+f*(f+2*l)+a;return i&&i.copy(this.origin).addScaledVector(this.direction,p),r&&r.copy(ua).addScaledVector(ss,f),m}intersectSphere(e,t){An.subVectors(e.center,this.origin);let i=An.dot(this.direction),r=An.dot(An)-i*i,s=e.radius*e.radius;if(r>s)return null;let o=Math.sqrt(s-r),c=i-o,l=i+o;return l<0?null:c<0?this.at(l,t):this.at(c,t)}intersectsSphere(e){return e.radius<0?!1:this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){let t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;let i=-(this.origin.dot(e.normal)+e.constant)/t;return i>=0?i:null}intersectPlane(e,t){let i=this.distanceToPlane(e);return i===null?null:this.at(i,t)}intersectsPlane(e){let t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let i,r,s,o,c,l,a=1/this.direction.x,d=1/this.direction.y,p=1/this.direction.z,f=this.origin;return a>=0?(i=(e.min.x-f.x)*a,r=(e.max.x-f.x)*a):(i=(e.max.x-f.x)*a,r=(e.min.x-f.x)*a),d>=0?(s=(e.min.y-f.y)*d,o=(e.max.y-f.y)*d):(s=(e.max.y-f.y)*d,o=(e.min.y-f.y)*d),i>o||s>r||((s>i||isNaN(i))&&(i=s),(o<r||isNaN(r))&&(r=o),p>=0?(c=(e.min.z-f.z)*p,l=(e.max.z-f.z)*p):(c=(e.max.z-f.z)*p,l=(e.min.z-f.z)*p),i>l||c>r)||((c>i||i!==i)&&(i=c),(l<r||r!==r)&&(r=l),r<0)?null:this.at(i>=0?i:r,t)}intersectsBox(e){return this.intersectBox(e,An)!==null}intersectTriangle(e,t,i,r,s){ha.subVectors(t,e),os.subVectors(i,e),da.crossVectors(ha,os);let o=this.direction.dot(da),c;if(o>0){if(r)return null;c=1}else if(o<0)c=-1,o=-o;else return null;Bn.subVectors(this.origin,e);let l=c*this.direction.dot(os.crossVectors(Bn,os));if(l<0)return null;let a=c*this.direction.dot(ha.cross(Bn));if(a<0||l+a>o)return null;let d=-c*Bn.dot(da);return d<0?null:this.at(d/o,s)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}},yt=class n{constructor(e,t,i,r,s,o,c,l,a,d,p,f,m,g,y,h){n.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,i,r,s,o,c,l,a,d,p,f,m,g,y,h)}set(e,t,i,r,s,o,c,l,a,d,p,f,m,g,y,h){let u=this.elements;return u[0]=e,u[4]=t,u[8]=i,u[12]=r,u[1]=s,u[5]=o,u[9]=c,u[13]=l,u[2]=a,u[6]=d,u[10]=p,u[14]=f,u[3]=m,u[7]=g,u[11]=y,u[15]=h,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new n().fromArray(this.elements)}copy(e){let t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],t[9]=i[9],t[10]=i[10],t[11]=i[11],t[12]=i[12],t[13]=i[13],t[14]=i[14],t[15]=i[15],this}copyPosition(e){let t=this.elements,i=e.elements;return t[12]=i[12],t[13]=i[13],t[14]=i[14],this}setFromMatrix3(e){let t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,i){return e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),i.setFromMatrixColumn(this,2),this}makeBasis(e,t,i){return this.set(e.x,t.x,i.x,0,e.y,t.y,i.y,0,e.z,t.z,i.z,0,0,0,0,1),this}extractRotation(e){let t=this.elements,i=e.elements,r=1/Ri.setFromMatrixColumn(e,0).length(),s=1/Ri.setFromMatrixColumn(e,1).length(),o=1/Ri.setFromMatrixColumn(e,2).length();return t[0]=i[0]*r,t[1]=i[1]*r,t[2]=i[2]*r,t[3]=0,t[4]=i[4]*s,t[5]=i[5]*s,t[6]=i[6]*s,t[7]=0,t[8]=i[8]*o,t[9]=i[9]*o,t[10]=i[10]*o,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){let t=this.elements,i=e.x,r=e.y,s=e.z,o=Math.cos(i),c=Math.sin(i),l=Math.cos(r),a=Math.sin(r),d=Math.cos(s),p=Math.sin(s);if(e.order==="XYZ"){let f=o*d,m=o*p,g=c*d,y=c*p;t[0]=l*d,t[4]=-l*p,t[8]=a,t[1]=m+g*a,t[5]=f-y*a,t[9]=-c*l,t[2]=y-f*a,t[6]=g+m*a,t[10]=o*l}else if(e.order==="YXZ"){let f=l*d,m=l*p,g=a*d,y=a*p;t[0]=f+y*c,t[4]=g*c-m,t[8]=o*a,t[1]=o*p,t[5]=o*d,t[9]=-c,t[2]=m*c-g,t[6]=y+f*c,t[10]=o*l}else if(e.order==="ZXY"){let f=l*d,m=l*p,g=a*d,y=a*p;t[0]=f-y*c,t[4]=-o*p,t[8]=g+m*c,t[1]=m+g*c,t[5]=o*d,t[9]=y-f*c,t[2]=-o*a,t[6]=c,t[10]=o*l}else if(e.order==="ZYX"){let f=o*d,m=o*p,g=c*d,y=c*p;t[0]=l*d,t[4]=g*a-m,t[8]=f*a+y,t[1]=l*p,t[5]=y*a+f,t[9]=m*a-g,t[2]=-a,t[6]=c*l,t[10]=o*l}else if(e.order==="YZX"){let f=o*l,m=o*a,g=c*l,y=c*a;t[0]=l*d,t[4]=y-f*p,t[8]=g*p+m,t[1]=p,t[5]=o*d,t[9]=-c*d,t[2]=-a*d,t[6]=m*p+g,t[10]=f-y*p}else if(e.order==="XZY"){let f=o*l,m=o*a,g=c*l,y=c*a;t[0]=l*d,t[4]=-p,t[8]=a*d,t[1]=f*p+y,t[5]=o*d,t[9]=m*p-g,t[2]=g*p-m,t[6]=c*d,t[10]=y*p+f}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(bh,e,Ah)}lookAt(e,t,i){let r=this.elements;return Wt.subVectors(e,t),Wt.lengthSq()===0&&(Wt.z=1),Wt.normalize(),zn.crossVectors(i,Wt),zn.lengthSq()===0&&(Math.abs(i.z)===1?Wt.x+=1e-4:Wt.z+=1e-4,Wt.normalize(),zn.crossVectors(i,Wt)),zn.normalize(),as.crossVectors(Wt,zn),r[0]=zn.x,r[4]=as.x,r[8]=Wt.x,r[1]=zn.y,r[5]=as.y,r[9]=Wt.y,r[2]=zn.z,r[6]=as.z,r[10]=Wt.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){let i=e.elements,r=t.elements,s=this.elements,o=i[0],c=i[4],l=i[8],a=i[12],d=i[1],p=i[5],f=i[9],m=i[13],g=i[2],y=i[6],h=i[10],u=i[14],E=i[3],x=i[7],_=i[11],A=i[15],N=r[0],w=r[4],O=r[8],T=r[12],M=r[1],R=r[5],I=r[9],U=r[13],P=r[2],X=r[6],W=r[10],q=r[14],G=r[3],ee=r[7],ae=r[11],ue=r[15];return s[0]=o*N+c*M+l*P+a*G,s[4]=o*w+c*R+l*X+a*ee,s[8]=o*O+c*I+l*W+a*ae,s[12]=o*T+c*U+l*q+a*ue,s[1]=d*N+p*M+f*P+m*G,s[5]=d*w+p*R+f*X+m*ee,s[9]=d*O+p*I+f*W+m*ae,s[13]=d*T+p*U+f*q+m*ue,s[2]=g*N+y*M+h*P+u*G,s[6]=g*w+y*R+h*X+u*ee,s[10]=g*O+y*I+h*W+u*ae,s[14]=g*T+y*U+h*q+u*ue,s[3]=E*N+x*M+_*P+A*G,s[7]=E*w+x*R+_*X+A*ee,s[11]=E*O+x*I+_*W+A*ae,s[15]=E*T+x*U+_*q+A*ue,this}multiplyScalar(e){let t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){let e=this.elements,t=e[0],i=e[4],r=e[8],s=e[12],o=e[1],c=e[5],l=e[9],a=e[13],d=e[2],p=e[6],f=e[10],m=e[14],g=e[3],y=e[7],h=e[11],u=e[15];return g*(+s*l*p-r*a*p-s*c*f+i*a*f+r*c*m-i*l*m)+y*(+t*l*m-t*a*f+s*o*f-r*o*m+r*a*d-s*l*d)+h*(+t*a*p-t*c*m-s*o*p+i*o*m+s*c*d-i*a*d)+u*(-r*c*d-t*l*p+t*c*f+r*o*p-i*o*f+i*l*d)}transpose(){let e=this.elements,t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,i){let r=this.elements;return e.isVector3?(r[12]=e.x,r[13]=e.y,r[14]=e.z):(r[12]=e,r[13]=t,r[14]=i),this}invert(){let e=this.elements,t=e[0],i=e[1],r=e[2],s=e[3],o=e[4],c=e[5],l=e[6],a=e[7],d=e[8],p=e[9],f=e[10],m=e[11],g=e[12],y=e[13],h=e[14],u=e[15],E=p*h*a-y*f*a+y*l*m-c*h*m-p*l*u+c*f*u,x=g*f*a-d*h*a-g*l*m+o*h*m+d*l*u-o*f*u,_=d*y*a-g*p*a+g*c*m-o*y*m-d*c*u+o*p*u,A=g*p*l-d*y*l-g*c*f+o*y*f+d*c*h-o*p*h,N=t*E+i*x+r*_+s*A;if(N===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);let w=1/N;return e[0]=E*w,e[1]=(y*f*s-p*h*s-y*r*m+i*h*m+p*r*u-i*f*u)*w,e[2]=(c*h*s-y*l*s+y*r*a-i*h*a-c*r*u+i*l*u)*w,e[3]=(p*l*s-c*f*s-p*r*a+i*f*a+c*r*m-i*l*m)*w,e[4]=x*w,e[5]=(d*h*s-g*f*s+g*r*m-t*h*m-d*r*u+t*f*u)*w,e[6]=(g*l*s-o*h*s-g*r*a+t*h*a+o*r*u-t*l*u)*w,e[7]=(o*f*s-d*l*s+d*r*a-t*f*a-o*r*m+t*l*m)*w,e[8]=_*w,e[9]=(g*p*s-d*y*s-g*i*m+t*y*m+d*i*u-t*p*u)*w,e[10]=(o*y*s-g*c*s+g*i*a-t*y*a-o*i*u+t*c*u)*w,e[11]=(d*c*s-o*p*s-d*i*a+t*p*a+o*i*m-t*c*m)*w,e[12]=A*w,e[13]=(d*y*r-g*p*r+g*i*f-t*y*f-d*i*h+t*p*h)*w,e[14]=(g*c*r-o*y*r-g*i*l+t*y*l+o*i*h-t*c*h)*w,e[15]=(o*p*r-d*c*r+d*i*l-t*p*l-o*i*f+t*c*f)*w,this}scale(e){let t=this.elements,i=e.x,r=e.y,s=e.z;return t[0]*=i,t[4]*=r,t[8]*=s,t[1]*=i,t[5]*=r,t[9]*=s,t[2]*=i,t[6]*=r,t[10]*=s,t[3]*=i,t[7]*=r,t[11]*=s,this}getMaxScaleOnAxis(){let e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],i=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],r=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,i,r))}makeTranslation(e,t,i){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,i,0,0,0,1),this}makeRotationX(e){let t=Math.cos(e),i=Math.sin(e);return this.set(1,0,0,0,0,t,-i,0,0,i,t,0,0,0,0,1),this}makeRotationY(e){let t=Math.cos(e),i=Math.sin(e);return this.set(t,0,i,0,0,1,0,0,-i,0,t,0,0,0,0,1),this}makeRotationZ(e){let t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,0,i,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){let i=Math.cos(t),r=Math.sin(t),s=1-i,o=e.x,c=e.y,l=e.z,a=s*o,d=s*c;return this.set(a*o+i,a*c-r*l,a*l+r*c,0,a*c+r*l,d*c+i,d*l-r*o,0,a*l-r*c,d*l+r*o,s*l*l+i,0,0,0,0,1),this}makeScale(e,t,i){return this.set(e,0,0,0,0,t,0,0,0,0,i,0,0,0,0,1),this}makeShear(e,t,i,r,s,o){return this.set(1,i,s,0,e,1,o,0,t,r,1,0,0,0,0,1),this}compose(e,t,i){let r=this.elements,s=t._x,o=t._y,c=t._z,l=t._w,a=s+s,d=o+o,p=c+c,f=s*a,m=s*d,g=s*p,y=o*d,h=o*p,u=c*p,E=l*a,x=l*d,_=l*p,A=i.x,N=i.y,w=i.z;return r[0]=(1-(y+u))*A,r[1]=(m+_)*A,r[2]=(g-x)*A,r[3]=0,r[4]=(m-_)*N,r[5]=(1-(f+u))*N,r[6]=(h+E)*N,r[7]=0,r[8]=(g+x)*w,r[9]=(h-E)*w,r[10]=(1-(f+y))*w,r[11]=0,r[12]=e.x,r[13]=e.y,r[14]=e.z,r[15]=1,this}decompose(e,t,i){let r=this.elements,s=Ri.set(r[0],r[1],r[2]).length(),o=Ri.set(r[4],r[5],r[6]).length(),c=Ri.set(r[8],r[9],r[10]).length();this.determinant()<0&&(s=-s),e.x=r[12],e.y=r[13],e.z=r[14],an.copy(this);let a=1/s,d=1/o,p=1/c;return an.elements[0]*=a,an.elements[1]*=a,an.elements[2]*=a,an.elements[4]*=d,an.elements[5]*=d,an.elements[6]*=d,an.elements[8]*=p,an.elements[9]*=p,an.elements[10]*=p,t.setFromRotationMatrix(an),i.x=s,i.y=o,i.z=c,this}makePerspective(e,t,i,r,s,o,c=ln,l=!1){let a=this.elements,d=2*s/(t-e),p=2*s/(i-r),f=(t+e)/(t-e),m=(i+r)/(i-r),g,y;if(l)g=s/(o-s),y=o*s/(o-s);else if(c===ln)g=-(o+s)/(o-s),y=-2*o*s/(o-s);else if(c===yr)g=-o/(o-s),y=-o*s/(o-s);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+c);return a[0]=d,a[4]=0,a[8]=f,a[12]=0,a[1]=0,a[5]=p,a[9]=m,a[13]=0,a[2]=0,a[6]=0,a[10]=g,a[14]=y,a[3]=0,a[7]=0,a[11]=-1,a[15]=0,this}makeOrthographic(e,t,i,r,s,o,c=ln,l=!1){let a=this.elements,d=2/(t-e),p=2/(i-r),f=-(t+e)/(t-e),m=-(i+r)/(i-r),g,y;if(l)g=1/(o-s),y=o/(o-s);else if(c===ln)g=-2/(o-s),y=-(o+s)/(o-s);else if(c===yr)g=-1/(o-s),y=-s/(o-s);else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+c);return a[0]=d,a[4]=0,a[8]=0,a[12]=f,a[1]=0,a[5]=p,a[9]=0,a[13]=m,a[2]=0,a[6]=0,a[10]=g,a[14]=y,a[3]=0,a[7]=0,a[11]=0,a[15]=1,this}equals(e){let t=this.elements,i=e.elements;for(let r=0;r<16;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<16;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){let i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e[t+9]=i[9],e[t+10]=i[10],e[t+11]=i[11],e[t+12]=i[12],e[t+13]=i[13],e[t+14]=i[14],e[t+15]=i[15],e}},Ri=new Z,an=new yt,bh=new Z(0,0,0),Ah=new Z(1,1,1),zn=new Z,as=new Z,Wt=new Z,Gc=new yt,Hc=new zt,dn=class n{constructor(e=0,t=0,i=0,r=n.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=i,this._order=r}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,i,r=this._order){return this._x=e,this._y=t,this._z=i,this._order=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,i=!0){let r=e.elements,s=r[0],o=r[4],c=r[8],l=r[1],a=r[5],d=r[9],p=r[2],f=r[6],m=r[10];switch(t){case"XYZ":this._y=Math.asin(et(c,-1,1)),Math.abs(c)<.9999999?(this._x=Math.atan2(-d,m),this._z=Math.atan2(-o,s)):(this._x=Math.atan2(f,a),this._z=0);break;case"YXZ":this._x=Math.asin(-et(d,-1,1)),Math.abs(d)<.9999999?(this._y=Math.atan2(c,m),this._z=Math.atan2(l,a)):(this._y=Math.atan2(-p,s),this._z=0);break;case"ZXY":this._x=Math.asin(et(f,-1,1)),Math.abs(f)<.9999999?(this._y=Math.atan2(-p,m),this._z=Math.atan2(-o,a)):(this._y=0,this._z=Math.atan2(l,s));break;case"ZYX":this._y=Math.asin(-et(p,-1,1)),Math.abs(p)<.9999999?(this._x=Math.atan2(f,m),this._z=Math.atan2(l,s)):(this._x=0,this._z=Math.atan2(-o,a));break;case"YZX":this._z=Math.asin(et(l,-1,1)),Math.abs(l)<.9999999?(this._x=Math.atan2(-d,a),this._y=Math.atan2(-p,s)):(this._x=0,this._y=Math.atan2(c,m));break;case"XZY":this._z=Math.asin(-et(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(f,a),this._y=Math.atan2(c,s)):(this._x=Math.atan2(-d,m),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,i===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,i){return Gc.makeRotationFromQuaternion(e),this.setFromRotationMatrix(Gc,t,i)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return Hc.setFromEuler(this),this.setFromQuaternion(Hc,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}};dn.DEFAULT_ORDER="XYZ";var xr=class{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}},Rh=0,Wc=new Z,wi=new zt,Rn=new yt,cs=new Z,ur=new Z,wh=new Z,Ch=new zt,Xc=new Z(1,0,0),Yc=new Z(0,1,0),qc=new Z(0,0,1),Kc={type:"added"},Ih={type:"removed"},Ci={type:"childadded",child:null},fa={type:"childremoved",child:null},Et=class n extends _n{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:Rh++}),this.uuid=tr(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=n.DEFAULT_UP.clone();let e=new Z,t=new dn,i=new zt,r=new Z(1,1,1);function s(){i.setFromEuler(t,!1)}function o(){t.setFromQuaternion(i,void 0,!1)}t._onChange(s),i._onChange(o),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:i},scale:{configurable:!0,enumerable:!0,value:r},modelViewMatrix:{value:new yt},normalMatrix:{value:new Ze}}),this.matrix=new yt,this.matrixWorld=new yt,this.matrixAutoUpdate=n.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=n.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new xr,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.customDepthMaterial=void 0,this.customDistanceMaterial=void 0,this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return wi.setFromAxisAngle(e,t),this.quaternion.multiply(wi),this}rotateOnWorldAxis(e,t){return wi.setFromAxisAngle(e,t),this.quaternion.premultiply(wi),this}rotateX(e){return this.rotateOnAxis(Xc,e)}rotateY(e){return this.rotateOnAxis(Yc,e)}rotateZ(e){return this.rotateOnAxis(qc,e)}translateOnAxis(e,t){return Wc.copy(e).applyQuaternion(this.quaternion),this.position.add(Wc.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(Xc,e)}translateY(e){return this.translateOnAxis(Yc,e)}translateZ(e){return this.translateOnAxis(qc,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(Rn.copy(this.matrixWorld).invert())}lookAt(e,t,i){e.isVector3?cs.copy(e):cs.set(e,t,i);let r=this.parent;this.updateWorldMatrix(!0,!1),ur.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?Rn.lookAt(ur,cs,this.up):Rn.lookAt(cs,ur,this.up),this.quaternion.setFromRotationMatrix(Rn),r&&(Rn.extractRotation(r.matrixWorld),wi.setFromRotationMatrix(Rn),this.quaternion.premultiply(wi.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(Kc),Ci.child=e,this.dispatchEvent(Ci),Ci.child=null):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.remove(arguments[i]);return this}let t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(Ih),fa.child=e,this.dispatchEvent(fa),fa.child=null),this}removeFromParent(){let e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),Rn.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),Rn.multiply(e.parent.matrixWorld)),e.applyMatrix4(Rn),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(Kc),Ci.child=e,this.dispatchEvent(Ci),Ci.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let i=0,r=this.children.length;i<r;i++){let o=this.children[i].getObjectByProperty(e,t);if(o!==void 0)return o}}getObjectsByProperty(e,t,i=[]){this[e]===t&&i.push(this);let r=this.children;for(let s=0,o=r.length;s<o;s++)r[s].getObjectsByProperty(e,t,i);return i}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ur,e,wh),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ur,Ch,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);let t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}traverse(e){e(this);let t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);let t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverseVisible(e)}traverseAncestors(e){let t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);let t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].updateMatrixWorld(e)}updateWorldMatrix(e,t){let i=this.parent;if(e===!0&&i!==null&&i.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),t===!0){let r=this.children;for(let s=0,o=r.length;s<o;s++)r[s].updateWorldMatrix(!1,!0)}}toJSON(e){let t=e===void 0||typeof e=="string",i={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},i.metadata={version:4.7,type:"Object",generator:"Object3D.toJSON"});let r={};r.uuid=this.uuid,r.type=this.type,this.name!==""&&(r.name=this.name),this.castShadow===!0&&(r.castShadow=!0),this.receiveShadow===!0&&(r.receiveShadow=!0),this.visible===!1&&(r.visible=!1),this.frustumCulled===!1&&(r.frustumCulled=!1),this.renderOrder!==0&&(r.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(r.userData=this.userData),r.layers=this.layers.mask,r.matrix=this.matrix.toArray(),r.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(r.matrixAutoUpdate=!1),this.isInstancedMesh&&(r.type="InstancedMesh",r.count=this.count,r.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(r.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(r.type="BatchedMesh",r.perObjectFrustumCulled=this.perObjectFrustumCulled,r.sortObjects=this.sortObjects,r.drawRanges=this._drawRanges,r.reservedRanges=this._reservedRanges,r.geometryInfo=this._geometryInfo.map(c=>({...c,boundingBox:c.boundingBox?c.boundingBox.toJSON():void 0,boundingSphere:c.boundingSphere?c.boundingSphere.toJSON():void 0})),r.instanceInfo=this._instanceInfo.map(c=>({...c})),r.availableInstanceIds=this._availableInstanceIds.slice(),r.availableGeometryIds=this._availableGeometryIds.slice(),r.nextIndexStart=this._nextIndexStart,r.nextVertexStart=this._nextVertexStart,r.geometryCount=this._geometryCount,r.maxInstanceCount=this._maxInstanceCount,r.maxVertexCount=this._maxVertexCount,r.maxIndexCount=this._maxIndexCount,r.geometryInitialized=this._geometryInitialized,r.matricesTexture=this._matricesTexture.toJSON(e),r.indirectTexture=this._indirectTexture.toJSON(e),this._colorsTexture!==null&&(r.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(r.boundingSphere=this.boundingSphere.toJSON()),this.boundingBox!==null&&(r.boundingBox=this.boundingBox.toJSON()));function s(c,l){return c[l.uuid]===void 0&&(c[l.uuid]=l.toJSON(e)),l.uuid}if(this.isScene)this.background&&(this.background.isColor?r.background=this.background.toJSON():this.background.isTexture&&(r.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(r.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){r.geometry=s(e.geometries,this.geometry);let c=this.geometry.parameters;if(c!==void 0&&c.shapes!==void 0){let l=c.shapes;if(Array.isArray(l))for(let a=0,d=l.length;a<d;a++){let p=l[a];s(e.shapes,p)}else s(e.shapes,l)}}if(this.isSkinnedMesh&&(r.bindMode=this.bindMode,r.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(s(e.skeletons,this.skeleton),r.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){let c=[];for(let l=0,a=this.material.length;l<a;l++)c.push(s(e.materials,this.material[l]));r.material=c}else r.material=s(e.materials,this.material);if(this.children.length>0){r.children=[];for(let c=0;c<this.children.length;c++)r.children.push(this.children[c].toJSON(e).object)}if(this.animations.length>0){r.animations=[];for(let c=0;c<this.animations.length;c++){let l=this.animations[c];r.animations.push(s(e.animations,l))}}if(t){let c=o(e.geometries),l=o(e.materials),a=o(e.textures),d=o(e.images),p=o(e.shapes),f=o(e.skeletons),m=o(e.animations),g=o(e.nodes);c.length>0&&(i.geometries=c),l.length>0&&(i.materials=l),a.length>0&&(i.textures=a),d.length>0&&(i.images=d),p.length>0&&(i.shapes=p),f.length>0&&(i.skeletons=f),m.length>0&&(i.animations=m),g.length>0&&(i.nodes=g)}return i.object=r,i;function o(c){let l=[];for(let a in c){let d=c[a];delete d.metadata,l.push(d)}return l}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let i=0;i<e.children.length;i++){let r=e.children[i];this.add(r.clone())}return this}};Et.DEFAULT_UP=new Z(0,1,0);Et.DEFAULT_MATRIX_AUTO_UPDATE=!0;Et.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;var cn=new Z,wn=new Z,pa=new Z,Cn=new Z,Ii=new Z,Pi=new Z,Zc=new Z,ma=new Z,ga=new Z,_a=new Z,ya=new vt,va=new vt,xa=new vt,Hn=class n{constructor(e=new Z,t=new Z,i=new Z){this.a=e,this.b=t,this.c=i}static getNormal(e,t,i,r){r.subVectors(i,t),cn.subVectors(e,t),r.cross(cn);let s=r.lengthSq();return s>0?r.multiplyScalar(1/Math.sqrt(s)):r.set(0,0,0)}static getBarycoord(e,t,i,r,s){cn.subVectors(r,t),wn.subVectors(i,t),pa.subVectors(e,t);let o=cn.dot(cn),c=cn.dot(wn),l=cn.dot(pa),a=wn.dot(wn),d=wn.dot(pa),p=o*a-c*c;if(p===0)return s.set(0,0,0),null;let f=1/p,m=(a*l-c*d)*f,g=(o*d-c*l)*f;return s.set(1-m-g,g,m)}static containsPoint(e,t,i,r){return this.getBarycoord(e,t,i,r,Cn)===null?!1:Cn.x>=0&&Cn.y>=0&&Cn.x+Cn.y<=1}static getInterpolation(e,t,i,r,s,o,c,l){return this.getBarycoord(e,t,i,r,Cn)===null?(l.x=0,l.y=0,"z"in l&&(l.z=0),"w"in l&&(l.w=0),null):(l.setScalar(0),l.addScaledVector(s,Cn.x),l.addScaledVector(o,Cn.y),l.addScaledVector(c,Cn.z),l)}static getInterpolatedAttribute(e,t,i,r,s,o){return ya.setScalar(0),va.setScalar(0),xa.setScalar(0),ya.fromBufferAttribute(e,t),va.fromBufferAttribute(e,i),xa.fromBufferAttribute(e,r),o.setScalar(0),o.addScaledVector(ya,s.x),o.addScaledVector(va,s.y),o.addScaledVector(xa,s.z),o}static isFrontFacing(e,t,i,r){return cn.subVectors(i,t),wn.subVectors(e,t),cn.cross(wn).dot(r)<0}set(e,t,i){return this.a.copy(e),this.b.copy(t),this.c.copy(i),this}setFromPointsAndIndices(e,t,i,r){return this.a.copy(e[t]),this.b.copy(e[i]),this.c.copy(e[r]),this}setFromAttributeAndIndices(e,t,i,r){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,i),this.c.fromBufferAttribute(e,r),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return cn.subVectors(this.c,this.b),wn.subVectors(this.a,this.b),cn.cross(wn).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return n.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return n.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,i,r,s){return n.getInterpolation(e,this.a,this.b,this.c,t,i,r,s)}containsPoint(e){return n.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return n.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){let i=this.a,r=this.b,s=this.c,o,c;Ii.subVectors(r,i),Pi.subVectors(s,i),ma.subVectors(e,i);let l=Ii.dot(ma),a=Pi.dot(ma);if(l<=0&&a<=0)return t.copy(i);ga.subVectors(e,r);let d=Ii.dot(ga),p=Pi.dot(ga);if(d>=0&&p<=d)return t.copy(r);let f=l*p-d*a;if(f<=0&&l>=0&&d<=0)return o=l/(l-d),t.copy(i).addScaledVector(Ii,o);_a.subVectors(e,s);let m=Ii.dot(_a),g=Pi.dot(_a);if(g>=0&&m<=g)return t.copy(s);let y=m*a-l*g;if(y<=0&&a>=0&&g<=0)return c=a/(a-g),t.copy(i).addScaledVector(Pi,c);let h=d*g-m*p;if(h<=0&&p-d>=0&&m-g>=0)return Zc.subVectors(s,r),c=(p-d)/(p-d+(m-g)),t.copy(r).addScaledVector(Zc,c);let u=1/(h+y+f);return o=y*u,c=f*u,t.copy(i).addScaledVector(Ii,o).addScaledVector(Pi,c)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}},tu={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},Vn={h:0,s:0,l:0},ls={h:0,s:0,l:0};function Ea(n,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?n+(e-n)*6*t:t<1/2?e:t<2/3?n+(e-n)*6*(2/3-t):n}var qe=class{constructor(e,t,i){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,i)}set(e,t,i){if(t===void 0&&i===void 0){let r=e;r&&r.isColor?this.copy(r):typeof r=="number"?this.setHex(r):typeof r=="string"&&this.setStyle(r)}else this.setRGB(e,t,i);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=pt){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,nt.colorSpaceToWorking(this,t),this}setRGB(e,t,i,r=nt.workingColorSpace){return this.r=e,this.g=t,this.b=i,nt.colorSpaceToWorking(this,r),this}setHSL(e,t,i,r=nt.workingColorSpace){if(e=ic(e,1),t=et(t,0,1),i=et(i,0,1),t===0)this.r=this.g=this.b=i;else{let s=i<=.5?i*(1+t):i+t-i*t,o=2*i-s;this.r=Ea(o,s,e+1/3),this.g=Ea(o,s,e),this.b=Ea(o,s,e-1/3)}return nt.colorSpaceToWorking(this,r),this}setStyle(e,t=pt){function i(s){s!==void 0&&parseFloat(s)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let r;if(r=/^(\w+)\(([^\)]*)\)/.exec(e)){let s,o=r[1],c=r[2];switch(o){case"rgb":case"rgba":if(s=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(c))return i(s[4]),this.setRGB(Math.min(255,parseInt(s[1],10))/255,Math.min(255,parseInt(s[2],10))/255,Math.min(255,parseInt(s[3],10))/255,t);if(s=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(c))return i(s[4]),this.setRGB(Math.min(100,parseInt(s[1],10))/100,Math.min(100,parseInt(s[2],10))/100,Math.min(100,parseInt(s[3],10))/100,t);break;case"hsl":case"hsla":if(s=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(c))return i(s[4]),this.setHSL(parseFloat(s[1])/360,parseFloat(s[2])/100,parseFloat(s[3])/100,t);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(r=/^\#([A-Fa-f\d]+)$/.exec(e)){let s=r[1],o=s.length;if(o===3)return this.setRGB(parseInt(s.charAt(0),16)/15,parseInt(s.charAt(1),16)/15,parseInt(s.charAt(2),16)/15,t);if(o===6)return this.setHex(parseInt(s,16),t);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=pt){let i=tu[e.toLowerCase()];return i!==void 0?this.setHex(i,t):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=Pn(e.r),this.g=Pn(e.g),this.b=Pn(e.b),this}copyLinearToSRGB(e){return this.r=Fi(e.r),this.g=Fi(e.g),this.b=Fi(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=pt){return nt.workingToColorSpace(It.copy(this),e),Math.round(et(It.r*255,0,255))*65536+Math.round(et(It.g*255,0,255))*256+Math.round(et(It.b*255,0,255))}getHexString(e=pt){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=nt.workingColorSpace){nt.workingToColorSpace(It.copy(this),t);let i=It.r,r=It.g,s=It.b,o=Math.max(i,r,s),c=Math.min(i,r,s),l,a,d=(c+o)/2;if(c===o)l=0,a=0;else{let p=o-c;switch(a=d<=.5?p/(o+c):p/(2-o-c),o){case i:l=(r-s)/p+(r<s?6:0);break;case r:l=(s-i)/p+2;break;case s:l=(i-r)/p+4;break}l/=6}return e.h=l,e.s=a,e.l=d,e}getRGB(e,t=nt.workingColorSpace){return nt.workingToColorSpace(It.copy(this),t),e.r=It.r,e.g=It.g,e.b=It.b,e}getStyle(e=pt){nt.workingToColorSpace(It.copy(this),e);let t=It.r,i=It.g,r=It.b;return e!==pt?`color(${e} ${t.toFixed(3)} ${i.toFixed(3)} ${r.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(i*255)},${Math.round(r*255)})`}offsetHSL(e,t,i){return this.getHSL(Vn),this.setHSL(Vn.h+e,Vn.s+t,Vn.l+i)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,i){return this.r=e.r+(t.r-e.r)*i,this.g=e.g+(t.g-e.g)*i,this.b=e.b+(t.b-e.b)*i,this}lerpHSL(e,t){this.getHSL(Vn),e.getHSL(ls);let i=mr(Vn.h,ls.h,t),r=mr(Vn.s,ls.s,t),s=mr(Vn.l,ls.l,t);return this.setHSL(i,r,s),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){let t=this.r,i=this.g,r=this.b,s=e.elements;return this.r=s[0]*t+s[3]*i+s[6]*r,this.g=s[1]*t+s[4]*i+s[7]*r,this.b=s[2]*t+s[5]*i+s[8]*r,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}},It=new qe;qe.NAMES=tu;var Ph=0,xn=class extends _n{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:Ph++}),this.uuid=tr(),this.name="",this.type="Material",this.blending=oi,this.side=un,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=Rs,this.blendDst=ws,this.blendEquation=Wn,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new qe(0,0,0),this.blendAlpha=0,this.depthFunc=ai,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=Ia,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=si,this.stencilZFail=si,this.stencilZPass=si,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.allowOverride=!0,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(let t in e){let i=e[t];if(i===void 0){console.warn(`THREE.Material: parameter '${t}' has value of undefined.`);continue}let r=this[t];if(r===void 0){console.warn(`THREE.Material: '${t}' is not a property of THREE.${this.type}.`);continue}r&&r.isColor?r.set(i):r&&r.isVector3&&i&&i.isVector3?r.copy(i):this[t]=i}}toJSON(e){let t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});let i={metadata:{version:4.7,type:"Material",generator:"Material.toJSON"}};i.uuid=this.uuid,i.type=this.type,this.name!==""&&(i.name=this.name),this.color&&this.color.isColor&&(i.color=this.color.getHex()),this.roughness!==void 0&&(i.roughness=this.roughness),this.metalness!==void 0&&(i.metalness=this.metalness),this.sheen!==void 0&&(i.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(i.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(i.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(i.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(i.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(i.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(i.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(i.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(i.shininess=this.shininess),this.clearcoat!==void 0&&(i.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(i.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(i.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(i.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(i.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,i.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.dispersion!==void 0&&(i.dispersion=this.dispersion),this.iridescence!==void 0&&(i.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(i.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(i.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(i.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(i.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(i.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(i.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(i.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(i.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(i.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(i.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(i.lightMap=this.lightMap.toJSON(e).uuid,i.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(i.aoMap=this.aoMap.toJSON(e).uuid,i.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(i.bumpMap=this.bumpMap.toJSON(e).uuid,i.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(i.normalMap=this.normalMap.toJSON(e).uuid,i.normalMapType=this.normalMapType,i.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(i.displacementMap=this.displacementMap.toJSON(e).uuid,i.displacementScale=this.displacementScale,i.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(i.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(i.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(i.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(i.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(i.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(i.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(i.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(i.combine=this.combine)),this.envMapRotation!==void 0&&(i.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(i.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(i.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(i.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(i.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(i.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(i.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(i.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(i.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(i.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(i.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(i.size=this.size),this.shadowSide!==null&&(i.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(i.sizeAttenuation=this.sizeAttenuation),this.blending!==oi&&(i.blending=this.blending),this.side!==un&&(i.side=this.side),this.vertexColors===!0&&(i.vertexColors=!0),this.opacity<1&&(i.opacity=this.opacity),this.transparent===!0&&(i.transparent=!0),this.blendSrc!==Rs&&(i.blendSrc=this.blendSrc),this.blendDst!==ws&&(i.blendDst=this.blendDst),this.blendEquation!==Wn&&(i.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(i.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(i.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(i.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(i.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(i.blendAlpha=this.blendAlpha),this.depthFunc!==ai&&(i.depthFunc=this.depthFunc),this.depthTest===!1&&(i.depthTest=this.depthTest),this.depthWrite===!1&&(i.depthWrite=this.depthWrite),this.colorWrite===!1&&(i.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(i.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==Ia&&(i.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(i.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(i.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==si&&(i.stencilFail=this.stencilFail),this.stencilZFail!==si&&(i.stencilZFail=this.stencilZFail),this.stencilZPass!==si&&(i.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(i.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(i.rotation=this.rotation),this.polygonOffset===!0&&(i.polygonOffset=!0),this.polygonOffsetFactor!==0&&(i.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(i.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(i.linewidth=this.linewidth),this.dashSize!==void 0&&(i.dashSize=this.dashSize),this.gapSize!==void 0&&(i.gapSize=this.gapSize),this.scale!==void 0&&(i.scale=this.scale),this.dithering===!0&&(i.dithering=!0),this.alphaTest>0&&(i.alphaTest=this.alphaTest),this.alphaHash===!0&&(i.alphaHash=!0),this.alphaToCoverage===!0&&(i.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(i.premultipliedAlpha=!0),this.forceSinglePass===!0&&(i.forceSinglePass=!0),this.wireframe===!0&&(i.wireframe=!0),this.wireframeLinewidth>1&&(i.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(i.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(i.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(i.flatShading=!0),this.visible===!1&&(i.visible=!1),this.toneMapped===!1&&(i.toneMapped=!1),this.fog===!1&&(i.fog=!1),Object.keys(this.userData).length>0&&(i.userData=this.userData);function r(s){let o=[];for(let c in s){let l=s[c];delete l.metadata,o.push(l)}return o}if(t){let s=r(e.textures),o=r(e.images);s.length>0&&(i.textures=s),o.length>0&&(i.images=o)}return i}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;let t=e.clippingPlanes,i=null;if(t!==null){let r=t.length;i=new Array(r);for(let s=0;s!==r;++s)i[s]=t[s].clone()}return this.clippingPlanes=i,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}},En=class extends xn{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new qe(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new dn,this.combine=ro,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}};var St=new Z,us=new ze,Lh=0,Ut=class{constructor(e,t,i=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:Lh++}),this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=i,this.usage=Pa,this.updateRanges=[],this.gpuType=Tn,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,i){e*=this.itemSize,i*=t.itemSize;for(let r=0,s=this.itemSize;r<s;r++)this.array[e+r]=t.array[i+r];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,i=this.count;t<i;t++)us.fromBufferAttribute(this,t),us.applyMatrix3(e),this.setXY(t,us.x,us.y);else if(this.itemSize===3)for(let t=0,i=this.count;t<i;t++)St.fromBufferAttribute(this,t),St.applyMatrix3(e),this.setXYZ(t,St.x,St.y,St.z);return this}applyMatrix4(e){for(let t=0,i=this.count;t<i;t++)St.fromBufferAttribute(this,t),St.applyMatrix4(e),this.setXYZ(t,St.x,St.y,St.z);return this}applyNormalMatrix(e){for(let t=0,i=this.count;t<i;t++)St.fromBufferAttribute(this,t),St.applyNormalMatrix(e),this.setXYZ(t,St.x,St.y,St.z);return this}transformDirection(e){for(let t=0,i=this.count;t<i;t++)St.fromBufferAttribute(this,t),St.transformDirection(e),this.setXYZ(t,St.x,St.y,St.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let i=this.array[e*this.itemSize+t];return this.normalized&&(i=Ui(i,this.array)),i}setComponent(e,t,i){return this.normalized&&(i=Dt(i,this.array)),this.array[e*this.itemSize+t]=i,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=Ui(t,this.array)),t}setX(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=Ui(t,this.array)),t}setY(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=Ui(t,this.array)),t}setZ(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=Ui(t,this.array)),t}setW(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,i){return e*=this.itemSize,this.normalized&&(t=Dt(t,this.array),i=Dt(i,this.array)),this.array[e+0]=t,this.array[e+1]=i,this}setXYZ(e,t,i,r){return e*=this.itemSize,this.normalized&&(t=Dt(t,this.array),i=Dt(i,this.array),r=Dt(r,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this}setXYZW(e,t,i,r,s){return e*=this.itemSize,this.normalized&&(t=Dt(t,this.array),i=Dt(i,this.array),r=Dt(r,this.array),s=Dt(s,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this.array[e+3]=s,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){let e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==Pa&&(e.usage=this.usage),e}};var Er=class extends Ut{constructor(e,t,i){super(new Uint16Array(e),t,i)}};var Sr=class extends Ut{constructor(e,t,i){super(new Uint32Array(e),t,i)}};var Qe=class extends Ut{constructor(e,t,i){super(new Float32Array(e),t,i)}},Nh=0,$t=new yt,Sa=new Et,Li=new Z,Xt=new vn,hr=new vn,Rt=new Z,Tt=class n extends _n{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:Nh++}),this.uuid=tr(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(sc(e)?Sr:Er)(e,1):this.index=e,this}setIndirect(e){return this.indirect=e,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,i=0){this.groups.push({start:e,count:t,materialIndex:i})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){let t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);let i=this.attributes.normal;if(i!==void 0){let s=new Ze().getNormalMatrix(e);i.applyNormalMatrix(s),i.needsUpdate=!0}let r=this.attributes.tangent;return r!==void 0&&(r.transformDirection(e),r.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return $t.makeRotationFromQuaternion(e),this.applyMatrix4($t),this}rotateX(e){return $t.makeRotationX(e),this.applyMatrix4($t),this}rotateY(e){return $t.makeRotationY(e),this.applyMatrix4($t),this}rotateZ(e){return $t.makeRotationZ(e),this.applyMatrix4($t),this}translate(e,t,i){return $t.makeTranslation(e,t,i),this.applyMatrix4($t),this}scale(e,t,i){return $t.makeScale(e,t,i),this.applyMatrix4($t),this}lookAt(e){return Sa.lookAt(e),Sa.updateMatrix(),this.applyMatrix4(Sa.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(Li).negate(),this.translate(Li.x,Li.y,Li.z),this}setFromPoints(e){let t=this.getAttribute("position");if(t===void 0){let i=[];for(let r=0,s=e.length;r<s;r++){let o=e[r];i.push(o.x,o.y,o.z||0)}this.setAttribute("position",new Qe(i,3))}else{let i=Math.min(e.length,t.count);for(let r=0;r<i;r++){let s=e[r];t.setXYZ(r,s.x,s.y,s.z||0)}e.length>t.count&&console.warn("THREE.BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new vn);let e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new Z(-1/0,-1/0,-1/0),new Z(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let i=0,r=t.length;i<r;i++){let s=t[i];Xt.setFromBufferAttribute(s),this.morphTargetsRelative?(Rt.addVectors(this.boundingBox.min,Xt.min),this.boundingBox.expandByPoint(Rt),Rt.addVectors(this.boundingBox.max,Xt.max),this.boundingBox.expandByPoint(Rt)):(this.boundingBox.expandByPoint(Xt.min),this.boundingBox.expandByPoint(Xt.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Xn);let e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new Z,1/0);return}if(e){let i=this.boundingSphere.center;if(Xt.setFromBufferAttribute(e),t)for(let s=0,o=t.length;s<o;s++){let c=t[s];hr.setFromBufferAttribute(c),this.morphTargetsRelative?(Rt.addVectors(Xt.min,hr.min),Xt.expandByPoint(Rt),Rt.addVectors(Xt.max,hr.max),Xt.expandByPoint(Rt)):(Xt.expandByPoint(hr.min),Xt.expandByPoint(hr.max))}Xt.getCenter(i);let r=0;for(let s=0,o=e.count;s<o;s++)Rt.fromBufferAttribute(e,s),r=Math.max(r,i.distanceToSquared(Rt));if(t)for(let s=0,o=t.length;s<o;s++){let c=t[s],l=this.morphTargetsRelative;for(let a=0,d=c.count;a<d;a++)Rt.fromBufferAttribute(c,a),l&&(Li.fromBufferAttribute(e,a),Rt.add(Li)),r=Math.max(r,i.distanceToSquared(Rt))}this.boundingSphere.radius=Math.sqrt(r),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){let e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}let i=t.position,r=t.normal,s=t.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new Ut(new Float32Array(4*i.count),4));let o=this.getAttribute("tangent"),c=[],l=[];for(let O=0;O<i.count;O++)c[O]=new Z,l[O]=new Z;let a=new Z,d=new Z,p=new Z,f=new ze,m=new ze,g=new ze,y=new Z,h=new Z;function u(O,T,M){a.fromBufferAttribute(i,O),d.fromBufferAttribute(i,T),p.fromBufferAttribute(i,M),f.fromBufferAttribute(s,O),m.fromBufferAttribute(s,T),g.fromBufferAttribute(s,M),d.sub(a),p.sub(a),m.sub(f),g.sub(f);let R=1/(m.x*g.y-g.x*m.y);isFinite(R)&&(y.copy(d).multiplyScalar(g.y).addScaledVector(p,-m.y).multiplyScalar(R),h.copy(p).multiplyScalar(m.x).addScaledVector(d,-g.x).multiplyScalar(R),c[O].add(y),c[T].add(y),c[M].add(y),l[O].add(h),l[T].add(h),l[M].add(h))}let E=this.groups;E.length===0&&(E=[{start:0,count:e.count}]);for(let O=0,T=E.length;O<T;++O){let M=E[O],R=M.start,I=M.count;for(let U=R,P=R+I;U<P;U+=3)u(e.getX(U+0),e.getX(U+1),e.getX(U+2))}let x=new Z,_=new Z,A=new Z,N=new Z;function w(O){A.fromBufferAttribute(r,O),N.copy(A);let T=c[O];x.copy(T),x.sub(A.multiplyScalar(A.dot(T))).normalize(),_.crossVectors(N,T);let R=_.dot(l[O])<0?-1:1;o.setXYZW(O,x.x,x.y,x.z,R)}for(let O=0,T=E.length;O<T;++O){let M=E[O],R=M.start,I=M.count;for(let U=R,P=R+I;U<P;U+=3)w(e.getX(U+0)),w(e.getX(U+1)),w(e.getX(U+2))}}computeVertexNormals(){let e=this.index,t=this.getAttribute("position");if(t!==void 0){let i=this.getAttribute("normal");if(i===void 0)i=new Ut(new Float32Array(t.count*3),3),this.setAttribute("normal",i);else for(let f=0,m=i.count;f<m;f++)i.setXYZ(f,0,0,0);let r=new Z,s=new Z,o=new Z,c=new Z,l=new Z,a=new Z,d=new Z,p=new Z;if(e)for(let f=0,m=e.count;f<m;f+=3){let g=e.getX(f+0),y=e.getX(f+1),h=e.getX(f+2);r.fromBufferAttribute(t,g),s.fromBufferAttribute(t,y),o.fromBufferAttribute(t,h),d.subVectors(o,s),p.subVectors(r,s),d.cross(p),c.fromBufferAttribute(i,g),l.fromBufferAttribute(i,y),a.fromBufferAttribute(i,h),c.add(d),l.add(d),a.add(d),i.setXYZ(g,c.x,c.y,c.z),i.setXYZ(y,l.x,l.y,l.z),i.setXYZ(h,a.x,a.y,a.z)}else for(let f=0,m=t.count;f<m;f+=3)r.fromBufferAttribute(t,f+0),s.fromBufferAttribute(t,f+1),o.fromBufferAttribute(t,f+2),d.subVectors(o,s),p.subVectors(r,s),d.cross(p),i.setXYZ(f+0,d.x,d.y,d.z),i.setXYZ(f+1,d.x,d.y,d.z),i.setXYZ(f+2,d.x,d.y,d.z);this.normalizeNormals(),i.needsUpdate=!0}}normalizeNormals(){let e=this.attributes.normal;for(let t=0,i=e.count;t<i;t++)Rt.fromBufferAttribute(e,t),Rt.normalize(),e.setXYZ(t,Rt.x,Rt.y,Rt.z)}toNonIndexed(){function e(c,l){let a=c.array,d=c.itemSize,p=c.normalized,f=new a.constructor(l.length*d),m=0,g=0;for(let y=0,h=l.length;y<h;y++){c.isInterleavedBufferAttribute?m=l[y]*c.data.stride+c.offset:m=l[y]*d;for(let u=0;u<d;u++)f[g++]=a[m++]}return new Ut(f,d,p)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;let t=new n,i=this.index.array,r=this.attributes;for(let c in r){let l=r[c],a=e(l,i);t.setAttribute(c,a)}let s=this.morphAttributes;for(let c in s){let l=[],a=s[c];for(let d=0,p=a.length;d<p;d++){let f=a[d],m=e(f,i);l.push(m)}t.morphAttributes[c]=l}t.morphTargetsRelative=this.morphTargetsRelative;let o=this.groups;for(let c=0,l=o.length;c<l;c++){let a=o[c];t.addGroup(a.start,a.count,a.materialIndex)}return t}toJSON(){let e={metadata:{version:4.7,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){let l=this.parameters;for(let a in l)l[a]!==void 0&&(e[a]=l[a]);return e}e.data={attributes:{}};let t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});let i=this.attributes;for(let l in i){let a=i[l];e.data.attributes[l]=a.toJSON(e.data)}let r={},s=!1;for(let l in this.morphAttributes){let a=this.morphAttributes[l],d=[];for(let p=0,f=a.length;p<f;p++){let m=a[p];d.push(m.toJSON(e.data))}d.length>0&&(r[l]=d,s=!0)}s&&(e.data.morphAttributes=r,e.data.morphTargetsRelative=this.morphTargetsRelative);let o=this.groups;o.length>0&&(e.data.groups=JSON.parse(JSON.stringify(o)));let c=this.boundingSphere;return c!==null&&(e.data.boundingSphere=c.toJSON()),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;let t={};this.name=e.name;let i=e.index;i!==null&&this.setIndex(i.clone());let r=e.attributes;for(let a in r){let d=r[a];this.setAttribute(a,d.clone(t))}let s=e.morphAttributes;for(let a in s){let d=[],p=s[a];for(let f=0,m=p.length;f<m;f++)d.push(p[f].clone(t));this.morphAttributes[a]=d}this.morphTargetsRelative=e.morphTargetsRelative;let o=e.groups;for(let a=0,d=o.length;a<d;a++){let p=o[a];this.addGroup(p.start,p.count,p.materialIndex)}let c=e.boundingBox;c!==null&&(this.boundingBox=c.clone());let l=e.boundingSphere;return l!==null&&(this.boundingSphere=l.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}},jc=new yt,ii=new Yn,hs=new Xn,Jc=new Z,ds=new Z,fs=new Z,ps=new Z,Ta=new Z,ms=new Z,$c=new Z,gs=new Z,Lt=class extends Et{constructor(e=new Tt,t=new En){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.count=1,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){let t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){let r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let s=0,o=r.length;s<o;s++){let c=r[s].name||String(s);this.morphTargetInfluences.push(0),this.morphTargetDictionary[c]=s}}}}getVertexPosition(e,t){let i=this.geometry,r=i.attributes.position,s=i.morphAttributes.position,o=i.morphTargetsRelative;t.fromBufferAttribute(r,e);let c=this.morphTargetInfluences;if(s&&c){ms.set(0,0,0);for(let l=0,a=s.length;l<a;l++){let d=c[l],p=s[l];d!==0&&(Ta.fromBufferAttribute(p,e),o?ms.addScaledVector(Ta,d):ms.addScaledVector(Ta.sub(t),d))}t.add(ms)}return t}raycast(e,t){let i=this.geometry,r=this.material,s=this.matrixWorld;r!==void 0&&(i.boundingSphere===null&&i.computeBoundingSphere(),hs.copy(i.boundingSphere),hs.applyMatrix4(s),ii.copy(e.ray).recast(e.near),!(hs.containsPoint(ii.origin)===!1&&(ii.intersectSphere(hs,Jc)===null||ii.origin.distanceToSquared(Jc)>(e.far-e.near)**2))&&(jc.copy(s).invert(),ii.copy(e.ray).applyMatrix4(jc),!(i.boundingBox!==null&&ii.intersectsBox(i.boundingBox)===!1)&&this._computeIntersections(e,t,ii)))}_computeIntersections(e,t,i){let r,s=this.geometry,o=this.material,c=s.index,l=s.attributes.position,a=s.attributes.uv,d=s.attributes.uv1,p=s.attributes.normal,f=s.groups,m=s.drawRange;if(c!==null)if(Array.isArray(o))for(let g=0,y=f.length;g<y;g++){let h=f[g],u=o[h.materialIndex],E=Math.max(h.start,m.start),x=Math.min(c.count,Math.min(h.start+h.count,m.start+m.count));for(let _=E,A=x;_<A;_+=3){let N=c.getX(_),w=c.getX(_+1),O=c.getX(_+2);r=_s(this,u,e,i,a,d,p,N,w,O),r&&(r.faceIndex=Math.floor(_/3),r.face.materialIndex=h.materialIndex,t.push(r))}}else{let g=Math.max(0,m.start),y=Math.min(c.count,m.start+m.count);for(let h=g,u=y;h<u;h+=3){let E=c.getX(h),x=c.getX(h+1),_=c.getX(h+2);r=_s(this,o,e,i,a,d,p,E,x,_),r&&(r.faceIndex=Math.floor(h/3),t.push(r))}}else if(l!==void 0)if(Array.isArray(o))for(let g=0,y=f.length;g<y;g++){let h=f[g],u=o[h.materialIndex],E=Math.max(h.start,m.start),x=Math.min(l.count,Math.min(h.start+h.count,m.start+m.count));for(let _=E,A=x;_<A;_+=3){let N=_,w=_+1,O=_+2;r=_s(this,u,e,i,a,d,p,N,w,O),r&&(r.faceIndex=Math.floor(_/3),r.face.materialIndex=h.materialIndex,t.push(r))}}else{let g=Math.max(0,m.start),y=Math.min(l.count,m.start+m.count);for(let h=g,u=y;h<u;h+=3){let E=h,x=h+1,_=h+2;r=_s(this,o,e,i,a,d,p,E,x,_),r&&(r.faceIndex=Math.floor(h/3),t.push(r))}}}};function Oh(n,e,t,i,r,s,o,c){let l;if(e.side===wt?l=i.intersectTriangle(o,s,r,!0,c):l=i.intersectTriangle(r,s,o,e.side===un,c),l===null)return null;gs.copy(c),gs.applyMatrix4(n.matrixWorld);let a=t.ray.origin.distanceTo(gs);return a<t.near||a>t.far?null:{distance:a,point:gs.clone(),object:n}}function _s(n,e,t,i,r,s,o,c,l,a){n.getVertexPosition(c,ds),n.getVertexPosition(l,fs),n.getVertexPosition(a,ps);let d=Oh(n,e,t,i,ds,fs,ps,$c);if(d){let p=new Z;Hn.getBarycoord($c,ds,fs,ps,p),r&&(d.uv=Hn.getInterpolatedAttribute(r,c,l,a,p,new ze)),s&&(d.uv1=Hn.getInterpolatedAttribute(s,c,l,a,p,new ze)),o&&(d.normal=Hn.getInterpolatedAttribute(o,c,l,a,p,new Z),d.normal.dot(i.direction)>0&&d.normal.multiplyScalar(-1));let f={a:c,b:l,c:a,normal:new Z,materialIndex:0};Hn.getNormal(ds,fs,ps,f.normal),d.face=f,d.barycoord=p}return d}var qn=class n extends Tt{constructor(e=1,t=1,i=1,r=1,s=1,o=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:i,widthSegments:r,heightSegments:s,depthSegments:o};let c=this;r=Math.floor(r),s=Math.floor(s),o=Math.floor(o);let l=[],a=[],d=[],p=[],f=0,m=0;g("z","y","x",-1,-1,i,t,e,o,s,0),g("z","y","x",1,-1,i,t,-e,o,s,1),g("x","z","y",1,1,e,i,t,r,o,2),g("x","z","y",1,-1,e,i,-t,r,o,3),g("x","y","z",1,-1,e,t,i,r,s,4),g("x","y","z",-1,-1,e,t,-i,r,s,5),this.setIndex(l),this.setAttribute("position",new Qe(a,3)),this.setAttribute("normal",new Qe(d,3)),this.setAttribute("uv",new Qe(p,2));function g(y,h,u,E,x,_,A,N,w,O,T){let M=_/w,R=A/O,I=_/2,U=A/2,P=N/2,X=w+1,W=O+1,q=0,G=0,ee=new Z;for(let ae=0;ae<W;ae++){let ue=ae*R-U;for(let _e=0;_e<X;_e++){let me=_e*M-I;ee[y]=me*E,ee[h]=ue*x,ee[u]=P,a.push(ee.x,ee.y,ee.z),ee[y]=0,ee[h]=0,ee[u]=N>0?1:-1,d.push(ee.x,ee.y,ee.z),p.push(_e/w),p.push(1-ae/O),q+=1}}for(let ae=0;ae<O;ae++)for(let ue=0;ue<w;ue++){let _e=f+ue+X*ae,me=f+ue+X*(ae+1),Me=f+(ue+1)+X*(ae+1),k=f+(ue+1)+X*ae;l.push(_e,me,k),l.push(me,Me,k),G+=6}c.addGroup(m,G,T),m+=G,f+=q}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}};function gi(n){let e={};for(let t in n){e[t]={};for(let i in n[t]){let r=n[t][i];r&&(r.isColor||r.isMatrix3||r.isMatrix4||r.isVector2||r.isVector3||r.isVector4||r.isTexture||r.isQuaternion)?r.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][i]=null):e[t][i]=r.clone():Array.isArray(r)?e[t][i]=r.slice():e[t][i]=r}}return e}function Nt(n){let e={};for(let t=0;t<n.length;t++){let i=gi(n[t]);for(let r in i)e[r]=i[r]}return e}function Dh(n){let e=[];for(let t=0;t<n.length;t++)e.push(n[t].clone());return e}function oc(n){let e=n.getRenderTarget();return e===null?n.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:nt.workingColorSpace}var nu={clone:gi,merge:Nt},Uh=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,Fh=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`,fn=class extends xn{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=Uh,this.fragmentShader=Fh,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=gi(e.uniforms),this.uniformsGroups=Dh(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){let t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(let r in this.uniforms){let o=this.uniforms[r].value;o&&o.isTexture?t.uniforms[r]={type:"t",value:o.toJSON(e).uuid}:o&&o.isColor?t.uniforms[r]={type:"c",value:o.getHex()}:o&&o.isVector2?t.uniforms[r]={type:"v2",value:o.toArray()}:o&&o.isVector3?t.uniforms[r]={type:"v3",value:o.toArray()}:o&&o.isVector4?t.uniforms[r]={type:"v4",value:o.toArray()}:o&&o.isMatrix3?t.uniforms[r]={type:"m3",value:o.toArray()}:o&&o.isMatrix4?t.uniforms[r]={type:"m4",value:o.toArray()}:t.uniforms[r]={value:o}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;let i={};for(let r in this.extensions)this.extensions[r]===!0&&(i[r]=!0);return Object.keys(i).length>0&&(t.extensions=i),t}},Tr=class extends Et{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new yt,this.projectionMatrix=new yt,this.projectionMatrixInverse=new yt,this.coordinateSystem=ln,this._reversedDepth=!1}get reversedDepth(){return this._reversedDepth}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,t){super.updateWorldMatrix(e,t),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}},Gn=new Z,Qc=new ze,el=new ze,Pt=class extends Tr{constructor(e=50,t=1,i=.1,r=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=i,this.far=r,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){let t=.5*this.getFilmHeight()/e;this.fov=zi*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){let e=Math.tan(pr*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return zi*2*Math.atan(Math.tan(pr*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,i){Gn.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(Gn.x,Gn.y).multiplyScalar(-e/Gn.z),Gn.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),i.set(Gn.x,Gn.y).multiplyScalar(-e/Gn.z)}getViewSize(e,t){return this.getViewBounds(e,Qc,el),t.subVectors(el,Qc)}setViewOffset(e,t,i,r,s,o){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=s,this.view.height=o,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let e=this.near,t=e*Math.tan(pr*.5*this.fov)/this.zoom,i=2*t,r=this.aspect*i,s=-.5*r,o=this.view;if(this.view!==null&&this.view.enabled){let l=o.fullWidth,a=o.fullHeight;s+=o.offsetX*r/l,t-=o.offsetY*i/a,r*=o.width/l,i*=o.height/a}let c=this.filmOffset;c!==0&&(s+=e*c/this.getFilmWidth()),this.projectionMatrix.makePerspective(s,s+r,t,t-i,e,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){let t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}},Ni=-90,Oi=1,Os=class extends Et{constructor(e,t,i){super(),this.type="CubeCamera",this.renderTarget=i,this.coordinateSystem=null,this.activeMipmapLevel=0;let r=new Pt(Ni,Oi,e,t);r.layers=this.layers,this.add(r);let s=new Pt(Ni,Oi,e,t);s.layers=this.layers,this.add(s);let o=new Pt(Ni,Oi,e,t);o.layers=this.layers,this.add(o);let c=new Pt(Ni,Oi,e,t);c.layers=this.layers,this.add(c);let l=new Pt(Ni,Oi,e,t);l.layers=this.layers,this.add(l);let a=new Pt(Ni,Oi,e,t);a.layers=this.layers,this.add(a)}updateCoordinateSystem(){let e=this.coordinateSystem,t=this.children.concat(),[i,r,s,o,c,l]=t;for(let a of t)this.remove(a);if(e===ln)i.up.set(0,1,0),i.lookAt(1,0,0),r.up.set(0,1,0),r.lookAt(-1,0,0),s.up.set(0,0,-1),s.lookAt(0,1,0),o.up.set(0,0,1),o.lookAt(0,-1,0),c.up.set(0,1,0),c.lookAt(0,0,1),l.up.set(0,1,0),l.lookAt(0,0,-1);else if(e===yr)i.up.set(0,-1,0),i.lookAt(-1,0,0),r.up.set(0,-1,0),r.lookAt(1,0,0),s.up.set(0,0,1),s.lookAt(0,1,0),o.up.set(0,0,-1),o.lookAt(0,-1,0),c.up.set(0,-1,0),c.lookAt(0,0,1),l.up.set(0,-1,0),l.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(let a of t)this.add(a),a.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();let{renderTarget:i,activeMipmapLevel:r}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());let[s,o,c,l,a,d]=this.children,p=e.getRenderTarget(),f=e.getActiveCubeFace(),m=e.getActiveMipmapLevel(),g=e.xr.enabled;e.xr.enabled=!1;let y=i.texture.generateMipmaps;i.texture.generateMipmaps=!1,e.setRenderTarget(i,0,r),e.render(t,s),e.setRenderTarget(i,1,r),e.render(t,o),e.setRenderTarget(i,2,r),e.render(t,c),e.setRenderTarget(i,3,r),e.render(t,l),e.setRenderTarget(i,4,r),e.render(t,a),i.texture.generateMipmaps=y,e.setRenderTarget(i,5,r),e.render(t,d),e.setRenderTarget(p,f,m),e.xr.enabled=g,i.texture.needsPMREMUpdate=!0}},Mr=class extends Ft{constructor(e=[],t=pi,i,r,s,o,c,l,a,d){super(e,t,i,r,s,o,c,l,a,d),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}},Ds=class extends yn{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;let i={width:e,height:e,depth:1},r=[i,i,i,i,i,i];this.texture=new Mr(r),this._setTextureOptions(t),this.texture.isRenderTargetTexture=!0}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;let i={uniforms:{tEquirect:{value:null}},vertexShader:`

				varying vec3 vWorldDirection;

				vec3 transformDirection( in vec3 dir, in mat4 matrix ) {

					return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );

				}

				void main() {

					vWorldDirection = transformDirection( position, modelMatrix );

					#include <begin_vertex>
					#include <project_vertex>

				}
			`,fragmentShader:`

				uniform sampler2D tEquirect;

				varying vec3 vWorldDirection;

				#include <common>

				void main() {

					vec3 direction = normalize( vWorldDirection );

					vec2 sampleUV = equirectUv( direction );

					gl_FragColor = texture2D( tEquirect, sampleUV );

				}
			`},r=new qn(5,5,5),s=new fn({name:"CubemapFromEquirect",uniforms:gi(i.uniforms),vertexShader:i.vertexShader,fragmentShader:i.fragmentShader,side:wt,blending:Nn});s.uniforms.tEquirect.value=t;let o=new Lt(r,s),c=t.minFilter;return t.minFilter===$n&&(t.minFilter=hn),new Os(1,10,this).update(e,o),t.minFilter=c,o.geometry.dispose(),o.material.dispose(),this}clear(e,t=!0,i=!0,r=!0){let s=e.getRenderTarget();for(let o=0;o<6;o++)e.setRenderTarget(this,o),e.clear(t,i,r);e.setRenderTarget(s)}},gn=class extends Et{constructor(){super(),this.isGroup=!0,this.type="Group"}},kh={type:"move"},Hi=class{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new gn,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new gn,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new Z,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new Z),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new gn,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new Z,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new Z),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){let t=this._hand;if(t)for(let i of e.hand.values())this._getHandJoint(t,i)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,i){let r=null,s=null,o=null,c=this._targetRay,l=this._grip,a=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(a&&e.hand){o=!0;for(let y of e.hand.values()){let h=t.getJointPose(y,i),u=this._getHandJoint(a,y);h!==null&&(u.matrix.fromArray(h.transform.matrix),u.matrix.decompose(u.position,u.rotation,u.scale),u.matrixWorldNeedsUpdate=!0,u.jointRadius=h.radius),u.visible=h!==null}let d=a.joints["index-finger-tip"],p=a.joints["thumb-tip"],f=d.position.distanceTo(p.position),m=.02,g=.005;a.inputState.pinching&&f>m+g?(a.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!a.inputState.pinching&&f<=m-g&&(a.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else l!==null&&e.gripSpace&&(s=t.getPose(e.gripSpace,i),s!==null&&(l.matrix.fromArray(s.transform.matrix),l.matrix.decompose(l.position,l.rotation,l.scale),l.matrixWorldNeedsUpdate=!0,s.linearVelocity?(l.hasLinearVelocity=!0,l.linearVelocity.copy(s.linearVelocity)):l.hasLinearVelocity=!1,s.angularVelocity?(l.hasAngularVelocity=!0,l.angularVelocity.copy(s.angularVelocity)):l.hasAngularVelocity=!1));c!==null&&(r=t.getPose(e.targetRaySpace,i),r===null&&s!==null&&(r=s),r!==null&&(c.matrix.fromArray(r.transform.matrix),c.matrix.decompose(c.position,c.rotation,c.scale),c.matrixWorldNeedsUpdate=!0,r.linearVelocity?(c.hasLinearVelocity=!0,c.linearVelocity.copy(r.linearVelocity)):c.hasLinearVelocity=!1,r.angularVelocity?(c.hasAngularVelocity=!0,c.angularVelocity.copy(r.angularVelocity)):c.hasAngularVelocity=!1,this.dispatchEvent(kh)))}return c!==null&&(c.visible=r!==null),l!==null&&(l.visible=s!==null),a!==null&&(a.visible=o!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){let i=new gn;i.matrixAutoUpdate=!1,i.visible=!1,e.joints[t.jointName]=i,e.add(i)}return e.joints[t.jointName]}};var ui=class extends Et{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new dn,this.environmentIntensity=1,this.environmentRotation=new dn,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){let t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(t.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(t.object.backgroundIntensity=this.backgroundIntensity),t.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(t.object.environmentIntensity=this.environmentIntensity),t.object.environmentRotation=this.environmentRotation.toArray(),t}};var br=class extends Ft{constructor(e=null,t=1,i=1,r,s,o,c,l,a=Bt,d=Bt,p,f){super(null,o,c,l,a,d,r,s,p,f),this.isDataTexture=!0,this.image={data:e,width:t,height:i},this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}};var Ma=new Z,Bh=new Z,zh=new Ze,Qt=class{constructor(e=new Z(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,i,r){return this.normal.set(e,t,i),this.constant=r,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,i){let r=Ma.subVectors(i,t).cross(Bh.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(r,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){let e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t){let i=e.delta(Ma),r=this.normal.dot(i);if(r===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;let s=-(e.start.dot(this.normal)+this.constant)/r;return s<0||s>1?null:t.copy(e.start).addScaledVector(i,s)}intersectsLine(e){let t=this.distanceToPoint(e.start),i=this.distanceToPoint(e.end);return t<0&&i>0||i<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){let i=t||zh.getNormalMatrix(e),r=this.coplanarPoint(Ma).applyMatrix4(e),s=this.normal.applyMatrix3(i).normalize();return this.constant=-r.dot(s),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}},ri=new Xn,Vh=new ze(.5,.5),ys=new Z,Wi=class{constructor(e=new Qt,t=new Qt,i=new Qt,r=new Qt,s=new Qt,o=new Qt){this.planes=[e,t,i,r,s,o]}set(e,t,i,r,s,o){let c=this.planes;return c[0].copy(e),c[1].copy(t),c[2].copy(i),c[3].copy(r),c[4].copy(s),c[5].copy(o),this}copy(e){let t=this.planes;for(let i=0;i<6;i++)t[i].copy(e.planes[i]);return this}setFromProjectionMatrix(e,t=ln,i=!1){let r=this.planes,s=e.elements,o=s[0],c=s[1],l=s[2],a=s[3],d=s[4],p=s[5],f=s[6],m=s[7],g=s[8],y=s[9],h=s[10],u=s[11],E=s[12],x=s[13],_=s[14],A=s[15];if(r[0].setComponents(a-o,m-d,u-g,A-E).normalize(),r[1].setComponents(a+o,m+d,u+g,A+E).normalize(),r[2].setComponents(a+c,m+p,u+y,A+x).normalize(),r[3].setComponents(a-c,m-p,u-y,A-x).normalize(),i)r[4].setComponents(l,f,h,_).normalize(),r[5].setComponents(a-l,m-f,u-h,A-_).normalize();else if(r[4].setComponents(a-l,m-f,u-h,A-_).normalize(),t===ln)r[5].setComponents(a+l,m+f,u+h,A+_).normalize();else if(t===yr)r[5].setComponents(l,f,h,_).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),ri.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{let t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),ri.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(ri)}intersectsSprite(e){ri.center.set(0,0,0);let t=Vh.distanceTo(e.center);return ri.radius=.7071067811865476+t,ri.applyMatrix4(e.matrixWorld),this.intersectsSphere(ri)}intersectsSphere(e){let t=this.planes,i=e.center,r=-e.radius;for(let s=0;s<6;s++)if(t[s].distanceToPoint(i)<r)return!1;return!0}intersectsBox(e){let t=this.planes;for(let i=0;i<6;i++){let r=t[i];if(ys.x=r.normal.x>0?e.max.x:e.min.x,ys.y=r.normal.y>0?e.max.y:e.min.y,ys.z=r.normal.z>0?e.max.z:e.min.z,r.distanceToPoint(ys)<0)return!1}return!0}containsPoint(e){let t=this.planes;for(let i=0;i<6;i++)if(t[i].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}};var Xi=class extends xn{constructor(e){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new qe(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}},Us=new Z,Fs=new Z,tl=new yt,dr=new Yn,vs=new Xn,ba=new Z,nl=new Z,ks=class extends Et{constructor(e=new Tt,t=new Xi){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){let e=this.geometry;if(e.index===null){let t=e.attributes.position,i=[0];for(let r=1,s=t.count;r<s;r++)Us.fromBufferAttribute(t,r-1),Fs.fromBufferAttribute(t,r),i[r]=i[r-1],i[r]+=Us.distanceTo(Fs);e.setAttribute("lineDistance",new Qe(i,1))}else console.warn("THREE.Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(e,t){let i=this.geometry,r=this.matrixWorld,s=e.params.Line.threshold,o=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),vs.copy(i.boundingSphere),vs.applyMatrix4(r),vs.radius+=s,e.ray.intersectsSphere(vs)===!1)return;tl.copy(r).invert(),dr.copy(e.ray).applyMatrix4(tl);let c=s/((this.scale.x+this.scale.y+this.scale.z)/3),l=c*c,a=this.isLineSegments?2:1,d=i.index,f=i.attributes.position;if(d!==null){let m=Math.max(0,o.start),g=Math.min(d.count,o.start+o.count);for(let y=m,h=g-1;y<h;y+=a){let u=d.getX(y),E=d.getX(y+1),x=xs(this,e,dr,l,u,E,y);x&&t.push(x)}if(this.isLineLoop){let y=d.getX(g-1),h=d.getX(m),u=xs(this,e,dr,l,y,h,g-1);u&&t.push(u)}}else{let m=Math.max(0,o.start),g=Math.min(f.count,o.start+o.count);for(let y=m,h=g-1;y<h;y+=a){let u=xs(this,e,dr,l,y,y+1,y);u&&t.push(u)}if(this.isLineLoop){let y=xs(this,e,dr,l,g-1,m,g-1);y&&t.push(y)}}}updateMorphTargets(){let t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){let r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let s=0,o=r.length;s<o;s++){let c=r[s].name||String(s);this.morphTargetInfluences.push(0),this.morphTargetDictionary[c]=s}}}}};function xs(n,e,t,i,r,s,o){let c=n.geometry.attributes.position;if(Us.fromBufferAttribute(c,r),Fs.fromBufferAttribute(c,s),t.distanceSqToSegment(Us,Fs,ba,nl)>i)return;ba.applyMatrix4(n.matrixWorld);let a=e.ray.origin.distanceTo(ba);if(!(a<e.near||a>e.far))return{distance:a,point:nl.clone().applyMatrix4(n.matrixWorld),index:o,face:null,faceIndex:null,barycoord:null,object:n}}var il=new Z,rl=new Z,Ar=class extends ks{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){let e=this.geometry;if(e.index===null){let t=e.attributes.position,i=[];for(let r=0,s=t.count;r<s;r+=2)il.fromBufferAttribute(t,r),rl.fromBufferAttribute(t,r+1),i[r]=r===0?0:i[r-1],i[r+1]=i[r]+il.distanceTo(rl);e.setAttribute("lineDistance",new Qe(i,1))}else console.warn("THREE.LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}};var Yi=class extends xn{constructor(e){super(),this.isPointsMaterial=!0,this.type="PointsMaterial",this.color=new qe(16777215),this.map=null,this.alphaMap=null,this.size=1,this.sizeAttenuation=!0,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.alphaMap=e.alphaMap,this.size=e.size,this.sizeAttenuation=e.sizeAttenuation,this.fog=e.fog,this}},sl=new yt,La=new Yn,Es=new Xn,Ss=new Z,Rr=class extends Et{constructor(e=new Tt,t=new Yi){super(),this.isPoints=!0,this.type="Points",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}raycast(e,t){let i=this.geometry,r=this.matrixWorld,s=e.params.Points.threshold,o=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),Es.copy(i.boundingSphere),Es.applyMatrix4(r),Es.radius+=s,e.ray.intersectsSphere(Es)===!1)return;sl.copy(r).invert(),La.copy(e.ray).applyMatrix4(sl);let c=s/((this.scale.x+this.scale.y+this.scale.z)/3),l=c*c,a=i.index,p=i.attributes.position;if(a!==null){let f=Math.max(0,o.start),m=Math.min(a.count,o.start+o.count);for(let g=f,y=m;g<y;g++){let h=a.getX(g);Ss.fromBufferAttribute(p,h),ol(Ss,h,l,r,e,t,this)}}else{let f=Math.max(0,o.start),m=Math.min(p.count,o.start+o.count);for(let g=f,y=m;g<y;g++)Ss.fromBufferAttribute(p,g),ol(Ss,g,l,r,e,t,this)}}updateMorphTargets(){let t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){let r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let s=0,o=r.length;s<o;s++){let c=r[s].name||String(s);this.morphTargetInfluences.push(0),this.morphTargetDictionary[c]=s}}}}};function ol(n,e,t,i,r,s,o){let c=La.distanceSqToPoint(n);if(c<t){let l=new Z;La.closestPointToPoint(n,l),l.applyMatrix4(i);let a=r.ray.origin.distanceTo(l);if(a<r.near||a>r.far)return;s.push({distance:a,distanceToRay:Math.sqrt(c),point:l,index:e,face:null,faceIndex:null,barycoord:null,object:o})}}var wr=class extends Ft{constructor(e,t,i=Qn,r,s,o,c=Bt,l=Bt,a,d=Bi,p=1){if(d!==Bi&&d!==er)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");let f={width:e,height:t,depth:p};super(f,r,s,o,c,l,d,i,a),this.isDepthTexture=!0,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new Gi(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){let t=super.toJSON(e);return this.compareFunction!==null&&(t.compareFunction=this.compareFunction),t}};var qi=class n extends Tt{constructor(e=1,t=1,i=1,r=32,s=1,o=!1,c=0,l=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:i,radialSegments:r,heightSegments:s,openEnded:o,thetaStart:c,thetaLength:l};let a=this;r=Math.floor(r),s=Math.floor(s);let d=[],p=[],f=[],m=[],g=0,y=[],h=i/2,u=0;E(),o===!1&&(e>0&&x(!0),t>0&&x(!1)),this.setIndex(d),this.setAttribute("position",new Qe(p,3)),this.setAttribute("normal",new Qe(f,3)),this.setAttribute("uv",new Qe(m,2));function E(){let _=new Z,A=new Z,N=0,w=(t-e)/i;for(let O=0;O<=s;O++){let T=[],M=O/s,R=M*(t-e)+e;for(let I=0;I<=r;I++){let U=I/r,P=U*l+c,X=Math.sin(P),W=Math.cos(P);A.x=R*X,A.y=-M*i+h,A.z=R*W,p.push(A.x,A.y,A.z),_.set(X,w,W).normalize(),f.push(_.x,_.y,_.z),m.push(U,1-M),T.push(g++)}y.push(T)}for(let O=0;O<r;O++)for(let T=0;T<s;T++){let M=y[T][O],R=y[T+1][O],I=y[T+1][O+1],U=y[T][O+1];(e>0||T!==0)&&(d.push(M,R,U),N+=3),(t>0||T!==s-1)&&(d.push(R,I,U),N+=3)}a.addGroup(u,N,0),u+=N}function x(_){let A=g,N=new ze,w=new Z,O=0,T=_===!0?e:t,M=_===!0?1:-1;for(let I=1;I<=r;I++)p.push(0,h*M,0),f.push(0,M,0),m.push(.5,.5),g++;let R=g;for(let I=0;I<=r;I++){let P=I/r*l+c,X=Math.cos(P),W=Math.sin(P);w.x=T*W,w.y=h*M,w.z=T*X,p.push(w.x,w.y,w.z),f.push(0,M,0),N.x=X*.5+.5,N.y=W*.5*M+.5,m.push(N.x,N.y),g++}for(let I=0;I<r;I++){let U=A+I,P=R+I;_===!0?d.push(P,P+1,U):d.push(P+1,P,U),O+=3}a.addGroup(u,O,_===!0?1:2),u+=O}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}},Cr=class n extends qi{constructor(e=1,t=1,i=32,r=1,s=!1,o=0,c=Math.PI*2){super(0,e,t,i,r,s,o,c),this.type="ConeGeometry",this.parameters={radius:e,height:t,radialSegments:i,heightSegments:r,openEnded:s,thetaStart:o,thetaLength:c}}static fromJSON(e){return new n(e.radius,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}};function Gh(n,e,t=2){let i=e&&e.length,r=i?e[0]*t:n.length,s=iu(n,0,r,t,!0),o=[];if(!s||s.next===s.prev)return o;let c,l,a;if(i&&(s=qh(n,e,s,t)),n.length>80*t){c=1/0,l=1/0;let d=-1/0,p=-1/0;for(let f=t;f<r;f+=t){let m=n[f],g=n[f+1];m<c&&(c=m),g<l&&(l=g),m>d&&(d=m),g>p&&(p=g)}a=Math.max(d-c,p-l),a=a!==0?32767/a:0}return Ir(s,o,t,c,l,a,0),o}function iu(n,e,t,i,r){let s;if(r===rd(n,e,t,i)>0)for(let o=e;o<t;o+=i)s=al(o/i|0,n[o],n[o+1],s);else for(let o=t-i;o>=e;o-=i)s=al(o/i|0,n[o],n[o+1],s);return s&&Ki(s,s.next)&&(Lr(s),s=s.next),s}function hi(n,e){if(!n)return n;e||(e=n);let t=n,i;do if(i=!1,!t.steiner&&(Ki(t,t.next)||_t(t.prev,t,t.next)===0)){if(Lr(t),t=e=t.prev,t===t.next)break;i=!0}else t=t.next;while(i||t!==e);return e}function Ir(n,e,t,i,r,s,o){if(!n)return;!o&&s&&$h(n,i,r,s);let c=n;for(;n.prev!==n.next;){let l=n.prev,a=n.next;if(s?Wh(n,i,r,s):Hh(n)){e.push(l.i,n.i,a.i),Lr(n),n=a.next,c=a.next;continue}if(n=a,n===c){o?o===1?(n=Xh(hi(n),e),Ir(n,e,t,i,r,s,2)):o===2&&Yh(n,e,t,i,r,s):Ir(hi(n),e,t,i,r,s,1);break}}}function Hh(n){let e=n.prev,t=n,i=n.next;if(_t(e,t,i)>=0)return!1;let r=e.x,s=t.x,o=i.x,c=e.y,l=t.y,a=i.y,d=Math.min(r,s,o),p=Math.min(c,l,a),f=Math.max(r,s,o),m=Math.max(c,l,a),g=i.next;for(;g!==e;){if(g.x>=d&&g.x<=f&&g.y>=p&&g.y<=m&&fr(r,c,s,l,o,a,g.x,g.y)&&_t(g.prev,g,g.next)>=0)return!1;g=g.next}return!0}function Wh(n,e,t,i){let r=n.prev,s=n,o=n.next;if(_t(r,s,o)>=0)return!1;let c=r.x,l=s.x,a=o.x,d=r.y,p=s.y,f=o.y,m=Math.min(c,l,a),g=Math.min(d,p,f),y=Math.max(c,l,a),h=Math.max(d,p,f),u=Na(m,g,e,t,i),E=Na(y,h,e,t,i),x=n.prevZ,_=n.nextZ;for(;x&&x.z>=u&&_&&_.z<=E;){if(x.x>=m&&x.x<=y&&x.y>=g&&x.y<=h&&x!==r&&x!==o&&fr(c,d,l,p,a,f,x.x,x.y)&&_t(x.prev,x,x.next)>=0||(x=x.prevZ,_.x>=m&&_.x<=y&&_.y>=g&&_.y<=h&&_!==r&&_!==o&&fr(c,d,l,p,a,f,_.x,_.y)&&_t(_.prev,_,_.next)>=0))return!1;_=_.nextZ}for(;x&&x.z>=u;){if(x.x>=m&&x.x<=y&&x.y>=g&&x.y<=h&&x!==r&&x!==o&&fr(c,d,l,p,a,f,x.x,x.y)&&_t(x.prev,x,x.next)>=0)return!1;x=x.prevZ}for(;_&&_.z<=E;){if(_.x>=m&&_.x<=y&&_.y>=g&&_.y<=h&&_!==r&&_!==o&&fr(c,d,l,p,a,f,_.x,_.y)&&_t(_.prev,_,_.next)>=0)return!1;_=_.nextZ}return!0}function Xh(n,e){let t=n;do{let i=t.prev,r=t.next.next;!Ki(i,r)&&su(i,t,t.next,r)&&Pr(i,r)&&Pr(r,i)&&(e.push(i.i,t.i,r.i),Lr(t),Lr(t.next),t=n=r),t=t.next}while(t!==n);return hi(t)}function Yh(n,e,t,i,r,s){let o=n;do{let c=o.next.next;for(;c!==o.prev;){if(o.i!==c.i&&td(o,c)){let l=ou(o,c);o=hi(o,o.next),l=hi(l,l.next),Ir(o,e,t,i,r,s,0),Ir(l,e,t,i,r,s,0);return}c=c.next}o=o.next}while(o!==n)}function qh(n,e,t,i){let r=[];for(let s=0,o=e.length;s<o;s++){let c=e[s]*i,l=s<o-1?e[s+1]*i:n.length,a=iu(n,c,l,i,!1);a===a.next&&(a.steiner=!0),r.push(ed(a))}r.sort(Kh);for(let s=0;s<r.length;s++)t=Zh(r[s],t);return t}function Kh(n,e){let t=n.x-e.x;if(t===0&&(t=n.y-e.y,t===0)){let i=(n.next.y-n.y)/(n.next.x-n.x),r=(e.next.y-e.y)/(e.next.x-e.x);t=i-r}return t}function Zh(n,e){let t=jh(n,e);if(!t)return e;let i=ou(t,n);return hi(i,i.next),hi(t,t.next)}function jh(n,e){let t=e,i=n.x,r=n.y,s=-1/0,o;if(Ki(n,t))return t;do{if(Ki(n,t.next))return t.next;if(r<=t.y&&r>=t.next.y&&t.next.y!==t.y){let p=t.x+(r-t.y)*(t.next.x-t.x)/(t.next.y-t.y);if(p<=i&&p>s&&(s=p,o=t.x<t.next.x?t:t.next,p===i))return o}t=t.next}while(t!==e);if(!o)return null;let c=o,l=o.x,a=o.y,d=1/0;t=o;do{if(i>=t.x&&t.x>=l&&i!==t.x&&ru(r<a?i:s,r,l,a,r<a?s:i,r,t.x,t.y)){let p=Math.abs(r-t.y)/(i-t.x);Pr(t,n)&&(p<d||p===d&&(t.x>o.x||t.x===o.x&&Jh(o,t)))&&(o=t,d=p)}t=t.next}while(t!==c);return o}function Jh(n,e){return _t(n.prev,n,e.prev)<0&&_t(e.next,n,n.next)<0}function $h(n,e,t,i){let r=n;do r.z===0&&(r.z=Na(r.x,r.y,e,t,i)),r.prevZ=r.prev,r.nextZ=r.next,r=r.next;while(r!==n);r.prevZ.nextZ=null,r.prevZ=null,Qh(r)}function Qh(n){let e,t=1;do{let i=n,r;n=null;let s=null;for(e=0;i;){e++;let o=i,c=0;for(let a=0;a<t&&(c++,o=o.nextZ,!!o);a++);let l=t;for(;c>0||l>0&&o;)c!==0&&(l===0||!o||i.z<=o.z)?(r=i,i=i.nextZ,c--):(r=o,o=o.nextZ,l--),s?s.nextZ=r:n=r,r.prevZ=s,s=r;i=o}s.nextZ=null,t*=2}while(e>1);return n}function Na(n,e,t,i,r){return n=(n-t)*r|0,e=(e-i)*r|0,n=(n|n<<8)&16711935,n=(n|n<<4)&252645135,n=(n|n<<2)&858993459,n=(n|n<<1)&1431655765,e=(e|e<<8)&16711935,e=(e|e<<4)&252645135,e=(e|e<<2)&858993459,e=(e|e<<1)&1431655765,n|e<<1}function ed(n){let e=n,t=n;do(e.x<t.x||e.x===t.x&&e.y<t.y)&&(t=e),e=e.next;while(e!==n);return t}function ru(n,e,t,i,r,s,o,c){return(r-o)*(e-c)>=(n-o)*(s-c)&&(n-o)*(i-c)>=(t-o)*(e-c)&&(t-o)*(s-c)>=(r-o)*(i-c)}function fr(n,e,t,i,r,s,o,c){return!(n===o&&e===c)&&ru(n,e,t,i,r,s,o,c)}function td(n,e){return n.next.i!==e.i&&n.prev.i!==e.i&&!nd(n,e)&&(Pr(n,e)&&Pr(e,n)&&id(n,e)&&(_t(n.prev,n,e.prev)||_t(n,e.prev,e))||Ki(n,e)&&_t(n.prev,n,n.next)>0&&_t(e.prev,e,e.next)>0)}function _t(n,e,t){return(e.y-n.y)*(t.x-e.x)-(e.x-n.x)*(t.y-e.y)}function Ki(n,e){return n.x===e.x&&n.y===e.y}function su(n,e,t,i){let r=Ms(_t(n,e,t)),s=Ms(_t(n,e,i)),o=Ms(_t(t,i,n)),c=Ms(_t(t,i,e));return!!(r!==s&&o!==c||r===0&&Ts(n,t,e)||s===0&&Ts(n,i,e)||o===0&&Ts(t,n,i)||c===0&&Ts(t,e,i))}function Ts(n,e,t){return e.x<=Math.max(n.x,t.x)&&e.x>=Math.min(n.x,t.x)&&e.y<=Math.max(n.y,t.y)&&e.y>=Math.min(n.y,t.y)}function Ms(n){return n>0?1:n<0?-1:0}function nd(n,e){let t=n;do{if(t.i!==n.i&&t.next.i!==n.i&&t.i!==e.i&&t.next.i!==e.i&&su(t,t.next,n,e))return!0;t=t.next}while(t!==n);return!1}function Pr(n,e){return _t(n.prev,n,n.next)<0?_t(n,e,n.next)>=0&&_t(n,n.prev,e)>=0:_t(n,e,n.prev)<0||_t(n,n.next,e)<0}function id(n,e){let t=n,i=!1,r=(n.x+e.x)/2,s=(n.y+e.y)/2;do t.y>s!=t.next.y>s&&t.next.y!==t.y&&r<(t.next.x-t.x)*(s-t.y)/(t.next.y-t.y)+t.x&&(i=!i),t=t.next;while(t!==n);return i}function ou(n,e){let t=Oa(n.i,n.x,n.y),i=Oa(e.i,e.x,e.y),r=n.next,s=e.prev;return n.next=e,e.prev=n,t.next=r,r.prev=t,i.next=t,t.prev=i,s.next=i,i.prev=s,i}function al(n,e,t,i){let r=Oa(n,e,t);return i?(r.next=i.next,r.prev=i,i.next.prev=r,i.next=r):(r.prev=r,r.next=r),r}function Lr(n){n.next.prev=n.prev,n.prev.next=n.next,n.prevZ&&(n.prevZ.nextZ=n.nextZ),n.nextZ&&(n.nextZ.prevZ=n.prevZ)}function Oa(n,e,t){return{i:n,x:e,y:t,prev:null,next:null,z:0,prevZ:null,nextZ:null,steiner:!1}}function rd(n,e,t,i){let r=0;for(let s=e,o=t-i;s<t;s+=i)r+=(n[o]-n[s])*(n[s+1]+n[o+1]),o=s;return r}var Da=class{static triangulate(e,t,i=2){return Gh(e,t,i)}},Nr=class n{static area(e){let t=e.length,i=0;for(let r=t-1,s=0;s<t;r=s++)i+=e[r].x*e[s].y-e[s].x*e[r].y;return i*.5}static isClockWise(e){return n.area(e)<0}static triangulateShape(e,t){let i=[],r=[],s=[];cl(e),ll(i,e);let o=e.length;t.forEach(cl);for(let l=0;l<t.length;l++)r.push(o),o+=t[l].length,ll(i,t[l]);let c=Da.triangulate(i,r);for(let l=0;l<c.length;l+=3)s.push(c.slice(l,l+3));return s}};function cl(n){let e=n.length;e>2&&n[e-1].equals(n[0])&&n.pop()}function ll(n,e){for(let t=0;t<e.length;t++)n.push(e[t].x),n.push(e[t].y)}var Or=class n extends Tt{constructor(e=1,t=1,i=1,r=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:i,heightSegments:r};let s=e/2,o=t/2,c=Math.floor(i),l=Math.floor(r),a=c+1,d=l+1,p=e/c,f=t/l,m=[],g=[],y=[],h=[];for(let u=0;u<d;u++){let E=u*f-o;for(let x=0;x<a;x++){let _=x*p-s;g.push(_,-E,0),y.push(0,0,1),h.push(x/c),h.push(1-u/l)}}for(let u=0;u<l;u++)for(let E=0;E<c;E++){let x=E+a*u,_=E+a*(u+1),A=E+1+a*(u+1),N=E+1+a*u;m.push(x,_,N),m.push(_,A,N)}this.setIndex(m),this.setAttribute("position",new Qe(g,3)),this.setAttribute("normal",new Qe(y,3)),this.setAttribute("uv",new Qe(h,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.width,e.height,e.widthSegments,e.heightSegments)}};var di=class n extends Tt{constructor(e=1,t=32,i=16,r=0,s=Math.PI*2,o=0,c=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:i,phiStart:r,phiLength:s,thetaStart:o,thetaLength:c},t=Math.max(3,Math.floor(t)),i=Math.max(2,Math.floor(i));let l=Math.min(o+c,Math.PI),a=0,d=[],p=new Z,f=new Z,m=[],g=[],y=[],h=[];for(let u=0;u<=i;u++){let E=[],x=u/i,_=0;u===0&&o===0?_=.5/t:u===i&&l===Math.PI&&(_=-.5/t);for(let A=0;A<=t;A++){let N=A/t;p.x=-e*Math.cos(r+N*s)*Math.sin(o+x*c),p.y=e*Math.cos(o+x*c),p.z=e*Math.sin(r+N*s)*Math.sin(o+x*c),g.push(p.x,p.y,p.z),f.copy(p).normalize(),y.push(f.x,f.y,f.z),h.push(N+_,1-x),E.push(a++)}d.push(E)}for(let u=0;u<i;u++)for(let E=0;E<t;E++){let x=d[u][E+1],_=d[u][E],A=d[u+1][E],N=d[u+1][E+1];(u!==0||o>0)&&m.push(x,_,N),(u!==i-1||l<Math.PI)&&m.push(_,A,N)}this.setIndex(m),this.setAttribute("position",new Qe(g,3)),this.setAttribute("normal",new Qe(y,3)),this.setAttribute("uv",new Qe(h,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new n(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}};var Dr=class extends xn{constructor(e){super(),this.isMeshPhongMaterial=!0,this.type="MeshPhongMaterial",this.color=new qe(16777215),this.specular=new qe(1118481),this.shininess=30,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new qe(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=ec,this.normalScale=new ze(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new dn,this.combine=ro,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.specular.copy(e.specular),this.shininess=e.shininess,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}};var Bs=class extends xn{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=Hl,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}},zs=class extends xn{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}};function bs(n,e){return!n||n.constructor===e?n:typeof e.BYTES_PER_ELEMENT=="number"?new e(n):Array.prototype.slice.call(n)}function sd(n){return ArrayBuffer.isView(n)&&!(n instanceof DataView)}var fi=class{constructor(e,t,i,r){this.parameterPositions=e,this._cachedIndex=0,this.resultBuffer=r!==void 0?r:new t.constructor(i),this.sampleValues=t,this.valueSize=i,this.settings=null,this.DefaultSettings_={}}evaluate(e){let t=this.parameterPositions,i=this._cachedIndex,r=t[i],s=t[i-1];e:{t:{let o;n:{i:if(!(e<r)){for(let c=i+2;;){if(r===void 0){if(e<s)break i;return i=t.length,this._cachedIndex=i,this.copySampleValue_(i-1)}if(i===c)break;if(s=r,r=t[++i],e<r)break t}o=t.length;break n}if(!(e>=s)){let c=t[1];e<c&&(i=2,s=c);for(let l=i-2;;){if(s===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(i===l)break;if(r=s,s=t[--i-1],e>=s)break t}o=i,i=0;break n}break e}for(;i<o;){let c=i+o>>>1;e<t[c]?o=c:i=c+1}if(r=t[i],s=t[i-1],s===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(r===void 0)return i=t.length,this._cachedIndex=i,this.copySampleValue_(i-1)}this._cachedIndex=i,this.intervalChanged_(i,s,r)}return this.interpolate_(i,s,e,r)}getSettings_(){return this.settings||this.DefaultSettings_}copySampleValue_(e){let t=this.resultBuffer,i=this.sampleValues,r=this.valueSize,s=e*r;for(let o=0;o!==r;++o)t[o]=i[s+o];return t}interpolate_(){throw new Error("call to abstract method")}intervalChanged_(){}},Vs=class extends fi{constructor(e,t,i,r){super(e,t,i,r),this._weightPrev=-0,this._offsetPrev=-0,this._weightNext=-0,this._offsetNext=-0,this.DefaultSettings_={endingStart:Ra,endingEnd:Ra}}intervalChanged_(e,t,i){let r=this.parameterPositions,s=e-2,o=e+1,c=r[s],l=r[o];if(c===void 0)switch(this.getSettings_().endingStart){case wa:s=e,c=2*t-i;break;case Ca:s=r.length-2,c=t+r[s]-r[s+1];break;default:s=e,c=i}if(l===void 0)switch(this.getSettings_().endingEnd){case wa:o=e,l=2*i-t;break;case Ca:o=1,l=i+r[1]-r[0];break;default:o=e-1,l=t}let a=(i-t)*.5,d=this.valueSize;this._weightPrev=a/(t-c),this._weightNext=a/(l-i),this._offsetPrev=s*d,this._offsetNext=o*d}interpolate_(e,t,i,r){let s=this.resultBuffer,o=this.sampleValues,c=this.valueSize,l=e*c,a=l-c,d=this._offsetPrev,p=this._offsetNext,f=this._weightPrev,m=this._weightNext,g=(i-t)/(r-t),y=g*g,h=y*g,u=-f*h+2*f*y-f*g,E=(1+f)*h+(-1.5-2*f)*y+(-.5+f)*g+1,x=(-1-m)*h+(1.5+m)*y+.5*g,_=m*h-m*y;for(let A=0;A!==c;++A)s[A]=u*o[d+A]+E*o[a+A]+x*o[l+A]+_*o[p+A];return s}},Gs=class extends fi{constructor(e,t,i,r){super(e,t,i,r)}interpolate_(e,t,i,r){let s=this.resultBuffer,o=this.sampleValues,c=this.valueSize,l=e*c,a=l-c,d=(i-t)/(r-t),p=1-d;for(let f=0;f!==c;++f)s[f]=o[a+f]*p+o[l+f]*d;return s}},Hs=class extends fi{constructor(e,t,i,r){super(e,t,i,r)}interpolate_(e){return this.copySampleValue_(e-1)}},qt=class{constructor(e,t,i,r){if(e===void 0)throw new Error("THREE.KeyframeTrack: track name is undefined");if(t===void 0||t.length===0)throw new Error("THREE.KeyframeTrack: no keyframes in track named "+e);this.name=e,this.times=bs(t,this.TimeBufferType),this.values=bs(i,this.ValueBufferType),this.setInterpolation(r||this.DefaultInterpolation)}static toJSON(e){let t=e.constructor,i;if(t.toJSON!==this.toJSON)i=t.toJSON(e);else{i={name:e.name,times:bs(e.times,Array),values:bs(e.values,Array)};let r=e.getInterpolation();r!==e.DefaultInterpolation&&(i.interpolation=r)}return i.type=e.ValueTypeName,i}InterpolantFactoryMethodDiscrete(e){return new Hs(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodLinear(e){return new Gs(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodSmooth(e){return new Vs(this.times,this.values,this.getValueSize(),e)}setInterpolation(e){let t;switch(e){case gr:t=this.InterpolantFactoryMethodDiscrete;break;case Is:t=this.InterpolantFactoryMethodLinear;break;case As:t=this.InterpolantFactoryMethodSmooth;break}if(t===void 0){let i="unsupported interpolation for "+this.ValueTypeName+" keyframe track named "+this.name;if(this.createInterpolant===void 0)if(e!==this.DefaultInterpolation)this.setInterpolation(this.DefaultInterpolation);else throw new Error(i);return console.warn("THREE.KeyframeTrack:",i),this}return this.createInterpolant=t,this}getInterpolation(){switch(this.createInterpolant){case this.InterpolantFactoryMethodDiscrete:return gr;case this.InterpolantFactoryMethodLinear:return Is;case this.InterpolantFactoryMethodSmooth:return As}}getValueSize(){return this.values.length/this.times.length}shift(e){if(e!==0){let t=this.times;for(let i=0,r=t.length;i!==r;++i)t[i]+=e}return this}scale(e){if(e!==1){let t=this.times;for(let i=0,r=t.length;i!==r;++i)t[i]*=e}return this}trim(e,t){let i=this.times,r=i.length,s=0,o=r-1;for(;s!==r&&i[s]<e;)++s;for(;o!==-1&&i[o]>t;)--o;if(++o,s!==0||o!==r){s>=o&&(o=Math.max(o,1),s=o-1);let c=this.getValueSize();this.times=i.slice(s,o),this.values=this.values.slice(s*c,o*c)}return this}validate(){let e=!0,t=this.getValueSize();t-Math.floor(t)!==0&&(console.error("THREE.KeyframeTrack: Invalid value size in track.",this),e=!1);let i=this.times,r=this.values,s=i.length;s===0&&(console.error("THREE.KeyframeTrack: Track is empty.",this),e=!1);let o=null;for(let c=0;c!==s;c++){let l=i[c];if(typeof l=="number"&&isNaN(l)){console.error("THREE.KeyframeTrack: Time is not a valid number.",this,c,l),e=!1;break}if(o!==null&&o>l){console.error("THREE.KeyframeTrack: Out of order keys.",this,c,l,o),e=!1;break}o=l}if(r!==void 0&&sd(r))for(let c=0,l=r.length;c!==l;++c){let a=r[c];if(isNaN(a)){console.error("THREE.KeyframeTrack: Value is not a valid number.",this,c,a),e=!1;break}}return e}optimize(){let e=this.times.slice(),t=this.values.slice(),i=this.getValueSize(),r=this.getInterpolation()===As,s=e.length-1,o=1;for(let c=1;c<s;++c){let l=!1,a=e[c],d=e[c+1];if(a!==d&&(c!==1||a!==e[0]))if(r)l=!0;else{let p=c*i,f=p-i,m=p+i;for(let g=0;g!==i;++g){let y=t[p+g];if(y!==t[f+g]||y!==t[m+g]){l=!0;break}}}if(l){if(c!==o){e[o]=e[c];let p=c*i,f=o*i;for(let m=0;m!==i;++m)t[f+m]=t[p+m]}++o}}if(s>0){e[o]=e[s];for(let c=s*i,l=o*i,a=0;a!==i;++a)t[l+a]=t[c+a];++o}return o!==e.length?(this.times=e.slice(0,o),this.values=t.slice(0,o*i)):(this.times=e,this.values=t),this}clone(){let e=this.times.slice(),t=this.values.slice(),i=this.constructor,r=new i(this.name,e,t);return r.createInterpolant=this.createInterpolant,r}};qt.prototype.ValueTypeName="";qt.prototype.TimeBufferType=Float32Array;qt.prototype.ValueBufferType=Float32Array;qt.prototype.DefaultInterpolation=Is;var Kn=class extends qt{constructor(e,t,i){super(e,t,i)}};Kn.prototype.ValueTypeName="bool";Kn.prototype.ValueBufferType=Array;Kn.prototype.DefaultInterpolation=gr;Kn.prototype.InterpolantFactoryMethodLinear=void 0;Kn.prototype.InterpolantFactoryMethodSmooth=void 0;var Ws=class extends qt{constructor(e,t,i,r){super(e,t,i,r)}};Ws.prototype.ValueTypeName="color";var Xs=class extends qt{constructor(e,t,i,r){super(e,t,i,r)}};Xs.prototype.ValueTypeName="number";var Ys=class extends fi{constructor(e,t,i,r){super(e,t,i,r)}interpolate_(e,t,i,r){let s=this.resultBuffer,o=this.sampleValues,c=this.valueSize,l=(i-t)/(r-t),a=e*c;for(let d=a+c;a!==d;a+=4)zt.slerpFlat(s,0,o,a-c,o,a,l);return s}},Ur=class extends qt{constructor(e,t,i,r){super(e,t,i,r)}InterpolantFactoryMethodLinear(e){return new Ys(this.times,this.values,this.getValueSize(),e)}};Ur.prototype.ValueTypeName="quaternion";Ur.prototype.InterpolantFactoryMethodSmooth=void 0;var Zn=class extends qt{constructor(e,t,i){super(e,t,i)}};Zn.prototype.ValueTypeName="string";Zn.prototype.ValueBufferType=Array;Zn.prototype.DefaultInterpolation=gr;Zn.prototype.InterpolantFactoryMethodLinear=void 0;Zn.prototype.InterpolantFactoryMethodSmooth=void 0;var qs=class extends qt{constructor(e,t,i,r){super(e,t,i,r)}};qs.prototype.ValueTypeName="vector";var ki={enabled:!1,files:{},add:function(n,e){this.enabled!==!1&&(this.files[n]=e)},get:function(n){if(this.enabled!==!1)return this.files[n]},remove:function(n){delete this.files[n]},clear:function(){this.files={}}},Ks=class{constructor(e,t,i){let r=this,s=!1,o=0,c=0,l,a=[];this.onStart=void 0,this.onLoad=e,this.onProgress=t,this.onError=i,this.abortController=new AbortController,this.itemStart=function(d){c++,s===!1&&r.onStart!==void 0&&r.onStart(d,o,c),s=!0},this.itemEnd=function(d){o++,r.onProgress!==void 0&&r.onProgress(d,o,c),o===c&&(s=!1,r.onLoad!==void 0&&r.onLoad())},this.itemError=function(d){r.onError!==void 0&&r.onError(d)},this.resolveURL=function(d){return l?l(d):d},this.setURLModifier=function(d){return l=d,this},this.addHandler=function(d,p){return a.push(d,p),this},this.removeHandler=function(d){let p=a.indexOf(d);return p!==-1&&a.splice(p,2),this},this.getHandler=function(d){for(let p=0,f=a.length;p<f;p+=2){let m=a[p],g=a[p+1];if(m.global&&(m.lastIndex=0),m.test(d))return g}return null},this.abort=function(){return this.abortController.abort(),this.abortController=new AbortController,this}}},au=new Ks,Kt=class{constructor(e){this.manager=e!==void 0?e:au,this.crossOrigin="anonymous",this.withCredentials=!1,this.path="",this.resourcePath="",this.requestHeader={}}load(){}loadAsync(e,t){let i=this;return new Promise(function(r,s){i.load(e,r,t,s)})}parse(){}setCrossOrigin(e){return this.crossOrigin=e,this}setWithCredentials(e){return this.withCredentials=e,this}setPath(e){return this.path=e,this}setResourcePath(e){return this.resourcePath=e,this}setRequestHeader(e){return this.requestHeader=e,this}abort(){return this}};Kt.DEFAULT_MATERIAL_NAME="__DEFAULT";var In={},Ua=class extends Error{constructor(e,t){super(e),this.response=t}},Fr=class extends Kt{constructor(e){super(e),this.mimeType="",this.responseType="",this._abortController=new AbortController}load(e,t,i,r){e===void 0&&(e=""),this.path!==void 0&&(e=this.path+e),e=this.manager.resolveURL(e);let s=ki.get(`file:${e}`);if(s!==void 0)return this.manager.itemStart(e),setTimeout(()=>{t&&t(s),this.manager.itemEnd(e)},0),s;if(In[e]!==void 0){In[e].push({onLoad:t,onProgress:i,onError:r});return}In[e]=[],In[e].push({onLoad:t,onProgress:i,onError:r});let o=new Request(e,{headers:new Headers(this.requestHeader),credentials:this.withCredentials?"include":"same-origin",signal:typeof AbortSignal.any=="function"?AbortSignal.any([this._abortController.signal,this.manager.abortController.signal]):this._abortController.signal}),c=this.mimeType,l=this.responseType;fetch(o).then(a=>{if(a.status===200||a.status===0){if(a.status===0&&console.warn("THREE.FileLoader: HTTP Status 0 received."),typeof ReadableStream>"u"||a.body===void 0||a.body.getReader===void 0)return a;let d=In[e],p=a.body.getReader(),f=a.headers.get("X-File-Size")||a.headers.get("Content-Length"),m=f?parseInt(f):0,g=m!==0,y=0,h=new ReadableStream({start(u){E();function E(){p.read().then(({done:x,value:_})=>{if(x)u.close();else{y+=_.byteLength;let A=new ProgressEvent("progress",{lengthComputable:g,loaded:y,total:m});for(let N=0,w=d.length;N<w;N++){let O=d[N];O.onProgress&&O.onProgress(A)}u.enqueue(_),E()}},x=>{u.error(x)})}}});return new Response(h)}else throw new Ua(`fetch for "${a.url}" responded with ${a.status}: ${a.statusText}`,a)}).then(a=>{switch(l){case"arraybuffer":return a.arrayBuffer();case"blob":return a.blob();case"document":return a.text().then(d=>new DOMParser().parseFromString(d,c));case"json":return a.json();default:if(c==="")return a.text();{let p=/charset="?([^;"\s]*)"?/i.exec(c),f=p&&p[1]?p[1].toLowerCase():void 0,m=new TextDecoder(f);return a.arrayBuffer().then(g=>m.decode(g))}}}).then(a=>{ki.add(`file:${e}`,a);let d=In[e];delete In[e];for(let p=0,f=d.length;p<f;p++){let m=d[p];m.onLoad&&m.onLoad(a)}}).catch(a=>{let d=In[e];if(d===void 0)throw this.manager.itemError(e),a;delete In[e];for(let p=0,f=d.length;p<f;p++){let m=d[p];m.onError&&m.onError(a)}this.manager.itemError(e)}).finally(()=>{this.manager.itemEnd(e)}),this.manager.itemStart(e)}setResponseType(e){return this.responseType=e,this}setMimeType(e){return this.mimeType=e,this}abort(){return this._abortController.abort(),this._abortController=new AbortController,this}};var Di=new WeakMap,Zs=class extends Kt{constructor(e){super(e)}load(e,t,i,r){this.path!==void 0&&(e=this.path+e),e=this.manager.resolveURL(e);let s=this,o=ki.get(`image:${e}`);if(o!==void 0){if(o.complete===!0)s.manager.itemStart(e),setTimeout(function(){t&&t(o),s.manager.itemEnd(e)},0);else{let p=Di.get(o);p===void 0&&(p=[],Di.set(o,p)),p.push({onLoad:t,onError:r})}return o}let c=Vi("img");function l(){d(),t&&t(this);let p=Di.get(this)||[];for(let f=0;f<p.length;f++){let m=p[f];m.onLoad&&m.onLoad(this)}Di.delete(this),s.manager.itemEnd(e)}function a(p){d(),r&&r(p),ki.remove(`image:${e}`);let f=Di.get(this)||[];for(let m=0;m<f.length;m++){let g=f[m];g.onError&&g.onError(p)}Di.delete(this),s.manager.itemError(e),s.manager.itemEnd(e)}function d(){c.removeEventListener("load",l,!1),c.removeEventListener("error",a,!1)}return c.addEventListener("load",l,!1),c.addEventListener("error",a,!1),e.slice(0,5)!=="data:"&&this.crossOrigin!==void 0&&(c.crossOrigin=this.crossOrigin),ki.add(`image:${e}`,c),s.manager.itemStart(e),c.src=e,c}};var kr=class extends Kt{constructor(e){super(e)}load(e,t,i,r){let s=new Ft,o=new Zs(this.manager);return o.setCrossOrigin(this.crossOrigin),o.setPath(this.path),o.load(e,function(c){s.image=c,s.needsUpdate=!0,t!==void 0&&t(s)},i,r),s}},Br=class extends Et{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new qe(e),this.intensity=t}dispose(){}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){let t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,this.groundColor!==void 0&&(t.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(t.object.distance=this.distance),this.angle!==void 0&&(t.object.angle=this.angle),this.decay!==void 0&&(t.object.decay=this.decay),this.penumbra!==void 0&&(t.object.penumbra=this.penumbra),this.shadow!==void 0&&(t.object.shadow=this.shadow.toJSON()),this.target!==void 0&&(t.object.target=this.target.uuid),t}},zr=class extends Br{constructor(e,t,i){super(e,i),this.isHemisphereLight=!0,this.type="HemisphereLight",this.position.copy(Et.DEFAULT_UP),this.updateMatrix(),this.groundColor=new qe(t)}copy(e,t){return super.copy(e,t),this.groundColor.copy(e.groundColor),this}},Aa=new yt,ul=new Z,hl=new Z,Fa=class{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new ze(512,512),this.mapType=pn,this.map=null,this.mapPass=null,this.matrix=new yt,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Wi,this._frameExtents=new ze(1,1),this._viewportCount=1,this._viewports=[new vt(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){let t=this.camera,i=this.matrix;ul.setFromMatrixPosition(e.matrixWorld),t.position.copy(ul),hl.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(hl),t.updateMatrixWorld(),Aa.multiplyMatrices(t.projectionMatrix,t.matrixWorldInverse),this._frustum.setFromProjectionMatrix(Aa,t.coordinateSystem,t.reversedDepth),t.reversedDepth?i.set(.5,0,0,.5,0,.5,0,.5,0,0,1,0,0,0,0,1):i.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),i.multiply(Aa)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.autoUpdate=e.autoUpdate,this.needsUpdate=e.needsUpdate,this.normalBias=e.normalBias,this.blurSamples=e.blurSamples,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){let e={};return this.intensity!==1&&(e.intensity=this.intensity),this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}};var Vr=class extends Tr{constructor(e=-1,t=1,i=1,r=-1,s=.1,o=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=i,this.bottom=r,this.near=s,this.far=o,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,i,r,s,o){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=s,this.view.height=o,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),i=(this.right+this.left)/2,r=(this.top+this.bottom)/2,s=i-e,o=i+e,c=r+t,l=r-t;if(this.view!==null&&this.view.enabled){let a=(this.right-this.left)/this.view.fullWidth/this.zoom,d=(this.top-this.bottom)/this.view.fullHeight/this.zoom;s+=a*this.view.offsetX,o=s+a*this.view.width,c-=d*this.view.offsetY,l=c-d*this.view.height}this.projectionMatrix.makeOrthographic(s,o,c,l,this.near,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){let t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}},ka=class extends Fa{constructor(){super(new Vr(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}},Zi=class extends Br{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(Et.DEFAULT_UP),this.updateMatrix(),this.target=new Et,this.shadow=new ka}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}};var Gr=class{static extractUrlBase(e){let t=e.lastIndexOf("/");return t===-1?"./":e.slice(0,t+1)}static resolveURL(e,t){return typeof e!="string"||e===""?"":(/^https?:\/\//i.test(t)&&/^\//.test(e)&&(t=t.replace(/(^https?:\/\/[^\/]+).*/i,"$1")),/^(https?:)?\/\//i.test(e)||/^data:.*,.*$/i.test(e)||/^blob:.*$/i.test(e)?e:t+e)}};var js=class extends Pt{constructor(e=[]){super(),this.isArrayCamera=!0,this.isMultiViewCamera=!1,this.cameras=e}};var ac="\\[\\]\\.:\\/",od=new RegExp("["+ac+"]","g"),cc="[^"+ac+"]",ad="[^"+ac.replace("\\.","")+"]",cd=/((?:WC+[\/:])*)/.source.replace("WC",cc),ld=/(WCOD+)?/.source.replace("WCOD",ad),ud=/(?:\.(WC+)(?:\[(.+)\])?)?/.source.replace("WC",cc),hd=/\.(WC+)(?:\[(.+)\])?/.source.replace("WC",cc),dd=new RegExp("^"+cd+ld+ud+hd+"$"),fd=["material","materials","bones","map"],Ba=class{constructor(e,t,i){let r=i||ft.parseTrackName(t);this._targetGroup=e,this._bindings=e.subscribe_(t,r)}getValue(e,t){this.bind();let i=this._targetGroup.nCachedObjects_,r=this._bindings[i];r!==void 0&&r.getValue(e,t)}setValue(e,t){let i=this._bindings;for(let r=this._targetGroup.nCachedObjects_,s=i.length;r!==s;++r)i[r].setValue(e,t)}bind(){let e=this._bindings;for(let t=this._targetGroup.nCachedObjects_,i=e.length;t!==i;++t)e[t].bind()}unbind(){let e=this._bindings;for(let t=this._targetGroup.nCachedObjects_,i=e.length;t!==i;++t)e[t].unbind()}},ft=class n{constructor(e,t,i){this.path=t,this.parsedPath=i||n.parseTrackName(t),this.node=n.findNode(e,this.parsedPath.nodeName),this.rootNode=e,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}static create(e,t,i){return e&&e.isAnimationObjectGroup?new n.Composite(e,t,i):new n(e,t,i)}static sanitizeNodeName(e){return e.replace(/\s/g,"_").replace(od,"")}static parseTrackName(e){let t=dd.exec(e);if(t===null)throw new Error("PropertyBinding: Cannot parse trackName: "+e);let i={nodeName:t[2],objectName:t[3],objectIndex:t[4],propertyName:t[5],propertyIndex:t[6]},r=i.nodeName&&i.nodeName.lastIndexOf(".");if(r!==void 0&&r!==-1){let s=i.nodeName.substring(r+1);fd.indexOf(s)!==-1&&(i.nodeName=i.nodeName.substring(0,r),i.objectName=s)}if(i.propertyName===null||i.propertyName.length===0)throw new Error("PropertyBinding: can not parse propertyName from trackName: "+e);return i}static findNode(e,t){if(t===void 0||t===""||t==="."||t===-1||t===e.name||t===e.uuid)return e;if(e.skeleton){let i=e.skeleton.getBoneByName(t);if(i!==void 0)return i}if(e.children){let i=function(s){for(let o=0;o<s.length;o++){let c=s[o];if(c.name===t||c.uuid===t)return c;let l=i(c.children);if(l)return l}return null},r=i(e.children);if(r)return r}return null}_getValue_unavailable(){}_setValue_unavailable(){}_getValue_direct(e,t){e[t]=this.targetObject[this.propertyName]}_getValue_array(e,t){let i=this.resolvedProperty;for(let r=0,s=i.length;r!==s;++r)e[t++]=i[r]}_getValue_arrayElement(e,t){e[t]=this.resolvedProperty[this.propertyIndex]}_getValue_toArray(e,t){this.resolvedProperty.toArray(e,t)}_setValue_direct(e,t){this.targetObject[this.propertyName]=e[t]}_setValue_direct_setNeedsUpdate(e,t){this.targetObject[this.propertyName]=e[t],this.targetObject.needsUpdate=!0}_setValue_direct_setMatrixWorldNeedsUpdate(e,t){this.targetObject[this.propertyName]=e[t],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_array(e,t){let i=this.resolvedProperty;for(let r=0,s=i.length;r!==s;++r)i[r]=e[t++]}_setValue_array_setNeedsUpdate(e,t){let i=this.resolvedProperty;for(let r=0,s=i.length;r!==s;++r)i[r]=e[t++];this.targetObject.needsUpdate=!0}_setValue_array_setMatrixWorldNeedsUpdate(e,t){let i=this.resolvedProperty;for(let r=0,s=i.length;r!==s;++r)i[r]=e[t++];this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_arrayElement(e,t){this.resolvedProperty[this.propertyIndex]=e[t]}_setValue_arrayElement_setNeedsUpdate(e,t){this.resolvedProperty[this.propertyIndex]=e[t],this.targetObject.needsUpdate=!0}_setValue_arrayElement_setMatrixWorldNeedsUpdate(e,t){this.resolvedProperty[this.propertyIndex]=e[t],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_fromArray(e,t){this.resolvedProperty.fromArray(e,t)}_setValue_fromArray_setNeedsUpdate(e,t){this.resolvedProperty.fromArray(e,t),this.targetObject.needsUpdate=!0}_setValue_fromArray_setMatrixWorldNeedsUpdate(e,t){this.resolvedProperty.fromArray(e,t),this.targetObject.matrixWorldNeedsUpdate=!0}_getValue_unbound(e,t){this.bind(),this.getValue(e,t)}_setValue_unbound(e,t){this.bind(),this.setValue(e,t)}bind(){let e=this.node,t=this.parsedPath,i=t.objectName,r=t.propertyName,s=t.propertyIndex;if(e||(e=n.findNode(this.rootNode,t.nodeName),this.node=e),this.getValue=this._getValue_unavailable,this.setValue=this._setValue_unavailable,!e){console.warn("THREE.PropertyBinding: No target node found for track: "+this.path+".");return}if(i){let a=t.objectIndex;switch(i){case"materials":if(!e.material){console.error("THREE.PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!e.material.materials){console.error("THREE.PropertyBinding: Can not bind to material.materials as node.material does not have a materials array.",this);return}e=e.material.materials;break;case"bones":if(!e.skeleton){console.error("THREE.PropertyBinding: Can not bind to bones as node does not have a skeleton.",this);return}e=e.skeleton.bones;for(let d=0;d<e.length;d++)if(e[d].name===a){a=d;break}break;case"map":if("map"in e){e=e.map;break}if(!e.material){console.error("THREE.PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!e.material.map){console.error("THREE.PropertyBinding: Can not bind to material.map as node.material does not have a map.",this);return}e=e.material.map;break;default:if(e[i]===void 0){console.error("THREE.PropertyBinding: Can not bind to objectName of node undefined.",this);return}e=e[i]}if(a!==void 0){if(e[a]===void 0){console.error("THREE.PropertyBinding: Trying to bind to objectIndex of objectName, but is undefined.",this,e);return}e=e[a]}}let o=e[r];if(o===void 0){let a=t.nodeName;console.error("THREE.PropertyBinding: Trying to update property for track: "+a+"."+r+" but it wasn't found.",e);return}let c=this.Versioning.None;this.targetObject=e,e.isMaterial===!0?c=this.Versioning.NeedsUpdate:e.isObject3D===!0&&(c=this.Versioning.MatrixWorldNeedsUpdate);let l=this.BindingType.Direct;if(s!==void 0){if(r==="morphTargetInfluences"){if(!e.geometry){console.error("THREE.PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.",this);return}if(!e.geometry.morphAttributes){console.error("THREE.PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.morphAttributes.",this);return}e.morphTargetDictionary[s]!==void 0&&(s=e.morphTargetDictionary[s])}l=this.BindingType.ArrayElement,this.resolvedProperty=o,this.propertyIndex=s}else o.fromArray!==void 0&&o.toArray!==void 0?(l=this.BindingType.HasFromToArray,this.resolvedProperty=o):Array.isArray(o)?(l=this.BindingType.EntireArray,this.resolvedProperty=o):this.propertyName=r;this.getValue=this.GetterByBindingType[l],this.setValue=this.SetterByBindingTypeAndVersioning[l][c]}unbind(){this.node=null,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}};ft.Composite=Ba;ft.prototype.BindingType={Direct:0,EntireArray:1,ArrayElement:2,HasFromToArray:3};ft.prototype.Versioning={None:0,NeedsUpdate:1,MatrixWorldNeedsUpdate:2};ft.prototype.GetterByBindingType=[ft.prototype._getValue_direct,ft.prototype._getValue_array,ft.prototype._getValue_arrayElement,ft.prototype._getValue_toArray];ft.prototype.SetterByBindingTypeAndVersioning=[[ft.prototype._setValue_direct,ft.prototype._setValue_direct_setNeedsUpdate,ft.prototype._setValue_direct_setMatrixWorldNeedsUpdate],[ft.prototype._setValue_array,ft.prototype._setValue_array_setNeedsUpdate,ft.prototype._setValue_array_setMatrixWorldNeedsUpdate],[ft.prototype._setValue_arrayElement,ft.prototype._setValue_arrayElement_setNeedsUpdate,ft.prototype._setValue_arrayElement_setMatrixWorldNeedsUpdate],[ft.prototype._setValue_fromArray,ft.prototype._setValue_fromArray_setNeedsUpdate,ft.prototype._setValue_fromArray_setMatrixWorldNeedsUpdate]];var C_=new Float32Array(1);var ji=class{constructor(e=1,t=0,i=0){this.radius=e,this.phi=t,this.theta=i}set(e,t,i){return this.radius=e,this.phi=t,this.theta=i,this}copy(e){return this.radius=e.radius,this.phi=e.phi,this.theta=e.theta,this}makeSafe(){return this.phi=et(this.phi,1e-6,Math.PI-1e-6),this}setFromVector3(e){return this.setFromCartesianCoords(e.x,e.y,e.z)}setFromCartesianCoords(e,t,i){return this.radius=Math.sqrt(e*e+t*t+i*i),this.radius===0?(this.theta=0,this.phi=0):(this.theta=Math.atan2(e,i),this.phi=Math.acos(et(t/this.radius,-1,1))),this}clone(){return new this.constructor().copy(this)}};var Hr=class extends _n{constructor(e,t=null){super(),this.object=e,this.domElement=t,this.enabled=!0,this.state=-1,this.keys={},this.mouseButtons={LEFT:null,MIDDLE:null,RIGHT:null},this.touches={ONE:null,TWO:null}}connect(e){if(e===void 0){console.warn("THREE.Controls: connect() now requires an element.");return}this.domElement!==null&&this.disconnect(),this.domElement=e}disconnect(){}dispose(){}update(){}};function lc(n,e,t,i){let r=pd(i);switch(t){case Za:return n*e;case Ja:return n*e/r.components*r.byteLength;case ho:return n*e/r.components*r.byteLength;case $a:return n*e*2/r.components*r.byteLength;case fo:return n*e*2/r.components*r.byteLength;case ja:return n*e*3/r.components*r.byteLength;case tn:return n*e*4/r.components*r.byteLength;case po:return n*e*4/r.components*r.byteLength;case Yr:case qr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case Kr:case Zr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case go:case yo:return Math.max(n,16)*Math.max(e,8)/4;case mo:case _o:return Math.max(n,8)*Math.max(e,8)/2;case vo:case xo:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case Eo:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case So:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case To:return Math.floor((n+4)/5)*Math.floor((e+3)/4)*16;case Mo:return Math.floor((n+4)/5)*Math.floor((e+4)/5)*16;case bo:return Math.floor((n+5)/6)*Math.floor((e+4)/5)*16;case Ao:return Math.floor((n+5)/6)*Math.floor((e+5)/6)*16;case Ro:return Math.floor((n+7)/8)*Math.floor((e+4)/5)*16;case wo:return Math.floor((n+7)/8)*Math.floor((e+5)/6)*16;case Co:return Math.floor((n+7)/8)*Math.floor((e+7)/8)*16;case Io:return Math.floor((n+9)/10)*Math.floor((e+4)/5)*16;case Po:return Math.floor((n+9)/10)*Math.floor((e+5)/6)*16;case Lo:return Math.floor((n+9)/10)*Math.floor((e+7)/8)*16;case No:return Math.floor((n+9)/10)*Math.floor((e+9)/10)*16;case Oo:return Math.floor((n+11)/12)*Math.floor((e+9)/10)*16;case Do:return Math.floor((n+11)/12)*Math.floor((e+11)/12)*16;case jr:case Uo:case Fo:return Math.ceil(n/4)*Math.ceil(e/4)*16;case Qa:case ko:return Math.ceil(n/4)*Math.ceil(e/4)*8;case Bo:case zo:return Math.ceil(n/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function pd(n){switch(n){case pn:case Ya:return{byteLength:1,components:1};case Ji:case qa:case $i:return{byteLength:2,components:1};case lo:case uo:return{byteLength:2,components:4};case Qn:case co:case Tn:return{byteLength:4,components:1};case Ka:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${n}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:"179"}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__="179");function Pu(){let n=null,e=!1,t=null,i=null;function r(s,o){t(s,o),i=n.requestAnimationFrame(r)}return{start:function(){e!==!0&&t!==null&&(i=n.requestAnimationFrame(r),e=!0)},stop:function(){n.cancelAnimationFrame(i),e=!1},setAnimationLoop:function(s){t=s},setContext:function(s){n=s}}}function gd(n){let e=new WeakMap;function t(c,l){let a=c.array,d=c.usage,p=a.byteLength,f=n.createBuffer();n.bindBuffer(l,f),n.bufferData(l,a,d),c.onUploadCallback();let m;if(a instanceof Float32Array)m=n.FLOAT;else if(typeof Float16Array<"u"&&a instanceof Float16Array)m=n.HALF_FLOAT;else if(a instanceof Uint16Array)c.isFloat16BufferAttribute?m=n.HALF_FLOAT:m=n.UNSIGNED_SHORT;else if(a instanceof Int16Array)m=n.SHORT;else if(a instanceof Uint32Array)m=n.UNSIGNED_INT;else if(a instanceof Int32Array)m=n.INT;else if(a instanceof Int8Array)m=n.BYTE;else if(a instanceof Uint8Array)m=n.UNSIGNED_BYTE;else if(a instanceof Uint8ClampedArray)m=n.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+a);return{buffer:f,type:m,bytesPerElement:a.BYTES_PER_ELEMENT,version:c.version,size:p}}function i(c,l,a){let d=l.array,p=l.updateRanges;if(n.bindBuffer(a,c),p.length===0)n.bufferSubData(a,0,d);else{p.sort((m,g)=>m.start-g.start);let f=0;for(let m=1;m<p.length;m++){let g=p[f],y=p[m];y.start<=g.start+g.count+1?g.count=Math.max(g.count,y.start+y.count-g.start):(++f,p[f]=y)}p.length=f+1;for(let m=0,g=p.length;m<g;m++){let y=p[m];n.bufferSubData(a,y.start*d.BYTES_PER_ELEMENT,d,y.start,y.count)}l.clearUpdateRanges()}l.onUploadCallback()}function r(c){return c.isInterleavedBufferAttribute&&(c=c.data),e.get(c)}function s(c){c.isInterleavedBufferAttribute&&(c=c.data);let l=e.get(c);l&&(n.deleteBuffer(l.buffer),e.delete(c))}function o(c,l){if(c.isInterleavedBufferAttribute&&(c=c.data),c.isGLBufferAttribute){let d=e.get(c);(!d||d.version<c.version)&&e.set(c,{buffer:c.buffer,type:c.type,bytesPerElement:c.elementSize,version:c.version});return}let a=e.get(c);if(a===void 0)e.set(c,t(c,l));else if(a.version<c.version){if(a.size!==c.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");i(a.buffer,c,l),a.version=c.version}}return{get:r,remove:s,update:o}}var _d=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,yd=`#ifdef USE_ALPHAHASH
	const float ALPHA_HASH_SCALE = 0.05;
	float hash2D( vec2 value ) {
		return fract( 1.0e4 * sin( 17.0 * value.x + 0.1 * value.y ) * ( 0.1 + abs( sin( 13.0 * value.y + value.x ) ) ) );
	}
	float hash3D( vec3 value ) {
		return hash2D( vec2( hash2D( value.xy ), value.z ) );
	}
	float getAlphaHashThreshold( vec3 position ) {
		float maxDeriv = max(
			length( dFdx( position.xyz ) ),
			length( dFdy( position.xyz ) )
		);
		float pixScale = 1.0 / ( ALPHA_HASH_SCALE * maxDeriv );
		vec2 pixScales = vec2(
			exp2( floor( log2( pixScale ) ) ),
			exp2( ceil( log2( pixScale ) ) )
		);
		vec2 alpha = vec2(
			hash3D( floor( pixScales.x * position.xyz ) ),
			hash3D( floor( pixScales.y * position.xyz ) )
		);
		float lerpFactor = fract( log2( pixScale ) );
		float x = ( 1.0 - lerpFactor ) * alpha.x + lerpFactor * alpha.y;
		float a = min( lerpFactor, 1.0 - lerpFactor );
		vec3 cases = vec3(
			x * x / ( 2.0 * a * ( 1.0 - a ) ),
			( x - 0.5 * a ) / ( 1.0 - a ),
			1.0 - ( ( 1.0 - x ) * ( 1.0 - x ) / ( 2.0 * a * ( 1.0 - a ) ) )
		);
		float threshold = ( x < ( 1.0 - a ) )
			? ( ( x < a ) ? cases.x : cases.y )
			: cases.z;
		return clamp( threshold , 1.0e-6, 1.0 );
	}
#endif`,vd=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,xd=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,Ed=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,Sd=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,Td=`#ifdef USE_AOMAP
	float ambientOcclusion = ( texture2D( aoMap, vAoMapUv ).r - 1.0 ) * aoMapIntensity + 1.0;
	reflectedLight.indirectDiffuse *= ambientOcclusion;
	#if defined( USE_CLEARCOAT ) 
		clearcoatSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_SHEEN ) 
		sheenSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD )
		float dotNV = saturate( dot( geometryNormal, geometryViewDir ) );
		reflectedLight.indirectSpecular *= computeSpecularOcclusion( dotNV, ambientOcclusion, material.roughness );
	#endif
#endif`,Md=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,bd=`#ifdef USE_BATCHING
	#if ! defined( GL_ANGLE_multi_draw )
	#define gl_DrawID _gl_DrawID
	uniform int _gl_DrawID;
	#endif
	uniform highp sampler2D batchingTexture;
	uniform highp usampler2D batchingIdTexture;
	mat4 getBatchingMatrix( const in float i ) {
		int size = textureSize( batchingTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( batchingTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( batchingTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( batchingTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( batchingTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
	float getIndirectIndex( const in int i ) {
		int size = textureSize( batchingIdTexture, 0 ).x;
		int x = i % size;
		int y = i / size;
		return float( texelFetch( batchingIdTexture, ivec2( x, y ), 0 ).r );
	}
#endif
#ifdef USE_BATCHING_COLOR
	uniform sampler2D batchingColorTexture;
	vec3 getBatchingColor( const in float i ) {
		int size = textureSize( batchingColorTexture, 0 ).x;
		int j = int( i );
		int x = j % size;
		int y = j / size;
		return texelFetch( batchingColorTexture, ivec2( x, y ), 0 ).rgb;
	}
#endif`,Ad=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,Rd=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,wd=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,Cd=`float G_BlinnPhong_Implicit( ) {
	return 0.25;
}
float D_BlinnPhong( const in float shininess, const in float dotNH ) {
	return RECIPROCAL_PI * ( shininess * 0.5 + 1.0 ) * pow( dotNH, shininess );
}
vec3 BRDF_BlinnPhong( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in vec3 specularColor, const in float shininess ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( specularColor, 1.0, dotVH );
	float G = G_BlinnPhong_Implicit( );
	float D = D_BlinnPhong( shininess, dotNH );
	return F * ( G * D );
} // validated`,Id=`#ifdef USE_IRIDESCENCE
	const mat3 XYZ_TO_REC709 = mat3(
		 3.2404542, -0.9692660,  0.0556434,
		-1.5371385,  1.8760108, -0.2040259,
		-0.4985314,  0.0415560,  1.0572252
	);
	vec3 Fresnel0ToIor( vec3 fresnel0 ) {
		vec3 sqrtF0 = sqrt( fresnel0 );
		return ( vec3( 1.0 ) + sqrtF0 ) / ( vec3( 1.0 ) - sqrtF0 );
	}
	vec3 IorToFresnel0( vec3 transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - vec3( incidentIor ) ) / ( transmittedIor + vec3( incidentIor ) ) );
	}
	float IorToFresnel0( float transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - incidentIor ) / ( transmittedIor + incidentIor ));
	}
	vec3 evalSensitivity( float OPD, vec3 shift ) {
		float phase = 2.0 * PI * OPD * 1.0e-9;
		vec3 val = vec3( 5.4856e-13, 4.4201e-13, 5.2481e-13 );
		vec3 pos = vec3( 1.6810e+06, 1.7953e+06, 2.2084e+06 );
		vec3 var = vec3( 4.3278e+09, 9.3046e+09, 6.6121e+09 );
		vec3 xyz = val * sqrt( 2.0 * PI * var ) * cos( pos * phase + shift ) * exp( - pow2( phase ) * var );
		xyz.x += 9.7470e-14 * sqrt( 2.0 * PI * 4.5282e+09 ) * cos( 2.2399e+06 * phase + shift[ 0 ] ) * exp( - 4.5282e+09 * pow2( phase ) );
		xyz /= 1.0685e-7;
		vec3 rgb = XYZ_TO_REC709 * xyz;
		return rgb;
	}
	vec3 evalIridescence( float outsideIOR, float eta2, float cosTheta1, float thinFilmThickness, vec3 baseF0 ) {
		vec3 I;
		float iridescenceIOR = mix( outsideIOR, eta2, smoothstep( 0.0, 0.03, thinFilmThickness ) );
		float sinTheta2Sq = pow2( outsideIOR / iridescenceIOR ) * ( 1.0 - pow2( cosTheta1 ) );
		float cosTheta2Sq = 1.0 - sinTheta2Sq;
		if ( cosTheta2Sq < 0.0 ) {
			return vec3( 1.0 );
		}
		float cosTheta2 = sqrt( cosTheta2Sq );
		float R0 = IorToFresnel0( iridescenceIOR, outsideIOR );
		float R12 = F_Schlick( R0, 1.0, cosTheta1 );
		float T121 = 1.0 - R12;
		float phi12 = 0.0;
		if ( iridescenceIOR < outsideIOR ) phi12 = PI;
		float phi21 = PI - phi12;
		vec3 baseIOR = Fresnel0ToIor( clamp( baseF0, 0.0, 0.9999 ) );		vec3 R1 = IorToFresnel0( baseIOR, iridescenceIOR );
		vec3 R23 = F_Schlick( R1, 1.0, cosTheta2 );
		vec3 phi23 = vec3( 0.0 );
		if ( baseIOR[ 0 ] < iridescenceIOR ) phi23[ 0 ] = PI;
		if ( baseIOR[ 1 ] < iridescenceIOR ) phi23[ 1 ] = PI;
		if ( baseIOR[ 2 ] < iridescenceIOR ) phi23[ 2 ] = PI;
		float OPD = 2.0 * iridescenceIOR * thinFilmThickness * cosTheta2;
		vec3 phi = vec3( phi21 ) + phi23;
		vec3 R123 = clamp( R12 * R23, 1e-5, 0.9999 );
		vec3 r123 = sqrt( R123 );
		vec3 Rs = pow2( T121 ) * R23 / ( vec3( 1.0 ) - R123 );
		vec3 C0 = R12 + Rs;
		I = C0;
		vec3 Cm = Rs - T121;
		for ( int m = 1; m <= 2; ++ m ) {
			Cm *= r123;
			vec3 Sm = 2.0 * evalSensitivity( float( m ) * OPD, float( m ) * phi );
			I += Cm * Sm;
		}
		return max( I, vec3( 0.0 ) );
	}
#endif`,Pd=`#ifdef USE_BUMPMAP
	uniform sampler2D bumpMap;
	uniform float bumpScale;
	vec2 dHdxy_fwd() {
		vec2 dSTdx = dFdx( vBumpMapUv );
		vec2 dSTdy = dFdy( vBumpMapUv );
		float Hll = bumpScale * texture2D( bumpMap, vBumpMapUv ).x;
		float dBx = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdx ).x - Hll;
		float dBy = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdy ).x - Hll;
		return vec2( dBx, dBy );
	}
	vec3 perturbNormalArb( vec3 surf_pos, vec3 surf_norm, vec2 dHdxy, float faceDirection ) {
		vec3 vSigmaX = normalize( dFdx( surf_pos.xyz ) );
		vec3 vSigmaY = normalize( dFdy( surf_pos.xyz ) );
		vec3 vN = surf_norm;
		vec3 R1 = cross( vSigmaY, vN );
		vec3 R2 = cross( vN, vSigmaX );
		float fDet = dot( vSigmaX, R1 ) * faceDirection;
		vec3 vGrad = sign( fDet ) * ( dHdxy.x * R1 + dHdxy.y * R2 );
		return normalize( abs( fDet ) * surf_norm - vGrad );
	}
#endif`,Ld=`#if NUM_CLIPPING_PLANES > 0
	vec4 plane;
	#ifdef ALPHA_TO_COVERAGE
		float distanceToPlane, distanceGradient;
		float clipOpacity = 1.0;
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
			distanceGradient = fwidth( distanceToPlane ) / 2.0;
			clipOpacity *= smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			if ( clipOpacity == 0.0 ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			float unionClipOpacity = 1.0;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
				distanceGradient = fwidth( distanceToPlane ) / 2.0;
				unionClipOpacity *= 1.0 - smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			}
			#pragma unroll_loop_end
			clipOpacity *= 1.0 - unionClipOpacity;
		#endif
		diffuseColor.a *= clipOpacity;
		if ( diffuseColor.a == 0.0 ) discard;
	#else
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			if ( dot( vClipPosition, plane.xyz ) > plane.w ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			bool clipped = true;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				clipped = ( dot( vClipPosition, plane.xyz ) > plane.w ) && clipped;
			}
			#pragma unroll_loop_end
			if ( clipped ) discard;
		#endif
	#endif
#endif`,Nd=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,Od=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,Dd=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,Ud=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,Fd=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,kd=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,Bd=`#if defined( USE_COLOR_ALPHA )
	vColor = vec4( 1.0 );
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	vColor = vec3( 1.0 );
#endif
#ifdef USE_COLOR
	vColor *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.xyz *= instanceColor.xyz;
#endif
#ifdef USE_BATCHING_COLOR
	vec3 batchingColor = getBatchingColor( getIndirectIndex( gl_DrawID ) );
	vColor.xyz *= batchingColor.xyz;
#endif`,zd=`#define PI 3.141592653589793
#define PI2 6.283185307179586
#define PI_HALF 1.5707963267948966
#define RECIPROCAL_PI 0.3183098861837907
#define RECIPROCAL_PI2 0.15915494309189535
#define EPSILON 1e-6
#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
#define whiteComplement( a ) ( 1.0 - saturate( a ) )
float pow2( const in float x ) { return x*x; }
vec3 pow2( const in vec3 x ) { return x*x; }
float pow3( const in float x ) { return x*x*x; }
float pow4( const in float x ) { float x2 = x*x; return x2*x2; }
float max3( const in vec3 v ) { return max( max( v.x, v.y ), v.z ); }
float average( const in vec3 v ) { return dot( v, vec3( 0.3333333 ) ); }
highp float rand( const in vec2 uv ) {
	const highp float a = 12.9898, b = 78.233, c = 43758.5453;
	highp float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
	return fract( sin( sn ) * c );
}
#ifdef HIGH_PRECISION
	float precisionSafeLength( vec3 v ) { return length( v ); }
#else
	float precisionSafeLength( vec3 v ) {
		float maxComponent = max3( abs( v ) );
		return length( v / maxComponent ) * maxComponent;
	}
#endif
struct IncidentLight {
	vec3 color;
	vec3 direction;
	bool visible;
};
struct ReflectedLight {
	vec3 directDiffuse;
	vec3 directSpecular;
	vec3 indirectDiffuse;
	vec3 indirectSpecular;
};
#ifdef USE_ALPHAHASH
	varying vec3 vPosition;
#endif
vec3 transformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );
}
vec3 inverseTransformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( vec4( dir, 0.0 ) * matrix ).xyz );
}
mat3 transposeMat3( const in mat3 m ) {
	mat3 tmp;
	tmp[ 0 ] = vec3( m[ 0 ].x, m[ 1 ].x, m[ 2 ].x );
	tmp[ 1 ] = vec3( m[ 0 ].y, m[ 1 ].y, m[ 2 ].y );
	tmp[ 2 ] = vec3( m[ 0 ].z, m[ 1 ].z, m[ 2 ].z );
	return tmp;
}
bool isPerspectiveMatrix( mat4 m ) {
	return m[ 2 ][ 3 ] == - 1.0;
}
vec2 equirectUv( in vec3 dir ) {
	float u = atan( dir.z, dir.x ) * RECIPROCAL_PI2 + 0.5;
	float v = asin( clamp( dir.y, - 1.0, 1.0 ) ) * RECIPROCAL_PI + 0.5;
	return vec2( u, v );
}
vec3 BRDF_Lambert( const in vec3 diffuseColor ) {
	return RECIPROCAL_PI * diffuseColor;
}
vec3 F_Schlick( const in vec3 f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
}
float F_Schlick( const in float f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
} // validated`,Vd=`#ifdef ENVMAP_TYPE_CUBE_UV
	#define cubeUV_minMipLevel 4.0
	#define cubeUV_minTileSize 16.0
	float getFace( vec3 direction ) {
		vec3 absDirection = abs( direction );
		float face = - 1.0;
		if ( absDirection.x > absDirection.z ) {
			if ( absDirection.x > absDirection.y )
				face = direction.x > 0.0 ? 0.0 : 3.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		} else {
			if ( absDirection.z > absDirection.y )
				face = direction.z > 0.0 ? 2.0 : 5.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		}
		return face;
	}
	vec2 getUV( vec3 direction, float face ) {
		vec2 uv;
		if ( face == 0.0 ) {
			uv = vec2( direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 1.0 ) {
			uv = vec2( - direction.x, - direction.z ) / abs( direction.y );
		} else if ( face == 2.0 ) {
			uv = vec2( - direction.x, direction.y ) / abs( direction.z );
		} else if ( face == 3.0 ) {
			uv = vec2( - direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 4.0 ) {
			uv = vec2( - direction.x, direction.z ) / abs( direction.y );
		} else {
			uv = vec2( direction.x, direction.y ) / abs( direction.z );
		}
		return 0.5 * ( uv + 1.0 );
	}
	vec3 bilinearCubeUV( sampler2D envMap, vec3 direction, float mipInt ) {
		float face = getFace( direction );
		float filterInt = max( cubeUV_minMipLevel - mipInt, 0.0 );
		mipInt = max( mipInt, cubeUV_minMipLevel );
		float faceSize = exp2( mipInt );
		highp vec2 uv = getUV( direction, face ) * ( faceSize - 2.0 ) + 1.0;
		if ( face > 2.0 ) {
			uv.y += faceSize;
			face -= 3.0;
		}
		uv.x += face * faceSize;
		uv.x += filterInt * 3.0 * cubeUV_minTileSize;
		uv.y += 4.0 * ( exp2( CUBEUV_MAX_MIP ) - faceSize );
		uv.x *= CUBEUV_TEXEL_WIDTH;
		uv.y *= CUBEUV_TEXEL_HEIGHT;
		#ifdef texture2DGradEXT
			return texture2DGradEXT( envMap, uv, vec2( 0.0 ), vec2( 0.0 ) ).rgb;
		#else
			return texture2D( envMap, uv ).rgb;
		#endif
	}
	#define cubeUV_r0 1.0
	#define cubeUV_m0 - 2.0
	#define cubeUV_r1 0.8
	#define cubeUV_m1 - 1.0
	#define cubeUV_r4 0.4
	#define cubeUV_m4 2.0
	#define cubeUV_r5 0.305
	#define cubeUV_m5 3.0
	#define cubeUV_r6 0.21
	#define cubeUV_m6 4.0
	float roughnessToMip( float roughness ) {
		float mip = 0.0;
		if ( roughness >= cubeUV_r1 ) {
			mip = ( cubeUV_r0 - roughness ) * ( cubeUV_m1 - cubeUV_m0 ) / ( cubeUV_r0 - cubeUV_r1 ) + cubeUV_m0;
		} else if ( roughness >= cubeUV_r4 ) {
			mip = ( cubeUV_r1 - roughness ) * ( cubeUV_m4 - cubeUV_m1 ) / ( cubeUV_r1 - cubeUV_r4 ) + cubeUV_m1;
		} else if ( roughness >= cubeUV_r5 ) {
			mip = ( cubeUV_r4 - roughness ) * ( cubeUV_m5 - cubeUV_m4 ) / ( cubeUV_r4 - cubeUV_r5 ) + cubeUV_m4;
		} else if ( roughness >= cubeUV_r6 ) {
			mip = ( cubeUV_r5 - roughness ) * ( cubeUV_m6 - cubeUV_m5 ) / ( cubeUV_r5 - cubeUV_r6 ) + cubeUV_m5;
		} else {
			mip = - 2.0 * log2( 1.16 * roughness );		}
		return mip;
	}
	vec4 textureCubeUV( sampler2D envMap, vec3 sampleDir, float roughness ) {
		float mip = clamp( roughnessToMip( roughness ), cubeUV_m0, CUBEUV_MAX_MIP );
		float mipF = fract( mip );
		float mipInt = floor( mip );
		vec3 color0 = bilinearCubeUV( envMap, sampleDir, mipInt );
		if ( mipF == 0.0 ) {
			return vec4( color0, 1.0 );
		} else {
			vec3 color1 = bilinearCubeUV( envMap, sampleDir, mipInt + 1.0 );
			return vec4( mix( color0, color1, mipF ), 1.0 );
		}
	}
#endif`,Gd=`vec3 transformedNormal = objectNormal;
#ifdef USE_TANGENT
	vec3 transformedTangent = objectTangent;
#endif
#ifdef USE_BATCHING
	mat3 bm = mat3( batchingMatrix );
	transformedNormal /= vec3( dot( bm[ 0 ], bm[ 0 ] ), dot( bm[ 1 ], bm[ 1 ] ), dot( bm[ 2 ], bm[ 2 ] ) );
	transformedNormal = bm * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = bm * transformedTangent;
	#endif
#endif
#ifdef USE_INSTANCING
	mat3 im = mat3( instanceMatrix );
	transformedNormal /= vec3( dot( im[ 0 ], im[ 0 ] ), dot( im[ 1 ], im[ 1 ] ), dot( im[ 2 ], im[ 2 ] ) );
	transformedNormal = im * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = im * transformedTangent;
	#endif
#endif
transformedNormal = normalMatrix * transformedNormal;
#ifdef FLIP_SIDED
	transformedNormal = - transformedNormal;
#endif
#ifdef USE_TANGENT
	transformedTangent = ( modelViewMatrix * vec4( transformedTangent, 0.0 ) ).xyz;
	#ifdef FLIP_SIDED
		transformedTangent = - transformedTangent;
	#endif
#endif`,Hd=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,Wd=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,Xd=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,Yd=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,qd="gl_FragColor = linearToOutputTexel( gl_FragColor );",Kd=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,Zd=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vec3 cameraToFrag;
		if ( isOrthographic ) {
			cameraToFrag = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToFrag = normalize( vWorldPosition - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vec3 reflectVec = reflect( cameraToFrag, worldNormal );
		#else
			vec3 reflectVec = refract( cameraToFrag, worldNormal, refractionRatio );
		#endif
	#else
		vec3 reflectVec = vReflect;
	#endif
	#ifdef ENVMAP_TYPE_CUBE
		vec4 envColor = textureCube( envMap, envMapRotation * vec3( flipEnvMap * reflectVec.x, reflectVec.yz ) );
	#else
		vec4 envColor = vec4( 0.0 );
	#endif
	#ifdef ENVMAP_BLENDING_MULTIPLY
		outgoingLight = mix( outgoingLight, outgoingLight * envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_MIX )
		outgoingLight = mix( outgoingLight, envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_ADD )
		outgoingLight += envColor.xyz * specularStrength * reflectivity;
	#endif
#endif`,jd=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,Jd=`#ifdef USE_ENVMAP
	uniform float reflectivity;
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		varying vec3 vWorldPosition;
		uniform float refractionRatio;
	#else
		varying vec3 vReflect;
	#endif
#endif`,$d=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,Qd=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vWorldPosition = worldPosition.xyz;
	#else
		vec3 cameraToVertex;
		if ( isOrthographic ) {
			cameraToVertex = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToVertex = normalize( worldPosition.xyz - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vReflect = reflect( cameraToVertex, worldNormal );
		#else
			vReflect = refract( cameraToVertex, worldNormal, refractionRatio );
		#endif
	#endif
#endif`,ef=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,tf=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,nf=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,rf=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,sf=`#ifdef USE_GRADIENTMAP
	uniform sampler2D gradientMap;
#endif
vec3 getGradientIrradiance( vec3 normal, vec3 lightDirection ) {
	float dotNL = dot( normal, lightDirection );
	vec2 coord = vec2( dotNL * 0.5 + 0.5, 0.0 );
	#ifdef USE_GRADIENTMAP
		return vec3( texture2D( gradientMap, coord ).r );
	#else
		vec2 fw = fwidth( coord ) * 0.5;
		return mix( vec3( 0.7 ), vec3( 1.0 ), smoothstep( 0.7 - fw.x, 0.7 + fw.x, coord.x ) );
	#endif
}`,of=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,af=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,cf=`varying vec3 vViewPosition;
struct LambertMaterial {
	vec3 diffuseColor;
	float specularStrength;
};
void RE_Direct_Lambert( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Lambert( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Lambert
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,lf=`uniform bool receiveShadow;
uniform vec3 ambientLightColor;
#if defined( USE_LIGHT_PROBES )
	uniform vec3 lightProbe[ 9 ];
#endif
vec3 shGetIrradianceAt( in vec3 normal, in vec3 shCoefficients[ 9 ] ) {
	float x = normal.x, y = normal.y, z = normal.z;
	vec3 result = shCoefficients[ 0 ] * 0.886227;
	result += shCoefficients[ 1 ] * 2.0 * 0.511664 * y;
	result += shCoefficients[ 2 ] * 2.0 * 0.511664 * z;
	result += shCoefficients[ 3 ] * 2.0 * 0.511664 * x;
	result += shCoefficients[ 4 ] * 2.0 * 0.429043 * x * y;
	result += shCoefficients[ 5 ] * 2.0 * 0.429043 * y * z;
	result += shCoefficients[ 6 ] * ( 0.743125 * z * z - 0.247708 );
	result += shCoefficients[ 7 ] * 2.0 * 0.429043 * x * z;
	result += shCoefficients[ 8 ] * 0.429043 * ( x * x - y * y );
	return result;
}
vec3 getLightProbeIrradiance( const in vec3 lightProbe[ 9 ], const in vec3 normal ) {
	vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
	vec3 irradiance = shGetIrradianceAt( worldNormal, lightProbe );
	return irradiance;
}
vec3 getAmbientLightIrradiance( const in vec3 ambientLightColor ) {
	vec3 irradiance = ambientLightColor;
	return irradiance;
}
float getDistanceAttenuation( const in float lightDistance, const in float cutoffDistance, const in float decayExponent ) {
	float distanceFalloff = 1.0 / max( pow( lightDistance, decayExponent ), 0.01 );
	if ( cutoffDistance > 0.0 ) {
		distanceFalloff *= pow2( saturate( 1.0 - pow4( lightDistance / cutoffDistance ) ) );
	}
	return distanceFalloff;
}
float getSpotAttenuation( const in float coneCosine, const in float penumbraCosine, const in float angleCosine ) {
	return smoothstep( coneCosine, penumbraCosine, angleCosine );
}
#if NUM_DIR_LIGHTS > 0
	struct DirectionalLight {
		vec3 direction;
		vec3 color;
	};
	uniform DirectionalLight directionalLights[ NUM_DIR_LIGHTS ];
	void getDirectionalLightInfo( const in DirectionalLight directionalLight, out IncidentLight light ) {
		light.color = directionalLight.color;
		light.direction = directionalLight.direction;
		light.visible = true;
	}
#endif
#if NUM_POINT_LIGHTS > 0
	struct PointLight {
		vec3 position;
		vec3 color;
		float distance;
		float decay;
	};
	uniform PointLight pointLights[ NUM_POINT_LIGHTS ];
	void getPointLightInfo( const in PointLight pointLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = pointLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float lightDistance = length( lVector );
		light.color = pointLight.color;
		light.color *= getDistanceAttenuation( lightDistance, pointLight.distance, pointLight.decay );
		light.visible = ( light.color != vec3( 0.0 ) );
	}
#endif
#if NUM_SPOT_LIGHTS > 0
	struct SpotLight {
		vec3 position;
		vec3 direction;
		vec3 color;
		float distance;
		float decay;
		float coneCos;
		float penumbraCos;
	};
	uniform SpotLight spotLights[ NUM_SPOT_LIGHTS ];
	void getSpotLightInfo( const in SpotLight spotLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = spotLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float angleCos = dot( light.direction, spotLight.direction );
		float spotAttenuation = getSpotAttenuation( spotLight.coneCos, spotLight.penumbraCos, angleCos );
		if ( spotAttenuation > 0.0 ) {
			float lightDistance = length( lVector );
			light.color = spotLight.color * spotAttenuation;
			light.color *= getDistanceAttenuation( lightDistance, spotLight.distance, spotLight.decay );
			light.visible = ( light.color != vec3( 0.0 ) );
		} else {
			light.color = vec3( 0.0 );
			light.visible = false;
		}
	}
#endif
#if NUM_RECT_AREA_LIGHTS > 0
	struct RectAreaLight {
		vec3 color;
		vec3 position;
		vec3 halfWidth;
		vec3 halfHeight;
	};
	uniform sampler2D ltc_1;	uniform sampler2D ltc_2;
	uniform RectAreaLight rectAreaLights[ NUM_RECT_AREA_LIGHTS ];
#endif
#if NUM_HEMI_LIGHTS > 0
	struct HemisphereLight {
		vec3 direction;
		vec3 skyColor;
		vec3 groundColor;
	};
	uniform HemisphereLight hemisphereLights[ NUM_HEMI_LIGHTS ];
	vec3 getHemisphereLightIrradiance( const in HemisphereLight hemiLight, const in vec3 normal ) {
		float dotNL = dot( normal, hemiLight.direction );
		float hemiDiffuseWeight = 0.5 * dotNL + 0.5;
		vec3 irradiance = mix( hemiLight.groundColor, hemiLight.skyColor, hemiDiffuseWeight );
		return irradiance;
	}
#endif`,uf=`#ifdef USE_ENVMAP
	vec3 getIBLIrradiance( const in vec3 normal ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * worldNormal, 1.0 );
			return PI * envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	vec3 getIBLRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 reflectVec = reflect( - viewDir, normal );
			reflectVec = normalize( mix( reflectVec, normal, roughness * roughness) );
			reflectVec = inverseTransformDirection( reflectVec, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );
			return envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	#ifdef USE_ANISOTROPY
		vec3 getIBLAnisotropyRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 bentNormal = cross( bitangent, viewDir );
				bentNormal = normalize( cross( bentNormal, bitangent ) );
				bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
				return getIBLRadiance( viewDir, bentNormal, roughness );
			#else
				return vec3( 0.0 );
			#endif
		}
	#endif
#endif`,hf=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,df=`varying vec3 vViewPosition;
struct ToonMaterial {
	vec3 diffuseColor;
};
void RE_Direct_Toon( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 irradiance = getGradientIrradiance( geometryNormal, directLight.direction ) * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Toon( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Toon
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,ff=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,pf=`varying vec3 vViewPosition;
struct BlinnPhongMaterial {
	vec3 diffuseColor;
	vec3 specularColor;
	float specularShininess;
	float specularStrength;
};
void RE_Direct_BlinnPhong( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
	reflectedLight.directSpecular += irradiance * BRDF_BlinnPhong( directLight.direction, geometryViewDir, geometryNormal, material.specularColor, material.specularShininess ) * material.specularStrength;
}
void RE_IndirectDiffuse_BlinnPhong( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_BlinnPhong
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,mf=`PhysicalMaterial material;
material.diffuseColor = diffuseColor.rgb * ( 1.0 - metalnessFactor );
vec3 dxy = max( abs( dFdx( nonPerturbedNormal ) ), abs( dFdy( nonPerturbedNormal ) ) );
float geometryRoughness = max( max( dxy.x, dxy.y ), dxy.z );
material.roughness = max( roughnessFactor, 0.0525 );material.roughness += geometryRoughness;
material.roughness = min( material.roughness, 1.0 );
#ifdef IOR
	material.ior = ior;
	#ifdef USE_SPECULAR
		float specularIntensityFactor = specularIntensity;
		vec3 specularColorFactor = specularColor;
		#ifdef USE_SPECULAR_COLORMAP
			specularColorFactor *= texture2D( specularColorMap, vSpecularColorMapUv ).rgb;
		#endif
		#ifdef USE_SPECULAR_INTENSITYMAP
			specularIntensityFactor *= texture2D( specularIntensityMap, vSpecularIntensityMapUv ).a;
		#endif
		material.specularF90 = mix( specularIntensityFactor, 1.0, metalnessFactor );
	#else
		float specularIntensityFactor = 1.0;
		vec3 specularColorFactor = vec3( 1.0 );
		material.specularF90 = 1.0;
	#endif
	material.specularColor = mix( min( pow2( ( material.ior - 1.0 ) / ( material.ior + 1.0 ) ) * specularColorFactor, vec3( 1.0 ) ) * specularIntensityFactor, diffuseColor.rgb, metalnessFactor );
#else
	material.specularColor = mix( vec3( 0.04 ), diffuseColor.rgb, metalnessFactor );
	material.specularF90 = 1.0;
#endif
#ifdef USE_CLEARCOAT
	material.clearcoat = clearcoat;
	material.clearcoatRoughness = clearcoatRoughness;
	material.clearcoatF0 = vec3( 0.04 );
	material.clearcoatF90 = 1.0;
	#ifdef USE_CLEARCOATMAP
		material.clearcoat *= texture2D( clearcoatMap, vClearcoatMapUv ).x;
	#endif
	#ifdef USE_CLEARCOAT_ROUGHNESSMAP
		material.clearcoatRoughness *= texture2D( clearcoatRoughnessMap, vClearcoatRoughnessMapUv ).y;
	#endif
	material.clearcoat = saturate( material.clearcoat );	material.clearcoatRoughness = max( material.clearcoatRoughness, 0.0525 );
	material.clearcoatRoughness += geometryRoughness;
	material.clearcoatRoughness = min( material.clearcoatRoughness, 1.0 );
#endif
#ifdef USE_DISPERSION
	material.dispersion = dispersion;
#endif
#ifdef USE_IRIDESCENCE
	material.iridescence = iridescence;
	material.iridescenceIOR = iridescenceIOR;
	#ifdef USE_IRIDESCENCEMAP
		material.iridescence *= texture2D( iridescenceMap, vIridescenceMapUv ).r;
	#endif
	#ifdef USE_IRIDESCENCE_THICKNESSMAP
		material.iridescenceThickness = (iridescenceThicknessMaximum - iridescenceThicknessMinimum) * texture2D( iridescenceThicknessMap, vIridescenceThicknessMapUv ).g + iridescenceThicknessMinimum;
	#else
		material.iridescenceThickness = iridescenceThicknessMaximum;
	#endif
#endif
#ifdef USE_SHEEN
	material.sheenColor = sheenColor;
	#ifdef USE_SHEEN_COLORMAP
		material.sheenColor *= texture2D( sheenColorMap, vSheenColorMapUv ).rgb;
	#endif
	material.sheenRoughness = clamp( sheenRoughness, 0.07, 1.0 );
	#ifdef USE_SHEEN_ROUGHNESSMAP
		material.sheenRoughness *= texture2D( sheenRoughnessMap, vSheenRoughnessMapUv ).a;
	#endif
#endif
#ifdef USE_ANISOTROPY
	#ifdef USE_ANISOTROPYMAP
		mat2 anisotropyMat = mat2( anisotropyVector.x, anisotropyVector.y, - anisotropyVector.y, anisotropyVector.x );
		vec3 anisotropyPolar = texture2D( anisotropyMap, vAnisotropyMapUv ).rgb;
		vec2 anisotropyV = anisotropyMat * normalize( 2.0 * anisotropyPolar.rg - vec2( 1.0 ) ) * anisotropyPolar.b;
	#else
		vec2 anisotropyV = anisotropyVector;
	#endif
	material.anisotropy = length( anisotropyV );
	if( material.anisotropy == 0.0 ) {
		anisotropyV = vec2( 1.0, 0.0 );
	} else {
		anisotropyV /= material.anisotropy;
		material.anisotropy = saturate( material.anisotropy );
	}
	material.alphaT = mix( pow2( material.roughness ), 1.0, pow2( material.anisotropy ) );
	material.anisotropyT = tbn[ 0 ] * anisotropyV.x + tbn[ 1 ] * anisotropyV.y;
	material.anisotropyB = tbn[ 1 ] * anisotropyV.x - tbn[ 0 ] * anisotropyV.y;
#endif`,gf=`struct PhysicalMaterial {
	vec3 diffuseColor;
	float roughness;
	vec3 specularColor;
	float specularF90;
	float dispersion;
	#ifdef USE_CLEARCOAT
		float clearcoat;
		float clearcoatRoughness;
		vec3 clearcoatF0;
		float clearcoatF90;
	#endif
	#ifdef USE_IRIDESCENCE
		float iridescence;
		float iridescenceIOR;
		float iridescenceThickness;
		vec3 iridescenceFresnel;
		vec3 iridescenceF0;
	#endif
	#ifdef USE_SHEEN
		vec3 sheenColor;
		float sheenRoughness;
	#endif
	#ifdef IOR
		float ior;
	#endif
	#ifdef USE_TRANSMISSION
		float transmission;
		float transmissionAlpha;
		float thickness;
		float attenuationDistance;
		vec3 attenuationColor;
	#endif
	#ifdef USE_ANISOTROPY
		float anisotropy;
		float alphaT;
		vec3 anisotropyT;
		vec3 anisotropyB;
	#endif
};
vec3 clearcoatSpecularDirect = vec3( 0.0 );
vec3 clearcoatSpecularIndirect = vec3( 0.0 );
vec3 sheenSpecularDirect = vec3( 0.0 );
vec3 sheenSpecularIndirect = vec3(0.0 );
vec3 Schlick_to_F0( const in vec3 f, const in float f90, const in float dotVH ) {
    float x = clamp( 1.0 - dotVH, 0.0, 1.0 );
    float x2 = x * x;
    float x5 = clamp( x * x2 * x2, 0.0, 0.9999 );
    return ( f - vec3( f90 ) * x5 ) / ( 1.0 - x5 );
}
float V_GGX_SmithCorrelated( const in float alpha, const in float dotNL, const in float dotNV ) {
	float a2 = pow2( alpha );
	float gv = dotNL * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNV ) );
	float gl = dotNV * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNL ) );
	return 0.5 / max( gv + gl, EPSILON );
}
float D_GGX( const in float alpha, const in float dotNH ) {
	float a2 = pow2( alpha );
	float denom = pow2( dotNH ) * ( a2 - 1.0 ) + 1.0;
	return RECIPROCAL_PI * a2 / pow2( denom );
}
#ifdef USE_ANISOTROPY
	float V_GGX_SmithCorrelated_Anisotropic( const in float alphaT, const in float alphaB, const in float dotTV, const in float dotBV, const in float dotTL, const in float dotBL, const in float dotNV, const in float dotNL ) {
		float gv = dotNL * length( vec3( alphaT * dotTV, alphaB * dotBV, dotNV ) );
		float gl = dotNV * length( vec3( alphaT * dotTL, alphaB * dotBL, dotNL ) );
		float v = 0.5 / ( gv + gl );
		return saturate(v);
	}
	float D_GGX_Anisotropic( const in float alphaT, const in float alphaB, const in float dotNH, const in float dotTH, const in float dotBH ) {
		float a2 = alphaT * alphaB;
		highp vec3 v = vec3( alphaB * dotTH, alphaT * dotBH, a2 * dotNH );
		highp float v2 = dot( v, v );
		float w2 = a2 / v2;
		return RECIPROCAL_PI * a2 * pow2 ( w2 );
	}
#endif
#ifdef USE_CLEARCOAT
	vec3 BRDF_GGX_Clearcoat( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material) {
		vec3 f0 = material.clearcoatF0;
		float f90 = material.clearcoatF90;
		float roughness = material.clearcoatRoughness;
		float alpha = pow2( roughness );
		vec3 halfDir = normalize( lightDir + viewDir );
		float dotNL = saturate( dot( normal, lightDir ) );
		float dotNV = saturate( dot( normal, viewDir ) );
		float dotNH = saturate( dot( normal, halfDir ) );
		float dotVH = saturate( dot( viewDir, halfDir ) );
		vec3 F = F_Schlick( f0, f90, dotVH );
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
		return F * ( V * D );
	}
#endif
vec3 BRDF_GGX( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 f0 = material.specularColor;
	float f90 = material.specularF90;
	float roughness = material.roughness;
	float alpha = pow2( roughness );
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( f0, f90, dotVH );
	#ifdef USE_IRIDESCENCE
		F = mix( F, material.iridescenceFresnel, material.iridescence );
	#endif
	#ifdef USE_ANISOTROPY
		float dotTL = dot( material.anisotropyT, lightDir );
		float dotTV = dot( material.anisotropyT, viewDir );
		float dotTH = dot( material.anisotropyT, halfDir );
		float dotBL = dot( material.anisotropyB, lightDir );
		float dotBV = dot( material.anisotropyB, viewDir );
		float dotBH = dot( material.anisotropyB, halfDir );
		float V = V_GGX_SmithCorrelated_Anisotropic( material.alphaT, alpha, dotTV, dotBV, dotTL, dotBL, dotNV, dotNL );
		float D = D_GGX_Anisotropic( material.alphaT, alpha, dotNH, dotTH, dotBH );
	#else
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
	#endif
	return F * ( V * D );
}
vec2 LTC_Uv( const in vec3 N, const in vec3 V, const in float roughness ) {
	const float LUT_SIZE = 64.0;
	const float LUT_SCALE = ( LUT_SIZE - 1.0 ) / LUT_SIZE;
	const float LUT_BIAS = 0.5 / LUT_SIZE;
	float dotNV = saturate( dot( N, V ) );
	vec2 uv = vec2( roughness, sqrt( 1.0 - dotNV ) );
	uv = uv * LUT_SCALE + LUT_BIAS;
	return uv;
}
float LTC_ClippedSphereFormFactor( const in vec3 f ) {
	float l = length( f );
	return max( ( l * l + f.z ) / ( l + 1.0 ), 0.0 );
}
vec3 LTC_EdgeVectorFormFactor( const in vec3 v1, const in vec3 v2 ) {
	float x = dot( v1, v2 );
	float y = abs( x );
	float a = 0.8543985 + ( 0.4965155 + 0.0145206 * y ) * y;
	float b = 3.4175940 + ( 4.1616724 + y ) * y;
	float v = a / b;
	float theta_sintheta = ( x > 0.0 ) ? v : 0.5 * inversesqrt( max( 1.0 - x * x, 1e-7 ) ) - v;
	return cross( v1, v2 ) * theta_sintheta;
}
vec3 LTC_Evaluate( const in vec3 N, const in vec3 V, const in vec3 P, const in mat3 mInv, const in vec3 rectCoords[ 4 ] ) {
	vec3 v1 = rectCoords[ 1 ] - rectCoords[ 0 ];
	vec3 v2 = rectCoords[ 3 ] - rectCoords[ 0 ];
	vec3 lightNormal = cross( v1, v2 );
	if( dot( lightNormal, P - rectCoords[ 0 ] ) < 0.0 ) return vec3( 0.0 );
	vec3 T1, T2;
	T1 = normalize( V - N * dot( V, N ) );
	T2 = - cross( N, T1 );
	mat3 mat = mInv * transposeMat3( mat3( T1, T2, N ) );
	vec3 coords[ 4 ];
	coords[ 0 ] = mat * ( rectCoords[ 0 ] - P );
	coords[ 1 ] = mat * ( rectCoords[ 1 ] - P );
	coords[ 2 ] = mat * ( rectCoords[ 2 ] - P );
	coords[ 3 ] = mat * ( rectCoords[ 3 ] - P );
	coords[ 0 ] = normalize( coords[ 0 ] );
	coords[ 1 ] = normalize( coords[ 1 ] );
	coords[ 2 ] = normalize( coords[ 2 ] );
	coords[ 3 ] = normalize( coords[ 3 ] );
	vec3 vectorFormFactor = vec3( 0.0 );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 0 ], coords[ 1 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 1 ], coords[ 2 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 2 ], coords[ 3 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 3 ], coords[ 0 ] );
	float result = LTC_ClippedSphereFormFactor( vectorFormFactor );
	return vec3( result );
}
#if defined( USE_SHEEN )
float D_Charlie( float roughness, float dotNH ) {
	float alpha = pow2( roughness );
	float invAlpha = 1.0 / alpha;
	float cos2h = dotNH * dotNH;
	float sin2h = max( 1.0 - cos2h, 0.0078125 );
	return ( 2.0 + invAlpha ) * pow( sin2h, invAlpha * 0.5 ) / ( 2.0 * PI );
}
float V_Neubelt( float dotNV, float dotNL ) {
	return saturate( 1.0 / ( 4.0 * ( dotNL + dotNV - dotNL * dotNV ) ) );
}
vec3 BRDF_Sheen( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, vec3 sheenColor, const in float sheenRoughness ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float D = D_Charlie( sheenRoughness, dotNH );
	float V = V_Neubelt( dotNV, dotNL );
	return sheenColor * ( D * V );
}
#endif
float IBLSheenBRDF( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	float r2 = roughness * roughness;
	float a = roughness < 0.25 ? -339.2 * r2 + 161.4 * roughness - 25.9 : -8.48 * r2 + 14.3 * roughness - 9.95;
	float b = roughness < 0.25 ? 44.0 * r2 - 23.7 * roughness + 3.26 : 1.97 * r2 - 3.27 * roughness + 0.72;
	float DG = exp( a * dotNV + b ) + ( roughness < 0.25 ? 0.0 : 0.1 * ( roughness - 0.25 ) );
	return saturate( DG * RECIPROCAL_PI );
}
vec2 DFGApprox( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	const vec4 c0 = vec4( - 1, - 0.0275, - 0.572, 0.022 );
	const vec4 c1 = vec4( 1, 0.0425, 1.04, - 0.04 );
	vec4 r = roughness * c0 + c1;
	float a004 = min( r.x * r.x, exp2( - 9.28 * dotNV ) ) * r.x + r.y;
	vec2 fab = vec2( - 1.04, 1.04 ) * a004 + r.zw;
	return fab;
}
vec3 EnvironmentBRDF( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness ) {
	vec2 fab = DFGApprox( normal, viewDir, roughness );
	return specularColor * fab.x + specularF90 * fab.y;
}
#ifdef USE_IRIDESCENCE
void computeMultiscatteringIridescence( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float iridescence, const in vec3 iridescenceF0, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#else
void computeMultiscattering( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#endif
	vec2 fab = DFGApprox( normal, viewDir, roughness );
	#ifdef USE_IRIDESCENCE
		vec3 Fr = mix( specularColor, iridescenceF0, iridescence );
	#else
		vec3 Fr = specularColor;
	#endif
	vec3 FssEss = Fr * fab.x + specularF90 * fab.y;
	float Ess = fab.x + fab.y;
	float Ems = 1.0 - Ess;
	vec3 Favg = Fr + ( 1.0 - Fr ) * 0.047619;	vec3 Fms = FssEss * Favg / ( 1.0 - Ems * Favg );
	singleScatter += FssEss;
	multiScatter += Fms * Ems;
}
#if NUM_RECT_AREA_LIGHTS > 0
	void RE_Direct_RectArea_Physical( const in RectAreaLight rectAreaLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
		vec3 normal = geometryNormal;
		vec3 viewDir = geometryViewDir;
		vec3 position = geometryPosition;
		vec3 lightPos = rectAreaLight.position;
		vec3 halfWidth = rectAreaLight.halfWidth;
		vec3 halfHeight = rectAreaLight.halfHeight;
		vec3 lightColor = rectAreaLight.color;
		float roughness = material.roughness;
		vec3 rectCoords[ 4 ];
		rectCoords[ 0 ] = lightPos + halfWidth - halfHeight;		rectCoords[ 1 ] = lightPos - halfWidth - halfHeight;
		rectCoords[ 2 ] = lightPos - halfWidth + halfHeight;
		rectCoords[ 3 ] = lightPos + halfWidth + halfHeight;
		vec2 uv = LTC_Uv( normal, viewDir, roughness );
		vec4 t1 = texture2D( ltc_1, uv );
		vec4 t2 = texture2D( ltc_2, uv );
		mat3 mInv = mat3(
			vec3( t1.x, 0, t1.y ),
			vec3(    0, 1,    0 ),
			vec3( t1.z, 0, t1.w )
		);
		vec3 fresnel = ( material.specularColor * t2.x + ( vec3( 1.0 ) - material.specularColor ) * t2.y );
		reflectedLight.directSpecular += lightColor * fresnel * LTC_Evaluate( normal, viewDir, position, mInv, rectCoords );
		reflectedLight.directDiffuse += lightColor * material.diffuseColor * LTC_Evaluate( normal, viewDir, position, mat3( 1.0 ), rectCoords );
	}
#endif
void RE_Direct_Physical( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	#ifdef USE_CLEARCOAT
		float dotNLcc = saturate( dot( geometryClearcoatNormal, directLight.direction ) );
		vec3 ccIrradiance = dotNLcc * directLight.color;
		clearcoatSpecularDirect += ccIrradiance * BRDF_GGX_Clearcoat( directLight.direction, geometryViewDir, geometryClearcoatNormal, material );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularDirect += irradiance * BRDF_Sheen( directLight.direction, geometryViewDir, geometryNormal, material.sheenColor, material.sheenRoughness );
	#endif
	reflectedLight.directSpecular += irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Physical( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectSpecular_Physical( const in vec3 radiance, const in vec3 irradiance, const in vec3 clearcoatRadiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight) {
	#ifdef USE_CLEARCOAT
		clearcoatSpecularIndirect += clearcoatRadiance * EnvironmentBRDF( geometryClearcoatNormal, geometryViewDir, material.clearcoatF0, material.clearcoatF90, material.clearcoatRoughness );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularIndirect += irradiance * material.sheenColor * IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
	#endif
	vec3 singleScattering = vec3( 0.0 );
	vec3 multiScattering = vec3( 0.0 );
	vec3 cosineWeightedIrradiance = irradiance * RECIPROCAL_PI;
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.iridescence, material.iridescenceFresnel, material.roughness, singleScattering, multiScattering );
	#else
		computeMultiscattering( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.roughness, singleScattering, multiScattering );
	#endif
	vec3 totalScattering = singleScattering + multiScattering;
	vec3 diffuse = material.diffuseColor * ( 1.0 - max( max( totalScattering.r, totalScattering.g ), totalScattering.b ) );
	reflectedLight.indirectSpecular += radiance * singleScattering;
	reflectedLight.indirectSpecular += multiScattering * cosineWeightedIrradiance;
	reflectedLight.indirectDiffuse += diffuse * cosineWeightedIrradiance;
}
#define RE_Direct				RE_Direct_Physical
#define RE_Direct_RectArea		RE_Direct_RectArea_Physical
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Physical
#define RE_IndirectSpecular		RE_IndirectSpecular_Physical
float computeSpecularOcclusion( const in float dotNV, const in float ambientOcclusion, const in float roughness ) {
	return saturate( pow( dotNV + ambientOcclusion, exp2( - 16.0 * roughness - 1.0 ) ) - 1.0 + ambientOcclusion );
}`,_f=`
vec3 geometryPosition = - vViewPosition;
vec3 geometryNormal = normal;
vec3 geometryViewDir = ( isOrthographic ) ? vec3( 0, 0, 1 ) : normalize( vViewPosition );
vec3 geometryClearcoatNormal = vec3( 0.0 );
#ifdef USE_CLEARCOAT
	geometryClearcoatNormal = clearcoatNormal;
#endif
#ifdef USE_IRIDESCENCE
	float dotNVi = saturate( dot( normal, geometryViewDir ) );
	if ( material.iridescenceThickness == 0.0 ) {
		material.iridescence = 0.0;
	} else {
		material.iridescence = saturate( material.iridescence );
	}
	if ( material.iridescence > 0.0 ) {
		material.iridescenceFresnel = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.specularColor );
		material.iridescenceF0 = Schlick_to_F0( material.iridescenceFresnel, 1.0, dotNVi );
	}
#endif
IncidentLight directLight;
#if ( NUM_POINT_LIGHTS > 0 ) && defined( RE_Direct )
	PointLight pointLight;
	#if defined( USE_SHADOWMAP ) && NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHTS; i ++ ) {
		pointLight = pointLights[ i ];
		getPointLightInfo( pointLight, geometryPosition, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_POINT_LIGHT_SHADOWS )
		pointLightShadow = pointLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getPointShadow( pointShadowMap[ i ], pointLightShadow.shadowMapSize, pointLightShadow.shadowIntensity, pointLightShadow.shadowBias, pointLightShadow.shadowRadius, vPointShadowCoord[ i ], pointLightShadow.shadowCameraNear, pointLightShadow.shadowCameraFar ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SPOT_LIGHTS > 0 ) && defined( RE_Direct )
	SpotLight spotLight;
	vec4 spotColor;
	vec3 spotLightCoord;
	bool inSpotLightMap;
	#if defined( USE_SHADOWMAP ) && NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHTS; i ++ ) {
		spotLight = spotLights[ i ];
		getSpotLightInfo( spotLight, geometryPosition, directLight );
		#if ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#define SPOT_LIGHT_MAP_INDEX UNROLLED_LOOP_INDEX
		#elif ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		#define SPOT_LIGHT_MAP_INDEX NUM_SPOT_LIGHT_MAPS
		#else
		#define SPOT_LIGHT_MAP_INDEX ( UNROLLED_LOOP_INDEX - NUM_SPOT_LIGHT_SHADOWS + NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#endif
		#if ( SPOT_LIGHT_MAP_INDEX < NUM_SPOT_LIGHT_MAPS )
			spotLightCoord = vSpotLightCoord[ i ].xyz / vSpotLightCoord[ i ].w;
			inSpotLightMap = all( lessThan( abs( spotLightCoord * 2. - 1. ), vec3( 1.0 ) ) );
			spotColor = texture2D( spotLightMap[ SPOT_LIGHT_MAP_INDEX ], spotLightCoord.xy );
			directLight.color = inSpotLightMap ? directLight.color * spotColor.rgb : directLight.color;
		#endif
		#undef SPOT_LIGHT_MAP_INDEX
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		spotLightShadow = spotLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( spotShadowMap[ i ], spotLightShadow.shadowMapSize, spotLightShadow.shadowIntensity, spotLightShadow.shadowBias, spotLightShadow.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_DIR_LIGHTS > 0 ) && defined( RE_Direct )
	DirectionalLight directionalLight;
	#if defined( USE_SHADOWMAP ) && NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHTS; i ++ ) {
		directionalLight = directionalLights[ i ];
		getDirectionalLightInfo( directionalLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_DIR_LIGHT_SHADOWS )
		directionalLightShadow = directionalLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowIntensity, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_RECT_AREA_LIGHTS > 0 ) && defined( RE_Direct_RectArea )
	RectAreaLight rectAreaLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_RECT_AREA_LIGHTS; i ++ ) {
		rectAreaLight = rectAreaLights[ i ];
		RE_Direct_RectArea( rectAreaLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if defined( RE_IndirectDiffuse )
	vec3 iblIrradiance = vec3( 0.0 );
	vec3 irradiance = getAmbientLightIrradiance( ambientLightColor );
	#if defined( USE_LIGHT_PROBES )
		irradiance += getLightProbeIrradiance( lightProbe, geometryNormal );
	#endif
	#if ( NUM_HEMI_LIGHTS > 0 )
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_HEMI_LIGHTS; i ++ ) {
			irradiance += getHemisphereLightIrradiance( hemisphereLights[ i ], geometryNormal );
		}
		#pragma unroll_loop_end
	#endif
#endif
#if defined( RE_IndirectSpecular )
	vec3 radiance = vec3( 0.0 );
	vec3 clearcoatRadiance = vec3( 0.0 );
#endif`,yf=`#if defined( RE_IndirectDiffuse )
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
		irradiance += lightMapIrradiance;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD ) && defined( ENVMAP_TYPE_CUBE_UV )
		iblIrradiance += getIBLIrradiance( geometryNormal );
	#endif
#endif
#if defined( USE_ENVMAP ) && defined( RE_IndirectSpecular )
	#ifdef USE_ANISOTROPY
		radiance += getIBLAnisotropyRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
	#else
		radiance += getIBLRadiance( geometryViewDir, geometryNormal, material.roughness );
	#endif
	#ifdef USE_CLEARCOAT
		clearcoatRadiance += getIBLRadiance( geometryViewDir, geometryClearcoatNormal, material.clearcoatRoughness );
	#endif
#endif`,vf=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,xf=`#if defined( USE_LOGDEPTHBUF )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,Ef=`#if defined( USE_LOGDEPTHBUF )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Sf=`#ifdef USE_LOGDEPTHBUF
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Tf=`#ifdef USE_LOGDEPTHBUF
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,Mf=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,bf=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,Af=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
	#if defined( USE_POINTS_UV )
		vec2 uv = vUv;
	#else
		vec2 uv = ( uvTransform * vec3( gl_PointCoord.x, 1.0 - gl_PointCoord.y, 1 ) ).xy;
	#endif
#endif
#ifdef USE_MAP
	diffuseColor *= texture2D( map, uv );
#endif
#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, uv ).g;
#endif`,Rf=`#if defined( USE_POINTS_UV )
	varying vec2 vUv;
#else
	#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
		uniform mat3 uvTransform;
	#endif
#endif
#ifdef USE_MAP
	uniform sampler2D map;
#endif
#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,wf=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,Cf=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,If=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,Pf=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,Lf=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Nf=`#ifdef USE_MORPHTARGETS
	#ifndef USE_INSTANCING_MORPH
		uniform float morphTargetBaseInfluence;
		uniform float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	#endif
	uniform sampler2DArray morphTargetsTexture;
	uniform ivec2 morphTargetsTextureSize;
	vec4 getMorph( const in int vertexIndex, const in int morphTargetIndex, const in int offset ) {
		int texelIndex = vertexIndex * MORPHTARGETS_TEXTURE_STRIDE + offset;
		int y = texelIndex / morphTargetsTextureSize.x;
		int x = texelIndex - y * morphTargetsTextureSize.x;
		ivec3 morphUV = ivec3( x, y, morphTargetIndex );
		return texelFetch( morphTargetsTexture, morphUV, 0 );
	}
#endif`,Of=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Df=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
#ifdef FLAT_SHADED
	vec3 fdx = dFdx( vViewPosition );
	vec3 fdy = dFdy( vViewPosition );
	vec3 normal = normalize( cross( fdx, fdy ) );
#else
	vec3 normal = normalize( vNormal );
	#ifdef DOUBLE_SIDED
		normal *= faceDirection;
	#endif
#endif
#if defined( USE_NORMALMAP_TANGENTSPACE ) || defined( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY )
	#ifdef USE_TANGENT
		mat3 tbn = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn = getTangentFrame( - vViewPosition, normal,
		#if defined( USE_NORMALMAP )
			vNormalMapUv
		#elif defined( USE_CLEARCOAT_NORMALMAP )
			vClearcoatNormalMapUv
		#else
			vUv
		#endif
		);
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn[0] *= faceDirection;
		tbn[1] *= faceDirection;
	#endif
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	#ifdef USE_TANGENT
		mat3 tbn2 = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn2 = getTangentFrame( - vViewPosition, normal, vClearcoatNormalMapUv );
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn2[0] *= faceDirection;
		tbn2[1] *= faceDirection;
	#endif
#endif
vec3 nonPerturbedNormal = normal;`,Uf=`#ifdef USE_NORMALMAP_OBJECTSPACE
	normal = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#ifdef FLIP_SIDED
		normal = - normal;
	#endif
	#ifdef DOUBLE_SIDED
		normal = normal * faceDirection;
	#endif
	normal = normalize( normalMatrix * normal );
#elif defined( USE_NORMALMAP_TANGENTSPACE )
	vec3 mapN = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	mapN.xy *= normalScale;
	normal = normalize( tbn * mapN );
#elif defined( USE_BUMPMAP )
	normal = perturbNormalArb( - vViewPosition, normal, dHdxy_fwd(), faceDirection );
#endif`,Ff=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,kf=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Bf=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,zf=`#ifdef USE_NORMALMAP
	uniform sampler2D normalMap;
	uniform vec2 normalScale;
#endif
#ifdef USE_NORMALMAP_OBJECTSPACE
	uniform mat3 normalMatrix;
#endif
#if ! defined ( USE_TANGENT ) && ( defined ( USE_NORMALMAP_TANGENTSPACE ) || defined ( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY ) )
	mat3 getTangentFrame( vec3 eye_pos, vec3 surf_norm, vec2 uv ) {
		vec3 q0 = dFdx( eye_pos.xyz );
		vec3 q1 = dFdy( eye_pos.xyz );
		vec2 st0 = dFdx( uv.st );
		vec2 st1 = dFdy( uv.st );
		vec3 N = surf_norm;
		vec3 q1perp = cross( q1, N );
		vec3 q0perp = cross( N, q0 );
		vec3 T = q1perp * st0.x + q0perp * st1.x;
		vec3 B = q1perp * st0.y + q0perp * st1.y;
		float det = max( dot( T, T ), dot( B, B ) );
		float scale = ( det == 0.0 ) ? 0.0 : inversesqrt( det );
		return mat3( T * scale, B * scale, N );
	}
#endif`,Vf=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,Gf=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,Hf=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,Wf=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,Xf=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,Yf=`vec3 packNormalToRGB( const in vec3 normal ) {
	return normalize( normal ) * 0.5 + 0.5;
}
vec3 unpackRGBToNormal( const in vec3 rgb ) {
	return 2.0 * rgb.xyz - 1.0;
}
const float PackUpscale = 256. / 255.;const float UnpackDownscale = 255. / 256.;const float ShiftRight8 = 1. / 256.;
const float Inv255 = 1. / 255.;
const vec4 PackFactors = vec4( 1.0, 256.0, 256.0 * 256.0, 256.0 * 256.0 * 256.0 );
const vec2 UnpackFactors2 = vec2( UnpackDownscale, 1.0 / PackFactors.g );
const vec3 UnpackFactors3 = vec3( UnpackDownscale / PackFactors.rg, 1.0 / PackFactors.b );
const vec4 UnpackFactors4 = vec4( UnpackDownscale / PackFactors.rgb, 1.0 / PackFactors.a );
vec4 packDepthToRGBA( const in float v ) {
	if( v <= 0.0 )
		return vec4( 0., 0., 0., 0. );
	if( v >= 1.0 )
		return vec4( 1., 1., 1., 1. );
	float vuf;
	float af = modf( v * PackFactors.a, vuf );
	float bf = modf( vuf * ShiftRight8, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec4( vuf * Inv255, gf * PackUpscale, bf * PackUpscale, af );
}
vec3 packDepthToRGB( const in float v ) {
	if( v <= 0.0 )
		return vec3( 0., 0., 0. );
	if( v >= 1.0 )
		return vec3( 1., 1., 1. );
	float vuf;
	float bf = modf( v * PackFactors.b, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec3( vuf * Inv255, gf * PackUpscale, bf );
}
vec2 packDepthToRG( const in float v ) {
	if( v <= 0.0 )
		return vec2( 0., 0. );
	if( v >= 1.0 )
		return vec2( 1., 1. );
	float vuf;
	float gf = modf( v * 256., vuf );
	return vec2( vuf * Inv255, gf );
}
float unpackRGBAToDepth( const in vec4 v ) {
	return dot( v, UnpackFactors4 );
}
float unpackRGBToDepth( const in vec3 v ) {
	return dot( v, UnpackFactors3 );
}
float unpackRGToDepth( const in vec2 v ) {
	return v.r * UnpackFactors2.r + v.g * UnpackFactors2.g;
}
vec4 pack2HalfToRGBA( const in vec2 v ) {
	vec4 r = vec4( v.x, fract( v.x * 255.0 ), v.y, fract( v.y * 255.0 ) );
	return vec4( r.x - r.y / 255.0, r.y, r.z - r.w / 255.0, r.w );
}
vec2 unpackRGBATo2Half( const in vec4 v ) {
	return vec2( v.x + ( v.y / 255.0 ), v.z + ( v.w / 255.0 ) );
}
float viewZToOrthographicDepth( const in float viewZ, const in float near, const in float far ) {
	return ( viewZ + near ) / ( near - far );
}
float orthographicDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return depth * ( near - far ) - near;
}
float viewZToPerspectiveDepth( const in float viewZ, const in float near, const in float far ) {
	return ( ( near + viewZ ) * far ) / ( ( far - near ) * viewZ );
}
float perspectiveDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return ( near * far ) / ( ( far - near ) * depth - far );
}`,qf=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,Kf=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,Zf=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,jf=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,Jf=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,$f=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,Qf=`#if NUM_SPOT_LIGHT_COORDS > 0
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#if NUM_SPOT_LIGHT_MAPS > 0
	uniform sampler2D spotLightMap[ NUM_SPOT_LIGHT_MAPS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform sampler2D directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		uniform sampler2D spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform sampler2D pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
	float texture2DCompare( sampler2D depths, vec2 uv, float compare ) {
		float depth = unpackRGBAToDepth( texture2D( depths, uv ) );
		#ifdef USE_REVERSEDEPTHBUF
			return step( depth, compare );
		#else
			return step( compare, depth );
		#endif
	}
	vec2 texture2DDistribution( sampler2D shadow, vec2 uv ) {
		return unpackRGBATo2Half( texture2D( shadow, uv ) );
	}
	float VSMShadow (sampler2D shadow, vec2 uv, float compare ){
		float occlusion = 1.0;
		vec2 distribution = texture2DDistribution( shadow, uv );
		#ifdef USE_REVERSEDEPTHBUF
			float hard_shadow = step( distribution.x, compare );
		#else
			float hard_shadow = step( compare , distribution.x );
		#endif
		if (hard_shadow != 1.0 ) {
			float distance = compare - distribution.x ;
			float variance = max( 0.00000, distribution.y * distribution.y );
			float softness_probability = variance / (variance + distance * distance );			softness_probability = clamp( ( softness_probability - 0.3 ) / ( 0.95 - 0.3 ), 0.0, 1.0 );			occlusion = clamp( max( hard_shadow, softness_probability ), 0.0, 1.0 );
		}
		return occlusion;
	}
	float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
		float shadow = 1.0;
		shadowCoord.xyz /= shadowCoord.w;
		shadowCoord.z += shadowBias;
		bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
		bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
		if ( frustumTest ) {
		#if defined( SHADOWMAP_TYPE_PCF )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx0 = - texelSize.x * shadowRadius;
			float dy0 = - texelSize.y * shadowRadius;
			float dx1 = + texelSize.x * shadowRadius;
			float dy1 = + texelSize.y * shadowRadius;
			float dx2 = dx0 / 2.0;
			float dy2 = dy0 / 2.0;
			float dx3 = dx1 / 2.0;
			float dy3 = dy1 / 2.0;
			shadow = (
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy1 ), shadowCoord.z )
			) * ( 1.0 / 17.0 );
		#elif defined( SHADOWMAP_TYPE_PCF_SOFT )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx = texelSize.x;
			float dy = texelSize.y;
			vec2 uv = shadowCoord.xy;
			vec2 f = fract( uv * shadowMapSize + 0.5 );
			uv -= f * texelSize;
			shadow = (
				texture2DCompare( shadowMap, uv, shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( dx, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( 0.0, dy ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + texelSize, shadowCoord.z ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, 0.0 ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 0.0 ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, dy ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( 0.0, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 0.0, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( texture2DCompare( shadowMap, uv + vec2( dx, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( dx, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( mix( texture2DCompare( shadowMap, uv + vec2( -dx, -dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, -dy ), shadowCoord.z ),
						  f.x ),
					 mix( texture2DCompare( shadowMap, uv + vec2( -dx, 2.0 * dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 2.0 * dy ), shadowCoord.z ),
						  f.x ),
					 f.y )
			) * ( 1.0 / 9.0 );
		#elif defined( SHADOWMAP_TYPE_VSM )
			shadow = VSMShadow( shadowMap, shadowCoord.xy, shadowCoord.z );
		#else
			shadow = texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z );
		#endif
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	vec2 cubeToUV( vec3 v, float texelSizeY ) {
		vec3 absV = abs( v );
		float scaleToCube = 1.0 / max( absV.x, max( absV.y, absV.z ) );
		absV *= scaleToCube;
		v *= scaleToCube * ( 1.0 - 2.0 * texelSizeY );
		vec2 planar = v.xy;
		float almostATexel = 1.5 * texelSizeY;
		float almostOne = 1.0 - almostATexel;
		if ( absV.z >= almostOne ) {
			if ( v.z > 0.0 )
				planar.x = 4.0 - v.x;
		} else if ( absV.x >= almostOne ) {
			float signX = sign( v.x );
			planar.x = v.z * signX + 2.0 * signX;
		} else if ( absV.y >= almostOne ) {
			float signY = sign( v.y );
			planar.x = v.x + 2.0 * signY + 2.0;
			planar.y = v.z * signY - 2.0;
		}
		return vec2( 0.125, 0.25 ) * planar + vec2( 0.375, 0.75 );
	}
	float getPointShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		
		float lightToPositionLength = length( lightToPosition );
		if ( lightToPositionLength - shadowCameraFar <= 0.0 && lightToPositionLength - shadowCameraNear >= 0.0 ) {
			float dp = ( lightToPositionLength - shadowCameraNear ) / ( shadowCameraFar - shadowCameraNear );			dp += shadowBias;
			vec3 bd3D = normalize( lightToPosition );
			vec2 texelSize = vec2( 1.0 ) / ( shadowMapSize * vec2( 4.0, 2.0 ) );
			#if defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_PCF_SOFT ) || defined( SHADOWMAP_TYPE_VSM )
				vec2 offset = vec2( - 1, 1 ) * shadowRadius * texelSize.y;
				shadow = (
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxx, texelSize.y ), dp )
				) * ( 1.0 / 9.0 );
			#else
				shadow = texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp );
			#endif
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
#endif`,ep=`#if NUM_SPOT_LIGHT_COORDS > 0
	uniform mat4 spotLightMatrix[ NUM_SPOT_LIGHT_COORDS ];
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform mat4 directionalShadowMatrix[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform mat4 pointShadowMatrix[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
#endif`,tp=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
	vec3 shadowWorldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
	vec4 shadowWorldPosition;
#endif
#if defined( USE_SHADOWMAP )
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * directionalLightShadows[ i ].shadowNormalBias, 0 );
			vDirectionalShadowCoord[ i ] = directionalShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * pointLightShadows[ i ].shadowNormalBias, 0 );
			vPointShadowCoord[ i ] = pointShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
#endif
#if NUM_SPOT_LIGHT_COORDS > 0
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_COORDS; i ++ ) {
		shadowWorldPosition = worldPosition;
		#if ( defined( USE_SHADOWMAP ) && UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
			shadowWorldPosition.xyz += shadowWorldNormal * spotLightShadows[ i ].shadowNormalBias;
		#endif
		vSpotLightCoord[ i ] = spotLightMatrix[ i ] * shadowWorldPosition;
	}
	#pragma unroll_loop_end
#endif`,np=`float getShadowMask() {
	float shadow = 1.0;
	#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
		directionalLight = directionalLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( directionalShadowMap[ i ], directionalLight.shadowMapSize, directionalLight.shadowIntensity, directionalLight.shadowBias, directionalLight.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_SHADOWS; i ++ ) {
		spotLight = spotLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( spotShadowMap[ i ], spotLight.shadowMapSize, spotLight.shadowIntensity, spotLight.shadowBias, spotLight.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
		pointLight = pointLightShadows[ i ];
		shadow *= receiveShadow ? getPointShadow( pointShadowMap[ i ], pointLight.shadowMapSize, pointLight.shadowIntensity, pointLight.shadowBias, pointLight.shadowRadius, vPointShadowCoord[ i ], pointLight.shadowCameraNear, pointLight.shadowCameraFar ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#endif
	return shadow;
}`,ip=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,rp=`#ifdef USE_SKINNING
	uniform mat4 bindMatrix;
	uniform mat4 bindMatrixInverse;
	uniform highp sampler2D boneTexture;
	mat4 getBoneMatrix( const in float i ) {
		int size = textureSize( boneTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( boneTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( boneTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( boneTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( boneTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
#endif`,sp=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,op=`#ifdef USE_SKINNING
	mat4 skinMatrix = mat4( 0.0 );
	skinMatrix += skinWeight.x * boneMatX;
	skinMatrix += skinWeight.y * boneMatY;
	skinMatrix += skinWeight.z * boneMatZ;
	skinMatrix += skinWeight.w * boneMatW;
	skinMatrix = bindMatrixInverse * skinMatrix * bindMatrix;
	objectNormal = vec4( skinMatrix * vec4( objectNormal, 0.0 ) ).xyz;
	#ifdef USE_TANGENT
		objectTangent = vec4( skinMatrix * vec4( objectTangent, 0.0 ) ).xyz;
	#endif
#endif`,ap=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,cp=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,lp=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,up=`#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
uniform float toneMappingExposure;
vec3 LinearToneMapping( vec3 color ) {
	return saturate( toneMappingExposure * color );
}
vec3 ReinhardToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	return saturate( color / ( vec3( 1.0 ) + color ) );
}
vec3 CineonToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	color = max( vec3( 0.0 ), color - 0.004 );
	return pow( ( color * ( 6.2 * color + 0.5 ) ) / ( color * ( 6.2 * color + 1.7 ) + 0.06 ), vec3( 2.2 ) );
}
vec3 RRTAndODTFit( vec3 v ) {
	vec3 a = v * ( v + 0.0245786 ) - 0.000090537;
	vec3 b = v * ( 0.983729 * v + 0.4329510 ) + 0.238081;
	return a / b;
}
vec3 ACESFilmicToneMapping( vec3 color ) {
	const mat3 ACESInputMat = mat3(
		vec3( 0.59719, 0.07600, 0.02840 ),		vec3( 0.35458, 0.90834, 0.13383 ),
		vec3( 0.04823, 0.01566, 0.83777 )
	);
	const mat3 ACESOutputMat = mat3(
		vec3(  1.60475, -0.10208, -0.00327 ),		vec3( -0.53108,  1.10813, -0.07276 ),
		vec3( -0.07367, -0.00605,  1.07602 )
	);
	color *= toneMappingExposure / 0.6;
	color = ACESInputMat * color;
	color = RRTAndODTFit( color );
	color = ACESOutputMat * color;
	return saturate( color );
}
const mat3 LINEAR_REC2020_TO_LINEAR_SRGB = mat3(
	vec3( 1.6605, - 0.1246, - 0.0182 ),
	vec3( - 0.5876, 1.1329, - 0.1006 ),
	vec3( - 0.0728, - 0.0083, 1.1187 )
);
const mat3 LINEAR_SRGB_TO_LINEAR_REC2020 = mat3(
	vec3( 0.6274, 0.0691, 0.0164 ),
	vec3( 0.3293, 0.9195, 0.0880 ),
	vec3( 0.0433, 0.0113, 0.8956 )
);
vec3 agxDefaultContrastApprox( vec3 x ) {
	vec3 x2 = x * x;
	vec3 x4 = x2 * x2;
	return + 15.5 * x4 * x2
		- 40.14 * x4 * x
		+ 31.96 * x4
		- 6.868 * x2 * x
		+ 0.4298 * x2
		+ 0.1191 * x
		- 0.00232;
}
vec3 AgXToneMapping( vec3 color ) {
	const mat3 AgXInsetMatrix = mat3(
		vec3( 0.856627153315983, 0.137318972929847, 0.11189821299995 ),
		vec3( 0.0951212405381588, 0.761241990602591, 0.0767994186031903 ),
		vec3( 0.0482516061458583, 0.101439036467562, 0.811302368396859 )
	);
	const mat3 AgXOutsetMatrix = mat3(
		vec3( 1.1271005818144368, - 0.1413297634984383, - 0.14132976349843826 ),
		vec3( - 0.11060664309660323, 1.157823702216272, - 0.11060664309660294 ),
		vec3( - 0.016493938717834573, - 0.016493938717834257, 1.2519364065950405 )
	);
	const float AgxMinEv = - 12.47393;	const float AgxMaxEv = 4.026069;
	color *= toneMappingExposure;
	color = LINEAR_SRGB_TO_LINEAR_REC2020 * color;
	color = AgXInsetMatrix * color;
	color = max( color, 1e-10 );	color = log2( color );
	color = ( color - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	color = clamp( color, 0.0, 1.0 );
	color = agxDefaultContrastApprox( color );
	color = AgXOutsetMatrix * color;
	color = pow( max( vec3( 0.0 ), color ), vec3( 2.2 ) );
	color = LINEAR_REC2020_TO_LINEAR_SRGB * color;
	color = clamp( color, 0.0, 1.0 );
	return color;
}
vec3 NeutralToneMapping( vec3 color ) {
	const float StartCompression = 0.8 - 0.04;
	const float Desaturation = 0.15;
	color *= toneMappingExposure;
	float x = min( color.r, min( color.g, color.b ) );
	float offset = x < 0.08 ? x - 6.25 * x * x : 0.04;
	color -= offset;
	float peak = max( color.r, max( color.g, color.b ) );
	if ( peak < StartCompression ) return color;
	float d = 1. - StartCompression;
	float newPeak = 1. - d * d / ( peak + d - StartCompression );
	color *= newPeak / peak;
	float g = 1. - 1. / ( Desaturation * ( peak - newPeak ) + 1. );
	return mix( color, vec3( newPeak ), g );
}
vec3 CustomToneMapping( vec3 color ) { return color; }`,hp=`#ifdef USE_TRANSMISSION
	material.transmission = transmission;
	material.transmissionAlpha = 1.0;
	material.thickness = thickness;
	material.attenuationDistance = attenuationDistance;
	material.attenuationColor = attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		material.transmission *= texture2D( transmissionMap, vTransmissionMapUv ).r;
	#endif
	#ifdef USE_THICKNESSMAP
		material.thickness *= texture2D( thicknessMap, vThicknessMapUv ).g;
	#endif
	vec3 pos = vWorldPosition;
	vec3 v = normalize( cameraPosition - pos );
	vec3 n = inverseTransformDirection( normal, viewMatrix );
	vec4 transmitted = getIBLVolumeRefraction(
		n, v, material.roughness, material.diffuseColor, material.specularColor, material.specularF90,
		pos, modelMatrix, viewMatrix, projectionMatrix, material.dispersion, material.ior, material.thickness,
		material.attenuationColor, material.attenuationDistance );
	material.transmissionAlpha = mix( material.transmissionAlpha, transmitted.a, material.transmission );
	totalDiffuse = mix( totalDiffuse, transmitted.rgb, material.transmission );
#endif`,dp=`#ifdef USE_TRANSMISSION
	uniform float transmission;
	uniform float thickness;
	uniform float attenuationDistance;
	uniform vec3 attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		uniform sampler2D transmissionMap;
	#endif
	#ifdef USE_THICKNESSMAP
		uniform sampler2D thicknessMap;
	#endif
	uniform vec2 transmissionSamplerSize;
	uniform sampler2D transmissionSamplerMap;
	uniform mat4 modelMatrix;
	uniform mat4 projectionMatrix;
	varying vec3 vWorldPosition;
	float w0( float a ) {
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - a + 3.0 ) - 3.0 ) + 1.0 );
	}
	float w1( float a ) {
		return ( 1.0 / 6.0 ) * ( a *  a * ( 3.0 * a - 6.0 ) + 4.0 );
	}
	float w2( float a ){
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - 3.0 * a + 3.0 ) + 3.0 ) + 1.0 );
	}
	float w3( float a ) {
		return ( 1.0 / 6.0 ) * ( a * a * a );
	}
	float g0( float a ) {
		return w0( a ) + w1( a );
	}
	float g1( float a ) {
		return w2( a ) + w3( a );
	}
	float h0( float a ) {
		return - 1.0 + w1( a ) / ( w0( a ) + w1( a ) );
	}
	float h1( float a ) {
		return 1.0 + w3( a ) / ( w2( a ) + w3( a ) );
	}
	vec4 bicubic( sampler2D tex, vec2 uv, vec4 texelSize, float lod ) {
		uv = uv * texelSize.zw + 0.5;
		vec2 iuv = floor( uv );
		vec2 fuv = fract( uv );
		float g0x = g0( fuv.x );
		float g1x = g1( fuv.x );
		float h0x = h0( fuv.x );
		float h1x = h1( fuv.x );
		float h0y = h0( fuv.y );
		float h1y = h1( fuv.y );
		vec2 p0 = ( vec2( iuv.x + h0x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p1 = ( vec2( iuv.x + h1x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p2 = ( vec2( iuv.x + h0x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		vec2 p3 = ( vec2( iuv.x + h1x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		return g0( fuv.y ) * ( g0x * textureLod( tex, p0, lod ) + g1x * textureLod( tex, p1, lod ) ) +
			g1( fuv.y ) * ( g0x * textureLod( tex, p2, lod ) + g1x * textureLod( tex, p3, lod ) );
	}
	vec4 textureBicubic( sampler2D sampler, vec2 uv, float lod ) {
		vec2 fLodSize = vec2( textureSize( sampler, int( lod ) ) );
		vec2 cLodSize = vec2( textureSize( sampler, int( lod + 1.0 ) ) );
		vec2 fLodSizeInv = 1.0 / fLodSize;
		vec2 cLodSizeInv = 1.0 / cLodSize;
		vec4 fSample = bicubic( sampler, uv, vec4( fLodSizeInv, fLodSize ), floor( lod ) );
		vec4 cSample = bicubic( sampler, uv, vec4( cLodSizeInv, cLodSize ), ceil( lod ) );
		return mix( fSample, cSample, fract( lod ) );
	}
	vec3 getVolumeTransmissionRay( const in vec3 n, const in vec3 v, const in float thickness, const in float ior, const in mat4 modelMatrix ) {
		vec3 refractionVector = refract( - v, normalize( n ), 1.0 / ior );
		vec3 modelScale;
		modelScale.x = length( vec3( modelMatrix[ 0 ].xyz ) );
		modelScale.y = length( vec3( modelMatrix[ 1 ].xyz ) );
		modelScale.z = length( vec3( modelMatrix[ 2 ].xyz ) );
		return normalize( refractionVector ) * thickness * modelScale;
	}
	float applyIorToRoughness( const in float roughness, const in float ior ) {
		return roughness * clamp( ior * 2.0 - 2.0, 0.0, 1.0 );
	}
	vec4 getTransmissionSample( const in vec2 fragCoord, const in float roughness, const in float ior ) {
		float lod = log2( transmissionSamplerSize.x ) * applyIorToRoughness( roughness, ior );
		return textureBicubic( transmissionSamplerMap, fragCoord.xy, lod );
	}
	vec3 volumeAttenuation( const in float transmissionDistance, const in vec3 attenuationColor, const in float attenuationDistance ) {
		if ( isinf( attenuationDistance ) ) {
			return vec3( 1.0 );
		} else {
			vec3 attenuationCoefficient = -log( attenuationColor ) / attenuationDistance;
			vec3 transmittance = exp( - attenuationCoefficient * transmissionDistance );			return transmittance;
		}
	}
	vec4 getIBLVolumeRefraction( const in vec3 n, const in vec3 v, const in float roughness, const in vec3 diffuseColor,
		const in vec3 specularColor, const in float specularF90, const in vec3 position, const in mat4 modelMatrix,
		const in mat4 viewMatrix, const in mat4 projMatrix, const in float dispersion, const in float ior, const in float thickness,
		const in vec3 attenuationColor, const in float attenuationDistance ) {
		vec4 transmittedLight;
		vec3 transmittance;
		#ifdef USE_DISPERSION
			float halfSpread = ( ior - 1.0 ) * 0.025 * dispersion;
			vec3 iors = vec3( ior - halfSpread, ior, ior + halfSpread );
			for ( int i = 0; i < 3; i ++ ) {
				vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, iors[ i ], modelMatrix );
				vec3 refractedRayExit = position + transmissionRay;
				vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
				vec2 refractionCoords = ndcPos.xy / ndcPos.w;
				refractionCoords += 1.0;
				refractionCoords /= 2.0;
				vec4 transmissionSample = getTransmissionSample( refractionCoords, roughness, iors[ i ] );
				transmittedLight[ i ] = transmissionSample[ i ];
				transmittedLight.a += transmissionSample.a;
				transmittance[ i ] = diffuseColor[ i ] * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance )[ i ];
			}
			transmittedLight.a /= 3.0;
		#else
			vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, ior, modelMatrix );
			vec3 refractedRayExit = position + transmissionRay;
			vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
			vec2 refractionCoords = ndcPos.xy / ndcPos.w;
			refractionCoords += 1.0;
			refractionCoords /= 2.0;
			transmittedLight = getTransmissionSample( refractionCoords, roughness, ior );
			transmittance = diffuseColor * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance );
		#endif
		vec3 attenuatedColor = transmittance * transmittedLight.rgb;
		vec3 F = EnvironmentBRDF( n, v, specularColor, specularF90, roughness );
		float transmittanceFactor = ( transmittance.r + transmittance.g + transmittance.b ) / 3.0;
		return vec4( ( 1.0 - F ) * attenuatedColor, 1.0 - ( 1.0 - transmittedLight.a ) * transmittanceFactor );
	}
#endif`,fp=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_SPECULARMAP
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,pp=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	uniform mat3 mapTransform;
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	uniform mat3 alphaMapTransform;
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	uniform mat3 lightMapTransform;
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	uniform mat3 aoMapTransform;
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	uniform mat3 bumpMapTransform;
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	uniform mat3 normalMapTransform;
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_DISPLACEMENTMAP
	uniform mat3 displacementMapTransform;
	varying vec2 vDisplacementMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	uniform mat3 emissiveMapTransform;
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	uniform mat3 metalnessMapTransform;
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	uniform mat3 roughnessMapTransform;
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	uniform mat3 anisotropyMapTransform;
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	uniform mat3 clearcoatMapTransform;
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform mat3 clearcoatNormalMapTransform;
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform mat3 clearcoatRoughnessMapTransform;
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	uniform mat3 sheenColorMapTransform;
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	uniform mat3 sheenRoughnessMapTransform;
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	uniform mat3 iridescenceMapTransform;
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform mat3 iridescenceThicknessMapTransform;
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SPECULARMAP
	uniform mat3 specularMapTransform;
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	uniform mat3 specularColorMapTransform;
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	uniform mat3 specularIntensityMapTransform;
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,mp=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	vUv = vec3( uv, 1 ).xy;
#endif
#ifdef USE_MAP
	vMapUv = ( mapTransform * vec3( MAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ALPHAMAP
	vAlphaMapUv = ( alphaMapTransform * vec3( ALPHAMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_LIGHTMAP
	vLightMapUv = ( lightMapTransform * vec3( LIGHTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_AOMAP
	vAoMapUv = ( aoMapTransform * vec3( AOMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_BUMPMAP
	vBumpMapUv = ( bumpMapTransform * vec3( BUMPMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_NORMALMAP
	vNormalMapUv = ( normalMapTransform * vec3( NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_DISPLACEMENTMAP
	vDisplacementMapUv = ( displacementMapTransform * vec3( DISPLACEMENTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_EMISSIVEMAP
	vEmissiveMapUv = ( emissiveMapTransform * vec3( EMISSIVEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_METALNESSMAP
	vMetalnessMapUv = ( metalnessMapTransform * vec3( METALNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ROUGHNESSMAP
	vRoughnessMapUv = ( roughnessMapTransform * vec3( ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ANISOTROPYMAP
	vAnisotropyMapUv = ( anisotropyMapTransform * vec3( ANISOTROPYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOATMAP
	vClearcoatMapUv = ( clearcoatMapTransform * vec3( CLEARCOATMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	vClearcoatNormalMapUv = ( clearcoatNormalMapTransform * vec3( CLEARCOAT_NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	vClearcoatRoughnessMapUv = ( clearcoatRoughnessMapTransform * vec3( CLEARCOAT_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCEMAP
	vIridescenceMapUv = ( iridescenceMapTransform * vec3( IRIDESCENCEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	vIridescenceThicknessMapUv = ( iridescenceThicknessMapTransform * vec3( IRIDESCENCE_THICKNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_COLORMAP
	vSheenColorMapUv = ( sheenColorMapTransform * vec3( SHEEN_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	vSheenRoughnessMapUv = ( sheenRoughnessMapTransform * vec3( SHEEN_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULARMAP
	vSpecularMapUv = ( specularMapTransform * vec3( SPECULARMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_COLORMAP
	vSpecularColorMapUv = ( specularColorMapTransform * vec3( SPECULAR_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	vSpecularIntensityMapUv = ( specularIntensityMapTransform * vec3( SPECULAR_INTENSITYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_TRANSMISSIONMAP
	vTransmissionMapUv = ( transmissionMapTransform * vec3( TRANSMISSIONMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_THICKNESSMAP
	vThicknessMapUv = ( thicknessMapTransform * vec3( THICKNESSMAP_UV, 1 ) ).xy;
#endif`,gp=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`,_p=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,yp=`uniform sampler2D t2D;
uniform float backgroundIntensity;
varying vec2 vUv;
void main() {
	vec4 texColor = texture2D( t2D, vUv );
	#ifdef DECODE_VIDEO_TEXTURE
		texColor = vec4( mix( pow( texColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), texColor.rgb * 0.0773993808, vec3( lessThanEqual( texColor.rgb, vec3( 0.04045 ) ) ) ), texColor.w );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,vp=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,xp=`#ifdef ENVMAP_TYPE_CUBE
	uniform samplerCube envMap;
#elif defined( ENVMAP_TYPE_CUBE_UV )
	uniform sampler2D envMap;
#endif
uniform float flipEnvMap;
uniform float backgroundBlurriness;
uniform float backgroundIntensity;
uniform mat3 backgroundRotation;
varying vec3 vWorldDirection;
#include <cube_uv_reflection_fragment>
void main() {
	#ifdef ENVMAP_TYPE_CUBE
		vec4 texColor = textureCube( envMap, backgroundRotation * vec3( flipEnvMap * vWorldDirection.x, vWorldDirection.yz ) );
	#elif defined( ENVMAP_TYPE_CUBE_UV )
		vec4 texColor = textureCubeUV( envMap, backgroundRotation * vWorldDirection, backgroundBlurriness );
	#else
		vec4 texColor = vec4( 0.0, 0.0, 0.0, 1.0 );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Ep=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Sp=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Tp=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
varying vec2 vHighPrecisionZW;
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vHighPrecisionZW = gl_Position.zw;
}`,Mp=`#if DEPTH_PACKING == 3200
	uniform float opacity;
#endif
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
varying vec2 vHighPrecisionZW;
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#if DEPTH_PACKING == 3200
		diffuseColor.a = opacity;
	#endif
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <logdepthbuf_fragment>
	#ifdef USE_REVERSEDEPTHBUF
		float fragCoordZ = vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ];
	#else
		float fragCoordZ = 0.5 * vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ] + 0.5;
	#endif
	#if DEPTH_PACKING == 3200
		gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );
	#elif DEPTH_PACKING == 3201
		gl_FragColor = packDepthToRGBA( fragCoordZ );
	#elif DEPTH_PACKING == 3202
		gl_FragColor = vec4( packDepthToRGB( fragCoordZ ), 1.0 );
	#elif DEPTH_PACKING == 3203
		gl_FragColor = vec4( packDepthToRG( fragCoordZ ), 0.0, 1.0 );
	#endif
}`,bp=`#define DISTANCE
varying vec3 vWorldPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <worldpos_vertex>
	#include <clipping_planes_vertex>
	vWorldPosition = worldPosition.xyz;
}`,Ap=`#define DISTANCE
uniform vec3 referencePosition;
uniform float nearDistance;
uniform float farDistance;
varying vec3 vWorldPosition;
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <clipping_planes_pars_fragment>
void main () {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	float dist = length( vWorldPosition - referencePosition );
	dist = ( dist - nearDistance ) / ( farDistance - nearDistance );
	dist = saturate( dist );
	gl_FragColor = packDepthToRGBA( dist );
}`,Rp=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,wp=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Cp=`uniform float scale;
attribute float lineDistance;
varying float vLineDistance;
#include <common>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	vLineDistance = scale * lineDistance;
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,Ip=`uniform vec3 diffuse;
uniform float opacity;
uniform float dashSize;
uniform float totalSize;
varying float vLineDistance;
#include <common>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	if ( mod( vLineDistance, totalSize ) > dashSize ) {
		discard;
	}
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,Pp=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#if defined ( USE_ENVMAP ) || defined ( USE_SKINNING )
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinbase_vertex>
		#include <skinnormal_vertex>
		#include <defaultnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <fog_vertex>
}`,Lp=`uniform vec3 diffuse;
uniform float opacity;
#ifndef FLAT_SHADED
	varying vec3 vNormal;
#endif
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		reflectedLight.indirectDiffuse += lightMapTexel.rgb * lightMapIntensity * RECIPROCAL_PI;
	#else
		reflectedLight.indirectDiffuse += vec3( 1.0 );
	#endif
	#include <aomap_fragment>
	reflectedLight.indirectDiffuse *= diffuseColor.rgb;
	vec3 outgoingLight = reflectedLight.indirectDiffuse;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Np=`#define LAMBERT
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Op=`#define LAMBERT
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_lambert_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_lambert_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Dp=`#define MATCAP
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <displacementmap_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
	vViewPosition = - mvPosition.xyz;
}`,Up=`#define MATCAP
uniform vec3 diffuse;
uniform float opacity;
uniform sampler2D matcap;
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	vec3 viewDir = normalize( vViewPosition );
	vec3 x = normalize( vec3( viewDir.z, 0.0, - viewDir.x ) );
	vec3 y = cross( viewDir, x );
	vec2 uv = vec2( dot( x, normal ), dot( y, normal ) ) * 0.495 + 0.5;
	#ifdef USE_MATCAP
		vec4 matcapColor = texture2D( matcap, uv );
	#else
		vec4 matcapColor = vec4( vec3( mix( 0.2, 0.8, uv.y ) ), 1.0 );
	#endif
	vec3 outgoingLight = diffuseColor.rgb * matcapColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Fp=`#define NORMAL
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	vViewPosition = - mvPosition.xyz;
#endif
}`,kp=`#define NORMAL
uniform float opacity;
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <packing>
#include <uv_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 0.0, 0.0, 0.0, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	gl_FragColor = vec4( packNormalToRGB( normal ), diffuseColor.a );
	#ifdef OPAQUE
		gl_FragColor.a = 1.0;
	#endif
}`,Bp=`#define PHONG
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,zp=`#define PHONG
uniform vec3 diffuse;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_phong_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_phong_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + reflectedLight.directSpecular + reflectedLight.indirectSpecular + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Vp=`#define STANDARD
varying vec3 vViewPosition;
#ifdef USE_TRANSMISSION
	varying vec3 vWorldPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
#ifdef USE_TRANSMISSION
	vWorldPosition = worldPosition.xyz;
#endif
}`,Gp=`#define STANDARD
#ifdef PHYSICAL
	#define IOR
	#define USE_SPECULAR
#endif
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;
#ifdef IOR
	uniform float ior;
#endif
#ifdef USE_SPECULAR
	uniform float specularIntensity;
	uniform vec3 specularColor;
	#ifdef USE_SPECULAR_COLORMAP
		uniform sampler2D specularColorMap;
	#endif
	#ifdef USE_SPECULAR_INTENSITYMAP
		uniform sampler2D specularIntensityMap;
	#endif
#endif
#ifdef USE_CLEARCOAT
	uniform float clearcoat;
	uniform float clearcoatRoughness;
#endif
#ifdef USE_DISPERSION
	uniform float dispersion;
#endif
#ifdef USE_IRIDESCENCE
	uniform float iridescence;
	uniform float iridescenceIOR;
	uniform float iridescenceThicknessMinimum;
	uniform float iridescenceThicknessMaximum;
#endif
#ifdef USE_SHEEN
	uniform vec3 sheenColor;
	uniform float sheenRoughness;
	#ifdef USE_SHEEN_COLORMAP
		uniform sampler2D sheenColorMap;
	#endif
	#ifdef USE_SHEEN_ROUGHNESSMAP
		uniform sampler2D sheenRoughnessMap;
	#endif
#endif
#ifdef USE_ANISOTROPY
	uniform vec2 anisotropyVector;
	#ifdef USE_ANISOTROPYMAP
		uniform sampler2D anisotropyMap;
	#endif
#endif
varying vec3 vViewPosition;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <iridescence_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_physical_pars_fragment>
#include <transmission_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <clearcoat_pars_fragment>
#include <iridescence_pars_fragment>
#include <roughnessmap_pars_fragment>
#include <metalnessmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <roughnessmap_fragment>
	#include <metalnessmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_physical_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 totalDiffuse = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse;
	vec3 totalSpecular = reflectedLight.directSpecular + reflectedLight.indirectSpecular;
	#include <transmission_fragment>
	vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;
	#ifdef USE_SHEEN
		float sheenEnergyComp = 1.0 - 0.157 * max3( material.sheenColor );
		outgoingLight = outgoingLight * sheenEnergyComp + sheenSpecularDirect + sheenSpecularIndirect;
	#endif
	#ifdef USE_CLEARCOAT
		float dotNVcc = saturate( dot( geometryClearcoatNormal, geometryViewDir ) );
		vec3 Fcc = F_Schlick( material.clearcoatF0, material.clearcoatF90, dotNVcc );
		outgoingLight = outgoingLight * ( 1.0 - material.clearcoat * Fcc ) + ( clearcoatSpecularDirect + clearcoatSpecularIndirect ) * material.clearcoat;
	#endif
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Hp=`#define TOON
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Wp=`#define TOON
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <gradientmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_toon_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_toon_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Xp=`uniform float size;
uniform float scale;
#include <common>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
#ifdef USE_POINTS_UV
	varying vec2 vUv;
	uniform mat3 uvTransform;
#endif
void main() {
	#ifdef USE_POINTS_UV
		vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	#endif
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	gl_PointSize = size;
	#ifdef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) gl_PointSize *= ( scale / - mvPosition.z );
	#endif
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <fog_vertex>
}`,Yp=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <color_pars_fragment>
#include <map_particle_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_particle_fragment>
	#include <color_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,qp=`#include <common>
#include <batching_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <shadowmap_pars_vertex>
void main() {
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Kp=`uniform vec3 color;
uniform float opacity;
#include <common>
#include <packing>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <logdepthbuf_pars_fragment>
#include <shadowmap_pars_fragment>
#include <shadowmask_pars_fragment>
void main() {
	#include <logdepthbuf_fragment>
	gl_FragColor = vec4( color, opacity * ( 1.0 - getShadowMask() ) );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,Zp=`uniform float rotation;
uniform vec2 center;
#include <common>
#include <uv_pars_vertex>
#include <fog_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	vec4 mvPosition = modelViewMatrix[ 3 ];
	vec2 scale = vec2( length( modelMatrix[ 0 ].xyz ), length( modelMatrix[ 1 ].xyz ) );
	#ifndef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) scale *= - mvPosition.z;
	#endif
	vec2 alignedPosition = ( position.xy - ( center - vec2( 0.5 ) ) ) * scale;
	vec2 rotatedPosition;
	rotatedPosition.x = cos( rotation ) * alignedPosition.x - sin( rotation ) * alignedPosition.y;
	rotatedPosition.y = sin( rotation ) * alignedPosition.x + cos( rotation ) * alignedPosition.y;
	mvPosition.xy += rotatedPosition;
	gl_Position = projectionMatrix * mvPosition;
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,jp=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,$e={alphahash_fragment:_d,alphahash_pars_fragment:yd,alphamap_fragment:vd,alphamap_pars_fragment:xd,alphatest_fragment:Ed,alphatest_pars_fragment:Sd,aomap_fragment:Td,aomap_pars_fragment:Md,batching_pars_vertex:bd,batching_vertex:Ad,begin_vertex:Rd,beginnormal_vertex:wd,bsdfs:Cd,iridescence_fragment:Id,bumpmap_pars_fragment:Pd,clipping_planes_fragment:Ld,clipping_planes_pars_fragment:Nd,clipping_planes_pars_vertex:Od,clipping_planes_vertex:Dd,color_fragment:Ud,color_pars_fragment:Fd,color_pars_vertex:kd,color_vertex:Bd,common:zd,cube_uv_reflection_fragment:Vd,defaultnormal_vertex:Gd,displacementmap_pars_vertex:Hd,displacementmap_vertex:Wd,emissivemap_fragment:Xd,emissivemap_pars_fragment:Yd,colorspace_fragment:qd,colorspace_pars_fragment:Kd,envmap_fragment:Zd,envmap_common_pars_fragment:jd,envmap_pars_fragment:Jd,envmap_pars_vertex:$d,envmap_physical_pars_fragment:uf,envmap_vertex:Qd,fog_vertex:ef,fog_pars_vertex:tf,fog_fragment:nf,fog_pars_fragment:rf,gradientmap_pars_fragment:sf,lightmap_pars_fragment:of,lights_lambert_fragment:af,lights_lambert_pars_fragment:cf,lights_pars_begin:lf,lights_toon_fragment:hf,lights_toon_pars_fragment:df,lights_phong_fragment:ff,lights_phong_pars_fragment:pf,lights_physical_fragment:mf,lights_physical_pars_fragment:gf,lights_fragment_begin:_f,lights_fragment_maps:yf,lights_fragment_end:vf,logdepthbuf_fragment:xf,logdepthbuf_pars_fragment:Ef,logdepthbuf_pars_vertex:Sf,logdepthbuf_vertex:Tf,map_fragment:Mf,map_pars_fragment:bf,map_particle_fragment:Af,map_particle_pars_fragment:Rf,metalnessmap_fragment:wf,metalnessmap_pars_fragment:Cf,morphinstance_vertex:If,morphcolor_vertex:Pf,morphnormal_vertex:Lf,morphtarget_pars_vertex:Nf,morphtarget_vertex:Of,normal_fragment_begin:Df,normal_fragment_maps:Uf,normal_pars_fragment:Ff,normal_pars_vertex:kf,normal_vertex:Bf,normalmap_pars_fragment:zf,clearcoat_normal_fragment_begin:Vf,clearcoat_normal_fragment_maps:Gf,clearcoat_pars_fragment:Hf,iridescence_pars_fragment:Wf,opaque_fragment:Xf,packing:Yf,premultiplied_alpha_fragment:qf,project_vertex:Kf,dithering_fragment:Zf,dithering_pars_fragment:jf,roughnessmap_fragment:Jf,roughnessmap_pars_fragment:$f,shadowmap_pars_fragment:Qf,shadowmap_pars_vertex:ep,shadowmap_vertex:tp,shadowmask_pars_fragment:np,skinbase_vertex:ip,skinning_pars_vertex:rp,skinning_vertex:sp,skinnormal_vertex:op,specularmap_fragment:ap,specularmap_pars_fragment:cp,tonemapping_fragment:lp,tonemapping_pars_fragment:up,transmission_fragment:hp,transmission_pars_fragment:dp,uv_pars_fragment:fp,uv_pars_vertex:pp,uv_vertex:mp,worldpos_vertex:gp,background_vert:_p,background_frag:yp,backgroundCube_vert:vp,backgroundCube_frag:xp,cube_vert:Ep,cube_frag:Sp,depth_vert:Tp,depth_frag:Mp,distanceRGBA_vert:bp,distanceRGBA_frag:Ap,equirect_vert:Rp,equirect_frag:wp,linedashed_vert:Cp,linedashed_frag:Ip,meshbasic_vert:Pp,meshbasic_frag:Lp,meshlambert_vert:Np,meshlambert_frag:Op,meshmatcap_vert:Dp,meshmatcap_frag:Up,meshnormal_vert:Fp,meshnormal_frag:kp,meshphong_vert:Bp,meshphong_frag:zp,meshphysical_vert:Vp,meshphysical_frag:Gp,meshtoon_vert:Hp,meshtoon_frag:Wp,points_vert:Xp,points_frag:Yp,shadow_vert:qp,shadow_frag:Kp,sprite_vert:Zp,sprite_frag:jp},Ae={common:{diffuse:{value:new qe(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new Ze},alphaMap:{value:null},alphaMapTransform:{value:new Ze},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new Ze}},envmap:{envMap:{value:null},envMapRotation:{value:new Ze},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new Ze}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new Ze}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new Ze},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new Ze},normalScale:{value:new ze(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new Ze},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new Ze}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new Ze}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new Ze}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new qe(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new qe(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new Ze},alphaTest:{value:0},uvTransform:{value:new Ze}},sprite:{diffuse:{value:new qe(16777215)},opacity:{value:1},center:{value:new ze(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new Ze},alphaMap:{value:null},alphaMapTransform:{value:new Ze},alphaTest:{value:0}}},Mn={basic:{uniforms:Nt([Ae.common,Ae.specularmap,Ae.envmap,Ae.aomap,Ae.lightmap,Ae.fog]),vertexShader:$e.meshbasic_vert,fragmentShader:$e.meshbasic_frag},lambert:{uniforms:Nt([Ae.common,Ae.specularmap,Ae.envmap,Ae.aomap,Ae.lightmap,Ae.emissivemap,Ae.bumpmap,Ae.normalmap,Ae.displacementmap,Ae.fog,Ae.lights,{emissive:{value:new qe(0)}}]),vertexShader:$e.meshlambert_vert,fragmentShader:$e.meshlambert_frag},phong:{uniforms:Nt([Ae.common,Ae.specularmap,Ae.envmap,Ae.aomap,Ae.lightmap,Ae.emissivemap,Ae.bumpmap,Ae.normalmap,Ae.displacementmap,Ae.fog,Ae.lights,{emissive:{value:new qe(0)},specular:{value:new qe(1118481)},shininess:{value:30}}]),vertexShader:$e.meshphong_vert,fragmentShader:$e.meshphong_frag},standard:{uniforms:Nt([Ae.common,Ae.envmap,Ae.aomap,Ae.lightmap,Ae.emissivemap,Ae.bumpmap,Ae.normalmap,Ae.displacementmap,Ae.roughnessmap,Ae.metalnessmap,Ae.fog,Ae.lights,{emissive:{value:new qe(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:$e.meshphysical_vert,fragmentShader:$e.meshphysical_frag},toon:{uniforms:Nt([Ae.common,Ae.aomap,Ae.lightmap,Ae.emissivemap,Ae.bumpmap,Ae.normalmap,Ae.displacementmap,Ae.gradientmap,Ae.fog,Ae.lights,{emissive:{value:new qe(0)}}]),vertexShader:$e.meshtoon_vert,fragmentShader:$e.meshtoon_frag},matcap:{uniforms:Nt([Ae.common,Ae.bumpmap,Ae.normalmap,Ae.displacementmap,Ae.fog,{matcap:{value:null}}]),vertexShader:$e.meshmatcap_vert,fragmentShader:$e.meshmatcap_frag},points:{uniforms:Nt([Ae.points,Ae.fog]),vertexShader:$e.points_vert,fragmentShader:$e.points_frag},dashed:{uniforms:Nt([Ae.common,Ae.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:$e.linedashed_vert,fragmentShader:$e.linedashed_frag},depth:{uniforms:Nt([Ae.common,Ae.displacementmap]),vertexShader:$e.depth_vert,fragmentShader:$e.depth_frag},normal:{uniforms:Nt([Ae.common,Ae.bumpmap,Ae.normalmap,Ae.displacementmap,{opacity:{value:1}}]),vertexShader:$e.meshnormal_vert,fragmentShader:$e.meshnormal_frag},sprite:{uniforms:Nt([Ae.sprite,Ae.fog]),vertexShader:$e.sprite_vert,fragmentShader:$e.sprite_frag},background:{uniforms:{uvTransform:{value:new Ze},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:$e.background_vert,fragmentShader:$e.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new Ze}},vertexShader:$e.backgroundCube_vert,fragmentShader:$e.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:$e.cube_vert,fragmentShader:$e.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:$e.equirect_vert,fragmentShader:$e.equirect_frag},distanceRGBA:{uniforms:Nt([Ae.common,Ae.displacementmap,{referencePosition:{value:new Z},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:$e.distanceRGBA_vert,fragmentShader:$e.distanceRGBA_frag},shadow:{uniforms:Nt([Ae.lights,Ae.fog,{color:{value:new qe(0)},opacity:{value:1}}]),vertexShader:$e.shadow_vert,fragmentShader:$e.shadow_frag}};Mn.physical={uniforms:Nt([Mn.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new Ze},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new Ze},clearcoatNormalScale:{value:new ze(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new Ze},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new Ze},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new Ze},sheen:{value:0},sheenColor:{value:new qe(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new Ze},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new Ze},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new Ze},transmissionSamplerSize:{value:new ze},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new Ze},attenuationDistance:{value:0},attenuationColor:{value:new qe(0)},specularColor:{value:new qe(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new Ze},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new Ze},anisotropyVector:{value:new ze},anisotropyMap:{value:null},anisotropyMapTransform:{value:new Ze}}]),vertexShader:$e.meshphysical_vert,fragmentShader:$e.meshphysical_frag};var Vo={r:0,b:0,g:0},_i=new dn,Jp=new yt;function $p(n,e,t,i,r,s,o){let c=new qe(0),l=s===!0?0:1,a,d,p=null,f=0,m=null;function g(x){let _=x.isScene===!0?x.background:null;return _&&_.isTexture&&(_=(x.backgroundBlurriness>0?t:e).get(_)),_}function y(x){let _=!1,A=g(x);A===null?u(c,l):A&&A.isColor&&(u(A,1),_=!0);let N=n.xr.getEnvironmentBlendMode();N==="additive"?i.buffers.color.setClear(0,0,0,1,o):N==="alpha-blend"&&i.buffers.color.setClear(0,0,0,0,o),(n.autoClear||_)&&(i.buffers.depth.setTest(!0),i.buffers.depth.setMask(!0),i.buffers.color.setMask(!0),n.clear(n.autoClearColor,n.autoClearDepth,n.autoClearStencil))}function h(x,_){let A=g(_);A&&(A.isCubeTexture||A.mapping===Wr)?(d===void 0&&(d=new Lt(new qn(1,1,1),new fn({name:"BackgroundCubeMaterial",uniforms:gi(Mn.backgroundCube.uniforms),vertexShader:Mn.backgroundCube.vertexShader,fragmentShader:Mn.backgroundCube.fragmentShader,side:wt,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),d.geometry.deleteAttribute("normal"),d.geometry.deleteAttribute("uv"),d.onBeforeRender=function(N,w,O){this.matrixWorld.copyPosition(O.matrixWorld)},Object.defineProperty(d.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),r.update(d)),_i.copy(_.backgroundRotation),_i.x*=-1,_i.y*=-1,_i.z*=-1,A.isCubeTexture&&A.isRenderTargetTexture===!1&&(_i.y*=-1,_i.z*=-1),d.material.uniforms.envMap.value=A,d.material.uniforms.flipEnvMap.value=A.isCubeTexture&&A.isRenderTargetTexture===!1?-1:1,d.material.uniforms.backgroundBlurriness.value=_.backgroundBlurriness,d.material.uniforms.backgroundIntensity.value=_.backgroundIntensity,d.material.uniforms.backgroundRotation.value.setFromMatrix4(Jp.makeRotationFromEuler(_i)),d.material.toneMapped=nt.getTransfer(A.colorSpace)!==at,(p!==A||f!==A.version||m!==n.toneMapping)&&(d.material.needsUpdate=!0,p=A,f=A.version,m=n.toneMapping),d.layers.enableAll(),x.unshift(d,d.geometry,d.material,0,0,null)):A&&A.isTexture&&(a===void 0&&(a=new Lt(new Or(2,2),new fn({name:"BackgroundMaterial",uniforms:gi(Mn.background.uniforms),vertexShader:Mn.background.vertexShader,fragmentShader:Mn.background.fragmentShader,side:un,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),a.geometry.deleteAttribute("normal"),Object.defineProperty(a.material,"map",{get:function(){return this.uniforms.t2D.value}}),r.update(a)),a.material.uniforms.t2D.value=A,a.material.uniforms.backgroundIntensity.value=_.backgroundIntensity,a.material.toneMapped=nt.getTransfer(A.colorSpace)!==at,A.matrixAutoUpdate===!0&&A.updateMatrix(),a.material.uniforms.uvTransform.value.copy(A.matrix),(p!==A||f!==A.version||m!==n.toneMapping)&&(a.material.needsUpdate=!0,p=A,f=A.version,m=n.toneMapping),a.layers.enableAll(),x.unshift(a,a.geometry,a.material,0,0,null))}function u(x,_){x.getRGB(Vo,oc(n)),i.buffers.color.setClear(Vo.r,Vo.g,Vo.b,_,o)}function E(){d!==void 0&&(d.geometry.dispose(),d.material.dispose(),d=void 0),a!==void 0&&(a.geometry.dispose(),a.material.dispose(),a=void 0)}return{getClearColor:function(){return c},setClearColor:function(x,_=1){c.set(x),l=_,u(c,l)},getClearAlpha:function(){return l},setClearAlpha:function(x){l=x,u(c,l)},render:y,addToRenderList:h,dispose:E}}function Qp(n,e){let t=n.getParameter(n.MAX_VERTEX_ATTRIBS),i={},r=f(null),s=r,o=!1;function c(M,R,I,U,P){let X=!1,W=p(U,I,R);s!==W&&(s=W,a(s.object)),X=m(M,U,I,P),X&&g(M,U,I,P),P!==null&&e.update(P,n.ELEMENT_ARRAY_BUFFER),(X||o)&&(o=!1,_(M,R,I,U),P!==null&&n.bindBuffer(n.ELEMENT_ARRAY_BUFFER,e.get(P).buffer))}function l(){return n.createVertexArray()}function a(M){return n.bindVertexArray(M)}function d(M){return n.deleteVertexArray(M)}function p(M,R,I){let U=I.wireframe===!0,P=i[M.id];P===void 0&&(P={},i[M.id]=P);let X=P[R.id];X===void 0&&(X={},P[R.id]=X);let W=X[U];return W===void 0&&(W=f(l()),X[U]=W),W}function f(M){let R=[],I=[],U=[];for(let P=0;P<t;P++)R[P]=0,I[P]=0,U[P]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:R,enabledAttributes:I,attributeDivisors:U,object:M,attributes:{},index:null}}function m(M,R,I,U){let P=s.attributes,X=R.attributes,W=0,q=I.getAttributes();for(let G in q)if(q[G].location>=0){let ae=P[G],ue=X[G];if(ue===void 0&&(G==="instanceMatrix"&&M.instanceMatrix&&(ue=M.instanceMatrix),G==="instanceColor"&&M.instanceColor&&(ue=M.instanceColor)),ae===void 0||ae.attribute!==ue||ue&&ae.data!==ue.data)return!0;W++}return s.attributesNum!==W||s.index!==U}function g(M,R,I,U){let P={},X=R.attributes,W=0,q=I.getAttributes();for(let G in q)if(q[G].location>=0){let ae=X[G];ae===void 0&&(G==="instanceMatrix"&&M.instanceMatrix&&(ae=M.instanceMatrix),G==="instanceColor"&&M.instanceColor&&(ae=M.instanceColor));let ue={};ue.attribute=ae,ae&&ae.data&&(ue.data=ae.data),P[G]=ue,W++}s.attributes=P,s.attributesNum=W,s.index=U}function y(){let M=s.newAttributes;for(let R=0,I=M.length;R<I;R++)M[R]=0}function h(M){u(M,0)}function u(M,R){let I=s.newAttributes,U=s.enabledAttributes,P=s.attributeDivisors;I[M]=1,U[M]===0&&(n.enableVertexAttribArray(M),U[M]=1),P[M]!==R&&(n.vertexAttribDivisor(M,R),P[M]=R)}function E(){let M=s.newAttributes,R=s.enabledAttributes;for(let I=0,U=R.length;I<U;I++)R[I]!==M[I]&&(n.disableVertexAttribArray(I),R[I]=0)}function x(M,R,I,U,P,X,W){W===!0?n.vertexAttribIPointer(M,R,I,P,X):n.vertexAttribPointer(M,R,I,U,P,X)}function _(M,R,I,U){y();let P=U.attributes,X=I.getAttributes(),W=R.defaultAttributeValues;for(let q in X){let G=X[q];if(G.location>=0){let ee=P[q];if(ee===void 0&&(q==="instanceMatrix"&&M.instanceMatrix&&(ee=M.instanceMatrix),q==="instanceColor"&&M.instanceColor&&(ee=M.instanceColor)),ee!==void 0){let ae=ee.normalized,ue=ee.itemSize,_e=e.get(ee);if(_e===void 0)continue;let me=_e.buffer,Me=_e.type,k=_e.bytesPerElement,Y=Me===n.INT||Me===n.UNSIGNED_INT||ee.gpuType===co;if(ee.isInterleavedBufferAttribute){let K=ee.data,ne=K.stride,ie=ee.offset;if(K.isInstancedInterleavedBuffer){for(let de=0;de<G.locationSize;de++)u(G.location+de,K.meshPerAttribute);M.isInstancedMesh!==!0&&U._maxInstanceCount===void 0&&(U._maxInstanceCount=K.meshPerAttribute*K.count)}else for(let de=0;de<G.locationSize;de++)h(G.location+de);n.bindBuffer(n.ARRAY_BUFFER,me);for(let de=0;de<G.locationSize;de++)x(G.location+de,ue/G.locationSize,Me,ae,ne*k,(ie+ue/G.locationSize*de)*k,Y)}else{if(ee.isInstancedBufferAttribute){for(let K=0;K<G.locationSize;K++)u(G.location+K,ee.meshPerAttribute);M.isInstancedMesh!==!0&&U._maxInstanceCount===void 0&&(U._maxInstanceCount=ee.meshPerAttribute*ee.count)}else for(let K=0;K<G.locationSize;K++)h(G.location+K);n.bindBuffer(n.ARRAY_BUFFER,me);for(let K=0;K<G.locationSize;K++)x(G.location+K,ue/G.locationSize,Me,ae,ue*k,ue/G.locationSize*K*k,Y)}}else if(W!==void 0){let ae=W[q];if(ae!==void 0)switch(ae.length){case 2:n.vertexAttrib2fv(G.location,ae);break;case 3:n.vertexAttrib3fv(G.location,ae);break;case 4:n.vertexAttrib4fv(G.location,ae);break;default:n.vertexAttrib1fv(G.location,ae)}}}}E()}function A(){O();for(let M in i){let R=i[M];for(let I in R){let U=R[I];for(let P in U)d(U[P].object),delete U[P];delete R[I]}delete i[M]}}function N(M){if(i[M.id]===void 0)return;let R=i[M.id];for(let I in R){let U=R[I];for(let P in U)d(U[P].object),delete U[P];delete R[I]}delete i[M.id]}function w(M){for(let R in i){let I=i[R];if(I[M.id]===void 0)continue;let U=I[M.id];for(let P in U)d(U[P].object),delete U[P];delete I[M.id]}}function O(){T(),o=!0,s!==r&&(s=r,a(s.object))}function T(){r.geometry=null,r.program=null,r.wireframe=!1}return{setup:c,reset:O,resetDefaultState:T,dispose:A,releaseStatesOfGeometry:N,releaseStatesOfProgram:w,initAttributes:y,enableAttribute:h,disableUnusedAttributes:E}}function em(n,e,t){let i;function r(a){i=a}function s(a,d){n.drawArrays(i,a,d),t.update(d,i,1)}function o(a,d,p){p!==0&&(n.drawArraysInstanced(i,a,d,p),t.update(d,i,p))}function c(a,d,p){if(p===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(i,a,0,d,0,p);let m=0;for(let g=0;g<p;g++)m+=d[g];t.update(m,i,1)}function l(a,d,p,f){if(p===0)return;let m=e.get("WEBGL_multi_draw");if(m===null)for(let g=0;g<a.length;g++)o(a[g],d[g],f[g]);else{m.multiDrawArraysInstancedWEBGL(i,a,0,d,0,f,0,p);let g=0;for(let y=0;y<p;y++)g+=d[y]*f[y];t.update(g,i,1)}}this.setMode=r,this.render=s,this.renderInstances=o,this.renderMultiDraw=c,this.renderMultiDrawInstances=l}function tm(n,e,t,i){let r;function s(){if(r!==void 0)return r;if(e.has("EXT_texture_filter_anisotropic")===!0){let w=e.get("EXT_texture_filter_anisotropic");r=n.getParameter(w.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else r=0;return r}function o(w){return!(w!==tn&&i.convert(w)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_FORMAT))}function c(w){let O=w===$i&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(w!==pn&&i.convert(w)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_TYPE)&&w!==Tn&&!O)}function l(w){if(w==="highp"){if(n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.HIGH_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.HIGH_FLOAT).precision>0)return"highp";w="mediump"}return w==="mediump"&&n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.MEDIUM_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let a=t.precision!==void 0?t.precision:"highp",d=l(a);d!==a&&(console.warn("THREE.WebGLRenderer:",a,"not supported, using",d,"instead."),a=d);let p=t.logarithmicDepthBuffer===!0,f=t.reversedDepthBuffer===!0&&e.has("EXT_clip_control"),m=n.getParameter(n.MAX_TEXTURE_IMAGE_UNITS),g=n.getParameter(n.MAX_VERTEX_TEXTURE_IMAGE_UNITS),y=n.getParameter(n.MAX_TEXTURE_SIZE),h=n.getParameter(n.MAX_CUBE_MAP_TEXTURE_SIZE),u=n.getParameter(n.MAX_VERTEX_ATTRIBS),E=n.getParameter(n.MAX_VERTEX_UNIFORM_VECTORS),x=n.getParameter(n.MAX_VARYING_VECTORS),_=n.getParameter(n.MAX_FRAGMENT_UNIFORM_VECTORS),A=g>0,N=n.getParameter(n.MAX_SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:s,getMaxPrecision:l,textureFormatReadable:o,textureTypeReadable:c,precision:a,logarithmicDepthBuffer:p,reversedDepthBuffer:f,maxTextures:m,maxVertexTextures:g,maxTextureSize:y,maxCubemapSize:h,maxAttributes:u,maxVertexUniforms:E,maxVaryings:x,maxFragmentUniforms:_,vertexTextures:A,maxSamples:N}}function nm(n){let e=this,t=null,i=0,r=!1,s=!1,o=new Qt,c=new Ze,l={value:null,needsUpdate:!1};this.uniform=l,this.numPlanes=0,this.numIntersection=0,this.init=function(p,f){let m=p.length!==0||f||i!==0||r;return r=f,i=p.length,m},this.beginShadows=function(){s=!0,d(null)},this.endShadows=function(){s=!1},this.setGlobalState=function(p,f){t=d(p,f,0)},this.setState=function(p,f,m){let g=p.clippingPlanes,y=p.clipIntersection,h=p.clipShadows,u=n.get(p);if(!r||g===null||g.length===0||s&&!h)s?d(null):a();else{let E=s?0:i,x=E*4,_=u.clippingState||null;l.value=_,_=d(g,f,x,m);for(let A=0;A!==x;++A)_[A]=t[A];u.clippingState=_,this.numIntersection=y?this.numPlanes:0,this.numPlanes+=E}};function a(){l.value!==t&&(l.value=t,l.needsUpdate=i>0),e.numPlanes=i,e.numIntersection=0}function d(p,f,m,g){let y=p!==null?p.length:0,h=null;if(y!==0){if(h=l.value,g!==!0||h===null){let u=m+y*4,E=f.matrixWorldInverse;c.getNormalMatrix(E),(h===null||h.length<u)&&(h=new Float32Array(u));for(let x=0,_=m;x!==y;++x,_+=4)o.copy(p[x]).applyMatrix4(E,c),o.normal.toArray(h,_),h[_+3]=o.constant}l.value=h,l.needsUpdate=!0}return e.numPlanes=y,e.numIntersection=0,h}}function im(n){let e=new WeakMap;function t(o,c){return c===so?o.mapping=pi:c===oo&&(o.mapping=mi),o}function i(o){if(o&&o.isTexture){let c=o.mapping;if(c===so||c===oo)if(e.has(o)){let l=e.get(o).texture;return t(l,o.mapping)}else{let l=o.image;if(l&&l.height>0){let a=new Ds(l.height);return a.fromEquirectangularTexture(n,o),e.set(o,a),o.addEventListener("dispose",r),t(a.texture,o.mapping)}else return null}}return o}function r(o){let c=o.target;c.removeEventListener("dispose",r);let l=e.get(c);l!==void 0&&(e.delete(c),l.dispose())}function s(){e=new WeakMap}return{get:i,dispose:s}}var ir=4,cu=[.125,.215,.35,.446,.526,.582],xi=20,uc=new Vr,lu=new qe,hc=null,dc=0,fc=0,pc=!1,vi=(1+Math.sqrt(5))/2,nr=1/vi,uu=[new Z(-vi,nr,0),new Z(vi,nr,0),new Z(-nr,0,vi),new Z(nr,0,vi),new Z(0,vi,-nr),new Z(0,vi,nr),new Z(-1,1,-1),new Z(1,1,-1),new Z(-1,1,1),new Z(1,1,1)],rm=new Z,Wo=class{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,t=0,i=.1,r=100,s={}){let{size:o=256,position:c=rm}=s;hc=this._renderer.getRenderTarget(),dc=this._renderer.getActiveCubeFace(),fc=this._renderer.getActiveMipmapLevel(),pc=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(o);let l=this._allocateTargets();return l.depthBuffer=!0,this._sceneToCubeUV(e,i,r,l,c),t>0&&this._blur(l,0,0,t),this._applyPMREM(l),this._cleanup(l),l}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=fu(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=du(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(hc,dc,fc),this._renderer.xr.enabled=pc,e.scissorTest=!1,Go(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===pi||e.mapping===mi?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),hc=this._renderer.getRenderTarget(),dc=this._renderer.getActiveCubeFace(),fc=this._renderer.getActiveMipmapLevel(),pc=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;let i=t||this._allocateTargets();return this._textureToCubeUV(e,i),this._applyPMREM(i),this._cleanup(i),i}_allocateTargets(){let e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,i={magFilter:hn,minFilter:hn,generateMipmaps:!1,type:$i,format:tn,colorSpace:ci,depthBuffer:!1},r=hu(e,t,i);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=hu(e,t,i);let{_lodMax:s}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=sm(s)),this._blurMaterial=om(s,e,t)}return r}_compileMaterial(e){let t=new Lt(this._lodPlanes[0],e);this._renderer.compile(t,uc)}_sceneToCubeUV(e,t,i,r,s){let l=new Pt(90,1,t,i),a=[1,-1,1,1,1,1],d=[1,1,1,-1,-1,-1],p=this._renderer,f=p.autoClear,m=p.toneMapping;p.getClearColor(lu),p.toneMapping=On,p.autoClear=!1,p.state.buffers.depth.getReversed()&&(p.setRenderTarget(r),p.clearDepth(),p.setRenderTarget(null));let y=new En({name:"PMREM.Background",side:wt,depthWrite:!1,depthTest:!1}),h=new Lt(new qn,y),u=!1,E=e.background;E?E.isColor&&(y.color.copy(E),e.background=null,u=!0):(y.color.copy(lu),u=!0);for(let x=0;x<6;x++){let _=x%3;_===0?(l.up.set(0,a[x],0),l.position.set(s.x,s.y,s.z),l.lookAt(s.x+d[x],s.y,s.z)):_===1?(l.up.set(0,0,a[x]),l.position.set(s.x,s.y,s.z),l.lookAt(s.x,s.y+d[x],s.z)):(l.up.set(0,a[x],0),l.position.set(s.x,s.y,s.z),l.lookAt(s.x,s.y,s.z+d[x]));let A=this._cubeSize;Go(r,_*A,x>2?A:0,A,A),p.setRenderTarget(r),u&&p.render(h,l),p.render(e,l)}h.geometry.dispose(),h.material.dispose(),p.toneMapping=m,p.autoClear=f,e.background=E}_textureToCubeUV(e,t){let i=this._renderer,r=e.mapping===pi||e.mapping===mi;r?(this._cubemapMaterial===null&&(this._cubemapMaterial=fu()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=du());let s=r?this._cubemapMaterial:this._equirectMaterial,o=new Lt(this._lodPlanes[0],s),c=s.uniforms;c.envMap.value=e;let l=this._cubeSize;Go(t,0,0,3*l,2*l),i.setRenderTarget(t),i.render(o,uc)}_applyPMREM(e){let t=this._renderer,i=t.autoClear;t.autoClear=!1;let r=this._lodPlanes.length;for(let s=1;s<r;s++){let o=Math.sqrt(this._sigmas[s]*this._sigmas[s]-this._sigmas[s-1]*this._sigmas[s-1]),c=uu[(r-s-1)%uu.length];this._blur(e,s-1,s,o,c)}t.autoClear=i}_blur(e,t,i,r,s){let o=this._pingPongRenderTarget;this._halfBlur(e,o,t,i,r,"latitudinal",s),this._halfBlur(o,e,i,i,r,"longitudinal",s)}_halfBlur(e,t,i,r,s,o,c){let l=this._renderer,a=this._blurMaterial;o!=="latitudinal"&&o!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");let d=3,p=new Lt(this._lodPlanes[r],a),f=a.uniforms,m=this._sizeLods[i]-1,g=isFinite(s)?Math.PI/(2*m):2*Math.PI/(2*xi-1),y=s/g,h=isFinite(s)?1+Math.floor(d*y):xi;h>xi&&console.warn(`sigmaRadians, ${s}, is too large and will clip, as it requested ${h} samples when the maximum is set to ${xi}`);let u=[],E=0;for(let w=0;w<xi;++w){let O=w/y,T=Math.exp(-O*O/2);u.push(T),w===0?E+=T:w<h&&(E+=2*T)}for(let w=0;w<u.length;w++)u[w]=u[w]/E;f.envMap.value=e.texture,f.samples.value=h,f.weights.value=u,f.latitudinal.value=o==="latitudinal",c&&(f.poleAxis.value=c);let{_lodMax:x}=this;f.dTheta.value=g,f.mipInt.value=x-i;let _=this._sizeLods[r],A=3*_*(r>x-ir?r-x+ir:0),N=4*(this._cubeSize-_);Go(t,A,N,3*_,2*_),l.setRenderTarget(t),l.render(p,uc)}};function sm(n){let e=[],t=[],i=[],r=n,s=n-ir+1+cu.length;for(let o=0;o<s;o++){let c=Math.pow(2,r);t.push(c);let l=1/c;o>n-ir?l=cu[o-n+ir-1]:o===0&&(l=0),i.push(l);let a=1/(c-2),d=-a,p=1+a,f=[d,d,p,d,p,p,d,d,p,p,d,p],m=6,g=6,y=3,h=2,u=1,E=new Float32Array(y*g*m),x=new Float32Array(h*g*m),_=new Float32Array(u*g*m);for(let N=0;N<m;N++){let w=N%3*2/3-1,O=N>2?0:-1,T=[w,O,0,w+2/3,O,0,w+2/3,O+1,0,w,O,0,w+2/3,O+1,0,w,O+1,0];E.set(T,y*g*N),x.set(f,h*g*N);let M=[N,N,N,N,N,N];_.set(M,u*g*N)}let A=new Tt;A.setAttribute("position",new Ut(E,y)),A.setAttribute("uv",new Ut(x,h)),A.setAttribute("faceIndex",new Ut(_,u)),e.push(A),r>ir&&r--}return{lodPlanes:e,sizeLods:t,sigmas:i}}function hu(n,e,t){let i=new yn(n,e,t);return i.texture.mapping=Wr,i.texture.name="PMREM.cubeUv",i.scissorTest=!0,i}function Go(n,e,t,i,r){n.viewport.set(e,t,i,r),n.scissor.set(e,t,i,r)}function om(n,e,t){let i=new Float32Array(xi),r=new Z(0,1,0);return new fn({name:"SphericalGaussianBlur",defines:{n:xi,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${n}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:i},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:r}},vertexShader:Mc(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform int samples;
			uniform float weights[ n ];
			uniform bool latitudinal;
			uniform float dTheta;
			uniform float mipInt;
			uniform vec3 poleAxis;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			vec3 getSample( float theta, vec3 axis ) {

				float cosTheta = cos( theta );
				// Rodrigues' axis-angle rotation
				vec3 sampleDirection = vOutputDirection * cosTheta
					+ cross( axis, vOutputDirection ) * sin( theta )
					+ axis * dot( axis, vOutputDirection ) * ( 1.0 - cosTheta );

				return bilinearCubeUV( envMap, sampleDirection, mipInt );

			}

			void main() {

				vec3 axis = latitudinal ? poleAxis : cross( poleAxis, vOutputDirection );

				if ( all( equal( axis, vec3( 0.0 ) ) ) ) {

					axis = vec3( vOutputDirection.z, 0.0, - vOutputDirection.x );

				}

				axis = normalize( axis );

				gl_FragColor = vec4( 0.0, 0.0, 0.0, 1.0 );
				gl_FragColor.rgb += weights[ 0 ] * getSample( 0.0, axis );

				for ( int i = 1; i < n; i++ ) {

					if ( i >= samples ) {

						break;

					}

					float theta = dTheta * float( i );
					gl_FragColor.rgb += weights[ i ] * getSample( -1.0 * theta, axis );
					gl_FragColor.rgb += weights[ i ] * getSample( theta, axis );

				}

			}
		`,blending:Nn,depthTest:!1,depthWrite:!1})}function du(){return new fn({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:Mc(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;

			#include <common>

			void main() {

				vec3 outputDirection = normalize( vOutputDirection );
				vec2 uv = equirectUv( outputDirection );

				gl_FragColor = vec4( texture2D ( envMap, uv ).rgb, 1.0 );

			}
		`,blending:Nn,depthTest:!1,depthWrite:!1})}function fu(){return new fn({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:Mc(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:Nn,depthTest:!1,depthWrite:!1})}function Mc(){return`

		precision mediump float;
		precision mediump int;

		attribute float faceIndex;

		varying vec3 vOutputDirection;

		// RH coordinate system; PMREM face-indexing convention
		vec3 getDirection( vec2 uv, float face ) {

			uv = 2.0 * uv - 1.0;

			vec3 direction = vec3( uv, 1.0 );

			if ( face == 0.0 ) {

				direction = direction.zyx; // ( 1, v, u ) pos x

			} else if ( face == 1.0 ) {

				direction = direction.xzy;
				direction.xz *= -1.0; // ( -u, 1, -v ) pos y

			} else if ( face == 2.0 ) {

				direction.x *= -1.0; // ( -u, v, 1 ) pos z

			} else if ( face == 3.0 ) {

				direction = direction.zyx;
				direction.xz *= -1.0; // ( -1, v, -u ) neg x

			} else if ( face == 4.0 ) {

				direction = direction.xzy;
				direction.xy *= -1.0; // ( -u, -1, v ) neg y

			} else if ( face == 5.0 ) {

				direction.z *= -1.0; // ( u, v, -1 ) neg z

			}

			return direction;

		}

		void main() {

			vOutputDirection = getDirection( uv, faceIndex );
			gl_Position = vec4( position, 1.0 );

		}
	`}function am(n){let e=new WeakMap,t=null;function i(c){if(c&&c.isTexture){let l=c.mapping,a=l===so||l===oo,d=l===pi||l===mi;if(a||d){let p=e.get(c),f=p!==void 0?p.texture.pmremVersion:0;if(c.isRenderTargetTexture&&c.pmremVersion!==f)return t===null&&(t=new Wo(n)),p=a?t.fromEquirectangular(c,p):t.fromCubemap(c,p),p.texture.pmremVersion=c.pmremVersion,e.set(c,p),p.texture;if(p!==void 0)return p.texture;{let m=c.image;return a&&m&&m.height>0||d&&m&&r(m)?(t===null&&(t=new Wo(n)),p=a?t.fromEquirectangular(c):t.fromCubemap(c),p.texture.pmremVersion=c.pmremVersion,e.set(c,p),c.addEventListener("dispose",s),p.texture):null}}}return c}function r(c){let l=0,a=6;for(let d=0;d<a;d++)c[d]!==void 0&&l++;return l===a}function s(c){let l=c.target;l.removeEventListener("dispose",s);let a=e.get(l);a!==void 0&&(e.delete(l),a.dispose())}function o(){e=new WeakMap,t!==null&&(t.dispose(),t=null)}return{get:i,dispose:o}}function cm(n){let e={};function t(i){if(e[i]!==void 0)return e[i];let r;switch(i){case"WEBGL_depth_texture":r=n.getExtension("WEBGL_depth_texture")||n.getExtension("MOZ_WEBGL_depth_texture")||n.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":r=n.getExtension("EXT_texture_filter_anisotropic")||n.getExtension("MOZ_EXT_texture_filter_anisotropic")||n.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":r=n.getExtension("WEBGL_compressed_texture_s3tc")||n.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":r=n.getExtension("WEBGL_compressed_texture_pvrtc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:r=n.getExtension(i)}return e[i]=r,r}return{has:function(i){return t(i)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(i){let r=t(i);return r===null&&li("THREE.WebGLRenderer: "+i+" extension not supported."),r}}}function lm(n,e,t,i){let r={},s=new WeakMap;function o(p){let f=p.target;f.index!==null&&e.remove(f.index);for(let g in f.attributes)e.remove(f.attributes[g]);f.removeEventListener("dispose",o),delete r[f.id];let m=s.get(f);m&&(e.remove(m),s.delete(f)),i.releaseStatesOfGeometry(f),f.isInstancedBufferGeometry===!0&&delete f._maxInstanceCount,t.memory.geometries--}function c(p,f){return r[f.id]===!0||(f.addEventListener("dispose",o),r[f.id]=!0,t.memory.geometries++),f}function l(p){let f=p.attributes;for(let m in f)e.update(f[m],n.ARRAY_BUFFER)}function a(p){let f=[],m=p.index,g=p.attributes.position,y=0;if(m!==null){let E=m.array;y=m.version;for(let x=0,_=E.length;x<_;x+=3){let A=E[x+0],N=E[x+1],w=E[x+2];f.push(A,N,N,w,w,A)}}else if(g!==void 0){let E=g.array;y=g.version;for(let x=0,_=E.length/3-1;x<_;x+=3){let A=x+0,N=x+1,w=x+2;f.push(A,N,N,w,w,A)}}else return;let h=new(sc(f)?Sr:Er)(f,1);h.version=y;let u=s.get(p);u&&e.remove(u),s.set(p,h)}function d(p){let f=s.get(p);if(f){let m=p.index;m!==null&&f.version<m.version&&a(p)}else a(p);return s.get(p)}return{get:c,update:l,getWireframeAttribute:d}}function um(n,e,t){let i;function r(f){i=f}let s,o;function c(f){s=f.type,o=f.bytesPerElement}function l(f,m){n.drawElements(i,m,s,f*o),t.update(m,i,1)}function a(f,m,g){g!==0&&(n.drawElementsInstanced(i,m,s,f*o,g),t.update(m,i,g))}function d(f,m,g){if(g===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(i,m,0,s,f,0,g);let h=0;for(let u=0;u<g;u++)h+=m[u];t.update(h,i,1)}function p(f,m,g,y){if(g===0)return;let h=e.get("WEBGL_multi_draw");if(h===null)for(let u=0;u<f.length;u++)a(f[u]/o,m[u],y[u]);else{h.multiDrawElementsInstancedWEBGL(i,m,0,s,f,0,y,0,g);let u=0;for(let E=0;E<g;E++)u+=m[E]*y[E];t.update(u,i,1)}}this.setMode=r,this.setIndex=c,this.render=l,this.renderInstances=a,this.renderMultiDraw=d,this.renderMultiDrawInstances=p}function hm(n){let e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function i(s,o,c){switch(t.calls++,o){case n.TRIANGLES:t.triangles+=c*(s/3);break;case n.LINES:t.lines+=c*(s/2);break;case n.LINE_STRIP:t.lines+=c*(s-1);break;case n.LINE_LOOP:t.lines+=c*s;break;case n.POINTS:t.points+=c*s;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",o);break}}function r(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:r,update:i}}function dm(n,e,t){let i=new WeakMap,r=new vt;function s(o,c,l){let a=o.morphTargetInfluences,d=c.morphAttributes.position||c.morphAttributes.normal||c.morphAttributes.color,p=d!==void 0?d.length:0,f=i.get(c);if(f===void 0||f.count!==p){let T=function(){w.dispose(),i.delete(c),c.removeEventListener("dispose",T)};f!==void 0&&f.texture.dispose();let m=c.morphAttributes.position!==void 0,g=c.morphAttributes.normal!==void 0,y=c.morphAttributes.color!==void 0,h=c.morphAttributes.position||[],u=c.morphAttributes.normal||[],E=c.morphAttributes.color||[],x=0;m===!0&&(x=1),g===!0&&(x=2),y===!0&&(x=3);let _=c.attributes.position.count*x,A=1;_>e.maxTextureSize&&(A=Math.ceil(_/e.maxTextureSize),_=e.maxTextureSize);let N=new Float32Array(_*A*4*p),w=new vr(N,_,A,p);w.type=Tn,w.needsUpdate=!0;let O=x*4;for(let M=0;M<p;M++){let R=h[M],I=u[M],U=E[M],P=_*A*4*M;for(let X=0;X<R.count;X++){let W=X*O;m===!0&&(r.fromBufferAttribute(R,X),N[P+W+0]=r.x,N[P+W+1]=r.y,N[P+W+2]=r.z,N[P+W+3]=0),g===!0&&(r.fromBufferAttribute(I,X),N[P+W+4]=r.x,N[P+W+5]=r.y,N[P+W+6]=r.z,N[P+W+7]=0),y===!0&&(r.fromBufferAttribute(U,X),N[P+W+8]=r.x,N[P+W+9]=r.y,N[P+W+10]=r.z,N[P+W+11]=U.itemSize===4?r.w:1)}}f={count:p,texture:w,size:new ze(_,A)},i.set(c,f),c.addEventListener("dispose",T)}if(o.isInstancedMesh===!0&&o.morphTexture!==null)l.getUniforms().setValue(n,"morphTexture",o.morphTexture,t);else{let m=0;for(let y=0;y<a.length;y++)m+=a[y];let g=c.morphTargetsRelative?1:1-m;l.getUniforms().setValue(n,"morphTargetBaseInfluence",g),l.getUniforms().setValue(n,"morphTargetInfluences",a)}l.getUniforms().setValue(n,"morphTargetsTexture",f.texture,t),l.getUniforms().setValue(n,"morphTargetsTextureSize",f.size)}return{update:s}}function fm(n,e,t,i){let r=new WeakMap;function s(l){let a=i.render.frame,d=l.geometry,p=e.get(l,d);if(r.get(p)!==a&&(e.update(p),r.set(p,a)),l.isInstancedMesh&&(l.hasEventListener("dispose",c)===!1&&l.addEventListener("dispose",c),r.get(l)!==a&&(t.update(l.instanceMatrix,n.ARRAY_BUFFER),l.instanceColor!==null&&t.update(l.instanceColor,n.ARRAY_BUFFER),r.set(l,a))),l.isSkinnedMesh){let f=l.skeleton;r.get(f)!==a&&(f.update(),r.set(f,a))}return p}function o(){r=new WeakMap}function c(l){let a=l.target;a.removeEventListener("dispose",c),t.remove(a.instanceMatrix),a.instanceColor!==null&&t.remove(a.instanceColor)}return{update:s,dispose:o}}var Lu=new Ft,pu=new wr(1,1),Nu=new vr,Ou=new Ns,Du=new Mr,mu=[],gu=[],_u=new Float32Array(16),yu=new Float32Array(9),vu=new Float32Array(4);function sr(n,e,t){let i=n[0];if(i<=0||i>0)return n;let r=e*t,s=mu[r];if(s===void 0&&(s=new Float32Array(r),mu[r]=s),e!==0){i.toArray(s,0);for(let o=1,c=0;o!==e;++o)c+=t,n[o].toArray(s,c)}return s}function Mt(n,e){if(n.length!==e.length)return!1;for(let t=0,i=n.length;t<i;t++)if(n[t]!==e[t])return!1;return!0}function bt(n,e){for(let t=0,i=e.length;t<i;t++)n[t]=e[t]}function qo(n,e){let t=gu[e];t===void 0&&(t=new Int32Array(e),gu[e]=t);for(let i=0;i!==e;++i)t[i]=n.allocateTextureUnit();return t}function pm(n,e){let t=this.cache;t[0]!==e&&(n.uniform1f(this.addr,e),t[0]=e)}function mm(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(Mt(t,e))return;n.uniform2fv(this.addr,e),bt(t,e)}}function gm(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(n.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(Mt(t,e))return;n.uniform3fv(this.addr,e),bt(t,e)}}function _m(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(Mt(t,e))return;n.uniform4fv(this.addr,e),bt(t,e)}}function ym(n,e){let t=this.cache,i=e.elements;if(i===void 0){if(Mt(t,e))return;n.uniformMatrix2fv(this.addr,!1,e),bt(t,e)}else{if(Mt(t,i))return;vu.set(i),n.uniformMatrix2fv(this.addr,!1,vu),bt(t,i)}}function vm(n,e){let t=this.cache,i=e.elements;if(i===void 0){if(Mt(t,e))return;n.uniformMatrix3fv(this.addr,!1,e),bt(t,e)}else{if(Mt(t,i))return;yu.set(i),n.uniformMatrix3fv(this.addr,!1,yu),bt(t,i)}}function xm(n,e){let t=this.cache,i=e.elements;if(i===void 0){if(Mt(t,e))return;n.uniformMatrix4fv(this.addr,!1,e),bt(t,e)}else{if(Mt(t,i))return;_u.set(i),n.uniformMatrix4fv(this.addr,!1,_u),bt(t,i)}}function Em(n,e){let t=this.cache;t[0]!==e&&(n.uniform1i(this.addr,e),t[0]=e)}function Sm(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(Mt(t,e))return;n.uniform2iv(this.addr,e),bt(t,e)}}function Tm(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(Mt(t,e))return;n.uniform3iv(this.addr,e),bt(t,e)}}function Mm(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(Mt(t,e))return;n.uniform4iv(this.addr,e),bt(t,e)}}function bm(n,e){let t=this.cache;t[0]!==e&&(n.uniform1ui(this.addr,e),t[0]=e)}function Am(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(Mt(t,e))return;n.uniform2uiv(this.addr,e),bt(t,e)}}function Rm(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(Mt(t,e))return;n.uniform3uiv(this.addr,e),bt(t,e)}}function wm(n,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(Mt(t,e))return;n.uniform4uiv(this.addr,e),bt(t,e)}}function Cm(n,e,t){let i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r);let s;this.type===n.SAMPLER_2D_SHADOW?(pu.compareFunction=tc,s=pu):s=Lu,t.setTexture2D(e||s,r)}function Im(n,e,t){let i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture3D(e||Ou,r)}function Pm(n,e,t){let i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTextureCube(e||Du,r)}function Lm(n,e,t){let i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture2DArray(e||Nu,r)}function Nm(n){switch(n){case 5126:return pm;case 35664:return mm;case 35665:return gm;case 35666:return _m;case 35674:return ym;case 35675:return vm;case 35676:return xm;case 5124:case 35670:return Em;case 35667:case 35671:return Sm;case 35668:case 35672:return Tm;case 35669:case 35673:return Mm;case 5125:return bm;case 36294:return Am;case 36295:return Rm;case 36296:return wm;case 35678:case 36198:case 36298:case 36306:case 35682:return Cm;case 35679:case 36299:case 36307:return Im;case 35680:case 36300:case 36308:case 36293:return Pm;case 36289:case 36303:case 36311:case 36292:return Lm}}function Om(n,e){n.uniform1fv(this.addr,e)}function Dm(n,e){let t=sr(e,this.size,2);n.uniform2fv(this.addr,t)}function Um(n,e){let t=sr(e,this.size,3);n.uniform3fv(this.addr,t)}function Fm(n,e){let t=sr(e,this.size,4);n.uniform4fv(this.addr,t)}function km(n,e){let t=sr(e,this.size,4);n.uniformMatrix2fv(this.addr,!1,t)}function Bm(n,e){let t=sr(e,this.size,9);n.uniformMatrix3fv(this.addr,!1,t)}function zm(n,e){let t=sr(e,this.size,16);n.uniformMatrix4fv(this.addr,!1,t)}function Vm(n,e){n.uniform1iv(this.addr,e)}function Gm(n,e){n.uniform2iv(this.addr,e)}function Hm(n,e){n.uniform3iv(this.addr,e)}function Wm(n,e){n.uniform4iv(this.addr,e)}function Xm(n,e){n.uniform1uiv(this.addr,e)}function Ym(n,e){n.uniform2uiv(this.addr,e)}function qm(n,e){n.uniform3uiv(this.addr,e)}function Km(n,e){n.uniform4uiv(this.addr,e)}function Zm(n,e,t){let i=this.cache,r=e.length,s=qo(t,r);Mt(i,s)||(n.uniform1iv(this.addr,s),bt(i,s));for(let o=0;o!==r;++o)t.setTexture2D(e[o]||Lu,s[o])}function jm(n,e,t){let i=this.cache,r=e.length,s=qo(t,r);Mt(i,s)||(n.uniform1iv(this.addr,s),bt(i,s));for(let o=0;o!==r;++o)t.setTexture3D(e[o]||Ou,s[o])}function Jm(n,e,t){let i=this.cache,r=e.length,s=qo(t,r);Mt(i,s)||(n.uniform1iv(this.addr,s),bt(i,s));for(let o=0;o!==r;++o)t.setTextureCube(e[o]||Du,s[o])}function $m(n,e,t){let i=this.cache,r=e.length,s=qo(t,r);Mt(i,s)||(n.uniform1iv(this.addr,s),bt(i,s));for(let o=0;o!==r;++o)t.setTexture2DArray(e[o]||Nu,s[o])}function Qm(n){switch(n){case 5126:return Om;case 35664:return Dm;case 35665:return Um;case 35666:return Fm;case 35674:return km;case 35675:return Bm;case 35676:return zm;case 5124:case 35670:return Vm;case 35667:case 35671:return Gm;case 35668:case 35672:return Hm;case 35669:case 35673:return Wm;case 5125:return Xm;case 36294:return Ym;case 36295:return qm;case 36296:return Km;case 35678:case 36198:case 36298:case 36306:case 35682:return Zm;case 35679:case 36299:case 36307:return jm;case 35680:case 36300:case 36308:case 36293:return Jm;case 36289:case 36303:case 36311:case 36292:return $m}}var gc=class{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.setValue=Nm(t.type)}},_c=class{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=Qm(t.type)}},yc=class{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,i){let r=this.seq;for(let s=0,o=r.length;s!==o;++s){let c=r[s];c.setValue(e,t[c.id],i)}}},mc=/(\w+)(\])?(\[|\.)?/g;function xu(n,e){n.seq.push(e),n.map[e.id]=e}function eg(n,e,t){let i=n.name,r=i.length;for(mc.lastIndex=0;;){let s=mc.exec(i),o=mc.lastIndex,c=s[1],l=s[2]==="]",a=s[3];if(l&&(c=c|0),a===void 0||a==="["&&o+2===r){xu(t,a===void 0?new gc(c,n,e):new _c(c,n,e));break}else{let p=t.map[c];p===void 0&&(p=new yc(c),xu(t,p)),t=p}}}var rr=class{constructor(e,t){this.seq=[],this.map={};let i=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let r=0;r<i;++r){let s=e.getActiveUniform(t,r),o=e.getUniformLocation(t,s.name);eg(s,o,this)}}setValue(e,t,i,r){let s=this.map[t];s!==void 0&&s.setValue(e,i,r)}setOptional(e,t,i){let r=t[i];r!==void 0&&this.setValue(e,i,r)}static upload(e,t,i,r){for(let s=0,o=t.length;s!==o;++s){let c=t[s],l=i[c.id];l.needsUpdate!==!1&&c.setValue(e,l.value,r)}}static seqWithValue(e,t){let i=[];for(let r=0,s=e.length;r!==s;++r){let o=e[r];o.id in t&&i.push(o)}return i}};function Eu(n,e,t){let i=n.createShader(e);return n.shaderSource(i,t),n.compileShader(i),i}var tg=37297,ng=0;function ig(n,e){let t=n.split(`
`),i=[],r=Math.max(e-6,0),s=Math.min(e+6,t.length);for(let o=r;o<s;o++){let c=o+1;i.push(`${c===e?">":" "} ${c}: ${t[o]}`)}return i.join(`
`)}var Su=new Ze;function rg(n){nt._getMatrix(Su,nt.workingColorSpace,n);let e=`mat3( ${Su.elements.map(t=>t.toFixed(4))} )`;switch(nt.getTransfer(n)){case _r:return[e,"LinearTransferOETF"];case at:return[e,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space: ",n),[e,"LinearTransferOETF"]}}function Tu(n,e,t){let i=n.getShaderParameter(e,n.COMPILE_STATUS),s=(n.getShaderInfoLog(e)||"").trim();if(i&&s==="")return"";let o=/ERROR: 0:(\d+)/.exec(s);if(o){let c=parseInt(o[1]);return t.toUpperCase()+`

`+s+`

`+ig(n.getShaderSource(e),c)}else return s}function sg(n,e){let t=rg(e);return[`vec4 ${n}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}function og(n,e){let t;switch(e){case Dl:t="Linear";break;case Ul:t="Reinhard";break;case Fl:t="Cineon";break;case kl:t="ACESFilmic";break;case zl:t="AgX";break;case Vl:t="Neutral";break;case Bl:t="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),t="Linear"}return"vec3 "+n+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}var Ho=new Z;function ag(){nt.getLuminanceCoefficients(Ho);let n=Ho.x.toFixed(4),e=Ho.y.toFixed(4),t=Ho.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${n}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function cg(n){return[n.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",n.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Jr).join(`
`)}function lg(n){let e=[];for(let t in n){let i=n[t];i!==!1&&e.push("#define "+t+" "+i)}return e.join(`
`)}function ug(n,e){let t={},i=n.getProgramParameter(e,n.ACTIVE_ATTRIBUTES);for(let r=0;r<i;r++){let s=n.getActiveAttrib(e,r),o=s.name,c=1;s.type===n.FLOAT_MAT2&&(c=2),s.type===n.FLOAT_MAT3&&(c=3),s.type===n.FLOAT_MAT4&&(c=4),t[o]={type:s.type,location:n.getAttribLocation(e,o),locationSize:c}}return t}function Jr(n){return n!==""}function Mu(n,e){let t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return n.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function bu(n,e){return n.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}var hg=/^[ \t]*#include +<([\w\d./]+)>/gm;function vc(n){return n.replace(hg,fg)}var dg=new Map;function fg(n,e){let t=$e[e];if(t===void 0){let i=dg.get(e);if(i!==void 0)t=$e[i],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,i);else throw new Error("Can not resolve #include <"+e+">")}return vc(t)}var pg=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function Au(n){return n.replace(pg,mg)}function mg(n,e,t,i){let r="";for(let s=parseInt(e);s<parseInt(t);s++)r+=i.replace(/\[\s*i\s*\]/g,"[ "+s+" ]").replace(/UNROLLED_LOOP_INDEX/g,s);return r}function Ru(n){let e=`precision ${n.precision} float;
	precision ${n.precision} int;
	precision ${n.precision} sampler2D;
	precision ${n.precision} samplerCube;
	precision ${n.precision} sampler3D;
	precision ${n.precision} sampler2DArray;
	precision ${n.precision} sampler2DShadow;
	precision ${n.precision} samplerCubeShadow;
	precision ${n.precision} sampler2DArrayShadow;
	precision ${n.precision} isampler2D;
	precision ${n.precision} isampler3D;
	precision ${n.precision} isamplerCube;
	precision ${n.precision} isampler2DArray;
	precision ${n.precision} usampler2D;
	precision ${n.precision} usampler3D;
	precision ${n.precision} usamplerCube;
	precision ${n.precision} usampler2DArray;
	`;return n.precision==="highp"?e+=`
#define HIGH_PRECISION`:n.precision==="mediump"?e+=`
#define MEDIUM_PRECISION`:n.precision==="lowp"&&(e+=`
#define LOW_PRECISION`),e}function gg(n){let e="SHADOWMAP_TYPE_BASIC";return n.shadowMapType===Va?e="SHADOWMAP_TYPE_PCF":n.shadowMapType===pl?e="SHADOWMAP_TYPE_PCF_SOFT":n.shadowMapType===Sn&&(e="SHADOWMAP_TYPE_VSM"),e}function _g(n){let e="ENVMAP_TYPE_CUBE";if(n.envMap)switch(n.envMapMode){case pi:case mi:e="ENVMAP_TYPE_CUBE";break;case Wr:e="ENVMAP_TYPE_CUBE_UV";break}return e}function yg(n){let e="ENVMAP_MODE_REFLECTION";return n.envMap&&n.envMapMode===mi&&(e="ENVMAP_MODE_REFRACTION"),e}function vg(n){let e="ENVMAP_BLENDING_NONE";if(n.envMap)switch(n.combine){case ro:e="ENVMAP_BLENDING_MULTIPLY";break;case Nl:e="ENVMAP_BLENDING_MIX";break;case Ol:e="ENVMAP_BLENDING_ADD";break}return e}function xg(n){let e=n.envMapCubeUVHeight;if(e===null)return null;let t=Math.log2(e)-2,i=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),112)),texelHeight:i,maxMip:t}}function Eg(n,e,t,i){let r=n.getContext(),s=t.defines,o=t.vertexShader,c=t.fragmentShader,l=gg(t),a=_g(t),d=yg(t),p=vg(t),f=xg(t),m=cg(t),g=lg(s),y=r.createProgram(),h,u,E=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(h=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Jr).join(`
`),h.length>0&&(h+=`
`),u=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Jr).join(`
`),u.length>0&&(u+=`
`)):(h=[Ru(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+d:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+l:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reversedDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Jr).join(`
`),u=[Ru(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+a:"",t.envMap?"#define "+d:"",t.envMap?"#define "+p:"",f?"#define CUBEUV_TEXEL_WIDTH "+f.texelWidth:"",f?"#define CUBEUV_TEXEL_HEIGHT "+f.texelHeight:"",f?"#define CUBEUV_MAX_MIP "+f.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor||t.batchingColor?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+l:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reversedDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==On?"#define TONE_MAPPING":"",t.toneMapping!==On?$e.tonemapping_pars_fragment:"",t.toneMapping!==On?og("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",$e.colorspace_pars_fragment,sg("linearToOutputTexel",t.outputColorSpace),ag(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(Jr).join(`
`)),o=vc(o),o=Mu(o,t),o=bu(o,t),c=vc(c),c=Mu(c,t),c=bu(c,t),o=Au(o),c=Au(c),t.isRawShaderMaterial!==!0&&(E=`#version 300 es
`,h=[m,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+h,u=["#define varying in",t.glslVersion===nc?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===nc?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+u);let x=E+h+o,_=E+u+c,A=Eu(r,r.VERTEX_SHADER,x),N=Eu(r,r.FRAGMENT_SHADER,_);r.attachShader(y,A),r.attachShader(y,N),t.index0AttributeName!==void 0?r.bindAttribLocation(y,0,t.index0AttributeName):t.morphTargets===!0&&r.bindAttribLocation(y,0,"position"),r.linkProgram(y);function w(R){if(n.debug.checkShaderErrors){let I=r.getProgramInfoLog(y)||"",U=r.getShaderInfoLog(A)||"",P=r.getShaderInfoLog(N)||"",X=I.trim(),W=U.trim(),q=P.trim(),G=!0,ee=!0;if(r.getProgramParameter(y,r.LINK_STATUS)===!1)if(G=!1,typeof n.debug.onShaderError=="function")n.debug.onShaderError(r,y,A,N);else{let ae=Tu(r,A,"vertex"),ue=Tu(r,N,"fragment");console.error("THREE.WebGLProgram: Shader Error "+r.getError()+" - VALIDATE_STATUS "+r.getProgramParameter(y,r.VALIDATE_STATUS)+`

Material Name: `+R.name+`
Material Type: `+R.type+`

Program Info Log: `+X+`
`+ae+`
`+ue)}else X!==""?console.warn("THREE.WebGLProgram: Program Info Log:",X):(W===""||q==="")&&(ee=!1);ee&&(R.diagnostics={runnable:G,programLog:X,vertexShader:{log:W,prefix:h},fragmentShader:{log:q,prefix:u}})}r.deleteShader(A),r.deleteShader(N),O=new rr(r,y),T=ug(r,y)}let O;this.getUniforms=function(){return O===void 0&&w(this),O};let T;this.getAttributes=function(){return T===void 0&&w(this),T};let M=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return M===!1&&(M=r.getProgramParameter(y,tg)),M},this.destroy=function(){i.releaseStatesOfProgram(this),r.deleteProgram(y),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=ng++,this.cacheKey=e,this.usedTimes=1,this.program=y,this.vertexShader=A,this.fragmentShader=N,this}var Sg=0,xc=class{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){let t=e.vertexShader,i=e.fragmentShader,r=this._getShaderStage(t),s=this._getShaderStage(i),o=this._getShaderCacheForMaterial(e);return o.has(r)===!1&&(o.add(r),r.usedTimes++),o.has(s)===!1&&(o.add(s),s.usedTimes++),this}remove(e){let t=this.materialCache.get(e);for(let i of t)i.usedTimes--,i.usedTimes===0&&this.shaderCache.delete(i.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){let t=this.materialCache,i=t.get(e);return i===void 0&&(i=new Set,t.set(e,i)),i}_getShaderStage(e){let t=this.shaderCache,i=t.get(e);return i===void 0&&(i=new Ec(e),t.set(e,i)),i}},Ec=class{constructor(e){this.id=Sg++,this.code=e,this.usedTimes=0}};function Tg(n,e,t,i,r,s,o){let c=new xr,l=new xc,a=new Set,d=[],p=r.logarithmicDepthBuffer,f=r.vertexTextures,m=r.precision,g={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function y(T){return a.add(T),T===0?"uv":`uv${T}`}function h(T,M,R,I,U){let P=I.fog,X=U.geometry,W=T.isMeshStandardMaterial?I.environment:null,q=(T.isMeshStandardMaterial?t:e).get(T.envMap||W),G=q&&q.mapping===Wr?q.image.height:null,ee=g[T.type];T.precision!==null&&(m=r.getMaxPrecision(T.precision),m!==T.precision&&console.warn("THREE.WebGLProgram.getParameters:",T.precision,"not supported, using",m,"instead."));let ae=X.morphAttributes.position||X.morphAttributes.normal||X.morphAttributes.color,ue=ae!==void 0?ae.length:0,_e=0;X.morphAttributes.position!==void 0&&(_e=1),X.morphAttributes.normal!==void 0&&(_e=2),X.morphAttributes.color!==void 0&&(_e=3);let me,Me,k,Y;if(ee){let ve=Mn[ee];me=ve.vertexShader,Me=ve.fragmentShader}else me=T.vertexShader,Me=T.fragmentShader,l.update(T),k=l.getVertexShaderID(T),Y=l.getFragmentShaderID(T);let K=n.getRenderTarget(),ne=n.state.buffers.depth.getReversed(),ie=U.isInstancedMesh===!0,de=U.isBatchedMesh===!0,Le=!!T.map,we=!!T.matcap,B=!!q,Ge=!!T.aoMap,Ne=!!T.lightMap,Ke=!!T.bumpMap,Oe=!!T.normalMap,Je=!!T.displacementMap,Re=!!T.emissiveMap,He=!!T.metalnessMap,ot=!!T.roughnessMap,it=T.anisotropy>0,S=T.clearcoat>0,v=T.dispersion>0,b=T.iridescence>0,D=T.sheen>0,L=T.transmission>0,F=it&&!!T.anisotropyMap,H=S&&!!T.clearcoatMap,z=S&&!!T.clearcoatNormalMap,j=S&&!!T.clearcoatRoughnessMap,te=b&&!!T.iridescenceMap,Q=b&&!!T.iridescenceThicknessMap,ce=D&&!!T.sheenColorMap,Ee=D&&!!T.sheenRoughnessMap,Se=!!T.specularMap,pe=!!T.specularColorMap,xe=!!T.specularIntensityMap,V=L&&!!T.transmissionMap,le=L&&!!T.thicknessMap,fe=!!T.gradientMap,ge=!!T.alphaMap,he=T.alphaTest>0,oe=!!T.alphaHash,Te=!!T.extensions,Fe=On;T.toneMapped&&(K===null||K.isXRRenderTarget===!0)&&(Fe=n.toneMapping);let De={shaderID:ee,shaderType:T.type,shaderName:T.name,vertexShader:me,fragmentShader:Me,defines:T.defines,customVertexShaderID:k,customFragmentShaderID:Y,isRawShaderMaterial:T.isRawShaderMaterial===!0,glslVersion:T.glslVersion,precision:m,batching:de,batchingColor:de&&U._colorsTexture!==null,instancing:ie,instancingColor:ie&&U.instanceColor!==null,instancingMorph:ie&&U.morphTexture!==null,supportsVertexTextures:f,outputColorSpace:K===null?n.outputColorSpace:K.isXRRenderTarget===!0?K.texture.colorSpace:ci,alphaToCoverage:!!T.alphaToCoverage,map:Le,matcap:we,envMap:B,envMapMode:B&&q.mapping,envMapCubeUVHeight:G,aoMap:Ge,lightMap:Ne,bumpMap:Ke,normalMap:Oe,displacementMap:f&&Je,emissiveMap:Re,normalMapObjectSpace:Oe&&T.normalMapType===Xl,normalMapTangentSpace:Oe&&T.normalMapType===ec,metalnessMap:He,roughnessMap:ot,anisotropy:it,anisotropyMap:F,clearcoat:S,clearcoatMap:H,clearcoatNormalMap:z,clearcoatRoughnessMap:j,dispersion:v,iridescence:b,iridescenceMap:te,iridescenceThicknessMap:Q,sheen:D,sheenColorMap:ce,sheenRoughnessMap:Ee,specularMap:Se,specularColorMap:pe,specularIntensityMap:xe,transmission:L,transmissionMap:V,thicknessMap:le,gradientMap:fe,opaque:T.transparent===!1&&T.blending===oi&&T.alphaToCoverage===!1,alphaMap:ge,alphaTest:he,alphaHash:oe,combine:T.combine,mapUv:Le&&y(T.map.channel),aoMapUv:Ge&&y(T.aoMap.channel),lightMapUv:Ne&&y(T.lightMap.channel),bumpMapUv:Ke&&y(T.bumpMap.channel),normalMapUv:Oe&&y(T.normalMap.channel),displacementMapUv:Je&&y(T.displacementMap.channel),emissiveMapUv:Re&&y(T.emissiveMap.channel),metalnessMapUv:He&&y(T.metalnessMap.channel),roughnessMapUv:ot&&y(T.roughnessMap.channel),anisotropyMapUv:F&&y(T.anisotropyMap.channel),clearcoatMapUv:H&&y(T.clearcoatMap.channel),clearcoatNormalMapUv:z&&y(T.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:j&&y(T.clearcoatRoughnessMap.channel),iridescenceMapUv:te&&y(T.iridescenceMap.channel),iridescenceThicknessMapUv:Q&&y(T.iridescenceThicknessMap.channel),sheenColorMapUv:ce&&y(T.sheenColorMap.channel),sheenRoughnessMapUv:Ee&&y(T.sheenRoughnessMap.channel),specularMapUv:Se&&y(T.specularMap.channel),specularColorMapUv:pe&&y(T.specularColorMap.channel),specularIntensityMapUv:xe&&y(T.specularIntensityMap.channel),transmissionMapUv:V&&y(T.transmissionMap.channel),thicknessMapUv:le&&y(T.thicknessMap.channel),alphaMapUv:ge&&y(T.alphaMap.channel),vertexTangents:!!X.attributes.tangent&&(Oe||it),vertexColors:T.vertexColors,vertexAlphas:T.vertexColors===!0&&!!X.attributes.color&&X.attributes.color.itemSize===4,pointsUvs:U.isPoints===!0&&!!X.attributes.uv&&(Le||ge),fog:!!P,useFog:T.fog===!0,fogExp2:!!P&&P.isFogExp2,flatShading:T.flatShading===!0&&T.wireframe===!1,sizeAttenuation:T.sizeAttenuation===!0,logarithmicDepthBuffer:p,reversedDepthBuffer:ne,skinning:U.isSkinnedMesh===!0,morphTargets:X.morphAttributes.position!==void 0,morphNormals:X.morphAttributes.normal!==void 0,morphColors:X.morphAttributes.color!==void 0,morphTargetsCount:ue,morphTextureStride:_e,numDirLights:M.directional.length,numPointLights:M.point.length,numSpotLights:M.spot.length,numSpotLightMaps:M.spotLightMap.length,numRectAreaLights:M.rectArea.length,numHemiLights:M.hemi.length,numDirLightShadows:M.directionalShadowMap.length,numPointLightShadows:M.pointShadowMap.length,numSpotLightShadows:M.spotShadowMap.length,numSpotLightShadowsWithMaps:M.numSpotLightShadowsWithMaps,numLightProbes:M.numLightProbes,numClippingPlanes:o.numPlanes,numClipIntersection:o.numIntersection,dithering:T.dithering,shadowMapEnabled:n.shadowMap.enabled&&R.length>0,shadowMapType:n.shadowMap.type,toneMapping:Fe,decodeVideoTexture:Le&&T.map.isVideoTexture===!0&&nt.getTransfer(T.map.colorSpace)===at,decodeVideoTextureEmissive:Re&&T.emissiveMap.isVideoTexture===!0&&nt.getTransfer(T.emissiveMap.colorSpace)===at,premultipliedAlpha:T.premultipliedAlpha,doubleSided:T.side===en,flipSided:T.side===wt,useDepthPacking:T.depthPacking>=0,depthPacking:T.depthPacking||0,index0AttributeName:T.index0AttributeName,extensionClipCullDistance:Te&&T.extensions.clipCullDistance===!0&&i.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(Te&&T.extensions.multiDraw===!0||de)&&i.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:i.has("KHR_parallel_shader_compile"),customProgramCacheKey:T.customProgramCacheKey()};return De.vertexUv1s=a.has(1),De.vertexUv2s=a.has(2),De.vertexUv3s=a.has(3),a.clear(),De}function u(T){let M=[];if(T.shaderID?M.push(T.shaderID):(M.push(T.customVertexShaderID),M.push(T.customFragmentShaderID)),T.defines!==void 0)for(let R in T.defines)M.push(R),M.push(T.defines[R]);return T.isRawShaderMaterial===!1&&(E(M,T),x(M,T),M.push(n.outputColorSpace)),M.push(T.customProgramCacheKey),M.join()}function E(T,M){T.push(M.precision),T.push(M.outputColorSpace),T.push(M.envMapMode),T.push(M.envMapCubeUVHeight),T.push(M.mapUv),T.push(M.alphaMapUv),T.push(M.lightMapUv),T.push(M.aoMapUv),T.push(M.bumpMapUv),T.push(M.normalMapUv),T.push(M.displacementMapUv),T.push(M.emissiveMapUv),T.push(M.metalnessMapUv),T.push(M.roughnessMapUv),T.push(M.anisotropyMapUv),T.push(M.clearcoatMapUv),T.push(M.clearcoatNormalMapUv),T.push(M.clearcoatRoughnessMapUv),T.push(M.iridescenceMapUv),T.push(M.iridescenceThicknessMapUv),T.push(M.sheenColorMapUv),T.push(M.sheenRoughnessMapUv),T.push(M.specularMapUv),T.push(M.specularColorMapUv),T.push(M.specularIntensityMapUv),T.push(M.transmissionMapUv),T.push(M.thicknessMapUv),T.push(M.combine),T.push(M.fogExp2),T.push(M.sizeAttenuation),T.push(M.morphTargetsCount),T.push(M.morphAttributeCount),T.push(M.numDirLights),T.push(M.numPointLights),T.push(M.numSpotLights),T.push(M.numSpotLightMaps),T.push(M.numHemiLights),T.push(M.numRectAreaLights),T.push(M.numDirLightShadows),T.push(M.numPointLightShadows),T.push(M.numSpotLightShadows),T.push(M.numSpotLightShadowsWithMaps),T.push(M.numLightProbes),T.push(M.shadowMapType),T.push(M.toneMapping),T.push(M.numClippingPlanes),T.push(M.numClipIntersection),T.push(M.depthPacking)}function x(T,M){c.disableAll(),M.supportsVertexTextures&&c.enable(0),M.instancing&&c.enable(1),M.instancingColor&&c.enable(2),M.instancingMorph&&c.enable(3),M.matcap&&c.enable(4),M.envMap&&c.enable(5),M.normalMapObjectSpace&&c.enable(6),M.normalMapTangentSpace&&c.enable(7),M.clearcoat&&c.enable(8),M.iridescence&&c.enable(9),M.alphaTest&&c.enable(10),M.vertexColors&&c.enable(11),M.vertexAlphas&&c.enable(12),M.vertexUv1s&&c.enable(13),M.vertexUv2s&&c.enable(14),M.vertexUv3s&&c.enable(15),M.vertexTangents&&c.enable(16),M.anisotropy&&c.enable(17),M.alphaHash&&c.enable(18),M.batching&&c.enable(19),M.dispersion&&c.enable(20),M.batchingColor&&c.enable(21),M.gradientMap&&c.enable(22),T.push(c.mask),c.disableAll(),M.fog&&c.enable(0),M.useFog&&c.enable(1),M.flatShading&&c.enable(2),M.logarithmicDepthBuffer&&c.enable(3),M.reversedDepthBuffer&&c.enable(4),M.skinning&&c.enable(5),M.morphTargets&&c.enable(6),M.morphNormals&&c.enable(7),M.morphColors&&c.enable(8),M.premultipliedAlpha&&c.enable(9),M.shadowMapEnabled&&c.enable(10),M.doubleSided&&c.enable(11),M.flipSided&&c.enable(12),M.useDepthPacking&&c.enable(13),M.dithering&&c.enable(14),M.transmission&&c.enable(15),M.sheen&&c.enable(16),M.opaque&&c.enable(17),M.pointsUvs&&c.enable(18),M.decodeVideoTexture&&c.enable(19),M.decodeVideoTextureEmissive&&c.enable(20),M.alphaToCoverage&&c.enable(21),T.push(c.mask)}function _(T){let M=g[T.type],R;if(M){let I=Mn[M];R=nu.clone(I.uniforms)}else R=T.uniforms;return R}function A(T,M){let R;for(let I=0,U=d.length;I<U;I++){let P=d[I];if(P.cacheKey===M){R=P,++R.usedTimes;break}}return R===void 0&&(R=new Eg(n,M,T,s),d.push(R)),R}function N(T){if(--T.usedTimes===0){let M=d.indexOf(T);d[M]=d[d.length-1],d.pop(),T.destroy()}}function w(T){l.remove(T)}function O(){l.dispose()}return{getParameters:h,getProgramCacheKey:u,getUniforms:_,acquireProgram:A,releaseProgram:N,releaseShaderCache:w,programs:d,dispose:O}}function Mg(){let n=new WeakMap;function e(o){return n.has(o)}function t(o){let c=n.get(o);return c===void 0&&(c={},n.set(o,c)),c}function i(o){n.delete(o)}function r(o,c,l){n.get(o)[c]=l}function s(){n=new WeakMap}return{has:e,get:t,remove:i,update:r,dispose:s}}function bg(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.material.id!==e.material.id?n.material.id-e.material.id:n.z!==e.z?n.z-e.z:n.id-e.id}function wu(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.z!==e.z?e.z-n.z:n.id-e.id}function Cu(){let n=[],e=0,t=[],i=[],r=[];function s(){e=0,t.length=0,i.length=0,r.length=0}function o(p,f,m,g,y,h){let u=n[e];return u===void 0?(u={id:p.id,object:p,geometry:f,material:m,groupOrder:g,renderOrder:p.renderOrder,z:y,group:h},n[e]=u):(u.id=p.id,u.object=p,u.geometry=f,u.material=m,u.groupOrder=g,u.renderOrder=p.renderOrder,u.z=y,u.group=h),e++,u}function c(p,f,m,g,y,h){let u=o(p,f,m,g,y,h);m.transmission>0?i.push(u):m.transparent===!0?r.push(u):t.push(u)}function l(p,f,m,g,y,h){let u=o(p,f,m,g,y,h);m.transmission>0?i.unshift(u):m.transparent===!0?r.unshift(u):t.unshift(u)}function a(p,f){t.length>1&&t.sort(p||bg),i.length>1&&i.sort(f||wu),r.length>1&&r.sort(f||wu)}function d(){for(let p=e,f=n.length;p<f;p++){let m=n[p];if(m.id===null)break;m.id=null,m.object=null,m.geometry=null,m.material=null,m.group=null}}return{opaque:t,transmissive:i,transparent:r,init:s,push:c,unshift:l,finish:d,sort:a}}function Ag(){let n=new WeakMap;function e(i,r){let s=n.get(i),o;return s===void 0?(o=new Cu,n.set(i,[o])):r>=s.length?(o=new Cu,s.push(o)):o=s[r],o}function t(){n=new WeakMap}return{get:e,dispose:t}}function Rg(){let n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={direction:new Z,color:new qe};break;case"SpotLight":t={position:new Z,direction:new Z,color:new qe,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new Z,color:new qe,distance:0,decay:0};break;case"HemisphereLight":t={direction:new Z,skyColor:new qe,groundColor:new qe};break;case"RectAreaLight":t={color:new qe,position:new Z,halfWidth:new Z,halfHeight:new Z};break}return n[e.id]=t,t}}}function wg(){let n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new ze};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new ze};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new ze,shadowCameraNear:1,shadowCameraFar:1e3};break}return n[e.id]=t,t}}}var Cg=0;function Ig(n,e){return(e.castShadow?2:0)-(n.castShadow?2:0)+(e.map?1:0)-(n.map?1:0)}function Pg(n){let e=new Rg,t=wg(),i={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let a=0;a<9;a++)i.probe.push(new Z);let r=new Z,s=new yt,o=new yt;function c(a){let d=0,p=0,f=0;for(let T=0;T<9;T++)i.probe[T].set(0,0,0);let m=0,g=0,y=0,h=0,u=0,E=0,x=0,_=0,A=0,N=0,w=0;a.sort(Ig);for(let T=0,M=a.length;T<M;T++){let R=a[T],I=R.color,U=R.intensity,P=R.distance,X=R.shadow&&R.shadow.map?R.shadow.map.texture:null;if(R.isAmbientLight)d+=I.r*U,p+=I.g*U,f+=I.b*U;else if(R.isLightProbe){for(let W=0;W<9;W++)i.probe[W].addScaledVector(R.sh.coefficients[W],U);w++}else if(R.isDirectionalLight){let W=e.get(R);if(W.color.copy(R.color).multiplyScalar(R.intensity),R.castShadow){let q=R.shadow,G=t.get(R);G.shadowIntensity=q.intensity,G.shadowBias=q.bias,G.shadowNormalBias=q.normalBias,G.shadowRadius=q.radius,G.shadowMapSize=q.mapSize,i.directionalShadow[m]=G,i.directionalShadowMap[m]=X,i.directionalShadowMatrix[m]=R.shadow.matrix,E++}i.directional[m]=W,m++}else if(R.isSpotLight){let W=e.get(R);W.position.setFromMatrixPosition(R.matrixWorld),W.color.copy(I).multiplyScalar(U),W.distance=P,W.coneCos=Math.cos(R.angle),W.penumbraCos=Math.cos(R.angle*(1-R.penumbra)),W.decay=R.decay,i.spot[y]=W;let q=R.shadow;if(R.map&&(i.spotLightMap[A]=R.map,A++,q.updateMatrices(R),R.castShadow&&N++),i.spotLightMatrix[y]=q.matrix,R.castShadow){let G=t.get(R);G.shadowIntensity=q.intensity,G.shadowBias=q.bias,G.shadowNormalBias=q.normalBias,G.shadowRadius=q.radius,G.shadowMapSize=q.mapSize,i.spotShadow[y]=G,i.spotShadowMap[y]=X,_++}y++}else if(R.isRectAreaLight){let W=e.get(R);W.color.copy(I).multiplyScalar(U),W.halfWidth.set(R.width*.5,0,0),W.halfHeight.set(0,R.height*.5,0),i.rectArea[h]=W,h++}else if(R.isPointLight){let W=e.get(R);if(W.color.copy(R.color).multiplyScalar(R.intensity),W.distance=R.distance,W.decay=R.decay,R.castShadow){let q=R.shadow,G=t.get(R);G.shadowIntensity=q.intensity,G.shadowBias=q.bias,G.shadowNormalBias=q.normalBias,G.shadowRadius=q.radius,G.shadowMapSize=q.mapSize,G.shadowCameraNear=q.camera.near,G.shadowCameraFar=q.camera.far,i.pointShadow[g]=G,i.pointShadowMap[g]=X,i.pointShadowMatrix[g]=R.shadow.matrix,x++}i.point[g]=W,g++}else if(R.isHemisphereLight){let W=e.get(R);W.skyColor.copy(R.color).multiplyScalar(U),W.groundColor.copy(R.groundColor).multiplyScalar(U),i.hemi[u]=W,u++}}h>0&&(n.has("OES_texture_float_linear")===!0?(i.rectAreaLTC1=Ae.LTC_FLOAT_1,i.rectAreaLTC2=Ae.LTC_FLOAT_2):(i.rectAreaLTC1=Ae.LTC_HALF_1,i.rectAreaLTC2=Ae.LTC_HALF_2)),i.ambient[0]=d,i.ambient[1]=p,i.ambient[2]=f;let O=i.hash;(O.directionalLength!==m||O.pointLength!==g||O.spotLength!==y||O.rectAreaLength!==h||O.hemiLength!==u||O.numDirectionalShadows!==E||O.numPointShadows!==x||O.numSpotShadows!==_||O.numSpotMaps!==A||O.numLightProbes!==w)&&(i.directional.length=m,i.spot.length=y,i.rectArea.length=h,i.point.length=g,i.hemi.length=u,i.directionalShadow.length=E,i.directionalShadowMap.length=E,i.pointShadow.length=x,i.pointShadowMap.length=x,i.spotShadow.length=_,i.spotShadowMap.length=_,i.directionalShadowMatrix.length=E,i.pointShadowMatrix.length=x,i.spotLightMatrix.length=_+A-N,i.spotLightMap.length=A,i.numSpotLightShadowsWithMaps=N,i.numLightProbes=w,O.directionalLength=m,O.pointLength=g,O.spotLength=y,O.rectAreaLength=h,O.hemiLength=u,O.numDirectionalShadows=E,O.numPointShadows=x,O.numSpotShadows=_,O.numSpotMaps=A,O.numLightProbes=w,i.version=Cg++)}function l(a,d){let p=0,f=0,m=0,g=0,y=0,h=d.matrixWorldInverse;for(let u=0,E=a.length;u<E;u++){let x=a[u];if(x.isDirectionalLight){let _=i.directional[p];_.direction.setFromMatrixPosition(x.matrixWorld),r.setFromMatrixPosition(x.target.matrixWorld),_.direction.sub(r),_.direction.transformDirection(h),p++}else if(x.isSpotLight){let _=i.spot[m];_.position.setFromMatrixPosition(x.matrixWorld),_.position.applyMatrix4(h),_.direction.setFromMatrixPosition(x.matrixWorld),r.setFromMatrixPosition(x.target.matrixWorld),_.direction.sub(r),_.direction.transformDirection(h),m++}else if(x.isRectAreaLight){let _=i.rectArea[g];_.position.setFromMatrixPosition(x.matrixWorld),_.position.applyMatrix4(h),o.identity(),s.copy(x.matrixWorld),s.premultiply(h),o.extractRotation(s),_.halfWidth.set(x.width*.5,0,0),_.halfHeight.set(0,x.height*.5,0),_.halfWidth.applyMatrix4(o),_.halfHeight.applyMatrix4(o),g++}else if(x.isPointLight){let _=i.point[f];_.position.setFromMatrixPosition(x.matrixWorld),_.position.applyMatrix4(h),f++}else if(x.isHemisphereLight){let _=i.hemi[y];_.direction.setFromMatrixPosition(x.matrixWorld),_.direction.transformDirection(h),y++}}}return{setup:c,setupView:l,state:i}}function Iu(n){let e=new Pg(n),t=[],i=[];function r(d){a.camera=d,t.length=0,i.length=0}function s(d){t.push(d)}function o(d){i.push(d)}function c(){e.setup(t)}function l(d){e.setupView(t,d)}let a={lightsArray:t,shadowsArray:i,camera:null,lights:e,transmissionRenderTarget:{}};return{init:r,state:a,setupLights:c,setupLightsView:l,pushLight:s,pushShadow:o}}function Lg(n){let e=new WeakMap;function t(r,s=0){let o=e.get(r),c;return o===void 0?(c=new Iu(n),e.set(r,[c])):s>=o.length?(c=new Iu(n),o.push(c)):c=o[s],c}function i(){e=new WeakMap}return{get:t,dispose:i}}var Ng=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,Og=`uniform sampler2D shadow_pass;
uniform vec2 resolution;
uniform float radius;
#include <packing>
void main() {
	const float samples = float( VSM_SAMPLES );
	float mean = 0.0;
	float squared_mean = 0.0;
	float uvStride = samples <= 1.0 ? 0.0 : 2.0 / ( samples - 1.0 );
	float uvStart = samples <= 1.0 ? 0.0 : - 1.0;
	for ( float i = 0.0; i < samples; i ++ ) {
		float uvOffset = uvStart + i * uvStride;
		#ifdef HORIZONTAL_PASS
			vec2 distribution = unpackRGBATo2Half( texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( uvOffset, 0.0 ) * radius ) / resolution ) );
			mean += distribution.x;
			squared_mean += distribution.y * distribution.y + distribution.x * distribution.x;
		#else
			float depth = unpackRGBAToDepth( texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( 0.0, uvOffset ) * radius ) / resolution ) );
			mean += depth;
			squared_mean += depth * depth;
		#endif
	}
	mean = mean / samples;
	squared_mean = squared_mean / samples;
	float std_dev = sqrt( squared_mean - mean * mean );
	gl_FragColor = pack2HalfToRGBA( vec2( mean, std_dev ) );
}`;function Dg(n,e,t){let i=new Wi,r=new ze,s=new ze,o=new vt,c=new Bs({depthPacking:Wl}),l=new zs,a={},d=t.maxTextureSize,p={[un]:wt,[wt]:un,[en]:en},f=new fn({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new ze},radius:{value:4}},vertexShader:Ng,fragmentShader:Og}),m=f.clone();m.defines.HORIZONTAL_PASS=1;let g=new Tt;g.setAttribute("position",new Ut(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));let y=new Lt(g,f),h=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=Va;let u=this.type;this.render=function(N,w,O){if(h.enabled===!1||h.autoUpdate===!1&&h.needsUpdate===!1||N.length===0)return;let T=n.getRenderTarget(),M=n.getActiveCubeFace(),R=n.getActiveMipmapLevel(),I=n.state;I.setBlending(Nn),I.buffers.depth.getReversed()?I.buffers.color.setClear(0,0,0,0):I.buffers.color.setClear(1,1,1,1),I.buffers.depth.setTest(!0),I.setScissorTest(!1);let U=u!==Sn&&this.type===Sn,P=u===Sn&&this.type!==Sn;for(let X=0,W=N.length;X<W;X++){let q=N[X],G=q.shadow;if(G===void 0){console.warn("THREE.WebGLShadowMap:",q,"has no shadow.");continue}if(G.autoUpdate===!1&&G.needsUpdate===!1)continue;r.copy(G.mapSize);let ee=G.getFrameExtents();if(r.multiply(ee),s.copy(G.mapSize),(r.x>d||r.y>d)&&(r.x>d&&(s.x=Math.floor(d/ee.x),r.x=s.x*ee.x,G.mapSize.x=s.x),r.y>d&&(s.y=Math.floor(d/ee.y),r.y=s.y*ee.y,G.mapSize.y=s.y)),G.map===null||U===!0||P===!0){let ue=this.type!==Sn?{minFilter:Bt,magFilter:Bt}:{};G.map!==null&&G.map.dispose(),G.map=new yn(r.x,r.y,ue),G.map.texture.name=q.name+".shadowMap",G.camera.updateProjectionMatrix()}n.setRenderTarget(G.map),n.clear();let ae=G.getViewportCount();for(let ue=0;ue<ae;ue++){let _e=G.getViewport(ue);o.set(s.x*_e.x,s.y*_e.y,s.x*_e.z,s.y*_e.w),I.viewport(o),G.updateMatrices(q,ue),i=G.getFrustum(),_(w,O,G.camera,q,this.type)}G.isPointLightShadow!==!0&&this.type===Sn&&E(G,O),G.needsUpdate=!1}u=this.type,h.needsUpdate=!1,n.setRenderTarget(T,M,R)};function E(N,w){let O=e.update(y);f.defines.VSM_SAMPLES!==N.blurSamples&&(f.defines.VSM_SAMPLES=N.blurSamples,m.defines.VSM_SAMPLES=N.blurSamples,f.needsUpdate=!0,m.needsUpdate=!0),N.mapPass===null&&(N.mapPass=new yn(r.x,r.y)),f.uniforms.shadow_pass.value=N.map.texture,f.uniforms.resolution.value=N.mapSize,f.uniforms.radius.value=N.radius,n.setRenderTarget(N.mapPass),n.clear(),n.renderBufferDirect(w,null,O,f,y,null),m.uniforms.shadow_pass.value=N.mapPass.texture,m.uniforms.resolution.value=N.mapSize,m.uniforms.radius.value=N.radius,n.setRenderTarget(N.map),n.clear(),n.renderBufferDirect(w,null,O,m,y,null)}function x(N,w,O,T){let M=null,R=O.isPointLight===!0?N.customDistanceMaterial:N.customDepthMaterial;if(R!==void 0)M=R;else if(M=O.isPointLight===!0?l:c,n.localClippingEnabled&&w.clipShadows===!0&&Array.isArray(w.clippingPlanes)&&w.clippingPlanes.length!==0||w.displacementMap&&w.displacementScale!==0||w.alphaMap&&w.alphaTest>0||w.map&&w.alphaTest>0||w.alphaToCoverage===!0){let I=M.uuid,U=w.uuid,P=a[I];P===void 0&&(P={},a[I]=P);let X=P[U];X===void 0&&(X=M.clone(),P[U]=X,w.addEventListener("dispose",A)),M=X}if(M.visible=w.visible,M.wireframe=w.wireframe,T===Sn?M.side=w.shadowSide!==null?w.shadowSide:w.side:M.side=w.shadowSide!==null?w.shadowSide:p[w.side],M.alphaMap=w.alphaMap,M.alphaTest=w.alphaToCoverage===!0?.5:w.alphaTest,M.map=w.map,M.clipShadows=w.clipShadows,M.clippingPlanes=w.clippingPlanes,M.clipIntersection=w.clipIntersection,M.displacementMap=w.displacementMap,M.displacementScale=w.displacementScale,M.displacementBias=w.displacementBias,M.wireframeLinewidth=w.wireframeLinewidth,M.linewidth=w.linewidth,O.isPointLight===!0&&M.isMeshDistanceMaterial===!0){let I=n.properties.get(M);I.light=O}return M}function _(N,w,O,T,M){if(N.visible===!1)return;if(N.layers.test(w.layers)&&(N.isMesh||N.isLine||N.isPoints)&&(N.castShadow||N.receiveShadow&&M===Sn)&&(!N.frustumCulled||i.intersectsObject(N))){N.modelViewMatrix.multiplyMatrices(O.matrixWorldInverse,N.matrixWorld);let U=e.update(N),P=N.material;if(Array.isArray(P)){let X=U.groups;for(let W=0,q=X.length;W<q;W++){let G=X[W],ee=P[G.materialIndex];if(ee&&ee.visible){let ae=x(N,ee,T,M);N.onBeforeShadow(n,N,w,O,U,ae,G),n.renderBufferDirect(O,null,U,ae,N,G),N.onAfterShadow(n,N,w,O,U,ae,G)}}}else if(P.visible){let X=x(N,P,T,M);N.onBeforeShadow(n,N,w,O,U,X,null),n.renderBufferDirect(O,null,U,X,N,null),N.onAfterShadow(n,N,w,O,U,X,null)}}let I=N.children;for(let U=0,P=I.length;U<P;U++)_(I[U],w,O,T,M)}function A(N){N.target.removeEventListener("dispose",A);for(let O in a){let T=a[O],M=N.target.uuid;M in T&&(T[M].dispose(),delete T[M])}}}var Ug={[Js]:$s,[Qs]:no,[eo]:io,[ai]:to,[$s]:Js,[no]:Qs,[io]:eo,[to]:ai};function Fg(n,e){function t(){let V=!1,le=new vt,fe=null,ge=new vt(0,0,0,0);return{setMask:function(he){fe!==he&&!V&&(n.colorMask(he,he,he,he),fe=he)},setLocked:function(he){V=he},setClear:function(he,oe,Te,Fe,De){De===!0&&(he*=Fe,oe*=Fe,Te*=Fe),le.set(he,oe,Te,Fe),ge.equals(le)===!1&&(n.clearColor(he,oe,Te,Fe),ge.copy(le))},reset:function(){V=!1,fe=null,ge.set(-1,0,0,0)}}}function i(){let V=!1,le=!1,fe=null,ge=null,he=null;return{setReversed:function(oe){if(le!==oe){let Te=e.get("EXT_clip_control");oe?Te.clipControlEXT(Te.LOWER_LEFT_EXT,Te.ZERO_TO_ONE_EXT):Te.clipControlEXT(Te.LOWER_LEFT_EXT,Te.NEGATIVE_ONE_TO_ONE_EXT),le=oe;let Fe=he;he=null,this.setClear(Fe)}},getReversed:function(){return le},setTest:function(oe){oe?K(n.DEPTH_TEST):ne(n.DEPTH_TEST)},setMask:function(oe){fe!==oe&&!V&&(n.depthMask(oe),fe=oe)},setFunc:function(oe){if(le&&(oe=Ug[oe]),ge!==oe){switch(oe){case Js:n.depthFunc(n.NEVER);break;case $s:n.depthFunc(n.ALWAYS);break;case Qs:n.depthFunc(n.LESS);break;case ai:n.depthFunc(n.LEQUAL);break;case eo:n.depthFunc(n.EQUAL);break;case to:n.depthFunc(n.GEQUAL);break;case no:n.depthFunc(n.GREATER);break;case io:n.depthFunc(n.NOTEQUAL);break;default:n.depthFunc(n.LEQUAL)}ge=oe}},setLocked:function(oe){V=oe},setClear:function(oe){he!==oe&&(le&&(oe=1-oe),n.clearDepth(oe),he=oe)},reset:function(){V=!1,fe=null,ge=null,he=null,le=!1}}}function r(){let V=!1,le=null,fe=null,ge=null,he=null,oe=null,Te=null,Fe=null,De=null;return{setTest:function(ve){V||(ve?K(n.STENCIL_TEST):ne(n.STENCIL_TEST))},setMask:function(ve){le!==ve&&!V&&(n.stencilMask(ve),le=ve)},setFunc:function(ve,Ie,be){(fe!==ve||ge!==Ie||he!==be)&&(n.stencilFunc(ve,Ie,be),fe=ve,ge=Ie,he=be)},setOp:function(ve,Ie,be){(oe!==ve||Te!==Ie||Fe!==be)&&(n.stencilOp(ve,Ie,be),oe=ve,Te=Ie,Fe=be)},setLocked:function(ve){V=ve},setClear:function(ve){De!==ve&&(n.clearStencil(ve),De=ve)},reset:function(){V=!1,le=null,fe=null,ge=null,he=null,oe=null,Te=null,Fe=null,De=null}}}let s=new t,o=new i,c=new r,l=new WeakMap,a=new WeakMap,d={},p={},f=new WeakMap,m=[],g=null,y=!1,h=null,u=null,E=null,x=null,_=null,A=null,N=null,w=new qe(0,0,0),O=0,T=!1,M=null,R=null,I=null,U=null,P=null,X=n.getParameter(n.MAX_COMBINED_TEXTURE_IMAGE_UNITS),W=!1,q=0,G=n.getParameter(n.VERSION);G.indexOf("WebGL")!==-1?(q=parseFloat(/^WebGL (\d)/.exec(G)[1]),W=q>=1):G.indexOf("OpenGL ES")!==-1&&(q=parseFloat(/^OpenGL ES (\d)/.exec(G)[1]),W=q>=2);let ee=null,ae={},ue=n.getParameter(n.SCISSOR_BOX),_e=n.getParameter(n.VIEWPORT),me=new vt().fromArray(ue),Me=new vt().fromArray(_e);function k(V,le,fe,ge){let he=new Uint8Array(4),oe=n.createTexture();n.bindTexture(V,oe),n.texParameteri(V,n.TEXTURE_MIN_FILTER,n.NEAREST),n.texParameteri(V,n.TEXTURE_MAG_FILTER,n.NEAREST);for(let Te=0;Te<fe;Te++)V===n.TEXTURE_3D||V===n.TEXTURE_2D_ARRAY?n.texImage3D(le,0,n.RGBA,1,1,ge,0,n.RGBA,n.UNSIGNED_BYTE,he):n.texImage2D(le+Te,0,n.RGBA,1,1,0,n.RGBA,n.UNSIGNED_BYTE,he);return oe}let Y={};Y[n.TEXTURE_2D]=k(n.TEXTURE_2D,n.TEXTURE_2D,1),Y[n.TEXTURE_CUBE_MAP]=k(n.TEXTURE_CUBE_MAP,n.TEXTURE_CUBE_MAP_POSITIVE_X,6),Y[n.TEXTURE_2D_ARRAY]=k(n.TEXTURE_2D_ARRAY,n.TEXTURE_2D_ARRAY,1,1),Y[n.TEXTURE_3D]=k(n.TEXTURE_3D,n.TEXTURE_3D,1,1),s.setClear(0,0,0,1),o.setClear(1),c.setClear(0),K(n.DEPTH_TEST),o.setFunc(ai),Ke(!1),Oe(za),K(n.CULL_FACE),Ge(Nn);function K(V){d[V]!==!0&&(n.enable(V),d[V]=!0)}function ne(V){d[V]!==!1&&(n.disable(V),d[V]=!1)}function ie(V,le){return p[V]!==le?(n.bindFramebuffer(V,le),p[V]=le,V===n.DRAW_FRAMEBUFFER&&(p[n.FRAMEBUFFER]=le),V===n.FRAMEBUFFER&&(p[n.DRAW_FRAMEBUFFER]=le),!0):!1}function de(V,le){let fe=m,ge=!1;if(V){fe=f.get(le),fe===void 0&&(fe=[],f.set(le,fe));let he=V.textures;if(fe.length!==he.length||fe[0]!==n.COLOR_ATTACHMENT0){for(let oe=0,Te=he.length;oe<Te;oe++)fe[oe]=n.COLOR_ATTACHMENT0+oe;fe.length=he.length,ge=!0}}else fe[0]!==n.BACK&&(fe[0]=n.BACK,ge=!0);ge&&n.drawBuffers(fe)}function Le(V){return g!==V?(n.useProgram(V),g=V,!0):!1}let we={[Wn]:n.FUNC_ADD,[gl]:n.FUNC_SUBTRACT,[_l]:n.FUNC_REVERSE_SUBTRACT};we[yl]=n.MIN,we[vl]=n.MAX;let B={[xl]:n.ZERO,[El]:n.ONE,[Sl]:n.SRC_COLOR,[Rs]:n.SRC_ALPHA,[wl]:n.SRC_ALPHA_SATURATE,[Al]:n.DST_COLOR,[Ml]:n.DST_ALPHA,[Tl]:n.ONE_MINUS_SRC_COLOR,[ws]:n.ONE_MINUS_SRC_ALPHA,[Rl]:n.ONE_MINUS_DST_COLOR,[bl]:n.ONE_MINUS_DST_ALPHA,[Cl]:n.CONSTANT_COLOR,[Il]:n.ONE_MINUS_CONSTANT_COLOR,[Pl]:n.CONSTANT_ALPHA,[Ll]:n.ONE_MINUS_CONSTANT_ALPHA};function Ge(V,le,fe,ge,he,oe,Te,Fe,De,ve){if(V===Nn){y===!0&&(ne(n.BLEND),y=!1);return}if(y===!1&&(K(n.BLEND),y=!0),V!==ml){if(V!==h||ve!==T){if((u!==Wn||_!==Wn)&&(n.blendEquation(n.FUNC_ADD),u=Wn,_=Wn),ve)switch(V){case oi:n.blendFuncSeparate(n.ONE,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case Ga:n.blendFunc(n.ONE,n.ONE);break;case Ha:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case Wa:n.blendFuncSeparate(n.DST_COLOR,n.ONE_MINUS_SRC_ALPHA,n.ZERO,n.ONE);break;default:console.error("THREE.WebGLState: Invalid blending: ",V);break}else switch(V){case oi:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case Ga:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE,n.ONE,n.ONE);break;case Ha:console.error("THREE.WebGLState: SubtractiveBlending requires material.premultipliedAlpha = true");break;case Wa:console.error("THREE.WebGLState: MultiplyBlending requires material.premultipliedAlpha = true");break;default:console.error("THREE.WebGLState: Invalid blending: ",V);break}E=null,x=null,A=null,N=null,w.set(0,0,0),O=0,h=V,T=ve}return}he=he||le,oe=oe||fe,Te=Te||ge,(le!==u||he!==_)&&(n.blendEquationSeparate(we[le],we[he]),u=le,_=he),(fe!==E||ge!==x||oe!==A||Te!==N)&&(n.blendFuncSeparate(B[fe],B[ge],B[oe],B[Te]),E=fe,x=ge,A=oe,N=Te),(Fe.equals(w)===!1||De!==O)&&(n.blendColor(Fe.r,Fe.g,Fe.b,De),w.copy(Fe),O=De),h=V,T=!1}function Ne(V,le){V.side===en?ne(n.CULL_FACE):K(n.CULL_FACE);let fe=V.side===wt;le&&(fe=!fe),Ke(fe),V.blending===oi&&V.transparent===!1?Ge(Nn):Ge(V.blending,V.blendEquation,V.blendSrc,V.blendDst,V.blendEquationAlpha,V.blendSrcAlpha,V.blendDstAlpha,V.blendColor,V.blendAlpha,V.premultipliedAlpha),o.setFunc(V.depthFunc),o.setTest(V.depthTest),o.setMask(V.depthWrite),s.setMask(V.colorWrite);let ge=V.stencilWrite;c.setTest(ge),ge&&(c.setMask(V.stencilWriteMask),c.setFunc(V.stencilFunc,V.stencilRef,V.stencilFuncMask),c.setOp(V.stencilFail,V.stencilZFail,V.stencilZPass)),Re(V.polygonOffset,V.polygonOffsetFactor,V.polygonOffsetUnits),V.alphaToCoverage===!0?K(n.SAMPLE_ALPHA_TO_COVERAGE):ne(n.SAMPLE_ALPHA_TO_COVERAGE)}function Ke(V){M!==V&&(V?n.frontFace(n.CW):n.frontFace(n.CCW),M=V)}function Oe(V){V!==dl?(K(n.CULL_FACE),V!==R&&(V===za?n.cullFace(n.BACK):V===fl?n.cullFace(n.FRONT):n.cullFace(n.FRONT_AND_BACK))):ne(n.CULL_FACE),R=V}function Je(V){V!==I&&(W&&n.lineWidth(V),I=V)}function Re(V,le,fe){V?(K(n.POLYGON_OFFSET_FILL),(U!==le||P!==fe)&&(n.polygonOffset(le,fe),U=le,P=fe)):ne(n.POLYGON_OFFSET_FILL)}function He(V){V?K(n.SCISSOR_TEST):ne(n.SCISSOR_TEST)}function ot(V){V===void 0&&(V=n.TEXTURE0+X-1),ee!==V&&(n.activeTexture(V),ee=V)}function it(V,le,fe){fe===void 0&&(ee===null?fe=n.TEXTURE0+X-1:fe=ee);let ge=ae[fe];ge===void 0&&(ge={type:void 0,texture:void 0},ae[fe]=ge),(ge.type!==V||ge.texture!==le)&&(ee!==fe&&(n.activeTexture(fe),ee=fe),n.bindTexture(V,le||Y[V]),ge.type=V,ge.texture=le)}function S(){let V=ae[ee];V!==void 0&&V.type!==void 0&&(n.bindTexture(V.type,null),V.type=void 0,V.texture=void 0)}function v(){try{n.compressedTexImage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function b(){try{n.compressedTexImage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function D(){try{n.texSubImage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function L(){try{n.texSubImage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function F(){try{n.compressedTexSubImage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function H(){try{n.compressedTexSubImage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function z(){try{n.texStorage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function j(){try{n.texStorage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function te(){try{n.texImage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function Q(){try{n.texImage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function ce(V){me.equals(V)===!1&&(n.scissor(V.x,V.y,V.z,V.w),me.copy(V))}function Ee(V){Me.equals(V)===!1&&(n.viewport(V.x,V.y,V.z,V.w),Me.copy(V))}function Se(V,le){let fe=a.get(le);fe===void 0&&(fe=new WeakMap,a.set(le,fe));let ge=fe.get(V);ge===void 0&&(ge=n.getUniformBlockIndex(le,V.name),fe.set(V,ge))}function pe(V,le){let ge=a.get(le).get(V);l.get(le)!==ge&&(n.uniformBlockBinding(le,ge,V.__bindingPointIndex),l.set(le,ge))}function xe(){n.disable(n.BLEND),n.disable(n.CULL_FACE),n.disable(n.DEPTH_TEST),n.disable(n.POLYGON_OFFSET_FILL),n.disable(n.SCISSOR_TEST),n.disable(n.STENCIL_TEST),n.disable(n.SAMPLE_ALPHA_TO_COVERAGE),n.blendEquation(n.FUNC_ADD),n.blendFunc(n.ONE,n.ZERO),n.blendFuncSeparate(n.ONE,n.ZERO,n.ONE,n.ZERO),n.blendColor(0,0,0,0),n.colorMask(!0,!0,!0,!0),n.clearColor(0,0,0,0),n.depthMask(!0),n.depthFunc(n.LESS),o.setReversed(!1),n.clearDepth(1),n.stencilMask(4294967295),n.stencilFunc(n.ALWAYS,0,4294967295),n.stencilOp(n.KEEP,n.KEEP,n.KEEP),n.clearStencil(0),n.cullFace(n.BACK),n.frontFace(n.CCW),n.polygonOffset(0,0),n.activeTexture(n.TEXTURE0),n.bindFramebuffer(n.FRAMEBUFFER,null),n.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),n.bindFramebuffer(n.READ_FRAMEBUFFER,null),n.useProgram(null),n.lineWidth(1),n.scissor(0,0,n.canvas.width,n.canvas.height),n.viewport(0,0,n.canvas.width,n.canvas.height),d={},ee=null,ae={},p={},f=new WeakMap,m=[],g=null,y=!1,h=null,u=null,E=null,x=null,_=null,A=null,N=null,w=new qe(0,0,0),O=0,T=!1,M=null,R=null,I=null,U=null,P=null,me.set(0,0,n.canvas.width,n.canvas.height),Me.set(0,0,n.canvas.width,n.canvas.height),s.reset(),o.reset(),c.reset()}return{buffers:{color:s,depth:o,stencil:c},enable:K,disable:ne,bindFramebuffer:ie,drawBuffers:de,useProgram:Le,setBlending:Ge,setMaterial:Ne,setFlipSided:Ke,setCullFace:Oe,setLineWidth:Je,setPolygonOffset:Re,setScissorTest:He,activeTexture:ot,bindTexture:it,unbindTexture:S,compressedTexImage2D:v,compressedTexImage3D:b,texImage2D:te,texImage3D:Q,updateUBOMapping:Se,uniformBlockBinding:pe,texStorage2D:z,texStorage3D:j,texSubImage2D:D,texSubImage3D:L,compressedTexSubImage2D:F,compressedTexSubImage3D:H,scissor:ce,viewport:Ee,reset:xe}}function kg(n,e,t,i,r,s,o){let c=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,l=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),a=new ze,d=new WeakMap,p,f=new WeakMap,m=!1;try{m=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function g(S,v){return m?new OffscreenCanvas(S,v):Vi("canvas")}function y(S,v,b){let D=1,L=it(S);if((L.width>b||L.height>b)&&(D=b/Math.max(L.width,L.height)),D<1)if(typeof HTMLImageElement<"u"&&S instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&S instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&S instanceof ImageBitmap||typeof VideoFrame<"u"&&S instanceof VideoFrame){let F=Math.floor(D*L.width),H=Math.floor(D*L.height);p===void 0&&(p=g(F,H));let z=v?g(F,H):p;return z.width=F,z.height=H,z.getContext("2d").drawImage(S,0,0,F,H),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+L.width+"x"+L.height+") to ("+F+"x"+H+")."),z}else return"data"in S&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+L.width+"x"+L.height+")."),S;return S}function h(S){return S.generateMipmaps}function u(S){n.generateMipmap(S)}function E(S){return S.isWebGLCubeRenderTarget?n.TEXTURE_CUBE_MAP:S.isWebGL3DRenderTarget?n.TEXTURE_3D:S.isWebGLArrayRenderTarget||S.isCompressedArrayTexture?n.TEXTURE_2D_ARRAY:n.TEXTURE_2D}function x(S,v,b,D,L=!1){if(S!==null){if(n[S]!==void 0)return n[S];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+S+"'")}let F=v;if(v===n.RED&&(b===n.FLOAT&&(F=n.R32F),b===n.HALF_FLOAT&&(F=n.R16F),b===n.UNSIGNED_BYTE&&(F=n.R8)),v===n.RED_INTEGER&&(b===n.UNSIGNED_BYTE&&(F=n.R8UI),b===n.UNSIGNED_SHORT&&(F=n.R16UI),b===n.UNSIGNED_INT&&(F=n.R32UI),b===n.BYTE&&(F=n.R8I),b===n.SHORT&&(F=n.R16I),b===n.INT&&(F=n.R32I)),v===n.RG&&(b===n.FLOAT&&(F=n.RG32F),b===n.HALF_FLOAT&&(F=n.RG16F),b===n.UNSIGNED_BYTE&&(F=n.RG8)),v===n.RG_INTEGER&&(b===n.UNSIGNED_BYTE&&(F=n.RG8UI),b===n.UNSIGNED_SHORT&&(F=n.RG16UI),b===n.UNSIGNED_INT&&(F=n.RG32UI),b===n.BYTE&&(F=n.RG8I),b===n.SHORT&&(F=n.RG16I),b===n.INT&&(F=n.RG32I)),v===n.RGB_INTEGER&&(b===n.UNSIGNED_BYTE&&(F=n.RGB8UI),b===n.UNSIGNED_SHORT&&(F=n.RGB16UI),b===n.UNSIGNED_INT&&(F=n.RGB32UI),b===n.BYTE&&(F=n.RGB8I),b===n.SHORT&&(F=n.RGB16I),b===n.INT&&(F=n.RGB32I)),v===n.RGBA_INTEGER&&(b===n.UNSIGNED_BYTE&&(F=n.RGBA8UI),b===n.UNSIGNED_SHORT&&(F=n.RGBA16UI),b===n.UNSIGNED_INT&&(F=n.RGBA32UI),b===n.BYTE&&(F=n.RGBA8I),b===n.SHORT&&(F=n.RGBA16I),b===n.INT&&(F=n.RGBA32I)),v===n.RGB&&b===n.UNSIGNED_INT_5_9_9_9_REV&&(F=n.RGB9_E5),v===n.RGBA){let H=L?_r:nt.getTransfer(D);b===n.FLOAT&&(F=n.RGBA32F),b===n.HALF_FLOAT&&(F=n.RGBA16F),b===n.UNSIGNED_BYTE&&(F=H===at?n.SRGB8_ALPHA8:n.RGBA8),b===n.UNSIGNED_SHORT_4_4_4_4&&(F=n.RGBA4),b===n.UNSIGNED_SHORT_5_5_5_1&&(F=n.RGB5_A1)}return(F===n.R16F||F===n.R32F||F===n.RG16F||F===n.RG32F||F===n.RGBA16F||F===n.RGBA32F)&&e.get("EXT_color_buffer_float"),F}function _(S,v){let b;return S?v===null||v===Qn||v===Qi?b=n.DEPTH24_STENCIL8:v===Tn?b=n.DEPTH32F_STENCIL8:v===Ji&&(b=n.DEPTH24_STENCIL8,console.warn("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):v===null||v===Qn||v===Qi?b=n.DEPTH_COMPONENT24:v===Tn?b=n.DEPTH_COMPONENT32F:v===Ji&&(b=n.DEPTH_COMPONENT16),b}function A(S,v){return h(S)===!0||S.isFramebufferTexture&&S.minFilter!==Bt&&S.minFilter!==hn?Math.log2(Math.max(v.width,v.height))+1:S.mipmaps!==void 0&&S.mipmaps.length>0?S.mipmaps.length:S.isCompressedTexture&&Array.isArray(S.image)?v.mipmaps.length:1}function N(S){let v=S.target;v.removeEventListener("dispose",N),O(v),v.isVideoTexture&&d.delete(v)}function w(S){let v=S.target;v.removeEventListener("dispose",w),M(v)}function O(S){let v=i.get(S);if(v.__webglInit===void 0)return;let b=S.source,D=f.get(b);if(D){let L=D[v.__cacheKey];L.usedTimes--,L.usedTimes===0&&T(S),Object.keys(D).length===0&&f.delete(b)}i.remove(S)}function T(S){let v=i.get(S);n.deleteTexture(v.__webglTexture);let b=S.source,D=f.get(b);delete D[v.__cacheKey],o.memory.textures--}function M(S){let v=i.get(S);if(S.depthTexture&&(S.depthTexture.dispose(),i.remove(S.depthTexture)),S.isWebGLCubeRenderTarget)for(let D=0;D<6;D++){if(Array.isArray(v.__webglFramebuffer[D]))for(let L=0;L<v.__webglFramebuffer[D].length;L++)n.deleteFramebuffer(v.__webglFramebuffer[D][L]);else n.deleteFramebuffer(v.__webglFramebuffer[D]);v.__webglDepthbuffer&&n.deleteRenderbuffer(v.__webglDepthbuffer[D])}else{if(Array.isArray(v.__webglFramebuffer))for(let D=0;D<v.__webglFramebuffer.length;D++)n.deleteFramebuffer(v.__webglFramebuffer[D]);else n.deleteFramebuffer(v.__webglFramebuffer);if(v.__webglDepthbuffer&&n.deleteRenderbuffer(v.__webglDepthbuffer),v.__webglMultisampledFramebuffer&&n.deleteFramebuffer(v.__webglMultisampledFramebuffer),v.__webglColorRenderbuffer)for(let D=0;D<v.__webglColorRenderbuffer.length;D++)v.__webglColorRenderbuffer[D]&&n.deleteRenderbuffer(v.__webglColorRenderbuffer[D]);v.__webglDepthRenderbuffer&&n.deleteRenderbuffer(v.__webglDepthRenderbuffer)}let b=S.textures;for(let D=0,L=b.length;D<L;D++){let F=i.get(b[D]);F.__webglTexture&&(n.deleteTexture(F.__webglTexture),o.memory.textures--),i.remove(b[D])}i.remove(S)}let R=0;function I(){R=0}function U(){let S=R;return S>=r.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+S+" texture units while this GPU supports only "+r.maxTextures),R+=1,S}function P(S){let v=[];return v.push(S.wrapS),v.push(S.wrapT),v.push(S.wrapR||0),v.push(S.magFilter),v.push(S.minFilter),v.push(S.anisotropy),v.push(S.internalFormat),v.push(S.format),v.push(S.type),v.push(S.generateMipmaps),v.push(S.premultiplyAlpha),v.push(S.flipY),v.push(S.unpackAlignment),v.push(S.colorSpace),v.join()}function X(S,v){let b=i.get(S);if(S.isVideoTexture&&He(S),S.isRenderTargetTexture===!1&&S.isExternalTexture!==!0&&S.version>0&&b.__version!==S.version){let D=S.image;if(D===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(D.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{Y(b,S,v);return}}else S.isExternalTexture&&(b.__webglTexture=S.sourceTexture?S.sourceTexture:null);t.bindTexture(n.TEXTURE_2D,b.__webglTexture,n.TEXTURE0+v)}function W(S,v){let b=i.get(S);if(S.isRenderTargetTexture===!1&&S.version>0&&b.__version!==S.version){Y(b,S,v);return}t.bindTexture(n.TEXTURE_2D_ARRAY,b.__webglTexture,n.TEXTURE0+v)}function q(S,v){let b=i.get(S);if(S.isRenderTargetTexture===!1&&S.version>0&&b.__version!==S.version){Y(b,S,v);return}t.bindTexture(n.TEXTURE_3D,b.__webglTexture,n.TEXTURE0+v)}function G(S,v){let b=i.get(S);if(S.version>0&&b.__version!==S.version){K(b,S,v);return}t.bindTexture(n.TEXTURE_CUBE_MAP,b.__webglTexture,n.TEXTURE0+v)}let ee={[Ln]:n.REPEAT,[Yt]:n.CLAMP_TO_EDGE,[Cs]:n.MIRRORED_REPEAT},ae={[Bt]:n.NEAREST,[Gl]:n.NEAREST_MIPMAP_NEAREST,[Xr]:n.NEAREST_MIPMAP_LINEAR,[hn]:n.LINEAR,[ao]:n.LINEAR_MIPMAP_NEAREST,[$n]:n.LINEAR_MIPMAP_LINEAR},ue={[Yl]:n.NEVER,[$l]:n.ALWAYS,[ql]:n.LESS,[tc]:n.LEQUAL,[Kl]:n.EQUAL,[Jl]:n.GEQUAL,[Zl]:n.GREATER,[jl]:n.NOTEQUAL};function _e(S,v){if(v.type===Tn&&e.has("OES_texture_float_linear")===!1&&(v.magFilter===hn||v.magFilter===ao||v.magFilter===Xr||v.magFilter===$n||v.minFilter===hn||v.minFilter===ao||v.minFilter===Xr||v.minFilter===$n)&&console.warn("THREE.WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),n.texParameteri(S,n.TEXTURE_WRAP_S,ee[v.wrapS]),n.texParameteri(S,n.TEXTURE_WRAP_T,ee[v.wrapT]),(S===n.TEXTURE_3D||S===n.TEXTURE_2D_ARRAY)&&n.texParameteri(S,n.TEXTURE_WRAP_R,ee[v.wrapR]),n.texParameteri(S,n.TEXTURE_MAG_FILTER,ae[v.magFilter]),n.texParameteri(S,n.TEXTURE_MIN_FILTER,ae[v.minFilter]),v.compareFunction&&(n.texParameteri(S,n.TEXTURE_COMPARE_MODE,n.COMPARE_REF_TO_TEXTURE),n.texParameteri(S,n.TEXTURE_COMPARE_FUNC,ue[v.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(v.magFilter===Bt||v.minFilter!==Xr&&v.minFilter!==$n||v.type===Tn&&e.has("OES_texture_float_linear")===!1)return;if(v.anisotropy>1||i.get(v).__currentAnisotropy){let b=e.get("EXT_texture_filter_anisotropic");n.texParameterf(S,b.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(v.anisotropy,r.getMaxAnisotropy())),i.get(v).__currentAnisotropy=v.anisotropy}}}function me(S,v){let b=!1;S.__webglInit===void 0&&(S.__webglInit=!0,v.addEventListener("dispose",N));let D=v.source,L=f.get(D);L===void 0&&(L={},f.set(D,L));let F=P(v);if(F!==S.__cacheKey){L[F]===void 0&&(L[F]={texture:n.createTexture(),usedTimes:0},o.memory.textures++,b=!0),L[F].usedTimes++;let H=L[S.__cacheKey];H!==void 0&&(L[S.__cacheKey].usedTimes--,H.usedTimes===0&&T(v)),S.__cacheKey=F,S.__webglTexture=L[F].texture}return b}function Me(S,v,b){return Math.floor(Math.floor(S/b)/v)}function k(S,v,b,D){let F=S.updateRanges;if(F.length===0)t.texSubImage2D(n.TEXTURE_2D,0,0,0,v.width,v.height,b,D,v.data);else{F.sort((Q,ce)=>Q.start-ce.start);let H=0;for(let Q=1;Q<F.length;Q++){let ce=F[H],Ee=F[Q],Se=ce.start+ce.count,pe=Me(Ee.start,v.width,4),xe=Me(ce.start,v.width,4);Ee.start<=Se+1&&pe===xe&&Me(Ee.start+Ee.count-1,v.width,4)===pe?ce.count=Math.max(ce.count,Ee.start+Ee.count-ce.start):(++H,F[H]=Ee)}F.length=H+1;let z=n.getParameter(n.UNPACK_ROW_LENGTH),j=n.getParameter(n.UNPACK_SKIP_PIXELS),te=n.getParameter(n.UNPACK_SKIP_ROWS);n.pixelStorei(n.UNPACK_ROW_LENGTH,v.width);for(let Q=0,ce=F.length;Q<ce;Q++){let Ee=F[Q],Se=Math.floor(Ee.start/4),pe=Math.ceil(Ee.count/4),xe=Se%v.width,V=Math.floor(Se/v.width),le=pe,fe=1;n.pixelStorei(n.UNPACK_SKIP_PIXELS,xe),n.pixelStorei(n.UNPACK_SKIP_ROWS,V),t.texSubImage2D(n.TEXTURE_2D,0,xe,V,le,fe,b,D,v.data)}S.clearUpdateRanges(),n.pixelStorei(n.UNPACK_ROW_LENGTH,z),n.pixelStorei(n.UNPACK_SKIP_PIXELS,j),n.pixelStorei(n.UNPACK_SKIP_ROWS,te)}}function Y(S,v,b){let D=n.TEXTURE_2D;(v.isDataArrayTexture||v.isCompressedArrayTexture)&&(D=n.TEXTURE_2D_ARRAY),v.isData3DTexture&&(D=n.TEXTURE_3D);let L=me(S,v),F=v.source;t.bindTexture(D,S.__webglTexture,n.TEXTURE0+b);let H=i.get(F);if(F.version!==H.__version||L===!0){t.activeTexture(n.TEXTURE0+b);let z=nt.getPrimaries(nt.workingColorSpace),j=v.colorSpace===Dn?null:nt.getPrimaries(v.colorSpace),te=v.colorSpace===Dn||z===j?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,v.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,v.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,v.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,te);let Q=y(v.image,!1,r.maxTextureSize);Q=ot(v,Q);let ce=s.convert(v.format,v.colorSpace),Ee=s.convert(v.type),Se=x(v.internalFormat,ce,Ee,v.colorSpace,v.isVideoTexture);_e(D,v);let pe,xe=v.mipmaps,V=v.isVideoTexture!==!0,le=H.__version===void 0||L===!0,fe=F.dataReady,ge=A(v,Q);if(v.isDepthTexture)Se=_(v.format===er,v.type),le&&(V?t.texStorage2D(n.TEXTURE_2D,1,Se,Q.width,Q.height):t.texImage2D(n.TEXTURE_2D,0,Se,Q.width,Q.height,0,ce,Ee,null));else if(v.isDataTexture)if(xe.length>0){V&&le&&t.texStorage2D(n.TEXTURE_2D,ge,Se,xe[0].width,xe[0].height);for(let he=0,oe=xe.length;he<oe;he++)pe=xe[he],V?fe&&t.texSubImage2D(n.TEXTURE_2D,he,0,0,pe.width,pe.height,ce,Ee,pe.data):t.texImage2D(n.TEXTURE_2D,he,Se,pe.width,pe.height,0,ce,Ee,pe.data);v.generateMipmaps=!1}else V?(le&&t.texStorage2D(n.TEXTURE_2D,ge,Se,Q.width,Q.height),fe&&k(v,Q,ce,Ee)):t.texImage2D(n.TEXTURE_2D,0,Se,Q.width,Q.height,0,ce,Ee,Q.data);else if(v.isCompressedTexture)if(v.isCompressedArrayTexture){V&&le&&t.texStorage3D(n.TEXTURE_2D_ARRAY,ge,Se,xe[0].width,xe[0].height,Q.depth);for(let he=0,oe=xe.length;he<oe;he++)if(pe=xe[he],v.format!==tn)if(ce!==null)if(V){if(fe)if(v.layerUpdates.size>0){let Te=lc(pe.width,pe.height,v.format,v.type);for(let Fe of v.layerUpdates){let De=pe.data.subarray(Fe*Te/pe.data.BYTES_PER_ELEMENT,(Fe+1)*Te/pe.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,he,0,0,Fe,pe.width,pe.height,1,ce,De)}v.clearLayerUpdates()}else t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,he,0,0,0,pe.width,pe.height,Q.depth,ce,pe.data)}else t.compressedTexImage3D(n.TEXTURE_2D_ARRAY,he,Se,pe.width,pe.height,Q.depth,0,pe.data,0,0);else console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else V?fe&&t.texSubImage3D(n.TEXTURE_2D_ARRAY,he,0,0,0,pe.width,pe.height,Q.depth,ce,Ee,pe.data):t.texImage3D(n.TEXTURE_2D_ARRAY,he,Se,pe.width,pe.height,Q.depth,0,ce,Ee,pe.data)}else{V&&le&&t.texStorage2D(n.TEXTURE_2D,ge,Se,xe[0].width,xe[0].height);for(let he=0,oe=xe.length;he<oe;he++)pe=xe[he],v.format!==tn?ce!==null?V?fe&&t.compressedTexSubImage2D(n.TEXTURE_2D,he,0,0,pe.width,pe.height,ce,pe.data):t.compressedTexImage2D(n.TEXTURE_2D,he,Se,pe.width,pe.height,0,pe.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):V?fe&&t.texSubImage2D(n.TEXTURE_2D,he,0,0,pe.width,pe.height,ce,Ee,pe.data):t.texImage2D(n.TEXTURE_2D,he,Se,pe.width,pe.height,0,ce,Ee,pe.data)}else if(v.isDataArrayTexture)if(V){if(le&&t.texStorage3D(n.TEXTURE_2D_ARRAY,ge,Se,Q.width,Q.height,Q.depth),fe)if(v.layerUpdates.size>0){let he=lc(Q.width,Q.height,v.format,v.type);for(let oe of v.layerUpdates){let Te=Q.data.subarray(oe*he/Q.data.BYTES_PER_ELEMENT,(oe+1)*he/Q.data.BYTES_PER_ELEMENT);t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,oe,Q.width,Q.height,1,ce,Ee,Te)}v.clearLayerUpdates()}else t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,0,Q.width,Q.height,Q.depth,ce,Ee,Q.data)}else t.texImage3D(n.TEXTURE_2D_ARRAY,0,Se,Q.width,Q.height,Q.depth,0,ce,Ee,Q.data);else if(v.isData3DTexture)V?(le&&t.texStorage3D(n.TEXTURE_3D,ge,Se,Q.width,Q.height,Q.depth),fe&&t.texSubImage3D(n.TEXTURE_3D,0,0,0,0,Q.width,Q.height,Q.depth,ce,Ee,Q.data)):t.texImage3D(n.TEXTURE_3D,0,Se,Q.width,Q.height,Q.depth,0,ce,Ee,Q.data);else if(v.isFramebufferTexture){if(le)if(V)t.texStorage2D(n.TEXTURE_2D,ge,Se,Q.width,Q.height);else{let he=Q.width,oe=Q.height;for(let Te=0;Te<ge;Te++)t.texImage2D(n.TEXTURE_2D,Te,Se,he,oe,0,ce,Ee,null),he>>=1,oe>>=1}}else if(xe.length>0){if(V&&le){let he=it(xe[0]);t.texStorage2D(n.TEXTURE_2D,ge,Se,he.width,he.height)}for(let he=0,oe=xe.length;he<oe;he++)pe=xe[he],V?fe&&t.texSubImage2D(n.TEXTURE_2D,he,0,0,ce,Ee,pe):t.texImage2D(n.TEXTURE_2D,he,Se,ce,Ee,pe);v.generateMipmaps=!1}else if(V){if(le){let he=it(Q);t.texStorage2D(n.TEXTURE_2D,ge,Se,he.width,he.height)}fe&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,ce,Ee,Q)}else t.texImage2D(n.TEXTURE_2D,0,Se,ce,Ee,Q);h(v)&&u(D),H.__version=F.version,v.onUpdate&&v.onUpdate(v)}S.__version=v.version}function K(S,v,b){if(v.image.length!==6)return;let D=me(S,v),L=v.source;t.bindTexture(n.TEXTURE_CUBE_MAP,S.__webglTexture,n.TEXTURE0+b);let F=i.get(L);if(L.version!==F.__version||D===!0){t.activeTexture(n.TEXTURE0+b);let H=nt.getPrimaries(nt.workingColorSpace),z=v.colorSpace===Dn?null:nt.getPrimaries(v.colorSpace),j=v.colorSpace===Dn||H===z?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,v.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,v.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,v.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,j);let te=v.isCompressedTexture||v.image[0].isCompressedTexture,Q=v.image[0]&&v.image[0].isDataTexture,ce=[];for(let oe=0;oe<6;oe++)!te&&!Q?ce[oe]=y(v.image[oe],!0,r.maxCubemapSize):ce[oe]=Q?v.image[oe].image:v.image[oe],ce[oe]=ot(v,ce[oe]);let Ee=ce[0],Se=s.convert(v.format,v.colorSpace),pe=s.convert(v.type),xe=x(v.internalFormat,Se,pe,v.colorSpace),V=v.isVideoTexture!==!0,le=F.__version===void 0||D===!0,fe=L.dataReady,ge=A(v,Ee);_e(n.TEXTURE_CUBE_MAP,v);let he;if(te){V&&le&&t.texStorage2D(n.TEXTURE_CUBE_MAP,ge,xe,Ee.width,Ee.height);for(let oe=0;oe<6;oe++){he=ce[oe].mipmaps;for(let Te=0;Te<he.length;Te++){let Fe=he[Te];v.format!==tn?Se!==null?V?fe&&t.compressedTexSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,Te,0,0,Fe.width,Fe.height,Se,Fe.data):t.compressedTexImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,Te,xe,Fe.width,Fe.height,0,Fe.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):V?fe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,Te,0,0,Fe.width,Fe.height,Se,pe,Fe.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,Te,xe,Fe.width,Fe.height,0,Se,pe,Fe.data)}}}else{if(he=v.mipmaps,V&&le){he.length>0&&ge++;let oe=it(ce[0]);t.texStorage2D(n.TEXTURE_CUBE_MAP,ge,xe,oe.width,oe.height)}for(let oe=0;oe<6;oe++)if(Q){V?fe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,0,0,0,ce[oe].width,ce[oe].height,Se,pe,ce[oe].data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,0,xe,ce[oe].width,ce[oe].height,0,Se,pe,ce[oe].data);for(let Te=0;Te<he.length;Te++){let De=he[Te].image[oe].image;V?fe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,Te+1,0,0,De.width,De.height,Se,pe,De.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,Te+1,xe,De.width,De.height,0,Se,pe,De.data)}}else{V?fe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,0,0,0,Se,pe,ce[oe]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,0,xe,Se,pe,ce[oe]);for(let Te=0;Te<he.length;Te++){let Fe=he[Te];V?fe&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,Te+1,0,0,Se,pe,Fe.image[oe]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+oe,Te+1,xe,Se,pe,Fe.image[oe])}}}h(v)&&u(n.TEXTURE_CUBE_MAP),F.__version=L.version,v.onUpdate&&v.onUpdate(v)}S.__version=v.version}function ne(S,v,b,D,L,F){let H=s.convert(b.format,b.colorSpace),z=s.convert(b.type),j=x(b.internalFormat,H,z,b.colorSpace),te=i.get(v),Q=i.get(b);if(Q.__renderTarget=v,!te.__hasExternalTextures){let ce=Math.max(1,v.width>>F),Ee=Math.max(1,v.height>>F);L===n.TEXTURE_3D||L===n.TEXTURE_2D_ARRAY?t.texImage3D(L,F,j,ce,Ee,v.depth,0,H,z,null):t.texImage2D(L,F,j,ce,Ee,0,H,z,null)}t.bindFramebuffer(n.FRAMEBUFFER,S),Re(v)?c.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,D,L,Q.__webglTexture,0,Je(v)):(L===n.TEXTURE_2D||L>=n.TEXTURE_CUBE_MAP_POSITIVE_X&&L<=n.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&n.framebufferTexture2D(n.FRAMEBUFFER,D,L,Q.__webglTexture,F),t.bindFramebuffer(n.FRAMEBUFFER,null)}function ie(S,v,b){if(n.bindRenderbuffer(n.RENDERBUFFER,S),v.depthBuffer){let D=v.depthTexture,L=D&&D.isDepthTexture?D.type:null,F=_(v.stencilBuffer,L),H=v.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,z=Je(v);Re(v)?c.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,z,F,v.width,v.height):b?n.renderbufferStorageMultisample(n.RENDERBUFFER,z,F,v.width,v.height):n.renderbufferStorage(n.RENDERBUFFER,F,v.width,v.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,H,n.RENDERBUFFER,S)}else{let D=v.textures;for(let L=0;L<D.length;L++){let F=D[L],H=s.convert(F.format,F.colorSpace),z=s.convert(F.type),j=x(F.internalFormat,H,z,F.colorSpace),te=Je(v);b&&Re(v)===!1?n.renderbufferStorageMultisample(n.RENDERBUFFER,te,j,v.width,v.height):Re(v)?c.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,te,j,v.width,v.height):n.renderbufferStorage(n.RENDERBUFFER,j,v.width,v.height)}}n.bindRenderbuffer(n.RENDERBUFFER,null)}function de(S,v){if(v&&v.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(t.bindFramebuffer(n.FRAMEBUFFER,S),!(v.depthTexture&&v.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");let D=i.get(v.depthTexture);D.__renderTarget=v,(!D.__webglTexture||v.depthTexture.image.width!==v.width||v.depthTexture.image.height!==v.height)&&(v.depthTexture.image.width=v.width,v.depthTexture.image.height=v.height,v.depthTexture.needsUpdate=!0),X(v.depthTexture,0);let L=D.__webglTexture,F=Je(v);if(v.depthTexture.format===Bi)Re(v)?c.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,L,0,F):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,L,0);else if(v.depthTexture.format===er)Re(v)?c.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,L,0,F):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,L,0);else throw new Error("Unknown depthTexture format")}function Le(S){let v=i.get(S),b=S.isWebGLCubeRenderTarget===!0;if(v.__boundDepthTexture!==S.depthTexture){let D=S.depthTexture;if(v.__depthDisposeCallback&&v.__depthDisposeCallback(),D){let L=()=>{delete v.__boundDepthTexture,delete v.__depthDisposeCallback,D.removeEventListener("dispose",L)};D.addEventListener("dispose",L),v.__depthDisposeCallback=L}v.__boundDepthTexture=D}if(S.depthTexture&&!v.__autoAllocateDepthBuffer){if(b)throw new Error("target.depthTexture not supported in Cube render targets");let D=S.texture.mipmaps;D&&D.length>0?de(v.__webglFramebuffer[0],S):de(v.__webglFramebuffer,S)}else if(b){v.__webglDepthbuffer=[];for(let D=0;D<6;D++)if(t.bindFramebuffer(n.FRAMEBUFFER,v.__webglFramebuffer[D]),v.__webglDepthbuffer[D]===void 0)v.__webglDepthbuffer[D]=n.createRenderbuffer(),ie(v.__webglDepthbuffer[D],S,!1);else{let L=S.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,F=v.__webglDepthbuffer[D];n.bindRenderbuffer(n.RENDERBUFFER,F),n.framebufferRenderbuffer(n.FRAMEBUFFER,L,n.RENDERBUFFER,F)}}else{let D=S.texture.mipmaps;if(D&&D.length>0?t.bindFramebuffer(n.FRAMEBUFFER,v.__webglFramebuffer[0]):t.bindFramebuffer(n.FRAMEBUFFER,v.__webglFramebuffer),v.__webglDepthbuffer===void 0)v.__webglDepthbuffer=n.createRenderbuffer(),ie(v.__webglDepthbuffer,S,!1);else{let L=S.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,F=v.__webglDepthbuffer;n.bindRenderbuffer(n.RENDERBUFFER,F),n.framebufferRenderbuffer(n.FRAMEBUFFER,L,n.RENDERBUFFER,F)}}t.bindFramebuffer(n.FRAMEBUFFER,null)}function we(S,v,b){let D=i.get(S);v!==void 0&&ne(D.__webglFramebuffer,S,S.texture,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,0),b!==void 0&&Le(S)}function B(S){let v=S.texture,b=i.get(S),D=i.get(v);S.addEventListener("dispose",w);let L=S.textures,F=S.isWebGLCubeRenderTarget===!0,H=L.length>1;if(H||(D.__webglTexture===void 0&&(D.__webglTexture=n.createTexture()),D.__version=v.version,o.memory.textures++),F){b.__webglFramebuffer=[];for(let z=0;z<6;z++)if(v.mipmaps&&v.mipmaps.length>0){b.__webglFramebuffer[z]=[];for(let j=0;j<v.mipmaps.length;j++)b.__webglFramebuffer[z][j]=n.createFramebuffer()}else b.__webglFramebuffer[z]=n.createFramebuffer()}else{if(v.mipmaps&&v.mipmaps.length>0){b.__webglFramebuffer=[];for(let z=0;z<v.mipmaps.length;z++)b.__webglFramebuffer[z]=n.createFramebuffer()}else b.__webglFramebuffer=n.createFramebuffer();if(H)for(let z=0,j=L.length;z<j;z++){let te=i.get(L[z]);te.__webglTexture===void 0&&(te.__webglTexture=n.createTexture(),o.memory.textures++)}if(S.samples>0&&Re(S)===!1){b.__webglMultisampledFramebuffer=n.createFramebuffer(),b.__webglColorRenderbuffer=[],t.bindFramebuffer(n.FRAMEBUFFER,b.__webglMultisampledFramebuffer);for(let z=0;z<L.length;z++){let j=L[z];b.__webglColorRenderbuffer[z]=n.createRenderbuffer(),n.bindRenderbuffer(n.RENDERBUFFER,b.__webglColorRenderbuffer[z]);let te=s.convert(j.format,j.colorSpace),Q=s.convert(j.type),ce=x(j.internalFormat,te,Q,j.colorSpace,S.isXRRenderTarget===!0),Ee=Je(S);n.renderbufferStorageMultisample(n.RENDERBUFFER,Ee,ce,S.width,S.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+z,n.RENDERBUFFER,b.__webglColorRenderbuffer[z])}n.bindRenderbuffer(n.RENDERBUFFER,null),S.depthBuffer&&(b.__webglDepthRenderbuffer=n.createRenderbuffer(),ie(b.__webglDepthRenderbuffer,S,!0)),t.bindFramebuffer(n.FRAMEBUFFER,null)}}if(F){t.bindTexture(n.TEXTURE_CUBE_MAP,D.__webglTexture),_e(n.TEXTURE_CUBE_MAP,v);for(let z=0;z<6;z++)if(v.mipmaps&&v.mipmaps.length>0)for(let j=0;j<v.mipmaps.length;j++)ne(b.__webglFramebuffer[z][j],S,v,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+z,j);else ne(b.__webglFramebuffer[z],S,v,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+z,0);h(v)&&u(n.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(H){for(let z=0,j=L.length;z<j;z++){let te=L[z],Q=i.get(te),ce=n.TEXTURE_2D;(S.isWebGL3DRenderTarget||S.isWebGLArrayRenderTarget)&&(ce=S.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(ce,Q.__webglTexture),_e(ce,te),ne(b.__webglFramebuffer,S,te,n.COLOR_ATTACHMENT0+z,ce,0),h(te)&&u(ce)}t.unbindTexture()}else{let z=n.TEXTURE_2D;if((S.isWebGL3DRenderTarget||S.isWebGLArrayRenderTarget)&&(z=S.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(z,D.__webglTexture),_e(z,v),v.mipmaps&&v.mipmaps.length>0)for(let j=0;j<v.mipmaps.length;j++)ne(b.__webglFramebuffer[j],S,v,n.COLOR_ATTACHMENT0,z,j);else ne(b.__webglFramebuffer,S,v,n.COLOR_ATTACHMENT0,z,0);h(v)&&u(z),t.unbindTexture()}S.depthBuffer&&Le(S)}function Ge(S){let v=S.textures;for(let b=0,D=v.length;b<D;b++){let L=v[b];if(h(L)){let F=E(S),H=i.get(L).__webglTexture;t.bindTexture(F,H),u(F),t.unbindTexture()}}}let Ne=[],Ke=[];function Oe(S){if(S.samples>0){if(Re(S)===!1){let v=S.textures,b=S.width,D=S.height,L=n.COLOR_BUFFER_BIT,F=S.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,H=i.get(S),z=v.length>1;if(z)for(let te=0;te<v.length;te++)t.bindFramebuffer(n.FRAMEBUFFER,H.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+te,n.RENDERBUFFER,null),t.bindFramebuffer(n.FRAMEBUFFER,H.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+te,n.TEXTURE_2D,null,0);t.bindFramebuffer(n.READ_FRAMEBUFFER,H.__webglMultisampledFramebuffer);let j=S.texture.mipmaps;j&&j.length>0?t.bindFramebuffer(n.DRAW_FRAMEBUFFER,H.__webglFramebuffer[0]):t.bindFramebuffer(n.DRAW_FRAMEBUFFER,H.__webglFramebuffer);for(let te=0;te<v.length;te++){if(S.resolveDepthBuffer&&(S.depthBuffer&&(L|=n.DEPTH_BUFFER_BIT),S.stencilBuffer&&S.resolveStencilBuffer&&(L|=n.STENCIL_BUFFER_BIT)),z){n.framebufferRenderbuffer(n.READ_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.RENDERBUFFER,H.__webglColorRenderbuffer[te]);let Q=i.get(v[te]).__webglTexture;n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,Q,0)}n.blitFramebuffer(0,0,b,D,0,0,b,D,L,n.NEAREST),l===!0&&(Ne.length=0,Ke.length=0,Ne.push(n.COLOR_ATTACHMENT0+te),S.depthBuffer&&S.resolveDepthBuffer===!1&&(Ne.push(F),Ke.push(F),n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,Ke)),n.invalidateFramebuffer(n.READ_FRAMEBUFFER,Ne))}if(t.bindFramebuffer(n.READ_FRAMEBUFFER,null),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),z)for(let te=0;te<v.length;te++){t.bindFramebuffer(n.FRAMEBUFFER,H.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+te,n.RENDERBUFFER,H.__webglColorRenderbuffer[te]);let Q=i.get(v[te]).__webglTexture;t.bindFramebuffer(n.FRAMEBUFFER,H.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+te,n.TEXTURE_2D,Q,0)}t.bindFramebuffer(n.DRAW_FRAMEBUFFER,H.__webglMultisampledFramebuffer)}else if(S.depthBuffer&&S.resolveDepthBuffer===!1&&l){let v=S.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,[v])}}}function Je(S){return Math.min(r.maxSamples,S.samples)}function Re(S){let v=i.get(S);return S.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&v.__useRenderToTexture!==!1}function He(S){let v=o.render.frame;d.get(S)!==v&&(d.set(S,v),S.update())}function ot(S,v){let b=S.colorSpace,D=S.format,L=S.type;return S.isCompressedTexture===!0||S.isVideoTexture===!0||b!==ci&&b!==Dn&&(nt.getTransfer(b)===at?(D!==tn||L!==pn)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",b)),v}function it(S){return typeof HTMLImageElement<"u"&&S instanceof HTMLImageElement?(a.width=S.naturalWidth||S.width,a.height=S.naturalHeight||S.height):typeof VideoFrame<"u"&&S instanceof VideoFrame?(a.width=S.displayWidth,a.height=S.displayHeight):(a.width=S.width,a.height=S.height),a}this.allocateTextureUnit=U,this.resetTextureUnits=I,this.setTexture2D=X,this.setTexture2DArray=W,this.setTexture3D=q,this.setTextureCube=G,this.rebindTextures=we,this.setupRenderTarget=B,this.updateRenderTargetMipmap=Ge,this.updateMultisampleRenderTarget=Oe,this.setupDepthRenderbuffer=Le,this.setupFrameBufferTexture=ne,this.useMultisampledRTT=Re}function Bg(n,e){function t(i,r=Dn){let s,o=nt.getTransfer(r);if(i===pn)return n.UNSIGNED_BYTE;if(i===lo)return n.UNSIGNED_SHORT_4_4_4_4;if(i===uo)return n.UNSIGNED_SHORT_5_5_5_1;if(i===Ka)return n.UNSIGNED_INT_5_9_9_9_REV;if(i===Ya)return n.BYTE;if(i===qa)return n.SHORT;if(i===Ji)return n.UNSIGNED_SHORT;if(i===co)return n.INT;if(i===Qn)return n.UNSIGNED_INT;if(i===Tn)return n.FLOAT;if(i===$i)return n.HALF_FLOAT;if(i===Za)return n.ALPHA;if(i===ja)return n.RGB;if(i===tn)return n.RGBA;if(i===Bi)return n.DEPTH_COMPONENT;if(i===er)return n.DEPTH_STENCIL;if(i===Ja)return n.RED;if(i===ho)return n.RED_INTEGER;if(i===$a)return n.RG;if(i===fo)return n.RG_INTEGER;if(i===po)return n.RGBA_INTEGER;if(i===Yr||i===qr||i===Kr||i===Zr)if(o===at)if(s=e.get("WEBGL_compressed_texture_s3tc_srgb"),s!==null){if(i===Yr)return s.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(i===qr)return s.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(i===Kr)return s.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(i===Zr)return s.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(s=e.get("WEBGL_compressed_texture_s3tc"),s!==null){if(i===Yr)return s.COMPRESSED_RGB_S3TC_DXT1_EXT;if(i===qr)return s.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(i===Kr)return s.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(i===Zr)return s.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(i===mo||i===go||i===_o||i===yo)if(s=e.get("WEBGL_compressed_texture_pvrtc"),s!==null){if(i===mo)return s.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(i===go)return s.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(i===_o)return s.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(i===yo)return s.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(i===vo||i===xo||i===Eo)if(s=e.get("WEBGL_compressed_texture_etc"),s!==null){if(i===vo||i===xo)return o===at?s.COMPRESSED_SRGB8_ETC2:s.COMPRESSED_RGB8_ETC2;if(i===Eo)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:s.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(i===So||i===To||i===Mo||i===bo||i===Ao||i===Ro||i===wo||i===Co||i===Io||i===Po||i===Lo||i===No||i===Oo||i===Do)if(s=e.get("WEBGL_compressed_texture_astc"),s!==null){if(i===So)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:s.COMPRESSED_RGBA_ASTC_4x4_KHR;if(i===To)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:s.COMPRESSED_RGBA_ASTC_5x4_KHR;if(i===Mo)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:s.COMPRESSED_RGBA_ASTC_5x5_KHR;if(i===bo)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:s.COMPRESSED_RGBA_ASTC_6x5_KHR;if(i===Ao)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:s.COMPRESSED_RGBA_ASTC_6x6_KHR;if(i===Ro)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:s.COMPRESSED_RGBA_ASTC_8x5_KHR;if(i===wo)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:s.COMPRESSED_RGBA_ASTC_8x6_KHR;if(i===Co)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:s.COMPRESSED_RGBA_ASTC_8x8_KHR;if(i===Io)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:s.COMPRESSED_RGBA_ASTC_10x5_KHR;if(i===Po)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:s.COMPRESSED_RGBA_ASTC_10x6_KHR;if(i===Lo)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:s.COMPRESSED_RGBA_ASTC_10x8_KHR;if(i===No)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:s.COMPRESSED_RGBA_ASTC_10x10_KHR;if(i===Oo)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:s.COMPRESSED_RGBA_ASTC_12x10_KHR;if(i===Do)return o===at?s.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:s.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(i===jr||i===Uo||i===Fo)if(s=e.get("EXT_texture_compression_bptc"),s!==null){if(i===jr)return o===at?s.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:s.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(i===Uo)return s.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(i===Fo)return s.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(i===Qa||i===ko||i===Bo||i===zo)if(s=e.get("EXT_texture_compression_rgtc"),s!==null){if(i===jr)return s.COMPRESSED_RED_RGTC1_EXT;if(i===ko)return s.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(i===Bo)return s.COMPRESSED_RED_GREEN_RGTC2_EXT;if(i===zo)return s.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return i===Qi?n.UNSIGNED_INT_24_8:n[i]!==void 0?n[i]:null}return{convert:t}}var Xo=class extends Ft{constructor(e=null){super(),this.sourceTexture=e,this.isExternalTexture=!0}},zg=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,Vg=`
uniform sampler2DArray depthColor;
uniform float depthWidth;
uniform float depthHeight;

void main() {

	vec2 coord = vec2( gl_FragCoord.x / depthWidth, gl_FragCoord.y / depthHeight );

	if ( coord.x >= 1.0 ) {

		gl_FragDepth = texture( depthColor, vec3( coord.x - 1.0, coord.y, 1 ) ).r;

	} else {

		gl_FragDepth = texture( depthColor, vec3( coord.x, coord.y, 0 ) ).r;

	}

}`,Sc=class{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t){if(this.texture===null){let i=new Xo(e.texture);(e.depthNear!==t.depthNear||e.depthFar!==t.depthFar)&&(this.depthNear=e.depthNear,this.depthFar=e.depthFar),this.texture=i}}getMesh(e){if(this.texture!==null&&this.mesh===null){let t=e.cameras[0].viewport,i=new fn({vertexShader:zg,fragmentShader:Vg,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new Lt(new Or(20,20),i)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}},Tc=class extends _n{constructor(e,t){super();let i=this,r=null,s=1,o=null,c="local-floor",l=1,a=null,d=null,p=null,f=null,m=null,g=null,y=new Sc,h={},u=t.getContextAttributes(),E=null,x=null,_=[],A=[],N=new ze,w=null,O=new Pt;O.viewport=new vt;let T=new Pt;T.viewport=new vt;let M=[O,T],R=new js,I=null,U=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(k){let Y=_[k];return Y===void 0&&(Y=new Hi,_[k]=Y),Y.getTargetRaySpace()},this.getControllerGrip=function(k){let Y=_[k];return Y===void 0&&(Y=new Hi,_[k]=Y),Y.getGripSpace()},this.getHand=function(k){let Y=_[k];return Y===void 0&&(Y=new Hi,_[k]=Y),Y.getHandSpace()};function P(k){let Y=A.indexOf(k.inputSource);if(Y===-1)return;let K=_[Y];K!==void 0&&(K.update(k.inputSource,k.frame,a||o),K.dispatchEvent({type:k.type,data:k.inputSource}))}function X(){r.removeEventListener("select",P),r.removeEventListener("selectstart",P),r.removeEventListener("selectend",P),r.removeEventListener("squeeze",P),r.removeEventListener("squeezestart",P),r.removeEventListener("squeezeend",P),r.removeEventListener("end",X),r.removeEventListener("inputsourceschange",W);for(let k=0;k<_.length;k++){let Y=A[k];Y!==null&&(A[k]=null,_[k].disconnect(Y))}I=null,U=null,y.reset();for(let k in h)delete h[k];e.setRenderTarget(E),m=null,f=null,p=null,r=null,x=null,Me.stop(),i.isPresenting=!1,e.setPixelRatio(w),e.setSize(N.width,N.height,!1),i.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(k){s=k,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(k){c=k,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return a||o},this.setReferenceSpace=function(k){a=k},this.getBaseLayer=function(){return f!==null?f:m},this.getBinding=function(){return p},this.getFrame=function(){return g},this.getSession=function(){return r},this.setSession=async function(k){if(r=k,r!==null){if(E=e.getRenderTarget(),r.addEventListener("select",P),r.addEventListener("selectstart",P),r.addEventListener("selectend",P),r.addEventListener("squeeze",P),r.addEventListener("squeezestart",P),r.addEventListener("squeezeend",P),r.addEventListener("end",X),r.addEventListener("inputsourceschange",W),u.xrCompatible!==!0&&await t.makeXRCompatible(),w=e.getPixelRatio(),e.getSize(N),typeof XRWebGLBinding<"u"&&(p=new XRWebGLBinding(r,t)),p!==null&&"createProjectionLayer"in XRWebGLBinding.prototype){let K=null,ne=null,ie=null;u.depth&&(ie=u.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,K=u.stencil?er:Bi,ne=u.stencil?Qi:Qn);let de={colorFormat:t.RGBA8,depthFormat:ie,scaleFactor:s};f=p.createProjectionLayer(de),r.updateRenderState({layers:[f]}),e.setPixelRatio(1),e.setSize(f.textureWidth,f.textureHeight,!1),x=new yn(f.textureWidth,f.textureHeight,{format:tn,type:pn,depthTexture:new wr(f.textureWidth,f.textureHeight,ne,void 0,void 0,void 0,void 0,void 0,void 0,K),stencilBuffer:u.stencil,colorSpace:e.outputColorSpace,samples:u.antialias?4:0,resolveDepthBuffer:f.ignoreDepthValues===!1,resolveStencilBuffer:f.ignoreDepthValues===!1})}else{let K={antialias:u.antialias,alpha:!0,depth:u.depth,stencil:u.stencil,framebufferScaleFactor:s};m=new XRWebGLLayer(r,t,K),r.updateRenderState({baseLayer:m}),e.setPixelRatio(1),e.setSize(m.framebufferWidth,m.framebufferHeight,!1),x=new yn(m.framebufferWidth,m.framebufferHeight,{format:tn,type:pn,colorSpace:e.outputColorSpace,stencilBuffer:u.stencil,resolveDepthBuffer:m.ignoreDepthValues===!1,resolveStencilBuffer:m.ignoreDepthValues===!1})}x.isXRRenderTarget=!0,this.setFoveation(l),a=null,o=await r.requestReferenceSpace(c),Me.setContext(r),Me.start(),i.isPresenting=!0,i.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(r!==null)return r.environmentBlendMode},this.getDepthTexture=function(){return y.getDepthTexture()};function W(k){for(let Y=0;Y<k.removed.length;Y++){let K=k.removed[Y],ne=A.indexOf(K);ne>=0&&(A[ne]=null,_[ne].disconnect(K))}for(let Y=0;Y<k.added.length;Y++){let K=k.added[Y],ne=A.indexOf(K);if(ne===-1){for(let de=0;de<_.length;de++)if(de>=A.length){A.push(K),ne=de;break}else if(A[de]===null){A[de]=K,ne=de;break}if(ne===-1)break}let ie=_[ne];ie&&ie.connect(K)}}let q=new Z,G=new Z;function ee(k,Y,K){q.setFromMatrixPosition(Y.matrixWorld),G.setFromMatrixPosition(K.matrixWorld);let ne=q.distanceTo(G),ie=Y.projectionMatrix.elements,de=K.projectionMatrix.elements,Le=ie[14]/(ie[10]-1),we=ie[14]/(ie[10]+1),B=(ie[9]+1)/ie[5],Ge=(ie[9]-1)/ie[5],Ne=(ie[8]-1)/ie[0],Ke=(de[8]+1)/de[0],Oe=Le*Ne,Je=Le*Ke,Re=ne/(-Ne+Ke),He=Re*-Ne;if(Y.matrixWorld.decompose(k.position,k.quaternion,k.scale),k.translateX(He),k.translateZ(Re),k.matrixWorld.compose(k.position,k.quaternion,k.scale),k.matrixWorldInverse.copy(k.matrixWorld).invert(),ie[10]===-1)k.projectionMatrix.copy(Y.projectionMatrix),k.projectionMatrixInverse.copy(Y.projectionMatrixInverse);else{let ot=Le+Re,it=we+Re,S=Oe-He,v=Je+(ne-He),b=B*we/it*ot,D=Ge*we/it*ot;k.projectionMatrix.makePerspective(S,v,b,D,ot,it),k.projectionMatrixInverse.copy(k.projectionMatrix).invert()}}function ae(k,Y){Y===null?k.matrixWorld.copy(k.matrix):k.matrixWorld.multiplyMatrices(Y.matrixWorld,k.matrix),k.matrixWorldInverse.copy(k.matrixWorld).invert()}this.updateCamera=function(k){if(r===null)return;let Y=k.near,K=k.far;y.texture!==null&&(y.depthNear>0&&(Y=y.depthNear),y.depthFar>0&&(K=y.depthFar)),R.near=T.near=O.near=Y,R.far=T.far=O.far=K,(I!==R.near||U!==R.far)&&(r.updateRenderState({depthNear:R.near,depthFar:R.far}),I=R.near,U=R.far),R.layers.mask=k.layers.mask|6,O.layers.mask=R.layers.mask&3,T.layers.mask=R.layers.mask&5;let ne=k.parent,ie=R.cameras;ae(R,ne);for(let de=0;de<ie.length;de++)ae(ie[de],ne);ie.length===2?ee(R,O,T):R.projectionMatrix.copy(O.projectionMatrix),ue(k,R,ne)};function ue(k,Y,K){K===null?k.matrix.copy(Y.matrixWorld):(k.matrix.copy(K.matrixWorld),k.matrix.invert(),k.matrix.multiply(Y.matrixWorld)),k.matrix.decompose(k.position,k.quaternion,k.scale),k.updateMatrixWorld(!0),k.projectionMatrix.copy(Y.projectionMatrix),k.projectionMatrixInverse.copy(Y.projectionMatrixInverse),k.isPerspectiveCamera&&(k.fov=zi*2*Math.atan(1/k.projectionMatrix.elements[5]),k.zoom=1)}this.getCamera=function(){return R},this.getFoveation=function(){if(!(f===null&&m===null))return l},this.setFoveation=function(k){l=k,f!==null&&(f.fixedFoveation=k),m!==null&&m.fixedFoveation!==void 0&&(m.fixedFoveation=k)},this.hasDepthSensing=function(){return y.texture!==null},this.getDepthSensingMesh=function(){return y.getMesh(R)},this.getCameraTexture=function(k){return h[k]};let _e=null;function me(k,Y){if(d=Y.getViewerPose(a||o),g=Y,d!==null){let K=d.views;m!==null&&(e.setRenderTargetFramebuffer(x,m.framebuffer),e.setRenderTarget(x));let ne=!1;K.length!==R.cameras.length&&(R.cameras.length=0,ne=!0);for(let we=0;we<K.length;we++){let B=K[we],Ge=null;if(m!==null)Ge=m.getViewport(B);else{let Ke=p.getViewSubImage(f,B);Ge=Ke.viewport,we===0&&(e.setRenderTargetTextures(x,Ke.colorTexture,Ke.depthStencilTexture),e.setRenderTarget(x))}let Ne=M[we];Ne===void 0&&(Ne=new Pt,Ne.layers.enable(we),Ne.viewport=new vt,M[we]=Ne),Ne.matrix.fromArray(B.transform.matrix),Ne.matrix.decompose(Ne.position,Ne.quaternion,Ne.scale),Ne.projectionMatrix.fromArray(B.projectionMatrix),Ne.projectionMatrixInverse.copy(Ne.projectionMatrix).invert(),Ne.viewport.set(Ge.x,Ge.y,Ge.width,Ge.height),we===0&&(R.matrix.copy(Ne.matrix),R.matrix.decompose(R.position,R.quaternion,R.scale)),ne===!0&&R.cameras.push(Ne)}let ie=r.enabledFeatures;if(ie&&ie.includes("depth-sensing")&&r.depthUsage=="gpu-optimized"&&p){let we=p.getDepthInformation(K[0]);we&&we.isValid&&we.texture&&y.init(we,r.renderState)}if(ie&&ie.includes("camera-access")&&(e.state.unbindTexture(),p))for(let we=0;we<K.length;we++){let B=K[we].camera;if(B){let Ge=h[B];Ge||(Ge=new Xo,h[B]=Ge);let Ne=p.getCameraImage(B);Ge.sourceTexture=Ne}}}for(let K=0;K<_.length;K++){let ne=A[K],ie=_[K];ne!==null&&ie!==void 0&&ie.update(ne,Y,a||o)}_e&&_e(k,Y),Y.detectedPlanes&&i.dispatchEvent({type:"planesdetected",data:Y}),g=null}let Me=new Pu;Me.setAnimationLoop(me),this.setAnimationLoop=function(k){_e=k},this.dispose=function(){}}},yi=new dn,Gg=new yt;function Hg(n,e){function t(h,u){h.matrixAutoUpdate===!0&&h.updateMatrix(),u.value.copy(h.matrix)}function i(h,u){u.color.getRGB(h.fogColor.value,oc(n)),u.isFog?(h.fogNear.value=u.near,h.fogFar.value=u.far):u.isFogExp2&&(h.fogDensity.value=u.density)}function r(h,u,E,x,_){u.isMeshBasicMaterial||u.isMeshLambertMaterial?s(h,u):u.isMeshToonMaterial?(s(h,u),p(h,u)):u.isMeshPhongMaterial?(s(h,u),d(h,u)):u.isMeshStandardMaterial?(s(h,u),f(h,u),u.isMeshPhysicalMaterial&&m(h,u,_)):u.isMeshMatcapMaterial?(s(h,u),g(h,u)):u.isMeshDepthMaterial?s(h,u):u.isMeshDistanceMaterial?(s(h,u),y(h,u)):u.isMeshNormalMaterial?s(h,u):u.isLineBasicMaterial?(o(h,u),u.isLineDashedMaterial&&c(h,u)):u.isPointsMaterial?l(h,u,E,x):u.isSpriteMaterial?a(h,u):u.isShadowMaterial?(h.color.value.copy(u.color),h.opacity.value=u.opacity):u.isShaderMaterial&&(u.uniformsNeedUpdate=!1)}function s(h,u){h.opacity.value=u.opacity,u.color&&h.diffuse.value.copy(u.color),u.emissive&&h.emissive.value.copy(u.emissive).multiplyScalar(u.emissiveIntensity),u.map&&(h.map.value=u.map,t(u.map,h.mapTransform)),u.alphaMap&&(h.alphaMap.value=u.alphaMap,t(u.alphaMap,h.alphaMapTransform)),u.bumpMap&&(h.bumpMap.value=u.bumpMap,t(u.bumpMap,h.bumpMapTransform),h.bumpScale.value=u.bumpScale,u.side===wt&&(h.bumpScale.value*=-1)),u.normalMap&&(h.normalMap.value=u.normalMap,t(u.normalMap,h.normalMapTransform),h.normalScale.value.copy(u.normalScale),u.side===wt&&h.normalScale.value.negate()),u.displacementMap&&(h.displacementMap.value=u.displacementMap,t(u.displacementMap,h.displacementMapTransform),h.displacementScale.value=u.displacementScale,h.displacementBias.value=u.displacementBias),u.emissiveMap&&(h.emissiveMap.value=u.emissiveMap,t(u.emissiveMap,h.emissiveMapTransform)),u.specularMap&&(h.specularMap.value=u.specularMap,t(u.specularMap,h.specularMapTransform)),u.alphaTest>0&&(h.alphaTest.value=u.alphaTest);let E=e.get(u),x=E.envMap,_=E.envMapRotation;x&&(h.envMap.value=x,yi.copy(_),yi.x*=-1,yi.y*=-1,yi.z*=-1,x.isCubeTexture&&x.isRenderTargetTexture===!1&&(yi.y*=-1,yi.z*=-1),h.envMapRotation.value.setFromMatrix4(Gg.makeRotationFromEuler(yi)),h.flipEnvMap.value=x.isCubeTexture&&x.isRenderTargetTexture===!1?-1:1,h.reflectivity.value=u.reflectivity,h.ior.value=u.ior,h.refractionRatio.value=u.refractionRatio),u.lightMap&&(h.lightMap.value=u.lightMap,h.lightMapIntensity.value=u.lightMapIntensity,t(u.lightMap,h.lightMapTransform)),u.aoMap&&(h.aoMap.value=u.aoMap,h.aoMapIntensity.value=u.aoMapIntensity,t(u.aoMap,h.aoMapTransform))}function o(h,u){h.diffuse.value.copy(u.color),h.opacity.value=u.opacity,u.map&&(h.map.value=u.map,t(u.map,h.mapTransform))}function c(h,u){h.dashSize.value=u.dashSize,h.totalSize.value=u.dashSize+u.gapSize,h.scale.value=u.scale}function l(h,u,E,x){h.diffuse.value.copy(u.color),h.opacity.value=u.opacity,h.size.value=u.size*E,h.scale.value=x*.5,u.map&&(h.map.value=u.map,t(u.map,h.uvTransform)),u.alphaMap&&(h.alphaMap.value=u.alphaMap,t(u.alphaMap,h.alphaMapTransform)),u.alphaTest>0&&(h.alphaTest.value=u.alphaTest)}function a(h,u){h.diffuse.value.copy(u.color),h.opacity.value=u.opacity,h.rotation.value=u.rotation,u.map&&(h.map.value=u.map,t(u.map,h.mapTransform)),u.alphaMap&&(h.alphaMap.value=u.alphaMap,t(u.alphaMap,h.alphaMapTransform)),u.alphaTest>0&&(h.alphaTest.value=u.alphaTest)}function d(h,u){h.specular.value.copy(u.specular),h.shininess.value=Math.max(u.shininess,1e-4)}function p(h,u){u.gradientMap&&(h.gradientMap.value=u.gradientMap)}function f(h,u){h.metalness.value=u.metalness,u.metalnessMap&&(h.metalnessMap.value=u.metalnessMap,t(u.metalnessMap,h.metalnessMapTransform)),h.roughness.value=u.roughness,u.roughnessMap&&(h.roughnessMap.value=u.roughnessMap,t(u.roughnessMap,h.roughnessMapTransform)),u.envMap&&(h.envMapIntensity.value=u.envMapIntensity)}function m(h,u,E){h.ior.value=u.ior,u.sheen>0&&(h.sheenColor.value.copy(u.sheenColor).multiplyScalar(u.sheen),h.sheenRoughness.value=u.sheenRoughness,u.sheenColorMap&&(h.sheenColorMap.value=u.sheenColorMap,t(u.sheenColorMap,h.sheenColorMapTransform)),u.sheenRoughnessMap&&(h.sheenRoughnessMap.value=u.sheenRoughnessMap,t(u.sheenRoughnessMap,h.sheenRoughnessMapTransform))),u.clearcoat>0&&(h.clearcoat.value=u.clearcoat,h.clearcoatRoughness.value=u.clearcoatRoughness,u.clearcoatMap&&(h.clearcoatMap.value=u.clearcoatMap,t(u.clearcoatMap,h.clearcoatMapTransform)),u.clearcoatRoughnessMap&&(h.clearcoatRoughnessMap.value=u.clearcoatRoughnessMap,t(u.clearcoatRoughnessMap,h.clearcoatRoughnessMapTransform)),u.clearcoatNormalMap&&(h.clearcoatNormalMap.value=u.clearcoatNormalMap,t(u.clearcoatNormalMap,h.clearcoatNormalMapTransform),h.clearcoatNormalScale.value.copy(u.clearcoatNormalScale),u.side===wt&&h.clearcoatNormalScale.value.negate())),u.dispersion>0&&(h.dispersion.value=u.dispersion),u.iridescence>0&&(h.iridescence.value=u.iridescence,h.iridescenceIOR.value=u.iridescenceIOR,h.iridescenceThicknessMinimum.value=u.iridescenceThicknessRange[0],h.iridescenceThicknessMaximum.value=u.iridescenceThicknessRange[1],u.iridescenceMap&&(h.iridescenceMap.value=u.iridescenceMap,t(u.iridescenceMap,h.iridescenceMapTransform)),u.iridescenceThicknessMap&&(h.iridescenceThicknessMap.value=u.iridescenceThicknessMap,t(u.iridescenceThicknessMap,h.iridescenceThicknessMapTransform))),u.transmission>0&&(h.transmission.value=u.transmission,h.transmissionSamplerMap.value=E.texture,h.transmissionSamplerSize.value.set(E.width,E.height),u.transmissionMap&&(h.transmissionMap.value=u.transmissionMap,t(u.transmissionMap,h.transmissionMapTransform)),h.thickness.value=u.thickness,u.thicknessMap&&(h.thicknessMap.value=u.thicknessMap,t(u.thicknessMap,h.thicknessMapTransform)),h.attenuationDistance.value=u.attenuationDistance,h.attenuationColor.value.copy(u.attenuationColor)),u.anisotropy>0&&(h.anisotropyVector.value.set(u.anisotropy*Math.cos(u.anisotropyRotation),u.anisotropy*Math.sin(u.anisotropyRotation)),u.anisotropyMap&&(h.anisotropyMap.value=u.anisotropyMap,t(u.anisotropyMap,h.anisotropyMapTransform))),h.specularIntensity.value=u.specularIntensity,h.specularColor.value.copy(u.specularColor),u.specularColorMap&&(h.specularColorMap.value=u.specularColorMap,t(u.specularColorMap,h.specularColorMapTransform)),u.specularIntensityMap&&(h.specularIntensityMap.value=u.specularIntensityMap,t(u.specularIntensityMap,h.specularIntensityMapTransform))}function g(h,u){u.matcap&&(h.matcap.value=u.matcap)}function y(h,u){let E=e.get(u).light;h.referencePosition.value.setFromMatrixPosition(E.matrixWorld),h.nearDistance.value=E.shadow.camera.near,h.farDistance.value=E.shadow.camera.far}return{refreshFogUniforms:i,refreshMaterialUniforms:r}}function Wg(n,e,t,i){let r={},s={},o=[],c=n.getParameter(n.MAX_UNIFORM_BUFFER_BINDINGS);function l(E,x){let _=x.program;i.uniformBlockBinding(E,_)}function a(E,x){let _=r[E.id];_===void 0&&(g(E),_=d(E),r[E.id]=_,E.addEventListener("dispose",h));let A=x.program;i.updateUBOMapping(E,A);let N=e.render.frame;s[E.id]!==N&&(f(E),s[E.id]=N)}function d(E){let x=p();E.__bindingPointIndex=x;let _=n.createBuffer(),A=E.__size,N=E.usage;return n.bindBuffer(n.UNIFORM_BUFFER,_),n.bufferData(n.UNIFORM_BUFFER,A,N),n.bindBuffer(n.UNIFORM_BUFFER,null),n.bindBufferBase(n.UNIFORM_BUFFER,x,_),_}function p(){for(let E=0;E<c;E++)if(o.indexOf(E)===-1)return o.push(E),E;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function f(E){let x=r[E.id],_=E.uniforms,A=E.__cache;n.bindBuffer(n.UNIFORM_BUFFER,x);for(let N=0,w=_.length;N<w;N++){let O=Array.isArray(_[N])?_[N]:[_[N]];for(let T=0,M=O.length;T<M;T++){let R=O[T];if(m(R,N,T,A)===!0){let I=R.__offset,U=Array.isArray(R.value)?R.value:[R.value],P=0;for(let X=0;X<U.length;X++){let W=U[X],q=y(W);typeof W=="number"||typeof W=="boolean"?(R.__data[0]=W,n.bufferSubData(n.UNIFORM_BUFFER,I+P,R.__data)):W.isMatrix3?(R.__data[0]=W.elements[0],R.__data[1]=W.elements[1],R.__data[2]=W.elements[2],R.__data[3]=0,R.__data[4]=W.elements[3],R.__data[5]=W.elements[4],R.__data[6]=W.elements[5],R.__data[7]=0,R.__data[8]=W.elements[6],R.__data[9]=W.elements[7],R.__data[10]=W.elements[8],R.__data[11]=0):(W.toArray(R.__data,P),P+=q.storage/Float32Array.BYTES_PER_ELEMENT)}n.bufferSubData(n.UNIFORM_BUFFER,I,R.__data)}}}n.bindBuffer(n.UNIFORM_BUFFER,null)}function m(E,x,_,A){let N=E.value,w=x+"_"+_;if(A[w]===void 0)return typeof N=="number"||typeof N=="boolean"?A[w]=N:A[w]=N.clone(),!0;{let O=A[w];if(typeof N=="number"||typeof N=="boolean"){if(O!==N)return A[w]=N,!0}else if(O.equals(N)===!1)return O.copy(N),!0}return!1}function g(E){let x=E.uniforms,_=0,A=16;for(let w=0,O=x.length;w<O;w++){let T=Array.isArray(x[w])?x[w]:[x[w]];for(let M=0,R=T.length;M<R;M++){let I=T[M],U=Array.isArray(I.value)?I.value:[I.value];for(let P=0,X=U.length;P<X;P++){let W=U[P],q=y(W),G=_%A,ee=G%q.boundary,ae=G+ee;_+=ee,ae!==0&&A-ae<q.storage&&(_+=A-ae),I.__data=new Float32Array(q.storage/Float32Array.BYTES_PER_ELEMENT),I.__offset=_,_+=q.storage}}}let N=_%A;return N>0&&(_+=A-N),E.__size=_,E.__cache={},this}function y(E){let x={boundary:0,storage:0};return typeof E=="number"||typeof E=="boolean"?(x.boundary=4,x.storage=4):E.isVector2?(x.boundary=8,x.storage=8):E.isVector3||E.isColor?(x.boundary=16,x.storage=12):E.isVector4?(x.boundary=16,x.storage=16):E.isMatrix3?(x.boundary=48,x.storage=48):E.isMatrix4?(x.boundary=64,x.storage=64):E.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",E),x}function h(E){let x=E.target;x.removeEventListener("dispose",h);let _=o.indexOf(x.__bindingPointIndex);o.splice(_,1),n.deleteBuffer(r[x.id]),delete r[x.id],delete s[x.id]}function u(){for(let E in r)n.deleteBuffer(r[E]);o=[],r={},s={}}return{bind:l,update:a,dispose:u}}var Yo=class{constructor(e={}){let{canvas:t=Ql(),context:i=null,depth:r=!0,stencil:s=!1,alpha:o=!1,antialias:c=!1,premultipliedAlpha:l=!0,preserveDrawingBuffer:a=!1,powerPreference:d="default",failIfMajorPerformanceCaveat:p=!1,reversedDepthBuffer:f=!1}=e;this.isWebGLRenderer=!0;let m;if(i!==null){if(typeof WebGLRenderingContext<"u"&&i instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");m=i.getContextAttributes().alpha}else m=o;let g=new Uint32Array(4),y=new Int32Array(4),h=null,u=null,E=[],x=[];this.domElement=t,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this.toneMapping=On,this.toneMappingExposure=1,this.transmissionResolutionScale=1;let _=this,A=!1;this._outputColorSpace=pt;let N=0,w=0,O=null,T=-1,M=null,R=new vt,I=new vt,U=null,P=new qe(0),X=0,W=t.width,q=t.height,G=1,ee=null,ae=null,ue=new vt(0,0,W,q),_e=new vt(0,0,W,q),me=!1,Me=new Wi,k=!1,Y=!1,K=new yt,ne=new Z,ie=new vt,de={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0},Le=!1;function we(){return O===null?G:1}let B=i;function Ge(C,J){return t.getContext(C,J)}try{let C={alpha:!0,depth:r,stencil:s,antialias:c,premultipliedAlpha:l,preserveDrawingBuffer:a,powerPreference:d,failIfMajorPerformanceCaveat:p};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${"179"}`),t.addEventListener("webglcontextlost",fe,!1),t.addEventListener("webglcontextrestored",ge,!1),t.addEventListener("webglcontextcreationerror",he,!1),B===null){let J="webgl2";if(B=Ge(J,C),B===null)throw Ge(J)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(C){throw console.error("THREE.WebGLRenderer: "+C.message),C}let Ne,Ke,Oe,Je,Re,He,ot,it,S,v,b,D,L,F,H,z,j,te,Q,ce,Ee,Se,pe,xe;function V(){Ne=new cm(B),Ne.init(),Se=new Bg(B,Ne),Ke=new tm(B,Ne,e,Se),Oe=new Fg(B,Ne),Ke.reversedDepthBuffer&&f&&Oe.buffers.depth.setReversed(!0),Je=new hm(B),Re=new Mg,He=new kg(B,Ne,Oe,Re,Ke,Se,Je),ot=new im(_),it=new am(_),S=new gd(B),pe=new Qp(B,S),v=new lm(B,S,Je,pe),b=new fm(B,v,S,Je),Q=new dm(B,Ke,He),z=new nm(Re),D=new Tg(_,ot,it,Ne,Ke,pe,z),L=new Hg(_,Re),F=new Ag,H=new Lg(Ne),te=new $p(_,ot,it,Oe,b,m,l),j=new Dg(_,b,Ke),xe=new Wg(B,Je,Ke,Oe),ce=new em(B,Ne,Je),Ee=new um(B,Ne,Je),Je.programs=D.programs,_.capabilities=Ke,_.extensions=Ne,_.properties=Re,_.renderLists=F,_.shadowMap=j,_.state=Oe,_.info=Je}V();let le=new Tc(_,B);this.xr=le,this.getContext=function(){return B},this.getContextAttributes=function(){return B.getContextAttributes()},this.forceContextLoss=function(){let C=Ne.get("WEBGL_lose_context");C&&C.loseContext()},this.forceContextRestore=function(){let C=Ne.get("WEBGL_lose_context");C&&C.restoreContext()},this.getPixelRatio=function(){return G},this.setPixelRatio=function(C){C!==void 0&&(G=C,this.setSize(W,q,!1))},this.getSize=function(C){return C.set(W,q)},this.setSize=function(C,J,re=!0){if(le.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}W=C,q=J,t.width=Math.floor(C*G),t.height=Math.floor(J*G),re===!0&&(t.style.width=C+"px",t.style.height=J+"px"),this.setViewport(0,0,C,J)},this.getDrawingBufferSize=function(C){return C.set(W*G,q*G).floor()},this.setDrawingBufferSize=function(C,J,re){W=C,q=J,G=re,t.width=Math.floor(C*re),t.height=Math.floor(J*re),this.setViewport(0,0,C,J)},this.getCurrentViewport=function(C){return C.copy(R)},this.getViewport=function(C){return C.copy(ue)},this.setViewport=function(C,J,re,se){C.isVector4?ue.set(C.x,C.y,C.z,C.w):ue.set(C,J,re,se),Oe.viewport(R.copy(ue).multiplyScalar(G).round())},this.getScissor=function(C){return C.copy(_e)},this.setScissor=function(C,J,re,se){C.isVector4?_e.set(C.x,C.y,C.z,C.w):_e.set(C,J,re,se),Oe.scissor(I.copy(_e).multiplyScalar(G).round())},this.getScissorTest=function(){return me},this.setScissorTest=function(C){Oe.setScissorTest(me=C)},this.setOpaqueSort=function(C){ee=C},this.setTransparentSort=function(C){ae=C},this.getClearColor=function(C){return C.copy(te.getClearColor())},this.setClearColor=function(){te.setClearColor(...arguments)},this.getClearAlpha=function(){return te.getClearAlpha()},this.setClearAlpha=function(){te.setClearAlpha(...arguments)},this.clear=function(C=!0,J=!0,re=!0){let se=0;if(C){let $=!1;if(O!==null){let ye=O.texture.format;$=ye===po||ye===fo||ye===ho}if($){let ye=O.texture.type,Ce=ye===pn||ye===Qn||ye===Ji||ye===Qi||ye===lo||ye===uo,Ue=te.getClearColor(),Pe=te.getClearAlpha(),Xe=Ue.r,Ye=Ue.g,Ve=Ue.b;Ce?(g[0]=Xe,g[1]=Ye,g[2]=Ve,g[3]=Pe,B.clearBufferuiv(B.COLOR,0,g)):(y[0]=Xe,y[1]=Ye,y[2]=Ve,y[3]=Pe,B.clearBufferiv(B.COLOR,0,y))}else se|=B.COLOR_BUFFER_BIT}J&&(se|=B.DEPTH_BUFFER_BIT),re&&(se|=B.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),B.clear(se)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){t.removeEventListener("webglcontextlost",fe,!1),t.removeEventListener("webglcontextrestored",ge,!1),t.removeEventListener("webglcontextcreationerror",he,!1),te.dispose(),F.dispose(),H.dispose(),Re.dispose(),ot.dispose(),it.dispose(),b.dispose(),pe.dispose(),xe.dispose(),D.dispose(),le.dispose(),le.removeEventListener("sessionstart",be),le.removeEventListener("sessionend",Be),ke.stop()};function fe(C){C.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),A=!0}function ge(){console.log("THREE.WebGLRenderer: Context Restored."),A=!1;let C=Je.autoReset,J=j.enabled,re=j.autoUpdate,se=j.needsUpdate,$=j.type;V(),Je.autoReset=C,j.enabled=J,j.autoUpdate=re,j.needsUpdate=se,j.type=$}function he(C){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",C.statusMessage)}function oe(C){let J=C.target;J.removeEventListener("dispose",oe),Te(J)}function Te(C){Fe(C),Re.remove(C)}function Fe(C){let J=Re.get(C).programs;J!==void 0&&(J.forEach(function(re){D.releaseProgram(re)}),C.isShaderMaterial&&D.releaseShaderCache(C))}this.renderBufferDirect=function(C,J,re,se,$,ye){J===null&&(J=de);let Ce=$.isMesh&&$.matrixWorld.determinant()<0,Ue=qu(C,J,re,se,$);Oe.setMaterial(se,Ce);let Pe=re.index,Xe=1;if(se.wireframe===!0){if(Pe=v.getWireframeAttribute(re),Pe===void 0)return;Xe=2}let Ye=re.drawRange,Ve=re.attributes.position,tt=Ye.start*Xe,ct=(Ye.start+Ye.count)*Xe;ye!==null&&(tt=Math.max(tt,ye.start*Xe),ct=Math.min(ct,(ye.start+ye.count)*Xe)),Pe!==null?(tt=Math.max(tt,0),ct=Math.min(ct,Pe.count)):Ve!=null&&(tt=Math.max(tt,0),ct=Math.min(ct,Ve.count));let xt=ct-tt;if(xt<0||xt===1/0)return;pe.setup($,se,Ue,re,Pe);let dt,ht=ce;if(Pe!==null&&(dt=S.get(Pe),ht=Ee,ht.setIndex(dt)),$.isMesh)se.wireframe===!0?(Oe.setLineWidth(se.wireframeLinewidth*we()),ht.setMode(B.LINES)):ht.setMode(B.TRIANGLES);else if($.isLine){let We=se.linewidth;We===void 0&&(We=1),Oe.setLineWidth(We*we()),$.isLineSegments?ht.setMode(B.LINES):$.isLineLoop?ht.setMode(B.LINE_LOOP):ht.setMode(B.LINE_STRIP)}else $.isPoints?ht.setMode(B.POINTS):$.isSprite&&ht.setMode(B.TRIANGLES);if($.isBatchedMesh)if($._multiDrawInstances!==null)li("THREE.WebGLRenderer: renderMultiDrawInstances has been deprecated and will be removed in r184. Append to renderMultiDraw arguments and use indirection."),ht.renderMultiDrawInstances($._multiDrawStarts,$._multiDrawCounts,$._multiDrawCount,$._multiDrawInstances);else if(Ne.get("WEBGL_multi_draw"))ht.renderMultiDraw($._multiDrawStarts,$._multiDrawCounts,$._multiDrawCount);else{let We=$._multiDrawStarts,mt=$._multiDrawCounts,rt=$._multiDrawCount,Gt=Pe?S.get(Pe).bytesPerElement:1,Si=Re.get(se).currentProgram.getUniforms();for(let Ht=0;Ht<rt;Ht++)Si.setValue(B,"_gl_DrawID",Ht),ht.render(We[Ht]/Gt,mt[Ht])}else if($.isInstancedMesh)ht.renderInstances(tt,xt,$.count);else if(re.isInstancedBufferGeometry){let We=re._maxInstanceCount!==void 0?re._maxInstanceCount:1/0,mt=Math.min(re.instanceCount,We);ht.renderInstances(tt,xt,mt)}else ht.render(tt,xt)};function De(C,J,re){C.transparent===!0&&C.side===en&&C.forceSinglePass===!1?(C.side=wt,C.needsUpdate=!0,ts(C,J,re),C.side=un,C.needsUpdate=!0,ts(C,J,re),C.side=en):ts(C,J,re)}this.compile=function(C,J,re=null){re===null&&(re=C),u=H.get(re),u.init(J),x.push(u),re.traverseVisible(function($){$.isLight&&$.layers.test(J.layers)&&(u.pushLight($),$.castShadow&&u.pushShadow($))}),C!==re&&C.traverseVisible(function($){$.isLight&&$.layers.test(J.layers)&&(u.pushLight($),$.castShadow&&u.pushShadow($))}),u.setupLights();let se=new Set;return C.traverse(function($){if(!($.isMesh||$.isPoints||$.isLine||$.isSprite))return;let ye=$.material;if(ye)if(Array.isArray(ye))for(let Ce=0;Ce<ye.length;Ce++){let Ue=ye[Ce];De(Ue,re,$),se.add(Ue)}else De(ye,re,$),se.add(ye)}),u=x.pop(),se},this.compileAsync=function(C,J,re=null){let se=this.compile(C,J,re);return new Promise($=>{function ye(){if(se.forEach(function(Ce){Re.get(Ce).currentProgram.isReady()&&se.delete(Ce)}),se.size===0){$(C);return}setTimeout(ye,10)}Ne.get("KHR_parallel_shader_compile")!==null?ye():setTimeout(ye,10)})};let ve=null;function Ie(C){ve&&ve(C)}function be(){ke.stop()}function Be(){ke.start()}let ke=new Pu;ke.setAnimationLoop(Ie),typeof self<"u"&&ke.setContext(self),this.setAnimationLoop=function(C){ve=C,le.setAnimationLoop(C),C===null?ke.stop():ke.start()},le.addEventListener("sessionstart",be),le.addEventListener("sessionend",Be),this.render=function(C,J){if(J!==void 0&&J.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(A===!0)return;if(C.matrixWorldAutoUpdate===!0&&C.updateMatrixWorld(),J.parent===null&&J.matrixWorldAutoUpdate===!0&&J.updateMatrixWorld(),le.enabled===!0&&le.isPresenting===!0&&(le.cameraAutoUpdate===!0&&le.updateCamera(J),J=le.getCamera()),C.isScene===!0&&C.onBeforeRender(_,C,J,O),u=H.get(C,x.length),u.init(J),x.push(u),K.multiplyMatrices(J.projectionMatrix,J.matrixWorldInverse),Me.setFromProjectionMatrix(K,ln,J.reversedDepth),Y=this.localClippingEnabled,k=z.init(this.clippingPlanes,Y),h=F.get(C,E.length),h.init(),E.push(h),le.enabled===!0&&le.isPresenting===!0){let ye=_.xr.getDepthSensingMesh();ye!==null&&ut(ye,J,-1/0,_.sortObjects)}ut(C,J,0,_.sortObjects),h.finish(),_.sortObjects===!0&&h.sort(ee,ae),Le=le.enabled===!1||le.isPresenting===!1||le.hasDepthSensing()===!1,Le&&te.addToRenderList(h,C),this.info.render.frame++,k===!0&&z.beginShadows();let re=u.state.shadowsArray;j.render(re,C,J),k===!0&&z.endShadows(),this.info.autoReset===!0&&this.info.reset();let se=h.opaque,$=h.transmissive;if(u.setupLights(),J.isArrayCamera){let ye=J.cameras;if($.length>0)for(let Ce=0,Ue=ye.length;Ce<Ue;Ce++){let Pe=ye[Ce];sn(se,$,C,Pe)}Le&&te.render(C);for(let Ce=0,Ue=ye.length;Ce<Ue;Ce++){let Pe=ye[Ce];rn(h,C,Pe,Pe.viewport)}}else $.length>0&&sn(se,$,C,J),Le&&te.render(C),rn(h,C,J);O!==null&&w===0&&(He.updateMultisampleRenderTarget(O),He.updateRenderTargetMipmap(O)),C.isScene===!0&&C.onAfterRender(_,C,J),pe.resetDefaultState(),T=-1,M=null,x.pop(),x.length>0?(u=x[x.length-1],k===!0&&z.setGlobalState(_.clippingPlanes,u.state.camera)):u=null,E.pop(),E.length>0?h=E[E.length-1]:h=null};function ut(C,J,re,se){if(C.visible===!1)return;if(C.layers.test(J.layers)){if(C.isGroup)re=C.renderOrder;else if(C.isLOD)C.autoUpdate===!0&&C.update(J);else if(C.isLight)u.pushLight(C),C.castShadow&&u.pushShadow(C);else if(C.isSprite){if(!C.frustumCulled||Me.intersectsSprite(C)){se&&ie.setFromMatrixPosition(C.matrixWorld).applyMatrix4(K);let Ce=b.update(C),Ue=C.material;Ue.visible&&h.push(C,Ce,Ue,re,ie.z,null)}}else if((C.isMesh||C.isLine||C.isPoints)&&(!C.frustumCulled||Me.intersectsObject(C))){let Ce=b.update(C),Ue=C.material;if(se&&(C.boundingSphere!==void 0?(C.boundingSphere===null&&C.computeBoundingSphere(),ie.copy(C.boundingSphere.center)):(Ce.boundingSphere===null&&Ce.computeBoundingSphere(),ie.copy(Ce.boundingSphere.center)),ie.applyMatrix4(C.matrixWorld).applyMatrix4(K)),Array.isArray(Ue)){let Pe=Ce.groups;for(let Xe=0,Ye=Pe.length;Xe<Ye;Xe++){let Ve=Pe[Xe],tt=Ue[Ve.materialIndex];tt&&tt.visible&&h.push(C,Ce,tt,re,ie.z,Ve)}}else Ue.visible&&h.push(C,Ce,Ue,re,ie.z,null)}}let ye=C.children;for(let Ce=0,Ue=ye.length;Ce<Ue;Ce++)ut(ye[Ce],J,re,se)}function rn(C,J,re,se){let $=C.opaque,ye=C.transmissive,Ce=C.transparent;u.setupLightsView(re),k===!0&&z.setGlobalState(_.clippingPlanes,re),se&&Oe.viewport(R.copy(se)),$.length>0&&Un($,J,re),ye.length>0&&Un(ye,J,re),Ce.length>0&&Un(Ce,J,re),Oe.buffers.depth.setTest(!0),Oe.buffers.depth.setMask(!0),Oe.buffers.color.setMask(!0),Oe.setPolygonOffset(!1)}function sn(C,J,re,se){if((re.isScene===!0?re.overrideMaterial:null)!==null)return;u.state.transmissionRenderTarget[se.id]===void 0&&(u.state.transmissionRenderTarget[se.id]=new yn(1,1,{generateMipmaps:!0,type:Ne.has("EXT_color_buffer_half_float")||Ne.has("EXT_color_buffer_float")?$i:pn,minFilter:$n,samples:4,stencilBuffer:s,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:nt.workingColorSpace}));let ye=u.state.transmissionRenderTarget[se.id],Ce=se.viewport||R;ye.setSize(Ce.z*_.transmissionResolutionScale,Ce.w*_.transmissionResolutionScale);let Ue=_.getRenderTarget(),Pe=_.getActiveCubeFace(),Xe=_.getActiveMipmapLevel();_.setRenderTarget(ye),_.getClearColor(P),X=_.getClearAlpha(),X<1&&_.setClearColor(16777215,.5),_.clear(),Le&&te.render(re);let Ye=_.toneMapping;_.toneMapping=On;let Ve=se.viewport;if(se.viewport!==void 0&&(se.viewport=void 0),u.setupLightsView(se),k===!0&&z.setGlobalState(_.clippingPlanes,se),Un(C,re,se),He.updateMultisampleRenderTarget(ye),He.updateRenderTargetMipmap(ye),Ne.has("WEBGL_multisampled_render_to_texture")===!1){let tt=!1;for(let ct=0,xt=J.length;ct<xt;ct++){let dt=J[ct],ht=dt.object,We=dt.geometry,mt=dt.material,rt=dt.group;if(mt.side===en&&ht.layers.test(se.layers)){let Gt=mt.side;mt.side=wt,mt.needsUpdate=!0,Oc(ht,re,se,We,mt,rt),mt.side=Gt,mt.needsUpdate=!0,tt=!0}}tt===!0&&(He.updateMultisampleRenderTarget(ye),He.updateRenderTargetMipmap(ye))}_.setRenderTarget(Ue,Pe,Xe),_.setClearColor(P,X),Ve!==void 0&&(se.viewport=Ve),_.toneMapping=Ye}function Un(C,J,re){let se=J.isScene===!0?J.overrideMaterial:null;for(let $=0,ye=C.length;$<ye;$++){let Ce=C[$],Ue=Ce.object,Pe=Ce.geometry,Xe=Ce.group,Ye=Ce.material;Ye.allowOverride===!0&&se!==null&&(Ye=se),Ue.layers.test(re.layers)&&Oc(Ue,J,re,Pe,Ye,Xe)}}function Oc(C,J,re,se,$,ye){C.onBeforeRender(_,J,re,se,$,ye),C.modelViewMatrix.multiplyMatrices(re.matrixWorldInverse,C.matrixWorld),C.normalMatrix.getNormalMatrix(C.modelViewMatrix),$.onBeforeRender(_,J,re,se,C,ye),$.transparent===!0&&$.side===en&&$.forceSinglePass===!1?($.side=wt,$.needsUpdate=!0,_.renderBufferDirect(re,J,se,$,C,ye),$.side=un,$.needsUpdate=!0,_.renderBufferDirect(re,J,se,$,C,ye),$.side=en):_.renderBufferDirect(re,J,se,$,C,ye),C.onAfterRender(_,J,re,se,$,ye)}function ts(C,J,re){J.isScene!==!0&&(J=de);let se=Re.get(C),$=u.state.lights,ye=u.state.shadowsArray,Ce=$.state.version,Ue=D.getParameters(C,$.state,ye,J,re),Pe=D.getProgramCacheKey(Ue),Xe=se.programs;se.environment=C.isMeshStandardMaterial?J.environment:null,se.fog=J.fog,se.envMap=(C.isMeshStandardMaterial?it:ot).get(C.envMap||se.environment),se.envMapRotation=se.environment!==null&&C.envMap===null?J.environmentRotation:C.envMapRotation,Xe===void 0&&(C.addEventListener("dispose",oe),Xe=new Map,se.programs=Xe);let Ye=Xe.get(Pe);if(Ye!==void 0){if(se.currentProgram===Ye&&se.lightsStateVersion===Ce)return Uc(C,Ue),Ye}else Ue.uniforms=D.getUniforms(C),C.onBeforeCompile(Ue,_),Ye=D.acquireProgram(Ue,Pe),Xe.set(Pe,Ye),se.uniforms=Ue.uniforms;let Ve=se.uniforms;return(!C.isShaderMaterial&&!C.isRawShaderMaterial||C.clipping===!0)&&(Ve.clippingPlanes=z.uniform),Uc(C,Ue),se.needsLights=Zu(C),se.lightsStateVersion=Ce,se.needsLights&&(Ve.ambientLightColor.value=$.state.ambient,Ve.lightProbe.value=$.state.probe,Ve.directionalLights.value=$.state.directional,Ve.directionalLightShadows.value=$.state.directionalShadow,Ve.spotLights.value=$.state.spot,Ve.spotLightShadows.value=$.state.spotShadow,Ve.rectAreaLights.value=$.state.rectArea,Ve.ltc_1.value=$.state.rectAreaLTC1,Ve.ltc_2.value=$.state.rectAreaLTC2,Ve.pointLights.value=$.state.point,Ve.pointLightShadows.value=$.state.pointShadow,Ve.hemisphereLights.value=$.state.hemi,Ve.directionalShadowMap.value=$.state.directionalShadowMap,Ve.directionalShadowMatrix.value=$.state.directionalShadowMatrix,Ve.spotShadowMap.value=$.state.spotShadowMap,Ve.spotLightMatrix.value=$.state.spotLightMatrix,Ve.spotLightMap.value=$.state.spotLightMap,Ve.pointShadowMap.value=$.state.pointShadowMap,Ve.pointShadowMatrix.value=$.state.pointShadowMatrix),se.currentProgram=Ye,se.uniformsList=null,Ye}function Dc(C){if(C.uniformsList===null){let J=C.currentProgram.getUniforms();C.uniformsList=rr.seqWithValue(J.seq,C.uniforms)}return C.uniformsList}function Uc(C,J){let re=Re.get(C);re.outputColorSpace=J.outputColorSpace,re.batching=J.batching,re.batchingColor=J.batchingColor,re.instancing=J.instancing,re.instancingColor=J.instancingColor,re.instancingMorph=J.instancingMorph,re.skinning=J.skinning,re.morphTargets=J.morphTargets,re.morphNormals=J.morphNormals,re.morphColors=J.morphColors,re.morphTargetsCount=J.morphTargetsCount,re.numClippingPlanes=J.numClippingPlanes,re.numIntersection=J.numClipIntersection,re.vertexAlphas=J.vertexAlphas,re.vertexTangents=J.vertexTangents,re.toneMapping=J.toneMapping}function qu(C,J,re,se,$){J.isScene!==!0&&(J=de),He.resetTextureUnits();let ye=J.fog,Ce=se.isMeshStandardMaterial?J.environment:null,Ue=O===null?_.outputColorSpace:O.isXRRenderTarget===!0?O.texture.colorSpace:ci,Pe=(se.isMeshStandardMaterial?it:ot).get(se.envMap||Ce),Xe=se.vertexColors===!0&&!!re.attributes.color&&re.attributes.color.itemSize===4,Ye=!!re.attributes.tangent&&(!!se.normalMap||se.anisotropy>0),Ve=!!re.morphAttributes.position,tt=!!re.morphAttributes.normal,ct=!!re.morphAttributes.color,xt=On;se.toneMapped&&(O===null||O.isXRRenderTarget===!0)&&(xt=_.toneMapping);let dt=re.morphAttributes.position||re.morphAttributes.normal||re.morphAttributes.color,ht=dt!==void 0?dt.length:0,We=Re.get(se),mt=u.state.lights;if(k===!0&&(Y===!0||C!==M)){let Ot=C===M&&se.id===T;z.setState(se,C,Ot)}let rt=!1;se.version===We.__version?(We.needsLights&&We.lightsStateVersion!==mt.state.version||We.outputColorSpace!==Ue||$.isBatchedMesh&&We.batching===!1||!$.isBatchedMesh&&We.batching===!0||$.isBatchedMesh&&We.batchingColor===!0&&$.colorTexture===null||$.isBatchedMesh&&We.batchingColor===!1&&$.colorTexture!==null||$.isInstancedMesh&&We.instancing===!1||!$.isInstancedMesh&&We.instancing===!0||$.isSkinnedMesh&&We.skinning===!1||!$.isSkinnedMesh&&We.skinning===!0||$.isInstancedMesh&&We.instancingColor===!0&&$.instanceColor===null||$.isInstancedMesh&&We.instancingColor===!1&&$.instanceColor!==null||$.isInstancedMesh&&We.instancingMorph===!0&&$.morphTexture===null||$.isInstancedMesh&&We.instancingMorph===!1&&$.morphTexture!==null||We.envMap!==Pe||se.fog===!0&&We.fog!==ye||We.numClippingPlanes!==void 0&&(We.numClippingPlanes!==z.numPlanes||We.numIntersection!==z.numIntersection)||We.vertexAlphas!==Xe||We.vertexTangents!==Ye||We.morphTargets!==Ve||We.morphNormals!==tt||We.morphColors!==ct||We.toneMapping!==xt||We.morphTargetsCount!==ht)&&(rt=!0):(rt=!0,We.__version=se.version);let Gt=We.currentProgram;rt===!0&&(Gt=ts(se,J,$));let Si=!1,Ht=!1,ar=!1,gt=Gt.getUniforms(),jt=We.uniforms;if(Oe.useProgram(Gt.program)&&(Si=!0,Ht=!0,ar=!0),se.id!==T&&(T=se.id,Ht=!0),Si||M!==C){Oe.buffers.depth.getReversed()&&C.reversedDepth!==!0&&(C._reversedDepth=!0,C.updateProjectionMatrix()),gt.setValue(B,"projectionMatrix",C.projectionMatrix),gt.setValue(B,"viewMatrix",C.matrixWorldInverse);let kt=gt.map.cameraPosition;kt!==void 0&&kt.setValue(B,ne.setFromMatrixPosition(C.matrixWorld)),Ke.logarithmicDepthBuffer&&gt.setValue(B,"logDepthBufFC",2/(Math.log(C.far+1)/Math.LN2)),(se.isMeshPhongMaterial||se.isMeshToonMaterial||se.isMeshLambertMaterial||se.isMeshBasicMaterial||se.isMeshStandardMaterial||se.isShaderMaterial)&&gt.setValue(B,"isOrthographic",C.isOrthographicCamera===!0),M!==C&&(M=C,Ht=!0,ar=!0)}if($.isSkinnedMesh){gt.setOptional(B,$,"bindMatrix"),gt.setOptional(B,$,"bindMatrixInverse");let Ot=$.skeleton;Ot&&(Ot.boneTexture===null&&Ot.computeBoneTexture(),gt.setValue(B,"boneTexture",Ot.boneTexture,He))}$.isBatchedMesh&&(gt.setOptional(B,$,"batchingTexture"),gt.setValue(B,"batchingTexture",$._matricesTexture,He),gt.setOptional(B,$,"batchingIdTexture"),gt.setValue(B,"batchingIdTexture",$._indirectTexture,He),gt.setOptional(B,$,"batchingColorTexture"),$._colorsTexture!==null&&gt.setValue(B,"batchingColorTexture",$._colorsTexture,He));let Jt=re.morphAttributes;if((Jt.position!==void 0||Jt.normal!==void 0||Jt.color!==void 0)&&Q.update($,re,Gt),(Ht||We.receiveShadow!==$.receiveShadow)&&(We.receiveShadow=$.receiveShadow,gt.setValue(B,"receiveShadow",$.receiveShadow)),se.isMeshGouraudMaterial&&se.envMap!==null&&(jt.envMap.value=Pe,jt.flipEnvMap.value=Pe.isCubeTexture&&Pe.isRenderTargetTexture===!1?-1:1),se.isMeshStandardMaterial&&se.envMap===null&&J.environment!==null&&(jt.envMapIntensity.value=J.environmentIntensity),Ht&&(gt.setValue(B,"toneMappingExposure",_.toneMappingExposure),We.needsLights&&Ku(jt,ar),ye&&se.fog===!0&&L.refreshFogUniforms(jt,ye),L.refreshMaterialUniforms(jt,se,G,q,u.state.transmissionRenderTarget[C.id]),rr.upload(B,Dc(We),jt,He)),se.isShaderMaterial&&se.uniformsNeedUpdate===!0&&(rr.upload(B,Dc(We),jt,He),se.uniformsNeedUpdate=!1),se.isSpriteMaterial&&gt.setValue(B,"center",$.center),gt.setValue(B,"modelViewMatrix",$.modelViewMatrix),gt.setValue(B,"normalMatrix",$.normalMatrix),gt.setValue(B,"modelMatrix",$.matrixWorld),se.isShaderMaterial||se.isRawShaderMaterial){let Ot=se.uniformsGroups;for(let kt=0,na=Ot.length;kt<na;kt++){let ei=Ot[kt];xe.update(ei,Gt),xe.bind(ei,Gt)}}return Gt}function Ku(C,J){C.ambientLightColor.needsUpdate=J,C.lightProbe.needsUpdate=J,C.directionalLights.needsUpdate=J,C.directionalLightShadows.needsUpdate=J,C.pointLights.needsUpdate=J,C.pointLightShadows.needsUpdate=J,C.spotLights.needsUpdate=J,C.spotLightShadows.needsUpdate=J,C.rectAreaLights.needsUpdate=J,C.hemisphereLights.needsUpdate=J}function Zu(C){return C.isMeshLambertMaterial||C.isMeshToonMaterial||C.isMeshPhongMaterial||C.isMeshStandardMaterial||C.isShadowMaterial||C.isShaderMaterial&&C.lights===!0}this.getActiveCubeFace=function(){return N},this.getActiveMipmapLevel=function(){return w},this.getRenderTarget=function(){return O},this.setRenderTargetTextures=function(C,J,re){let se=Re.get(C);se.__autoAllocateDepthBuffer=C.resolveDepthBuffer===!1,se.__autoAllocateDepthBuffer===!1&&(se.__useRenderToTexture=!1),Re.get(C.texture).__webglTexture=J,Re.get(C.depthTexture).__webglTexture=se.__autoAllocateDepthBuffer?void 0:re,se.__hasExternalTextures=!0},this.setRenderTargetFramebuffer=function(C,J){let re=Re.get(C);re.__webglFramebuffer=J,re.__useDefaultFramebuffer=J===void 0};let ju=B.createFramebuffer();this.setRenderTarget=function(C,J=0,re=0){O=C,N=J,w=re;let se=!0,$=null,ye=!1,Ce=!1;if(C){let Pe=Re.get(C);if(Pe.__useDefaultFramebuffer!==void 0)Oe.bindFramebuffer(B.FRAMEBUFFER,null),se=!1;else if(Pe.__webglFramebuffer===void 0)He.setupRenderTarget(C);else if(Pe.__hasExternalTextures)He.rebindTextures(C,Re.get(C.texture).__webglTexture,Re.get(C.depthTexture).__webglTexture);else if(C.depthBuffer){let Ve=C.depthTexture;if(Pe.__boundDepthTexture!==Ve){if(Ve!==null&&Re.has(Ve)&&(C.width!==Ve.image.width||C.height!==Ve.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");He.setupDepthRenderbuffer(C)}}let Xe=C.texture;(Xe.isData3DTexture||Xe.isDataArrayTexture||Xe.isCompressedArrayTexture)&&(Ce=!0);let Ye=Re.get(C).__webglFramebuffer;C.isWebGLCubeRenderTarget?(Array.isArray(Ye[J])?$=Ye[J][re]:$=Ye[J],ye=!0):C.samples>0&&He.useMultisampledRTT(C)===!1?$=Re.get(C).__webglMultisampledFramebuffer:Array.isArray(Ye)?$=Ye[re]:$=Ye,R.copy(C.viewport),I.copy(C.scissor),U=C.scissorTest}else R.copy(ue).multiplyScalar(G).floor(),I.copy(_e).multiplyScalar(G).floor(),U=me;if(re!==0&&($=ju),Oe.bindFramebuffer(B.FRAMEBUFFER,$)&&se&&Oe.drawBuffers(C,$),Oe.viewport(R),Oe.scissor(I),Oe.setScissorTest(U),ye){let Pe=Re.get(C.texture);B.framebufferTexture2D(B.FRAMEBUFFER,B.COLOR_ATTACHMENT0,B.TEXTURE_CUBE_MAP_POSITIVE_X+J,Pe.__webglTexture,re)}else if(Ce){let Pe=J;for(let Xe=0;Xe<C.textures.length;Xe++){let Ye=Re.get(C.textures[Xe]);B.framebufferTextureLayer(B.FRAMEBUFFER,B.COLOR_ATTACHMENT0+Xe,Ye.__webglTexture,re,Pe)}}else if(C!==null&&re!==0){let Pe=Re.get(C.texture);B.framebufferTexture2D(B.FRAMEBUFFER,B.COLOR_ATTACHMENT0,B.TEXTURE_2D,Pe.__webglTexture,re)}T=-1},this.readRenderTargetPixels=function(C,J,re,se,$,ye,Ce,Ue=0){if(!(C&&C.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Pe=Re.get(C).__webglFramebuffer;if(C.isWebGLCubeRenderTarget&&Ce!==void 0&&(Pe=Pe[Ce]),Pe){Oe.bindFramebuffer(B.FRAMEBUFFER,Pe);try{let Xe=C.textures[Ue],Ye=Xe.format,Ve=Xe.type;if(!Ke.textureFormatReadable(Ye)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!Ke.textureTypeReadable(Ve)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}J>=0&&J<=C.width-se&&re>=0&&re<=C.height-$&&(C.textures.length>1&&B.readBuffer(B.COLOR_ATTACHMENT0+Ue),B.readPixels(J,re,se,$,Se.convert(Ye),Se.convert(Ve),ye))}finally{let Xe=O!==null?Re.get(O).__webglFramebuffer:null;Oe.bindFramebuffer(B.FRAMEBUFFER,Xe)}}},this.readRenderTargetPixelsAsync=async function(C,J,re,se,$,ye,Ce,Ue=0){if(!(C&&C.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Pe=Re.get(C).__webglFramebuffer;if(C.isWebGLCubeRenderTarget&&Ce!==void 0&&(Pe=Pe[Ce]),Pe)if(J>=0&&J<=C.width-se&&re>=0&&re<=C.height-$){Oe.bindFramebuffer(B.FRAMEBUFFER,Pe);let Xe=C.textures[Ue],Ye=Xe.format,Ve=Xe.type;if(!Ke.textureFormatReadable(Ye))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!Ke.textureTypeReadable(Ve))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");let tt=B.createBuffer();B.bindBuffer(B.PIXEL_PACK_BUFFER,tt),B.bufferData(B.PIXEL_PACK_BUFFER,ye.byteLength,B.STREAM_READ),C.textures.length>1&&B.readBuffer(B.COLOR_ATTACHMENT0+Ue),B.readPixels(J,re,se,$,Se.convert(Ye),Se.convert(Ve),0);let ct=O!==null?Re.get(O).__webglFramebuffer:null;Oe.bindFramebuffer(B.FRAMEBUFFER,ct);let xt=B.fenceSync(B.SYNC_GPU_COMMANDS_COMPLETE,0);return B.flush(),await eu(B,xt,4),B.bindBuffer(B.PIXEL_PACK_BUFFER,tt),B.getBufferSubData(B.PIXEL_PACK_BUFFER,0,ye),B.deleteBuffer(tt),B.deleteSync(xt),ye}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")},this.copyFramebufferToTexture=function(C,J=null,re=0){let se=Math.pow(2,-re),$=Math.floor(C.image.width*se),ye=Math.floor(C.image.height*se),Ce=J!==null?J.x:0,Ue=J!==null?J.y:0;He.setTexture2D(C,0),B.copyTexSubImage2D(B.TEXTURE_2D,re,0,0,Ce,Ue,$,ye),Oe.unbindTexture()};let Ju=B.createFramebuffer(),$u=B.createFramebuffer();this.copyTextureToTexture=function(C,J,re=null,se=null,$=0,ye=null){ye===null&&($!==0?(li("WebGLRenderer: copyTextureToTexture function signature has changed to support src and dst mipmap levels."),ye=$,$=0):ye=0);let Ce,Ue,Pe,Xe,Ye,Ve,tt,ct,xt,dt=C.isCompressedTexture?C.mipmaps[ye]:C.image;if(re!==null)Ce=re.max.x-re.min.x,Ue=re.max.y-re.min.y,Pe=re.isBox3?re.max.z-re.min.z:1,Xe=re.min.x,Ye=re.min.y,Ve=re.isBox3?re.min.z:0;else{let Jt=Math.pow(2,-$);Ce=Math.floor(dt.width*Jt),Ue=Math.floor(dt.height*Jt),C.isDataArrayTexture?Pe=dt.depth:C.isData3DTexture?Pe=Math.floor(dt.depth*Jt):Pe=1,Xe=0,Ye=0,Ve=0}se!==null?(tt=se.x,ct=se.y,xt=se.z):(tt=0,ct=0,xt=0);let ht=Se.convert(J.format),We=Se.convert(J.type),mt;J.isData3DTexture?(He.setTexture3D(J,0),mt=B.TEXTURE_3D):J.isDataArrayTexture||J.isCompressedArrayTexture?(He.setTexture2DArray(J,0),mt=B.TEXTURE_2D_ARRAY):(He.setTexture2D(J,0),mt=B.TEXTURE_2D),B.pixelStorei(B.UNPACK_FLIP_Y_WEBGL,J.flipY),B.pixelStorei(B.UNPACK_PREMULTIPLY_ALPHA_WEBGL,J.premultiplyAlpha),B.pixelStorei(B.UNPACK_ALIGNMENT,J.unpackAlignment);let rt=B.getParameter(B.UNPACK_ROW_LENGTH),Gt=B.getParameter(B.UNPACK_IMAGE_HEIGHT),Si=B.getParameter(B.UNPACK_SKIP_PIXELS),Ht=B.getParameter(B.UNPACK_SKIP_ROWS),ar=B.getParameter(B.UNPACK_SKIP_IMAGES);B.pixelStorei(B.UNPACK_ROW_LENGTH,dt.width),B.pixelStorei(B.UNPACK_IMAGE_HEIGHT,dt.height),B.pixelStorei(B.UNPACK_SKIP_PIXELS,Xe),B.pixelStorei(B.UNPACK_SKIP_ROWS,Ye),B.pixelStorei(B.UNPACK_SKIP_IMAGES,Ve);let gt=C.isDataArrayTexture||C.isData3DTexture,jt=J.isDataArrayTexture||J.isData3DTexture;if(C.isDepthTexture){let Jt=Re.get(C),Ot=Re.get(J),kt=Re.get(Jt.__renderTarget),na=Re.get(Ot.__renderTarget);Oe.bindFramebuffer(B.READ_FRAMEBUFFER,kt.__webglFramebuffer),Oe.bindFramebuffer(B.DRAW_FRAMEBUFFER,na.__webglFramebuffer);for(let ei=0;ei<Pe;ei++)gt&&(B.framebufferTextureLayer(B.READ_FRAMEBUFFER,B.COLOR_ATTACHMENT0,Re.get(C).__webglTexture,$,Ve+ei),B.framebufferTextureLayer(B.DRAW_FRAMEBUFFER,B.COLOR_ATTACHMENT0,Re.get(J).__webglTexture,ye,xt+ei)),B.blitFramebuffer(Xe,Ye,Ce,Ue,tt,ct,Ce,Ue,B.DEPTH_BUFFER_BIT,B.NEAREST);Oe.bindFramebuffer(B.READ_FRAMEBUFFER,null),Oe.bindFramebuffer(B.DRAW_FRAMEBUFFER,null)}else if($!==0||C.isRenderTargetTexture||Re.has(C)){let Jt=Re.get(C),Ot=Re.get(J);Oe.bindFramebuffer(B.READ_FRAMEBUFFER,Ju),Oe.bindFramebuffer(B.DRAW_FRAMEBUFFER,$u);for(let kt=0;kt<Pe;kt++)gt?B.framebufferTextureLayer(B.READ_FRAMEBUFFER,B.COLOR_ATTACHMENT0,Jt.__webglTexture,$,Ve+kt):B.framebufferTexture2D(B.READ_FRAMEBUFFER,B.COLOR_ATTACHMENT0,B.TEXTURE_2D,Jt.__webglTexture,$),jt?B.framebufferTextureLayer(B.DRAW_FRAMEBUFFER,B.COLOR_ATTACHMENT0,Ot.__webglTexture,ye,xt+kt):B.framebufferTexture2D(B.DRAW_FRAMEBUFFER,B.COLOR_ATTACHMENT0,B.TEXTURE_2D,Ot.__webglTexture,ye),$!==0?B.blitFramebuffer(Xe,Ye,Ce,Ue,tt,ct,Ce,Ue,B.COLOR_BUFFER_BIT,B.NEAREST):jt?B.copyTexSubImage3D(mt,ye,tt,ct,xt+kt,Xe,Ye,Ce,Ue):B.copyTexSubImage2D(mt,ye,tt,ct,Xe,Ye,Ce,Ue);Oe.bindFramebuffer(B.READ_FRAMEBUFFER,null),Oe.bindFramebuffer(B.DRAW_FRAMEBUFFER,null)}else jt?C.isDataTexture||C.isData3DTexture?B.texSubImage3D(mt,ye,tt,ct,xt,Ce,Ue,Pe,ht,We,dt.data):J.isCompressedArrayTexture?B.compressedTexSubImage3D(mt,ye,tt,ct,xt,Ce,Ue,Pe,ht,dt.data):B.texSubImage3D(mt,ye,tt,ct,xt,Ce,Ue,Pe,ht,We,dt):C.isDataTexture?B.texSubImage2D(B.TEXTURE_2D,ye,tt,ct,Ce,Ue,ht,We,dt.data):C.isCompressedTexture?B.compressedTexSubImage2D(B.TEXTURE_2D,ye,tt,ct,dt.width,dt.height,ht,dt.data):B.texSubImage2D(B.TEXTURE_2D,ye,tt,ct,Ce,Ue,ht,We,dt);B.pixelStorei(B.UNPACK_ROW_LENGTH,rt),B.pixelStorei(B.UNPACK_IMAGE_HEIGHT,Gt),B.pixelStorei(B.UNPACK_SKIP_PIXELS,Si),B.pixelStorei(B.UNPACK_SKIP_ROWS,Ht),B.pixelStorei(B.UNPACK_SKIP_IMAGES,ar),ye===0&&J.generateMipmaps&&B.generateMipmap(mt),Oe.unbindTexture()},this.copyTextureToTexture3D=function(C,J,re=null,se=null,$=0){return li('WebGLRenderer: copyTextureToTexture3D function has been deprecated. Use "copyTextureToTexture" instead.'),this.copyTextureToTexture(C,J,re,se,$)},this.initRenderTarget=function(C){Re.get(C).__webglFramebuffer===void 0&&He.setupRenderTarget(C)},this.initTexture=function(C){C.isCubeTexture?He.setTextureCube(C,0):C.isData3DTexture?He.setTexture3D(C,0):C.isDataArrayTexture||C.isCompressedArrayTexture?He.setTexture2DArray(C,0):He.setTexture2D(C,0),Oe.unbindTexture()},this.resetState=function(){N=0,w=0,O=null,Oe.reset(),pe.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return ln}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;let t=this.getContext();t.drawingBufferColorSpace=nt._getDrawingBufferColorSpace(e),t.unpackColorSpace=nt._getUnpackColorSpace()}};var Uu={type:"change"},Ac={type:"start"},ku={type:"end"},Ko=new Yn,Fu=new Qt,Yg=Math.cos(70*rc.DEG2RAD),At=new Z,Vt=2*Math.PI,lt={NONE:-1,ROTATE:0,DOLLY:1,PAN:2,TOUCH_ROTATE:3,TOUCH_PAN:4,TOUCH_DOLLY_PAN:5,TOUCH_DOLLY_ROTATE:6},bc=1e-6,Zo=class extends Hr{constructor(e,t=null){super(e,t),this.state=lt.NONE,this.target=new Z,this.cursor=new Z,this.minDistance=0,this.maxDistance=1/0,this.minZoom=0,this.maxZoom=1/0,this.minTargetRadius=0,this.maxTargetRadius=1/0,this.minPolarAngle=0,this.maxPolarAngle=Math.PI,this.minAzimuthAngle=-1/0,this.maxAzimuthAngle=1/0,this.enableDamping=!1,this.dampingFactor=.05,this.enableZoom=!0,this.zoomSpeed=1,this.enableRotate=!0,this.rotateSpeed=1,this.keyRotateSpeed=1,this.enablePan=!0,this.panSpeed=1,this.screenSpacePanning=!0,this.keyPanSpeed=7,this.zoomToCursor=!1,this.autoRotate=!1,this.autoRotateSpeed=2,this.keys={LEFT:"ArrowLeft",UP:"ArrowUp",RIGHT:"ArrowRight",BOTTOM:"ArrowDown"},this.mouseButtons={LEFT:jn.ROTATE,MIDDLE:jn.DOLLY,RIGHT:jn.PAN},this.touches={ONE:Jn.ROTATE,TWO:Jn.DOLLY_PAN},this.target0=this.target.clone(),this.position0=this.object.position.clone(),this.zoom0=this.object.zoom,this._domElementKeyEvents=null,this._lastPosition=new Z,this._lastQuaternion=new zt,this._lastTargetPosition=new Z,this._quat=new zt().setFromUnitVectors(e.up,new Z(0,1,0)),this._quatInverse=this._quat.clone().invert(),this._spherical=new ji,this._sphericalDelta=new ji,this._scale=1,this._panOffset=new Z,this._rotateStart=new ze,this._rotateEnd=new ze,this._rotateDelta=new ze,this._panStart=new ze,this._panEnd=new ze,this._panDelta=new ze,this._dollyStart=new ze,this._dollyEnd=new ze,this._dollyDelta=new ze,this._dollyDirection=new Z,this._mouse=new ze,this._performCursorZoom=!1,this._pointers=[],this._pointerPositions={},this._controlActive=!1,this._onPointerMove=Kg.bind(this),this._onPointerDown=qg.bind(this),this._onPointerUp=Zg.bind(this),this._onContextMenu=n_.bind(this),this._onMouseWheel=$g.bind(this),this._onKeyDown=Qg.bind(this),this._onTouchStart=e_.bind(this),this._onTouchMove=t_.bind(this),this._onMouseDown=jg.bind(this),this._onMouseMove=Jg.bind(this),this._interceptControlDown=i_.bind(this),this._interceptControlUp=r_.bind(this),this.domElement!==null&&this.connect(this.domElement),this.update()}connect(e){super.connect(e),this.domElement.addEventListener("pointerdown",this._onPointerDown),this.domElement.addEventListener("pointercancel",this._onPointerUp),this.domElement.addEventListener("contextmenu",this._onContextMenu),this.domElement.addEventListener("wheel",this._onMouseWheel,{passive:!1}),this.domElement.getRootNode().addEventListener("keydown",this._interceptControlDown,{passive:!0,capture:!0}),this.domElement.style.touchAction="none"}disconnect(){this.domElement.removeEventListener("pointerdown",this._onPointerDown),this.domElement.removeEventListener("pointermove",this._onPointerMove),this.domElement.removeEventListener("pointerup",this._onPointerUp),this.domElement.removeEventListener("pointercancel",this._onPointerUp),this.domElement.removeEventListener("wheel",this._onMouseWheel),this.domElement.removeEventListener("contextmenu",this._onContextMenu),this.stopListenToKeyEvents(),this.domElement.getRootNode().removeEventListener("keydown",this._interceptControlDown,{capture:!0}),this.domElement.style.touchAction="auto"}dispose(){this.disconnect()}getPolarAngle(){return this._spherical.phi}getAzimuthalAngle(){return this._spherical.theta}getDistance(){return this.object.position.distanceTo(this.target)}listenToKeyEvents(e){e.addEventListener("keydown",this._onKeyDown),this._domElementKeyEvents=e}stopListenToKeyEvents(){this._domElementKeyEvents!==null&&(this._domElementKeyEvents.removeEventListener("keydown",this._onKeyDown),this._domElementKeyEvents=null)}saveState(){this.target0.copy(this.target),this.position0.copy(this.object.position),this.zoom0=this.object.zoom}reset(){this.target.copy(this.target0),this.object.position.copy(this.position0),this.object.zoom=this.zoom0,this.object.updateProjectionMatrix(),this.dispatchEvent(Uu),this.update(),this.state=lt.NONE}update(e=null){let t=this.object.position;At.copy(t).sub(this.target),At.applyQuaternion(this._quat),this._spherical.setFromVector3(At),this.autoRotate&&this.state===lt.NONE&&this._rotateLeft(this._getAutoRotationAngle(e)),this.enableDamping?(this._spherical.theta+=this._sphericalDelta.theta*this.dampingFactor,this._spherical.phi+=this._sphericalDelta.phi*this.dampingFactor):(this._spherical.theta+=this._sphericalDelta.theta,this._spherical.phi+=this._sphericalDelta.phi);let i=this.minAzimuthAngle,r=this.maxAzimuthAngle;isFinite(i)&&isFinite(r)&&(i<-Math.PI?i+=Vt:i>Math.PI&&(i-=Vt),r<-Math.PI?r+=Vt:r>Math.PI&&(r-=Vt),i<=r?this._spherical.theta=Math.max(i,Math.min(r,this._spherical.theta)):this._spherical.theta=this._spherical.theta>(i+r)/2?Math.max(i,this._spherical.theta):Math.min(r,this._spherical.theta)),this._spherical.phi=Math.max(this.minPolarAngle,Math.min(this.maxPolarAngle,this._spherical.phi)),this._spherical.makeSafe(),this.enableDamping===!0?this.target.addScaledVector(this._panOffset,this.dampingFactor):this.target.add(this._panOffset),this.target.sub(this.cursor),this.target.clampLength(this.minTargetRadius,this.maxTargetRadius),this.target.add(this.cursor);let s=!1;if(this.zoomToCursor&&this._performCursorZoom||this.object.isOrthographicCamera)this._spherical.radius=this._clampDistance(this._spherical.radius);else{let o=this._spherical.radius;this._spherical.radius=this._clampDistance(this._spherical.radius*this._scale),s=o!=this._spherical.radius}if(At.setFromSpherical(this._spherical),At.applyQuaternion(this._quatInverse),t.copy(this.target).add(At),this.object.lookAt(this.target),this.enableDamping===!0?(this._sphericalDelta.theta*=1-this.dampingFactor,this._sphericalDelta.phi*=1-this.dampingFactor,this._panOffset.multiplyScalar(1-this.dampingFactor)):(this._sphericalDelta.set(0,0,0),this._panOffset.set(0,0,0)),this.zoomToCursor&&this._performCursorZoom){let o=null;if(this.object.isPerspectiveCamera){let c=At.length();o=this._clampDistance(c*this._scale);let l=c-o;this.object.position.addScaledVector(this._dollyDirection,l),this.object.updateMatrixWorld(),s=!!l}else if(this.object.isOrthographicCamera){let c=new Z(this._mouse.x,this._mouse.y,0);c.unproject(this.object);let l=this.object.zoom;this.object.zoom=Math.max(this.minZoom,Math.min(this.maxZoom,this.object.zoom/this._scale)),this.object.updateProjectionMatrix(),s=l!==this.object.zoom;let a=new Z(this._mouse.x,this._mouse.y,0);a.unproject(this.object),this.object.position.sub(a).add(c),this.object.updateMatrixWorld(),o=At.length()}else console.warn("WARNING: OrbitControls.js encountered an unknown camera type - zoom to cursor disabled."),this.zoomToCursor=!1;o!==null&&(this.screenSpacePanning?this.target.set(0,0,-1).transformDirection(this.object.matrix).multiplyScalar(o).add(this.object.position):(Ko.origin.copy(this.object.position),Ko.direction.set(0,0,-1).transformDirection(this.object.matrix),Math.abs(this.object.up.dot(Ko.direction))<Yg?this.object.lookAt(this.target):(Fu.setFromNormalAndCoplanarPoint(this.object.up,this.target),Ko.intersectPlane(Fu,this.target))))}else if(this.object.isOrthographicCamera){let o=this.object.zoom;this.object.zoom=Math.max(this.minZoom,Math.min(this.maxZoom,this.object.zoom/this._scale)),o!==this.object.zoom&&(this.object.updateProjectionMatrix(),s=!0)}return this._scale=1,this._performCursorZoom=!1,s||this._lastPosition.distanceToSquared(this.object.position)>bc||8*(1-this._lastQuaternion.dot(this.object.quaternion))>bc||this._lastTargetPosition.distanceToSquared(this.target)>bc?(this.dispatchEvent(Uu),this._lastPosition.copy(this.object.position),this._lastQuaternion.copy(this.object.quaternion),this._lastTargetPosition.copy(this.target),!0):!1}_getAutoRotationAngle(e){return e!==null?Vt/60*this.autoRotateSpeed*e:Vt/60/60*this.autoRotateSpeed}_getZoomScale(e){let t=Math.abs(e*.01);return Math.pow(.95,this.zoomSpeed*t)}_rotateLeft(e){this._sphericalDelta.theta-=e}_rotateUp(e){this._sphericalDelta.phi-=e}_panLeft(e,t){At.setFromMatrixColumn(t,0),At.multiplyScalar(-e),this._panOffset.add(At)}_panUp(e,t){this.screenSpacePanning===!0?At.setFromMatrixColumn(t,1):(At.setFromMatrixColumn(t,0),At.crossVectors(this.object.up,At)),At.multiplyScalar(e),this._panOffset.add(At)}_pan(e,t){let i=this.domElement;if(this.object.isPerspectiveCamera){let r=this.object.position;At.copy(r).sub(this.target);let s=At.length();s*=Math.tan(this.object.fov/2*Math.PI/180),this._panLeft(2*e*s/i.clientHeight,this.object.matrix),this._panUp(2*t*s/i.clientHeight,this.object.matrix)}else this.object.isOrthographicCamera?(this._panLeft(e*(this.object.right-this.object.left)/this.object.zoom/i.clientWidth,this.object.matrix),this._panUp(t*(this.object.top-this.object.bottom)/this.object.zoom/i.clientHeight,this.object.matrix)):(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - pan disabled."),this.enablePan=!1)}_dollyOut(e){this.object.isPerspectiveCamera||this.object.isOrthographicCamera?this._scale/=e:(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - dolly/zoom disabled."),this.enableZoom=!1)}_dollyIn(e){this.object.isPerspectiveCamera||this.object.isOrthographicCamera?this._scale*=e:(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - dolly/zoom disabled."),this.enableZoom=!1)}_updateZoomParameters(e,t){if(!this.zoomToCursor)return;this._performCursorZoom=!0;let i=this.domElement.getBoundingClientRect(),r=e-i.left,s=t-i.top,o=i.width,c=i.height;this._mouse.x=r/o*2-1,this._mouse.y=-(s/c)*2+1,this._dollyDirection.set(this._mouse.x,this._mouse.y,1).unproject(this.object).sub(this.object.position).normalize()}_clampDistance(e){return Math.max(this.minDistance,Math.min(this.maxDistance,e))}_handleMouseDownRotate(e){this._rotateStart.set(e.clientX,e.clientY)}_handleMouseDownDolly(e){this._updateZoomParameters(e.clientX,e.clientX),this._dollyStart.set(e.clientX,e.clientY)}_handleMouseDownPan(e){this._panStart.set(e.clientX,e.clientY)}_handleMouseMoveRotate(e){this._rotateEnd.set(e.clientX,e.clientY),this._rotateDelta.subVectors(this._rotateEnd,this._rotateStart).multiplyScalar(this.rotateSpeed);let t=this.domElement;this._rotateLeft(Vt*this._rotateDelta.x/t.clientHeight),this._rotateUp(Vt*this._rotateDelta.y/t.clientHeight),this._rotateStart.copy(this._rotateEnd),this.update()}_handleMouseMoveDolly(e){this._dollyEnd.set(e.clientX,e.clientY),this._dollyDelta.subVectors(this._dollyEnd,this._dollyStart),this._dollyDelta.y>0?this._dollyOut(this._getZoomScale(this._dollyDelta.y)):this._dollyDelta.y<0&&this._dollyIn(this._getZoomScale(this._dollyDelta.y)),this._dollyStart.copy(this._dollyEnd),this.update()}_handleMouseMovePan(e){this._panEnd.set(e.clientX,e.clientY),this._panDelta.subVectors(this._panEnd,this._panStart).multiplyScalar(this.panSpeed),this._pan(this._panDelta.x,this._panDelta.y),this._panStart.copy(this._panEnd),this.update()}_handleMouseWheel(e){this._updateZoomParameters(e.clientX,e.clientY),e.deltaY<0?this._dollyIn(this._getZoomScale(e.deltaY)):e.deltaY>0&&this._dollyOut(this._getZoomScale(e.deltaY)),this.update()}_handleKeyDown(e){let t=!1;switch(e.code){case this.keys.UP:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateUp(Vt*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(0,this.keyPanSpeed),t=!0;break;case this.keys.BOTTOM:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateUp(-Vt*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(0,-this.keyPanSpeed),t=!0;break;case this.keys.LEFT:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateLeft(Vt*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(this.keyPanSpeed,0),t=!0;break;case this.keys.RIGHT:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateLeft(-Vt*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(-this.keyPanSpeed,0),t=!0;break}t&&(e.preventDefault(),this.update())}_handleTouchStartRotate(e){if(this._pointers.length===1)this._rotateStart.set(e.pageX,e.pageY);else{let t=this._getSecondPointerPosition(e),i=.5*(e.pageX+t.x),r=.5*(e.pageY+t.y);this._rotateStart.set(i,r)}}_handleTouchStartPan(e){if(this._pointers.length===1)this._panStart.set(e.pageX,e.pageY);else{let t=this._getSecondPointerPosition(e),i=.5*(e.pageX+t.x),r=.5*(e.pageY+t.y);this._panStart.set(i,r)}}_handleTouchStartDolly(e){let t=this._getSecondPointerPosition(e),i=e.pageX-t.x,r=e.pageY-t.y,s=Math.sqrt(i*i+r*r);this._dollyStart.set(0,s)}_handleTouchStartDollyPan(e){this.enableZoom&&this._handleTouchStartDolly(e),this.enablePan&&this._handleTouchStartPan(e)}_handleTouchStartDollyRotate(e){this.enableZoom&&this._handleTouchStartDolly(e),this.enableRotate&&this._handleTouchStartRotate(e)}_handleTouchMoveRotate(e){if(this._pointers.length==1)this._rotateEnd.set(e.pageX,e.pageY);else{let i=this._getSecondPointerPosition(e),r=.5*(e.pageX+i.x),s=.5*(e.pageY+i.y);this._rotateEnd.set(r,s)}this._rotateDelta.subVectors(this._rotateEnd,this._rotateStart).multiplyScalar(this.rotateSpeed);let t=this.domElement;this._rotateLeft(Vt*this._rotateDelta.x/t.clientHeight),this._rotateUp(Vt*this._rotateDelta.y/t.clientHeight),this._rotateStart.copy(this._rotateEnd)}_handleTouchMovePan(e){if(this._pointers.length===1)this._panEnd.set(e.pageX,e.pageY);else{let t=this._getSecondPointerPosition(e),i=.5*(e.pageX+t.x),r=.5*(e.pageY+t.y);this._panEnd.set(i,r)}this._panDelta.subVectors(this._panEnd,this._panStart).multiplyScalar(this.panSpeed),this._pan(this._panDelta.x,this._panDelta.y),this._panStart.copy(this._panEnd)}_handleTouchMoveDolly(e){let t=this._getSecondPointerPosition(e),i=e.pageX-t.x,r=e.pageY-t.y,s=Math.sqrt(i*i+r*r);this._dollyEnd.set(0,s),this._dollyDelta.set(0,Math.pow(this._dollyEnd.y/this._dollyStart.y,this.zoomSpeed)),this._dollyOut(this._dollyDelta.y),this._dollyStart.copy(this._dollyEnd);let o=(e.pageX+t.x)*.5,c=(e.pageY+t.y)*.5;this._updateZoomParameters(o,c)}_handleTouchMoveDollyPan(e){this.enableZoom&&this._handleTouchMoveDolly(e),this.enablePan&&this._handleTouchMovePan(e)}_handleTouchMoveDollyRotate(e){this.enableZoom&&this._handleTouchMoveDolly(e),this.enableRotate&&this._handleTouchMoveRotate(e)}_addPointer(e){this._pointers.push(e.pointerId)}_removePointer(e){delete this._pointerPositions[e.pointerId];for(let t=0;t<this._pointers.length;t++)if(this._pointers[t]==e.pointerId){this._pointers.splice(t,1);return}}_isTrackingPointer(e){for(let t=0;t<this._pointers.length;t++)if(this._pointers[t]==e.pointerId)return!0;return!1}_trackPointer(e){let t=this._pointerPositions[e.pointerId];t===void 0&&(t=new ze,this._pointerPositions[e.pointerId]=t),t.set(e.pageX,e.pageY)}_getSecondPointerPosition(e){let t=e.pointerId===this._pointers[0]?this._pointers[1]:this._pointers[0];return this._pointerPositions[t]}_customWheelEvent(e){let t=e.deltaMode,i={clientX:e.clientX,clientY:e.clientY,deltaY:e.deltaY};switch(t){case 1:i.deltaY*=16;break;case 2:i.deltaY*=100;break}return e.ctrlKey&&!this._controlActive&&(i.deltaY*=10),i}};function qg(n){this.enabled!==!1&&(this._pointers.length===0&&(this.domElement.setPointerCapture(n.pointerId),this.domElement.addEventListener("pointermove",this._onPointerMove),this.domElement.addEventListener("pointerup",this._onPointerUp)),!this._isTrackingPointer(n)&&(this._addPointer(n),n.pointerType==="touch"?this._onTouchStart(n):this._onMouseDown(n)))}function Kg(n){this.enabled!==!1&&(n.pointerType==="touch"?this._onTouchMove(n):this._onMouseMove(n))}function Zg(n){switch(this._removePointer(n),this._pointers.length){case 0:this.domElement.releasePointerCapture(n.pointerId),this.domElement.removeEventListener("pointermove",this._onPointerMove),this.domElement.removeEventListener("pointerup",this._onPointerUp),this.dispatchEvent(ku),this.state=lt.NONE;break;case 1:let e=this._pointers[0],t=this._pointerPositions[e];this._onTouchStart({pointerId:e,pageX:t.x,pageY:t.y});break}}function jg(n){let e;switch(n.button){case 0:e=this.mouseButtons.LEFT;break;case 1:e=this.mouseButtons.MIDDLE;break;case 2:e=this.mouseButtons.RIGHT;break;default:e=-1}switch(e){case jn.DOLLY:if(this.enableZoom===!1)return;this._handleMouseDownDolly(n),this.state=lt.DOLLY;break;case jn.ROTATE:if(n.ctrlKey||n.metaKey||n.shiftKey){if(this.enablePan===!1)return;this._handleMouseDownPan(n),this.state=lt.PAN}else{if(this.enableRotate===!1)return;this._handleMouseDownRotate(n),this.state=lt.ROTATE}break;case jn.PAN:if(n.ctrlKey||n.metaKey||n.shiftKey){if(this.enableRotate===!1)return;this._handleMouseDownRotate(n),this.state=lt.ROTATE}else{if(this.enablePan===!1)return;this._handleMouseDownPan(n),this.state=lt.PAN}break;default:this.state=lt.NONE}this.state!==lt.NONE&&this.dispatchEvent(Ac)}function Jg(n){switch(this.state){case lt.ROTATE:if(this.enableRotate===!1)return;this._handleMouseMoveRotate(n);break;case lt.DOLLY:if(this.enableZoom===!1)return;this._handleMouseMoveDolly(n);break;case lt.PAN:if(this.enablePan===!1)return;this._handleMouseMovePan(n);break}}function $g(n){this.enabled===!1||this.enableZoom===!1||this.state!==lt.NONE||(n.preventDefault(),this.dispatchEvent(Ac),this._handleMouseWheel(this._customWheelEvent(n)),this.dispatchEvent(ku))}function Qg(n){this.enabled!==!1&&this._handleKeyDown(n)}function e_(n){switch(this._trackPointer(n),this._pointers.length){case 1:switch(this.touches.ONE){case Jn.ROTATE:if(this.enableRotate===!1)return;this._handleTouchStartRotate(n),this.state=lt.TOUCH_ROTATE;break;case Jn.PAN:if(this.enablePan===!1)return;this._handleTouchStartPan(n),this.state=lt.TOUCH_PAN;break;default:this.state=lt.NONE}break;case 2:switch(this.touches.TWO){case Jn.DOLLY_PAN:if(this.enableZoom===!1&&this.enablePan===!1)return;this._handleTouchStartDollyPan(n),this.state=lt.TOUCH_DOLLY_PAN;break;case Jn.DOLLY_ROTATE:if(this.enableZoom===!1&&this.enableRotate===!1)return;this._handleTouchStartDollyRotate(n),this.state=lt.TOUCH_DOLLY_ROTATE;break;default:this.state=lt.NONE}break;default:this.state=lt.NONE}this.state!==lt.NONE&&this.dispatchEvent(Ac)}function t_(n){switch(this._trackPointer(n),this.state){case lt.TOUCH_ROTATE:if(this.enableRotate===!1)return;this._handleTouchMoveRotate(n),this.update();break;case lt.TOUCH_PAN:if(this.enablePan===!1)return;this._handleTouchMovePan(n),this.update();break;case lt.TOUCH_DOLLY_PAN:if(this.enableZoom===!1&&this.enablePan===!1)return;this._handleTouchMoveDollyPan(n),this.update();break;case lt.TOUCH_DOLLY_ROTATE:if(this.enableZoom===!1&&this.enableRotate===!1)return;this._handleTouchMoveDollyRotate(n),this.update();break;default:this.state=lt.NONE}}function n_(n){this.enabled!==!1&&n.preventDefault()}function i_(n){n.key==="Control"&&(this._controlActive=!0,this.domElement.getRootNode().addEventListener("keyup",this._interceptControlUp,{passive:!0,capture:!0}))}function r_(n){n.key==="Control"&&(this._controlActive=!1,this.domElement.getRootNode().removeEventListener("keyup",this._interceptControlUp,{passive:!0,capture:!0}))}var je=(n,e)=>()=>(e||(e={exports:{}},n(e.exports,e)),e.exports),Bu=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.VERSION=void 0,n.VERSION="9.0.1"}),st=je((exports,module)=>{"use strict";var __spreadArray=exports&&exports.__spreadArray||function(n,e){for(var t=0,i=e.length,r=n.length;t<i;t++,r++)n[r]=e[t];return n};Object.defineProperty(exports,"__esModule",{value:!0}),exports.toFastProperties=exports.timer=exports.peek=exports.isES2015MapSupported=exports.PRINT_WARNING=exports.PRINT_ERROR=exports.packArray=exports.IDENTITY=exports.NOOP=exports.merge=exports.groupBy=exports.defaults=exports.assignNoOverwrite=exports.assign=exports.zipObject=exports.sortBy=exports.indexOf=exports.some=exports.difference=exports.every=exports.isObject=exports.isRegExp=exports.isArray=exports.partial=exports.uniq=exports.compact=exports.reduce=exports.findAll=exports.find=exports.cloneObj=exports.cloneArr=exports.contains=exports.has=exports.pick=exports.reject=exports.filter=exports.dropRight=exports.drop=exports.isFunction=exports.isUndefined=exports.isString=exports.forEach=exports.last=exports.first=exports.flatten=exports.map=exports.mapValues=exports.values=exports.keys=exports.isEmpty=void 0;function isEmpty(n){return n&&n.length===0}exports.isEmpty=isEmpty;function keys(n){return n==null?[]:Object.keys(n)}exports.keys=keys;function values(n){for(var e=[],t=Object.keys(n),i=0;i<t.length;i++)e.push(n[t[i]]);return e}exports.values=values;function mapValues(n,e){for(var t=[],i=keys(n),r=0;r<i.length;r++){var s=i[r];t.push(e.call(null,n[s],s))}return t}exports.mapValues=mapValues;function map(n,e){for(var t=[],i=0;i<n.length;i++)t.push(e.call(null,n[i],i));return t}exports.map=map;function flatten(n){for(var e=[],t=0;t<n.length;t++){var i=n[t];Array.isArray(i)?e=e.concat(flatten(i)):e.push(i)}return e}exports.flatten=flatten;function first(n){return isEmpty(n)?void 0:n[0]}exports.first=first;function last(n){var e=n&&n.length;return e?n[e-1]:void 0}exports.last=last;function forEach(n,e){if(Array.isArray(n))for(var t=0;t<n.length;t++)e.call(null,n[t],t);else if(isObject(n))for(var i=keys(n),t=0;t<i.length;t++){var r=i[t],s=n[r];e.call(null,s,r)}else throw Error("non exhaustive match")}exports.forEach=forEach;function isString(n){return typeof n=="string"}exports.isString=isString;function isUndefined(n){return n===void 0}exports.isUndefined=isUndefined;function isFunction(n){return n instanceof Function}exports.isFunction=isFunction;function drop(n,e){return e===void 0&&(e=1),n.slice(e,n.length)}exports.drop=drop;function dropRight(n,e){return e===void 0&&(e=1),n.slice(0,n.length-e)}exports.dropRight=dropRight;function filter(n,e){var t=[];if(Array.isArray(n))for(var i=0;i<n.length;i++){var r=n[i];e.call(null,r)&&t.push(r)}return t}exports.filter=filter;function reject(n,e){return filter(n,function(t){return!e(t)})}exports.reject=reject;function pick(n,e){for(var t=Object.keys(n),i={},r=0;r<t.length;r++){var s=t[r],o=n[s];e(o)&&(i[s]=o)}return i}exports.pick=pick;function has(n,e){return isObject(n)?n.hasOwnProperty(e):!1}exports.has=has;function contains(n,e){return find(n,function(t){return t===e})!==void 0}exports.contains=contains;function cloneArr(n){for(var e=[],t=0;t<n.length;t++)e.push(n[t]);return e}exports.cloneArr=cloneArr;function cloneObj(n){var e={};for(var t in n)Object.prototype.hasOwnProperty.call(n,t)&&(e[t]=n[t]);return e}exports.cloneObj=cloneObj;function find(n,e){for(var t=0;t<n.length;t++){var i=n[t];if(e.call(null,i))return i}}exports.find=find;function findAll(n,e){for(var t=[],i=0;i<n.length;i++){var r=n[i];e.call(null,r)&&t.push(r)}return t}exports.findAll=findAll;function reduce(n,e,t){for(var i=Array.isArray(n),r=i?n:values(n),s=i?[]:keys(n),o=t,c=0;c<r.length;c++)o=e.call(null,o,r[c],i?c:s[c]);return o}exports.reduce=reduce;function compact(n){return reject(n,function(e){return e==null})}exports.compact=compact;function uniq(n,e){e===void 0&&(e=function(i){return i});var t=[];return reduce(n,function(i,r){var s=e(r);return contains(t,s)?i:(t.push(s),i.concat(r))},[])}exports.uniq=uniq;function partial(n){for(var e=[],t=1;t<arguments.length;t++)e[t-1]=arguments[t];var i=[null],r=i.concat(e);return Function.bind.apply(n,r)}exports.partial=partial;function isArray(n){return Array.isArray(n)}exports.isArray=isArray;function isRegExp(n){return n instanceof RegExp}exports.isRegExp=isRegExp;function isObject(n){return n instanceof Object}exports.isObject=isObject;function every(n,e){for(var t=0;t<n.length;t++)if(!e(n[t],t))return!1;return!0}exports.every=every;function difference(n,e){return reject(n,function(t){return contains(e,t)})}exports.difference=difference;function some(n,e){for(var t=0;t<n.length;t++)if(e(n[t]))return!0;return!1}exports.some=some;function indexOf(n,e){for(var t=0;t<n.length;t++)if(n[t]===e)return t;return-1}exports.indexOf=indexOf;function sortBy(n,e){var t=cloneArr(n);return t.sort(function(i,r){return e(i)-e(r)}),t}exports.sortBy=sortBy;function zipObject(n,e){if(n.length!==e.length)throw Error("can't zipObject with different number of keys and values!");for(var t={},i=0;i<n.length;i++)t[n[i]]=e[i];return t}exports.zipObject=zipObject;function assign(n){for(var e=[],t=1;t<arguments.length;t++)e[t-1]=arguments[t];for(var i=0;i<e.length;i++)for(var r=e[i],s=keys(r),o=0;o<s.length;o++){var c=s[o];n[c]=r[c]}return n}exports.assign=assign;function assignNoOverwrite(n){for(var e=[],t=1;t<arguments.length;t++)e[t-1]=arguments[t];for(var i=0;i<e.length;i++)for(var r=e[i],s=keys(r),o=0;o<s.length;o++){var c=s[o];has(n,c)||(n[c]=r[c])}return n}exports.assignNoOverwrite=assignNoOverwrite;function defaults(){for(var n=[],e=0;e<arguments.length;e++)n[e]=arguments[e];return assignNoOverwrite.apply(void 0,__spreadArray([{}],n))}exports.defaults=defaults;function groupBy(n,e){var t={};return forEach(n,function(i){var r=e(i),s=t[r];s?s.push(i):t[r]=[i]}),t}exports.groupBy=groupBy;function merge(n,e){for(var t=cloneObj(n),i=keys(e),r=0;r<i.length;r++){var s=i[r],o=e[s];t[s]=o}return t}exports.merge=merge;function NOOP(){}exports.NOOP=NOOP;function IDENTITY(n){return n}exports.IDENTITY=IDENTITY;function packArray(n){for(var e=[],t=0;t<n.length;t++){var i=n[t];e.push(i!==void 0?i:void 0)}return e}exports.packArray=packArray;function PRINT_ERROR(n){console&&console.error&&console.error("Error: "+n)}exports.PRINT_ERROR=PRINT_ERROR;function PRINT_WARNING(n){console&&console.warn&&console.warn("Warning: "+n)}exports.PRINT_WARNING=PRINT_WARNING;function isES2015MapSupported(){return typeof Map=="function"}exports.isES2015MapSupported=isES2015MapSupported;function peek(n){return n[n.length-1]}exports.peek=peek;function timer(n){var e=new Date().getTime(),t=n(),i=new Date().getTime(),r=i-e;return{time:r,value:t}}exports.timer=timer;function toFastProperties(toBecomeFast){function FakeConstructor(){}FakeConstructor.prototype=toBecomeFast;var fakeInstance=new FakeConstructor;function fakeAccess(){return typeof fakeInstance.bar}return fakeAccess(),fakeAccess(),toBecomeFast}exports.toFastProperties=toFastProperties}),Rc=je((n,e)=>{(function(t,i){typeof define=="function"&&define.amd?define([],i):typeof e=="object"&&e.exports?e.exports=i():t.regexpToAst=i()})(typeof self<"u"?self:n,function(){function t(){}t.prototype.saveState=function(){return{idx:this.idx,input:this.input,groupIdx:this.groupIdx}},t.prototype.restoreState=function(h){this.idx=h.idx,this.input=h.input,this.groupIdx=h.groupIdx},t.prototype.pattern=function(h){this.idx=0,this.input=h,this.groupIdx=0,this.consumeChar("/");var u=this.disjunction();this.consumeChar("/");for(var E={type:"Flags",loc:{begin:this.idx,end:h.length},global:!1,ignoreCase:!1,multiLine:!1,unicode:!1,sticky:!1};this.isRegExpFlag();)switch(this.popChar()){case"g":l(E,"global");break;case"i":l(E,"ignoreCase");break;case"m":l(E,"multiLine");break;case"u":l(E,"unicode");break;case"y":l(E,"sticky");break}if(this.idx!==this.input.length)throw Error("Redundant input: "+this.input.substring(this.idx));return{type:"Pattern",flags:E,value:u,loc:this.loc(0)}},t.prototype.disjunction=function(){var h=[],u=this.idx;for(h.push(this.alternative());this.peekChar()==="|";)this.consumeChar("|"),h.push(this.alternative());return{type:"Disjunction",value:h,loc:this.loc(u)}},t.prototype.alternative=function(){for(var h=[],u=this.idx;this.isTerm();)h.push(this.term());return{type:"Alternative",value:h,loc:this.loc(u)}},t.prototype.term=function(){return this.isAssertion()?this.assertion():this.atom()},t.prototype.assertion=function(){var h=this.idx;switch(this.popChar()){case"^":return{type:"StartAnchor",loc:this.loc(h)};case"$":return{type:"EndAnchor",loc:this.loc(h)};case"\\":switch(this.popChar()){case"b":return{type:"WordBoundary",loc:this.loc(h)};case"B":return{type:"NonWordBoundary",loc:this.loc(h)}}throw Error("Invalid Assertion Escape");case"(":this.consumeChar("?");var u;switch(this.popChar()){case"=":u="Lookahead";break;case"!":u="NegativeLookahead";break}a(u);var E=this.disjunction();return this.consumeChar(")"),{type:u,value:E,loc:this.loc(h)}}d()},t.prototype.quantifier=function(h){var u,E=this.idx;switch(this.popChar()){case"*":u={atLeast:0,atMost:1/0};break;case"+":u={atLeast:1,atMost:1/0};break;case"?":u={atLeast:0,atMost:1};break;case"{":var x=this.integerIncludingZero();switch(this.popChar()){case"}":u={atLeast:x,atMost:x};break;case",":var _;this.isDigit()?(_=this.integerIncludingZero(),u={atLeast:x,atMost:_}):u={atLeast:x,atMost:1/0},this.consumeChar("}");break}if(h===!0&&u===void 0)return;a(u);break}if(!(h===!0&&u===void 0))return a(u),this.peekChar(0)==="?"?(this.consumeChar("?"),u.greedy=!1):u.greedy=!0,u.type="Quantifier",u.loc=this.loc(E),u},t.prototype.atom=function(){var h,u=this.idx;switch(this.peekChar()){case".":h=this.dotAll();break;case"\\":h=this.atomEscape();break;case"[":h=this.characterClass();break;case"(":h=this.group();break}return h===void 0&&this.isPatternCharacter()&&(h=this.patternCharacter()),a(h),h.loc=this.loc(u),this.isQuantifier()&&(h.quantifier=this.quantifier()),h},t.prototype.dotAll=function(){return this.consumeChar("."),{type:"Set",complement:!0,value:[o(`
`),o("\r"),o("\u2028"),o("\u2029")]}},t.prototype.atomEscape=function(){switch(this.consumeChar("\\"),this.peekChar()){case"1":case"2":case"3":case"4":case"5":case"6":case"7":case"8":case"9":return this.decimalEscapeAtom();case"d":case"D":case"s":case"S":case"w":case"W":return this.characterClassEscape();case"f":case"n":case"r":case"t":case"v":return this.controlEscapeAtom();case"c":return this.controlLetterEscapeAtom();case"0":return this.nulCharacterAtom();case"x":return this.hexEscapeSequenceAtom();case"u":return this.regExpUnicodeEscapeSequenceAtom();default:return this.identityEscapeAtom()}},t.prototype.decimalEscapeAtom=function(){var h=this.positiveInteger();return{type:"GroupBackReference",value:h}},t.prototype.characterClassEscape=function(){var h,u=!1;switch(this.popChar()){case"d":h=f;break;case"D":h=f,u=!0;break;case"s":h=g;break;case"S":h=g,u=!0;break;case"w":h=m;break;case"W":h=m,u=!0;break}return a(h),{type:"Set",value:h,complement:u}},t.prototype.controlEscapeAtom=function(){var h;switch(this.popChar()){case"f":h=o("\f");break;case"n":h=o(`
`);break;case"r":h=o("\r");break;case"t":h=o("	");break;case"v":h=o("\v");break}return a(h),{type:"Character",value:h}},t.prototype.controlLetterEscapeAtom=function(){this.consumeChar("c");var h=this.popChar();if(/[a-zA-Z]/.test(h)===!1)throw Error("Invalid ");var u=h.toUpperCase().charCodeAt(0)-64;return{type:"Character",value:u}},t.prototype.nulCharacterAtom=function(){return this.consumeChar("0"),{type:"Character",value:o("\0")}},t.prototype.hexEscapeSequenceAtom=function(){return this.consumeChar("x"),this.parseHexDigits(2)},t.prototype.regExpUnicodeEscapeSequenceAtom=function(){return this.consumeChar("u"),this.parseHexDigits(4)},t.prototype.identityEscapeAtom=function(){var h=this.popChar();return{type:"Character",value:o(h)}},t.prototype.classPatternCharacterAtom=function(){switch(this.peekChar()){case`
`:case"\r":case"\u2028":case"\u2029":case"\\":case"]":throw Error("TBD");default:var h=this.popChar();return{type:"Character",value:o(h)}}},t.prototype.characterClass=function(){var h=[],u=!1;for(this.consumeChar("["),this.peekChar(0)==="^"&&(this.consumeChar("^"),u=!0);this.isClassAtom();){var E=this.classAtom(),x=E.type==="Character";if(x&&this.isRangeDash()){this.consumeChar("-");var _=this.classAtom(),A=_.type==="Character";if(A){if(_.value<E.value)throw Error("Range out of order in character class");h.push({from:E.value,to:_.value})}else c(E.value,h),h.push(o("-")),c(_.value,h)}else c(E.value,h)}return this.consumeChar("]"),{type:"Set",complement:u,value:h}},t.prototype.classAtom=function(){switch(this.peekChar()){case"]":case`
`:case"\r":case"\u2028":case"\u2029":throw Error("TBD");case"\\":return this.classEscape();default:return this.classPatternCharacterAtom()}},t.prototype.classEscape=function(){switch(this.consumeChar("\\"),this.peekChar()){case"b":return this.consumeChar("b"),{type:"Character",value:o("\b")};case"d":case"D":case"s":case"S":case"w":case"W":return this.characterClassEscape();case"f":case"n":case"r":case"t":case"v":return this.controlEscapeAtom();case"c":return this.controlLetterEscapeAtom();case"0":return this.nulCharacterAtom();case"x":return this.hexEscapeSequenceAtom();case"u":return this.regExpUnicodeEscapeSequenceAtom();default:return this.identityEscapeAtom()}},t.prototype.group=function(){var h=!0;(this.consumeChar("("),this.peekChar(0))==="?"?(this.consumeChar("?"),this.consumeChar(":"),h=!1):this.groupIdx++;var u=this.disjunction();this.consumeChar(")");var E={type:"Group",capturing:h,value:u};return h&&(E.idx=this.groupIdx),E},t.prototype.positiveInteger=function(){var h=this.popChar();if(s.test(h)===!1)throw Error("Expecting a positive integer");for(;r.test(this.peekChar(0));)h+=this.popChar();return parseInt(h,10)},t.prototype.integerIncludingZero=function(){var h=this.popChar();if(r.test(h)===!1)throw Error("Expecting an integer");for(;r.test(this.peekChar(0));)h+=this.popChar();return parseInt(h,10)},t.prototype.patternCharacter=function(){var h=this.popChar();switch(h){case`
`:case"\r":case"\u2028":case"\u2029":case"^":case"$":case"\\":case".":case"*":case"+":case"?":case"(":case")":case"[":case"|":throw Error("TBD");default:return{type:"Character",value:o(h)}}},t.prototype.isRegExpFlag=function(){switch(this.peekChar(0)){case"g":case"i":case"m":case"u":case"y":return!0;default:return!1}},t.prototype.isRangeDash=function(){return this.peekChar()==="-"&&this.isClassAtom(1)},t.prototype.isDigit=function(){return r.test(this.peekChar(0))},t.prototype.isClassAtom=function(h){switch(h===void 0&&(h=0),this.peekChar(h)){case"]":case`
`:case"\r":case"\u2028":case"\u2029":return!1;default:return!0}},t.prototype.isTerm=function(){return this.isAtom()||this.isAssertion()},t.prototype.isAtom=function(){if(this.isPatternCharacter())return!0;switch(this.peekChar(0)){case".":case"\\":case"[":case"(":return!0;default:return!1}},t.prototype.isAssertion=function(){switch(this.peekChar(0)){case"^":case"$":return!0;case"\\":switch(this.peekChar(1)){case"b":case"B":return!0;default:return!1}case"(":return this.peekChar(1)==="?"&&(this.peekChar(2)==="="||this.peekChar(2)==="!");default:return!1}},t.prototype.isQuantifier=function(){var h=this.saveState();try{return this.quantifier(!0)!==void 0}catch{return!1}finally{this.restoreState(h)}},t.prototype.isPatternCharacter=function(){switch(this.peekChar()){case"^":case"$":case"\\":case".":case"*":case"+":case"?":case"(":case")":case"[":case"|":case"/":case`
`:case"\r":case"\u2028":case"\u2029":return!1;default:return!0}},t.prototype.parseHexDigits=function(h){for(var u="",E=0;E<h;E++){var x=this.popChar();if(i.test(x)===!1)throw Error("Expecting a HexDecimal digits");u+=x}var _=parseInt(u,16);return{type:"Character",value:_}},t.prototype.peekChar=function(h){return h===void 0&&(h=0),this.input[this.idx+h]},t.prototype.popChar=function(){var h=this.peekChar(0);return this.consumeChar(),h},t.prototype.consumeChar=function(h){if(h!==void 0&&this.input[this.idx]!==h)throw Error("Expected: '"+h+"' but found: '"+this.input[this.idx]+"' at offset: "+this.idx);if(this.idx>=this.input.length)throw Error("Unexpected end of input");this.idx++},t.prototype.loc=function(h){return{begin:h,end:this.idx}};var i=/[0-9a-fA-F]/,r=/[0-9]/,s=/[1-9]/;function o(h){return h.charCodeAt(0)}function c(h,u){h.length!==void 0?h.forEach(function(E){u.push(E)}):u.push(h)}function l(h,u){if(h[u]===!0)throw"duplicate flag "+u;h[u]=!0}function a(h){if(h===void 0)throw Error("Internal Error - Should never get here!")}function d(){throw Error("Internal Error - Should never get here!")}var p,f=[];for(p=o("0");p<=o("9");p++)f.push(p);var m=[o("_")].concat(f);for(p=o("a");p<=o("z");p++)m.push(p);for(p=o("A");p<=o("Z");p++)m.push(p);var g=[o(" "),o("\f"),o(`
`),o("\r"),o("	"),o("\v"),o("	"),o(" "),o(" "),o(" "),o(" "),o(" "),o(" "),o(" "),o(" "),o(" "),o(" "),o(" "),o(" "),o(" "),o("\u2028"),o("\u2029"),o(" "),o(" "),o("　"),o("\uFEFF")];function y(){}return y.prototype.visitChildren=function(h){for(var u in h){var E=h[u];h.hasOwnProperty(u)&&(E.type!==void 0?this.visit(E):Array.isArray(E)&&E.forEach(function(x){this.visit(x)},this))}},y.prototype.visit=function(h){switch(h.type){case"Pattern":this.visitPattern(h);break;case"Flags":this.visitFlags(h);break;case"Disjunction":this.visitDisjunction(h);break;case"Alternative":this.visitAlternative(h);break;case"StartAnchor":this.visitStartAnchor(h);break;case"EndAnchor":this.visitEndAnchor(h);break;case"WordBoundary":this.visitWordBoundary(h);break;case"NonWordBoundary":this.visitNonWordBoundary(h);break;case"Lookahead":this.visitLookahead(h);break;case"NegativeLookahead":this.visitNegativeLookahead(h);break;case"Character":this.visitCharacter(h);break;case"Set":this.visitSet(h);break;case"Group":this.visitGroup(h);break;case"GroupBackReference":this.visitGroupBackReference(h);break;case"Quantifier":this.visitQuantifier(h);break}this.visitChildren(h)},y.prototype.visitPattern=function(h){},y.prototype.visitFlags=function(h){},y.prototype.visitDisjunction=function(h){},y.prototype.visitAlternative=function(h){},y.prototype.visitStartAnchor=function(h){},y.prototype.visitEndAnchor=function(h){},y.prototype.visitWordBoundary=function(h){},y.prototype.visitNonWordBoundary=function(h){},y.prototype.visitLookahead=function(h){},y.prototype.visitNegativeLookahead=function(h){},y.prototype.visitCharacter=function(h){},y.prototype.visitSet=function(h){},y.prototype.visitGroup=function(h){},y.prototype.visitGroupBackReference=function(h){},y.prototype.visitQuantifier=function(h){},{RegExpParser:t,BaseRegExpVisitor:y,VERSION:"0.5.0"}})}),wc=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.clearRegExpParserCache=n.getRegExpAst=void 0;var e=Rc(),t={},i=new e.RegExpParser;function r(o){var c=o.toString();if(t.hasOwnProperty(c))return t[c];var l=i.pattern(c);return t[c]=l,l}n.getRegExpAst=r;function s(){t={}}n.clearRegExpParserCache=s}),s_=je(n=>{"use strict";var e=n&&n.__extends||(function(){var y=function(h,u){return y=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(E,x){E.__proto__=x}||function(E,x){for(var _ in x)Object.prototype.hasOwnProperty.call(x,_)&&(E[_]=x[_])},y(h,u)};return function(h,u){if(typeof u!="function"&&u!==null)throw new TypeError("Class extends value "+String(u)+" is not a constructor or null");y(h,u);function E(){this.constructor=h}h.prototype=u===null?Object.create(u):(E.prototype=u.prototype,new E)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.canMatchCharCode=n.firstCharOptimizedIndices=n.getOptimizedStartCodesIndices=n.failedOptimizationPrefixMsg=void 0;var t=Rc(),i=st(),r=wc(),s=zu(),o="Complement Sets are not supported for first char optimization";n.failedOptimizationPrefixMsg=`Unable to use "first char" lexer optimizations:
`;function c(y,h){h===void 0&&(h=!1);try{var u=r.getRegExpAst(y),E=l(u.value,{},u.flags.ignoreCase);return E}catch(_){if(_.message===o)h&&i.PRINT_WARNING(""+n.failedOptimizationPrefixMsg+("	Unable to optimize: < "+y.toString()+` >
`)+`	Complement Sets cannot be automatically optimized.
	This will disable the lexer's first char optimizations.
	See: https://chevrotain.io/docs/guide/resolving_lexer_errors.html#COMPLEMENT for details.`);else{var x="";h&&(x=`
	This will disable the lexer's first char optimizations.
	See: https://chevrotain.io/docs/guide/resolving_lexer_errors.html#REGEXP_PARSING for details.`),i.PRINT_ERROR(n.failedOptimizationPrefixMsg+`
`+("	Failed parsing: < "+y.toString()+` >
`)+("	Using the regexp-to-ast library version: "+t.VERSION+`
`)+"	Please open an issue at: https://github.com/bd82/regexp-to-ast/issues"+x)}}return[]}n.getOptimizedStartCodesIndices=c;function l(y,h,u){switch(y.type){case"Disjunction":for(var E=0;E<y.value.length;E++)l(y.value[E],h,u);break;case"Alternative":for(var x=y.value,E=0;E<x.length;E++){var _=x[E];switch(_.type){case"EndAnchor":case"GroupBackReference":case"Lookahead":case"NegativeLookahead":case"StartAnchor":case"WordBoundary":case"NonWordBoundary":continue}var A=_;switch(A.type){case"Character":a(A.value,h,u);break;case"Set":if(A.complement===!0)throw Error(o);i.forEach(A.value,function(O){if(typeof O=="number")a(O,h,u);else{var T=O;if(u===!0)for(var M=T.from;M<=T.to;M++)a(M,h,u);else{for(var M=T.from;M<=T.to&&M<s.minOptimizationVal;M++)a(M,h,u);if(T.to>=s.minOptimizationVal)for(var R=T.from>=s.minOptimizationVal?T.from:s.minOptimizationVal,I=T.to,U=s.charCodeToOptimizedIndex(R),P=s.charCodeToOptimizedIndex(I),X=U;X<=P;X++)h[X]=X}}});break;case"Group":l(A.value,h,u);break;default:throw Error("Non Exhaustive Match")}var N=A.quantifier!==void 0&&A.quantifier.atLeast===0;if(A.type==="Group"&&f(A)===!1||A.type!=="Group"&&N===!1)break}break;default:throw Error("non exhaustive match!")}return i.values(h)}n.firstCharOptimizedIndices=l;function a(y,h,u){var E=s.charCodeToOptimizedIndex(y);h[E]=E,u===!0&&d(y,h)}function d(y,h){var u=String.fromCharCode(y),E=u.toUpperCase();if(E!==u){var x=s.charCodeToOptimizedIndex(E.charCodeAt(0));h[x]=x}else{var _=u.toLowerCase();if(_!==u){var x=s.charCodeToOptimizedIndex(_.charCodeAt(0));h[x]=x}}}function p(y,h){return i.find(y.value,function(u){if(typeof u=="number")return i.contains(h,u);var E=u;return i.find(h,function(x){return E.from<=x&&x<=E.to})!==void 0})}function f(y){return y.quantifier&&y.quantifier.atLeast===0?!0:y.value?i.isArray(y.value)?i.every(y.value,f):f(y.value):!1}var m=(function(y){e(h,y);function h(u){var E=y.call(this)||this;return E.targetCharCodes=u,E.found=!1,E}return h.prototype.visitChildren=function(u){if(this.found!==!0){switch(u.type){case"Lookahead":this.visitLookahead(u);return;case"NegativeLookahead":this.visitNegativeLookahead(u);return}y.prototype.visitChildren.call(this,u)}},h.prototype.visitCharacter=function(u){i.contains(this.targetCharCodes,u.value)&&(this.found=!0)},h.prototype.visitSet=function(u){u.complement?p(u,this.targetCharCodes)===void 0&&(this.found=!0):p(u,this.targetCharCodes)!==void 0&&(this.found=!0)},h})(t.BaseRegExpVisitor);function g(y,h){if(h instanceof RegExp){var u=r.getRegExpAst(h),E=new m(y);return E.visit(u),E.found}else return i.find(h,function(x){return i.contains(y,x.charCodeAt(0))})!==void 0}n.canMatchCharCode=g}),zu=je(n=>{"use strict";var e=n&&n.__extends||(function(){var k=function(Y,K){return k=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(ne,ie){ne.__proto__=ie}||function(ne,ie){for(var de in ie)Object.prototype.hasOwnProperty.call(ie,de)&&(ne[de]=ie[de])},k(Y,K)};return function(Y,K){if(typeof K!="function"&&K!==null)throw new TypeError("Class extends value "+String(K)+" is not a constructor or null");k(Y,K);function ne(){this.constructor=Y}Y.prototype=K===null?Object.create(K):(ne.prototype=K.prototype,new ne)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.charCodeToOptimizedIndex=n.minOptimizationVal=n.buildLineBreakIssueMessage=n.LineTerminatorOptimizedTester=n.isShortPattern=n.isCustomPattern=n.cloneEmptyGroups=n.performWarningRuntimeChecks=n.performRuntimeChecks=n.addStickyFlag=n.addStartOfInput=n.findUnreachablePatterns=n.findModesThatDoNotExist=n.findInvalidGroupType=n.findDuplicatePatterns=n.findUnsupportedFlags=n.findStartOfInputAnchor=n.findEmptyMatchRegExps=n.findEndOfInputAnchor=n.findInvalidPatterns=n.findMissingPatterns=n.validatePatterns=n.analyzeTokenTypes=n.enableSticky=n.disableSticky=n.SUPPORT_STICKY=n.MODES=n.DEFAULT_MODE=void 0;var t=Rc(),i=jo(),r=st(),s=s_(),o=wc(),c="PATTERN";n.DEFAULT_MODE="defaultMode",n.MODES="modes",n.SUPPORT_STICKY=typeof new RegExp("(?:)").sticky=="boolean";function l(){n.SUPPORT_STICKY=!1}n.disableSticky=l;function a(){n.SUPPORT_STICKY=!0}n.enableSticky=a;function d(k,Y){Y=r.defaults(Y,{useSticky:n.SUPPORT_STICKY,debug:!1,safeMode:!1,positionTracking:"full",lineTerminatorCharacters:["\r",`
`],tracer:function(S,v){return v()}});var K=Y.tracer;K("initCharCodeToOptimizedIndexMap",function(){Me()});var ne;K("Reject Lexer.NA",function(){ne=r.reject(k,function(S){return S[c]===i.Lexer.NA})});var ie=!1,de;K("Transform Patterns",function(){ie=!1,de=r.map(ne,function(S){var v=S[c];if(r.isRegExp(v)){var b=v.source;return b.length===1&&b!=="^"&&b!=="$"&&b!=="."&&!v.ignoreCase?b:b.length===2&&b[0]==="\\"&&!r.contains(["d","D","s","S","t","r","n","t","0","c","b","B","f","v","w","W"],b[1])?b[1]:Y.useSticky?I(v):R(v)}else{if(r.isFunction(v))return ie=!0,{exec:v};if(r.has(v,"exec"))return ie=!0,v;if(typeof v=="string"){if(v.length===1)return v;var D=v.replace(/[\\^$.*+?()[\]{}|]/g,"\\$&"),L=new RegExp(D);return Y.useSticky?I(L):R(L)}else throw Error("non exhaustive match")}})});var Le,we,B,Ge,Ne;K("misc mapping",function(){Le=r.map(ne,function(S){return S.tokenTypeIdx}),we=r.map(ne,function(S){var v=S.GROUP;if(v!==i.Lexer.SKIPPED){if(r.isString(v))return v;if(r.isUndefined(v))return!1;throw Error("non exhaustive match")}}),B=r.map(ne,function(S){var v=S.LONGER_ALT;if(v){var b=r.indexOf(ne,v);return b}}),Ge=r.map(ne,function(S){return S.PUSH_MODE}),Ne=r.map(ne,function(S){return r.has(S,"POP_MODE")})});var Ke;K("Line Terminator Handling",function(){var S=ae(Y.lineTerminatorCharacters);Ke=r.map(ne,function(v){return!1}),Y.positionTracking!=="onlyOffset"&&(Ke=r.map(ne,function(v){if(r.has(v,"LINE_BREAKS"))return v.LINE_BREAKS;if(G(v,S)===!1)return s.canMatchCharCode(S,v.PATTERN)}))});var Oe,Je,Re,He;K("Misc Mapping #2",function(){Oe=r.map(ne,W),Je=r.map(de,q),Re=r.reduce(ne,function(S,v){var b=v.GROUP;return r.isString(b)&&b!==i.Lexer.SKIPPED&&(S[b]=[]),S},{}),He=r.map(de,function(S,v){return{pattern:de[v],longerAlt:B[v],canLineTerminator:Ke[v],isCustom:Oe[v],short:Je[v],group:we[v],push:Ge[v],pop:Ne[v],tokenTypeIdx:Le[v],tokenType:ne[v]}})});var ot=!0,it=[];return Y.safeMode||K("First Char Optimization",function(){it=r.reduce(ne,function(S,v,b){if(typeof v.PATTERN=="string"){var D=v.PATTERN.charCodeAt(0),L=me(D);ue(S,L,He[b])}else if(r.isArray(v.START_CHARS_HINT)){var F;r.forEach(v.START_CHARS_HINT,function(z){var j=typeof z=="string"?z.charCodeAt(0):z,te=me(j);F!==te&&(F=te,ue(S,te,He[b]))})}else if(r.isRegExp(v.PATTERN))if(v.PATTERN.unicode)ot=!1,Y.ensureOptimizations&&r.PRINT_ERROR(""+s.failedOptimizationPrefixMsg+("	Unable to analyze < "+v.PATTERN.toString()+` > pattern.
`)+`	The regexp unicode flag is not currently supported by the regexp-to-ast library.
	This will disable the lexer's first char optimizations.
	For details See: https://chevrotain.io/docs/guide/resolving_lexer_errors.html#UNICODE_OPTIMIZE`);else{var H=s.getOptimizedStartCodesIndices(v.PATTERN,Y.ensureOptimizations);r.isEmpty(H)&&(ot=!1),r.forEach(H,function(z){ue(S,z,He[b])})}else Y.ensureOptimizations&&r.PRINT_ERROR(""+s.failedOptimizationPrefixMsg+("	TokenType: <"+v.name+`> is using a custom token pattern without providing <start_chars_hint> parameter.
`)+`	This will disable the lexer's first char optimizations.
	For details See: https://chevrotain.io/docs/guide/resolving_lexer_errors.html#CUSTOM_OPTIMIZE`),ot=!1;return S},[])}),K("ArrayPacking",function(){it=r.packArray(it)}),{emptyGroups:Re,patternIdxToConfig:He,charCodeToPatternIdxToConfig:it,hasCustom:ie,canBeOptimized:ot}}n.analyzeTokenTypes=d;function p(k,Y){var K=[],ne=m(k);K=K.concat(ne.errors);var ie=g(ne.valid),de=ie.valid;return K=K.concat(ie.errors),K=K.concat(f(de)),K=K.concat(N(de)),K=K.concat(w(de,Y)),K=K.concat(O(de)),K}n.validatePatterns=p;function f(k){var Y=[],K=r.filter(k,function(ne){return r.isRegExp(ne[c])});return Y=Y.concat(h(K)),Y=Y.concat(x(K)),Y=Y.concat(_(K)),Y=Y.concat(A(K)),Y=Y.concat(u(K)),Y}function m(k){var Y=r.filter(k,function(ie){return!r.has(ie,c)}),K=r.map(Y,function(ie){return{message:"Token Type: ->"+ie.name+"<- missing static 'PATTERN' property",type:i.LexerDefinitionErrorType.MISSING_PATTERN,tokenTypes:[ie]}}),ne=r.difference(k,Y);return{errors:K,valid:ne}}n.findMissingPatterns=m;function g(k){var Y=r.filter(k,function(ie){var de=ie[c];return!r.isRegExp(de)&&!r.isFunction(de)&&!r.has(de,"exec")&&!r.isString(de)}),K=r.map(Y,function(ie){return{message:"Token Type: ->"+ie.name+"<- static 'PATTERN' can only be a RegExp, a Function matching the {CustomPatternMatcherFunc} type or an Object matching the {ICustomPattern} interface.",type:i.LexerDefinitionErrorType.INVALID_PATTERN,tokenTypes:[ie]}}),ne=r.difference(k,Y);return{errors:K,valid:ne}}n.findInvalidPatterns=g;var y=/[^\\][\$]/;function h(k){var Y=(function(ie){e(de,ie);function de(){var Le=ie!==null&&ie.apply(this,arguments)||this;return Le.found=!1,Le}return de.prototype.visitEndAnchor=function(Le){this.found=!0},de})(t.BaseRegExpVisitor),K=r.filter(k,function(ie){var de=ie[c];try{var Le=o.getRegExpAst(de),we=new Y;return we.visit(Le),we.found}catch{return y.test(de.source)}}),ne=r.map(K,function(ie){return{message:`Unexpected RegExp Anchor Error:
	Token Type: ->`+ie.name+`<- static 'PATTERN' cannot contain end of input anchor '$'
	See chevrotain.io/docs/guide/resolving_lexer_errors.html#ANCHORS	for details.`,type:i.LexerDefinitionErrorType.EOI_ANCHOR_FOUND,tokenTypes:[ie]}});return ne}n.findEndOfInputAnchor=h;function u(k){var Y=r.filter(k,function(ne){var ie=ne[c];return ie.test("")}),K=r.map(Y,function(ne){return{message:"Token Type: ->"+ne.name+"<- static 'PATTERN' must not match an empty string",type:i.LexerDefinitionErrorType.EMPTY_MATCH_PATTERN,tokenTypes:[ne]}});return K}n.findEmptyMatchRegExps=u;var E=/[^\\[][\^]|^\^/;function x(k){var Y=(function(ie){e(de,ie);function de(){var Le=ie!==null&&ie.apply(this,arguments)||this;return Le.found=!1,Le}return de.prototype.visitStartAnchor=function(Le){this.found=!0},de})(t.BaseRegExpVisitor),K=r.filter(k,function(ie){var de=ie[c];try{var Le=o.getRegExpAst(de),we=new Y;return we.visit(Le),we.found}catch{return E.test(de.source)}}),ne=r.map(K,function(ie){return{message:`Unexpected RegExp Anchor Error:
	Token Type: ->`+ie.name+`<- static 'PATTERN' cannot contain start of input anchor '^'
	See https://chevrotain.io/docs/guide/resolving_lexer_errors.html#ANCHORS	for details.`,type:i.LexerDefinitionErrorType.SOI_ANCHOR_FOUND,tokenTypes:[ie]}});return ne}n.findStartOfInputAnchor=x;function _(k){var Y=r.filter(k,function(ne){var ie=ne[c];return ie instanceof RegExp&&(ie.multiline||ie.global)}),K=r.map(Y,function(ne){return{message:"Token Type: ->"+ne.name+"<- static 'PATTERN' may NOT contain global('g') or multiline('m')",type:i.LexerDefinitionErrorType.UNSUPPORTED_FLAGS_FOUND,tokenTypes:[ne]}});return K}n.findUnsupportedFlags=_;function A(k){var Y=[],K=r.map(k,function(de){return r.reduce(k,function(Le,we){return de.PATTERN.source===we.PATTERN.source&&!r.contains(Y,we)&&we.PATTERN!==i.Lexer.NA&&(Y.push(we),Le.push(we)),Le},[])});K=r.compact(K);var ne=r.filter(K,function(de){return de.length>1}),ie=r.map(ne,function(de){var Le=r.map(de,function(B){return B.name}),we=r.first(de).PATTERN;return{message:"The same RegExp pattern ->"+we+"<-"+("has been used in all of the following Token Types: "+Le.join(", ")+" <-"),type:i.LexerDefinitionErrorType.DUPLICATE_PATTERNS_FOUND,tokenTypes:de}});return ie}n.findDuplicatePatterns=A;function N(k){var Y=r.filter(k,function(ne){if(!r.has(ne,"GROUP"))return!1;var ie=ne.GROUP;return ie!==i.Lexer.SKIPPED&&ie!==i.Lexer.NA&&!r.isString(ie)}),K=r.map(Y,function(ne){return{message:"Token Type: ->"+ne.name+"<- static 'GROUP' can only be Lexer.SKIPPED/Lexer.NA/A String",type:i.LexerDefinitionErrorType.INVALID_GROUP_TYPE_FOUND,tokenTypes:[ne]}});return K}n.findInvalidGroupType=N;function w(k,Y){var K=r.filter(k,function(ie){return ie.PUSH_MODE!==void 0&&!r.contains(Y,ie.PUSH_MODE)}),ne=r.map(K,function(ie){var de="Token Type: ->"+ie.name+"<- static 'PUSH_MODE' value cannot refer to a Lexer Mode ->"+ie.PUSH_MODE+"<-which does not exist";return{message:de,type:i.LexerDefinitionErrorType.PUSH_MODE_DOES_NOT_EXIST,tokenTypes:[ie]}});return ne}n.findModesThatDoNotExist=w;function O(k){var Y=[],K=r.reduce(k,function(ne,ie,de){var Le=ie.PATTERN;return Le===i.Lexer.NA||(r.isString(Le)?ne.push({str:Le,idx:de,tokenType:ie}):r.isRegExp(Le)&&M(Le)&&ne.push({str:Le.source,idx:de,tokenType:ie})),ne},[]);return r.forEach(k,function(ne,ie){r.forEach(K,function(de){var Le=de.str,we=de.idx,B=de.tokenType;if(ie<we&&T(Le,ne.PATTERN)){var Ge="Token: ->"+B.name+`<- can never be matched.
`+("Because it appears AFTER the Token Type ->"+ne.name+"<-")+`in the lexer's definition.
See https://chevrotain.io/docs/guide/resolving_lexer_errors.html#UNREACHABLE`;Y.push({message:Ge,type:i.LexerDefinitionErrorType.UNREACHABLE_PATTERN,tokenTypes:[ne,B]})}})}),Y}n.findUnreachablePatterns=O;function T(k,Y){if(r.isRegExp(Y)){var K=Y.exec(k);return K!==null&&K.index===0}else{if(r.isFunction(Y))return Y(k,0,[],{});if(r.has(Y,"exec"))return Y.exec(k,0,[],{});if(typeof Y=="string")return Y===k;throw Error("non exhaustive match")}}function M(k){var Y=[".","\\","[","]","|","^","$","(",")","?","*","+","{"];return r.find(Y,function(K){return k.source.indexOf(K)!==-1})===void 0}function R(k){var Y=k.ignoreCase?"i":"";return new RegExp("^(?:"+k.source+")",Y)}n.addStartOfInput=R;function I(k){var Y=k.ignoreCase?"iy":"y";return new RegExp(""+k.source,Y)}n.addStickyFlag=I;function U(k,Y,K){var ne=[];return r.has(k,n.DEFAULT_MODE)||ne.push({message:"A MultiMode Lexer cannot be initialized without a <"+n.DEFAULT_MODE+`> property in its definition
`,type:i.LexerDefinitionErrorType.MULTI_MODE_LEXER_WITHOUT_DEFAULT_MODE}),r.has(k,n.MODES)||ne.push({message:"A MultiMode Lexer cannot be initialized without a <"+n.MODES+`> property in its definition
`,type:i.LexerDefinitionErrorType.MULTI_MODE_LEXER_WITHOUT_MODES_PROPERTY}),r.has(k,n.MODES)&&r.has(k,n.DEFAULT_MODE)&&!r.has(k.modes,k.defaultMode)&&ne.push({message:"A MultiMode Lexer cannot be initialized with a "+n.DEFAULT_MODE+": <"+k.defaultMode+`>which does not exist
`,type:i.LexerDefinitionErrorType.MULTI_MODE_LEXER_DEFAULT_MODE_VALUE_DOES_NOT_EXIST}),r.has(k,n.MODES)&&r.forEach(k.modes,function(ie,de){r.forEach(ie,function(Le,we){r.isUndefined(Le)&&ne.push({message:"A Lexer cannot be initialized using an undefined Token Type. Mode:"+("<"+de+"> at index: <"+we+`>
`),type:i.LexerDefinitionErrorType.LEXER_DEFINITION_CANNOT_CONTAIN_UNDEFINED})})}),ne}n.performRuntimeChecks=U;function P(k,Y,K){var ne=[],ie=!1,de=r.compact(r.flatten(r.mapValues(k.modes,function(B){return B}))),Le=r.reject(de,function(B){return B[c]===i.Lexer.NA}),we=ae(K);return Y&&r.forEach(Le,function(B){var Ge=G(B,we);if(Ge!==!1){var Ne=ee(B,Ge),Ke={message:Ne,type:Ge.issue,tokenType:B};ne.push(Ke)}else r.has(B,"LINE_BREAKS")?B.LINE_BREAKS===!0&&(ie=!0):s.canMatchCharCode(we,B.PATTERN)&&(ie=!0)}),Y&&!ie&&ne.push({message:`Warning: No LINE_BREAKS Found.
	This Lexer has been defined to track line and column information,
	But none of the Token Types can be identified as matching a line terminator.
	See https://chevrotain.io/docs/guide/resolving_lexer_errors.html#LINE_BREAKS
	for details.`,type:i.LexerDefinitionErrorType.NO_LINE_BREAKS_FLAGS}),ne}n.performWarningRuntimeChecks=P;function X(k){var Y={},K=r.keys(k);return r.forEach(K,function(ne){var ie=k[ne];if(r.isArray(ie))Y[ne]=[];else throw Error("non exhaustive match")}),Y}n.cloneEmptyGroups=X;function W(k){var Y=k.PATTERN;if(r.isRegExp(Y))return!1;if(r.isFunction(Y)||r.has(Y,"exec"))return!0;if(r.isString(Y))return!1;throw Error("non exhaustive match")}n.isCustomPattern=W;function q(k){return r.isString(k)&&k.length===1?k.charCodeAt(0):!1}n.isShortPattern=q,n.LineTerminatorOptimizedTester={test:function(k){for(var Y=k.length,K=this.lastIndex;K<Y;K++){var ne=k.charCodeAt(K);if(ne===10)return this.lastIndex=K+1,!0;if(ne===13)return k.charCodeAt(K+1)===10?this.lastIndex=K+2:this.lastIndex=K+1,!0}return!1},lastIndex:0};function G(k,Y){if(r.has(k,"LINE_BREAKS"))return!1;if(r.isRegExp(k.PATTERN)){try{s.canMatchCharCode(Y,k.PATTERN)}catch(K){return{issue:i.LexerDefinitionErrorType.IDENTIFY_TERMINATOR,errMsg:K.message}}return!1}else{if(r.isString(k.PATTERN))return!1;if(W(k))return{issue:i.LexerDefinitionErrorType.CUSTOM_LINE_BREAK};throw Error("non exhaustive match")}}function ee(k,Y){if(Y.issue===i.LexerDefinitionErrorType.IDENTIFY_TERMINATOR)return`Warning: unable to identify line terminator usage in pattern.
`+("	The problem is in the <"+k.name+`> Token Type
`)+("	 Root cause: "+Y.errMsg+`.
`)+"	For details See: https://chevrotain.io/docs/guide/resolving_lexer_errors.html#IDENTIFY_TERMINATOR";if(Y.issue===i.LexerDefinitionErrorType.CUSTOM_LINE_BREAK)return`Warning: A Custom Token Pattern should specify the <line_breaks> option.
`+("	The problem is in the <"+k.name+`> Token Type
`)+"	For details See: https://chevrotain.io/docs/guide/resolving_lexer_errors.html#CUSTOM_LINE_BREAK";throw Error("non exhaustive match")}n.buildLineBreakIssueMessage=ee;function ae(k){var Y=r.map(k,function(K){return r.isString(K)&&K.length>0?K.charCodeAt(0):K});return Y}function ue(k,Y,K){k[Y]===void 0?k[Y]=[K]:k[Y].push(K)}n.minOptimizationVal=256;var _e=[];function me(k){return k<n.minOptimizationVal?k:_e[k]}n.charCodeToOptimizedIndex=me;function Me(){if(r.isEmpty(_e)){_e=new Array(65536);for(var k=0;k<65536;k++)_e[k]=k>255?255+~~(k/255):k}}}),$r=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.isTokenType=n.hasExtendingTokensTypesMapProperty=n.hasExtendingTokensTypesProperty=n.hasCategoriesProperty=n.hasShortKeyProperty=n.singleAssignCategoriesToksMap=n.assignCategoriesMapProp=n.assignCategoriesTokensProp=n.assignTokenDefaultProps=n.expandCategories=n.augmentTokenTypes=n.tokenIdxToClass=n.tokenShortNameIdx=n.tokenStructuredMatcherNoCategories=n.tokenStructuredMatcher=void 0;var e=st();function t(y,h){var u=y.tokenTypeIdx;return u===h.tokenTypeIdx?!0:h.isParent===!0&&h.categoryMatchesMap[u]===!0}n.tokenStructuredMatcher=t;function i(y,h){return y.tokenTypeIdx===h.tokenTypeIdx}n.tokenStructuredMatcherNoCategories=i,n.tokenShortNameIdx=1,n.tokenIdxToClass={};function r(y){var h=s(y);o(h),l(h),c(h),e.forEach(h,function(u){u.isParent=u.categoryMatches.length>0})}n.augmentTokenTypes=r;function s(y){for(var h=e.cloneArr(y),u=y,E=!0;E;){u=e.compact(e.flatten(e.map(u,function(_){return _.CATEGORIES})));var x=e.difference(u,h);h=h.concat(x),e.isEmpty(x)?E=!1:u=x}return h}n.expandCategories=s;function o(y){e.forEach(y,function(h){d(h)||(n.tokenIdxToClass[n.tokenShortNameIdx]=h,h.tokenTypeIdx=n.tokenShortNameIdx++),p(h)&&!e.isArray(h.CATEGORIES)&&(h.CATEGORIES=[h.CATEGORIES]),p(h)||(h.CATEGORIES=[]),f(h)||(h.categoryMatches=[]),m(h)||(h.categoryMatchesMap={})})}n.assignTokenDefaultProps=o;function c(y){e.forEach(y,function(h){h.categoryMatches=[],e.forEach(h.categoryMatchesMap,function(u,E){h.categoryMatches.push(n.tokenIdxToClass[E].tokenTypeIdx)})})}n.assignCategoriesTokensProp=c;function l(y){e.forEach(y,function(h){a([],h)})}n.assignCategoriesMapProp=l;function a(y,h){e.forEach(y,function(u){h.categoryMatchesMap[u.tokenTypeIdx]=!0}),e.forEach(h.CATEGORIES,function(u){var E=y.concat(h);e.contains(E,u)||a(E,u)})}n.singleAssignCategoriesToksMap=a;function d(y){return e.has(y,"tokenTypeIdx")}n.hasShortKeyProperty=d;function p(y){return e.has(y,"CATEGORIES")}n.hasCategoriesProperty=p;function f(y){return e.has(y,"categoryMatches")}n.hasExtendingTokensTypesProperty=f;function m(y){return e.has(y,"categoryMatchesMap")}n.hasExtendingTokensTypesMapProperty=m;function g(y){return e.has(y,"tokenTypeIdx")}n.isTokenType=g}),Vu=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.defaultLexerErrorProvider=void 0,n.defaultLexerErrorProvider={buildUnableToPopLexerModeMessage:function(e){return"Unable to pop Lexer Mode after encountering Token ->"+e.image+"<- The Mode Stack is empty"},buildUnexpectedCharactersMessage:function(e,t,i,r,s){return"unexpected character: ->"+e.charAt(t)+"<- at offset: "+t+","+(" skipped "+i+" characters.")}}}),jo=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.Lexer=n.LexerDefinitionErrorType=void 0;var e=zu(),t=st(),i=$r(),r=Vu(),s=wc(),o;(function(a){a[a.MISSING_PATTERN=0]="MISSING_PATTERN",a[a.INVALID_PATTERN=1]="INVALID_PATTERN",a[a.EOI_ANCHOR_FOUND=2]="EOI_ANCHOR_FOUND",a[a.UNSUPPORTED_FLAGS_FOUND=3]="UNSUPPORTED_FLAGS_FOUND",a[a.DUPLICATE_PATTERNS_FOUND=4]="DUPLICATE_PATTERNS_FOUND",a[a.INVALID_GROUP_TYPE_FOUND=5]="INVALID_GROUP_TYPE_FOUND",a[a.PUSH_MODE_DOES_NOT_EXIST=6]="PUSH_MODE_DOES_NOT_EXIST",a[a.MULTI_MODE_LEXER_WITHOUT_DEFAULT_MODE=7]="MULTI_MODE_LEXER_WITHOUT_DEFAULT_MODE",a[a.MULTI_MODE_LEXER_WITHOUT_MODES_PROPERTY=8]="MULTI_MODE_LEXER_WITHOUT_MODES_PROPERTY",a[a.MULTI_MODE_LEXER_DEFAULT_MODE_VALUE_DOES_NOT_EXIST=9]="MULTI_MODE_LEXER_DEFAULT_MODE_VALUE_DOES_NOT_EXIST",a[a.LEXER_DEFINITION_CANNOT_CONTAIN_UNDEFINED=10]="LEXER_DEFINITION_CANNOT_CONTAIN_UNDEFINED",a[a.SOI_ANCHOR_FOUND=11]="SOI_ANCHOR_FOUND",a[a.EMPTY_MATCH_PATTERN=12]="EMPTY_MATCH_PATTERN",a[a.NO_LINE_BREAKS_FLAGS=13]="NO_LINE_BREAKS_FLAGS",a[a.UNREACHABLE_PATTERN=14]="UNREACHABLE_PATTERN",a[a.IDENTIFY_TERMINATOR=15]="IDENTIFY_TERMINATOR",a[a.CUSTOM_LINE_BREAK=16]="CUSTOM_LINE_BREAK"})(o=n.LexerDefinitionErrorType||(n.LexerDefinitionErrorType={}));var c={deferDefinitionErrorsHandling:!1,positionTracking:"full",lineTerminatorsPattern:/\n|\r\n?/g,lineTerminatorCharacters:[`
`,"\r"],ensureOptimizations:!1,safeMode:!1,errorMessageProvider:r.defaultLexerErrorProvider,traceInitPerf:!1,skipValidations:!1};Object.freeze(c);var l=(function(){function a(d,p){var f=this;if(p===void 0&&(p=c),this.lexerDefinition=d,this.lexerDefinitionErrors=[],this.lexerDefinitionWarning=[],this.patternIdxToConfig={},this.charCodeToPatternIdxToConfig={},this.modes=[],this.emptyGroups={},this.config=void 0,this.trackStartLines=!0,this.trackEndLines=!0,this.hasCustom=!1,this.canModeBeOptimized={},typeof p=="boolean")throw Error(`The second argument to the Lexer constructor is now an ILexerConfig Object.
a boolean 2nd argument is no longer supported`);this.config=t.merge(c,p);var m=this.config.traceInitPerf;m===!0?(this.traceInitMaxIdent=1/0,this.traceInitPerf=!0):typeof m=="number"&&(this.traceInitMaxIdent=m,this.traceInitPerf=!0),this.traceInitIndent=-1,this.TRACE_INIT("Lexer Constructor",function(){var g,y=!0;f.TRACE_INIT("Lexer Config handling",function(){if(f.config.lineTerminatorsPattern===c.lineTerminatorsPattern)f.config.lineTerminatorsPattern=e.LineTerminatorOptimizedTester;else if(f.config.lineTerminatorCharacters===c.lineTerminatorCharacters)throw Error(`Error: Missing <lineTerminatorCharacters> property on the Lexer config.
	For details See: https://chevrotain.io/docs/guide/resolving_lexer_errors.html#MISSING_LINE_TERM_CHARS`);if(p.safeMode&&p.ensureOptimizations)throw Error('"safeMode" and "ensureOptimizations" flags are mutually exclusive.');f.trackStartLines=/full|onlyStart/i.test(f.config.positionTracking),f.trackEndLines=/full/i.test(f.config.positionTracking),t.isArray(d)?(g={modes:{}},g.modes[e.DEFAULT_MODE]=t.cloneArr(d),g[e.DEFAULT_MODE]=e.DEFAULT_MODE):(y=!1,g=t.cloneObj(d))}),f.config.skipValidations===!1&&(f.TRACE_INIT("performRuntimeChecks",function(){f.lexerDefinitionErrors=f.lexerDefinitionErrors.concat(e.performRuntimeChecks(g,f.trackStartLines,f.config.lineTerminatorCharacters))}),f.TRACE_INIT("performWarningRuntimeChecks",function(){f.lexerDefinitionWarning=f.lexerDefinitionWarning.concat(e.performWarningRuntimeChecks(g,f.trackStartLines,f.config.lineTerminatorCharacters))})),g.modes=g.modes?g.modes:{},t.forEach(g.modes,function(x,_){g.modes[_]=t.reject(x,function(A){return t.isUndefined(A)})});var h=t.keys(g.modes);if(t.forEach(g.modes,function(x,_){f.TRACE_INIT("Mode: <"+_+"> processing",function(){if(f.modes.push(_),f.config.skipValidations===!1&&f.TRACE_INIT("validatePatterns",function(){f.lexerDefinitionErrors=f.lexerDefinitionErrors.concat(e.validatePatterns(x,h))}),t.isEmpty(f.lexerDefinitionErrors)){i.augmentTokenTypes(x);var A;f.TRACE_INIT("analyzeTokenTypes",function(){A=e.analyzeTokenTypes(x,{lineTerminatorCharacters:f.config.lineTerminatorCharacters,positionTracking:p.positionTracking,ensureOptimizations:p.ensureOptimizations,safeMode:p.safeMode,tracer:f.TRACE_INIT.bind(f)})}),f.patternIdxToConfig[_]=A.patternIdxToConfig,f.charCodeToPatternIdxToConfig[_]=A.charCodeToPatternIdxToConfig,f.emptyGroups=t.merge(f.emptyGroups,A.emptyGroups),f.hasCustom=A.hasCustom||f.hasCustom,f.canModeBeOptimized[_]=A.canBeOptimized}})}),f.defaultMode=g.defaultMode,!t.isEmpty(f.lexerDefinitionErrors)&&!f.config.deferDefinitionErrorsHandling){var u=t.map(f.lexerDefinitionErrors,function(x){return x.message}),E=u.join(`-----------------------
`);throw new Error(`Errors detected in definition of Lexer:
`+E)}t.forEach(f.lexerDefinitionWarning,function(x){t.PRINT_WARNING(x.message)}),f.TRACE_INIT("Choosing sub-methods implementations",function(){if(e.SUPPORT_STICKY?(f.chopInput=t.IDENTITY,f.match=f.matchWithTest):(f.updateLastIndex=t.NOOP,f.match=f.matchWithExec),y&&(f.handleModes=t.NOOP),f.trackStartLines===!1&&(f.computeNewColumn=t.IDENTITY),f.trackEndLines===!1&&(f.updateTokenEndLineColumnLocation=t.NOOP),/full/i.test(f.config.positionTracking))f.createTokenInstance=f.createFullToken;else if(/onlyStart/i.test(f.config.positionTracking))f.createTokenInstance=f.createStartOnlyToken;else if(/onlyOffset/i.test(f.config.positionTracking))f.createTokenInstance=f.createOffsetOnlyToken;else throw Error('Invalid <positionTracking> config option: "'+f.config.positionTracking+'"');f.hasCustom?(f.addToken=f.addTokenUsingPush,f.handlePayload=f.handlePayloadWithCustom):(f.addToken=f.addTokenUsingMemberAccess,f.handlePayload=f.handlePayloadNoCustom)}),f.TRACE_INIT("Failed Optimization Warnings",function(){var x=t.reduce(f.canModeBeOptimized,function(_,A,N){return A===!1&&_.push(N),_},[]);if(p.ensureOptimizations&&!t.isEmpty(x))throw Error("Lexer Modes: < "+x.join(", ")+` > cannot be optimized.
	 Disable the "ensureOptimizations" lexer config flag to silently ignore this and run the lexer in an un-optimized mode.
	 Or inspect the console log for details on how to resolve these issues.`)}),f.TRACE_INIT("clearRegExpParserCache",function(){s.clearRegExpParserCache()}),f.TRACE_INIT("toFastProperties",function(){t.toFastProperties(f)})})}return a.prototype.tokenize=function(d,p){if(p===void 0&&(p=this.defaultMode),!t.isEmpty(this.lexerDefinitionErrors)){var f=t.map(this.lexerDefinitionErrors,function(y){return y.message}),m=f.join(`-----------------------
`);throw new Error(`Unable to Tokenize because Errors detected in definition of Lexer:
`+m)}var g=this.tokenizeInternal(d,p);return g},a.prototype.tokenizeInternal=function(d,p){var f=this,m,g,y,h,u,E,x,_,A,N,w,O,T,M,R,I=d,U=I.length,P=0,X=0,W=this.hasCustom?0:Math.floor(d.length/10),q=new Array(W),G=[],ee=this.trackStartLines?1:void 0,ae=this.trackStartLines?1:void 0,ue=e.cloneEmptyGroups(this.emptyGroups),_e=this.trackStartLines,me=this.config.lineTerminatorsPattern,Me=0,k=[],Y=[],K=[],ne=[];Object.freeze(ne);var ie=void 0;function de(){return k}function Le(z){var j=e.charCodeToOptimizedIndex(z),te=Y[j];return te===void 0?ne:te}var we=function(z){if(K.length===1&&z.tokenType.PUSH_MODE===void 0){var j=f.config.errorMessageProvider.buildUnableToPopLexerModeMessage(z);G.push({offset:z.startOffset,line:z.startLine!==void 0?z.startLine:void 0,column:z.startColumn!==void 0?z.startColumn:void 0,length:z.image.length,message:j})}else{K.pop();var te=t.last(K);k=f.patternIdxToConfig[te],Y=f.charCodeToPatternIdxToConfig[te],Me=k.length;var Q=f.canModeBeOptimized[te]&&f.config.safeMode===!1;Y&&Q?ie=Le:ie=de}};function B(z){K.push(z),Y=this.charCodeToPatternIdxToConfig[z],k=this.patternIdxToConfig[z],Me=k.length,Me=k.length;var j=this.canModeBeOptimized[z]&&this.config.safeMode===!1;Y&&j?ie=Le:ie=de}B.call(this,p);for(var Ge;P<U;){u=null;var Ne=I.charCodeAt(P),Ke=ie(Ne),Oe=Ke.length;for(m=0;m<Oe;m++){Ge=Ke[m];var Je=Ge.pattern;E=null;var Re=Ge.short;if(Re!==!1?Ne===Re&&(u=Je):Ge.isCustom===!0?(R=Je.exec(I,P,q,ue),R!==null?(u=R[0],R.payload!==void 0&&(E=R.payload)):u=null):(this.updateLastIndex(Je,P),u=this.match(Je,d,P)),u!==null){if(h=Ge.longerAlt,h!==void 0){var He=k[h],ot=He.pattern;x=null,He.isCustom===!0?(R=ot.exec(I,P,q,ue),R!==null?(y=R[0],R.payload!==void 0&&(x=R.payload)):y=null):(this.updateLastIndex(ot,P),y=this.match(ot,d,P)),y&&y.length>u.length&&(u=y,E=x,Ge=He)}break}}if(u!==null){if(_=u.length,A=Ge.group,A!==void 0&&(N=Ge.tokenTypeIdx,w=this.createTokenInstance(u,P,N,Ge.tokenType,ee,ae,_),this.handlePayload(w,E),A===!1?X=this.addToken(q,X,w):ue[A].push(w)),d=this.chopInput(d,_),P=P+_,ae=this.computeNewColumn(ae,_),_e===!0&&Ge.canLineTerminator===!0){var it=0,S=void 0,v=void 0;me.lastIndex=0;do S=me.test(u),S===!0&&(v=me.lastIndex-1,it++);while(S===!0);it!==0&&(ee=ee+it,ae=_-v,this.updateTokenEndLineColumnLocation(w,A,v,it,ee,ae,_))}this.handleModes(Ge,we,B,w)}else{for(var b=P,D=ee,L=ae,F=!1;!F&&P<U;)for(T=I.charCodeAt(P),d=this.chopInput(d,1),P++,g=0;g<Me;g++){var H=k[g],Je=H.pattern,Re=H.short;if(Re!==!1?I.charCodeAt(P)===Re&&(F=!0):H.isCustom===!0?F=Je.exec(I,P,q,ue)!==null:(this.updateLastIndex(Je,P),F=Je.exec(d)!==null),F===!0)break}O=P-b,M=this.config.errorMessageProvider.buildUnexpectedCharactersMessage(I,b,O,D,L),G.push({offset:b,line:D,column:L,length:O,message:M})}}return this.hasCustom||(q.length=X),{tokens:q,groups:ue,errors:G}},a.prototype.handleModes=function(d,p,f,m){if(d.pop===!0){var g=d.push;p(m),g!==void 0&&f.call(this,g)}else d.push!==void 0&&f.call(this,d.push)},a.prototype.chopInput=function(d,p){return d.substring(p)},a.prototype.updateLastIndex=function(d,p){d.lastIndex=p},a.prototype.updateTokenEndLineColumnLocation=function(d,p,f,m,g,y,h){var u,E;p!==void 0&&(u=f===h-1,E=u?-1:0,m===1&&u===!0||(d.endLine=g+E,d.endColumn=y-1+-E))},a.prototype.computeNewColumn=function(d,p){return d+p},a.prototype.createTokenInstance=function(){for(var d=[],p=0;p<arguments.length;p++)d[p]=arguments[p];return null},a.prototype.createOffsetOnlyToken=function(d,p,f,m){return{image:d,startOffset:p,tokenTypeIdx:f,tokenType:m}},a.prototype.createStartOnlyToken=function(d,p,f,m,g,y){return{image:d,startOffset:p,startLine:g,startColumn:y,tokenTypeIdx:f,tokenType:m}},a.prototype.createFullToken=function(d,p,f,m,g,y,h){return{image:d,startOffset:p,endOffset:p+h-1,startLine:g,endLine:g,startColumn:y,endColumn:y+h-1,tokenTypeIdx:f,tokenType:m}},a.prototype.addToken=function(d,p,f){return 666},a.prototype.addTokenUsingPush=function(d,p,f){return d.push(f),p},a.prototype.addTokenUsingMemberAccess=function(d,p,f){return d[p]=f,p++,p},a.prototype.handlePayload=function(d,p){},a.prototype.handlePayloadNoCustom=function(d,p){},a.prototype.handlePayloadWithCustom=function(d,p){p!==null&&(d.payload=p)},a.prototype.match=function(d,p,f){return null},a.prototype.matchWithTest=function(d,p,f){var m=d.test(p);return m===!0?p.substring(f,d.lastIndex):null},a.prototype.matchWithExec=function(d,p){var f=d.exec(p);return f!==null?f[0]:f},a.prototype.TRACE_INIT=function(d,p){if(this.traceInitPerf===!0){this.traceInitIndent++;var f=new Array(this.traceInitIndent+1).join("	");this.traceInitIndent<this.traceInitMaxIdent&&console.log(f+"--> <"+d+">");var m=t.timer(p),g=m.time,y=m.value,h=g>10?console.warn:console.log;return this.traceInitIndent<this.traceInitMaxIdent&&h(f+"<-- <"+d+"> time: "+g+"ms"),this.traceInitIndent--,y}else return p()},a.SKIPPED="This marks a skipped Token pattern, this means each token identified by it willbe consumed and then thrown into oblivion, this can be used to for example to completely ignore whitespace.",a.NA=/NOT_APPLICABLE/,a})();n.Lexer=l}),Ei=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.tokenMatcher=n.createTokenInstance=n.EOF=n.createToken=n.hasTokenLabel=n.tokenName=n.tokenLabel=void 0;var e=st(),t=jo(),i=$r();function r(_){return o(_)?_.LABEL:_.name}n.tokenLabel=r;function s(_){return _.name}n.tokenName=s;function o(_){return e.isString(_.LABEL)&&_.LABEL!==""}n.hasTokenLabel=o;var c="parent",l="categories",a="label",d="group",p="push_mode",f="pop_mode",m="longer_alt",g="line_breaks",y="start_chars_hint";function h(_){return u(_)}n.createToken=h;function u(_){var A=_.pattern,N={};if(N.name=_.name,e.isUndefined(A)||(N.PATTERN=A),e.has(_,c))throw`The parent property is no longer supported.
See: https://github.com/chevrotain/chevrotain/issues/564#issuecomment-349062346 for details.`;return e.has(_,l)&&(N.CATEGORIES=_[l]),i.augmentTokenTypes([N]),e.has(_,a)&&(N.LABEL=_[a]),e.has(_,d)&&(N.GROUP=_[d]),e.has(_,f)&&(N.POP_MODE=_[f]),e.has(_,p)&&(N.PUSH_MODE=_[p]),e.has(_,m)&&(N.LONGER_ALT=_[m]),e.has(_,g)&&(N.LINE_BREAKS=_[g]),e.has(_,y)&&(N.START_CHARS_HINT=_[y]),N}n.EOF=h({name:"EOF",pattern:t.Lexer.NA}),i.augmentTokenTypes([n.EOF]);function E(_,A,N,w,O,T,M,R){return{image:A,startOffset:N,endOffset:w,startLine:O,endLine:T,startColumn:M,endColumn:R,tokenTypeIdx:_.tokenTypeIdx,tokenType:_}}n.createTokenInstance=E;function x(_,A){return i.tokenStructuredMatcher(_,A)}n.tokenMatcher=x}),Zt=je(n=>{"use strict";var e=n&&n.__extends||(function(){var u=function(E,x){return u=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(_,A){_.__proto__=A}||function(_,A){for(var N in A)Object.prototype.hasOwnProperty.call(A,N)&&(_[N]=A[N])},u(E,x)};return function(E,x){if(typeof x!="function"&&x!==null)throw new TypeError("Class extends value "+String(x)+" is not a constructor or null");u(E,x);function _(){this.constructor=E}E.prototype=x===null?Object.create(x):(_.prototype=x.prototype,new _)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.serializeProduction=n.serializeGrammar=n.Terminal=n.Alternation=n.RepetitionWithSeparator=n.Repetition=n.RepetitionMandatoryWithSeparator=n.RepetitionMandatory=n.Option=n.Alternative=n.Rule=n.NonTerminal=n.AbstractProduction=void 0;var t=st(),i=Ei(),r=(function(){function u(E){this._definition=E}return Object.defineProperty(u.prototype,"definition",{get:function(){return this._definition},set:function(E){this._definition=E},enumerable:!1,configurable:!0}),u.prototype.accept=function(E){E.visit(this),t.forEach(this.definition,function(x){x.accept(E)})},u})();n.AbstractProduction=r;var s=(function(u){e(E,u);function E(x){var _=u.call(this,[])||this;return _.idx=1,t.assign(_,t.pick(x,function(A){return A!==void 0})),_}return Object.defineProperty(E.prototype,"definition",{get:function(){return this.referencedRule!==void 0?this.referencedRule.definition:[]},set:function(x){},enumerable:!1,configurable:!0}),E.prototype.accept=function(x){x.visit(this)},E})(r);n.NonTerminal=s;var o=(function(u){e(E,u);function E(x){var _=u.call(this,x.definition)||this;return _.orgText="",t.assign(_,t.pick(x,function(A){return A!==void 0})),_}return E})(r);n.Rule=o;var c=(function(u){e(E,u);function E(x){var _=u.call(this,x.definition)||this;return _.ignoreAmbiguities=!1,t.assign(_,t.pick(x,function(A){return A!==void 0})),_}return E})(r);n.Alternative=c;var l=(function(u){e(E,u);function E(x){var _=u.call(this,x.definition)||this;return _.idx=1,t.assign(_,t.pick(x,function(A){return A!==void 0})),_}return E})(r);n.Option=l;var a=(function(u){e(E,u);function E(x){var _=u.call(this,x.definition)||this;return _.idx=1,t.assign(_,t.pick(x,function(A){return A!==void 0})),_}return E})(r);n.RepetitionMandatory=a;var d=(function(u){e(E,u);function E(x){var _=u.call(this,x.definition)||this;return _.idx=1,t.assign(_,t.pick(x,function(A){return A!==void 0})),_}return E})(r);n.RepetitionMandatoryWithSeparator=d;var p=(function(u){e(E,u);function E(x){var _=u.call(this,x.definition)||this;return _.idx=1,t.assign(_,t.pick(x,function(A){return A!==void 0})),_}return E})(r);n.Repetition=p;var f=(function(u){e(E,u);function E(x){var _=u.call(this,x.definition)||this;return _.idx=1,t.assign(_,t.pick(x,function(A){return A!==void 0})),_}return E})(r);n.RepetitionWithSeparator=f;var m=(function(u){e(E,u);function E(x){var _=u.call(this,x.definition)||this;return _.idx=1,_.ignoreAmbiguities=!1,_.hasPredicates=!1,t.assign(_,t.pick(x,function(A){return A!==void 0})),_}return Object.defineProperty(E.prototype,"definition",{get:function(){return this._definition},set:function(x){this._definition=x},enumerable:!1,configurable:!0}),E})(r);n.Alternation=m;var g=(function(){function u(E){this.idx=1,t.assign(this,t.pick(E,function(x){return x!==void 0}))}return u.prototype.accept=function(E){E.visit(this)},u})();n.Terminal=g;function y(u){return t.map(u,h)}n.serializeGrammar=y;function h(u){function E(A){return t.map(A,h)}if(u instanceof s)return{type:"NonTerminal",name:u.nonTerminalName,idx:u.idx};if(u instanceof c)return{type:"Alternative",definition:E(u.definition)};if(u instanceof l)return{type:"Option",idx:u.idx,definition:E(u.definition)};if(u instanceof a)return{type:"RepetitionMandatory",idx:u.idx,definition:E(u.definition)};if(u instanceof d)return{type:"RepetitionMandatoryWithSeparator",idx:u.idx,separator:h(new g({terminalType:u.separator})),definition:E(u.definition)};if(u instanceof f)return{type:"RepetitionWithSeparator",idx:u.idx,separator:h(new g({terminalType:u.separator})),definition:E(u.definition)};if(u instanceof p)return{type:"Repetition",idx:u.idx,definition:E(u.definition)};if(u instanceof m)return{type:"Alternation",idx:u.idx,definition:E(u.definition)};if(u instanceof g){var x={type:"Terminal",name:u.terminalType.name,label:i.tokenLabel(u.terminalType),idx:u.idx},_=u.terminalType.PATTERN;return u.terminalType.PATTERN&&(x.pattern=t.isRegExp(_)?_.source:_),x}else{if(u instanceof o)return{type:"Rule",name:u.name,orgText:u.orgText,definition:E(u.definition)};throw Error("non exhaustive match")}}n.serializeProduction=h}),Cc=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.RestWalker=void 0;var e=st(),t=Zt(),i=(function(){function s(){}return s.prototype.walk=function(o,c){var l=this;c===void 0&&(c=[]),e.forEach(o.definition,function(a,d){var p=e.drop(o.definition,d+1);if(a instanceof t.NonTerminal)l.walkProdRef(a,p,c);else if(a instanceof t.Terminal)l.walkTerminal(a,p,c);else if(a instanceof t.Alternative)l.walkFlat(a,p,c);else if(a instanceof t.Option)l.walkOption(a,p,c);else if(a instanceof t.RepetitionMandatory)l.walkAtLeastOne(a,p,c);else if(a instanceof t.RepetitionMandatoryWithSeparator)l.walkAtLeastOneSep(a,p,c);else if(a instanceof t.RepetitionWithSeparator)l.walkManySep(a,p,c);else if(a instanceof t.Repetition)l.walkMany(a,p,c);else if(a instanceof t.Alternation)l.walkOr(a,p,c);else throw Error("non exhaustive match")})},s.prototype.walkTerminal=function(o,c,l){},s.prototype.walkProdRef=function(o,c,l){},s.prototype.walkFlat=function(o,c,l){var a=c.concat(l);this.walk(o,a)},s.prototype.walkOption=function(o,c,l){var a=c.concat(l);this.walk(o,a)},s.prototype.walkAtLeastOne=function(o,c,l){var a=[new t.Option({definition:o.definition})].concat(c,l);this.walk(o,a)},s.prototype.walkAtLeastOneSep=function(o,c,l){var a=r(o,c,l);this.walk(o,a)},s.prototype.walkMany=function(o,c,l){var a=[new t.Option({definition:o.definition})].concat(c,l);this.walk(o,a)},s.prototype.walkManySep=function(o,c,l){var a=r(o,c,l);this.walk(o,a)},s.prototype.walkOr=function(o,c,l){var a=this,d=c.concat(l);e.forEach(o.definition,function(p){var f=new t.Alternative({definition:[p]});a.walk(f,d)})},s})();n.RestWalker=i;function r(s,o,c){var l=[new t.Option({definition:[new t.Terminal({terminalType:s.separator})].concat(s.definition)})],a=l.concat(o,c);return a}}),Qr=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.GAstVisitor=void 0;var e=Zt(),t=(function(){function i(){}return i.prototype.visit=function(r){var s=r;switch(s.constructor){case e.NonTerminal:return this.visitNonTerminal(s);case e.Alternative:return this.visitAlternative(s);case e.Option:return this.visitOption(s);case e.RepetitionMandatory:return this.visitRepetitionMandatory(s);case e.RepetitionMandatoryWithSeparator:return this.visitRepetitionMandatoryWithSeparator(s);case e.RepetitionWithSeparator:return this.visitRepetitionWithSeparator(s);case e.Repetition:return this.visitRepetition(s);case e.Alternation:return this.visitAlternation(s);case e.Terminal:return this.visitTerminal(s);case e.Rule:return this.visitRule(s);default:throw Error("non exhaustive match")}},i.prototype.visitNonTerminal=function(r){},i.prototype.visitAlternative=function(r){},i.prototype.visitOption=function(r){},i.prototype.visitRepetition=function(r){},i.prototype.visitRepetitionMandatory=function(r){},i.prototype.visitRepetitionMandatoryWithSeparator=function(r){},i.prototype.visitRepetitionWithSeparator=function(r){},i.prototype.visitAlternation=function(r){},i.prototype.visitTerminal=function(r){},i.prototype.visitRule=function(r){},i})();n.GAstVisitor=t}),Jo=je(n=>{"use strict";var e=n&&n.__extends||(function(){var f=function(m,g){return f=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(y,h){y.__proto__=h}||function(y,h){for(var u in h)Object.prototype.hasOwnProperty.call(h,u)&&(y[u]=h[u])},f(m,g)};return function(m,g){if(typeof g!="function"&&g!==null)throw new TypeError("Class extends value "+String(g)+" is not a constructor or null");f(m,g);function y(){this.constructor=m}m.prototype=g===null?Object.create(g):(y.prototype=g.prototype,new y)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.collectMethods=n.DslMethodsCollectorVisitor=n.getProductionDslName=n.isBranchingProd=n.isOptionalProd=n.isSequenceProd=void 0;var t=st(),i=Zt(),r=Qr();function s(f){return f instanceof i.Alternative||f instanceof i.Option||f instanceof i.Repetition||f instanceof i.RepetitionMandatory||f instanceof i.RepetitionMandatoryWithSeparator||f instanceof i.RepetitionWithSeparator||f instanceof i.Terminal||f instanceof i.Rule}n.isSequenceProd=s;function o(f,m){m===void 0&&(m=[]);var g=f instanceof i.Option||f instanceof i.Repetition||f instanceof i.RepetitionWithSeparator;return g?!0:f instanceof i.Alternation?t.some(f.definition,function(y){return o(y,m)}):f instanceof i.NonTerminal&&t.contains(m,f)?!1:f instanceof i.AbstractProduction?(f instanceof i.NonTerminal&&m.push(f),t.every(f.definition,function(y){return o(y,m)})):!1}n.isOptionalProd=o;function c(f){return f instanceof i.Alternation}n.isBranchingProd=c;function l(f){if(f instanceof i.NonTerminal)return"SUBRULE";if(f instanceof i.Option)return"OPTION";if(f instanceof i.Alternation)return"OR";if(f instanceof i.RepetitionMandatory)return"AT_LEAST_ONE";if(f instanceof i.RepetitionMandatoryWithSeparator)return"AT_LEAST_ONE_SEP";if(f instanceof i.RepetitionWithSeparator)return"MANY_SEP";if(f instanceof i.Repetition)return"MANY";if(f instanceof i.Terminal)return"CONSUME";throw Error("non exhaustive match")}n.getProductionDslName=l;var a=(function(f){e(m,f);function m(){var g=f!==null&&f.apply(this,arguments)||this;return g.separator="-",g.dslMethods={option:[],alternation:[],repetition:[],repetitionWithSeparator:[],repetitionMandatory:[],repetitionMandatoryWithSeparator:[]},g}return m.prototype.reset=function(){this.dslMethods={option:[],alternation:[],repetition:[],repetitionWithSeparator:[],repetitionMandatory:[],repetitionMandatoryWithSeparator:[]}},m.prototype.visitTerminal=function(g){var y=g.terminalType.name+this.separator+"Terminal";t.has(this.dslMethods,y)||(this.dslMethods[y]=[]),this.dslMethods[y].push(g)},m.prototype.visitNonTerminal=function(g){var y=g.nonTerminalName+this.separator+"Terminal";t.has(this.dslMethods,y)||(this.dslMethods[y]=[]),this.dslMethods[y].push(g)},m.prototype.visitOption=function(g){this.dslMethods.option.push(g)},m.prototype.visitRepetitionWithSeparator=function(g){this.dslMethods.repetitionWithSeparator.push(g)},m.prototype.visitRepetitionMandatory=function(g){this.dslMethods.repetitionMandatory.push(g)},m.prototype.visitRepetitionMandatoryWithSeparator=function(g){this.dslMethods.repetitionMandatoryWithSeparator.push(g)},m.prototype.visitRepetition=function(g){this.dslMethods.repetition.push(g)},m.prototype.visitAlternation=function(g){this.dslMethods.alternation.push(g)},m})(r.GAstVisitor);n.DslMethodsCollectorVisitor=a;var d=new a;function p(f){d.reset(),f.accept(d);var m=d.dslMethods;return d.reset(),m}n.collectMethods=p}),Gu=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.firstForTerminal=n.firstForBranching=n.firstForSequence=n.first=void 0;var e=st(),t=Zt(),i=Jo();function r(l){if(l instanceof t.NonTerminal)return r(l.referencedRule);if(l instanceof t.Terminal)return c(l);if(i.isSequenceProd(l))return s(l);if(i.isBranchingProd(l))return o(l);throw Error("non exhaustive match")}n.first=r;function s(l){for(var a=[],d=l.definition,p=0,f=d.length>p,m,g=!0;f&&g;)m=d[p],g=i.isOptionalProd(m),a=a.concat(r(m)),p=p+1,f=d.length>p;return e.uniq(a)}n.firstForSequence=s;function o(l){var a=e.map(l.definition,function(d){return r(d)});return e.uniq(e.flatten(a))}n.firstForBranching=o;function c(l){return[l.terminalType]}n.firstForTerminal=c}),Hu=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.IN=void 0,n.IN="_~IN~_"}),o_=je(n=>{"use strict";var e=n&&n.__extends||(function(){var p=function(f,m){return p=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(g,y){g.__proto__=y}||function(g,y){for(var h in y)Object.prototype.hasOwnProperty.call(y,h)&&(g[h]=y[h])},p(f,m)};return function(f,m){if(typeof m!="function"&&m!==null)throw new TypeError("Class extends value "+String(m)+" is not a constructor or null");p(f,m);function g(){this.constructor=f}f.prototype=m===null?Object.create(m):(g.prototype=m.prototype,new g)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.buildInProdFollowPrefix=n.buildBetweenProdsFollowPrefix=n.computeAllProdsFollows=n.ResyncFollowsWalker=void 0;var t=Cc(),i=Gu(),r=st(),s=Hu(),o=Zt(),c=(function(p){e(f,p);function f(m){var g=p.call(this)||this;return g.topProd=m,g.follows={},g}return f.prototype.startWalking=function(){return this.walk(this.topProd),this.follows},f.prototype.walkTerminal=function(m,g,y){},f.prototype.walkProdRef=function(m,g,y){var h=a(m.referencedRule,m.idx)+this.topProd.name,u=g.concat(y),E=new o.Alternative({definition:u}),x=i.first(E);this.follows[h]=x},f})(t.RestWalker);n.ResyncFollowsWalker=c;function l(p){var f={};return r.forEach(p,function(m){var g=new c(m).startWalking();r.assign(f,g)}),f}n.computeAllProdsFollows=l;function a(p,f){return p.name+f+s.IN}n.buildBetweenProdsFollowPrefix=a;function d(p){var f=p.terminalType.name;return f+p.idx+s.IN}n.buildInProdFollowPrefix=d}),$o=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.defaultGrammarValidatorErrorProvider=n.defaultGrammarResolverErrorProvider=n.defaultParserErrorProvider=void 0;var e=Ei(),t=st(),i=st(),r=Zt(),s=Jo();n.defaultParserErrorProvider={buildMismatchTokenMessage:function(o){var c=o.expected,l=o.actual,a=o.previous,d=o.ruleName,p=e.hasTokenLabel(c),f=p?"--> "+e.tokenLabel(c)+" <--":"token of type --> "+c.name+" <--",m="Expecting "+f+" but found --> '"+l.image+"' <--";return m},buildNotAllInputParsedMessage:function(o){var c=o.firstRedundant,l=o.ruleName;return"Redundant input, expecting EOF but found: "+c.image},buildNoViableAltMessage:function(o){var c=o.expectedPathsPerAlt,l=o.actual,a=o.previous,d=o.customUserDescription,p=o.ruleName,f="Expecting: ",m=i.first(l).image,g=`
but found: '`+m+"'";if(d)return f+d+g;var y=i.reduce(c,function(x,_){return x.concat(_)},[]),h=i.map(y,function(x){return"["+i.map(x,function(_){return e.tokenLabel(_)}).join(", ")+"]"}),u=i.map(h,function(x,_){return"  "+(_+1)+". "+x}),E=`one of these possible Token sequences:
`+u.join(`
`);return f+E+g},buildEarlyExitMessage:function(o){var c=o.expectedIterationPaths,l=o.actual,a=o.customUserDescription,d=o.ruleName,p="Expecting: ",f=i.first(l).image,m=`
but found: '`+f+"'";if(a)return p+a+m;var g=i.map(c,function(h){return"["+i.map(h,function(u){return e.tokenLabel(u)}).join(",")+"]"}),y=`expecting at least one iteration which starts with one of these possible Token sequences::
  `+("<"+g.join(" ,")+">");return p+y+m}},Object.freeze(n.defaultParserErrorProvider),n.defaultGrammarResolverErrorProvider={buildRuleNotFoundError:function(o,c){var l="Invalid grammar, reference to a rule which is not defined: ->"+c.nonTerminalName+`<-
inside top level rule: ->`+o.name+"<-";return l}},n.defaultGrammarValidatorErrorProvider={buildDuplicateFoundError:function(o,c){function l(h){return h instanceof r.Terminal?h.terminalType.name:h instanceof r.NonTerminal?h.nonTerminalName:""}var a=o.name,d=i.first(c),p=d.idx,f=s.getProductionDslName(d),m=l(d),g=p>0,y="->"+f+(g?p:"")+"<- "+(m?"with argument: ->"+m+"<-":"")+`
                  appears more than once (`+c.length+" times) in the top level rule: ->"+a+`<-.
                  For further details see: https://chevrotain.io/docs/FAQ.html#NUMERICAL_SUFFIXES
                  `;return y=y.replace(/[ \t]+/g," "),y=y.replace(/\s\s+/g,`
`),y},buildNamespaceConflictError:function(o){var c=`Namespace conflict found in grammar.
`+("The grammar has both a Terminal(Token) and a Non-Terminal(Rule) named: <"+o.name+`>.
`)+`To resolve this make sure each Terminal and Non-Terminal names are unique
This is easy to accomplish by using the convention that Terminal names start with an uppercase letter
and Non-Terminal names start with a lower case letter.`;return c},buildAlternationPrefixAmbiguityError:function(o){var c=i.map(o.prefixPath,function(d){return e.tokenLabel(d)}).join(", "),l=o.alternation.idx===0?"":o.alternation.idx,a="Ambiguous alternatives: <"+o.ambiguityIndices.join(" ,")+`> due to common lookahead prefix
`+("in <OR"+l+"> inside <"+o.topLevelRule.name+`> Rule,
`)+("<"+c+`> may appears as a prefix path in all these alternatives.
`)+`See: https://chevrotain.io/docs/guide/resolving_grammar_errors.html#COMMON_PREFIX
For Further details.`;return a},buildAlternationAmbiguityError:function(o){var c=i.map(o.prefixPath,function(d){return e.tokenLabel(d)}).join(", "),l=o.alternation.idx===0?"":o.alternation.idx,a="Ambiguous Alternatives Detected: <"+o.ambiguityIndices.join(" ,")+"> in <OR"+l+">"+(" inside <"+o.topLevelRule.name+`> Rule,
`)+("<"+c+`> may appears as a prefix path in all these alternatives.
`);return a=a+`See: https://chevrotain.io/docs/guide/resolving_grammar_errors.html#AMBIGUOUS_ALTERNATIVES
For Further details.`,a},buildEmptyRepetitionError:function(o){var c=s.getProductionDslName(o.repetition);o.repetition.idx!==0&&(c+=o.repetition.idx);var l="The repetition <"+c+"> within Rule <"+o.topLevelRule.name+`> can never consume any tokens.
This could lead to an infinite loop.`;return l},buildTokenNameError:function(o){return"deprecated"},buildEmptyAlternationError:function(o){var c="Ambiguous empty alternative: <"+(o.emptyChoiceIdx+1)+">"+(" in <OR"+o.alternation.idx+"> inside <"+o.topLevelRule.name+`> Rule.
`)+"Only the last alternative may be an empty alternative.";return c},buildTooManyAlternativesError:function(o){var c=`An Alternation cannot have more than 256 alternatives:
`+("<OR"+o.alternation.idx+"> inside <"+o.topLevelRule.name+`> Rule.
 has `+(o.alternation.definition.length+1)+" alternatives.");return c},buildLeftRecursionError:function(o){var c=o.topLevelRule.name,l=t.map(o.leftRecursionPath,function(p){return p.name}),a=c+" --> "+l.concat([c]).join(" --> "),d=`Left Recursion found in grammar.
`+("rule: <"+c+`> can be invoked from itself (directly or indirectly)
`)+(`without consuming any Tokens. The grammar path that causes this is:
 `+a+`
`)+` To fix this refactor your grammar to remove the left recursion.
see: https://en.wikipedia.org/wiki/LL_parser#Left_Factoring.`;return d},buildInvalidRuleNameError:function(o){return"deprecated"},buildDuplicateRuleNameError:function(o){var c;o.topLevelRule instanceof r.Rule?c=o.topLevelRule.name:c=o.topLevelRule;var l="Duplicate definition, rule: ->"+c+"<- is already defined in the grammar: ->"+o.grammarName+"<-";return l}}}),a_=je(n=>{"use strict";var e=n&&n.__extends||(function(){var c=function(l,a){return c=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(d,p){d.__proto__=p}||function(d,p){for(var f in p)Object.prototype.hasOwnProperty.call(p,f)&&(d[f]=p[f])},c(l,a)};return function(l,a){if(typeof a!="function"&&a!==null)throw new TypeError("Class extends value "+String(a)+" is not a constructor or null");c(l,a);function d(){this.constructor=l}l.prototype=a===null?Object.create(a):(d.prototype=a.prototype,new d)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.GastRefResolverVisitor=n.resolveGrammar=void 0;var t=nn(),i=st(),r=Qr();function s(c,l){var a=new o(c,l);return a.resolveRefs(),a.errors}n.resolveGrammar=s;var o=(function(c){e(l,c);function l(a,d){var p=c.call(this)||this;return p.nameToTopRule=a,p.errMsgProvider=d,p.errors=[],p}return l.prototype.resolveRefs=function(){var a=this;i.forEach(i.values(this.nameToTopRule),function(d){a.currTopLevel=d,d.accept(a)})},l.prototype.visitNonTerminal=function(a){var d=this.nameToTopRule[a.nonTerminalName];if(d)a.referencedRule=d;else{var p=this.errMsgProvider.buildRuleNotFoundError(this.currTopLevel,a);this.errors.push({message:p,type:t.ParserDefinitionErrorType.UNRESOLVED_SUBRULE_REF,ruleName:this.currTopLevel.name,unresolvedRefName:a.nonTerminalName})}},l})(r.GAstVisitor);n.GastRefResolverVisitor=o}),Qo=je(n=>{"use strict";var e=n&&n.__extends||(function(){var h=function(u,E){return h=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(x,_){x.__proto__=_}||function(x,_){for(var A in _)Object.prototype.hasOwnProperty.call(_,A)&&(x[A]=_[A])},h(u,E)};return function(u,E){if(typeof E!="function"&&E!==null)throw new TypeError("Class extends value "+String(E)+" is not a constructor or null");h(u,E);function x(){this.constructor=u}u.prototype=E===null?Object.create(E):(x.prototype=E.prototype,new x)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.nextPossibleTokensAfter=n.possiblePathsFrom=n.NextTerminalAfterAtLeastOneSepWalker=n.NextTerminalAfterAtLeastOneWalker=n.NextTerminalAfterManySepWalker=n.NextTerminalAfterManyWalker=n.AbstractNextTerminalAfterProductionWalker=n.NextAfterTokenWalker=n.AbstractNextPossibleTokensWalker=void 0;var t=Cc(),i=st(),r=Gu(),s=Zt(),o=(function(h){e(u,h);function u(E,x){var _=h.call(this)||this;return _.topProd=E,_.path=x,_.possibleTokTypes=[],_.nextProductionName="",_.nextProductionOccurrence=0,_.found=!1,_.isAtEndOfPath=!1,_}return u.prototype.startWalking=function(){if(this.found=!1,this.path.ruleStack[0]!==this.topProd.name)throw Error("The path does not start with the walker's top Rule!");return this.ruleStack=i.cloneArr(this.path.ruleStack).reverse(),this.occurrenceStack=i.cloneArr(this.path.occurrenceStack).reverse(),this.ruleStack.pop(),this.occurrenceStack.pop(),this.updateExpectedNext(),this.walk(this.topProd),this.possibleTokTypes},u.prototype.walk=function(E,x){x===void 0&&(x=[]),this.found||h.prototype.walk.call(this,E,x)},u.prototype.walkProdRef=function(E,x,_){if(E.referencedRule.name===this.nextProductionName&&E.idx===this.nextProductionOccurrence){var A=x.concat(_);this.updateExpectedNext(),this.walk(E.referencedRule,A)}},u.prototype.updateExpectedNext=function(){i.isEmpty(this.ruleStack)?(this.nextProductionName="",this.nextProductionOccurrence=0,this.isAtEndOfPath=!0):(this.nextProductionName=this.ruleStack.pop(),this.nextProductionOccurrence=this.occurrenceStack.pop())},u})(t.RestWalker);n.AbstractNextPossibleTokensWalker=o;var c=(function(h){e(u,h);function u(E,x){var _=h.call(this,E,x)||this;return _.path=x,_.nextTerminalName="",_.nextTerminalOccurrence=0,_.nextTerminalName=_.path.lastTok.name,_.nextTerminalOccurrence=_.path.lastTokOccurrence,_}return u.prototype.walkTerminal=function(E,x,_){if(this.isAtEndOfPath&&E.terminalType.name===this.nextTerminalName&&E.idx===this.nextTerminalOccurrence&&!this.found){var A=x.concat(_),N=new s.Alternative({definition:A});this.possibleTokTypes=r.first(N),this.found=!0}},u})(o);n.NextAfterTokenWalker=c;var l=(function(h){e(u,h);function u(E,x){var _=h.call(this)||this;return _.topRule=E,_.occurrence=x,_.result={token:void 0,occurrence:void 0,isEndOfRule:void 0},_}return u.prototype.startWalking=function(){return this.walk(this.topRule),this.result},u})(t.RestWalker);n.AbstractNextTerminalAfterProductionWalker=l;var a=(function(h){e(u,h);function u(){return h!==null&&h.apply(this,arguments)||this}return u.prototype.walkMany=function(E,x,_){if(E.idx===this.occurrence){var A=i.first(x.concat(_));this.result.isEndOfRule=A===void 0,A instanceof s.Terminal&&(this.result.token=A.terminalType,this.result.occurrence=A.idx)}else h.prototype.walkMany.call(this,E,x,_)},u})(l);n.NextTerminalAfterManyWalker=a;var d=(function(h){e(u,h);function u(){return h!==null&&h.apply(this,arguments)||this}return u.prototype.walkManySep=function(E,x,_){if(E.idx===this.occurrence){var A=i.first(x.concat(_));this.result.isEndOfRule=A===void 0,A instanceof s.Terminal&&(this.result.token=A.terminalType,this.result.occurrence=A.idx)}else h.prototype.walkManySep.call(this,E,x,_)},u})(l);n.NextTerminalAfterManySepWalker=d;var p=(function(h){e(u,h);function u(){return h!==null&&h.apply(this,arguments)||this}return u.prototype.walkAtLeastOne=function(E,x,_){if(E.idx===this.occurrence){var A=i.first(x.concat(_));this.result.isEndOfRule=A===void 0,A instanceof s.Terminal&&(this.result.token=A.terminalType,this.result.occurrence=A.idx)}else h.prototype.walkAtLeastOne.call(this,E,x,_)},u})(l);n.NextTerminalAfterAtLeastOneWalker=p;var f=(function(h){e(u,h);function u(){return h!==null&&h.apply(this,arguments)||this}return u.prototype.walkAtLeastOneSep=function(E,x,_){if(E.idx===this.occurrence){var A=i.first(x.concat(_));this.result.isEndOfRule=A===void 0,A instanceof s.Terminal&&(this.result.token=A.terminalType,this.result.occurrence=A.idx)}else h.prototype.walkAtLeastOneSep.call(this,E,x,_)},u})(l);n.NextTerminalAfterAtLeastOneSepWalker=f;function m(h,u,E){E===void 0&&(E=[]),E=i.cloneArr(E);var x=[],_=0;function A(T){return T.concat(i.drop(h,_+1))}function N(T){var M=m(A(T),u,E);return x.concat(M)}for(;E.length<u&&_<h.length;){var w=h[_];if(w instanceof s.Alternative||w instanceof s.NonTerminal)return N(w.definition);if(w instanceof s.Option)x=N(w.definition);else if(w instanceof s.RepetitionMandatory){var O=w.definition.concat([new s.Repetition({definition:w.definition})]);return N(O)}else if(w instanceof s.RepetitionMandatoryWithSeparator){var O=[new s.Alternative({definition:w.definition}),new s.Repetition({definition:[new s.Terminal({terminalType:w.separator})].concat(w.definition)})];return N(O)}else if(w instanceof s.RepetitionWithSeparator){var O=w.definition.concat([new s.Repetition({definition:[new s.Terminal({terminalType:w.separator})].concat(w.definition)})]);x=N(O)}else if(w instanceof s.Repetition){var O=w.definition.concat([new s.Repetition({definition:w.definition})]);x=N(O)}else{if(w instanceof s.Alternation)return i.forEach(w.definition,function(T){i.isEmpty(T.definition)===!1&&(x=N(T.definition))}),x;if(w instanceof s.Terminal)E.push(w.terminalType);else throw Error("non exhaustive match")}_++}return x.push({partialPath:E,suffixDef:i.drop(h,_)}),x}n.possiblePathsFrom=m;function g(h,u,E,x){var _="EXIT_NONE_TERMINAL",A=[_],N="EXIT_ALTERNATIVE",w=!1,O=u.length,T=O-x-1,M=[],R=[];for(R.push({idx:-1,def:h,ruleStack:[],occurrenceStack:[]});!i.isEmpty(R);){var I=R.pop();if(I===N){w&&i.last(R).idx<=T&&R.pop();continue}var U=I.def,P=I.idx,X=I.ruleStack,W=I.occurrenceStack;if(!i.isEmpty(U)){var q=U[0];if(q===_){var G={idx:P,def:i.drop(U),ruleStack:i.dropRight(X),occurrenceStack:i.dropRight(W)};R.push(G)}else if(q instanceof s.Terminal)if(P<O-1){var ee=P+1,ae=u[ee];if(E(ae,q.terminalType)){var G={idx:ee,def:i.drop(U),ruleStack:X,occurrenceStack:W};R.push(G)}}else if(P===O-1)M.push({nextTokenType:q.terminalType,nextTokenOccurrence:q.idx,ruleStack:X,occurrenceStack:W}),w=!0;else throw Error("non exhaustive match");else if(q instanceof s.NonTerminal){var ue=i.cloneArr(X);ue.push(q.nonTerminalName);var _e=i.cloneArr(W);_e.push(q.idx);var G={idx:P,def:q.definition.concat(A,i.drop(U)),ruleStack:ue,occurrenceStack:_e};R.push(G)}else if(q instanceof s.Option){var me={idx:P,def:i.drop(U),ruleStack:X,occurrenceStack:W};R.push(me),R.push(N);var Me={idx:P,def:q.definition.concat(i.drop(U)),ruleStack:X,occurrenceStack:W};R.push(Me)}else if(q instanceof s.RepetitionMandatory){var k=new s.Repetition({definition:q.definition,idx:q.idx}),Y=q.definition.concat([k],i.drop(U)),G={idx:P,def:Y,ruleStack:X,occurrenceStack:W};R.push(G)}else if(q instanceof s.RepetitionMandatoryWithSeparator){var K=new s.Terminal({terminalType:q.separator}),k=new s.Repetition({definition:[K].concat(q.definition),idx:q.idx}),Y=q.definition.concat([k],i.drop(U)),G={idx:P,def:Y,ruleStack:X,occurrenceStack:W};R.push(G)}else if(q instanceof s.RepetitionWithSeparator){var me={idx:P,def:i.drop(U),ruleStack:X,occurrenceStack:W};R.push(me),R.push(N);var K=new s.Terminal({terminalType:q.separator}),ne=new s.Repetition({definition:[K].concat(q.definition),idx:q.idx}),Y=q.definition.concat([ne],i.drop(U)),Me={idx:P,def:Y,ruleStack:X,occurrenceStack:W};R.push(Me)}else if(q instanceof s.Repetition){var me={idx:P,def:i.drop(U),ruleStack:X,occurrenceStack:W};R.push(me),R.push(N);var ne=new s.Repetition({definition:q.definition,idx:q.idx}),Y=q.definition.concat([ne],i.drop(U)),Me={idx:P,def:Y,ruleStack:X,occurrenceStack:W};R.push(Me)}else if(q instanceof s.Alternation)for(var ie=q.definition.length-1;ie>=0;ie--){var de=q.definition[ie],Le={idx:P,def:de.definition.concat(i.drop(U)),ruleStack:X,occurrenceStack:W};R.push(Le),R.push(N)}else if(q instanceof s.Alternative)R.push({idx:P,def:q.definition.concat(i.drop(U)),ruleStack:X,occurrenceStack:W});else if(q instanceof s.Rule)R.push(y(q,P,X,W));else throw Error("non exhaustive match")}}return M}n.nextPossibleTokensAfter=g;function y(h,u,E,x){var _=i.cloneArr(E);_.push(h.name);var A=i.cloneArr(x);return A.push(1),{idx:u,def:h.definition,ruleStack:_,occurrenceStack:A}}}),ea=je(n=>{"use strict";var e=n&&n.__extends||(function(){var T=function(M,R){return T=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(I,U){I.__proto__=U}||function(I,U){for(var P in U)Object.prototype.hasOwnProperty.call(U,P)&&(I[P]=U[P])},T(M,R)};return function(M,R){if(typeof R!="function"&&R!==null)throw new TypeError("Class extends value "+String(R)+" is not a constructor or null");T(M,R);function I(){this.constructor=M}M.prototype=R===null?Object.create(R):(I.prototype=R.prototype,new I)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.areTokenCategoriesNotUsed=n.isStrictPrefixOfPath=n.containsPath=n.getLookaheadPathsForOptionalProd=n.getLookaheadPathsForOr=n.lookAheadSequenceFromAlternatives=n.buildSingleAlternativeLookaheadFunction=n.buildAlternativesLookAheadFunc=n.buildLookaheadFuncForOptionalProd=n.buildLookaheadFuncForOr=n.getProdType=n.PROD_TYPE=void 0;var t=st(),i=Qo(),r=Cc(),s=$r(),o=Zt(),c=Qr(),l;(function(T){T[T.OPTION=0]="OPTION",T[T.REPETITION=1]="REPETITION",T[T.REPETITION_MANDATORY=2]="REPETITION_MANDATORY",T[T.REPETITION_MANDATORY_WITH_SEPARATOR=3]="REPETITION_MANDATORY_WITH_SEPARATOR",T[T.REPETITION_WITH_SEPARATOR=4]="REPETITION_WITH_SEPARATOR",T[T.ALTERNATION=5]="ALTERNATION"})(l=n.PROD_TYPE||(n.PROD_TYPE={}));function a(T){if(T instanceof o.Option)return l.OPTION;if(T instanceof o.Repetition)return l.REPETITION;if(T instanceof o.RepetitionMandatory)return l.REPETITION_MANDATORY;if(T instanceof o.RepetitionMandatoryWithSeparator)return l.REPETITION_MANDATORY_WITH_SEPARATOR;if(T instanceof o.RepetitionWithSeparator)return l.REPETITION_WITH_SEPARATOR;if(T instanceof o.Alternation)return l.ALTERNATION;throw Error("non exhaustive match")}n.getProdType=a;function d(T,M,R,I,U,P){var X=_(T,M,R),W=O(X)?s.tokenStructuredMatcherNoCategories:s.tokenStructuredMatcher;return P(X,I,W,U)}n.buildLookaheadFuncForOr=d;function p(T,M,R,I,U,P){var X=A(T,M,U,R),W=O(X)?s.tokenStructuredMatcherNoCategories:s.tokenStructuredMatcher;return P(X[0],W,I)}n.buildLookaheadFuncForOptionalProd=p;function f(T,M,R,I){var U=T.length,P=t.every(T,function(q){return t.every(q,function(G){return G.length===1})});if(M)return function(q){for(var G=t.map(q,function(ne){return ne.GATE}),ee=0;ee<U;ee++){var ae=T[ee],ue=ae.length,_e=G[ee];if(!(_e!==void 0&&_e.call(this)===!1))e:for(var me=0;me<ue;me++){for(var Me=ae[me],k=Me.length,Y=0;Y<k;Y++){var K=this.LA(Y+1);if(R(K,Me[Y])===!1)continue e}return ee}}};if(P&&!I){var X=t.map(T,function(q){return t.flatten(q)}),W=t.reduce(X,function(q,G,ee){return t.forEach(G,function(ae){t.has(q,ae.tokenTypeIdx)||(q[ae.tokenTypeIdx]=ee),t.forEach(ae.categoryMatches,function(ue){t.has(q,ue)||(q[ue]=ee)})}),q},[]);return function(){var q=this.LA(1);return W[q.tokenTypeIdx]}}else return function(){for(var q=0;q<U;q++){var G=T[q],ee=G.length;e:for(var ae=0;ae<ee;ae++){for(var ue=G[ae],_e=ue.length,me=0;me<_e;me++){var Me=this.LA(me+1);if(R(Me,ue[me])===!1)continue e}return q}}}}n.buildAlternativesLookAheadFunc=f;function m(T,M,R){var I=t.every(T,function(G){return G.length===1}),U=T.length;if(I&&!R){var P=t.flatten(T);if(P.length===1&&t.isEmpty(P[0].categoryMatches)){var X=P[0],W=X.tokenTypeIdx;return function(){return this.LA(1).tokenTypeIdx===W}}else{var q=t.reduce(P,function(G,ee,ae){return G[ee.tokenTypeIdx]=!0,t.forEach(ee.categoryMatches,function(ue){G[ue]=!0}),G},[]);return function(){var G=this.LA(1);return q[G.tokenTypeIdx]===!0}}}else return function(){e:for(var G=0;G<U;G++){for(var ee=T[G],ae=ee.length,ue=0;ue<ae;ue++){var _e=this.LA(ue+1);if(M(_e,ee[ue])===!1)continue e}return!0}return!1}}n.buildSingleAlternativeLookaheadFunction=m;var g=(function(T){e(M,T);function M(R,I,U){var P=T.call(this)||this;return P.topProd=R,P.targetOccurrence=I,P.targetProdType=U,P}return M.prototype.startWalking=function(){return this.walk(this.topProd),this.restDef},M.prototype.checkIsTarget=function(R,I,U,P){return R.idx===this.targetOccurrence&&this.targetProdType===I?(this.restDef=U.concat(P),!0):!1},M.prototype.walkOption=function(R,I,U){this.checkIsTarget(R,l.OPTION,I,U)||T.prototype.walkOption.call(this,R,I,U)},M.prototype.walkAtLeastOne=function(R,I,U){this.checkIsTarget(R,l.REPETITION_MANDATORY,I,U)||T.prototype.walkOption.call(this,R,I,U)},M.prototype.walkAtLeastOneSep=function(R,I,U){this.checkIsTarget(R,l.REPETITION_MANDATORY_WITH_SEPARATOR,I,U)||T.prototype.walkOption.call(this,R,I,U)},M.prototype.walkMany=function(R,I,U){this.checkIsTarget(R,l.REPETITION,I,U)||T.prototype.walkOption.call(this,R,I,U)},M.prototype.walkManySep=function(R,I,U){this.checkIsTarget(R,l.REPETITION_WITH_SEPARATOR,I,U)||T.prototype.walkOption.call(this,R,I,U)},M})(r.RestWalker),y=(function(T){e(M,T);function M(R,I,U){var P=T.call(this)||this;return P.targetOccurrence=R,P.targetProdType=I,P.targetRef=U,P.result=[],P}return M.prototype.checkIsTarget=function(R,I){R.idx===this.targetOccurrence&&this.targetProdType===I&&(this.targetRef===void 0||R===this.targetRef)&&(this.result=R.definition)},M.prototype.visitOption=function(R){this.checkIsTarget(R,l.OPTION)},M.prototype.visitRepetition=function(R){this.checkIsTarget(R,l.REPETITION)},M.prototype.visitRepetitionMandatory=function(R){this.checkIsTarget(R,l.REPETITION_MANDATORY)},M.prototype.visitRepetitionMandatoryWithSeparator=function(R){this.checkIsTarget(R,l.REPETITION_MANDATORY_WITH_SEPARATOR)},M.prototype.visitRepetitionWithSeparator=function(R){this.checkIsTarget(R,l.REPETITION_WITH_SEPARATOR)},M.prototype.visitAlternation=function(R){this.checkIsTarget(R,l.ALTERNATION)},M})(c.GAstVisitor);function h(T){for(var M=new Array(T),R=0;R<T;R++)M[R]=[];return M}function u(T){for(var M=[""],R=0;R<T.length;R++){for(var I=T[R],U=[],P=0;P<M.length;P++){var X=M[P];U.push(X+"_"+I.tokenTypeIdx);for(var W=0;W<I.categoryMatches.length;W++){var q="_"+I.categoryMatches[W];U.push(X+q)}}M=U}return M}function E(T,M,R){for(var I=0;I<T.length;I++)if(I!==R)for(var U=T[I],P=0;P<M.length;P++){var X=M[P];if(U[X]===!0)return!1}return!0}function x(T,M){for(var R=t.map(T,function(ee){return i.possiblePathsFrom([ee],1)}),I=h(R.length),U=t.map(R,function(ee){var ae={};return t.forEach(ee,function(ue){var _e=u(ue.partialPath);t.forEach(_e,function(me){ae[me]=!0})}),ae}),P=R,X=1;X<=M;X++){var W=P;P=h(W.length);for(var q=function(ee){for(var ae=W[ee],ue=0;ue<ae.length;ue++){var _e=ae[ue].partialPath,me=ae[ue].suffixDef,Me=u(_e),k=E(U,Me,ee);if(k||t.isEmpty(me)||_e.length===M){var Y=I[ee];if(N(Y,_e)===!1){Y.push(_e);for(var K=0;K<Me.length;K++){var ne=Me[K];U[ee][ne]=!0}}}else{var ie=i.possiblePathsFrom(me,X+1,_e);P[ee]=P[ee].concat(ie),t.forEach(ie,function(de){var Le=u(de.partialPath);t.forEach(Le,function(we){U[ee][we]=!0})})}}},G=0;G<W.length;G++)q(G)}return I}n.lookAheadSequenceFromAlternatives=x;function _(T,M,R,I){var U=new y(T,l.ALTERNATION,I);return M.accept(U),x(U.result,R)}n.getLookaheadPathsForOr=_;function A(T,M,R,I){var U=new y(T,R);M.accept(U);var P=U.result,X=new g(M,T,R),W=X.startWalking(),q=new o.Alternative({definition:P}),G=new o.Alternative({definition:W});return x([q,G],I)}n.getLookaheadPathsForOptionalProd=A;function N(T,M){e:for(var R=0;R<T.length;R++){var I=T[R];if(I.length===M.length){for(var U=0;U<I.length;U++){var P=M[U],X=I[U],W=P===X||X.categoryMatchesMap[P.tokenTypeIdx]!==void 0;if(W===!1)continue e}return!0}}return!1}n.containsPath=N;function w(T,M){return T.length<M.length&&t.every(T,function(R,I){var U=M[I];return R===U||U.categoryMatchesMap[R.tokenTypeIdx]})}n.isStrictPrefixOfPath=w;function O(T){return t.every(T,function(M){return t.every(M,function(R){return t.every(R,function(I){return t.isEmpty(I.categoryMatches)})})})}n.areTokenCategoriesNotUsed=O}),Wu=je(n=>{"use strict";var e=n&&n.__extends||(function(){var I=function(U,P){return I=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(X,W){X.__proto__=W}||function(X,W){for(var q in W)Object.prototype.hasOwnProperty.call(W,q)&&(X[q]=W[q])},I(U,P)};return function(U,P){if(typeof P!="function"&&P!==null)throw new TypeError("Class extends value "+String(P)+" is not a constructor or null");I(U,P);function X(){this.constructor=U}U.prototype=P===null?Object.create(P):(X.prototype=P.prototype,new X)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.checkPrefixAlternativesAmbiguities=n.validateSomeNonEmptyLookaheadPath=n.validateTooManyAlts=n.RepetionCollector=n.validateAmbiguousAlternationAlternatives=n.validateEmptyOrAlternative=n.getFirstNoneTerminal=n.validateNoLeftRecursion=n.validateRuleIsOverridden=n.validateRuleDoesNotAlreadyExist=n.OccurrenceValidationCollector=n.identifyProductionForDuplicates=n.validateGrammar=void 0;var t=st(),i=st(),r=nn(),s=Jo(),o=ea(),c=Qo(),l=Zt(),a=Qr();function d(I,U,P,X,W){var q=t.map(I,function(k){return p(k,X)}),G=t.map(I,function(k){return u(k,k,X)}),ee=[],ae=[],ue=[];i.every(G,i.isEmpty)&&(ee=i.map(I,function(k){return _(k,X)}),ae=i.map(I,function(k){return A(k,U,X)}),ue=O(I,U,X));var _e=R(I,P,X),me=i.map(I,function(k){return w(k,X)}),Me=i.map(I,function(k){return y(k,I,W,X)});return t.flatten(q.concat(ue,G,ee,ae,_e,me,Me))}n.validateGrammar=d;function p(I,U){var P=new g;I.accept(P);var X=P.allProductions,W=t.groupBy(X,f),q=t.pick(W,function(ee){return ee.length>1}),G=t.map(t.values(q),function(ee){var ae=t.first(ee),ue=U.buildDuplicateFoundError(I,ee),_e=s.getProductionDslName(ae),me={message:ue,type:r.ParserDefinitionErrorType.DUPLICATE_PRODUCTIONS,ruleName:I.name,dslName:_e,occurrence:ae.idx},Me=m(ae);return Me&&(me.parameter=Me),me});return G}function f(I){return s.getProductionDslName(I)+"_#_"+I.idx+"_#_"+m(I)}n.identifyProductionForDuplicates=f;function m(I){return I instanceof l.Terminal?I.terminalType.name:I instanceof l.NonTerminal?I.nonTerminalName:""}var g=(function(I){e(U,I);function U(){var P=I!==null&&I.apply(this,arguments)||this;return P.allProductions=[],P}return U.prototype.visitNonTerminal=function(P){this.allProductions.push(P)},U.prototype.visitOption=function(P){this.allProductions.push(P)},U.prototype.visitRepetitionWithSeparator=function(P){this.allProductions.push(P)},U.prototype.visitRepetitionMandatory=function(P){this.allProductions.push(P)},U.prototype.visitRepetitionMandatoryWithSeparator=function(P){this.allProductions.push(P)},U.prototype.visitRepetition=function(P){this.allProductions.push(P)},U.prototype.visitAlternation=function(P){this.allProductions.push(P)},U.prototype.visitTerminal=function(P){this.allProductions.push(P)},U})(a.GAstVisitor);n.OccurrenceValidationCollector=g;function y(I,U,P,X){var W=[],q=i.reduce(U,function(ee,ae){return ae.name===I.name?ee+1:ee},0);if(q>1){var G=X.buildDuplicateRuleNameError({topLevelRule:I,grammarName:P});W.push({message:G,type:r.ParserDefinitionErrorType.DUPLICATE_RULE_NAME,ruleName:I.name})}return W}n.validateRuleDoesNotAlreadyExist=y;function h(I,U,P){var X=[],W;return t.contains(U,I)||(W="Invalid rule override, rule: ->"+I+"<- cannot be overridden in the grammar: ->"+P+"<-as it is not defined in any of the super grammars ",X.push({message:W,type:r.ParserDefinitionErrorType.INVALID_RULE_OVERRIDE,ruleName:I})),X}n.validateRuleIsOverridden=h;function u(I,U,P,X){X===void 0&&(X=[]);var W=[],q=E(U.definition);if(t.isEmpty(q))return[];var G=I.name,ee=t.contains(q,I);ee&&W.push({message:P.buildLeftRecursionError({topLevelRule:I,leftRecursionPath:X}),type:r.ParserDefinitionErrorType.LEFT_RECURSION,ruleName:G});var ae=t.difference(q,X.concat([I])),ue=t.map(ae,function(_e){var me=t.cloneArr(X);return me.push(_e),u(I,_e,P,me)});return W.concat(t.flatten(ue))}n.validateNoLeftRecursion=u;function E(I){var U=[];if(t.isEmpty(I))return U;var P=t.first(I);if(P instanceof l.NonTerminal)U.push(P.referencedRule);else if(P instanceof l.Alternative||P instanceof l.Option||P instanceof l.RepetitionMandatory||P instanceof l.RepetitionMandatoryWithSeparator||P instanceof l.RepetitionWithSeparator||P instanceof l.Repetition)U=U.concat(E(P.definition));else if(P instanceof l.Alternation)U=t.flatten(t.map(P.definition,function(G){return E(G.definition)}));else if(!(P instanceof l.Terminal))throw Error("non exhaustive match");var X=s.isOptionalProd(P),W=I.length>1;if(X&&W){var q=t.drop(I);return U.concat(E(q))}else return U}n.getFirstNoneTerminal=E;var x=(function(I){e(U,I);function U(){var P=I!==null&&I.apply(this,arguments)||this;return P.alternations=[],P}return U.prototype.visitAlternation=function(P){this.alternations.push(P)},U})(a.GAstVisitor);function _(I,U){var P=new x;I.accept(P);var X=P.alternations,W=t.reduce(X,function(q,G){var ee=t.dropRight(G.definition),ae=t.map(ee,function(ue,_e){var me=c.nextPossibleTokensAfter([ue],[],null,1);return t.isEmpty(me)?{message:U.buildEmptyAlternationError({topLevelRule:I,alternation:G,emptyChoiceIdx:_e}),type:r.ParserDefinitionErrorType.NONE_LAST_EMPTY_ALT,ruleName:I.name,occurrence:G.idx,alternative:_e+1}:null});return q.concat(t.compact(ae))},[]);return W}n.validateEmptyOrAlternative=_;function A(I,U,P){var X=new x;I.accept(X);var W=X.alternations;W=i.reject(W,function(G){return G.ignoreAmbiguities===!0});var q=t.reduce(W,function(G,ee){var ae=ee.idx,ue=ee.maxLookahead||U,_e=o.getLookaheadPathsForOr(ae,I,ue,ee),me=T(_e,ee,I,P),Me=M(_e,ee,I,P);return G.concat(me,Me)},[]);return q}n.validateAmbiguousAlternationAlternatives=A;var N=(function(I){e(U,I);function U(){var P=I!==null&&I.apply(this,arguments)||this;return P.allProductions=[],P}return U.prototype.visitRepetitionWithSeparator=function(P){this.allProductions.push(P)},U.prototype.visitRepetitionMandatory=function(P){this.allProductions.push(P)},U.prototype.visitRepetitionMandatoryWithSeparator=function(P){this.allProductions.push(P)},U.prototype.visitRepetition=function(P){this.allProductions.push(P)},U})(a.GAstVisitor);n.RepetionCollector=N;function w(I,U){var P=new x;I.accept(P);var X=P.alternations,W=t.reduce(X,function(q,G){return G.definition.length>255&&q.push({message:U.buildTooManyAlternativesError({topLevelRule:I,alternation:G}),type:r.ParserDefinitionErrorType.TOO_MANY_ALTS,ruleName:I.name,occurrence:G.idx}),q},[]);return W}n.validateTooManyAlts=w;function O(I,U,P){var X=[];return i.forEach(I,function(W){var q=new N;W.accept(q);var G=q.allProductions;i.forEach(G,function(ee){var ae=o.getProdType(ee),ue=ee.maxLookahead||U,_e=ee.idx,me=o.getLookaheadPathsForOptionalProd(_e,W,ae,ue),Me=me[0];if(i.isEmpty(i.flatten(Me))){var k=P.buildEmptyRepetitionError({topLevelRule:W,repetition:ee});X.push({message:k,type:r.ParserDefinitionErrorType.NO_NON_EMPTY_LOOKAHEAD,ruleName:W.name})}})}),X}n.validateSomeNonEmptyLookaheadPath=O;function T(I,U,P,X){var W=[],q=i.reduce(I,function(ee,ae,ue){return U.definition[ue].ignoreAmbiguities===!0||i.forEach(ae,function(_e){var me=[ue];i.forEach(I,function(Me,k){ue!==k&&o.containsPath(Me,_e)&&U.definition[k].ignoreAmbiguities!==!0&&me.push(k)}),me.length>1&&!o.containsPath(W,_e)&&(W.push(_e),ee.push({alts:me,path:_e}))}),ee},[]),G=t.map(q,function(ee){var ae=i.map(ee.alts,function(_e){return _e+1}),ue=X.buildAlternationAmbiguityError({topLevelRule:P,alternation:U,ambiguityIndices:ae,prefixPath:ee.path});return{message:ue,type:r.ParserDefinitionErrorType.AMBIGUOUS_ALTS,ruleName:P.name,occurrence:U.idx,alternatives:[ee.alts]}});return G}function M(I,U,P,X){var W=[],q=i.reduce(I,function(G,ee,ae){var ue=i.map(ee,function(_e){return{idx:ae,path:_e}});return G.concat(ue)},[]);return i.forEach(q,function(G){var ee=U.definition[G.idx];if(ee.ignoreAmbiguities!==!0){var ae=G.idx,ue=G.path,_e=i.findAll(q,function(Me){return U.definition[Me.idx].ignoreAmbiguities!==!0&&Me.idx<ae&&o.isStrictPrefixOfPath(Me.path,ue)}),me=i.map(_e,function(Me){var k=[Me.idx+1,ae+1],Y=U.idx===0?"":U.idx,K=X.buildAlternationPrefixAmbiguityError({topLevelRule:P,alternation:U,ambiguityIndices:k,prefixPath:Me.path});return{message:K,type:r.ParserDefinitionErrorType.AMBIGUOUS_PREFIX_ALTS,ruleName:P.name,occurrence:Y,alternatives:k}});W=W.concat(me)}}),W}n.checkPrefixAlternativesAmbiguities=M;function R(I,U,P){var X=[],W=i.map(U,function(q){return q.name});return i.forEach(I,function(q){var G=q.name;if(i.contains(W,G)){var ee=P.buildNamespaceConflictError(q);X.push({message:ee,type:r.ParserDefinitionErrorType.CONFLICT_TOKENS_RULES_NAMESPACE,ruleName:G})}}),X}}),c_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.validateGrammar=n.resolveGrammar=void 0;var e=st(),t=a_(),i=Wu(),r=$o();function s(c){c=e.defaults(c,{errMsgProvider:r.defaultGrammarResolverErrorProvider});var l={};return e.forEach(c.rules,function(a){l[a.name]=a}),t.resolveGrammar(l,c.errMsgProvider)}n.resolveGrammar=s;function o(c){return c=e.defaults(c,{errMsgProvider:r.defaultGrammarValidatorErrorProvider}),i.validateGrammar(c.rules,c.maxLookahead,c.tokenTypes,c.errMsgProvider,c.grammarName)}n.validateGrammar=o}),es=je(n=>{"use strict";var e=n&&n.__extends||(function(){var g=function(y,h){return g=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(u,E){u.__proto__=E}||function(u,E){for(var x in E)Object.prototype.hasOwnProperty.call(E,x)&&(u[x]=E[x])},g(y,h)};return function(y,h){if(typeof h!="function"&&h!==null)throw new TypeError("Class extends value "+String(h)+" is not a constructor or null");g(y,h);function u(){this.constructor=y}y.prototype=h===null?Object.create(h):(u.prototype=h.prototype,new u)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.EarlyExitException=n.NotAllInputParsedException=n.NoViableAltException=n.MismatchedTokenException=n.isRecognitionException=void 0;var t=st(),i="MismatchedTokenException",r="NoViableAltException",s="EarlyExitException",o="NotAllInputParsedException",c=[i,r,s,o];Object.freeze(c);function l(g){return t.contains(c,g.name)}n.isRecognitionException=l;var a=(function(g){e(y,g);function y(h,u){var E=this.constructor,x=g.call(this,h)||this;return x.token=u,x.resyncedTokens=[],Object.setPrototypeOf(x,E.prototype),Error.captureStackTrace&&Error.captureStackTrace(x,x.constructor),x}return y})(Error),d=(function(g){e(y,g);function y(h,u,E){var x=g.call(this,h,u)||this;return x.previousToken=E,x.name=i,x}return y})(a);n.MismatchedTokenException=d;var p=(function(g){e(y,g);function y(h,u,E){var x=g.call(this,h,u)||this;return x.previousToken=E,x.name=r,x}return y})(a);n.NoViableAltException=p;var f=(function(g){e(y,g);function y(h,u){var E=g.call(this,h,u)||this;return E.name=o,E}return y})(a);n.NotAllInputParsedException=f;var m=(function(g){e(y,g);function y(h,u,E){var x=g.call(this,h,u)||this;return x.previousToken=E,x.name=s,x}return y})(a);n.EarlyExitException=m}),Xu=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.attemptInRepetitionRecovery=n.Recoverable=n.InRuleRecoveryException=n.IN_RULE_RECOVERY_EXCEPTION=n.EOF_FOLLOW_KEY=void 0;var e=Ei(),t=st(),i=es(),r=Hu(),s=nn();n.EOF_FOLLOW_KEY={},n.IN_RULE_RECOVERY_EXCEPTION="InRuleRecoveryException";function o(a){this.name=n.IN_RULE_RECOVERY_EXCEPTION,this.message=a}n.InRuleRecoveryException=o,o.prototype=Error.prototype;var c=(function(){function a(){}return a.prototype.initRecoverable=function(d){this.firstAfterRepMap={},this.resyncFollows={},this.recoveryEnabled=t.has(d,"recoveryEnabled")?d.recoveryEnabled:s.DEFAULT_PARSER_CONFIG.recoveryEnabled,this.recoveryEnabled&&(this.attemptInRepetitionRecovery=l)},a.prototype.getTokenToInsert=function(d){var p=e.createTokenInstance(d,"",NaN,NaN,NaN,NaN,NaN,NaN);return p.isInsertedInRecovery=!0,p},a.prototype.canTokenTypeBeInsertedInRecovery=function(d){return!0},a.prototype.tryInRepetitionRecovery=function(d,p,f,m){for(var g=this,y=this.findReSyncTokenType(),h=this.exportLexerState(),u=[],E=!1,x=this.LA(1),_=this.LA(1),A=function(){var N=g.LA(0),w=g.errorMessageProvider.buildMismatchTokenMessage({expected:m,actual:x,previous:N,ruleName:g.getCurrRuleFullName()}),O=new i.MismatchedTokenException(w,x,g.LA(0));O.resyncedTokens=t.dropRight(u),g.SAVE_ERROR(O)};!E;)if(this.tokenMatcher(_,m)){A();return}else if(f.call(this)){A(),d.apply(this,p);return}else this.tokenMatcher(_,y)?E=!0:(_=this.SKIP_TOKEN(),this.addToResyncTokens(_,u));this.importLexerState(h)},a.prototype.shouldInRepetitionRecoveryBeTried=function(d,p,f){return!(f===!1||d===void 0||p===void 0||this.tokenMatcher(this.LA(1),d)||this.isBackTracking()||this.canPerformInRuleRecovery(d,this.getFollowsForInRuleRecovery(d,p)))},a.prototype.getFollowsForInRuleRecovery=function(d,p){var f=this.getCurrentGrammarPath(d,p),m=this.getNextPossibleTokenTypes(f);return m},a.prototype.tryInRuleRecovery=function(d,p){if(this.canRecoverWithSingleTokenInsertion(d,p)){var f=this.getTokenToInsert(d);return f}if(this.canRecoverWithSingleTokenDeletion(d)){var m=this.SKIP_TOKEN();return this.consumeToken(),m}throw new o("sad sad panda")},a.prototype.canPerformInRuleRecovery=function(d,p){return this.canRecoverWithSingleTokenInsertion(d,p)||this.canRecoverWithSingleTokenDeletion(d)},a.prototype.canRecoverWithSingleTokenInsertion=function(d,p){var f=this;if(!this.canTokenTypeBeInsertedInRecovery(d)||t.isEmpty(p))return!1;var m=this.LA(1),g=t.find(p,function(y){return f.tokenMatcher(m,y)})!==void 0;return g},a.prototype.canRecoverWithSingleTokenDeletion=function(d){var p=this.tokenMatcher(this.LA(2),d);return p},a.prototype.isInCurrentRuleReSyncSet=function(d){var p=this.getCurrFollowKey(),f=this.getFollowSetFromFollowKey(p);return t.contains(f,d)},a.prototype.findReSyncTokenType=function(){for(var d=this.flattenFollowSet(),p=this.LA(1),f=2;;){var m=p.tokenType;if(t.contains(d,m))return m;p=this.LA(f),f++}},a.prototype.getCurrFollowKey=function(){if(this.RULE_STACK.length===1)return n.EOF_FOLLOW_KEY;var d=this.getLastExplicitRuleShortName(),p=this.getLastExplicitRuleOccurrenceIndex(),f=this.getPreviousExplicitRuleShortName();return{ruleName:this.shortRuleNameToFullName(d),idxInCallingRule:p,inRule:this.shortRuleNameToFullName(f)}},a.prototype.buildFullFollowKeyStack=function(){var d=this,p=this.RULE_STACK,f=this.RULE_OCCURRENCE_STACK;return t.map(p,function(m,g){return g===0?n.EOF_FOLLOW_KEY:{ruleName:d.shortRuleNameToFullName(m),idxInCallingRule:f[g],inRule:d.shortRuleNameToFullName(p[g-1])}})},a.prototype.flattenFollowSet=function(){var d=this,p=t.map(this.buildFullFollowKeyStack(),function(f){return d.getFollowSetFromFollowKey(f)});return t.flatten(p)},a.prototype.getFollowSetFromFollowKey=function(d){if(d===n.EOF_FOLLOW_KEY)return[e.EOF];var p=d.ruleName+d.idxInCallingRule+r.IN+d.inRule;return this.resyncFollows[p]},a.prototype.addToResyncTokens=function(d,p){return this.tokenMatcher(d,e.EOF)||p.push(d),p},a.prototype.reSyncTo=function(d){for(var p=[],f=this.LA(1);this.tokenMatcher(f,d)===!1;)f=this.SKIP_TOKEN(),this.addToResyncTokens(f,p);return t.dropRight(p)},a.prototype.attemptInRepetitionRecovery=function(d,p,f,m,g,y,h){},a.prototype.getCurrentGrammarPath=function(d,p){var f=this.getHumanReadableRuleStack(),m=t.cloneArr(this.RULE_OCCURRENCE_STACK),g={ruleStack:f,occurrenceStack:m,lastTok:d,lastTokOccurrence:p};return g},a.prototype.getHumanReadableRuleStack=function(){var d=this;return t.map(this.RULE_STACK,function(p){return d.shortRuleNameToFullName(p)})},a})();n.Recoverable=c;function l(a,d,p,f,m,g,y){var h=this.getKeyForAutomaticLookahead(f,m),u=this.firstAfterRepMap[h];if(u===void 0){var E=this.getCurrRuleFullName(),x=this.getGAstProductions()[E],_=new g(x,m);u=_.startWalking(),this.firstAfterRepMap[h]=u}var A=u.token,N=u.occurrence,w=u.isEndOfRule;this.RULE_STACK.length===1&&w&&A===void 0&&(A=e.EOF,N=1),this.shouldInRepetitionRecoveryBeTried(A,N,y)&&this.tryInRepetitionRecovery(a,d,p,A)}n.attemptInRepetitionRecovery=l}),Ic=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.getKeyForAutomaticLookahead=n.AT_LEAST_ONE_SEP_IDX=n.MANY_SEP_IDX=n.AT_LEAST_ONE_IDX=n.MANY_IDX=n.OPTION_IDX=n.OR_IDX=n.BITS_FOR_ALT_IDX=n.BITS_FOR_RULE_IDX=n.BITS_FOR_OCCURRENCE_IDX=n.BITS_FOR_METHOD_TYPE=void 0,n.BITS_FOR_METHOD_TYPE=4,n.BITS_FOR_OCCURRENCE_IDX=8,n.BITS_FOR_RULE_IDX=12,n.BITS_FOR_ALT_IDX=8,n.OR_IDX=1<<n.BITS_FOR_OCCURRENCE_IDX,n.OPTION_IDX=2<<n.BITS_FOR_OCCURRENCE_IDX,n.MANY_IDX=3<<n.BITS_FOR_OCCURRENCE_IDX,n.AT_LEAST_ONE_IDX=4<<n.BITS_FOR_OCCURRENCE_IDX,n.MANY_SEP_IDX=5<<n.BITS_FOR_OCCURRENCE_IDX,n.AT_LEAST_ONE_SEP_IDX=6<<n.BITS_FOR_OCCURRENCE_IDX;function e(i,r,s){return s|r|i}n.getKeyForAutomaticLookahead=e;var t=32-n.BITS_FOR_ALT_IDX}),l_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.LooksAhead=void 0;var e=ea(),t=st(),i=nn(),r=Ic(),s=Jo(),o=(function(){function c(){}return c.prototype.initLooksAhead=function(l){this.dynamicTokensEnabled=t.has(l,"dynamicTokensEnabled")?l.dynamicTokensEnabled:i.DEFAULT_PARSER_CONFIG.dynamicTokensEnabled,this.maxLookahead=t.has(l,"maxLookahead")?l.maxLookahead:i.DEFAULT_PARSER_CONFIG.maxLookahead,this.lookAheadFuncsCache=t.isES2015MapSupported()?new Map:[],t.isES2015MapSupported()?(this.getLaFuncFromCache=this.getLaFuncFromMap,this.setLaFuncCache=this.setLaFuncCacheUsingMap):(this.getLaFuncFromCache=this.getLaFuncFromObj,this.setLaFuncCache=this.setLaFuncUsingObj)},c.prototype.preComputeLookaheadFunctions=function(l){var a=this;t.forEach(l,function(d){a.TRACE_INIT(d.name+" Rule Lookahead",function(){var p=s.collectMethods(d),f=p.alternation,m=p.repetition,g=p.option,y=p.repetitionMandatory,h=p.repetitionMandatoryWithSeparator,u=p.repetitionWithSeparator;t.forEach(f,function(E){var x=E.idx===0?"":E.idx;a.TRACE_INIT(""+s.getProductionDslName(E)+x,function(){var _=e.buildLookaheadFuncForOr(E.idx,d,E.maxLookahead||a.maxLookahead,E.hasPredicates,a.dynamicTokensEnabled,a.lookAheadBuilderForAlternatives),A=r.getKeyForAutomaticLookahead(a.fullRuleNameToShort[d.name],r.OR_IDX,E.idx);a.setLaFuncCache(A,_)})}),t.forEach(m,function(E){a.computeLookaheadFunc(d,E.idx,r.MANY_IDX,e.PROD_TYPE.REPETITION,E.maxLookahead,s.getProductionDslName(E))}),t.forEach(g,function(E){a.computeLookaheadFunc(d,E.idx,r.OPTION_IDX,e.PROD_TYPE.OPTION,E.maxLookahead,s.getProductionDslName(E))}),t.forEach(y,function(E){a.computeLookaheadFunc(d,E.idx,r.AT_LEAST_ONE_IDX,e.PROD_TYPE.REPETITION_MANDATORY,E.maxLookahead,s.getProductionDslName(E))}),t.forEach(h,function(E){a.computeLookaheadFunc(d,E.idx,r.AT_LEAST_ONE_SEP_IDX,e.PROD_TYPE.REPETITION_MANDATORY_WITH_SEPARATOR,E.maxLookahead,s.getProductionDslName(E))}),t.forEach(u,function(E){a.computeLookaheadFunc(d,E.idx,r.MANY_SEP_IDX,e.PROD_TYPE.REPETITION_WITH_SEPARATOR,E.maxLookahead,s.getProductionDslName(E))})})})},c.prototype.computeLookaheadFunc=function(l,a,d,p,f,m){var g=this;this.TRACE_INIT(""+m+(a===0?"":a),function(){var y=e.buildLookaheadFuncForOptionalProd(a,l,f||g.maxLookahead,g.dynamicTokensEnabled,p,g.lookAheadBuilderForOptional),h=r.getKeyForAutomaticLookahead(g.fullRuleNameToShort[l.name],d,a);g.setLaFuncCache(h,y)})},c.prototype.lookAheadBuilderForOptional=function(l,a,d){return e.buildSingleAlternativeLookaheadFunction(l,a,d)},c.prototype.lookAheadBuilderForAlternatives=function(l,a,d,p){return e.buildAlternativesLookAheadFunc(l,a,d,p)},c.prototype.getKeyForAutomaticLookahead=function(l,a){var d=this.getLastExplicitRuleShortName();return r.getKeyForAutomaticLookahead(d,l,a)},c.prototype.getLaFuncFromCache=function(l){},c.prototype.getLaFuncFromMap=function(l){return this.lookAheadFuncsCache.get(l)},c.prototype.getLaFuncFromObj=function(l){return this.lookAheadFuncsCache[l]},c.prototype.setLaFuncCache=function(l,a){},c.prototype.setLaFuncCacheUsingMap=function(l,a){this.lookAheadFuncsCache.set(l,a)},c.prototype.setLaFuncUsingObj=function(l,a){this.lookAheadFuncsCache[l]=a},c})();n.LooksAhead=o}),u_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.addNoneTerminalToCst=n.addTerminalToCst=n.setNodeLocationFull=n.setNodeLocationOnlyOffset=void 0;function e(s,o){isNaN(s.startOffset)===!0?(s.startOffset=o.startOffset,s.endOffset=o.endOffset):s.endOffset<o.endOffset&&(s.endOffset=o.endOffset)}n.setNodeLocationOnlyOffset=e;function t(s,o){isNaN(s.startOffset)===!0?(s.startOffset=o.startOffset,s.startColumn=o.startColumn,s.startLine=o.startLine,s.endOffset=o.endOffset,s.endColumn=o.endColumn,s.endLine=o.endLine):s.endOffset<o.endOffset&&(s.endOffset=o.endOffset,s.endColumn=o.endColumn,s.endLine=o.endLine)}n.setNodeLocationFull=t;function i(s,o,c){s.children[c]===void 0?s.children[c]=[o]:s.children[c].push(o)}n.addTerminalToCst=i;function r(s,o,c){s.children[o]===void 0?s.children[o]=[c]:s.children[o].push(c)}n.addNoneTerminalToCst=r}),Yu=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.defineNameProp=n.functionName=n.classNameFromInstance=void 0;var e=st();function t(o){return r(o.constructor)}n.classNameFromInstance=t;var i="name";function r(o){var c=o.name;return c||"anonymous"}n.functionName=r;function s(o,c){var l=Object.getOwnPropertyDescriptor(o,i);return e.isUndefined(l)||l.configurable?(Object.defineProperty(o,i,{enumerable:!1,configurable:!0,writable:!1,value:c}),!0):!1}n.defineNameProp=s}),h_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.validateRedundantMethods=n.validateMissingCstMethods=n.validateVisitor=n.CstVisitorDefinitionError=n.createBaseVisitorConstructorWithDefaults=n.createBaseSemanticVisitorConstructor=n.defaultVisit=void 0;var e=st(),t=Yu();function i(p,f){for(var m=e.keys(p),g=m.length,y=0;y<g;y++)for(var h=m[y],u=p[h],E=u.length,x=0;x<E;x++){var _=u[x];_.tokenTypeIdx===void 0&&this[_.name](_.children,f)}}n.defaultVisit=i;function r(p,f){var m=function(){};t.defineNameProp(m,p+"BaseSemantics");var g={visit:function(y,h){if(e.isArray(y)&&(y=y[0]),!e.isUndefined(y))return this[y.name](y.children,h)},validateVisitor:function(){var y=c(this,f);if(!e.isEmpty(y)){var h=e.map(y,function(u){return u.msg});throw Error("Errors Detected in CST Visitor <"+t.functionName(this.constructor)+`>:
	`+(""+h.join(`

`).replace(/\n/g,`
	`)))}}};return m.prototype=g,m.prototype.constructor=m,m._RULE_NAMES=f,m}n.createBaseSemanticVisitorConstructor=r;function s(p,f,m){var g=function(){};t.defineNameProp(g,p+"BaseSemanticsWithDefaults");var y=Object.create(m.prototype);return e.forEach(f,function(h){y[h]=i}),g.prototype=y,g.prototype.constructor=g,g}n.createBaseVisitorConstructorWithDefaults=s;var o;(function(p){p[p.REDUNDANT_METHOD=0]="REDUNDANT_METHOD",p[p.MISSING_METHOD=1]="MISSING_METHOD"})(o=n.CstVisitorDefinitionError||(n.CstVisitorDefinitionError={}));function c(p,f){var m=l(p,f),g=d(p,f);return m.concat(g)}n.validateVisitor=c;function l(p,f){var m=e.map(f,function(g){if(!e.isFunction(p[g]))return{msg:"Missing visitor method: <"+g+"> on "+t.functionName(p.constructor)+" CST Visitor.",type:o.MISSING_METHOD,methodName:g}});return e.compact(m)}n.validateMissingCstMethods=l;var a=["constructor","visit","validateVisitor"];function d(p,f){var m=[];for(var g in p)e.isFunction(p[g])&&!e.contains(a,g)&&!e.contains(f,g)&&m.push({msg:"Redundant visitor method: <"+g+"> on "+t.functionName(p.constructor)+` CST Visitor
There is no Grammar Rule corresponding to this method's name.
`,type:o.REDUNDANT_METHOD,methodName:g});return m}n.validateRedundantMethods=d}),d_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.TreeBuilder=void 0;var e=u_(),t=st(),i=h_(),r=nn(),s=(function(){function o(){}return o.prototype.initTreeBuilder=function(c){if(this.CST_STACK=[],this.outputCst=c.outputCst,this.nodeLocationTracking=t.has(c,"nodeLocationTracking")?c.nodeLocationTracking:r.DEFAULT_PARSER_CONFIG.nodeLocationTracking,!this.outputCst)this.cstInvocationStateUpdate=t.NOOP,this.cstFinallyStateUpdate=t.NOOP,this.cstPostTerminal=t.NOOP,this.cstPostNonTerminal=t.NOOP,this.cstPostRule=t.NOOP;else if(/full/i.test(this.nodeLocationTracking))this.recoveryEnabled?(this.setNodeLocationFromToken=e.setNodeLocationFull,this.setNodeLocationFromNode=e.setNodeLocationFull,this.cstPostRule=t.NOOP,this.setInitialNodeLocation=this.setInitialNodeLocationFullRecovery):(this.setNodeLocationFromToken=t.NOOP,this.setNodeLocationFromNode=t.NOOP,this.cstPostRule=this.cstPostRuleFull,this.setInitialNodeLocation=this.setInitialNodeLocationFullRegular);else if(/onlyOffset/i.test(this.nodeLocationTracking))this.recoveryEnabled?(this.setNodeLocationFromToken=e.setNodeLocationOnlyOffset,this.setNodeLocationFromNode=e.setNodeLocationOnlyOffset,this.cstPostRule=t.NOOP,this.setInitialNodeLocation=this.setInitialNodeLocationOnlyOffsetRecovery):(this.setNodeLocationFromToken=t.NOOP,this.setNodeLocationFromNode=t.NOOP,this.cstPostRule=this.cstPostRuleOnlyOffset,this.setInitialNodeLocation=this.setInitialNodeLocationOnlyOffsetRegular);else if(/none/i.test(this.nodeLocationTracking))this.setNodeLocationFromToken=t.NOOP,this.setNodeLocationFromNode=t.NOOP,this.cstPostRule=t.NOOP,this.setInitialNodeLocation=t.NOOP;else throw Error('Invalid <nodeLocationTracking> config option: "'+c.nodeLocationTracking+'"')},o.prototype.setInitialNodeLocationOnlyOffsetRecovery=function(c){c.location={startOffset:NaN,endOffset:NaN}},o.prototype.setInitialNodeLocationOnlyOffsetRegular=function(c){c.location={startOffset:this.LA(1).startOffset,endOffset:NaN}},o.prototype.setInitialNodeLocationFullRecovery=function(c){c.location={startOffset:NaN,startLine:NaN,startColumn:NaN,endOffset:NaN,endLine:NaN,endColumn:NaN}},o.prototype.setInitialNodeLocationFullRegular=function(c){var l=this.LA(1);c.location={startOffset:l.startOffset,startLine:l.startLine,startColumn:l.startColumn,endOffset:NaN,endLine:NaN,endColumn:NaN}},o.prototype.cstInvocationStateUpdate=function(c,l){var a={name:c,children:{}};this.setInitialNodeLocation(a),this.CST_STACK.push(a)},o.prototype.cstFinallyStateUpdate=function(){this.CST_STACK.pop()},o.prototype.cstPostRuleFull=function(c){var l=this.LA(0),a=c.location;a.startOffset<=l.startOffset?(a.endOffset=l.endOffset,a.endLine=l.endLine,a.endColumn=l.endColumn):(a.startOffset=NaN,a.startLine=NaN,a.startColumn=NaN)},o.prototype.cstPostRuleOnlyOffset=function(c){var l=this.LA(0),a=c.location;a.startOffset<=l.startOffset?a.endOffset=l.endOffset:a.startOffset=NaN},o.prototype.cstPostTerminal=function(c,l){var a=this.CST_STACK[this.CST_STACK.length-1];e.addTerminalToCst(a,l,c),this.setNodeLocationFromToken(a.location,l)},o.prototype.cstPostNonTerminal=function(c,l){var a=this.CST_STACK[this.CST_STACK.length-1];e.addNoneTerminalToCst(a,l,c),this.setNodeLocationFromNode(a.location,c.location)},o.prototype.getBaseCstVisitorConstructor=function(){if(t.isUndefined(this.baseCstVisitorConstructor)){var c=i.createBaseSemanticVisitorConstructor(this.className,t.keys(this.gastProductionsCache));return this.baseCstVisitorConstructor=c,c}return this.baseCstVisitorConstructor},o.prototype.getBaseCstVisitorConstructorWithDefaults=function(){if(t.isUndefined(this.baseCstVisitorWithDefaultsConstructor)){var c=i.createBaseVisitorConstructorWithDefaults(this.className,t.keys(this.gastProductionsCache),this.getBaseCstVisitorConstructor());return this.baseCstVisitorWithDefaultsConstructor=c,c}return this.baseCstVisitorWithDefaultsConstructor},o.prototype.getLastExplicitRuleShortName=function(){var c=this.RULE_STACK;return c[c.length-1]},o.prototype.getPreviousExplicitRuleShortName=function(){var c=this.RULE_STACK;return c[c.length-2]},o.prototype.getLastExplicitRuleOccurrenceIndex=function(){var c=this.RULE_OCCURRENCE_STACK;return c[c.length-1]},o})();n.TreeBuilder=s}),f_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.LexerAdapter=void 0;var e=nn(),t=(function(){function i(){}return i.prototype.initLexerAdapter=function(){this.tokVector=[],this.tokVectorLength=0,this.currIdx=-1},Object.defineProperty(i.prototype,"input",{get:function(){return this.tokVector},set:function(r){if(this.selfAnalysisDone!==!0)throw Error("Missing <performSelfAnalysis> invocation at the end of the Parser's constructor.");this.reset(),this.tokVector=r,this.tokVectorLength=r.length},enumerable:!1,configurable:!0}),i.prototype.SKIP_TOKEN=function(){return this.currIdx<=this.tokVector.length-2?(this.consumeToken(),this.LA(1)):e.END_OF_FILE},i.prototype.LA=function(r){var s=this.currIdx+r;return s<0||this.tokVectorLength<=s?e.END_OF_FILE:this.tokVector[s]},i.prototype.consumeToken=function(){this.currIdx++},i.prototype.exportLexerState=function(){return this.currIdx},i.prototype.importLexerState=function(r){this.currIdx=r},i.prototype.resetLexerState=function(){this.currIdx=-1},i.prototype.moveToTerminatedState=function(){this.currIdx=this.tokVector.length-1},i.prototype.getLexerPosition=function(){return this.exportLexerState()},i})();n.LexerAdapter=t}),p_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.RecognizerApi=void 0;var e=st(),t=es(),i=nn(),r=$o(),s=Wu(),o=Zt(),c=(function(){function l(){}return l.prototype.ACTION=function(a){return a.call(this)},l.prototype.consume=function(a,d,p){return this.consumeInternal(d,a,p)},l.prototype.subrule=function(a,d,p){return this.subruleInternal(d,a,p)},l.prototype.option=function(a,d){return this.optionInternal(d,a)},l.prototype.or=function(a,d){return this.orInternal(d,a)},l.prototype.many=function(a,d){return this.manyInternal(a,d)},l.prototype.atLeastOne=function(a,d){return this.atLeastOneInternal(a,d)},l.prototype.CONSUME=function(a,d){return this.consumeInternal(a,0,d)},l.prototype.CONSUME1=function(a,d){return this.consumeInternal(a,1,d)},l.prototype.CONSUME2=function(a,d){return this.consumeInternal(a,2,d)},l.prototype.CONSUME3=function(a,d){return this.consumeInternal(a,3,d)},l.prototype.CONSUME4=function(a,d){return this.consumeInternal(a,4,d)},l.prototype.CONSUME5=function(a,d){return this.consumeInternal(a,5,d)},l.prototype.CONSUME6=function(a,d){return this.consumeInternal(a,6,d)},l.prototype.CONSUME7=function(a,d){return this.consumeInternal(a,7,d)},l.prototype.CONSUME8=function(a,d){return this.consumeInternal(a,8,d)},l.prototype.CONSUME9=function(a,d){return this.consumeInternal(a,9,d)},l.prototype.SUBRULE=function(a,d){return this.subruleInternal(a,0,d)},l.prototype.SUBRULE1=function(a,d){return this.subruleInternal(a,1,d)},l.prototype.SUBRULE2=function(a,d){return this.subruleInternal(a,2,d)},l.prototype.SUBRULE3=function(a,d){return this.subruleInternal(a,3,d)},l.prototype.SUBRULE4=function(a,d){return this.subruleInternal(a,4,d)},l.prototype.SUBRULE5=function(a,d){return this.subruleInternal(a,5,d)},l.prototype.SUBRULE6=function(a,d){return this.subruleInternal(a,6,d)},l.prototype.SUBRULE7=function(a,d){return this.subruleInternal(a,7,d)},l.prototype.SUBRULE8=function(a,d){return this.subruleInternal(a,8,d)},l.prototype.SUBRULE9=function(a,d){return this.subruleInternal(a,9,d)},l.prototype.OPTION=function(a){return this.optionInternal(a,0)},l.prototype.OPTION1=function(a){return this.optionInternal(a,1)},l.prototype.OPTION2=function(a){return this.optionInternal(a,2)},l.prototype.OPTION3=function(a){return this.optionInternal(a,3)},l.prototype.OPTION4=function(a){return this.optionInternal(a,4)},l.prototype.OPTION5=function(a){return this.optionInternal(a,5)},l.prototype.OPTION6=function(a){return this.optionInternal(a,6)},l.prototype.OPTION7=function(a){return this.optionInternal(a,7)},l.prototype.OPTION8=function(a){return this.optionInternal(a,8)},l.prototype.OPTION9=function(a){return this.optionInternal(a,9)},l.prototype.OR=function(a){return this.orInternal(a,0)},l.prototype.OR1=function(a){return this.orInternal(a,1)},l.prototype.OR2=function(a){return this.orInternal(a,2)},l.prototype.OR3=function(a){return this.orInternal(a,3)},l.prototype.OR4=function(a){return this.orInternal(a,4)},l.prototype.OR5=function(a){return this.orInternal(a,5)},l.prototype.OR6=function(a){return this.orInternal(a,6)},l.prototype.OR7=function(a){return this.orInternal(a,7)},l.prototype.OR8=function(a){return this.orInternal(a,8)},l.prototype.OR9=function(a){return this.orInternal(a,9)},l.prototype.MANY=function(a){this.manyInternal(0,a)},l.prototype.MANY1=function(a){this.manyInternal(1,a)},l.prototype.MANY2=function(a){this.manyInternal(2,a)},l.prototype.MANY3=function(a){this.manyInternal(3,a)},l.prototype.MANY4=function(a){this.manyInternal(4,a)},l.prototype.MANY5=function(a){this.manyInternal(5,a)},l.prototype.MANY6=function(a){this.manyInternal(6,a)},l.prototype.MANY7=function(a){this.manyInternal(7,a)},l.prototype.MANY8=function(a){this.manyInternal(8,a)},l.prototype.MANY9=function(a){this.manyInternal(9,a)},l.prototype.MANY_SEP=function(a){this.manySepFirstInternal(0,a)},l.prototype.MANY_SEP1=function(a){this.manySepFirstInternal(1,a)},l.prototype.MANY_SEP2=function(a){this.manySepFirstInternal(2,a)},l.prototype.MANY_SEP3=function(a){this.manySepFirstInternal(3,a)},l.prototype.MANY_SEP4=function(a){this.manySepFirstInternal(4,a)},l.prototype.MANY_SEP5=function(a){this.manySepFirstInternal(5,a)},l.prototype.MANY_SEP6=function(a){this.manySepFirstInternal(6,a)},l.prototype.MANY_SEP7=function(a){this.manySepFirstInternal(7,a)},l.prototype.MANY_SEP8=function(a){this.manySepFirstInternal(8,a)},l.prototype.MANY_SEP9=function(a){this.manySepFirstInternal(9,a)},l.prototype.AT_LEAST_ONE=function(a){this.atLeastOneInternal(0,a)},l.prototype.AT_LEAST_ONE1=function(a){return this.atLeastOneInternal(1,a)},l.prototype.AT_LEAST_ONE2=function(a){this.atLeastOneInternal(2,a)},l.prototype.AT_LEAST_ONE3=function(a){this.atLeastOneInternal(3,a)},l.prototype.AT_LEAST_ONE4=function(a){this.atLeastOneInternal(4,a)},l.prototype.AT_LEAST_ONE5=function(a){this.atLeastOneInternal(5,a)},l.prototype.AT_LEAST_ONE6=function(a){this.atLeastOneInternal(6,a)},l.prototype.AT_LEAST_ONE7=function(a){this.atLeastOneInternal(7,a)},l.prototype.AT_LEAST_ONE8=function(a){this.atLeastOneInternal(8,a)},l.prototype.AT_LEAST_ONE9=function(a){this.atLeastOneInternal(9,a)},l.prototype.AT_LEAST_ONE_SEP=function(a){this.atLeastOneSepFirstInternal(0,a)},l.prototype.AT_LEAST_ONE_SEP1=function(a){this.atLeastOneSepFirstInternal(1,a)},l.prototype.AT_LEAST_ONE_SEP2=function(a){this.atLeastOneSepFirstInternal(2,a)},l.prototype.AT_LEAST_ONE_SEP3=function(a){this.atLeastOneSepFirstInternal(3,a)},l.prototype.AT_LEAST_ONE_SEP4=function(a){this.atLeastOneSepFirstInternal(4,a)},l.prototype.AT_LEAST_ONE_SEP5=function(a){this.atLeastOneSepFirstInternal(5,a)},l.prototype.AT_LEAST_ONE_SEP6=function(a){this.atLeastOneSepFirstInternal(6,a)},l.prototype.AT_LEAST_ONE_SEP7=function(a){this.atLeastOneSepFirstInternal(7,a)},l.prototype.AT_LEAST_ONE_SEP8=function(a){this.atLeastOneSepFirstInternal(8,a)},l.prototype.AT_LEAST_ONE_SEP9=function(a){this.atLeastOneSepFirstInternal(9,a)},l.prototype.RULE=function(a,d,p){if(p===void 0&&(p=i.DEFAULT_RULE_CONFIG),e.contains(this.definedRulesNames,a)){var f=r.defaultGrammarValidatorErrorProvider.buildDuplicateRuleNameError({topLevelRule:a,grammarName:this.className}),m={message:f,type:i.ParserDefinitionErrorType.DUPLICATE_RULE_NAME,ruleName:a};this.definitionErrors.push(m)}this.definedRulesNames.push(a);var g=this.defineRule(a,d,p);return this[a]=g,g},l.prototype.OVERRIDE_RULE=function(a,d,p){p===void 0&&(p=i.DEFAULT_RULE_CONFIG);var f=[];f=f.concat(s.validateRuleIsOverridden(a,this.definedRulesNames,this.className)),this.definitionErrors=this.definitionErrors.concat(f);var m=this.defineRule(a,d,p);return this[a]=m,m},l.prototype.BACKTRACK=function(a,d){return function(){this.isBackTrackingStack.push(1);var p=this.saveRecogState();try{return a.apply(this,d),!0}catch(f){if(t.isRecognitionException(f))return!1;throw f}finally{this.reloadRecogState(p),this.isBackTrackingStack.pop()}}},l.prototype.getGAstProductions=function(){return this.gastProductionsCache},l.prototype.getSerializedGastProductions=function(){return o.serializeGrammar(e.values(this.gastProductionsCache))},l})();n.RecognizerApi=c}),m_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.RecognizerEngine=void 0;var e=st(),t=Ic(),i=es(),r=ea(),s=Qo(),o=nn(),c=Xu(),l=Ei(),a=$r(),d=Yu(),p=(function(){function f(){}return f.prototype.initRecognizerEngine=function(m,g){if(this.className=d.classNameFromInstance(this),this.shortRuleNameToFull={},this.fullRuleNameToShort={},this.ruleShortNameIdx=256,this.tokenMatcher=a.tokenStructuredMatcherNoCategories,this.definedRulesNames=[],this.tokensMap={},this.isBackTrackingStack=[],this.RULE_STACK=[],this.RULE_OCCURRENCE_STACK=[],this.gastProductionsCache={},e.has(g,"serializedGrammar"))throw Error(`The Parser's configuration can no longer contain a <serializedGrammar> property.
	See: https://chevrotain.io/docs/changes/BREAKING_CHANGES.html#_6-0-0
	For Further details.`);if(e.isArray(m)){if(e.isEmpty(m))throw Error(`A Token Vocabulary cannot be empty.
	Note that the first argument for the parser constructor
	is no longer a Token vector (since v4.0).`);if(typeof m[0].startOffset=="number")throw Error(`The Parser constructor no longer accepts a token vector as the first argument.
	See: https://chevrotain.io/docs/changes/BREAKING_CHANGES.html#_4-0-0
	For Further details.`)}if(e.isArray(m))this.tokensMap=e.reduce(m,function(E,x){return E[x.name]=x,E},{});else if(e.has(m,"modes")&&e.every(e.flatten(e.values(m.modes)),a.isTokenType)){var y=e.flatten(e.values(m.modes)),h=e.uniq(y);this.tokensMap=e.reduce(h,function(E,x){return E[x.name]=x,E},{})}else if(e.isObject(m))this.tokensMap=e.cloneObj(m);else throw new Error("<tokensDictionary> argument must be An Array of Token constructors, A dictionary of Token constructors or an IMultiModeLexerDefinition");this.tokensMap.EOF=l.EOF;var u=e.every(e.values(m),function(E){return e.isEmpty(E.categoryMatches)});this.tokenMatcher=u?a.tokenStructuredMatcherNoCategories:a.tokenStructuredMatcher,a.augmentTokenTypes(e.values(this.tokensMap))},f.prototype.defineRule=function(m,g,y){if(this.selfAnalysisDone)throw Error("Grammar rule <"+m+`> may not be defined after the 'performSelfAnalysis' method has been called'
Make sure that all grammar rule definitions are done before 'performSelfAnalysis' is called.`);var h=e.has(y,"resyncEnabled")?y.resyncEnabled:o.DEFAULT_RULE_CONFIG.resyncEnabled,u=e.has(y,"recoveryValueFunc")?y.recoveryValueFunc:o.DEFAULT_RULE_CONFIG.recoveryValueFunc,E=this.ruleShortNameIdx<<t.BITS_FOR_METHOD_TYPE+t.BITS_FOR_OCCURRENCE_IDX;this.ruleShortNameIdx++,this.shortRuleNameToFull[E]=m,this.fullRuleNameToShort[m]=E;function x(N){try{if(this.outputCst===!0){g.apply(this,N);var w=this.CST_STACK[this.CST_STACK.length-1];return this.cstPostRule(w),w}else return g.apply(this,N)}catch(O){return this.invokeRuleCatch(O,h,u)}finally{this.ruleFinallyStateUpdate()}}var _=function(N,w){return N===void 0&&(N=0),this.ruleInvocationStateUpdate(E,m,N),x.call(this,w)},A="ruleName";return _[A]=m,_.originalGrammarAction=g,_},f.prototype.invokeRuleCatch=function(m,g,y){var h=this.RULE_STACK.length===1,u=g&&!this.isBackTracking()&&this.recoveryEnabled;if(i.isRecognitionException(m)){var E=m;if(u){var x=this.findReSyncTokenType();if(this.isInCurrentRuleReSyncSet(x))if(E.resyncedTokens=this.reSyncTo(x),this.outputCst){var _=this.CST_STACK[this.CST_STACK.length-1];return _.recoveredNode=!0,_}else return y();else{if(this.outputCst){var _=this.CST_STACK[this.CST_STACK.length-1];_.recoveredNode=!0,E.partialCstResult=_}throw E}}else{if(h)return this.moveToTerminatedState(),y();throw E}}else throw m},f.prototype.optionInternal=function(m,g){var y=this.getKeyForAutomaticLookahead(t.OPTION_IDX,g);return this.optionInternalLogic(m,g,y)},f.prototype.optionInternalLogic=function(m,g,y){var h=this,u=this.getLaFuncFromCache(y),E,x;if(m.DEF!==void 0){if(E=m.DEF,x=m.GATE,x!==void 0){var _=u;u=function(){return x.call(h)&&_.call(h)}}}else E=m;if(u.call(this)===!0)return E.call(this)},f.prototype.atLeastOneInternal=function(m,g){var y=this.getKeyForAutomaticLookahead(t.AT_LEAST_ONE_IDX,m);return this.atLeastOneInternalLogic(m,g,y)},f.prototype.atLeastOneInternalLogic=function(m,g,y){var h=this,u=this.getLaFuncFromCache(y),E,x;if(g.DEF!==void 0){if(E=g.DEF,x=g.GATE,x!==void 0){var _=u;u=function(){return x.call(h)&&_.call(h)}}}else E=g;if(u.call(this)===!0)for(var A=this.doSingleRepetition(E);u.call(this)===!0&&A===!0;)A=this.doSingleRepetition(E);else throw this.raiseEarlyExitException(m,r.PROD_TYPE.REPETITION_MANDATORY,g.ERR_MSG);this.attemptInRepetitionRecovery(this.atLeastOneInternal,[m,g],u,t.AT_LEAST_ONE_IDX,m,s.NextTerminalAfterAtLeastOneWalker)},f.prototype.atLeastOneSepFirstInternal=function(m,g){var y=this.getKeyForAutomaticLookahead(t.AT_LEAST_ONE_SEP_IDX,m);this.atLeastOneSepFirstInternalLogic(m,g,y)},f.prototype.atLeastOneSepFirstInternalLogic=function(m,g,y){var h=this,u=g.DEF,E=g.SEP,x=this.getLaFuncFromCache(y);if(x.call(this)===!0){u.call(this);for(var _=function(){return h.tokenMatcher(h.LA(1),E)};this.tokenMatcher(this.LA(1),E)===!0;)this.CONSUME(E),u.call(this);this.attemptInRepetitionRecovery(this.repetitionSepSecondInternal,[m,E,_,u,s.NextTerminalAfterAtLeastOneSepWalker],_,t.AT_LEAST_ONE_SEP_IDX,m,s.NextTerminalAfterAtLeastOneSepWalker)}else throw this.raiseEarlyExitException(m,r.PROD_TYPE.REPETITION_MANDATORY_WITH_SEPARATOR,g.ERR_MSG)},f.prototype.manyInternal=function(m,g){var y=this.getKeyForAutomaticLookahead(t.MANY_IDX,m);return this.manyInternalLogic(m,g,y)},f.prototype.manyInternalLogic=function(m,g,y){var h=this,u=this.getLaFuncFromCache(y),E,x;if(g.DEF!==void 0){if(E=g.DEF,x=g.GATE,x!==void 0){var _=u;u=function(){return x.call(h)&&_.call(h)}}}else E=g;for(var A=!0;u.call(this)===!0&&A===!0;)A=this.doSingleRepetition(E);this.attemptInRepetitionRecovery(this.manyInternal,[m,g],u,t.MANY_IDX,m,s.NextTerminalAfterManyWalker,A)},f.prototype.manySepFirstInternal=function(m,g){var y=this.getKeyForAutomaticLookahead(t.MANY_SEP_IDX,m);this.manySepFirstInternalLogic(m,g,y)},f.prototype.manySepFirstInternalLogic=function(m,g,y){var h=this,u=g.DEF,E=g.SEP,x=this.getLaFuncFromCache(y);if(x.call(this)===!0){u.call(this);for(var _=function(){return h.tokenMatcher(h.LA(1),E)};this.tokenMatcher(this.LA(1),E)===!0;)this.CONSUME(E),u.call(this);this.attemptInRepetitionRecovery(this.repetitionSepSecondInternal,[m,E,_,u,s.NextTerminalAfterManySepWalker],_,t.MANY_SEP_IDX,m,s.NextTerminalAfterManySepWalker)}},f.prototype.repetitionSepSecondInternal=function(m,g,y,h,u){for(;y();)this.CONSUME(g),h.call(this);this.attemptInRepetitionRecovery(this.repetitionSepSecondInternal,[m,g,y,h,u],y,t.AT_LEAST_ONE_SEP_IDX,m,u)},f.prototype.doSingleRepetition=function(m){var g=this.getLexerPosition();m.call(this);var y=this.getLexerPosition();return y>g},f.prototype.orInternal=function(m,g){var y=this.getKeyForAutomaticLookahead(t.OR_IDX,g),h=e.isArray(m)?m:m.DEF,u=this.getLaFuncFromCache(y),E=u.call(this,h);if(E!==void 0){var x=h[E];return x.ALT.call(this)}this.raiseNoAltException(g,m.ERR_MSG)},f.prototype.ruleFinallyStateUpdate=function(){if(this.RULE_STACK.pop(),this.RULE_OCCURRENCE_STACK.pop(),this.cstFinallyStateUpdate(),this.RULE_STACK.length===0&&this.isAtEndOfInput()===!1){var m=this.LA(1),g=this.errorMessageProvider.buildNotAllInputParsedMessage({firstRedundant:m,ruleName:this.getCurrRuleFullName()});this.SAVE_ERROR(new i.NotAllInputParsedException(g,m))}},f.prototype.subruleInternal=function(m,g,y){var h;try{var u=y!==void 0?y.ARGS:void 0;return h=m.call(this,g,u),this.cstPostNonTerminal(h,y!==void 0&&y.LABEL!==void 0?y.LABEL:m.ruleName),h}catch(E){this.subruleInternalError(E,y,m.ruleName)}},f.prototype.subruleInternalError=function(m,g,y){throw i.isRecognitionException(m)&&m.partialCstResult!==void 0&&(this.cstPostNonTerminal(m.partialCstResult,g!==void 0&&g.LABEL!==void 0?g.LABEL:y),delete m.partialCstResult),m},f.prototype.consumeInternal=function(m,g,y){var h;try{var u=this.LA(1);this.tokenMatcher(u,m)===!0?(this.consumeToken(),h=u):this.consumeInternalError(m,u,y)}catch(E){h=this.consumeInternalRecovery(m,g,E)}return this.cstPostTerminal(y!==void 0&&y.LABEL!==void 0?y.LABEL:m.name,h),h},f.prototype.consumeInternalError=function(m,g,y){var h,u=this.LA(0);throw y!==void 0&&y.ERR_MSG?h=y.ERR_MSG:h=this.errorMessageProvider.buildMismatchTokenMessage({expected:m,actual:g,previous:u,ruleName:this.getCurrRuleFullName()}),this.SAVE_ERROR(new i.MismatchedTokenException(h,g,u))},f.prototype.consumeInternalRecovery=function(m,g,y){if(this.recoveryEnabled&&y.name==="MismatchedTokenException"&&!this.isBackTracking()){var h=this.getFollowsForInRuleRecovery(m,g);try{return this.tryInRuleRecovery(m,h)}catch(u){throw u.name===c.IN_RULE_RECOVERY_EXCEPTION?y:u}}else throw y},f.prototype.saveRecogState=function(){var m=this.errors,g=e.cloneArr(this.RULE_STACK);return{errors:m,lexerState:this.exportLexerState(),RULE_STACK:g,CST_STACK:this.CST_STACK}},f.prototype.reloadRecogState=function(m){this.errors=m.errors,this.importLexerState(m.lexerState),this.RULE_STACK=m.RULE_STACK},f.prototype.ruleInvocationStateUpdate=function(m,g,y){this.RULE_OCCURRENCE_STACK.push(y),this.RULE_STACK.push(m),this.cstInvocationStateUpdate(g,m)},f.prototype.isBackTracking=function(){return this.isBackTrackingStack.length!==0},f.prototype.getCurrRuleFullName=function(){var m=this.getLastExplicitRuleShortName();return this.shortRuleNameToFull[m]},f.prototype.shortRuleNameToFullName=function(m){return this.shortRuleNameToFull[m]},f.prototype.isAtEndOfInput=function(){return this.tokenMatcher(this.LA(1),l.EOF)},f.prototype.reset=function(){this.resetLexerState(),this.isBackTrackingStack=[],this.errors=[],this.RULE_STACK=[],this.CST_STACK=[],this.RULE_OCCURRENCE_STACK=[]},f})();n.RecognizerEngine=p}),g_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.ErrorHandler=void 0;var e=es(),t=st(),i=ea(),r=nn(),s=(function(){function o(){}return o.prototype.initErrorHandler=function(c){this._errors=[],this.errorMessageProvider=t.has(c,"errorMessageProvider")?c.errorMessageProvider:r.DEFAULT_PARSER_CONFIG.errorMessageProvider},o.prototype.SAVE_ERROR=function(c){if(e.isRecognitionException(c))return c.context={ruleStack:this.getHumanReadableRuleStack(),ruleOccurrenceStack:t.cloneArr(this.RULE_OCCURRENCE_STACK)},this._errors.push(c),c;throw Error("Trying to save an Error which is not a RecognitionException")},Object.defineProperty(o.prototype,"errors",{get:function(){return t.cloneArr(this._errors)},set:function(c){this._errors=c},enumerable:!1,configurable:!0}),o.prototype.raiseEarlyExitException=function(c,l,a){for(var d=this.getCurrRuleFullName(),p=this.getGAstProductions()[d],f=i.getLookaheadPathsForOptionalProd(c,p,l,this.maxLookahead),m=f[0],g=[],y=1;y<=this.maxLookahead;y++)g.push(this.LA(y));var h=this.errorMessageProvider.buildEarlyExitMessage({expectedIterationPaths:m,actual:g,previous:this.LA(0),customUserDescription:a,ruleName:d});throw this.SAVE_ERROR(new e.EarlyExitException(h,this.LA(1),this.LA(0)))},o.prototype.raiseNoAltException=function(c,l){for(var a=this.getCurrRuleFullName(),d=this.getGAstProductions()[a],p=i.getLookaheadPathsForOr(c,d,this.maxLookahead),f=[],m=1;m<=this.maxLookahead;m++)f.push(this.LA(m));var g=this.LA(0),y=this.errorMessageProvider.buildNoViableAltMessage({expectedPathsPerAlt:p,actual:f,previous:g,customUserDescription:l,ruleName:this.getCurrRuleFullName()});throw this.SAVE_ERROR(new e.NoViableAltException(y,this.LA(1),g))},o})();n.ErrorHandler=s}),__=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.ContentAssist=void 0;var e=Qo(),t=st(),i=(function(){function r(){}return r.prototype.initContentAssist=function(){},r.prototype.computeContentAssist=function(s,o){var c=this.gastProductionsCache[s];if(t.isUndefined(c))throw Error("Rule ->"+s+"<- does not exist in this grammar.");return e.nextPossibleTokensAfter([c],o,this.tokenMatcher,this.maxLookahead)},r.prototype.getNextPossibleTokenTypes=function(s){var o=t.first(s.ruleStack),c=this.getGAstProductions(),l=c[o],a=new e.NextAfterTokenWalker(l,s).startWalking();return a},r})();n.ContentAssist=i}),y_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.GastRecorder=void 0;var e=st(),t=Zt(),i=jo(),r=$r(),s=Ei(),o=nn(),c=Ic(),l={description:"This Object indicates the Parser is during Recording Phase"};Object.freeze(l);var a=!0,d=Math.pow(2,c.BITS_FOR_OCCURRENCE_IDX)-1,p=s.createToken({name:"RECORDING_PHASE_TOKEN",pattern:i.Lexer.NA});r.augmentTokenTypes([p]);var f=s.createTokenInstance(p,`This IToken indicates the Parser is in Recording Phase
	See: https://chevrotain.io/docs/guide/internals.html#grammar-recording for details`,-1,-1,-1,-1,-1,-1);Object.freeze(f);var m={name:`This CSTNode indicates the Parser is in Recording Phase
	See: https://chevrotain.io/docs/guide/internals.html#grammar-recording for details`,children:{}},g=(function(){function x(){}return x.prototype.initGastRecorder=function(_){this.recordingProdStack=[],this.RECORDING_PHASE=!1},x.prototype.enableRecording=function(){var _=this;this.RECORDING_PHASE=!0,this.TRACE_INIT("Enable Recording",function(){for(var A=function(w){var O=w>0?w:"";_["CONSUME"+O]=function(T,M){return this.consumeInternalRecord(T,w,M)},_["SUBRULE"+O]=function(T,M){return this.subruleInternalRecord(T,w,M)},_["OPTION"+O]=function(T){return this.optionInternalRecord(T,w)},_["OR"+O]=function(T){return this.orInternalRecord(T,w)},_["MANY"+O]=function(T){this.manyInternalRecord(w,T)},_["MANY_SEP"+O]=function(T){this.manySepFirstInternalRecord(w,T)},_["AT_LEAST_ONE"+O]=function(T){this.atLeastOneInternalRecord(w,T)},_["AT_LEAST_ONE_SEP"+O]=function(T){this.atLeastOneSepFirstInternalRecord(w,T)}},N=0;N<10;N++)A(N);_.consume=function(w,O,T){return this.consumeInternalRecord(O,w,T)},_.subrule=function(w,O,T){return this.subruleInternalRecord(O,w,T)},_.option=function(w,O){return this.optionInternalRecord(O,w)},_.or=function(w,O){return this.orInternalRecord(O,w)},_.many=function(w,O){this.manyInternalRecord(w,O)},_.atLeastOne=function(w,O){this.atLeastOneInternalRecord(w,O)},_.ACTION=_.ACTION_RECORD,_.BACKTRACK=_.BACKTRACK_RECORD,_.LA=_.LA_RECORD})},x.prototype.disableRecording=function(){var _=this;this.RECORDING_PHASE=!1,this.TRACE_INIT("Deleting Recording methods",function(){for(var A=0;A<10;A++){var N=A>0?A:"";delete _["CONSUME"+N],delete _["SUBRULE"+N],delete _["OPTION"+N],delete _["OR"+N],delete _["MANY"+N],delete _["MANY_SEP"+N],delete _["AT_LEAST_ONE"+N],delete _["AT_LEAST_ONE_SEP"+N]}delete _.consume,delete _.subrule,delete _.option,delete _.or,delete _.many,delete _.atLeastOne,delete _.ACTION,delete _.BACKTRACK,delete _.LA})},x.prototype.ACTION_RECORD=function(_){},x.prototype.BACKTRACK_RECORD=function(_,A){return function(){return!0}},x.prototype.LA_RECORD=function(_){return o.END_OF_FILE},x.prototype.topLevelRuleRecord=function(_,A){try{var N=new t.Rule({definition:[],name:_});return N.name=_,this.recordingProdStack.push(N),A.call(this),this.recordingProdStack.pop(),N}catch(w){if(w.KNOWN_RECORDER_ERROR!==!0)try{w.message=w.message+`
	 This error was thrown during the "grammar recording phase" For more info see:
	https://chevrotain.io/docs/guide/internals.html#grammar-recording`}catch{throw w}throw w}},x.prototype.optionInternalRecord=function(_,A){return y.call(this,t.Option,_,A)},x.prototype.atLeastOneInternalRecord=function(_,A){y.call(this,t.RepetitionMandatory,A,_)},x.prototype.atLeastOneSepFirstInternalRecord=function(_,A){y.call(this,t.RepetitionMandatoryWithSeparator,A,_,a)},x.prototype.manyInternalRecord=function(_,A){y.call(this,t.Repetition,A,_)},x.prototype.manySepFirstInternalRecord=function(_,A){y.call(this,t.RepetitionWithSeparator,A,_,a)},x.prototype.orInternalRecord=function(_,A){return h.call(this,_,A)},x.prototype.subruleInternalRecord=function(_,A,N){if(E(A),!_||e.has(_,"ruleName")===!1){var w=new Error("<SUBRULE"+u(A)+"> argument is invalid"+(" expecting a Parser method reference but got: <"+JSON.stringify(_)+">")+(`
 inside top level rule: <`+this.recordingProdStack[0].name+">"));throw w.KNOWN_RECORDER_ERROR=!0,w}var O=e.peek(this.recordingProdStack),T=_.ruleName,M=new t.NonTerminal({idx:A,nonTerminalName:T,referencedRule:void 0});return O.definition.push(M),this.outputCst?m:l},x.prototype.consumeInternalRecord=function(_,A,N){if(E(A),!r.hasShortKeyProperty(_)){var w=new Error("<CONSUME"+u(A)+"> argument is invalid"+(" expecting a TokenType reference but got: <"+JSON.stringify(_)+">")+(`
 inside top level rule: <`+this.recordingProdStack[0].name+">"));throw w.KNOWN_RECORDER_ERROR=!0,w}var O=e.peek(this.recordingProdStack),T=new t.Terminal({idx:A,terminalType:_});return O.definition.push(T),f},x})();n.GastRecorder=g;function y(x,_,A,N){N===void 0&&(N=!1),E(A);var w=e.peek(this.recordingProdStack),O=e.isFunction(_)?_:_.DEF,T=new x({definition:[],idx:A});return N&&(T.separator=_.SEP),e.has(_,"MAX_LOOKAHEAD")&&(T.maxLookahead=_.MAX_LOOKAHEAD),this.recordingProdStack.push(T),O.call(this),w.definition.push(T),this.recordingProdStack.pop(),l}function h(x,_){var A=this;E(_);var N=e.peek(this.recordingProdStack),w=e.isArray(x)===!1,O=w===!1?x:x.DEF,T=new t.Alternation({definition:[],idx:_,ignoreAmbiguities:w&&x.IGNORE_AMBIGUITIES===!0});e.has(x,"MAX_LOOKAHEAD")&&(T.maxLookahead=x.MAX_LOOKAHEAD);var M=e.some(O,function(R){return e.isFunction(R.GATE)});return T.hasPredicates=M,N.definition.push(T),e.forEach(O,function(R){var I=new t.Alternative({definition:[]});T.definition.push(I),e.has(R,"IGNORE_AMBIGUITIES")?I.ignoreAmbiguities=R.IGNORE_AMBIGUITIES:e.has(R,"GATE")&&(I.ignoreAmbiguities=!0),A.recordingProdStack.push(I),R.ALT.call(A),A.recordingProdStack.pop()}),l}function u(x){return x===0?"":""+x}function E(x){if(x<0||x>d){var _=new Error("Invalid DSL Method idx value: <"+x+`>
	`+("Idx value must be a none negative value smaller than "+(d+1)));throw _.KNOWN_RECORDER_ERROR=!0,_}}}),v_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.PerformanceTracer=void 0;var e=st(),t=nn(),i=(function(){function r(){}return r.prototype.initPerformanceTracer=function(s){if(e.has(s,"traceInitPerf")){var o=s.traceInitPerf,c=typeof o=="number";this.traceInitMaxIdent=c?o:1/0,this.traceInitPerf=c?o>0:o}else this.traceInitMaxIdent=0,this.traceInitPerf=t.DEFAULT_PARSER_CONFIG.traceInitPerf;this.traceInitIndent=-1},r.prototype.TRACE_INIT=function(s,o){if(this.traceInitPerf===!0){this.traceInitIndent++;var c=new Array(this.traceInitIndent+1).join("	");this.traceInitIndent<this.traceInitMaxIdent&&console.log(c+"--> <"+s+">");var l=e.timer(o),a=l.time,d=l.value,p=a>10?console.warn:console.log;return this.traceInitIndent<this.traceInitMaxIdent&&p(c+"<-- <"+s+"> time: "+a+"ms"),this.traceInitIndent--,d}else return o()},r})();n.PerformanceTracer=i}),x_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.applyMixins=void 0;function e(t,i){i.forEach(function(r){var s=r.prototype;Object.getOwnPropertyNames(s).forEach(function(o){if(o!=="constructor"){var c=Object.getOwnPropertyDescriptor(s,o);c&&(c.get||c.set)?Object.defineProperty(t.prototype,o,c):t.prototype[o]=r.prototype[o]}})})}n.applyMixins=e}),nn=je(n=>{"use strict";var e=n&&n.__extends||(function(){var w=function(O,T){return w=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(M,R){M.__proto__=R}||function(M,R){for(var I in R)Object.prototype.hasOwnProperty.call(R,I)&&(M[I]=R[I])},w(O,T)};return function(O,T){if(typeof T!="function"&&T!==null)throw new TypeError("Class extends value "+String(T)+" is not a constructor or null");w(O,T);function M(){this.constructor=O}O.prototype=T===null?Object.create(T):(M.prototype=T.prototype,new M)}})();Object.defineProperty(n,"__esModule",{value:!0}),n.EmbeddedActionsParser=n.CstParser=n.Parser=n.EMPTY_ALT=n.ParserDefinitionErrorType=n.DEFAULT_RULE_CONFIG=n.DEFAULT_PARSER_CONFIG=n.END_OF_FILE=void 0;var t=st(),i=o_(),r=Ei(),s=$o(),o=c_(),c=Xu(),l=l_(),a=d_(),d=f_(),p=p_(),f=m_(),m=g_(),g=__(),y=y_(),h=v_(),u=x_();n.END_OF_FILE=r.createTokenInstance(r.EOF,"",NaN,NaN,NaN,NaN,NaN,NaN),Object.freeze(n.END_OF_FILE),n.DEFAULT_PARSER_CONFIG=Object.freeze({recoveryEnabled:!1,maxLookahead:3,dynamicTokensEnabled:!1,outputCst:!0,errorMessageProvider:s.defaultParserErrorProvider,nodeLocationTracking:"none",traceInitPerf:!1,skipValidations:!1}),n.DEFAULT_RULE_CONFIG=Object.freeze({recoveryValueFunc:function(){},resyncEnabled:!0});var E;(function(w){w[w.INVALID_RULE_NAME=0]="INVALID_RULE_NAME",w[w.DUPLICATE_RULE_NAME=1]="DUPLICATE_RULE_NAME",w[w.INVALID_RULE_OVERRIDE=2]="INVALID_RULE_OVERRIDE",w[w.DUPLICATE_PRODUCTIONS=3]="DUPLICATE_PRODUCTIONS",w[w.UNRESOLVED_SUBRULE_REF=4]="UNRESOLVED_SUBRULE_REF",w[w.LEFT_RECURSION=5]="LEFT_RECURSION",w[w.NONE_LAST_EMPTY_ALT=6]="NONE_LAST_EMPTY_ALT",w[w.AMBIGUOUS_ALTS=7]="AMBIGUOUS_ALTS",w[w.CONFLICT_TOKENS_RULES_NAMESPACE=8]="CONFLICT_TOKENS_RULES_NAMESPACE",w[w.INVALID_TOKEN_NAME=9]="INVALID_TOKEN_NAME",w[w.NO_NON_EMPTY_LOOKAHEAD=10]="NO_NON_EMPTY_LOOKAHEAD",w[w.AMBIGUOUS_PREFIX_ALTS=11]="AMBIGUOUS_PREFIX_ALTS",w[w.TOO_MANY_ALTS=12]="TOO_MANY_ALTS"})(E=n.ParserDefinitionErrorType||(n.ParserDefinitionErrorType={}));function x(w){return w===void 0&&(w=void 0),function(){return w}}n.EMPTY_ALT=x;var _=(function(){function w(O,T){this.definitionErrors=[],this.selfAnalysisDone=!1;var M=this;if(M.initErrorHandler(T),M.initLexerAdapter(),M.initLooksAhead(T),M.initRecognizerEngine(O,T),M.initRecoverable(T),M.initTreeBuilder(T),M.initContentAssist(),M.initGastRecorder(T),M.initPerformanceTracer(T),t.has(T,"ignoredIssues"))throw new Error(`The <ignoredIssues> IParserConfig property has been deprecated.
	Please use the <IGNORE_AMBIGUITIES> flag on the relevant DSL method instead.
	See: https://chevrotain.io/docs/guide/resolving_grammar_errors.html#IGNORING_AMBIGUITIES
	For further details.`);this.skipValidations=t.has(T,"skipValidations")?T.skipValidations:n.DEFAULT_PARSER_CONFIG.skipValidations}return w.performSelfAnalysis=function(O){throw Error("The **static** `performSelfAnalysis` method has been deprecated.	\nUse the **instance** method with the same name instead.")},w.prototype.performSelfAnalysis=function(){var O=this;this.TRACE_INIT("performSelfAnalysis",function(){var T;O.selfAnalysisDone=!0;var M=O.className;O.TRACE_INIT("toFastProps",function(){t.toFastProperties(O)}),O.TRACE_INIT("Grammar Recording",function(){try{O.enableRecording(),t.forEach(O.definedRulesNames,function(I){var U=O[I],P=U.originalGrammarAction,X=void 0;O.TRACE_INIT(I+" Rule",function(){X=O.topLevelRuleRecord(I,P)}),O.gastProductionsCache[I]=X})}finally{O.disableRecording()}});var R=[];if(O.TRACE_INIT("Grammar Resolving",function(){R=o.resolveGrammar({rules:t.values(O.gastProductionsCache)}),O.definitionErrors=O.definitionErrors.concat(R)}),O.TRACE_INIT("Grammar Validations",function(){if(t.isEmpty(R)&&O.skipValidations===!1){var I=o.validateGrammar({rules:t.values(O.gastProductionsCache),maxLookahead:O.maxLookahead,tokenTypes:t.values(O.tokensMap),errMsgProvider:s.defaultGrammarValidatorErrorProvider,grammarName:M});O.definitionErrors=O.definitionErrors.concat(I)}}),t.isEmpty(O.definitionErrors)&&(O.recoveryEnabled&&O.TRACE_INIT("computeAllProdsFollows",function(){var I=i.computeAllProdsFollows(t.values(O.gastProductionsCache));O.resyncFollows=I}),O.TRACE_INIT("ComputeLookaheadFunctions",function(){O.preComputeLookaheadFunctions(t.values(O.gastProductionsCache))})),!w.DEFER_DEFINITION_ERRORS_HANDLING&&!t.isEmpty(O.definitionErrors))throw T=t.map(O.definitionErrors,function(I){return I.message}),new Error(`Parser Definition Errors detected:
 `+T.join(`
-------------------------------
`))})},w.DEFER_DEFINITION_ERRORS_HANDLING=!1,w})();n.Parser=_,u.applyMixins(_,[c.Recoverable,l.LooksAhead,a.TreeBuilder,d.LexerAdapter,f.RecognizerEngine,p.RecognizerApi,m.ErrorHandler,g.ContentAssist,y.GastRecorder,h.PerformanceTracer]);var A=(function(w){e(O,w);function O(T,M){M===void 0&&(M=n.DEFAULT_PARSER_CONFIG);var R=this,I=t.cloneObj(M);return I.outputCst=!0,R=w.call(this,T,I)||this,R}return O})(_);n.CstParser=A;var N=(function(w){e(O,w);function O(T,M){M===void 0&&(M=n.DEFAULT_PARSER_CONFIG);var R=this,I=t.cloneObj(M);return I.outputCst=!1,R=w.call(this,T,I)||this,R}return O})(_);n.EmbeddedActionsParser=N}),E_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.createSyntaxDiagramsCode=void 0;var e=Bu();function t(i,r){var s=r===void 0?{}:r,o=s.resourceBase,c=o===void 0?"https://unpkg.com/chevrotain@"+e.VERSION+"/diagrams/":o,l=s.css,a=l===void 0?"https://unpkg.com/chevrotain@"+e.VERSION+"/diagrams/diagrams.css":l,d=`
<!-- This is a generated file -->
<!DOCTYPE html>
<meta charset="utf-8">
<style>
  body {
    background-color: hsl(30, 20%, 95%)
  }
</style>

`,p=`
<link rel='stylesheet' href='`+a+`'>
`,f=`
<script src='`+c+`vendor/railroad-diagrams.js'><\/script>
<script src='`+c+`src/diagrams_builder.js'><\/script>
<script src='`+c+`src/diagrams_behavior.js'><\/script>
<script src='`+c+`src/main.js'><\/script>
`,m=`
<div id="diagrams" align="center"></div>
`,g=`
<script>
    window.serializedGrammar = `+JSON.stringify(i,null,"  ")+`;
<\/script>
`,y=`
<script>
    var diagramsDiv = document.getElementById("diagrams");
    main.drawDiagramsFromSerializedGrammar(serializedGrammar, diagramsDiv);
<\/script>
`;return d+p+f+m+g+y}n.createSyntaxDiagramsCode=t}),S_=je(n=>{"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.Parser=n.createSyntaxDiagramsCode=n.clearCache=n.GAstVisitor=n.serializeProduction=n.serializeGrammar=n.Terminal=n.Rule=n.RepetitionWithSeparator=n.RepetitionMandatoryWithSeparator=n.RepetitionMandatory=n.Repetition=n.Option=n.NonTerminal=n.Alternative=n.Alternation=n.defaultLexerErrorProvider=n.NoViableAltException=n.NotAllInputParsedException=n.MismatchedTokenException=n.isRecognitionException=n.EarlyExitException=n.defaultParserErrorProvider=n.tokenName=n.tokenMatcher=n.tokenLabel=n.EOF=n.createTokenInstance=n.createToken=n.LexerDefinitionErrorType=n.Lexer=n.EMPTY_ALT=n.ParserDefinitionErrorType=n.EmbeddedActionsParser=n.CstParser=n.VERSION=void 0;var e=Bu();Object.defineProperty(n,"VERSION",{enumerable:!0,get:function(){return e.VERSION}});var t=nn();Object.defineProperty(n,"CstParser",{enumerable:!0,get:function(){return t.CstParser}}),Object.defineProperty(n,"EmbeddedActionsParser",{enumerable:!0,get:function(){return t.EmbeddedActionsParser}}),Object.defineProperty(n,"ParserDefinitionErrorType",{enumerable:!0,get:function(){return t.ParserDefinitionErrorType}}),Object.defineProperty(n,"EMPTY_ALT",{enumerable:!0,get:function(){return t.EMPTY_ALT}});var i=jo();Object.defineProperty(n,"Lexer",{enumerable:!0,get:function(){return i.Lexer}}),Object.defineProperty(n,"LexerDefinitionErrorType",{enumerable:!0,get:function(){return i.LexerDefinitionErrorType}});var r=Ei();Object.defineProperty(n,"createToken",{enumerable:!0,get:function(){return r.createToken}}),Object.defineProperty(n,"createTokenInstance",{enumerable:!0,get:function(){return r.createTokenInstance}}),Object.defineProperty(n,"EOF",{enumerable:!0,get:function(){return r.EOF}}),Object.defineProperty(n,"tokenLabel",{enumerable:!0,get:function(){return r.tokenLabel}}),Object.defineProperty(n,"tokenMatcher",{enumerable:!0,get:function(){return r.tokenMatcher}}),Object.defineProperty(n,"tokenName",{enumerable:!0,get:function(){return r.tokenName}});var s=$o();Object.defineProperty(n,"defaultParserErrorProvider",{enumerable:!0,get:function(){return s.defaultParserErrorProvider}});var o=es();Object.defineProperty(n,"EarlyExitException",{enumerable:!0,get:function(){return o.EarlyExitException}}),Object.defineProperty(n,"isRecognitionException",{enumerable:!0,get:function(){return o.isRecognitionException}}),Object.defineProperty(n,"MismatchedTokenException",{enumerable:!0,get:function(){return o.MismatchedTokenException}}),Object.defineProperty(n,"NotAllInputParsedException",{enumerable:!0,get:function(){return o.NotAllInputParsedException}}),Object.defineProperty(n,"NoViableAltException",{enumerable:!0,get:function(){return o.NoViableAltException}});var c=Vu();Object.defineProperty(n,"defaultLexerErrorProvider",{enumerable:!0,get:function(){return c.defaultLexerErrorProvider}});var l=Zt();Object.defineProperty(n,"Alternation",{enumerable:!0,get:function(){return l.Alternation}}),Object.defineProperty(n,"Alternative",{enumerable:!0,get:function(){return l.Alternative}}),Object.defineProperty(n,"NonTerminal",{enumerable:!0,get:function(){return l.NonTerminal}}),Object.defineProperty(n,"Option",{enumerable:!0,get:function(){return l.Option}}),Object.defineProperty(n,"Repetition",{enumerable:!0,get:function(){return l.Repetition}}),Object.defineProperty(n,"RepetitionMandatory",{enumerable:!0,get:function(){return l.RepetitionMandatory}}),Object.defineProperty(n,"RepetitionMandatoryWithSeparator",{enumerable:!0,get:function(){return l.RepetitionMandatoryWithSeparator}}),Object.defineProperty(n,"RepetitionWithSeparator",{enumerable:!0,get:function(){return l.RepetitionWithSeparator}}),Object.defineProperty(n,"Rule",{enumerable:!0,get:function(){return l.Rule}}),Object.defineProperty(n,"Terminal",{enumerable:!0,get:function(){return l.Terminal}});var a=Zt();Object.defineProperty(n,"serializeGrammar",{enumerable:!0,get:function(){return a.serializeGrammar}}),Object.defineProperty(n,"serializeProduction",{enumerable:!0,get:function(){return a.serializeProduction}});var d=Qr();Object.defineProperty(n,"GAstVisitor",{enumerable:!0,get:function(){return d.GAstVisitor}});function p(){console.warn(`The clearCache function was 'soft' removed from the Chevrotain API.
	 It performs no action other than printing this message.
	 Please avoid using it as it will be completely removed in the future`)}n.clearCache=p;var f=E_();Object.defineProperty(n,"createSyntaxDiagramsCode",{enumerable:!0,get:function(){return f.createSyntaxDiagramsCode}});var m=(function(){function g(){throw new Error(`The Parser class has been deprecated, use CstParser or EmbeddedActionsParser instead.
See: https://chevrotain.io/docs/changes/BREAKING_CHANGES.html#_7-0-0`)}return g})();n.Parser=m}),or=S_();var ta=class extends Kt{constructor(e){super(e)}load(e,t,i,r){let s=this,o=s.path===""?Gr.extractUrlBase(e):s.path,c=new Fr(s.manager);c.setPath(s.path),c.setRequestHeader(s.requestHeader),c.setWithCredentials(s.withCredentials),c.load(e,function(l){try{t(s.parse(l,o))}catch(a){r?r(a):console.error(a),s.manager.itemError(e)}},i,r)}parse(e,t){let i={};function r(S){let v=s(),b=new Pc(v.tokens),D=new Lc(v.tokenVocabulary),L=o(D.getBaseCstVisitorConstructor()),F=b.lex(S);D.input=F.tokens;let H=D.vrml();if(D.errors.length>0)throw console.error(D.errors),Error("THREE.VRMLLoader: Parsing errors detected.");return L.visit(H)}function s(){let S=or.createToken,v=S({name:"RouteIdentifier",pattern:/[^\x30-\x39\0-\x20\x22\x27\x23\x2b\x2c\x2d\x2e\x5b\x5d\x5c\x7b\x7d][^\0-\x20\x22\x27\x23\x2b\x2c\x2d\x2e\x5b\x5d\x5c\x7b\x7d]*[\.][^\x30-\x39\0-\x20\x22\x27\x23\x2b\x2c\x2d\x2e\x5b\x5d\x5c\x7b\x7d][^\0-\x20\x22\x27\x23\x2b\x2c\x2d\x2e\x5b\x5d\x5c\x7b\x7d]*/}),b=S({name:"Identifier",pattern:/[^\x30-\x39\0-\x20\x22\x27\x23\x2b\x2c\x2d\x2e\x5b\x5d\x5c\x7b\x7d]([^\0-\x20\x22\x27\x23\x2b\x2c\x2e\x5b\x5d\x5c\x7b\x7d])*/,longer_alt:v}),D=["Anchor","Billboard","Collision","Group","Transform","Inline","LOD","Switch","AudioClip","DirectionalLight","PointLight","Script","Shape","Sound","SpotLight","WorldInfo","CylinderSensor","PlaneSensor","ProximitySensor","SphereSensor","TimeSensor","TouchSensor","VisibilitySensor","Box","Cone","Cylinder","ElevationGrid","Extrusion","IndexedFaceSet","IndexedLineSet","PointSet","Sphere","Color","Coordinate","Normal","TextureCoordinate","Appearance","FontStyle","ImageTexture","Material","MovieTexture","PixelTexture","TextureTransform","ColorInterpolator","CoordinateInterpolator","NormalInterpolator","OrientationInterpolator","PositionInterpolator","ScalarInterpolator","Background","Fog","NavigationInfo","Viewpoint","Text"],L=S({name:"Version",pattern:/#VRML.*/,longer_alt:b}),F=S({name:"NodeName",pattern:new RegExp(D.join("|")),longer_alt:b}),H=S({name:"DEF",pattern:/DEF/,longer_alt:b}),z=S({name:"USE",pattern:/USE/,longer_alt:b}),j=S({name:"ROUTE",pattern:/ROUTE/,longer_alt:b}),te=S({name:"TO",pattern:/TO/,longer_alt:b}),Q=S({name:"StringLiteral",pattern:/"(?:[^\\"\n\r]|\\[bfnrtv"\\/]|\\u[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])*"/}),ce=S({name:"HexLiteral",pattern:/0[xX][0-9a-fA-F]+/}),Ee=S({name:"NumberLiteral",pattern:/[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?/}),Se=S({name:"TrueLiteral",pattern:/TRUE/}),pe=S({name:"FalseLiteral",pattern:/FALSE/}),xe=S({name:"NullLiteral",pattern:/NULL/}),V=S({name:"LSquare",pattern:/\[/}),le=S({name:"RSquare",pattern:/]/}),fe=S({name:"LCurly",pattern:/{/}),ge=S({name:"RCurly",pattern:/}/}),he=S({name:"Comment",pattern:/#.*/,group:or.Lexer.SKIPPED}),Te=[S({name:"WhiteSpace",pattern:/[ ,\s]/,group:or.Lexer.SKIPPED}),F,H,z,j,te,Se,pe,xe,L,b,v,Q,ce,Ee,V,le,fe,ge,he],Fe={};for(let De=0,ve=Te.length;De<ve;De++){let Ie=Te[De];Fe[Ie.name]=Ie}return{tokens:Te,tokenVocabulary:Fe}}function o(S){class v extends S{constructor(){super(),this.validateVisitor()}vrml(L){let F={version:this.visit(L.version),nodes:[],routes:[]};for(let H=0,z=L.node.length;H<z;H++){let j=L.node[H];F.nodes.push(this.visit(j))}if(L.route)for(let H=0,z=L.route.length;H<z;H++){let j=L.route[H];F.routes.push(this.visit(j))}return F}version(L){return L.Version[0].image}node(L){let F={name:L.NodeName[0].image,fields:[]};if(L.field)for(let H=0,z=L.field.length;H<z;H++){let j=L.field[H];F.fields.push(this.visit(j))}return L.def&&(F.DEF=this.visit(L.def[0])),F}field(L){let F={name:L.Identifier[0].image,type:null,values:null},H;return L.singleFieldValue&&(H=this.visit(L.singleFieldValue[0])),L.multiFieldValue&&(H=this.visit(L.multiFieldValue[0])),F.type=H.type,F.values=H.values,F}def(L){return(L.Identifier||L.NodeName)[0].image}use(L){return{USE:(L.Identifier||L.NodeName)[0].image}}singleFieldValue(L){return b(this,L)}multiFieldValue(L){return b(this,L)}route(L){return{FROM:L.RouteIdentifier[0].image,TO:L.RouteIdentifier[1].image}}}function b(D,L){let F={type:null,values:[]};if(L.node){F.type="node";for(let H=0,z=L.node.length;H<z;H++){let j=L.node[H];F.values.push(D.visit(j))}}if(L.use){F.type="use";for(let H=0,z=L.use.length;H<z;H++){let j=L.use[H];F.values.push(D.visit(j))}}if(L.StringLiteral){F.type="string";for(let H=0,z=L.StringLiteral.length;H<z;H++){let j=L.StringLiteral[H];F.values.push(j.image.replace(/'|"/g,""))}}if(L.NumberLiteral){F.type="number";for(let H=0,z=L.NumberLiteral.length;H<z;H++){let j=L.NumberLiteral[H];F.values.push(parseFloat(j.image))}}if(L.HexLiteral){F.type="hex";for(let H=0,z=L.HexLiteral.length;H<z;H++){let j=L.HexLiteral[H];F.values.push(j.image)}}if(L.TrueLiteral){F.type="boolean";for(let H=0,z=L.TrueLiteral.length;H<z;H++)L.TrueLiteral[H].image==="TRUE"&&F.values.push(!0)}if(L.FalseLiteral){F.type="boolean";for(let H=0,z=L.FalseLiteral.length;H<z;H++)L.FalseLiteral[H].image==="FALSE"&&F.values.push(!1)}return L.NullLiteral&&(F.type="null",L.NullLiteral.forEach(function(){F.values.push(null)})),F}return new v}function c(S){let v=S.nodes,b=new ui;for(let D=0,L=v.length;D<L;D++){let F=v[D];l(F)}for(let D=0,L=v.length;D<L;D++){let F=v[D],H=a(F);H instanceof Et&&b.add(H),F.name==="WorldInfo"&&(b.userData.worldInfo=H)}return b}function l(S){S.DEF&&(i[S.DEF]=S);let v=S.fields;for(let b=0,D=v.length;b<D;b++){let L=v[b];if(L.type==="node"){let F=L.values;for(let H=0,z=F.length;H<z;H++)l(F[H])}}}function a(S){return S.USE?W(S.USE):(S.build!==void 0||(S.build=d(S)),S.build)}function d(S){let v=S.name,b;switch(v){case"Anchor":case"Group":case"Transform":case"Collision":b=p(S);break;case"Background":b=f(S);break;case"Shape":b=m(S);break;case"Appearance":b=g(S);break;case"Material":b=y(S);break;case"ImageTexture":b=x(S);break;case"PixelTexture":b=E(S);break;case"TextureTransform":b=_(S);break;case"IndexedFaceSet":b=w(S);break;case"IndexedLineSet":b=O(S);break;case"PointSet":b=T(S);break;case"Box":b=M(S);break;case"Cone":b=R(S);break;case"Cylinder":b=I(S);break;case"Sphere":b=U(S);break;case"ElevationGrid":b=P(S);break;case"Extrusion":b=X(S);break;case"Color":case"Coordinate":case"Normal":case"TextureCoordinate":b=A(S);break;case"WorldInfo":b=N(S);break;case"Billboard":case"Inline":case"LOD":case"Switch":case"AudioClip":case"DirectionalLight":case"PointLight":case"Script":case"Sound":case"SpotLight":case"CylinderSensor":case"PlaneSensor":case"ProximitySensor":case"SphereSensor":case"TimeSensor":case"TouchSensor":case"VisibilitySensor":case"Text":case"FontStyle":case"MovieTexture":case"ColorInterpolator":case"CoordinateInterpolator":case"NormalInterpolator":case"OrientationInterpolator":case"PositionInterpolator":case"ScalarInterpolator":case"Fog":case"NavigationInfo":case"Viewpoint":break;default:console.warn("THREE.VRMLLoader: Unknown node:",v);break}return b!==void 0&&S.DEF!==void 0&&b.hasOwnProperty("name")===!0&&(b.name=S.DEF),b}function p(S){let v=new gn,b=S.fields;for(let D=0,L=b.length;D<L;D++){let F=b[D],H=F.name,z=F.values;switch(H){case"bboxCenter":break;case"bboxSize":break;case"center":break;case"children":q(z,v);break;case"description":break;case"collide":break;case"parameter":break;case"rotation":let j=new Z(z[0],z[1],z[2]).normalize(),te=z[3];v.quaternion.setFromAxisAngle(j,te);break;case"scale":v.scale.set(z[0],z[1],z[2]);break;case"scaleOrientation":break;case"translation":v.position.set(z[0],z[1],z[2]);break;case"proxy":break;case"url":break;default:console.warn("THREE.VRMLLoader: Unknown field:",H);break}}return v}function f(S){let v=new gn,b,D,L,F,H=S.fields;for(let j=0,te=H.length;j<te;j++){let Q=H[j],ce=Q.name,Ee=Q.values;switch(ce){case"groundAngle":b=Ee;break;case"groundColor":D=Ee;break;case"backUrl":break;case"bottomUrl":break;case"frontUrl":break;case"leftUrl":break;case"rightUrl":break;case"topUrl":break;case"skyAngle":L=Ee;break;case"skyColor":F=Ee;break;default:console.warn("THREE.VRMLLoader: Unknown field:",ce);break}}let z=1e4;if(F){let j=new di(z,32,16),te=new En({fog:!1,side:wt,depthWrite:!1,depthTest:!1});F.length>3?(Re(j,z,L,Oe(F),!0),te.vertexColors=!0):te.color.setRGB(F[0],F[1],F[2],pt);let Q=new Lt(j,te);v.add(Q)}if(D&&D.length>0){let j=new di(z,32,16,0,2*Math.PI,.5*Math.PI,1.5*Math.PI),te=new En({fog:!1,side:wt,vertexColors:!0,depthWrite:!1,depthTest:!1});Re(j,z,b,Oe(D),!1);let Q=new Lt(j,te);v.add(Q)}return v.renderOrder=-1/0,v}function m(S){let v=S.fields,b=new En({name:Kt.DEFAULT_MATERIAL_NAME,color:0}),D;for(let F=0,H=v.length;F<H;F++){let z=v[F],j=z.name,te=z.values;switch(j){case"appearance":te[0]!==null&&(b=a(te[0]));break;case"geometry":te[0]!==null&&(D=a(te[0]));break;default:console.warn("THREE.VRMLLoader: Unknown field:",j);break}}let L;if(D&&D.attributes.position){let F=D._type;if(F==="points"){let H=new Yi({name:Kt.DEFAULT_MATERIAL_NAME,color:16777215,opacity:b.opacity,transparent:b.transparent});D.attributes.color!==void 0?H.vertexColors=!0:b.isMeshPhongMaterial&&H.color.copy(b.emissive),L=new Rr(D,H)}else if(F==="line"){let H=new Xi({name:Kt.DEFAULT_MATERIAL_NAME,color:16777215,opacity:b.opacity,transparent:b.transparent});D.attributes.color!==void 0?H.vertexColors=!0:b.isMeshPhongMaterial&&H.color.copy(b.emissive),L=new Ar(D,H)}else D._solid!==void 0&&(b.side=D._solid?un:en),D.attributes.color!==void 0&&(b.vertexColors=!0),L=new Lt(D,b)}else L=new Et,L.visible=!1;return L}function g(S){let v=new Dr,b,D=S.fields;for(let L=0,F=D.length;L<F;L++){let H=D[L],z=H.name,j=H.values;switch(z){case"material":if(j[0]!==null){let Q=a(j[0]);Q.diffuseColor&&v.color.copy(Q.diffuseColor),Q.emissiveColor&&v.emissive.copy(Q.emissiveColor),Q.shininess&&(v.shininess=Q.shininess),Q.specularColor&&v.specular.copy(Q.specularColor),Q.transparency&&(v.opacity=1-Q.transparency),Q.transparency>0&&(v.transparent=!0)}else v=new En({name:Kt.DEFAULT_MATERIAL_NAME,color:0});break;case"texture":let te=j[0];te!==null&&(te.name==="ImageTexture"||te.name==="PixelTexture")&&(v.map=a(te));break;case"textureTransform":j[0]!==null&&(b=a(j[0]));break;default:console.warn("THREE.VRMLLoader: Unknown field:",z);break}}if(v.map){if(v.map.__type){switch(v.map.__type){case mn.INTENSITY_ALPHA:v.opacity=1;break;case mn.RGB:v.color.set(16777215);break;case mn.RGBA:v.color.set(16777215),v.opacity=1;break;default:}delete v.map.__type}b&&(v.map.center.copy(b.center),v.map.rotation=b.rotation,v.map.repeat.copy(b.scale),v.map.offset.copy(b.translation))}return v}function y(S){let v={},b=S.fields;for(let D=0,L=b.length;D<L;D++){let F=b[D],H=F.name,z=F.values;switch(H){case"ambientIntensity":break;case"diffuseColor":v.diffuseColor=new qe().setRGB(z[0],z[1],z[2],pt);break;case"emissiveColor":v.emissiveColor=new qe().setRGB(z[0],z[1],z[2],pt);break;case"shininess":v.shininess=z[0];break;case"specularColor":v.specularColor=new qe().setRGB(z[0],z[1],z[2],pt);break;case"transparency":v.transparency=z[0];break;default:console.warn("THREE.VRMLLoader: Unknown field:",H);break}}return v}function h(S,v,b){let D;switch(v){case mn.INTENSITY:D=parseInt(S),b.r=D,b.g=D,b.b=D,b.a=1;break;case mn.INTENSITY_ALPHA:D=parseInt("0x"+S.substring(2,4)),b.r=D,b.g=D,b.b=D,b.a=parseInt("0x"+S.substring(4,6));break;case mn.RGB:b.r=parseInt("0x"+S.substring(2,4)),b.g=parseInt("0x"+S.substring(4,6)),b.b=parseInt("0x"+S.substring(6,8)),b.a=1;break;case mn.RGBA:b.r=parseInt("0x"+S.substring(2,4)),b.g=parseInt("0x"+S.substring(4,6)),b.b=parseInt("0x"+S.substring(6,8)),b.a=parseInt("0x"+S.substring(8,10));break;default:}}function u(S){let v;switch(S){case 1:v=mn.INTENSITY;break;case 2:v=mn.INTENSITY_ALPHA;break;case 3:v=mn.RGB;break;case 4:v=mn.RGBA;break;default:}return v}function E(S){let v,b=Ln,D=Ln,L=S.fields;for(let F=0,H=L.length;F<H;F++){let z=L[F],j=z.name,te=z.values;switch(j){case"image":let Q=te[0],ce=te[1],Ee=te[2],Se=u(Ee),pe=new Uint8Array(4*Q*ce),xe={r:0,g:0,b:0,a:0};for(let V=3,le=0,fe=te.length;V<fe;V++,le++){h(te[V],Se,xe);let ge=le*4;pe[ge+0]=xe.r,pe[ge+1]=xe.g,pe[ge+2]=xe.b,pe[ge+3]=xe.a}v=new br(pe,Q,ce),v.colorSpace=pt,v.needsUpdate=!0,v.__type=Se;break;case"repeatS":te[0]===!1&&(b=Yt);break;case"repeatT":te[0]===!1&&(D=Yt);break;default:console.warn("THREE.VRMLLoader: Unknown field:",j);break}}return v&&(v.wrapS=b,v.wrapT=D),v}function x(S){let v,b=Ln,D=Ln,L=S.fields;for(let F=0,H=L.length;F<H;F++){let z=L[F],j=z.name,te=z.values;switch(j){case"url":let Q=te[0];Q&&(v=He.load(Q));break;case"repeatS":te[0]===!1&&(b=Yt);break;case"repeatT":te[0]===!1&&(D=Yt);break;default:console.warn("THREE.VRMLLoader: Unknown field:",j);break}}return v&&(v.wrapS=b,v.wrapT=D,v.colorSpace=pt),v}function _(S){let v={center:new ze,rotation:new ze,scale:new ze,translation:new ze},b=S.fields;for(let D=0,L=b.length;D<L;D++){let F=b[D],H=F.name,z=F.values;switch(H){case"center":v.center.set(z[0],z[1]);break;case"rotation":v.rotation=z[0];break;case"scale":v.scale.set(z[0],z[1]);break;case"translation":v.translation.set(z[0],z[1]);break;default:console.warn("THREE.VRMLLoader: Unknown field:",H);break}}return v}function A(S){return S.fields[0].values}function N(S){let v={},b=S.fields;for(let D=0,L=b.length;D<L;D++){let F=b[D],H=F.name,z=F.values;switch(H){case"title":v.title=z[0];break;case"info":v.info=z;break;default:console.warn("THREE.VRMLLoader: Unknown field:",H);break}}return v}function w(S){let v,b,D,L,F=!0,H=!0,z=0,j,te,Q,ce,Ee=!0,Se=!0,pe=S.fields;for(let oe=0,Te=pe.length;oe<Te;oe++){let Fe=pe[oe],De=Fe.name,ve=Fe.values;switch(De){case"color":let Ie=ve[0];Ie!==null&&(v=a(Ie));break;case"coord":let be=ve[0];be!==null&&(b=a(be));break;case"normal":let Be=ve[0];Be!==null&&(D=a(Be));break;case"texCoord":let ke=ve[0];ke!==null&&(L=a(ke));break;case"ccw":F=ve[0];break;case"colorIndex":j=ve;break;case"colorPerVertex":Ee=ve[0];break;case"convex":break;case"coordIndex":te=ve;break;case"creaseAngle":z=ve[0];break;case"normalIndex":Q=ve;break;case"normalPerVertex":Se=ve[0];break;case"solid":H=ve[0];break;case"texCoordIndex":ce=ve;break;default:console.warn("THREE.VRMLLoader: Unknown field:",De);break}}if(te===void 0)return console.warn("THREE.VRMLLoader: Missing coordIndex."),new Tt;let xe=G(te,F),V,le,fe;if(v){if(Ee===!0)if(j&&j.length>0){let oe=G(j,F);V=ie(xe,oe,v,3)}else V=we(xe,new Qe(v,3));else if(j&&j.length>0){let oe=ae(v,j),Te=ee(oe,te);V=de(xe,Te)}else{let oe=ee(v,te);V=de(xe,oe)}Je(V)}if(D)if(Se===!0)if(Q&&Q.length>0){let oe=G(Q,F);le=ie(xe,oe,D,3)}else le=we(xe,new Qe(D,3));else if(Q&&Q.length>0){let oe=ae(D,Q),Te=ee(oe,te);le=de(xe,Te)}else{let oe=ee(D,te);le=de(xe,oe)}else le=Ne(xe,b,z);if(L)if(ce&&ce.length>0){let oe=G(ce,F);fe=ie(xe,oe,L,2)}else fe=we(xe,new Qe(L,2));let ge=new Tt,he=we(xe,new Qe(b,3));return ge.setAttribute("position",he),ge.setAttribute("normal",le),V&&ge.setAttribute("color",V),fe&&ge.setAttribute("uv",fe),ge._solid=H,ge._type="mesh",ge}function O(S){let v,b,D,L,F=!0,H=S.fields;for(let ce=0,Ee=H.length;ce<Ee;ce++){let Se=H[ce],pe=Se.name,xe=Se.values;switch(pe){case"color":let V=xe[0];V!==null&&(v=a(V));break;case"coord":let le=xe[0];le!==null&&(b=a(le));break;case"colorIndex":D=xe;break;case"colorPerVertex":F=xe[0];break;case"coordIndex":L=xe;break;default:console.warn("THREE.VRMLLoader: Unknown field:",pe);break}}let z,j=ue(L);if(v){if(F===!0)if(D.length>0){let ce=ue(D);z=ie(j,ce,v,3)}else z=we(j,new Qe(v,3));else if(D.length>0){let ce=ae(v,D),Ee=_e(ce,L);z=Le(j,Ee)}else{let ce=_e(v,L);z=Le(j,ce)}Je(z)}let te=new Tt,Q=we(j,new Qe(b,3));return te.setAttribute("position",Q),z&&te.setAttribute("color",z),te._type="line",te}function T(S){let v,b,D=S.fields;for(let F=0,H=D.length;F<H;F++){let z=D[F],j=z.name,te=z.values;switch(j){case"color":let Q=te[0];Q!==null&&(v=a(Q));break;case"coord":let ce=te[0];ce!==null&&(b=a(ce));break;default:console.warn("THREE.VRMLLoader: Unknown field:",j);break}}let L=new Tt;if(L.setAttribute("position",new Qe(b,3)),v){let F=new Qe(v,3);Je(F),L.setAttribute("color",F)}return L._type="points",L}function M(S){let v=new Z(2,2,2),b=S.fields;for(let L=0,F=b.length;L<F;L++){let H=b[L],z=H.name,j=H.values;z==="size"?(v.x=j[0],v.y=j[1],v.z=j[2]):console.warn("THREE.VRMLLoader: Unknown field:",z)}return new qn(v.x,v.y,v.z)}function R(S){let v=1,b=2,D=!1,L=S.fields;for(let H=0,z=L.length;H<z;H++){let j=L[H],te=j.name,Q=j.values;switch(te){case"bottom":D=!Q[0];break;case"bottomRadius":v=Q[0];break;case"height":b=Q[0];break;case"side":break;default:console.warn("THREE.VRMLLoader: Unknown field:",te);break}}return new Cr(v,b,16,1,D)}function I(S){let v=1,b=2,D=S.fields;for(let F=0,H=D.length;F<H;F++){let z=D[F],j=z.name,te=z.values;switch(j){case"bottom":break;case"radius":v=te[0];break;case"height":b=te[0];break;case"side":break;case"top":break;default:console.warn("THREE.VRMLLoader: Unknown field:",j);break}}return new qi(v,v,b,16,1)}function U(S){let v=1,b=S.fields;for(let L=0,F=b.length;L<F;L++){let H=b[L],z=H.name,j=H.values;z==="radius"?v=j[0]:console.warn("THREE.VRMLLoader: Unknown field:",z)}return new di(v,16,16)}function P(S){let v,b,D,L,F=!0,H=!0,z=!0,j=!0,te=0,Q=2,ce=2,Ee=1,Se=1,pe=S.fields;for(let ve=0,Ie=pe.length;ve<Ie;ve++){let be=pe[ve],Be=be.name,ke=be.values;switch(Be){case"color":let ut=ke[0];ut!==null&&(v=a(ut));break;case"normal":let rn=ke[0];rn!==null&&(b=a(rn));break;case"texCoord":let sn=ke[0];sn!==null&&(D=a(sn));break;case"height":L=ke;break;case"ccw":j=ke[0];break;case"colorPerVertex":F=ke[0];break;case"creaseAngle":te=ke[0];break;case"normalPerVertex":H=ke[0];break;case"solid":z=ke[0];break;case"xDimension":Q=ke[0];break;case"xSpacing":Ee=ke[0];break;case"zDimension":ce=ke[0];break;case"zSpacing":Se=ke[0];break;default:console.warn("THREE.VRMLLoader: Unknown field:",Be);break}}let xe=[],V=[],le=[],fe=[];for(let ve=0;ve<ce;ve++)for(let Ie=0;Ie<Q;Ie++){let be=ve*Q+Ie,Be=Ee*ve,ke=L[be],ut=Se*Ie;if(xe.push(Be,ke,ut),v&&F===!0){let rn=v[be*3+0],sn=v[be*3+1],Un=v[be*3+2];le.push(rn,sn,Un)}if(b&&H===!0){let rn=b[be*3+0],sn=b[be*3+1],Un=b[be*3+2];V.push(rn,sn,Un)}if(D){let rn=D[be*2+0],sn=D[be*2+1];fe.push(rn,sn)}else fe.push(ve/(Q-1),Ie/(ce-1))}let ge=[];for(let ve=0;ve<Q-1;ve++)for(let Ie=0;Ie<ce-1;Ie++){let be=ve+Ie*Q,Be=ve+(Ie+1)*Q,ke=ve+1+(Ie+1)*Q,ut=ve+1+Ie*Q;j===!0?(ge.push(be,ke,Be),ge.push(ke,be,ut)):(ge.push(be,Be,ke),ge.push(ke,ut,be))}let he=we(ge,new Qe(xe,3)),oe=we(ge,new Qe(fe,2)),Te,Fe;if(v){if(F===!1){for(let ve=0;ve<Q-1;ve++)for(let Ie=0;Ie<ce-1;Ie++){let be=ve+Ie*(Q-1),Be=v[be*3+0],ke=v[be*3+1],ut=v[be*3+2];le.push(Be,ke,ut),le.push(Be,ke,ut),le.push(Be,ke,ut),le.push(Be,ke,ut),le.push(Be,ke,ut),le.push(Be,ke,ut)}Te=new Qe(le,3)}else Te=we(ge,new Qe(le,3));Je(Te)}if(b)if(H===!1){for(let ve=0;ve<Q-1;ve++)for(let Ie=0;Ie<ce-1;Ie++){let be=ve+Ie*(Q-1),Be=b[be*3+0],ke=b[be*3+1],ut=b[be*3+2];V.push(Be,ke,ut),V.push(Be,ke,ut),V.push(Be,ke,ut),V.push(Be,ke,ut),V.push(Be,ke,ut),V.push(Be,ke,ut)}Fe=new Qe(V,3)}else Fe=we(ge,new Qe(V,3));else Fe=Ne(ge,xe,te);let De=new Tt;return De.setAttribute("position",he),De.setAttribute("normal",Fe),De.setAttribute("uv",oe),Te&&De.setAttribute("color",Te),De._solid=z,De._type="mesh",De}function X(S){let v=[1,1,1,-1,-1,-1,-1,1,1,1],b=[0,0,0,0,1,0],D,L,F=!0,H=!0,z=0,j=!0,te=!0,Q=S.fields;for(let De=0,ve=Q.length;De<ve;De++){let Ie=Q[De],be=Ie.name,Be=Ie.values;switch(be){case"beginCap":F=Be[0];break;case"ccw":H=Be[0];break;case"convex":break;case"creaseAngle":z=Be[0];break;case"crossSection":v=Be;break;case"endCap":j=Be[0];break;case"orientation":L=Be;break;case"scale":D=Be;break;case"solid":te=Be[0];break;case"spine":b=Be;break;default:console.warn("THREE.VRMLLoader: Unknown field:",be);break}}let ce=v[0]===v[v.length-2]&&v[1]===v[v.length-1],Ee=[],Se=new Z,pe=new Z,xe=new Z,V=new Z,le=new zt;for(let De=0,ve=0,Ie=0,be=b.length;De<be;De+=3,ve+=2,Ie+=4){Se.fromArray(b,De),pe.x=D?D[ve+0]:1,pe.y=1,pe.z=D?D[ve+1]:1,xe.x=L?L[Ie+0]:0,xe.y=L?L[Ie+1]:0,xe.z=L?L[Ie+2]:1;let Be=L?L[Ie+3]:0;for(let ke=0,ut=v.length;ke<ut;ke+=2)V.x=v[ke+0],V.y=0,V.z=v[ke+1],V.multiply(pe),le.setFromAxisAngle(xe,Be),V.applyQuaternion(le),V.add(Se),Ee.push(V.x,V.y,V.z)}let fe=[],ge=b.length/3,he=v.length/2;for(let De=0;De<ge-1;De++)for(let ve=0;ve<he-1;ve++){let Ie=ve+De*he,be=ve+1+De*he,Be=ve+(De+1)*he,ke=ve+1+(De+1)*he;ve===he-2&&ce===!0&&(be=De*he,ke=(De+1)*he),H===!0?(fe.push(Ie,be,Be),fe.push(Be,be,ke)):(fe.push(Ie,Be,be),fe.push(Be,ke,be))}if(F===!0||j===!0){let De=[];for(let be=0,Be=v.length;be<Be;be+=2)De.push(new ze(v[be],v[be+1]));let ve=Nr.triangulateShape(De,[]),Ie=[];for(let be=0,Be=ve.length;be<Be;be++){let ke=ve[be];Ie.push(ke[0],ke[1],ke[2])}if(F===!0)for(let be=0,Be=Ie.length;be<Be;be+=3)H===!0?fe.push(Ie[be+0],Ie[be+1],Ie[be+2]):fe.push(Ie[be+0],Ie[be+2],Ie[be+1]);if(j===!0){let be=he*(ge-1);for(let Be=0,ke=Ie.length;Be<ke;Be+=3)H===!0?fe.push(be+Ie[Be+0],be+Ie[Be+2],be+Ie[Be+1]):fe.push(be+Ie[Be+0],be+Ie[Be+1],be+Ie[Be+2])}}let oe=we(fe,new Qe(Ee,3)),Te=Ne(fe,Ee,z),Fe=new Tt;return Fe.setAttribute("position",oe),Fe.setAttribute("normal",Te),Fe._solid=te,Fe._type="mesh",Fe}function W(S){let v=i[S],b=a(v);return b.isObject3D||b.isMaterial?b.clone():b}function q(S,v){for(let b=0,D=S.length;b<D;b++){let L=a(S[b]);L instanceof Et&&v.add(L)}}function G(S,v){let b=[],D=0;for(let L=0,F=S.length;L<F;L++){let H=S[D],z=S[L+(v?1:2)],j=S[L+(v?2:1)];b.push(H,z,j),(S[L+3]===-1||L+3>=F)&&(L+=3,D=L+1)}return b}function ee(S,v){let b=[],D=0;for(let L=0,F=v.length;L<F;L++){let H=D*3,z=S[H],j=S[H+1],te=S[H+2];b.push(z,j,te),(v[L+3]===-1||L+3>=F)&&(L+=3,D++)}return b}function ae(S,v){let b=[];for(let D=0,L=v.length;D<L;D++){let H=v[D]*3,z=S[H],j=S[H+1],te=S[H+2];b.push(z,j,te)}return b}function ue(S){let v=[];for(let b=0,D=S.length;b<D;b++){let L=S[b],F=S[b+1];v.push(L,F),(S[b+2]===-1||b+2>=D)&&(b+=2)}return v}function _e(S,v){let b=[],D=0;for(let L=0,F=v.length;L<F;L++){let H=D*3,z=S[H],j=S[H+1],te=S[H+2];b.push(z,j,te),(v[L+2]===-1||L+2>=F)&&(L+=2,D++)}return b}let me=new Z,Me=new Z,k=new Z,Y=new ze,K=new ze,ne=new ze;function ie(S,v,b,D){let L=[];for(let F=0,H=S.length;F<H;F+=3){let z=v[F],j=v[F+1],te=v[F+2];D===2?(Y.fromArray(b,z*D),K.fromArray(b,j*D),ne.fromArray(b,te*D),L.push(Y.x,Y.y),L.push(K.x,K.y),L.push(ne.x,ne.y)):(me.fromArray(b,z*D),Me.fromArray(b,j*D),k.fromArray(b,te*D),L.push(me.x,me.y,me.z),L.push(Me.x,Me.y,Me.z),L.push(k.x,k.y,k.z))}return new Qe(L,D)}function de(S,v){let b=[];for(let D=0,L=0,F=S.length;D<F;D+=3,L++)me.fromArray(v,L*3),b.push(me.x,me.y,me.z),b.push(me.x,me.y,me.z),b.push(me.x,me.y,me.z);return new Qe(b,3)}function Le(S,v){let b=[];for(let D=0,L=0,F=S.length;D<F;D+=2,L++)me.fromArray(v,L*3),b.push(me.x,me.y,me.z),b.push(me.x,me.y,me.z);return new Qe(b,3)}function we(S,v){let b=v.array,D=v.itemSize,L=new b.constructor(S.length*D),F=0,H=0;for(let z=0,j=S.length;z<j;z++){F=S[z]*D;for(let te=0;te<D;te++)L[H++]=b[F++]}return new Qe(L,D)}let B=new Z,Ge=new Z;function Ne(S,v,b){let D=[],L={};for(let H=0,z=S.length;H<z;H+=3){let j=S[H],te=S[H+1],Q=S[H+2],ce=new Nc(j,te,Q);me.fromArray(v,j*3),Me.fromArray(v,te*3),k.fromArray(v,Q*3),Ge.subVectors(k,Me),B.subVectors(me,Me),Ge.cross(B),Ge.normalize(),ce.normal.copy(Ge),L[j]===void 0&&(L[j]=[]),L[te]===void 0&&(L[te]=[]),L[Q]===void 0&&(L[Q]=[]),L[j].push(ce.normal),L[te].push(ce.normal),L[Q].push(ce.normal),D.push(ce)}let F=[];for(let H=0,z=D.length;H<z;H++){let j=D[H],te=Ke(L[j.a],j.normal,b),Q=Ke(L[j.b],j.normal,b),ce=Ke(L[j.c],j.normal,b);me.fromArray(v,j.a*3),Me.fromArray(v,j.b*3),k.fromArray(v,j.c*3),F.push(te.x,te.y,te.z),F.push(Q.x,Q.y,Q.z),F.push(ce.x,ce.y,ce.z)}return new Qe(F,3)}function Ke(S,v,b){let D=new Z;if(b===0)D.copy(v);else for(let L=0,F=S.length;L<F;L++)S[L].angleTo(v)<b&&D.add(S[L]);return D.normalize()}function Oe(S){let v=[];for(let b=0,D=S.length;b<D;b+=3)v.push(new qe(S[b],S[b+1],S[b+2]));return v}function Je(S){let v=new qe;for(let b=0;b<S.count;b++)v.fromBufferAttribute(S,b),nt.colorSpaceToWorking(v,pt),S.setXYZ(b,v.r,v.g,v.b)}function Re(S,v,b,D,L){let F=[],H=L===!0?0:Math.PI;for(let Ee=0,Se=D.length;Ee<Se;Ee++){let pe=Ee===0?0:b[Ee-1];pe=L===!0?pe:H-pe;let xe=new Z;xe.setFromSphericalCoords(v,pe,0),F.push(xe)}let z=S.index,j=S.attributes.position,te=new Ut(new Float32Array(S.attributes.position.count*3),3),Q=new Z,ce=new qe;for(let Ee=0;Ee<z.count;Ee++){let Se=z.getX(Ee);Q.fromBufferAttribute(j,Se);let pe,xe,V=1;for(let ge=1;ge<F.length;ge++){pe=ge-1,xe=ge;let he=F[pe],oe=F[xe];if(L===!0){if(Q.y<=he.y&&Q.y>oe.y){V=Math.abs(he.y-Q.y)/Math.abs(he.y-oe.y);break}}else if(Q.y>=he.y&&Q.y<oe.y){V=Math.abs(he.y-Q.y)/Math.abs(he.y-oe.y);break}}let le=D[pe],fe=D[xe];ce.copy(le).lerp(fe,V),nt.colorSpaceToWorking(ce,pt),te.setXYZ(Se,ce.r,ce.g,ce.b)}S.setAttribute("color",te)}let He=new kr(this.manager);if(He.setPath(this.resourcePath||t).setCrossOrigin(this.crossOrigin),e.indexOf("#VRML V2.0")===-1)throw Error("THREE.VRMLLexer: Version of VRML asset not supported.");let ot=r(e);return c(ot)}},Pc=class{constructor(e){this.lexer=new or.Lexer(e)}lex(e){let t=this.lexer.tokenize(e);if(t.errors.length>0)throw console.error(t.errors),Error("THREE.VRMLLexer: Lexing errors detected.");return t}},T_=or.CstParser,Lc=class extends T_{constructor(e){super(e);let t=this,i=e.Version,r=e.LCurly,s=e.RCurly,o=e.LSquare,c=e.RSquare,l=e.Identifier,a=e.RouteIdentifier,d=e.StringLiteral,p=e.HexLiteral,f=e.NumberLiteral,m=e.TrueLiteral,g=e.FalseLiteral,y=e.NullLiteral,h=e.DEF,u=e.USE,E=e.ROUTE,x=e.TO,_=e.NodeName;t.RULE("vrml",function(){t.SUBRULE(t.version),t.AT_LEAST_ONE(function(){t.SUBRULE(t.node)}),t.MANY(function(){t.SUBRULE(t.route)})}),t.RULE("version",function(){t.CONSUME(i)}),t.RULE("node",function(){t.OPTION(function(){t.SUBRULE(t.def)}),t.CONSUME(_),t.CONSUME(r),t.MANY(function(){t.SUBRULE(t.field)}),t.CONSUME(s)}),t.RULE("field",function(){t.CONSUME(l),t.OR2([{ALT:function(){t.SUBRULE(t.singleFieldValue)}},{ALT:function(){t.SUBRULE(t.multiFieldValue)}}])}),t.RULE("def",function(){t.CONSUME(h),t.OR([{ALT:function(){t.CONSUME(l)}},{ALT:function(){t.CONSUME(_)}}])}),t.RULE("use",function(){t.CONSUME(u),t.OR([{ALT:function(){t.CONSUME(l)}},{ALT:function(){t.CONSUME(_)}}])}),t.RULE("singleFieldValue",function(){t.AT_LEAST_ONE(function(){t.OR([{ALT:function(){t.SUBRULE(t.node)}},{ALT:function(){t.SUBRULE(t.use)}},{ALT:function(){t.CONSUME(d)}},{ALT:function(){t.CONSUME(p)}},{ALT:function(){t.CONSUME(f)}},{ALT:function(){t.CONSUME(m)}},{ALT:function(){t.CONSUME(g)}},{ALT:function(){t.CONSUME(y)}}])})}),t.RULE("multiFieldValue",function(){t.CONSUME(o),t.MANY(function(){t.OR([{ALT:function(){t.SUBRULE(t.node)}},{ALT:function(){t.SUBRULE(t.use)}},{ALT:function(){t.CONSUME(d)}},{ALT:function(){t.CONSUME(p)}},{ALT:function(){t.CONSUME(f)}},{ALT:function(){t.CONSUME(y)}}])}),t.CONSUME(c)}),t.RULE("route",function(){t.CONSUME(E),t.CONSUME(a),t.CONSUME(x),t.CONSUME2(a)}),this.performSelfAnalysis()}},Nc=class{constructor(e,t,i){this.a=e,this.b=t,this.c=i,this.normal=new Z}},mn={INTENSITY:1,INTENSITY_ALPHA:2,RGB:3,RGBA:4};function M_(n){let e=Uint8Array.from(atob(n.trim()),t=>t.charCodeAt(0));return new TextDecoder().decode(e)}function b_(n,e,t){let i=new vn().setFromObject(t),r=i.getCenter(new Z),s=Math.max(i.getSize(new Z).length(),1);return n.near=Math.max(s/1e3,.01),n.far=s*100,n.position.copy(r).add(new Z(s*.9,-s*.9,s*.72)),e.target.copy(r),e.update(),()=>{n.position.copy(r).add(new Z(s*.9,-s*.9,s*.72)),e.target.copy(r),e.update()}}function A_(n,e){let t=document.getElementById(n),i=document.getElementById(e);if(!t||!i||!window.WebGLRenderingContext)return!1;let r;try{r=new ta().parse(M_(i.textContent||""))}catch{return t.dataset.viewerStatus="parse-failed",!1}let s=new ui;s.background=new qe(1120295);let o=new Pt(36,1,.1,1e4),c=new Yo({antialias:!0});c.setPixelRatio(Math.min(window.devicePixelRatio||1,2)),c.outputColorSpace=pt,t.appendChild(c.domElement),s.add(r),s.add(new zr(16777215,1516884,2.4));let l=new Zi(16777215,3);l.position.set(120,-140,180),s.add(l);let a=new Zi(9684477,1);a.position.set(-100,70,60),s.add(a);let d=new Zo(o,c.domElement);d.enableDamping=!0,d.dampingFactor=.08,d.minDistance=1,d.maxDistance=1e4;let p=b_(o,d,r),f=()=>{let g=Math.max(t.clientWidth,320),y=Math.max(t.clientHeight,360);(c.domElement.width!==g||c.domElement.height!==y)&&(c.setSize(g,y,!1),o.aspect=g/y,o.updateProjectionMatrix()),d.update(),c.render(s,o),requestAnimationFrame(f)};c.domElement.addEventListener("dblclick",p);let m=t.querySelector("img");return m&&(m.hidden=!0),t.dataset.viewerStatus="ready",f(),!0}return rh(R_);})();
