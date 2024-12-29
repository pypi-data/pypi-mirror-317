export const id=4776;export const ids=[4776];export const modules={22560:(e,t,i)=>{var a=i(85461),o=(i(23981),i(98597)),n=i(196),s=i(79278),d=i(33167),l=i(24517);i(96334),i(96396),i(59373),i(43689);(0,a.A)([(0,n.EM)("ha-base-time-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"autoValidate",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"format",value(){return 12}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"days",value(){return 0}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"hours",value(){return 0}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"minutes",value(){return 0}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"seconds",value(){return 0}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"milliseconds",value(){return 0}},{kind:"field",decorators:[(0,n.MZ)()],key:"dayLabel",value(){return""}},{kind:"field",decorators:[(0,n.MZ)()],key:"hourLabel",value(){return""}},{kind:"field",decorators:[(0,n.MZ)()],key:"minLabel",value(){return""}},{kind:"field",decorators:[(0,n.MZ)()],key:"secLabel",value(){return""}},{kind:"field",decorators:[(0,n.MZ)()],key:"millisecLabel",value(){return""}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"enableSecond",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"enableMillisecond",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"enableDay",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"noHoursLimit",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)()],key:"amPm",value(){return"AM"}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"clearable",value:void 0},{kind:"method",key:"render",value:function(){return o.qy`
      ${this.label?o.qy`<label>${this.label}${this.required?" *":""}</label>`:""}
      <div class="time-input-wrap-wrap">
        <div class="time-input-wrap">
          ${this.enableDay?o.qy`
                <ha-textfield
                  id="day"
                  type="number"
                  inputmode="numeric"
                  .value=${this.days.toFixed()}
                  .label=${this.dayLabel}
                  name="days"
                  @change=${this._valueChanged}
                  @focusin=${this._onFocus}
                  no-spinner
                  .required=${this.required}
                  .autoValidate=${this.autoValidate}
                  min="0"
                  .disabled=${this.disabled}
                  suffix=":"
                  class="hasSuffix"
                >
                </ha-textfield>
              `:""}

          <ha-textfield
            id="hour"
            type="number"
            inputmode="numeric"
            .value=${this.hours.toFixed()}
            .label=${this.hourLabel}
            name="hours"
            @change=${this._valueChanged}
            @focusin=${this._onFocus}
            no-spinner
            .required=${this.required}
            .autoValidate=${this.autoValidate}
            maxlength="2"
            max=${(0,s.J)(this._hourMax)}
            min="0"
            .disabled=${this.disabled}
            suffix=":"
            class="hasSuffix"
          >
          </ha-textfield>
          <ha-textfield
            id="min"
            type="number"
            inputmode="numeric"
            .value=${this._formatValue(this.minutes)}
            .label=${this.minLabel}
            @change=${this._valueChanged}
            @focusin=${this._onFocus}
            name="minutes"
            no-spinner
            .required=${this.required}
            .autoValidate=${this.autoValidate}
            maxlength="2"
            max="59"
            min="0"
            .disabled=${this.disabled}
            .suffix=${this.enableSecond?":":""}
            class=${this.enableSecond?"has-suffix":""}
          >
          </ha-textfield>
          ${this.enableSecond?o.qy`<ha-textfield
                id="sec"
                type="number"
                inputmode="numeric"
                .value=${this._formatValue(this.seconds)}
                .label=${this.secLabel}
                @change=${this._valueChanged}
                @focusin=${this._onFocus}
                name="seconds"
                no-spinner
                .required=${this.required}
                .autoValidate=${this.autoValidate}
                maxlength="2"
                max="59"
                min="0"
                .disabled=${this.disabled}
                .suffix=${this.enableMillisecond?":":""}
                class=${this.enableMillisecond?"has-suffix":""}
              >
              </ha-textfield>`:""}
          ${this.enableMillisecond?o.qy`<ha-textfield
                id="millisec"
                type="number"
                .value=${this._formatValue(this.milliseconds,3)}
                .label=${this.millisecLabel}
                @change=${this._valueChanged}
                @focusin=${this._onFocus}
                name="milliseconds"
                no-spinner
                .required=${this.required}
                .autoValidate=${this.autoValidate}
                maxlength="3"
                max="999"
                min="0"
                .disabled=${this.disabled}
              >
              </ha-textfield>`:""}
          ${!this.clearable||this.required||this.disabled?o.s6:o.qy`<ha-icon-button
                label="clear"
                @click=${this._clearValue}
                .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              ></ha-icon-button>`}
        </div>

        ${24===this.format?"":o.qy`<ha-select
              .required=${this.required}
              .value=${this.amPm}
              .disabled=${this.disabled}
              name="amPm"
              naturalMenuWidth
              fixedMenuPosition
              @selected=${this._valueChanged}
              @closed=${l.d}
            >
              <mwc-list-item value="AM">AM</mwc-list-item>
              <mwc-list-item value="PM">PM</mwc-list-item>
            </ha-select>`}
        ${this.helper?o.qy`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
      </div>
    `}},{kind:"method",key:"_clearValue",value:function(){(0,d.r)(this,"value-changed")}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.currentTarget;this[t.name]="amPm"===t.name?t.value:Number(t.value);const i={hours:this.hours,minutes:this.minutes,seconds:this.seconds,milliseconds:this.milliseconds};this.enableDay&&(i.days=this.days),12===this.format&&(i.amPm=this.amPm),(0,d.r)(this,"value-changed",{value:i})}},{kind:"method",key:"_onFocus",value:function(e){e.currentTarget.select()}},{kind:"method",key:"_formatValue",value:function(e,t=2){return e.toString().padStart(t,"0")}},{kind:"get",key:"_hourMax",value:function(){if(!this.noHoursLimit)return 12===this.format?12:23}},{kind:"field",static:!0,key:"styles",value(){return o.AH`
    :host([clearable]) {
      position: relative;
    }
    :host {
      display: block;
    }
    .time-input-wrap-wrap {
      display: flex;
    }
    .time-input-wrap {
      display: flex;
      border-radius: var(--mdc-shape-small, 4px) var(--mdc-shape-small, 4px) 0 0;
      overflow: hidden;
      position: relative;
      direction: ltr;
      padding-right: 3px;
    }
    ha-textfield {
      width: 55px;
      text-align: center;
      --mdc-shape-small: 0;
      --text-field-appearance: none;
      --text-field-padding: 0 4px;
      --text-field-suffix-padding-left: 2px;
      --text-field-suffix-padding-right: 0;
      --text-field-text-align: center;
    }
    ha-textfield.hasSuffix {
      --text-field-padding: 0 0 0 4px;
    }
    ha-textfield:first-child {
      --text-field-border-top-left-radius: var(--mdc-shape-medium);
    }
    ha-textfield:last-child {
      --text-field-border-top-right-radius: var(--mdc-shape-medium);
    }
    ha-select {
      --mdc-shape-small: 0;
      width: 85px;
    }
    :host([clearable]) .mdc-select__anchor {
        padding-inline-end: var(--select-selected-text-padding-end, 12px);
    }
    ha-icon-button {
      position: relative
      --mdc-icon-button-size: 36px;
      --mdc-icon-size: 20px;
      color: var(--secondary-text-color);
      direction: var(--direction);
      display: flex;
      align-items: center;
      background-color:var(--mdc-text-field-fill-color, whitesmoke);
      border-bottom-style: solid;
      border-bottom-width: 1px;
    }
    label {
      -moz-osx-font-smoothing: grayscale;
      -webkit-font-smoothing: antialiased;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, Roboto, sans-serif)
      );
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      line-height: var(--mdc-typography-body2-line-height, 1.25rem);
      font-weight: var(--mdc-typography-body2-font-weight, 400);
      letter-spacing: var(
        --mdc-typography-body2-letter-spacing,
        0.0178571429em
      );
      text-decoration: var(--mdc-typography-body2-text-decoration, inherit);
      text-transform: var(--mdc-typography-body2-text-transform, inherit);
      color: var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));
      padding-left: 4px;
      padding-inline-start: 4px;
      padding-inline-end: initial;
    }
  `}}]}}),o.WF)},6759:(e,t,i)=>{var a=i(85461),o=i(98597),n=i(196),s=i(33167);i(22560);(0,a.A)([(0,n.EM)("ha-duration-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"enableMillisecond",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"enableDay",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.P)("paper-time-input",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-base-time-input
        .label=${this.label}
        .helper=${this.helper}
        .required=${this.required}
        .clearable=${!this.required&&void 0!==this.data}
        .autoValidate=${this.required}
        .disabled=${this.disabled}
        errorMessage="Required"
        enableSecond
        .enableMillisecond=${this.enableMillisecond}
        .enableDay=${this.enableDay}
        format="24"
        .days=${this._days}
        .hours=${this._hours}
        .minutes=${this._minutes}
        .seconds=${this._seconds}
        .milliseconds=${this._milliseconds}
        @value-changed=${this._durationChanged}
        noHoursLimit
        dayLabel="dd"
        hourLabel="hh"
        minLabel="mm"
        secLabel="ss"
        millisecLabel="ms"
      ></ha-base-time-input>
    `}},{kind:"get",key:"_days",value:function(){return this.data?.days?Number(this.data.days):this.required||this.data?0:NaN}},{kind:"get",key:"_hours",value:function(){return this.data?.hours?Number(this.data.hours):this.required||this.data?0:NaN}},{kind:"get",key:"_minutes",value:function(){return this.data?.minutes?Number(this.data.minutes):this.required||this.data?0:NaN}},{kind:"get",key:"_seconds",value:function(){return this.data?.seconds?Number(this.data.seconds):this.required||this.data?0:NaN}},{kind:"get",key:"_milliseconds",value:function(){return this.data?.milliseconds?Number(this.data.milliseconds):this.required||this.data?0:NaN}},{kind:"method",key:"_durationChanged",value:function(e){e.stopPropagation();const t=e.detail.value?{...e.detail.value}:void 0;t&&(t.hours||=0,t.minutes||=0,t.seconds||=0,"days"in t&&(t.days||=0),"milliseconds"in t&&(t.milliseconds||=0),this.enableMillisecond||t.milliseconds?t.milliseconds>999&&(t.seconds+=Math.floor(t.milliseconds/1e3),t.milliseconds%=1e3):delete t.milliseconds,t.seconds>59&&(t.minutes+=Math.floor(t.seconds/60),t.seconds%=60),t.minutes>59&&(t.hours+=Math.floor(t.minutes/60),t.minutes%=60),this.enableDay&&t.hours>24&&(t.days=(t.days??0)+Math.floor(t.hours/24),t.hours%=24)),(0,s.r)(this,"value-changed",{value:t})}}]}}),o.WF)},54776:(e,t,i)=>{i.r(t),i.d(t,{HaActionSelector:()=>se});var a=i(85461),o=i(98597),n=i(196),s=i(45081),d=i(12873),l=i(69534),c=i(92518),r=i(66580),h=i(67905),u=i(33167),p=i(63049),v=i(45787),m=(i(66494),i(69154),i(29222),i(3820)),f=i(77237),k=i(26349),g=(i(23981),i(69760)),y=i(90662),_=i(24517),b=i(1695),$=i(78226),M=(i(91074),i(80920),i(94392),i(91686),i(96396),i(60929),i(44164)),w=i(54671),A=i(96041),x=i(56591),V=i(53935),C=i(91330),H=i(76201),L=i(56678),Z=i(28712),z=i(95336),q=i(40884),F=i(27761),P=i(31238);const E="ui.panel.config.automation.editor.actions.type",B=(e,t,i,a,o,n,s=!1)=>{try{const d=R(e,t,i,a,o,n,s);if("string"!=typeof d)throw new Error(String(d));return d}catch(d){console.error(d);let e="Error in describing action";return d.message&&(e+=": "+d.message),e}},R=(e,t,i,a,o,n,s=!1)=>{if(o.alias&&!s)return o.alias;if(n||(n=(0,d.pq)(o)),"service"===n){const n=o,s=[],d=n.target||n.data;if(d)for(const[o,l]of Object.entries({area_id:"areas",device_id:"devices",entity_id:"entities",floor_id:"floors",label_id:"labels"})){if(!(o in d))continue;const n=(0,A.e)(d[o])||[];for(const d of n){if((0,L.F)(d)){s.push(e.localize(`${E}.service.description.target_template`,{name:l}));break}if("entity_id"===o)if(d.includes(".")){const t=e.states[d];t?s.push((0,C.u)(t)):s.push(d)}else{const i=(0,F.P9)(t)[d];i?s.push((0,F.jh)(e,i)||d):"all"===d?s.push(e.localize(`${E}.service.description.target_every_entity`)):s.push(e.localize(`${E}.service.description.target_unknown_entity`))}else if("device_id"===o){const t=e.devices[d];t?s.push((0,q.xn)(t,e)):s.push(e.localize(`${E}.service.description.target_unknown_device`))}else if("area_id"===o){const t=e.areas[d];t?.name?s.push(t.name):s.push(e.localize(`${E}.service.description.target_unknown_area`))}else if("floor_id"===o){const t=a[d]??void 0;t?.name?s.push(t.name):s.push(e.localize(`${E}.service.description.target_unknown_floor`))}else if("label_id"===o){const t=i.find((e=>e.label_id===d));t?.name?s.push(t.name):s.push(e.localize(`${E}.service.description.target_unknown_label`))}else s.push(d)}}if(n.service_template||n.action&&(0,L.F)(n.action))return e.localize(s.length?`${E}.service.description.service_based_on_template`:`${E}.service.description.service_based_on_template_no_targets`,{targets:(0,H.c)(e.locale,s)});if(n.action){const[t,i]=n.action.split(".",2),a=e.localize(`component.${t}.services.${i}.name`)||e.services[t][i]?.name;return n.metadata?e.localize(s.length?`${E}.service.description.service_name`:`${E}.service.description.service_name_no_targets`,{domain:(0,P.p$)(e.localize,t),name:a||n.action,targets:(0,H.c)(e.locale,s)}):e.localize(s.length?`${E}.service.description.service_based_on_name`:`${E}.service.description.service_based_on_name_no_targets`,{name:a?`${(0,P.p$)(e.localize,t)}: ${a}`:n.action,targets:(0,H.c)(e.locale,s)})}return e.localize(`${E}.service.description.service`)}if("delay"===n){const t=o;let i;return i="number"==typeof t.delay?e.localize(`${E}.delay.description.duration_string`,{string:(0,V.A)(t.delay)}):"string"==typeof t.delay?(0,L.F)(t.delay)?e.localize(`${E}.delay.description.duration_template`):e.localize(`${E}.delay.description.duration_string`,{string:t.delay||e.localize(`${E}.delay.description.duration_unknown`)}):t.delay?e.localize(`${E}.delay.description.duration_string`,{string:(0,x.a)(e.locale,t.delay)}):e.localize(`${E}.delay.description.duration_string`,{string:e.localize(`${E}.delay.description.duration_unknown`)}),e.localize(`${E}.delay.description.full`,{duration:i})}if("activate_scene"===n){const t=o;let i;if(i="scene"in t?t.scene:t.target?.entity_id||t.entity_id,!i)return e.localize(`${E}.activate_scene.description.activate_scene`);const a=i?e.states[i]:void 0;return e.localize(`${E}.activate_scene.description.activate_scene_with_name`,{name:a?(0,C.u)(a):i})}if("play_media"===n){const t=o,i=t.target?.entity_id||t.entity_id,a=i?e.states[i]:void 0;return e.localize(`${E}.play_media.description.full`,{hasMedia:t.metadata.title||t.data.media_content_id?"true":"false",media:t.metadata.title||t.data.media_content_id,hasMediaPlayer:a||void 0!==i?"true":"false",mediaPlayer:a?(0,C.u)(a):i})}if("wait_for_trigger"===n){const t=o,i=(0,A.e)(t.wait_for_trigger);return i&&0!==i.length?e.localize(`${E}.wait_for_trigger.description.wait_for_triggers`,{count:i.length}):e.localize(`${E}.wait_for_trigger.description.wait_for_a_trigger`)}if("variables"===n){const t=o;return e.localize(`${E}.variables.description.full`,{names:(0,H.c)(e.locale,Object.keys(t.variables))})}if("fire_event"===n){const t=o;return(0,L.F)(t.event)?e.localize(`${E}.event.description.full`,{name:e.localize(`${E}.event.description.template`)}):e.localize(`${E}.event.description.full`,{name:t.event})}if("wait_template"===n)return e.localize(`${E}.wait_template.description.full`);if("stop"===n){const t=o;return e.localize(`${E}.stop.description.full`,{hasReason:void 0!==t.stop?"true":"false",reason:t.stop})}if("if"===n){return void 0!==o.else?e.localize(`${E}.if.description.if_else`):e.localize(`${E}.if.description.if`)}if("choose"===n){const t=o;if(t.choose){const i=(0,A.e)(t.choose).length+(t.default?1:0);return e.localize(`${E}.choose.description.full`,{number:i})}return e.localize(`${E}.choose.description.no_action`)}if("repeat"===n){const t=o;let i="";if("count"in t.repeat){const a=t.repeat.count;i=e.localize(`${E}.repeat.description.count`,{count:a})}else if("while"in t.repeat){const a=(0,A.e)(t.repeat.while);i=e.localize(`${E}.repeat.description.while_count`,{count:a.length})}else if("until"in t.repeat){const a=(0,A.e)(t.repeat.until);i=e.localize(`${E}.repeat.description.until_count`,{count:a.length})}else if("for_each"in t.repeat){const a=(0,A.e)(t.repeat.for_each).map((e=>JSON.stringify(e)));i=e.localize(`${E}.repeat.description.for_each`,{items:(0,H.c)(e.locale,a)})}return e.localize(`${E}.repeat.description.full`,{chosenAction:i})}if("check_condition"===n)return e.localize(`${E}.check_condition.description.full`,{condition:(0,Z.p)(o,e,t)});if("device_action"===n){const i=o;if(!i.device_id)return e.localize(`${E}.device_id.description.no_device`);const a=(0,z.PV)(e,t,i);if(a)return a;const n=e.states[i.entity_id];return`${i.type||"Perform action with"} ${n?(0,C.u)(n):i.entity_id}`}if("sequence"===n){const t=o,i=(0,A.e)(t.sequence).length;return e.localize(`${E}.sequence.description.full`,{number:i})}if("parallel"===n){const t=o,i=(0,A.e)(t.parallel).length;return e.localize(`${E}.parallel.description.full`,{number:i})}if("set_conversation_response"===n){const t=o;return e.localize(`${E}.set_conversation_response.description.full`,{response:t.set_conversation_response})}return n};var D=i(31447),S=i(43799),O=i(34947);i(85067);const N=["scene"];(0,a.A)([(0,n.EM)("ha-automation-action-activate_scene")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{action:"scene.turn_on",target:{entity_id:""},metadata:{}}}},{kind:"method",key:"render",value:function(){let e;return e="scene"in this.action?this.action.scene:this.action.target?.entity_id,o.qy`
      <ha-entity-picker
        .hass=${this.hass}
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.activate_scene.scene")}
        .value=${e}
        .disabled=${this.disabled}
        @value-changed=${this._entityPicked}
        .includeDomains=${N}
        allow-custom-entity
      ></ha-entity-picker>
    `}},{kind:"method",key:"_entityPicked",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.action,action:"scene.turn_on",target:{entity_id:e.detail.value},metadata:{}}})}}]}}),o.WF);var W=i(74754);i(3115);(0,a.A)([(0,n.EM)("ha-automation-option-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"option",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"index",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"first",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"last",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_expanded",value(){return!1}},{kind:"field",decorators:[(0,n.wk)(),(0,k.Fg)({context:w.ih,subscribe:!0})],key:"_entityReg",value:void 0},{kind:"method",key:"_expandedChanged",value:function(e){"option"===e.currentTarget.id&&(this._expanded=e.detail.expanded)}},{kind:"method",key:"_getDescription",value:function(){const e=(0,A.e)(this.option.conditions);if(!e||0===e.length)return this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.no_conditions");let t="";return"string"==typeof e[0]?t+=e[0]:t+=(0,Z.p)(e[0],this.hass,this._entityReg),e.length>1&&(t+=this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.option_description_additional",{numberOfAdditionalConditions:e.length-1})),t}},{kind:"method",key:"render",value:function(){return this.option?o.qy`
      <ha-card outlined>
        <ha-expansion-panel
          leftChevron
          @expanded-changed=${this._expandedChanged}
          id="option"
        >
          <h3 slot="header">
            ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.option",{number:this.index+1})}:
            ${this.option.alias||(this._expanded?"":this._getDescription())}
          </h3>

          <slot name="icons" slot="icons"></slot>

          <ha-button-menu
            slot="icons"
            @action=${this._handleAction}
            @click=${W.w}
            @closed=${_.d}
            fixed
          >
            <ha-icon-button
              slot="trigger"
              .label=${this.hass.localize("ui.common.menu")}
              .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
            ></ha-icon-button>
            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.rename")}
              <ha-svg-icon slot="graphic" .path=${"M18,17H10.5L12.5,15H18M6,17V14.5L13.88,6.65C14.07,6.45 14.39,6.45 14.59,6.65L16.35,8.41C16.55,8.61 16.55,8.92 16.35,9.12L8.47,17M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3Z"}></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.duplicate")}
              <ha-svg-icon
                slot="graphic"
                .path=${"M11,17H4A2,2 0 0,1 2,15V3A2,2 0 0,1 4,1H16V3H4V15H11V13L15,16L11,19V17M19,21V7H8V13H6V7A2,2 0 0,1 8,5H19A2,2 0 0,1 21,7V21A2,2 0 0,1 19,23H8A2,2 0 0,1 6,21V19H8V21H19Z"}
              ></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item
              graphic="icon"
              .disabled=${this.disabled||this.first}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.move_up")}
              <ha-svg-icon slot="graphic" .path=${"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"}></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item
              graphic="icon"
              .disabled=${this.disabled||this.last}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.move_down")}
              <ha-svg-icon slot="graphic" .path=${"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z"}></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item
              class="warning"
              graphic="icon"
              .disabled=${this.disabled}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.remove_option")}
              <ha-svg-icon
                class="warning"
                slot="graphic"
                .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
              ></ha-svg-icon>
            </mwc-list-item>
          </ha-button-menu>

          <div class="card-content">
            <h4>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.conditions")}:
            </h4>
            <ha-automation-condition
              .conditions=${(0,A.e)(this.option.conditions)}
              .disabled=${this.disabled}
              .hass=${this.hass}
              @value-changed=${this._conditionChanged}
            ></ha-automation-condition>
            <h4>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.sequence")}:
            </h4>
            <ha-automation-action
              .actions=${(0,A.e)(this.option.sequence)||[]}
              .disabled=${this.disabled}
              .hass=${this.hass}
              @value-changed=${this._actionChanged}
            ></ha-automation-action>
          </div>
        </ha-expansion-panel>
      </ha-card>
    `:o.s6}},{kind:"method",key:"_handleAction",value:async function(e){switch(e.detail.index){case 0:await this._renameOption();break;case 1:(0,u.r)(this,"duplicate");break;case 2:(0,u.r)(this,"move-up");break;case 3:(0,u.r)(this,"move-down");break;case 4:this._removeOption()}}},{kind:"method",key:"_removeOption",value:function(){(0,D.dk)(this,{title:this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.delete_confirm_title"),text:this.hass.localize("ui.panel.config.automation.editor.actions.delete_confirm_text"),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.delete"),destructive:!0,confirm:()=>(0,u.r)(this,"value-changed",{value:null})})}},{kind:"method",key:"_renameOption",value:async function(){const e=await(0,D.an)(this,{title:this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.change_alias"),inputLabel:this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.alias"),inputType:"string",placeholder:(0,b.Z)(this._getDescription()),defaultValue:this.option.alias,confirmText:this.hass.localize("ui.common.submit")});if(null!==e){const t={...this.option};""===e?delete t.alias:t.alias=e,(0,u.r)(this,"value-changed",{value:t})}}},{kind:"method",key:"_conditionChanged",value:function(e){e.stopPropagation();const t=e.detail.value,i={...this.option,conditions:t};(0,u.r)(this,"value-changed",{value:i})}},{kind:"method",key:"_actionChanged",value:function(e){e.stopPropagation();const t=e.detail.value,i={...this.option,sequence:t};(0,u.r)(this,"value-changed",{value:i})}},{kind:"method",key:"expand",value:function(){this.updateComplete.then((()=>{this.shadowRoot.querySelector("ha-expansion-panel").expanded=!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[S.RF,o.AH`
        ha-button-menu,
        ha-icon-button {
          --mdc-theme-text-primary-on-background: var(--primary-text-color);
        }
        .disabled {
          opacity: 0.5;
          pointer-events: none;
        }
        ha-expansion-panel {
          --expansion-panel-summary-padding: 0 0 0 8px;
          --expansion-panel-content-padding: 0;
        }
        h3 {
          margin: 0;
          font-size: inherit;
          font-weight: inherit;
        }
        .card-content {
          padding: 16px;
        }

        mwc-list-item[disabled] {
          --mdc-theme-text-primary-on-background: var(--disabled-text-color);
        }
        mwc-list-item.hidden {
          display: none;
        }
        .warning ul {
          margin: 4px 0;
        }
        li[role="separator"] {
          border-bottom-color: var(--divider-color);
        }
      `]}}]}}),o.WF);(0,a.A)([(0,n.EM)("ha-automation-option")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_showReorder",value(){return!1}},{kind:"field",decorators:[(0,h.I)({key:"automationClipboard",state:!0,subscribe:!0,storage:"sessionStorage"})],key:"_clipboard",value:void 0},{kind:"field",key:"_focusLastOptionOnChange",value(){return!1}},{kind:"field",key:"_optionsKeys",value(){return new WeakMap}},{kind:"field",key:"_unsubMql",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,l.A)(i,"connectedCallback",this,3)([]),this._unsubMql=(0,p.m)("(min-width: 600px)",(e=>{this._showReorder=e}))}},{kind:"method",key:"disconnectedCallback",value:function(){(0,l.A)(i,"disconnectedCallback",this,3)([]),this._unsubMql?.(),this._unsubMql=void 0}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-sortable
        handle-selector=".handle"
        draggable-selector="ha-automation-option-row"
        .disabled=${!this._showReorder||this.disabled}
        group="options"
        invert-swap
        @item-moved=${this._optionMoved}
        @item-added=${this._optionAdded}
        @item-removed=${this._optionRemoved}
      >
        <div class="options">
          ${(0,r.u)(this.options,(e=>this._getKey(e)),((e,t)=>o.qy`
              <ha-automation-option-row
                .sortableData=${e}
                .index=${t}
                .first=${0===t}
                .last=${t===this.options.length-1}
                .option=${e}
                .narrow=${this.narrow}
                .disabled=${this.disabled}
                @duplicate=${this._duplicateOption}
                @move-down=${this._moveDown}
                @move-up=${this._moveUp}
                @value-changed=${this._optionChanged}
                .hass=${this.hass}
              >
                ${this._showReorder&&!this.disabled?o.qy`
                      <div class="handle" slot="icons">
                        <ha-svg-icon .path=${"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"}></ha-svg-icon>
                      </div>
                    `:o.s6}
              </ha-automation-option-row>
            `))}
          <div class="buttons">
            <ha-button
              outlined
              .disabled=${this.disabled}
              .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.add_option")}
              @click=${this._addOption}
            >
              <ha-svg-icon .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"} slot="icon"></ha-svg-icon>
            </ha-button>
          </div>
        </div>
      </ha-sortable>
    `}},{kind:"method",key:"updated",value:function(e){if((0,l.A)(i,"updated",this,3)([e]),e.has("options")&&this._focusLastOptionOnChange){this._focusLastOptionOnChange=!1;const e=this.shadowRoot.querySelector("ha-automation-option-row:last-of-type");e.updateComplete.then((()=>{e.expand(),e.scrollIntoView(),e.focus()}))}}},{kind:"method",key:"expandAll",value:function(){this.shadowRoot.querySelectorAll("ha-automation-option-row").forEach((e=>{e.expand()}))}},{kind:"field",key:"_addOption",value(){return()=>{const e=this.options.concat({conditions:[],sequence:[]});this._focusLastOptionOnChange=!0,(0,u.r)(this,"value-changed",{value:e})}}},{kind:"method",key:"_getKey",value:function(e){return this._optionsKeys.has(e)||this._optionsKeys.set(e,Math.random().toString()),this._optionsKeys.get(e)}},{kind:"method",key:"_moveUp",value:function(e){e.stopPropagation();const t=e.target.index,i=t-1;this._move(t,i)}},{kind:"method",key:"_moveDown",value:function(e){e.stopPropagation();const t=e.target.index,i=t+1;this._move(t,i)}},{kind:"method",key:"_move",value:function(e,t){const i=this.options.concat(),a=i.splice(e,1)[0];i.splice(t,0,a),this.options=i,(0,u.r)(this,"value-changed",{value:i})}},{kind:"method",key:"_optionMoved",value:function(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail;this._move(t,i)}},{kind:"method",key:"_optionAdded",value:async function(e){e.stopPropagation();const{index:t,data:i}=e.detail,a=[...this.options.slice(0,t),i,...this.options.slice(t)];this.options=a,await(0,v.E)(),(0,u.r)(this,"value-changed",{value:this.options})}},{kind:"method",key:"_optionRemoved",value:async function(e){e.stopPropagation();const{index:t}=e.detail,i=this.options[t];this.options=this.options.filter((e=>e!==i)),await(0,v.E)();const a=this.options.filter((e=>e!==i));(0,u.r)(this,"value-changed",{value:a})}},{kind:"method",key:"_optionChanged",value:function(e){e.stopPropagation();const t=[...this.options],i=e.detail.value,a=e.target.index;if(null===i)t.splice(a,1);else{const e=this._getKey(t[a]);this._optionsKeys.set(i,e),t[a]=i}(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_duplicateOption",value:function(e){e.stopPropagation();const t=e.target.index;(0,u.r)(this,"value-changed",{value:this.options.concat((0,c.A)(this.options[t]))})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      .options {
        padding: 16px;
        margin: -16px;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      .sortable-ghost {
        background: none;
        border-radius: var(--ha-card-border-radius, 12px);
      }
      .sortable-drag {
        background: none;
      }
      ha-automation-option-row {
        display: block;
        scroll-margin-top: 48px;
      }
      ha-svg-icon {
        height: 20px;
      }
      .handle {
        padding: 12px;
        cursor: move; /* fallback if grab cursor is unsupported */
        cursor: grab;
      }
      .handle ha-svg-icon {
        pointer-events: none;
        height: 24px;
      }
      .buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        order: 1;
      }
    `}}]}}),o.WF),(0,a.A)([(0,n.EM)("ha-automation-action-choose")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_showDefault",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{choose:[{conditions:[],sequence:[]}]}}},{kind:"method",key:"render",value:function(){const e=this.action,t=e.choose?(0,A.e)(e.choose):[];return o.qy`
      <ha-automation-option
        .options=${t}
        .disabled=${this.disabled}
        @value-changed=${this._optionsChanged}
        .hass=${this.hass}
      ></ha-automation-option>

      ${this._showDefault||e.default?o.qy`
            <h2>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.default")}:
            </h2>
            <ha-automation-action
              .actions=${(0,A.e)(e.default)||[]}
              .disabled=${this.disabled}
              @value-changed=${this._defaultChanged}
              .hass=${this.hass}
            ></ha-automation-action>
          `:o.qy`
            <div class="link-button-row">
              <button
                class="link"
                @click=${this._addDefault}
                .disabled=${this.disabled}
              >
                ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.add_default")}
              </button>
            </div>
          `}
    `}},{kind:"method",key:"_addDefault",value:function(){this._showDefault=!0}},{kind:"method",key:"_optionsChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:{...this.action,choose:t}})}},{kind:"method",key:"_defaultChanged",value:function(e){e.stopPropagation(),this._showDefault=!0;const t=e.detail.value,i={...this.action,default:t};0===t.length&&delete i.default,(0,u.r)(this,"value-changed",{value:i})}},{kind:"get",static:!0,key:"styles",value:function(){return[S.RF,o.AH`
        .link-button-row {
          padding: 14px 14px 0 14px;
        }
      `]}}]}}),o.WF);var T=i(66412),U=(i(96334),i(84265));i(38750);(0,a.A)([(0,n.EM)("ha-automation-action-condition")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{condition:"state"}}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-select
        fixedMenuPosition
        .label=${this.hass.localize("ui.panel.config.automation.editor.conditions.type_select")}
        .disabled=${this.disabled}
        .value=${this.action.condition}
        naturalMenuWidth
        @selected=${this._typeChanged}
      >
        ${this._processedTypes(this.hass.localize).map((([e,t,i])=>o.qy`
            <mwc-list-item .value=${e} graphic="icon">
              ${t}<ha-svg-icon slot="graphic" .path=${i}></ha-svg-icon
            ></mwc-list-item>
          `))}
      </ha-select>
      <ha-automation-condition-editor
        .condition=${this.action}
        .disabled=${this.disabled}
        .hass=${this.hass}
        @value-changed=${this._conditionChanged}
      ></ha-automation-condition-editor>
    `}},{kind:"field",key:"_processedTypes",value(){return(0,s.A)((e=>Object.entries(U.D).map((([t,i])=>[t,e(`ui.panel.config.automation.editor.conditions.type.${t}.label`),i])).sort(((e,t)=>(0,T.x)(e[1],t[1],this.hass.locale.language)))))}},{kind:"method",key:"_conditionChanged",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:e.detail.value})}},{kind:"method",key:"_typeChanged",value:function(e){const t=e.target.value;if(!t)return;const i=customElements.get(`ha-automation-condition-${t}`);t!==this.action.condition&&(0,u.r)(this,"value-changed",{value:{...i.defaultConfig}})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-select {
        margin-bottom: 24px;
      }
    `}}]}}),o.WF);i(6759);var I=i(87545);(0,a.A)([(0,n.EM)("ha-automation-action-delay")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_timeData",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{delay:""}}},{kind:"method",key:"willUpdate",value:function(e){e.has("action")&&(this.action&&(0,L.r)(this.action)?(0,u.r)(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.no_template_editor_support"))):this._timeData=(0,I.z)(this.action.delay))}},{kind:"method",key:"render",value:function(){return o.qy`<ha-duration-input
      .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.delay.delay")}
      .disabled=${this.disabled}
      .data=${this._timeData}
      enableMillisecond
      required
      @value-changed=${this._valueChanged}
    ></ha-duration-input>`}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;t&&(0,u.r)(this,"value-changed",{value:{...this.action,delay:t}})}}]}}),o.WF);var K=i(82358);(0,a.A)([(0,n.EM)("ha-device-action-picker")],(function(e,t){return{F:class extends t{constructor(){super(z.PV,z.am,(e=>({device_id:e||"",domain:"",entity_id:""}))),e(this)}},d:[{kind:"get",key:"NO_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.actions.no_actions")}},{kind:"get",key:"UNKNOWN_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.actions.unknown_action")}}]}}),K.V);i(87190),i(93259);(0,a.A)([(0,n.EM)("ha-automation-action-device_id")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_deviceId",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_capabilities",value:void 0},{kind:"field",decorators:[(0,n.wk)(),(0,k.Fg)({context:w.ih,subscribe:!0})],key:"_entityReg",value:void 0},{kind:"field",key:"_origAction",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{device_id:"",domain:"",entity_id:""}}},{kind:"field",key:"_extraFieldsData",value(){return(0,s.A)(((e,t)=>{const i={};return t.extra_fields.forEach((t=>{void 0!==e[t.name]&&(i[t.name]=e[t.name])})),i}))}},{kind:"method",key:"shouldUpdate",value:function(e){return!e.has("action")||(!this.action.device_id||this.action.device_id in this.hass.devices||((0,u.r)(this,"ui-mode-not-available",Error(this.hass.localize("ui.panel.config.automation.editor.edit_unknown_device"))),!1))}},{kind:"method",key:"render",value:function(){const e=this._deviceId||this.action.device_id;return o.qy`
      <ha-device-picker
        .value=${e}
        .disabled=${this.disabled}
        @value-changed=${this._devicePicked}
        .hass=${this.hass}
        label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.device_id.label")}
      ></ha-device-picker>
      <ha-device-action-picker
        .value=${this.action}
        .deviceId=${e}
        .disabled=${this.disabled}
        @value-changed=${this._deviceActionPicked}
        .hass=${this.hass}
        label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.device_id.action")}
      ></ha-device-action-picker>
      ${this._capabilities?.extra_fields?.length?o.qy`
            <ha-form
              .hass=${this.hass}
              .data=${this._extraFieldsData(this.action,this._capabilities)}
              .schema=${this._capabilities.extra_fields}
              .disabled=${this.disabled}
              .computeLabel=${(0,z.T_)(this.hass,this.action)}
              .computeHelper=${(0,z.TH)(this.hass,this.action)}
              @value-changed=${this._extraFieldsChanged}
            ></ha-form>
          `:""}
    `}},{kind:"method",key:"firstUpdated",value:function(){this._capabilities||this._getCapabilities(),this.action&&(this._origAction=this.action)}},{kind:"method",key:"updated",value:function(e){const t=e.get("action");t&&!(0,z.Po)(this._entityReg,t,this.action)&&(this._deviceId=void 0,this._getCapabilities())}},{kind:"method",key:"_getCapabilities",value:async function(){this._capabilities=this.action.domain?await(0,z.jR)(this.hass,this.action):void 0}},{kind:"method",key:"_devicePicked",value:function(e){e.stopPropagation(),this._deviceId=e.target.value,void 0===this._deviceId&&(0,u.r)(this,"value-changed",{value:i.defaultConfig})}},{kind:"method",key:"_deviceActionPicked",value:function(e){e.stopPropagation();let t=e.detail.value;this._origAction&&(0,z.Po)(this._entityReg,this._origAction,t)&&(t=this._origAction),(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_extraFieldsChanged",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.action,...e.detail.value}})}},{kind:"field",static:!0,key:"styles",value(){return o.AH`
    ha-device-picker {
      display: block;
      margin-bottom: 24px;
    }

    ha-device-action-picker {
      display: block;
    }

    ha-form {
      display: block;
      margin-top: 24px;
    }
  `}}]}}),o.WF);i(10214),i(59373),i(42459);(0,a.A)([(0,n.EM)("ha-automation-action-event")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-yaml-editor",!0)],key:"_yamlEditor",value:void 0},{kind:"field",key:"_actionData",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{event:"",event_data:{}}}},{kind:"method",key:"updated",value:function(e){e.has("action")&&(this._actionData&&this._actionData!==this.action.event_data&&this._yamlEditor&&this._yamlEditor.setValue(this.action.event_data),this._actionData=this.action.event_data)}},{kind:"method",key:"render",value:function(){const{event:e,event_data:t}=this.action;return o.qy`
      <ha-textfield
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.event.event")}
        .value=${e}
        .disabled=${this.disabled}
        @change=${this._eventChanged}
      ></ha-textfield>
      <ha-yaml-editor
        .hass=${this.hass}
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.event.event_data")}
        .name=${"event_data"}
        .readOnly=${this.disabled}
        .defaultValue=${t}
        @value-changed=${this._dataChanged}
      ></ha-yaml-editor>
    `}},{kind:"method",key:"_dataChanged",value:function(e){e.stopPropagation(),e.detail.isValid&&(this._actionData=e.detail.value,ae(this,e))}},{kind:"method",key:"_eventChanged",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.action,event:e.target.value}})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-textfield {
        display: block;
      }
    `}}]}}),o.WF),(0,a.A)([(0,n.EM)("ha-automation-action-if")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_showElse",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{if:[],then:[]}}},{kind:"method",key:"render",value:function(){const e=this.action;return o.qy`
      <h3>
        ${this.hass.localize("ui.panel.config.automation.editor.actions.type.if.if")}*:
      </h3>
      <ha-automation-condition
        .conditions=${e.if}
        .disabled=${this.disabled}
        @value-changed=${this._ifChanged}
        .hass=${this.hass}
      ></ha-automation-condition>

      <h3>
        ${this.hass.localize("ui.panel.config.automation.editor.actions.type.if.then")}*:
      </h3>
      <ha-automation-action
        .actions=${e.then}
        .disabled=${this.disabled}
        @value-changed=${this._thenChanged}
        .hass=${this.hass}
      ></ha-automation-action>
      ${this._showElse||e.else?o.qy`
            <h3>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.if.else")}:
            </h3>
            <ha-automation-action
              .actions=${e.else||[]}
              .disabled=${this.disabled}
              @value-changed=${this._elseChanged}
              .hass=${this.hass}
            ></ha-automation-action>
          `:o.qy` <div class="link-button-row">
            <button
              class="link"
              @click=${this._addElse}
              .disabled=${this.disabled}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.if.add_else")}
            </button>
          </div>`}
    `}},{kind:"method",key:"_addElse",value:function(){this._showElse=!0}},{kind:"method",key:"_ifChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:{...this.action,if:t}})}},{kind:"method",key:"_thenChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:{...this.action,then:t}})}},{kind:"method",key:"_elseChanged",value:function(e){e.stopPropagation(),this._showElse=!0;const t=e.detail.value,i={...this.action,else:t};0===t.length&&delete i.else,(0,u.r)(this,"value-changed",{value:i})}},{kind:"get",static:!0,key:"styles",value:function(){return[S.RF,o.AH`
        .link-button-row {
          padding: 14px;
        }
      `]}}]}}),o.WF),(0,a.A)([(0,n.EM)("ha-automation-action-parallel")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{parallel:[]}}},{kind:"method",key:"render",value:function(){const e=this.action;return o.qy`
      <ha-automation-action
        .actions=${e.parallel}
        .disabled=${this.disabled}
        @value-changed=${this._actionsChanged}
        .hass=${this.hass}
      ></ha-automation-action>
    `}},{kind:"method",key:"_actionsChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:{...this.action,parallel:t}})}},{kind:"get",static:!0,key:"styles",value:function(){return S.RF}}]}}),o.WF);i(28957);(0,a.A)([(0,n.EM)("ha-automation-action-play_media")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{action:"media_player.play_media",target:{entity_id:""},data:{media_content_id:"",media_content_type:""},metadata:{}}}},{kind:"field",key:"_getSelectorValue",value(){return(0,s.A)((e=>({entity_id:e.target?.entity_id||e.entity_id,media_content_id:e.data?.media_content_id,media_content_type:e.data?.media_content_type,metadata:e.metadata})))}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-selector-media
        .hass=${this.hass}
        .disabled=${this.disabled}
        .value=${this._getSelectorValue(this.action)}
        @value-changed=${this._valueChanged}
      ></ha-selector-media>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.action,action:"media_player.play_media",target:{entity_id:e.detail.value.entity_id},data:{media_content_id:e.detail.value.media_content_id,media_content_type:e.detail.value.media_content_type},metadata:e.detail.value.metadata||{}}})}}]}}),o.WF);const j=["count","while","until","for_each"],Y=e=>j.find((t=>t in e));(0,a.A)([(0,n.EM)("ha-automation-action-repeat")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{repeat:{count:2,sequence:[]}}}},{kind:"field",key:"_schema",value(){return(0,s.A)(((e,t,i)=>[{name:"type",selector:{select:{mode:"dropdown",options:j.map((t=>({value:t,label:e(`ui.panel.config.automation.editor.actions.type.repeat.type.${t}.label`)})))}}},..."count"===t?[{name:"count",required:!0,selector:i?{template:{}}:{number:{mode:"box",min:1}}}]:[],..."until"===t||"while"===t?[{name:t,selector:{condition:{}}}]:[],..."for_each"===t?[{name:"for_each",required:!0,selector:{object:{}}}]:[],{name:"sequence",selector:{action:{}}}]))}},{kind:"method",key:"render",value:function(){const e=this.action.repeat,t=Y(e),i=this._schema(this.hass.localize,t??"count","count"in e&&"string"==typeof e.count&&(0,L.F)(e.count)),a={...e,type:t};return o.qy`<ha-form
      .hass=${this.hass}
      .data=${a}
      .schema=${i}
      .disabled=${this.disabled}
      @value-changed=${this._valueChanged}
      .computeLabel=${this._computeLabelCallback}
    ></ha-form>`}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value,i=t.type;delete t.type;i!==Y(this.action.repeat)&&("count"===i&&(t.count=2,delete t.while,delete t.until,delete t.for_each),"while"===i&&(t.while=t.until??[],delete t.count,delete t.until,delete t.for_each),"until"===i&&(t.until=t.while??[],delete t.count,delete t.while,delete t.for_each),"for_each"===i&&(t.for_each={},delete t.count,delete t.while,delete t.until)),(0,u.r)(this,"value-changed",{value:{...this.action,repeat:{...t}}})}},{kind:"get",static:!0,key:"styles",value:function(){return[S.RF,o.AH`
        ha-textfield {
          margin-top: 16px;
        }
      `]}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"type":return this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.type_select");case"count":return this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.type.count.label");case"while":return this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.type.while.conditions")+":";case"until":return this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.type.until.conditions")+":";case"for_each":return this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.type.for_each.items")+":";case"sequence":return this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.sequence")+":"}return""}}}]}}),o.WF),(0,a.A)([(0,n.EM)("ha-automation-action-sequence")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{sequence:[]}}},{kind:"method",key:"render",value:function(){const{action:e}=this;return o.qy`
      <ha-automation-action
        .actions=${e.sequence}
        .disabled=${this.disabled}
        @value-changed=${this._actionsChanged}
        .hass=${this.hass}
      ></ha-automation-action>
    `}},{kind:"method",key:"_actionsChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:{...this.action,sequence:t}})}},{kind:"get",static:!0,key:"styles",value:function(){return S.RF}}]}}),o.WF);var J=i(63428),Q=i(19263),X=i(59782);i(26862);(0,a.A)([(0,n.EM)("ha-automation-action-service")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_action",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_responseChecked",value(){return!1}},{kind:"field",key:"_fields",value(){return(0,s.A)(((e,t)=>{if(!t)return{fields:{}};const i=(0,Q.m)(t),a=(0,X.Y)(t);return i in e&&a in e[i]?{fields:e[i][a].fields}:{fields:{}}}))}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{action:"",data:{}}}},{kind:"method",key:"willUpdate",value:function(e){if(!e.has("action"))return;try{(0,J.vA)(this.action,d.BD)}catch(i){return void(0,u.r)(this,"ui-mode-not-available",i)}const t=this._fields(this.hass.services,this.action?.action).fields;this.action&&(Object.entries(this.action).some((([e,t])=>"data"!==e&&(0,L.r)(t)))||this.action.data&&Object.entries(this.action.data).some((([e,i])=>{const a=t[e];return(!a?.selector||!("template"in a.selector)&&!("object"in a.selector))&&(0,L.r)(i)})))?(0,u.r)(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.no_template_editor_support"))):this.action.entity_id?(this._action={...this.action,data:{...this.action.data,entity_id:this.action.entity_id}},delete this._action.entity_id):this._action=this.action}},{kind:"method",key:"render",value:function(){if(!this._action)return o.s6;const[e,t]=this._action.action?this._action.action.split(".",2):[void 0,void 0];return o.qy`
      <ha-service-control
        .narrow=${this.narrow}
        .hass=${this.hass}
        .value=${this._action}
        .disabled=${this.disabled}
        .showAdvanced=${this.hass.userData?.showAdvanced}
        .hidePicker=${!!this._action.metadata}
        @value-changed=${this._actionChanged}
      ></ha-service-control>
      ${e&&t&&this.hass.services[e]?.[t]?.response?o.qy`<ha-settings-row .narrow=${this.narrow}>
            ${this.hass.services[e][t].response.optional?o.qy`<ha-checkbox
                  .checked=${this._action.response_variable||this._responseChecked}
                  .disabled=${this.disabled}
                  @change=${this._responseCheckboxChanged}
                  slot="prefix"
                ></ha-checkbox>`:o.qy`<div slot="prefix" class="checkbox-spacer"></div>`}
            <span slot="heading"
              >${this.hass.localize("ui.panel.config.automation.editor.actions.type.service.response_variable")}</span
            >
            <span slot="description">
              ${this.hass.services[e][t].response.optional?this.hass.localize("ui.panel.config.automation.editor.actions.type.service.has_optional_response"):this.hass.localize("ui.panel.config.automation.editor.actions.type.service.has_response")}
            </span>
            <ha-textfield
              .value=${this._action.response_variable||""}
              .required=${!this.hass.services[e][t].response.optional}
              .disabled=${this.disabled||this.hass.services[e][t].response.optional&&!this._action.response_variable&&!this._responseChecked}
              @change=${this._responseVariableChanged}
            ></ha-textfield>
          </ha-settings-row>`:o.s6}
    `}},{kind:"method",key:"_actionChanged",value:function(e){e.detail.value===this._action&&e.stopPropagation();const t={...this.action,...e.detail.value};if("response_variable"in this.action){const[e,i]=this._action.action?this._action.action.split(".",2):[void 0,void 0];e&&i&&this.hass.services[e]?.[i]&&!("response"in this.hass.services[e][i])&&(delete t.response_variable,this._responseChecked=!1)}(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_responseVariableChanged",value:function(e){const t={...this.action,response_variable:e.target.value};e.target.value||delete t.response_variable,(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_responseCheckboxChanged",value:function(e){if(this._responseChecked=e.target.checked,!this._responseChecked){const e={...this.action};delete e.response_variable,(0,u.r)(this,"value-changed",{value:e})}}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-service-control {
        display: block;
        margin: 0 -16px;
      }
      ha-settings-row {
        margin: 0 -16px;
        padding: var(--service-control-padding, 0 16px);
      }
      ha-settings-row {
        --paper-time-input-justify-content: flex-end;
        --settings-row-content-width: 100%;
        --settings-row-prefix-display: contents;
        border-top: var(
          --service-control-items-border-top,
          1px solid var(--divider-color)
        );
      }
      ha-checkbox {
        margin-left: -16px;
        margin-inline-start: -16px;
        margin-inline-end: initial;
      }
      .checkbox-spacer {
        width: 32px;
      }
    `}}]}}),o.WF);const G=[{name:"set_conversation_response",selector:{template:{}}}];(0,a.A)([(0,n.EM)("ha-automation-action-set_conversation_response")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{set_conversation_response:""}}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-form
        .hass=${this.hass}
        .data=${this.action}
        .schema=${G}
        .disabled=${this.disabled}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"field",key:"_computeLabelCallback",value(){return()=>this.hass.localize("ui.panel.config.automation.editor.actions.type.set_conversation_response.label")}}]}}),o.WF);i(32694),i(99438);(0,a.A)([(0,n.EM)("ha-automation-action-stop")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{stop:""}}},{kind:"method",key:"render",value:function(){const{error:e,stop:t,response_variable:i}=this.action;return o.qy`
      <ha-textfield
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.stop.stop")}
        .value=${t}
        .disabled=${this.disabled}
        @change=${this._stopChanged}
      ></ha-textfield>
      <ha-textfield
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.stop.response_variable")}
        .value=${i||""}
        .disabled=${this.disabled}
        @change=${this._responseChanged}
      ></ha-textfield>
      <ha-formfield
        .disabled=${this.disabled}
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.stop.error")}
      >
        <ha-switch
          .disabled=${this.disabled}
          .checked=${e??!1}
          @change=${this._errorChanged}
        ></ha-switch>
      </ha-formfield>
    `}},{kind:"method",key:"_stopChanged",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.action,stop:e.target.value}})}},{kind:"method",key:"_responseChanged",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.action,response_variable:e.target.value}})}},{kind:"method",key:"_errorChanged",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.action,error:e.target.checked}})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-textfield {
        display: block;
        margin-bottom: 24px;
      }
    `}}]}}),o.WF);i(17417);(0,a.A)([(0,n.EM)("ha-automation-action-wait_for_trigger")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{wait_for_trigger:[]}}},{kind:"method",key:"render",value:function(){const e=(0,I.z)(this.action.timeout);return o.qy`
      <ha-duration-input
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.wait_for_trigger.timeout")}
        .data=${e}
        .disabled=${this.disabled}
        enableMillisecond
        @value-changed=${this._timeoutChanged}
      ></ha-duration-input>
      <ha-formfield
        .disabled=${this.disabled}
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.wait_for_trigger.continue_timeout")}
      >
        <ha-switch
          .checked=${this.action.continue_on_timeout??!0}
          .disabled=${this.disabled}
          @change=${this._continueChanged}
        ></ha-switch>
      </ha-formfield>
      <ha-automation-trigger
        .triggers=${(0,A.e)(this.action.wait_for_trigger)}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .name=${"wait_for_trigger"}
        @value-changed=${this._valueChanged}
      ></ha-automation-trigger>
    `}},{kind:"method",key:"_timeoutChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:{...this.action,timeout:t}})}},{kind:"method",key:"_continueChanged",value:function(e){(0,u.r)(this,"value-changed",{value:{...this.action,continue_on_timeout:e.target.checked}})}},{kind:"method",key:"_valueChanged",value:function(e){ae(this,e)}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-duration-input {
        display: block;
        margin-bottom: 24px;
      }
      ha-automation-trigger {
        display: block;
        margin-top: 24px;
      }
    `}}]}}),o.WF);const ee=[{name:"wait_template",selector:{template:{}}},{name:"timeout",required:!1,selector:{text:{}}},{name:"continue_on_timeout",selector:{boolean:{}}}];(0,a.A)([(0,n.EM)("ha-automation-action-wait_template")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{wait_template:"",continue_on_timeout:!0}}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-form
        .hass=${this.hass}
        .data=${this.action}
        .schema=${ee}
        .disabled=${this.disabled}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.actions.type.wait_template.${"continue_on_timeout"===e.name?"continue_timeout":e.name}`)}}]}}),o.WF);const te="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z",ie=e=>{if(e)return"action"in e||"scene"in e?(0,d.pq)(e):["and","or","not"].some((t=>t in e))?"condition":Object.keys(m.O$).find((t=>t in e))},ae=(e,t)=>{t.stopPropagation();const i=t.target?.name;if(!i)return;const a=t.detail?.value||t.target.value;if((e.action[i]||"")===a)return;let o;a?o={...e.action,[i]:a}:(o={...e.action},delete o[i]),(0,u.r)(e,"value-changed",{value:o})},oe=e=>e.preventDefault();(0,a.A)([(0,n.EM)("ha-automation-action-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"first",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"last",value:void 0},{kind:"field",decorators:[(0,h.I)({key:"automationClipboard",state:!1,subscribe:!0,storage:"sessionStorage"})],key:"_clipboard",value:void 0},{kind:"field",decorators:[(0,n.wk)(),(0,k.Fg)({context:w.ih,subscribe:!0})],key:"_entityReg",value:void 0},{kind:"field",decorators:[(0,n.wk)(),(0,k.Fg)({context:w.HD,subscribe:!0})],key:"_labelReg",value:void 0},{kind:"field",decorators:[(0,n.wk)(),(0,k.Fg)({context:w.rf,subscribe:!0})],key:"_floorReg",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_warnings",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_uiModeAvailable",value(){return!0}},{kind:"field",decorators:[(0,n.wk)()],key:"_yamlMode",value(){return!1}},{kind:"field",decorators:[(0,n.P)("ha-yaml-editor")],key:"_yamlEditor",value:void 0},{kind:"method",key:"willUpdate",value:function(e){if(!e.has("action"))return;const t=ie(this.action);this._uiModeAvailable=void 0!==t&&!m.ix.has(t),this._uiModeAvailable||this._yamlMode||(this._yamlMode=!0)}},{kind:"method",key:"updated",value:function(e){if(e.has("action")&&this._yamlMode){const e=this._yamlEditor;e&&e.value!==this.action&&e.setValue(this.action)}}},{kind:"method",key:"render",value:function(){if(!this.action)return o.s6;const e=ie(this.action),t=this._yamlMode;return o.qy`
      <ha-card outlined>
        ${!1===this.action.enabled?o.qy`
              <div class="disabled-bar">
                ${this.hass.localize("ui.panel.config.automation.editor.actions.disabled")}
              </div>
            `:o.s6}
        <ha-expansion-panel leftChevron>
          <h3 slot="header">
            ${"service"===e&&"action"in this.action&&this.action.action?o.qy`<ha-service-icon
                  class="action-icon"
                  .hass=${this.hass}
                  .service=${this.action.action}
                ></ha-service-icon>`:o.qy`<ha-svg-icon
                  class="action-icon"
                  .path=${m.O$[e]}
                ></ha-svg-icon>`}
            ${(0,b.Z)(B(this.hass,this._entityReg,this._labelReg,this._floorReg,this.action))}
          </h3>

          <slot name="icons" slot="icons"></slot>

          ${"condition"!==e&&!0===this.action.continue_on_error?o.qy`<div slot="icons">
                <ha-svg-icon .path=${"M18.75 22.16L16 19.16L17.16 18L18.75 19.59L22.34 16L23.5 17.41L18.75 22.16M13 13V7H11V13H13M13 17V15H11V17H13M12 2C17.5 2 22 6.5 22 12L21.91 13.31C21.31 13.11 20.67 13 20 13C16.69 13 14 15.69 14 19C14 19.95 14.22 20.85 14.62 21.65C13.78 21.88 12.91 22 12 22C6.5 22 2 17.5 2 12C2 6.5 6.5 2 12 2Z"}></ha-svg-icon>
                <simple-tooltip animation-delay="0">
                  ${this.hass.localize("ui.panel.config.automation.editor.actions.continue_on_error")}
                </simple-tooltip>
              </div> `:o.s6}

          <ha-button-menu
            slot="icons"
            @action=${this._handleAction}
            @click=${oe}
            @closed=${_.d}
            fixed
          >
            <ha-icon-button
              slot="trigger"
              .label=${this.hass.localize("ui.common.menu")}
              .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
            ></ha-icon-button>
            <mwc-list-item graphic="icon">
              ${this.hass.localize("ui.panel.config.automation.editor.actions.run")}
              <ha-svg-icon slot="graphic" .path=${"M8,5.14V19.14L19,12.14L8,5.14Z"}></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.rename")}
              <ha-svg-icon slot="graphic" .path=${"M18,17H10.5L12.5,15H18M6,17V14.5L13.88,6.65C14.07,6.45 14.39,6.45 14.59,6.65L16.35,8.41C16.55,8.61 16.55,8.92 16.35,9.12L8.47,17M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3Z"}></ha-svg-icon>
            </mwc-list-item>

            <li divider role="separator"></li>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.duplicate")}
              <ha-svg-icon
                slot="graphic"
                .path=${"M11,17H4A2,2 0 0,1 2,15V3A2,2 0 0,1 4,1H16V3H4V15H11V13L15,16L11,19V17M19,21V7H8V13H6V7A2,2 0 0,1 8,5H19A2,2 0 0,1 21,7V21A2,2 0 0,1 19,23H8A2,2 0 0,1 6,21V19H8V21H19Z"}
              ></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.triggers.copy")}
              <ha-svg-icon slot="graphic" .path=${"M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"}></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.triggers.cut")}
              <ha-svg-icon slot="graphic" .path=${"M19,3L13,9L15,11L22,4V3M12,12.5A0.5,0.5 0 0,1 11.5,12A0.5,0.5 0 0,1 12,11.5A0.5,0.5 0 0,1 12.5,12A0.5,0.5 0 0,1 12,12.5M6,20A2,2 0 0,1 4,18C4,16.89 4.9,16 6,16A2,2 0 0,1 8,18C8,19.11 7.1,20 6,20M6,8A2,2 0 0,1 4,6C4,4.89 4.9,4 6,4A2,2 0 0,1 8,6C8,7.11 7.1,8 6,8M9.64,7.64C9.87,7.14 10,6.59 10,6A4,4 0 0,0 6,2A4,4 0 0,0 2,6A4,4 0 0,0 6,10C6.59,10 7.14,9.87 7.64,9.64L10,12L7.64,14.36C7.14,14.13 6.59,14 6,14A4,4 0 0,0 2,18A4,4 0 0,0 6,22A4,4 0 0,0 10,18C10,17.41 9.87,16.86 9.64,16.36L12,14L19,21H22V20L9.64,7.64Z"}></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item
              graphic="icon"
              .disabled=${this.disabled||this.first}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.move_up")}
              <ha-svg-icon slot="graphic" .path=${"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"}></ha-svg-icon
            ></mwc-list-item>

            <mwc-list-item
              graphic="icon"
              .disabled=${this.disabled||this.last}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.move_down")}
              <ha-svg-icon slot="graphic" .path=${"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z"}></ha-svg-icon
            ></mwc-list-item>

            <li divider role="separator"></li>

            <mwc-list-item .disabled=${!this._uiModeAvailable} graphic="icon">
              ${this.hass.localize("ui.panel.config.automation.editor.edit_ui")}
              ${t?"":o.qy`<ha-svg-icon
                    class="selected_menu_item"
                    slot="graphic"
                    .path=${te}
                  ></ha-svg-icon>`}
            </mwc-list-item>

            <mwc-list-item .disabled=${!this._uiModeAvailable} graphic="icon">
              ${this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
              ${t?o.qy`<ha-svg-icon
                    class="selected_menu_item"
                    slot="graphic"
                    .path=${te}
                  ></ha-svg-icon>`:""}
            </mwc-list-item>

            <li divider role="separator"></li>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${!1===this.action.enabled?this.hass.localize("ui.panel.config.automation.editor.actions.enable"):this.hass.localize("ui.panel.config.automation.editor.actions.disable")}
              <ha-svg-icon
                slot="graphic"
                .path=${!1===this.action.enabled?"M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M10,16.5L16,12L10,7.5V16.5Z":"M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4M9,9V15H15V9"}
              ></ha-svg-icon>
            </mwc-list-item>
            <mwc-list-item
              class="warning"
              graphic="icon"
              .disabled=${this.disabled}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.actions.delete")}
              <ha-svg-icon
                class="warning"
                slot="graphic"
                .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
              ></ha-svg-icon>
            </mwc-list-item>
          </ha-button-menu>

          <div
            class=${(0,g.H)({"card-content":!0,disabled:!1===this.action.enabled})}
          >
            ${this._warnings?o.qy`<ha-alert
                  alert-type="warning"
                  .title=${this.hass.localize("ui.errors.config.editor_not_supported")}
                >
                  ${this._warnings.length>0&&void 0!==this._warnings[0]?o.qy` <ul>
                        ${this._warnings.map((e=>o.qy`<li>${e}</li>`))}
                      </ul>`:""}
                  ${this.hass.localize("ui.errors.config.edit_in_yaml_supported")}
                </ha-alert>`:""}
            ${t?o.qy`
                  ${void 0===e?o.qy`
                        ${this.hass.localize("ui.panel.config.automation.editor.actions.unsupported_action")}
                      `:""}
                  <ha-yaml-editor
                    .hass=${this.hass}
                    .defaultValue=${this.action}
                    .readOnly=${this.disabled}
                    @value-changed=${this._onYamlChange}
                  ></ha-yaml-editor>
                `:o.qy`
                  <div
                    @ui-mode-not-available=${this._handleUiModeNotAvailable}
                    @value-changed=${this._onUiChanged}
                  >
                    ${(0,y._)(`ha-automation-action-${e}`,{hass:this.hass,action:this.action,narrow:this.narrow,disabled:this.disabled})}
                  </div>
                `}
          </div>
        </ha-expansion-panel>
      </ha-card>
    `}},{kind:"method",key:"_handleUiModeNotAvailable",value:function(e){e.stopPropagation(),this._warnings=(0,$._)(this.hass,e.detail).warnings,this._yamlMode||(this._yamlMode=!0)}},{kind:"method",key:"_handleAction",value:async function(e){switch(e.detail.index){case 0:this._runAction();break;case 1:await this._renameAction();break;case 2:(0,u.r)(this,"duplicate");break;case 3:this._setClipboard();break;case 4:this._setClipboard(),(0,u.r)(this,"value-changed",{value:null});break;case 5:(0,u.r)(this,"move-up");break;case 6:(0,u.r)(this,"move-down");break;case 7:this._switchUiMode(),this.expand();break;case 8:this._switchYamlMode(),this.expand();break;case 9:this._onDisable();break;case 10:this._onDelete()}}},{kind:"method",key:"_setClipboard",value:function(){this._clipboard={...this._clipboard,action:(0,c.A)(this.action)}}},{kind:"method",key:"_onDisable",value:function(){const e=!(this.action.enabled??1),t={...this.action,enabled:e};(0,u.r)(this,"value-changed",{value:t}),this._yamlMode&&this._yamlEditor?.setValue(t)}},{kind:"method",key:"_runAction",value:async function(){const e=await(0,M.$)(this.hass,{actions:this.action});if(e.actions.valid){try{await(t=this.hass,i=this.action,t.callWS({type:"execute_script",sequence:i}))}catch(a){return void(0,D.K$)(this,{title:this.hass.localize("ui.panel.config.automation.editor.actions.run_action_error"),text:a.message||a})}var t,i;(0,O.P)(this,{message:this.hass.localize("ui.panel.config.automation.editor.actions.run_action_success")})}else(0,D.K$)(this,{title:this.hass.localize("ui.panel.config.automation.editor.actions.invalid_action"),text:e.actions.error})}},{kind:"method",key:"_onDelete",value:function(){(0,D.dk)(this,{title:this.hass.localize("ui.panel.config.automation.editor.actions.delete_confirm_title"),text:this.hass.localize("ui.panel.config.automation.editor.actions.delete_confirm_text"),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.delete"),destructive:!0,confirm:()=>{(0,u.r)(this,"value-changed",{value:null})}})}},{kind:"method",key:"_onYamlChange",value:function(e){e.stopPropagation(),e.detail.isValid&&(0,u.r)(this,"value-changed",{value:(0,d.Rn)(e.detail.value)})}},{kind:"method",key:"_onUiChanged",value:function(e){e.stopPropagation();const t={...this.action.alias?{alias:this.action.alias}:{},...e.detail.value};(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_switchUiMode",value:function(){this._warnings=void 0,this._yamlMode=!1}},{kind:"method",key:"_switchYamlMode",value:function(){this._warnings=void 0,this._yamlMode=!0}},{kind:"method",key:"_renameAction",value:async function(){const e=await(0,D.an)(this,{title:this.hass.localize("ui.panel.config.automation.editor.actions.change_alias"),inputLabel:this.hass.localize("ui.panel.config.automation.editor.actions.alias"),inputType:"string",placeholder:(0,b.Z)(B(this.hass,this._entityReg,this._labelReg,this._floorReg,this.action,void 0,!0)),defaultValue:this.action.alias,confirmText:this.hass.localize("ui.common.submit")});if(null!==e){const t={...this.action};""===e?delete t.alias:t.alias=e,(0,u.r)(this,"value-changed",{value:t}),this._yamlMode&&this._yamlEditor?.setValue(t)}}},{kind:"method",key:"expand",value:function(){this.updateComplete.then((()=>{this.shadowRoot.querySelector("ha-expansion-panel").expanded=!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[S.RF,o.AH`
        ha-button-menu,
        ha-icon-button {
          --mdc-theme-text-primary-on-background: var(--primary-text-color);
        }
        .disabled {
          opacity: 0.5;
          pointer-events: none;
        }
        ha-expansion-panel {
          --expansion-panel-summary-padding: 0 0 0 8px;
          --expansion-panel-content-padding: 0;
        }
        h3 {
          margin: 0;
          font-size: inherit;
          font-weight: inherit;
        }
        .action-icon {
          display: none;
        }
        @media (min-width: 870px) {
          .action-icon {
            display: inline-block;
            color: var(--secondary-text-color);
            opacity: 0.9;
            margin-right: 8px;
            margin-inline-end: 8px;
            margin-inline-start: initial;
          }
        }
        .card-content {
          padding: 16px;
        }
        .disabled-bar {
          background: var(--divider-color, #e0e0e0);
          text-align: center;
          border-top-right-radius: var(--ha-card-border-radius);
          border-top-left-radius: var(--ha-card-border-radius);
        }

        mwc-list-item[disabled] {
          --mdc-theme-text-primary-on-background: var(--disabled-text-color);
        }
        mwc-list-item.hidden {
          display: none;
        }
        .warning ul {
          margin: 4px 0;
        }
        .selected_menu_item {
          color: var(--primary-color);
        }
        li[role="separator"] {
          border-bottom-color: var(--divider-color);
        }
      `]}}]}}),o.WF);const ne="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z";(0,a.A)([(0,n.EM)("ha-automation-action")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"actions",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_showReorder",value(){return!1}},{kind:"field",decorators:[(0,h.I)({key:"automationClipboard",state:!0,subscribe:!0,storage:"sessionStorage"})],key:"_clipboard",value:void 0},{kind:"field",key:"_focusLastActionOnChange",value(){return!1}},{kind:"field",key:"_actionKeys",value(){return new WeakMap}},{kind:"field",key:"_unsubMql",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,l.A)(i,"connectedCallback",this,3)([]),this._unsubMql=(0,p.m)("(min-width: 600px)",(e=>{this._showReorder=e}))}},{kind:"method",key:"disconnectedCallback",value:function(){(0,l.A)(i,"disconnectedCallback",this,3)([]),this._unsubMql?.(),this._unsubMql=void 0}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-sortable
        handle-selector=".handle"
        draggable-selector="ha-automation-action-row"
        .disabled=${!this._showReorder||this.disabled}
        group="actions"
        invert-swap
        @item-moved=${this._actionMoved}
        @item-added=${this._actionAdded}
        @item-removed=${this._actionRemoved}
      >
        <div class="actions">
          ${(0,r.u)(this.actions,(e=>this._getKey(e)),((e,t)=>o.qy`
              <ha-automation-action-row
                .sortableData=${e}
                .index=${t}
                .first=${0===t}
                .last=${t===this.actions.length-1}
                .action=${e}
                .narrow=${this.narrow}
                .disabled=${this.disabled}
                @duplicate=${this._duplicateAction}
                @move-down=${this._moveDown}
                @move-up=${this._moveUp}
                @value-changed=${this._actionChanged}
                .hass=${this.hass}
              >
                ${this._showReorder&&!this.disabled?o.qy`
                      <div class="handle" slot="icons">
                        <ha-svg-icon .path=${"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"}></ha-svg-icon>
                      </div>
                    `:o.s6}
              </ha-automation-action-row>
            `))}
          <div class="buttons">
            <ha-button
              outlined
              .disabled=${this.disabled}
              .label=${this.hass.localize("ui.panel.config.automation.editor.actions.add")}
              @click=${this._addActionDialog}
            >
              <ha-svg-icon .path=${ne} slot="icon"></ha-svg-icon>
            </ha-button>
            <ha-button
              .disabled=${this.disabled}
              .label=${this.hass.localize("ui.panel.config.automation.editor.actions.add_building_block")}
              @click=${this._addActionBuildingBlockDialog}
            >
              <ha-svg-icon .path=${ne} slot="icon"></ha-svg-icon>
            </ha-button>
          </div>
        </div>
      </ha-sortable>
    `}},{kind:"method",key:"updated",value:function(e){if((0,l.A)(i,"updated",this,3)([e]),e.has("actions")&&this._focusLastActionOnChange){this._focusLastActionOnChange=!1;const e=this.shadowRoot.querySelector("ha-automation-action-row:last-of-type");e.updateComplete.then((()=>{e.expand(),e.scrollIntoView(),e.focus()}))}}},{kind:"method",key:"expandAll",value:function(){this.shadowRoot.querySelectorAll("ha-automation-action-row").forEach((e=>{e.expand()}))}},{kind:"method",key:"_addActionDialog",value:function(){(0,f.g)(this,{type:"action",add:this._addAction,clipboardItem:ie(this._clipboard?.action)})}},{kind:"method",key:"_addActionBuildingBlockDialog",value:function(){(0,f.g)(this,{type:"action",add:this._addAction,clipboardItem:ie(this._clipboard?.action),group:"building_blocks"})}},{kind:"field",key:"_addAction",value(){return e=>{let t;if(e===f.u)t=this.actions.concat((0,c.A)(this._clipboard.action));else if((0,m.kd)(e))t=this.actions.concat({action:(0,m.cQ)(e),metadata:{}});else{const i=customElements.get(`ha-automation-action-${e}`);t=this.actions.concat(i?{...i.defaultConfig}:{[e]:{}})}this._focusLastActionOnChange=!0,(0,u.r)(this,"value-changed",{value:t})}}},{kind:"method",key:"_getKey",value:function(e){return this._actionKeys.has(e)||this._actionKeys.set(e,Math.random().toString()),this._actionKeys.get(e)}},{kind:"method",key:"_moveUp",value:function(e){e.stopPropagation();const t=e.target.index,i=t-1;this._move(t,i)}},{kind:"method",key:"_moveDown",value:function(e){e.stopPropagation();const t=e.target.index,i=t+1;this._move(t,i)}},{kind:"method",key:"_move",value:function(e,t){const i=this.actions.concat(),a=i.splice(e,1)[0];i.splice(t,0,a),this.actions=i,(0,u.r)(this,"value-changed",{value:i})}},{kind:"method",key:"_actionMoved",value:function(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail;this._move(t,i)}},{kind:"method",key:"_actionAdded",value:async function(e){e.stopPropagation();const{index:t,data:i}=e.detail,a=[...this.actions.slice(0,t),i,...this.actions.slice(t)];this.actions=a,await(0,v.E)(),(0,u.r)(this,"value-changed",{value:this.actions})}},{kind:"method",key:"_actionRemoved",value:async function(e){e.stopPropagation();const{index:t}=e.detail,i=this.actions[t];this.actions=this.actions.filter((e=>e!==i)),await(0,v.E)();const a=this.actions.filter((e=>e!==i));(0,u.r)(this,"value-changed",{value:a})}},{kind:"method",key:"_actionChanged",value:function(e){e.stopPropagation();const t=[...this.actions],i=e.detail.value,a=e.target.index;if(null===i)t.splice(a,1);else{const e=this._getKey(t[a]);this._actionKeys.set(i,e),t[a]=i}(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_duplicateAction",value:function(e){e.stopPropagation();const t=e.target.index;(0,u.r)(this,"value-changed",{value:this.actions.concat((0,c.A)(this.actions[t]))})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      .actions {
        padding: 16px;
        margin: -16px;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      .sortable-ghost {
        background: none;
        border-radius: var(--ha-card-border-radius, 12px);
      }
      .sortable-drag {
        background: none;
      }
      ha-automation-action-row {
        display: block;
        scroll-margin-top: 48px;
      }
      ha-svg-icon {
        height: 20px;
      }
      .handle {
        padding: 12px;
        cursor: move; /* fallback if grab cursor is unsupported */
        cursor: grab;
      }
      .handle ha-svg-icon {
        pointer-events: none;
        height: 24px;
      }
      .buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        order: 1;
      }
    `}}]}}),o.WF);let se=(0,a.A)([(0,n.EM)("ha-selector-action")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",key:"_actions",value(){return(0,s.A)((e=>e?(0,d.Rn)(e):[]))}},{kind:"method",key:"render",value:function(){return o.qy`
      ${this.label?o.qy`<label>${this.label}</label>`:o.s6}
      <ha-automation-action
        .disabled=${this.disabled}
        .actions=${this._actions(this.value)}
        .hass=${this.hass}
      ></ha-automation-action>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-automation-action {
        display: block;
        margin-bottom: 16px;
      }
      label {
        display: block;
        margin-bottom: 4px;
        font-weight: 500;
      }
    `}}]}}),o.WF)},99438:(e,t,i)=>{var a=i(85461),o=i(69534),n=i(23605),s=i(18354),d=i(98597),l=i(196),c=i(97976);(0,a.A)([(0,l.EM)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"haptic",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){(0,o.A)(i,"firstUpdated",this,3)([]),this.addEventListener("change",(()=>{this.haptic&&(0,c.j)("light")}))}},{kind:"field",static:!0,key:"styles",value(){return[s.R,d.AH`
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
    `]}}]}}),n.U)},3820:(e,t,i)=>{i.d(t,{O$:()=>a,_c:()=>n,cQ:()=>l,ix:()=>o,kd:()=>d,ts:()=>s});const a={condition:"M4 2A2 2 0 0 0 2 4V12H4V8H6V12H8V4A2 2 0 0 0 6 2H4M4 4H6V6H4M22 15.5V14A2 2 0 0 0 20 12H16V22H20A2 2 0 0 0 22 20V18.5A1.54 1.54 0 0 0 20.5 17A1.54 1.54 0 0 0 22 15.5M20 20H18V18H20V20M20 16H18V14H20M5.79 21.61L4.21 20.39L18.21 2.39L19.79 3.61Z",delay:"M12,20A7,7 0 0,1 5,13A7,7 0 0,1 12,6A7,7 0 0,1 19,13A7,7 0 0,1 12,20M19.03,7.39L20.45,5.97C20,5.46 19.55,5 19.04,4.56L17.62,6C16.07,4.74 14.12,4 12,4A9,9 0 0,0 3,13A9,9 0 0,0 12,22C17,22 21,17.97 21,13C21,10.88 20.26,8.93 19.03,7.39M11,14H13V8H11M15,1H9V3H15V1Z",event:"M10,9A1,1 0 0,1 11,8A1,1 0 0,1 12,9V13.47L13.21,13.6L18.15,15.79C18.68,16.03 19,16.56 19,17.14V21.5C18.97,22.32 18.32,22.97 17.5,23H11C10.62,23 10.26,22.85 10,22.57L5.1,18.37L5.84,17.6C6.03,17.39 6.3,17.28 6.58,17.28H6.8L10,19V9M11,5A4,4 0 0,1 15,9C15,10.5 14.2,11.77 13,12.46V11.24C13.61,10.69 14,9.89 14,9A3,3 0 0,0 11,6A3,3 0 0,0 8,9C8,9.89 8.39,10.69 9,11.24V12.46C7.8,11.77 7,10.5 7,9A4,4 0 0,1 11,5M11,3A6,6 0 0,1 17,9C17,10.7 16.29,12.23 15.16,13.33L14.16,12.88C15.28,11.96 16,10.56 16,9A5,5 0 0,0 11,4A5,5 0 0,0 6,9C6,11.05 7.23,12.81 9,13.58V14.66C6.67,13.83 5,11.61 5,9A6,6 0 0,1 11,3Z",play_media:"M8,5.14V19.14L19,12.14L8,5.14Z",activate_scene:"M17.5,12A1.5,1.5 0 0,1 16,10.5A1.5,1.5 0 0,1 17.5,9A1.5,1.5 0 0,1 19,10.5A1.5,1.5 0 0,1 17.5,12M14.5,8A1.5,1.5 0 0,1 13,6.5A1.5,1.5 0 0,1 14.5,5A1.5,1.5 0 0,1 16,6.5A1.5,1.5 0 0,1 14.5,8M9.5,8A1.5,1.5 0 0,1 8,6.5A1.5,1.5 0 0,1 9.5,5A1.5,1.5 0 0,1 11,6.5A1.5,1.5 0 0,1 9.5,8M6.5,12A1.5,1.5 0 0,1 5,10.5A1.5,1.5 0 0,1 6.5,9A1.5,1.5 0 0,1 8,10.5A1.5,1.5 0 0,1 6.5,12M12,3A9,9 0 0,0 3,12A9,9 0 0,0 12,21A1.5,1.5 0 0,0 13.5,19.5C13.5,19.11 13.35,18.76 13.11,18.5C12.88,18.23 12.73,17.88 12.73,17.5A1.5,1.5 0 0,1 14.23,16H16A5,5 0 0,0 21,11C21,6.58 16.97,3 12,3Z",service:"M12,5A2,2 0 0,1 14,7C14,7.24 13.96,7.47 13.88,7.69C17.95,8.5 21,11.91 21,16H3C3,11.91 6.05,8.5 10.12,7.69C10.04,7.47 10,7.24 10,7A2,2 0 0,1 12,5M22,19H2V17H22V19Z",wait_template:"M8,3A2,2 0 0,0 6,5V9A2,2 0 0,1 4,11H3V13H4A2,2 0 0,1 6,15V19A2,2 0 0,0 8,21H10V19H8V14A2,2 0 0,0 6,12A2,2 0 0,0 8,10V5H10V3M16,3A2,2 0 0,1 18,5V9A2,2 0 0,0 20,11H21V13H20A2,2 0 0,0 18,15V19A2,2 0 0,1 16,21H14V19H16V14A2,2 0 0,1 18,12A2,2 0 0,1 16,10V5H14V3H16Z",wait_for_trigger:"M12,9A2,2 0 0,1 10,7C10,5.89 10.9,5 12,5C13.11,5 14,5.89 14,7A2,2 0 0,1 12,9M12,14A2,2 0 0,1 10,12C10,10.89 10.9,10 12,10C13.11,10 14,10.89 14,12A2,2 0 0,1 12,14M12,19A2,2 0 0,1 10,17C10,15.89 10.9,15 12,15C13.11,15 14,15.89 14,17A2,2 0 0,1 12,19M20,10H17V8.86C18.72,8.41 20,6.86 20,5H17V4A1,1 0 0,0 16,3H8A1,1 0 0,0 7,4V5H4C4,6.86 5.28,8.41 7,8.86V10H4C4,11.86 5.28,13.41 7,13.86V15H4C4,16.86 5.28,18.41 7,18.86V20A1,1 0 0,0 8,21H16A1,1 0 0,0 17,20V18.86C18.72,18.41 20,16.86 20,15H17V13.86C18.72,13.41 20,11.86 20,10Z",repeat:"M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z",choose:"M11,5H8L12,1L16,5H13V9.43C12.25,9.89 11.58,10.46 11,11.12V5M22,11L18,7V10C14.39,9.85 11.31,12.57 11,16.17C9.44,16.72 8.62,18.44 9.17,20C9.72,21.56 11.44,22.38 13,21.83C14.56,21.27 15.38,19.56 14.83,18C14.53,17.14 13.85,16.47 13,16.17C13.47,12.17 17.47,11.97 17.95,11.97V14.97L22,11M10.63,11.59C9.3,10.57 7.67,10 6,10V7L2,11L6,15V12C7.34,12.03 8.63,12.5 9.64,13.4C9.89,12.76 10.22,12.15 10.63,11.59Z",if:"M14,4L16.29,6.29L13.41,9.17L14.83,10.59L17.71,7.71L20,10V4M10,4H4V10L6.29,7.71L11,12.41V20H13V11.59L7.71,6.29",device_id:"M3 6H21V4H3C1.9 4 1 4.9 1 6V18C1 19.1 1.9 20 3 20H7V18H3V6M13 12H9V13.78C8.39 14.33 8 15.11 8 16C8 16.89 8.39 17.67 9 18.22V20H13V18.22C13.61 17.67 14 16.88 14 16S13.61 14.33 13 13.78V12M11 17.5C10.17 17.5 9.5 16.83 9.5 16S10.17 14.5 11 14.5 12.5 15.17 12.5 16 11.83 17.5 11 17.5M22 8H16C15.5 8 15 8.5 15 9V19C15 19.5 15.5 20 16 20H22C22.5 20 23 19.5 23 19V9C23 8.5 22.5 8 22 8M21 18H17V10H21V18Z",stop:"M13 24C9.74 24 6.81 22 5.6 19L2.57 11.37C2.26 10.58 3 9.79 3.81 10.05L4.6 10.31C5.16 10.5 5.62 10.92 5.84 11.47L7.25 15H8V3.25C8 2.56 8.56 2 9.25 2S10.5 2.56 10.5 3.25V12H11.5V1.25C11.5 .56 12.06 0 12.75 0S14 .56 14 1.25V12H15V2.75C15 2.06 15.56 1.5 16.25 1.5C16.94 1.5 17.5 2.06 17.5 2.75V12H18.5V5.75C18.5 5.06 19.06 4.5 19.75 4.5S21 5.06 21 5.75V16C21 20.42 17.42 24 13 24Z",sequence:"M7,13V11H21V13H7M7,19V17H21V19H7M7,7V5H21V7H7M3,8V5H2V4H4V8H3M2,17V16H5V20H2V19H4V18.5H3V17.5H4V17H2M4.25,10A0.75,0.75 0 0,1 5,10.75C5,10.95 4.92,11.14 4.79,11.27L3.12,13H5V14H2V13.08L4,11H2V10H4.25Z",parallel:"M16,4.5V7H5V9H16V11.5L19.5,8M16,12.5V15H5V17H16V19.5L19.5,16",variables:"M21 2H3C1.9 2 1 2.9 1 4V20C1 21.1 1.9 22 3 22H21C22.1 22 23 21.1 23 20V4C23 2.9 22.1 2 21 2M21 20H3V6H21V20M16.6 8C18.1 9.3 19 11.1 19 13C19 14.9 18.1 16.7 16.6 18L15 17.4C16.3 16.4 17 14.7 17 13S16.3 9.6 15 8.6L16.6 8M7.4 8L9 8.6C7.7 9.6 7 11.3 7 13S7.7 16.4 9 17.4L7.4 18C5.9 16.7 5 14.9 5 13S5.9 9.3 7.4 8M12.1 12L13.5 10H15L12.8 13L14.1 16H12.8L12 14L10.6 16H9L11.3 12.9L10 10H11.3L12.1 12Z",set_conversation_response:"M12,8H4A2,2 0 0,0 2,10V14A2,2 0 0,0 4,16H5V20A1,1 0 0,0 6,21H8A1,1 0 0,0 9,20V16H12L17,20V4L12,8M21.5,12C21.5,13.71 20.54,15.26 19,16V8C20.53,8.75 21.5,10.3 21.5,12Z"},o=new Set(["variables"]),n={device_id:{},helpers:{icon:"M21.71 20.29L20.29 21.71A1 1 0 0 1 18.88 21.71L7 9.85A3.81 3.81 0 0 1 6 10A4 4 0 0 1 2.22 4.7L4.76 7.24L5.29 6.71L6.71 5.29L7.24 4.76L4.7 2.22A4 4 0 0 1 10 6A3.81 3.81 0 0 1 9.85 7L21.71 18.88A1 1 0 0 1 21.71 20.29M2.29 18.88A1 1 0 0 0 2.29 20.29L3.71 21.71A1 1 0 0 0 5.12 21.71L10.59 16.25L7.76 13.42M20 2L16 4V6L13.83 8.17L15.83 10.17L18 8H20L22 4Z",members:{}},building_blocks:{icon:"M18.5 18.5C19.04 18.5 19.5 18.96 19.5 19.5S19.04 20.5 18.5 20.5H6.5C5.96 20.5 5.5 20.04 5.5 19.5S5.96 18.5 6.5 18.5H18.5M18.5 17H6.5C5.13 17 4 18.13 4 19.5S5.13 22 6.5 22H18.5C19.88 22 21 20.88 21 19.5S19.88 17 18.5 17M21 11H18V7H13L10 11V16H22L21 11M11.54 11L13.5 8.5H16V11H11.54M9.76 3.41L4.76 2L2 11.83C1.66 13.11 2.41 14.44 3.7 14.8L4.86 15.12L8.15 12.29L4.27 11.21L6.15 4.46L8.94 5.24C9.5 5.53 10.71 6.34 11.47 7.37L12.5 6H12.94C11.68 4.41 9.85 3.46 9.76 3.41Z",members:{condition:{},delay:{},wait_template:{},wait_for_trigger:{},repeat:{},choose:{},if:{},stop:{},sequence:{},parallel:{},variables:{}}},other:{icon:"M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M10,12A2,2 0 0,1 12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12M4,12A2,2 0 0,1 6,10A2,2 0 0,1 8,12A2,2 0 0,1 6,14A2,2 0 0,1 4,12Z",members:{event:{},service:{},set_conversation_response:{}}}},s="__SERVICE__",d=e=>e?.startsWith(s),l=e=>e.substring(s.length)},97976:(e,t,i)=>{i.d(t,{j:()=>o});var a=i(33167);const o=e=>{(0,a.r)(window,"haptic",e)}}};
//# sourceMappingURL=rV60lATY.js.map