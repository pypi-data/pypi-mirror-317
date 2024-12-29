export const id=9123;export const ids=[9123];export const modules={29123:(e,s,i)=>{var t=i(85461),r=i(69534),l=i(98597),a=i(196),o=i(11355);i(72266);var n=i(33167);i(91074);(0,t.A)([(0,a.EM)("flow-preview-template")],(function(e,s){class i extends s{constructor(...s){super(...s),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"flowType",value:void 0},{kind:"field",key:"handler",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"stepId",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"flowId",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"stepData",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_preview",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_listeners",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_error",value:void 0},{kind:"field",key:"_unsub",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.A)(i,"disconnectedCallback",this,3)([]),this._unsub&&(this._unsub.then((e=>e())),this._unsub=void 0)}},{kind:"method",key:"willUpdate",value:function(e){e.has("stepData")&&this._debouncedSubscribePreview()}},{kind:"method",key:"render",value:function(){return this._error?l.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:l.qy`<entity-preview-row
        .hass=${this.hass}
        .stateObj=${this._preview}
      ></entity-preview-row>
      ${this._listeners?.time?l.qy`
            <p>
              ${this.hass.localize("ui.dialogs.helper_settings.template.time")}
            </p>
          `:l.s6}
      ${this._listeners?this._listeners.all?l.qy`
              <p class="all_listeners">
                ${this.hass.localize("ui.dialogs.helper_settings.template.all_listeners")}
              </p>
            `:this._listeners.domains.length||this._listeners.entities.length?l.qy`
                <p>
                  ${this.hass.localize("ui.dialogs.helper_settings.template.listeners")}
                </p>
                <ul>
                  ${this._listeners.domains.sort().map((e=>l.qy`
                        <li>
                          <b
                            >${this.hass.localize("ui.dialogs.helper_settings.template.domain")}</b
                          >: ${e}
                        </li>
                      `))}
                  ${this._listeners.entities.sort().map((e=>l.qy`
                        <li>
                          <b
                            >${this.hass.localize("ui.dialogs.helper_settings.template.entity")}</b
                          >: ${e}
                        </li>
                      `))}
                </ul>
              `:this._listeners.time?l.s6:l.qy`<p class="all_listeners">
                  ${this.hass.localize("ui.dialogs.helper_settings.template.no_listeners")}
                </p>`:l.s6} `}},{kind:"field",key:"_setPreview",value(){return e=>{if("error"in e)return this._error=e.error,void(this._preview=void 0);this._error=void 0,this._listeners=e.listeners;const s=(new Date).toISOString();this._preview={entity_id:`${this.stepId}.___flow_preview___`,last_changed:s,last_updated:s,context:{id:"",parent_id:null,user_id:null},attributes:e.attributes,state:e.state}}}},{kind:"field",key:"_debouncedSubscribePreview",value(){return(0,o.s)((()=>{this._subscribePreview()}),250)}},{kind:"method",key:"_subscribePreview",value:async function(){var e,s,i,t,r;if(this._unsub&&((await this._unsub)(),this._unsub=void 0),"repair_flow"!==this.flowType)try{this._unsub=(e=this.hass,s=this.flowId,i=this.flowType,t=this.stepData,r=this._setPreview,e.connection.subscribeMessage(r,{type:"template/start_preview",flow_id:s,flow_type:i,user_input:t})),await this._unsub,(0,n.r)(this,"set-flow-errors",{errors:{}})}catch(l){"string"==typeof l.message?this._error=l.message:(this._error=void 0,(0,n.r)(this,"set-flow-errors",l.message)),this._unsub=void 0,this._preview=void 0}}}]}}),l.WF)}};
//# sourceMappingURL=atV-bVjo.js.map