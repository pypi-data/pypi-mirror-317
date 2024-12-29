/*! For license information please see l16OHnFW.js.LICENSE.txt */
export const id=1565;export const ids=[1565];export const modules={78017:(e,t,a)=>{const n=Intl&&Intl.DateTimeFormat,r=[38,33,36],i=[40,34,35],o=new Set([37,...r]),s=new Set([39,...i]),l=new Set([39,...r]),d=new Set([37,...i]),c=new Set([37,39,...r,...i]);var h=a(76513),u=a(98597),p=a(196),y=a(34078),m=a(2154),f=a(3982);const b=e=>(0,f.ps)(e)?e._$litType$.h:e.strings,_=(0,m.u$)(class extends m.WL{constructor(e){super(e),this.tt=new WeakMap}render(e){return[e]}update(e,[t]){const a=(0,f.qb)(this.et)?b(this.et):null,n=(0,f.qb)(t)?b(t):null;if(null!==a&&(null===n||a!==n)){const t=(0,f.cN)(e).pop();let n=this.tt.get(a);if(void 0===n){const e=document.createDocumentFragment();n=(0,y.XX)(y.s6,e),n.setConnected(!1),this.tt.set(a,n)}(0,f.mY)(n,[t]),(0,f.Dx)(n,void 0,t)}if(null!==n){if(null===a||a!==n){const t=this.tt.get(n);if(void 0!==t){const a=(0,f.cN)(t).pop();(0,f.Jz)(e),(0,f.Dx)(e,void 0,a),(0,f.mY)(e,[a])}}this.et=t}else this.et=void 0;return this.render(t)}});var w=a(69760),g=a(66580);function v(e,t,a){return new Date(Date.UTC(e,t,a))}const k=u.qy`<svg height="24" viewBox="0 0 24 24" width="24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"></path></svg>`,D=u.qy`<svg height="24" viewBox="0 0 24 24" width="24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"></path></svg>`,x=u.AH`
button {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;

  position: relative;
  display: block;
  margin: 0;
  padding: 0;
  background: none; /** NOTE: IE11 fix */
  color: inherit;
  border: none;
  font: inherit;
  text-align: left;
  text-transform: inherit;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}
`,C=(u.AH`
a {
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);

  position: relative;
  display: inline-block;
  background: initial;
  color: inherit;
  font: inherit;
  text-transform: inherit;
  text-decoration: none;
  outline: none;
}
a:focus,
a:focus.page-selected {
  text-decoration: underline;
}
`,u.AH`
svg {
  display: block;
  min-width: var(--svg-icon-min-width, 24px);
  min-height: var(--svg-icon-min-height, 24px);
  fill: var(--svg-icon-fill, currentColor);
  pointer-events: none;
}
`,u.AH`[hidden] { display: none !important; }`,u.AH`
:host {
  display: block;

  /* --app-datepicker-width: 300px; */
  /* --app-datepicker-primary-color: #4285f4; */
  /* --app-datepicker-header-height: 80px; */
}

* {
  box-sizing: border-box;
}
`);function T(e,t){return+t-+e}function S({hasAltKey:e,keyCode:t,focusedDate:a,selectedDate:n,disabledDaysSet:r,disabledDatesSet:i,minTime:c,maxTime:h}){const u=a.getUTCFullYear(),p=a.getUTCMonth(),y=a.getUTCDate(),m=+a,f=n.getUTCFullYear(),b=n.getUTCMonth();let _=u,w=p,g=y,k=!0;switch((b!==p||f!==u)&&(_=f,w=b,g=1,k=34===t||33===t||35===t),k){case m===c&&o.has(t):case m===h&&s.has(t):break;case 38===t:g-=7;break;case 40===t:g+=7;break;case 37===t:g-=1;break;case 39===t:g+=1;break;case 34===t:e?_+=1:w+=1;break;case 33===t:e?_-=1:w-=1;break;case 35===t:w+=1,g=0;break;default:g=1}if(34===t||33===t){const e=v(_,w+1,0).getUTCDate();g>e&&(g=e)}const D=function({keyCode:e,disabledDaysSet:t,disabledDatesSet:a,focusedDate:n,maxTime:r,minTime:i}){const o=+n;let s=o<i,c=o>r;if(T(i,r)<864e5)return n;let h=s||c||t.has(n.getUTCDay())||a.has(o);if(!h)return n;let u=0,p=s===c?n:new Date(s?i-864e5:864e5+r);const y=p.getUTCFullYear(),m=p.getUTCMonth();let f=p.getUTCDate();for(;h;)(s||!c&&l.has(e))&&(f+=1),(c||!s&&d.has(e))&&(f-=1),p=v(y,m,f),u=+p,s||(s=u<i,s&&(p=new Date(i),u=+p,f=p.getUTCDate())),c||(c=u>r,c&&(p=new Date(r),u=+p,f=p.getUTCDate())),h=t.has(p.getUTCDay())||a.has(u);return p}({keyCode:t,maxTime:h,minTime:c,disabledDaysSet:r,disabledDatesSet:i,focusedDate:v(_,w,g)});return D}function F(e,t,a){return e.dispatchEvent(new CustomEvent(t,{detail:a,bubbles:!0,composed:!0}))}function M(e,t){return e.composedPath().find((e=>e instanceof HTMLElement&&t(e)))}function $(e){return t=>e.format(t).replace(/\u200e/gi,"")}function U(e){const t=n(e,{timeZone:"UTC",weekday:"short",month:"short",day:"numeric"}),a=n(e,{timeZone:"UTC",day:"numeric"}),r=n(e,{timeZone:"UTC",year:"numeric",month:"short",day:"numeric"}),i=n(e,{timeZone:"UTC",year:"numeric",month:"long"}),o=n(e,{timeZone:"UTC",weekday:"long"}),s=n(e,{timeZone:"UTC",weekday:"narrow"}),l=n(e,{timeZone:"UTC",year:"numeric"});return{locale:e,dateFormat:$(t),dayFormat:$(a),fullDateFormat:$(r),longMonthYearFormat:$(i),longWeekdayFormat:$(o),narrowWeekdayFormat:$(s),yearFormat:$(l)}}function N(e,t){const a=function(e,t){const a=t.getUTCFullYear(),n=t.getUTCMonth(),r=t.getUTCDate(),i=t.getUTCDay();let o=i;return"first-4-day-week"===e&&(o=3),"first-day-of-year"===e&&(o=6),"first-full-week"===e&&(o=0),v(a,n,r-i+o)}(e,t),n=v(a.getUTCFullYear(),0,1),r=1+(+a-+n)/864e5;return Math.ceil(r/7)}function L(e){if(e>=0&&e<7)return Math.abs(e);return((e<0?7*Math.ceil(Math.abs(e)):0)+e)%7}function W(e,t,a){const n=L(e-t);return a?1+n:n}function E(e){const{dayFormat:t,fullDateFormat:a,locale:n,longWeekdayFormat:r,narrowWeekdayFormat:i,selectedDate:o,disabledDates:s,disabledDays:l,firstDayOfWeek:d,max:c,min:h,showWeekNumber:u,weekLabel:p,weekNumberType:y}=e,m=null==h?Number.MIN_SAFE_INTEGER:+h,f=null==c?Number.MAX_SAFE_INTEGER:+c,b=function(e){const{firstDayOfWeek:t=0,showWeekNumber:a=!1,weekLabel:n,longWeekdayFormat:r,narrowWeekdayFormat:i}=e||{},o=1+(t+(t<0?7:0))%7,s=n||"Wk",l=a?[{label:"Wk"===s?"Week":s,value:s}]:[],d=Array.from(Array(7)).reduce(((e,t,a)=>{const n=v(2017,0,o+a);return e.push({label:r(n),value:i(n)}),e}),l);return d}({longWeekdayFormat:r,narrowWeekdayFormat:i,firstDayOfWeek:d,showWeekNumber:u,weekLabel:p}),_=e=>[n,e.toJSON(),null==s?void 0:s.join("_"),null==l?void 0:l.join("_"),d,null==c?void 0:c.toJSON(),null==h?void 0:h.toJSON(),u,p,y].filter(Boolean).join(":"),w=o.getUTCFullYear(),g=o.getUTCMonth(),k=[-1,0,1].map((e=>{const r=v(w,g+e,1),i=+v(w,g+e+1,0),o=_(r);if(i<m||+r>f)return{key:o,calendar:[],disabledDatesSet:new Set,disabledDaysSet:new Set};const b=function(e){const{date:t,dayFormat:a,disabledDates:n=[],disabledDays:r=[],firstDayOfWeek:i=0,fullDateFormat:o,locale:s="en-US",max:l,min:d,showWeekNumber:c=!1,weekLabel:h="Week",weekNumberType:u="first-4-day-week"}=e||{},p=L(i),y=t.getUTCFullYear(),m=t.getUTCMonth(),f=v(y,m,1),b=new Set(r.map((e=>W(e,p,c)))),_=new Set(n.map((e=>+e))),w=[f.toJSON(),p,s,null==l?"":l.toJSON(),null==d?"":d.toJSON(),Array.from(b).join(","),Array.from(_).join(","),u].filter(Boolean).join(":"),g=W(f.getUTCDay(),p,c),k=null==d?+new Date("2000-01-01"):+d,D=null==l?+new Date("2100-12-31"):+l,x=c?8:7,C=v(y,1+m,0).getUTCDate(),T=[];let S=[],F=!1,M=1;for(const $ of[0,1,2,3,4,5]){for(const e of[0,1,2,3,4,5,6].concat(7===x?[]:[7])){const t=e+$*x;if(!F&&c&&0===e){const e=N(u,v(y,m,M-($<1?p:0))),t=`${h} ${e}`;S.push({fullDate:null,label:t,value:`${e}`,key:`${w}:${t}`,disabled:!0});continue}if(F||t<g){S.push({fullDate:null,label:"",value:"",key:`${w}:${t}`,disabled:!0});continue}const n=v(y,m,M),r=+n,i=b.has(e)||_.has(r)||r<k||r>D;i&&_.add(r),S.push({fullDate:n,label:o(n),value:a(n),key:`${w}:${n.toJSON()}`,disabled:i}),M+=1,M>C&&(F=!0)}T.push(S),S=[]}return{disabledDatesSet:_,calendar:T,disabledDaysSet:new Set(r.map((e=>L(e)))),key:w}}({dayFormat:t,fullDateFormat:a,locale:n,disabledDates:s,disabledDays:l,firstDayOfWeek:d,max:c,min:h,showWeekNumber:u,weekLabel:p,weekNumberType:y,date:r});return{...b,key:o}})),D=[],x=new Set,C=new Set;for(const v of k){const{disabledDatesSet:e,disabledDaysSet:t,...a}=v;if(a.calendar.length>0){if(t.size>0)for(const e of t)C.add(e);if(e.size>0)for(const t of e)x.add(t)}D.push(a)}return{calendars:D,weekdays:b,disabledDatesSet:x,disabledDaysSet:C,key:_(o)}}function Y(e){const t=null==e?new Date:new Date(e),a="string"==typeof e&&(/^\d{4}-\d{2}-\d{2}$/i.test(e)||/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}(Z|\+00:00|-00:00)$/i.test(e)),n="number"==typeof e&&e>0&&isFinite(e);let r=t.getFullYear(),i=t.getMonth(),o=t.getDate();return(a||n)&&(r=t.getUTCFullYear(),i=t.getUTCMonth(),o=t.getUTCDate()),v(r,i,o)}function O(e,t){return e.classList.contains(t)}function q(e,t){return!(null==e||!(t instanceof Date)||isNaN(+t))}function V(e){return e-Math.floor(e)>0?+e.toFixed(3):e}function A(e){return{passive:!0,handleEvent:e}}function Z(e,t){const a="string"==typeof e&&e.length>0?e.split(/,\s*/i):[];return a.length?"function"==typeof t?a.map(t):a:[]}function P(e){if(e instanceof Date&&!isNaN(+e)){const t=e.toJSON();return null==t?"":t.replace(/^(.+)T.+/i,"$1")}return""}function H(e,t){if(T(e,t)<864e5)return[];const a=e.getUTCFullYear();return Array.from(Array(t.getUTCFullYear()-a+1),((e,t)=>t+a))}function z(e,t,a){const n="number"==typeof e?e:+e,r=+t,i=+a;return n<r?r:n>i?i:e}var I,K,j=a(86029);function R(e){const{clientX:t,clientY:a,pageX:n,pageY:r}=e,i=Math.max(n,t),o=Math.max(r,a),s=e.identifier||e.pointerId;return{x:i,y:o,id:null==s?0:s}}function B(e,t){const a=t.changedTouches;if(null==a)return{newPointer:R(t),oldPointer:e};const n=Array.from(a,(e=>R(e)));return{newPointer:null==e?n[0]:n.find((t=>t.id===e.id)),oldPointer:e}}function J(e,t,a){e.addEventListener(t,a,!!j.QQ&&{passive:!0})}class X{constructor(e,t){this._element=e,this._startPointer=null;const{down:a,move:n,up:r}=t;this._down=this._onDown(a),this._move=this._onMove(n),this._up=this._onUp(r),e&&e.addEventListener&&(e.addEventListener("mousedown",this._down),J(e,"touchstart",this._down),J(e,"touchmove",this._move),J(e,"touchend",this._up))}disconnect(){const e=this._element;e&&e.removeEventListener&&(e.removeEventListener("mousedown",this._down),e.removeEventListener("touchstart",this._down),e.removeEventListener("touchmove",this._move),e.removeEventListener("touchend",this._up))}_onDown(e){return t=>{t instanceof MouseEvent&&(this._element.addEventListener("mousemove",this._move),this._element.addEventListener("mouseup",this._up),this._element.addEventListener("mouseleave",this._up));const{newPointer:a}=B(this._startPointer,t);e(a,t),this._startPointer=a}}_onMove(e){return t=>{this._updatePointers(e,t)}}_onUp(e){return t=>{this._updatePointers(e,t,!0)}}_updatePointers(e,t,a){a&&t instanceof MouseEvent&&(this._element.removeEventListener("mousemove",this._move),this._element.removeEventListener("mouseup",this._up),this._element.removeEventListener("mouseleave",this._up));const{newPointer:n,oldPointer:r}=B(this._startPointer,t);e(n,r,t),this._startPointer=a?null:n}}class G extends u.WF{constructor(){super(),this.firstDayOfWeek=0,this.showWeekNumber=!1,this.weekNumberType="first-4-day-week",this.landscape=!1,this.locale=n&&n().resolvedOptions&&n().resolvedOptions().locale||"en-US",this.disabledDays="",this.disabledDates="",this.weekLabel="Wk",this.inline=!1,this.dragRatio=.15,this._hasMin=!1,this._hasMax=!1,this._disabledDaysSet=new Set,this._disabledDatesSet=new Set,this._dx=-1/0,this._hasNativeWebAnimation="animate"in HTMLElement.prototype,this._updatingDateWithKey=!1;const e=Y(),t=U(this.locale),a=P(e),r=Y("2100-12-31");this.value=a,this.startView="calendar",this._min=new Date(e),this._max=new Date(r),this._todayDate=e,this._maxDate=r,this._yearList=H(e,r),this._selectedDate=new Date(e),this._focusedDate=new Date(e),this._formatters=t}get startView(){return this._startView}set startView(e){const t=e||"calendar";if("calendar"!==t&&"yearList"!==t)return;const a=this._startView;this._startView=t,this.requestUpdate("startView",a)}get min(){return this._hasMin?P(this._min):""}set min(e){const t=Y(e),a=q(e,t);this._min=a?t:this._todayDate,this._hasMin=a,this.requestUpdate("min")}get max(){return this._hasMax?P(this._max):""}set max(e){const t=Y(e),a=q(e,t);this._max=a?t:this._maxDate,this._hasMax=a,this.requestUpdate("max")}get value(){return P(this._focusedDate)}set value(e){const t=Y(e),a=q(e,t)?t:this._todayDate;this._focusedDate=new Date(a),this._selectedDate=this._lastSelectedDate=new Date(a)}disconnectedCallback(){super.disconnectedCallback(),this._tracker&&(this._tracker.disconnect(),this._tracker=void 0)}render(){this._formatters.locale!==this.locale&&(this._formatters=U(this.locale));const e="yearList"===this._startView?this._renderDatepickerYearList():this._renderDatepickerCalendar(),t=this.inline?null:u.qy`<div class="datepicker-header" part="header">${this._renderHeaderSelectorButton()}</div>`;return u.qy`
    ${t}
    <div class="datepicker-body" part="body">${_(e)}</div>
    `}firstUpdated(){let e;e="calendar"===this._startView?this.inline?this.shadowRoot.querySelector(".btn__month-selector"):this._buttonSelectorYear:this._yearViewListItem,F(this,"datepicker-first-updated",{firstFocusableElement:e,value:this.value})}async updated(e){const t=this._startView;if(e.has("min")||e.has("max")){this._yearList=H(this._min,this._max),"yearList"===t&&this.requestUpdate();const e=+this._min,a=+this._max;if(T(e,a)>864e5){const t=+this._focusedDate;let n=t;t<e&&(n=e),t>a&&(n=a),this.value=P(new Date(n))}}if(e.has("_startView")||e.has("startView")){if("yearList"===t){const e=48*(this._selectedDate.getUTCFullYear()-this._min.getUTCFullYear()-2);!function(e,t){if(null==e.scrollTo){const{top:a,left:n}=t||{};e.scrollTop=a||0,e.scrollLeft=n||0}else e.scrollTo(t)}(this._yearViewFullList,{top:e,left:0})}if("calendar"===t&&null==this._tracker){const e=this.calendarsContainer;let t=!1,a=!1,n=!1;if(e){const r={down:()=>{n||(t=!0,this._dx=0)},move:(r,i)=>{if(n||!t)return;const o=this._dx,s=o<0&&O(e,"has-max-date")||o>0&&O(e,"has-min-date");!s&&Math.abs(o)>0&&t&&(a=!0,e.style.transform=`translateX(${V(o)}px)`),this._dx=s?0:o+(r.x-i.x)},up:async(r,i,o)=>{if(t&&a){const r=this._dx,i=e.getBoundingClientRect().width/3,o=Math.abs(r)>Number(this.dragRatio)*i,s=350,l="cubic-bezier(0, 0, .4, 1)",d=o?V(i*(r<0?-1:1)):0;n=!0,await async function(e,t){const{hasNativeWebAnimation:a=!1,keyframes:n=[],options:r={duration:100}}=t||{};if(Array.isArray(n)&&n.length)return new Promise((t=>{if(a)e.animate(n,r).onfinish=()=>t();else{const[,a]=n||[],i=()=>{e.removeEventListener("transitionend",i),t()};e.addEventListener("transitionend",i),e.style.transitionDuration=`${r.duration}ms`,r.easing&&(e.style.transitionTimingFunction=r.easing),Object.keys(a).forEach((t=>{t&&(e.style[t]=a[t])}))}}))}(e,{hasNativeWebAnimation:this._hasNativeWebAnimation,keyframes:[{transform:`translateX(${r}px)`},{transform:`translateX(${d}px)`}],options:{duration:s,easing:l}}),o&&this._updateMonth(r<0?"next":"previous").handleEvent(),t=a=n=!1,this._dx=-1/0,e.removeAttribute("style"),F(this,"datepicker-animation-finished")}else t&&(this._updateFocusedDate(o),t=a=!1,this._dx=-1/0)}};this._tracker=new X(e,r)}}e.get("_startView")&&"calendar"===t&&this._focusElement('[part="year-selector"]')}this._updatingDateWithKey&&(this._focusElement('[part="calendars"]:nth-of-type(2) .day--focused'),this._updatingDateWithKey=!1)}_focusElement(e){const t=this.shadowRoot.querySelector(e);t&&t.focus()}_renderHeaderSelectorButton(){const{yearFormat:e,dateFormat:t}=this._formatters,a="calendar"===this.startView,n=this._focusedDate,r=t(n),i=e(n);return u.qy`
    <button
      class="${(0,w.H)({"btn__year-selector":!0,selected:!a})}"
      type="button"
      part="year-selector"
      data-view="${"yearList"}"
      @click="${this._updateView("yearList")}">${i}</button>

    <div class="datepicker-toolbar" part="toolbar">
      <button
        class="${(0,w.H)({"btn__calendar-selector":!0,selected:a})}"
        type="button"
        part="calendar-selector"
        data-view="${"calendar"}"
        @click="${this._updateView("calendar")}">${r}</button>
    </div>
    `}_renderDatepickerYearList(){const{yearFormat:e}=this._formatters,t=this._focusedDate.getUTCFullYear();return u.qy`
    <div class="datepicker-body__year-list-view" part="year-list-view">
      <div class="year-list-view__full-list" part="year-list" @click="${this._updateYear}">
      ${this._yearList.map((a=>u.qy`<button
        class="${(0,w.H)({"year-list-view__list-item":!0,"year--selected":t===a})}"
        type="button"
        part="year"
        .year="${a}">${e(v(a,0,1))}</button>`))}</div>
    </div>
    `}_renderDatepickerCalendar(){const{longMonthYearFormat:e,dayFormat:t,fullDateFormat:a,longWeekdayFormat:n,narrowWeekdayFormat:r}=this._formatters,i=Z(this.disabledDays,Number),o=Z(this.disabledDates,Y),s=this.showWeekNumber,l=this._focusedDate,d=this.firstDayOfWeek,c=Y(),h=this._selectedDate,p=this._max,y=this._min,{calendars:m,disabledDaysSet:f,disabledDatesSet:b,weekdays:_}=E({dayFormat:t,fullDateFormat:a,longWeekdayFormat:n,narrowWeekdayFormat:r,firstDayOfWeek:d,disabledDays:i,disabledDates:o,locale:this.locale,selectedDate:h,showWeekNumber:this.showWeekNumber,weekNumberType:this.weekNumberType,max:p,min:y,weekLabel:this.weekLabel}),v=!m[0].calendar.length,x=!m[2].calendar.length,C=_.map((e=>u.qy`<th
        class="calendar-weekday"
        part="calendar-weekday"
        role="columnheader"
        aria-label="${e.label}"
      >
        <div class="weekday" part="weekday">${e.value}</div>
      </th>`)),T=(0,g.u)(m,(e=>e.key),(({calendar:t},a)=>{if(!t.length)return u.qy`<div class="calendar-container" part="calendar"></div>`;const n=`calendarcaption${a}`,r=t[1][1].fullDate,i=1===a,o=i&&!this._isInVisibleMonth(l,h)?S({disabledDaysSet:f,disabledDatesSet:b,hasAltKey:!1,keyCode:36,focusedDate:l,selectedDate:h,minTime:+y,maxTime:+p}):l;return u.qy`
      <div class="calendar-container" part="calendar">
        <table class="calendar-table" part="table" role="grid" aria-labelledby="${n}">
          <caption id="${n}">
            <div class="calendar-label" part="label">${r?e(r):""}</div>
          </caption>

          <thead role="rowgroup">
            <tr class="calendar-weekdays" part="weekdays" role="row">${C}</tr>
          </thead>

          <tbody role="rowgroup">${t.map((e=>u.qy`<tr role="row">${e.map(((e,t)=>{const{disabled:a,fullDate:n,label:r,value:d}=e;if(!n&&d&&s&&t<1)return u.qy`<th
                      class="full-calendar__day weekday-label"
                      part="calendar-day"
                      scope="row"
                      role="rowheader"
                      abbr="${r}"
                      aria-label="${r}"
                    >${d}</th>`;if(!d||!n)return u.qy`<td class="full-calendar__day day--empty" part="calendar-day"></td>`;const h=+new Date(n),p=+l===h,y=i&&o.getUTCDate()===Number(d);return u.qy`
                  <td
                    tabindex="${y?"0":"-1"}"
                    class="${(0,w.H)({"full-calendar__day":!0,"day--disabled":a,"day--today":+c===h,"day--focused":!a&&p})}"
                    part="calendar-day${+c===h?" calendar-today":""}"
                    role="gridcell"
                    aria-disabled="${a?"true":"false"}"
                    aria-label="${r}"
                    aria-selected="${p?"true":"false"}"
                    .fullDate="${n}"
                    .day="${d}"
                  >
                    <div
                      class="calendar-day"
                      part="day${+c===h?" today":""}"
                    >${d}</div>
                  </td>
                  `}))}</tr>`))}</tbody>
        </table>
      </div>
      `}));return this._disabledDatesSet=b,this._disabledDaysSet=f,u.qy`
    <div class="datepicker-body__calendar-view" part="calendar-view">
      <div class="calendar-view__month-selector" part="month-selectors">
        <div class="month-selector-container">${v?null:u.qy`
          <button
            class="btn__month-selector"
            type="button"
            part="month-selector"
            aria-label="Previous month"
            @click="${this._updateMonth("previous")}"
          >${k}</button>
        `}</div>

        <div class="month-selector-container">${x?null:u.qy`
          <button
            class="btn__month-selector"
            type="button"
            part="month-selector"
            aria-label="Next month"
            @click="${this._updateMonth("next")}"
          >${D}</button>
        `}</div>
      </div>

      <div
        class="${(0,w.H)({"calendars-container":!0,"has-min-date":v,"has-max-date":x})}"
        part="calendars"
        @keyup="${this._updateFocusedDateWithKeyboard}"
      >${T}</div>
    </div>
    `}_updateView(e){return A((()=>{"calendar"===e&&(this._selectedDate=this._lastSelectedDate=new Date(z(this._focusedDate,this._min,this._max))),this._startView=e}))}_updateMonth(e){return A((()=>{if(null==this.calendarsContainer)return this.updateComplete;const t=this._lastSelectedDate||this._selectedDate,a=this._min,n=this._max,r="previous"===e,i=v(t.getUTCFullYear(),t.getUTCMonth()+(r?-1:1),1),o=i.getUTCFullYear(),s=i.getUTCMonth(),l=a.getUTCFullYear(),d=a.getUTCMonth(),c=n.getUTCFullYear(),h=n.getUTCMonth();return o<l||o<=l&&s<d||(o>c||o>=c&&s>h)||(this._lastSelectedDate=i,this._selectedDate=this._lastSelectedDate),this.updateComplete}))}_updateYear(e){const t=M(e,(e=>O(e,"year-list-view__list-item")));if(null==t)return;const a=z(new Date(this._focusedDate).setUTCFullYear(+t.year),this._min,this._max);this._selectedDate=this._lastSelectedDate=new Date(a),this._focusedDate=new Date(a),this._startView="calendar"}_updateFocusedDate(e){const t=M(e,(e=>O(e,"full-calendar__day")));null==t||["day--empty","day--disabled","day--focused","weekday-label"].some((e=>O(t,e)))||(this._focusedDate=new Date(t.fullDate),F(this,"datepicker-value-updated",{isKeypress:!1,value:this.value}))}_updateFocusedDateWithKeyboard(e){const t=e.keyCode;if(13===t||32===t)return F(this,"datepicker-value-updated",{keyCode:t,isKeypress:!0,value:this.value}),void(this._focusedDate=new Date(this._selectedDate));if(9===t||!c.has(t))return;const a=this._selectedDate,n=S({keyCode:t,selectedDate:a,disabledDatesSet:this._disabledDatesSet,disabledDaysSet:this._disabledDaysSet,focusedDate:this._focusedDate,hasAltKey:e.altKey,maxTime:+this._max,minTime:+this._min});this._isInVisibleMonth(n,a)||(this._selectedDate=this._lastSelectedDate=n),this._focusedDate=n,this._updatingDateWithKey=!0,F(this,"datepicker-value-updated",{keyCode:t,isKeypress:!0,value:this.value})}_isInVisibleMonth(e,t){const a=e.getUTCFullYear(),n=e.getUTCMonth(),r=t.getUTCFullYear(),i=t.getUTCMonth();return a===r&&n===i}get calendarsContainer(){return this.shadowRoot.querySelector(".calendars-container")}}G.styles=[C,x,u.AH`
    :host {
      width: 312px;
      /** NOTE: Magic number as 16:9 aspect ratio does not look good */
      /* height: calc((var(--app-datepicker-width) / .66) - var(--app-datepicker-footer-height, 56px)); */
      background-color: var(--app-datepicker-bg-color, #fff);
      color: var(--app-datepicker-color, #000);
      border-radius:
        var(--app-datepicker-border-top-left-radius, 0)
        var(--app-datepicker-border-top-right-radius, 0)
        var(--app-datepicker-border-bottom-right-radius, 0)
        var(--app-datepicker-border-bottom-left-radius, 0);
      contain: content;
      overflow: hidden;
    }
    :host([landscape]) {
      display: flex;

      /** <iphone-5-landscape-width> - <standard-side-margin-width> */
      min-width: calc(568px - 16px * 2);
      width: calc(568px - 16px * 2);
    }

    .datepicker-header + .datepicker-body {
      border-top: 1px solid var(--app-datepicker-separator-color, #ddd);
    }
    :host([landscape]) > .datepicker-header + .datepicker-body {
      border-top: none;
      border-left: 1px solid var(--app-datepicker-separator-color, #ddd);
    }

    .datepicker-header {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      position: relative;
      padding: 16px 24px;
    }
    :host([landscape]) > .datepicker-header {
      /** :this.<one-liner-month-day-width> + :this.<side-padding-width> */
      min-width: calc(14ch + 24px * 2);
    }

    .btn__year-selector,
    .btn__calendar-selector {
      color: var(--app-datepicker-selector-color, rgba(0, 0, 0, .55));
      cursor: pointer;
      /* outline: none; */
    }
    .btn__year-selector.selected,
    .btn__calendar-selector.selected {
      color: currentColor;
    }

    /**
      * NOTE: IE11-only fix. This prevents formatted focused date from overflowing the container.
      */
    .datepicker-toolbar {
      width: 100%;
    }

    .btn__year-selector {
      font-size: 16px;
      font-weight: 700;
    }
    .btn__calendar-selector {
      font-size: 36px;
      font-weight: 700;
      line-height: 1;
    }

    .datepicker-body {
      position: relative;
      width: 100%;
      overflow: hidden;
    }

    .datepicker-body__calendar-view {
      min-height: 56px;
    }

    .calendar-view__month-selector {
      display: flex;
      align-items: center;

      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      padding: 0 8px;
      z-index: 1;
    }

    .month-selector-container {
      max-height: 56px;
      height: 100%;
    }
    .month-selector-container + .month-selector-container {
      margin: 0 0 0 auto;
    }

    .btn__month-selector {
      padding: calc((56px - 24px) / 2);
      /**
        * NOTE: button element contains no text, only SVG.
        * No extra height will incur with such setting.
        */
      line-height: 0;
    }
    .btn__month-selector > svg {
      fill: currentColor;
    }

    .calendars-container {
      display: flex;
      justify-content: center;

      position: relative;
      top: 0;
      left: calc(-100%);
      width: calc(100% * 3);
      transform: translateZ(0);
      will-change: transform;
      /**
        * NOTE: Required for Pointer Events API to work on touch devices.
        * Native \`pan-y\` action will be fired by the browsers since we only care about the
        * horizontal direction. This is great as vertical scrolling still works even when touch
        * event happens on a datepicker's calendar.
        */
      touch-action: pan-y;
      /* outline: none; */
    }

    .year-list-view__full-list {
      max-height: calc(48px * 7);
      overflow-y: auto;

      scrollbar-color: var(--app-datepicker-scrollbar-thumb-bg-color, rgba(0, 0, 0, .35)) rgba(0, 0, 0, 0);
      scrollbar-width: thin;
    }
    .year-list-view__full-list::-webkit-scrollbar {
      width: 8px;
      background-color: rgba(0, 0, 0, 0);
    }
    .year-list-view__full-list::-webkit-scrollbar-thumb {
      background-color: var(--app-datepicker-scrollbar-thumb-bg-color, rgba(0, 0, 0, .35));
      border-radius: 50px;
    }
    .year-list-view__full-list::-webkit-scrollbar-thumb:hover {
      background-color: var(--app-datepicker-scrollbar-thumb-hover-bg-color, rgba(0, 0, 0, .5));
    }

    .calendar-weekdays > th,
    .weekday-label {
      color: var(--app-datepicker-weekday-color, rgba(0, 0, 0, .55));
      font-weight: 400;
      transform: translateZ(0);
      will-change: transform;
    }

    .calendar-container,
    .calendar-label,
    .calendar-table {
      width: 100%;
    }

    .calendar-container {
      position: relative;
      padding: 0 16px 16px;
    }

    .calendar-table {
      -moz-user-select: none;
      -webkit-user-select: none;
      user-select: none;

      border-collapse: collapse;
      border-spacing: 0;
      text-align: center;
    }

    .calendar-label {
      display: flex;
      align-items: center;
      justify-content: center;

      height: 56px;
      font-weight: 500;
      text-align: center;
    }

    .calendar-weekday,
    .full-calendar__day {
      position: relative;
      width: calc(100% / 7);
      height: 0;
      padding: calc(100% / 7 / 2) 0;
      outline: none;
      text-align: center;
    }
    .full-calendar__day:not(.day--disabled):focus {
      outline: #000 dotted 1px;
      outline: -webkit-focus-ring-color auto 1px;
    }
    :host([showweeknumber]) .calendar-weekday,
    :host([showweeknumber]) .full-calendar__day {
      width: calc(100% / 8);
      padding-top: calc(100% / 8);
      padding-bottom: 0;
    }
    :host([showweeknumber]) th.weekday-label {
      padding: 0;
    }

    /**
      * NOTE: Interesting fact! That is ::after will trigger paint when dragging. This will trigger
      * layout and paint on **ONLY** affected nodes. This is much cheaper as compared to rendering
      * all :::after of all calendar day elements. When dragging the entire calendar container,
      * because of all layout and paint trigger on each and every ::after, this becomes a expensive
      * task for the browsers especially on low-end devices. Even though animating opacity is much
      * cheaper, the technique does not work here. Adding 'will-change' will further reduce overall
      * painting at the expense of memory consumption as many cells in a table has been promoted
      * a its own layer.
      */
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.weekday-label) {
      transform: translateZ(0);
      will-change: transform;
    }
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.weekday-label).day--focused::after,
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.day--focused):not(.weekday-label):hover::after {
      content: '';
      display: block;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: var(--app-datepicker-accent-color, #1a73e8);
      border-radius: 50%;
      opacity: 0;
      pointer-events: none;
    }
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.weekday-label) {
      cursor: pointer;
      pointer-events: auto;
      -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    }
    .full-calendar__day.day--focused:not(.day--empty):not(.day--disabled):not(.weekday-label)::after,
    .full-calendar__day.day--today.day--focused:not(.day--empty):not(.day--disabled):not(.weekday-label)::after {
      opacity: 1;
    }

    .calendar-weekday > .weekday,
    .full-calendar__day > .calendar-day {
      display: flex;
      align-items: center;
      justify-content: center;

      position: absolute;
      top: 5%;
      left: 5%;
      width: 90%;
      height: 90%;
      color: currentColor;
      font-size: 14px;
      pointer-events: none;
      z-index: 1;
    }
    .full-calendar__day.day--today {
      color: var(--app-datepicker-accent-color, #1a73e8);
    }
    .full-calendar__day.day--focused,
    .full-calendar__day.day--today.day--focused {
      color: var(--app-datepicker-focused-day-color, #fff);
    }
    .full-calendar__day.day--empty,
    .full-calendar__day.weekday-label,
    .full-calendar__day.day--disabled > .calendar-day {
      pointer-events: none;
    }
    .full-calendar__day.day--disabled:not(.day--today) {
      color: var(--app-datepicker-disabled-day-color, rgba(0, 0, 0, .55));
    }

    .year-list-view__list-item {
      position: relative;
      width: 100%;
      padding: 12px 16px;
      text-align: center;
      /** NOTE: Reduce paint when hovering and scrolling, but this increases memory usage */
      /* will-change: opacity; */
      /* outline: none; */
    }
    .year-list-view__list-item::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: var(--app-datepicker-focused-year-bg-color, #000);
      opacity: 0;
      pointer-events: none;
    }
    .year-list-view__list-item:focus::after {
      opacity: .05;
    }
    .year-list-view__list-item.year--selected {
      color: var(--app-datepicker-accent-color, #1a73e8);
      font-size: 24px;
      font-weight: 500;
    }

    @media (any-hover: hover) {
      .btn__month-selector:hover,
      .year-list-view__list-item:hover {
        cursor: pointer;
      }
      .full-calendar__day:not(.day--empty):not(.day--disabled):not(.day--focused):not(.weekday-label):hover::after {
        opacity: .15;
      }
      .year-list-view__list-item:hover::after {
        opacity: .05;
      }
    }

    @supports (background: -webkit-canvas(squares)) {
      .calendar-container {
        padding: 56px 16px 16px;
      }

      table > caption {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translate3d(-50%, 0, 0);
        will-change: transform;
      }
    }
    `],(0,h.Cg)([(0,p.MZ)({type:Number,reflect:!0})],G.prototype,"firstDayOfWeek",void 0),(0,h.Cg)([(0,p.MZ)({type:Boolean,reflect:!0})],G.prototype,"showWeekNumber",void 0),(0,h.Cg)([(0,p.MZ)({type:String,reflect:!0})],G.prototype,"weekNumberType",void 0),(0,h.Cg)([(0,p.MZ)({type:Boolean,reflect:!0})],G.prototype,"landscape",void 0),(0,h.Cg)([(0,p.MZ)({type:String,reflect:!0})],G.prototype,"startView",null),(0,h.Cg)([(0,p.MZ)({type:String,reflect:!0})],G.prototype,"min",null),(0,h.Cg)([(0,p.MZ)({type:String,reflect:!0})],G.prototype,"max",null),(0,h.Cg)([(0,p.MZ)({type:String})],G.prototype,"value",null),(0,h.Cg)([(0,p.MZ)({type:String})],G.prototype,"locale",void 0),(0,h.Cg)([(0,p.MZ)({type:String})],G.prototype,"disabledDays",void 0),(0,h.Cg)([(0,p.MZ)({type:String})],G.prototype,"disabledDates",void 0),(0,h.Cg)([(0,p.MZ)({type:String})],G.prototype,"weekLabel",void 0),(0,h.Cg)([(0,p.MZ)({type:Boolean})],G.prototype,"inline",void 0),(0,h.Cg)([(0,p.MZ)({type:Number})],G.prototype,"dragRatio",void 0),(0,h.Cg)([(0,p.MZ)({type:Date,attribute:!1})],G.prototype,"_selectedDate",void 0),(0,h.Cg)([(0,p.MZ)({type:Date,attribute:!1})],G.prototype,"_focusedDate",void 0),(0,h.Cg)([(0,p.MZ)({type:String,attribute:!1})],G.prototype,"_startView",void 0),(0,h.Cg)([(0,p.P)(".year-list-view__full-list")],G.prototype,"_yearViewFullList",void 0),(0,h.Cg)([(0,p.P)(".btn__year-selector")],G.prototype,"_buttonSelectorYear",void 0),(0,h.Cg)([(0,p.P)(".year-list-view__list-item")],G.prototype,"_yearViewListItem",void 0),(0,h.Cg)([(0,p.Ls)({passive:!0})],G.prototype,"_updateYear",null),(0,h.Cg)([(0,p.Ls)({passive:!0})],G.prototype,"_updateFocusedDateWithKeyboard",null),I="app-datepicker",K=G,window.customElements&&!window.customElements.get(I)&&window.customElements.define(I,K)},92178:(e,t,a)=>{a.d(t,{q:()=>r});let n={};function r(){return n}},66911:(e,t,a)=>{a.d(t,{x:()=>r});var n=a(66859);function r(e,...t){const a=n.w.bind(null,e||t.find((e=>"object"==typeof e)));return t.map(a)}},6619:(e,t,a)=>{a.d(t,{Cg:()=>i,_P:()=>s,my:()=>n,s0:()=>o,w4:()=>r});Math.pow(10,8);const n=6048e5,r=864e5,i=6e4,o=36e5,s=Symbol.for("constructDateFrom")},66859:(e,t,a)=>{a.d(t,{w:()=>r});var n=a(6619);function r(e,t){return"function"==typeof e?e(t):e&&"object"==typeof e&&n._P in e?e[n._P](t):e instanceof Date?new e.constructor(t):new Date(t)}},5711:(e,t,a)=>{a.d(t,{m:()=>l});var n=a(97245);function r(e){const t=(0,n.a)(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return a.setUTCFullYear(t.getFullYear()),+e-+a}var i=a(66911),o=a(6619),s=a(5801);function l(e,t,a){const[n,l]=(0,i.x)(a?.in,e,t),d=(0,s.o)(n),c=(0,s.o)(l),h=+d-r(d),u=+c-r(c);return Math.round((h-u)/o.w4)}},5801:(e,t,a)=>{a.d(t,{o:()=>r});var n=a(97245);function r(e,t){const a=(0,n.a)(e,t?.in);return a.setHours(0,0,0,0),a}},91791:(e,t,a)=>{a.d(t,{k:()=>i});var n=a(92178),r=a(97245);function i(e,t){const a=(0,n.q)(),i=t?.weekStartsOn??t?.locale?.options?.weekStartsOn??a.weekStartsOn??a.locale?.options?.weekStartsOn??0,o=(0,r.a)(e,t?.in),s=o.getDay(),l=(s<i?7:0)+s-i;return o.setDate(o.getDate()-l),o.setHours(0,0,0,0),o}},97245:(e,t,a)=>{a.d(t,{a:()=>r});var n=a(66859);function r(e,t){return(0,n.w)(t||e,e)}}};
//# sourceMappingURL=l16OHnFW.js.map