/*! For license information please see ank5LayD.js.LICENSE.txt */
export const id=7150;export const ids=[7150];export const modules={47150:(e,t,o)=>{o.r(t),o.d(t,{HaFormBoolean:()=>h});var a=o(85461),i=o(76513),d=o(196),r=o(80487),l=o(4258);let n=class extends r.M{};n.styles=[l.R],n=(0,i.Cg)([(0,d.EM)("mwc-formfield")],n);var s=o(98597),c=o(33167);o(19887);let h=(0,a.A)([(0,d.EM)("ha-form-boolean")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.P)("ha-checkbox",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return s.qy`
      <mwc-formfield .label=${this.label}>
        <ha-checkbox
          .checked=${this.data}
          .disabled=${this.disabled}
          @change=${this._valueChanged}
        ></ha-checkbox>
        <span slot="label">
          <p class="primary">${this.label}</p>
          ${this.helper?s.qy`<p class="secondary">${this.helper}</p>`:s.s6}
        </span>
      </mwc-formfield>
    `}},{kind:"method",key:"_valueChanged",value:function(e){(0,c.r)(this,"value-changed",{value:e.target.checked})}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`
      ha-formfield {
        display: flex;
        min-height: 56px;
        align-items: center;
        --mdc-typography-body2-font-size: 1em;
      }
      p {
        margin: 0;
      }
      .secondary {
        direction: var(--direction);
        padding-top: 4px;
        box-sizing: border-box;
        color: var(--secondary-text-color);
        font-size: 0.875rem;
        font-weight: var(--mdc-typography-body2-font-weight, 400);
      }
    `}}]}}),s.WF)}};
//# sourceMappingURL=ank5LayD.js.map