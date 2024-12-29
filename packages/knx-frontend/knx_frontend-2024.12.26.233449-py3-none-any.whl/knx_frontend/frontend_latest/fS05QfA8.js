export const id=178;export const ids=[178];export const modules={79592:(e,t,i)=>{i.d(t,{g:()=>a});const a=e=>(t,i)=>e.includes(t,i)},90662:(e,t,i)=>{i.d(t,{_:()=>n});var a=i(98597),o=i(3358);const n=(0,o.u$)(class extends o.WL{constructor(e){if(super(e),this._element=void 0,e.type!==o.OA.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}update(e,[t,i]){return this._element&&this._element.localName===t?(i&&Object.entries(i).forEach((([e,t])=>{this._element[e]=t})),a.c0):this.render(t,i)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach((([e,t])=>{this._element[e]=t})),this._element}})},24517:(e,t,i)=>{i.d(t,{d:()=>a});const a=e=>e.stopPropagation()},91330:(e,t,i)=>{i.d(t,{u:()=>o});var a=i(59782);const o=e=>{return t=e.entity_id,void 0===(i=e.attributes).friendly_name?(0,a.Y)(t).replace(/_/g," "):(i.friendly_name??"").toString();var t,i}},38848:(e,t,i)=>{i.d(t,{H:()=>k});var a=i(84381);let o=function(e){return e[e.Null=0]="Null",e[e.Backspace=8]="Backspace",e[e.Tab=9]="Tab",e[e.LineFeed=10]="LineFeed",e[e.CarriageReturn=13]="CarriageReturn",e[e.Space=32]="Space",e[e.ExclamationMark=33]="ExclamationMark",e[e.DoubleQuote=34]="DoubleQuote",e[e.Hash=35]="Hash",e[e.DollarSign=36]="DollarSign",e[e.PercentSign=37]="PercentSign",e[e.Ampersand=38]="Ampersand",e[e.SingleQuote=39]="SingleQuote",e[e.OpenParen=40]="OpenParen",e[e.CloseParen=41]="CloseParen",e[e.Asterisk=42]="Asterisk",e[e.Plus=43]="Plus",e[e.Comma=44]="Comma",e[e.Dash=45]="Dash",e[e.Period=46]="Period",e[e.Slash=47]="Slash",e[e.Digit0=48]="Digit0",e[e.Digit1=49]="Digit1",e[e.Digit2=50]="Digit2",e[e.Digit3=51]="Digit3",e[e.Digit4=52]="Digit4",e[e.Digit5=53]="Digit5",e[e.Digit6=54]="Digit6",e[e.Digit7=55]="Digit7",e[e.Digit8=56]="Digit8",e[e.Digit9=57]="Digit9",e[e.Colon=58]="Colon",e[e.Semicolon=59]="Semicolon",e[e.LessThan=60]="LessThan",e[e.Equals=61]="Equals",e[e.GreaterThan=62]="GreaterThan",e[e.QuestionMark=63]="QuestionMark",e[e.AtSign=64]="AtSign",e[e.A=65]="A",e[e.B=66]="B",e[e.C=67]="C",e[e.D=68]="D",e[e.E=69]="E",e[e.F=70]="F",e[e.G=71]="G",e[e.H=72]="H",e[e.I=73]="I",e[e.J=74]="J",e[e.K=75]="K",e[e.L=76]="L",e[e.M=77]="M",e[e.N=78]="N",e[e.O=79]="O",e[e.P=80]="P",e[e.Q=81]="Q",e[e.R=82]="R",e[e.S=83]="S",e[e.T=84]="T",e[e.U=85]="U",e[e.V=86]="V",e[e.W=87]="W",e[e.X=88]="X",e[e.Y=89]="Y",e[e.Z=90]="Z",e[e.OpenSquareBracket=91]="OpenSquareBracket",e[e.Backslash=92]="Backslash",e[e.CloseSquareBracket=93]="CloseSquareBracket",e[e.Caret=94]="Caret",e[e.Underline=95]="Underline",e[e.BackTick=96]="BackTick",e[e.a=97]="a",e[e.b=98]="b",e[e.c=99]="c",e[e.d=100]="d",e[e.e=101]="e",e[e.f=102]="f",e[e.g=103]="g",e[e.h=104]="h",e[e.i=105]="i",e[e.j=106]="j",e[e.k=107]="k",e[e.l=108]="l",e[e.m=109]="m",e[e.n=110]="n",e[e.o=111]="o",e[e.p=112]="p",e[e.q=113]="q",e[e.r=114]="r",e[e.s=115]="s",e[e.t=116]="t",e[e.u=117]="u",e[e.v=118]="v",e[e.w=119]="w",e[e.x=120]="x",e[e.y=121]="y",e[e.z=122]="z",e[e.OpenCurlyBrace=123]="OpenCurlyBrace",e[e.Pipe=124]="Pipe",e[e.CloseCurlyBrace=125]="CloseCurlyBrace",e[e.Tilde=126]="Tilde",e}({});const n=128;function r(){const e=[],t=[];for(let i=0;i<=n;i++)t[i]=0;for(let i=0;i<=n;i++)e.push(t.slice(0));return e}function s(e,t){if(t<0||t>=e.length)return!1;const i=e.codePointAt(t);switch(i){case o.Underline:case o.Dash:case o.Period:case o.Space:case o.Slash:case o.Backslash:case o.SingleQuote:case o.DoubleQuote:case o.Colon:case o.DollarSign:case o.LessThan:case o.OpenParen:case o.OpenSquareBracket:return!0;case void 0:return!1;default:return(a=i)>=127462&&a<=127487||8986===a||8987===a||9200===a||9203===a||a>=9728&&a<=10175||11088===a||11093===a||a>=127744&&a<=128591||a>=128640&&a<=128764||a>=128992&&a<=129003||a>=129280&&a<=129535||a>=129648&&a<=129750?!0:!1}var a}function d(e,t){if(t<0||t>=e.length)return!1;switch(e.charCodeAt(t)){case o.Space:case o.Tab:return!0;default:return!1}}function l(e,t,i){return t[e]!==i[e]}var c=function(e){return e[e.Diag=1]="Diag",e[e.Left=2]="Left",e[e.LeftLeft=3]="LeftLeft",e}(c||{});function h(e,t,i,a,o,r,s){const d=e.length>n?n:e.length,h=a.length>n?n:a.length;if(i>=d||r>=h||d-i>h-r)return;if(!function(e,t,i,a,o,n,r=!1){for(;t<i&&o<n;)e[t]===a[o]&&(r&&(p[t]=o),t+=1),o+=1;return t===i}(t,i,d,o,r,h,!0))return;let y;!function(e,t,i,a,o,n){let r=e-1,s=t-1;for(;r>=i&&s>=a;)o[r]===n[s]&&(v[r]=s,r--),s--}(d,h,i,r,t,o);let k,b,_=1;const x=[!1];for(y=1,k=i;k<d;y++,k++){const n=p[k],s=v[k],l=k+1<d?v[k+1]:h;for(_=n-r+1,b=n;b<l;_++,b++){let d=Number.MIN_SAFE_INTEGER,l=!1;b<=s&&(d=u(e,t,k,i,a,o,b,h,r,0===m[y-1][_-1],x));let p=0;d!==Number.MAX_SAFE_INTEGER&&(l=!0,p=d+g[y-1][_-1]);const v=b>n,$=v?g[y][_-1]+(m[y][_-1]>0?-5:0):0,w=b>n+1&&m[y][_-1]>0,M=w?g[y][_-2]+(m[y][_-2]>0?-5:0):0;if(w&&(!v||M>=$)&&(!l||M>=p))g[y][_]=M,f[y][_]=c.LeftLeft,m[y][_]=0;else if(v&&(!l||$>=p))g[y][_]=$,f[y][_]=c.Left,m[y][_]=0;else{if(!l)throw new Error("not possible");g[y][_]=p,f[y][_]=c.Diag,m[y][_]=m[y-1][_-1]+1}}}if(!x[0]&&!s)return;y--,_--;const $=[g[y][_],r];let w=0,M=0;for(;y>=1;){let e=_;do{const t=f[y][e];if(t===c.LeftLeft)e-=2;else{if(t!==c.Left)break;e-=1}}while(e>=1);w>1&&t[i+y-1]===o[r+_-1]&&!l(e+r-1,a,o)&&w+1>m[y][e]&&(e=_),e===_?w++:w=1,M||(M=e),y--,_=e-1,$.push(_)}h===d&&($[0]+=2);const C=M-d;return $[0]-=C,$}function u(e,t,i,a,o,n,r,c,h,u,p){if(t[i]!==n[r])return Number.MIN_SAFE_INTEGER;let v=1,m=!1;return r===i-a?v=e[i]===o[r]?7:5:!l(r,o,n)||0!==r&&l(r-1,o,n)?!s(n,r)||0!==r&&s(n,r-1)?(s(n,r-1)||d(n,r-1))&&(v=5,m=!0):v=5:(v=e[i]===o[r]?7:5,m=!0),v>1&&i===a&&(p[0]=!0),m||(m=l(r,o,n)||s(n,r-1)||d(n,r-1)),i===a?r>h&&(v-=m?3:5):v+=u?m?2:0:m?0:1,r+1===c&&(v-=m?3:5),v}const p=y(256),v=y(256),m=r(),g=r(),f=r();function y(e){const t=[];for(let i=0;i<=e;i++)t[i]=0;return t}const k=(e,t)=>t.map((t=>(t.score=((e,t)=>{let i=Number.NEGATIVE_INFINITY;for(const o of t.strings){const t=h(e,(0,a.s)(e.toLowerCase()),0,o,(0,a.s)(o.toLowerCase()),0,!0);if(!t)continue;const n=0===t[0]?1:t[0];n>i&&(i=n)}if(i!==Number.NEGATIVE_INFINITY)return i})(e,t),t))).filter((e=>void 0!==e.score)).sort((({score:e=0},{score:t=0})=>e>t?-1:e<t?1:0))},84381:(e,t,i)=>{i.d(t,{s:()=>a});const a=e=>e.normalize("NFD").replace(/[\u0300-\u036F]/g,"")},73409:(e,t,i)=>{var a=i(85461),o=i(53449),n=i(196);(0,a.A)([(0,n.EM)("ha-chip-set")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[]}}),o.Y)},28331:(e,t,i)=>{var a=i(85461),o=i(69534),n=i(39050),r=i(98597),s=i(196);(0,a.A)([(0,s.EM)("ha-input-chip")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",static:!0,key:"styles",value(){return[...(0,o.A)(i,"styles",this),r.AH`
      :host {
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-sys-color-on-surface-variant: var(--primary-text-color);
        --md-sys-color-on-secondary-container: var(--primary-text-color);
        --md-input-chip-container-shape: 16px;
        --md-input-chip-outline-color: var(--outline-color);
        --md-input-chip-selected-container-color: rgba(
          var(--rgb-primary-text-color),
          0.15
        );
        --ha-input-chip-selected-container-opacity: 1;
        --md-input-chip-label-text-font: Roboto, sans-serif;
      }
      /** Set the size of mdc icons **/
      ::slotted([slot="icon"]) {
        display: flex;
        --mdc-icon-size: var(--md-input-chip-icon-size, 18px);
      }
      .selected::before {
        opacity: var(--ha-input-chip-selected-container-opacity);
      }
    `]}}]}}),n.U)},91074:(e,t,i)=>{i.r(t);var a=i(85461),o=i(98597),n=i(196),r=i(69760),s=i(33167);i(96396),i(29222);const d={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};(0,a.A)([(0,n.EM)("ha-alert")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)()],key:"title",value(){return""}},{kind:"field",decorators:[(0,n.MZ)({attribute:"alert-type"})],key:"alertType",value(){return"info"}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"dismissable",value(){return!1}},{kind:"method",key:"render",value:function(){return o.qy`
      <div
        class="issue-type ${(0,r.H)({[this.alertType]:!0})}"
        role="alert"
      >
        <div class="icon ${this.title?"":"no-title"}">
          <slot name="icon">
            <ha-svg-icon .path=${d[this.alertType]}></ha-svg-icon>
          </slot>
        </div>
        <div class="content">
          <div class="main-content">
            ${this.title?o.qy`<div class="title">${this.title}</div>`:""}
            <slot></slot>
          </div>
          <div class="action">
            <slot name="action">
              ${this.dismissable?o.qy`<ha-icon-button
                    @click=${this._dismiss_clicked}
                    label="Dismiss alert"
                    .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
                  ></ha-icon-button>`:""}
            </slot>
          </div>
        </div>
      </div>
    `}},{kind:"method",key:"_dismiss_clicked",value:function(){(0,s.r)(this,"alert-dismissed-clicked")}},{kind:"field",static:!0,key:"styles",value(){return o.AH`
    .issue-type {
      position: relative;
      padding: 8px;
      display: flex;
    }
    .issue-type::after {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      opacity: 0.12;
      pointer-events: none;
      content: "";
      border-radius: 4px;
    }
    .icon {
      z-index: 1;
    }
    .icon.no-title {
      align-self: center;
    }
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      text-align: var(--float-start);
    }
    .action {
      z-index: 1;
      width: min-content;
      --mdc-theme-primary: var(--primary-text-color);
    }
    .main-content {
      overflow-wrap: anywhere;
      word-break: break-word;
      margin-left: 8px;
      margin-right: 0;
      margin-inline-start: 8px;
      margin-inline-end: 0;
    }
    .title {
      margin-top: 2px;
      font-weight: bold;
    }
    .action mwc-button,
    .action ha-icon-button {
      --mdc-theme-primary: var(--primary-text-color);
      --mdc-icon-button-size: 36px;
    }
    .issue-type.info > .icon {
      color: var(--info-color);
    }
    .issue-type.info::after {
      background-color: var(--info-color);
    }

    .issue-type.warning > .icon {
      color: var(--warning-color);
    }
    .issue-type.warning::after {
      background-color: var(--warning-color);
    }

    .issue-type.error > .icon {
      color: var(--error-color);
    }
    .issue-type.error::after {
      background-color: var(--error-color);
    }

    .issue-type.success > .icon {
      color: var(--success-color);
    }
    .issue-type.success::after {
      background-color: var(--success-color);
    }
    :host ::slotted(ul) {
      margin: 0;
      padding-inline-start: 20px;
    }
  `}}]}}),o.WF)},57046:(e,t,i)=>{var a=i(85461),o=i(98597),n=i(196),r=i(69760),s=i(45081),d=i(33167),l=i(19263),c=i(38848),h=i(13473),u=i(40884),p=i(31447),v=i(83895);i(66442),i(96396),i(9484),i(29222);const m=e=>o.qy`<ha-list-item
    graphic="icon"
    class=${(0,r.H)({"add-new":e.area_id===g})}
  >
    ${e.icon?o.qy`<ha-icon slot="graphic" .icon=${e.icon}></ha-icon>`:o.qy`<ha-svg-icon slot="graphic" .path=${"M20 2H4C2.9 2 2 2.9 2 4V20C2 21.11 2.9 22 4 22H20C21.11 22 22 21.11 22 20V4C22 2.9 21.11 2 20 2M4 6L6 4H10.9L4 10.9V6M4 13.7L13.7 4H18.6L4 18.6V13.7M20 18L18 20H13.1L20 13.1V18M20 10.3L10.3 20H5.4L20 5.4V10.3Z"}></ha-svg-icon>`}
    ${e.name}
  </ha-list-item>`,g="___ADD_NEW___",f="___NO_ITEMS___",y="___ADD_NEW_SUGGESTION___";(0,a.A)([(0,n.EM)("ha-area-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"no-add"})],key:"noAdd",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array,attribute:"exclude-areas"})],key:"excludeAreas",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"deviceFilter",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"entityFilter",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_suggestion",value:void 0},{kind:"field",key:"_init",value(){return!1}},{kind:"method",key:"open",value:async function(){await this.updateComplete,await(this.comboBox?.open())}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this.comboBox?.focus())}},{kind:"field",key:"_getAreas",value(){return(0,s.A)(((e,t,i,a,o,n,r,s,d,c)=>{let h,p,v={};(a||o||n||r||s)&&(v=(0,u.g2)(i),h=t,p=i.filter((e=>e.area_id)),a&&(h=h.filter((e=>{const t=v[e.id];return!(!t||!t.length)&&v[e.id].some((e=>a.includes((0,l.m)(e.entity_id))))})),p=p.filter((e=>a.includes((0,l.m)(e.entity_id))))),o&&(h=h.filter((e=>{const t=v[e.id];return!t||!t.length||i.every((e=>!o.includes((0,l.m)(e.entity_id))))})),p=p.filter((e=>!o.includes((0,l.m)(e.entity_id))))),n&&(h=h.filter((e=>{const t=v[e.id];return!(!t||!t.length)&&v[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&n.includes(t.attributes.device_class))}))})),p=p.filter((e=>{const t=this.hass.states[e.entity_id];return t.attributes.device_class&&n.includes(t.attributes.device_class)}))),r&&(h=h.filter((e=>r(e)))),s&&(h=h.filter((e=>{const t=v[e.id];return!(!t||!t.length)&&v[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&s(t)}))})),p=p.filter((e=>{const t=this.hass.states[e.entity_id];return!!t&&s(t)}))));let m,y=e;return h&&(m=h.filter((e=>e.area_id)).map((e=>e.area_id))),p&&(m=(m??[]).concat(p.filter((e=>e.area_id)).map((e=>e.area_id)))),m&&(y=y.filter((e=>m.includes(e.area_id)))),c&&(y=y.filter((e=>!c.includes(e.area_id)))),y.length||(y=[{area_id:f,floor_id:null,name:this.hass.localize("ui.components.area-picker.no_areas"),picture:null,icon:null,aliases:[],labels:[],created_at:0,modified_at:0}]),d?y:[...y,{area_id:g,floor_id:null,name:this.hass.localize("ui.components.area-picker.add_new"),picture:null,icon:"mdi:plus",aliases:[],labels:[],created_at:0,modified_at:0}]}))}},{kind:"method",key:"updated",value:function(e){if(!this._init&&this.hass||this._init&&e.has("_opened")&&this._opened){this._init=!0;const e=this._getAreas(Object.values(this.hass.areas),Object.values(this.hass.devices),Object.values(this.hass.entities),this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.noAdd,this.excludeAreas).map((e=>({...e,strings:[e.area_id,...e.aliases,e.name]})));this.comboBox.items=e,this.comboBox.filteredItems=e}}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-combo-box
        .hass=${this.hass}
        .helper=${this.helper}
        item-value-path="area_id"
        item-id-path="area_id"
        item-label-path="name"
        .value=${this._value}
        .disabled=${this.disabled}
        .required=${this.required}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.area-picker.area"):this.label}
        .placeholder=${this.placeholder?this.hass.areas[this.placeholder]?.name:void 0}
        .renderer=${m}
        @filter-changed=${this._filterChanged}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._areaChanged}
      >
      </ha-combo-box>
    `}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.target,i=e.detail.value;if(!i)return void(this.comboBox.filteredItems=this.comboBox.items);const a=(0,c.H)(i,t.items?.filter((e=>![f,g].includes(e.label_id)))||[]);0===a.length?this.noAdd?(this._suggestion=i,this.comboBox.filteredItems=[{area_id:y,floor_id:null,name:this.hass.localize("ui.components.area-picker.add_new_sugestion",{name:this._suggestion}),icon:"mdi:plus",picture:null,labels:[],aliases:[],created_at:0,modified_at:0}]):this.comboBox.filteredItems=[{area_id:f,floor_id:null,name:this.hass.localize("ui.components.area-picker.no_match"),icon:null,picture:null,labels:[],aliases:[],created_at:0,modified_at:0}]:this.comboBox.filteredItems=a}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_areaChanged",value:function(e){e.stopPropagation();let t=e.detail.value;if(t===f)return t="",void this.comboBox.setInputValue("");[y,g].includes(t)?(e.target.value=this._value,this.hass.loadFragmentTranslation("config"),(0,v.J)(this,{suggestedName:t===y?this._suggestion:"",createEntry:async e=>{try{const t=await(0,h.L3)(this.hass,e),i=[...Object.values(this.hass.areas),t];this.comboBox.filteredItems=this._getAreas(i,Object.values(this.hass.devices),Object.values(this.hass.entities),this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.noAdd,this.excludeAreas),await this.updateComplete,await this.comboBox.updateComplete,this._setValue(t.area_id)}catch(t){(0,p.K$)(this,{title:this.hass.localize("ui.components.area-picker.failed_create_area"),text:t.message})}}}),this._suggestion=void 0,this.comboBox.setInputValue("")):t!==this._value&&this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,d.r)(this,"value-changed",{value:e}),(0,d.r)(this,"change")}),0)}}]}}),o.WF)},66494:(e,t,i)=>{var a=i(85461),o=i(58068),n=i(98597),r=i(196),s=i(75538);(0,a.A)([(0,r.EM)("ha-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[s.R,n.AH`
      ::slotted([slot="icon"]) {
        margin-inline-start: 0px;
        margin-inline-end: 8px;
        direction: var(--direction);
        display: block;
      }
      .mdc-button {
        height: var(--button-height, 36px);
      }
      .trailing-icon {
        display: flex;
      }
      .slot-container {
        overflow: var(--button-slot-container-overflow, visible);
      }
    `]}}]}}),o.$)},94392:(e,t,i)=>{var a=i(85461),o=i(98597),n=i(196);(0,a.A)([(0,n.EM)("ha-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)()],key:"header",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"raised",value(){return!1}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        background: var(
          --ha-card-background,
          var(--card-background-color, white)
        );
        -webkit-backdrop-filter: var(--ha-card-backdrop-filter, none);
        backdrop-filter: var(--ha-card-backdrop-filter, none);
        box-shadow: var(--ha-card-box-shadow, none);
        box-sizing: border-box;
        border-radius: var(--ha-card-border-radius, 12px);
        border-width: var(--ha-card-border-width, 1px);
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      :host([raised]) {
        border: none;
        box-shadow: var(
          --ha-card-box-shadow,
          0px 2px 1px -1px rgba(0, 0, 0, 0.2),
          0px 1px 1px 0px rgba(0, 0, 0, 0.14),
          0px 1px 3px 0px rgba(0, 0, 0, 0.12)
        );
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, var(--primary-text-color));
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 48px;
        padding: 12px 16px 16px;
        display: block;
        margin-block-start: 0px;
        margin-block-end: 0px;
        font-weight: normal;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid var(--divider-color, #e8e8e8);
        padding: 5px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return o.qy`
      ${this.header?o.qy`<h1 class="card-header">${this.header}</h1>`:o.s6}
      <slot></slot>
    `}}]}}),o.WF)},66442:(e,t,i)=>{var a=i(85461),o=i(69534),n=i(54854),r=(i(1843),i(19945)),s=i(98597),d=i(196),l=i(79278),c=i(33167);i(96396),i(9484),i(59373);(0,r.SF)("vaadin-combo-box-item",s.AH`
    :host {
      padding: 0 !important;
    }
    :host([focused]:not([disabled])) {
      background-color: rgba(var(--rgb-primary-text-color, 0, 0, 0), 0.12);
    }
    :host([selected]:not([disabled])) {
      background-color: transparent;
      color: var(--mdc-theme-primary);
      --mdc-ripple-color: var(--mdc-theme-primary);
      --mdc-theme-text-primary-on-background: var(--mdc-theme-primary);
    }
    :host([selected]:not([disabled])):before {
      background-color: var(--mdc-theme-primary);
      opacity: 0.12;
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
    :host([selected][focused]:not([disabled])):before {
      opacity: 0.24;
    }
    :host(:hover:not([disabled])) {
      background-color: transparent;
    }
    [part="content"] {
      width: 100%;
    }
    [part="checkmark"] {
      display: none;
    }
  `);(0,a.A)([(0,d.EM)("ha-combo-box")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"validationMessage",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"invalid",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"icon",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"items",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"filteredItems",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"dataProvider",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:"allow-custom-value",type:Boolean})],key:"allowCustomValue",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({attribute:"item-value-path"})],key:"itemValuePath",value(){return"value"}},{kind:"field",decorators:[(0,d.MZ)({attribute:"item-label-path"})],key:"itemLabelPath",value(){return"label"}},{kind:"field",decorators:[(0,d.MZ)({attribute:"item-id-path"})],key:"itemIdPath",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"renderer",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean,reflect:!0})],key:"opened",value(){return!1}},{kind:"field",decorators:[(0,d.P)("vaadin-combo-box-light",!0)],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,d.P)("ha-textfield",!0)],key:"_inputElement",value:void 0},{kind:"field",key:"_overlayMutationObserver",value:void 0},{kind:"field",key:"_bodyMutationObserver",value:void 0},{kind:"method",key:"open",value:async function(){await this.updateComplete,this._comboBox?.open()}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this._inputElement?.updateComplete),this._inputElement?.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.A)(i,"disconnectedCallback",this,3)([]),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}},{kind:"get",key:"selectedItem",value:function(){return this._comboBox.selectedItem}},{kind:"method",key:"setInputValue",value:function(e){this._comboBox.value=e}},{kind:"method",key:"render",value:function(){return s.qy`
      <!-- @ts-ignore Tag definition is not included in theme folder -->
      <vaadin-combo-box-light
        .itemValuePath=${this.itemValuePath}
        .itemIdPath=${this.itemIdPath}
        .itemLabelPath=${this.itemLabelPath}
        .items=${this.items}
        .value=${this.value||""}
        .filteredItems=${this.filteredItems}
        .dataProvider=${this.dataProvider}
        .allowCustomValue=${this.allowCustomValue}
        .disabled=${this.disabled}
        .required=${this.required}
        ${(0,n.d)(this.renderer||this._defaultRowRenderer)}
        @opened-changed=${this._openedChanged}
        @filter-changed=${this._filterChanged}
        @value-changed=${this._valueChanged}
        attr-for-value="value"
      >
        <ha-textfield
          label=${(0,l.J)(this.label)}
          placeholder=${(0,l.J)(this.placeholder)}
          ?disabled=${this.disabled}
          ?required=${this.required}
          validationMessage=${(0,l.J)(this.validationMessage)}
          .errorMessage=${this.errorMessage}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          input-spellcheck="false"
          .suffix=${s.qy`<div
            style="width: 28px;"
            role="none presentation"
          ></div>`}
          .icon=${this.icon}
          .invalid=${this.invalid}
          .helper=${this.helper}
          helperPersistent
        >
          <slot name="icon" slot="leadingIcon"></slot>
        </ha-textfield>
        ${this.value?s.qy`<ha-svg-icon
              role="button"
              tabindex="-1"
              aria-label=${(0,l.J)(this.hass?.localize("ui.common.clear"))}
              class="clear-button"
              .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              @click=${this._clearValue}
            ></ha-svg-icon>`:""}
        <ha-svg-icon
          role="button"
          tabindex="-1"
          aria-label=${(0,l.J)(this.label)}
          aria-expanded=${this.opened?"true":"false"}
          class="toggle-button"
          .path=${this.opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"}
          @click=${this._toggleOpen}
        ></ha-svg-icon>
      </vaadin-combo-box-light>
    `}},{kind:"field",key:"_defaultRowRenderer",value(){return e=>s.qy`<ha-list-item>
      ${this.itemLabelPath?e[this.itemLabelPath]:e}
    </ha-list-item>`}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),(0,c.r)(this,"value-changed",{value:void 0})}},{kind:"method",key:"_toggleOpen",value:function(e){this.opened?(this._comboBox?.close(),e.stopPropagation()):this._comboBox?.inputElement.focus()}},{kind:"method",key:"_openedChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(setTimeout((()=>{this.opened=t}),0),(0,c.r)(this,"opened-changed",{value:e.detail.value}),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else this._bodyMutationObserver?.disconnect(),this._bodyMutationObserver=void 0}},{kind:"method",key:"_observeBody",value:function(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver((e=>{e.forEach((e=>{e.addedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)})),e.removedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0)}))}))})),this._bodyMutationObserver.observe(document.body,{childList:!0}))}},{kind:"method",key:"_removeInert",value:function(e){if(e.inert)return e.inert=!1,this._overlayMutationObserver?.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver((e=>{e.forEach((e=>{if("inert"===e.attributeName){const t=e.target;t.inert&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0,t.inert=!1)}}))})),this._overlayMutationObserver.observe(e,{attributes:!0}))}},{kind:"method",key:"_filterChanged",value:function(e){e.stopPropagation(),(0,c.r)(this,"filter-changed",{value:e.detail.value})}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0);const t=e.detail.value;t!==this.value&&(0,c.r)(this,"value-changed",{value:t||void 0})}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`
      :host {
        display: block;
        width: 100%;
      }
      vaadin-combo-box-light {
        position: relative;
        --vaadin-combo-box-overlay-max-height: calc(45vh - 56px);
      }
      ha-textfield {
        width: 100%;
      }
      ha-textfield > ha-icon-button {
        --mdc-icon-button-size: 24px;
        padding: 2px;
        color: var(--secondary-text-color);
      }
      ha-svg-icon {
        color: var(--input-dropdown-icon-color);
        position: absolute;
        cursor: pointer;
      }
      .toggle-button {
        right: 12px;
        top: -10px;
        inset-inline-start: initial;
        inset-inline-end: 12px;
        direction: var(--direction);
      }
      :host([opened]) .toggle-button {
        color: var(--primary-color);
      }
      .clear-button {
        --mdc-icon-size: 20px;
        top: -7px;
        right: 36px;
        inset-inline-start: initial;
        inset-inline-end: 36px;
        direction: var(--direction);
      }
    `}}]}}),s.WF)},91686:(e,t,i)=>{var a=i(85461),o=i(69534),n=i(98597),r=i(196),s=i(69760),d=i(33167),l=i(45787);i(29222);const c="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z";(0,a.A)([(0,r.EM)("ha-expansion-panel")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"expanded",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"outlined",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"leftChevron",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"noCollapse",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)()],key:"header",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"secondary",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_showContent",value(){return this.expanded}},{kind:"field",decorators:[(0,r.P)(".container")],key:"_container",value:void 0},{kind:"method",key:"render",value:function(){return n.qy`
      <div class="top ${(0,s.H)({expanded:this.expanded})}">
        <div
          id="summary"
          class=${(0,s.H)({noCollapse:this.noCollapse})}
          @click=${this._toggleContainer}
          @keydown=${this._toggleContainer}
          @focus=${this._focusChanged}
          @blur=${this._focusChanged}
          role="button"
          tabindex=${this.noCollapse?-1:0}
          aria-expanded=${this.expanded}
          aria-controls="sect1"
        >
          ${this.leftChevron&&!this.noCollapse?n.qy`
                <ha-svg-icon
                  .path=${c}
                  class="summary-icon ${(0,s.H)({expanded:this.expanded})}"
                ></ha-svg-icon>
              `:""}
          <slot name="header">
            <div class="header">
              ${this.header}
              <slot class="secondary" name="secondary">${this.secondary}</slot>
            </div>
          </slot>
          ${this.leftChevron||this.noCollapse?"":n.qy`
                <ha-svg-icon
                  .path=${c}
                  class="summary-icon ${(0,s.H)({expanded:this.expanded})}"
                ></ha-svg-icon>
              `}
          <slot name="icons"></slot>
        </div>
      </div>
      <div
        class="container ${(0,s.H)({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
        role="region"
        aria-labelledby="summary"
        aria-hidden=${!this.expanded}
        tabindex="-1"
      >
        ${this._showContent?n.qy`<slot></slot>`:""}
      </div>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,o.A)(i,"willUpdate",this,3)([e]),e.has("expanded")&&(this._showContent=this.expanded,setTimeout((()=>{this._container.style.overflow=this.expanded?"initial":"hidden"}),300))}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._container.style.removeProperty("height"),this._container.style.overflow=this.expanded?"initial":"hidden",this._showContent=this.expanded}},{kind:"method",key:"_toggleContainer",value:async function(e){if(e.defaultPrevented)return;if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;if(e.preventDefault(),this.noCollapse)return;const t=!this.expanded;(0,d.r)(this,"expanded-will-change",{expanded:t}),this._container.style.overflow="hidden",t&&(this._showContent=!0,await(0,l.E)());const i=this._container.scrollHeight;this._container.style.height=`${i}px`,t||setTimeout((()=>{this._container.style.height="0px"}),0),this.expanded=t,(0,d.r)(this,"expanded-changed",{expanded:this.expanded})}},{kind:"method",key:"_focusChanged",value:function(e){this.noCollapse||this.shadowRoot.querySelector(".top").classList.toggle("focused","focus"===e.type)}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      :host {
        display: block;
      }

      .top {
        display: flex;
        align-items: center;
        border-radius: var(--ha-card-border-radius, 12px);
      }

      .top.expanded {
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
      }

      .top.focused {
        background: var(--input-fill-color);
      }

      :host([outlined]) {
        box-shadow: none;
        border-width: 1px;
        border-style: solid;
        border-color: var(--outline-color);
        border-radius: var(--ha-card-border-radius, 12px);
      }

      .summary-icon {
        transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
        direction: var(--direction);
        margin-left: 8px;
        margin-inline-start: 8px;
        margin-inline-end: initial;
      }

      :host([leftchevron]) .summary-icon {
        margin-left: 0;
        margin-right: 8px;
        margin-inline-start: 0;
        margin-inline-end: 8px;
      }

      #summary {
        flex: 1;
        display: flex;
        padding: var(--expansion-panel-summary-padding, 0 8px);
        min-height: 48px;
        align-items: center;
        cursor: pointer;
        overflow: hidden;
        font-weight: 500;
        outline: none;
      }
      #summary.noCollapse {
        cursor: default;
      }

      .summary-icon.expanded {
        transform: rotate(180deg);
      }

      .header,
      ::slotted([slot="header"]) {
        flex: 1;
      }

      .container {
        padding: var(--expansion-panel-content-padding, 0 8px);
        overflow: hidden;
        transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
        height: 0px;
      }

      .container.expanded {
        height: auto;
      }

      .secondary {
        display: block;
        color: var(--secondary-text-color);
        font-size: 12px;
      }
    `}}]}}),n.WF)},32694:(e,t,i)=>{var a=i(85461),o=i(80487),n=i(4258),r=i(98597),s=i(196),d=i(69760),l=i(33167);(0,a.A)([(0,s.EM)("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return r.qy` <div class="mdc-form-field ${(0,d.H)(e)}">
      <slot></slot>
      <label class="mdc-label" @click=${this._labelClick}>
        <slot name="label">${this.label}</slot>
      </label>
    </div>`}},{kind:"method",key:"_labelClick",value:function(){const e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,l.r)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,l.r)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value(){return[n.R,r.AH`
      :host(:not([alignEnd])) ::slotted(ha-switch) {
        margin-right: 10px;
        margin-inline-end: 10px;
        margin-inline-start: inline;
      }
      .mdc-form-field {
        align-items: var(--ha-formfield-align-items, center);
        gap: 4px;
      }
      .mdc-form-field > label {
        direction: var(--direction);
        margin-inline-start: 0;
        margin-inline-end: auto;
        padding: 0;
      }
      :host([disabled]) label {
        color: var(--disabled-text-color);
      }
    `]}}]}}),o.M)},94333:(e,t,i)=>{i.r(t),i.d(t,{HaIconNext:()=>s});var a=i(85461),o=i(196),n=i(10),r=i(29222);let s=(0,a.A)([(0,o.EM)("ha-icon-next")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)()],key:"path",value(){return"rtl"===n.G.document.dir?"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z":"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"}}]}}),r.HaSvgIcon)},43689:(e,t,i)=>{var a=i(85461),o=i(98597),n=i(196);(0,a.A)([(0,n.EM)("ha-input-helper-text")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return o.qy`<slot></slot>`}},{kind:"field",static:!0,key:"styles",value(){return o.AH`
    :host {
      display: block;
      color: var(--mdc-text-field-label-ink-color, rgba(0, 0, 0, 0.6));
      font-size: 0.75rem;
      padding-left: 16px;
      padding-right: 16px;
      padding-inline-start: 16px;
      padding-inline-end: 16px;
    }
  `}}]}}),o.WF)},9484:(e,t,i)=>{var a=i(85461),o=i(69534),n=i(46175),r=i(45592),s=i(98597),d=i(196);(0,a.A)([(0,d.EM)("ha-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,o.A)(i,"renderRipple",this,3)([])}},{kind:"get",static:!0,key:"styles",value:function(){return[r.R,s.AH`
        :host {
          padding-left: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-start: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-right: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-end: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
        }
        :host([graphic="avatar"]:not([twoLine])),
        :host([graphic="icon"]:not([twoLine])) {
          height: 48px;
        }
        span.material-icons:first-of-type {
          margin-inline-start: 0px !important;
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            16px
          ) !important;
          direction: var(--direction) !important;
        }
        span.material-icons:last-of-type {
          margin-inline-start: auto !important;
          margin-inline-end: 0px !important;
          direction: var(--direction) !important;
        }
        .mdc-deprecated-list-item__meta {
          display: var(--mdc-list-item-meta-display);
          align-items: center;
          flex-shrink: 0;
        }
        :host([graphic="icon"]:not([twoline]))
          .mdc-deprecated-list-item__graphic {
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            20px
          ) !important;
        }
        :host([multiline-secondary]) {
          height: auto;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__text {
          padding: 8px 0;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text {
          text-overflow: initial;
          white-space: normal;
          overflow: auto;
          display: inline-block;
          margin-top: 10px;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__primary-text {
          margin-top: 10px;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__secondary-text::before {
          display: none;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__primary-text::before {
          display: none;
        }
        :host([disabled]) {
          color: var(--disabled-text-color);
        }
        :host([noninteractive]) {
          pointer-events: unset;
        }
      `,"rtl"===document.dir?s.AH`
            span.material-icons:first-of-type,
            span.material-icons:last-of-type {
              direction: rtl !important;
              --direction: rtl;
            }
          `:s.AH``]}}]}}),n.J)},26589:(e,t,i)=>{var a=i(85461),o=i(98597),n=i(196),r=i(33167),s=i(43799);i(66494),i(96396),i(59373);(0,a.A)([(0,n.EM)("ha-multi-textfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"inputType",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"inputSuffix",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"inputPrefix",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"addLabel",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"removeLabel",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"item-index",type:Boolean})],key:"itemIndex",value(){return!1}},{kind:"method",key:"render",value:function(){return o.qy`
      ${this._items.map(((e,t)=>{const i=""+(this.itemIndex?` ${t+1}`:"");return o.qy`
          <div class="layout horizontal center-center row">
            <ha-textfield
              .suffix=${this.inputSuffix}
              .prefix=${this.inputPrefix}
              .type=${this.inputType}
              .autocomplete=${this.autocomplete}
              .disabled=${this.disabled}
              dialogInitialFocus=${t}
              .index=${t}
              class="flex-auto"
              .label=${""+(this.label?`${this.label}${i}`:"")}
              .value=${e}
              ?data-last=${t===this._items.length-1}
              @input=${this._editItem}
              @keydown=${this._keyDown}
            ></ha-textfield>
            <ha-icon-button
              .disabled=${this.disabled}
              .index=${t}
              slot="navigationIcon"
              .label=${this.removeLabel??this.hass?.localize("ui.common.remove")??"Remove"}
              @click=${this._removeItem}
              .path=${"M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z"}
            ></ha-icon-button>
          </div>
        `}))}
      <div class="layout horizontal center-center">
        <ha-button @click=${this._addItem} .disabled=${this.disabled}>
          ${this.addLabel??this.hass?.localize("ui.common.add")??"Add"}
          <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-button>
      </div>
    `}},{kind:"get",key:"_items",value:function(){return this.value??[]}},{kind:"method",key:"_addItem",value:async function(){const e=[...this._items,""];this._fireChanged(e),await this.updateComplete;const t=this.shadowRoot?.querySelector("ha-textfield[data-last]");t?.focus()}},{kind:"method",key:"_editItem",value:async function(e){const t=e.target.index,i=[...this._items];i[t]=e.target.value,this._fireChanged(i)}},{kind:"method",key:"_keyDown",value:async function(e){"Enter"===e.key&&(e.stopPropagation(),this._addItem())}},{kind:"method",key:"_removeItem",value:async function(e){const t=e.target.index,i=[...this._items];i.splice(t,1),this._fireChanged(i)}},{kind:"method",key:"_fireChanged",value:function(e){this.value=e,(0,r.r)(this,"value-changed",{value:e})}},{kind:"get",static:!0,key:"styles",value:function(){return[s.RF,o.AH`
        .row {
          margin-bottom: 8px;
        }
        ha-textfield {
          display: block;
        }
        ha-icon-button {
          display: block;
        }
        ha-button {
          margin-left: 8px;
          margin-inline-start: 8px;
          margin-inline-end: initial;
        }
      `]}}]}}),o.WF)},32283:(e,t,i)=>{var a=i(85461),o=i(78259),n=i(14414),r=i(98597),s=i(196);(0,a.A)([(0,s.EM)("ha-radio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[n.R,r.AH`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `]}}]}}),o.F)},96334:(e,t,i)=>{var a=i(85461),o=i(69534),n=i(32503),r=i(50988),s=i(98597),d=i(196),l=i(11355),c=i(45787);i(96396);(0,a.A)([(0,d.EM)("ha-select")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"icon",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean,reflect:!0})],key:"clearable",value(){return!1}},{kind:"method",key:"render",value:function(){return s.qy`
      ${(0,o.A)(i,"render",this,3)([])}
      ${this.clearable&&!this.required&&!this.disabled&&this.value?s.qy`<ha-icon-button
            label="clear"
            @click=${this._clearValue}
            .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
          ></ha-icon-button>`:s.s6}
    `}},{kind:"method",key:"renderLeadingIcon",value:function(){return this.icon?s.qy`<span class="mdc-select__icon"
      ><slot name="icon"></slot
    ></span>`:s.s6}},{kind:"method",key:"connectedCallback",value:function(){(0,o.A)(i,"connectedCallback",this,3)([]),window.addEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.A)(i,"disconnectedCallback",this,3)([]),window.removeEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"_clearValue",value:function(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}},{kind:"field",key:"_translationsUpdated",value(){return(0,l.s)((async()=>{await(0,c.E)(),this.layoutOptions()}),500)}},{kind:"field",static:!0,key:"styles",value(){return[r.R,s.AH`
      :host([clearable]) {
        position: relative;
      }
      .mdc-select:not(.mdc-select--disabled) .mdc-select__icon {
        color: var(--secondary-text-color);
      }
      .mdc-select__anchor {
        width: var(--ha-select-min-width, 200px);
      }
      .mdc-select--filled .mdc-select__anchor {
        height: var(--ha-select-height, 56px);
      }
      .mdc-select--filled .mdc-floating-label {
        inset-inline-start: 12px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label {
        inset-inline-start: 48px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select .mdc-select__anchor {
        padding-inline-start: 12px;
        padding-inline-end: 0px;
        direction: var(--direction);
      }
      .mdc-select__anchor .mdc-floating-label--float-above {
        transform-origin: var(--float-start);
      }
      .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 0px);
      }
      :host([clearable]) .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 12px);
      }
      ha-icon-button {
        position: absolute;
        top: 10px;
        right: 28px;
        --mdc-icon-button-size: 36px;
        --mdc-icon-size: 20px;
        color: var(--secondary-text-color);
        inset-inline-start: initial;
        inset-inline-end: 28px;
        direction: var(--direction);
      }
    `]}}]}}),n.o)},357:(e,t,i)=>{i.r(t),i.d(t,{HaNumberSelector:()=>d});var a=i(85461),o=i(98597),n=i(196),r=i(69760),s=i(33167);i(43689),i(53335),i(59373);let d=(0,a.A)([(0,n.EM)("ha-selector-number")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",key:"_valueStr",value(){return""}},{kind:"method",key:"willUpdate",value:function(e){e.has("value")&&(""!==this._valueStr&&this.value===Number(this._valueStr)||(this._valueStr=null==this.value||isNaN(this.value)?"":this.value.toString()))}},{kind:"method",key:"render",value:function(){const e="box"===this.selector.number?.mode||void 0===this.selector.number?.min||void 0===this.selector.number?.max;let t;if(!e&&(t=this.selector.number.step??1,"any"===t)){t=1;const e=(this.selector.number.max-this.selector.number.min)/100;for(;t>e;)t/=10}return o.qy`
      ${this.label&&!e?o.qy`${this.label}${this.required?"*":""}`:o.s6}
      <div class="input">
        ${e?o.s6:o.qy`
              <ha-slider
                labeled
                .min=${this.selector.number.min}
                .max=${this.selector.number.max}
                .value=${this.value??""}
                .step=${t}
                .disabled=${this.disabled}
                .required=${this.required}
                @change=${this._handleSliderChange}
                .ticks=${this.selector.number?.slider_ticks}
              >
              </ha-slider>
            `}
        <ha-textfield
          .inputMode=${"any"===this.selector.number?.step||(this.selector.number?.step??1)%1!=0?"decimal":"numeric"}
          .label=${e?this.label:void 0}
          .placeholder=${this.placeholder}
          class=${(0,r.H)({single:e})}
          .min=${this.selector.number?.min}
          .max=${this.selector.number?.max}
          .value=${this._valueStr??""}
          .step=${this.selector.number?.step??1}
          helperPersistent
          .helper=${e?this.helper:void 0}
          .disabled=${this.disabled}
          .required=${this.required}
          .suffix=${this.selector.number?.unit_of_measurement}
          type="number"
          autoValidate
          ?no-spinner=${!e}
          @input=${this._handleInputChange}
        >
        </ha-textfield>
      </div>
      ${!e&&this.helper?o.qy`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:o.s6}
    `}},{kind:"method",key:"_handleInputChange",value:function(e){e.stopPropagation(),this._valueStr=e.target.value;const t=""===e.target.value||isNaN(e.target.value)?void 0:Number(e.target.value);this.value!==t&&(0,s.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_handleSliderChange",value:function(e){e.stopPropagation();const t=Number(e.target.value);this.value!==t&&(0,s.r)(this,"value-changed",{value:t})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      .input {
        display: flex;
        justify-content: space-between;
        align-items: center;
        direction: ltr;
      }
      ha-slider {
        flex: 1;
        margin-right: 16px;
        margin-inline-end: 16px;
        margin-inline-start: 0;
      }
      ha-textfield {
        --ha-textfield-input-width: 40px;
      }
      .single {
        --ha-textfield-input-width: unset;
        flex: 1;
      }
    `}}]}}),o.WF)},33768:(e,t,i)=>{i.r(t),i.d(t,{HaSelectSelector:()=>h});var a=i(85461),o=(i(23981),i(98597)),n=i(196),r=i(66580),s=i(96041),d=i(33167),l=i(24517),c=i(66412);i(73409),i(28331),i(19887),i(66442),i(32694),i(43689),i(32283),i(96334),i(69154);let h=(0,a.A)([(0,n.EM)("ha-selector-select")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"method",key:"_itemMoved",value:function(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail;this._move(t,i)}},{kind:"method",key:"_move",value:function(e,t){const i=this.value.concat(),a=i.splice(e,1)[0];i.splice(t,0,a),this.value=i,(0,d.r)(this,"value-changed",{value:i})}},{kind:"field",key:"_filter",value(){return""}},{kind:"method",key:"render",value:function(){const e=this.selector.select?.options?.map((e=>"object"==typeof e?e:{value:e,label:e}))||[],t=this.selector.select?.translation_key;if(this.localizeValue&&t&&e.forEach((e=>{const i=this.localizeValue(`${t}.options.${e.value}`);i&&(e.label=i)})),this.selector.select?.sort&&e.sort(((e,t)=>(0,c.S)(e.label,t.label,this.hass.locale.language))),!this.selector.select?.custom_value&&!this.selector.select?.reorder&&"list"===this._mode){if(!this.selector.select?.multiple)return o.qy`
          <div>
            ${this.label}
            ${e.map((e=>o.qy`
                <ha-formfield
                  .label=${e.label}
                  .disabled=${e.disabled||this.disabled}
                >
                  <ha-radio
                    .checked=${e.value===this.value}
                    .value=${e.value}
                    .disabled=${e.disabled||this.disabled}
                    @change=${this._valueChanged}
                  ></ha-radio>
                </ha-formfield>
              `))}
          </div>
          ${this._renderHelper()}
        `;const t=this.value&&""!==this.value?(0,s.e)(this.value):[];return o.qy`
        <div>
          ${this.label}
          ${e.map((e=>o.qy`
              <ha-formfield .label=${e.label}>
                <ha-checkbox
                  .checked=${t.includes(e.value)}
                  .value=${e.value}
                  .disabled=${e.disabled||this.disabled}
                  @change=${this._checkboxChanged}
                ></ha-checkbox>
              </ha-formfield>
            `))}
        </div>
        ${this._renderHelper()}
      `}if(this.selector.select?.multiple){const t=this.value&&""!==this.value?(0,s.e)(this.value):[],i=e.filter((e=>!e.disabled&&!t?.includes(e.value)));return o.qy`
        ${t?.length?o.qy`
              <ha-sortable
                no-style
                .disabled=${!this.selector.select.reorder}
                @item-moved=${this._itemMoved}
              >
                <ha-chip-set>
                  ${(0,r.u)(t,(e=>e),((t,i)=>{const a=e.find((e=>e.value===t))?.label||t;return o.qy`
                        <ha-input-chip
                          .idx=${i}
                          @remove=${this._removeItem}
                          .label=${a}
                          selected
                        >
                          ${this.selector.select?.reorder?o.qy`
                                <ha-svg-icon
                                  slot="icon"
                                  .path=${"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"}
                                  data-handle
                                ></ha-svg-icon>
                              `:o.s6}
                          ${e.find((e=>e.value===t))?.label||t}
                        </ha-input-chip>
                      `}))}
                </ha-chip-set>
              </ha-sortable>
            `:o.s6}

        <ha-combo-box
          item-value-path="value"
          item-label-path="label"
          .hass=${this.hass}
          .label=${this.label}
          .helper=${this.helper}
          .disabled=${this.disabled}
          .required=${this.required&&!t.length}
          .value=${""}
          .items=${i}
          .allowCustomValue=${this.selector.select.custom_value??!1}
          @filter-changed=${this._filterChanged}
          @value-changed=${this._comboBoxValueChanged}
          @opened-changed=${this._openedChanged}
        ></ha-combo-box>
      `}if(this.selector.select?.custom_value){void 0===this.value||Array.isArray(this.value)||e.find((e=>e.value===this.value))||e.unshift({value:this.value,label:this.value});const t=e.filter((e=>!e.disabled));return o.qy`
        <ha-combo-box
          item-value-path="value"
          item-label-path="label"
          .hass=${this.hass}
          .label=${this.label}
          .helper=${this.helper}
          .disabled=${this.disabled}
          .required=${this.required}
          .items=${t}
          .value=${this.value}
          @filter-changed=${this._filterChanged}
          @value-changed=${this._comboBoxValueChanged}
          @opened-changed=${this._openedChanged}
        ></ha-combo-box>
      `}return o.qy`
      <ha-select
        fixedMenuPosition
        naturalMenuWidth
        .label=${this.label??""}
        .value=${this.value??""}
        .helper=${this.helper??""}
        .disabled=${this.disabled}
        .required=${this.required}
        clearable
        @closed=${l.d}
        @selected=${this._valueChanged}
      >
        ${e.map((e=>o.qy`
            <mwc-list-item .value=${e.value} .disabled=${e.disabled}
              >${e.label}</mwc-list-item
            >
          `))}
      </ha-select>
    `}},{kind:"method",key:"_renderHelper",value:function(){return this.helper?o.qy`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}},{kind:"get",key:"_mode",value:function(){return this.selector.select?.mode||((this.selector.select?.options?.length||0)<6?"list":"dropdown")}},{kind:"method",key:"_valueChanged",value:function(e){if(e.stopPropagation(),-1===e.detail?.index&&void 0!==this.value)return void(0,d.r)(this,"value-changed",{value:void 0});const t=e.detail?.value||e.target.value;this.disabled||void 0===t||t===(this.value??"")||(0,d.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_checkboxChanged",value:function(e){if(e.stopPropagation(),this.disabled)return;let t;const i=e.target.value,a=e.target.checked,o=this.value&&""!==this.value?(0,s.e)(this.value):[];if(a){if(o.includes(i))return;t=[...o,i]}else{if(!o?.includes(i))return;t=o.filter((e=>e!==i))}(0,d.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_removeItem",value:async function(e){e.stopPropagation();const t=[...(0,s.e)(this.value)];t.splice(e.target.idx,1),(0,d.r)(this,"value-changed",{value:t}),await this.updateComplete,this._filterChanged()}},{kind:"method",key:"_comboBoxValueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(this.disabled||""===t)return;if(!this.selector.select?.multiple)return void(0,d.r)(this,"value-changed",{value:t});const i=this.value&&""!==this.value?(0,s.e)(this.value):[];void 0!==t&&i.includes(t)||(setTimeout((()=>{this._filterChanged(),this.comboBox.setInputValue("")}),0),(0,d.r)(this,"value-changed",{value:[...i,t]}))}},{kind:"method",key:"_openedChanged",value:function(e){e?.detail.value&&this._filterChanged()}},{kind:"method",key:"_filterChanged",value:function(e){this._filter=e?.detail.value||"";const t=this.comboBox.items?.filter((e=>(e.label||e.value).toLowerCase().includes(this._filter?.toLowerCase())));this._filter&&this.selector.select?.custom_value&&t&&!t.some((e=>(e.label||e.value)===this._filter))&&t.unshift({label:this._filter,value:this._filter}),this.comboBox.filteredItems=t}},{kind:"field",static:!0,key:"styles",value(){return o.AH`
    :host {
      position: relative;
    }
    ha-select,
    mwc-formfield,
    ha-formfield {
      display: block;
    }
    mwc-list-item[disabled] {
      --mdc-theme-text-primary-on-background: var(--disabled-text-color);
    }
    ha-chip-set {
      padding: 8px 0;
    }

    .sortable-fallback {
      display: none;
      opacity: 0;
    }

    .sortable-ghost {
      opacity: 0.4;
    }

    .sortable-drag {
      cursor: grabbing;
    }
  `}}]}}),o.WF)},74259:(e,t,i)=>{i.r(t),i.d(t,{HaTextSelector:()=>d});var a=i(85461),o=i(98597),n=i(196),r=i(96041),s=i(33167);i(96396),i(26589),i(77984),i(59373);let d=(0,a.A)([(0,n.EM)("ha-selector-text")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"name",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.wk)()],key:"_unmaskedPassword",value(){return!1}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,this.renderRoot.querySelector("ha-textarea, ha-textfield")?.focus()}},{kind:"method",key:"render",value:function(){return this.selector.text?.multiple?o.qy`
        <ha-multi-textfield
          .hass=${this.hass}
          .value=${(0,r.e)(this.value??[])}
          .disabled=${this.disabled}
          .label=${this.label}
          .inputType=${this.selector.text?.type}
          .inputSuffix=${this.selector.text?.suffix}
          .inputPrefix=${this.selector.text?.prefix}
          .autocomplete=${this.selector.text?.autocomplete}
          @value-changed=${this._handleChange}
        >
        </ha-multi-textfield>
      `:this.selector.text?.multiline?o.qy`<ha-textarea
        .name=${this.name}
        .label=${this.label}
        .placeholder=${this.placeholder}
        .value=${this.value||""}
        .helper=${this.helper}
        helperPersistent
        .disabled=${this.disabled}
        @input=${this._handleChange}
        autocapitalize="none"
        .autocomplete=${this.selector.text?.autocomplete}
        spellcheck="false"
        .required=${this.required}
        autogrow
      ></ha-textarea>`:o.qy`<ha-textfield
        .name=${this.name}
        .value=${this.value||""}
        .placeholder=${this.placeholder||""}
        .helper=${this.helper}
        helperPersistent
        .disabled=${this.disabled}
        .type=${this._unmaskedPassword?"text":this.selector.text?.type}
        @input=${this._handleChange}
        @change=${this._handleChange}
        .label=${this.label||""}
        .prefix=${this.selector.text?.prefix}
        .suffix=${"password"===this.selector.text?.type?o.qy`<div style="width: 24px"></div>`:this.selector.text?.suffix}
        .required=${this.required}
        .autocomplete=${this.selector.text?.autocomplete}
      ></ha-textfield>
      ${"password"===this.selector.text?.type?o.qy`<ha-icon-button
            toggles
            .label=${this.hass?.localize(this._unmaskedPassword?"ui.components.selectors.text.hide_password":"ui.components.selectors.text.show_password")||(this._unmaskedPassword?"Hide password":"Show password")}
            @click=${this._toggleUnmaskedPassword}
            .path=${this._unmaskedPassword?"M11.83,9L15,12.16C15,12.11 15,12.05 15,12A3,3 0 0,0 12,9C11.94,9 11.89,9 11.83,9M7.53,9.8L9.08,11.35C9.03,11.56 9,11.77 9,12A3,3 0 0,0 12,15C12.22,15 12.44,14.97 12.65,14.92L14.2,16.47C13.53,16.8 12.79,17 12,17A5,5 0 0,1 7,12C7,11.21 7.2,10.47 7.53,9.8M2,4.27L4.28,6.55L4.73,7C3.08,8.3 1.78,10 1,12C2.73,16.39 7,19.5 12,19.5C13.55,19.5 15.03,19.2 16.38,18.66L16.81,19.08L19.73,22L21,20.73L3.27,3M12,7A5,5 0 0,1 17,12C17,12.64 16.87,13.26 16.64,13.82L19.57,16.75C21.07,15.5 22.27,13.86 23,12C21.27,7.61 17,4.5 12,4.5C10.6,4.5 9.26,4.75 8,5.2L10.17,7.35C10.74,7.13 11.35,7 12,7Z":"M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z"}
          ></ha-icon-button>`:""}`}},{kind:"method",key:"_toggleUnmaskedPassword",value:function(){this._unmaskedPassword=!this._unmaskedPassword}},{kind:"method",key:"_handleChange",value:function(e){let t=e.detail?.value??e.target.value;this.value!==t&&((""===t||Array.isArray(t)&&0===t.length)&&!this.required&&(t=void 0),(0,s.r)(this,"value-changed",{value:t}))}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        display: block;
        position: relative;
      }
      ha-textarea,
      ha-textfield {
        width: 100%;
      }
      ha-icon-button {
        position: absolute;
        top: 8px;
        right: 8px;
        inset-inline-start: initial;
        inset-inline-end: 8px;
        --mdc-icon-button-size: 40px;
        --mdc-icon-size: 20px;
        color: var(--secondary-text-color);
        direction: var(--direction);
      }
    `}}]}}),o.WF)},52631:(e,t,i)=>{var a=i(85461),o=i(98597),n=i(196),r=i(45081),s=i(90662),d=i(36831);const l={action:()=>Promise.all([i.e(5175),i.e(614),i.e(4538),i.e(5426),i.e(2159),i.e(6376),i.e(7417),i.e(4314),i.e(6862),i.e(8957),i.e(4776)]).then(i.bind(i,54776)),addon:()=>i.e(5519).then(i.bind(i,55519)),area:()=>i.e(5853).then(i.bind(i,95853)),area_filter:()=>i.e(3983).then(i.bind(i,23983)),attribute:()=>Promise.all([i.e(2159),i.e(3330)]).then(i.bind(i,88136)),assist_pipeline:()=>i.e(7674).then(i.bind(i,97674)),boolean:()=>i.e(7562).then(i.bind(i,67562)),color_rgb:()=>i.e(4147).then(i.bind(i,74147)),condition:()=>Promise.all([i.e(5175),i.e(4538),i.e(5426),i.e(2159),i.e(6376),i.e(4314),i.e(4801)]).then(i.bind(i,95187)),config_entry:()=>i.e(543).then(i.bind(i,10543)),conversation_agent:()=>i.e(7701).then(i.bind(i,7701)),constant:()=>i.e(4088).then(i.bind(i,94088)),country:()=>i.e(2119).then(i.bind(i,22119)),date:()=>i.e(1596).then(i.bind(i,11596)),datetime:()=>i.e(4117).then(i.bind(i,64117)),device:()=>i.e(2939).then(i.bind(i,12939)),duration:()=>i.e(4304).then(i.bind(i,24304)),entity:()=>Promise.all([i.e(4538),i.e(5426),i.e(3069)]).then(i.bind(i,73133)),statistic:()=>Promise.all([i.e(4538),i.e(5426),i.e(9920)]).then(i.bind(i,64886)),file:()=>i.e(582).then(i.bind(i,40582)),floor:()=>i.e(716).then(i.bind(i,90716)),label:()=>Promise.all([i.e(9549),i.e(4817)]).then(i.bind(i,95576)),image:()=>i.e(3399).then(i.bind(i,43399)),language:()=>i.e(1670).then(i.bind(i,71670)),navigation:()=>i.e(14).then(i.bind(i,90014)),number:()=>Promise.resolve().then(i.bind(i,357)),object:()=>i.e(367).then(i.bind(i,20367)),qr_code:()=>Promise.all([i.e(8345),i.e(8353)]).then(i.bind(i,48353)),select:()=>Promise.resolve().then(i.bind(i,33768)),selector:()=>i.e(8985).then(i.bind(i,28985)),state:()=>i.e(8628).then(i.bind(i,58628)),backup_location:()=>i.e(518).then(i.bind(i,30518)),stt:()=>i.e(7263).then(i.bind(i,87263)),target:()=>Promise.all([i.e(2457),i.e(4538),i.e(5426),i.e(2537)]).then(i.bind(i,20513)),template:()=>i.e(4806).then(i.bind(i,4806)),text:()=>Promise.resolve().then(i.bind(i,74259)),time:()=>i.e(6401).then(i.bind(i,36401)),icon:()=>Promise.all([i.e(4538),i.e(8709)]).then(i.bind(i,18709)),media:()=>Promise.all([i.e(8957),i.e(8387)]).then(i.bind(i,28957)),theme:()=>i.e(4206).then(i.bind(i,64206)),trigger:()=>Promise.all([i.e(5175),i.e(4538),i.e(5426),i.e(2159),i.e(6376),i.e(7417),i.e(6924)]).then(i.bind(i,41382)),tts:()=>i.e(2808).then(i.bind(i,62808)),tts_voice:()=>i.e(1940).then(i.bind(i,1940)),location:()=>i.e(3391).then(i.bind(i,63391)),color_temp:()=>Promise.all([i.e(9540),i.e(6249)]).then(i.bind(i,16249)),ui_action:()=>Promise.all([i.e(2673),i.e(4538),i.e(6862),i.e(7519)]).then(i.bind(i,43368)),ui_color:()=>i.e(5608).then(i.bind(i,15608)),ui_state_content:()=>Promise.all([i.e(4241),i.e(1503),i.e(4540)]).then(i.bind(i,72159))},c=new Set(["ui-action","ui-color"]);(0,a.A)([(0,n.EM)("ha-selector")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"name",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"focus",value:async function(){await this.updateComplete,this.renderRoot.querySelector("#selector")?.focus()}},{kind:"get",key:"_type",value:function(){const e=Object.keys(this.selector)[0];return c.has(e)?e.replace("-","_"):e}},{kind:"method",key:"willUpdate",value:function(e){e.has("selector")&&this.selector&&l[this._type]?.()}},{kind:"field",key:"_handleLegacySelector",value(){return(0,r.A)((e=>{if("entity"in e)return(0,d.UU)(e);if("device"in e)return(0,d.tD)(e);const t=Object.keys(this.selector)[0];return c.has(t)?{[t.replace("-","_")]:e[t]}:e}))}},{kind:"method",key:"render",value:function(){return o.qy`
      ${(0,s._)(`ha-selector-${this._type}`,{hass:this.hass,name:this.name,selector:this._handleLegacySelector(this.selector),value:this.value,label:this.label,placeholder:this.placeholder,disabled:this.disabled,required:this.required,helper:this.helper,context:this.context,localizeValue:this.localizeValue,id:"selector"})}
    `}}]}}),o.WF)},93650:(e,t,i)=>{var a=i(85461),o=i(98597),n=i(196);(0,a.A)([(0,n.EM)("ha-settings-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"slim",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"three-line"})],key:"threeLine",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"wrap-heading",reflect:!0})],key:"wrapHeading",value(){return!1}},{kind:"method",key:"render",value:function(){return o.qy`
      <div class="prefix-wrap">
        <slot name="prefix"></slot>
        <div
          class="body"
          ?two-line=${!this.threeLine}
          ?three-line=${this.threeLine}
        >
          <slot name="heading"></slot>
          <div class="secondary"><slot name="description"></slot></div>
        </div>
      </div>
      <div class="content"><slot></slot></div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        display: flex;
        padding: 0 16px;
        align-content: normal;
        align-self: auto;
        align-items: center;
      }
      .body {
        padding-top: 8px;
        padding-bottom: 8px;
        padding-left: 0;
        padding-inline-start: 0;
        padding-right: 16px;
        padding-inline-end: 16px;
        overflow: hidden;
        display: var(--layout-vertical_-_display, flex);
        flex-direction: var(--layout-vertical_-_flex-direction, column);
        justify-content: var(
          --layout-center-justified_-_justify-content,
          center
        );
        flex: var(--layout-flex_-_flex, 1);
        flex-basis: var(--layout-flex_-_flex-basis, 0.000000001px);
      }
      .body[three-line] {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }
      :host(:not([wrap-heading])) body > * {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      .body > .secondary {
        display: block;
        padding-top: 4px;
        font-family: var(
          --mdc-typography-body2-font-family,
          var(--mdc-typography-font-family, Roboto, sans-serif)
        );
        -webkit-font-smoothing: antialiased;
        font-size: var(--mdc-typography-body2-font-size, 0.875rem);
        font-weight: var(--mdc-typography-body2-font-weight, 400);
        line-height: normal;
        color: var(--secondary-text-color);
      }
      .body[two-line] {
        min-height: calc(
          var(--paper-item-body-two-line-min-height, 72px) - 16px
        );
        flex: 1;
      }
      .content {
        display: contents;
      }
      :host(:not([narrow])) .content {
        display: var(--settings-row-content-display, flex);
        justify-content: flex-end;
        flex: 1;
        padding: 16px 0;
      }
      .content ::slotted(*) {
        width: var(--settings-row-content-width);
      }
      :host([narrow]) {
        align-items: normal;
        flex-direction: column;
        border-top: 1px solid var(--divider-color);
        padding-bottom: 8px;
      }
      ::slotted(ha-switch) {
        padding: 16px 0;
      }
      .secondary {
        white-space: normal;
      }
      .prefix-wrap {
        display: var(--settings-row-prefix-display);
      }
      :host([narrow]) .prefix-wrap {
        display: flex;
        align-items: center;
      }
      :host([slim]),
      :host([slim]) .content,
      :host([slim]) ::slotted(ha-switch) {
        padding: 0;
      }
      :host([slim]) .body {
        min-height: 0;
      }
    `}}]}}),o.WF)},53335:(e,t,i)=>{var a=i(85461),o=i(69534),n=i(30885),r=i(98597),s=i(196),d=i(10);(0,a.A)([(0,s.EM)("ha-slider")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"connectedCallback",value:function(){(0,o.A)(i,"connectedCallback",this,3)([]),this.dir=d.G.document.dir}},{kind:"field",static:!0,key:"styles",value(){return[...(0,o.A)(i,"styles",this),r.AH`
      :host {
        --md-sys-color-primary: var(--primary-color);
        --md-sys-color-on-primary: var(--text-primary-color);
        --md-sys-color-outline: var(--outline-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-slider-handle-width: 14px;
        --md-slider-handle-height: 14px;
        --md-slider-state-layer-size: 24px;
        min-width: 100px;
        min-inline-size: 100px;
        width: 200px;
      }
    `]}}]}}),n.$)},69154:(e,t,i)=>{var a=i(85461),o=i(69534),n=i(98597),r=i(196),s=i(33167);(0,a.A)([(0,r.EM)("ha-sortable")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",key:"_sortable",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"no-style"})],key:"noStyle",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:String,attribute:"draggable-selector"})],key:"draggableSelector",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:String,attribute:"handle-selector"})],key:"handleSelector",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:String,attribute:"filter"})],key:"filter",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:String})],key:"group",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"invert-swap"})],key:"invertSwap",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"rollback",value(){return!0}},{kind:"method",key:"updated",value:function(e){e.has("disabled")&&(this.disabled?this._destroySortable():this._createSortable())}},{kind:"field",key:"_shouldBeDestroy",value(){return!1}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.A)(a,"disconnectedCallback",this,3)([]),this._shouldBeDestroy=!0,setTimeout((()=>{this._shouldBeDestroy&&(this._destroySortable(),this._shouldBeDestroy=!1)}),1)}},{kind:"method",key:"connectedCallback",value:function(){(0,o.A)(a,"connectedCallback",this,3)([]),this._shouldBeDestroy=!1,this.hasUpdated&&!this.disabled&&this._createSortable()}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"render",value:function(){return this.noStyle?n.s6:n.qy`
      <style>
        .sortable-fallback {
          display: none !important;
        }

        .sortable-ghost {
          box-shadow: 0 0 0 2px var(--primary-color);
          background: rgba(var(--rgb-primary-color), 0.25);
          border-radius: 4px;
          opacity: 0.4;
        }

        .sortable-drag {
          border-radius: 4px;
          opacity: 1;
          background: var(--card-background-color);
          box-shadow: 0px 4px 8px 3px #00000026;
          cursor: grabbing;
        }
      </style>
    `}},{kind:"method",key:"_createSortable",value:async function(){if(this._sortable)return;const e=this.children[0];if(!e)return;const t=(await Promise.all([i.e(8681),i.e(2617)]).then(i.bind(i,2617))).default,a={scroll:!0,forceAutoScrollFallback:!0,scrollSpeed:20,animation:150,...this.options,onChoose:this._handleChoose,onStart:this._handleStart,onEnd:this._handleEnd,onUpdate:this._handleUpdate,onAdd:this._handleAdd,onRemove:this._handleRemove};this.draggableSelector&&(a.draggable=this.draggableSelector),this.handleSelector&&(a.handle=this.handleSelector),void 0!==this.invertSwap&&(a.invertSwap=this.invertSwap),this.group&&(a.group=this.group),this.filter&&(a.filter=this.filter),this._sortable=new t(e,a)}},{kind:"field",key:"_handleUpdate",value(){return e=>{(0,s.r)(this,"item-moved",{newIndex:e.newIndex,oldIndex:e.oldIndex})}}},{kind:"field",key:"_handleAdd",value(){return e=>{(0,s.r)(this,"item-added",{index:e.newIndex,data:e.item.sortableData})}}},{kind:"field",key:"_handleRemove",value(){return e=>{(0,s.r)(this,"item-removed",{index:e.oldIndex})}}},{kind:"field",key:"_handleEnd",value(){return async e=>{(0,s.r)(this,"drag-end"),this.rollback&&e.item.placeholder&&(e.item.placeholder.replaceWith(e.item),delete e.item.placeholder)}}},{kind:"field",key:"_handleStart",value(){return()=>{(0,s.r)(this,"drag-start")}}},{kind:"field",key:"_handleChoose",value(){return e=>{this.rollback&&(e.item.placeholder=document.createComment("sort-placeholder"),e.item.after(e.item.placeholder))}}},{kind:"method",key:"_destroySortable",value:function(){this._sortable&&(this._sortable.destroy(),this._sortable=void 0)}}]}}),n.WF)},77984:(e,t,i)=>{var a=i(85461),o=i(69534),n=i(47451),r=i(65050),s=i(72692),d=i(98597),l=i(196);(0,a.A)([(0,l.EM)("ha-textarea")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.MZ)({type:Boolean,reflect:!0})],key:"autogrow",value(){return!1}},{kind:"method",key:"updated",value:function(e){(0,o.A)(i,"updated",this,3)([e]),this.autogrow&&e.has("value")&&(this.mdcRoot.dataset.value=this.value+'=​"')}},{kind:"field",static:!0,key:"styles",value(){return[r.R,s.R,d.AH`
      :host([autogrow]) .mdc-text-field {
        position: relative;
        min-height: 74px;
        min-width: 178px;
        max-height: 200px;
      }
      :host([autogrow]) .mdc-text-field:after {
        content: attr(data-value);
        margin-top: 23px;
        margin-bottom: 9px;
        line-height: 1.5rem;
        min-height: 42px;
        padding: 0px 32px 0 16px;
        letter-spacing: var(
          --mdc-typography-subtitle1-letter-spacing,
          0.009375em
        );
        visibility: hidden;
        white-space: pre-wrap;
      }
      :host([autogrow]) .mdc-text-field__input {
        position: absolute;
        height: calc(100% - 32px);
      }
      :host([autogrow]) .mdc-text-field.mdc-text-field--no-label:after {
        margin-top: 16px;
        margin-bottom: 16px;
      }
      .mdc-floating-label {
        inset-inline-start: 16px !important;
        inset-inline-end: initial !important;
        transform-origin: var(--float-start) top;
      }
    `]}}]}}),n.u)},13473:(e,t,i)=>{i.d(t,{L3:()=>o,dj:()=>r,gs:()=>n});var a=i(66412);i(99812);const o=(e,t)=>e.callWS({type:"config/area_registry/create",...t}),n=(e,t,i)=>e.callWS({type:"config/area_registry/update",area_id:t,...i}),r=(e,t)=>(i,o)=>{const n=t?t.indexOf(i):-1,r=t?t.indexOf(o):-1;if(-1===n&&-1===r){const t=e?.[i]?.name??i,n=e?.[o]?.name??o;return(0,a.x)(t,n)}return-1===n?1:-1===r?-1:n-r}},40884:(e,t,i)=>{i.d(t,{FB:()=>n,fk:()=>s,g2:()=>r,xn:()=>o});var a=i(91330);i(66412);const o=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,o=e.states[t];if(o)return(0,a.u)(o)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device",{type:t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)}),n=(e,t,i)=>e.callWS({type:"config/device_registry/update",device_id:t,...i}),r=e=>{const t={};for(const i of e)i.device_id&&(i.device_id in t||(t[i.device_id]=[]),t[i.device_id].push(i));return t},s=(e,t,i,a)=>{const o={};for(const n of t){const t=e[n.entity_id];t?.domain&&null!==n.device_id&&(o[n.device_id]=o[n.device_id]||new Set,o[n.device_id].add(t.domain))}if(i&&a)for(const n of i)for(const e of n.config_entries){const t=a.find((t=>t.entry_id===e));t?.domain&&(o[n.id]=o[n.id]||new Set,o[n.id].add(t.domain))}return o}},36831:(e,t,i)=>{i.d(t,{DF:()=>p,Lo:()=>k,MH:()=>l,MM:()=>v,Qz:()=>u,Ru:()=>g,UU:()=>f,_7:()=>h,bZ:()=>c,m0:()=>d,tD:()=>y,vX:()=>m});var a=i(96041),o=i(80085),n=i(60222),r=i(23135),s=i(40884);const d=(e,t,i,a,o,n,r)=>{const s=[],d=[],l=[];return Object.values(i).forEach((i=>{i.labels.includes(t)&&u(e,o,a,i.area_id,n,r)&&l.push(i.area_id)})),Object.values(a).forEach((i=>{i.labels.includes(t)&&p(e,Object.values(o),i,n,r)&&d.push(i.id)})),Object.values(o).forEach((i=>{i.labels.includes(t)&&v(e.states[i.entity_id],n,r)&&s.push(i.entity_id)})),{areas:l,devices:d,entities:s}},l=(e,t,i,a,o)=>{const n=[];return Object.values(i).forEach((i=>{i.floor_id===t&&u(e,e.entities,e.devices,i.area_id,a,o)&&n.push(i.area_id)})),{areas:n}},c=(e,t,i,a,o,n)=>{const r=[],s=[];return Object.values(i).forEach((i=>{i.area_id===t&&p(e,Object.values(a),i,o,n)&&s.push(i.id)})),Object.values(a).forEach((i=>{i.area_id===t&&v(e.states[i.entity_id],o,n)&&r.push(i.entity_id)})),{devices:s,entities:r}},h=(e,t,i,a,o)=>{const n=[];return Object.values(i).forEach((i=>{i.device_id===t&&v(e.states[i.entity_id],a,o)&&n.push(i.entity_id)})),{entities:n}},u=(e,t,i,a,o,n)=>!!Object.values(i).some((i=>!(i.area_id!==a||!p(e,Object.values(t),i,o,n))))||Object.values(t).some((t=>!(t.area_id!==a||!v(e.states[t.entity_id],o,n)))),p=(e,t,i,o,n)=>{const r=n?(0,s.fk)(n,t):void 0;if(o.target?.device&&!(0,a.e)(o.target.device).some((e=>m(e,i,r))))return!1;if(o.target?.entity){return t.filter((e=>e.device_id===i.id)).some((t=>{const i=e.states[t.entity_id];return v(i,o,n)}))}return!0},v=(e,t,i)=>!t.target?.entity||(0,a.e)(t.target.entity).some((t=>g(t,e,i))),m=(e,t,i)=>{const{manufacturer:a,model:o,integration:n}=e;return(!a||t.manufacturer===a)&&((!o||t.model===o)&&!(n&&i&&!i?.[t.id]?.has(n)))},g=(e,t,i)=>{const{domain:r,device_class:s,supported_features:d,integration:l}=e;if(r){const e=(0,o.t)(t);if(Array.isArray(r)?!r.includes(e):e!==r)return!1}if(s){const e=t.attributes.device_class;if(e&&Array.isArray(s)?!s.includes(e):e!==s)return!1}return!(d&&!(0,a.e)(d).some((e=>(0,n.$)(t,e))))&&(!l||i?.[t.entity_id]?.domain===l)},f=e=>{if(!e.entity)return{entity:null};if("filter"in e.entity)return e;const{domain:t,integration:i,device_class:a,...o}=e.entity;return t||i||a?{entity:{...o,filter:{domain:t,integration:i,device_class:a}}}:{entity:o}},y=e=>{if(!e.device)return{device:null};if("filter"in e.device)return e;const{integration:t,manufacturer:i,model:a,...o}=e.device;return t||i||a?{device:{...o,filter:{integration:t,manufacturer:i,model:a}}}:{device:o}},k=e=>{let t;if("target"in e)t=(0,a.e)(e.target?.entity);else if("entity"in e){if(e.entity?.include_entities)return;t=(0,a.e)(e.entity?.filter)}if(!t)return;const i=t.flatMap((e=>e.integration||e.device_class||e.supported_features||!e.domain?[]:(0,a.e)(e.domain).filter((e=>(0,r.z)(e)))));return[...new Set(i)]}},99812:(e,t,i)=>{i(66412)},83895:(e,t,i)=>{i.d(t,{J:()=>n});var a=i(33167);const o=()=>Promise.all([i.e(3895),i.e(9549),i.e(7860),i.e(2011)]).then(i.bind(i,72011)),n=(e,t)=>{(0,a.r)(e,"show-dialog",{dialogTag:"dialog-area-registry-detail",dialogImport:o,dialogParams:t})}},23135:(e,t,i)=>{i.d(t,{z:()=>a});const a=(0,i(79592).g)(["input_boolean","input_button","input_text","input_number","input_datetime","input_select","counter","timer","schedule"])},23059:(e,t,i)=>{i.d(t,{V:()=>n,e:()=>o});var a=i(47420);const o={payload:e=>null==e.payload?"":Array.isArray(e.payload)?e.payload.reduce(((e,t)=>e+t.toString(16).padStart(2,"0")),"0x"):e.payload.toString(),valueWithUnit:e=>null==e.value?"":"number"==typeof e.value||"boolean"==typeof e.value||"string"==typeof e.value?e.value.toString()+(e.unit?" "+e.unit:""):(0,a.Bh)(e.value),timeWithMilliseconds:e=>new Date(e.timestamp).toLocaleTimeString(["en-US"],{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dateWithMilliseconds:e=>new Date(e.timestamp).toLocaleTimeString([],{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dptNumber:e=>null==e.dpt_main?"":null==e.dpt_sub?e.dpt_main.toString():e.dpt_main.toString()+"."+e.dpt_sub.toString().padStart(3,"0"),dptNameNumber:e=>{const t=o.dptNumber(e);return null==e.dpt_name?`DPT ${t}`:t?`DPT ${t} ${e.dpt_name}`:e.dpt_name}},n=e=>null==e?"":e.main+(e.sub?"."+e.sub.toString().padStart(3,"0"):"")},70178:(e,t,i)=>{i.r(t),i.d(t,{KNXCreateEntity:()=>j});var a=i(85461),o=i(98597),n=i(196),r=i(26349),s=(i(61424),i(97626)),d=(i(92312),i(32010),i(43799));(0,a.A)([(0,n.EM)("hass-subpage")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"header",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"main-page"})],key:"mainPage",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"supervisor",value(){return!1}},{kind:"field",decorators:[(0,s.a)(".content")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"render",value:function(){return o.qy`
      <div class="toolbar">
        ${this.mainPage||history.state?.root?o.qy`
              <ha-menu-button
                .hassio=${this.supervisor}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:this.backPath?o.qy`
                <a href=${this.backPath}>
                  <ha-icon-button-arrow-prev
                    .hass=${this.hass}
                  ></ha-icon-button-arrow-prev>
                </a>
              `:o.qy`
                <ha-icon-button-arrow-prev
                  .hass=${this.hass}
                  @click=${this._backTapped}
                ></ha-icon-button-arrow-prev>
              `}

        <div class="main-title"><slot name="header">${this.header}</slot></div>
        <slot name="toolbar-icon"></slot>
      </div>
      <div class="content ha-scrollbar" @scroll=${this._saveScrollPos}>
        <slot></slot>
      </div>
      <div id="fab">
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[(0,n.Ls)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[d.dp,o.AH`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
          overflow: hidden;
          position: relative;
        }

        :host([narrow]) {
          width: 100%;
          position: fixed;
        }

        .toolbar {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: var(--header-height);
          padding: 8px 12px;
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
        .toolbar a {
          color: var(--sidebar-text-color);
          text-decoration: none;
        }

        ha-menu-button,
        ha-icon-button-arrow-prev,
        ::slotted([slot="toolbar-icon"]) {
          pointer-events: auto;
          color: var(--sidebar-icon-color);
        }

        .main-title {
          margin: var(--margin-title);
          line-height: 20px;
          min-width: 0;
          flex-grow: 1;
          overflow-wrap: break-word;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
          text-overflow: ellipsis;
          padding-bottom: 1px;
        }

        .content {
          position: relative;
          width: 100%;
          height: calc(100% - 1px - var(--header-height));
          overflow-y: auto;
          overflow: auto;
          -webkit-overflow-scrolling: touch;
        }

        #fab {
          position: absolute;
          right: calc(16px + env(safe-area-inset-right));
          inset-inline-end: calc(16px + env(safe-area-inset-right));
          inset-inline-start: initial;
          bottom: calc(16px + env(safe-area-inset-bottom));
          z-index: 1;
          display: flex;
          flex-wrap: wrap;
          justify-content: flex-end;
          gap: 8px;
        }
        :host([narrow]) #fab.tabs {
          bottom: calc(84px + env(safe-area-inset-bottom));
        }
        #fab[is-wide] {
          bottom: 24px;
          right: 24px;
          inset-inline-end: 24px;
          inset-inline-start: initial;
        }
      `]}}]}}),o.WF);i(91074),i(94392),i(97661),i(29222),i(29805);var l=i(79278),c=i(13314);i(94333),i(9484);(0,a.A)([(0,n.EM)("ha-navigation-list")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"pages",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"hasSecondary",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"method",key:"render",value:function(){return o.qy`
      <mwc-list
        innerRole="menu"
        itemRoles="menuitem"
        innerAriaLabel=${(0,l.J)(this.label)}
        @action=${this._handleListAction}
      >
        ${this.pages.map((e=>o.qy`
            <ha-list-item
              graphic="avatar"
              .twoline=${this.hasSecondary}
              .hasMeta=${!this.narrow}
            >
              <div
                slot="graphic"
                class=${e.iconColor?"icon-background":""}
                .style="background-color: ${e.iconColor||"undefined"}"
              >
                <ha-svg-icon .path=${e.iconPath}></ha-svg-icon>
              </div>
              <span>${e.name}</span>
              ${this.hasSecondary?o.qy`<span slot="secondary">${e.description}</span>`:""}
              ${this.narrow?"":o.qy`<ha-icon-next slot="meta"></ha-icon-next>`}
            </ha-list-item>
          `))}
      </mwc-list>
    `}},{kind:"method",key:"_handleListAction",value:function(e){const t=this.pages[e.detail.index].path;t.endsWith("#external-app-configuration")?this.hass.auth.external.fireMessage({type:"config_screen/show"}):(0,c.o)(t)}},{kind:"field",static:!0,key:"styles",value(){return o.AH`
    :host {
      --mdc-list-vertical-padding: 0;
    }
    ha-svg-icon,
    ha-icon-next {
      color: var(--secondary-text-color);
      height: 24px;
      width: 24px;
      display: block;
    }
    ha-svg-icon {
      padding: 8px;
    }
    .icon-background {
      border-radius: 50%;
    }
    .icon-background ha-svg-icon {
      color: #fff;
    }
    ha-list-item {
      cursor: pointer;
      font-size: var(--navigation-list-item-title-font-size);
    }
  `}}]}}),o.WF);var h=i(10),u=i(33167),p=i(50036),v=i(69534),m=i(69760),g=i(66580);(0,a.A)([(0,n.EM)("ha-control-select")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"vertical",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"hide-label"})],key:"hideLabel",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_activeIndex",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,v.A)(i,"firstUpdated",this,3)([e]),this.setAttribute("role","listbox"),this.hasAttribute("tabindex")||this.setAttribute("tabindex","0")}},{kind:"method",key:"updated",value:function(e){if((0,v.A)(i,"updated",this,3)([e]),e.has("_activeIndex")){const e=null!=this._activeIndex?this.options?.[this._activeIndex]?.value:void 0,t=null!=e?`option-${e}`:void 0;this.setAttribute("aria-activedescendant",t??"")}if(e.has("vertical")){const e=this.vertical?"vertical":"horizontal";this.setAttribute("aria-orientation",e)}}},{kind:"method",key:"connectedCallback",value:function(){(0,v.A)(i,"connectedCallback",this,3)([]),this._setupListeners()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,v.A)(i,"disconnectedCallback",this,3)([]),this._destroyListeners()}},{kind:"method",key:"_setupListeners",value:function(){this.addEventListener("focus",this._handleFocus),this.addEventListener("blur",this._handleBlur),this.addEventListener("keydown",this._handleKeydown)}},{kind:"method",key:"_destroyListeners",value:function(){this.removeEventListener("focus",this._handleFocus),this.removeEventListener("blur",this._handleBlur),this.removeEventListener("keydown",this._handleKeydown)}},{kind:"method",key:"_handleFocus",value:function(){this.disabled||(this._activeIndex=(null!=this.value?this.options?.findIndex((e=>e.value===this.value)):void 0)??0)}},{kind:"method",key:"_handleBlur",value:function(){this._activeIndex=void 0}},{kind:"method",key:"_handleKeydown",value:function(e){if(!this.options||null==this._activeIndex||this.disabled)return;const t=this.options[this._activeIndex].value;switch(e.key){case" ":this.value=t,(0,u.r)(this,"value-changed",{value:t});break;case"ArrowUp":case"ArrowLeft":this._activeIndex=this._activeIndex<=0?this.options.length-1:this._activeIndex-1;break;case"ArrowDown":case"ArrowRight":this._activeIndex=(this._activeIndex+1)%this.options.length;break;case"Home":this._activeIndex=0;break;case"End":this._activeIndex=this.options.length-1;break;default:return}e.preventDefault()}},{kind:"method",key:"_handleOptionClick",value:function(e){if(this.disabled)return;const t=e.target.value;this.value=t,(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_handleOptionMouseDown",value:function(e){if(this.disabled)return;e.preventDefault();const t=e.target.value;this._activeIndex=this.options?.findIndex((e=>e.value===t))}},{kind:"method",key:"_handleOptionMouseUp",value:function(e){e.preventDefault(),this._activeIndex=void 0}},{kind:"method",key:"render",value:function(){return o.qy`
      <div class="container">
        ${this.options?(0,g.u)(this.options,(e=>e.value),((e,t)=>this._renderOption(e,t))):o.s6}
      </div>
    `}},{kind:"method",key:"_renderOption",value:function(e,t){return o.qy`
      <div
        id=${`option-${e.value}`}
        class=${(0,m.H)({option:!0,selected:this.value===e.value,focused:this._activeIndex===t})}
        role="option"
        .value=${e.value}
        aria-selected=${this.value===e.value}
        aria-label=${(0,l.J)(e.label)}
        title=${(0,l.J)(e.label)}
        @click=${this._handleOptionClick}
        @mousedown=${this._handleOptionMouseDown}
        @mouseup=${this._handleOptionMouseUp}
      >
        <div class="content">
          ${e.path?o.qy`<ha-svg-icon .path=${e.path}></ha-svg-icon>`:e.icon||o.s6}
          ${e.label&&!this.hideLabel?o.qy`<span>${e.label}</span>`:o.s6}
        </div>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        display: block;
        --control-select-color: var(--primary-color);
        --control-select-focused-opacity: 0.2;
        --control-select-selected-opacity: 1;
        --control-select-background: var(--disabled-color);
        --control-select-background-opacity: 0.2;
        --control-select-thickness: 40px;
        --control-select-border-radius: 10px;
        --control-select-padding: 4px;
        --control-select-button-border-radius: calc(
          var(--control-select-border-radius) - var(--control-select-padding)
        );
        --mdc-icon-size: 20px;
        height: var(--control-select-thickness);
        width: 100%;
        border-radius: var(--control-select-border-radius);
        outline: none;
        transition: box-shadow 180ms ease-in-out;
        font-style: normal;
        font-weight: 500;
        color: var(--primary-text-color);
        user-select: none;
        -webkit-tap-highlight-color: transparent;
      }
      :host(:focus-visible) {
        box-shadow: 0 0 0 2px var(--control-select-color);
      }
      :host([vertical]) {
        width: var(--control-select-thickness);
        height: 100%;
      }
      .container {
        position: relative;
        height: 100%;
        width: 100%;
        border-radius: var(--control-select-border-radius);
        transform: translateZ(0);
        overflow: hidden;
        display: flex;
        flex-direction: row;
        padding: var(--control-select-padding);
        box-sizing: border-box;
      }
      .container::before {
        position: absolute;
        content: "";
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background: var(--control-select-background);
        opacity: var(--control-select-background-opacity);
      }

      .container > *:not(:last-child) {
        margin-right: var(--control-select-padding);
        margin-inline-end: var(--control-select-padding);
        margin-inline-start: initial;
        direction: var(--direction);
      }
      .option {
        cursor: pointer;
        position: relative;
        flex: 1;
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: var(--control-select-button-border-radius);
        overflow: hidden;
        /* For safari border-radius overflow */
        z-index: 0;
      }
      .content > *:not(:last-child) {
        margin-bottom: 4px;
      }
      .option::before {
        position: absolute;
        content: "";
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background-color: var(--control-select-color);
        opacity: 0;
        transition:
          background-color ease-in-out 180ms,
          opacity ease-in-out 80ms;
      }
      .option.focused::before,
      .option:hover::before {
        opacity: var(--control-select-focused-opacity);
      }
      .option.selected {
        color: white;
      }
      .option.selected::before {
        opacity: var(--control-select-selected-opacity);
      }
      .option .content {
        position: relative;
        pointer-events: none;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        padding: 2px;
        width: 100%;
        box-sizing: border-box;
      }
      .option .content span {
        display: block;
        width: 100%;
        -webkit-hyphens: auto;
        -moz-hyphens: auto;
        hyphens: auto;
      }
      :host([vertical]) {
        width: var(--control-select-thickness);
        height: auto;
      }
      :host([vertical]) .container {
        flex-direction: column;
      }
      :host([vertical]) .container > *:not(:last-child) {
        margin-right: initial;
        margin-inline-end: initial;
        margin-bottom: var(--control-select-padding);
      }
      :host([disabled]) {
        --control-select-color: var(--disabled-color);
        --control-select-focused-opacity: 0;
        color: var(--disabled-color);
      }
      :host([disabled]) .option {
        cursor: not-allowed;
      }
    `}}]}}),o.WF);i(91686),i(52631),i(93650),i(33768),i(96396),i(32694);(0,a.A)([(0,n.EM)("knx-dpt-selector")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"options",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"invalid",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"invalidMessage",value:void 0},{kind:"method",key:"render",value:function(){return o.qy`
      <div>
        ${this.label??o.s6}
        ${this.options.map((e=>o.qy`
            <div class="formfield">
              <ha-radio
                .checked=${e.value===this.value}
                .value=${e.value}
                .disabled=${this.disabled}
                @change=${this._valueChanged}
              ></ha-radio>
              <label .value=${e.value} @click=${this._valueChanged}>
                <p>${e.label}</p>
                ${e.description?o.qy`<p class="secondary">${e.description}</p>`:o.s6}
              </label>
            </div>
          `))}
        ${this.invalidMessage?o.qy`<p class="invalid-message">${this.invalidMessage}</p>`:o.s6}
      </div>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.target.value;this.disabled||void 0===t||t===(this.value??"")||(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",static:!0,key:"styles",value(){return[o.AH`
      :host([invalid]) div {
        color: var(--error-color);
      }

      .formfield {
        display: flex;
        align-items: center;
      }

      label {
        min-width: 200px; /* to make it easier to click */
      }

      p {
        pointer-events: none;
        color: var(--primary-text-color);
        margin: 0px;
      }

      .secondary {
        padding-top: 4px;
        font-family: var(
          --mdc-typography-body2-font-family,
          var(--mdc-typography-font-family, Roboto, sans-serif)
        );
        -webkit-font-smoothing: antialiased;
        font-size: var(--mdc-typography-body2-font-size, 0.875rem);
        font-weight: var(--mdc-typography-body2-font-weight, 400);
        line-height: normal;
        color: var(--secondary-text-color);
      }

      .invalid-message {
        font-size: 0.75rem;
        color: var(--error-color);
        padding-left: 16px;
      }
    `]}}]}}),o.WF);var f=i(61328);const y=new f.Q("knx-drag-drop-context"),k=Symbol("drag-drop-context");class b{constructor(e){this._groupAddress=void 0,this._updateObservers=void 0,this.gaDragStartHandler=e=>{const t=e.target,i=t.ga;i?(this._groupAddress=i,y.debug("dragstart",i.address,this),e.dataTransfer?.setData("text/group-address",i.address),this._updateObservers()):y.warn("dragstart: no 'ga' property found",t)},this.gaDragEndHandler=e=>{y.debug("dragend",this),this._groupAddress=void 0,this._updateObservers()},this.gaDragIndicatorStartHandler=e=>{const t=e.target.ga;t&&(this._groupAddress=t,y.debug("drag indicator start",t.address,this),this._updateObservers())},this.gaDragIndicatorEndHandler=e=>{y.debug("drag indicator end",this),this._groupAddress=void 0,this._updateObservers()},this._updateObservers=e}get groupAddress(){return this._groupAddress}}const _=(0,r.q6)(k),x=(e,t)=>t.some((t=>e.main===t.main&&(!t.sub||e.sub===t.sub))),$=(e,t)=>{const i=((e,t)=>Object.entries(e.group_addresses).reduce(((e,[i,a])=>(a.dpt&&x(a.dpt,t)&&(e[i]=a),e)),{}))(e,t);return Object.entries(e.communication_objects).reduce(((e,[t,a])=>(a.group_address_links.some((e=>e in i))&&(e[t]=a),e)),{})},w=(e,t)=>{if(!e)return;const i=[];for(const a of e)if(a.path){const[e,...o]=a.path;e===t&&i.push({...a,path:o})}return i.length?i:void 0},M=e=>e.map((e=>({value:e.address,label:`${e.address} - ${e.name}`})));(0,a.A)([(0,n.EM)("knx-group-address-selector")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Fg)({context:_,subscribe:!0})],key:"_dragDropContext",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"config",value(){return{}}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,n.MZ)({reflect:!0})],key:"key",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"validationErrors",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_showPassive",value(){return!1}},{kind:"field",key:"validGroupAddresses",value(){return[]}},{kind:"field",key:"filteredGroupAddresses",value(){return[]}},{kind:"field",key:"addressOptions",value(){return[]}},{kind:"field",key:"dptSelectorDisabled",value(){return!1}},{kind:"field",key:"_validGADropTarget",value:void 0},{kind:"field",key:"_dragOverTimeout",value(){return{}}},{kind:"field",decorators:[(0,n.P)(".passive")],key:"_passiveContainer",value:void 0},{kind:"field",decorators:[(0,n.YG)("ha-selector-select")],key:"_gaSelectors",value:void 0},{kind:"method",key:"getValidGroupAddresses",value:function(e){return this.knx.project?.project_loaded?Object.values(this.knx.project.knxproject.group_addresses).filter((t=>!!t.dpt&&x(t.dpt,e))):[]}},{kind:"method",key:"getValidDptFromConfigValue",value:function(){return this.config.dpt?this.options.dptSelect?.find((e=>e.value===this.config.dpt))?.dpt:void 0}},{kind:"method",key:"connectedCallback",value:function(){(0,v.A)(i,"connectedCallback",this,3)([]),this.validGroupAddresses=this.getValidGroupAddresses(this.options.validDPTs??this.options.dptSelect?.map((e=>e.dpt))??[]),this.filteredGroupAddresses=this.validGroupAddresses,this.addressOptions=M(this.filteredGroupAddresses)}},{kind:"method",key:"shouldUpdate",value:function(e){return!(1===e.size&&e.has("hass"))}},{kind:"method",key:"willUpdate",value:function(e){if(e.has("config")){const t=this.getValidDptFromConfigValue();if(e.get("config")?.dpt!==this.config.dpt&&(this.filteredGroupAddresses=t?this.getValidGroupAddresses([t]):this.validGroupAddresses,this.addressOptions=M(this.filteredGroupAddresses)),t&&this.knx.project?.project_loaded){const e=[this.config.write,this.config.state,...this.config.passive??[]].filter((e=>null!=e));this.dptSelectorDisabled=e.length>0&&e.every((e=>{const i=this.knx.project?.knxproject.group_addresses[e]?.dpt;return!!i&&x(i,[t])}))}else this.dptSelectorDisabled=!1}this._validGADropTarget=this._dragDropContext?.groupAddress?this.filteredGroupAddresses.includes(this._dragDropContext.groupAddress):void 0}},{kind:"method",key:"updated",value:function(e){e.has("validationErrors")&&this._gaSelectors.forEach((async e=>{await e.updateComplete;const t=w(this.validationErrors,e.key)?.[0];e.comboBox.errorMessage=t?.error_message,e.comboBox.invalid=!!t}))}},{kind:"method",key:"render",value:function(){const e=this.config.passive&&this.config.passive.length>0,t=!0===this._validGADropTarget,i=!1===this._validGADropTarget;return o.qy`
      <div class="main">
        <div class="selectors">
          ${this.options.write?o.qy`<ha-selector-select
                class=${(0,m.H)({"valid-drop-zone":t,"invalid-drop-zone":i})}
                .hass=${this.hass}
                .label=${"Send address"+(this.label?` - ${this.label}`:"")}
                .required=${this.options.write.required}
                .selector=${{select:{multiple:!1,custom_value:!0,options:this.addressOptions}}}
                .key=${"write"}
                .value=${this.config.write}
                @value-changed=${this._updateConfig}
                @dragover=${this._dragOverHandler}
                @drop=${this._dropHandler}
              ></ha-selector-select>`:o.s6}
          ${this.options.state?o.qy`<ha-selector-select
                class=${(0,m.H)({"valid-drop-zone":t,"invalid-drop-zone":i})}
                .hass=${this.hass}
                .label=${"State address"+(this.label?` - ${this.label}`:"")}
                .required=${this.options.state.required}
                .selector=${{select:{multiple:!1,custom_value:!0,options:this.addressOptions}}}
                .key=${"state"}
                .value=${this.config.state}
                @value-changed=${this._updateConfig}
                @dragover=${this._dragOverHandler}
                @drop=${this._dropHandler}
              ></ha-selector-select>`:o.s6}
        </div>
        <div class="options">
          <ha-icon-button
            .disabled=${!!e}
            .path=${this._showPassive?"M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z":"M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"}
            .label=${"Toggle passive address visibility"}
            @click=${this._togglePassiveVisibility}
          ></ha-icon-button>
        </div>
      </div>
      <div
        class="passive ${(0,m.H)({expanded:e||this._showPassive})}"
        @transitionend=${this._handleTransitionEnd}
      >
        <ha-selector-select
          class=${(0,m.H)({"valid-drop-zone":t,"invalid-drop-zone":i})}
          .hass=${this.hass}
          .label=${"Passive addresses"+(this.label?` - ${this.label}`:"")}
          .required=${!1}
          .selector=${{select:{multiple:!0,custom_value:!0,options:this.addressOptions}}}
          .key=${"passive"}
          .value=${this.config.passive}
          @value-changed=${this._updateConfig}
          @dragover=${this._dragOverHandler}
          @drop=${this._dropHandler}
        ></ha-selector-select>
      </div>
      ${this.options.dptSelect?this._renderDptSelector():o.s6}
    `}},{kind:"method",key:"_renderDptSelector",value:function(){const e=w(this.validationErrors,"dpt")?.[0];return o.qy`<knx-dpt-selector
      .key=${"dpt"}
      .label=${"Datapoint type"}
      .options=${this.options.dptSelect}
      .value=${this.config.dpt}
      .disabled=${this.dptSelectorDisabled}
      .invalid=${!!e}
      .invalidMessage=${e?.error_message}
      @value-changed=${this._updateConfig}
    >
    </knx-dpt-selector>`}},{kind:"method",key:"_updateConfig",value:function(e){e.stopPropagation();const t=e.target,i=e.detail.value,a={...this.config,[t.key]:i};this._updateDptSelector(t.key,a),this.config=a,(0,u.r)(this,"value-changed",{value:this.config}),this.requestUpdate()}},{kind:"method",key:"_updateDptSelector",value:function(e,t){if(!this.options.dptSelect||!this.knx.project?.project_loaded)return;let i;if("write"===e||"state"===e)i=t[e];else{if("passive"!==e)return;{const e=t.passive?.filter((e=>!this.config.passive?.includes(e)))?.[0];i=e}}if(t.write||t.state||t.passive?.length||(t.dpt=void 0),void 0===this.config.dpt){const e=this.validGroupAddresses.find((e=>e.address===i))?.dpt;if(!e)return;const a=this.options.dptSelect.find((t=>t.dpt.main===e.main&&t.dpt.sub===e.sub)),o=a?a.value:this.options.dptSelect.find((t=>x(e,[t.dpt])))?.value;t.dpt=o}}},{kind:"method",key:"_togglePassiveVisibility",value:function(e){e.stopPropagation(),e.preventDefault();const t=!this._showPassive;this._passiveContainer.style.overflow="hidden";const i=this._passiveContainer.scrollHeight;this._passiveContainer.style.height=`${i}px`,t||setTimeout((()=>{this._passiveContainer.style.height="0px"}),0),this._showPassive=t}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._passiveContainer.style.removeProperty("height"),this._passiveContainer.style.overflow=this._showPassive?"initial":"hidden"}},{kind:"method",key:"_dragOverHandler",value:function(e){if(![...e.dataTransfer.types].includes("text/group-address"))return;e.preventDefault(),e.dataTransfer.dropEffect="move";const t=e.target;this._dragOverTimeout[t.key]?clearTimeout(this._dragOverTimeout[t.key]):t.classList.add("active-drop-zone"),this._dragOverTimeout[t.key]=setTimeout((()=>{delete this._dragOverTimeout[t.key],t.classList.remove("active-drop-zone")}),100)}},{kind:"method",key:"_dropHandler",value:function(e){const t=e.dataTransfer.getData("text/group-address");if(!t)return;e.stopPropagation(),e.preventDefault();const i=e.target,a={...this.config};if(i.selector.select.multiple){const e=[...this.config[i.key]??[],t];a[i.key]=e}else a[i.key]=t;this._updateDptSelector(i.key,a),(0,u.r)(this,"value-changed",{value:a}),setTimeout((()=>i.comboBox._inputElement.blur()))}},{kind:"field",static:!0,key:"styles",value(){return o.AH`
    .main {
      display: flex;
      flex-direction: row;
    }

    .selectors {
      flex: 1;
      padding-right: 16px;
    }

    .options {
      width: 48px;
      display: flex;
      flex-direction: column-reverse;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }

    .passive {
      overflow: hidden;
      transition: height 150ms cubic-bezier(0.4, 0, 0.2, 1);
      height: 0px;
      margin-right: 64px; /* compensate for .options */
    }

    .passive.expanded {
      height: auto;
    }

    ha-selector-select {
      display: block;
      margin-bottom: 16px;
      transition:
        box-shadow 250ms,
        opacity 250ms;
    }

    .valid-drop-zone {
      box-shadow: 0px 0px 5px 2px rgba(var(--rgb-primary-color), 0.5);
    }

    .valid-drop-zone.active-drop-zone {
      box-shadow: 0px 0px 5px 2px var(--primary-color);
    }

    .invalid-drop-zone {
      opacity: 0.5;
    }

    .invalid-drop-zone.active-drop-zone {
      box-shadow: 0px 0px 5px 2px var(--error-color);
    }
  `}}]}}),o.WF);i(357);(0,a.A)([(0,n.EM)("knx-sync-state-selector-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)()],key:"key",value(){return"sync_state"}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"noneValid",value(){return!0}},{kind:"field",key:"_strategy",value(){return!0}},{kind:"field",key:"_minutes",value(){return 60}},{kind:"method",key:"_hasMinutes",value:function(e){return"expire"===e||"every"===e}},{kind:"method",key:"willUpdate",value:function(){if("boolean"==typeof this.value)return void(this._strategy=this.value);const[e,t]=this.value.split(" ");this._strategy=e,+t&&(this._minutes=+t)}},{kind:"method",key:"render",value:function(){return o.qy` <div class="inline">
      <ha-selector-select
        .hass=${this.hass}
        .label=${"Strategy"}
        .selector=${{select:{multiple:!1,custom_value:!1,mode:"dropdown",options:[{value:!0,label:"Default"},...this.noneValid?[{value:!1,label:"Never"}]:[],{value:"init",label:"Once when connection established"},{value:"expire",label:"Expire after last value update"},{value:"every",label:"Scheduled every"}]}}}
        .key=${"strategy"}
        .value=${this._strategy}
        @value-changed=${this._handleChange}
      >
      </ha-selector-select>
      <ha-selector-number
        .hass=${this.hass}
        .disabled=${!this._hasMinutes(this._strategy)}
        .selector=${{number:{min:2,max:1440,step:1,unit_of_measurement:"minutes"}}}
        .key=${"minutes"}
        .value=${this._minutes}
        @value-changed=${this._handleChange}
      >
      </ha-selector-number>
    </div>`}},{kind:"method",key:"_handleChange",value:function(e){let t,i;e.stopPropagation(),"strategy"===e.target.key?(t=e.detail.value,i=this._minutes):(t=this._strategy,i=e.detail.value);const a=this._hasMinutes(t)?`${t} ${i}`:t;(0,u.r)(this,"value-changed",{value:a})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      .inline {
        width: 100%;
        display: inline-flex;
        flex-flow: row wrap;
        gap: 16px;
        justify-content: space-between;
      }

      .inline > * {
        flex: 1;
      }
    `}}]}}),o.WF);i(74259);var C=i(45081),A=(i(66442),i(58068),i(57046),i(88762),i(39987));const H=new f.Q("create_device_dialog");(0,a.A)([(0,n.EM)("knx-device-create-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"deviceName",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"area",value:void 0},{kind:"field",key:"_deviceEntry",value:void 0},{kind:"method",key:"closeDialog",value:function(e){(0,u.r)(this,"create-device-dialog-closed",{newDevice:this._deviceEntry},{bubbles:!1})}},{kind:"method",key:"_createDevice",value:function(){(0,A.Jv)(this.hass,{name:this.deviceName,area_id:this.area}).then((e=>{this._deviceEntry=e})).catch((e=>{H.error("getGroupMonitorInfo",e),(0,c.o)("/knx/error",{replace:!0,data:e})})).finally((()=>{this.closeDialog(void 0)}))}},{kind:"method",key:"render",value:function(){return o.qy`<ha-dialog
      open
      .heading=${"Create new device"}
      scrimClickAction
      escapeKeyAction
      defaultAction="ignore"
    >
      <ha-selector-text
        .hass=${this.hass}
        .label=${"Name"}
        .required=${!0}
        .selector=${{text:{type:"text"}}}
        .key=${"deviceName"}
        .value=${this.deviceName}
        @value-changed=${this._valueChanged}
      ></ha-selector-text>
      <ha-area-picker
        .hass=${this.hass}
        .label=${"Area"}
        .key=${"area"}
        .value=${this.area}
        @value-changed=${this._valueChanged}
      >
      </ha-area-picker>
      <mwc-button slot="secondaryAction" @click=${this.closeDialog}>
        ${this.hass.localize("ui.common.cancel")}
      </mwc-button>
      <mwc-button slot="primaryAction" @click=${this._createDevice}>
        ${this.hass.localize("ui.common.add")}
      </mwc-button>
    </ha-dialog>`}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this[e.target.key]=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return[d.nA,o.AH`
        @media all and (min-width: 600px) {
          ha-dialog {
            --mdc-dialog-min-width: 480px;
          }
        }
      `]}}]}}),o.WF);var D=i(38848),q=i(66412);const Z=e=>"knx"===e[0],L=e=>e.identifiers.some(Z),S=e=>Object.values(e.devices).filter(L),P=e=>{const t=e.identifiers.find(Z);return t?t[1]:void 0},V=e=>o.qy`<ha-list-item
    class=${(0,m.H)({"add-new":"add_new"===e.id})}
    .twoline=${!!e.area}
  >
    <span>${e.name}</span>
    <span slot="secondary">${e.area}</span>
  </ha-list-item>`;(0,a.A)([(0,n.EM)("knx-device-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_showCreateDeviceDialog",value(){return!1}},{kind:"field",key:"_deviceId",value:void 0},{kind:"field",key:"_suggestion",value:void 0},{kind:"field",key:"_init",value(){return!1}},{kind:"field",key:"_getDevices",value(){return(0,C.A)(((e,t)=>[{id:"add_new",name:"Add new device…",area:"",strings:[]},...e.map((e=>{const i=e.name_by_user??e.name??"";return{id:e.id,identifier:P(e),name:i,area:e.area_id&&t[e.area_id]?t[e.area_id].name:this.hass.localize("ui.components.device-picker.no_area"),strings:[i||""]}})).sort(((e,t)=>(0,q.x)(e.name||"",t.name||"",this.hass.locale.language)))]))}},{kind:"method",key:"_addDevice",value:async function(e){const t=[...S(this.hass),e],i=this._getDevices(t,this.hass.areas);this.comboBox.items=i,this.comboBox.filteredItems=i,await this.updateComplete,await this.comboBox.updateComplete}},{kind:"method",key:"open",value:async function(){await this.updateComplete,await(this.comboBox?.open())}},{kind:"method",key:"focus",value:async function(){await this.updateComplete,await(this.comboBox?.focus())}},{kind:"method",key:"updated",value:function(e){if(!this._init&&this.hass||this._init&&e.has("_opened")&&this._opened){this._init=!0;const e=this._getDevices(S(this.hass),this.hass.areas),t=this.value?e.find((e=>e.identifier===this.value))?.id:void 0;this.comboBox.value=t,this._deviceId=t,this.comboBox.items=e,this.comboBox.filteredItems=e}}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.device-picker.device"):this.label}
        .value=${this._deviceId}
        .renderer=${V}
        item-id-path="id"
        item-value-path="id"
        item-label-path="name"
        @filter-changed=${this._filterChanged}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._deviceChanged}
      ></ha-combo-box>
      ${this._showCreateDeviceDialog?this._renderCreateDeviceDialog():o.s6}
    `}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.target,i=e.detail.value;if(!i)return void(this.comboBox.filteredItems=this.comboBox.items);const a=(0,D.H)(i,t.items||[]);this._suggestion=i,this.comboBox.filteredItems=[...a,{id:"add_new_suggestion",name:`Add new device '${this._suggestion}'`}]}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();let t=e.detail.value;"no_devices"===t&&(t=""),["add_new_suggestion","add_new"].includes(t)?(e.target.value=this._deviceId,this._openCreateDeviceDialog()):t!==this._deviceId&&this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e){const t=this.comboBox.items.find((t=>t.id===e)),i=t?.identifier;this.value=i,this._deviceId=t?.id,setTimeout((()=>{(0,u.r)(this,"value-changed",{value:i}),(0,u.r)(this,"change")}),0)}},{kind:"method",key:"_renderCreateDeviceDialog",value:function(){return o.qy`
      <knx-device-create-dialog
        .hass=${this.hass}
        @create-device-dialog-closed=${this._closeCreateDeviceDialog}
        .deviceName=${this._suggestion}
      ></knx-device-create-dialog>
    `}},{kind:"method",key:"_openCreateDeviceDialog",value:function(){this._showCreateDeviceDialog=!0}},{kind:"method",key:"_closeCreateDeviceDialog",value:async function(e){const t=e.detail.newDevice;t?await this._addDevice(t):this.comboBox.setInputValue(""),this._setValue(t?.id),this._suggestion=void 0,this._showCreateDeviceDialog=!1}}]}}),o.WF);const E=(e,t,i,a)=>{const n=t.device_info?((e,t)=>Object.values(e.devices).find((e=>e.identifiers.find((e=>Z(e)&&e[1]===t)))))(e,t.device_info):void 0,r=n?n.name_by_user??n.name:"",s=a?.find((e=>!e.path||0===e.path.length));return o.qy`
    <ha-card outlined>
      <h1 class="card-header">Entity configuration</h1>
      <p class="card-content">Home Assistant specific settings.</p>
      ${a&&s?o.qy`<ha-alert
              .alertType=${"error"}
              .title=${s.error_message}
            ></ha-alert>`:o.s6}
      <ha-settings-row narrow>
        <div slot="heading">Device</div>
        <div slot="description">A device allows to group multiple entities.</div>
        <knx-device-picker
          .hass=${e}
          .key=${"device_info"}
          .value=${t.device_info??void 0}
          @value-changed=${i}
        ></knx-device-picker>
      </ha-settings-row>
      <ha-settings-row narrow>
        <div slot="heading">Name</div>
        <div slot="description">Name of the entity.</div>
        <ha-selector-text
          .hass=${e}
          .label=${"Name"}
          .required=${!n}
          .selector=${{text:{type:"text",prefix:r}}}
          .key=${"name"}
          .value=${t.name}
          @value-changed=${i}
        ></ha-selector-text>
      </ha-settings-row>
      <ha-expansion-panel .header=${"Advanced"} outlined>
        <ha-selector-select
          .hass=${e}
          .label=${"Entity category"}
          .helper=${"Leave empty for standard behaviour."}
          .required=${!1}
          .selector=${{select:{multiple:!1,custom_value:!1,mode:"dropdown",options:[{value:"config",label:"Config"},{value:"diagnostic",label:"Diagnostic"}]}}}
          .key=${"entity_category"}
          .value=${t.entity_category}
          @value-changed=${i}
        ></ha-selector-select>
      </ha-expansion-panel>
    </ha-card>
  `},B=new f.Q("knx-configure-entity");(0,a.A)([(0,n.EM)("knx-configure-entity")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"platform",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"config",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"schema",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"validationErrors",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,v.A)(i,"connectedCallback",this,3)([]),this.config||(this.config={entity:{},knx:{}})}},{kind:"method",key:"render",value:function(){const e=w(this.validationErrors,"data");return o.qy`
      <div class="header">
        <h1><ha-svg-icon .path=${this.platform.iconPath}></ha-svg-icon>${this.platform.name}</h1>
        <p>${this.platform.description}</p>
      </div>
      <slot name="knx-validation-error"></slot>
      <ha-card outlined>
        <h1 class="card-header">KNX configuration</h1>
        ${this.generateRootGroups(this.platform.schema,w(e,"knx"))}
      </ha-card>
      ${E(this.hass,this.config.entity??{},this._updateConfig("entity"),w(e,"entity"))}
    `}},{kind:"method",key:"generateRootGroups",value:function(e,t){const i=[],a=[];return e.forEach((e=>{e.advanced?a.push(e):i.push(e)})),o.qy`
      ${i.map((e=>this._generateSettingsGroup(e,t)))}
      ${a.length?o.qy` <ha-expansion-panel .header=${"Advanced"} outlined>
            ${a.map((e=>this._generateSettingsGroup(e,t)))}
          </ha-expansion-panel>`:o.s6}
    `}},{kind:"method",key:"_generateSettingsGroup",value:function(e,t){return!0===e.collapsible?o.qy` <ha-expansion-panel
        outlined
        .header=${e.heading}
        .secondary=${e.description}
        .expanded=${this._groupHasGroupAddressInConfig(e)}
        >${this._generateItems(e.selectors,t)}
      </ha-expansion-panel>`:o.qy` <ha-settings-row narrow>
      <div slot="heading">${e.heading}</div>
      <div slot="description">${e.description}</div>
      ${this._generateItems(e.selectors,t)}
    </ha-settings-row>`}},{kind:"method",key:"_groupHasGroupAddressInConfig",value:function(e){return void 0!==this.config&&e.selectors.some((e=>"group_address"===e.type?this._hasGroupAddressInConfig(e,this.config.knx):"group_select"===e.type&&e.options.some((e=>e.schema.some((e=>"settings_group"===e.type?this._groupHasGroupAddressInConfig(e):"group_address"===e.type&&this._hasGroupAddressInConfig(e,this.config.knx)))))))}},{kind:"method",key:"_hasGroupAddressInConfig",value:function(e,t){if(!(e.name in t))return!1;const i=t[e.name];return void 0!==i.write||(void 0!==i.state||!!i.passive?.length)}},{kind:"method",key:"_generateItems",value:function(e,t){return o.qy`${e.map((e=>this._generateItem(e,t)))}`}},{kind:"method",key:"_generateItem",value:function(e,t){switch(e.type){case"group_address":return o.qy`
          <knx-group-address-selector
            .hass=${this.hass}
            .knx=${this.knx}
            .key=${e.name}
            .label=${e.label}
            .config=${this.config.knx[e.name]??{}}
            .options=${e.options}
            .validationErrors=${w(t,e.name)}
            @value-changed=${this._updateConfig("knx")}
          ></knx-group-address-selector>
        `;case"selector":return void 0!==e.default&&null==this.config.knx[e.name]&&(this.config.knx[e.name]=e.default),o.qy`
          <ha-selector
            .hass=${this.hass}
            .selector=${e.selector}
            .label=${e.label}
            .helper=${e.helper}
            .key=${e.name}
            .value=${this.config.knx[e.name]}
            @value-changed=${this._updateConfig("knx")}
          ></ha-selector>
        `;case"sync_state":return o.qy`
          <knx-sync-state-selector-row
            .hass=${this.hass}
            .key=${e.name}
            .value=${this.config.knx[e.name]??!0}
            .noneValid=${!1}
            @value-changed=${this._updateConfig("knx")}
          ></knx-sync-state-selector-row>
        `;case"group_select":return this._generateGroupSelect(e,t);default:return B.error("Unknown selector type",e),o.s6}}},{kind:"method",key:"_generateGroupSelect",value:function(e,t){const i=this.config.knx[e.name]??(this.config.knx[e.name]=e.options[0].value),a=e.options.find((e=>e.value===i));return void 0===a&&B.error("No option found for value",i),o.qy` <ha-control-select
        .options=${e.options}
        .value=${i}
        .key=${e.name}
        @value-changed=${this._updateConfig("knx")}
      ></ha-control-select>
      ${a?o.qy` <p class="group-description">${a.description}</p>
            <div class="group-selection">
              ${a.schema.map((e=>"settings_group"===e.type?this._generateSettingsGroup(e,t):this._generateItem(e,t)))}
            </div>`:o.s6}`}},{kind:"method",key:"_updateConfig",value:function(e){return t=>{t.stopPropagation(),this.config[e]||(this.config[e]={}),this.config[e][t.target.key]=t.detail.value,B.debug(`update ${e} key "${t.target.key}" with "${t.detail.value}"`),(0,u.r)(this,"knx-entity-configuration-changed",this.config),this.requestUpdate()}}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      p {
        color: var(--secondary-text-color);
      }

      .header {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        padding: 0 16px 16px;

        & h1 {
          display: inline-flex;
          align-items: center;
          font-size: 26px;
          letter-spacing: -0.012em;
          line-height: 48px;
          font-weight: normal;
          margin-bottom: 14px;

          & ha-svg-icon {
            color: var(--text-primary-color);
            padding: 8px;
            background-color: var(--blue-color);
            border-radius: 50%;
            margin-right: 8px;
          }
        }

        & p {
          margin-top: -8px;
          line-height: 24px;
        }
      }

      ::slotted(ha-alert) {
        margin-top: 0 !important;
      }

      ha-card {
        margin-bottom: 24px;
        padding: 16px;

        & .card-header {
          display: inline-flex;
          align-items: center;
        }
      }

      ha-expansion-panel {
        margin-bottom: 16px;
      }
      ha-expansion-panel > :first-child {
        margin-top: 16px;
      }
      ha-expansion-panel > ha-settings-row:first-child {
        border: 0;
      }

      ha-settings-row {
        margin-bottom: 16px;
        padding: 0;
      }
      ha-control-select {
        padding: 0;
        margin-bottom: 16px;
      }

      .group-description {
        align-items: center;
        margin-top: -8px;
        padding-left: 8px;
        padding-bottom: 8px;
      }

      .group-selection {
        padding-left: 16px;
        padding-right: 16px;
        & ha-settings-row:first-child {
          border-top: 0;
        }
      }

      knx-group-address-selector,
      ha-selector,
      ha-selector-text,
      ha-selector-select,
      knx-sync-state-selector-row,
      knx-device-picker {
        display: block;
        margin-bottom: 16px;
      }

      ha-alert {
        display: block;
        margin: 20px auto;
        max-width: 720px;

        & summary {
          padding: 10px;
        }
      }
    `}}]}}),o.WF);var I=i(23059);const O=new f.Q("knx-project-device-tree");(0,a.A)([(0,n.EM)("knx-project-device-tree")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Fg)({context:_})],key:"_dragDropContext",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"validDPTs",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_selectedDevice",value:void 0},{kind:"field",key:"deviceTree",value(){return[]}},{kind:"method",key:"connectedCallback",value:function(){(0,v.A)(i,"connectedCallback",this,3)([]);const e=this.validDPTs?.length?$(this.data,this.validDPTs):this.data.communication_objects,t=Object.values(this.data.devices).map((t=>{const i=[],a=Object.fromEntries(Object.entries(t.channels).map((([e,t])=>[e,{name:t.name,comObjects:[]}])));for(const n of t.communication_object_ids){if(!(n in e))continue;const t=e[n];t.channel&&t.channel in a?a[t.channel].comObjects.push(t):i.push(t)}const o=Object.entries(a).reduce(((e,[t,i])=>(i.comObjects.length&&(e[t]=i),e)),{});return{ia:t.individual_address,name:t.name,manufacturer:t.manufacturer_name,description:t.description.split(/[\r\n]/,1)[0],noChannelComObjects:i,channels:o}}));this.deviceTree=t.filter((e=>!!e.noChannelComObjects.length||!!Object.keys(e.channels).length))}},{kind:"method",key:"render",value:function(){return o.qy`<div class="device-tree-view">
      ${this._selectedDevice?this._renderSelectedDevice(this._selectedDevice):this._renderDevices()}
    </div>`}},{kind:"method",key:"_renderDevices",value:function(){return this.deviceTree.length?o.qy`<ul class="devices">
      ${(0,g.u)(this.deviceTree,(e=>e.ia),(e=>o.qy`<li class="clickable" @click=${this._selectDevice} .device=${e}>
            ${this._renderDevice(e)}
          </li>`))}
    </ul>`:o.qy`<ha-alert alert-type="info">No suitable device found in project data.</ha-alert>`}},{kind:"method",key:"_renderDevice",value:function(e){return o.qy`<div class="item">
      <span class="icon ia">
        <ha-svg-icon .path=${"M15,20A1,1 0 0,0 14,19H13V17H17A2,2 0 0,0 19,15V5A2,2 0 0,0 17,3H7A2,2 0 0,0 5,5V15A2,2 0 0,0 7,17H11V19H10A1,1 0 0,0 9,20H2V22H9A1,1 0 0,0 10,23H14A1,1 0 0,0 15,22H22V20H15M7,15V5H17V15H7Z"}></ha-svg-icon>
        <span>${e.ia}</span>
      </span>
      <div class="description">
        <p>${e.manufacturer}</p>
        <p>${e.name}</p>
        ${e.description?o.qy`<p>${e.description}</p>`:o.s6}
      </div>
    </div>`}},{kind:"method",key:"_renderSelectedDevice",value:function(e){return o.qy`<ul class="selected-device">
      <li class="back-item clickable" @click=${this._selectDevice}>
        <div class="item">
          <ha-svg-icon class="back-icon" .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}></ha-svg-icon>
          ${this._renderDevice(e)}
        </div>
      </li>
      ${this._renderChannels(e)}
    </ul>`}},{kind:"method",key:"_renderChannels",value:function(e){return o.qy`${this._renderComObjects(e.noChannelComObjects)}
    ${(0,g.u)(Object.entries(e.channels),(([t,i])=>`${e.ia}_ch_${t}`),(([e,t])=>t.comObjects.length?o.qy`<li class="channel">${t.name}</li>
              ${this._renderComObjects(t.comObjects)}`:o.s6))} `}},{kind:"method",key:"_renderComObjects",value:function(e){return o.qy`${(0,g.u)(e,(e=>`${e.device_address}_co_${e.number}`),(e=>{return o.qy`<li class="com-object">
          <div class="item">
            <span class="icon co"
              ><ha-svg-icon .path=${"M22 12C22 6.5 17.5 2 12 2S2 6.5 2 12 6.5 22 12 22 22 17.5 22 12M15 6.5L18.5 10L15 13.5V11H11V9H15V6.5M9 17.5L5.5 14L9 10.5V13H13V15H9V17.5Z"}></ha-svg-icon
              ><span>${e.number}</span></span
            >
            <div class="description">
              <p>
                ${e.text}${e.function_text?" - "+e.function_text:""}
              </p>
              <p class="co-info">${t=e.flags,`${t.read?"R":"–"} ${t.write?"W":"–"} ${t.transmit?"T":"–"} ${t.update?"U":"–"}`}</p>
            </div>
          </div>
          <ul class="group-addresses">
            ${this._renderGroupAddresses(e.group_address_links)}
          </ul>
        </li>`;var t}))} `}},{kind:"method",key:"_renderGroupAddresses",value:function(e){const t=e.map((e=>this.data.group_addresses[e]));return o.qy`${(0,g.u)(t,(e=>e.identifier),(e=>o.qy`<li
          draggable="true"
          @dragstart=${this._dragDropContext?.gaDragStartHandler}
          @dragend=${this._dragDropContext?.gaDragEndHandler}
          @mouseover=${this._dragDropContext?.gaDragIndicatorStartHandler}
          @focus=${this._dragDropContext?.gaDragIndicatorStartHandler}
          @mouseout=${this._dragDropContext?.gaDragIndicatorEndHandler}
          @blur=${this._dragDropContext?.gaDragIndicatorEndHandler}
          .ga=${e}
        >
          <div class="item">
            <ha-svg-icon
              class="drag-icon"
              .path=${"M9,3H11V5H9V3M13,3H15V5H13V3M9,7H11V9H9V7M13,7H15V9H13V7M9,11H11V13H9V11M13,11H15V13H13V11M9,15H11V17H9V15M13,15H15V17H13V15M9,19H11V21H9V19M13,19H15V21H13V19Z"}
              .viewBox=${"4 0 16 24"}
            ></ha-svg-icon>
            <span class="icon ga">
              <span>${e.address}</span>
            </span>
            <div class="description">
              <p>${e.name}</p>
              <p class="ga-info">${(e=>{const t=(0,I.V)(e.dpt);return t?`DPT ${t}`:""})(e)}</p>
            </div>
          </div>
        </li>`))} `}},{kind:"method",key:"_selectDevice",value:function(e){const t=e.target.device;O.debug("select device",t),this._selectedDevice=t,this.scrollTop=0}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        display: block;
        box-sizing: border-box;
        margin: 0;
        height: 100%;
        overflow-y: scroll;
        overflow-x: hidden;
        background-color: var(--sidebar-background-color);
        color: var(--sidebar-menu-button-text-color, --primary-text-color);
        margin-right: env(safe-area-inset-right);
        border-left: 1px solid var(--divider-color);
        padding-left: 8px;
      }

      ha-alert {
        display: block;
        margin-right: 8px;
        margin-top: 8px;
      }

      ul {
        list-style-type: none;
        padding: 0;
        margin-block-start: 8px;
      }

      li {
        display: block;
        margin-bottom: 4px;
        & div.item {
          /* icon and text */
          display: flex;
          align-items: center;
          pointer-events: none;
          & > div {
            /* optional container for multiple paragraphs */
            min-width: 0;
            width: 100%;
          }
        }
      }

      li p {
        margin: 0;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }

      span.icon {
        flex: 0 0 auto;
        display: inline-flex;
        /* align-self: stretch; */
        align-items: center;

        color: var(--text-primary-color);
        font-size: 1rem;
        font-weight: 700;
        border-radius: 12px;
        padding: 3px 6px;
        margin-right: 4px;

        & > ha-svg-icon {
          float: left;
          width: 16px;
          height: 16px;
          margin-right: 4px;
        }

        & > span {
          /* icon text */
          flex: 1;
          text-align: center;
        }
      }

      span.ia {
        flex-basis: 70px;
        background-color: var(--label-badge-grey);
        & > ha-svg-icon {
          transform: rotate(90deg);
        }
      }

      span.co {
        flex-basis: 44px;
        background-color: var(--amber-color);
      }

      span.ga {
        flex-basis: 54px;
        background-color: var(--knx-green);
      }

      .description {
        margin-top: 4px;
        margin-bottom: 4px;
      }

      p.co-info,
      p.ga-info {
        font-size: 0.85rem;
        font-weight: 300;
      }

      .back-item {
        margin-left: -8px; /* revert host padding to have gapless border */
        padding-left: 8px;
        margin-top: -8px; /* revert ul margin-block-start to have gapless hover effect */
        padding-top: 8px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--divider-color);
        margin-bottom: 8px;
      }

      .back-icon {
        margin-right: 8px;
        color: var(--label-badge-grey);
      }

      li.channel {
        border-top: 1px solid var(--divider-color);
        border-bottom: 1px solid var(--divider-color);
        padding: 4px 16px;
        font-weight: 500;
      }

      li.clickable {
        cursor: pointer;
      }
      li.clickable:hover {
        background-color: rgba(var(--rgb-primary-text-color), 0.04);
      }

      li[draggable="true"] {
        cursor: grab;
      }
      li[draggable="true"]:hover {
        border-radius: 12px;
        background-color: rgba(var(--rgb-primary-color), 0.2);
      }

      ul.group-addresses {
        margin-top: 0;
        margin-bottom: 8px;

        & > li:not(:first-child) {
          /* passive addresses for this com-object */
          opacity: 0.8;
        }
      }
    `}}]}}),o.WF);const T={switch:{name:"Switch",iconPath:"M18.4 1.6C18 1.2 17.5 1 17 1H7C6.5 1 6 1.2 5.6 1.6C5.2 2 5 2.5 5 3V21C5 21.5 5.2 22 5.6 22.4C6 22.8 6.5 23 7 23H17C17.5 23 18 22.8 18.4 22.4C18.8 22 19 21.5 19 21V3C19 2.5 18.8 2 18.4 1.6M16 7C16 7.6 15.6 8 15 8H9C8.4 8 8 7.6 8 7V5C8 4.4 8.4 4 9 4H15C15.6 4 16 4.4 16 5V7Z",color:"var(--blue-color)",description:"The KNX switch platform is used as an interface to switching actuators.",schema:[{type:"settings_group",heading:"Switching",description:"DPT 1 group addresses controlling the switch function.",selectors:[{name:"ga_switch",type:"group_address",options:{write:{required:!0},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"invert",type:"selector",selector:{boolean:null},label:"Invert",helper:"Invert payloads before processing or sending."},{name:"respond_to_read",type:"selector",selector:{boolean:null},label:"Respond to read",helper:"Respond to GroupValueRead telegrams received to the configured address."}]},{type:"settings_group",advanced:!0,heading:"State updater",description:"Actively request state updates from KNX bus for state addresses.",selectors:[{name:"sync_state",type:"sync_state"}]}]},light:{name:"Light",iconPath:i(93758).n_.light,color:"var(--amber-color)",description:"The KNX light platform is used as an interface to dimming actuators, LED controllers, DALI gateways and similar.",schema:[{type:"settings_group",heading:"Switching",description:"DPT 1 group addresses turning the light on or off.",selectors:[{name:"ga_switch",type:"group_address",options:{write:{required:!0},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}}]},{type:"settings_group",heading:"Brightness",description:"DPT 5 group addresses controlling the brightness.",selectors:[{name:"ga_brightness",type:"group_address",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"Color temperature",description:"Control the lights color temperature.",collapsible:!0,selectors:[{name:"ga_color_temp",type:"group_address",options:{write:{required:!1},state:{required:!1},passive:!0,dptSelect:[{value:"5.001",label:"Percent",description:"DPT 5.001",dpt:{main:5,sub:1}},{value:"7.600",label:"Kelvin",description:"DPT 7.600",dpt:{main:7,sub:600}},{value:"9",label:"2-byte float",description:"DPT 9",dpt:{main:9,sub:null}}]}},{name:"color_temp_min",type:"selector",label:"Warmest possible color temperature",default:2700,selector:{number:{min:1e3,max:9e3,step:1,unit_of_measurement:"Kelvin"}}},{name:"color_temp_max",type:"selector",label:"Coldest possible color temperature",default:6e3,selector:{number:{min:1e3,max:9e3,step:1,unit_of_measurement:"Kelvin"}}}]},{type:"settings_group",heading:"Color",description:"Control the light color.",collapsible:!0,selectors:[{type:"group_select",name:"_light_color_mode_schema",options:[{label:"Single address",description:"RGB, RGBW or XYY color controlled by a single group address",value:"default",schema:[{name:"ga_color",type:"group_address",options:{write:{required:!1},state:{required:!1},passive:!0,dptSelect:[{value:"232.600",label:"RGB",description:"DPT 232.600",dpt:{main:232,sub:600}},{value:"251.600",label:"RGBW",description:"DPT 251.600",dpt:{main:251,sub:600}},{value:"242.600",label:"XYY",description:"DPT 242.600",dpt:{main:242,sub:600}}]}}]},{label:"Individual addresses",description:"RGB(W) using individual state and brightness group addresses",value:"individual",schema:[{type:"settings_group",heading:"Red",description:"Control the lights red color. Brightness group address is required.",selectors:[{name:"ga_red_switch",type:"group_address",label:"Switch",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"ga_red_brightness",type:"group_address",label:"Brightness",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"Green",description:"Control the lights green color. Brightness group address is required.",selectors:[{name:"ga_green_switch",type:"group_address",label:"Switch",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"ga_green_brightness",type:"group_address",label:"Brightness",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"Blue",description:"Control the lights blue color. Brightness group address is required.",selectors:[{name:"ga_blue_switch",type:"group_address",label:"Switch",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"ga_blue_brightness",type:"group_address",label:"Brightness",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"White",description:"Control the lights white color. Brightness group address is required.",selectors:[{name:"ga_white_switch",type:"group_address",label:"Switch",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:1,sub:null}]}},{name:"ga_white_brightness",type:"group_address",label:"Brightness",options:{write:{required:!1},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]}]},{label:"HSV",description:"Hue, saturation and brightness using individual group addresses",value:"hsv",schema:[{type:"settings_group",heading:"Hue",description:"Control the lights hue.",selectors:[{name:"ga_hue",type:"group_address",options:{write:{required:!0},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]},{type:"settings_group",heading:"Saturation",description:"Control the lights saturation.",selectors:[{name:"ga_saturation",type:"group_address",options:{write:{required:!0},state:{required:!1},passive:!0,validDPTs:[{main:5,sub:1}]}}]}]}]}]},{type:"settings_group",advanced:!0,heading:"State updater",description:"Actively request state updates from KNX bus for state addresses.",selectors:[{name:"sync_state",type:"sync_state"}]}]}},F=new f.Q("knx-create-entity");let j=(0,a.A)([(0,n.EM)("knx-create-entity")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_loading",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_validationErrors",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_validationBaseError",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-alert")],key:"_alertElement",value:void 0},{kind:"field",key:"_intent",value:void 0},{kind:"field",key:"entityPlatform",value:void 0},{kind:"field",key:"entityId",value:void 0},{kind:"field",key:"_dragDropContextProvider",value(){return new r.DT(this,{context:_,initialValue:new b((()=>{this._dragDropContextProvider.updateObservers()}))})}},{kind:"method",key:"firstUpdated",value:function(){this.knx.project||this.knx.loadProject().then((()=>{this.requestUpdate()}))}},{kind:"method",key:"willUpdate",value:function(e){if(e.has("route")){const e=this.route.prefix.split("/").at(-1);if("create"!==e&&"edit"!==e)return F.error("Unknown intent",e),void(this._intent=void 0);if(this._intent=e,"create"===e){const e=this.route.path.split("/")[1];this.entityPlatform=e,this._config=void 0,this._loading=!1}else"edit"===e&&(this.entityId=this.route.path.split("/")[1],this._loading=!0,(0,A.wE)(this.hass,this.entityId).then((e=>{const{platform:t,data:i}=e;this.entityPlatform=t,this._config=i})).catch((e=>{F.warn("Fetching entity config failed.",e),this.entityPlatform=void 0})).finally((()=>{this._loading=!1})))}}},{kind:"method",key:"render",value:function(){return this.hass&&this.knx.project&&this._intent&&!this._loading?"edit"===this._intent?this._renderEdit():this._renderCreate():o.qy` <hass-loading-screen></hass-loading-screen> `}},{kind:"method",key:"_renderCreate",value:function(){if(!this.entityPlatform)return this._renderTypeSelection();const e=T[this.entityPlatform];return e?this._renderEntityConfig(e,!0):(F.error("Unknown platform",this.entityPlatform),this._renderTypeSelection())}},{kind:"method",key:"_renderEdit",value:function(){if(!this.entityPlatform)return this._renderNotFound();const e=T[this.entityPlatform];return e?this._renderEntityConfig(e,!1):(F.error("Unknown platform",this.entityPlatform),this._renderNotFound())}},{kind:"method",key:"_renderNotFound",value:function(){return o.qy`
      <hass-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .back-path=${this.backPath}
        .header=${"Edit entity"}
      >
        <div class="content">
          <ha-alert alert-type="error">Entity not found: <code>${this.entityId}</code></ha-alert>
        </div>
      </hass-subpage>
    `}},{kind:"method",key:"_renderTypeSelection",value:function(){return o.qy`
      <hass-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .back-path=${this.backPath}
        .header=${"Select entity type"}
      >
        <div class="type-selection">
          <ha-card outlined .header=${"Create KNX entity"}>
            <!-- <p>Some help text</p> -->
            <ha-navigation-list
              .hass=${this.hass}
              .narrow=${this.narrow}
              .pages=${Object.entries(T).map((([e,t])=>({name:t.name,description:t.description,iconPath:t.iconPath,iconColor:t.color,path:`/knx/entities/create/${e}`})))}
              hasSecondary
              .label=${"Select entity type"}
            ></ha-navigation-list>
          </ha-card>
        </div>
      </hass-subpage>
    `}},{kind:"method",key:"_renderEntityConfig",value:function(e,t){return o.qy`<hass-subpage
      .hass=${this.hass}
      .narrow=${this.narrow}
      .back-path=${this.backPath}
      .header=${t?"Create new entity":`Edit ${this.entityId}`}
    >
      <div class="content">
        <div class="entity-config">
          <knx-configure-entity
            .hass=${this.hass}
            .knx=${this.knx}
            .platform=${e}
            .config=${this._config}
            .validationErrors=${this._validationErrors}
            @knx-entity-configuration-changed=${this._configChanged}
          >
            ${this._validationBaseError?o.qy`<ha-alert slot="knx-validation-error" alert-type="error">
                  <details>
                    <summary><b>Validation error</b></summary>
                    <p>Base error: ${this._validationBaseError}</p>
                    ${this._validationErrors?.map((e=>o.qy`<p>
                          ${e.error_class}: ${e.error_message} in ${e.path?.join(" / ")}
                        </p>`))??o.s6}
                  </details>
                </ha-alert>`:o.s6}
          </knx-configure-entity>
          <ha-fab
            .label=${t?"Create":"Save"}
            extended
            @click=${t?this._entityCreate:this._entityUpdate}
            ?disabled=${void 0===this._config}
          >
            <ha-svg-icon slot="icon" .path=${t?"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z":"M5,3A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5.5L18.5,3H17V9A1,1 0 0,1 16,10H8A1,1 0 0,1 7,9V3H5M12,4V9H15V4H12M7,12H17A1,1 0 0,1 18,13V19H6V13A1,1 0 0,1 7,12Z"}></ha-svg-icon>
          </ha-fab>
        </div>
        ${this.knx.project?.project_loaded?o.qy` <div class="panel">
              <knx-project-device-tree
                .data=${this.knx.project.knxproject}
                .validDPTs=${(e=>{const t=[];return e.forEach((e=>{e.selectors.forEach((e=>{"group_address"===e.type&&(e.options.validDPTs?t.push(...e.options.validDPTs):e.options.dptSelect&&t.push(...e.options.dptSelect.map((e=>e.dpt))))}))})),t.reduce(((e,t)=>e.some((e=>{return a=t,(i=e).main===a.main&&i.sub===a.sub;var i,a}))?e:e.concat([t])),[])})(e.schema)}
              ></knx-project-device-tree>
            </div>`:o.s6}
      </div>
    </hass-subpage>`}},{kind:"method",key:"_configChanged",value:function(e){e.stopPropagation(),F.warn("configChanged",e.detail),this._config=e.detail,this._validationErrors&&this._entityValidate()}},{kind:"field",key:"_entityValidate",value(){return(0,p.n)((()=>{F.debug("validate",this._config),void 0!==this._config&&void 0!==this.entityPlatform&&(0,A.UD)(this.hass,{platform:this.entityPlatform,data:this._config}).then((e=>{this._handleValidationError(e,!1)})).catch((e=>{F.error("validateEntity",e),(0,c.o)("/knx/error",{replace:!0,data:e})}))}),250)}},{kind:"method",key:"_entityCreate",value:function(e){e.stopPropagation(),void 0!==this._config&&void 0!==this.entityPlatform?(0,A.S$)(this.hass,{platform:this.entityPlatform,data:this._config}).then((e=>{this._handleValidationError(e,!0)||(F.debug("Successfully created entity",e.entity_id),(0,c.o)("/knx/entities",{replace:!0}),e.entity_id?this._entityMoreInfoSettings(e.entity_id):F.error("entity_id not found after creation."))})).catch((e=>{F.error("Error creating entity",e),(0,c.o)("/knx/error",{replace:!0,data:e})})):F.error("No config found.")}},{kind:"method",key:"_entityUpdate",value:function(e){e.stopPropagation(),void 0!==this._config&&void 0!==this.entityId&&void 0!==this.entityPlatform?(0,A.zU)(this.hass,{platform:this.entityPlatform,entity_id:this.entityId,data:this._config}).then((e=>{this._handleValidationError(e,!0)||(F.debug("Successfully updated entity",this.entityId),(0,c.o)("/knx/entities",{replace:!0}))})).catch((e=>{F.error("Error updating entity",e),(0,c.o)("/knx/error",{replace:!0,data:e})})):F.error("No config found.")}},{kind:"method",key:"_handleValidationError",value:function(e,t){return!1===e.success?(F.warn("Validation error",e),this._validationErrors=e.errors,this._validationBaseError=e.error_base,t&&setTimeout((()=>this._alertElement.scrollIntoView({behavior:"smooth"}))),!0):(this._validationErrors=void 0,this._validationBaseError=void 0,F.debug("Validation passed",e.entity_id),!1)}},{kind:"method",key:"_entityMoreInfoSettings",value:function(e){(0,u.r)(h.G.document.querySelector("home-assistant"),"hass-more-info",{entityId:e,view:"settings"})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      hass-loading-screen {
        --app-header-background-color: var(--sidebar-background-color);
        --app-header-text-color: var(--sidebar-text-color);
      }

      .type-selection {
        margin: 20px auto 80px;
        max-width: 720px;
      }

      @media screen and (max-width: 600px) {
        .panel {
          display: none;
        }
      }

      .content {
        display: flex;
        flex-direction: row;
        height: 100%;
        width: 100%;

        & > .entity-config {
          flex-grow: 1;
          flex-shrink: 1;
          height: 100%;
          overflow-y: scroll;
        }

        & > .panel {
          flex-grow: 0;
          flex-shrink: 3;
          width: 480px;
          min-width: 280px;
        }
      }

      knx-configure-entity {
        display: block;
        margin: 20px auto 40px; /* leave 80px space for fab */
        max-width: 720px;
      }

      ha-alert {
        display: block;
        margin: 20px auto;
        max-width: 720px;

        & summary {
          padding: 10px;
        }
      }

      ha-fab {
        /* not slot="fab" to move out of panel */
        float: right;
        margin-right: calc(16px + env(safe-area-inset-right));
        margin-bottom: 40px;
        z-index: 1;
      }
    `}}]}}),o.WF)}};
//# sourceMappingURL=fS05QfA8.js.map