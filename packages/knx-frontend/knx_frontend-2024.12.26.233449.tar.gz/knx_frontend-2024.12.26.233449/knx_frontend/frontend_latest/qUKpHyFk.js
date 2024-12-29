/*! For license information please see qUKpHyFk.js.LICENSE.txt */
export const id=4987;export const ids=[4987];export const modules={94090:(e,t,i)=>{var o=i(85461),s=i(69534),a=i(98597),r=i(196),c=i(12506),n=i(66534),l=i(33167),d=i(24517);i(9484),i(81643),i(96334);const h="M20.65,20.87L18.3,18.5L12,12.23L8.44,8.66L7,7.25L4.27,4.5L3,5.77L5.78,8.55C3.23,11.69 3.42,16.31 6.34,19.24C7.9,20.8 9.95,21.58 12,21.58C13.79,21.58 15.57,21 17.03,19.8L19.73,22.5L21,21.23L20.65,20.87M12,19.59C10.4,19.59 8.89,18.97 7.76,17.83C6.62,16.69 6,15.19 6,13.59C6,12.27 6.43,11 7.21,10L12,14.77V19.59M12,5.1V9.68L19.25,16.94C20.62,14 20.09,10.37 17.65,7.93L12,2.27L8.3,5.97L9.71,7.38L12,5.1Z",u="M17.5,12A1.5,1.5 0 0,1 16,10.5A1.5,1.5 0 0,1 17.5,9A1.5,1.5 0 0,1 19,10.5A1.5,1.5 0 0,1 17.5,12M14.5,8A1.5,1.5 0 0,1 13,6.5A1.5,1.5 0 0,1 14.5,5A1.5,1.5 0 0,1 16,6.5A1.5,1.5 0 0,1 14.5,8M9.5,8A1.5,1.5 0 0,1 8,6.5A1.5,1.5 0 0,1 9.5,5A1.5,1.5 0 0,1 11,6.5A1.5,1.5 0 0,1 9.5,8M6.5,12A1.5,1.5 0 0,1 5,10.5A1.5,1.5 0 0,1 6.5,9A1.5,1.5 0 0,1 8,10.5A1.5,1.5 0 0,1 6.5,12M12,3A9,9 0 0,0 3,12A9,9 0 0,0 12,21A1.5,1.5 0 0,0 13.5,19.5C13.5,19.11 13.35,18.76 13.11,18.5C12.88,18.23 12.73,17.88 12.73,17.5A1.5,1.5 0 0,1 14.23,16H16A5,5 0 0,0 21,11C21,6.58 16.97,3 12,3Z";(0,o.A)([(0,r.EM)("ha-color-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:String,attribute:"default_color"})],key:"defaultColor",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"include_state"})],key:"includeState",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"include_none"})],key:"includeNone",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.P)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,s.A)(i,"connectedCallback",this,3)([]),this._select?.layoutOptions()}},{kind:"method",key:"_valueSelected",value:function(e){if(e.stopPropagation(),!this.isConnected)return;const t=e.target.value;this.value=t===this.defaultColor?void 0:t,(0,l.r)(this,"value-changed",{value:this.value})}},{kind:"method",key:"render",value:function(){const e=this.value||this.defaultColor||"",t=!(n.l.has(e)||"none"===e||"state"===e);return a.qy`
      <ha-select
        .icon=${Boolean(e)}
        .label=${this.label}
        .value=${e}
        .helper=${this.helper}
        .disabled=${this.disabled}
        @closed=${d.d}
        @selected=${this._valueSelected}
        fixedMenuPosition
        naturalMenuWidth
        .clearable=${!this.defaultColor}
      >
        ${e?a.qy`
              <span slot="icon">
                ${"none"===e?a.qy`
                      <ha-svg-icon path=${h}></ha-svg-icon>
                    `:"state"===e?a.qy`<ha-svg-icon path=${u}></ha-svg-icon>`:this.renderColorCircle(e||"grey")}
              </span>
            `:a.s6}
        ${this.includeNone?a.qy`
              <ha-list-item value="none" graphic="icon">
                ${this.hass.localize("ui.components.color-picker.none")}
                ${"none"===this.defaultColor?` (${this.hass.localize("ui.components.color-picker.default")})`:a.s6}
                <ha-svg-icon
                  slot="graphic"
                  path=${h}
                ></ha-svg-icon>
              </ha-list-item>
            `:a.s6}
        ${this.includeState?a.qy`
              <ha-list-item value="state" graphic="icon">
                ${this.hass.localize("ui.components.color-picker.state")}
                ${"state"===this.defaultColor?` (${this.hass.localize("ui.components.color-picker.default")})`:a.s6}
                <ha-svg-icon slot="graphic" path=${u}></ha-svg-icon>
              </ha-list-item>
            `:a.s6}
        ${this.includeState||this.includeNone?a.qy`<ha-md-divider role="separator" tabindex="-1"></ha-md-divider>`:a.s6}
        ${Array.from(n.l).map((e=>a.qy`
            <ha-list-item .value=${e} graphic="icon">
              ${this.hass.localize(`ui.components.color-picker.colors.${e}`)||e}
              ${this.defaultColor===e?` (${this.hass.localize("ui.components.color-picker.default")})`:a.s6}
              <span slot="graphic">${this.renderColorCircle(e)}</span>
            </ha-list-item>
          `))}
        ${t?a.qy`
              <ha-list-item .value=${e} graphic="icon">
                ${e}
                <span slot="graphic">${this.renderColorCircle(e)}</span>
              </ha-list-item>
            `:a.s6}
      </ha-select>
    `}},{kind:"method",key:"renderColorCircle",value:function(e){return a.qy`
      <span
        class="circle-color"
        style=${(0,c.W)({"--circle-color":(0,n.M)(e)})}
      ></span>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      .circle-color {
        display: block;
        background-color: var(--circle-color, var(--divider-color));
        border-radius: 10px;
        width: 20px;
        height: 20px;
        box-sizing: border-box;
      }
      ha-select {
        width: 100%;
      }
    `}}]}}),a.WF)},81643:(e,t,i)=>{var o=i(85461),s=i(69534),a=i(53401),r=i(98597),c=i(196);(0,o.A)([(0,c.EM)("ha-md-divider")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",static:!0,key:"styles",value(){return[...(0,s.A)(i,"styles",this),r.AH`
      :host {
        --md-divider-color: var(--divider-color);
      }
    `]}}]}}),a.h)},99438:(e,t,i)=>{var o=i(85461),s=i(69534),a=i(23605),r=i(18354),c=i(98597),n=i(196),l=i(97976);(0,o.A)([(0,n.EM)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"haptic",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){(0,s.A)(i,"firstUpdated",this,3)([]),this.addEventListener("change",(()=>{this.haptic&&(0,l.j)("light")}))}},{kind:"field",static:!0,key:"styles",value(){return[r.R,c.AH`
      :host {
        --mdc-theme-secondary: var(--switch-checked-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
        background-color: var(--switch-checked-button-color);
        border-color: var(--switch-checked-button-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__track {
        background-color: var(--switch-checked-track-color);
        border-color: var(--switch-checked-track-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
        background-color: var(--switch-unchecked-button-color);
        border-color: var(--switch-unchecked-button-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
        background-color: var(--switch-unchecked-track-color);
        border-color: var(--switch-unchecked-track-color);
      }
    `]}}]}}),a.U)},97976:(e,t,i)=>{i.d(t,{j:()=>s});var o=i(33167);const s=e=>{(0,o.r)(window,"haptic",e)}},64987:(e,t,i)=>{i.r(t);var o=i(85461),s=(i(58068),i(98597)),a=i(196),r=i(33167),c=(i(91074),i(88762)),n=(i(32694),i(99438),i(59373),i(77984),i(94090),i(43799));(0,o.A)([(0,a.EM)("dialog-label-detail")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_color",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_description",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_submitting",value(){return!1}},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._error=void 0,this._params.entry?(this._name=this._params.entry.name||"",this._icon=this._params.entry.icon||"",this._color=this._params.entry.color||"",this._description=this._params.entry.description||""):(this._name=this._params.suggestedName||"",this._icon="",this._color="",this._description=""),document.body.addEventListener("keydown",this._handleKeyPress)}},{kind:"field",key:"_handleKeyPress",value(){return e=>{"Escape"===e.key&&e.stopPropagation()}}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,r.r)(this,"dialog-closed",{dialog:this.localName}),document.body.removeEventListener("keydown",this._handleKeyPress)}},{kind:"method",key:"render",value:function(){return this._params?s.qy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        .heading=${(0,c.l)(this.hass,this._params.entry?this._params.entry.name||this._params.entry.label_id:this.hass.localize("ui.panel.config.labels.detail.new_label"))}
      >
        <div>
          ${this._error?s.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
          <div class="form">
            <ha-textfield
              dialogInitialFocus
              .value=${this._name}
              .configValue=${"name"}
              @input=${this._input}
              .label=${this.hass.localize("ui.panel.config.labels.detail.name")}
              .validationMessage=${this.hass.localize("ui.panel.config.labels.detail.required_error_msg")}
              required
            ></ha-textfield>
            <ha-icon-picker
              .value=${this._icon}
              .hass=${this.hass}
              .configValue=${"icon"}
              @value-changed=${this._valueChanged}
              .label=${this.hass.localize("ui.panel.config.labels.detail.icon")}
            ></ha-icon-picker>
            <ha-color-picker
              .value=${this._color}
              .configValue=${"color"}
              .hass=${this.hass}
              @value-changed=${this._valueChanged}
              .label=${this.hass.localize("ui.panel.config.labels.detail.color")}
            ></ha-color-picker>
            <ha-textarea
              .value=${this._description}
              .configValue=${"description"}
              @input=${this._input}
              .label=${this.hass.localize("ui.panel.config.labels.detail.description")}
            ></ha-textarea>
          </div>
        </div>
        ${this._params.entry&&this._params.removeEntry?s.qy`
              <mwc-button
                slot="secondaryAction"
                class="warning"
                @click=${this._deleteEntry}
                .disabled=${this._submitting}
              >
                ${this.hass.localize("ui.panel.config.labels.detail.delete")}
              </mwc-button>
            `:s.s6}
        <mwc-button
          slot="primaryAction"
          @click=${this._updateEntry}
          .disabled=${this._submitting||!this._name}
        >
          ${this._params.entry?this.hass.localize("ui.panel.config.labels.detail.update"):this.hass.localize("ui.panel.config.labels.detail.create")}
        </mwc-button>
      </ha-dialog>
    `:s.s6}},{kind:"method",key:"_input",value:function(e){const t=e.target,i=t.configValue;this._error=void 0,this[`_${i}`]=t.value}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.target.configValue;this._error=void 0,this[`_${t}`]=e.detail.value||""}},{kind:"method",key:"_updateEntry",value:async function(){let e;this._submitting=!0;try{const t={name:this._name.trim(),icon:this._icon.trim()||null,color:this._color.trim()||null,description:this._description.trim()||null};e=this._params.entry?await this._params.updateEntry(t):await this._params.createEntry(t),this.closeDialog()}catch(t){this._error=t?t.message:"Unknown error"}finally{this._submitting=!1}return e}},{kind:"method",key:"_deleteEntry",value:async function(){this._submitting=!0;try{await this._params.removeEntry()&&(this._params=void 0)}finally{this._submitting=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[n.nA,s.AH`
        a {
          color: var(--primary-color);
        }
        ha-textarea,
        ha-textfield,
        ha-icon-picker,
        ha-color-picker {
          display: block;
        }
        ha-color-picker,
        ha-textarea {
          margin-top: 16px;
        }
      `]}}]}}),s.WF)},23605:(e,t,i)=>{i.d(t,{U:()=>v});var o=i(76513),s=(i(86395),i(5789)),a=i(71086),r=i(16584),c=i(90523),n=i(4943),l={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},d={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"};const h=function(e){function t(i){return e.call(this,(0,o.Cl)((0,o.Cl)({},t.defaultAdapter),i))||this}return(0,o.C6)(t,e),Object.defineProperty(t,"strings",{get:function(){return d},enumerable:!1,configurable:!0}),Object.defineProperty(t,"cssClasses",{get:function(){return l},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),t.prototype.setChecked=function(e){this.adapter.setNativeControlChecked(e),this.updateAriaChecked(e),this.updateCheckedStyling(e)},t.prototype.setDisabled=function(e){this.adapter.setNativeControlDisabled(e),e?this.adapter.addClass(l.DISABLED):this.adapter.removeClass(l.DISABLED)},t.prototype.handleChange=function(e){var t=e.target;this.updateAriaChecked(t.checked),this.updateCheckedStyling(t.checked)},t.prototype.updateCheckedStyling=function(e){e?this.adapter.addClass(l.CHECKED):this.adapter.removeClass(l.CHECKED)},t.prototype.updateAriaChecked=function(e){this.adapter.setNativeControlAttr(d.ARIA_CHECKED_ATTR,""+!!e)},t}(n.I);var u=i(98597),p=i(196),m=i(79278);class v extends a.O{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=h,this.rippleHandlers=new c.I((()=>(this.shouldRenderRipple=!0,this.ripple)))}changeHandler(e){this.mdcFoundation.handleChange(e),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},(0,a.i)(this.mdcRoot)),{setNativeControlChecked:e=>{this.formElement.checked=e},setNativeControlDisabled:e=>{this.formElement.disabled=e},setNativeControlAttr:(e,t)=>{this.formElement.setAttribute(e,t)}})}renderRipple(){return this.shouldRenderRipple?u.qy`
        <mwc-ripple
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const e=this.formElement;e&&(this.rippleHandlers.startFocus(),e.focus())}blur(){const e=this.formElement;e&&(this.rippleHandlers.endFocus(),e.blur())}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}render(){return u.qy`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              aria-label="${(0,m.J)(this.ariaLabel)}"
              aria-labelledby="${(0,m.J)(this.ariaLabelledBy)}"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,o.Cg)([(0,p.MZ)({type:Boolean}),(0,r.P)((function(e){this.mdcFoundation.setChecked(e)}))],v.prototype,"checked",void 0),(0,o.Cg)([(0,p.MZ)({type:Boolean}),(0,r.P)((function(e){this.mdcFoundation.setDisabled(e)}))],v.prototype,"disabled",void 0),(0,o.Cg)([s.T,(0,p.MZ)({attribute:"aria-label"})],v.prototype,"ariaLabel",void 0),(0,o.Cg)([s.T,(0,p.MZ)({attribute:"aria-labelledby"})],v.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,p.P)(".mdc-switch")],v.prototype,"mdcRoot",void 0),(0,o.Cg)([(0,p.P)("input")],v.prototype,"formElement",void 0),(0,o.Cg)([(0,p.nJ)("mwc-ripple")],v.prototype,"ripple",void 0),(0,o.Cg)([(0,p.wk)()],v.prototype,"shouldRenderRipple",void 0),(0,o.Cg)([(0,p.Ls)({passive:!0})],v.prototype,"handleRippleMouseDown",null),(0,o.Cg)([(0,p.Ls)({passive:!0})],v.prototype,"handleRippleTouchStart",null)},18354:(e,t,i)=>{i.d(t,{R:()=>o});const o=i(98597).AH`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`},53401:(e,t,i)=>{i.d(t,{h:()=>n});var o=i(76513),s=i(196),a=i(98597);class r extends a.WF{constructor(){super(...arguments),this.inset=!1,this.insetStart=!1,this.insetEnd=!1}}(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],r.prototype,"inset",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"inset-start"})],r.prototype,"insetStart",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"inset-end"})],r.prototype,"insetEnd",void 0);const c=a.AH`:host{box-sizing:border-box;color:var(--md-divider-color, var(--md-sys-color-outline-variant, #cac4d0));display:flex;height:var(--md-divider-thickness, 1px);width:100%}:host([inset]),:host([inset-start]){padding-inline-start:16px}:host([inset]),:host([inset-end]){padding-inline-end:16px}:host::before{background:currentColor;content:"";height:100%;width:100%}@media(forced-colors: active){:host::before{background:CanvasText}}
`;let n=class extends r{};n.styles=[c],n=(0,o.Cg)([(0,s.EM)("md-divider")],n)}};
//# sourceMappingURL=qUKpHyFk.js.map