"use strict";(self.webpackChunksandbox_fusion=self.webpackChunksandbox_fusion||[]).push([[6061],{74454:(e,n,t)=>{t.r(n),t.d(n,{default:()=>u});t(96540);var i=t(34164),a=t(44084),l=t(17559),r=t(13472),s=t(74848);function c(e){let{className:n}=e;return(0,s.jsx)(r.A,{type:"caution",title:(0,s.jsx)(a.Yh,{}),className:(0,i.A)(n,l.G.common.draftBanner),children:(0,s.jsx)(a.TT,{})})}function o(e){let{className:n}=e;return(0,s.jsx)(r.A,{type:"caution",title:(0,s.jsx)(a.Rc,{}),className:(0,i.A)(n,l.G.common.unlistedBanner),children:(0,s.jsx)(a.Uh,{})})}function d(e){return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(a.AE,{}),(0,s.jsx)(o,{...e})]})}function u(e){let{metadata:n}=e;const{unlisted:t,frontMatter:i}=n;return(0,s.jsxs)(s.Fragment,{children:[(t||i.unlisted)&&(0,s.jsx)(d,{}),i.draft&&(0,s.jsx)(c,{})]})}},67973:(e,n,t)=>{t.r(n),t.d(n,{default:()=>f});t(96540);var i=t(34164),a=t(45500),l=t(17559),r=t(653),s=t(72857),c=t(67763),o=t(74454),d=t(4336);const u={mdxPageWrapper:"mdxPageWrapper_j9I6"};var m=t(74848);function f(e){const{content:n}=e,{metadata:t,assets:f}=n,{title:h,editUrl:x,description:v,frontMatter:g,lastUpdatedBy:p,lastUpdatedAt:j}=t,{keywords:b,wrapperClassName:L,hide_table_of_contents:A}=g,N=f.image??g.image,C=!!(x||j||p);return(0,m.jsx)(a.e3,{className:(0,i.A)(L??l.G.wrapper.mdxPages,l.G.page.mdxPage),children:(0,m.jsxs)(r.A,{children:[(0,m.jsx)(a.be,{title:h,description:v,keywords:b,image:N}),(0,m.jsx)("main",{className:"container container--fluid margin-vert--lg",children:(0,m.jsxs)("div",{className:(0,i.A)("row",u.mdxPageWrapper),children:[(0,m.jsxs)("div",{className:(0,i.A)("col",!A&&"col--8"),children:[(0,m.jsx)(o.default,{metadata:t}),(0,m.jsx)("article",{children:(0,m.jsx)(s.A,{children:(0,m.jsx)(n,{})})}),C&&(0,m.jsx)(d.A,{className:(0,i.A)("margin-top--sm",l.G.pages.pageFooterEditMetaRow),editUrl:x,lastUpdatedAt:j,lastUpdatedBy:p})]}),!A&&n.toc.length>0&&(0,m.jsx)("div",{className:"col col--2",children:(0,m.jsx)(c.A,{toc:n.toc,minHeadingLevel:g.toc_min_heading_level,maxHeadingLevel:g.toc_max_heading_level})})]})})]})})}},67763:(e,n,t)=>{t.d(n,{A:()=>o});t(96540);var i=t(34164),a=t(19114);const l={tableOfContents:"tableOfContents_bqdL",docItemContainer:"docItemContainer_F8PC"};var r=t(74848);const s="table-of-contents__link toc-highlight",c="table-of-contents__link--active";function o(e){let{className:n,...t}=e;return(0,r.jsx)("div",{className:(0,i.A)(l.tableOfContents,"thin-scrollbar",n),children:(0,r.jsx)(a.A,{...t,linkClassName:s,linkActiveClassName:c})})}},19114:(e,n,t)=>{t.d(n,{A:()=>u});var i=t(96540),a=t(6342),l=t(37243),r=t(20366),s=t(28774),c=t(74848);function o(e){let{toc:n,className:t,linkClassName:i,isChild:a}=e;return n.length?(0,c.jsx)("ul",{className:a?void 0:t,children:n.map((e=>(0,c.jsxs)("li",{children:[(0,c.jsx)(s.default,{to:`#${e.id}`,className:i??void 0,dangerouslySetInnerHTML:{__html:e.value}}),(0,c.jsx)(o,{isChild:!0,toc:e.children,className:t,linkClassName:i})]},e.id)))}):null}const d=i.memo(o);function u(e){let{toc:n,className:t="table-of-contents table-of-contents__left-border",linkClassName:s="table-of-contents__link",linkActiveClassName:o,minHeadingLevel:u,maxHeadingLevel:m,...f}=e;const h=(0,a.p)(),x=u??h.tableOfContents.minHeadingLevel,v=m??h.tableOfContents.maxHeadingLevel,g=(0,l.h)({toc:n,minHeadingLevel:x,maxHeadingLevel:v}),p=(0,i.useMemo)((()=>{if(s&&o)return{linkClassName:s,linkActiveClassName:o,minHeadingLevel:x,maxHeadingLevel:v}}),[s,o,x,v]);return(0,r.i)(p),(0,c.jsx)(d,{toc:g,className:t,linkClassName:s,...f})}},20366:(e,n,t)=>{t.d(n,{i:()=>c});var i=t(96540),a=t(6342);function l(e){const n=e.getBoundingClientRect();return n.top===n.bottom?l(e.parentNode):n}function r(e,n){let{anchorTopOffset:t}=n;const i=e.find((e=>l(e).top>=t));if(i){return function(e){return e.top>0&&e.bottom<window.innerHeight/2}(l(i))?i:e[e.indexOf(i)-1]??null}return e[e.length-1]??null}function s(){const e=(0,i.useRef)(0),{navbar:{hideOnScroll:n}}=(0,a.p)();return(0,i.useEffect)((()=>{e.current=n?0:document.querySelector(".navbar").clientHeight}),[n]),e}function c(e){const n=(0,i.useRef)(void 0),t=s();(0,i.useEffect)((()=>{if(!e)return()=>{};const{linkClassName:i,linkActiveClassName:a,minHeadingLevel:l,maxHeadingLevel:s}=e;function c(){const e=function(e){return Array.from(document.getElementsByClassName(e))}(i),c=function(e){let{minHeadingLevel:n,maxHeadingLevel:t}=e;const i=[];for(let a=n;a<=t;a+=1)i.push(`h${a}.anchor`);return Array.from(document.querySelectorAll(i.join()))}({minHeadingLevel:l,maxHeadingLevel:s}),o=r(c,{anchorTopOffset:t.current}),d=e.find((e=>o&&o.id===function(e){return decodeURIComponent(e.href.substring(e.href.indexOf("#")+1))}(e)));e.forEach((e=>{!function(e,t){t?(n.current&&n.current!==e&&n.current.classList.remove(a),e.classList.add(a),n.current=e):e.classList.remove(a)}(e,e===d)}))}return document.addEventListener("scroll",c),document.addEventListener("resize",c),c(),()=>{document.removeEventListener("scroll",c),document.removeEventListener("resize",c)}}),[e,t])}},44084:(e,n,t)=>{t.d(n,{AE:()=>c,Rc:()=>r,TT:()=>d,Uh:()=>s,Yh:()=>o});t(96540);var i=t(21312),a=t(5260),l=t(74848);function r(){return(0,l.jsx)(i.default,{id:"theme.contentVisibility.unlistedBanner.title",description:"The unlisted content banner title",children:"Unlisted page"})}function s(){return(0,l.jsx)(i.default,{id:"theme.contentVisibility.unlistedBanner.message",description:"The unlisted content banner message",children:"This page is unlisted. Search engines will not index it, and only users having a direct link can access it."})}function c(){return(0,l.jsx)(a.A,{children:(0,l.jsx)("meta",{name:"robots",content:"noindex, nofollow"})})}function o(){return(0,l.jsx)(i.default,{id:"theme.contentVisibility.draftBanner.title",description:"The draft content banner title",children:"Draft page"})}function d(){return(0,l.jsx)(i.default,{id:"theme.contentVisibility.draftBanner.message",description:"The draft content banner message",children:"This page is a draft. It will only be visible in dev and be excluded from the production build."})}},36266:(e,n,t)=>{t.d(n,{i:()=>a});var i=t(44586);function a(e){void 0===e&&(e={});const{i18n:{currentLocale:n}}=(0,i.default)(),t=function(){const{i18n:{currentLocale:e,localeConfigs:n}}=(0,i.default)();return n[e].calendar}();return new Intl.DateTimeFormat(n,{calendar:t,...e})}},88473:(e,n,t)=>{t.d(n,{c:()=>l});var i=t(96540),a=t(74848);function l(e){const{mdxAdmonitionTitle:n,rest:t}=function(e){const n=i.Children.toArray(e),t=n.find((e=>i.isValidElement(e)&&"mdxAdmonitionTitle"===e.type)),l=n.filter((e=>e!==t)),r=t?.props.children;return{mdxAdmonitionTitle:r,rest:l.length>0?(0,a.jsx)(a.Fragment,{children:l}):null}}(e.children),l=e.title??n;return{...e,...l&&{title:l},children:t}}},37243:(e,n,t)=>{t.d(n,{h:()=>s,v:()=>l});var i=t(96540);function a(e){const n=e.map((e=>({...e,parentIndex:-1,children:[]}))),t=Array(7).fill(-1);n.forEach(((e,n)=>{const i=t.slice(2,e.level);e.parentIndex=Math.max(...i),t[e.level]=n}));const i=[];return n.forEach((e=>{const{parentIndex:t,...a}=e;t>=0?n[t].children.push(a):i.push(a)})),i}function l(e){return(0,i.useMemo)((()=>a(e)),[e])}function r(e){let{toc:n,minHeadingLevel:t,maxHeadingLevel:i}=e;return n.flatMap((e=>{const n=r({toc:e.children,minHeadingLevel:t,maxHeadingLevel:i});return function(e){return e.level>=t&&e.level<=i}(e)?[{...e,children:n}]:n}))}function s(e){let{toc:n,minHeadingLevel:t,maxHeadingLevel:l}=e;return(0,i.useMemo)((()=>r({toc:a(n),minHeadingLevel:t,maxHeadingLevel:l})),[n,t,l])}}}]);