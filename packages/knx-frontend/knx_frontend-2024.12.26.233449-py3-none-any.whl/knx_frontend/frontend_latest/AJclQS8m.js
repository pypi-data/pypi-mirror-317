export const id=6805;export const ids=[6805];export const modules={6805:(e,i,t)=>{t.r(i);var a=t(85461),s=t(98597),n=t(196),l=t(33167),o=(t(32694),t(32283),t(59373),t(43799));(0,a.A)([(0,n.EM)("ha-input_number-form")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",key:"_item",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_max",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_min",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_mode",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_step",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_unit_of_measurement",value:void 0},{kind:"set",key:"item",value:function(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._max=e.max??100,this._min=e.min??0,this._mode=e.mode||"slider",this._step=e.step??1,this._unit_of_measurement=e.unit_of_measurement):(this._item={min:0,max:100},this._name="",this._icon="",this._max=100,this._min=0,this._mode="slider",this._step=1)}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>this.shadowRoot?.querySelector("[dialogInitialFocus]")?.focus()))}},{kind:"method",key:"render",value:function(){return this.hass?s.qy`
      <div class="form">
        <ha-textfield
          .value=${this._name}
          .configValue=${"name"}
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.name")}
          autoValidate
          required
          .validationMessage=${this.hass.localize("ui.dialogs.helper_settings.required_error_msg")}
          dialogInitialFocus
        ></ha-textfield>
        <ha-icon-picker
          .hass=${this.hass}
          .value=${this._icon}
          .configValue=${"icon"}
          @value-changed=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.icon")}
        ></ha-icon-picker>
        <ha-textfield
          .value=${this._min}
          .configValue=${"min"}
          type="number"
          step="any"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.min")}
        ></ha-textfield>
        <ha-textfield
          .value=${this._max}
          .configValue=${"max"}
          type="number"
          step="any"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.max")}
        ></ha-textfield>
        ${this.hass.userData?.showAdvanced?s.qy`
              <div class="layout horizontal center justified">
                ${this.hass.localize("ui.dialogs.helper_settings.input_number.mode")}
                <ha-formfield
                  .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.slider")}
                >
                  <ha-radio
                    name="mode"
                    value="slider"
                    .checked=${"slider"===this._mode}
                    @change=${this._modeChanged}
                  ></ha-radio>
                </ha-formfield>
                <ha-formfield
                  .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.box")}
                >
                  <ha-radio
                    name="mode"
                    value="box"
                    .checked=${"box"===this._mode}
                    @change=${this._modeChanged}
                  ></ha-radio>
                </ha-formfield>
              </div>
              <ha-textfield
                .value=${this._step}
                .configValue=${"step"}
                type="number"
                step="any"
                @input=${this._valueChanged}
                .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.step")}
              ></ha-textfield>

              <ha-textfield
                .value=${this._unit_of_measurement||""}
                .configValue=${"unit_of_measurement"}
                @input=${this._valueChanged}
                .label=${this.hass.localize("ui.dialogs.helper_settings.input_number.unit_of_measurement")}
              ></ha-textfield>
            `:""}
      </div>
    `:s.s6}},{kind:"method",key:"_modeChanged",value:function(e){(0,l.r)(this,"value-changed",{value:{...this._item,mode:e.target.value}})}},{kind:"method",key:"_valueChanged",value:function(e){if(!this.new&&!this._item)return;e.stopPropagation();const i=e.target,t=i.configValue,a="number"===i.type?Number(i.value):e.detail?.value||i.value;if(this[`_${t}`]===a)return;const s={...this._item};void 0===a||""===a?delete s[t]:s[t]=a,(0,l.r)(this,"value-changed",{value:s})}},{kind:"get",static:!0,key:"styles",value:function(){return[o.RF,s.AH`
        .form {
          color: var(--primary-text-color);
        }

        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
      `]}}]}}),s.WF)}};
//# sourceMappingURL=AJclQS8m.js.map