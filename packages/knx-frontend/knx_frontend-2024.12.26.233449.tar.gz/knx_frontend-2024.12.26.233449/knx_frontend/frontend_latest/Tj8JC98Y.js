export const id=6880;export const ids=[6880];export const modules={96880:(e,t,i)=>{i.r(t),i.d(t,{HaFormGrid:()=>s});var a=i(85461),o=i(69534),r=(i(93259),i(98597)),d=i(196);let s=(0,a.A)([(0,d.EM)("ha-form-grid")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"computeHelper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"localizeValue",value:void 0},{kind:"method",key:"focus",value:async function(){await this.updateComplete,this.renderRoot.querySelector("ha-form")?.focus()}},{kind:"method",key:"updated",value:function(e){(0,o.A)(i,"updated",this,3)([e]),e.has("schema")&&(this.schema.column_min_width?this.style.setProperty("--form-grid-min-width",this.schema.column_min_width):this.style.setProperty("--form-grid-min-width",""))}},{kind:"method",key:"render",value:function(){return r.qy`
      ${this.schema.schema.map((e=>r.qy`
          <ha-form
            .hass=${this.hass}
            .data=${this.data}
            .schema=${[e]}
            .disabled=${this.disabled}
            .computeLabel=${this.computeLabel}
            .computeHelper=${this.computeHelper}
            .localizeValue=${this.localizeValue}
          ></ha-form>
        `))}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`
      :host {
        display: grid !important;
        grid-template-columns: repeat(
          var(--form-grid-column-count, auto-fit),
          minmax(var(--form-grid-min-width, 200px), 1fr)
        );
        grid-column-gap: 8px;
        grid-row-gap: 24px;
      }
      :host > ha-form {
        display: block;
      }
    `}}]}}),r.WF)}};
//# sourceMappingURL=Tj8JC98Y.js.map