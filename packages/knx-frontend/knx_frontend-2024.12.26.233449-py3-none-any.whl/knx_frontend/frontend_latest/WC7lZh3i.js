export const id=6249;export const ids=[6249];export const modules={68873:(e,t,i)=>{i.d(t,{a:()=>o});var r=i(6601),a=i(19263);function o(e,t){const i=(0,a.m)(e.entity_id),o=void 0!==t?t:e?.state;if(["button","event","input_button","scene"].includes(i))return o!==r.Hh;if((0,r.g0)(o))return!1;if(o===r.KF&&"alert"!==i)return!1;switch(i){case"alarm_control_panel":return"disarmed"!==o;case"alert":return"idle"!==o;case"cover":case"valve":return"closed"!==o;case"device_tracker":case"person":return"not_home"!==o;case"lawn_mower":return["mowing","error"].includes(o);case"lock":return"locked"!==o;case"media_player":return"standby"!==o;case"vacuum":return!["idle","docked","paused"].includes(o);case"plant":return"problem"===o;case"group":return["on","home","open","locked","problem"].includes(o);case"timer":return"active"===o;case"camera":return"streaming"===o}return!0}},86935:(e,t,i)=>{i.d(t,{mT:()=>u,Se:()=>l});var r=i(6601),a=i(19263);var o=i(94848);var s=i(68873);const n=new Set(["alarm_control_panel","alert","automation","binary_sensor","calendar","camera","climate","cover","device_tracker","fan","group","humidifier","input_boolean","lawn_mower","light","lock","media_player","person","plant","remote","schedule","script","siren","sun","switch","timer","update","vacuum","valve","water_heater"]),l=(e,t)=>{if((void 0!==t?t:e?.state)===r.Hh)return"var(--state-unavailable-color)";const i=c(e,t);return i?(a=i,Array.isArray(a)?a.reverse().reduce(((e,t)=>`var(${t}${e?`, ${e}`:""})`),void 0):`var(${a})`):void 0;var a},d=(e,t,i)=>{const r=void 0!==i?i:t.state,a=(0,s.a)(t,i),n=[],l=(0,o.Y)(r,"_"),d=a?"active":"inactive",c=t.attributes.device_class;return c&&n.push(`--state-${e}-${c}-${l}-color`),n.push(`--state-${e}-${l}-color`,`--state-${e}-${d}-color`,`--state-${d}-color`),n},c=(e,t)=>{const i=void 0!==t?t:e?.state,r=(0,a.m)(e.entity_id),o=e.attributes.device_class;if("sensor"===r&&"battery"===o){const e=(e=>{const t=Number(e);if(!isNaN(t))return t>=70?"--state-sensor-battery-high-color":t>=30?"--state-sensor-battery-medium-color":"--state-sensor-battery-low-color"})(i);if(e)return[e]}if("group"===r){const i=(e=>{const t=e.attributes.entity_id||[],i=[...new Set(t.map((e=>(0,a.m)(e))))];return 1===i.length?i[0]:void 0})(e);if(i&&n.has(i))return d(i,e,t)}if(n.has(r))return d(r,e,t)},u=e=>{if(e.attributes.brightness&&"plant"!==(0,a.m)(e.entity_id)){return`brightness(${(e.attributes.brightness+245)/5}%)`}return""}},17963:(e,t,i)=>{i.d(t,{ZV:()=>a});var r=i(76415);const a=(e,t,i)=>{const a=t?(e=>{switch(e.number_format){case r.jG.comma_decimal:return["en-US","en"];case r.jG.decimal_comma:return["de","es","it"];case r.jG.space_comma:return["fr","sv","cs"];case r.jG.system:return;default:return e.language}})(t):void 0;return Number.isNaN=Number.isNaN||function e(t){return"number"==typeof t&&e(t)},t?.number_format===r.jG.none||Number.isNaN(Number(e))?Number.isNaN(Number(e))||""===e||t?.number_format!==r.jG.none?"string"==typeof e?e:`${((e,t=2)=>Math.round(e*10**t)/10**t)(e,i?.maximumFractionDigits).toString()}${"currency"===i?.style?` ${i.currency}`:""}`:new Intl.NumberFormat("en-US",o(e,{...i,useGrouping:!1})).format(Number(e)):new Intl.NumberFormat(a,o(e,i)).format(Number(e))},o=(e,t)=>{const i={maximumFractionDigits:2,...t};if("string"!=typeof e)return i;if(!t||void 0===t.minimumFractionDigits&&void 0===t.maximumFractionDigits){const t=e.indexOf(".")>-1?e.split(".")[1].length:0;i.minimumFractionDigits=t,i.maximumFractionDigits=t}return i}},94848:(e,t,i)=>{i.d(t,{Y:()=>r});const r=(e,t="_")=>{const i="àáâäæãåāăąçćčđďèéêëēėęěğǵḧîïíīįìıİłḿñńǹňôöòóœøōõőṕŕřßśšşșťțûüùúūǘůűųẃẍÿýžźż·",r=`aaaaaaaaaacccddeeeeeeeegghiiiiiiiilmnnnnoooooooooprrsssssttuuuuuuuuuwxyyzzz${t}`,a=new RegExp(i.split("").join("|"),"g");let o;return""===e?o="":(o=e.toString().toLowerCase().replace(a,(e=>r.charAt(i.indexOf(e)))).replace(/(\d),(?=\d)/g,"$1").replace(/[^a-z0-9]+/g,t).replace(new RegExp(`(${t})\\1+`,"g"),"$1").replace(new RegExp(`^${t}+`),"").replace(new RegExp(`${t}+$`),""),""===o&&(o="unknown")),o}},80106:(e,t,i)=>{i.d(t,{d:()=>r});const r=e=>{switch(e.language){case"cz":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},16249:(e,t,i)=>{i.r(t),i.d(t,{HaColorTempSelector:()=>z});var r=i(85461),a=i(98597),o=i(196),s=i(12506),n=i(45081),l=i(33167);i(43689),i(53335);(0,r.A)([(0,o.EM)("ha-labeled-slider")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"labeled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)()],key:"caption",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"min",value(){return 0}},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"max",value(){return 100}},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"step",value(){return 1}},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"extra",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)()],key:"icon",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"value",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`
      <div class="title">${this._getTitle()}</div>
      <div class="extra-container"><slot name="extra"></slot></div>
      <div class="slider-container">
        ${this.icon?a.qy`<ha-icon icon=${this.icon}></ha-icon>`:a.s6}
        <ha-slider
          .min=${this.min}
          .max=${this.max}
          .step=${this.step}
          .labeled=${this.labeled}
          .disabled=${this.disabled}
          .value=${this.value}
          @change=${this._inputChanged}
        ></ha-slider>
      </div>
      ${this.helper?a.qy`<ha-input-helper-text> ${this.helper} </ha-input-helper-text>`:a.s6}
    `}},{kind:"method",key:"_getTitle",value:function(){return`${this.caption}${this.caption&&this.required?" *":""}`}},{kind:"method",key:"_inputChanged",value:function(e){(0,l.r)(this,"value-changed",{value:Number(e.target.value)})}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host {
        display: block;
      }

      .title {
        margin: 5px 0 8px;
        color: var(--primary-text-color);
      }

      .slider-container {
        display: flex;
      }

      ha-icon {
        margin-top: 8px;
        color: var(--secondary-text-color);
      }

      ha-slider {
        flex-grow: 1;
        background-image: var(--ha-slider-background);
        border-radius: 4px;
      }
    `}}]}}),a.WF);var d=i(69534),c=i(26709);const u=(e,t,i)=>Math.min(Math.max(e,t),i),h=2700,m=6500,v=e=>{const t=e/100;return[p(t),k(t),g(t)]},p=e=>{if(e<=66)return 255;return u(329.698727446*(e-60)**-.1332047592,0,255)},k=e=>{let t;return t=e<=66?99.4708025861*Math.log(e)-161.1195681661:288.1221695283*(e-60)**-.0755148492,u(t,0,255)},g=e=>{if(e>=66)return 255;if(e<=19)return 0;const t=138.5177312231*Math.log(e-10)-305.0447927307;return u(t,0,255)},b=e=>Math.floor(1e6/e);var f=i(86935),y=i(50036),_=i(9540),w=i(69760),x=i(17963),$=i(80106);const M=new Set(["ArrowRight","ArrowUp","ArrowLeft","ArrowDown","PageUp","PageDown","Home","End"]);(0,r.A)([(0,o.EM)("ha-control-slider")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"locale",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)()],key:"mode",value(){return"start"}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,reflect:!0})],key:"vertical",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,attribute:"show-handle"})],key:"showHandle",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,attribute:"inverted"})],key:"inverted",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({attribute:"tooltip-position"})],key:"tooltipPosition",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"unit",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:"tooltip-mode"})],key:"tooltipMode",value(){return"interaction"}},{kind:"field",decorators:[(0,o.MZ)({attribute:"touch-action"})],key:"touchAction",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"step",value(){return 1}},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"min",value(){return 0}},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"max",value(){return 100}},{kind:"field",decorators:[(0,o.wk)()],key:"pressed",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"tooltipVisible",value(){return!1}},{kind:"field",key:"_mc",value:void 0},{kind:"method",key:"valueToPercentage",value:function(e){const t=(this.boundedValue(e)-this.min)/(this.max-this.min);return this.inverted?1-t:t}},{kind:"method",key:"percentageToValue",value:function(e){return(this.max-this.min)*(this.inverted?1-e:e)+this.min}},{kind:"method",key:"steppedValue",value:function(e){return Math.round(e/this.step)*this.step}},{kind:"method",key:"boundedValue",value:function(e){return Math.min(Math.max(e,this.min),this.max)}},{kind:"method",key:"firstUpdated",value:function(e){(0,d.A)(i,"firstUpdated",this,3)([e]),this.setupListeners(),this.setAttribute("role","slider"),this.hasAttribute("tabindex")||this.setAttribute("tabindex","0")}},{kind:"method",key:"updated",value:function(e){if((0,d.A)(i,"updated",this,3)([e]),e.has("value")){const e=this.steppedValue(this.value??0);this.setAttribute("aria-valuenow",e.toString()),this.setAttribute("aria-valuetext",this._formatValue(e))}if(e.has("min")&&this.setAttribute("aria-valuemin",this.min.toString()),e.has("max")&&this.setAttribute("aria-valuemax",this.max.toString()),e.has("vertical")){const e=this.vertical?"vertical":"horizontal";this.setAttribute("aria-orientation",e)}}},{kind:"method",key:"connectedCallback",value:function(){(0,d.A)(i,"connectedCallback",this,3)([]),this.setupListeners()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,d.A)(i,"disconnectedCallback",this,3)([]),this.destroyListeners()}},{kind:"field",decorators:[(0,o.P)("#slider")],key:"slider",value:void 0},{kind:"method",key:"setupListeners",value:function(){if(this.slider&&!this._mc){let e;this._mc=new _.mS(this.slider,{touchAction:this.touchAction??(this.vertical?"pan-x":"pan-y")}),this._mc.add(new _.uq({threshold:10,direction:_.ge,enable:!0})),this._mc.add(new _.Cx({event:"singletap"})),this._mc.on("panstart",(()=>{this.disabled||(this.pressed=!0,this._showTooltip(),e=this.value)})),this._mc.on("pancancel",(()=>{this.disabled||(this.pressed=!1,this._hideTooltip(),this.value=e)})),this._mc.on("panmove",(e=>{if(this.disabled)return;const t=this._getPercentageFromEvent(e);this.value=this.percentageToValue(t);const i=this.steppedValue(this.value);(0,l.r)(this,"slider-moved",{value:i})})),this._mc.on("panend",(e=>{if(this.disabled)return;this.pressed=!1,this._hideTooltip();const t=this._getPercentageFromEvent(e);this.value=this.steppedValue(this.percentageToValue(t)),(0,l.r)(this,"slider-moved",{value:void 0}),(0,l.r)(this,"value-changed",{value:this.value})})),this._mc.on("singletap",(e=>{if(this.disabled)return;const t=this._getPercentageFromEvent(e);this.value=this.steppedValue(this.percentageToValue(t)),(0,l.r)(this,"value-changed",{value:this.value})})),this.addEventListener("keydown",this._handleKeyDown),this.addEventListener("keyup",this._handleKeyUp)}}},{kind:"method",key:"destroyListeners",value:function(){this._mc&&(this._mc.destroy(),this._mc=void 0),this.removeEventListener("keydown",this._handleKeyDown),this.removeEventListener("keyup",this._handleKeyUp)}},{kind:"get",key:"_tenPercentStep",value:function(){return Math.max(this.step,(this.max-this.min)/10)}},{kind:"method",key:"_showTooltip",value:function(){null!=this._tooltipTimeout&&window.clearTimeout(this._tooltipTimeout),this.tooltipVisible=!0}},{kind:"method",key:"_hideTooltip",value:function(e){e?this._tooltipTimeout=window.setTimeout((()=>{this.tooltipVisible=!1}),e):this.tooltipVisible=!1}},{kind:"method",key:"_handleKeyDown",value:function(e){if(M.has(e.code)){switch(e.preventDefault(),e.code){case"ArrowRight":case"ArrowUp":this.value=this.boundedValue((this.value??0)+this.step);break;case"ArrowLeft":case"ArrowDown":this.value=this.boundedValue((this.value??0)-this.step);break;case"PageUp":this.value=this.steppedValue(this.boundedValue((this.value??0)+this._tenPercentStep));break;case"PageDown":this.value=this.steppedValue(this.boundedValue((this.value??0)-this._tenPercentStep));break;case"Home":this.value=this.min;break;case"End":this.value=this.max}this._showTooltip(),(0,l.r)(this,"slider-moved",{value:this.value})}}},{kind:"field",key:"_tooltipTimeout",value:void 0},{kind:"method",key:"_handleKeyUp",value:function(e){M.has(e.code)&&(e.preventDefault(),this._hideTooltip(500),(0,l.r)(this,"value-changed",{value:this.value}))}},{kind:"field",key:"_getPercentageFromEvent",value(){return e=>{if(this.vertical){const t=e.center.y,i=e.target.getBoundingClientRect().top,r=e.target.clientHeight;return Math.max(Math.min(1,1-(t-i)/r),0)}const t=e.center.x,i=e.target.getBoundingClientRect().left,r=e.target.clientWidth;return Math.max(Math.min(1,(t-i)/r),0)}}},{kind:"method",key:"_formatValue",value:function(e){var t,i;return`${(0,x.ZV)(e,this.locale)}${this.unit?`${t=this.unit,i=this.locale,"°"===t?"":i&&"%"===t?(0,$.d)(i):" "}${this.unit}`:""}`}},{kind:"method",key:"_renderTooltip",value:function(){if("never"===this.tooltipMode)return a.s6;const e=this.tooltipPosition??(this.vertical?"left":"top"),t="always"===this.tooltipMode||this.tooltipVisible&&"interaction"===this.tooltipMode,i=this.steppedValue(this.value??0);return a.qy`
      <span
        aria-hidden="true"
        class="tooltip ${(0,w.H)({visible:t,[e]:!0,[this.mode??"start"]:!0,"show-handle":this.showHandle})}"
      >
        ${this._formatValue(i)}
      </span>
    `}},{kind:"method",key:"render",value:function(){return a.qy`
      <div
        class="container${(0,w.H)({pressed:this.pressed})}"
        style=${(0,s.W)({"--value":`${this.valueToPercentage(this.value??0)}`})}
      >
        <div id="slider" class="slider">
          <div class="slider-track-background"></div>
          <slot name="background"></slot>
          ${"cursor"===this.mode?null!=this.value?a.qy`
                  <div
                    class=${(0,w.H)({"slider-track-cursor":!0})}
                  ></div>
                `:null:a.qy`
                <div
                  class=${(0,w.H)({"slider-track-bar":!0,[this.mode??"start"]:!0,"show-handle":this.showHandle})}
                ></div>
              `}
        </div>
        ${this._renderTooltip()}
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host {
        display: block;
        --control-slider-color: var(--primary-color);
        --control-slider-background: var(--disabled-color);
        --control-slider-background-opacity: 0.2;
        --control-slider-thickness: 40px;
        --control-slider-border-radius: 10px;
        --control-slider-tooltip-font-size: 14px;
        height: var(--control-slider-thickness);
        width: 100%;
        border-radius: var(--control-slider-border-radius);
        outline: none;
        transition: box-shadow 180ms ease-in-out;
      }
      :host(:focus-visible) {
        box-shadow: 0 0 0 2px var(--control-slider-color);
      }
      :host([vertical]) {
        width: var(--control-slider-thickness);
        height: 100%;
      }
      .container {
        position: relative;
        height: 100%;
        width: 100%;
        --handle-size: 4px;
        --handle-margin: calc(var(--control-slider-thickness) / 8);
      }
      .tooltip {
        pointer-events: none;
        user-select: none;
        position: absolute;
        background-color: var(--clear-background-color);
        color: var(--primary-text-color);
        font-size: var(--control-slider-tooltip-font-size);
        border-radius: 0.8em;
        padding: 0.2em 0.4em;
        opacity: 0;
        white-space: nowrap;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        transition:
          opacity 180ms ease-in-out,
          left 180ms ease-in-out,
          bottom 180ms ease-in-out;
        --handle-spacing: calc(2 * var(--handle-margin) + var(--handle-size));
        --slider-tooltip-margin: -4px;
        --slider-tooltip-range: 100%;
        --slider-tooltip-offset: 0px;
        --slider-tooltip-position: calc(
          min(
            max(
              var(--value) * var(--slider-tooltip-range) +
                var(--slider-tooltip-offset),
              0%
            ),
            100%
          )
        );
      }
      .tooltip.start {
        --slider-tooltip-offset: calc(-0.5 * (var(--handle-spacing)));
      }
      .tooltip.end {
        --slider-tooltip-offset: calc(0.5 * (var(--handle-spacing)));
      }
      .tooltip.cursor {
        --slider-tooltip-range: calc(100% - var(--handle-spacing));
        --slider-tooltip-offset: calc(0.5 * (var(--handle-spacing)));
      }
      .tooltip.show-handle {
        --slider-tooltip-range: calc(100% - var(--handle-spacing));
        --slider-tooltip-offset: calc(0.5 * (var(--handle-spacing)));
      }
      .tooltip.visible {
        opacity: 1;
      }
      .tooltip.top {
        transform: translate3d(-50%, -100%, 0);
        top: var(--slider-tooltip-margin);
        left: 50%;
      }
      .tooltip.bottom {
        transform: translate3d(-50%, 100%, 0);
        bottom: var(--slider-tooltip-margin);
        left: 50%;
      }
      .tooltip.left {
        transform: translate3d(-100%, 50%, 0);
        bottom: 50%;
        left: var(--slider-tooltip-margin);
      }
      .tooltip.right {
        transform: translate3d(100%, 50%, 0);
        bottom: 50%;
        right: var(--slider-tooltip-margin);
      }
      :host(:not([vertical])) .tooltip.top,
      :host(:not([vertical])) .tooltip.bottom {
        left: var(--slider-tooltip-position);
      }
      :host([vertical]) .tooltip.right,
      :host([vertical]) .tooltip.left {
        bottom: var(--slider-tooltip-position);
      }
      .slider {
        position: relative;
        height: 100%;
        width: 100%;
        border-radius: var(--control-slider-border-radius);
        transform: translateZ(0);
        overflow: hidden;
        cursor: pointer;
      }
      .slider * {
        pointer-events: none;
      }
      .slider .slider-track-background {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background: var(--control-slider-background);
        opacity: var(--control-slider-background-opacity);
      }
      ::slotted([slot="background"]) {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
      }
      .slider .slider-track-bar {
        --border-radius: var(--control-slider-border-radius);
        --slider-size: 100%;
        position: absolute;
        height: 100%;
        width: 100%;
        background-color: var(--control-slider-color);
        transition:
          transform 180ms ease-in-out,
          background-color 180ms ease-in-out;
      }
      .slider .slider-track-bar.show-handle {
        --slider-size: calc(
          100% - 2 * var(--handle-margin) - var(--handle-size)
        );
      }
      .slider .slider-track-bar::after {
        display: block;
        content: "";
        position: absolute;
        margin: auto;
        border-radius: var(--handle-size);
        background-color: white;
      }
      .slider .slider-track-bar {
        top: 0;
        left: 0;
        transform: translate3d(
          calc((var(--value, 0) - 1) * var(--slider-size)),
          0,
          0
        );
        border-radius: 0 8px 8px 0;
      }
      .slider .slider-track-bar:after {
        top: 0;
        bottom: 0;
        right: var(--handle-margin);
        height: 50%;
        width: var(--handle-size);
      }
      .slider .slider-track-bar.end {
        right: 0;
        left: initial;
        transform: translate3d(
          calc(var(--value, 0) * var(--slider-size)),
          0,
          0
        );
        border-radius: 8px 0 0 8px;
      }
      .slider .slider-track-bar.end::after {
        right: initial;
        left: var(--handle-margin);
      }

      :host([vertical]) .slider .slider-track-bar {
        bottom: 0;
        left: 0;
        transform: translate3d(
          0,
          calc((1 - var(--value, 0)) * var(--slider-size)),
          0
        );
        border-radius: 8px 8px 0 0;
      }
      :host([vertical]) .slider .slider-track-bar:after {
        top: var(--handle-margin);
        right: 0;
        left: 0;
        bottom: initial;
        width: 50%;
        height: var(--handle-size);
      }
      :host([vertical]) .slider .slider-track-bar.end {
        top: 0;
        bottom: initial;
        transform: translate3d(
          0,
          calc((0 - var(--value, 0)) * var(--slider-size)),
          0
        );
        border-radius: 0 0 8px 8px;
      }
      :host([vertical]) .slider .slider-track-bar.end::after {
        top: initial;
        bottom: var(--handle-margin);
      }

      .slider .slider-track-cursor:after {
        display: block;
        content: "";
        background-color: var(--secondary-text-color);
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        margin: auto;
        border-radius: var(--handle-size);
      }

      .slider .slider-track-cursor {
        --cursor-size: calc(var(--control-slider-thickness) / 4);
        position: absolute;
        background-color: white;
        border-radius: var(--handle-size);
        transition:
          left 180ms ease-in-out,
          bottom 180ms ease-in-out;
        top: 0;
        bottom: 0;
        left: calc(var(--value, 0) * (100% - var(--cursor-size)));
        width: var(--cursor-size);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
      }
      .slider .slider-track-cursor:after {
        height: 50%;
        width: var(--handle-size);
      }

      :host([vertical]) .slider .slider-track-cursor {
        top: initial;
        right: 0;
        left: 0;
        bottom: calc(var(--value, 0) * (100% - var(--cursor-size)));
        height: var(--cursor-size);
        width: 100%;
      }
      :host([vertical]) .slider .slider-track-cursor:after {
        height: var(--handle-size);
        width: 50%;
      }
      .pressed .tooltip {
        transition: opacity 180ms ease-in-out;
      }
      .pressed .slider-track-bar,
      .pressed .slider-track-cursor {
        transition: none;
      }
      :host(:disabled) .slider {
        cursor: not-allowed;
      }
    `}}]}}),a.WF);var N=i(6601);let T=function(e){return e.UNKNOWN="unknown",e.ONOFF="onoff",e.BRIGHTNESS="brightness",e.COLOR_TEMP="color_temp",e.HS="hs",e.XY="xy",e.RGB="rgb",e.RGBW="rgbw",e.RGBWW="rgbww",e.WHITE="white",e}({});const V=[T.HS,T.XY,T.RGB,T.RGBW,T.RGBWW];T.COLOR_TEMP,T.BRIGHTNESS,T.WHITE;var Z=i(7133);const A=(e,t)=>{const i=[],r=(t-e)/10;for(let a=0;a<11;a++){const t=e+r*a,o=(0,c.v2)(v(t));i.push([.1*a,o])}return i.map((([e,t])=>`${t} ${100*e}%`)).join(", ")};(0,r.A)([(0,o.EM)("light-color-temp-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_ctPickerValue",value:void 0},{kind:"method",key:"render",value:function(){if(!this.stateObj)return a.s6;const e=this.stateObj.attributes.min_color_temp_kelvin??h,t=this.stateObj.attributes.max_color_temp_kelvin??m,i=this._generateTemperatureGradient(e,t),r=(0,f.Se)(this.stateObj);return a.qy`
      <ha-control-slider
        touch-action="none"
        inverted
        vertical
        .value=${this._ctPickerValue}
        .min=${e}
        .max=${t}
        mode="cursor"
        @value-changed=${this._ctColorChanged}
        @slider-moved=${this._ctColorCursorMoved}
        .ariaLabel=${this.hass.localize("ui.dialogs.more_info_control.light.color_temp")}
        style=${(0,s.W)({"--control-slider-color":r,"--gradient":i})}
        .disabled=${this.stateObj.state===N.Hh}
        .unit=${Z.rM.light.color_temp_kelvin}
        .locale=${this.hass.locale}
      >
      </ha-control-slider>
    `}},{kind:"field",key:"_generateTemperatureGradient",value(){return(0,n.A)(((e,t)=>A(e,t)))}},{kind:"method",key:"_updateSliderValues",value:function(){const e=this.stateObj;"on"===e.state?this._ctPickerValue=e.attributes.color_mode===T.COLOR_TEMP?e.attributes.color_temp_kelvin:void 0:this._ctPickerValue=void 0}},{kind:"method",key:"willUpdate",value:function(e){(0,d.A)(i,"willUpdate",this,3)([e]),e.has("stateObj")&&this._updateSliderValues()}},{kind:"method",key:"_ctColorCursorMoved",value:function(e){const t=e.detail.value;isNaN(t)||this._ctPickerValue===t||(this._ctPickerValue=t,(0,l.r)(this,"color-hovered",{color_temp_kelvin:t}),this._throttleUpdateColorTemp())}},{kind:"field",key:"_throttleUpdateColorTemp",value(){return(0,y.n)((()=>{this._updateColorTemp()}),500)}},{kind:"method",key:"_ctColorChanged",value:function(e){const t=e.detail.value;(0,l.r)(this,"color-hovered",void 0),isNaN(t)||this._ctPickerValue===t||(this._ctPickerValue=t,this._updateColorTemp())}},{kind:"method",key:"_updateColorTemp",value:function(){const e=this._ctPickerValue;this._applyColor({color_temp_kelvin:e})}},{kind:"method",key:"_applyColor",value:function(e,t){(0,l.r)(this,"color-changed",e),this.hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,...e,...t})}},{kind:"get",static:!0,key:"styles",value:function(){return[a.AH`
        :host {
          display: flex;
          flex-direction: column;
        }

        ha-control-slider {
          height: 45vh;
          max-height: 320px;
          min-height: 200px;
          --control-slider-thickness: 130px;
          --control-slider-border-radius: 36px;
          --control-slider-color: var(--primary-color);
          --control-slider-background: -webkit-linear-gradient(
            top,
            var(--gradient)
          );
          --control-slider-tooltip-font-size: 20px;
          --control-slider-background-opacity: 1;
        }
      `]}}]}}),a.WF);let z=(0,r.A)([(0,o.EM)("ha-selector-color_temp")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){let e,t;if("kelvin"===this.selector.color_temp?.unit)e=this.selector.color_temp?.min??h,t=this.selector.color_temp?.max??m;else e=this.selector.color_temp?.min??this.selector.color_temp?.min_mireds??153,t=this.selector.color_temp?.max??this.selector.color_temp?.max_mireds??500;const i=this._generateTemperatureGradient(this.selector.color_temp?.unit??"mired",e,t);return a.qy`
      <ha-labeled-slider
        style=${(0,s.W)({"--ha-slider-background":`linear-gradient( to var(--float-end), ${i})`})}
        labeled
        icon="hass:thermometer"
        .caption=${this.label||""}
        .min=${e}
        .max=${t}
        .value=${this.value}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .required=${this.required}
        @value-changed=${this._valueChanged}
      ></ha-labeled-slider>
    `}},{kind:"field",key:"_generateTemperatureGradient",value(){return(0,n.A)(((e,t,i)=>{let r;switch(e){case"kelvin":r=A(t,i);break;case"mired":r=A(b(t),b(i))}return r}))}},{kind:"method",key:"_valueChanged",value:function(e){(0,l.r)(this,"value-changed",{value:Number(e.detail.value)})}}]}}),a.WF)},6601:(e,t,i)=>{i.d(t,{HV:()=>o,Hh:()=>a,KF:()=>n,ON:()=>s,g0:()=>c,s7:()=>l});var r=i(79592);const a="unavailable",o="unknown",s="on",n="off",l=[a,o],d=[a,o,n],c=(0,r.g)(l);(0,r.g)(d)},7133:(e,t,i)=>{i.d(t,{rM:()=>r});new Set(["temperature","current_temperature","target_temperature","target_temp_temp","target_temp_high","target_temp_low","target_temp_step","min_temp","max_temp"]);const r={climate:{humidity:"%",current_humidity:"%",target_humidity_low:"%",target_humidity_high:"%",target_humidity_step:"%",min_humidity:"%",max_humidity:"%"},cover:{current_position:"%",current_tilt_position:"%"},fan:{percentage:"%"},humidifier:{humidity:"%",current_humidity:"%",min_humidity:"%",max_humidity:"%"},light:{color_temp:"mired",max_mireds:"mired",min_mireds:"mired",color_temp_kelvin:"K",min_color_temp_kelvin:"K",max_color_temp_kelvin:"K",brightness:"%"},sun:{azimuth:"°",elevation:"°"},vacuum:{battery_level:"%"},valve:{current_position:"%"},sensor:{battery_level:"%"},media_player:{volume_level:"%"}}},76415:(e,t,i)=>{i.d(t,{Hg:()=>a,Wj:()=>o,jG:()=>r,ow:()=>s,zt:()=>n});let r=function(e){return e.language="language",e.system="system",e.comma_decimal="comma_decimal",e.decimal_comma="decimal_comma",e.space_comma="space_comma",e.none="none",e}({}),a=function(e){return e.language="language",e.system="system",e.am_pm="12",e.twenty_four="24",e}({}),o=function(e){return e.local="local",e.server="server",e}({}),s=function(e){return e.language="language",e.system="system",e.DMY="DMY",e.MDY="MDY",e.YMD="YMD",e}({}),n=function(e){return e.language="language",e.monday="monday",e.tuesday="tuesday",e.wednesday="wednesday",e.thursday="thursday",e.friday="friday",e.saturday="saturday",e.sunday="sunday",e}({})}};
//# sourceMappingURL=WC7lZh3i.js.map