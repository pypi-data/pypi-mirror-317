export const id=1670;export const ids=[1670];export const modules={20678:(e,a,t)=>{t.d(a,{T:()=>s});var l=t(45081);const s=(e,a)=>{try{return i(a)?.of(e)??e}catch{return e}},i=(0,l.A)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})))},24110:(e,a,t)=>{var l={};t.r(l);var s=t(85461),i=t(69534),n=t(98597),u=t(196),r=t(45081),o=t(33167),d=t(24517),h=t(20678),c=t(66412);t(9484),t(96334);(0,s.A)([(0,u.EM)("ha-language-picker")],(function(e,a){class t extends a{constructor(...a){super(...a),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,u.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,u.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,u.MZ)({type:Array})],key:"languages",value:void 0},{kind:"field",decorators:[(0,u.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,u.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,u.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,u.MZ)({type:Boolean})],key:"nativeName",value(){return!1}},{kind:"field",decorators:[(0,u.MZ)({type:Boolean})],key:"noSort",value(){return!1}},{kind:"field",decorators:[(0,u.wk)()],key:"_defaultLanguages",value(){return[]}},{kind:"field",decorators:[(0,u.P)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,i.A)(t,"firstUpdated",this,3)([e]),this._computeDefaultLanguageOptions()}},{kind:"method",key:"updated",value:function(e){(0,i.A)(t,"updated",this,3)([e]);const a=e.has("hass")&&this.hass&&e.get("hass")&&e.get("hass").locale.language!==this.hass.locale.language;if(e.has("languages")||e.has("value")||a){if(this._select.layoutOptions(),this._select.value!==this.value&&(0,o.r)(this,"value-changed",{value:this._select.value}),!this.value)return;const e=this._getLanguagesOptions(this.languages??this._defaultLanguages,this.nativeName,this.hass?.locale).findIndex((e=>e.value===this.value));-1===e&&(this.value=void 0),a&&this._select.select(e)}}},{kind:"field",key:"_getLanguagesOptions",value(){return(0,r.A)(((e,a,t)=>{let s=[];if(a){const a=l.translationMetadata.translations;s=e.map((e=>{let t=a[e]?.nativeName;if(!t)try{t=new Intl.DisplayNames(e,{type:"language",fallback:"code"}).of(e)}catch(l){t=e}return{value:e,label:t}}))}else t&&(s=e.map((e=>({value:e,label:(0,h.T)(e,t)}))));return!this.noSort&&t&&s.sort(((e,a)=>(0,c.S)(e.label,a.label,t.language))),s}))}},{kind:"method",key:"_computeDefaultLanguageOptions",value:function(){this._defaultLanguages=Object.keys(l.translationMetadata.translations)}},{kind:"method",key:"render",value:function(){const e=this._getLanguagesOptions(this.languages??this._defaultLanguages,this.nativeName,this.hass?.locale),a=this.value??(this.required?e[0]?.value:this.value);return n.qy`
      <ha-select
        .label=${this.label??(this.hass?.localize("ui.components.language-picker.language")||"Language")}
        .value=${a||""}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${d.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${0===e.length?n.qy`<ha-list-item value=""
              >${this.hass?.localize("ui.components.language-picker.no_languages")||"No languages"}</ha-list-item
            >`:e.map((e=>n.qy`
                <ha-list-item .value=${e.value}
                  >${e.label}</ha-list-item
                >
              `))}
      </ha-select>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const a=e.target;""!==a.value&&a.value!==this.value&&(this.value=a.value,(0,o.r)(this,"value-changed",{value:this.value}))}}]}}),n.WF)},71670:(e,a,t)=>{t.r(a),t.d(a,{HaLanguageSelector:()=>n});var l=t(85461),s=t(98597),i=t(196);t(24110);let n=(0,l.A)([(0,i.EM)("ha-selector-language")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,i.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,i.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,i.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return s.qy`
      <ha-language-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .languages=${this.selector.language?.languages}
        .nativeName=${Boolean(this.selector?.language?.native_name)}
        .noSort=${Boolean(this.selector?.language?.no_sort)}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-language-picker>
    `}},{kind:"field",static:!0,key:"styles",value(){return s.AH`
    ha-language-picker {
      width: 100%;
    }
  `}}]}}),s.WF)}};
//# sourceMappingURL=-jgzM4gB.js.map