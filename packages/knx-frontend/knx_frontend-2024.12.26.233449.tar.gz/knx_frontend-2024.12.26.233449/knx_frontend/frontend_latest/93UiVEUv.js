export const id=919;export const ids=[919];export const modules={90919:(a,i,e)=>{e.r(i),e.d(i,{DialogAreaFilter:()=>c});var t=e(85461),s=(e(29805),e(98597)),o=e(196),l=e(69760),n=e(66580),d=e(33167),r=(e(66494),e(88762),e(96396),e(9484),e(69154),e(13473)),h=e(43799);let c=(0,t.A)([(0,o.EM)("dialog-area-filter")],(function(a,i){return{F:class extends i{constructor(...i){super(...i),a(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_dialogParams",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_hidden",value(){return[]}},{kind:"field",decorators:[(0,o.wk)()],key:"_areas",value(){return[]}},{kind:"method",key:"showDialog",value:function(a){this._dialogParams=a,this._hidden=a.initialValue?.hidden??[];const i=a.initialValue?.order??[],e=Object.keys(this.hass.areas);this._areas=e.concat().sort((0,r.dj)(this.hass.areas,i))}},{kind:"method",key:"closeDialog",value:function(){this._dialogParams=void 0,this._hidden=[],this._areas=[],(0,d.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"_submit",value:function(){const a=this._areas.filter((a=>!this._hidden.includes(a))),i={hidden:this._hidden,order:a};this._dialogParams?.submit?.(i),this.closeDialog()}},{kind:"method",key:"_cancel",value:function(){this._dialogParams?.cancel?.(),this.closeDialog()}},{kind:"method",key:"_areaMoved",value:function(a){a.stopPropagation();const{oldIndex:i,newIndex:e}=a.detail,t=this._areas.concat(),s=t.splice(i,1)[0];t.splice(e,0,s),this._areas=t}},{kind:"method",key:"render",value:function(){if(!this._dialogParams||!this.hass)return s.s6;const a=this._areas;return s.qy`
      <ha-dialog
        open
        @closed=${this._cancel}
        .heading=${this._dialogParams.title??this.hass.localize("ui.components.area-filter.title")}
      >
        <ha-sortable
          draggable-selector=".draggable"
          handle-selector=".handle"
          @item-moved=${this._areaMoved}
        >
          <mwc-list class="areas">
            ${(0,n.u)(a,(a=>a),((a,i)=>{const e=!this._hidden.includes(a),t=this.hass.areas[a]?.name||a;return s.qy`
                  <ha-list-item
                    class=${(0,l.H)({hidden:!e,draggable:e})}
                    hasMeta
                    graphic="icon"
                    noninteractive
                  >
                    ${e?s.qy`<ha-svg-icon
                          class="handle"
                          .path=${"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"}
                          slot="graphic"
                        ></ha-svg-icon>`:s.s6}
                    ${t}
                    <ha-icon-button
                      tabindex="0"
                      class="action"
                      .path=${e?"M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z":"M11.83,9L15,12.16C15,12.11 15,12.05 15,12A3,3 0 0,0 12,9C11.94,9 11.89,9 11.83,9M7.53,9.8L9.08,11.35C9.03,11.56 9,11.77 9,12A3,3 0 0,0 12,15C12.22,15 12.44,14.97 12.65,14.92L14.2,16.47C13.53,16.8 12.79,17 12,17A5,5 0 0,1 7,12C7,11.21 7.2,10.47 7.53,9.8M2,4.27L4.28,6.55L4.73,7C3.08,8.3 1.78,10 1,12C2.73,16.39 7,19.5 12,19.5C13.55,19.5 15.03,19.2 16.38,18.66L16.81,19.08L19.73,22L21,20.73L3.27,3M12,7A5,5 0 0,1 17,12C17,12.64 16.87,13.26 16.64,13.82L19.57,16.75C21.07,15.5 22.27,13.86 23,12C21.27,7.61 17,4.5 12,4.5C10.6,4.5 9.26,4.75 8,5.2L10.17,7.35C10.74,7.13 11.35,7 12,7Z"}
                      slot="meta"
                      .label=${this.hass.localize("ui.components.area-filter."+(e?"hide":"show"),{area:t})}
                      .area=${a}
                      @click=${this._toggle}
                    ></ha-icon-button>
                  </ha-list-item>
                `}))}
          </mwc-list>
        </ha-sortable>
        <ha-button slot="secondaryAction" dialogAction="cancel">
          ${this.hass.localize("ui.common.cancel")}
        </ha-button>
        <ha-button @click=${this._submit} slot="primaryAction">
          ${this.hass.localize("ui.common.submit")}
        </ha-button>
      </ha-dialog>
    `}},{kind:"method",key:"_toggle",value:function(a){const i=a.target.area,e=[...this._hidden??[]];e.includes(i)?e.splice(e.indexOf(i),1):e.push(i),this._hidden=e;const t=this._areas.filter((a=>!this._hidden.includes(a))),s=this._areas.filter((a=>this._hidden.includes(a)));this._areas=[...t,...s]}},{kind:"get",static:!0,key:"styles",value:function(){return[h.nA,s.AH`
        ha-dialog {
          /* Place above other dialogs */
          --dialog-z-index: 104;
          --dialog-content-padding: 0;
        }
        ha-list-item {
          overflow: visible;
        }
        .hidden {
          color: var(--disabled-text-color);
        }
        .handle {
          cursor: move; /* fallback if grab cursor is unsupported */
          cursor: grab;
        }
        .actions {
          display: flex;
          flex-direction: row;
        }
        ha-icon-button {
          display: block;
          margin: -12px;
        }
      `]}}]}}),s.WF)}};
//# sourceMappingURL=93UiVEUv.js.map