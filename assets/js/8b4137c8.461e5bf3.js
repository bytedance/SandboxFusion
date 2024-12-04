"use strict";(self.webpackChunksandbox_fusion=self.webpackChunksandbox_fusion||[]).push([[7291],{62327:(e,t,s)=>{s.r(t),s.d(t,{assets:()=>l,contentTitle:()=>i,default:()=>h,frontMatter:()=>a,metadata:()=>c,toc:()=>d});var n=s(74848),o=s(28453),r=s(3514);const a={},i="Using Datasets",c={id:"docs/how-to/use-dataset/index",title:"Using Datasets",description:"This is an introduction to how to evaluate models on specific datasets.",source:"@site/docs/docs/how-to/use-dataset/index.md",sourceDirName:"docs/how-to/use-dataset",slug:"/docs/how-to/use-dataset/",permalink:"/SandboxFusion/docs/docs/how-to/use-dataset/",draft:!1,unlisted:!1,editUrl:"https://github.com/bytedance/SandboxFusion/tree/main/docs/docs/docs/how-to/use-dataset/index.md",tags:[],version:"current",frontMatter:{},sidebar:"docSidebar",previous:{title:"Jupyter Mode",permalink:"/SandboxFusion/docs/docs/how-to/run-code/jupyter-mode"},next:{title:"FullStack Bench",permalink:"/SandboxFusion/docs/docs/how-to/use-dataset/fullstack-bench"}},l={},d=[];function u(e){const t={a:"a",h1:"h1",header:"header",p:"p",...(0,o.R)(),...e.components};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(t.header,{children:(0,n.jsx)(t.h1,{id:"using-datasets",children:"Using Datasets"})}),"\n",(0,n.jsx)(t.p,{children:"This is an introduction to how to evaluate models on specific datasets."}),"\n",(0,n.jsxs)(t.p,{children:["Please refer to ",(0,n.jsx)(t.a,{href:"/docs/category/dataset-detail",children:"Dataset Details"})," to understand the concept of datasets."]}),"\n",(0,n.jsx)(t.p,{children:"We provide one implementation that is as correct as possible, but we do not guarantee that the logics of the dataset are exactly the same as the original."}),"\n",(0,n.jsx)(r.A,{})]})}function h(e={}){const{wrapper:t}={...(0,o.R)(),...e.components};return t?(0,n.jsx)(t,{...e,children:(0,n.jsx)(u,{...e})}):u(e)}},3514:(e,t,s)=>{s.d(t,{A:()=>j});s(96540);var n=s(34164),o=s(26972),r=s(28774),a=s(53465),i=s(16654),c=s(21312),l=s(51107);const d={cardContainer:"cardContainer_fWXF",cardTitle:"cardTitle_rnsV",cardDescription:"cardDescription_PWke"};var u=s(74848);function h(e){let{href:t,children:s}=e;return(0,u.jsx)(r.default,{href:t,className:(0,n.A)("card padding--lg",d.cardContainer),children:s})}function m(e){let{href:t,icon:s,title:o,description:r}=e;return(0,u.jsxs)(h,{href:t,children:[(0,u.jsxs)(l.default,{as:"h2",className:(0,n.A)("text--truncate",d.cardTitle),title:o,children:[s," ",o]}),r&&(0,u.jsx)("p",{className:(0,n.A)("text--truncate",d.cardDescription),title:r,children:r})]})}function f(e){let{item:t}=e;const s=(0,o.Nr)(t),n=function(){const{selectMessage:e}=(0,a.W)();return t=>e(t,(0,c.translate)({message:"1 item|{count} items",id:"theme.docs.DocCard.categoryDescription.plurals",description:"The default description for a category card in the generated index about how many items this category includes"},{count:t}))}();return s?(0,u.jsx)(m,{href:s,icon:"\ud83d\uddc3\ufe0f",title:t.label,description:t.description??n(t.items.length)}):null}function p(e){let{item:t}=e;const s=(0,i.A)(t.href)?"\ud83d\udcc4\ufe0f":"\ud83d\udd17",n=(0,o.cC)(t.docId??void 0);return(0,u.jsx)(m,{href:t.href,icon:s,title:t.label,description:t.description??n?.description})}function x(e){let{item:t}=e;switch(t.type){case"link":return(0,u.jsx)(p,{item:t});case"category":return(0,u.jsx)(f,{item:t});default:throw new Error(`unknown item type ${JSON.stringify(t)}`)}}function g(e){let{className:t}=e;const s=(0,o.$S)();return(0,u.jsx)(j,{items:s.items,className:t})}function j(e){const{items:t,className:s}=e;if(!t)return(0,u.jsx)(g,{...e});const r=(0,o.d1)(t);return(0,u.jsx)("section",{className:(0,n.A)("row",s),children:r.map(((e,t)=>(0,u.jsx)("article",{className:"col col--6 margin-bottom--lg",children:(0,u.jsx)(x,{item:e})},t)))})}},53465:(e,t,s)=>{s.d(t,{W:()=>d});var n=s(96540),o=s(44586),r=s(96763);const a=["zero","one","two","few","many","other"];function i(e){return a.filter((t=>e.includes(t)))}const c={locale:"en",pluralForms:i(["one","other"]),select:e=>1===e?"one":"other"};function l(){const{i18n:{currentLocale:e}}=(0,o.default)();return(0,n.useMemo)((()=>{try{return function(e){const t=new Intl.PluralRules(e);return{locale:e,pluralForms:i(t.resolvedOptions().pluralCategories),select:e=>t.select(e)}}(e)}catch(t){return r.error(`Failed to use Intl.PluralRules for locale "${e}".\nDocusaurus will fallback to the default (English) implementation.\nError: ${t.message}\n`),c}}),[e])}function d(){const e=l();return{selectMessage:(t,s)=>function(e,t,s){const n=e.split("|");if(1===n.length)return n[0];n.length>s.pluralForms.length&&r.error(`For locale=${s.locale}, a maximum of ${s.pluralForms.length} plural forms are expected (${s.pluralForms.join(",")}), but the message contains ${n.length}: ${e}`);const o=s.select(t),a=s.pluralForms.indexOf(o);return n[Math.min(a,n.length-1)]}(s,t,e)}}}}]);