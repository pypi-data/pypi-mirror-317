import asyncio, warnings

class BaseNode:
    def __init__(self): self.params,self.successors={},{}
    def set_params(self,params): self.params=params
    def add_successor(self,node,action="default"):
        if action in self.successors: warnings.warn(f"Overwriting successor for action '{action}'")
        self.successors[action]=node;return node
    def prep(self,shared): return None
    def exec(self,prep_res): return None
    def _exec(self,prep_res): return self.exec(prep_res)
    def post(self,shared,prep_res,exec_res): return "default"
    def _run(self,shared):
        prep_res=self.prep(shared)
        exec_res=self._exec(prep_res)
        return self.post(shared,prep_res,exec_res)
    def run(self,shared):
        if self.successors: warnings.warn("Node won't run successors. Use a parent Flow instead.")
        return self._run(shared)
    def __rshift__(self,other): return self.add_successor(other)
    def __sub__(self,action):
        if isinstance(action,str): return _ConditionalTransition(self,action)
        raise TypeError("Action must be a string")

class _ConditionalTransition:
    def __init__(self,src,action): self.src,self.action=src,action
    def __rshift__(self,tgt): return self.src.add_successor(tgt,self.action)

class Node(BaseNode):
    def __init__(self,max_retries=1): 
        super().__init__()
        self.max_retries=max_retries
    def process_after_fail(self,prep_res,exc): raise exc
    def _exec(self,prep_res):
        for i in range(self.max_retries):
            try:return super()._exec(prep_res)
            except Exception as e:
                if i==self.max_retries-1:return self.process_after_fail(prep_res,e)

class BatchNode(Node):
    def prep(self,shared): return []
    def _exec(self,items): return [super(Node,self)._exec(i) for i in items]

class Flow(BaseNode):
    def __init__(self,start):
        super().__init__()
        self.start=start
    def get_next_node(self,curr,action):
        nxt=curr.successors.get(action if action is not None else "default")
        if not nxt and curr.successors: warnings.warn(f"Flow ends: action '{action}' not found in {list(curr.successors)}")
        return nxt
    def _orchestrate(self,shared,params=None):
        curr,p=self.start,(params if params else {**self.params})
        while curr:
            curr.set_params(p)
            curr=self.get_next_node(curr,curr._run(shared))
    def _run(self,shared):
        self._orchestrate(shared)
        return self.post(shared,self.prep(shared),None)
    def exec(self,prep_res): 
        raise RuntimeError("Flow should not exec directly. Create a child Node instead.")

class BatchFlow(Flow):
    def prep(self,shared): return []
    def _run(self,shared):
        prep_res=self.prep(shared)
        for batch_params in prep_res:self._orchestrate(shared,{**self.params,**batch_params})
        return self.post(shared,prep_res,None)

class AsyncNode(Node):
    def post(self,shared,prep_res,exec_res): 
        raise RuntimeError("AsyncNode should post using post_async instead.")
    async def post_async(self,shared,prep_res,exec_res):
        await asyncio.sleep(0);return "default"
    async def run_async(self,shared):
        if self.successors: 
            warnings.warn("Node won't run successors. Use a parent AsyncFlow instead.")
        return await self._run_async(shared)
    async def _run_async(self,shared):
        prep_res=self.prep(shared)
        exec_res=self._exec(prep_res)
        return await self.post_async(shared,prep_res,exec_res)
    def _run(self,shared): raise RuntimeError("AsyncNode should run using run_async instead.")

class AsyncFlow(Flow,AsyncNode):
    async def _orchestrate_async(self,shared,params=None):
        curr,p=self.start,(params if params else {**self.params})
        while curr:
            curr.set_params(p)
            c=await curr._run_async(shared) if hasattr(curr,"run_async") else curr._run(shared)
            curr=self.get_next_node(curr,c)
    async def _run_async(self,shared):
        await self._orchestrate_async(shared)
        return await self.post_async(shared,self.prep(shared),None)

class BatchAsyncFlow(BatchFlow,AsyncFlow):
    async def _run_async(self,shared):
        prep_res=self.prep(shared)
        for batch_params in prep_res:await self._orchestrate_async(shared,{**self.params,**batch_params})
        return await self.post_async(shared,prep_res,None)