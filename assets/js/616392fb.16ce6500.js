"use strict";(self.webpackChunksandbox_fusion=self.webpackChunksandbox_fusion||[]).push([[4748],{39084:(t,e,a)=>{a.r(e),a.d(e,{assets:()=>c,contentTitle:()=>d,default:()=>h,frontMatter:()=>u,metadata:()=>p,toc:()=>r});var s=a(74848),i=a(28453),l=a(43180),n=a(42843);const u={sidebar_position:4},d="MBPP",p={id:"docs/how-to/use-dataset/mbpp",title:"MBPP",description:"This is the test set of Mostly Basic Python Problems Dataset, with id in [11, 510].",source:"@site/docs/docs/how-to/use-dataset/mbpp.mdx",sourceDirName:"docs/how-to/use-dataset",slug:"/docs/how-to/use-dataset/mbpp",permalink:"/SandboxFusion/docs/docs/how-to/use-dataset/mbpp",draft:!1,unlisted:!1,editUrl:"https://github.com/bytedance/SandboxFusion/tree/main/docs/docs/docs/how-to/use-dataset/mbpp.mdx",tags:[],version:"current",sidebarPosition:4,frontMatter:{sidebar_position:4},sidebar:"docSidebar",previous:{title:"MultiPL-E HumanEval",permalink:"/SandboxFusion/docs/docs/how-to/use-dataset/multiple-humaneval"},next:{title:"MultiPL-E MBPP",permalink:"/SandboxFusion/docs/docs/how-to/use-dataset/multiple-mbpp"}},c={},r=[];function g(t){const e={a:"a",h1:"h1",header:"header",p:"p",...(0,i.R)(),...t.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(e.header,{children:(0,s.jsx)(e.h1,{id:"mbpp",children:"MBPP"})}),"\n",(0,s.jsxs)(e.p,{children:["This is the test set of ",(0,s.jsx)(e.a,{href:"https://github.com/google-research/google-research/tree/master/mbpp",children:"Mostly Basic Python Problems Dataset"}),", with id in [11, 510]."]}),"\n",(0,s.jsx)(l.A,{datasetKey:"MBPP",generateDocFunc:n.x,configFields:[{name:"is_fewshot",type:"boolean",description:"Append fewshot examples before problem"},{name:"run_timeout",type:"number",description:"Execution timeout in seconds"}],initialConfig:{is_fewshot:!0,run_timeout:20}})]})}function h(t={}){const{wrapper:e}={...(0,i.R)(),...t.components};return e?(0,s.jsx)(e,{...t,children:(0,s.jsx)(g,{...t})}):g(t)}},42843:(t,e,a)=>{a.d(e,{x:()=>n});var s=a(27856),i=a(52138),l=a(74848);const n=t=>{let{selectedDataset:e,datasetType:a,config:n,generatePythonDict:u}=t;n.dataset_type=a;const d=u(n);let p=`load_dataset("${e.huggingFace.id}", split="${e.huggingFace.split}")`;return e.huggingFace.subset&&(p=`load_dataset("${e.huggingFace.id}", "${e.huggingFace.subset}", split="${e.huggingFace.split}")`),(0,l.jsxs)(l.Fragment,{children:[(0,l.jsx)(i.default,{language:"python",children:`from datasets import load_dataset\nimport requests\n\nconfig = ${d}\n\n# Get dataset data in sandbox format\ndata = list(${p})\n\nconfig['provided_data'] = data\nprompts = requests.post('${s.A.host}/get_prompts', json={\n  'dataset': '${e.dataset}',\n  'config': config\n}).json()\n\nprint('please perform model inference on these prompts:')\nprint('\\n'.join([p['prompt'] for p in prompts[:3]]))\nprint('...')\n\n# your model inference code here\ncompletions = ['' for _ in prompts]\n\nfor completion, sample in zip(completions, data):\n    config['provided_data'] = sample\n    res = requests.post('${s.A.host}/submit', json={\n        'dataset': '${e.dataset}',\n        'id': '',\n        'completion': completion,\n        'config': config\n    })\n\n    print(f'result: {res.json()}')\n    break`}),(0,l.jsx)("p",{children:"Note: always put raw completion in the request, Sandbox will handle the extraction of code according to different modes."})]})}},43180:(t,e,a)=>{a.d(e,{A:()=>f});var s=a(96540),i=a(27856),l=a(51107),n=a(36628),u=a(57611),d=a(17996),p=a(35181),c=a(72451),r=a(43106),g=a(23232),h=a(91696),o=a(19591),m=a(49162),_=a(53881),v=a(618),b=a(73231),x=a(46780),F=a(88933),j=a(74848);const P=function(t,e){void 0===e&&(e=2);const a=" ".repeat(e);return`{\n${Object.entries(t).map((t=>{let[s,i]=t;return"object"==typeof i&&null!==i?`${a}'${s}': ${P(i,e+2)}`:"boolean"==typeof i?`${a}'${s}': ${i?"True":"False"}`:`${a}'${s}': ${JSON.stringify(i)}`})).join(",\n")}\n${" ".repeat(e-2)}}`},f=t=>{let{datasetKey:e,generateDocFunc:a,configFields:f,initialConfig:y}=t;const E=i.A.datasets[e].datasets,M=i.A.datasets[e].datasetType,[A,C]=(0,s.useState)(E[0]),[L,X]=(0,s.useState)(y),w=(t,e)=>{if(t.startsWith("extra.")){const a=t.split(".")[1];X((t=>({...t,extra:{...t.extra,[a]:e}})))}else X((a=>({...a,[t]:e})))},k=t=>{const e=t.name.startsWith("extra.")?L.extra[t.name.split(".")[1]]:L[t.name];switch(t.type){case"number":return(0,j.jsx)(n.A,{type:"number",value:e,onChange:e=>w(t.name,parseInt(e.target.value,10)),fullWidth:!0});case"boolean":return(0,j.jsx)(u.A,{checked:e,onChange:e=>w(t.name,e.target.checked),color:"primary"});case"select":return"locale"===t.name?(0,j.jsxs)(d.A,{value:e,onChange:e=>w(t.name,e.target.value),row:!0,children:[(0,j.jsx)(p.A,{value:"en",control:(0,j.jsx)(c.A,{}),label:"English"}),(0,j.jsx)(p.A,{value:"zh",control:(0,j.jsx)(c.A,{}),label:"Chinese"})]}):"language"===t.name?(0,j.jsxs)(r.A,{value:e,onChange:e=>w(t.name,e.target.value),fullWidth:!0,children:[(0,j.jsx)(g.A,{value:"cpp",children:"C++"}),(0,j.jsx)(g.A,{value:"python",children:"Python"}),(0,j.jsx)(g.A,{value:"java",children:"Java"})]}):"extra.autoeval_extract_code_mode"===t.name?(0,j.jsxs)(r.A,{value:e,onChange:e=>w(t.name,e.target.value),fullWidth:!0,children:[(0,j.jsx)(g.A,{value:"FIRST_BLOCK_ONLY",children:"First Block Only"}),(0,j.jsx)(g.A,{value:"ALL_BLOCKS",children:"All Blocks"})]}):"extra.mode"===t.name?(0,j.jsxs)(d.A,{value:e,onChange:e=>w(t.name,e.target.value),row:!0,children:[(0,j.jsx)(p.A,{value:"input",control:(0,j.jsx)(c.A,{}),label:"input"}),(0,j.jsx)(p.A,{value:"output",control:(0,j.jsx)(c.A,{}),label:"output"})]}):null;case"text":return(0,j.jsx)(n.A,{value:e,onChange:e=>w(t.name,e.target.value),fullWidth:!0,multiline:!0,rows:3});default:return(0,j.jsx)(n.A,{value:e,onChange:e=>w(t.name,e.target.value),fullWidth:!0})}};return(0,j.jsxs)(j.Fragment,{children:[E.length>1&&(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)("header",{children:(0,j.jsx)(l.default,{as:"h2",children:"Subset Selection"})}),(0,j.jsx)(h.A,{component:"fieldset",children:(0,j.jsx)(d.A,{value:A.id,onChange:t=>{const e=t.target.value,a=E.find((t=>t.id===e))||E[0];C(a)},children:E.map((t=>(0,j.jsx)(p.A,{value:t.id,control:(0,j.jsx)(c.A,{}),label:t.id},t.id)))})})]}),(0,j.jsx)("header",{children:(0,j.jsx)(l.default,{as:"h2",children:"Configuration"})}),(0,j.jsx)(o.A,{component:m.A,sx:{mb:3},children:(0,j.jsxs)(_.A,{children:[(0,j.jsx)(v.A,{children:(0,j.jsxs)(b.A,{children:[(0,j.jsx)(x.A,{children:"Field"}),(0,j.jsx)(x.A,{children:"Value"}),(0,j.jsx)(x.A,{children:"Description"})]})}),(0,j.jsx)(F.A,{children:f.map((t=>(0,j.jsxs)(b.A,{children:[(0,j.jsx)(x.A,{children:t.name}),(0,j.jsx)(x.A,{children:k(t)}),(0,j.jsx)(x.A,{children:t.description})]},t.name)))})]})}),(0,j.jsx)("header",{children:(0,j.jsx)(l.default,{as:"h2",children:"Usage"})}),a({selectedDataset:A,datasetType:M,config:L,pythonConfig:P(L),generatePythonDict:P})]})}},27856:(t,e,a)=>{a.d(e,{A:()=>i,E:()=>s});const s={FullStackBench:{datasetType:"AutoEvalDataset",datasets:[{id:"full_stack_bench_zh",dataset:"full_stack_bench_zh",huggingFace:{id:"ByteDance/FullStackBench",subset:"zh",split:"test"}},{id:"full_stack_bench_en",dataset:"full_stack_bench_en",huggingFace:{id:"ByteDance/FullStackBench",subset:"en",split:"test"}}]},AutoEval:{datasetType:"AutoEvalDataset",datasets:[{id:"leetcode_sample_python",dataset:"leetcode_sample_python",huggingFace:{id:"sine/LeetCodeSample",subset:"python",split:"test"}}]},HumanEval:{datasetType:"HumanEvalDataset",datasets:[{id:"humaneval_python",dataset:"humaneval_python",huggingFace:{id:"openai/openai_humaneval",split:"test"}}]},MBPP:{datasetType:"MBPPDataset",datasets:[{id:"mbpp",dataset:"mbpp",huggingFace:{id:"laylarsssss/FusedMBPP",split:"test"}}]},MHPP:{datasetType:"MHPPDataset",datasets:[{id:"mhpp_140",dataset:"mhpp",huggingFace:{id:"laylarsssss/FusedMHPP",subset:"mhpp",split:"test"}},{id:"mhpp_210",dataset:"mhpp",huggingFace:{id:"laylarsssss/FusedMHPP",subset:"mhpp_210",split:"test"}}]},MiniF2F:{datasetType:"MiniF2FLean4Dataset",datasets:[{id:"minif2f_lean4_test",dataset:"minif2f_lean4_test",huggingFace:{id:"laylarsssss/FusedMHPP",split:"test"}},{id:"minif2f_lean4_valid",dataset:"minif2f_lean4_valid",huggingFace:{id:"laylarsssss/FusedMHPP",split:"test"}}]},MultipleHumanEval:{datasetType:"MultiPLEDataset",datasets:[{id:"humaneval_cpp",dataset:"multiple_cpp",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-cpp",split:"test"}},{id:"humaneval_typescript",dataset:"multiple_typescript",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-ts",split:"test"}},{id:"humaneval_bash",dataset:"multiple_bash",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-sh",split:"test"}},{id:"humaneval_csharp",dataset:"multiple_csharp",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-cs",split:"test"}},{id:"humaneval_go",dataset:"multiple_go",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-go",split:"test"}},{id:"humaneval_java",dataset:"multiple_java",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-java",split:"test"}},{id:"humaneval_lua",dataset:"multiple_lua",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-lua",split:"test"}},{id:"humaneval_javascript",dataset:"multiple_javascript",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-js",split:"test"}},{id:"humaneval_php",dataset:"multiple_php",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-php",split:"test"}},{id:"humaneval_perl",dataset:"multiple_perl",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-pl",split:"test"}},{id:"humaneval_racket",dataset:"multiple_racket",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-rkt",split:"test"}},{id:"humaneval_r",dataset:"multiple_r",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-r",split:"test"}},{id:"humaneval_rust",dataset:"multiple_rust",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-rs",split:"test"}},{id:"humaneval_scala",dataset:"multiple_scala",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-scala",split:"test"}},{id:"humaneval_swift",dataset:"multiple_swift",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-swift",split:"test"}},{id:"humaneval_ruby",dataset:"multiple_ruby",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-ruby",split:"test"}},{id:"humaneval_d",dataset:"multiple_d",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-d",split:"test"}},{id:"humaneval_julia",dataset:"multiple_julia",huggingFace:{id:"nuprl/MultiPL-E",subset:"humaneval-jl",split:"test"}}]},MultipleMBPP:{datasetType:"MultiPLEDataset",datasets:[{id:"mbpp_cpp",dataset:"multiple_cpp",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-cpp",split:"test"}},{id:"mbpp_typescript",dataset:"multiple_typescript",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-ts",split:"test"}},{id:"mbpp_bash",dataset:"multiple_bash",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-sh",split:"test"}},{id:"mbpp_csharp",dataset:"multiple_csharp",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-cs",split:"test"}},{id:"mbpp_go",dataset:"multiple_go",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-go",split:"test"}},{id:"mbpp_java",dataset:"multiple_java",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-java",split:"test"}},{id:"mbpp_lua",dataset:"multiple_lua",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-lua",split:"test"}},{id:"mbpp_javascript",dataset:"multiple_javascript",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-js",split:"test"}},{id:"mbpp_php",dataset:"multiple_php",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-php",split:"test"}},{id:"mbpp_perl",dataset:"multiple_perl",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-pl",split:"test"}},{id:"mbpp_racket",dataset:"multiple_racket",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-rkt",split:"test"}},{id:"mbpp_r",dataset:"multiple_r",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-r",split:"test"}},{id:"mbpp_rust",dataset:"multiple_rust",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-rs",split:"test"}},{id:"mbpp_scala",dataset:"multiple_scala",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-scala",split:"test"}},{id:"mbpp_swift",dataset:"multiple_swift",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-swift",split:"test"}},{id:"mbpp_ruby",dataset:"multiple_ruby",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-ruby",split:"test"}},{id:"mbpp_d",dataset:"multiple_d",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-d",split:"test"}},{id:"mbpp_julia",dataset:"multiple_julia",huggingFace:{id:"nuprl/MultiPL-E",subset:"mbpp-jl",split:"test"}}]},CommonOJ:{datasetType:"CommonOJDataset",datasets:[{id:"code_contests_train",dataset:"code_contests_train",huggingFace:{id:"sine/FusedCodeContests",split:"train"}},{id:"code_contests_valid",dataset:"code_contests_valid",huggingFace:{id:"sine/FusedCodeContests",split:"valid"}},{id:"code_contests_test",dataset:"code_contests_test",huggingFace:{id:"sine/FusedCodeContests",split:"test"}}]},CRUXEval:{datasetType:"CruxEvalDataset",datasets:[{id:"cruxeval",dataset:"cruxeval",huggingFace:{id:"cruxeval-org/cruxeval",split:"test"}}]},CRUXEvalX:{datasetType:"CruxEvalDataset",datasets:[{id:"cruxeval_x_D_ut",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"D_ut",split:"test"}},{id:"cruxeval_x_R",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"R",split:"test"}},{id:"cruxeval_x_bash",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"bash",split:"test"}},{id:"cruxeval_x_cpp",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"cpp",split:"test"}},{id:"cruxeval_x_csharp",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"csharp",split:"test"}},{id:"cruxeval_x_go_test",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"go_test",split:"test"}},{id:"cruxeval_x_java",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"java",split:"test"}},{id:"cruxeval_x_julia",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"julia",split:"test"}},{id:"cruxeval_x_lua",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"lua",split:"test"}},{id:"cruxeval_x_nodejs",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"nodejs",split:"test"}},{id:"cruxeval_x_perl",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"perl",split:"test"}},{id:"cruxeval_x_php",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"php",split:"test"}},{id:"cruxeval_x_python",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"python",split:"test"}},{id:"cruxeval_x_racket",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"racket",split:"test"}},{id:"cruxeval_x_ruby",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"ruby",split:"test"}},{id:"cruxeval_x_rust",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"rust",split:"test"}},{id:"cruxeval_x_scala",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"scala",split:"test"}},{id:"cruxeval_x_swift",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"swift",split:"test"}},{id:"cruxeval_x_typescript",dataset:"cruxeval_x",huggingFace:{id:"sine/FusedCRUXEvalX",subset:"typescript",split:"test"}}]},NaturalCodeBench:{datasetType:"NaturalCodeBenchDataset",datasets:[{id:"ncb_python_zh",dataset:"ncb_python_zh",huggingFace:{id:"sine/FusedNaturalCodeBench",subset:"python_zh",split:"test"}},{id:"ncb_python_en",dataset:"ncb_python_en",huggingFace:{id:"sine/FusedNaturalCodeBench",subset:"python_en",split:"test"}},{id:"ncb_java_zh",dataset:"ncb_java_zh",huggingFace:{id:"sine/FusedNaturalCodeBench",subset:"java_zh",split:"test"}},{id:"ncb_java_en",dataset:"ncb_java_en",huggingFace:{id:"sine/FusedNaturalCodeBench",subset:"java_en",split:"test"}}]},PALMath:{datasetType:"PalMathDataset",datasets:[{id:"asdiv",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"asdiv",split:"test"}},{id:"gsm8k",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"gsm8k",split:"test"}},{id:"hard",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"hard",split:"test"}},{id:"math",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"math",split:"test"}},{id:"mawps",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"mawps",split:"test"}},{id:"svamp",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"svamp",split:"test"}},{id:"tabmwp",dataset:"palmath",huggingFace:{id:"sine/FusedPALMath",subset:"tabmwp",split:"test"}}]},VerilogEval:{datasetType:"PalMathDataset",datasets:[{id:"verilogeval_human",dataset:"verilogeval_human",huggingFace:{id:"sine/FusedVerilogEval",subset:"human",split:"test"}},{id:"verilogeval_machine",dataset:"verilogeval_machine",huggingFace:{id:"sine/FusedVerilogEval",subset:"machine",split:"test"}}]}},i={image:"volcengine/sandbox-fusion:server-20241204",cnImage:"vemlp-cn-beijing.cr.volces.com/preset-images/code-sandbox:server-20241204",host:"http://localhost:8080",datasets:s}}}]);