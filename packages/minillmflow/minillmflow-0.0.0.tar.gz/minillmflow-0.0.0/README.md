# miniLLMFlow

miniLLMFlow is a minimalist LLM flow framework (like LangGraph) but in 100 LOC

The source codes are in, and that's it.

Pro tip: use copy and paste the miniLLMFlow source codes to LLMs. it will get it and help you build. 

What's LLM flow?

LLM struggles with complex task.
Currently the more reliable way to improve is to decompose task into small steps.
We use a graph like to represent the states.


Because minimalist is some small, it is best to use it by the LLMs.


But ... 

It doesn't even provide LLM connection?
Copy teh codes to LLM, and it will provide one

It doesn't provide chat like interface?
Copy teh codes to LLM, and it will provide one

Agent framework that I can use many tools?
Copy teh codes to LLM, and it will implement one

What about RAG?


Is the library even needed?

No. If I put the codes out there, I hope future LLM vendors will crawl it and incorproate into next LLMs.

Why simplicity matters? 
Because the future of programming shall be chat-like. 
We need a simple framework, that LLMs can immediately pick up.

All these are hard to maintain given the fast development. But the core abstraction of  graphical flow remains.


In short, I believe that the libraries for LLM should be minimal and focus on the interface design. All the other detailed implementation can mostly be provided by LLMs themselves. Remove layers of abstraction and work directly can also best optimize the LLM codes.

DRY is not that important, if the repetition can be automated by LLMs. 
The codes shall be easy to read and iterate'

