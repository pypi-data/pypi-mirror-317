/*! For license information please see HNMHdrw8.js.LICENSE.txt */
export const id=3069;export const ids=[3069];export const modules={68873:(e,t,i)=>{i.d(t,{a:()=>a});var s=i(6601),n=i(19263);function a(e,t){const i=(0,n.m)(e.entity_id),a=void 0!==t?t:e?.state;if(["button","event","input_button","scene"].includes(i))return a!==s.Hh;if((0,s.g0)(a))return!1;if(a===s.KF&&"alert"!==i)return!1;switch(i){case"alarm_control_panel":return"disarmed"!==a;case"alert":return"idle"!==a;case"cover":case"valve":return"closed"!==a;case"device_tracker":case"person":return"not_home"!==a;case"lawn_mower":return["mowing","error"].includes(a);case"lock":return"locked"!==a;case"media_player":return"standby"!==a;case"vacuum":return!["idle","docked","paused"].includes(a);case"plant":return"problem"===a;case"group":return["on","home","open","locked","problem"].includes(a);case"timer":return"active"===a;case"camera":return"streaming"===a}return!0}},18889:(e,t,i)=>{i.d(t,{n:()=>n});const s=/^(\w+)\.(\w+)$/,n=e=>s.test(e)},85067:(e,t,i)=>{var s=i(85461),n=(i(9484),i(98597)),a=i(196),r=i(45081),l=i(33167),d=i(19263),o=i(91330),u=i(38848),c=(i(66442),i(96396),i(29222),i(85426),i(66412));const h=()=>i.e(2882).then(i.bind(i,22882));var y=i(31238),v=i(23135);const k="___create-new-entity___";(0,s.A)([(0,a.EM)("ha-entity-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array})],key:"createDomains",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"include-unit-of-measurement"})],key:"includeUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"include-entities"})],key:"includeEntities",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,attribute:"exclude-entities"})],key:"excludeEntities",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"hideClearIcon",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({attribute:"item-label-path"})],key:"itemLabelPath",value(){return"friendly_name"}},{kind:"field",decorators:[(0,a.wk)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,a.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"method",key:"open",value:async function(){await this.updateComplete,await(this.comboBox?.open())}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this.comboBox?.focus())}},{kind:"field",key:"_initedStates",value(){return!1}},{kind:"field",key:"_states",value(){return[]}},{kind:"field",key:"_rowRenderer",value(){return e=>n.qy`<ha-list-item graphic="avatar" .twoline=${!!e.entity_id}>
      ${e.state?n.qy`<state-badge
            slot="graphic"
            .stateObj=${e}
            .hass=${this.hass}
          ></state-badge>`:""}
      <span>${e.friendly_name}</span>
      <span slot="secondary"
        >${e.entity_id.startsWith(k)?this.hass.localize("ui.components.entity.entity-picker.new_entity"):e.entity_id}</span
      >
    </ha-list-item>`}},{kind:"field",key:"_getStates",value(){return(0,r.A)(((e,t,i,s,n,a,r,l,u,h)=>{let m=[];if(!t)return[];let p=Object.keys(t.states);const f=h?.length?h.map((e=>{const i=t.localize("ui.components.entity.entity-picker.create_helper",{domain:(0,v.z)(e)?t.localize(`ui.panel.config.helpers.types.${e}`):(0,y.p$)(t.localize,e)});return{entity_id:k+e,state:"on",last_changed:"",last_updated:"",context:{id:"",user_id:null,parent_id:null},friendly_name:i,attributes:{icon:"mdi:plus"},strings:[e,i]}})):[];return p.length?(l&&(p=p.filter((e=>l.includes(e)))),u&&(p=p.filter((e=>!u.includes(e)))),i&&(p=p.filter((e=>i.includes((0,d.m)(e))))),s&&(p=p.filter((e=>!s.includes((0,d.m)(e))))),m=p.map((e=>{const i=(0,o.u)(t.states[e])||e;return{...t.states[e],friendly_name:i,strings:[e,i]}})).sort(((e,t)=>(0,c.S)(e.friendly_name,t.friendly_name,this.hass.locale.language))),a&&(m=m.filter((e=>e.entity_id===this.value||e.attributes.device_class&&a.includes(e.attributes.device_class)))),r&&(m=m.filter((e=>e.entity_id===this.value||e.attributes.unit_of_measurement&&r.includes(e.attributes.unit_of_measurement)))),n&&(m=m.filter((e=>e.entity_id===this.value||n(e)))),m.length?(f?.length&&m.push(...f),m):[{entity_id:"",state:"",last_changed:"",last_updated:"",context:{id:"",user_id:null,parent_id:null},friendly_name:this.hass.localize("ui.components.entity.entity-picker.no_match"),attributes:{friendly_name:this.hass.localize("ui.components.entity.entity-picker.no_match"),icon:"mdi:magnify"},strings:[]},...f]):[{entity_id:"",state:"",last_changed:"",last_updated:"",context:{id:"",user_id:null,parent_id:null},friendly_name:this.hass.localize("ui.components.entity.entity-picker.no_entities"),attributes:{friendly_name:this.hass.localize("ui.components.entity.entity-picker.no_entities"),icon:"mdi:magnify"},strings:[]},...f]}))}},{kind:"method",key:"shouldUpdate",value:function(e){return!!(e.has("value")||e.has("label")||e.has("disabled"))||!(!e.has("_opened")&&this._opened)}},{kind:"method",key:"willUpdate",value:function(e){(!this._initedStates||e.has("_opened")&&this._opened)&&(this._states=this._getStates(this._opened,this.hass,this.includeDomains,this.excludeDomains,this.entityFilter,this.includeDeviceClasses,this.includeUnitOfMeasurement,this.includeEntities,this.excludeEntities,this.createDomains),this._initedStates&&(this.comboBox.filteredItems=this._states),this._initedStates=!0),e.has("createDomains")&&this.createDomains?.length&&this.hass.loadFragmentTranslation("config")}},{kind:"method",key:"render",value:function(){return n.qy`
      <ha-combo-box
        item-value-path="entity_id"
        .itemLabelPath=${this.itemLabelPath}
        .hass=${this.hass}
        .value=${this._value}
        .label=${void 0===this.label?this.hass.localize("ui.components.entity.entity-picker.entity"):this.label}
        .helper=${this.helper}
        .allowCustomValue=${this.allowCustomEntity}
        .filteredItems=${this._states}
        .renderer=${this._rowRenderer}
        .required=${this.required}
        .disabled=${this.disabled}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
        @filter-changed=${this._filterChanged}
      >
      </ha-combo-box>
    `}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value?.trim();if(t&&t.startsWith(k)){const e=t.substring(23);return i=this,s={domain:e,dialogClosedCallback:e=>{e.entityId&&this._setValue(e.entityId)}},void(0,l.r)(i,"show-dialog",{dialogTag:"dialog-helper-detail",dialogImport:h,dialogParams:s})}var i,s;t!==this._value&&this._setValue(t)}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.target,i=e.detail.value.trim().toLowerCase();t.filteredItems=i.length?(0,u.H)(i,this._states):this._states}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,l.r)(this,"value-changed",{value:e}),(0,l.r)(this,"change")}),0)}}]}}),n.WF)},73133:(e,t,i)=>{i.r(t),i.d(t,{HaEntitySelector:()=>y});var s=i(85461),n=i(69534),a=i(98597),r=i(196),l=i(96041),d=i(33167),o=i(88502),u=i(36831),c=i(45081),h=i(18889);i(85067);(0,s.A)([(0,r.EM)("ha-entities-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-unit-of-measurement"})],key:"includeUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"include-entities"})],key:"includeEntities",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,attribute:"exclude-entities"})],key:"excludeEntities",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:"picked-entity-label"})],key:"pickedEntityLabel",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:"pick-entity-label"})],key:"pickEntityLabel",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array})],key:"createDomains",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return a.s6;const e=this._currentEntities;return a.qy`
      ${e.map((e=>a.qy`
          <div>
            <ha-entity-picker
              allow-custom-entity
              .curValue=${e}
              .hass=${this.hass}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeEntities=${this.includeEntities}
              .excludeEntities=${this.excludeEntities}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
              .entityFilter=${this.entityFilter}
              .value=${e}
              .label=${this.pickedEntityLabel}
              .disabled=${this.disabled}
              .createDomains=${this.createDomains}
              @value-changed=${this._entityChanged}
            ></ha-entity-picker>
          </div>
        `))}
      <div>
        <ha-entity-picker
          allow-custom-entity
          .hass=${this.hass}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeEntities=${this.includeEntities}
          .excludeEntities=${this._excludeEntities(this.value,this.excludeEntities)}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .includeUnitOfMeasurement=${this.includeUnitOfMeasurement}
          .entityFilter=${this.entityFilter}
          .label=${this.pickEntityLabel}
          .helper=${this.helper}
          .disabled=${this.disabled}
          .createDomains=${this.createDomains}
          .required=${this.required&&!e.length}
          @value-changed=${this._addEntity}
        ></ha-entity-picker>
      </div>
    `}},{kind:"field",key:"_excludeEntities",value(){return(0,c.A)(((e,t)=>void 0===e?t:[...t||[],...e]))}},{kind:"get",key:"_currentEntities",value:function(){return this.value||[]}},{kind:"method",key:"_updateEntities",value:async function(e){this.value=e,(0,d.r)(this,"value-changed",{value:e})}},{kind:"method",key:"_entityChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t||void 0!==i&&!(0,h.n)(i))return;const s=this._currentEntities;i&&!s.includes(i)?this._updateEntities(s.map((e=>e===t?i:e))):this._updateEntities(s.filter((e=>e!==t)))}},{kind:"method",key:"_addEntity",value:async function(e){e.stopPropagation();const t=e.detail.value;if(!t)return;if(e.currentTarget.value="",!t)return;const i=this._currentEntities;i.includes(t)||this._updateEntities([...i,t])}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    div {
      margin-top: 8px;
    }
  `}}]}}),a.WF);let y=(0,s.A)([(0,r.EM)("ha-selector-entity")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_entitySources",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,r.wk)()],key:"_createDomains",value:void 0},{kind:"method",key:"_hasIntegration",value:function(e){return e.entity?.filter&&(0,l.e)(e.entity.filter).some((e=>e.integration))}},{kind:"method",key:"willUpdate",value:function(e){e.has("selector")&&void 0!==this.value&&(this.selector.entity?.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,d.r)(this,"value-changed",{value:this.value})):!this.selector.entity?.multiple&&Array.isArray(this.value)&&(this.value=this.value[0],(0,d.r)(this,"value-changed",{value:this.value})))}},{kind:"method",key:"render",value:function(){return this._hasIntegration(this.selector)&&!this._entitySources?a.s6:this.selector.entity?.multiple?a.qy`
      ${this.label?a.qy`<label>${this.label}</label>`:""}
      <ha-entities-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .includeEntities=${this.selector.entity.include_entities}
        .excludeEntities=${this.selector.entity.exclude_entities}
        .entityFilter=${this._filterEntities}
        .createDomains=${this._createDomains}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-entities-picker>
    `:a.qy`<ha-entity-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .includeEntities=${this.selector.entity?.include_entities}
        .excludeEntities=${this.selector.entity?.exclude_entities}
        .entityFilter=${this._filterEntities}
        .createDomains=${this._createDomains}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-entity
      ></ha-entity-picker>`}},{kind:"method",key:"updated",value:function(e){(0,n.A)(i,"updated",this,3)([e]),e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,o.c)(this.hass).then((e=>{this._entitySources=e})),e.has("selector")&&(this._createDomains=(0,u.Lo)(this.selector))}},{kind:"field",key:"_filterEntities",value(){return e=>!this.selector?.entity?.filter||(0,l.e)(this.selector.entity.filter).some((t=>(0,u.Ru)(t,e,this._entitySources)))}}]}}),a.WF)},6601:(e,t,i)=>{i.d(t,{HV:()=>a,Hh:()=>n,KF:()=>l,ON:()=>r,g0:()=>u,s7:()=>d});var s=i(79592);const n="unavailable",a="unknown",r="on",l="off",d=[n,a],o=[n,a,l],u=(0,s.g)(d);(0,s.g)(o)},88502:(e,t,i)=>{i.d(t,{c:()=>a});const s=async(e,t,i,n,a,...r)=>{const l=a,d=l[e],o=d=>n&&n(a,d.result)!==d.cacheKey?(l[e]=void 0,s(e,t,i,n,a,...r)):d.result;if(d)return d instanceof Promise?d.then(o):o(d);const u=i(a,...r);return l[e]=u,u.then((i=>{l[e]={result:i,cacheKey:n?.(a,i)},setTimeout((()=>{l[e]=void 0}),t)}),(()=>{l[e]=void 0})),u},n=e=>e.callWS({type:"entity/source"}),a=e=>s("_entitySources",3e4,n,(e=>Object.keys(e.states).length),e)},31238:(e,t,i)=>{i.d(t,{QC:()=>a,fK:()=>n,p$:()=>s});const s=(e,t,i)=>e(`component.${t}.title`)||i?.name||t,n=(e,t)=>{const i={type:"manifest/list"};return t&&(i.integrations=t),e.callWS(i)},a=(e,t)=>e.callWS({type:"manifest/get",integration:t})},86625:(e,t,i)=>{i.d(t,{T:()=>h});var s=i(34078),n=i(3982),a=i(3267);class r{constructor(e){this.G=e}disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}}class l{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var e;null!==(e=this.Y)&&void 0!==e||(this.Y=new Promise((e=>this.Z=e)))}resume(){var e;null===(e=this.Z)||void 0===e||e.call(this),this.Y=this.Z=void 0}}var d=i(2154);const o=e=>!(0,n.sO)(e)&&"function"==typeof e.then,u=1073741823;class c extends a.Kq{constructor(){super(...arguments),this._$C_t=u,this._$Cwt=[],this._$Cq=new r(this),this._$CK=new l}render(...e){var t;return null!==(t=e.find((e=>!o(e))))&&void 0!==t?t:s.c0}update(e,t){const i=this._$Cwt;let n=i.length;this._$Cwt=t;const a=this._$Cq,r=this._$CK;this.isConnected||this.disconnected();for(let s=0;s<t.length&&!(s>this._$C_t);s++){const e=t[s];if(!o(e))return this._$C_t=s,e;s<n&&e===i[s]||(this._$C_t=u,n=0,Promise.resolve(e).then((async t=>{for(;r.get();)await r.get();const i=a.deref();if(void 0!==i){const s=i._$Cwt.indexOf(e);s>-1&&s<i._$C_t&&(i._$C_t=s,i.setValue(t))}})))}return s.c0}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const h=(0,d.u$)(c)}};
//# sourceMappingURL=HNMHdrw8.js.map