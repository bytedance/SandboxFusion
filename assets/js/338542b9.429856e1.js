"use strict";(self.webpackChunksandbox_fusion=self.webpackChunksandbox_fusion||[]).push([[1781],{30221:(e,n,o)=>{o.r(n),o.d(n,{assets:()=>i,contentTitle:()=>t,default:()=>m,frontMatter:()=>r,metadata:()=>c,toc:()=>l});var a=o(74848),s=o(28453);const r={sidebar_position:3},t="Configuration File",c={id:"docs/reference/config",title:"Configuration File",description:"The runtime configuration file is controlled by the environment variable SANDBOXCONFIG. The corresponding file path is sandbox/configs/.yaml. By default, the configuration is set to sandbox/configs/local.yaml.",source:"@site/docs/docs/reference/config.md",sourceDirName:"docs/reference",slug:"/docs/reference/config",permalink:"/SandboxFusion/docs/docs/reference/config",draft:!1,unlisted:!1,editUrl:"https://github.com/bytedance/SandboxFusion/tree/main/docs/docs/docs/reference/config.md",tags:[],version:"current",sidebarPosition:3,frontMatter:{sidebar_position:3},sidebar:"docSidebar",previous:{title:"CommonOJ",permalink:"/SandboxFusion/docs/docs/reference/dataset-detail/common-oj"},next:{title:"Explanation",permalink:"/SandboxFusion/docs/category/explanation"}},i={},l=[];function d(e){const n={code:"code",h1:"h1",header:"header",p:"p",pre:"pre",...(0,s.R)(),...e.components};return(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(n.header,{children:(0,a.jsx)(n.h1,{id:"configuration-file",children:"Configuration File"})}),"\n",(0,a.jsxs)(n.p,{children:["The runtime configuration file is controlled by the environment variable SANDBOX_CONFIG. The corresponding file path is ",(0,a.jsx)(n.code,{children:"sandbox/configs/{SANDBOX_CONFIG}.yaml"}),". By default, the configuration is set to ",(0,a.jsx)(n.code,{children:"sandbox/configs/local.yaml"}),"."]}),"\n",(0,a.jsx)(n.pre,{children:(0,a.jsx)(n.code,{className:"language-yaml",children:"online_judge:\n  database:\n    backend:\n      type: mysql  # or none\n      user: mysql_user\n      password: mysql_password\n      host: mysql_host\n      port: mysql_port\n    cache:  # optional cache, remove to disable\n      path: memory  # sqlite database path, file address or memory\n      sources:\n      - type: mysql  # cache data source, mysql for online database, local for local folder\n        tables:\n        - name: table_name\n          columns: [id, labels, content, test]\n  # Maximum concurrency when requesting the sandbox\n  max_runner_concurrency: 5\nrunner:\n  isolation: none  # Isolation level when running code, none (no isolation) or lite (overlayfs+cgroups+namespace, recommended for use within docker to avoid affecting the host machine)\n  cleanup_process: false  # Kill all processes unrelated to the sandbox service after each request, use with caution locally\n  restore_bash: true  # Check bash binary integrity and attempt to restore after each request\n  max_concurrency: 0  # Maximum concurrency, 0 for no limit\ncommon:\n  logging_color: false  # Whether to include color in log output\n"})}),"\n",(0,a.jsx)(n.p,{children:"Below are examples of configuration files for different scenarios."}),"\n",(0,a.jsx)(n.p,{children:"local.yaml for local development:"}),"\n",(0,a.jsx)(n.pre,{children:(0,a.jsx)(n.code,{className:"language-yaml",children:"online_judge:\n  database:\n    backend:\n      type: none  # Don't connect to online database\n    cache:\n      path: memory  # Location of local cache sqlite database, here it's in memory\n      sources:\n        - type: local  # Read jsonl files from local folder as cache\n          path: sandbox/tests/datasets/samples\n  max_runner_concurrency: 3\nrunner:\n  isolation: none\n  cleanup_process: false\n  restore_bash: false\n  max_concurrency: 34\ncommon:\n  logging_color: true\n"})}),"\n",(0,a.jsx)(n.p,{children:"ci.yaml for integration testing environment:"}),"\n",(0,a.jsx)(n.p,{children:"The integration testing environment uses all local information"}),"\n",(0,a.jsx)(n.pre,{children:(0,a.jsx)(n.code,{className:"language-yaml",children:"online_judge:\n  database:\n    backend:\n      type: none\n    cache:\n      path: memory\n      sources:\n        - type: local\n          path: sandbox/tests/datasets/samples\n  max_runner_concurrency: 3\nrunner:\n  isolation: lite\n  cleanup_process: false\n  restore_bash: false\n  max_concurrency: 0  # concurrency in ci is limited by pytest-xdist\ncommon:\n  logging_color: true\n"})})]})}function m(e={}){const{wrapper:n}={...(0,s.R)(),...e.components};return n?(0,a.jsx)(n,{...e,children:(0,a.jsx)(d,{...e})}):d(e)}}}]);