export const id=9168;export const ids=[9168];export const modules={57162:(e,t,i)=>{i.d(t,{l:()=>a});const a=async e=>{if(navigator.clipboard)try{return void(await navigator.clipboard.writeText(e))}catch{}const t=document.createElement("textarea");t.value=e,document.body.appendChild(t),t.select(),document.execCommand("copy"),document.body.removeChild(t)}},51029:(e,t,i)=>{var a=i(85461),s=i(69534),n=i(98597),o=i(196),r=i(45081),d=i(33167),l=i(24517);const c={key:"Mod-s",run:e=>((0,d.r)(e.dom,"editor-save"),!0)},h=e=>{const t=document.createElement("ha-icon");return t.icon=e.label,t};(0,a.A)([(0,o.EM)("ha-code-editor")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"mode",value(){return"yaml"}},{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"readOnly",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"linewrap",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,attribute:"autocomplete-entities"})],key:"autocompleteEntities",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,attribute:"autocomplete-icons"})],key:"autocompleteIcons",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"error",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_value",value(){return""}},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"field",key:"_iconList",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;const e=this._loadedCodeMirror.highlightingFor(this.codemirror.state,[this._loadedCodeMirror.tags.comment]);return!!this.renderRoot.querySelector(`span.${e}`)}},{kind:"method",key:"connectedCallback",value:function(){(0,s.A)(a,"connectedCallback",this,3)([]),this.hasUpdated&&this.requestUpdate(),this.addEventListener("keydown",l.d),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,s.A)(a,"disconnectedCallback",this,3)([]),this.removeEventListener("keydown",l.d),this.updateComplete.then((()=>{this.codemirror.destroy(),delete this.codemirror}))}},{kind:"method",key:"scheduleUpdate",value:async function(){this._loadedCodeMirror??=await Promise.all([i.e(7807),i.e(8791)]).then(i.bind(i,78791)),(0,s.A)(a,"scheduleUpdate",this,3)([])}},{kind:"method",key:"update",value:function(e){if((0,s.A)(a,"update",this,3)([e]),!this.codemirror)return void this._createCodeMirror();const t=[];e.has("mode")&&t.push({effects:[this._loadedCodeMirror.langCompartment.reconfigure(this._mode),this._loadedCodeMirror.foldingCompartment.reconfigure(this._getFoldingExtensions())]}),e.has("readOnly")&&t.push({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("linewrap")&&t.push({effects:this._loadedCodeMirror.linewrapCompartment.reconfigure(this.linewrap?this._loadedCodeMirror.EditorView.lineWrapping:[])}),e.has("_value")&&this._value!==this.value&&t.push({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),t.length>0&&this.codemirror.dispatch(...t),e.has("error")&&this.classList.toggle("error-state",this.error)}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_createCodeMirror",value:function(){if(!this._loadedCodeMirror)throw new Error("Cannot create editor before CodeMirror is loaded");const e=[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.history(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.crosshairCursor(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.indentationMarkers({thickness:0,activeThickness:1,colors:{activeLight:"var(--secondary-text-color)",activeDark:"var(--secondary-text-color)"}}),this._loadedCodeMirror.keymap.of([...this._loadedCodeMirror.defaultKeymap,...this._loadedCodeMirror.searchKeymap,...this._loadedCodeMirror.historyKeymap,...this._loadedCodeMirror.tabKeyBindings,c]),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.haTheme,this._loadedCodeMirror.haSyntaxHighlighting,this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.linewrapCompartment.of(this.linewrap?this._loadedCodeMirror.EditorView.lineWrapping:[]),this._loadedCodeMirror.EditorView.updateListener.of(this._onUpdate),this._loadedCodeMirror.foldingCompartment.of(this._getFoldingExtensions())];if(!this.readOnly){const t=[];this.autocompleteEntities&&this.hass&&t.push(this._entityCompletions.bind(this)),this.autocompleteIcons&&t.push(this._mdiCompletions.bind(this)),t.length>0&&e.push(this._loadedCodeMirror.autocompletion({override:t,maxRenderedOptions:10}))}this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:e}),parent:this.renderRoot})}},{kind:"field",key:"_getStates",value(){return(0,r.A)((e=>{if(!e)return[];return Object.keys(e).map((t=>({type:"variable",label:t,detail:e[t].attributes.friendly_name,info:`State: ${e[t].state}`})))}))}},{kind:"method",key:"_entityCompletions",value:function(e){const t=e.matchBefore(/[a-z_]{3,}\.\w*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=this._getStates(this.hass.states);return i&&i.length?{from:Number(t.from),options:i,validFor:/^[a-z_]{3,}\.\w*$/}:null}},{kind:"field",key:"_getIconItems",value(){return async()=>{if(!this._iconList){let e;e=(await i.e(3174).then(i.t.bind(i,83174,19))).default,this._iconList=e.map((e=>({type:"variable",label:`mdi:${e.name}`,detail:e.keywords.join(", "),info:h})))}return this._iconList}}},{kind:"method",key:"_mdiCompletions",value:async function(e){const t=e.matchBefore(/mdi:\S*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=await this._getIconItems();return{from:Number(t.from),options:i,validFor:/^mdi:\S*$/}}},{kind:"field",key:"_onUpdate",value(){return e=>{e.docChanged&&(this._value=e.state.doc.toString(),(0,d.r)(this,"value-changed",{value:this._value}))}}},{kind:"field",key:"_getFoldingExtensions",value(){return()=>"yaml"===this.mode?[this._loadedCodeMirror.foldGutter(),this._loadedCodeMirror.foldingOnIndent]:[]}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      :host(.error-state) .cm-gutters {
        border-color: var(--error-state-color, red);
      }
    `}}]}}),n.mN)},42459:(e,t,i)=>{var a=i(85461),s=i(69534),n=i(47420),o=i(98597),r=i(196),d=i(33167),l=i(43799),c=(i(51029),i(34947)),h=i(57162);i(66494);(0,a.A)([(0,r.EM)("ha-yaml-editor")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"yamlSchema",value(){return n.my}},{kind:"field",decorators:[(0,r.MZ)()],key:"defaultValue",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"isValid",value(){return!0}},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"autoUpdate",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"readOnly",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"copyClipboard",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"hasExtraActions",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_yaml",value(){return""}},{kind:"field",decorators:[(0,r.P)("ha-code-editor")],key:"_codeEditor",value:void 0},{kind:"method",key:"setValue",value:function(e){try{this._yaml=(e=>{if("object"!=typeof e||null===e)return!1;for(const t in e)if(Object.prototype.hasOwnProperty.call(e,t))return!1;return!0})(e)?"":(0,n.Bh)(e,{schema:this.yamlSchema,quotingType:'"',noRefs:!0})}catch(t){console.error(t,e),alert(`There was an error converting to YAML: ${t}`)}}},{kind:"method",key:"firstUpdated",value:function(){void 0!==this.defaultValue&&this.setValue(this.defaultValue)}},{kind:"method",key:"willUpdate",value:function(e){(0,s.A)(i,"willUpdate",this,3)([e]),this.autoUpdate&&e.has("value")&&this.setValue(this.value)}},{kind:"method",key:"focus",value:function(){this._codeEditor?.codemirror&&this._codeEditor?.codemirror.focus()}},{kind:"method",key:"render",value:function(){return void 0===this._yaml?o.s6:o.qy`
      ${this.label?o.qy`<p>${this.label}${this.required?" *":""}</p>`:o.s6}
      <ha-code-editor
        .hass=${this.hass}
        .value=${this._yaml}
        .readOnly=${this.readOnly}
        mode="yaml"
        autocomplete-entities
        autocomplete-icons
        .error=${!1===this.isValid}
        @value-changed=${this._onChange}
        dir="ltr"
      ></ha-code-editor>
      ${this.copyClipboard||this.hasExtraActions?o.qy`
            <div class="card-actions">
              ${this.copyClipboard?o.qy`
                    <ha-button @click=${this._copyYaml}>
                      ${this.hass.localize("ui.components.yaml-editor.copy_to_clipboard")}
                    </ha-button>
                  `:o.s6}
              <slot name="extra-actions"></slot>
            </div>
          `:o.s6}
    `}},{kind:"method",key:"_onChange",value:function(e){let t;e.stopPropagation(),this._yaml=e.detail.value;let i=!0;if(this._yaml)try{t=(0,n.Hh)(this._yaml,{schema:this.yamlSchema})}catch(a){i=!1}else t={};this.value=t,this.isValid=i,(0,d.r)(this,"value-changed",{value:t,isValid:i})}},{kind:"get",key:"yaml",value:function(){return this._yaml}},{kind:"method",key:"_copyYaml",value:async function(){this.yaml&&(await(0,h.l)(this.yaml),(0,c.P)(this,{message:this.hass.localize("ui.common.copied_clipboard")}))}},{kind:"get",static:!0,key:"styles",value:function(){return[l.RF,o.AH`
        .card-actions {
          border-radius: var(
            --actions-border-radius,
            0px 0px var(--ha-card-border-radius, 12px)
              var(--ha-card-border-radius, 12px)
          );
          border: 1px solid var(--divider-color);
          padding: 5px 16px;
        }
        ha-code-editor {
          flex-grow: 1;
        }
      `]}}]}}),o.WF)},9168:(e,t,i)=>{i.r(t),i.d(t,{DialogVoiceAssistantPipelineDetail:()=>C});var a=i(85461),s=i(98597),n=i(196),o=i(33167),r=(i(66494),i(32714),i(93259),i(82286)),d=i(43799),l=i(45081);(0,a.A)([(0,n.EM)("assist-pipeline-detail-config")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"supportedLanguages",value:void 0},{kind:"method",key:"focus",value:async function(){await this.updateComplete;const e=this.renderRoot?.querySelector("ha-form");e?.focus()}},{kind:"field",key:"_schema",value(){return(0,l.A)((e=>[{name:"",type:"grid",schema:[{name:"name",required:!0,selector:{text:{}}},e?{name:"language",required:!0,selector:{language:{languages:e}}}:{name:"",type:"constant"}]}]))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){return s.qy`
      <div class="section">
        <div class="intro">
          <h3>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.title")}
          </h3>
          <p>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.description")}
          </p>
        </div>
        <ha-form
          .schema=${this._schema(this.supportedLanguages)}
          .data=${this.data}
          .hass=${this.hass}
          .computeLabel=${this._computeLabel}
        ></ha-form>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`
      .section {
        border: 1px solid var(--divider-color);
        border-radius: 8px;
        box-sizing: border-box;
        padding: 16px;
      }
      .intro {
        margin-bottom: 16px;
      }
      h3 {
        font-weight: normal;
        font-size: 22px;
        line-height: 28px;
        margin-top: 0;
        margin-bottom: 4px;
      }
      p {
        color: var(--secondary-text-color);
        font-size: var(--mdc-typography-body2-font-size, 0.875rem);
        margin-top: 0;
        margin-bottom: 0;
      }
    `}}]}}),s.WF),(0,a.A)([(0,n.EM)("assist-pipeline-detail-conversation")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_supportedLanguages",value:void 0},{kind:"field",key:"_schema",value(){return(0,l.A)(((e,t)=>[{name:"",type:"grid",schema:[{name:"conversation_engine",required:!0,selector:{conversation_agent:{language:e}}},"*"!==t&&t?.length?{name:"conversation_language",required:!0,selector:{language:{languages:t,no_sort:!0}}}:{name:"",type:"constant"}]}]))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){return s.qy`
      <div class="section">
        <div class="intro">
          <h3>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.title")}
          </h3>
          <p>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.description")}
          </p>
        </div>
        <ha-form
          .schema=${this._schema(this.data?.language,this._supportedLanguages)}
          .data=${this.data}
          .hass=${this.hass}
          .computeLabel=${this._computeLabel}
          @supported-languages-changed=${this._supportedLanguagesChanged}
        ></ha-form>
      </div>
    `}},{kind:"method",key:"_supportedLanguagesChanged",value:function(e){"*"===e.detail.value&&setTimeout((()=>{const e={...this.data};e.conversation_language="*",(0,o.r)(this,"value-changed",{value:e})}),0),this._supportedLanguages=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`
      .section {
        border: 1px solid var(--divider-color);
        border-radius: 8px;
        box-sizing: border-box;
        padding: 16px;
      }
      .intro {
        margin-bottom: 16px;
      }
      h3 {
        font-weight: normal;
        font-size: 22px;
        line-height: 28px;
        margin-top: 0;
        margin-bottom: 4px;
      }
      p {
        color: var(--secondary-text-color);
        font-size: var(--mdc-typography-body2-font-size, 0.875rem);
        margin-top: 0;
        margin-bottom: 0;
      }
    `}}]}}),s.WF),(0,a.A)([(0,n.EM)("assist-pipeline-detail-stt")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_supportedLanguages",value:void 0},{kind:"field",key:"_schema",value(){return(0,l.A)(((e,t)=>[{name:"",type:"grid",schema:[{name:"stt_engine",selector:{stt:{language:e}}},t?.length?{name:"stt_language",required:!0,selector:{language:{languages:t,no_sort:!0}}}:{name:"",type:"constant"}]}]))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){return s.qy`
      <div class="section">
        <div class="intro">
          <h3>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.title")}
          </h3>
          <p>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.description")}
          </p>
        </div>
        <ha-form
          .schema=${this._schema(this.data?.language,this._supportedLanguages)}
          .data=${this.data}
          .hass=${this.hass}
          .computeLabel=${this._computeLabel}
          @supported-languages-changed=${this._supportedLanguagesChanged}
        ></ha-form>
      </div>
    `}},{kind:"method",key:"_supportedLanguagesChanged",value:function(e){this._supportedLanguages=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`
      .section {
        border: 1px solid var(--divider-color);
        border-radius: 8px;
        box-sizing: border-box;
        padding: 16px;
      }
      .intro {
        margin-bottom: 16px;
      }
      h3 {
        font-weight: normal;
        font-size: 22px;
        line-height: 28px;
        margin-top: 0;
        margin-bottom: 4px;
      }
      p {
        color: var(--secondary-text-color);
        font-size: var(--mdc-typography-body2-font-size, 0.875rem);
        margin-top: 0;
        margin-bottom: 0;
      }
    `}}]}}),s.WF);const c=()=>i.e(2527).then(i.bind(i,2527));(0,a.A)([(0,n.EM)("assist-pipeline-detail-tts")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_supportedLanguages",value:void 0},{kind:"field",key:"_schema",value(){return(0,l.A)(((e,t)=>[{name:"",type:"grid",schema:[{name:"tts_engine",selector:{tts:{language:e}}},t?.length?{name:"tts_language",required:!0,selector:{language:{languages:t,no_sort:!0}}}:{name:"",type:"constant"},{name:"tts_voice",selector:{tts_voice:{}},context:{language:"tts_language",engineId:"tts_engine"},required:!0}]}]))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){return s.qy`
      <div class="section">
        <div class="content">
          <div class="intro">
          <h3>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.title")}
          </h3>
          <p>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.description")}
          </p>
          </div>
          <ha-form
            .schema=${this._schema(this.data?.language,this._supportedLanguages)}
            .data=${this.data}
            .hass=${this.hass}
            .computeLabel=${this._computeLabel}
            @supported-languages-changed=${this._supportedLanguagesChanged}
          ></ha-form>
        </div>

       ${this.data?.tts_engine?s.qy`<div class="footer">
               <ha-button
                 .label=${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.try_tts")}
                 @click=${this._preview}
               >
               </ha-button>
             </div>`:s.s6}
        </div>
      </div>
    `}},{kind:"method",key:"_preview",value:async function(){if(!this.data)return;const e=this.data.tts_engine,t=this.data.tts_language||void 0,i=this.data.tts_voice||void 0;var a,s;e&&(a=this,s={engine:e,language:t,voice:i},(0,o.r)(a,"show-dialog",{addHistory:!1,dialogTag:"dialog-tts-try",dialogImport:c,dialogParams:s}))}},{kind:"method",key:"_supportedLanguagesChanged",value:function(e){this._supportedLanguages=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`
      .section {
        border: 1px solid var(--divider-color);
        border-radius: 8px;
      }
      .content {
        padding: 16px;
      }
      .intro {
        margin-bottom: 16px;
      }
      h3 {
        font-weight: normal;
        font-size: 22px;
        line-height: 28px;
        margin-top: 0;
        margin-bottom: 4px;
      }
      p {
        color: var(--secondary-text-color);
        font-size: var(--mdc-typography-body2-font-size, 0.875rem);
        margin-top: 0;
        margin-bottom: 0;
      }
      .footer {
        border-top: 1px solid var(--divider-color);
        padding: 8px 16px;
      }
    `}}]}}),s.WF);var h=i(31750);(0,a.A)([(0,n.EM)("assist-pipeline-detail-wakeword")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_wakeWords",value:void 0},{kind:"field",key:"_schema",value(){return(0,l.A)((e=>[{name:"",type:"grid",schema:[{name:"wake_word_entity",selector:{entity:{domain:"wake_word"}}},e?.length?{name:"wake_word_id",required:!0,selector:{select:{mode:"dropdown",sort:!0,options:e.map((e=>({value:e.id,label:e.name})))}}}:{name:"",type:"constant"}]}]))}},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"willUpdate",value:function(e){e.has("data")&&e.get("data")?.wake_word_entity!==this.data?.wake_word_entity&&(e.get("data")?.wake_word_entity&&this.data?.wake_word_id&&(0,o.r)(this,"value-changed",{value:{...this.data,wake_word_id:void 0}}),this._fetchWakeWords())}},{kind:"field",key:"_hasWakeWorkEntities",value(){return(0,l.A)((e=>Object.keys(e).some((e=>e.startsWith("wake_word.")))))}},{kind:"method",key:"render",value:function(){const e=this._hasWakeWorkEntities(this.hass.states);return s.qy`
      <div class="section">
        <div class="content">
          <div class="intro">
            <h3>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.title")}
            </h3>
            <p>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.description")}
            </p>
          </div>
          ${e?s.s6:s.qy`${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.no_wake_words")}
                <a
                  href=${(0,h.o)(this.hass,"/voice_control/install_wake_word_add_on/")}
                  target="_blank"
                  rel="noreferrer noopener"
                  >${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.no_wake_words_link")}</a
                >`}
          <ha-form
            .schema=${this._schema(this._wakeWords)}
            .data=${this.data}
            .hass=${this.hass}
            .computeLabel=${this._computeLabel}
            .disabled=${!e}
          ></ha-form>
        </div>
      </div>
    `}},{kind:"method",key:"_fetchWakeWords",value:async function(){if(this._wakeWords=void 0,!this.data?.wake_word_entity)return;const e=this.data.wake_word_entity,t=await(i=this.hass,a=e,i.callWS({type:"wake_word/info",entity_id:a}));var i,a;this.data.wake_word_entity===e&&(this._wakeWords=t.wake_words,!this.data||this.data?.wake_word_id&&this._wakeWords.some((e=>e.id===this.data.wake_word_id))||(0,o.r)(this,"value-changed",{value:{...this.data,wake_word_id:this._wakeWords[0]?.id}}))}},{kind:"get",static:!0,key:"styles",value:function(){return s.AH`
      .section {
        border: 1px solid var(--divider-color);
        border-radius: 8px;
      }
      .content {
        padding: 16px;
      }
      .intro {
        margin-bottom: 16px;
      }
      h3 {
        font-weight: normal;
        font-size: 22px;
        line-height: 28px;
        margin-top: 0;
        margin-bottom: 4px;
      }
      p {
        color: var(--secondary-text-color);
        font-size: var(--mdc-typography-body2-font-size, 0.875rem);
        margin-top: 0;
        margin-bottom: 0;
      }
      a {
        color: var(--primary-color);
      }
    `}}]}}),s.WF);i(94392),i(91074),i(73279),i(91686);var u=i(17963),p=(i(42459),i(31447));const v={pipeline:"Pipeline",language:"Language"},g={engine:"Engine"},m={engine:"Engine"},_={engine:"Engine",language:"Language",intent_input:"Input"},y={engine:"Engine",language:"Language",voice:"Voice",tts_input:"Input"},k={ready:0,wake_word:1,stt:2,intent:3,tts:4,done:5,error:6},f=(e,t)=>e.init_options?k[e.init_options.start_stage]<=k[t]&&k[t]<=k[e.init_options.end_stage]:t in e,w=(e,t,i)=>"error"in e&&i===t?s.qy`
    <ha-alert alert-type="error">
      ${e.error.message} (${e.error.code})
    </ha-alert>
  `:"",b=(e,t,i,a="-start")=>{const n=t.events.find((e=>e.type===`${i}`+a)),o=t.events.find((e=>e.type===`${i}-end`));if(!n)return"";if(!o)return"error"in t?s.qy`❌`:s.qy`
      <ha-circular-progress size="small" indeterminate></ha-circular-progress>
    `;const r=new Date(o.timestamp).getTime()-new Date(n.timestamp).getTime(),d=(0,u.ZV)(r/1e3,e.locale,{maximumFractionDigits:2});return s.qy`${d}s ✅`},$=(e,t)=>Object.entries(t).map((([t,i])=>s.qy`
      <div class="row">
        <div>${i}</div>
        <div>${e[t]}</div>
      </div>
    `)),x=(e,t)=>{const i={};let a=!1;for(const s in e)s in t||"done"===s||(a=!0,i[s]=e[s]);return a?s.qy`<ha-expansion-panel>
        <span slot="header">Raw</span>
        <ha-yaml-editor readOnly autoUpdate .value=${i}></ha-yaml-editor>
      </ha-expansion-panel>`:""};(0,a.A)([(0,n.EM)("assist-render-pipeline-run")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"pipelineRun",value:void 0},{kind:"method",key:"render",value:function(){const e=this.pipelineRun&&["tts","intent","stt","wake_word"].find((e=>e in this.pipelineRun))||"ready",t=[],i=(this.pipelineRun.init_options&&"text"in this.pipelineRun.init_options.input?this.pipelineRun.init_options.input.text:void 0)||this.pipelineRun?.stt?.stt_output?.text||this.pipelineRun?.intent?.intent_input;return i&&t.push({from:"user",text:i}),this.pipelineRun?.intent?.intent_output?.response?.speech?.plain?.speech&&t.push({from:"hass",text:this.pipelineRun.intent.intent_output.response.speech.plain.speech}),s.qy`
      <ha-card>
        <div class="card-content">
          <div class="row heading">
            <div>Run</div>
            <div>${this.pipelineRun.stage}</div>
          </div>

          ${$(this.pipelineRun.run,v)}
          ${t.length>0?s.qy`
                <div class="messages">
                  ${t.map((({from:e,text:t})=>s.qy`
                      <div class=${`message ${e}`}>${t}</div>
                    `))}
                </div>
                <div style="clear:both"></div>
              `:""}
        </div>
      </ha-card>

      ${w(this.pipelineRun,"ready",e)}
      ${f(this.pipelineRun,"wake_word")?s.qy`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Wake word</span>
                  ${b(this.hass,this.pipelineRun,"wake_word")}
                </div>
                ${this.pipelineRun.wake_word?s.qy`
                      <div class="card-content">
                        ${$(this.pipelineRun.wake_word,m)}
                        ${this.pipelineRun.wake_word.wake_word_output?s.qy`<div class="row">
                                <div>Model</div>
                                <div>
                                  ${this.pipelineRun.wake_word.wake_word_output.ww_id}
                                </div>
                              </div>
                              <div class="row">
                                <div>Timestamp</div>
                                <div>
                                  ${this.pipelineRun.wake_word.wake_word_output.timestamp}
                                </div>
                              </div>`:""}
                        ${x(this.pipelineRun.wake_word,g)}
                      </div>
                    `:""}
              </div>
            </ha-card>
          `:""}
      ${w(this.pipelineRun,"wake_word",e)}
      ${f(this.pipelineRun,"stt")?s.qy`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Speech-to-text</span>
                  ${b(this.hass,this.pipelineRun,"stt","-vad-end")}
                </div>
                ${this.pipelineRun.stt?s.qy`
                      <div class="card-content">
                        ${$(this.pipelineRun.stt,m)}
                        <div class="row">
                          <div>Language</div>
                          <div>${this.pipelineRun.stt.metadata.language}</div>
                        </div>
                        ${this.pipelineRun.stt.stt_output?s.qy`<div class="row">
                              <div>Output</div>
                              <div>${this.pipelineRun.stt.stt_output.text}</div>
                            </div>`:""}
                        ${x(this.pipelineRun.stt,m)}
                      </div>
                    `:""}
              </div>
            </ha-card>
          `:""}
      ${w(this.pipelineRun,"stt",e)}
      ${f(this.pipelineRun,"intent")?s.qy`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Natural Language Processing</span>
                  ${b(this.hass,this.pipelineRun,"intent")}
                </div>
                ${this.pipelineRun.intent?s.qy`
                      <div class="card-content">
                        ${$(this.pipelineRun.intent,_)}
                        ${this.pipelineRun.intent.intent_output?s.qy`<div class="row">
                                <div>Response type</div>
                                <div>
                                  ${this.pipelineRun.intent.intent_output.response.response_type}
                                </div>
                              </div>
                              ${"error"===this.pipelineRun.intent.intent_output.response.response_type?s.qy`<div class="row">
                                    <div>Error code</div>
                                    <div>
                                      ${this.pipelineRun.intent.intent_output.response.data.code}
                                    </div>
                                  </div>`:""}`:""}
                        ${x(this.pipelineRun.intent,_)}
                      </div>
                    `:""}
              </div>
            </ha-card>
          `:""}
      ${w(this.pipelineRun,"intent",e)}
      ${f(this.pipelineRun,"tts")?s.qy`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Text-to-speech</span>
                  ${b(this.hass,this.pipelineRun,"tts")}
                </div>
                ${this.pipelineRun.tts?s.qy`
                      <div class="card-content">
                        ${$(this.pipelineRun.tts,y)}
                        ${x(this.pipelineRun.tts,y)}
                      </div>
                    `:""}
              </div>
              ${this.pipelineRun?.tts?.tts_output?s.qy`
                    <div class="card-actions">
                      <ha-button @click=${this._playTTS}>
                        Play Audio
                      </ha-button>
                    </div>
                  `:""}
            </ha-card>
          `:""}
      ${w(this.pipelineRun,"tts",e)}
      <ha-card>
        <ha-expansion-panel>
          <span slot="header">Raw</span>
          <ha-yaml-editor
            readOnly
            autoUpdate
            .value=${this.pipelineRun}
          ></ha-yaml-editor>
        </ha-expansion-panel>
      </ha-card>
    `}},{kind:"method",key:"_playTTS",value:function(){const e=this.pipelineRun.tts.tts_output.url,t=new Audio(e);t.addEventListener("error",(()=>{(0,p.K$)(this,{title:"Error",text:"Error playing audio"})})),t.addEventListener("canplaythrough",(()=>{t.play()}))}},{kind:"field",static:!0,key:"styles",value(){return s.AH`
    :host {
      display: block;
    }
    ha-card,
    ha-alert {
      display: block;
      margin-bottom: 16px;
    }
    .row {
      display: flex;
      justify-content: space-between;
    }
    .row > div:last-child {
      text-align: right;
    }
    ha-expansion-panel {
      padding-left: 8px;
      padding-inline-start: 8px;
      padding-inline-end: initial;
    }
    .card-content ha-expansion-panel {
      padding-left: 0px;
      padding-inline-start: 0px;
      padding-inline-end: initial;
      --expansion-panel-summary-padding: 0px;
      --expansion-panel-content-padding: 0px;
    }
    .heading {
      font-weight: 500;
      margin-bottom: 16px;
    }

    .messages {
      margin-top: 8px;
    }

    .message {
      font-size: 18px;
      margin: 8px 0;
      padding: 8px;
      border-radius: 15px;
      clear: both;
    }

    .message.user {
      margin-left: 24px;
      margin-inline-start: 24px;
      margin-inline-end: initial;
      float: var(--float-end);
      text-align: right;
      border-bottom-right-radius: 0px;
      background-color: var(--light-primary-color);
      color: var(--text-light-primary-color, var(--primary-text-color));
      direction: var(--direction);
    }

    .message.hass {
      margin-right: 24px;
      margin-inline-end: 24px;
      margin-inline-start: initial;
      float: var(--float-start);
      border-bottom-left-radius: 0px;
      background-color: var(--primary-color);
      color: var(--text-primary-color);
      direction: var(--direction);
    }
  `}}]}}),s.WF),(0,a.A)([(0,n.EM)("assist-render-pipeline-events")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"events",value:void 0},{kind:"field",key:"_processEvents",value(){return(0,l.A)((e=>{let t;return e.forEach((e=>{t=(0,r.QC)(t,e)})),t}))}},{kind:"method",key:"render",value:function(){const e=this._processEvents(this.events);return e?s.qy`
      <assist-render-pipeline-run
        .hass=${this.hass}
        .pipelineRun=${e}
      ></assist-render-pipeline-run>
    `:this.events.length?s.qy`<ha-alert alert-type="error">Error showing run</ha-alert>
          <ha-card>
            <ha-expansion-panel>
              <span slot="header">Raw</span>
              <pre>${JSON.stringify(this.events,null,2)}</pre>
            </ha-expansion-panel>
          </ha-card>`:s.qy`<ha-alert alert-type="warning"
        >There were no events in this run.</ha-alert
      >`}}]}}),s.WF);var M=i(19263);let C=(0,a.A)([(0,n.EM)("dialog-voice-assistant-pipeline-detail")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_data",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_cloudActive",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_submitting",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_supportedLanguages",value:void 0},{kind:"method",key:"showDialog",value:function(e){if(this._params=e,this._error=void 0,this._cloudActive=this._params.cloudActiveSubscription,this._params.pipeline)return void(this._data=this._params.pipeline);let t,i;if(this._cloudActive)for(const a of Object.values(this.hass.entities))if("cloud"===a.platform)if("stt"===(0,M.m)(a.entity_id)){if(t=a.entity_id,i)break}else if("tts"===(0,M.m)(a.entity_id)&&(i=a.entity_id,t))break;this._data={language:(this.hass.config.language||this.hass.locale.language).substring(0,2),stt_engine:t,tts_engine:i}}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._data=void 0,(0,o.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"firstUpdated",value:function(){this._getSupportedLanguages()}},{kind:"method",key:"_getSupportedLanguages",value:async function(){const{languages:e}=await(0,r.ds)(this.hass);this._supportedLanguages=e}},{kind:"method",key:"render",value:function(){if(!this._params||!this._data)return s.s6;const e=this._params.pipeline?.id?this._params.pipeline.name:this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_title");return s.qy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        .heading=${e}
      >
        <ha-dialog-header slot="heading">
          <ha-icon-button
            slot="navigationIcon"
            dialogAction="cancel"
            .label=${this.hass.localize("ui.common.close")}
            .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
          ></ha-icon-button>
          <span slot="title" .title=${e}>${e}</span>
        </ha-dialog-header>
        <div class="content">
          ${this._error?s.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:s.s6}
          <assist-pipeline-detail-config
            .hass=${this.hass}
            .data=${this._data}
            .supportedLanguages=${this._supportedLanguages}
            keys="name,language"
            @value-changed=${this._valueChanged}
            ?dialogInitialFocus=${!this._params.pipeline?.id}
          ></assist-pipeline-detail-config>
          <assist-pipeline-detail-conversation
            .hass=${this.hass}
            .data=${this._data}
            keys="conversation_engine,conversation_language"
            @value-changed=${this._valueChanged}
          ></assist-pipeline-detail-conversation>
          ${this._cloudActive||"cloud"!==this._data.tts_engine&&"cloud"!==this._data.stt_engine?s.s6:s.qy`
                <ha-alert alert-type="warning">
                  ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_message")}
                  <a
                    href="/config/cloud"
                    slot="action"
                    @click=${this.closeDialog}
                  >
                    <ha-button>
                      ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_action")}
                    </ha-button>
                  </a>
                </ha-alert>
              `}
          <assist-pipeline-detail-stt
            .hass=${this.hass}
            .data=${this._data}
            keys="stt_engine,stt_language"
            @value-changed=${this._valueChanged}
          ></assist-pipeline-detail-stt>
          <assist-pipeline-detail-tts
            .hass=${this.hass}
            .data=${this._data}
            keys="tts_engine,tts_language,tts_voice"
            @value-changed=${this._valueChanged}
          ></assist-pipeline-detail-tts>
          ${this._params.hideWakeWord?s.s6:s.qy`<assist-pipeline-detail-wakeword
                .hass=${this.hass}
                .data=${this._data}
                keys="wake_word_entity,wake_word_id"
                @value-changed=${this._valueChanged}
              ></assist-pipeline-detail-wakeword>`}
        </div>
        <ha-button
          slot="primaryAction"
          @click=${this._updatePipeline}
          .disabled=${this._submitting}
          dialogInitialFocus
        >
          ${this._params.pipeline?.id?this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.update_assistant_action"):this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_action")}
        </ha-button>
      </ha-dialog>
    `}},{kind:"method",key:"_valueChanged",value:function(e){this._error=void 0;const t={};e.currentTarget.getAttribute("keys").split(",").forEach((i=>{t[i]=e.detail.value[i]})),this._data={...this._data,...t}}},{kind:"method",key:"_updatePipeline",value:async function(){this._submitting=!0;try{const e=this._data,t={name:e.name,language:e.language,conversation_engine:e.conversation_engine,conversation_language:e.conversation_language??null,stt_engine:e.stt_engine??null,stt_language:e.stt_language??null,tts_engine:e.tts_engine??null,tts_language:e.tts_language??null,tts_voice:e.tts_voice??null,wake_word_entity:e.wake_word_entity??null,wake_word_id:e.wake_word_id??null};this._params.pipeline?.id?await this._params.updatePipeline(t):this._params.createPipeline?await this._params.createPipeline(t):console.error("No createPipeline function provided"),this.closeDialog()}catch(e){this._error=e?.message||"Unknown error"}finally{this._submitting=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[d.nA,s.AH`
        .content > *:not(:last-child) {
          margin-bottom: 16px;
          display: block;
        }
        ha-alert {
          margin-bottom: 16px;
          display: block;
        }
        a {
          text-decoration: none;
        }
      `]}}]}}),s.WF)}};
//# sourceMappingURL=YU-gkmCZ.js.map