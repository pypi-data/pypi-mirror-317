export const id=543;export const ids=[543];export const modules={10543:(e,i,t)=>{t.r(i),t.d(i,{HaConfigEntrySelector:()=>u});var n=t(85461),a=t(98597),o=t(196),r=(t(23981),t(33167)),s=t(66412),d=t(81407),l=t(31238),c=t(47424);t(66442);(0,n.A)([(0,o.EM)("ha-config-entry-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"integration",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"value",value(){return""}},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,o.P)("ha-combo-box")],key:"_comboBox",value:void 0},{kind:"method",key:"open",value:function(){this._comboBox?.open()}},{kind:"method",key:"focus",value:function(){this._comboBox?.focus()}},{kind:"method",key:"firstUpdated",value:function(){this._getConfigEntries()}},{kind:"field",key:"_rowRenderer",value(){return e=>a.qy`<mwc-list-item twoline graphic="icon">
      <span
        >${e.title||this.hass.localize("ui.panel.config.integrations.config_entry.unnamed_entry")}</span
      >
      <span slot="secondary">${e.localized_domain_name}</span>
      <img
        alt=""
        slot="graphic"
        src=${(0,c.MR)({domain:e.domain,type:"icon",darkOptimized:this.hass.themes?.darkMode})}
        crossorigin="anonymous"
        referrerpolicy="no-referrer"
        @error=${this._onImageError}
        @load=${this._onImageLoad}
      />
    </mwc-list-item>`}},{kind:"method",key:"render",value:function(){return this._configEntries?a.qy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.config-entry-picker.config_entry"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .renderer=${this._rowRenderer}
        .items=${this._configEntries}
        item-value-path="entry_id"
        item-id-path="entry_id"
        item-label-path="title"
        @value-changed=${this._valueChanged}
      ></ha-combo-box>
    `:a.s6}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.visibility="hidden"}},{kind:"method",key:"_getConfigEntries",value:async function(){(0,d.VN)(this.hass,{type:["device","hub","service"],domain:this.integration}).then((e=>{this._configEntries=e.map((e=>({...e,localized_domain_name:(0,l.p$)(this.hass.localize,e.domain)}))).sort(((e,i)=>(0,s.S)(e.localized_domain_name+e.title,i.localized_domain_name+i.title,this.hass.locale.language)))}))}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const i=e.detail.value;i!==this._value&&this._setValue(i)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,r.r)(this,"value-changed",{value:e}),(0,r.r)(this,"change")}),0)}}]}}),a.WF);let u=(0,n.A)([(0,o.EM)("ha-selector-config_entry")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return a.qy`<ha-config-entry-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      .integration=${this.selector.config_entry?.integration}
      allow-custom-entity
    ></ha-config-entry-picker>`}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    ha-config-entry-picker {
      width: 100%;
    }
  `}}]}}),a.WF)},31238:(e,i,t)=>{t.d(i,{QC:()=>o,fK:()=>a,p$:()=>n});const n=(e,i,t)=>e(`component.${i}.title`)||t?.name||i,a=(e,i)=>{const t={type:"manifest/list"};return i&&(t.integrations=i),e.callWS(t)},o=(e,i)=>e.callWS({type:"manifest/get",integration:i})},47424:(e,i,t)=>{t.d(i,{MR:()=>n,a_:()=>a,bg:()=>o});const n=e=>`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,a=e=>e.split("/")[4],o=e=>e.startsWith("https://brands.home-assistant.io/")}};
//# sourceMappingURL=vnuqhAfJ.js.map