export const id=2939;export const ids=[2939];export const modules={87190:(e,i,t)=>{var s=t(85461),a=t(98597),d=t(196),l=t(45081),r=t(33167),n=t(19263),o=t(66412),c=t(38848),u=t(40884);t(66442),t(9484);const h=e=>a.qy`<ha-list-item .twoline=${!!e.area}>
    <span>${e.name}</span>
    <span slot="secondary">${e.area}</span>
  </ha-list-item>`;(0,s.A)([(0,d.EM)("ha-device-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Array,attribute:"exclude-devices"})],key:"excludeDevices",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,d.wk)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,d.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_init",value(){return!1}},{kind:"field",key:"_getDevices",value(){return(0,l.A)(((e,i,t,s,a,d,l,r,c)=>{if(!e.length)return[{id:"no_devices",area:"",name:this.hass.localize("ui.components.device-picker.no_devices"),strings:[]}];let h={};(s||a||d||r)&&(h=(0,u.g2)(t));let v=e.filter((e=>e.id===this.value||!e.disabled_by));s&&(v=v.filter((e=>{const i=h[e.id];return!(!i||!i.length)&&h[e.id].some((e=>s.includes((0,n.m)(e.entity_id))))}))),a&&(v=v.filter((e=>{const i=h[e.id];return!i||!i.length||t.every((e=>!a.includes((0,n.m)(e.entity_id))))}))),c&&(v=v.filter((e=>!c.includes(e.id)))),d&&(v=v.filter((e=>{const i=h[e.id];return!(!i||!i.length)&&h[e.id].some((e=>{const i=this.hass.states[e.entity_id];return!!i&&(i.attributes.device_class&&d.includes(i.attributes.device_class))}))}))),r&&(v=v.filter((e=>{const i=h[e.id];return!(!i||!i.length)&&i.some((e=>{const i=this.hass.states[e.entity_id];return!!i&&r(i)}))}))),l&&(v=v.filter((e=>e.id===this.value||l(e))));const k=v.map((e=>{const t=(0,u.xn)(e,this.hass,h[e.id]);return{id:e.id,name:t,area:e.area_id&&i[e.area_id]?i[e.area_id].name:this.hass.localize("ui.components.device-picker.no_area"),strings:[t||""]}}));return k.length?1===k.length?k:k.sort(((e,i)=>(0,o.x)(e.name||"",i.name||"",this.hass.locale.language))):[{id:"no_devices",area:"",name:this.hass.localize("ui.components.device-picker.no_match"),strings:[]}]}))}},{kind:"method",key:"open",value:async function(){await this.updateComplete,await(this.comboBox?.open())}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this.comboBox?.focus())}},{kind:"method",key:"updated",value:function(e){if(!this._init&&this.hass||this._init&&e.has("_opened")&&this._opened){this._init=!0;const e=this._getDevices(Object.values(this.hass.devices),this.hass.areas,Object.values(this.hass.entities),this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.excludeDevices);this.comboBox.items=e,this.comboBox.filteredItems=e}}},{kind:"method",key:"render",value:function(){return a.qy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.device-picker.device"):this.label}
        .value=${this._value}
        .helper=${this.helper}
        .renderer=${h}
        .disabled=${this.disabled}
        .required=${this.required}
        item-id-path="id"
        item-value-path="id"
        item-label-path="name"
        @opened-changed=${this._openedChanged}
        @value-changed=${this._deviceChanged}
        @filter-changed=${this._filterChanged}
      ></ha-combo-box>
    `}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_filterChanged",value:function(e){const i=e.target,t=e.detail.value.toLowerCase();i.filteredItems=t.length?(0,c.H)(t,i.items||[]):i.items}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();let i=e.detail.value;"no_devices"===i&&(i=""),i!==this._value&&this._setValue(i)}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,r.r)(this,"value-changed",{value:e}),(0,r.r)(this,"change")}),0)}}]}}),a.WF)},12939:(e,i,t)=>{t.r(i),t.d(i,{HaDeviceSelector:()=>k});var s=t(85461),a=t(69534),d=t(98597),l=t(196),r=t(45081),n=t(96041),o=t(33167),c=t(40884),u=t(88502),h=t(81407),v=t(36831);t(87190);(0,s.A)([(0,l.EM)("ha-devices-picker")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"picked-device-label"})],key:"pickedDeviceLabel",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:"pick-device-label"})],key:"pickDeviceLabel",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return d.s6;const e=this._currentDevices;return d.qy`
      ${e.map((e=>d.qy`
          <div>
            <ha-device-picker
              allow-custom-entity
              .curValue=${e}
              .hass=${this.hass}
              .deviceFilter=${this.deviceFilter}
              .entityFilter=${this.entityFilter}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .value=${e}
              .label=${this.pickedDeviceLabel}
              .disabled=${this.disabled}
              @value-changed=${this._deviceChanged}
            ></ha-device-picker>
          </div>
        `))}
      <div>
        <ha-device-picker
          allow-custom-entity
          .hass=${this.hass}
          .helper=${this.helper}
          .deviceFilter=${this.deviceFilter}
          .entityFilter=${this.entityFilter}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .excludeDevices=${e}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .label=${this.pickDeviceLabel}
          .disabled=${this.disabled}
          .required=${this.required&&!e.length}
          @value-changed=${this._addDevice}
        ></ha-device-picker>
      </div>
    `}},{kind:"get",key:"_currentDevices",value:function(){return this.value||[]}},{kind:"method",key:"_updateDevices",value:async function(e){(0,o.r)(this,"value-changed",{value:e}),this.value=e}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();const i=e.currentTarget.curValue,t=e.detail.value;t!==i&&(void 0===t?this._updateDevices(this._currentDevices.filter((e=>e!==i))):this._updateDevices(this._currentDevices.map((e=>e===i?t:e))))}},{kind:"method",key:"_addDevice",value:async function(e){e.stopPropagation();const i=e.detail.value;if(e.currentTarget.value="",!i)return;const t=this._currentDevices;t.includes(i)||this._updateDevices([...t,i])}},{kind:"field",static:!0,key:"styles",value(){return d.AH`
    div {
      margin-top: 8px;
    }
  `}}]}}),d.WF);let k=(0,s.A)([(0,l.EM)("ha-selector-device")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",key:"_deviceIntegrationLookup",value(){return(0,r.A)(c.fk)}},{kind:"method",key:"_hasIntegration",value:function(e){return e.device?.filter&&(0,n.e)(e.device.filter).some((e=>e.integration))||e.device?.entity&&(0,n.e)(e.device.entity).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){e.has("selector")&&void 0!==this.value&&(this.selector.device?.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,o.r)(this,"value-changed",{value:this.value})):!this.selector.device?.multiple&&Array.isArray(this.value)&&(this.value=this.value[0],(0,o.r)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"updated",value:function(e){(0,a.A)(t,"updated",this,3)([e]),e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,u.c)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,h.VN)(this.hass).then((e=>{this._configEntries=e})))}},{kind:"method",key:"render",value:function(){return this._hasIntegration(this.selector)&&!this._entitySources?d.s6:this.selector.device?.multiple?d.qy`
      ${this.label?d.qy`<label>${this.label}</label>`:""}
      <ha-devices-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .deviceFilter=${this._filterDevices}
        .entityFilter=${this.selector.device?.entity?this._filterEntities:void 0}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-devices-picker>
    `:d.qy`
        <ha-device-picker
          .hass=${this.hass}
          .value=${this.value}
          .label=${this.label}
          .helper=${this.helper}
          .deviceFilter=${this._filterDevices}
          .entityFilter=${this.selector.device?.entity?this._filterEntities:void 0}
          .disabled=${this.disabled}
          .required=${this.required}
          allow-custom-entity
        ></ha-device-picker>
      `}},{kind:"field",key:"_filterDevices",value(){return e=>{if(!this.selector.device?.filter)return!0;const i=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,n.e)(this.selector.device.filter).some((t=>(0,v.vX)(t,e,i)))}}},{kind:"field",key:"_filterEntities",value(){return e=>(0,n.e)(this.selector.device.entity).some((i=>(0,v.Ru)(i,e,this._entitySources)))}}]}}),d.WF)},88502:(e,i,t)=>{t.d(i,{c:()=>d});const s=async(e,i,t,a,d,...l)=>{const r=d,n=r[e],o=n=>a&&a(d,n.result)!==n.cacheKey?(r[e]=void 0,s(e,i,t,a,d,...l)):n.result;if(n)return n instanceof Promise?n.then(o):o(n);const c=t(d,...l);return r[e]=c,c.then((t=>{r[e]={result:t,cacheKey:a?.(d,t)},setTimeout((()=>{r[e]=void 0}),i)}),(()=>{r[e]=void 0})),c},a=e=>e.callWS({type:"entity/source"}),d=e=>s("_entitySources",3e4,a,(e=>Object.keys(e.states).length),e)}};
//# sourceMappingURL=kLaTaf2V.js.map