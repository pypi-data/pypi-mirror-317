import asyncio, warnings

class BaseNode:
    def __init__(self): self.params, self.successors = {}, {}
    def set_params(self, params): self.params = params
    def add_successor(self, node, cond="default"):
        if cond in self.successors: warnings.warn(f"Overwriting existing successor for '{cond}'")
        self.successors[cond] = node; return node
    def prep(self, shared): return None
    def exec(self, shared, prep_res): return None
    def _exec(self, shared, prep_res): return self.exec(shared, prep_res)
    def post(self, shared, prep_res, exec_res): return "default"
    def _run(self, shared):
        prep_res = self.prep(shared); exec_res = self._exec(shared, prep_res)
        return self.post(shared, prep_res, exec_res)
    def run(self, shared):
        if self.successors: warnings.warn("This node has successors. Create a parent Flow instead to run them.")
        return self._run(shared)
    def __rshift__(self, other): return self.add_successor(other)
    def __sub__(self, cond):
        if isinstance(cond, str): return _ConditionalTransition(self, cond)
        raise TypeError("Condition must be a string")

class _ConditionalTransition:
    def __init__(self, src, cond): self.src, self.cond = src, cond
    def __rshift__(self, tgt): return self.src.add_successor(tgt, self.cond)

class Node(BaseNode):
    def __init__(self, max_retries=1): super().__init__(); self.max_retries = max_retries
    def process_after_fail(self, shared, prep_res, exc): raise exc
    def _exec(self, shared, prep_res):
        for i in range(self.max_retries):
            try: return super()._exec(shared, prep_res)
            except Exception as e:
                if i == self.max_retries - 1: return self.process_after_fail(shared, prep_res, e)

class BatchNode(Node):
    def prep(self, shared): return []
    def exec(self, shared, item): return None
    def _exec(self, shared, items): return [super(Node, self)._exec(shared, i) for i in items]

class BaseFlow(BaseNode):
    def __init__(self, start_node): super().__init__(); self.start_node = start_node
    def get_next_node(self, curr, cond):
        nxt = curr.successors.get(cond)
        if nxt is None and curr.successors: warnings.warn(f"Flow ends. '{cond}' not among {list(curr.successors.keys())}")
        return nxt

class Flow(BaseFlow):
    def _exec(self, shared, params=None):
        curr, p = self.start_node, (params if params else self.params.copy())
        while curr:
            curr.set_params(p); c = curr._run(shared)
            curr = self.get_next_node(curr, c)
    def exec(self, shared, prep_res): raise NotImplementedError

class BaseBatchFlow(BaseFlow):
    def prep(self, shared): return []

class BatchFlow(BaseBatchFlow, Flow):
    def _run(self, shared):
        prep_res = self.prep(shared)
        for batch_params in prep_res:
            flow_params = self.params.copy(); flow_params.update(batch_params)
            self._exec(shared, flow_params)
        return self.post(shared, prep_res, None)

class AsyncNode(Node):
    def post(self, shared, prep_res, exec_res): raise NotImplementedError("Use post_async")
    async def post_async(self, shared, prep_res, exec_res): await asyncio.sleep(0); return "default"
    async def run_async(self, shared):
        if self.successors: warnings.warn("This node has successors. Create a parent AsyncFlow instead to run them.")
        return await self._run_async(shared)
    async def _run_async(self, shared):
        prep_res = self.prep(shared); exec_res = self._exec(shared, prep_res)
        return await self.post_async(shared, prep_res, exec_res)
    def _run(self, shared): raise RuntimeError("AsyncNode requires async execution. Use run_async instead.")

class AsyncFlow(BaseFlow, AsyncNode):
    async def _exec_async(self, shared, params=None):
        curr, p = self.start_node, (params if params else self.params.copy())
        while curr:
            curr.set_params(p)
            c = await curr._run_async(shared) if hasattr(curr, "run_async") else curr._run(shared)
            curr = self.get_next_node(curr, c)
    async def _run_async(self, shared):
        prep_res = self.prep(shared)
        await self._exec_async(shared)
        return await self.post_async(shared, prep_res, None)

class BatchAsyncFlow(BaseBatchFlow, AsyncFlow):
    async def _run_async(self, shared):
        prep_res = self.prep(shared)
        for batch_params in prep_res:
            flow_params = self.params.copy(); flow_params.update(batch_params)
            await self._exec_async(shared, flow_params)
        return await self.post_async(shared, prep_res, None)