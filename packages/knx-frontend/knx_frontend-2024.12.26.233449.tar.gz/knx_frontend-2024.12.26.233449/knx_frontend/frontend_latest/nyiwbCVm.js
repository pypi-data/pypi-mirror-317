export const id=8387;export const ids=[8387];export const modules={68873:(e,t,r)=>{r.d(t,{a:()=>i});var a=r(6601),n=r(19263);function i(e,t){const r=(0,n.m)(e.entity_id),i=void 0!==t?t:e?.state;if(["button","event","input_button","scene"].includes(r))return i!==a.Hh;if((0,a.g0)(i))return!1;if(i===a.KF&&"alert"!==r)return!1;switch(r){case"alarm_control_panel":return"disarmed"!==i;case"alert":return"idle"!==i;case"cover":case"valve":return"closed"!==i;case"device_tracker":case"person":return"not_home"!==i;case"lawn_mower":return["mowing","error"].includes(i);case"lock":return"locked"!==i;case"media_player":return"standby"!==i;case"vacuum":return!["idle","docked","paused"].includes(i);case"plant":return"problem"===i;case"group":return["on","home","open","locked","problem"].includes(i);case"timer":return"active"===i;case"camera":return"streaming"===i}return!0}},93259:(e,t,r)=>{var a=r(85461),n=r(69534),i=r(98597),o=r(196),s=r(90662),l=r(33167);r(91074),r(52631);const d={boolean:()=>r.e(7150).then(r.bind(r,47150)),constant:()=>r.e(3908).then(r.bind(r,73908)),float:()=>r.e(2292).then(r.bind(r,82292)),grid:()=>r.e(6880).then(r.bind(r,96880)),expandable:()=>r.e(6048).then(r.bind(r,66048)),integer:()=>r.e(3172).then(r.bind(r,73172)),multi_select:()=>r.e(5494).then(r.bind(r,95494)),positive_time_period_dict:()=>r.e(8590).then(r.bind(r,38590)),select:()=>r.e(3644).then(r.bind(r,73644)),string:()=>r.e(9345).then(r.bind(r,39345))},u=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;(0,a.A)([(0,o.EM)("ha-form")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof i.mN&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{"selector"in e||d[e.type]?.()}))}},{kind:"method",key:"render",value:function(){return i.qy`
      <div class="root" part="root">
        ${this.error&&this.error.base?i.qy`
              <ha-alert alert-type="error">
                ${this._computeError(this.error.base,this.schema)}
              </ha-alert>
            `:""}
        ${this.schema.map((e=>{const t=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),r=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return i.qy`
            ${t?i.qy`
                  <ha-alert own-margin alert-type="error">
                    ${this._computeError(t,e)}
                  </ha-alert>
                `:r?i.qy`
                    <ha-alert own-margin alert-type="warning">
                      ${this._computeWarning(r,e)}
                    </ha-alert>
                  `:""}
            ${"selector"in e?i.qy`<ha-selector
                  .schema=${e}
                  .hass=${this.hass}
                  .name=${e.name}
                  .selector=${e.selector}
                  .value=${u(this.data,e)}
                  .label=${this._computeLabel(e,this.data)}
                  .disabled=${e.disabled||this.disabled||!1}
                  .placeholder=${e.required?"":e.default}
                  .helper=${this._computeHelper(e)}
                  .localizeValue=${this.localizeValue}
                  .required=${e.required||!1}
                  .context=${this._generateContext(e)}
                ></ha-selector>`:(0,s._)(this.fieldElementName(e.type),{schema:e,data:u(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:this.hass?.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e),...this.getFormProperties()})}
          `}))}
      </div>
    `}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[r,a]of Object.entries(e.context))t[r]=this.data[a];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,n.A)(r,"createRenderRoot",this,3)([]);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const r=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data={...this.data,...r},(0,l.r)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?i.qy`<ul>
        ${e.map((e=>i.qy`<li>
              ${this.computeError?this.computeError(e,t):e}
            </li>`))}
      </ul>`:this.computeError?this.computeError(e,t):e}},{kind:"method",key:"_computeWarning",value:function(e,t){return this.computeWarning?this.computeWarning(e,t):e}},{kind:"get",static:!0,key:"styles",value:function(){return i.AH`
      .root > * {
        display: block;
      }
      .root > *:not([own-margin]):not(:last-child) {
        margin-bottom: 24px;
      }
      ha-alert[own-margin] {
        margin-bottom: 4px;
      }
    `}}]}}),i.WF)},6601:(e,t,r)=>{r.d(t,{HV:()=>i,Hh:()=>n,KF:()=>s,ON:()=>o,g0:()=>u,s7:()=>l});var a=r(79592);const n="unavailable",i="unknown",o="on",s="off",l=[n,i],d=[n,i,s],u=(0,a.g)(l);(0,a.g)(d)}};
//# sourceMappingURL=nyiwbCVm.js.map