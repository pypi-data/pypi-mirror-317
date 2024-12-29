/*! For license information please see v3E1s9ZP.js.LICENSE.txt */
export const id=9920;export const ids=[9920];export const modules={68873:(t,e,i)=>{i.d(e,{a:()=>n});var s=i(6601),a=i(19263);function n(t,e){const i=(0,a.m)(t.entity_id),n=void 0!==e?e:t?.state;if(["button","event","input_button","scene"].includes(i))return n!==s.Hh;if((0,s.g0)(n))return!1;if(n===s.KF&&"alert"!==i)return!1;switch(i){case"alarm_control_panel":return"disarmed"!==n;case"alert":return"idle"!==n;case"cover":case"valve":return"closed"!==n;case"device_tracker":case"person":return"not_home"!==n;case"lawn_mower":return["mowing","error"].includes(n);case"lock":return"locked"!==n;case"media_player":return"standby"!==n;case"vacuum":return!["idle","docked","paused"].includes(n);case"plant":return"problem"===n;case"group":return["on","home","open","locked","problem"].includes(n);case"timer":return"active"===n;case"camera":return"streaming"===n}return!0}},64886:(t,e,i)=>{i.r(e),i.d(e,{HaStatisticSelector:()=>p});var s=i(85461),a=i(98597),n=i(196),c=i(66580),r=i(33167),d=(i(23981),i(45081)),l=i(96041),o=i(66412),u=i(91330);const h=(t,e,i)=>{const s=t.states[e];return s?(0,u.u)(s):i?.name||e};var v=i(31750),k=(i(66442),i(29222),i(85426),i(38848));(0,s.A)([(0,n.EM)("ha-statistic-picker")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"statistic-types"})],key:"statisticTypes",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"statisticIds",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Array,attribute:"include-statistics-unit-of-measurement"})],key:"includeStatisticsUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"include-unit-class"})],key:"includeUnitClass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"include-device-class"})],key:"includeDeviceClass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"entities-only"})],key:"entitiesOnly",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Array,attribute:"exclude-statistics"})],key:"excludeStatistics",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helpMissingEntityUrl",value(){return"/more-info/statistics/"}},{kind:"field",decorators:[(0,n.wk)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_init",value(){return!1}},{kind:"field",key:"_statistics",value(){return[]}},{kind:"field",decorators:[(0,n.wk)()],key:"_filteredItems",value(){}},{kind:"field",key:"_rowRenderer",value(){return t=>a.qy`<mwc-list-item graphic="avatar" twoline>
      ${t.state?a.qy`<state-badge
            slot="graphic"
            .stateObj=${t.state}
            .hass=${this.hass}
          ></state-badge>`:""}
      <span>${t.name}</span>
      <span slot="secondary"
        >${""===t.id||"__missing"===t.id?a.qy`<a
              target="_blank"
              rel="noopener noreferrer"
              href=${(0,v.o)(this.hass,this.helpMissingEntityUrl)}
              >${this.hass.localize("ui.components.statistic-picker.learn_more")}</a
            >`:t.id}</span
      >
    </mwc-list-item>`}},{kind:"field",key:"_getStatistics",value(){return(0,d.A)(((t,e,i,s,a,n,c)=>{if(!t.length)return[{id:"",name:this.hass.localize("ui.components.statistic-picker.no_statistics"),strings:[]}];if(e){const i=(0,l.e)(e);t=t.filter((t=>i.includes(t.statistics_unit_of_measurement)))}if(i){const e=(0,l.e)(i);t=t.filter((t=>e.includes(t.unit_class)))}if(s){const e=(0,l.e)(s);t=t.filter((t=>{const i=this.hass.states[t.statistic_id];return!i||e.includes(i.attributes.device_class||"")}))}const r=[];return t.forEach((t=>{if(n&&t.statistic_id!==c&&n.includes(t.statistic_id))return;const e=this.hass.states[t.statistic_id];if(!e){if(!a){const e=t.statistic_id,i=h(this.hass,t.statistic_id,t);r.push({id:e,name:i,strings:[e,i]})}return}const i=t.statistic_id,s=h(this.hass,t.statistic_id,t);r.push({id:i,name:s,state:e,strings:[i,s]})})),r.length?(r.length>1&&r.sort(((t,e)=>(0,o.x)(t.name||"",e.name||"",this.hass.locale.language))),r.push({id:"__missing",name:this.hass.localize("ui.components.statistic-picker.missing_entity"),strings:[]}),r):[{id:"",name:this.hass.localize("ui.components.statistic-picker.no_match"),strings:[]}]}))}},{kind:"method",key:"open",value:function(){this.comboBox?.open()}},{kind:"method",key:"focus",value:function(){this.comboBox?.focus()}},{kind:"method",key:"willUpdate",value:function(t){(!this.hasUpdated&&!this.statisticIds||t.has("statisticTypes"))&&this._getStatisticIds(),(!this._init&&this.statisticIds||t.has("_opened")&&this._opened)&&(this._init=!0,this.hasUpdated?this._statistics=this._getStatistics(this.statisticIds,this.includeStatisticsUnitOfMeasurement,this.includeUnitClass,this.includeDeviceClass,this.entitiesOnly,this.excludeStatistics,this.value):this.updateComplete.then((()=>{this._statistics=this._getStatistics(this.statisticIds,this.includeStatisticsUnitOfMeasurement,this.includeUnitClass,this.includeDeviceClass,this.entitiesOnly,this.excludeStatistics,this.value)})))}},{kind:"method",key:"render",value:function(){return 0===this._statistics.length?a.s6:a.qy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.statistic-picker.statistic"):this.label}
        .value=${this._value}
        .renderer=${this._rowRenderer}
        .disabled=${this.disabled}
        .allowCustomValue=${this.allowCustomEntity}
        .items=${this._statistics}
        .filteredItems=${this._filteredItems??this._statistics}
        item-value-path="id"
        item-id-path="id"
        item-label-path="name"
        @opened-changed=${this._openedChanged}
        @value-changed=${this._statisticChanged}
        @filter-changed=${this._filterChanged}
      ></ha-combo-box>
    `}},{kind:"method",key:"_getStatisticIds",value:async function(){var t,e;this.statisticIds=await(t=this.hass,e=this.statisticTypes,t.callWS({type:"recorder/list_statistic_ids",statistic_type:e}))}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_statisticChanged",value:function(t){t.stopPropagation();let e=t.detail.value;"__missing"===e&&(e=""),e!==this._value&&this._setValue(e)}},{kind:"method",key:"_openedChanged",value:function(t){this._opened=t.detail.value}},{kind:"method",key:"_filterChanged",value:function(t){const e=t.detail.value.toLowerCase();this._filteredItems=e.length?(0,k.H)(e,this._statistics):void 0}},{kind:"method",key:"_setValue",value:function(t){this.value=t,setTimeout((()=>{(0,r.r)(this,"value-changed",{value:t}),(0,r.r)(this,"change")}),0)}}]}}),a.WF),(0,s.A)([(0,n.EM)("ha-statistics-picker")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"statisticIds",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"statistic-types"})],key:"statisticTypes",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"picked-statistic-label"})],key:"pickedStatisticLabel",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"pick-statistic-label"})],key:"pickStatisticLabel",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"include-statistics-unit-of-measurement"})],key:"includeStatisticsUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"include-unit-class"})],key:"includeUnitClass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"include-device-class"})],key:"includeDeviceClass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"ignore-restrictions-on-first-statistic"})],key:"ignoreRestrictionsOnFirstStatistic",value(){return!1}},{kind:"method",key:"render",value:function(){if(!this.hass)return a.s6;const t=this.ignoreRestrictionsOnFirstStatistic&&this._currentStatistics.length<=1,e=t?void 0:this.includeStatisticsUnitOfMeasurement,i=t?void 0:this.includeUnitClass,s=t?void 0:this.includeDeviceClass,n=t?void 0:this.statisticTypes;return a.qy`
      ${(0,c.u)(this._currentStatistics,(t=>t),(t=>a.qy`
          <div>
            <ha-statistic-picker
              .curValue=${t}
              .hass=${this.hass}
              .includeStatisticsUnitOfMeasurement=${e}
              .includeUnitClass=${i}
              .includeDeviceClass=${s}
              .value=${t}
              .statisticTypes=${n}
              .statisticIds=${this.statisticIds}
              .label=${this.pickedStatisticLabel}
              .excludeStatistics=${this.value}
              .allowCustomEntity=${this.allowCustomEntity}
              @value-changed=${this._statisticChanged}
            ></ha-statistic-picker>
          </div>
        `))}
      <div>
        <ha-statistic-picker
          .hass=${this.hass}
          .includeStatisticsUnitOfMeasurement=${this.includeStatisticsUnitOfMeasurement}
          .includeUnitClass=${this.includeUnitClass}
          .includeDeviceClass=${this.includeDeviceClass}
          .statisticTypes=${this.statisticTypes}
          .statisticIds=${this.statisticIds}
          .label=${this.pickStatisticLabel}
          .excludeStatistics=${this.value}
          .allowCustomEntity=${this.allowCustomEntity}
          @value-changed=${this._addStatistic}
        ></ha-statistic-picker>
      </div>
    `}},{kind:"get",key:"_currentStatistics",value:function(){return this.value||[]}},{kind:"method",key:"_updateStatistics",value:async function(t){this.value=t,(0,r.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_statisticChanged",value:function(t){t.stopPropagation();const e=t.currentTarget.curValue,i=t.detail.value;if(i===e)return;const s=this._currentStatistics;i&&!s.includes(i)?this._updateStatistics(s.map((t=>t===e?i:t))):this._updateStatistics(s.filter((t=>t!==e)))}},{kind:"method",key:"_addStatistic",value:async function(t){t.stopPropagation();const e=t.detail.value;if(!e)return;if(t.currentTarget.value="",!e)return;const i=this._currentStatistics;i.includes(e)||this._updateStatistics([...i,e])}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host {
        width: 200px;
        display: block;
      }
      ha-statistic-picker {
        display: block;
        width: 100%;
        margin-top: 8px;
      }
    `}}]}}),a.WF);let p=(0,s.A)([(0,n.EM)("ha-selector-statistic")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return this.selector.statistic.multiple?a.qy`
      ${this.label?a.qy`<label>${this.label}</label>`:""}
      <ha-statistics-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-statistics-picker>
    `:a.qy`<ha-statistic-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-entity
      ></ha-statistic-picker>`}}]}}),a.WF)},6601:(t,e,i)=>{i.d(e,{HV:()=>n,Hh:()=>a,KF:()=>r,ON:()=>c,g0:()=>o,s7:()=>d});var s=i(79592);const a="unavailable",n="unknown",c="on",r="off",d=[a,n],l=[a,n,r],o=(0,s.g)(d);(0,s.g)(l)},31750:(t,e,i)=>{i.d(e,{o:()=>s});const s=(t,e)=>`https://${t.config.version.includes("b")?"rc":t.config.version.includes("dev")?"next":"www"}.home-assistant.io${e}`},86625:(t,e,i)=>{i.d(e,{T:()=>h});var s=i(34078),a=i(3982),n=i(3267);class c{constructor(t){this.G=t}disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}}class r{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null===(t=this.Z)||void 0===t||t.call(this),this.Y=this.Z=void 0}}var d=i(2154);const l=t=>!(0,a.sO)(t)&&"function"==typeof t.then,o=1073741823;class u extends n.Kq{constructor(){super(...arguments),this._$C_t=o,this._$Cwt=[],this._$Cq=new c(this),this._$CK=new r}render(...t){var e;return null!==(e=t.find((t=>!l(t))))&&void 0!==e?e:s.c0}update(t,e){const i=this._$Cwt;let a=i.length;this._$Cwt=e;const n=this._$Cq,c=this._$CK;this.isConnected||this.disconnected();for(let s=0;s<e.length&&!(s>this._$C_t);s++){const t=e[s];if(!l(t))return this._$C_t=s,t;s<a&&t===i[s]||(this._$C_t=o,a=0,Promise.resolve(t).then((async e=>{for(;c.get();)await c.get();const i=n.deref();if(void 0!==i){const s=i._$Cwt.indexOf(t);s>-1&&s<i._$C_t&&(i._$C_t=s,i.setValue(e))}})))}return s.c0}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const h=(0,d.u$)(u)}};
//# sourceMappingURL=v3E1s9ZP.js.map