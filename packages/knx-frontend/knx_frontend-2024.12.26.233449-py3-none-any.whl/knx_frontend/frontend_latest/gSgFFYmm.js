export const id=7860;export const ids=[7860];export const modules={80106:(e,i,a)=>{a.d(i,{d:()=>t});const t=e=>{switch(e.language){case"cz":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},86640:(e,i,a)=>{var t=a(85461),o=a(98597),l=a(196),s=a(33167);a(26589);(0,t.A)([(0,l.EM)("ha-aliases-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Array})],key:"aliases",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){return this.aliases?o.qy`
      <ha-multi-textfield
        .hass=${this.hass}
        .value=${this.aliases}
        .disabled=${this.disabled}
        .label=${this.hass.localize("ui.dialogs.aliases.label")}
        .removeLabel=${this.hass.localize("ui.dialogs.aliases.remove")}
        .addLabel=${this.hass.localize("ui.dialogs.aliases.add")}
        item-index
        @value-changed=${this._aliasesChanged}
      >
      </ha-multi-textfield>
    `:o.s6}},{kind:"method",key:"_aliasesChanged",value:function(e){(0,s.r)(this,"value-changed",{value:e})}}]}}),o.WF)},96287:(e,i,a)=>{var t=a(85461),o=a(69534),l=(a(8774),a(98597)),s=a(196),r=a(69760),n=a(33167),d=(a(66494),a(96396),a(80106)),c=a(96041);const u="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",h="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z";(0,t.A)([(0,s.EM)("ha-file-upload")],(function(e,i){class a extends i{constructor(...i){super(...i),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"accept",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"icon",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"secondary",value:void 0},{kind:"field",decorators:[(0,s.MZ)()],key:"supports",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Object})],key:"value",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"multiple",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Boolean})],key:"uploading",value(){return!1}},{kind:"field",decorators:[(0,s.MZ)({type:Number})],key:"progress",value:void 0},{kind:"field",decorators:[(0,s.MZ)({type:Boolean,attribute:"auto-open-file-dialog"})],key:"autoOpenFileDialog",value(){return!1}},{kind:"field",decorators:[(0,s.wk)()],key:"_drag",value(){return!1}},{kind:"field",decorators:[(0,s.P)("#input")],key:"_input",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,o.A)(a,"firstUpdated",this,3)([e]),this.autoOpenFileDialog&&this._openFilePicker()}},{kind:"method",key:"render",value:function(){return l.qy`
      ${this.uploading?l.qy`<div class="container">
            <div class="row">
              <span class="header"
                >${this.value?this.hass?.localize("ui.components.file-upload.uploading_name",{name:this.value.toString()}):this.hass?.localize("ui.components.file-upload.uploading")}</span
              >
              ${this.progress?l.qy`<span class="progress"
                    >${this.progress}${(0,d.d)(this.hass.locale)}%</span
                  >`:""}
            </div>
            <mwc-linear-progress
              .indeterminate=${!this.progress}
              .progress=${this.progress?this.progress/100:void 0}
            ></mwc-linear-progress>
          </div>`:l.qy`<label
            for=${this.value?"":"input"}
            class="container ${(0,r.H)({dragged:this._drag,multiple:this.multiple,value:Boolean(this.value)})}"
            @drop=${this._handleDrop}
            @dragenter=${this._handleDragStart}
            @dragover=${this._handleDragStart}
            @dragleave=${this._handleDragEnd}
            @dragend=${this._handleDragEnd}
            >${this.value?"string"==typeof this.value?l.qy`<div class="row">
                    <div class="value" @click=${this._openFilePicker}>
                      <ha-svg-icon
                        .path=${this.icon||h}
                      ></ha-svg-icon>
                      ${this.value}
                    </div>
                    <ha-icon-button
                      @click=${this._clearValue}
                      .label=${this.hass?.localize("ui.common.delete")||"Delete"}
                      .path=${u}
                    ></ha-icon-button>
                  </div>`:(this.value instanceof FileList?Array.from(this.value):(0,c.e)(this.value)).map((e=>l.qy`<div class="row">
                        <div class="value" @click=${this._openFilePicker}>
                          <ha-svg-icon
                            .path=${this.icon||h}
                          ></ha-svg-icon>
                          ${e.name} - ${((e=0,i=2)=>{if(0===e)return"0 Bytes";i=i<0?0:i;const a=Math.floor(Math.log(e)/Math.log(1024));return`${parseFloat((e/1024**a).toFixed(i))} ${["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][a]}`})(e.size)}
                        </div>
                        <ha-icon-button
                          @click=${this._clearValue}
                          .label=${this.hass?.localize("ui.common.delete")||"Delete"}
                          .path=${u}
                        ></ha-icon-button>
                      </div>`)):l.qy`<ha-svg-icon
                    class="big-icon"
                    .path=${this.icon||h}
                  ></ha-svg-icon>
                  <ha-button unelevated @click=${this._openFilePicker}>
                    ${this.label||this.hass?.localize("ui.components.file-upload.label")}
                  </ha-button>
                  <span class="secondary"
                    >${this.secondary||this.hass?.localize("ui.components.file-upload.secondary")}</span
                  >
                  <span class="supports">${this.supports}</span>`}
            <input
              id="input"
              type="file"
              class="file"
              .accept=${this.accept}
              .multiple=${this.multiple}
              @change=${this._handleFilePicked}
          /></label>`}
    `}},{kind:"method",key:"_openFilePicker",value:function(){this._input?.click()}},{kind:"method",key:"_handleDrop",value:function(e){e.preventDefault(),e.stopPropagation(),e.dataTransfer?.files&&(0,n.r)(this,"file-picked",{files:this.multiple||1===e.dataTransfer.files.length?Array.from(e.dataTransfer.files):[e.dataTransfer.files[0]]}),this._drag=!1}},{kind:"method",key:"_handleDragStart",value:function(e){e.preventDefault(),e.stopPropagation(),this._drag=!0}},{kind:"method",key:"_handleDragEnd",value:function(e){e.preventDefault(),e.stopPropagation(),this._drag=!1}},{kind:"method",key:"_handleFilePicked",value:function(e){0!==e.target.files.length&&(this.value=e.target.files,(0,n.r)(this,"file-picked",{files:e.target.files}))}},{kind:"method",key:"_clearValue",value:function(e){e.preventDefault(),this._input.value="",this.value=void 0,(0,n.r)(this,"change")}},{kind:"get",static:!0,key:"styles",value:function(){return l.AH`
      :host {
        display: block;
        height: 240px;
      }
      :host([disabled]) {
        pointer-events: none;
        color: var(--disabled-text-color);
      }
      .container {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: solid 1px
          var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
        border-radius: var(--mdc-shape-small, 4px);
        height: 100%;
      }
      label.container {
        border: dashed 1px
          var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
        cursor: pointer;
      }
      :host([disabled]) .container {
        border-color: var(--disabled-color);
      }
      label.dragged {
        border-color: var(--primary-color);
      }
      .dragged:before {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: var(--primary-color);
        content: "";
        opacity: var(--dark-divider-opacity);
        pointer-events: none;
        border-radius: var(--mdc-shape-small, 4px);
      }
      label.value {
        cursor: default;
      }
      label.value.multiple {
        justify-content: unset;
        overflow: auto;
      }
      .highlight {
        color: var(--primary-color);
      }
      .row {
        display: flex;
        width: 100%;
        align-items: center;
        justify-content: space-between;
        padding: 0 16px;
        box-sizing: border-box;
      }
      ha-button {
        margin-bottom: 4px;
      }
      .supports {
        color: var(--secondary-text-color);
        font-size: 12px;
      }
      :host([disabled]) .secondary {
        color: var(--disabled-text-color);
      }
      input.file {
        display: none;
      }
      .value {
        cursor: pointer;
      }
      .value ha-svg-icon {
        margin-right: 8px;
        margin-inline-end: 8px;
        margin-inline-start: initial;
      }
      .big-icon {
        --mdc-icon-size: 48px;
        margin-bottom: 8px;
      }
      ha-button {
        --mdc-button-outline-color: var(--primary-color);
        --mdc-icon-button-size: 24px;
      }
      mwc-linear-progress {
        width: 100%;
        padding: 16px;
        box-sizing: border-box;
      }
      .header {
        font-weight: 500;
      }
      .progress {
        color: var(--secondary-text-color);
      }
    `}}]}}),l.WF)},47385:(e,i,a)=>{var t=a(85461),o=a(98597),l=a(196),s=a(33167),r=a(43799),n=a(10377),d=a(31447);const c=()=>Promise.all([a.e(4857),a.e(2e3)]).then(a.bind(a,12e3));a(66494),a(73279),a(96287);(0,t.A)([(0,l.EM)("ha-picture-upload")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"value",value(){return null}},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"secondary",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"supports",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"currentImageAltText",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"crop",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"cropOptions",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"original",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Number})],key:"size",value(){return 512}},{kind:"field",decorators:[(0,l.wk)()],key:"_uploading",value(){return!1}},{kind:"method",key:"render",value:function(){return this.value?o.qy`<div class="center-vertical">
      <div class="value">
        <img
          .src=${this.value}
          alt=${this.currentImageAltText||this.hass.localize("ui.components.picture-upload.current_image_alt")}
        />
        <div>
          <ha-button
            @click=${this._handleChangeClick}
            .label=${this.hass.localize("ui.components.picture-upload.change_picture")}
          >
          </ha-button>
        </div>
      </div>
    </div>`:o.qy`
        <ha-file-upload
          .hass=${this.hass}
          .icon=${"M18 15V18H15V20H18V23H20V20H23V18H20V15H18M13.3 21H5C3.9 21 3 20.1 3 19V5C3 3.9 3.9 3 5 3H19C20.1 3 21 3.9 21 5V13.3C20.4 13.1 19.7 13 19 13C17.9 13 16.8 13.3 15.9 13.9L14.5 12L11 16.5L8.5 13.5L5 18H13.1C13 18.3 13 18.7 13 19C13 19.7 13.1 20.4 13.3 21Z"}
          .label=${this.label||this.hass.localize("ui.components.picture-upload.label")}
          .secondary=${this.secondary}
          .supports=${this.supports||this.hass.localize("ui.components.picture-upload.supported_formats")}
          .uploading=${this._uploading}
          @file-picked=${this._handleFilePicked}
          @change=${this._handleFileCleared}
          accept="image/png, image/jpeg, image/gif"
        ></ha-file-upload>
      `}},{kind:"method",key:"_handleChangeClick",value:function(){this.value=null,(0,s.r)(this,"change")}},{kind:"method",key:"_handleFilePicked",value:async function(e){const i=e.detail.files[0];this.crop?this._cropFile(i):this._uploadFile(i)}},{kind:"method",key:"_handleFileCleared",value:async function(){this.value=null}},{kind:"method",key:"_cropFile",value:async function(e){var i,a;["image/png","image/jpeg","image/gif"].includes(e.type)?(i=this,a={file:e,options:this.cropOptions||{round:!1,aspectRatio:NaN},croppedCallback:e=>{this._uploadFile(e)}},(0,s.r)(i,"show-dialog",{dialogTag:"image-cropper-dialog",dialogImport:c,dialogParams:a})):(0,d.K$)(this,{text:this.hass.localize("ui.components.picture-upload.unsupported_format")})}},{kind:"method",key:"_uploadFile",value:async function(e){if(["image/png","image/jpeg","image/gif"].includes(e.type)){this._uploading=!0;try{const i=await(0,n.mF)(this.hass,e);this.value=(0,n.Q0)(i.id,this.size,this.original),(0,s.r)(this,"change")}catch(i){(0,d.K$)(this,{text:i.toString()})}finally{this._uploading=!1}}else(0,d.K$)(this,{text:this.hass.localize("ui.components.picture-upload.unsupported_format")})}},{kind:"get",static:!0,key:"styles",value:function(){return[r.RF,o.AH`
        :host {
          display: block;
          height: 240px;
        }
        ha-file-upload {
          height: 100%;
        }
        .center-vertical {
          display: flex;
          align-items: center;
          height: 100%;
        }
        .value {
          width: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        img {
          max-width: 100%;
          max-height: 200px;
          margin-bottom: 4px;
          border-radius: var(--file-upload-image-border-radius);
        }
      `]}}]}}),o.WF)},10377:(e,i,a)=>{a.d(i,{Q0:()=>o,fO:()=>t,mF:()=>l});const t="/api/image/serve/",o=(e,i,a=!1)=>{if(!a&&!i)throw new Error("Size must be provided if original is false");return a?`/api/image/serve/${e}/original`:`/api/image/serve/${e}/${i}x${i}`},l=async(e,i)=>{const a=new FormData;a.append("file",i);const t=await e.fetchWithAuth("/api/image/upload",{method:"POST",body:a});if(413===t.status)throw new Error(`Uploaded image is too large (${i.name})`);if(200!==t.status)throw new Error("Unknown error");return t.json()}}};
//# sourceMappingURL=gSgFFYmm.js.map