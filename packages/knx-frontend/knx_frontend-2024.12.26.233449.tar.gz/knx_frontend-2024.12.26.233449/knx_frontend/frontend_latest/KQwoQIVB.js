export const id=1247;export const ids=[1247];export const modules={93259:(e,t,a)=>{var i=a(85461),o=a(69534),r=a(98597),n=a(196),s=a(90662),l=a(33167);a(91074),a(52631);const d={boolean:()=>a.e(7150).then(a.bind(a,47150)),constant:()=>a.e(3908).then(a.bind(a,73908)),float:()=>a.e(2292).then(a.bind(a,82292)),grid:()=>a.e(6880).then(a.bind(a,96880)),expandable:()=>a.e(6048).then(a.bind(a,66048)),integer:()=>a.e(3172).then(a.bind(a,73172)),multi_select:()=>a.e(5494).then(a.bind(a,95494)),positive_time_period_dict:()=>a.e(8590).then(a.bind(a,38590)),select:()=>a.e(3644).then(a.bind(a,73644)),string:()=>a.e(9345).then(a.bind(a,39345))},c=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;(0,i.A)([(0,n.EM)("ha-form")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof r.mN&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{"selector"in e||d[e.type]?.()}))}},{kind:"method",key:"render",value:function(){return r.qy`
      <div class="root" part="root">
        ${this.error&&this.error.base?r.qy`
              <ha-alert alert-type="error">
                ${this._computeError(this.error.base,this.schema)}
              </ha-alert>
            `:""}
        ${this.schema.map((e=>{const t=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),a=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return r.qy`
            ${t?r.qy`
                  <ha-alert own-margin alert-type="error">
                    ${this._computeError(t,e)}
                  </ha-alert>
                `:a?r.qy`
                    <ha-alert own-margin alert-type="warning">
                      ${this._computeWarning(a,e)}
                    </ha-alert>
                  `:""}
            ${"selector"in e?r.qy`<ha-selector
                  .schema=${e}
                  .hass=${this.hass}
                  .name=${e.name}
                  .selector=${e.selector}
                  .value=${c(this.data,e)}
                  .label=${this._computeLabel(e,this.data)}
                  .disabled=${e.disabled||this.disabled||!1}
                  .placeholder=${e.required?"":e.default}
                  .helper=${this._computeHelper(e)}
                  .localizeValue=${this.localizeValue}
                  .required=${e.required||!1}
                  .context=${this._generateContext(e)}
                ></ha-selector>`:(0,s._)(this.fieldElementName(e.type),{schema:e,data:c(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:this.hass?.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e),...this.getFormProperties()})}
          `}))}
      </div>
    `}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[a,i]of Object.entries(e.context))t[a]=this.data[i];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,o.A)(a,"createRenderRoot",this,3)([]);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data={...this.data,...a},(0,l.r)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?r.qy`<ul>
        ${e.map((e=>r.qy`<li>
              ${this.computeError?this.computeError(e,t):e}
            </li>`))}
      </ul>`:this.computeError?this.computeError(e,t):e}},{kind:"method",key:"_computeWarning",value:function(e,t){return this.computeWarning?this.computeWarning(e,t):e}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`
      .root > * {
        display: block;
      }
      .root > *:not([own-margin]):not(:last-child) {
        margin-bottom: 24px;
      }
      ha-alert[own-margin] {
        margin-bottom: 4px;
      }
    `}}]}}),r.WF)},21247:(e,t,a)=>{a.r(t);var i=a(85461),o=a(98597),r=a(196),n=a(33167),s=a(88762),l=(a(93259),a(66494),a(43799));const d=[{name:"from",required:!0,selector:{time:{no_second:!0}}},{name:"to",required:!0,selector:{time:{no_second:!0}}}];let c=(0,i.A)(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_data",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_params",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._error=void 0,this._data=e.block}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._data=void 0,(0,n.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params&&this._data?o.qy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${(0,s.l)(this.hass,this.hass.localize("ui.dialogs.helper_settings.schedule.edit_schedule_block"))}
      >
        <div>
          <ha-form
            .hass=${this.hass}
            .schema=${d}
            .data=${this._data}
            .error=${this._error}
            .computeLabel=${this._computeLabelCallback}
            @value-changed=${this._valueChanged}
          ></ha-form>
        </div>
        <ha-button
          slot="secondaryAction"
          class="warning"
          @click=${this._deleteBlock}
        >
          ${this.hass.localize("ui.common.delete")}
        </ha-button>
        <ha-button slot="primaryAction" @click=${this._updateBlock}>
          ${this.hass.localize("ui.common.save")}
        </ha-button>
      </ha-dialog>
    `:o.s6}},{kind:"method",key:"_valueChanged",value:function(e){this._error=void 0,this._data=e.detail.value}},{kind:"method",key:"_updateBlock",value:function(){try{this._params.updateBlock(this._data),this.closeDialog()}catch(e){this._error={base:e?e.message:"Unknown error"}}}},{kind:"method",key:"_deleteBlock",value:function(){try{this._params.deleteBlock(),this.closeDialog()}catch(e){this._error={base:e?e.message:"Unknown error"}}}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"from":return this.hass.localize("ui.dialogs.helper_settings.schedule.start");case"to":return this.hass.localize("ui.dialogs.helper_settings.schedule.end")}return""}}},{kind:"get",static:!0,key:"styles",value:function(){return[l.nA]}}]}}),o.WF);customElements.define("dialog-schedule-block-info",c)}};
//# sourceMappingURL=KQwoQIVB.js.map