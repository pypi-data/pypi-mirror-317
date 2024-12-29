export const id=2536;export const ids=[2536];export const modules={65206:(e,t,a)=>{var i=a(85461),o=a(69534),l=a(92518),r=a(98597),n=a(196),d=a(69760),s=a(79278),c=a(12506),h=a(45081),u=a(97626),b=a(33167),p=a(66412),m=a(11355);const f=(e,t)=>{const a={};for(const i of e){const e=t(i);e in a?a[e].push(i):a[e]=[i]}return a};var v=a(43799),_=a(31646),k=(a(19887),a(29222),a(82927),a(84292));let g;const y=()=>(g||(g=(0,k.LV)(new Worker(new URL(a.p+a.u(2321),a.b),{type:"module"}))),g);var x=a(45787);const w="zzzzz_undefined";(0,i.A)([(0,n.EM)("ha-data-table")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"columns",value(){return{}}},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"data",value(){return[]}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"selectable",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"clickable",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"hasFab",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"appendRow",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"auto-height"})],key:"autoHeight",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:String})],key:"id",value(){return"id"}},{kind:"field",decorators:[(0,n.MZ)({type:String})],key:"noDataText",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:String})],key:"searchLabel",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:String})],key:"filter",value(){return""}},{kind:"field",decorators:[(0,n.MZ)()],key:"groupColumn",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"groupOrder",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"sortColumn",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"sortDirection",value(){return null}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"initialCollapsedGroups",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hiddenColumns",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"columnOrder",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_filterable",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_filter",value(){return""}},{kind:"field",decorators:[(0,n.wk)()],key:"_filteredData",value(){return[]}},{kind:"field",decorators:[(0,n.wk)()],key:"_headerHeight",value(){return 0}},{kind:"field",decorators:[(0,n.P)("slot[name='header']")],key:"_header",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_collapsedGroups",value(){return[]}},{kind:"field",key:"_checkableRowsCount",value:void 0},{kind:"field",key:"_checkedRows",value(){return[]}},{kind:"field",key:"_sortColumns",value(){return{}}},{kind:"field",key:"_curRequest",value(){return 0}},{kind:"field",key:"_lastUpdate",value(){return 0}},{kind:"field",decorators:[(0,u.a)(".scroller")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_debounceSearch",value(){return(0,m.s)((e=>{this._filter=e}),100,!1)}},{kind:"method",key:"clearSelection",value:function(){this._checkedRows=[],this._checkedRowsChanged()}},{kind:"method",key:"selectAll",value:function(){this._checkedRows=this._filteredData.filter((e=>!1!==e.selectable)).map((e=>e[this.id])),this._checkedRowsChanged()}},{kind:"method",key:"select",value:function(e,t){t&&(this._checkedRows=[]),e.forEach((e=>{const t=this._filteredData.find((t=>t[this.id]===e));!1===t?.selectable||this._checkedRows.includes(e)||this._checkedRows.push(e)})),this._checkedRowsChanged()}},{kind:"method",key:"unselect",value:function(e){e.forEach((e=>{const t=this._checkedRows.indexOf(e);t>-1&&this._checkedRows.splice(t,1)})),this._checkedRowsChanged()}},{kind:"method",key:"connectedCallback",value:function(){(0,o.A)(a,"connectedCallback",this,3)([]),this._filteredData.length&&(this._filteredData=[...this._filteredData])}},{kind:"method",key:"firstUpdated",value:function(){this.updateComplete.then((()=>this._calcTableHeight()))}},{kind:"method",key:"updated",value:function(){const e=this.renderRoot.querySelector(".mdc-data-table__header-row");e&&(e.scrollWidth>e.clientWidth?this.style.setProperty("--table-row-width",`${e.scrollWidth}px`):this.style.removeProperty("--table-row-width"))}},{kind:"method",key:"willUpdate",value:function(e){if((0,o.A)(a,"willUpdate",this,3)([e]),this.hasUpdated||(0,_.i)(),e.has("columns")){if(this._filterable=Object.values(this.columns).some((e=>e.filterable)),!this.sortColumn)for(const t in this.columns)if(this.columns[t].direction){this.sortDirection=this.columns[t].direction,this.sortColumn=t,(0,b.r)(this,"sorting-changed",{column:t,direction:this.sortDirection});break}const e=(0,l.A)(this.columns);Object.values(e).forEach((e=>{delete e.title,delete e.template,delete e.extraTemplate})),this._sortColumns=e}e.has("filter")&&this._debounceSearch(this.filter),e.has("data")&&(this._checkableRowsCount=this.data.filter((e=>!1!==e.selectable)).length),!this.hasUpdated&&this.initialCollapsedGroups?(this._collapsedGroups=this.initialCollapsedGroups,(0,b.r)(this,"collapsed-changed",{value:this._collapsedGroups})):e.has("groupColumn")&&(this._collapsedGroups=[],(0,b.r)(this,"collapsed-changed",{value:this._collapsedGroups})),(e.has("data")||e.has("columns")||e.has("_filter")||e.has("sortColumn")||e.has("sortDirection"))&&this._sortFilterData(),(e.has("selectable")||e.has("hiddenColumns"))&&(this._filteredData=[...this._filteredData])}},{kind:"field",key:"_sortedColumns",value(){return(0,h.A)(((e,t)=>t&&t.length?Object.keys(e).sort(((e,a)=>{const i=t.indexOf(e),o=t.indexOf(a);if(i!==o){if(-1===i)return 1;if(-1===o)return-1}return i-o})).reduce(((t,a)=>(t[a]=e[a],t)),{}):e))}},{kind:"method",key:"render",value:function(){const e=this.localizeFunc||this.hass.localize,t=this._sortedColumns(this.columns,this.columnOrder);return r.qy`
      <div class="mdc-data-table">
        <slot name="header" @slotchange=${this._calcTableHeight}>
          ${this._filterable?r.qy`
                <div class="table-header">
                  <search-input
                    .hass=${this.hass}
                    @value-changed=${this._handleSearchChange}
                    .label=${this.searchLabel}
                    .noLabelFloat=${this.noLabelFloat}
                  ></search-input>
                </div>
              `:""}
        </slot>
        <div
          class="mdc-data-table__table ${(0,d.H)({"auto-height":this.autoHeight})}"
          role="table"
          aria-rowcount=${this._filteredData.length+1}
          style=${(0,c.W)({height:this.autoHeight?53*(this._filteredData.length||1)+53+"px":`calc(100% - ${this._headerHeight}px)`})}
        >
          <div
            class="mdc-data-table__header-row"
            role="row"
            aria-rowindex="1"
            @scroll=${this._scrollContent}
          >
            <slot name="header-row">
              ${this.selectable?r.qy`
                    <div
                      class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                      role="columnheader"
                    >
                      <ha-checkbox
                        class="mdc-data-table__row-checkbox"
                        @change=${this._handleHeaderRowCheckboxClick}
                        .indeterminate=${this._checkedRows.length&&this._checkedRows.length!==this._checkableRowsCount}
                        .checked=${this._checkedRows.length&&this._checkedRows.length===this._checkableRowsCount}
                      >
                      </ha-checkbox>
                    </div>
                  `:""}
              ${Object.entries(t).map((([e,t])=>{if(t.hidden||(this.columnOrder&&this.columnOrder.includes(e)?this.hiddenColumns?.includes(e)??t.defaultHidden:t.defaultHidden))return r.s6;const a=e===this.sortColumn,i={"mdc-data-table__header-cell--numeric":"numeric"===t.type,"mdc-data-table__header-cell--icon":"icon"===t.type,"mdc-data-table__header-cell--icon-button":"icon-button"===t.type,"mdc-data-table__header-cell--overflow-menu":"overflow-menu"===t.type,"mdc-data-table__header-cell--overflow":"overflow"===t.type,sortable:Boolean(t.sortable),"not-sorted":Boolean(t.sortable&&!a)};return r.qy`
                  <div
                    aria-label=${(0,s.J)(t.label)}
                    class="mdc-data-table__header-cell ${(0,d.H)(i)}"
                    style=${(0,c.W)({minWidth:t.minWidth,maxWidth:t.maxWidth,flex:t.flex||1})}
                    role="columnheader"
                    aria-sort=${(0,s.J)(a?"desc"===this.sortDirection?"descending":"ascending":void 0)}
                    @click=${this._handleHeaderClick}
                    .columnId=${e}
                  >
                    ${t.sortable?r.qy`
                          <ha-svg-icon
                            .path=${a&&"desc"===this.sortDirection?"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z":"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"}
                          ></ha-svg-icon>
                        `:""}
                    <span>${t.title}</span>
                  </div>
                `}))}
            </slot>
          </div>
          ${this._filteredData.length?r.qy`
                <lit-virtualizer
                  scroller
                  class="mdc-data-table__content scroller ha-scrollbar"
                  @scroll=${this._saveScrollPos}
                  .items=${this._groupData(this._filteredData,e,this.appendRow,this.hasFab,this.groupColumn,this.groupOrder,this._collapsedGroups)}
                  .keyFunction=${this._keyFunction}
                  .renderItem=${(e,a)=>this._renderRow(t,this.narrow,e,a)}
                ></lit-virtualizer>
              `:r.qy`
                <div class="mdc-data-table__content">
                  <div class="mdc-data-table__row" role="row">
                    <div class="mdc-data-table__cell grows center" role="cell">
                      ${this.noDataText||e("ui.components.data-table.no-data")}
                    </div>
                  </div>
                </div>
              `}
        </div>
      </div>
    `}},{kind:"field",key:"_keyFunction",value(){return e=>e?.[this.id]||e}},{kind:"field",key:"_renderRow",value(){return(e,t,a,i)=>a?a.append?r.qy`<div class="mdc-data-table__row">${a.content}</div>`:a.empty?r.qy`<div class="mdc-data-table__row"></div>`:r.qy`
      <div
        aria-rowindex=${i+2}
        role="row"
        .rowId=${a[this.id]}
        @click=${this._handleRowClick}
        class="mdc-data-table__row ${(0,d.H)({"mdc-data-table__row--selected":this._checkedRows.includes(String(a[this.id])),clickable:this.clickable})}"
        aria-selected=${(0,s.J)(!!this._checkedRows.includes(String(a[this.id]))||void 0)}
        .selectable=${!1!==a.selectable}
      >
        ${this.selectable?r.qy`
              <div
                class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                role="cell"
              >
                <ha-checkbox
                  class="mdc-data-table__row-checkbox"
                  @change=${this._handleRowCheckboxClick}
                  .rowId=${a[this.id]}
                  .disabled=${!1===a.selectable}
                  .checked=${this._checkedRows.includes(String(a[this.id]))}
                >
                </ha-checkbox>
              </div>
            `:""}
        ${Object.entries(e).map((([i,o])=>t&&!o.main&&!o.showNarrow||o.hidden||(this.columnOrder&&this.columnOrder.includes(i)?this.hiddenColumns?.includes(i)??o.defaultHidden:o.defaultHidden)?r.s6:r.qy`
            <div
              @mouseover=${this._setTitle}
              @focus=${this._setTitle}
              role=${o.main?"rowheader":"cell"}
              class="mdc-data-table__cell ${(0,d.H)({"mdc-data-table__cell--flex":"flex"===o.type,"mdc-data-table__cell--numeric":"numeric"===o.type,"mdc-data-table__cell--icon":"icon"===o.type,"mdc-data-table__cell--icon-button":"icon-button"===o.type,"mdc-data-table__cell--overflow-menu":"overflow-menu"===o.type,"mdc-data-table__cell--overflow":"overflow"===o.type,forceLTR:Boolean(o.forceLTR)})}"
              style=${(0,c.W)({minWidth:o.minWidth,maxWidth:o.maxWidth,flex:o.flex||1})}
            >
              ${o.template?o.template(a):t&&o.main?r.qy`<div class="primary">${a[i]}</div>
                      <div class="secondary">
                        ${Object.entries(e).filter((([e,t])=>!(t.hidden||t.main||t.showNarrow||(this.columnOrder&&this.columnOrder.includes(e)?this.hiddenColumns?.includes(e)??t.defaultHidden:t.defaultHidden)))).map((([e,t],i)=>r.qy`${0!==i?" ⸱ ":r.s6}${t.template?t.template(a):a[e]}`))}
                      </div>
                      ${o.extraTemplate?o.extraTemplate(a):r.s6}`:r.qy`${a[i]}${o.extraTemplate?o.extraTemplate(a):r.s6}`}
            </div>
          `))}
      </div>
    `:r.s6}},{kind:"method",key:"_sortFilterData",value:async function(){const e=(new Date).getTime(),t=e-this._lastUpdate,a=e-this._curRequest;this._curRequest=e;const i=!this._lastUpdate||t>500&&a<500;let o=this.data;if(this._filter&&(o=await this._memFilterData(this.data,this._sortColumns,this._filter.trim())),!i&&this._curRequest!==e)return;const l=this.sortColumn?((e,t,a,i,o)=>y().sortData(e,t,a,i,o))(o,this._sortColumns[this.sortColumn],this.sortDirection,this.sortColumn,this.hass.locale.language):o,[r]=await Promise.all([l,x.E]),n=(new Date).getTime()-e;n<100&&await new Promise((e=>{setTimeout(e,100-n)})),(i||this._curRequest===e)&&(this._lastUpdate=e,this._filteredData=r)}},{kind:"field",key:"_groupData",value(){return(0,h.A)(((e,t,a,i,o,l,n)=>{if(a||i||o){let d=[...e];if(o){const e=f(d,(e=>e[o]));e.undefined&&(e[w]=e.undefined,delete e.undefined);const a=Object.keys(e).sort(((e,t)=>{const a=l?.indexOf(e)??-1,i=l?.indexOf(t)??-1;return a!==i?-1===a?1:-1===i?-1:a-i:(0,p.x)(["","-","—"].includes(e)?"zzz":e,["","-","—"].includes(t)?"zzz":t,this.hass.locale.language)})).reduce(((t,a)=>(t[a]=e[a],t)),{}),i=[];Object.entries(a).forEach((([e,a])=>{i.push({append:!0,content:r.qy`<div
                class="mdc-data-table__cell group-header"
                role="cell"
                .group=${e}
                @click=${this._collapseGroup}
              >
                <ha-icon-button
                  .path=${"M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"}
                  class=${n.includes(e)?"collapsed":""}
                >
                </ha-icon-button>
                ${e===w?t("ui.components.data-table.ungrouped"):e||""}
              </div>`}),n.includes(e)||i.push(...a)})),d=i}return a&&d.push({append:!0,content:a}),i&&d.push({empty:!0}),d}return e}))}},{kind:"field",key:"_memFilterData",value(){return(0,h.A)(((e,t,a)=>((e,t,a)=>y().filterData(e,t,a))(e,t,a)))}},{kind:"method",key:"_handleHeaderClick",value:function(e){const t=e.currentTarget.columnId;this.columns[t].sortable&&(this.sortDirection&&this.sortColumn===t?"asc"===this.sortDirection?this.sortDirection="desc":this.sortDirection=null:this.sortDirection="asc",this.sortColumn=null===this.sortDirection?void 0:t,(0,b.r)(this,"sorting-changed",{column:t,direction:this.sortDirection}))}},{kind:"method",key:"_handleHeaderRowCheckboxClick",value:function(e){e.target.checked?this.selectAll():(this._checkedRows=[],this._checkedRowsChanged())}},{kind:"field",key:"_handleRowCheckboxClick",value(){return e=>{const t=e.currentTarget,a=t.rowId;if(t.checked){if(this._checkedRows.includes(a))return;this._checkedRows=[...this._checkedRows,a]}else this._checkedRows=this._checkedRows.filter((e=>e!==a));this._checkedRowsChanged()}}},{kind:"field",key:"_handleRowClick",value(){return e=>{if(e.composedPath().find((e=>["ha-checkbox","mwc-button","ha-button","ha-icon-button","ha-assist-chip"].includes(e.localName))))return;const t=e.currentTarget.rowId;(0,b.r)(this,"row-click",{id:t},{bubbles:!1})}}},{kind:"method",key:"_setTitle",value:function(e){const t=e.currentTarget;t.scrollWidth>t.offsetWidth&&t.setAttribute("title",t.innerText)}},{kind:"method",key:"_checkedRowsChanged",value:function(){this._filteredData.length&&(this._filteredData=[...this._filteredData]),(0,b.r)(this,"selection-changed",{value:this._checkedRows})}},{kind:"method",key:"_handleSearchChange",value:function(e){this.filter||this._debounceSearch(e.detail.value)}},{kind:"method",key:"_calcTableHeight",value:async function(){this.autoHeight||(await this.updateComplete,this._headerHeight=this._header.clientHeight)}},{kind:"method",decorators:[(0,n.Ls)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop,this.renderRoot.querySelector(".mdc-data-table__header-row").scrollLeft=e.target.scrollLeft}},{kind:"method",decorators:[(0,n.Ls)({passive:!0})],key:"_scrollContent",value:function(e){this.renderRoot.querySelector("lit-virtualizer").scrollLeft=e.target.scrollLeft}},{kind:"field",key:"_collapseGroup",value(){return e=>{const t=e.currentTarget.group;this._collapsedGroups.includes(t)?this._collapsedGroups=this._collapsedGroups.filter((e=>e!==t)):this._collapsedGroups=[...this._collapsedGroups,t],(0,b.r)(this,"collapsed-changed",{value:this._collapsedGroups})}}},{kind:"method",key:"expandAllGroups",value:function(){this._collapsedGroups=[],(0,b.r)(this,"collapsed-changed",{value:this._collapsedGroups})}},{kind:"method",key:"collapseAllGroups",value:function(){if(!this.groupColumn||!this.data.some((e=>e[this.groupColumn])))return;const e=f(this.data,(e=>e[this.groupColumn]));e.undefined&&(e[w]=e.undefined,delete e.undefined),this._collapsedGroups=Object.keys(e),(0,b.r)(this,"collapsed-changed",{value:this._collapsedGroups})}},{kind:"get",static:!0,key:"styles",value:function(){return[v.dp,r.AH`
        /* default mdc styles, colors changed, without checkbox styles */
        :host {
          height: 100%;
        }
        .mdc-data-table__content {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table {
          background-color: var(--data-table-background-color);
          border-radius: 4px;
          border-width: 1px;
          border-style: solid;
          border-color: var(--divider-color);
          display: inline-flex;
          flex-direction: column;
          box-sizing: border-box;
          overflow: hidden;
        }

        .mdc-data-table__row--selected {
          background-color: rgba(var(--rgb-primary-color), 0.04);
        }

        .mdc-data-table__row {
          display: flex;
          height: var(--data-table-row-height, 52px);
          width: var(--table-row-width, 100%);
        }

        .mdc-data-table__row ~ .mdc-data-table__row {
          border-top: 1px solid var(--divider-color);
        }

        .mdc-data-table__row.clickable:not(
            .mdc-data-table__row--selected
          ):hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .mdc-data-table__header-cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__header-row {
          height: 56px;
          display: flex;
          border-bottom: 1px solid var(--divider-color);
          overflow: auto;
        }

        /* Hide scrollbar for Chrome, Safari and Opera */
        .mdc-data-table__header-row::-webkit-scrollbar {
          display: none;
        }

        /* Hide scrollbar for IE, Edge and Firefox */
        .mdc-data-table__header-row {
          -ms-overflow-style: none; /* IE and Edge */
          scrollbar-width: none; /* Firefox */
        }

        .mdc-data-table__cell,
        .mdc-data-table__header-cell {
          padding-right: 16px;
          padding-left: 16px;
          min-width: 150px;
          align-self: center;
          overflow: hidden;
          text-overflow: ellipsis;
          flex-shrink: 0;
          box-sizing: border-box;
        }

        .mdc-data-table__cell.mdc-data-table__cell--flex {
          display: flex;
          overflow: initial;
        }

        .mdc-data-table__cell.mdc-data-table__cell--icon {
          overflow: initial;
        }

        .mdc-data-table__header-cell--checkbox,
        .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 16px;
          /* @noflip */
          padding-right: 0;
          /* @noflip */
          padding-inline-start: 16px;
          /* @noflip */
          padding-inline-end: initial;
          width: 60px;
          min-width: 60px;
        }

        .mdc-data-table__table {
          height: 100%;
          width: 100%;
          border: 0;
          white-space: nowrap;
          position: relative;
        }

        .mdc-data-table__cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
          flex-grow: 0;
          flex-shrink: 0;
        }

        .mdc-data-table__cell a {
          color: inherit;
          text-decoration: none;
        }

        .mdc-data-table__cell--numeric {
          text-align: var(--float-end);
        }

        .mdc-data-table__cell--icon {
          color: var(--secondary-text-color);
          text-align: center;
        }

        .mdc-data-table__header-cell--icon,
        .mdc-data-table__cell--icon {
          min-width: 64px;
          flex: 0 0 64px !important;
        }

        .mdc-data-table__cell--icon img {
          width: 24px;
          height: 24px;
        }

        .mdc-data-table__header-cell.mdc-data-table__header-cell--icon {
          text-align: center;
        }

        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(
            .not-sorted
          ) {
          text-align: var(--float-start);
        }

        .mdc-data-table__cell--icon:first-child img,
        .mdc-data-table__cell--icon:first-child ha-icon,
        .mdc-data-table__cell--icon:first-child ha-svg-icon,
        .mdc-data-table__cell--icon:first-child ha-state-icon,
        .mdc-data-table__cell--icon:first-child ha-domain-icon,
        .mdc-data-table__cell--icon:first-child ha-service-icon {
          margin-left: 8px;
          margin-inline-start: 8px;
          margin-inline-end: initial;
        }

        .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: -8px;
          margin-inline-end: -8px;
          margin-inline-start: initial;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          min-width: 64px;
          flex: 0 0 64px !important;
          padding: 8px;
        }

        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          min-width: 56px;
          width: 56px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--icon-button {
          color: var(--secondary-text-color);
          text-overflow: clip;
        }

        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          width: 64px;
        }

        .mdc-data-table__cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child {
          padding-left: 16px;
          padding-inline-start: 16px;
          padding-inline-end: initial;
        }

        .mdc-data-table__cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          padding-right: 16px;
          padding-inline-end: 16px;
          padding-inline-start: initial;
        }
        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--overflow,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--overflow {
          overflow: initial;
        }
        .mdc-data-table__cell--icon-button a {
          color: var(--secondary-text-color);
        }

        .mdc-data-table__header-cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.375rem;
          font-weight: 500;
          letter-spacing: 0.0071428571em;
          text-decoration: inherit;
          text-transform: inherit;
          text-align: var(--float-start);
        }

        .mdc-data-table__header-cell--numeric {
          text-align: var(--float-end);
        }
        .mdc-data-table__header-cell--numeric.sortable:hover,
        .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: var(--float-start);
        }

        /* custom from here */

        .group-header {
          padding-top: 12px;
          height: var(--data-table-row-height, 52px);
          padding-left: 12px;
          padding-inline-start: 12px;
          padding-inline-end: initial;
          width: 100%;
          font-weight: 500;
          display: flex;
          align-items: center;
          cursor: pointer;
          background-color: var(--primary-background-color);
        }

        .group-header ha-icon-button {
          transition: transform 0.2s ease;
        }

        .group-header ha-icon-button.collapsed {
          transform: rotate(180deg);
        }

        :host {
          display: block;
        }

        .mdc-data-table {
          display: block;
          border-width: var(--data-table-border-width, 1px);
          height: 100%;
        }
        .mdc-data-table__header-cell {
          overflow: hidden;
          position: relative;
        }
        .mdc-data-table__header-cell span {
          position: relative;
          left: 0px;
          inset-inline-start: 0px;
          inset-inline-end: initial;
        }

        .mdc-data-table__header-cell.sortable {
          cursor: pointer;
        }
        .mdc-data-table__header-cell > * {
          transition: var(--float-start) 0.2s ease;
        }
        .mdc-data-table__header-cell ha-svg-icon {
          top: -3px;
          position: absolute;
        }
        .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          left: -20px;
          inset-inline-start: -20px;
          inset-inline-end: initial;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) span,
        .mdc-data-table__header-cell.sortable.not-sorted:hover span {
          left: 24px;
          inset-inline-start: 24px;
          inset-inline-end: initial;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) ha-svg-icon,
        .mdc-data-table__header-cell.sortable:hover.not-sorted ha-svg-icon {
          left: 12px;
          inset-inline-start: 12px;
          inset-inline-end: initial;
        }
        .table-header {
          border-bottom: 1px solid var(--divider-color);
        }
        search-input {
          display: block;
          flex: 1;
          --mdc-text-field-fill-color: var(--sidebar-background-color);
          --mdc-text-field-idle-line-color: transparent;
        }
        slot[name="header"] {
          display: block;
        }
        .center {
          text-align: center;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        .scroller {
          height: calc(100% - 57px);
          overflow: overlay !important;
        }

        .mdc-data-table__table.auto-height .scroller {
          overflow-y: hidden !important;
        }
        .grows {
          flex-grow: 1;
          flex-shrink: 1;
        }
        .forceLTR {
          direction: ltr;
        }
        .clickable {
          cursor: pointer;
        }
        lit-virtualizer {
          contain: size layout !important;
          overscroll-behavior: contain;
        }
      `]}}]}}),r.WF)},82927:(e,t,a)=>{var i=a(85461),o=a(98597),l=a(196),r=(a(96396),a(29222),a(59373),a(33167));(0,i.A)([(0,l.EM)("search-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"filter",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"suffix",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:String})],key:"label",value:void 0},{kind:"method",key:"focus",value:function(){this._input?.focus()}},{kind:"field",decorators:[(0,l.P)("ha-textfield",!0)],key:"_input",value:void 0},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-textfield
        .autofocus=${this.autofocus}
        .label=${this.label||this.hass.localize("ui.common.search")}
        .value=${this.filter||""}
        icon
        .iconTrailing=${this.filter||this.suffix}
        @input=${this._filterInputChanged}
      >
        <slot name="prefix" slot="leadingIcon">
          <ha-svg-icon
            tabindex="-1"
            class="prefix"
            .path=${"M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z"}
          ></ha-svg-icon>
        </slot>
        <div class="trailing" slot="trailingIcon">
          ${this.filter&&o.qy`
            <ha-icon-button
              @click=${this._clearSearch}
              .label=${this.hass.localize("ui.common.clear")}
              .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              class="clear-button"
            ></ha-icon-button>
          `}
          <slot name="suffix"></slot>
        </div>
      </ha-textfield>
    `}},{kind:"method",key:"_filterChanged",value:async function(e){(0,r.r)(this,"value-changed",{value:String(e)})}},{kind:"method",key:"_filterInputChanged",value:async function(e){this._filterChanged(e.target.value)}},{kind:"method",key:"_clearSearch",value:async function(){this._filterChanged("")}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        display: inline-flex;
      }
      ha-svg-icon,
      ha-icon-button {
        color: var(--primary-text-color);
      }
      ha-svg-icon {
        outline: none;
      }
      .clear-button {
        --mdc-icon-size: 20px;
      }
      ha-textfield {
        display: inherit;
      }
      .trailing {
        display: flex;
        align-items: center;
      }
    `}}]}}),o.WF)},7341:(e,t,a)=>{var i=a(85461),o=a(69534),l=a(98597),r=a(196),n=a(69760),d=a(45081),s=a(97626),c=(a(92312),a(32010),a(29222),a(79278)),h=a(22431),u=a(87515);(0,i.A)([(0,r.EM)("ha-ripple")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",key:"attachableTouchController",value(){return new h.i(this,this.onTouchControlChange.bind(this))}},{kind:"method",key:"attach",value:function(e){(0,o.A)(a,"attach",this,3)([e]),this.attachableTouchController.attach(e)}},{kind:"method",key:"detach",value:function(){(0,o.A)(a,"detach",this,3)([]),this.attachableTouchController.detach()}},{kind:"field",key:"_handleTouchEnd",value(){return()=>{this.disabled||(0,o.A)(a,"endPressAnimation",this,3)([])}}},{kind:"method",key:"onTouchControlChange",value:function(e,t){e?.removeEventListener("touchend",this._handleTouchEnd),t?.addEventListener("touchend",this._handleTouchEnd)}},{kind:"field",static:!0,key:"styles",value(){return[...(0,o.A)(a,"styles",this),l.AH`
      :host {
        --md-ripple-hover-opacity: var(--ha-ripple-hover-opacity, 0.08);
        --md-ripple-pressed-opacity: var(--ha-ripple-pressed-opacity, 0.12);
        --md-ripple-hover-color: var(
          --ha-ripple-hover-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );
        --md-ripple-pressed-color: var(
          --ha-ripple-pressed-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );
      }
    `]}}]}}),u.o),(0,i.A)([(0,r.EM)("ha-tab")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"active",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)()],key:"name",value:void 0},{kind:"method",key:"render",value:function(){return l.qy`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${(0,c.J)(this.name)}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?l.qy`<slot name="icon"></slot>`:""}
        <span class="name">${this.name}</span>
        <ha-ripple></ha-ripple>
      </div>
    `}},{kind:"method",key:"_handleKeyDown",value:function(e){"Enter"===e.key&&e.target.click()}},{kind:"get",static:!0,key:"styles",value:function(){return l.AH`
      div {
        padding: 0 32px;
        display: flex;
        flex-direction: column;
        text-align: center;
        box-sizing: border-box;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: var(--header-height);
        cursor: pointer;
        position: relative;
        outline: none;
      }

      .name {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
      }

      :host([active]) {
        color: var(--primary-color);
      }

      :host(:not([narrow])[active]) div {
        border-bottom: 2px solid var(--primary-color);
      }

      :host([narrow]) {
        min-width: 0;
        display: flex;
        justify-content: center;
        overflow: hidden;
      }

      :host([narrow]) div {
        padding: 0 4px;
      }

      div:focus-visible:before {
        position: absolute;
        display: block;
        content: "";
        inset: 0;
        background-color: var(--secondary-text-color);
        opacity: 0.08;
      }
    `}}]}}),l.WF);var b=a(43799),p=a(96041),m=a(32872);const f=(e,t)=>!t.component||(0,p.e)(t.component).some((t=>(0,m.x)(e,t))),v=(e,t)=>!t.not_component||!(0,p.e)(t.not_component).some((t=>(0,m.x)(e,t))),_=e=>e.core,k=(e,t)=>(e=>e.advancedOnly)(t)&&!(e=>e.userData?.showAdvanced)(e);(0,i.A)([(0,r.EM)("hass-tabs-subpage")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"supervisor",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"main-page"})],key:"mainPage",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"pane",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_activeTab",value:void 0},{kind:"field",decorators:[(0,s.a)(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return(0,d.A)(((e,t,a,i,o,r)=>{const n=e.filter((e=>((e,t)=>(_(t)||f(e,t))&&!k(e,t)&&v(e,t))(this.hass,e)));if(n.length<2){if(1===n.length){const e=n[0];return[e.translationKey?r(e.translationKey):e.name]}return[""]}return n.map((e=>l.qy`
          <a href=${e.path}>
            <ha-tab
              .hass=${this.hass}
              .active=${e.path===t?.path}
              .narrow=${this.narrow}
              .name=${e.translationKey?r(e.translationKey):e.name}
            >
              ${e.iconPath?l.qy`<ha-svg-icon
                    slot="icon"
                    .path=${e.iconPath}
                  ></ha-svg-icon>`:""}
            </ha-tab>
          </a>
        `))}))}},{kind:"method",key:"willUpdate",value:function(e){e.has("route")&&(this._activeTab=this.tabs.find((e=>`${this.route.prefix}${this.route.path}`.includes(e.path)))),(0,o.A)(a,"willUpdate",this,3)([e])}},{kind:"method",key:"render",value:function(){const e=this._getTabs(this.tabs,this._activeTab,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),t=e.length>1;return l.qy`
      <div class="toolbar">
        <slot name="toolbar">
          <div class="toolbar-content">
            ${this.mainPage||!this.backPath&&history.state?.root?l.qy`
                  <ha-menu-button
                    .hassio=${this.supervisor}
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                `:this.backPath?l.qy`
                    <a href=${this.backPath}>
                      <ha-icon-button-arrow-prev
                        .hass=${this.hass}
                      ></ha-icon-button-arrow-prev>
                    </a>
                  `:l.qy`
                    <ha-icon-button-arrow-prev
                      .hass=${this.hass}
                      @click=${this._backTapped}
                    ></ha-icon-button-arrow-prev>
                  `}
            ${this.narrow||!t?l.qy`<div class="main-title">
                  <slot name="header">${t?"":e[0]}</slot>
                </div>`:""}
            ${t&&!this.narrow?l.qy`<div id="tabbar">${e}</div>`:""}
            <div id="toolbar-icon">
              <slot name="toolbar-icon"></slot>
            </div>
          </div>
        </slot>
        ${t&&this.narrow?l.qy`<div id="tabbar" class="bottom-bar">${e}</div>`:""}
      </div>
      <div class="container">
        ${this.pane?l.qy`<div class="pane">
              <div class="shadow-container"></div>
              <div class="ha-scrollbar">
                <slot name="pane"></slot>
              </div>
            </div>`:l.s6}
        <div
          class="content ha-scrollbar ${(0,n.H)({tabs:t})}"
          @scroll=${this._saveScrollPos}
        >
          <slot></slot>
        </div>
      </div>
      <div id="fab" class=${(0,n.H)({tabs:t})}>
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[(0,r.Ls)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[b.dp,l.AH`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }

        :host([narrow]) {
          width: 100%;
          position: fixed;
        }

        .container {
          display: flex;
          height: calc(100% - var(--header-height));
        }

        :host([narrow]) .container {
          height: 100%;
        }

        ha-menu-button {
          margin-right: 24px;
          margin-inline-end: 24px;
          margin-inline-start: initial;
        }

        .toolbar {
          font-size: 20px;
          height: var(--header-height);
          background-color: var(--sidebar-background-color);
          font-weight: 400;
          border-bottom: 1px solid var(--divider-color);
          box-sizing: border-box;
        }
        .toolbar-content {
          padding: 8px 12px;
          display: flex;
          align-items: center;
          height: 100%;
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar-content {
            padding: 4px;
          }
        }
        .toolbar a {
          color: var(--sidebar-text-color);
          text-decoration: none;
        }
        .bottom-bar a {
          width: 25%;
        }

        #tabbar {
          display: flex;
          font-size: 14px;
          overflow: hidden;
        }

        #tabbar > a {
          overflow: hidden;
          max-width: 45%;
        }

        #tabbar.bottom-bar {
          position: absolute;
          bottom: 0;
          left: 0;
          padding: 0 16px;
          box-sizing: border-box;
          background-color: var(--sidebar-background-color);
          border-top: 1px solid var(--divider-color);
          justify-content: space-around;
          z-index: 2;
          font-size: 12px;
          width: 100%;
          padding-bottom: env(safe-area-inset-bottom);
        }

        #tabbar:not(.bottom-bar) {
          flex: 1;
          justify-content: center;
        }

        :host(:not([narrow])) #toolbar-icon {
          min-width: 40px;
        }

        ha-menu-button,
        ha-icon-button-arrow-prev,
        ::slotted([slot="toolbar-icon"]) {
          display: flex;
          flex-shrink: 0;
          pointer-events: auto;
          color: var(--sidebar-icon-color);
        }

        .main-title {
          flex: 1;
          max-height: var(--header-height);
          line-height: 20px;
          color: var(--sidebar-text-color);
          margin: var(--main-title-margin, var(--margin-title));
        }

        .content {
          position: relative;
          width: calc(
            100% - env(safe-area-inset-left) - env(safe-area-inset-right)
          );
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
          margin-inline-start: env(safe-area-inset-left);
          margin-inline-end: env(safe-area-inset-right);
          overflow: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([narrow]) .content.tabs {
          height: calc(100% - 2 * var(--header-height));
          height: calc(
            100% - 2 * var(--header-height) - env(safe-area-inset-bottom)
          );
        }

        #fab {
          position: fixed;
          right: calc(16px + env(safe-area-inset-right));
          inset-inline-end: calc(16px + env(safe-area-inset-right));
          inset-inline-start: initial;
          bottom: calc(16px + env(safe-area-inset-bottom));
          z-index: 1;
          display: flex;
          flex-wrap: wrap;
          justify-content: flex-end;
          gap: 8px;
        }
        :host([narrow]) #fab.tabs {
          bottom: calc(84px + env(safe-area-inset-bottom));
        }
        #fab[is-wide] {
          bottom: 24px;
          right: 24px;
          inset-inline-end: 24px;
          inset-inline-start: initial;
        }

        .pane {
          border-right: 1px solid var(--divider-color);
          border-inline-end: 1px solid var(--divider-color);
          border-inline-start: initial;
          box-sizing: border-box;
          display: flex;
          flex: 0 0 var(--sidepane-width, 250px);
          width: var(--sidepane-width, 250px);
          flex-direction: column;
          position: relative;
        }
        .pane .ha-scrollbar {
          flex: 1;
        }
      `]}}]}}),l.WF)},31646:(e,t,a)=>{a.d(t,{i:()=>i});const i=async()=>{await a.e(3331).then(a.bind(a,83331))}}};
//# sourceMappingURL=XO9ulkAd.js.map