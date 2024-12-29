export const id=6862;export const ids=[6862];export const modules={26862:(e,t,i)=>{var a=i(85461),s=i(98597),n=i(196),r=i(45081),l=i(96041),d=i(33167),o=i(19263),c=i(59782),h=i(60222),u=i(31238),v=i(36831),_=i(31750),k=(i(19887),i(96396),i(52631),i(10214),i(93650),i(42459),i(86625)),f=(i(29222),i(74538));(0,a.A)([(0,n.EM)("ha-service-section-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"service",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"section",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"icon",value:void 0},{kind:"method",key:"render",value:function(){if(this.icon)return s.qy`<ha-icon .icon=${this.icon}></ha-icon>`;if(!this.service||!this.section)return s.s6;if(!this.hass)return this._renderFallback();const e=(0,f.Yw)(this.hass,this.service,this.section).then((e=>e?s.qy`<ha-icon .icon=${e}></ha-icon>`:this._renderFallback()));return s.qy`${(0,k.T)(e)}`}},{kind:"method",key:"_renderFallback",value:function(){return s.s6}}]}}),s.WF);const y=e=>e.selector&&!e.required&&!("boolean"in e.selector&&e.default);(0,a.A)([(0,n.EM)("ha-service-control")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"showAdvanced",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"hidePicker",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"hideDescription",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_value",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_checkedKeys",value(){return new Set}},{kind:"field",decorators:[(0,n.wk)()],key:"_manifest",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-yaml-editor")],key:"_yamlEditor",value:void 0},{kind:"method",key:"willUpdate",value:function(e){if(this.hasUpdated||(this.hass.loadBackendTranslation("services"),this.hass.loadBackendTranslation("selector")),!e.has("value"))return;const t=e.get("value");t?.action!==this.value?.action&&(this._checkedKeys=new Set);const i=this._getServiceInfo(this.value?.action,this.hass.services);if(this.value?.action?t?.action&&(0,o.m)(this.value.action)===(0,o.m)(t.action)||this._fetchManifest((0,o.m)(this.value?.action)):this._manifest=void 0,i&&"target"in i&&(this.value?.data?.entity_id||this.value?.data?.area_id||this.value?.data?.device_id)){const e={...this.value.target};this.value.data.entity_id&&!this.value.target?.entity_id&&(e.entity_id=this.value.data.entity_id),this.value.data.area_id&&!this.value.target?.area_id&&(e.area_id=this.value.data.area_id),this.value.data.device_id&&!this.value.target?.device_id&&(e.device_id=this.value.data.device_id),this._value={...this.value,target:e,data:{...this.value.data}},delete this._value.data.entity_id,delete this._value.data.device_id,delete this._value.data.area_id}else this._value=this.value;if(t?.action!==this.value?.action){let e=!1;if(this._value&&i){const t=this.value&&!("data"in this.value);this._value.data||(this._value.data={}),i.flatFields.forEach((i=>{i.selector&&i.required&&void 0===i.default&&"boolean"in i.selector&&void 0===this._value.data[i.key]&&(e=!0,this._value.data[i.key]=!1),t&&i.selector&&void 0!==i.default&&void 0===this._value.data[i.key]&&(e=!0,this._value.data[i.key]=i.default)}))}e&&(0,d.r)(this,"value-changed",{value:{...this._value}})}if(this._value?.data){const e=this._yamlEditor;e&&e.value!==this._value.data&&e.setValue(this._value.data)}}},{kind:"field",key:"_getServiceInfo",value(){return(0,r.A)(((e,t)=>{if(!e||!t)return;const i=(0,o.m)(e),a=(0,c.Y)(e);if(!(i in t))return;if(!(a in t[i]))return;const s=Object.entries(t[i][a].fields).map((([e,t])=>({key:e,...t,selector:t.selector}))),n=[],r=[];return s.forEach((e=>{e.fields?Object.entries(e.fields).forEach((([e,t])=>{n.push({...t,key:e}),t.selector&&r.push(e)})):(n.push(e),e.selector&&r.push(e.key))})),{...t[i][a],fields:s,flatFields:n,hasSelector:r}}))}},{kind:"field",key:"_getTargetedEntities",value(){return(0,r.A)(((e,t)=>{const i=e?{target:e}:{target:{}},a=(0,l.e)(t?.target?.entity_id||t?.data?.entity_id)?.slice()||[],s=(0,l.e)(t?.target?.device_id||t?.data?.device_id)?.slice()||[],n=(0,l.e)(t?.target?.area_id||t?.data?.area_id)?.slice()||[],r=(0,l.e)(t?.target?.floor_id||t?.data?.floor_id)?.slice(),d=(0,l.e)(t?.target?.label_id||t?.data?.label_id)?.slice();return d&&d.forEach((e=>{const t=(0,v.m0)(this.hass,e,this.hass.areas,this.hass.devices,this.hass.entities,i);s.push(...t.devices),a.push(...t.entities),n.push(...t.areas)})),r&&r.forEach((e=>{const t=(0,v.MH)(this.hass,e,this.hass.areas,i);n.push(...t.areas)})),n.length&&n.forEach((e=>{const t=(0,v.bZ)(this.hass,e,this.hass.devices,this.hass.entities,i);a.push(...t.entities),s.push(...t.devices)})),s.length&&s.forEach((e=>{a.push(...(0,v._7)(this.hass,e,this.hass.entities,i).entities)})),a}))}},{kind:"method",key:"_filterField",value:function(e,t){return!!t.length&&!!t.some((t=>{const i=this.hass.states[t];return!!i&&(!!e.supported_features?.some((e=>(0,h.$)(i,e)))||!(!e.attribute||!Object.entries(e.attribute).some((([e,t])=>e in i.attributes&&((e,t)=>"object"==typeof t?!!Array.isArray(t)&&t.some((t=>e.includes(t))):e.includes(t))(t,i.attributes[e])))))}))}},{kind:"field",key:"_targetSelector",value(){return(0,r.A)((e=>e?{target:{...e}}:{target:{}}))}},{kind:"method",key:"render",value:function(){const e=this._getServiceInfo(this._value?.action,this.hass.services),t=e?.fields.length&&!e.hasSelector.length||e&&Object.keys(this._value?.data||{}).some((t=>!e.hasSelector.includes(t))),i=t&&e?.fields.find((e=>"entity_id"===e.key)),a=Boolean(!t&&e?.flatFields.some((e=>y(e)))),n=this._getTargetedEntities(e?.target,this._value),r=this._value?.action?(0,o.m)(this._value.action):void 0,l=this._value?.action?(0,c.Y)(this._value.action):void 0,d=l&&this.hass.localize(`component.${r}.services.${l}.description`)||e?.description;return s.qy`${this.hidePicker?s.s6:s.qy`<ha-service-picker
          .hass=${this.hass}
          .value=${this._value?.action}
          .disabled=${this.disabled}
          @value-changed=${this._serviceChanged}
        ></ha-service-picker>`}
    ${this.hideDescription?s.s6:s.qy`
          <div class="description">
            ${d?s.qy`<p>${d}</p>`:""}
            ${this._manifest?s.qy` <a
                  href=${this._manifest.is_built_in?(0,_.o)(this.hass,`/integrations/${this._manifest.domain}`):this._manifest.documentation}
                  title=${this.hass.localize("ui.components.service-control.integration_doc")}
                  target="_blank"
                  rel="noreferrer"
                >
                  <ha-icon-button
                    .path=${"M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z"}
                    class="help-icon"
                  ></ha-icon-button>
                </a>`:s.s6}
          </div>
        `}
    ${e&&"target"in e?s.qy`<ha-settings-row .narrow=${this.narrow}>
          ${a?s.qy`<div slot="prefix" class="checkbox-spacer"></div>`:""}
          <span slot="heading"
            >${this.hass.localize("ui.components.service-control.target")}</span
          >
          <span slot="description"
            >${this.hass.localize("ui.components.service-control.target_secondary")}</span
          ><ha-selector
            .hass=${this.hass}
            .selector=${this._targetSelector(e.target)}
            .disabled=${this.disabled}
            @value-changed=${this._targetChanged}
            .value=${this._value?.target}
          ></ha-selector
        ></ha-settings-row>`:i?s.qy`<ha-entity-picker
            .hass=${this.hass}
            .disabled=${this.disabled}
            .value=${this._value?.data?.entity_id}
            .label=${this.hass.localize(`component.${r}.services.${l}.fields.entity_id.description`)||i.description}
            @value-changed=${this._entityPicked}
            allow-custom-entity
          ></ha-entity-picker>`:""}
    ${t?s.qy`<ha-yaml-editor
          .hass=${this.hass}
          .label=${this.hass.localize("ui.components.service-control.action_data")}
          .name=${"data"}
          .readOnly=${this.disabled}
          .defaultValue=${this._value?.data}
          @value-changed=${this._dataChanged}
        ></ha-yaml-editor>`:e?.fields.map((e=>{if(!e.fields)return this._renderField(e,a,r,l,n);const t=Object.entries(e.fields).map((([e,t])=>({key:e,...t})));return t.length&&this._hasFilteredFields(t,n)?s.qy`<ha-expansion-panel
                leftChevron
                .expanded=${!e.collapsed}
                .header=${this.hass.localize(`component.${r}.services.${l}.sections.${e.key}.name`)||e.name||e.key}
                .secondary=${this._getSectionDescription(e,r,l)}
              >
                <ha-service-section-icon
                  slot="icons"
                  .hass=${this.hass}
                  .service=${this._value.action}
                  .section=${e.key}
                ></ha-service-section-icon>
                ${Object.entries(e.fields).map((([e,t])=>this._renderField({key:e,...t},a,r,l,n)))}
              </ha-expansion-panel>`:s.s6}))} `}},{kind:"method",key:"_getSectionDescription",value:function(e,t,i){return this.hass.localize(`component.${t}.services.${i}.sections.${e.key}.description`)}},{kind:"method",key:"_hasFilteredFields",value:function(e,t){return e.some((e=>!e.filter||this._filterField(e.filter,t)))}},{kind:"field",key:"_renderField",value(){return(e,t,i,a,n)=>{if(e.filter&&!this._filterField(e.filter,n))return s.s6;const r=e?.selector??{text:void 0},l=y(e);return e.selector&&(!e.advanced||this.showAdvanced||this._value?.data&&void 0!==this._value.data[e.key])?s.qy`<ha-settings-row .narrow=${this.narrow}>
          ${l?s.qy`<ha-checkbox
                .key=${e.key}
                .checked=${this._checkedKeys.has(e.key)||this._value?.data&&void 0!==this._value.data[e.key]}
                .disabled=${this.disabled}
                @change=${this._checkboxChanged}
                slot="prefix"
              ></ha-checkbox>`:t?s.qy`<div slot="prefix" class="checkbox-spacer"></div>`:""}
          <span slot="heading"
            >${this.hass.localize(`component.${i}.services.${a}.fields.${e.key}.name`)||e.name||e.key}</span
          >
          <span slot="description"
            >${this.hass.localize(`component.${i}.services.${a}.fields.${e.key}.description`)||e?.description}</span
          >
          <ha-selector
            .disabled=${this.disabled||l&&!this._checkedKeys.has(e.key)&&(!this._value?.data||void 0===this._value.data[e.key])}
            .hass=${this.hass}
            .selector=${r}
            .key=${e.key}
            @value-changed=${this._serviceDataChanged}
            .value=${this._value?.data?this._value.data[e.key]:void 0}
            .placeholder=${e.default}
            .localizeValue=${this._localizeValueCallback}
          ></ha-selector>
        </ha-settings-row>`:""}}},{kind:"field",key:"_localizeValueCallback",value(){return e=>this._value?.action?this.hass.localize(`component.${(0,o.m)(this._value.action)}.selector.${e}`):""}},{kind:"method",key:"_checkboxChanged",value:function(e){const t=e.currentTarget.checked,i=e.currentTarget.key;let a;if(t){this._checkedKeys.add(i);const e=this._getServiceInfo(this._value?.action,this.hass.services)?.flatFields.find((e=>e.key===i));let t=e?.default;null==t&&e?.selector&&"constant"in e.selector&&(t=e.selector.constant?.value),null==t&&e?.selector&&"boolean"in e.selector&&(t=!1),null!=t&&(a={...this._value?.data,[i]:t})}else this._checkedKeys.delete(i),a={...this._value?.data},delete a[i];a&&(0,d.r)(this,"value-changed",{value:{...this._value,data:a}}),this.requestUpdate("_checkedKeys")}},{kind:"method",key:"_serviceChanged",value:function(e){if(e.stopPropagation(),e.detail.value===this._value?.action)return;const t=e.detail.value||"";let i;if(t){const e=this._getServiceInfo(t,this.hass.services),a=this._value?.target;if(a&&e?.target){const t={target:{...e.target}};let s=(0,l.e)(a.entity_id||this._value.data?.entity_id)?.slice()||[],n=(0,l.e)(a.device_id||this._value.data?.device_id)?.slice()||[],r=(0,l.e)(a.area_id||this._value.data?.area_id)?.slice()||[];r.length&&(r=r.filter((e=>(0,v.Qz)(this.hass,this.hass.entities,this.hass.devices,e,t)))),n.length&&(n=n.filter((e=>(0,v.DF)(this.hass,Object.values(this.hass.entities),this.hass.devices[e],t)))),s.length&&(s=s.filter((e=>(0,v.MM)(this.hass.states[e],t)))),i={...s.length?{entity_id:s}:{},...n.length?{device_id:n}:{},...r.length?{area_id:r}:{}}}}const a={action:t,target:i};(0,d.r)(this,"value-changed",{value:a})}},{kind:"method",key:"_entityPicked",value:function(e){e.stopPropagation();const t=e.detail.value;if(this._value?.data?.entity_id===t)return;let i;!t&&this._value?.data?(i={...this._value},delete i.data.entity_id):i={...this._value,data:{...this._value?.data,entity_id:e.detail.value}},(0,d.r)(this,"value-changed",{value:i})}},{kind:"method",key:"_targetChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(this._value?.target===t)return;let i;t?i={...this._value,target:e.detail.value}:(i={...this._value},delete i.target),(0,d.r)(this,"value-changed",{value:i})}},{kind:"method",key:"_serviceDataChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.key,i=e.detail.value;if(!(this._value?.data?.[t]!==i&&(this._value?.data&&t in this._value.data||""!==i&&void 0!==i)))return;const a={...this._value?.data,[t]:i};""!==i&&void 0!==i||delete a[t],(0,d.r)(this,"value-changed",{value:{...this._value,data:a}})}},{kind:"method",key:"_dataChanged",value:function(e){e.stopPropagation(),e.detail.isValid&&(0,d.r)(this,"value-changed",{value:{...this._value,data:e.detail.value}})}},{kind:"method",key:"_fetchManifest",value:async function(e){this._manifest=void 0;try{this._manifest=await(0,u.QC)(this.hass,e)}catch(t){}}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`
      ha-settings-row {
        padding: var(--service-control-padding, 0 16px);
      }
      ha-settings-row {
        --paper-time-input-justify-content: flex-end;
        --settings-row-content-width: 100%;
        --settings-row-prefix-display: contents;
        border-top: var(
          --service-control-items-border-top,
          1px solid var(--divider-color)
        );
      }
      ha-service-picker,
      ha-entity-picker,
      ha-yaml-editor {
        display: block;
        margin: var(--service-control-padding, 0 16px);
      }
      ha-yaml-editor {
        padding: 16px 0;
      }
      p {
        margin: var(--service-control-padding, 0 16px);
        padding: 16px 0;
      }
      :host([hidePicker]) p {
        padding-top: 0;
      }
      .checkbox-spacer {
        width: 32px;
      }
      ha-checkbox {
        margin-left: -16px;
        margin-inline-start: -16px;
        margin-inline-end: initial;
      }
      .help-icon {
        color: var(--secondary-text-color);
      }
      .description {
        justify-content: space-between;
        display: flex;
        align-items: center;
        padding-right: 2px;
        padding-inline-end: 2px;
        padding-inline-start: initial;
      }
      .description p {
        direction: ltr;
      }
      ha-expansion-panel {
        --ha-card-border-radius: 0;
        --expansion-panel-summary-padding: 0 16px;
        --expansion-panel-content-padding: 0;
      }
    `}}]}}),s.WF)},60929:(e,t,i)=>{var a=i(85461),s=i(98597),n=i(196),r=i(86625),l=i(93758),d=i(19263),o=i(74538);i(29222);(0,a.A)([(0,n.EM)("ha-service-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"service",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"icon",value:void 0},{kind:"method",key:"render",value:function(){if(this.icon)return s.qy`<ha-icon .icon=${this.icon}></ha-icon>`;if(!this.service)return s.s6;if(!this.hass)return this._renderFallback();const e=(0,o.f$)(this.hass,this.service).then((e=>e?s.qy`<ha-icon .icon=${e}></ha-icon>`:this._renderFallback()));return s.qy`${(0,r.T)(e)}`}},{kind:"method",key:"_renderFallback",value:function(){const e=(0,d.m)(this.service);return s.qy`
      <ha-svg-icon
        .path=${l.n_[e]||l.Gn}
      ></ha-svg-icon>
    `}}]}}),s.WF)},10214:(e,t,i)=>{var a=i(85461),s=i(98597),n=i(196),r=i(45081),l=i(33167),d=i(31238),o=(i(66442),i(9484),i(60929),i(74538));(0,a.A)([(0,n.EM)("ha-service-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_filter",value:void 0},{kind:"method",key:"willUpdate",value:function(){this.hasUpdated||(this.hass.loadBackendTranslation("services"),(0,o.Yd)(this.hass))}},{kind:"field",key:"_rowRenderer",value(){return e=>s.qy`<ha-list-item twoline graphic="icon">
        <ha-service-icon
          slot="graphic"
          .hass=${this.hass}
          .service=${e.service}
        ></ha-service-icon>
        <span>${e.name}</span>
        <span slot="secondary"
          >${e.name===e.service?"":e.service}</span
        >
      </ha-list-item>`}},{kind:"method",key:"render",value:function(){return s.qy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${this.hass.localize("ui.components.service-picker.action")}
        .filteredItems=${this._filteredServices(this.hass.localize,this.hass.services,this._filter)}
        .value=${this.value}
        .disabled=${this.disabled}
        .renderer=${this._rowRenderer}
        item-value-path="service"
        item-label-path="name"
        allow-custom-value
        @filter-changed=${this._filterChanged}
        @value-changed=${this._valueChanged}
      ></ha-combo-box>
    `}},{kind:"field",key:"_services",value(){return(0,r.A)(((e,t)=>{if(!t)return[];const i=[];return Object.keys(t).sort().forEach((a=>{const s=Object.keys(t[a]).sort();for(const n of s)i.push({service:`${a}.${n}`,name:`${(0,d.p$)(e,a)}: ${this.hass.localize(`component.${a}.services.${n}.name`)||t[a][n].name||n}`})})),i}))}},{kind:"field",key:"_filteredServices",value(){return(0,r.A)(((e,t,i)=>{if(!t)return[];const a=this._services(e,t);if(!i)return a;const s=i.split(" ");return a.filter((e=>{const t=e.name.toLowerCase(),i=e.service.toLowerCase();return s.every((e=>t.includes(e)||i.includes(e)))}))}))}},{kind:"method",key:"_filterChanged",value:function(e){this._filter=e.detail.value.toLowerCase()}},{kind:"method",key:"_valueChanged",value:function(e){this.value=e.detail.value,(0,l.r)(this,"change"),(0,l.r)(this,"value-changed",{value:this.value})}}]}}),s.WF)},31750:(e,t,i)=>{i.d(t,{o:()=>a});const a=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}};
//# sourceMappingURL=YsV9mk7i.js.map