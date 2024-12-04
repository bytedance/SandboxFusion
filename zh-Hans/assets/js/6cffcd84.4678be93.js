"use strict";(self.webpackChunksandbox_fusion=self.webpackChunksandbox_fusion||[]).push([[8771],{50804:(e,t,a)=>{a.r(t),a.d(t,{assets:()=>c,contentTitle:()=>d,default:()=>g,frontMatter:()=>u,metadata:()=>p,toc:()=>r});var s=a(74848),i=a(28453),l=a(43180),n=a(42843);const u={sidebar_position:2},d="HumanEval",p={id:"docs/how-to/use-dataset/humaneval",title:"HumanEval",description:"This is the original HumanEval dataset. To test the dataset on instruction finetuned models, we also provided a freeform mode.",source:"@site/i18n/zh-Hans/docusaurus-plugin-content-docs/current/docs/how-to/use-dataset/humaneval.mdx",sourceDirName:"docs/how-to/use-dataset",slug:"/docs/how-to/use-dataset/humaneval",permalink:"/SandboxFusion/zh-Hans/docs/docs/how-to/use-dataset/humaneval",draft:!1,unlisted:!1,editUrl:"https://github.com/bytedance/SandboxFusion/tree/main/docs/docs/docs/how-to/use-dataset/humaneval.mdx",tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"docSidebar",previous:{title:"FullStack Bench",permalink:"/SandboxFusion/zh-Hans/docs/docs/how-to/use-dataset/fullstack-bench"},next:{title:"MultiPL-E HumanEval",permalink:"/SandboxFusion/zh-Hans/docs/docs/how-to/use-dataset/multiple-humaneval"}},c={},r=[];function h(e){const t={a:"a",h1:"h1",header:"header",p:"p",...(0,i.R)(),...e.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(t.header,{children:(0,s.jsx)(t.h1,{id:"humaneval",children:"HumanEval"})}),"\n",(0,s.jsxs)(t.p,{children:["This is the original ",(0,s.jsx)(t.a,{href:"https://github.com/openai/human-eval",children:"HumanEval"})," dataset. To test the dataset on instruction finetuned models, we also provided a freeform mode."]}),"\n",(0,s.jsx)(l.A,{datasetKey:"HumanEval",generateDocFunc:n.x,configFields:[{name:"extra.is_freeform",type:"boolean",description:"Use freeform mode for instruction finetuned models"},{name:"locale",type:"select",description:"Locale of freeform prompts"},{name:"run_timeout",type:"number",description:"Execution timeout in seconds"}],initialConfig:{locale:"en",run_timeout:20,extra:{is_freeform:!1}}})]})}function g(e={}){const{wrapper:t}={...(0,i.R)(),...e.components};return t?(0,s.jsx)(t,{...e,children:(0,s.jsx)(h,{...e})}):h(e)}},42843:(e,t,a)=>{a.d(t,{x:()=>n});var s=a(27856),i=a(52138),l=a(74848);const n=e=>{let{selectedDataset:t,datasetType:a,config:n,generatePythonDict:u}=e;n.dataset_type=a;const d=u(n);let p=`load_dataset("${t.huggingFace.id}", split="${t.huggingFace.split}")`;return t.huggingFace.subset&&(p=`load_dataset("${t.huggingFace.id}", "${t.huggingFace.subset}", split="${t.huggingFace.split}")`),(0,l.jsxs)(l.Fragment,{children:[(0,l.jsx)(i.default,{language:"python",children:`from datasets import load_dataset\nimport requests\n\nconfig = ${d}\n\n# Get dataset data in sandbox format\ndata = list(${p})\n\nconfig['provided_data'] = data\nprompts = requests.post('${s.A.host}/get_prompts', json={\n  'dataset': '${t.dataset}',\n  'config': config\n}).json()\n\nprint('please perform model inference on these prompts:')\nprint('\\n'.join([p['prompt'] for p in prompts[:3]]))\nprint('...')\n\n# your model inference code here\ncompletions = ['' for _ in prompts]\n\nfor completion, sample in zip(completions, data):\n    config['provided_data'] = sample\n    res = requests.post('${s.A.host}/submit', json={\n        'dataset': '${t.dataset}',\n        'id': '',\n        'completion': completion,\n        'config': config\n    })\n\n    print(f'result: {res.json()}')\n    break`}),(0,l.jsx)("p",{children:"Note: always put raw completion in the request, Sandbox will handle the extraction of code according to different modes."})]})}},43180:(e,t,a)=>{a.d(t,{A:()=>E});var s=a(96540),i=a(27856),l=a(51107),n=a(36628),u=a(57611),d=a(17996),p=a(35181),c=a(72451),r=a(43106),h=a(23232),g=a(91696),o=a(19591),m=a(49162),_=a(53881),v=a(618),b=a(73231),x=a(46780),F=a(88933),j=a(74848);const f=function(e,t){void 0===t&&(t=2);const a=" ".repeat(t);return`{\n${Object.entries(e).map((e=>{let[s,i]=e;return"object"==typeof i&&null!==i?`${a}'${s}': ${f(i,t+2)}`:"boolean"==typeof i?`${a}'${s}': ${i?"True":"False"}`:`${a}'${s}': ${JSON.stringify(i)}`})).join(",\n")}\n${" ".repeat(t-2)}}`},E=e=>{let{datasetKey:t,generateDocFunc:a,configFields:E,initialConfig:y}=e;const P=i.A.datasets[t].datasets,M=i.A.datasets[t].datasetType,[A,C]=(0,s.useState)(P[0]),[L,X]=(0,s.useState)(y),w=(e,t)=>{if(e.startsWith("extra.")){const a=e.split(".")[1];X((e=>({...e,extra:{...e.extra,[a]:t}})))}else X((a=>({...a,[e]:t})))},k=e=>{const t=e.name.startsWith("extra.")?L.extra[e.name.split(".")[1]]:L[e.name];switch(e.type){case"number":return(0,j.jsx)(n.A,{type:"number",value:t,onChange:t=>w(e.name,parseInt(t.target.value,10)),fullWidth:!0});case"boolean":return(0,j.jsx)(u.A,{checked:t,onChange:t=>w(e.name,t.target.checked),color:"primary"});case"select":return"locale"===e.name?(0,j.jsxs)(d.A,{value:t,onChange:t=>w(e.name,t.target.value),row:!0,children:[(0,j.jsx)(p.A,{value:"en",control:(0,j.jsx)(c.A,{}),label:"English"}),(0,j.jsx)(p.A,{value:"zh",control:(0,j.jsx)(c.A,{}),label:"Chinese"})]}):"language"===e.name?(0,j.jsxs)(r.A,{value:t,onChange:t=>w(e.name,t.target.value),fullWidth:!0,children:[(0,j.jsx)(h.A,{value:"cpp",children:"C++"}),(0,j.jsx)(h.A,{value:"python",children:"Python"}),(0,j.jsx)(h.A,{value:"java",children:"Java"})]}):"extra.autoeval_extract_code_mode"===e.name?(0,j.jsxs)(r.A,{value:t,onChange:t=>w(e.name,t.target.value),fullWidth:!0,children:[(0,j.jsx)(h.A,{value:"FIRST_BLOCK_ONLY",children:"First Block Only"}),(0,j.jsx)(h.A,{value:"ALL_BLOCKS",children:"All Blocks"})]}):"extra.mode"===e.name?(0,j.jsxs)(d.A,{value:t,onChange:t=>w(e.name,t.target.value),row:!0,children:[(0,j.jsx)(p.A,{value:"input",control:(0,j.jsx)(c.A,{}),label:"input"}),(0,j.jsx)(p.A,{value:"output",control:(0,j.jsx)(c.A,{}),label:"output"})]}):null;case"text":return(0,j.jsx)(n.A,{value:t,onChange:t=>w(e.name,t.target.value),fullWidth:!0,multiline:!0,rows:3});default:return(0,j.jsx)(n.A,{value:t,onChange:t=>w(e.name,t.target.value),fullWidth:!0})}};return(0,j.jsxs)(j.Fragment,{children:[P.length>1&&(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)("header",{children:(0,j.jsx)(l.default,{as:"h2",children:"Subset Selection"})}),(0,j.jsx)(g.A,{component:"fieldset",children:(0,j.jsx)(d.A,{value:A.id,onChange:e=>{const t=e.target.value,a=P.find((e=>e.id===t))||P[0];C(a)},children:P.map((e=>(0,j.jsx)(p.A,{value:e.id,control:(0,j.jsx)(c.A,{}),label:e.id},e.id)))})})]}),(0,j.jsx)("header",{children:(0,j.jsx)(l.default,{as:"h2",children:"Configuration"})}),(0,j.jsx)(o.A,{component:m.A,sx:{mb:3},children:(0,j.jsxs)(_.A,{children:[(0,j.jsx)(v.A,{children:(0,j.jsxs)(b.A,{children:[(0,j.jsx)(x.A,{children:"Field"}),(0,j.jsx)(x.A,{children:"Value"}),(0,j.jsx)(x.A,{children:"Description"})]})}),(0,j.jsx)(F.A,{children:E.map((e=>(0,j.jsxs)(b.A,{children:[(0,j.jsx)(x.A,{children:e.name}),(0,j.jsx)(x.A,{children:k(e)}),(0,j.jsx)(x.A,{children:e.description})]},e.name)))})]})}),(0,j.jsx)("header",{children:(0,j.jsx)(l.default,{as:"h2",children:"Usage"})}),a({selectedDataset:A,datasetType:M,config:L,pythonConfig:f(L),generatePythonDict:f})]})}},27856:(e,t,a)=>{a.d(t,{A:()=>i,E:()=>s});const s={FullStackBench:{datasetType:"AutoEvalDataset",datasets:[{id:"full_stack_bench_zh",dataset:"full_stack_bench_zh",huggingFace:{id:"ByteDance/FullStackBench",subset:"zh",split:"test"}},{id:"full_stack_bench_en",dataset:"full_stack_bench_en",huggingFace:{id:"ByteDance/FullStackBench",subset:"en",split:"test"}}]},AutoEval:{datasetType:"AutoEvalDataset",datasets:[{id:"leetcode_sample_python",dataset:"leetcode_sample_python",huggingFace:{id:"sine/LeetCodeSample",subset:"python",split:"test"}}]},HumanEval:{datasetType:"HumanEvalDataset",datasets:[{id:"humaneval_python",dataset:"humaneval_python",huggingFace:{id:"openai/openai_humaneval",split:"test"}}]},MBPP:{datasetType:"MBPPDataset",datasets:[{id:"mbpp",dataset:"mbpp",huggingFace:{id:"laylarsssss/FusedMBPP",split:"test"}}]},MHPP:{datasetType:"MHPPDataset",datasets:[{id:"mhpp_140",dataset:"mhpp",huggingFace:{id:"laylarsssss/FusedMHPP",subset:"mhpp",split:"test"}},{id:"mhpp_210",dataset:"mhpp",huggingFace:{id:"laylarsssss/FusedMHPP",subset:"mhpp_210",split:"test"}}]},MiniF2F:{datasetType:"MiniF2FLean4Dataset",datasets:[{id:"minif2f_lean4_test",dataset:"minif2f_lean4_test",huggingFace:{id:"laylarsssss/FusedMHPP",split:"test"}},{id:"minif2f_lean4_valid",dataset:"minif2f_lean4_valid",huggingFace:{id:"laylarsssss/FusedMHPP",split:"test"}}]},MultipleHumanEval:{datasetType:"MultiPLEDataset",datasets:[{id:"humaneval_cpp",dataset:"multiple_cpp",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-cpp",split:"test"}},{id:"humaneval_typescript",dataset:"multiple_typescript",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-ts",split:"test"}},{id:"humaneval_bash",dataset:"multiple_bash",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-sh",split:"test"}},{id:"humaneval_csharp",dataset:"multiple_csharp",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-cs",split:"test"}},{id:"humaneval_go",dataset:"multiple_go",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-go",split:"test"}},{id:"humaneval_java",dataset:"multiple_java",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-java",split:"test"}},{id:"humaneval_lua",dataset:"multiple_lua",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-lua",split:"test"}},{id:"humaneval_javascript",dataset:"multiple_javascript",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-js",split:"test"}},{id:"humaneval_php",dataset:"multiple_php",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-php",split:"test"}},{id:"humaneval_perl",dataset:"multiple_perl",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-pl",split:"test"}},{id:"humaneval_racket",dataset:"multiple_racket",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-rkt",split:"test"}},{id:"humaneval_r",dataset:"multiple_r",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-r",split:"test"}},{id:"humaneval_rust",dataset:"multiple_rust",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-rs",split:"test"}},{id:"humaneval_scala",dataset:"multiple_scala",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-scala",split:"test"}},{id:"humaneval_swift",dataset:"multiple_swift",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-swift",split:"test"}},{id:"humaneval_ruby",dataset:"multiple_ruby",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-ruby",split:"test"}},{id:"humaneval_d",dataset:"multiple_d",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-d",split:"test"}},{id:"humaneval_julia",dataset:"multiple_julia",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-jl",split:"test"}}]},MultipleMBPP:{datasetType:"MultiPLEDataset",datasets:[{id:"mbpp_cpp",dataset:"multiple_cpp",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-cpp",split:"test"}},{id:"mbpp_typescript",dataset:"multiple_typescript",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-ts",split:"test"}},{id:"mbpp_bash",dataset:"multiple_bash",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-sh",split:"test"}},{id:"mbpp_csharp",dataset:"multiple_csharp",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-cs",split:"test"}},{id:"mbpp_go",dataset:"multiple_go",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-go",split:"test"}},{id:"mbpp_java",dataset:"multiple_java",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-java",split:"test"}},{id:"mbpp_lua",dataset:"multiple_lua",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-lua",split:"test"}},{id:"mbpp_javascript",dataset:"multiple_javascript",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-js",split:"test"}},{id:"mbpp_php",dataset:"multiple_php",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-php",split:"test"}},{id:"mbpp_perl",dataset:"multiple_perl",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-pl",split:"test"}},{id:"mbpp_racket",dataset:"multiple_racket",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-rkt",split:"test"}},{id:"mbpp_r",dataset:"multiple_r",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-r",split:"test"}},{id:"mbpp_rust",dataset:"multiple_rust",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-rs",split:"test"}},{id:"mbpp_scala",dataset:"multiple_scala",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-scala",split:"test"}},{id:"mbpp_swift",dataset:"multiple_swift",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-swift",split:"test"}},{id:"mbpp_ruby",dataset:"multiple_ruby",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-ruby",split:"test"}},{id:"mbpp_d",dataset:"multiple_d",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-d",split:"test"}},{id:"mbpp_julia",dataset:"multiple_julia",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-jl",split:"test"}}]},CommonOJ:{datasetType:"CommonOJDataset",datasets:[{id:"code_contests_train",dataset:"code_contests_train",huggingFace:{id:"sine/FusedCodeContests",split:"train"}},{id:"code_contests_valid",dataset:"code_contests_valid",huggingFace:{id:"sine/FusedCodeContests",split:"valid"}},{id:"code_contests_test",dataset:"code_contests_test",huggingFace:{id:"sine/FusedCodeContests",split:"test"}}]},CRUXEval:{datasetType:"CruxEvalDataset",datasets:[{id:"cruxeval",dataset:"cruxeval",huggingFace:{id:"cruxeval-org/cruxeval",split:"test"}}]},CRUXEvalX:{datasetType:"CruxEvalDataset",datasets:[{id:"cruxeval_x_D_ut",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"D_ut",split:"test"}},{id:"cruxeval_x_R",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"R",split:"test"}},{id:"cruxeval_x_bash",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"bash",split:"test"}},{id:"cruxeval_x_cpp",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"cpp",split:"test"}},{id:"cruxeval_x_csharp",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"csharp",split:"test"}},{id:"cruxeval_x_go_test",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"go_test",split:"test"}},{id:"cruxeval_x_java",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"java",split:"test"}},{id:"cruxeval_x_julia",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"julia",split:"test"}},{id:"cruxeval_x_lua",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"lua",split:"test"}},{id:"cruxeval_x_nodejs",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"nodejs",split:"test"}},{id:"cruxeval_x_perl",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"perl",split:"test"}},{id:"cruxeval_x_php",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"php",split:"test"}},{id:"cruxeval_x_python",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"python",split:"test"}},{id:"cruxeval_x_racket",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"racket",split:"test"}},{id:"cruxeval_x_ruby",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"ruby",split:"test"}},{id:"cruxeval_x_rust",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"rust",split:"test"}},{id:"cruxeval_x_scala",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"scala",split:"test"}},{id:"cruxeval_x_swift",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"swift",split:"test"}},{id:"cruxeval_x_typescript",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"typescript",split:"test"}}]},NaturalCodeBench:{datasetType:"NaturalCodeBenchDataset",datasets:[{id:"ncb_python_zh",dataset:"ncb_python_zh",huggingFace:{id:"sine/FusedNaturalCodeBench",subset:"python_zh",split:"test"}},{id:"ncb_python_en",dataset:"ncb_python_en",huggingFace:{id:"sine/FusedNaturalCodeBench",subset:"python_en",split:"test"}},{id:"ncb_java_zh",dataset:"ncb_java_zh",huggingFace:{id:"sine/FusedNaturalCodeBench",subset:"java_zh",split:"test"}},{id:"ncb_java_en",dataset:"ncb_java_en",huggingFace:{id:"sine/FusedNaturalCodeBench",subset:"java_en",split:"test"}}]},PALMath:{datasetType:"PalMathDataset",datasets:[{id:"asdiv",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"asdiv",split:"test"}},{id:"gsm8k",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"gsm8k",split:"test"}},{id:"hard",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"hard",split:"test"}},{id:"math",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"math",split:"test"}},{id:"mawps",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"mawps",split:"test"}},{id:"svamp",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"svamp",split:"test"}},{id:"tabmwp",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"tabmwp",split:"test"}}]},VerilogEval:{datasetType:"PalMathDataset",datasets:[{id:"verilogeval_human",dataset:"verilogeval_human",huggingFace:{id:"sine/FusedVerilogEval",subset:"human",split:"test"}},{id:"verilogeval_machine",dataset:"verilogeval_machine",huggingFace:{id:"sine/FusedVerilogEval",subset:"machine",split:"test"}}]}},i={image:"volcengine/sandbox-fusion:server-20241204",cnImage:"vemlp-cn-beijing.cr.volces.com/preset-images/code-sandbox:server-20241204",host:"http://localhost:8080",datasets:s}}}]);