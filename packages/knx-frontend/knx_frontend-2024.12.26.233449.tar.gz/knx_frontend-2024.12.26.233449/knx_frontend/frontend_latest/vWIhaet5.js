/*! For license information please see vWIhaet5.js.LICENSE.txt */
export const id=7248;export const ids=[7248];export const modules={45063:(t,e,i)=>{var s=i(85461),n=i(98597),a=i(196),o=i(86625),r=i(93758),c=i(80085),d=i(74538);i(29222);(0,s.A)([(0,a.EM)("ha-state-icon")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"stateValue",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"icon",value:void 0},{kind:"method",key:"render",value:function(){const t=this.icon||this.stateObj&&this.hass?.entities[this.stateObj.entity_id]?.icon||this.stateObj?.attributes.icon;if(t)return n.qy`<ha-icon .icon=${t}></ha-icon>`;if(!this.stateObj)return n.s6;if(!this.hass)return this._renderFallback();const e=(0,d.fq)(this.hass,this.stateObj,this.stateValue).then((t=>t?n.qy`<ha-icon .icon=${t}></ha-icon>`:this._renderFallback()));return n.qy`${(0,o.T)(e)}`}},{kind:"method",key:"_renderFallback",value:function(){const t=(0,c.t)(this.stateObj);return n.qy`
      <ha-svg-icon
        .path=${r.n_[t]||r.lW}
      ></ha-svg-icon>
    `}}]}}),n.WF)},7248:(t,e,i)=>{i.r(e),i.d(e,{KNXEntitiesView:()=>v});var s=i(85461),n=i(98597),a=i(196),o=i(45081),r=(i(61424),i(66867),i(97661),i(96396),i(45063),i(29222),i(13314)),c=i(10),d=i(33167),l=i(31447),h=i(39987),u=i(61328);const y=new u.Q("knx-entities-view");let v=(0,s.A)([(0,a.EM)("knx-entities-view")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"knx_entities",value(){return[]}},{kind:"field",decorators:[(0,a.wk)()],key:"filterDevice",value(){return null}},{kind:"method",key:"firstUpdated",value:function(){this._fetchEntities()}},{kind:"method",key:"willUpdate",value:function(){const t=new URLSearchParams(c.G.location.search);this.filterDevice=t.get("device_id")}},{kind:"method",key:"_fetchEntities",value:async function(){(0,h.ek)(this.hass).then((t=>{y.debug(`Fetched ${t.length} entity entries.`),this.knx_entities=t.map((t=>{const e=this.hass.states[t.entity_id],i=t.device_id?this.hass.devices[t.device_id]:void 0,s=t.area_id??i?.area_id,n=s?this.hass.areas[s]:void 0;return{...t,entityState:e,area:n}}))})).catch((t=>{y.error("getEntityEntries",t),(0,r.o)("/knx/error",{replace:!0,data:t})}))}},{kind:"field",key:"_columns",value(){return(0,o.A)((t=>{const e="56px",i="176px";return{icon:{title:"",minWidth:e,maxWidth:e,type:"icon",template:t=>n.qy`
          <ha-state-icon
            slot="item-icon"
            .hass=${this.hass}
            .stateObj=${t.entityState}
          ></ha-state-icon>
        `},friendly_name:{showNarrow:!0,filterable:!0,sortable:!0,title:"Friendly Name",flex:2,template:t=>t.entityState?.attributes.friendly_name??""},entity_id:{filterable:!0,sortable:!0,title:"Entity ID",flex:1},device:{filterable:!0,sortable:!0,title:"Device",flex:1,template:t=>t.device_id?this.hass.devices[t.device_id].name??"":""},device_id:{hidden:!0,title:"Device ID",filterable:!0,template:t=>t.device_id??""},area:{title:"Area",sortable:!0,filterable:!0,flex:1,template:t=>t.area?.name??""},actions:{showNarrow:!0,title:"",minWidth:i,maxWidth:i,type:"icon-button",template:t=>n.qy`
          <ha-icon-button
            .label=${"More info"}
            .path=${"M11 7V9H13V7H11M14 17V15H13V11H10V13H11V15H10V17H14M22 12C22 17.5 17.5 22 12 22C6.5 22 2 17.5 2 12C2 6.5 6.5 2 12 2C17.5 2 22 6.5 22 12M20 12C20 7.58 16.42 4 12 4C7.58 4 4 7.58 4 12C4 16.42 7.58 20 12 20C16.42 20 20 16.42 20 12Z"}
            .entityEntry=${t}
            @click=${this._entityMoreInfo}
          ></ha-icon-button>
          <ha-icon-button
            .label=${this.hass.localize("ui.common.edit")}
            .path=${"M14.06,9L15,9.94L5.92,19H5V18.08L14.06,9M17.66,3C17.41,3 17.15,3.1 16.96,3.29L15.13,5.12L18.88,8.87L20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18.17,3.09 17.92,3 17.66,3M14.06,6.19L3,17.25V21H6.75L17.81,9.94L14.06,6.19Z"}
            .entityEntry=${t}
            @click=${this._entityEdit}
          ></ha-icon-button>
          <ha-icon-button
            .label=${this.hass.localize("ui.common.delete")}
            .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
            .entityEntry=${t}
            @click=${this._entityDelete}
          ></ha-icon-button>
        `}}}))}},{kind:"field",key:"_entityEdit",value(){return t=>{t.stopPropagation();const e=t.target.entityEntry;(0,r.o)("/knx/entities/edit/"+e.entity_id)}}},{kind:"field",key:"_entityMoreInfo",value(){return t=>{t.stopPropagation();const e=t.target.entityEntry;(0,d.r)(c.G.document.querySelector("home-assistant"),"hass-more-info",{entityId:e.entity_id})}}},{kind:"field",key:"_entityDelete",value(){return t=>{t.stopPropagation();const e=t.target.entityEntry;(0,l.dk)(this,{text:`${this.hass.localize("ui.common.delete")} ${e.entity_id}?`}).then((t=>{t&&(0,h.$b)(this.hass,e.entity_id).then((()=>{y.debug("entity deleted",e.entity_id),this._fetchEntities()})).catch((t=>{(0,l.K$)(this,{title:"Deletion failed",text:t})}))}))}}},{kind:"method",key:"render",value:function(){return this.hass&&this.knx_entities?n.qy`
      <hass-tabs-subpage-data-table
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${this.tabs}
        .localizeFunc=${this.knx.localize}
        .columns=${this._columns(this.hass.language)}
        .data=${this.knx_entities}
        .hasFab=${!0}
        .searchLabel=${this.hass.localize("ui.components.data-table.search")}
        .clickable=${!1}
        .filter=${this.filterDevice}
      >
        <ha-fab
          slot="fab"
          .label=${this.hass.localize("ui.common.add")}
          extended
          @click=${this._entityCreate}
        >
          <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage-data-table>
    `:n.qy` <hass-loading-screen></hass-loading-screen> `}},{kind:"method",key:"_entityCreate",value:function(){(0,r.o)("/knx/entities/create")}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      hass-loading-screen {
        --app-header-background-color: var(--sidebar-background-color);
        --app-header-text-color: var(--sidebar-text-color);
      }
    `}}]}}),n.WF)},86625:(t,e,i)=>{i.d(e,{T:()=>u});var s=i(34078),n=i(3982),a=i(3267);class o{constructor(t){this.G=t}disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}}class r{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null===(t=this.Z)||void 0===t||t.call(this),this.Y=this.Z=void 0}}var c=i(2154);const d=t=>!(0,n.sO)(t)&&"function"==typeof t.then,l=1073741823;class h extends a.Kq{constructor(){super(...arguments),this._$C_t=l,this._$Cwt=[],this._$Cq=new o(this),this._$CK=new r}render(...t){var e;return null!==(e=t.find((t=>!d(t))))&&void 0!==e?e:s.c0}update(t,e){const i=this._$Cwt;let n=i.length;this._$Cwt=e;const a=this._$Cq,o=this._$CK;this.isConnected||this.disconnected();for(let s=0;s<e.length&&!(s>this._$C_t);s++){const t=e[s];if(!d(t))return this._$C_t=s,t;s<n&&t===i[s]||(this._$C_t=l,n=0,Promise.resolve(t).then((async e=>{for(;o.get();)await o.get();const i=a.deref();if(void 0!==i){const s=i._$Cwt.indexOf(t);s>-1&&s<i._$C_t&&(i._$C_t=s,i.setValue(e))}})))}return s.c0}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const u=(0,c.u$)(h)}};
//# sourceMappingURL=vWIhaet5.js.map