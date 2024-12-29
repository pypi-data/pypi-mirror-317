/*! For license information please see p51odqrB.js.LICENSE.txt */
export const id=8709;export const ids=[8709];export const modules={18709:(t,e,s)=>{s.r(e),s.d(e,{HaIconSelector:()=>c});var i=s(85461),n=s(98597),o=s(196),r=s(86625),a=s(33167),d=s(74538);s(45063);let c=(0,i.A)([(0,o.EM)("ha-selector-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){const t=this.context?.icon_entity,e=t?this.hass.states[t]:void 0,s=this.selector.icon?.placeholder||e?.attributes.icon||e&&(0,r.T)((0,d.fq)(this.hass,e));return n.qy`
      <ha-icon-picker
        .hass=${this.hass}
        .label=${this.label}
        .value=${this.value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .placeholder=${this.selector.icon?.placeholder??s}
        @value-changed=${this._valueChanged}
      >
        ${!s&&e?n.qy`
              <ha-state-icon
                slot="fallback"
                .hass=${this.hass}
                .stateObj=${e}
              ></ha-state-icon>
            `:n.s6}
      </ha-icon-picker>
    `}},{kind:"method",key:"_valueChanged",value:function(t){(0,a.r)(this,"value-changed",{value:t.detail.value})}}]}}),n.WF)},45063:(t,e,s)=>{var i=s(85461),n=s(98597),o=s(196),r=s(86625),a=s(93758),d=s(80085),c=s(74538);s(29222);(0,i.A)([(0,o.EM)("ha-state-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"stateValue",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"icon",value:void 0},{kind:"method",key:"render",value:function(){const t=this.icon||this.stateObj&&this.hass?.entities[this.stateObj.entity_id]?.icon||this.stateObj?.attributes.icon;if(t)return n.qy`<ha-icon .icon=${t}></ha-icon>`;if(!this.stateObj)return n.s6;if(!this.hass)return this._renderFallback();const e=(0,c.fq)(this.hass,this.stateObj,this.stateValue).then((t=>t?n.qy`<ha-icon .icon=${t}></ha-icon>`:this._renderFallback()));return n.qy`${(0,r.T)(e)}`}},{kind:"method",key:"_renderFallback",value:function(){const t=(0,d.t)(this.stateObj);return n.qy`
      <ha-svg-icon
        .path=${a.n_[t]||a.lW}
      ></ha-svg-icon>
    `}}]}}),n.WF)},86625:(t,e,s)=>{s.d(e,{T:()=>u});var i=s(34078),n=s(3982),o=s(3267);class r{constructor(t){this.G=t}disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}}class a{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null===(t=this.Z)||void 0===t||t.call(this),this.Y=this.Z=void 0}}var d=s(2154);const c=t=>!(0,n.sO)(t)&&"function"==typeof t.then,h=1073741823;class l extends o.Kq{constructor(){super(...arguments),this._$C_t=h,this._$Cwt=[],this._$Cq=new r(this),this._$CK=new a}render(...t){var e;return null!==(e=t.find((t=>!c(t))))&&void 0!==e?e:i.c0}update(t,e){const s=this._$Cwt;let n=s.length;this._$Cwt=e;const o=this._$Cq,r=this._$CK;this.isConnected||this.disconnected();for(let i=0;i<e.length&&!(i>this._$C_t);i++){const t=e[i];if(!c(t))return this._$C_t=i,t;i<n&&t===s[i]||(this._$C_t=h,n=0,Promise.resolve(t).then((async e=>{for(;r.get();)await r.get();const s=o.deref();if(void 0!==s){const i=s._$Cwt.indexOf(t);i>-1&&i<s._$C_t&&(s._$C_t=i,s.setValue(e))}})))}return i.c0}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const u=(0,d.u$)(l)}};
//# sourceMappingURL=p51odqrB.js.map