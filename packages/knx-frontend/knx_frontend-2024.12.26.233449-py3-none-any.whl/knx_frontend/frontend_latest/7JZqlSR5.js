/*! For license information please see 7JZqlSR5.js.LICENSE.txt */
export const id=2882;export const ids=[2882];export const modules={53935:(t,i,e)=>{e.d(i,{A:()=>n});const o=t=>t<10?`0${t}`:t;function n(t){const i=Math.floor(t/3600),e=Math.floor(t%3600/60),n=Math.floor(t%3600%60);return i>0?`${i}:${o(e)}:${o(n)}`:e>0?`${e}:${o(n)}`:n>0?""+n:null}},49371:(t,i,e)=>{e.d(i,{PN:()=>a,jm:()=>s,sR:()=>r,t1:()=>n,yu:()=>l});e(31238);const o={"HA-Frontend-Base":`${location.protocol}//${location.host}`},n=(t,i,e)=>t.callApi("POST","config/config_entries/flow",{handler:i,show_advanced_options:Boolean(t.userData?.showAdvanced),entry_id:e},o),a=(t,i)=>t.callApi("GET",`config/config_entries/flow/${i}`,void 0,o),s=(t,i,e)=>t.callApi("POST",`config/config_entries/flow/${i}`,e,o),r=(t,i)=>t.callApi("DELETE",`config/config_entries/flow/${i}`),l=(t,i)=>t.callApi("GET","config/config_entries/flow_handlers"+(i?`?type=${i}`:""))},61399:(t,i,e)=>{e.d(i,{mx:()=>o,sF:()=>n});const o=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],n=(t,i)=>t.callWS({type:"schedule/create",...i})},25705:(t,i,e)=>{e.d(i,{PF:()=>s,CR:()=>n,ls:()=>a});var o=e(53935);const n=(t,i)=>t.callWS({type:"timer/create",...i}),a=t=>{if(!t.attributes.remaining)return;let i=function(t){const i=t.split(":").map(Number);return 3600*i[0]+60*i[1]+i[2]}(t.attributes.remaining);if("active"===t.state){const e=(new Date).getTime(),o=new Date(t.attributes.finishes_at).getTime();i=Math.max((o-e)/1e3,0)}return i},s=(t,i,e)=>{if(!i)return null;if("idle"===i.state||0===e)return t.formatEntityState(i);let n=(0,o.A)(e||0)||"0";return"paused"===i.state&&(n=`${n} (${t.formatEntityState(i)})`),n}},63283:(t,i,e)=>{e.d(i,{W:()=>r});var o=e(98597),n=e(49371),a=e(31238),s=e(50006);const r=(t,i)=>(0,s.g)(t,i,{flowType:"config_flow",showDevices:!0,createFlow:async(t,e)=>{const[o]=await Promise.all([(0,n.t1)(t,e,i.entryId),t.loadFragmentTranslation("config"),t.loadBackendTranslation("config",e),t.loadBackendTranslation("selector",e),t.loadBackendTranslation("title",e)]);return o},fetchFlow:async(t,i)=>{const e=await(0,n.PN)(t,i);return await t.loadFragmentTranslation("config"),await t.loadBackendTranslation("config",e.handler),await t.loadBackendTranslation("selector",e.handler),e},handleFlowStep:n.jm,deleteFlow:n.sR,renderAbortDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.abort.${i.reason}`,i.description_placeholders);return e?o.qy`
            <ha-markdown allowsvg breaks .content=${e}></ha-markdown>
          `:i.reason},renderShowFormStepHeader(t,i){return t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.title`,i.description_placeholders)||t.localize(`component.${i.handler}.title`)},renderShowFormStepDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.description`,i.description_placeholders);return e?o.qy`
            <ha-markdown allowsvg breaks .content=${e}></ha-markdown>
          `:""},renderShowFormStepFieldLabel(t,i,e,o){if("expandable"===e.type)return t.localize(`component.${i.handler}.config.step.${i.step_id}.sections.${e.name}.name`);const n=o?.path?.[0]?`sections.${o.path[0]}.`:"";return t.localize(`component.${i.handler}.config.step.${i.step_id}.${n}data.${e.name}`)||e.name},renderShowFormStepFieldHelper(t,i,e,n){if("expandable"===e.type)return t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.sections.${e.name}.description`);const a=n?.path?.[0]?`sections.${n.path[0]}.`:"",s=t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.${a}data_description.${e.name}`,i.description_placeholders);return s?o.qy`<ha-markdown breaks .content=${s}></ha-markdown>`:""},renderShowFormStepFieldError(t,i,e){return t.localize(`component.${i.translation_domain||i.translation_domain||i.handler}.config.error.${e}`,i.description_placeholders)||e},renderShowFormStepFieldLocalizeValue(t,i,e){return t.localize(`component.${i.handler}.selector.${e}`)},renderShowFormStepSubmitButton(t,i){return t.localize(`component.${i.handler}.config.step.${i.step_id}.submit`)||t.localize("ui.panel.config.integrations.config_flow."+(!1===i.last_step?"next":"submit"))},renderExternalStepHeader(t,i){return t.localize(`component.${i.handler}.config.step.${i.step_id}.title`)||t.localize("ui.panel.config.integrations.config_flow.external_step.open_site")},renderExternalStepDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.${i.step_id}.description`,i.description_placeholders);return o.qy`
        <p>
          ${t.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${e?o.qy`
              <ha-markdown
                allowsvg
                breaks
                .content=${e}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.create_entry.${i.description||"default"}`,i.description_placeholders);return o.qy`
        ${e?o.qy`
              <ha-markdown
                allowsvg
                breaks
                .content=${e}
              ></ha-markdown>
            `:""}
        <p>
          ${t.localize("ui.panel.config.integrations.config_flow.created_config",{name:i.title})}
        </p>
      `},renderShowFormProgressHeader(t,i){return t.localize(`component.${i.handler}.config.step.${i.step_id}.title`)||t.localize(`component.${i.handler}.title`)},renderShowFormProgressDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.progress.${i.progress_action}`,i.description_placeholders);return e?o.qy`
            <ha-markdown allowsvg breaks .content=${e}></ha-markdown>
          `:""},renderMenuHeader(t,i){return t.localize(`component.${i.handler}.config.step.${i.step_id}.title`)||t.localize(`component.${i.handler}.title`)},renderMenuDescription(t,i){const e=t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.description`,i.description_placeholders);return e?o.qy`
            <ha-markdown allowsvg breaks .content=${e}></ha-markdown>
          `:""},renderMenuOption(t,i,e){return t.localize(`component.${i.translation_domain||i.handler}.config.step.${i.step_id}.menu_options.${e}`,i.description_placeholders)},renderLoadingDescription(t,i,e,o){if("loading_flow"!==i&&"loading_step"!==i)return"";const n=o?.handler||e;return t.localize(`ui.panel.config.integrations.config_flow.loading.${i}`,{integration:n?(0,a.p$)(t.localize,n):t.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},50006:(t,i,e)=>{e.d(i,{g:()=>a});var o=e(33167);const n=()=>Promise.all([e.e(4932),e.e(5721)]).then(e.bind(e,55721)),a=(t,i,e)=>{(0,o.r)(t,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:{...i,flowConfig:e,dialogParentElement:t}})}},22882:(t,i,e)=>{e.r(i),e.d(i,{DialogHelperDetail:()=>w});var o=e(85461),n=(e(58068),e(87777),e(98597)),a=e(196),s=e(69760),r=e(32872),l=e(90662);e(73279);var d=e(88762),c=(e(9484),e(49371));var h=e(31238),m=e(61399),p=e(25705),u=e(63283),g=e(43799),f=e(47424),y=e(23135);const _={input_boolean:{create:(t,i)=>t.callWS({type:"input_boolean/create",...i}),import:()=>e.e(3266).then(e.bind(e,53266))},input_button:{create:(t,i)=>t.callWS({type:"input_button/create",...i}),import:()=>e.e(9946).then(e.bind(e,99946))},input_text:{create:(t,i)=>t.callWS({type:"input_text/create",...i}),import:()=>e.e(8431).then(e.bind(e,38431))},input_number:{create:(t,i)=>t.callWS({type:"input_number/create",...i}),import:()=>e.e(6805).then(e.bind(e,6805))},input_datetime:{create:(t,i)=>t.callWS({type:"input_datetime/create",...i}),import:()=>e.e(4293).then(e.bind(e,74293))},input_select:{create:(t,i)=>t.callWS({type:"input_select/create",...i}),import:()=>e.e(1186).then(e.bind(e,1186))},counter:{create:(t,i)=>t.callWS({type:"counter/create",...i}),import:()=>e.e(3971).then(e.bind(e,3971))},timer:{create:p.CR,import:()=>e.e(1240).then(e.bind(e,71240))},schedule:{create:m.sF,import:()=>Promise.all([e.e(1025),e.e(9502)]).then(e.bind(e,99502))}};let w=(0,o.A)([(0,a.EM)("dialog-helper-detail")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_item",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,a.wk)()],key:"_domain",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_submitting",value(){return!1}},{kind:"field",decorators:[(0,a.P)(".form")],key:"_form",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_helperFlows",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_loading",value(){return!1}},{kind:"field",key:"_params",value:void 0},{kind:"method",key:"showDialog",value:async function(t){this._params=t,this._domain=t.domain,this._item=void 0,this._domain&&this._domain in _&&await _[this._domain].import(),this._opened=!0,await this.updateComplete,this.hass.loadFragmentTranslation("config");const i=await(0,c.yu)(this.hass,["helper"]);await this.hass.loadBackendTranslation("title",i,!0),this._helperFlows=i}},{kind:"method",key:"closeDialog",value:function(){this._opened=!1,this._error=void 0,this._domain=void 0,this._params=void 0}},{kind:"method",key:"render",value:function(){if(!this._opened)return n.s6;let t;if(this._domain)t=n.qy`
        <div class="form" @value-changed=${this._valueChanged}>
          ${this._error?n.qy`<div class="error">${this._error}</div>`:""}
          ${(0,l._)(`ha-${this._domain}-form`,{hass:this.hass,item:this._item,new:!0})}
        </div>
        <mwc-button
          slot="primaryAction"
          @click=${this._createItem}
          .disabled=${this._submitting}
        >
          ${this.hass.localize("ui.panel.config.helpers.dialog.create")}
        </mwc-button>
        ${this._params?.domain?n.s6:n.qy`<mwc-button
              slot="secondaryAction"
              @click=${this._goBack}
              .disabled=${this._submitting}
            >
              ${this.hass.localize("ui.common.back")}
            </mwc-button>`}
      `;else if(this._loading||void 0===this._helperFlows)t=n.qy`<ha-circular-progress
        indeterminate
      ></ha-circular-progress>`;else{const i=[];for(const t of Object.keys(_))i.push([t,this.hass.localize(`ui.panel.config.helpers.types.${t}`)||t]);for(const t of this._helperFlows)i.push([t,(0,h.p$)(this.hass.localize,t)]);i.sort(((t,i)=>t[1].localeCompare(i[1]))),t=n.qy`
        <mwc-list
          innerRole="listbox"
          itemRoles="option"
          innerAriaLabel=${this.hass.localize("ui.panel.config.helpers.dialog.create_helper")}
          rootTabbable
          dialogInitialFocus
        >
          ${i.map((([t,i])=>{const e=!(t in _)||(0,r.x)(this.hass,t);return n.qy`
              <ha-list-item
                .disabled=${!e}
                hasmeta
                .domain=${t}
                @request-selected=${this._domainPicked}
                graphic="icon"
              >
                <img
                  slot="graphic"
                  loading="lazy"
                  alt=""
                  src=${(0,f.MR)({domain:t,type:"icon",useFallback:!0,darkOptimized:this.hass.themes?.darkMode})}
                  crossorigin="anonymous"
                  referrerpolicy="no-referrer"
                />
                <span class="item-text"> ${i} </span>
                <ha-icon-next slot="meta"></ha-icon-next>
              </ha-list-item>
              ${e?"":n.qy`
                    <simple-tooltip animation-delay="0"
                      >${this.hass.localize("ui.dialogs.helper_settings.platform_not_loaded",{platform:t})}</simple-tooltip
                    >
                  `}
            `}))}
        </mwc-list>
      `}return n.qy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        class=${(0,s.H)({"button-left":!this._domain})}
        scrimClickAction
        escapeKeyAction
        .hideActions=${!this._domain}
        .heading=${(0,d.l)(this.hass,this._domain?this.hass.localize("ui.panel.config.helpers.dialog.create_platform",{platform:(0,y.z)(this._domain)&&this.hass.localize(`ui.panel.config.helpers.types.${this._domain}`)||this._domain}):this.hass.localize("ui.panel.config.helpers.dialog.create_helper"))}
      >
        ${t}
      </ha-dialog>
    `}},{kind:"method",key:"_valueChanged",value:function(t){this._item=t.detail.value}},{kind:"method",key:"_createItem",value:async function(){if(this._domain&&this._item){this._submitting=!0,this._error="";try{const t=await _[this._domain].create(this.hass,this._item);this._params?.dialogClosedCallback&&t.id&&this._params.dialogClosedCallback({flowFinished:!0,entityId:`${this._domain}.${t.id}`}),this.closeDialog()}catch(t){this._error=t.message||"Unknown error"}finally{this._submitting=!1}}}},{kind:"method",key:"_domainPicked",value:async function(t){if(!(t=>!(!t.detail.selected||"property"!==t.detail.source||(t.currentTarget.selected=!1,0)))(t))return;const i=t.currentTarget.domain;if(i in _){this._loading=!0;try{await _[i].import(),this._domain=i}finally{this._loading=!1}this._focusForm()}else(0,u.W)(this,{startFlowHandler:i,manifest:await(0,h.QC)(this.hass,i),dialogClosedCallback:this._params.dialogClosedCallback}),this.closeDialog()}},{kind:"method",key:"_focusForm",value:async function(){await this.updateComplete,(this._form?.lastElementChild).focus()}},{kind:"method",key:"_goBack",value:function(){this._domain=void 0,this._item=void 0,this._error=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return[g.nA,n.AH`
        ha-dialog.button-left {
          --justify-action-buttons: flex-start;
        }
        ha-dialog {
          --dialog-content-padding: 0;
          --dialog-scroll-divider-color: transparent;
          --mdc-dialog-max-height: 60vh;
        }
        @media all and (min-width: 550px) {
          ha-dialog {
            --mdc-dialog-min-width: 500px;
          }
        }
        ha-icon-next {
          width: 24px;
        }
        .form {
          padding: 24px;
        }
      `]}}]}}),n.WF)},47424:(t,i,e)=>{e.d(i,{MR:()=>o,a_:()=>n,bg:()=>a});const o=t=>`https://brands.home-assistant.io/${t.brand?"brands/":""}${t.useFallback?"_/":""}${t.domain}/${t.darkOptimized?"dark_":""}${t.type}.png`,n=t=>t.split("/")[4],a=t=>t.startsWith("https://brands.home-assistant.io/")},87777:(t,i,e)=>{var o=e(98597);class n extends o.WF{static get styles(){return[o.AH`
        :host {
          display: block;
          position: absolute;
          outline: none;
          z-index: 1002;
          -moz-user-select: none;
          -ms-user-select: none;
          -webkit-user-select: none;
          user-select: none;
          cursor: default;
          pointer-events: none;
        }

        #tooltip {
          display: block;
          outline: none;
          font-size: var(--simple-tooltip-font-size, 10px);
          line-height: 1;
          background-color: var(--simple-tooltip-background, #616161);
          color: var(--simple-tooltip-text-color, white);
          padding: 8px;
          border-radius: var(--simple-tooltip-border-radius, 2px);
          width: var(--simple-tooltip-width);
        }

        @keyframes keyFrameScaleUp {
          0% {
            transform: scale(0);
          }

          100% {
            transform: scale(1);
          }
        }

        @keyframes keyFrameScaleDown {
          0% {
            transform: scale(1);
          }

          100% {
            transform: scale(0);
          }
        }

        @keyframes keyFrameFadeInOpacity {
          0% {
            opacity: 0;
          }

          100% {
            opacity: var(--simple-tooltip-opacity, 0.9);
          }
        }

        @keyframes keyFrameFadeOutOpacity {
          0% {
            opacity: var(--simple-tooltip-opacity, 0.9);
          }

          100% {
            opacity: 0;
          }
        }

        @keyframes keyFrameSlideDownIn {
          0% {
            transform: translateY(-2000px);
            opacity: 0;
          }

          10% {
            opacity: 0.2;
          }

          100% {
            transform: translateY(0);
            opacity: var(--simple-tooltip-opacity, 0.9);
          }
        }

        @keyframes keyFrameSlideDownOut {
          0% {
            transform: translateY(0);
            opacity: var(--simple-tooltip-opacity, 0.9);
          }

          10% {
            opacity: 0.2;
          }

          100% {
            transform: translateY(-2000px);
            opacity: 0;
          }
        }

        .fade-in-animation {
          opacity: 0;
          animation-delay: var(--simple-tooltip-delay-in, 500ms);
          animation-name: keyFrameFadeInOpacity;
          animation-iteration-count: 1;
          animation-timing-function: ease-in;
          animation-duration: var(--simple-tooltip-duration-in, 500ms);
          animation-fill-mode: forwards;
        }

        .fade-out-animation {
          opacity: var(--simple-tooltip-opacity, 0.9);
          animation-delay: var(--simple-tooltip-delay-out, 0ms);
          animation-name: keyFrameFadeOutOpacity;
          animation-iteration-count: 1;
          animation-timing-function: ease-in;
          animation-duration: var(--simple-tooltip-duration-out, 500ms);
          animation-fill-mode: forwards;
        }

        .scale-up-animation {
          transform: scale(0);
          opacity: var(--simple-tooltip-opacity, 0.9);
          animation-delay: var(--simple-tooltip-delay-in, 500ms);
          animation-name: keyFrameScaleUp;
          animation-iteration-count: 1;
          animation-timing-function: ease-in;
          animation-duration: var(--simple-tooltip-duration-in, 500ms);
          animation-fill-mode: forwards;
        }

        .scale-down-animation {
          transform: scale(1);
          opacity: var(--simple-tooltip-opacity, 0.9);
          animation-delay: var(--simple-tooltip-delay-out, 500ms);
          animation-name: keyFrameScaleDown;
          animation-iteration-count: 1;
          animation-timing-function: ease-in;
          animation-duration: var(--simple-tooltip-duration-out, 500ms);
          animation-fill-mode: forwards;
        }

        .slide-down-animation {
          transform: translateY(-2000px);
          opacity: 0;
          animation-delay: var(--simple-tooltip-delay-out, 500ms);
          animation-name: keyFrameSlideDownIn;
          animation-iteration-count: 1;
          animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
          animation-duration: var(--simple-tooltip-duration-out, 500ms);
          animation-fill-mode: forwards;
        }

        .slide-down-animation-out {
          transform: translateY(0);
          opacity: var(--simple-tooltip-opacity, 0.9);
          animation-delay: var(--simple-tooltip-delay-out, 500ms);
          animation-name: keyFrameSlideDownOut;
          animation-iteration-count: 1;
          animation-timing-function: cubic-bezier(0.4, 0, 1, 1);
          animation-duration: var(--simple-tooltip-duration-out, 500ms);
          animation-fill-mode: forwards;
        }

        .cancel-animation {
          animation-delay: -30s !important;
        }

        .hidden {
          position: absolute;
          left: -10000px;
          inset-inline-start: -10000px;
          inset-inline-end: initial;
          top: auto;
          width: 1px;
          height: 1px;
          overflow: hidden;
        }
      `]}render(){return o.qy` <div
      id="tooltip"
      class="hidden"
      @animationend="${this._onAnimationEnd}"
    >
      <slot></slot>
    </div>`}static get properties(){return{...super.properties,for:{type:String},manualMode:{type:Boolean,attribute:"manual-mode"},position:{type:String},fitToVisibleBounds:{type:Boolean,attribute:"fit-to-visible-bounds"},offset:{type:Number},marginTop:{type:Number,attribute:"margin-top"},animationDelay:{type:Number,attribute:"animation-delay"},animationEntry:{type:String,attribute:"animation-entry"},animationExit:{type:String,attribute:"animation-exit"},_showing:{type:Boolean}}}static get tag(){return"simple-tooltip"}constructor(){super(),this.manualMode=!1,this.position="bottom",this.fitToVisibleBounds=!1,this.offset=14,this.marginTop=14,this.animationEntry="",this.animationExit="",this.animationConfig={entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]},setTimeout((()=>{this.addEventListener("webkitAnimationEnd",this._onAnimationEnd.bind(this)),this.addEventListener("mouseenter",this.hide.bind(this))}),0)}get target(){var t=this.parentNode,i=this.getRootNode();return this.for?i.querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t}disconnectedCallback(){this.manualMode||this._removeListeners(),super.disconnectedCallback()}playAnimation(t){"entry"===t?this.show():"exit"===t&&this.hide()}cancelAnimation(){this.shadowRoot.querySelector("#tooltip").classList.add("cancel-animation")}show(){if(!this._showing){if(""===this.textContent.trim()){for(var t=!0,i=this.children,e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.shadowRoot.querySelector("#tooltip").classList.remove("hidden"),this.shadowRoot.querySelector("#tooltip").classList.remove("cancel-animation"),this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.shadowRoot.querySelector("#tooltip").classList.add(this._getAnimationType("entry"))}}hide(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0,clearTimeout(this.__debounceCancel),this.__debounceCancel=setTimeout((()=>{this._cancelAnimation()}),5e3)}}updatePosition(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,o=this.offsetParent.getBoundingClientRect(),n=this._target.getBoundingClientRect(),a=this.getBoundingClientRect(),s=(n.width-a.width)/2,r=(n.height-a.height)/2,l=n.left-o.left,d=n.top-o.top;switch(this.position){case"top":i=l+s,e=d-a.height-t;break;case"bottom":i=l+s,e=d+n.height+t;break;case"left":i=l-a.width-t,e=d+r;break;case"right":i=l+n.width+t,e=d+r}this.fitToVisibleBounds?(o.left+i+a.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),o.top+e+a.height>window.innerHeight?(this.style.bottom=o.height-d+t+"px",this.style.top="auto"):(this.style.top=Math.max(-o.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}}_addListeners(){this._target&&(this._target.addEventListener("mouseenter",this.show.bind(this)),this._target.addEventListener("focus",this.show.bind(this)),this._target.addEventListener("mouseleave",this.hide.bind(this)),this._target.addEventListener("blur",this.hide.bind(this)),this._target.addEventListener("tap",this.hide.bind(this)))}_findTarget(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()}_manualModeChanged(){this.manualMode?this._removeListeners():this._addListeners()}_cancelAnimation(){this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("entry")),this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("exit")),this.shadowRoot.querySelector("#tooltip").classList.remove("cancel-animation"),this.shadowRoot.querySelector("#tooltip").classList.add("hidden")}_onAnimationFinish(){this._showing&&(this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("entry")),this.shadowRoot.querySelector("#tooltip").classList.remove("cancel-animation"),this.shadowRoot.querySelector("#tooltip").classList.add(this._getAnimationType("exit")))}_onAnimationEnd(){this._animationPlaying=!1,this._showing||(this.shadowRoot.querySelector("#tooltip").classList.remove(this._getAnimationType("exit")),this.shadowRoot.querySelector("#tooltip").classList.add("hidden"))}_getAnimationType(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?document.documentElement.style.setProperty("--simple-tooltip-delay-in",i+"ms"):"exit"===t&&document.documentElement.style.setProperty("--simple-tooltip-delay-out",i+"ms")}return this.animationConfig[t][0].name}}_removeListeners(){this._target&&(this._target.removeEventListener("mouseover",this.show.bind(this)),this._target.removeEventListener("focusin",this.show.bind(this)),this._target.removeEventListener("mouseout",this.hide.bind(this)),this._target.removeEventListener("focusout",this.hide.bind(this)),this._target.removeEventListener("click",this.hide.bind(this)))}firstUpdated(t){this.setAttribute("role","tooltip"),this.setAttribute("tabindex",-1),this._findTarget()}updated(t){t.forEach(((t,i)=>{"for"==i&&this._findTarget(this[i],t),"manualMode"==i&&this._manualModeChanged(this[i],t),"animationDelay"==i&&this._delayChange(this[i],t)}))}_delayChange(t){500!==t&&document.documentElement.style.setProperty("--simple-tooltip-delay-in",t+"ms")}}customElements.define(n.tag,n)}};
//# sourceMappingURL=7JZqlSR5.js.map