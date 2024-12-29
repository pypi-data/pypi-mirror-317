<h1 align="center">Mini LLM Flow</h1>

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://zachary62.github.io/miniLLMFlow/)

A [100-line](minillmflow/__init__.py) minimalist LLM framework for agents, task decomposition, RAG, etc.

- Install via  ```pip install minillmflow```, or just copy the [source](minillmflow/__init__.py) (only 100 lines)

- **Pro tip:** Build LLM apps with LLMs assistants (ChatGPT, Claude, etc.) via [this prompt](assets/prompt)

Documentation: https://zachary62.github.io/miniLLMFlow/

## Why Mini LLM Flow?

Mini LLM Flow is designed to be **the framework used by LLMs**. In the future, LLM projects will self-programmed by LLMs themselves: Users specify requirements, and LLMs will design, build, and maintain. Current LLMs:

1. **👍 Shine at Low-level Implementation:**  LLMs can handle APIs, tools, chunking, prompting, etc. These don't belong in a general-purpose framework; they're too specialized to maintain and optimize.

2. **👎 Struggle with High-level Paradigms:** Paradigms like MapReduce, task decomposition, and agents are powerful. However, designing these elegantly remains challenging for LLMs.

The ideal framework for LLMs should (1) remove specialized low-level implementations, and (2) keep high-level paradigms to program against. Hence, I built this minimal (100-line) framework so LLMs can focus on what matters.  

Mini LLM Flow is also a great learning resource, as current frameworks abstract too much away.

<div align="center">
  <img src="/assets/minillmflow.jpg" width="400"/>
</div>

## Tutorial

- Documentation: https://zachary62.github.io/miniLLMFlow/

- Beginner Tutorial: [Text summarization for Paul Graham Essay + QA agent](https://colab.research.google.com/github/zachary62/miniLLMFlow/blob/main/cookbook/demo.ipynb)

    - Have questions for this tutorial? Ask LLM assistants through [this prompt](https://chatgpt.com/share/676f16d2-7064-8000-b9d7-f6874346a6b5)
