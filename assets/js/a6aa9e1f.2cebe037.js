"use strict";(self.webpackChunksandbox_fusion=self.webpackChunksandbox_fusion||[]).push([[7643],{82052:(e,t,a)=>{a.r(t),a.d(t,{default:()=>v});a(96540);var n=a(34164),s=a(44586),r=a(45500),l=a(17559),i=a(28027),o=a(21312),c=a(39022),d=a(74848);function u(e){const{metadata:t}=e,{previousPage:a,nextPage:n}=t;return(0,d.jsxs)("nav",{className:"pagination-nav","aria-label":(0,o.translate)({id:"theme.blog.paginator.navAriaLabel",message:"Blog list page navigation",description:"The ARIA label for the blog pagination"}),children:[a&&(0,d.jsx)(c.A,{permalink:a,title:(0,d.jsx)(o.default,{id:"theme.blog.paginator.newerEntries",description:"The label used to navigate to the newer blog posts page (previous page)",children:"Newer entries"})}),n&&(0,d.jsx)(c.A,{permalink:n,title:(0,d.jsx)(o.default,{id:"theme.blog.paginator.olderEntries",description:"The label used to navigate to the older blog posts page (next page)",children:"Older entries"}),isNext:!0})]})}var m=a(41463),g=a(44096),h=a(82907);function x(e){let{items:t,component:a=h.A}=e;return(0,d.jsx)(d.Fragment,{children:t.map((e=>{let{content:t}=e;return(0,d.jsx)(g.in,{content:t,children:(0,d.jsx)(a,{children:(0,d.jsx)(t,{})})},t.metadata.permalink)}))})}var p=a(5260);function j(e){const t=(0,g.kJ)(e);return(0,d.jsx)(p.A,{children:(0,d.jsx)("script",{type:"application/ld+json",children:JSON.stringify(t)})})}function f(e){const{metadata:t}=e,{siteConfig:{title:a}}=(0,s.default)(),{blogDescription:n,blogTitle:l,permalink:i}=t,o="/"===i?a:l;return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(r.be,{title:o,description:n}),(0,d.jsx)(m.A,{tag:"blog_posts_list"})]})}function b(e){const{metadata:t,items:a,sidebar:n}=e;return(0,d.jsxs)(i.A,{sidebar:n,children:[(0,d.jsx)(x,{items:a}),(0,d.jsx)(u,{metadata:t})]})}function v(e){return(0,d.jsxs)(r.e3,{className:(0,n.A)(l.G.wrapper.blogPages,l.G.page.blogListPage),children:[(0,d.jsx)(f,{...e}),(0,d.jsx)(j,{...e}),(0,d.jsx)(b,{...e})]})}},82907:(e,t,a)=>{a.d(t,{A:()=>U});a(96540);var n=a(34164),s=a(44096),r=a(74848);function l(e){let{children:t,className:a}=e;return(0,r.jsx)("article",{className:a,children:t})}var i=a(28774);const o={title:"title_f1Hy"};function c(e){let{className:t}=e;const{metadata:a,isBlogPostPage:l}=(0,s.e7)(),{permalink:c,title:d}=a,u=l?"h1":"h2";return(0,r.jsx)(u,{className:(0,n.A)(o.title,t),children:l?d:(0,r.jsx)(i.default,{to:c,children:d})})}var d=a(21312),u=a(53465),m=a(36266);const g={container:"container_mt6G"};function h(e){let{readingTime:t}=e;const a=function(){const{selectMessage:e}=(0,u.W)();return t=>{const a=Math.ceil(t);return e(a,(0,d.translate)({id:"theme.blog.post.readingTime.plurals",description:'Pluralized label for "{readingTime} min read". Use as much plural forms (separated by "|") as your language support (see https://www.unicode.org/cldr/cldr-aux/charts/34/supplemental/language_plural_rules.html)',message:"One min read|{readingTime} min read"},{readingTime:a}))}}();return(0,r.jsx)(r.Fragment,{children:a(t)})}function x(e){let{date:t,formattedDate:a}=e;return(0,r.jsx)("time",{dateTime:t,children:a})}function p(){return(0,r.jsx)(r.Fragment,{children:" \xb7 "})}function j(e){let{className:t}=e;const{metadata:a}=(0,s.e7)(),{date:l,readingTime:i}=a,o=(0,m.i)({day:"numeric",month:"long",year:"numeric",timeZone:"UTC"});return(0,r.jsxs)("div",{className:(0,n.A)(g.container,"margin-vert--md",t),children:[(0,r.jsx)(x,{date:l,formattedDate:(c=l,o.format(new Date(c)))}),void 0!==i&&(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)(p,{}),(0,r.jsx)(h,{readingTime:i})]})]});var c}var f=a(56913);const b={authorCol:"authorCol_Hf19",imageOnlyAuthorRow:"imageOnlyAuthorRow_pa_O",imageOnlyAuthorCol:"imageOnlyAuthorCol_G86a"};function v(e){let{className:t}=e;const{metadata:{authors:a},assets:l}=(0,s.e7)();if(0===a.length)return null;const i=a.every((e=>{let{name:t}=e;return!t})),o=1===a.length;return(0,r.jsx)("div",{className:(0,n.A)("margin-top--md margin-bottom--sm",i?b.imageOnlyAuthorRow:"row",t),children:a.map(((e,t)=>(0,r.jsx)("div",{className:(0,n.A)(!i&&(o?"col col--12":"col col--6"),i?b.imageOnlyAuthorCol:b.authorCol),children:(0,r.jsx)(f.A,{author:{...e,imageURL:l.authorsImageUrls[t]??e.imageURL}})},t)))})}function A(){return(0,r.jsxs)("header",{children:[(0,r.jsx)(c,{}),(0,r.jsx)(j,{}),(0,r.jsx)(v,{})]})}var N=a(70440),_=a(72857);function T(e){let{children:t,className:a}=e;const{isBlogPostPage:l}=(0,s.e7)();return(0,r.jsx)("div",{id:l?N.LU:void 0,className:(0,n.A)("markdown",a),children:(0,r.jsx)(_.A,{children:t})})}var k=a(17559),w=a(4336),y=a(58046);function C(){return(0,r.jsx)("b",{children:(0,r.jsx)(d.default,{id:"theme.blog.post.readMore",description:"The label used in blog post item excerpts to link to full blog posts",children:"Read more"})})}function P(e){const{blogPostTitle:t,...a}=e;return(0,r.jsx)(i.default,{"aria-label":(0,d.translate)({message:"Read more about {title}",id:"theme.blog.post.readMoreLabel",description:"The ARIA label for the link to full blog posts from excerpts"},{title:t}),...a,children:(0,r.jsx)(C,{})})}function R(){const{metadata:e,isBlogPostPage:t}=(0,s.e7)(),{tags:a,title:l,editUrl:i,hasTruncateMarker:o,lastUpdatedBy:c,lastUpdatedAt:d}=e,u=!t&&o,m=a.length>0;if(!(m||u||i))return null;if(t){const e=!!(i||d||c);return(0,r.jsxs)("footer",{className:"docusaurus-mt-lg",children:[m&&(0,r.jsx)("div",{className:(0,n.A)("row","margin-top--sm",k.G.blog.blogFooterEditMetaRow),children:(0,r.jsx)("div",{className:"col",children:(0,r.jsx)(y.A,{tags:a})})}),e&&(0,r.jsx)(w.A,{className:(0,n.A)("margin-top--sm",k.G.blog.blogFooterEditMetaRow),editUrl:i,lastUpdatedAt:d,lastUpdatedBy:c})]})}return(0,r.jsxs)("footer",{className:"row docusaurus-mt-lg",children:[m&&(0,r.jsx)("div",{className:(0,n.A)("col",{"col--9":u}),children:(0,r.jsx)(y.A,{tags:a})}),u&&(0,r.jsx)("div",{className:(0,n.A)("col text--right",{"col--3":m}),children:(0,r.jsx)(P,{blogPostTitle:l,to:e.permalink})})]})}function U(e){let{children:t,className:a}=e;const i=function(){const{isBlogPostPage:e}=(0,s.e7)();return e?void 0:"margin-bottom--xl"}();return(0,r.jsxs)(l,{className:(0,n.A)(i,a),children:[(0,r.jsx)(A,{}),(0,r.jsx)(T,{children:t}),(0,r.jsx)(R,{})]})}},39022:(e,t,a)=>{a.d(t,{A:()=>l});a(96540);var n=a(34164),s=a(28774),r=a(74848);function l(e){const{permalink:t,title:a,subLabel:l,isNext:i}=e;return(0,r.jsxs)(s.default,{className:(0,n.A)("pagination-nav__link",i?"pagination-nav__link--next":"pagination-nav__link--prev"),to:t,children:[l&&(0,r.jsx)("div",{className:"pagination-nav__sublabel",children:l}),(0,r.jsx)("div",{className:"pagination-nav__label",children:a})]})}},58046:(e,t,a)=>{a.d(t,{A:()=>d});a(96540);var n=a(34164),s=a(21312),r=a(28774);const l={tag:"tag_zVej",tagRegular:"tagRegular_sFm0",tagWithCount:"tagWithCount_h2kH"};var i=a(74848);function o(e){let{permalink:t,label:a,count:s,description:o}=e;return(0,i.jsxs)(r.default,{href:t,title:o,className:(0,n.A)(l.tag,s?l.tagWithCount:l.tagRegular),children:[a,s&&(0,i.jsx)("span",{children:s})]})}const c={tags:"tags_jXut",tag:"tag_QGVx"};function d(e){let{tags:t}=e;return(0,i.jsxs)(i.Fragment,{children:[(0,i.jsx)("b",{children:(0,i.jsx)(s.default,{id:"theme.tags.tagsListLabel",description:"The label alongside a tag list",children:"Tags:"})}),(0,i.jsx)("ul",{className:(0,n.A)(c.tags,"padding--none","margin-left--sm"),children:t.map((e=>(0,i.jsx)("li",{className:c.tag,children:(0,i.jsx)(o,{...e})},e.permalink)))})]})}},36266:(e,t,a)=>{a.d(t,{i:()=>s});var n=a(44586);function s(e){void 0===e&&(e={});const{i18n:{currentLocale:t}}=(0,n.default)(),a=function(){const{i18n:{currentLocale:e,localeConfigs:t}}=(0,n.default)();return t[e].calendar}();return new Intl.DateTimeFormat(t,{calendar:a,...e})}},88473:(e,t,a)=>{a.d(t,{c:()=>r});var n=a(96540),s=a(74848);function r(e){const{mdxAdmonitionTitle:t,rest:a}=function(e){const t=n.Children.toArray(e),a=t.find((e=>n.isValidElement(e)&&"mdxAdmonitionTitle"===e.type)),r=t.filter((e=>e!==a)),l=a?.props.children;return{mdxAdmonitionTitle:l,rest:r.length>0?(0,s.jsx)(s.Fragment,{children:r}):null}}(e.children),r=e.title??t;return{...e,...r&&{title:r},children:a}}}}]);