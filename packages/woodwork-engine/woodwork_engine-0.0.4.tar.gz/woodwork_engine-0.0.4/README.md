## AI Agents
In this project, I've thought of an AI Agent as an AI replacement for a human that can perform many tasks. For example, we've seen the rise of AI software engineers, that aim to complete the many tasks a software engineer has to carry-out.

The main issue in these agents is simulating human workflows. Using the AI software engineer agent example, if a segmentation fault occurs but it didn't previously, we can isolate the problem down to the last couple of sections of code. Currently, AI agents lack this decision making capability, however the current state-of-the-art solutions cobble together an LLM with an API and a knowledge base and expect it to just work.

The investigation of this project is to see if focus on development of the infrastructure of these AI solutions can lead to better performance. This will aim to alleviate as much hard-coding as possible, hopefully in a step towards AGI.

## The Project
Through creating an IaC tool for AI Agent workflows, I'll aim to create a general structure and workflow for similar projects. I'll aim to include an example of this workflow in use to create one of my own AI Agents.

Personally, as I have a large interest in software engineering, a lot of my time will be in designing the config file parser and infrastructure code. I'll also aim to keep up with recent research to develop a thoughtful solution.

## AI Agent Solution
### Components of an AI Agent
There seems to be a couple of main components:
1. Memory
2. Input Formatter
3. Decision Maker
4. Output Formatter
5. Functions

With 3. and 4. traditionally being merged. These components often have reinforcement learning applied to fine tune the agent.

### Agent Memory
This is typically referred to as the Knowledge Base (KB), used primarily in Retrieval Augmented Generation (RAG). This essentially allows us to use similar or relevant information to pass as to another part of the AI Agent workflow.

Typically, the problem with AI Agent performance is related to its context, assuming that modern LLMs are able to reason relatively well given the correct information. Design of this system should accomodate future developments.