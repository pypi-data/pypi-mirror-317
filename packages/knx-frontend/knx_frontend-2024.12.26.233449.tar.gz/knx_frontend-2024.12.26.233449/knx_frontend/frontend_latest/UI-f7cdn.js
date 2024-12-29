/*! For license information please see UI-f7cdn.js.LICENSE.txt */
export const id=1424;export const ids=[1424,4649];export const modules={73279:(e,t,r)=>{var o=r(85461),a=r(69534),i=r(57305),n=r(98597),s=r(196);(0,o.A)([(0,s.EM)("ha-circular-progress")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,s.MZ)({attribute:"aria-label",type:String})],key:"ariaLabel",value(){return"Loading"}},{kind:"field",decorators:[(0,s.MZ)()],key:"size",value(){return"medium"}},{kind:"method",key:"updated",value:function(e){if((0,a.A)(r,"updated",this,3)([e]),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"field",static:!0,key:"styles",value(){return[...(0,a.A)(r,"styles",this),n.AH`
      :host {
        --md-sys-color-primary: var(--primary-color);
        --md-circular-progress-size: 48px;
      }
    `]}}]}}),i.U)},92312:(e,t,r)=>{r.r(t),r.d(t,{HaIconButtonArrowPrev:()=>s});var o=r(85461),a=r(98597),i=r(196),n=r(10);r(96396);let s=(0,o.A)([(0,i.EM)("ha-icon-button-arrow-prev")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,i.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,i.wk)()],key:"_icon",value(){return"rtl"===n.G.document.dir?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}},{kind:"method",key:"render",value:function(){return a.qy`
      <ha-icon-button
        .disabled=${this.disabled}
        .label=${this.label||this.hass?.localize("ui.common.back")||"Back"}
        .path=${this._icon}
      ></ha-icon-button>
    `}}]}}),a.WF)},96396:(e,t,r)=>{r.r(t),r.d(t,{HaIconButton:()=>s});var o=r(85461),a=(r(25413),r(98597)),i=r(196),n=r(79278);r(29222);let s=(0,o.A)([(0,i.EM)("ha-icon-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,i.MZ)({type:String})],key:"path",value:void 0},{kind:"field",decorators:[(0,i.MZ)({type:String})],key:"label",value:void 0},{kind:"field",decorators:[(0,i.MZ)({type:String,attribute:"aria-haspopup"})],key:"ariaHasPopup",value:void 0},{kind:"field",decorators:[(0,i.MZ)({type:Boolean})],key:"hideTitle",value(){return!1}},{kind:"field",decorators:[(0,i.P)("mwc-icon-button",!0)],key:"_button",value:void 0},{kind:"method",key:"focus",value:function(){this._button?.focus()}},{kind:"field",static:!0,key:"shadowRootOptions",value(){return{mode:"open",delegatesFocus:!0}}},{kind:"method",key:"render",value:function(){return a.qy`
      <mwc-icon-button
        aria-label=${(0,n.J)(this.label)}
        title=${(0,n.J)(this.hideTitle?void 0:this.label)}
        aria-haspopup=${(0,n.J)(this.ariaHasPopup)}
        .disabled=${this.disabled}
      >
        ${this.path?a.qy`<ha-svg-icon .path=${this.path}></ha-svg-icon>`:a.qy`<slot></slot>`}
      </mwc-icon-button>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host {
        display: inline-block;
        outline: none;
      }
      :host([disabled]) {
        pointer-events: none;
      }
      mwc-icon-button {
        --mdc-theme-on-primary: currentColor;
        --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
      }
    `}}]}}),a.WF)},32010:(e,t,r)=>{var o=r(85461),a=r(69534),i=r(98597),n=r(196),s=r(33167);class c{constructor(){this.notifications=void 0,this.notifications={}}processMessage(e){if("removed"===e.type)for(const t of Object.keys(e.notifications))delete this.notifications[t];else this.notifications={...this.notifications,...e.notifications};return Object.values(this.notifications)}}r(96396);(0,o.A)([(0,n.EM)("ha-menu-button")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"hassio",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_hasNotifications",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_show",value(){return!1}},{kind:"field",key:"_alwaysVisible",value(){return!1}},{kind:"field",key:"_attachNotifOnConnect",value(){return!1}},{kind:"field",key:"_unsubNotifications",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.A)(r,"connectedCallback",this,3)([]),this._attachNotifOnConnect&&(this._attachNotifOnConnect=!1,this._subscribeNotifications())}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.A)(r,"disconnectedCallback",this,3)([]),this._unsubNotifications&&(this._attachNotifOnConnect=!0,this._unsubNotifications(),this._unsubNotifications=void 0)}},{kind:"method",key:"render",value:function(){if(!this._show)return i.s6;const e=this._hasNotifications&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);return i.qy`
      <ha-icon-button
        .label=${this.hass.localize("ui.sidebar.sidebar_toggle")}
        .path=${"M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"}
        @click=${this._toggleMenu}
      ></ha-icon-button>
      ${e?i.qy`<div class="dot"></div>`:""}
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,a.A)(r,"firstUpdated",this,3)([e]),this.hassio&&(this._alwaysVisible=(Number(window.parent.frontendVersion)||0)<20190710)}},{kind:"method",key:"willUpdate",value:function(e){if((0,a.A)(r,"willUpdate",this,3)([e]),!e.has("narrow")&&!e.has("hass"))return;const t=e.has("hass")?e.get("hass"):this.hass,o=(e.has("narrow")?e.get("narrow"):this.narrow)||"always_hidden"===t?.dockedSidebar,i=this.narrow||"always_hidden"===this.hass.dockedSidebar;this.hasUpdated&&o===i||(this._show=i||this._alwaysVisible,i?this._subscribeNotifications():this._unsubNotifications&&(this._unsubNotifications(),this._unsubNotifications=void 0))}},{kind:"method",key:"_subscribeNotifications",value:function(){if(this._unsubNotifications)throw new Error("Already subscribed");this._unsubNotifications=((e,t)=>{const r=new c,o=e.subscribeMessage((e=>t(r.processMessage(e))),{type:"persistent_notification/subscribe"});return()=>{o.then((e=>e?.()))}})(this.hass.connection,(e=>{this._hasNotifications=e.length>0}))}},{kind:"method",key:"_toggleMenu",value:function(){(0,s.r)(this,"hass-toggle-menu")}},{kind:"get",static:!0,key:"styles",value:function(){return i.AH`
      :host {
        position: relative;
      }
      .dot {
        pointer-events: none;
        position: absolute;
        background-color: var(--accent-color);
        width: 12px;
        height: 12px;
        top: 9px;
        right: 7px;
        inset-inline-end: 7px;
        inset-inline-start: initial;
        border-radius: 50%;
        border: 2px solid var(--app-header-background-color);
      }
    `}}]}}),i.WF)},29222:(e,t,r)=>{r.r(t),r.d(t,{HaSvgIcon:()=>n});var o=r(85461),a=r(98597),i=r(196);let n=(0,o.A)([(0,i.EM)("ha-svg-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.MZ)()],key:"path",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"secondaryPath",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"viewBox",value:void 0},{kind:"method",key:"render",value:function(){return a.JW`
    <svg
      viewBox=${this.viewBox||"0 0 24 24"}
      preserveAspectRatio="xMidYMid meet"
      focusable="false"
      role="img"
      aria-hidden="true"
    >
      <g>
        ${this.path?a.JW`<path class="primary-path" d=${this.path}></path>`:a.s6}
        ${this.secondaryPath?a.JW`<path class="secondary-path" d=${this.secondaryPath}></path>`:a.s6}
      </g>
    </svg>`}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host {
        display: var(--ha-icon-display, inline-flex);
        align-items: center;
        justify-content: center;
        position: relative;
        vertical-align: middle;
        fill: var(--icon-primary-color, currentcolor);
        width: var(--mdc-icon-size, 24px);
        height: var(--mdc-icon-size, 24px);
      }
      svg {
        width: 100%;
        height: 100%;
        pointer-events: none;
        display: block;
      }
      path.primary-path {
        opacity: var(--icon-primary-opactity, 1);
      }
      path.secondary-path {
        fill: var(--icon-secondary-color, currentcolor);
        opacity: var(--icon-secondary-opactity, 0.5);
      }
    `}}]}}),a.WF)},61424:(e,t,r)=>{r.r(t);var o=r(85461),a=r(98597),i=r(196),n=(r(73279),r(92312),r(32010),r(43799));(0,o.A)([(0,i.EM)("hass-loading-screen")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.MZ)({type:Boolean,attribute:"no-toolbar"})],key:"noToolbar",value(){return!1}},{kind:"field",decorators:[(0,i.MZ)({type:Boolean})],key:"rootnav",value(){return!1}},{kind:"field",decorators:[(0,i.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,i.MZ)()],key:"message",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`
      ${this.noToolbar?"":a.qy`<div class="toolbar">
            ${this.rootnav||history.state?.root?a.qy`
                  <ha-menu-button
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                `:a.qy`
                  <ha-icon-button-arrow-prev
                    .hass=${this.hass}
                    @click=${this._handleBack}
                  ></ha-icon-button-arrow-prev>
                `}
          </div>`}
      <div class="content">
        <ha-circular-progress indeterminate></ha-circular-progress>
        ${this.message?a.qy`<div id="loading-text">${this.message}</div>`:a.s6}
      </div>
    `}},{kind:"method",key:"_handleBack",value:function(){history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[n.RF,a.AH`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }
        .toolbar {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: var(--header-height);
          padding: 8px 12px;
          pointer-events: none;
          background-color: var(--app-header-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar {
            padding: 4px;
          }
        }
        ha-menu-button,
        ha-icon-button-arrow-prev {
          pointer-events: auto;
        }
        .content {
          height: calc(100% - var(--header-height));
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        #loading-text {
          max-width: 350px;
          margin-top: 16px;
        }
      `]}}]}}),a.WF)},43799:(e,t,r)=>{r.d(t,{RF:()=>i,dp:()=>s,nA:()=>n,og:()=>a});var o=r(98597);const a=o.AH`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
    outline: none;
  }
`,i=o.AH`
  :host {
    font-family: var(--paper-font-body1_-_font-family);
    -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
    font-size: var(--paper-font-body1_-_font-size);
    font-weight: var(--paper-font-body1_-_font-weight);
    line-height: var(--paper-font-body1_-_line-height);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
    margin-inline-start: 20px;
    margin-inline-end: initial;
  }

  h1 {
    font-family: var(--paper-font-headline_-_font-family);
    -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
    white-space: var(--paper-font-headline_-_white-space);
    overflow: var(--paper-font-headline_-_overflow);
    text-overflow: var(--paper-font-headline_-_text-overflow);
    font-size: var(--paper-font-headline_-_font-size);
    font-weight: var(--paper-font-headline_-_font-weight);
    line-height: var(--paper-font-headline_-_line-height);
  }

  h2 {
    font-family: var(--paper-font-title_-_font-family);
    -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
    white-space: var(--paper-font-title_-_white-space);
    overflow: var(--paper-font-title_-_overflow);
    text-overflow: var(--paper-font-title_-_text-overflow);
    font-size: var(--paper-font-title_-_font-size);
    font-weight: var(--paper-font-title_-_font-weight);
    line-height: var(--paper-font-title_-_line-height);
  }

  h3 {
    font-family: var(--paper-font-subhead_-_font-family);
    -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
    white-space: var(--paper-font-subhead_-_white-space);
    overflow: var(--paper-font-subhead_-_overflow);
    text-overflow: var(--paper-font-subhead_-_text-overflow);
    font-size: var(--paper-font-subhead_-_font-size);
    font-weight: var(--paper-font-subhead_-_font-weight);
    line-height: var(--paper-font-subhead_-_line-height);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  ha-button.warning,
  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }

  ${a}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`,n=o.AH`
  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-max-width: min(600px, 95vw);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --vertical-align-dialog: flex-end;
      --ha-dialog-border-radius: 0;
    }
  }
  mwc-button.warning,
  ha-button.warning {
    --mdc-theme-primary: var(--error-color);
  }
  .error {
    color: var(--error-color);
  }
`,s=o.AH`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`;o.AH`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`},67371:(e,t,r)=>{r.d(t,{n:()=>l});var o=r(98597);const a=["role","ariaAtomic","ariaAutoComplete","ariaBusy","ariaChecked","ariaColCount","ariaColIndex","ariaColSpan","ariaCurrent","ariaDisabled","ariaExpanded","ariaHasPopup","ariaHidden","ariaInvalid","ariaKeyShortcuts","ariaLabel","ariaLevel","ariaLive","ariaModal","ariaMultiLine","ariaMultiSelectable","ariaOrientation","ariaPlaceholder","ariaPosInSet","ariaPressed","ariaReadOnly","ariaRequired","ariaRoleDescription","ariaRowCount","ariaRowIndex","ariaRowSpan","ariaSelected","ariaSetSize","ariaSort","ariaValueMax","ariaValueMin","ariaValueNow","ariaValueText"],i=a.map(s);function n(e){return i.includes(e)}function s(e){return e.replace("aria","aria-").replace(/Elements?/g,"").toLowerCase()}const c=Symbol("privateIgnoreAttributeChangesFor");function l(e){var t;if(o.S$)return e;class r extends e{constructor(){super(...arguments),this[t]=new Set}attributeChangedCallback(e,t,r){if(!n(e))return void super.attributeChangedCallback(e,t,r);if(this[c].has(e))return;this[c].add(e),this.removeAttribute(e),this[c].delete(e);const o=h(e);null===r?delete this.dataset[o]:this.dataset[o]=r,this.requestUpdate(h(e),t)}getAttribute(e){return n(e)?super.getAttribute(d(e)):super.getAttribute(e)}removeAttribute(e){super.removeAttribute(e),n(e)&&(super.removeAttribute(d(e)),this.requestUpdate())}}return t=c,function(e){for(const t of a){const r=s(t),o=d(r),a=h(r);e.createProperty(t,{attribute:r,noAccessor:!0}),e.createProperty(Symbol(o),{attribute:o,noAccessor:!0}),Object.defineProperty(e.prototype,t,{configurable:!0,enumerable:!0,get(){return this.dataset[a]??null},set(e){const r=this.dataset[a]??null;e!==r&&(null===e?delete this.dataset[a]:this.dataset[a]=e,this.requestUpdate(t,r))}})}}(r),r}function d(e){return`data-${e}`}function h(e){return e.replace(/-\w/,(e=>e[1].toUpperCase()))}},57305:(e,t,r)=>{r.d(t,{U:()=>h});var o=r(76513),a=r(196),i=r(98597),n=r(69760);const s=(0,r(67371).n)(i.WF);class c extends s{constructor(){super(...arguments),this.value=0,this.max=1,this.indeterminate=!1,this.fourColor=!1}render(){const{ariaLabel:e}=this;return i.qy`
      <div
        class="progress ${(0,n.H)(this.getRenderClasses())}"
        role="progressbar"
        aria-label="${e||i.s6}"
        aria-valuemin="0"
        aria-valuemax=${this.max}
        aria-valuenow=${this.indeterminate?i.s6:this.value}
        >${this.renderIndicator()}</div
      >
    `}getRenderClasses(){return{indeterminate:this.indeterminate,"four-color":this.fourColor}}}(0,o.Cg)([(0,a.MZ)({type:Number})],c.prototype,"value",void 0),(0,o.Cg)([(0,a.MZ)({type:Number})],c.prototype,"max",void 0),(0,o.Cg)([(0,a.MZ)({type:Boolean})],c.prototype,"indeterminate",void 0),(0,o.Cg)([(0,a.MZ)({type:Boolean,attribute:"four-color"})],c.prototype,"fourColor",void 0);class l extends c{renderIndicator(){return this.indeterminate?this.renderIndeterminateContainer():this.renderDeterminateContainer()}renderDeterminateContainer(){const e=100*(1-this.value/this.max);return i.qy`
      <svg viewBox="0 0 4800 4800">
        <circle class="track" pathLength="100"></circle>
        <circle
          class="active-track"
          pathLength="100"
          stroke-dashoffset=${e}></circle>
      </svg>
    `}renderIndeterminateContainer(){return i.qy` <div class="spinner">
      <div class="left">
        <div class="circle"></div>
      </div>
      <div class="right">
        <div class="circle"></div>
      </div>
    </div>`}}const d=i.AH`:host{--_active-indicator-color: var(--md-circular-progress-active-indicator-color, var(--md-sys-color-primary, #6750a4));--_active-indicator-width: var(--md-circular-progress-active-indicator-width, 10);--_four-color-active-indicator-four-color: var(--md-circular-progress-four-color-active-indicator-four-color, var(--md-sys-color-tertiary-container, #ffd8e4));--_four-color-active-indicator-one-color: var(--md-circular-progress-four-color-active-indicator-one-color, var(--md-sys-color-primary, #6750a4));--_four-color-active-indicator-three-color: var(--md-circular-progress-four-color-active-indicator-three-color, var(--md-sys-color-tertiary, #7d5260));--_four-color-active-indicator-two-color: var(--md-circular-progress-four-color-active-indicator-two-color, var(--md-sys-color-primary-container, #eaddff));--_size: var(--md-circular-progress-size, 48px);display:inline-flex;vertical-align:middle;width:var(--_size);height:var(--_size);position:relative;align-items:center;justify-content:center;contain:strict;content-visibility:auto}.progress{flex:1;align-self:stretch;margin:4px}.progress,.spinner,.left,.right,.circle,svg,.track,.active-track{position:absolute;inset:0}svg{transform:rotate(-90deg)}circle{cx:50%;cy:50%;r:calc(50%*(1 - var(--_active-indicator-width)/100));stroke-width:calc(var(--_active-indicator-width)*1%);stroke-dasharray:100;fill:rgba(0,0,0,0)}.active-track{transition:stroke-dashoffset 500ms cubic-bezier(0, 0, 0.2, 1);stroke:var(--_active-indicator-color)}.track{stroke:rgba(0,0,0,0)}.progress.indeterminate{animation:linear infinite linear-rotate;animation-duration:1568.2352941176ms}.spinner{animation:infinite both rotate-arc;animation-duration:5332ms;animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1)}.left{overflow:hidden;inset:0 50% 0 0}.right{overflow:hidden;inset:0 0 0 50%}.circle{box-sizing:border-box;border-radius:50%;border:solid calc(var(--_active-indicator-width)/100*(var(--_size) - 8px));border-color:var(--_active-indicator-color) var(--_active-indicator-color) rgba(0,0,0,0) rgba(0,0,0,0);animation:expand-arc;animation-iteration-count:infinite;animation-fill-mode:both;animation-duration:1333ms,5332ms;animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1)}.four-color .circle{animation-name:expand-arc,four-color}.left .circle{rotate:135deg;inset:0 -100% 0 0}.right .circle{rotate:100deg;inset:0 0 0 -100%;animation-delay:-666.5ms,0ms}@media(forced-colors: active){.active-track{stroke:CanvasText}.circle{border-color:CanvasText CanvasText Canvas Canvas}}@keyframes expand-arc{0%{transform:rotate(265deg)}50%{transform:rotate(130deg)}100%{transform:rotate(265deg)}}@keyframes rotate-arc{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes linear-rotate{to{transform:rotate(360deg)}}@keyframes four-color{0%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}15%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}25%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}40%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}50%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}65%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}75%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}90%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}100%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}}
`;let h=class extends l{};h.styles=[d],h=(0,o.Cg)([(0,a.EM)("md-circular-progress")],h)}};
//# sourceMappingURL=UI-f7cdn.js.map