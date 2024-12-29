export const id=7701;export const ids=[7701];export const modules={7701:(e,t,n)=>{n.r(t),n.d(t,{HaConversationAgentSelector:()=>k});var o=n(85461),i=n(98597),a=n(196),s=n(69534),r=n(33167),l=n(24517),d=n(11355),c=n(81407),p=n(193),u=n(31238);const h=(e,t)=>e.callApi("POST","config/config_entries/options/flow",{handler:t,show_advanced_options:Boolean(e.userData?.showAdvanced)}),g=(e,t)=>e.callApi("GET",`config/config_entries/options/flow/${t}`),m=(e,t,n)=>e.callApi("POST",`config/config_entries/options/flow/${t}`,n),v=(e,t)=>e.callApi("DELETE",`config/config_entries/options/flow/${t}`);var _=n(50006);n(9484),n(96334);var f=n(27761);const y="__NONE_OPTION__";(0,o.A)([(0,a.EM)("ha-conversation-agent-picker")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[(0,a.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,a.wk)()],key:"_agents",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_configEntry",value:void 0},{kind:"method",key:"render",value:function(){if(!this._agents)return i.s6;let e=this.value;if(!e&&this.required){for(const t of this._agents)if("conversation.home_assistant"===t.id&&t.supported_languages.includes(this.language)){e=t.id;break}if(!e)for(const t of this._agents)if("*"===t.supported_languages&&t.supported_languages.includes(this.language)){e=t.id;break}}return e||(e=y),i.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.coversation-agent-picker.conversation_agent")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${l.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?i.s6:i.qy`<ha-list-item .value=${y}>
              ${this.hass.localize("ui.components.coversation-agent-picker.none")}
            </ha-list-item>`}
        ${this._agents.map((e=>i.qy`<ha-list-item
              .value=${e.id}
              .disabled=${"*"!==e.supported_languages&&0===e.supported_languages.length}
            >
              ${e.name}
            </ha-list-item>`))}</ha-select
      >${this._configEntry?.supports_options?i.qy`<ha-icon-button
            .path=${"M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"}
            @click=${this._openOptionsFlow}
          ></ha-icon-button>`:""}
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,s.A)(n,"willUpdate",this,3)([e]),this.hasUpdated?e.has("language")&&this._debouncedUpdateAgents():this._updateAgents(),e.has("value")&&this._maybeFetchConfigEntry()}},{kind:"method",key:"_maybeFetchConfigEntry",value:async function(){if(this.value&&this.value in this.hass.entities)try{const e=await(0,f.v)(this.hass,this.value);if(!e.config_entry_id)return void(this._configEntry=void 0);this._configEntry=(await(0,c.Vx)(this.hass,e.config_entry_id)).config_entry}catch(e){this._configEntry=void 0}else this._configEntry=void 0}},{kind:"field",key:"_debouncedUpdateAgents",value(){return(0,d.s)((()=>this._updateAgents()),500)}},{kind:"method",key:"_updateAgents",value:async function(){const{agents:e}=await(0,p.vc)(this.hass,this.language,this.hass.config.country||void 0);if(this._agents=e,!this.value)return;const t=e.find((e=>e.id===this.value));(0,r.r)(this,"supported-languages-changed",{value:t?.supported_languages}),(!t||"*"!==t.supported_languages&&0===t.supported_languages.length)&&(this.value=void 0,(0,r.r)(this,"value-changed",{value:this.value}))}},{kind:"method",key:"_openOptionsFlow",value:async function(){var e,t,n;this._configEntry&&(e=this,t=this._configEntry,n={manifest:await(0,u.QC)(this.hass,this._configEntry.domain)},(0,_.g)(e,{startFlowHandler:t.entry_id,domain:t.domain,...n},{flowType:"options_flow",showDevices:!1,createFlow:async(e,n)=>{const[o]=await Promise.all([h(e,n),e.loadFragmentTranslation("config"),e.loadBackendTranslation("options",t.domain),e.loadBackendTranslation("selector",t.domain)]);return o},fetchFlow:async(e,n)=>{const[o]=await Promise.all([g(e,n),e.loadFragmentTranslation("config"),e.loadBackendTranslation("options",t.domain),e.loadBackendTranslation("selector",t.domain)]);return o},handleFlowStep:m,deleteFlow:v,renderAbortDescription(e,n){const o=e.localize(`component.${n.translation_domain||t.domain}.options.abort.${n.reason}`,n.description_placeholders);return o?i.qy`
              <ha-markdown
                breaks
                allowsvg
                .content=${o}
              ></ha-markdown>
            `:n.reason},renderShowFormStepHeader(e,n){return e.localize(`component.${n.translation_domain||t.domain}.options.step.${n.step_id}.title`,n.description_placeholders)||e.localize("ui.dialogs.options_flow.form.header")},renderShowFormStepDescription(e,n){const o=e.localize(`component.${n.translation_domain||t.domain}.options.step.${n.step_id}.description`,n.description_placeholders);return o?i.qy`
              <ha-markdown
                allowsvg
                breaks
                .content=${o}
              ></ha-markdown>
            `:""},renderShowFormStepFieldLabel(e,n,o,i){if("expandable"===o.type)return e.localize(`component.${t.domain}.options.step.${n.step_id}.sections.${o.name}.name`);const a=i?.path?.[0]?`sections.${i.path[0]}.`:"";return e.localize(`component.${t.domain}.options.step.${n.step_id}.${a}data.${o.name}`)||o.name},renderShowFormStepFieldHelper(e,n,o,a){if("expandable"===o.type)return e.localize(`component.${n.translation_domain||t.domain}.options.step.${n.step_id}.sections.${o.name}.description`);const s=a?.path?.[0]?`sections.${a.path[0]}.`:"",r=e.localize(`component.${n.translation_domain||t.domain}.options.step.${n.step_id}.${s}data_description.${o.name}`,n.description_placeholders);return r?i.qy`<ha-markdown breaks .content=${r}></ha-markdown>`:""},renderShowFormStepFieldError(e,n,o){return e.localize(`component.${n.translation_domain||t.domain}.options.error.${o}`,n.description_placeholders)||o},renderShowFormStepFieldLocalizeValue(e,n,o){return e.localize(`component.${t.domain}.selector.${o}`)},renderShowFormStepSubmitButton(e,n){return e.localize(`component.${t.domain}.options.step.${n.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===n.last_step?"next":"submit"))},renderExternalStepHeader(e,t){return""},renderExternalStepDescription(e,t){return""},renderCreateEntryDescription(e,t){return i.qy`
          <p>${e.localize("ui.dialogs.options_flow.success.description")}</p>
        `},renderShowFormProgressHeader(e,n){return e.localize(`component.${t.domain}.options.step.${n.step_id}.title`)||e.localize(`component.${t.domain}.title`)},renderShowFormProgressDescription(e,n){const o=e.localize(`component.${n.translation_domain||t.domain}.options.progress.${n.progress_action}`,n.description_placeholders);return o?i.qy`
              <ha-markdown
                allowsvg
                breaks
                .content=${o}
              ></ha-markdown>
            `:""},renderMenuHeader(e,n){return e.localize(`component.${t.domain}.options.step.${n.step_id}.title`)||e.localize(`component.${t.domain}.title`)},renderMenuDescription(e,n){const o=e.localize(`component.${n.translation_domain||t.domain}.options.step.${n.step_id}.description`,n.description_placeholders);return o?i.qy`
              <ha-markdown
                allowsvg
                breaks
                .content=${o}
              ></ha-markdown>
            `:""},renderMenuOption(e,n,o){return e.localize(`component.${n.translation_domain||t.domain}.options.step.${n.step_id}.menu_options.${o}`,n.description_placeholders)},renderLoadingDescription(e,n){return e.localize(`component.${t.domain}.options.loading`)||("loading_flow"===n||"loading_step"===n?e.localize(`ui.dialogs.options_flow.loading.${n}`,{integration:(0,u.p$)(e.localize,t.domain)}):"")}}))}},{kind:"get",static:!0,key:"styles",value:function(){return i.AH`
      :host {
        display: flex;
        align-items: center;
      }
      ha-select {
        width: 100%;
      }
      ha-icon-button {
        color: var(--secondary-text-color);
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===y||(this.value=t.value===y?void 0:t.value,(0,r.r)(this,"value-changed",{value:this.value}),(0,r.r)(this,"supported-languages-changed",{value:this._agents.find((e=>e.id===this.value))?.supported_languages}))}}]}}),i.WF);let k=(0,o.A)([(0,a.EM)("ha-selector-conversation_agent")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){return i.qy`<ha-conversation-agent-picker
      .hass=${this.hass}
      .value=${this.value}
      .language=${this.selector.conversation_agent?.language||this.context?.language}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-conversation-agent-picker>`}},{kind:"field",static:!0,key:"styles",value(){return i.AH`
    ha-conversation-agent-picker {
      width: 100%;
    }
  `}}]}}),i.WF)},193:(e,t,n)=>{n.d(t,{ZE:()=>o,vc:()=>i});let o=function(e){return e[e.CONTROL=1]="CONTROL",e}({});const i=(e,t,n)=>e.callWS({type:"conversation/agent/list",language:t,country:n})},27761:(e,t,n)=>{n.d(t,{jh:()=>a,Ox:()=>r,P9:()=>l,v:()=>s});var o=n(45081),i=n(91330);n(66412);const a=(e,t)=>{if(t.name)return t.name;const n=e.states[t.entity_id];return n?(0,i.u)(n):t.original_name?t.original_name:t.entity_id},s=(e,t)=>e.callWS({type:"config/entity_registry/get",entity_id:t}),r=(0,o.A)((e=>{const t={};for(const n of e)t[n.entity_id]=n;return t})),l=(0,o.A)((e=>{const t={};for(const n of e)t[n.id]=n;return t}))},31238:(e,t,n)=>{n.d(t,{QC:()=>a,fK:()=>i,p$:()=>o});const o=(e,t,n)=>e(`component.${t}.title`)||n?.name||t,i=(e,t)=>{const n={type:"manifest/list"};return t&&(n.integrations=t),e.callWS(n)},a=(e,t)=>e.callWS({type:"manifest/get",integration:t})},50006:(e,t,n)=>{n.d(t,{g:()=>a});var o=n(33167);const i=()=>Promise.all([n.e(4932),n.e(5721)]).then(n.bind(n,55721)),a=(e,t,n)=>{(0,o.r)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:i,dialogParams:{...t,flowConfig:n,dialogParentElement:e}})}}};
//# sourceMappingURL=wOf0L-mO.js.map