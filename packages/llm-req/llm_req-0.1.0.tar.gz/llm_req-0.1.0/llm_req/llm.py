import requests, aiohttp
from typing import List,Any, Optional, Dict
from .struct import ChatMessage, ChatCompletionResponse, ChatCompletionRequest, ChatCompletionResponseStreamChoice, MachineInfo,ClearRequest
from .tool import get_tools,dispatch_tool
import json
from abc import ABC
import logging
import sys
import os
from loguru import logger

import warnings
warnings.filterwarnings("ignore", message=".*certificate verification.*")

try:
    from .code import get_kernel, execute, extract_code
except:
    print("can not import code interpreter, may be jupyter_client ipykernel and Image not installed")
# from termcolor import cprint, colored

class LLM:
    """
            Load a model from local or remote
        if want to use stream mode:
            'streaming=True'
        if want to use langchain's Callback:
            examples: 'callbacks=[StreamingStdOutCallbackHandler(), AsyncWebsocketHandler()]'

        if want use cpu: # default will try to use gpu
            'cpu=True'
        
        if want to use remote's model:
            'remote_host="xx.xxx.xx.xx"'  , if set this , will auto call by ws://xx.xxx.xxx.xx:15000"
            optional:
                remote_callback: a callback function, will call when receive a new token like  'callback(new_token, history, response)'
                if not set, will print to stdout

    """
    id: str = "Hammer2.1-7b"
    max_tokens: int = 50000
    temperature: float = 0.01
    top_p = 0.9
    history :List[ChatMessage] = []
    history_id = "default"
    tokenizer: Any = None
    model: Any = None
    history_len: int = 10
    use_https: bool = False
    model: Any = None
    tokenizer: Any = None
    cpu: bool = False
    streaming: bool = False
    system:str = "You are ChatGLM3, a helpful assistant. Follow the user's instructions carefully. Respond using markdown."
    verbose: bool = False
    
    remote_host: Any = None
    functions: Optional[Dict]
    cache:Optional[bool] = True

    def __init__(self, remote_host: str, use_tools=False, use_code=False):
        self.remote_host = remote_host
        self.use_code = False
        self.functions = None
        if remote_host.startswith("https"):
            self.use_https = True
        else:
            self.use_https = False
        if remote_host.startswith("http"):
            self.remote_host = remote_host.split("://")[1].strip()

        if use_tools:
            self.functions = get_tools()
            self.id = self.id.replace("-128k", "").replace("-32k","")
        if use_code:
            self.functions = None
            self.use_code = use_code

        # self.functions = get_tools()
        self.token = ""
        self._schema = "https" if self.use_https else "http"
        
    def set_history(self, hist:List[str]):
        self.history = hist
    
    def copy_llm(self):
        ee =  LLM(
            remote_host= self.remote_host
        )
        ee._schema = self._schema
        ee.history = self.history.copy()
        return ee
    
    def load_tools(self, name):
        fus = get_tools()
        if name in fus:
            if self.functions is None:
                self.functions = {
                    name: fus[name]
                }
            else:
                self.functions[name]= fus[name]
    

    @property
    def _llm_type(self) -> str:
        return "ChatGLM"

    def info(self):
        url = f"{self._schema}://{self.remote_host}/v1/device/info"
        m = MachineInfo()
        data = m.json()
        response = requests.post(url, json=data)
        return response.json()
    
    def clear_history(self):
        self.history = []
        return self
    
    def clear_model(self,id):
        # /v1/models/clear
        url = f"{self._schema}://{self.remote_host}/v1/models/clear"
        m = ClearRequest(id=id)
        data = m.json()
        response = requests.post(url, json=data)
        return response.json()
    
    
    def add_hist(self,prompt=None, role="user",content=None,name=None):
        if prompt:
            self.history.append(ChatMessage(role="user", content=prompt))
        
        if content:
            if  not isinstance(content, str) and isinstance(content, dict):
                content = json.dumps(content)
            else:
                self.history.append(ChatMessage(role=role, content=content, name=name))
    
    def __call__(self, prompt):
        for i in self.stream(prompt):
            yield i

    def as_json(self):
        if "```json\n" in self.history[-1].content:
            return json.loads(self.history[-1].content.split("```json\n")[1].split("```")[0])
    
    def as_code(self):
        if "```python\n" in self.history[-1].content:
            return self.history[-1].content.split("```python\n")[1].split("```")[0]

    def as_shell(self):
        if "```bash\n" in self.history[-1].content:
            return self.history[-1].content.split("```bash\n")[1].split("```")[0]
    
    
    # wrrite use slef << some  magic method
    def out(self,prompt, out=sys.stdout):
        for i in self(prompt):
            print(i["new"], end="", file=out, flush=True)
    
    def __lshift__(self, prompt):
        return self.out(prompt)

    
    def stream(self,prompt: str):
        uri = f"{self._schema}://{self.remote_host}/v1/chat/completions"
        result = ''
        if self.functions is None or len(self.functions) == 0:
            if self.use_code:
                info = {
                    "home": os.environ.get("HOME"),
                    "platform" : sys.platform,
                    "pwd" : os.environ.get("PWD"),
                }
                home = os.environ.get("HOME")
                msgs = [
                    ChatMessage(role="system", content=f"你是一位智能AI助手，你叫ChatGLM4，你连接着一台电脑，但请注意不能联网。在使用Python解决任务时，你可以运行代码并得到结果，如果运行结果有错误，你需要尽可能对代码进行改进。你可以处理用户上传到电脑上的文件，文件默认存储路径是{home}，这台电脑的用户信息: {info}。"),
                ]
            else:
            
                msgs = [
                    ChatMessage(role="system", content=self.system)
                ]
        
            
        else:
            msgs = [
                # ChatMessage(role="system", content=self.system)
            ]
            # info = {
            #     "home": os.environ.get("HOME"),
            #     "platform" : sys.platform,
            #     "pwd" : os.environ.get("PWD"),
            # }

            # msgs = [
            #     ChatMessage(role="system", content=f"Answer the following questions as best as you can.local machine's info: {info}\n.You have access to the following tools:", tools=self.functions),
            # ]
            pass
        for h in self.history:
            if isinstance(h, ChatMessage):
                msgs.append(h)
            else:
                role,hist_prompt,response_msg = h
                if role == "user":
                    msgs.append(ChatMessage(role="user", content=hist_prompt.strip()))
                    msgs.append(ChatMessage(role="assistant", content=response_msg.strip()))
        
        msgs.append(ChatMessage(role="user", content=prompt,tools=self.functions))

        gen = self.create_chat_completion(uri, msgs, temperature=self.temperature, max_tokens=self.max_tokens, top_p=self.top_p, functions=self.functions, model=self.id)
        ss = ""
        role = ""
        function_replys = []
        for r in gen:
            for choice in r.choices:
                if choice.finish_reason == "stop":
                    self.add_hist(prompt=prompt, content=result, role=role)
                    break
                elif choice.finish_reason == "function_call":
                    
                    # print(choice)
                    # import ipdb;ipdb.set_trace()
                    if "interpreter" in ss and "```python":
                        try:
                            code = extract_code(ss)

                            if code:
                                kernel = get_kernel()
                                res_type , res = execute(code, kernel)
                                # import ipdb;ipdb.set_trace()
                                
                                if res_type == 'text' and len(res) > self.max_tokens:
                                    res = res[:self.max_tokens] + ' [TRUNCATED]'
                                if res_type is None:
                                    print("rest err to replys")
                                    function_replys.append(("interpreter", res))
                                    self.add_hist(role="observation", content=res)
                                elif res_type == "text":
                                    function_replys.append(("interpreter", res))
                                    self.add_hist(role="observation", content=res)

                                else:
                                    print(res)
                                print("Code Type:",res_type)
                                print("Code Result:","\n",res)
                            
                        except Exception as e:
                            logging.error(f"[chatglm +222]call func err:{e} {ss}")
                            pass
                    else:
                        if choice.delta.tool_calls:
                            for function_call in choice.delta.tool_calls:
                                # logger.info(f"function_call: {function_call}")
                                function_args = json.loads(function_call['function']['arguments'])
                                
                                try:
                                    
                                    
                                    logger.info("-------------------- call ------------------------------")
                                    function_res = dispatch_tool(function_call['function']['name'], function_args)
                                    logger.info(function_res)
                                    function_replys.append((function_call['function']['name'], function_res))
                                    self.add_hist(role="observation", content=function_res)
                                except Exception as e:
                                    logging.error(f"[chatglm +235]call func err:{e} {function_call}")
                                # break

                if choice.delta.content is not None:
                    msg = {}
                    # yield choice.delta
                    role = choice.delta.role
                    msg["new"] = choice.delta.content
                    ss += choice.delta.content
                    msg["response"] = ss
                    msg["verbose"] = self.verbose
                    result = ss
                    yield msg
                # ss = ""
        
        
        # self.history = self.history+[[prompt, result]]

        while len(function_replys) > 0:
            func_name, func_res = function_replys.pop()
            msgs.append(ChatMessage(role="observation", content=func_res, name=func_name))
            ss = ""
            for r in self.create_chat_completion(uri, msgs, temperature=self.temperature, max_tokens=self.max_tokens, top_p=self.top_p, functions=self.functions, model=self.id):
                for choice in r.choices:
                    if choice.finish_reason == "stop":
                        self.add_hist(content=result, role=role)
                        break
                    elif choice.finish_reason == "function_call":

                        
                        if "interpreter" in ss and "```python" in ss:
                            # try:
                            code = extract_code(ss)

                            if code:
                                kernel = get_kernel()
                                result = execute(code, kernel)
                                # print("resilt: ", result)
                                # import ipdb;ipdb.set_trace()
                                res_type , res = result
                                # import ipdb;ipdb.set_trace()
                                
                                if res_type == 'text' and len(res) > self.max_tokens:
                                    res = res[:self.max_tokens] + ' [TRUNCATED]'

                                if res_type is None:
                                    function_replys.append(("interpreter", res))
                                    self.add_hist(role="observation", content=res)
                                elif res_type == "text":
                                    function_replys.append(("interpreter", res))
                                    self.add_hist(role="observation", content=res)
                                elif res_type == "error":
                                    function_replys.append(("interpreter", str(res)))
                                else:
                                    print(res)
                                print("Code Type:",res_type)
                                print("Code Result:","\n",res)
                                
                            # except Exception as e:
                            #     logging.error(f"[chatglm +286]call func err:{e}")
                            #     pass
                        else:
                            function_call = choice.delta.function_call
                            try:
                                function_args = json.loads(function_call.arguments)
                                print(choice.dict())
                                print("-------------------- call ------------------------------")

                                function_res = dispatch_tool(function_call.name, function_args)
                                print(function_res)
                                function_replys.append((function_call.name, function_res))
                                logging.info(f"Tool Call Response: {ss}")
                                self.add_hist(role="observation", content=function_res)

                            except Exception as e:
                                logging.error(f"[chatglm +302]call func err:{e}")
                            break

                    if choice.delta.content is not None:
                        msg = {}
                        # yield choice.delta
                        role = choice.delta.role
                        msg["new"] = choice.delta.content
                        ss += choice.delta.content
                        msg["response"] = ss
                        msg["verbose"] = self.verbose
                        result = ss
                        yield msg
                        # ss = ""
         


    def create_chat_completion(self, url, messages:List[ChatMessage], functions=None, use_stream=True,model="chatglm3-6b-32k",temperature=0.8,top_p=0.8, max_tokens=8000):
        req = ChatCompletionRequest(
            model=model, 
            functions=functions,
            tools=list(functions.values()) if functions else None, 
            messages=messages,
            top_p=top_p,
            temperature=temperature,
            stream=use_stream,
            max_tokens=max_tokens,
        )
        data = req.dict()
        # token=self.token
        # print(data["tools"])
        headers = {
            # "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=data,headers=headers,verify=False, stream=use_stream, timeout=1000)
        if response.status_code == 200:
            if use_stream:
                # 处理流式响应
                
                for line in response.iter_lines():
                    if line:
                        
                        decoded_line = line.decode('utf-8')[6:]
                        try:
                            if decoded_line.strip():
                                response_json = json.loads(decoded_line.strip())
                                
                                c = ChatCompletionResponse.from_dict(response_json)
                                # import ipdb;ipdb.set_trace()
                                if c.choices[-1].finish_reason == "stop":
                                    yield c
                                    break
                                elif c.choices[-1].finish_reason == "function_call":
                                    yield c
                                    break
                                
                                yield c
                                
                        except Exception as e:
                            # cprint(decoded_line,'red')
                            
                            # raise e
                            pass
            else:
                # 处理非流式响应
                decoded_line = response.json()
                # content = decoded_line.get("choices", [{}])[0].get("message", "").get("content", "")
                yield ChatCompletionResponse.parse_obj(decoded_line)
        else:
            print("Error:", response.status_code, url, response.content)
            return None

    async def acreate_chat_completion(self, url, messages:List[ChatMessage], functions=None, use_stream=True,model="chatglm3-6b-128k",temperature=0.8,top_p=0.8, max_tokens=8000):
        req = ChatCompletionRequest(
            model=model, 
            functions=functions,
            messages=messages,
            top_p=top_p,
            temperature=temperature,
            stream=use_stream,
            max_tokens=max_tokens,
        )
        data = req.dict()
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
        
                if response.status == 200:
                    if use_stream:
                        # 处理流式响应
                        # import ipdb;ipdb.set_trace()
                        while 1:
                            try:
                                line = await response.content.readline()
                                if line:
                                    decoded_line = line.decode('utf-8')[6:]
                                    try:
                                        if decoded_line.strip():
                                            response_json = json.loads(decoded_line.strip())
                                            # content = response_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                            c = ChatCompletionResponse.parse_obj(response_json)
                                            
                                            if c.choices[-1].finish_reason == "stop":
                                                yield c
                                                break
                                            elif c.choices[-1].finish_reason == "function_call":
                                                yield c
                                                break
                                            yield c
                                            
                                            
                                    except:
                                        # print("Special Token:", decoded_line)
                                        pass
                            except EOFError:
                                break
                        
                            
                    else:
                        # 处理非流式响应
                        decoded_line = response.json()
                        # content = decoded_line.get("choices", [{}])[0].get("message", "").get("content", "")
                        yield ChatCompletionResponse.parse_obj(decoded_line)
                else:
                    print("Error:", response.status)
                