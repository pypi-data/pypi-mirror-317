export const id=1940;export const ids=[1940];export const modules={1940:(e,i,t)=>{t.r(i),t.d(i,{HaTTSVoiceSelector:()=>l});var s=t(85461),a=t(98597),d=t(196);t(75973);let l=(0,s.A)([(0,d.EM)("ha-selector-tts_voice")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`<ha-tts-voice-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .language=${this.selector.tts_voice?.language||this.context?.language}
      .engineId=${this.selector.tts_voice?.engineId||this.context?.engineId}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-tts-voice-picker>`}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    ha-tts-picker {
      width: 100%;
    }
  `}}]}}),a.WF)},75973:(e,i,t)=>{var s=t(85461),a=t(69534),d=t(98597),l=t(196),o=t(33167),n=t(24517),u=t(11355),r=t(6933);t(9484),t(96334);const c="__NONE_OPTION__";(0,s.A)([(0,l.EM)("ha-tts-voice-picker")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,l.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"engineId",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.wk)()],key:"_voices",value:void 0},{kind:"field",decorators:[(0,l.P)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"render",value:function(){if(!this._voices)return d.s6;const e=this.value??(this.required?this._voices[0]?.voice_id:c);return d.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.tts-voice-picker.voice")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${n.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?d.s6:d.qy`<ha-list-item .value=${c}>
              ${this.hass.localize("ui.components.tts-voice-picker.none")}
            </ha-list-item>`}
        ${this._voices.map((e=>d.qy`<ha-list-item .value=${e.voice_id}>
              ${e.name}
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,a.A)(t,"willUpdate",this,3)([e]),this.hasUpdated?(e.has("language")||e.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}},{kind:"field",key:"_debouncedUpdateVoices",value(){return(0,u.s)((()=>this._updateVoices()),500)}},{kind:"method",key:"_updateVoices",value:async function(){this.engineId&&this.language?(this._voices=(await(0,r.z3)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((e=>e.voice_id===this.value))||(this.value=void 0,(0,o.r)(this,"value-changed",{value:this.value})))):this._voices=void 0}},{kind:"method",key:"updated",value:function(e){(0,a.A)(t,"updated",this,3)([e]),e.has("_voices")&&this._select?.value!==this.value&&(this._select?.layoutOptions(),(0,o.r)(this,"value-changed",{value:this._select?.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return d.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const i=e.target;!this.hass||""===i.value||i.value===this.value||void 0===this.value&&i.value===c||(this.value=i.value===c?void 0:i.value,(0,o.r)(this,"value-changed",{value:this.value}))}}]}}),d.WF)},6933:(e,i,t)=>{t.d(i,{EF:()=>l,S_:()=>s,Xv:()=>o,ni:()=>d,u1:()=>n,z3:()=>u});const s=(e,i)=>e.callApi("POST","tts_get_url",i),a="media-source://tts/",d=e=>e.startsWith(a),l=e=>e.substring(19),o=(e,i,t)=>e.callWS({type:"tts/engine/list",language:i,country:t}),n=(e,i)=>e.callWS({type:"tts/engine/get",engine_id:i}),u=(e,i,t)=>e.callWS({type:"tts/engine/voices",engine_id:i,language:t})}};
//# sourceMappingURL=vTM8CPc3.js.map