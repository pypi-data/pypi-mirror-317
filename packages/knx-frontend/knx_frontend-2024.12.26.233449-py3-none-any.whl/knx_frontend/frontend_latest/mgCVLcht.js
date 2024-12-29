export const id=2e3;export const ids=[2e3];export const modules={12e3:(e,i,o)=>{o.r(i),o.d(i,{HaImagecropperDialog:()=>l});var t=o(85461),a=(o(58068),o(56889)),r=o.n(a),s=o(32609),c=o(98597),p=o(196),n=o(69760),d=(o(88762),o(43799));let l=(0,t.A)([(0,p.EM)("image-cropper-dialog")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,p.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,p.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,p.wk)()],key:"_open",value(){return!1}},{kind:"field",decorators:[(0,p.P)("img",!0)],key:"_image",value:void 0},{kind:"field",key:"_cropper",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._open=!0}},{kind:"method",key:"closeDialog",value:function(){this._open=!1,this._params=void 0,this._cropper?.destroy(),this._cropper=void 0}},{kind:"method",key:"updated",value:function(e){e.has("_params")&&this._params&&(this._cropper?this._cropper.replace(URL.createObjectURL(this._params.file)):(this._image.src=URL.createObjectURL(this._params.file),this._cropper=new(r())(this._image,{aspectRatio:this._params.options.aspectRatio,viewMode:1,dragMode:"move",minCropBoxWidth:50,ready:()=>{URL.revokeObjectURL(this._image.src)}})))}},{kind:"method",key:"render",value:function(){return c.qy`<ha-dialog
      @closed=${this.closeDialog}
      scrimClickAction
      escapeKeyAction
      .open=${this._open}
    >
      <div
        class="container ${(0,n.H)({round:Boolean(this._params?.options.round)})}"
      >
        <img alt=${this.hass.localize("ui.dialogs.image_cropper.crop_image")} />
      </div>
      <mwc-button slot="secondaryAction" @click=${this.closeDialog}>
        ${this.hass.localize("ui.common.cancel")}
      </mwc-button>
      <mwc-button slot="primaryAction" @click=${this._cropImage}>
        ${this.hass.localize("ui.dialogs.image_cropper.crop")}
      </mwc-button>
    </ha-dialog>`}},{kind:"method",key:"_cropImage",value:function(){this._cropper.getCroppedCanvas().toBlob((e=>{if(!e)return;const i=new File([e],this._params.file.name,{type:this._params.options.type||this._params.file.type});this._params.croppedCallback(i),this.closeDialog()}),this._params.options.type||this._params.file.type,this._params.options.quality)}},{kind:"get",static:!0,key:"styles",value:function(){return[d.nA,c.AH`
        ${(0,c.iz)(s)}
        .container {
          max-width: 640px;
        }
        img {
          max-width: 100%;
        }
        .container.round .cropper-view-box,
        .container.round .cropper-face {
          border-radius: 50%;
        }
        .cropper-line,
        .cropper-point,
        .cropper-point.point-se::before {
          background-color: var(--primary-color);
        }
      `]}}]}}),c.WF)}};
//# sourceMappingURL=mgCVLcht.js.map