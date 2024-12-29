export const id=3526;export const ids=[3526];export const modules={58636:(t,e,i)=>{i.d(e,{PE:()=>o});var s=i(67319),a=i(76415);const n=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],o=t=>t.first_weekday===a.zt.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(t.language).weekInfo.firstDay%7:(0,s.S)(t.language)%7:n.includes(t.first_weekday)?n.indexOf(t.first_weekday):1},3139:(t,e,i)=>{i.d(e,{K:()=>l});var s=i(45081),a=i(91499),n=i(91791),o=i(17781),r=i(58636);const d={second:45,minute:45,hour:22,day:5,week:4,month:11},c=(0,s.A)((t=>new Intl.RelativeTimeFormat(t.language,{numeric:"auto"}))),l=(t,e,i,s=!0)=>{const l=function(t,e=Date.now(),i,s={}){const c={...d,...s||{}},l=(+t-+e)/1e3;if(Math.abs(l)<c.second)return{value:Math.round(l),unit:"second"};const h=l/60;if(Math.abs(h)<c.minute)return{value:Math.round(h),unit:"minute"};const u=l/3600;if(Math.abs(u)<c.hour)return{value:Math.round(u),unit:"hour"};const p=new Date(t),v=new Date(e);p.setHours(0,0,0,0),v.setHours(0,0,0,0);const f=(0,a.c)(p,v);if(0===f)return{value:Math.round(u),unit:"hour"};if(Math.abs(f)<c.day)return{value:f,unit:"day"};const g=(0,r.PE)(i),y=(0,n.k)(p,{weekStartsOn:g}),m=(0,n.k)(v,{weekStartsOn:g}),k=(0,o.I)(y,m);if(0===k)return{value:f,unit:"day"};if(Math.abs(k)<c.week)return{value:k,unit:"week"};const _=p.getFullYear()-v.getFullYear(),w=12*_+p.getMonth()-v.getMonth();return 0===w?{value:k,unit:"week"}:Math.abs(w)<c.month||0===_?{value:w,unit:"month"}:{value:Math.round(_),unit:"year"}}(t,i,e);return s?c(e).format(l.value,l.unit):Intl.NumberFormat(e.language,{style:"unit",unit:l.unit,unitDisplay:"long"}).format(Math.abs(l.value))}},68873:(t,e,i)=>{i.d(e,{a:()=>n});var s=i(6601),a=i(19263);function n(t,e){const i=(0,a.m)(t.entity_id),n=void 0!==e?e:t?.state;if(["button","event","input_button","scene"].includes(i))return n!==s.Hh;if((0,s.g0)(n))return!1;if(n===s.KF&&"alert"!==i)return!1;switch(i){case"alarm_control_panel":return"disarmed"!==n;case"alert":return"idle"!==n;case"cover":case"valve":return"closed"!==n;case"device_tracker":case"person":return"not_home"!==n;case"lawn_mower":return["mowing","error"].includes(n);case"lock":return"locked"!==n;case"media_player":return"standby"!==n;case"vacuum":return!["idle","docked","paused"].includes(n);case"plant":return"problem"===n;case"group":return["on","home","open","locked","problem"].includes(n);case"timer":return"active"===n;case"camera":return"streaming"===n}return!0}},20678:(t,e,i)=>{i.d(e,{T:()=>a});var s=i(45081);const a=(t,e)=>{try{return n(e)?.of(t)??t}catch{return t}},n=(0,s.A)((t=>new Intl.DisplayNames(t.language,{type:"language",fallback:"code"})))},1695:(t,e,i)=>{i.d(e,{Z:()=>s});const s=t=>t.charAt(0).toUpperCase()+t.slice(1)},19411:(t,e,i)=>{i.d(e,{b:()=>s});const s=(t,e)=>{if(t===e)return!0;if(t&&e&&"object"==typeof t&&"object"==typeof e){if(t.constructor!==e.constructor)return!1;let i,a;if(Array.isArray(t)){if(a=t.length,a!==e.length)return!1;for(i=a;0!=i--;)if(!s(t[i],e[i]))return!1;return!0}if(t instanceof Map&&e instanceof Map){if(t.size!==e.size)return!1;for(i of t.entries())if(!e.has(i[0]))return!1;for(i of t.entries())if(!s(i[1],e.get(i[0])))return!1;return!0}if(t instanceof Set&&e instanceof Set){if(t.size!==e.size)return!1;for(i of t.entries())if(!e.has(i[0]))return!1;return!0}if(ArrayBuffer.isView(t)&&ArrayBuffer.isView(e)){if(a=t.length,a!==e.length)return!1;for(i=a;0!=i--;)if(t[i]!==e[i])return!1;return!0}if(t.constructor===RegExp)return t.source===e.source&&t.flags===e.flags;if(t.valueOf!==Object.prototype.valueOf)return t.valueOf()===e.valueOf();if(t.toString!==Object.prototype.toString)return t.toString()===e.toString();const n=Object.keys(t);if(a=n.length,a!==Object.keys(e).length)return!1;for(i=a;0!=i--;)if(!Object.prototype.hasOwnProperty.call(e,n[i]))return!1;for(i=a;0!=i--;){const a=n[i];if(!s(t[a],e[a]))return!1}return!0}return t!=t&&e!=e}},32714:(t,e,i)=>{var s=i(85461),a=i(98597),n=i(196);(0,s.A)([(0,n.EM)("ha-dialog-header")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"method",key:"render",value:function(){return a.qy`
      <header class="header">
        <div class="header-bar">
          <section class="header-navigation-icon">
            <slot name="navigationIcon"></slot>
          </section>
          <section class="header-content">
            <div class="header-title">
              <slot name="title"></slot>
            </div>
            <div class="header-subtitle">
              <slot name="subtitle"></slot>
            </div>
          </section>
          <section class="header-action-items">
            <slot name="actionItems"></slot>
          </section>
        </div>
        <slot></slot>
      </header>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[a.AH`
        :host {
          display: block;
        }
        :host([show-border]) {
          border-bottom: 1px solid
            var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
        }
        .header-bar {
          display: flex;
          flex-direction: row;
          align-items: flex-start;
          padding: 4px;
          box-sizing: border-box;
        }
        .header-content {
          flex: 1;
          padding: 10px 4px;
          min-width: 0;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .header-title {
          font-size: 22px;
          line-height: 28px;
          font-weight: 400;
        }
        .header-subtitle {
          font-size: 14px;
          line-height: 20px;
          color: var(--secondary-text-color);
        }
        @media all and (min-width: 450px) and (min-height: 500px) {
          .header-bar {
            padding: 12px;
          }
        }
        .header-navigation-icon {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
        .header-action-items {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
      `]}}]}}),a.WF)},52462:(t,e,i)=>{var s=i(85461),a=i(69534),n=i(55089),o=i(98597),r=i(196);(0,s.A)([(0,r.EM)("ha-md-list-item")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",static:!0,key:"styles",value(){return[...(0,a.A)(i,"styles",this),o.AH`
      :host {
        --ha-icon-display: block;
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-secondary: var(--secondary-text-color);
        --md-sys-color-surface: var(--card-background-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-sys-color-on-surface-variant: var(--secondary-text-color);
      }
      md-item {
        overflow: var(--md-item-overflow, hidden);
      }
    `]}}]}}),n.n)},71020:(t,e,i)=>{var s=i(85461),a=i(69534),n=i(98371),o=i(98597),r=i(196);(0,s.A)([(0,r.EM)("ha-md-list")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",static:!0,key:"styles",value(){return[...(0,a.A)(i,"styles",this),o.AH`
      :host {
        --md-sys-color-surface: var(--card-background-color);
      }
    `]}}]}}),n.Y)},71662:(t,e,i)=>{var s=i(85461),a=i(69534),n=i(20196),o=i(98597),r=i(196),d=i(3139),c=i(1695);(0,s.A)([(0,r.EM)("ha-relative-time")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"datetime",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"capitalize",value(){return!1}},{kind:"field",key:"_interval",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.A)(i,"disconnectedCallback",this,3)([]),this._clearInterval()}},{kind:"method",key:"connectedCallback",value:function(){(0,a.A)(i,"connectedCallback",this,3)([]),this.datetime&&this._startInterval()}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"firstUpdated",value:function(t){(0,a.A)(i,"firstUpdated",this,3)([t]),this._updateRelative()}},{kind:"method",key:"update",value:function(t){(0,a.A)(i,"update",this,3)([t]),this._updateRelative()}},{kind:"method",key:"_clearInterval",value:function(){this._interval&&(window.clearInterval(this._interval),this._interval=void 0)}},{kind:"method",key:"_startInterval",value:function(){this._clearInterval(),this._interval=window.setInterval((()=>this._updateRelative()),6e4)}},{kind:"method",key:"_updateRelative",value:function(){if(this.datetime){const t="string"==typeof this.datetime?(0,n.H)(this.datetime):this.datetime,e=(0,d.K)(t,this.hass.locale);this.innerHTML=this.capitalize?(0,c.Z)(e):e}else this.innerHTML=this.hass.localize("ui.components.relative_time.never")}}]}}),o.mN)},75973:(t,e,i)=>{var s=i(85461),a=i(69534),n=i(98597),o=i(196),r=i(33167),d=i(24517),c=i(11355),l=i(6933);i(9484),i(96334);const h="__NONE_OPTION__";(0,s.A)([(0,o.EM)("ha-tts-voice-picker")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"engineId",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_voices",value:void 0},{kind:"field",decorators:[(0,o.P)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"render",value:function(){if(!this._voices)return n.s6;const t=this.value??(this.required?this._voices[0]?.voice_id:h);return n.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.tts-voice-picker.voice")}
        .value=${t}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${d.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?n.s6:n.qy`<ha-list-item .value=${h}>
              ${this.hass.localize("ui.components.tts-voice-picker.none")}
            </ha-list-item>`}
        ${this._voices.map((t=>n.qy`<ha-list-item .value=${t.voice_id}>
              ${t.name}
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(t){(0,a.A)(i,"willUpdate",this,3)([t]),this.hasUpdated?(t.has("language")||t.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}},{kind:"field",key:"_debouncedUpdateVoices",value(){return(0,c.s)((()=>this._updateVoices()),500)}},{kind:"method",key:"_updateVoices",value:async function(){this.engineId&&this.language?(this._voices=(await(0,l.z3)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((t=>t.voice_id===this.value))||(this.value=void 0,(0,r.r)(this,"value-changed",{value:this.value})))):this._voices=void 0}},{kind:"method",key:"updated",value:function(t){(0,a.A)(i,"updated",this,3)([t]),t.has("_voices")&&this._select?.value!==this.value&&(this._select?.layoutOptions(),(0,r.r)(this,"value-changed",{value:this._select?.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(t){const e=t.target;!this.hass||""===e.value||e.value===this.value||void 0===this.value&&e.value===h||(this.value=e.value===h?void 0:e.value,(0,r.r)(this,"value-changed",{value:this.value}))}}]}}),n.WF)},82286:(t,e,i)=>{i.d(e,{QC:()=>s,ds:()=>c,mp:()=>o,nx:()=>n,u6:()=>r,vU:()=>a,zn:()=>d});const s=(t,e,i)=>"run-start"===e.type?t={init_options:i,stage:"ready",run:e.data,events:[e]}:t?((t="wake_word-start"===e.type?{...t,stage:"wake_word",wake_word:{...e.data,done:!1}}:"wake_word-end"===e.type?{...t,wake_word:{...t.wake_word,...e.data,done:!0}}:"stt-start"===e.type?{...t,stage:"stt",stt:{...e.data,done:!1}}:"stt-end"===e.type?{...t,stt:{...t.stt,...e.data,done:!0}}:"intent-start"===e.type?{...t,stage:"intent",intent:{...e.data,done:!1}}:"intent-end"===e.type?{...t,intent:{...t.intent,...e.data,done:!0}}:"tts-start"===e.type?{...t,stage:"tts",tts:{...e.data,done:!1}}:"tts-end"===e.type?{...t,tts:{...t.tts,...e.data,done:!0}}:"run-end"===e.type?{...t,stage:"done"}:"error"===e.type?{...t,stage:"error",error:e.data}:{...t}).events=[...t.events,e],t):void console.warn("Received unexpected event before receiving session",e),a=(t,e,i)=>t.connection.subscribeMessage(e,{...i,type:"assist_pipeline/run"}),n=t=>t.callWS({type:"assist_pipeline/pipeline/list"}),o=(t,e)=>t.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:e}),r=(t,e)=>t.callWS({type:"assist_pipeline/pipeline/create",...e}),d=(t,e,i)=>t.callWS({type:"assist_pipeline/pipeline/update",pipeline_id:e,...i}),c=t=>t.callWS({type:"assist_pipeline/language/list"})},2365:(t,e,i)=>{i.d(e,{eN:()=>s});const s=t=>t.callWS({type:"cloud/status"})},97976:(t,e,i)=>{i.d(e,{j:()=>a});var s=i(33167);const a=t=>{(0,s.r)(window,"haptic",t)}},11373:(t,e,i)=>{i.d(e,{T:()=>s});const s=(t,e,i)=>t.callWS({type:"stt/engine/list",language:e,country:i})},6933:(t,e,i)=>{i.d(e,{EF:()=>o,S_:()=>s,Xv:()=>r,ni:()=>n,u1:()=>d,z3:()=>c});const s=(t,e)=>t.callApi("POST","tts_get_url",e),a="media-source://tts/",n=t=>t.startsWith(a),o=t=>t.substring(19),r=(t,e,i)=>t.callWS({type:"tts/engine/list",language:e,country:i}),d=(t,e)=>t.callWS({type:"tts/engine/get",engine_id:e}),c=(t,e,i)=>t.callWS({type:"tts/engine/voices",engine_id:e,language:i})},17214:(t,e,i)=>{i.r(e),i.d(e,{HaVoiceAssistantSetupDialog:()=>J,STEP:()=>X});var s=i(85461),a=(i(58068),i(98597)),n=i(196),o=i(45081),r=i(33167),d=i(19263),c=(i(88762),i(32575)),l=i(6601),h=i(43799),u=i(40884),p=i(31447);const v=[h.RF,a.AH`
    :host {
      align-items: center;
      text-align: center;
      min-height: 300px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 100%;
      padding: 24px;
      box-sizing: border-box;
    }
    .content {
      flex: 1;
    }
    .content img {
      width: 120px;
    }
    @media all and (max-width: 450px), all and (max-height: 500px) {
      .content img {
        margin-top: 68px;
        margin-bottom: 68px;
      }
    }
    .footer {
      display: flex;
      width: 100%;
      flex-direction: row;
      justify-content: flex-end;
    }
    .footer.full-width {
      flex-direction: column;
    }
    .footer.full-width ha-button {
      width: 100%;
    }
    .footer.centered {
      justify-content: center;
    }
    .footer.side-by-side {
      justify-content: space-between;
    }
  `];i(57046);(0,s.A)([(0,n.EM)("ha-voice-assistant-setup-step-area")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"deviceId",value:void 0},{kind:"method",key:"render",value:function(){const t=this.hass.devices[this.deviceId];return a.qy`<div class="content">
        <img src="/static/images/voice-assistant/area.png" />
        <h1>Select area</h1>
        <p class="secondary">
          When you voice assistant knows where it is, it can better control the
          devices around it.
        </p>
        <ha-area-picker
          .hass=${this.hass}
          .value=${t.area_id}
        ></ha-area-picker>
      </div>
      <div class="footer">
        <ha-button @click=${this._setArea} unelevated>Next</ha-button>
      </div>`}},{kind:"method",key:"_setArea",value:async function(){const t=this.shadowRoot.querySelector("ha-area-picker").value;t?(await(0,u.FB)(this.hass,this.deviceId,{area_id:t}),this._nextStep()):(0,p.K$)(this,{text:"Please select an area"})}},{kind:"method",key:"_nextStep",value:function(){(0,r.r)(this,"next-step")}},{kind:"field",static:!0,key:"styles",value(){return[v,a.AH`
      ha-area-picker {
        display: block;
        width: 100%;
        margin-bottom: 24px;
      }
    `]}}]}}),a.WF);i(71020),i(52462);var f=i(20678);(0,s.A)([(0,n.EM)("ha-voice-assistant-setup-step-change-wake-word")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"assistConfiguration",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"assistEntityId",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`<div class="padding content">
        <img src="/static/images/voice-assistant/change-wake-word.png" />
        <h1>Change wake word</h1>
        <p class="secondary">
          Some wake words are better for
          ${(0,f.T)(this.hass.locale.language,this.hass.locale)} and
          voice than others. Please try them out.
        </p>
      </div>
      <ha-md-list>
        ${this.assistConfiguration.available_wake_words.map((t=>a.qy`<ha-md-list-item
              interactive
              type="button"
              @click=${this._wakeWordPicked}
              .value=${t.id}
            >
              ${t.wake_word}
              <ha-icon-next slot="end"></ha-icon-next>
            </ha-md-list-item>`))}
      </ha-md-list>`}},{kind:"method",key:"_wakeWordPicked",value:async function(t){if(!this.assistEntityId)return;const e=t.currentTarget.value;await(0,c.g5)(this.hass,this.assistEntityId,[e]),this._nextStep()}},{kind:"method",key:"_nextStep",value:function(){(0,r.r)(this,"next-step",{step:X.WAKEWORD,updateConfig:!0})}},{kind:"field",static:!0,key:"styles",value(){return[v,a.AH`
      :host {
        padding: 0;
      }
      .padding {
        padding: 24px;
      }
      ha-md-list {
        width: 100%;
        text-align: initial;
        margin-bottom: 24px;
      }
    `]}}]}}),a.WF);var g=i(69534),y=(i(66494),i(73279),i(31750));(0,s.A)([(0,n.EM)("ha-voice-assistant-setup-step-check")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"assistEntityId",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_status",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_showLoader",value(){return!1}},{kind:"method",key:"willUpdate",value:function(t){(0,g.A)(i,"willUpdate",this,3)([t]),this.hasUpdated?"success"===this._status&&t.has("hass")&&"idle"===this.hass.states[this.assistEntityId]?.state&&this._nextStep():this._testConnection()}},{kind:"method",key:"render",value:function(){return a.qy`<div class="content">
      ${"timeout"===this._status?a.qy`<img src="/static/images/voice-assistant/error.png" />
            <h1>The voice assistant is unable to connect to Home Assistant</h1>
            <p class="secondary">
              To play audio, the voice assistant device has to connect to Home
              Assistant to fetch the files. Our test shows that the device is
              unable to reach the Home Assistant server.
            </p>
            <div class="footer">
              <a
                href=${(0,y.o)(this.hass,"/voice_control/troubleshooting/#i-dont-get-a-voice-response")}
                ><ha-button>Help me</ha-button></a
              >
              <ha-button @click=${this._testConnection}>Retry</ha-button>
            </div>`:a.qy`<img src="/static/images/voice-assistant/hi.png" />
            <h1>Hi</h1>
            <p class="secondary">
              Over the next couple steps we're going to personalize your voice
              assistant.
            </p>

            ${this._showLoader?a.qy`<ha-circular-progress
                  indeterminate
                ></ha-circular-progress>`:a.s6} `}
    </div>`}},{kind:"method",key:"_testConnection",value:async function(){this._status=void 0,this._showLoader=!1;const t=setTimeout((()=>{this._showLoader=!0}),3e3),e=await(0,c.tl)(this.hass,this.assistEntityId);clearTimeout(t),this._showLoader=!1,this._status=e.status}},{kind:"method",key:"_nextStep",value:function(){(0,r.r)(this,"next-step",{noPrevious:!0})}},{kind:"field",static:!0,key:"styles",value(){return v}}]}}),a.WF);i(29222);var m=i(47424);(0,s.A)([(0,n.EM)("ha-voice-assistant-setup-step-cloud")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`<div class="content">
        <img
          src=${`/static/images/logo_nabu_casa${this.hass.themes?.darkMode?"_dark":""}.png`}
          alt="Nabu Casa logo"
        />
        <h1>The power of Home Assistant Cloud</h1>
        <div class="features">
          <div class="feature speech">
            <div class="logos">
              <div class="round-icon">
                <ha-svg-icon .path=${"M8,7A2,2 0 0,1 10,9V14A2,2 0 0,1 8,16A2,2 0 0,1 6,14V9A2,2 0 0,1 8,7M14,14C14,16.97 11.84,19.44 9,19.92V22H7V19.92C4.16,19.44 2,16.97 2,14H4A4,4 0 0,0 8,18A4,4 0 0,0 12,14H14M21.41,9.41L17.17,13.66L18.18,10H14A2,2 0 0,1 12,8V4A2,2 0 0,1 14,2H20A2,2 0 0,1 22,4V8C22,8.55 21.78,9.05 21.41,9.41Z"}></ha-svg-icon>
              </div>
            </div>
            <h2>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.speech.title")}
              <span class="no-wrap"></span>
            </h2>
            <p>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.speech.text")}
            </p>
          </div>
          <div class="feature access">
            <div class="logos">
              <div class="round-icon">
                <ha-svg-icon .path=${"M17.9,17.39C17.64,16.59 16.89,16 16,16H15V13A1,1 0 0,0 14,12H8V10H10A1,1 0 0,0 11,9V7H13A2,2 0 0,0 15,5V4.59C17.93,5.77 20,8.64 20,12C20,14.08 19.2,15.97 17.9,17.39M11,19.93C7.05,19.44 4,16.08 4,12C4,11.38 4.08,10.78 4.21,10.21L9,15V16A2,2 0 0,0 11,18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"}></ha-svg-icon>
              </div>
            </div>
            <h2>
              Remote access
              <span class="no-wrap"></span>
            </h2>
            <p>
              Secure remote access to your system while supporting the
              development of Home Assistant.
            </p>
          </div>
          <div class="feature">
            <div class="logos">
              <img
                alt="Google Assistant"
                src=${(0,m.MR)({domain:"google_assistant",type:"icon",darkOptimized:this.hass.themes?.darkMode})}
                crossorigin="anonymous"
                referrerpolicy="no-referrer"
              />
              <img
                alt="Amazon Alexa"
                src=${(0,m.MR)({domain:"alexa",type:"icon",darkOptimized:this.hass.themes?.darkMode})}
                crossorigin="anonymous"
                referrerpolicy="no-referrer"
              />
            </div>
            <h2>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.assistants.title")}
            </h2>
            <p>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.assistants.text")}
            </p>
          </div>
        </div>
      </div>
      <div class="footer side-by-side">
        <a
          href="https://www.nabucasa.com"
          target="_blank"
          rel="noreferrer noopenner"
        >
          <ha-button>
            <ha-svg-icon .path=${"M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"} slot="icon"></ha-svg-icon>
            nabucasa.com
          </ha-button>
        </a>
        <a href="/config/cloud/register" @click=${this._close}
          ><ha-button unelevated>Try 1 month for free</ha-button></a
        >
      </div>`}},{kind:"method",key:"_close",value:function(){(0,r.r)(this,"closed")}},{kind:"field",static:!0,key:"styles",value(){return[v,a.AH`
      .features {
        display: flex;
        flex-direction: column;
        grid-gap: 16px;
        padding: 16px;
      }
      .feature {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 16px;
      }
      .feature .logos {
        margin-bottom: 16px;
      }
      .feature .logos > * {
        width: 40px;
        height: 40px;
        margin: 0 4px;
      }
      .round-icon {
        border-radius: 50%;
        color: #6e41ab;
        background-color: #e8dcf7;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
      }
      .access .round-icon {
        color: #00aef8;
        background-color: #cceffe;
      }
      .feature h2 {
        font-weight: 500;
        font-size: 16px;
        line-height: 24px;
        margin-top: 0;
        margin-bottom: 8px;
      }
      .feature p {
        font-weight: 400;
        font-size: 14px;
        line-height: 20px;
        margin: 0;
      }
    `]}}]}}),a.WF);var k=i(32872),_=i(82286),w=i(2365),b=i(11373),x=i(6933);(0,s.A)([(0,n.EM)("ha-voice-assistant-setup-step-pipeline")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"assistConfiguration",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"deviceId",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"assistEntityId",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_showFirst",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_showSecond",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_showThird",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_showFourth",value(){return!1}},{kind:"method",key:"willUpdate",value:function(t){(0,g.A)(i,"willUpdate",this,3)([t]),this.hasUpdated||this._checkCloud()}},{kind:"method",key:"firstUpdated",value:function(t){(0,g.A)(i,"firstUpdated",this,3)([t]),setTimeout((()=>{this._showFirst=!0}),200),setTimeout((()=>{this._showSecond=!0}),600),setTimeout((()=>{this._showThird=!0}),3e3),setTimeout((()=>{this._showFourth=!0}),8e3)}},{kind:"method",key:"render",value:function(){return a.qy`<div class="content">
      <h1>What hardware do you want to use?</h1>
      <p class="secondary">
        How quickly your assistant responds depends on the power of the
        hardware.
      </p>
      <div class="container">
        <div class="messages-container cloud">
          <div class="message user ${this._showFirst?"show":""}">
            ${this._showFirst?"Turn on the lights in the bedroom":"…"}
          </div>
          ${this._showFirst?a.qy`<div class="timing user">0.2 seconds</div>`:a.s6}
          ${this._showFirst?a.qy` <div class="message hass ${this._showSecond?"show":""}">
                ${this._showSecond?"Turned on the lights":"…"}
              </div>`:a.s6}
          ${this._showSecond?a.qy`<div class="timing hass">0.4 seconds</div>`:a.s6}
        </div>
        <h2>Home Assistant Cloud</h2>
        <p>Ideal if you don't have a powerful system at home.</p>
        <ha-button @click=${this._setupCloud}>Learn more</ha-button>
      </div>
      <div class="container">
        <div class="messages-container rpi">
          <div class="message user ${this._showThird?"show":""}">
            ${this._showThird?"Turn on the lights in the bedroom":"…"}
          </div>
          ${this._showThird?a.qy`<div class="timing user">3 seconds</div>`:a.s6}
          ${this._showThird?a.qy`<div class="message hass ${this._showFourth?"show":""}">
                ${this._showFourth?"Turned on the lights":"…"}
              </div>`:a.s6}
          ${this._showFourth?a.qy`<div class="timing hass">5 seconds</div>`:a.s6}
        </div>
        <h2>Do-it-yourself</h2>
        <p>
          Install add-ons or containers to run it on your own system. Powerful
          hardware is needed for fast responses.
        </p>
        <a
          href=${(0,y.o)(this.hass,"/voice_control/voice_remote_local_assistant/")}
          target="_blank"
          rel="noreferrer noopenner"
        >
          <ha-button @click=${this._skip}>
            <ha-svg-icon .path=${"M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"} slot="icon"></ha-svg-icon>
            Learn more</ha-button
          >
        </a>
      </div>
    </div>`}},{kind:"method",key:"_checkCloud",value:async function(){if(!(0,k.x)(this.hass,"cloud"))return;const t=await(0,w.eN)(this.hass);if(!t.logged_in||!t.active_subscription)return;let e,i;for(const o of Object.values(this.hass.entities))if("cloud"===o.platform){const t=(0,d.m)(o.entity_id);if("tts"===t)e=o.entity_id;else{if("stt"!==t)continue;i=o.entity_id}if(e&&i)break}const s=await(0,_.nx)(this.hass),a=s.pipelines.find((t=>t.id===s.preferred_pipeline));if(a&&a.tts_engine===e&&a.stt_engine===i)return await this.hass.callService("select","select_option",{option:"preferred"},{entity_id:this.assistConfiguration?.pipeline_entity_id}),void(0,r.r)(this,"next-step",{step:X.SUCCESS,noPrevious:!0});let n=s.pipelines.find((t=>t.tts_engine===e&&t.stt_engine===i));if(!n){const t=(await(0,x.Xv)(this.hass,this.hass.config.language,this.hass.config.country||void 0)).providers.find((t=>t.engine_id===e)),a=await(0,x.z3)(this.hass,e,t?.supported_languages[0]||this.hass.config.language),o=(await(0,b.T)(this.hass,this.hass.config.language,this.hass.config.country||void 0)).providers.find((t=>t.engine_id===i));let r="Home Assistant Cloud",d=1;for(;s.pipelines.find((t=>t.name===r));)r=`${r} ${d}`,d++;n=await(0,_.u6)(this.hass,{name:r,language:this.hass.config.language,conversation_engine:"conversation.home_assistant",conversation_language:this.hass.config.language,stt_engine:i,stt_language:o.supported_languages[0],tts_engine:e,tts_language:t.supported_languages[0],tts_voice:a.voices[0].voice_id,wake_word_entity:null,wake_word_id:null})}await this.hass.callService("select","select_option",{option:n.name},{entity_id:this.assistConfiguration?.pipeline_entity_id}),(0,r.r)(this,"next-step",{step:X.SUCCESS,noPrevious:!0})}},{kind:"method",key:"_setupCloud",value:async function(){this._nextStep(X.CLOUD)}},{kind:"method",key:"_skip",value:function(){this._nextStep(X.SUCCESS)}},{kind:"method",key:"_nextStep",value:function(t){(0,r.r)(this,"next-step",{step:t})}},{kind:"field",static:!0,key:"styles",value(){return[v,a.AH`
      .container {
        border-radius: 16px;
        border: 1px solid var(--divider-color);
        overflow: hidden;
        padding-bottom: 16px;
      }
      .container:last-child {
        margin-top: 16px;
      }
      .messages-container {
        padding: 24px;
        box-sizing: border-box;
        height: 195px;
        background: var(--input-fill-color);
        display: flex;
        flex-direction: column;
      }
      .message {
        white-space: nowrap;
        font-size: 18px;
        clear: both;
        margin: 8px 0;
        padding: 8px;
        border-radius: 15px;
        height: 36px;
        box-sizing: border-box;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 30px;
      }
      .rpi .message {
        transition: width 1s;
      }
      .cloud .message {
        transition: width 0.5s;
      }

      .message.user {
        margin-left: 24px;
        margin-inline-start: 24px;
        margin-inline-end: initial;
        align-self: self-end;
        text-align: right;
        border-bottom-right-radius: 0px;
        background-color: var(--primary-color);
        color: var(--text-primary-color);
        direction: var(--direction);
      }
      .timing.user {
        align-self: self-end;
      }

      .message.user.show {
        width: 295px;
      }

      .message.hass {
        margin-right: 24px;
        margin-inline-end: 24px;
        margin-inline-start: initial;
        align-self: self-start;
        border-bottom-left-radius: 0px;
        background-color: var(--secondary-background-color);
        color: var(--primary-text-color);
        direction: var(--direction);
      }
      .timing.hass {
        align-self: self-start;
      }

      .message.hass.show {
        width: 184px;
      }
    `]}}]}}),a.WF);var $=i(24517);i(96334),i(75973);const A=(t,e,i)=>t.callService("select","select_option",{option:i},{entity_id:e}),C=()=>i.e(9168).then(i.bind(i,9168));i(23981);var E=i(91330),S=i(97976);function I(t,e){if(e.has("_config"))return!0;if(!e.has("hass"))return!1;const i=e.get("hass");return!i||(i.connected!==t.hass.connected||i.themes!==t.hass.themes||i.locale!==t.hass.locale||i.localize!==t.hass.localize||i.formatEntityState!==t.hass.formatEntityState||i.formatEntityAttributeName!==t.hass.formatEntityAttributeName||i.formatEntityAttributeValue!==t.hass.formatEntityAttributeValue||i.config.state!==t.hass.config.state)}function M(t,e,i){return t.states[i]!==e.states[i]}function H(t,e,i){const s=t.entities[i],a=e.entities[i];return s?.display_precision!==a?.display_precision}var W=i(69760),L=i(79278),T=i(93758);i(85426),i(71662);var q=i(3358),P=i(19411),z=i(14630);class F extends HTMLElement{constructor(...t){super(...t),this.holdTime=500,this.timer=void 0,this.held=!1,this.cancelled=!1,this.dblClickTimeout=void 0}connectedCallback(){Object.assign(this.style,{position:"fixed",width:z.C?"100px":"50px",height:z.C?"100px":"50px",transform:"translate(-50%, -50%) scale(0)",pointerEvents:"none",zIndex:"999",background:"var(--primary-color)",display:null,opacity:"0.2",borderRadius:"50%",transition:"transform 180ms ease-in-out"}),["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach((t=>{document.addEventListener(t,(()=>{this.cancelled=!0,this.timer&&(this.stopAnimation(),clearTimeout(this.timer),this.timer=void 0)}),{passive:!0})}))}bind(t,e={}){t.actionHandler&&(0,P.b)(e,t.actionHandler.options)||(t.actionHandler?(t.removeEventListener("touchstart",t.actionHandler.start),t.removeEventListener("touchend",t.actionHandler.end),t.removeEventListener("touchcancel",t.actionHandler.end),t.removeEventListener("mousedown",t.actionHandler.start),t.removeEventListener("click",t.actionHandler.end),t.removeEventListener("keydown",t.actionHandler.handleKeyDown)):t.addEventListener("contextmenu",(t=>{const e=t||window.event;return e.preventDefault&&e.preventDefault(),e.stopPropagation&&e.stopPropagation(),e.cancelBubble=!0,e.returnValue=!1,!1})),t.actionHandler={options:e},e.disabled||(t.actionHandler.start=t=>{let i,s;this.cancelled=!1,t.touches?(i=t.touches[0].clientX,s=t.touches[0].clientY):(i=t.clientX,s=t.clientY),e.hasHold&&(this.held=!1,this.timer=window.setTimeout((()=>{this.startAnimation(i,s),this.held=!0}),this.holdTime))},t.actionHandler.end=t=>{if(["touchend","touchcancel"].includes(t.type)&&this.cancelled)return;const i=t.target;t.cancelable&&t.preventDefault(),e.hasHold&&(clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0),e.hasHold&&this.held?(0,r.r)(i,"action",{action:"hold"}):e.hasDoubleClick?"click"===t.type&&t.detail<2||!this.dblClickTimeout?this.dblClickTimeout=window.setTimeout((()=>{this.dblClickTimeout=void 0,(0,r.r)(i,"action",{action:"tap"})}),250):(clearTimeout(this.dblClickTimeout),this.dblClickTimeout=void 0,(0,r.r)(i,"action",{action:"double_tap"})):(0,r.r)(i,"action",{action:"tap"})},t.actionHandler.handleKeyDown=t=>{["Enter"," "].includes(t.key)&&t.currentTarget.actionHandler.end(t)},t.addEventListener("touchstart",t.actionHandler.start,{passive:!0}),t.addEventListener("touchend",t.actionHandler.end),t.addEventListener("touchcancel",t.actionHandler.end),t.addEventListener("mousedown",t.actionHandler.start,{passive:!0}),t.addEventListener("click",t.actionHandler.end),t.addEventListener("keydown",t.actionHandler.handleKeyDown)))}startAnimation(t,e){Object.assign(this.style,{left:`${t}px`,top:`${e}px`,transform:"translate(-50%, -50%) scale(1)"})}stopAnimation(){Object.assign(this.style,{left:null,top:null,transform:"translate(-50%, -50%) scale(0)"})}}customElements.define("action-handler",F);const D=(t,e)=>{const i=(()=>{const t=document.body;if(t.querySelector("action-handler"))return t.querySelector("action-handler");const e=document.createElement("action-handler");return t.appendChild(e),e})();i&&i.bind(t,e)},Z=(0,q.u$)(class extends q.WL{update(t,[e]){return D(t.element,e),a.c0}render(t){}});var V=i(13314),O=i(31238);const U=()=>i.e(810).then(i.bind(i,60810));var N=i(34947);const R=(t,e)=>((t,e,i=!0)=>{const s=(0,d.m)(e),a="group"===s?"homeassistant":s;let n;switch(s){case"lock":n=i?"unlock":"lock";break;case"cover":n=i?"open_cover":"close_cover";break;case"button":case"input_button":n="press";break;case"scene":n="turn_on";break;case"valve":n=i?"open_valve":"close_valve";break;default:n=i?"turn_on":"turn_off"}return t.callService(a,n,{entity_id:e})})(t,e,T.jj.includes(t.states[e].state)),j=async(t,e,i,s)=>{let a;if("double_tap"===s&&i.double_tap_action?a=i.double_tap_action:"hold"===s&&i.hold_action?a=i.hold_action:"tap"===s&&i.tap_action&&(a=i.tap_action),a||(a={action:"more-info"}),a.confirmation&&(!a.confirmation.exemptions||!a.confirmation.exemptions.some((t=>t.user===e.user?.id)))){let i;if((0,S.j)("warning"),"call-service"===a.action||"perform-action"===a.action){const[t,s]=(a.perform_action||a.service).split(".",2),n=e.services;if(t in n&&s in n[t]){await e.loadBackendTranslation("title");const a=await e.loadBackendTranslation("services");i=`${(0,O.p$)(a,t)}: ${a(`component.${t}.services.${i}.name`)||n[t][s].name||s}`}}if(!(await(0,p.dk)(t,{text:a.confirmation.text||e.localize("ui.panel.lovelace.cards.actions.action_confirmation",{action:i||e.localize(`ui.panel.lovelace.editor.action-editor.actions.${a.action}`)||a.action})})))return}switch(a.action){case"more-info":{const s=a.entity||i.entity||i.camera_image||i.image_entity;s?(0,r.r)(t,"hass-more-info",{entityId:s}):((0,N.P)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_entity_more_info")}),(0,S.j)("failure"));break}case"navigate":a.navigation_path?(0,V.o)(a.navigation_path,{replace:a.navigation_replace}):((0,N.P)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_navigation_path")}),(0,S.j)("failure"));break;case"url":a.url_path?window.open(a.url_path):((0,N.P)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_url")}),(0,S.j)("failure"));break;case"toggle":i.entity?(R(e,i.entity),(0,S.j)("light")):((0,N.P)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_entity_toggle")}),(0,S.j)("failure"));break;case"perform-action":case"call-service":{if(!a.perform_action&&!a.service)return(0,N.P)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_action")}),void(0,S.j)("failure");const[i,s]=(a.perform_action||a.service).split(".",2);e.callService(i,s,a.data??a.service_data,a.target),(0,S.j)("light");break}case"assist":((t,e,i)=>{e.auth.external?.config.hasAssist?e.auth.external.fireMessage({type:"assist/show",payload:{pipeline_id:i.pipeline_id,start_listening:i.start_listening??!0}}):(0,r.r)(t,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:U,dialogParams:{pipeline_id:i.pipeline_id,start_listening:i.start_listening??!1}})})(t,e,{start_listening:a.start_listening??!1,pipeline_id:a.pipeline_id??"last_used"});break;case"fire-dom-event":(0,r.r)(t,"ll-custom",a)}};function K(t){return void 0!==t&&"none"!==t.action}var B=i(63873);i(91074);const Y=(t,e)=>t.config.state!==B.m2?t.localize("ui.panel.lovelace.warning.entity_not_found",{entity:e||"[empty]"}):t.localize("ui.panel.lovelace.warning.starting");(0,s.A)([(0,n.EM)("hui-warning")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"method",key:"render",value:function(){return a.qy`<ha-alert alert-type="warning"><slot></slot></ha-alert> `}}]}}),a.WF),(0,s.A)([(0,n.EM)("hui-generic-entity-row")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"config",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"secondaryText",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"hideName",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"catchInteraction",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass||!this.config)return a.s6;const t=this.config.entity?this.hass.states[this.config.entity]:void 0;if(!t)return a.qy`
        <hui-warning>
          ${Y(this.hass,this.config.entity)}
        </hui-warning>
      `;const e=(0,d.m)(this.config.entity),i=function(t){return!t.tap_action||K(t.tap_action)||K(t.hold_action)||K(t.double_tap_action)}(this.config),s=this.secondaryText||this.config.secondary_info,n=this.config.name??(0,E.u)(t);return a.qy`
      <state-badge
        class=${(0,W.H)({pointer:i})}
        .hass=${this.hass}
        .stateObj=${t}
        .overrideIcon=${this.config.icon}
        .overrideImage=${this.config.image}
        .stateColor=${this.config.state_color}
        @action=${this._handleAction}
        .actionHandler=${Z({hasHold:K(this.config.hold_action),hasDoubleClick:K(this.config.double_tap_action)})}
        tabindex=${(0,L.J)(!this.config.tap_action||K(this.config.tap_action)?"0":void 0)}
      ></state-badge>
      ${this.hideName?a.s6:a.qy`<div
            class="info ${(0,W.H)({pointer:i,"text-content":!s})}"
            @action=${this._handleAction}
            .actionHandler=${Z({hasHold:K(this.config.hold_action),hasDoubleClick:K(this.config.double_tap_action)})}
            .title=${n}
          >
            ${this.config.name||(0,E.u)(t)}
            ${s?a.qy`
                  <div class="secondary">
                    ${this.secondaryText||("entity-id"===this.config.secondary_info?t.entity_id:"last-changed"===this.config.secondary_info?a.qy`
                            <ha-relative-time
                              .hass=${this.hass}
                              .datetime=${t.last_changed}
                              capitalize
                            ></ha-relative-time>
                          `:"last-updated"===this.config.secondary_info?a.qy`
                              <ha-relative-time
                                .hass=${this.hass}
                                .datetime=${t.last_updated}
                                capitalize
                              ></ha-relative-time>
                            `:"last-triggered"===this.config.secondary_info?t.attributes.last_triggered?a.qy`
                                  <ha-relative-time
                                    .hass=${this.hass}
                                    .datetime=${t.attributes.last_triggered}
                                    capitalize
                                  ></ha-relative-time>
                                `:this.hass.localize("ui.panel.lovelace.cards.entities.never_triggered"):"position"===this.config.secondary_info&&void 0!==t.attributes.current_position?`${this.hass.localize("ui.card.cover.position")}: ${t.attributes.current_position}`:"tilt-position"===this.config.secondary_info&&void 0!==t.attributes.current_tilt_position?`${this.hass.localize("ui.card.cover.tilt_position")}: ${t.attributes.current_tilt_position}`:"brightness"===this.config.secondary_info&&t.attributes.brightness?a.qy`${Math.round(t.attributes.brightness/255*100)}
                                    %`:"")}
                  </div>
                `:""}
          </div>`}
      ${this.catchInteraction??!T.yd.includes(e)?a.qy`<div
            class="text-content value ${(0,W.H)({pointer:i})}"
            @action=${this._handleAction}
            .actionHandler=${Z({hasHold:K(this.config.hold_action),hasDoubleClick:K(this.config.double_tap_action)})}
          >
            <div class="state"><slot></slot></div>
          </div>`:a.qy`<slot></slot>`}
    `}},{kind:"method",key:"updated",value:function(t){var e,s,a;(0,g.A)(i,"updated",this,3)([t]),e=this,s="no-secondary",void 0!==(a=!this.secondaryText&&!this.config?.secondary_info)&&(a=!!a),e.hasAttribute(s)?a||e.removeAttribute(s):!1!==a&&e.setAttribute(s,"")}},{kind:"method",key:"_handleAction",value:function(t){j(this,this.hass,this.config,t.detail.action)}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host {
        display: flex;
        align-items: center;
        flex-direction: row;
      }
      .info {
        margin-left: 16px;
        margin-right: 8px;
        margin-inline-start: 16px;
        margin-inline-end: 8px;
        flex: 1 1 30%;
      }
      .info,
      .info > * {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .flex ::slotted(*) {
        margin-left: 8px;
        margin-inline-start: 8px;
        margin-inline-end: initial;
        min-width: 0;
      }
      .flex ::slotted([slot="secondary"]) {
        margin-left: 0;
        margin-inline-start: 0;
        margin-inline-end: initial;
      }
      .secondary,
      ha-relative-time {
        color: var(--secondary-text-color);
      }
      state-badge {
        flex: 0 0 40px;
      }
      .pointer {
        cursor: pointer;
      }
      .state {
        text-align: var(--float-end);
      }
      .value {
        direction: ltr;
      }
    `}}]}}),a.WF),(0,s.A)([(0,n.EM)("hui-select-entity-row")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t||!t.entity)throw new Error("Entity must be specified");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return function(t,e){if(I(t,e))return!0;if(!e.has("hass"))return!1;const i=e.get("hass"),s=t.hass;return M(i,s,t._config.entity)||H(i,s,t._config.entity)}(this,t)}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return a.s6;const t=this.hass.states[this._config.entity];return t?a.qy`
      <hui-generic-entity-row
        .hass=${this.hass}
        .config=${this._config}
        hideName
      >
        <ha-select
          .label=${this._config.name||(0,E.u)(t)}
          .value=${t.state}
          .disabled=${t.state===l.Hh}
          naturalMenuWidth
          @selected=${this._selectedChanged}
          @click=${$.d}
          @closed=${$.d}
        >
          ${t.attributes.options?t.attributes.options.map((e=>a.qy`
                  <mwc-list-item .value=${e}>
                    ${this.hass.formatEntityState(t,e)}
                  </mwc-list-item>
                `)):""}
        </ha-select>
      </hui-generic-entity-row>
    `:a.qy`
        <hui-warning>
          ${Y(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      hui-generic-entity-row {
        display: flex;
        align-items: center;
      }
      ha-select {
        width: 100%;
        --ha-select-min-width: 0;
      }
    `}},{kind:"method",key:"_selectedChanged",value:function(t){const e=this.hass.states[this._config.entity],i=t.target.value;i!==e.state&&e.attributes.options.includes(i)&&((0,S.j)("light"),A(this.hass,e.entity_id,i))}}]}}),a.WF);(0,s.A)([(0,n.EM)("ha-voice-assistant-setup-step-success")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"assistConfiguration",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"deviceId",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"assistEntityId",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_ttsSettings",value:void 0},{kind:"method",key:"willUpdate",value:function(t){if((0,g.A)(i,"willUpdate",this,3)([t]),t.has("assistConfiguration"))this._setTtsSettings();else if(t.has("hass")&&this.assistConfiguration){const e=t.get("hass");if(e){const t=e.states[this.assistConfiguration.pipeline_entity_id],i=this.hass.states[this.assistConfiguration.pipeline_entity_id];t.state!==i.state&&this._setTtsSettings()}}}},{kind:"method",key:"render",value:function(){const t=this.assistConfiguration?this.hass.states[this.assistConfiguration.pipeline_entity_id]:void 0;return a.qy`<div class="content">
        <img src="/static/images/voice-assistant/heart.png" />
        <h1>Ready to Assist!</h1>
        <p class="secondary">
          Make any final customizations here. You can always change these in the
          Voice Assistants section of the settings page.
        </p>
        <div class="rows">
          ${this.assistConfiguration&&this.assistConfiguration.available_wake_words.length>1?a.qy` <div class="row">
                <ha-select
                  .label=${"Wake word"}
                  @closed=${$.d}
                  fixedMenuPosition
                  naturalMenuWidth
                  .value=${this.assistConfiguration.active_wake_words[0]}
                  @selected=${this._wakeWordPicked}
                >
                  ${this.assistConfiguration.available_wake_words.map((t=>a.qy`<ha-list-item .value=${t.id}>
                        ${t.wake_word}
                      </ha-list-item>`))}
                </ha-select>
                <ha-button @click=${this._testWakeWord}>
                  <ha-svg-icon slot="icon" .path=${"M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z"}></ha-svg-icon>
                  Test
                </ha-button>
              </div>`:a.s6}
          ${t?a.qy`<div class="row">
                <ha-select
                  .label=${"Assistant"}
                  @closed=${$.d}
                  .value=${t?.state}
                  fixedMenuPosition
                  naturalMenuWidth
                  @selected=${this._pipelinePicked}
                >
                  ${t?.attributes.options.map((e=>a.qy`<ha-list-item .value=${e}>
                        ${this.hass.formatEntityState(t,e)}
                      </ha-list-item>`))}
                </ha-select>
                <ha-button @click=${this._openPipeline}>
                  <ha-svg-icon slot="icon" .path=${"M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"}></ha-svg-icon>
                  Edit
                </ha-button>
              </div>`:a.s6}
          ${this._ttsSettings?a.qy`<div class="row">
                <ha-tts-voice-picker
                  .hass=${this.hass}
                  .engineId=${this._ttsSettings.engine}
                  .language=${this._ttsSettings.language}
                  .value=${this._ttsSettings.voice}
                  @value-changed=${this._voicePicked}
                  @closed=${$.d}
                ></ha-tts-voice-picker>
                <ha-button @click=${this._testTts}>
                  <ha-svg-icon slot="icon" .path=${"M8,5.14V19.14L19,12.14L8,5.14Z"}></ha-svg-icon>
                  Try
                </ha-button>
              </div>`:a.s6}
        </div>
      </div>
      <div class="footer">
        <ha-button @click=${this._close} unelevated>Done</ha-button>
      </div>`}},{kind:"method",key:"_getPipeline",value:async function(){if(!this.assistConfiguration?.pipeline_entity_id)return[void 0,void 0];const t=this.hass.states[this.assistConfiguration?.pipeline_entity_id].state,e=await(0,_.nx)(this.hass);let i;return i="preferred"===t?e.pipelines.find((t=>t.id===e.preferred_pipeline)):e.pipelines.find((e=>e.name===t)),[i,e.preferred_pipeline]}},{kind:"method",key:"_wakeWordPicked",value:async function(t){const e=t.target.value;await(0,c.g5)(this.hass,this.assistEntityId,[e])}},{kind:"method",key:"_pipelinePicked",value:function(t){const e=this.hass.states[this.assistConfiguration.pipeline_entity_id],i=t.target.value;i!==e.state&&e.attributes.options.includes(i)&&A(this.hass,e.entity_id,i)}},{kind:"method",key:"_setTtsSettings",value:async function(){const[t]=await this._getPipeline();this._ttsSettings=t?{engine:t.tts_engine,voice:t.tts_voice,language:t.tts_language}:void 0}},{kind:"method",key:"_voicePicked",value:async function(t){const[e]=await this._getPipeline();e&&await(0,_.zn)(this.hass,e.id,{...e,tts_voice:t.detail.value})}},{kind:"method",key:"_testTts",value:function(){this._announce("Hello, how can I help you?")}},{kind:"method",key:"_announce",value:async function(t){this.assistEntityId&&await(0,c.ew)(this.hass,this.assistEntityId,t)}},{kind:"method",key:"_testWakeWord",value:function(){(0,r.r)(this,"next-step",{step:X.WAKEWORD,nextStep:X.SUCCESS,updateConfig:!0})}},{kind:"method",key:"_openPipeline",value:async function(){const[t]=await this._getPipeline();if(!t)return;const e=await(0,w.eN)(this.hass);var i,s;i=this,s={cloudActiveSubscription:e.logged_in&&e.active_subscription,pipeline:t,updatePipeline:async e=>{await(0,_.zn)(this.hass,t.id,e)},hideWakeWord:!0},(0,r.r)(i,"show-dialog",{dialogTag:"dialog-voice-assistant-pipeline-detail",dialogImport:C,dialogParams:s})}},{kind:"method",key:"_close",value:function(){(0,r.r)(this,"closed")}},{kind:"field",static:!0,key:"styles",value(){return[v,a.AH`
      ha-md-list-item {
        text-align: initial;
      }
      ha-tts-voice-picker {
        display: block;
      }
      .footer {
        margin-top: 24px;
      }
      .rows {
        gap: 16px;
        display: flex;
        flex-direction: column;
      }
      .row {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .row > *:first-child {
        flex: 1;
        margin-right: 4px;
      }
      .row ha-button {
        width: 82px;
      }
    `]}}]}}),a.WF);var G=i(2503);(0,s.A)([(0,n.EM)("ha-voice-assistant-setup-step-update")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"updateEntityId",value:void 0},{kind:"field",key:"_updated",value(){return!1}},{kind:"field",key:"_refreshTimeout",value:void 0},{kind:"method",key:"willUpdate",value:function(t){if((0,g.A)(i,"willUpdate",this,3)([t]),this.updateEntityId){if(t.has("hass")&&this.updateEntityId){const e=t.get("hass");if(e){const t=e.states[this.updateEntityId],i=this.hass.states[this.updateEntityId];if(t?.state===l.Hh&&i?.state!==l.Hh||t?.state!==l.ON&&i?.state===l.ON)return void this._tryUpdate(!1)}}t.has("updateEntityId")&&this._tryUpdate(!0)}else this._nextStep()}},{kind:"method",key:"render",value:function(){if(!this.updateEntityId||!(this.updateEntityId in this.hass.states))return a.s6;const t=this.hass.states[this.updateEntityId],e=t&&(0,G.RJ)(t);return a.qy`<div class="content">
      <img src="/static/images/voice-assistant/update.png" />
      <h1>
        ${t&&("unavailable"===t.state||(0,G.Jy)(t))?"Updating your voice assistant":"Checking for updates"}
      </h1>
      <p class="secondary">
        We are making sure you have the latest and greatest version of your
        voice assistant. This may take a few minutes.
      </p>
      <ha-circular-progress
        .value=${e?t.attributes.update_percentage/100:void 0}
        .indeterminate=${!e}
      ></ha-circular-progress>
      <p>
        ${t?.state===l.Hh?"Restarting voice assistant":e?`Installing ${t.attributes.update_percentage}%`:""}
      </p>
    </div>`}},{kind:"method",key:"_tryUpdate",value:async function(t){if(clearTimeout(this._refreshTimeout),!this.updateEntityId)return;const e=this.hass.states[this.updateEntityId];e&&this.hass.states[e.entity_id].state===l.ON&&(0,G.VK)(e)?(this._updated=!0,await this.hass.callService("update","install",{},{entity_id:e.entity_id})):t?(await this.hass.callService("homeassistant","update_entity",{},{entity_id:this.updateEntityId}),this._refreshTimeout=window.setTimeout((()=>{this._nextStep()}),5e3)):this._nextStep()}},{kind:"method",key:"_nextStep",value:function(){(0,r.r)(this,"next-step",{noPrevious:!0,updateConfig:this._updated})}},{kind:"field",static:!0,key:"styles",value(){return[v,a.AH`
      ha-circular-progress {
        margin-top: 24px;
        margin-bottom: 24px;
      }
    `]}}]}}),a.WF);i(32714);(0,s.A)([(0,n.EM)("ha-voice-assistant-setup-step-wake-word")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"assistConfiguration",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"assistEntityId",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_detected",value(){return!1}},{kind:"field",key:"_sub",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,g.A)(i,"disconnectedCallback",this,3)([]),this._stopListeningWakeWord()}},{kind:"method",key:"willUpdate",value:function(t){(0,g.A)(i,"willUpdate",this,3)([t]),t.has("assistEntityId")&&(this._detected=!1,this._listenWakeWord())}},{kind:"field",key:"_activeWakeWord",value(){return(0,o.A)((t=>{if(!t)return"";const e=t.active_wake_words[0];return t.available_wake_words.find((t=>t.id===e))?.wake_word}))}},{kind:"method",key:"render",value:function(){if(!this.assistEntityId)return a.s6;return"idle"!==this.hass.states[this.assistEntityId].state?a.qy`<ha-circular-progress indeterminate></ha-circular-progress>`:a.qy`<div class="content">
        ${this._detected?a.qy`<img src="/static/images/voice-assistant/ok-nabu.png" />
              <h1>
                Say “${this._activeWakeWord(this.assistConfiguration)}” again
              </h1>
              <p class="secondary">
                To make sure the wake word works for you.
              </p>`:a.qy`
          <img src="/static/images/voice-assistant/sleep.png" />
          <h1>
            Say “${this._activeWakeWord(this.assistConfiguration)}” to wake the
            device up
          </h1>
          <p class="secondary">Setup will continue once the device is awake.</p>
        </div>`}
      </div>
      <div class="footer centered">
        <ha-button @click=${this._changeWakeWord}>Change wake word</ha-button>
      </div>`}},{kind:"method",key:"_listenWakeWord",value:async function(){const t=this.assistEntityId;t&&(await this._stopListeningWakeWord(),this._sub=(0,c.ds)(this.hass,t,(()=>{this._stopListeningWakeWord(),this._detected?this._nextStep():(this._detected=!0,this._listenWakeWord())})))}},{kind:"method",key:"_stopListeningWakeWord",value:async function(){try{(await this._sub)?.()}catch(t){}this._sub=void 0}},{kind:"method",key:"_nextStep",value:function(){(0,r.r)(this,"next-step")}},{kind:"method",key:"_changeWakeWord",value:function(){(0,r.r)(this,"next-step",{step:X.CHANGE_WAKEWORD})}},{kind:"field",static:!0,key:"styles",value(){return v}}]}}),a.WF);let X=function(t){return t[t.INIT=0]="INIT",t[t.UPDATE=1]="UPDATE",t[t.CHECK=2]="CHECK",t[t.WAKEWORD=3]="WAKEWORD",t[t.AREA=4]="AREA",t[t.PIPELINE=5]="PIPELINE",t[t.SUCCESS=6]="SUCCESS",t[t.CLOUD=7]="CLOUD",t[t.CHANGE_WAKEWORD=8]="CHANGE_WAKEWORD",t}({}),J=(0,s.A)([(0,n.EM)("ha-voice-assistant-setup-dialog")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_step",value(){return X.INIT}},{kind:"field",decorators:[(0,n.wk)()],key:"_assistConfiguration",value:void 0},{kind:"field",key:"_previousSteps",value(){return[]}},{kind:"field",key:"_nextStep",value:void 0},{kind:"method",key:"showDialog",value:async function(t){this._params=t,await this._fetchAssistConfiguration(),this._step=X.UPDATE}},{kind:"method",key:"closeDialog",value:async function(){this.renderRoot.querySelector("ha-dialog")?.close()}},{kind:"method",key:"_dialogClosed",value:function(){this._params=void 0,this._assistConfiguration=void 0,this._previousSteps=[],this._nextStep=void 0,this._step=X.INIT,(0,r.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"field",key:"_deviceEntities",value(){return(0,o.A)(((t,e)=>Object.values(e).filter((e=>e.device_id===t))))}},{kind:"field",key:"_findDomainEntityId",value(){return(0,o.A)(((t,e,i)=>{const s=this._deviceEntities(t,e);return s.find((t=>(0,d.m)(t.entity_id)===i))?.entity_id}))}},{kind:"method",key:"render",value:function(){if(!this._params)return a.s6;const t=this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite"),e=t?this.hass.states[t]:void 0;return a.qy`
      <ha-dialog
        open
        @closed=${this._dialogClosed}
        .heading=${"Voice Satellite setup"}
        hideActions
        escapeKeyAction
        scrimClickAction
      >
        <ha-dialog-header slot="heading">
          ${this._previousSteps.length?a.qy`<ha-icon-button
                slot="navigationIcon"
                .label=${this.hass.localize("ui.common.back")??"Back"}
                .path=${"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"}
                @click=${this._goToPreviousStep}
              ></ha-icon-button>`:this._step!==X.UPDATE?a.qy`<ha-icon-button
                  slot="navigationIcon"
                  .label=${this.hass.localize("ui.dialogs.generic.close")??"Close"}
                  .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
                  @click=${this.closeDialog}
                ></ha-icon-button>`:a.s6}
          ${this._step===X.WAKEWORD||this._step===X.AREA||this._step===X.PIPELINE?a.qy`<ha-button
                @click=${this._goToNextStep}
                class="skip-btn"
                slot="actionItems"
                >Skip</ha-button
              >`:a.s6}
        </ha-dialog-header>
        <div class="content" @next-step=${this._goToNextStep}>
          ${this._step===X.UPDATE?a.qy`<ha-voice-assistant-setup-step-update
                .hass=${this.hass}
                .updateEntityId=${this._findDomainEntityId(this._params.deviceId,this.hass.entities,"update")}
              ></ha-voice-assistant-setup-step-update>`:e?.state===l.Hh?a.qy`Your voice assistant is not available.`:this._step===X.CHECK?a.qy`<ha-voice-assistant-setup-step-check
                    .hass=${this.hass}
                    .assistEntityId=${this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite")}
                  ></ha-voice-assistant-setup-step-check>`:this._step===X.WAKEWORD?a.qy`<ha-voice-assistant-setup-step-wake-word
                      .hass=${this.hass}
                      .assistConfiguration=${this._assistConfiguration}
                      .assistEntityId=${this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite")}
                    ></ha-voice-assistant-setup-step-wake-word>`:this._step===X.CHANGE_WAKEWORD?a.qy`
                        <ha-voice-assistant-setup-step-change-wake-word
                          .hass=${this.hass}
                          .assistConfiguration=${this._assistConfiguration}
                          .assistEntityId=${this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite")}
                        ></ha-voice-assistant-setup-step-change-wake-word>
                      `:this._step===X.AREA?a.qy`
                          <ha-voice-assistant-setup-step-area
                            .hass=${this.hass}
                            .deviceId=${this._params.deviceId}
                          ></ha-voice-assistant-setup-step-area>
                        `:this._step===X.PIPELINE?a.qy`<ha-voice-assistant-setup-step-pipeline
                            .hass=${this.hass}
                            .assistConfiguration=${this._assistConfiguration}
                            .assistEntityId=${this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite")}
                          ></ha-voice-assistant-setup-step-pipeline>`:this._step===X.CLOUD?a.qy`<ha-voice-assistant-setup-step-cloud
                              .hass=${this.hass}
                            ></ha-voice-assistant-setup-step-cloud>`:this._step===X.SUCCESS?a.qy`<ha-voice-assistant-setup-step-success
                                .hass=${this.hass}
                                .assistConfiguration=${this._assistConfiguration}
                                .assistEntityId=${this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite")}
                              ></ha-voice-assistant-setup-step-success>`:a.s6}
        </div>
      </ha-dialog>
    `}},{kind:"method",key:"_fetchAssistConfiguration",value:async function(){return this._assistConfiguration=await(0,c.Vy)(this.hass,this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite")),this._assistConfiguration}},{kind:"method",key:"_goToPreviousStep",value:function(){this._previousSteps.length&&(this._step=this._previousSteps.pop())}},{kind:"method",key:"_goToNextStep",value:function(t){t.detail?.updateConfig&&this._fetchAssistConfiguration(),t.detail?.nextStep&&(this._nextStep=t.detail.nextStep),t.detail?.noPrevious||this._previousSteps.push(this._step),t.detail?.step?this._step=t.detail.step:this._nextStep?(this._step=this._nextStep,this._nextStep=void 0):this._step+=1}},{kind:"get",static:!0,key:"styles",value:function(){return[h.nA,a.AH`
        ha-dialog {
          --dialog-content-padding: 0;
        }
        @media all and (min-width: 450px) and (min-height: 500px) {
          ha-dialog {
            --mdc-dialog-min-width: 560px;
            --mdc-dialog-max-width: 560px;
            --mdc-dialog-min-width: min(560px, 95vw);
            --mdc-dialog-max-width: min(560px, 95vw);
          }
        }
        ha-dialog-header {
          height: 56px;
        }
        @media all and (max-width: 450px), all and (max-height: 500px) {
          .content {
            height: calc(100vh - 56px);
          }
        }
        .skip-btn {
          margin-top: 6px;
        }
      `]}}]}}),a.WF)},47424:(t,e,i)=>{i.d(e,{MR:()=>s,a_:()=>a,bg:()=>n});const s=t=>`https://brands.home-assistant.io/${t.brand?"brands/":""}${t.useFallback?"_/":""}${t.domain}/${t.darkOptimized?"dark_":""}${t.type}.png`,a=t=>t.split("/")[4],n=t=>t.startsWith("https://brands.home-assistant.io/")},14630:(t,e,i)=>{i.d(e,{C:()=>s});const s="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0},34947:(t,e,i)=>{i.d(e,{P:()=>a});var s=i(33167);const a=(t,e)=>(0,s.r)(t,"hass-notification",e)}};
//# sourceMappingURL=jFz4LWDh.js.map