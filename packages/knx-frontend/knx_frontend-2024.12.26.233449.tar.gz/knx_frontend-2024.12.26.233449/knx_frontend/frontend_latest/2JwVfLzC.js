export const id=5519;export const ids=[5519];export const modules={32872:(e,o,s)=>{s.d(o,{x:()=>a});const a=(e,o)=>e&&e.config.components.includes(o)},14656:(e,o,s)=>{s.d(o,{v:()=>a});const a=(e,o,s,a)=>{const[i,t,d]=e.split(".",3);return Number(i)>o||Number(i)===o&&(void 0===a?Number(t)>=s:Number(t)>s)||void 0!==a&&Number(i)===o&&Number(t)===s&&Number(d)>=a}},55519:(e,o,s)=>{s.r(o),s.d(o,{HaAddonSelector:()=>c});var a=s(85461),i=s(98597),t=s(196),d=s(32872),r=s(33167),n=s(66412),l=s(14656),u=s(12263);s(91074),s(66442),s(9484);const h=e=>i.qy`<ha-list-item twoline graphic="icon">
    <span>${e.name}</span>
    <span slot="secondary">${e.slug}</span>
    ${e.icon?i.qy`<img
          alt=""
          slot="graphic"
          .src="/api/hassio/addons/${e.slug}/icon"
        />`:""}
  </ha-list-item>`;(0,a.A)([(0,t.EM)("ha-addon-picker")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"value",value(){return""}},{kind:"field",decorators:[(0,t.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,t.wk)()],key:"_addons",value:void 0},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,t.P)("ha-combo-box")],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,t.wk)()],key:"_error",value:void 0},{kind:"method",key:"open",value:function(){this._comboBox?.open()}},{kind:"method",key:"focus",value:function(){this._comboBox?.focus()}},{kind:"method",key:"firstUpdated",value:function(){this._getAddons()}},{kind:"method",key:"render",value:function(){return this._error?i.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:this._addons?i.qy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.addon-picker.addon"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .renderer=${h}
        .items=${this._addons}
        item-value-path="slug"
        item-id-path="slug"
        item-label-path="name"
        @value-changed=${this._addonChanged}
      ></ha-combo-box>
    `:i.s6}},{kind:"method",key:"_getAddons",value:async function(){try{if((0,d.x)(this.hass,"hassio")){const e=await(async e=>(0,l.v)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/addons",method:"get"}):(0,u.PS)(await e.callApi("GET","hassio/addons")))(this.hass);this._addons=e.addons.filter((e=>e.version)).sort(((e,o)=>(0,n.x)(e.name,o.name,this.hass.locale.language)))}else this._error=this.hass.localize("ui.components.addon-picker.error.no_supervisor")}catch(e){this._error=this.hass.localize("ui.components.addon-picker.error.fetch_addons")}}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_addonChanged",value:function(e){e.stopPropagation();const o=e.detail.value;o!==this._value&&this._setValue(o)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,r.r)(this,"value-changed",{value:e}),(0,r.r)(this,"change")}),0)}}]}}),i.WF);let c=(0,a.A)([(0,t.EM)("ha-selector-addon")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",decorators:[(0,t.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,t.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return i.qy`<ha-addon-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      allow-custom-entity
    ></ha-addon-picker>`}},{kind:"field",static:!0,key:"styles",value(){return i.AH`
    ha-addon-picker {
      width: 100%;
    }
  `}}]}}),i.WF)},12263:(e,o,s)=>{s.d(o,{PS:()=>a,VR:()=>i});const a=e=>e.data,i=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])}};
//# sourceMappingURL=2JwVfLzC.js.map