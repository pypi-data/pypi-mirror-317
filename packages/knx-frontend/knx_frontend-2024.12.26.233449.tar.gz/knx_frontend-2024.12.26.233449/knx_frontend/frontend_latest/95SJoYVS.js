export const id=4817;export const ids=[4817];export const modules={95576:(e,t,r)=>{r.r(t),r.d(t,{HaLabelSelector:()=>d});var a=r(85461),l=r(98597),i=r(196),s=r(96041),n=r(33167);r(49549);let d=(0,a.A)([(0,i.EM)("ha-selector-label")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"name",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,i.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,i.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,i.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return this.selector.label.multiple?l.qy`
        <ha-labels-picker
          no-add
          .hass=${this.hass}
          .value=${(0,s.e)(this.value??[])}
          .disabled=${this.disabled}
          .label=${this.label}
          @value-changed=${this._handleChange}
        >
        </ha-labels-picker>
      `:l.qy`
      <ha-label-picker
        no-add
        .hass=${this.hass}
        .value=${this.value}
        .disabled=${this.disabled}
        .label=${this.label}
        @value-changed=${this._handleChange}
      >
      </ha-label-picker>
    `}},{kind:"method",key:"_handleChange",value:function(e){let t=e.detail.value;this.value!==t&&((""===t||Array.isArray(t)&&0===t.length)&&!this.required&&(t=void 0),(0,n.r)(this,"value-changed",{value:t}))}},{kind:"get",static:!0,key:"styles",value:function(){return l.AH`
      ha-labels-picker {
        display: block;
        width: 100%;
      }
    `}}]}}),l.WF)},44856:(e,t,r)=>{r.d(t,{N:()=>i});const a=e=>{let t=[];function r(r,a){e=a?r:Object.assign(Object.assign({},e),r);let l=t;for(let t=0;t<l.length;t++)l[t](e)}return{get state(){return e},action(t){function a(e){r(e,!1)}return function(){let r=[e];for(let e=0;e<arguments.length;e++)r.push(arguments[e]);let l=t.apply(this,r);if(null!=l)return l instanceof Promise?l.then(a):a(l)}},setState:r,clearState(){e=void 0},subscribe(e){return t.push(e),()=>{!function(e){let r=[];for(let a=0;a<t.length;a++)t[a]===e?e=null:r.push(t[a]);t=r}(e)}}}},l=(e,t,r,l,i={unsubGrace:!0})=>{if(e[t])return e[t];let s,n,d=0,o=a();const u=()=>{if(!r)throw new Error("Collection does not support refresh");return r(e).then((e=>o.setState(e,!0)))},c=()=>u().catch((t=>{if(e.connected)throw t})),h=()=>{n=void 0,s&&s.then((e=>{e()})),o.clearState(),e.removeEventListener("ready",u),e.removeEventListener("disconnected",v)},v=()=>{n&&(clearTimeout(n),h())};return e[t]={get state(){return o.state},refresh:u,subscribe(t){d++,1===d&&(()=>{if(void 0!==n)return clearTimeout(n),void(n=void 0);l&&(s=l(e,o)),r&&(e.addEventListener("ready",c),c()),e.addEventListener("disconnected",v)})();const a=o.subscribe(t);return void 0!==o.state&&setTimeout((()=>t(o.state)),0),()=>{a(),d--,d||(i.unsubGrace?n=setTimeout(h,5e3):h())}}},e[t]},i=(e,t,r,a,i)=>l(a,e,t,r).subscribe(i)}};
//# sourceMappingURL=95SJoYVS.js.map