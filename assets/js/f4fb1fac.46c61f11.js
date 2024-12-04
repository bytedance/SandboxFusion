"use strict";(self.webpackChunksandbox_fusion=self.webpackChunksandbox_fusion||[]).push([[2928],{35274:(e,a,n)=>{n.r(a),n.d(a,{assets:()=>t,contentTitle:()=>d,default:()=>j,frontMatter:()=>c,metadata:()=>r,toc:()=>o});var s=n(74848),i=n(28453);const c={},d="Java",r={id:"docs/reference/execution-detail/java",title:"Java",description:"Version: JDK 21",source:"@site/docs/docs/reference/execution-detail/java.md",sourceDirName:"docs/reference/execution-detail",slug:"/docs/reference/execution-detail/java",permalink:"/SandboxFusion/docs/docs/reference/execution-detail/java",draft:!1,unlisted:!1,editUrl:"https://github.com/bytedance/SandboxFusion/tree/main/docs/docs/docs/reference/execution-detail/java.md",tags:[],version:"current",frontMatter:{},sidebar:"docSidebar",previous:{title:"go",permalink:"/SandboxFusion/docs/docs/reference/execution-detail/go"},next:{title:"Lean",permalink:"/SandboxFusion/docs/docs/reference/execution-detail/lean"}},t={},o=[{value:"Java",id:"java-1",level:2},{value:"JUnit",id:"junit",level:2}];function l(e){const a={code:"code",h1:"h1",h2:"h2",header:"header",p:"p",pre:"pre",...(0,i.R)(),...e.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(a.header,{children:(0,s.jsx)(a.h1,{id:"java",children:"Java"})}),"\n",(0,s.jsx)(a.p,{children:"Version: JDK 21"}),"\n",(0,s.jsxs)(a.p,{children:["Java supports two running modes: ",(0,s.jsx)(a.code,{children:"java"})," and ",(0,s.jsx)(a.code,{children:"junit"}),"."]}),"\n",(0,s.jsx)(a.h2,{id:"java-1",children:"Java"}),"\n",(0,s.jsxs)(a.p,{children:["In ",(0,s.jsx)(a.code,{children:"java"})," mode, the compilation command is ",(0,s.jsx)(a.code,{children:"javac -cp .:javatuples-1.2.jar:<jars> Main.java"}),", and the execution command is ",(0,s.jsx)(a.code,{children:"java -cp .:javatuples-1.2.jar:<jars> -ea Main"}),"."]}),"\n",(0,s.jsxs)(a.p,{children:["Here, ",(0,s.jsx)(a.code,{children:"jars"})," refers to all files ending with ",(0,s.jsx)(a.code,{children:".jar"})," in the files passed as parameters."]}),"\n",(0,s.jsx)(a.p,{children:"Please ensure that the Java class name passed in is Main."}),"\n",(0,s.jsx)(a.h2,{id:"junit",children:"JUnit"}),"\n",(0,s.jsxs)(a.p,{children:["In ",(0,s.jsx)(a.code,{children:"junit"})," mode, the compilation command is"]}),"\n",(0,s.jsx)(a.pre,{children:(0,s.jsx)(a.code,{className:"language-bash",children:"javac -cp .:junit-platform-console-standalone-1.8.2.jar:junit-jupiter-api-5.11.0-javadoc.jar:<jars> *.java\n"})}),"\n",(0,s.jsx)(a.p,{children:"and the execution command is"}),"\n",(0,s.jsx)(a.pre,{children:(0,s.jsx)(a.code,{className:"language-bash",children:"java -jar ./junit-platform-console-standalone-1.8.2.jar --class-path .:junit-platform-console-standalone-1.8.2.jar:junit-jupiter-api-5.11.0-javadoc.jar:<jars> --scan-class-path\n"})}),"\n",(0,s.jsxs)(a.p,{children:["The sandbox automatically detects the class name in the code passed as the code parameter and places it in the corresponding ",(0,s.jsx)(a.code,{children:".java"})," file. If no class name is found, it will still be placed in ",(0,s.jsx)(a.code,{children:"Main.java"}),"."]})]})}function j(e={}){const{wrapper:a}={...(0,i.R)(),...e.components};return a?(0,s.jsx)(a,{...e,children:(0,s.jsx)(l,{...e})}):l(e)}}}]);