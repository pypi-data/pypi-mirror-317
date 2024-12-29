export const id=7674;export const ids=[7674];export const modules={20678:(e,t,i)=>{i.d(t,{T:()=>a});var s=i(45081);const a=(e,t)=>{try{return n(t)?.of(e)??e}catch{return e}},n=(0,s.A)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})))},37939:(e,t,i)=>{var s=i(85461),a=i(69534),n=i(98597),l=i(196),d=i(33167),r=i(24517),o=i(20678),p=i(82286);i(9484),i(96334);const u="preferred",c="last_used";(0,s.A)([(0,l.EM)("ha-assist-pipeline-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"includeLastUsed",value(){return!1}},{kind:"field",decorators:[(0,l.wk)()],key:"_pipelines",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_preferredPipeline",value(){return null}},{kind:"get",key:"_default",value:function(){return this.includeLastUsed?c:u}},{kind:"method",key:"render",value:function(){if(!this._pipelines)return n.s6;const e=this.value??this._default;return n.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.pipeline-picker.pipeline")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${r.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.includeLastUsed?n.qy`
              <ha-list-item .value=${c}>
                ${this.hass.localize("ui.components.pipeline-picker.last_used")}
              </ha-list-item>
            `:null}
        <ha-list-item .value=${u}>
          ${this.hass.localize("ui.components.pipeline-picker.preferred",{preferred:this._pipelines.find((e=>e.id===this._preferredPipeline))?.name})}
        </ha-list-item>
        ${this._pipelines.map((e=>n.qy`<ha-list-item .value=${e.id}>
              ${e.name}
              (${(0,o.T)(e.language,this.hass.locale)})
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,a.A)(i,"firstUpdated",this,3)([e]),(0,p.nx)(this.hass).then((e=>{this._pipelines=e.pipelines,this._preferredPipeline=e.preferred_pipeline}))}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===this._default||(this.value=t.value===this._default?void 0:t.value,(0,d.r)(this,"value-changed",{value:this.value}))}}]}}),n.WF)},97674:(e,t,i)=>{i.r(t),i.d(t,{HaAssistPipelineSelector:()=>l});var s=i(85461),a=i(98597),n=i(196);i(37939);let l=(0,s.A)([(0,n.EM)("ha-selector-assist_pipeline")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return a.qy`
      <ha-assist-pipeline-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .includeLastUsed=${Boolean(this.selector.assist_pipeline?.include_last_used)}
      ></ha-assist-pipeline-picker>
    `}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    ha-conversation-agent-picker {
      width: 100%;
    }
  `}}]}}),a.WF)},82286:(e,t,i)=>{i.d(t,{QC:()=>s,ds:()=>o,mp:()=>l,nx:()=>n,u6:()=>d,vU:()=>a,zn:()=>r});const s=(e,t,i)=>"run-start"===t.type?e={init_options:i,stage:"ready",run:t.data,events:[t]}:e?((e="wake_word-start"===t.type?{...e,stage:"wake_word",wake_word:{...t.data,done:!1}}:"wake_word-end"===t.type?{...e,wake_word:{...e.wake_word,...t.data,done:!0}}:"stt-start"===t.type?{...e,stage:"stt",stt:{...t.data,done:!1}}:"stt-end"===t.type?{...e,stt:{...e.stt,...t.data,done:!0}}:"intent-start"===t.type?{...e,stage:"intent",intent:{...t.data,done:!1}}:"intent-end"===t.type?{...e,intent:{...e.intent,...t.data,done:!0}}:"tts-start"===t.type?{...e,stage:"tts",tts:{...t.data,done:!1}}:"tts-end"===t.type?{...e,tts:{...e.tts,...t.data,done:!0}}:"run-end"===t.type?{...e,stage:"done"}:"error"===t.type?{...e,stage:"error",error:t.data}:{...e}).events=[...e.events,t],e):void console.warn("Received unexpected event before receiving session",t),a=(e,t,i)=>e.connection.subscribeMessage(t,{...i,type:"assist_pipeline/run"}),n=e=>e.callWS({type:"assist_pipeline/pipeline/list"}),l=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:t}),d=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/create",...t}),r=(e,t,i)=>e.callWS({type:"assist_pipeline/pipeline/update",pipeline_id:t,...i}),o=e=>e.callWS({type:"assist_pipeline/language/list"})}};
//# sourceMappingURL=93hHYV33.js.map