export const id=3391;export const ids=[3391];export const modules={56695:(e,t,a)=>{a.d(t,{Yq:()=>r,zB:()=>l});var i=a(45081),o=a(76415),n=a(84656);(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",month:"long",day:"numeric",timeZone:(0,n.w)(e.time_zone,t)})));const r=(e,t,a)=>s(t,a.time_zone).format(e),s=(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",timeZone:(0,n.w)(e.time_zone,t)}))),l=((0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"short",day:"numeric",timeZone:(0,n.w)(e.time_zone,t)}))),(e,t,a)=>{const i=d(t,a.time_zone);if(t.date_format===o.ow.language||t.date_format===o.ow.system)return i.format(e);const n=i.formatToParts(e),r=n.find((e=>"literal"===e.type))?.value,s=n.find((e=>"day"===e.type))?.value,l=n.find((e=>"month"===e.type))?.value,u=n.find((e=>"year"===e.type))?.value,c=n.at(n.length-1);let h="literal"===c?.type?c?.value:"";"bg"===t.language&&t.date_format===o.ow.YMD&&(h="");return{[o.ow.DMY]:`${s}${r}${l}${r}${u}${h}`,[o.ow.MDY]:`${l}${r}${s}${r}${u}${h}`,[o.ow.YMD]:`${u}${r}${l}${r}${s}${h}`}[t.date_format]}),d=(0,i.A)(((e,t)=>{const a=e.date_format===o.ow.system?void 0:e.language;return e.date_format===o.ow.language||(e.date_format,o.ow.system),new Intl.DateTimeFormat(a,{year:"numeric",month:"numeric",day:"numeric",timeZone:(0,n.w)(e.time_zone,t)})}));(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{day:"numeric",month:"short",timeZone:(0,n.w)(e.time_zone,t)}))),(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{month:"long",year:"numeric",timeZone:(0,n.w)(e.time_zone,t)}))),(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{month:"long",timeZone:(0,n.w)(e.time_zone,t)}))),(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",timeZone:(0,n.w)(e.time_zone,t)}))),(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",timeZone:(0,n.w)(e.time_zone,t)}))),(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"short",timeZone:(0,n.w)(e.time_zone,t)})))},37491:(e,t,a)=>{a.d(t,{r6:()=>r});var i=a(45081),o=(a(56695),a(13634),a(84656)),n=a(49655);const r=(e,t,a)=>s(t,a.time_zone).format(e),s=(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,o.w)(e.time_zone,t)})));(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"short",day:"numeric",hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,o.w)(e.time_zone,t)}))),(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{month:"short",day:"numeric",hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,o.w)(e.time_zone,t)}))),(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,o.w)(e.time_zone,t)})))},13634:(e,t,a)=>{a.d(t,{LW:()=>h,Xs:()=>u,fU:()=>r,ie:()=>l});var i=a(45081),o=a(84656),n=a(49655);const r=(e,t,a)=>s(t,a.time_zone).format(e),s=(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,o.w)(e.time_zone,t)}))),l=(e,t,a)=>d(t,a.time_zone).format(e),d=(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,o.w)(e.time_zone,t)}))),u=(e,t,a)=>c(t,a.time_zone).format(e),c=(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,o.w)(e.time_zone,t)}))),h=(e,t,a)=>m(t,a.time_zone).format(e),m=(0,i.A)(((e,t)=>new Intl.DateTimeFormat("en-GB",{hour:"numeric",minute:"2-digit",hour12:!1,timeZone:(0,o.w)(e.time_zone,t)})))},84656:(e,t,a)=>{a.d(t,{w:()=>n});var i=a(76415);const o=Intl.DateTimeFormat?.().resolvedOptions?.().timeZone??"UTC",n=(e,t)=>e===i.Wj.local&&"UTC"!==o?o:t},49655:(e,t,a)=>{a.d(t,{J:()=>n});var i=a(45081),o=a(76415);const n=(0,i.A)((e=>{if(e.time_format===o.Hg.language||e.time_format===o.Hg.system){const t=e.time_format===o.Hg.language?e.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(t).includes("10")}return e.time_format===o.Hg.am_pm}))},93259:(e,t,a)=>{var i=a(85461),o=a(69534),n=a(98597),r=a(196),s=a(90662),l=a(33167);a(91074),a(52631);const d={boolean:()=>a.e(7150).then(a.bind(a,47150)),constant:()=>a.e(3908).then(a.bind(a,73908)),float:()=>a.e(2292).then(a.bind(a,82292)),grid:()=>a.e(6880).then(a.bind(a,96880)),expandable:()=>a.e(6048).then(a.bind(a,66048)),integer:()=>a.e(3172).then(a.bind(a,73172)),multi_select:()=>a.e(5494).then(a.bind(a,95494)),positive_time_period_dict:()=>a.e(8590).then(a.bind(a,38590)),select:()=>a.e(3644).then(a.bind(a,73644)),string:()=>a.e(9345).then(a.bind(a,39345))},u=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;(0,i.A)([(0,r.EM)("ha-form")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"error",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"warning",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"computeError",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"computeWarning",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"getFormProperties",value:function(){return{}}},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof n.mN&&await t.updateComplete,t.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{"selector"in e||d[e.type]?.()}))}},{kind:"method",key:"render",value:function(){return n.qy`
      <div class="root" part="root">
        ${this.error&&this.error.base?n.qy`
              <ha-alert alert-type="error">
                ${this._computeError(this.error.base,this.schema)}
              </ha-alert>
            `:""}
        ${this.schema.map((e=>{const t=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),a=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return n.qy`
            ${t?n.qy`
                  <ha-alert own-margin alert-type="error">
                    ${this._computeError(t,e)}
                  </ha-alert>
                `:a?n.qy`
                    <ha-alert own-margin alert-type="warning">
                      ${this._computeWarning(a,e)}
                    </ha-alert>
                  `:""}
            ${"selector"in e?n.qy`<ha-selector
                  .schema=${e}
                  .hass=${this.hass}
                  .name=${e.name}
                  .selector=${e.selector}
                  .value=${u(this.data,e)}
                  .label=${this._computeLabel(e,this.data)}
                  .disabled=${e.disabled||this.disabled||!1}
                  .placeholder=${e.required?"":e.default}
                  .helper=${this._computeHelper(e)}
                  .localizeValue=${this.localizeValue}
                  .required=${e.required||!1}
                  .context=${this._generateContext(e)}
                ></ha-selector>`:(0,s._)(this.fieldElementName(e.type),{schema:e,data:u(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:this.hass?.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e),...this.getFormProperties()})}
          `}))}
      </div>
    `}},{kind:"method",key:"fieldElementName",value:function(e){return`ha-form-${e}`}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[a,i]of Object.entries(e.context))t[a]=this.data[i];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=(0,o.A)(a,"createRenderRoot",this,3)([]);return this.addValueChangedListener(e),e}},{kind:"method",key:"addValueChangedListener",value:function(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data={...this.data,...a},(0,l.r)(this,"value-changed",{value:this.data})}))}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return Array.isArray(e)?n.qy`<ul>
        ${e.map((e=>n.qy`<li>
              ${this.computeError?this.computeError(e,t):e}
            </li>`))}
      </ul>`:this.computeError?this.computeError(e,t):e}},{kind:"method",key:"_computeWarning",value:function(e,t){return this.computeWarning?this.computeWarning(e,t):e}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      .root > * {
        display: block;
      }
      .root > *:not([own-margin]):not(:last-child) {
        margin-bottom: 24px;
      }
      ha-alert[own-margin] {
        margin-bottom: 4px;
      }
    `}}]}}),n.WF)},63391:(e,t,a)=>{a.r(t),a.d(t,{HaLocationSelector:()=>M});var i=a(85461),o=a(98597),n=a(196),r=a(45081),s=a(33167),l=a(69534),d=(a(43689),a(66859));function u(e){return(0,d.w)(e,Date.now())}var c=a(78330);function h(e,t){return(0,c.r)((0,d.w)(t?.in||e,e),u(t?.in||e))}var m=a(37491),p=a(13634);const f=e=>e.tileLayer("https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}"+(e.Browser.retina?"@2x.png":".png"),{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',subdomains:"abcd",minZoom:0,maxZoom:20});var y=a(80085),g=a(91330),k=a(14630),v=(a(96396),a(12506));let _=(0,i.A)(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:"entity-id"})],key:"entityId",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"entity-name"})],key:"entityName",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"entity-picture"})],key:"entityPicture",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:"entity-color"})],key:"entityColor",value:void 0},{kind:"method",key:"render",value:function(){return o.qy`
      <div
        class="marker ${this.entityPicture?"picture":""}"
        style=${(0,v.W)({"border-color":this.entityColor})}
        @click=${this._badgeTap}
      >
        ${this.entityPicture?o.qy`<div
              class="entity-picture"
              style=${(0,v.W)({"background-image":`url(${this.entityPicture})`})}
            ></div>`:this.entityName}
      </div>
    `}},{kind:"method",key:"_badgeTap",value:function(e){e.stopPropagation(),this.entityId&&(0,s.r)(this,"hass-more-info",{entityId:this.entityId})}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      .marker {
        display: flex;
        justify-content: center;
        text-align: center;
        align-items: center;
        box-sizing: border-box;
        width: 48px;
        height: 48px;
        font-size: var(--ha-marker-font-size, 1.5em);
        border-radius: var(--ha-marker-border-radius, 50%);
        border: 1px solid var(--ha-marker-color, var(--primary-color));
        color: var(--primary-text-color);
        background-color: var(--card-background-color);
      }
      .marker.picture {
        overflow: hidden;
      }
      .entity-picture {
        background-size: cover;
        height: 100%;
        width: 100%;
      }
    `}}]}}),o.WF);customElements.define("ha-entity-marker",_);const b=e=>"string"==typeof e?e:e.entity_id;(0,i.A)([(0,n.EM)("ha-map")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"entities",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"paths",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"layers",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"autoFit",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"renderPassive",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"interactiveZones",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"fitZones",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:"theme-mode",type:String})],key:"themeMode",value(){return"auto"}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"zoom",value(){return 14}},{kind:"field",decorators:[(0,n.wk)()],key:"_loaded",value(){return!1}},{kind:"field",key:"leafletMap",value:void 0},{kind:"field",key:"Leaflet",value:void 0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"field",key:"_mapItems",value(){return[]}},{kind:"field",key:"_mapFocusItems",value(){return[]}},{kind:"field",key:"_mapZones",value(){return[]}},{kind:"field",key:"_mapFocusZones",value(){return[]}},{kind:"field",key:"_mapPaths",value(){return[]}},{kind:"method",key:"connectedCallback",value:function(){(0,l.A)(i,"connectedCallback",this,3)([]),this._loadMap(),this._attachObserver()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,l.A)(i,"disconnectedCallback",this,3)([]),this.leafletMap&&(this.leafletMap.remove(),this.leafletMap=void 0,this.Leaflet=void 0),this._loaded=!1,this._resizeObserver&&this._resizeObserver.unobserve(this)}},{kind:"method",key:"update",value:function(e){if((0,l.A)(i,"update",this,3)([e]),!this._loaded)return;let t=!1;const a=e.get("hass");if(e.has("_loaded")||e.has("entities"))this._drawEntities(),t=!0;else if(this._loaded&&a&&this.entities)for(const i of this.entities)if(a.states[b(i)]!==this.hass.states[b(i)]){this._drawEntities(),t=!0;break}(e.has("_loaded")||e.has("paths"))&&this._drawPaths(),(e.has("_loaded")||e.has("layers"))&&(this._drawLayers(e.get("layers")),t=!0),(e.has("_loaded")||this.autoFit&&t)&&this.fitMap(),e.has("zoom")&&this.leafletMap.setZoom(this.zoom),(e.has("themeMode")||e.has("hass")&&(!a||a.themes?.darkMode!==this.hass.themes?.darkMode))&&this._updateMapStyle()}},{kind:"get",key:"_darkMode",value:function(){return"dark"===this.themeMode||"auto"===this.themeMode&&Boolean(this.hass.themes.darkMode)}},{kind:"method",key:"_updateMapStyle",value:function(){const e=this.renderRoot.querySelector("#map");e.classList.toggle("dark",this._darkMode),e.classList.toggle("forced-dark","dark"===this.themeMode),e.classList.toggle("forced-light","light"===this.themeMode)}},{kind:"field",key:"_loading",value(){return!1}},{kind:"method",key:"_loadMap",value:async function(){if(this._loading)return;let e=this.shadowRoot.getElementById("map");e||(e=document.createElement("div"),e.id="map",this.shadowRoot.append(e)),this._loading=!0;try{[this.leafletMap,this.Leaflet]=await(async e=>{if(!e.parentNode)throw new Error("Cannot setup Leaflet map on disconnected element");const t=(await a.e(5027).then(a.t.bind(a,75027,23))).default;t.Icon.Default.imagePath="/static/images/leaflet/images/";const i=t.map(e),o=document.createElement("link");return o.setAttribute("href","/static/images/leaflet/leaflet.css"),o.setAttribute("rel","stylesheet"),e.parentNode.appendChild(o),i.setView([52.3731339,4.8903147],13),[i,t,f(t).addTo(i)]})(e),this._updateMapStyle(),this._loaded=!0}finally{this._loading=!1}}},{kind:"method",key:"fitMap",value:function(e){if(!this.leafletMap||!this.Leaflet||!this.hass)return;if(!this._mapFocusItems.length&&!this._mapFocusZones.length&&!this.layers?.length)return void this.leafletMap.setView(new this.Leaflet.LatLng(this.hass.config.latitude,this.hass.config.longitude),e?.zoom||this.zoom);let t=this.Leaflet.latLngBounds(this._mapFocusItems?this._mapFocusItems.map((e=>e.getLatLng())):[]);this._mapFocusZones?.forEach((e=>{t.extend("getBounds"in e?e.getBounds():e.getLatLng())})),this.layers?.forEach((e=>{t.extend("getBounds"in e?e.getBounds():e.getLatLng())})),t=t.pad(e?.pad??.5),this.leafletMap.fitBounds(t,{maxZoom:e?.zoom||this.zoom})}},{kind:"method",key:"fitBounds",value:function(e,t){if(!this.leafletMap||!this.Leaflet||!this.hass)return;const a=this.Leaflet.latLngBounds(e).pad(t?.pad??.5);this.leafletMap.fitBounds(a,{maxZoom:t?.zoom||this.zoom})}},{kind:"method",key:"_drawLayers",value:function(e){if(e&&e.forEach((e=>e.remove())),!this.layers)return;const t=this.leafletMap;this.layers.forEach((e=>{t.addLayer(e)}))}},{kind:"method",key:"_computePathTooltip",value:function(e,t){let a;return a=e.fullDatetime?(0,m.r6)(t.timestamp,this.hass.locale,this.hass.config):h(t.timestamp)?(0,p.ie)(t.timestamp,this.hass.locale,this.hass.config):(0,p.Xs)(t.timestamp,this.hass.locale,this.hass.config),`${e.name}<br>${a}`}},{kind:"method",key:"_drawPaths",value:function(){const e=this.hass,t=this.leafletMap,a=this.Leaflet;if(!e||!t||!a)return;if(this._mapPaths.length&&(this._mapPaths.forEach((e=>e.remove())),this._mapPaths=[]),!this.paths)return;const i=getComputedStyle(this).getPropertyValue("--dark-primary-color");this.paths.forEach((e=>{let o,n;e.gradualOpacity&&(o=e.gradualOpacity/(e.points.length-2),n=1-e.gradualOpacity);for(let t=0;t<e.points.length-1;t++){const r=e.gradualOpacity?n+t*o:void 0;this._mapPaths.push(a.circleMarker(e.points[t].point,{radius:k.C?8:3,color:e.color||i,opacity:r,fillOpacity:r,interactive:!0}).bindTooltip(this._computePathTooltip(e,e.points[t]),{direction:"top"})),this._mapPaths.push(a.polyline([e.points[t].point,e.points[t+1].point],{color:e.color||i,opacity:r,interactive:!1}))}const r=e.points.length-1;if(r>=0){const t=e.gradualOpacity?n+r*o:void 0;this._mapPaths.push(a.circleMarker(e.points[r].point,{radius:k.C?8:3,color:e.color||i,opacity:t,fillOpacity:t,interactive:!0}).bindTooltip(this._computePathTooltip(e,e.points[r]),{direction:"top"}))}this._mapPaths.forEach((e=>t.addLayer(e)))}))}},{kind:"method",key:"_drawEntities",value:function(){const e=this.hass,t=this.leafletMap,a=this.Leaflet;if(!e||!t||!a)return;if(this._mapItems.length&&(this._mapItems.forEach((e=>e.remove())),this._mapItems=[],this._mapFocusItems=[]),this._mapZones.length&&(this._mapZones.forEach((e=>e.remove())),this._mapZones=[],this._mapFocusZones=[]),!this.entities)return;const i=getComputedStyle(this),o=i.getPropertyValue("--accent-color"),n=i.getPropertyValue("--secondary-text-color"),r=i.getPropertyValue("--dark-primary-color"),s=this._darkMode?"dark":"light";for(const l of this.entities){const t=e.states[b(l)];if(!t)continue;const i="string"!=typeof l?l.name:void 0,d=i??(0,g.u)(t),{latitude:u,longitude:c,passive:h,icon:m,radius:p,entity_picture:f,gps_accuracy:k}=t.attributes;if(!u||!c)continue;if("zone"===(0,y.t)(t)){if(h&&!this.renderPassive)continue;let e="";if(m){const t=document.createElement("ha-icon");t.setAttribute("icon",m),e=t.outerHTML}else{const t=document.createElement("span");t.innerHTML=d,e=t.outerHTML}this._mapZones.push(a.marker([u,c],{icon:a.divIcon({html:e,iconSize:[24,24],className:s}),interactive:this.interactiveZones,title:d}));const t=a.circle([u,c],{interactive:!1,color:h?n:o,radius:p});this._mapZones.push(t),!this.fitZones||"string"!=typeof l&&!1===l.focus||this._mapFocusZones.push(t);continue}const v="string"!=typeof l&&"state"===l.label_mode?this.hass.formatEntityState(t):i??d.split(" ").map((e=>e[0])).join("").substr(0,3),_=a.marker([u,c],{icon:a.divIcon({html:`\n              <ha-entity-marker\n                entity-id="${b(l)}"\n                entity-name="${v}"\n                entity-picture="${f?this.hass.hassUrl(f):""}"\n                ${"string"!=typeof l?`entity-color="${l.color}"`:""}\n              ></ha-entity-marker>\n            `,iconSize:[48,48],className:""}),title:d});this._mapItems.push(_),"string"!=typeof l&&!1===l.focus||this._mapFocusItems.push(_),k&&this._mapItems.push(a.circle([u,c],{interactive:!1,color:r,radius:k}))}this._mapItems.forEach((e=>t.addLayer(e))),this._mapZones.forEach((e=>t.addLayer(e)))}},{kind:"method",key:"_attachObserver",value:async function(){this._resizeObserver||(this._resizeObserver=new ResizeObserver((()=>{this.leafletMap?.invalidateSize({debounceMoveend:!0})}))),this._resizeObserver.observe(this)}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        display: block;
        height: 300px;
      }
      #map {
        height: 100%;
      }
      #map.dark {
        background: #090909;
      }
      #map.forced-dark {
        color: #ffffff;
        --map-filter: invert(0.9) hue-rotate(170deg) brightness(1.5)
          contrast(1.2) saturate(0.3);
      }
      #map.forced-light {
        background: #ffffff;
        color: #000000;
        --map-filter: invert(0);
      }
      #map:active {
        cursor: grabbing;
        cursor: -moz-grabbing;
        cursor: -webkit-grabbing;
      }
      .leaflet-tile-pane {
        filter: var(--map-filter);
      }
      .dark .leaflet-bar a {
        background-color: #1c1c1c;
        color: #ffffff;
      }
      .dark .leaflet-bar a:hover {
        background-color: #313131;
      }
      .leaflet-marker-draggable {
        cursor: move !important;
      }
      .leaflet-edit-resize {
        border-radius: 50%;
        cursor: nesw-resize !important;
      }
      .named-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        color: var(--primary-text-color);
      }
      .leaflet-pane {
        z-index: 0 !important;
      }
      .leaflet-control,
      .leaflet-top,
      .leaflet-bottom {
        z-index: 1 !important;
      }
      .leaflet-tooltip {
        padding: 8px;
        font-size: 90%;
        background: rgba(80, 80, 80, 0.9) !important;
        color: white !important;
        border-radius: 4px;
        box-shadow: none !important;
        text-align: center;
      }
    `}}]}}),o.mN),(0,i.A)([(0,n.EM)("ha-locations-editor")],(function(e,t){class i extends t{constructor(){super(),e(this),this._loadPromise=a.e(5027).then(a.t.bind(a,75027,23)).then((e=>a.e(9943).then(a.t.bind(a,19943,23)).then((()=>(this.Leaflet=e.default,this._updateMarkers(),this.updateComplete.then((()=>this.fitMap())))))))}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"locations",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"autoFit",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"zoom",value(){return 16}},{kind:"field",decorators:[(0,n.MZ)({attribute:"theme-mode",type:String})],key:"themeMode",value(){return"auto"}},{kind:"field",decorators:[(0,n.wk)()],key:"_locationMarkers",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_circles",value(){return{}}},{kind:"field",decorators:[(0,n.P)("ha-map",!0)],key:"map",value:void 0},{kind:"field",key:"Leaflet",value:void 0},{kind:"field",key:"_loadPromise",value:void 0},{kind:"method",key:"fitMap",value:function(e){this.map.fitMap(e)}},{kind:"method",key:"fitBounds",value:function(e,t){this.map.fitBounds(e,t)}},{kind:"method",key:"fitMarker",value:async function(e,t){if(this.Leaflet||await this._loadPromise,!this.map.leafletMap||!this._locationMarkers)return;const a=this._locationMarkers[e];if(a)if("getBounds"in a)this.map.leafletMap.fitBounds(a.getBounds()),a.bringToFront();else{const i=this._circles[e];i?this.map.leafletMap.fitBounds(i.getBounds()):this.map.leafletMap.setView(a.getLatLng(),t?.zoom||this.zoom)}}},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-map
        .hass=${this.hass}
        .layers=${this._getLayers(this._circles,this._locationMarkers)}
        .zoom=${this.zoom}
        .autoFit=${this.autoFit}
        .themeMode=${this.themeMode}
      ></ha-map>
      ${this.helper?o.qy`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
    `}},{kind:"field",key:"_getLayers",value(){return(0,r.A)(((e,t)=>{const a=[];return Array.prototype.push.apply(a,Object.values(e)),t&&Array.prototype.push.apply(a,Object.values(t)),a}))}},{kind:"method",key:"willUpdate",value:function(e){(0,l.A)(i,"willUpdate",this,3)([e]),this.Leaflet&&e.has("locations")&&this._updateMarkers()}},{kind:"method",key:"updated",value:function(e){if(this.Leaflet&&e.has("locations")){const t=e.get("locations"),a=this.locations?.filter(((e,a)=>!t[a]||(e.latitude!==t[a].latitude||e.longitude!==t[a].longitude)&&this.map.leafletMap?.getBounds().contains({lat:t[a].latitude,lng:t[a].longitude})&&!this.map.leafletMap?.getBounds().contains({lat:e.latitude,lng:e.longitude})));1===a?.length&&this.map.leafletMap?.panTo({lat:a[0].latitude,lng:a[0].longitude})}}},{kind:"method",key:"_updateLocation",value:function(e){const t=e.target,a=t.getLatLng();let i=a.lng;Math.abs(i)>180&&(i=(i%360+540)%360-180);const o=[a.lat,i];(0,s.r)(this,"location-updated",{id:t.id,location:o},{bubbles:!1})}},{kind:"method",key:"_updateRadius",value:function(e){const t=e.target,a=this._locationMarkers[t.id];(0,s.r)(this,"radius-updated",{id:t.id,radius:a.getRadius()},{bubbles:!1})}},{kind:"method",key:"_markerClicked",value:function(e){const t=e.target;(0,s.r)(this,"marker-clicked",{id:t.id},{bubbles:!1})}},{kind:"method",key:"_updateMarkers",value:function(){if(!this.locations||!this.locations.length)return this._circles={},void(this._locationMarkers=void 0);const e={},t={},a=getComputedStyle(this).getPropertyValue("--accent-color");this.locations.forEach((i=>{let o;if(i.icon||i.iconPath){const e=document.createElement("div");let t;e.className="named-icon",void 0!==i.name&&(e.innerText=i.name),i.icon?(t=document.createElement("ha-icon"),t.setAttribute("icon",i.icon)):(t=document.createElement("ha-svg-icon"),t.setAttribute("path",i.iconPath)),e.prepend(t),o=this.Leaflet.divIcon({html:e.outerHTML,iconSize:[24,24],className:"light"})}if(i.radius){const n=this.Leaflet.circle([i.latitude,i.longitude],{color:i.radius_color||a,radius:i.radius});i.radius_editable||i.location_editable?(n.editing.enable(),n.addEventListener("add",(()=>{const e=n.editing._moveMarker,t=n.editing._resizeMarkers[0];o&&e.setIcon(o),t.id=e.id=i.id,e.addEventListener("dragend",(e=>this._updateLocation(e))).addEventListener("click",(e=>this._markerClicked(e))),i.radius_editable?t.addEventListener("dragend",(e=>this._updateRadius(e))):t.remove()})),e[i.id]=n):t[i.id]=n}if(!i.radius||!i.radius_editable&&!i.location_editable){const t={title:i.name,draggable:i.location_editable};o&&(t.icon=o);const a=this.Leaflet.marker([i.latitude,i.longitude],t).addEventListener("dragend",(e=>this._updateLocation(e))).addEventListener("click",(e=>this._markerClicked(e)));a.id=i.id,e[i.id]=a}})),this._circles=t,this._locationMarkers=e,(0,s.r)(this,"markers-updated")}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-map {
        display: block;
        height: 100%;
      }
    `}}]}}),o.WF);a(93259);let M=(0,i.A)([(0,n.EM)("ha-selector-location")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",key:"_schema",value(){return(0,r.A)(((e,t)=>[{name:"",type:"grid",schema:[{name:"latitude",required:!0,selector:{number:{step:"any"}}},{name:"longitude",required:!0,selector:{number:{step:"any"}}}]},...e?[{name:"radius",required:!0,default:1e3,disabled:!!t,selector:{number:{min:0,step:1,mode:"box"}}}]:[]]))}},{kind:"method",key:"willUpdate",value:function(){this.value||(this.value={latitude:this.hass.config.latitude,longitude:this.hass.config.longitude,radius:this.selector.location?.radius?1e3:void 0})}},{kind:"method",key:"render",value:function(){return o.qy`
      <p>${this.label?this.label:""}</p>
      <ha-locations-editor
        class="flex"
        .hass=${this.hass}
        .helper=${this.helper}
        .locations=${this._location(this.selector,this.value)}
        @location-updated=${this._locationChanged}
        @radius-updated=${this._radiusChanged}
      ></ha-locations-editor>
      <ha-form
        .hass=${this.hass}
        .schema=${this._schema(this.selector.location?.radius,this.selector.location?.radius_readonly)}
        .data=${this.value}
        .computeLabel=${this._computeLabel}
        .disabled=${this.disabled}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"field",key:"_location",value(){return(0,r.A)(((e,t)=>{const a=getComputedStyle(this),i=e.location?.radius?a.getPropertyValue("--zone-radius-color")||a.getPropertyValue("--accent-color"):void 0;return[{id:"location",latitude:!t||isNaN(t.latitude)?this.hass.config.latitude:t.latitude,longitude:!t||isNaN(t.longitude)?this.hass.config.longitude:t.longitude,radius:e.location?.radius?t?.radius||1e3:void 0,radius_color:i,icon:e.location?.icon||e.location?.radius?"mdi:map-marker-radius":"mdi:map-marker",location_editable:!0,radius_editable:!!e.location?.radius&&!e.location?.radius_readonly}]}))}},{kind:"method",key:"_locationChanged",value:function(e){const[t,a]=e.detail.location;(0,s.r)(this,"value-changed",{value:{...this.value,latitude:t,longitude:a}})}},{kind:"method",key:"_radiusChanged",value:function(e){const t=Math.round(e.detail.radius);(0,s.r)(this,"value-changed",{value:{...this.value,radius:t}})}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value,a=Math.round(e.detail.value.radius);(0,s.r)(this,"value-changed",{value:{latitude:t.latitude,longitude:t.longitude,...this.selector.location?.radius&&!this.selector.location?.radius_readonly?{radius:a}:{}}})}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.components.selectors.location.${e.name}`):""}},{kind:"field",static:!0,key:"styles",value(){return o.AH`
    ha-locations-editor {
      display: block;
      height: 400px;
      margin-bottom: 16px;
    }
    p {
      margin-top: 0;
    }
  `}}]}}),o.WF)},76415:(e,t,a)=>{a.d(t,{Hg:()=>o,Wj:()=>n,jG:()=>i,ow:()=>r,zt:()=>s});let i=function(e){return e.language="language",e.system="system",e.comma_decimal="comma_decimal",e.decimal_comma="decimal_comma",e.space_comma="space_comma",e.none="none",e}({}),o=function(e){return e.language="language",e.system="system",e.am_pm="12",e.twenty_four="24",e}({}),n=function(e){return e.local="local",e.server="server",e}({}),r=function(e){return e.language="language",e.system="system",e.DMY="DMY",e.MDY="MDY",e.YMD="YMD",e}({}),s=function(e){return e.language="language",e.monday="monday",e.tuesday="tuesday",e.wednesday="wednesday",e.thursday="thursday",e.friday="friday",e.saturday="saturday",e.sunday="sunday",e}({})},14630:(e,t,a)=>{a.d(t,{C:()=>i});const i="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0},66911:(e,t,a)=>{a.d(t,{x:()=>o});var i=a(66859);function o(e,...t){const a=i.w.bind(null,e||t.find((e=>"object"==typeof e)));return t.map(a)}},6619:(e,t,a)=>{a.d(t,{Cg:()=>n,_P:()=>s,my:()=>i,s0:()=>r,w4:()=>o});Math.pow(10,8);const i=6048e5,o=864e5,n=6e4,r=36e5,s=Symbol.for("constructDateFrom")},66859:(e,t,a)=>{a.d(t,{w:()=>o});var i=a(6619);function o(e,t){return"function"==typeof e?e(t):e&&"object"==typeof e&&i._P in e?e[i._P](t):e instanceof Date?new e.constructor(t):new Date(t)}},78330:(e,t,a)=>{a.d(t,{r:()=>n});var i=a(66911),o=a(5801);function n(e,t,a){const[n,r]=(0,i.x)(a?.in,e,t);return+(0,o.o)(n)==+(0,o.o)(r)}},5801:(e,t,a)=>{a.d(t,{o:()=>o});var i=a(97245);function o(e,t){const a=(0,i.a)(e,t?.in);return a.setHours(0,0,0,0),a}},97245:(e,t,a)=>{a.d(t,{a:()=>o});var i=a(66859);function o(e,t){return(0,i.w)(t||e,e)}}};
//# sourceMappingURL=r4MaHswo.js.map