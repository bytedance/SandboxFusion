"use strict";(self.webpackChunksandbox_fusion=self.webpackChunksandbox_fusion||[]).push([[3418],{59828:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>c,contentTitle:()=>l,default:()=>m,frontMatter:()=>i,metadata:()=>r,snippet1:()=>u,snippet2:()=>p,toc:()=>h});var s=t(74848),o=t(28453),d=t(27856),a=t(52138);const i={sidebar_position:1},l="Upload & Download Files",r={id:"docs/how-to/run-code/upload-download-files",title:"Upload & Download Files",description:"Both the runcode and runjupyter interfaces support two file-related parameters:",source:"@site/docs/docs/how-to/run-code/upload-download-files.mdx",sourceDirName:"docs/how-to/run-code",slug:"/docs/how-to/run-code/upload-download-files",permalink:"/SandboxFusion/docs/docs/how-to/run-code/upload-download-files",draft:!1,unlisted:!1,editUrl:"https://github.com/bytedance/SandboxFusion/tree/main/docs/docs/docs/how-to/run-code/upload-download-files.mdx",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"docSidebar",previous:{title:"Run Code",permalink:"/SandboxFusion/docs/category/run-code"},next:{title:"Jupyter Mode",permalink:"/SandboxFusion/docs/docs/how-to/run-code/jupyter-mode"}},c={},u=String.raw`import json
import base64
import requests

with open('flag.txt', 'rb') as f:
    content = f.read()
base64_content = base64.b64encode(content).decode('utf-8')

response = requests.post('${d.A.host}/run_code', json={
    'code': 'print(open("flag.txt").read())',
    'language': 'python',
    'files': {'flag.txt': base64_content}
})

print(json.dumps(response.json(), indent=2))
`,p=String.raw`import json
import base64
import requests

response = requests.post('${d.A.host}/run_code', json={
    'code': 'open("flag.txt", "w").write("this is a secret")',
    'language': 'python',
    'fetch_files': ['flag.txt']
})

print(json.dumps(response.json(), indent=2))
print(base64.b64decode(response.json()['files']['flag.txt']).decode('utf-8'))
`,h=[{value:"Upload",id:"upload",level:2},{value:"Download",id:"download",level:2}];function f(e){const n={code:"code",h1:"h1",h2:"h2",header:"header",li:"li",p:"p",pre:"pre",ul:"ul",...(0,o.R)(),...e.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(n.header,{children:(0,s.jsx)(n.h1,{id:"upload--download-files",children:"Upload & Download Files"})}),"\n",(0,s.jsx)(n.p,{children:"Both the run_code and run_jupyter interfaces support two file-related parameters:"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:"files: A dictionary of files to be uploaded before code execution, mapping file paths to file contents in base64 format"}),"\n",(0,s.jsx)(n.li,{children:"fetch_files: A list of file paths to be retrieved after code execution"}),"\n"]}),"\n",(0,s.jsx)(n.p,{children:"Since the usage of these parameters is identical, we'll use the run_code interface as an example to demonstrate file upload and download."}),"\n",(0,s.jsx)(n.h2,{id:"upload",children:"Upload"}),"\n","\n",(0,s.jsx)(a.default,{language:"python",children:u}),"\n",(0,s.jsx)(n.p,{children:"Output:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-json",children:'{\n  "status": "Success",\n  "message": "",\n  "compile_result": null,\n  "run_result": {\n    "status": "Finished",\n    "execution_time": 0.018889427185058594,\n    "return_code": 0,\n    "stdout": "secret flag\\n",\n    "stderr": ""\n  },\n  "executor_pod_name": null,\n  "files": {}\n}\n'})}),"\n",(0,s.jsx)(n.p,{children:"File paths are relative to the script's directory (a randomly generated /tmp/tmpxxxx) by default. You can also specify absolute paths like /tmp/flag.txt. If the specified path doesn't exist, the corresponding folder will be created first."}),"\n",(0,s.jsx)(n.h2,{id:"download",children:"Download"}),"\n","\n",(0,s.jsx)(a.default,{language:"python",children:p}),"\n",(0,s.jsx)(n.p,{children:"Output:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-json",children:'{\n  "status": "Success",\n  "message": "",\n  "compile_result": null,\n  "run_result": {\n    "status": "Finished",\n    "execution_time": 0.023561477661132812,\n    "return_code": 0,\n    "stdout": "",\n    "stderr": ""\n  },\n  "executor_pod_name": null,\n  "files": {\n    "flag.txt": "dGhpcyBpcyBhIHNlY3JldA=="\n  }\n}\nthis is a secret\n'})}),"\n",(0,s.jsx)(n.p,{children:"The rules for file paths are the same as in the upload section."})]})}function m(e={}){const{wrapper:n}={...(0,o.R)(),...e.components};return n?(0,s.jsx)(n,{...e,children:(0,s.jsx)(f,{...e})}):f(e)}},27856:(e,n,t)=>{t.d(n,{A:()=>s});const s={image:"vemlp-cn-beijing.cr.volces.com/preset-images/code-sandbox:opensource_20241022",host:"http://localhost:8080",datasets:{AutoEval:{datasets:[{id:"leetcode_sample_python",huggingFace:{id:"sine/LeetCodeSample",subset:"python",split:"test"}}]},HumanEval:{datasets:[{id:"humaneval_python",huggingFace:{id:"sine/FusedHumanEvalPython",split:"test"}}]},CommonOJ:{datasets:[{id:"code_contests_train",huggingFace:{id:"sine/FusedCodeContests",split:"train"}},{id:"code_contests_valid",huggingFace:{id:"sine/FusedCodeContests",split:"valid"}},{id:"code_contests_test",huggingFace:{id:"sine/FusedCodeContests",split:"test"}}]}}}}}]);