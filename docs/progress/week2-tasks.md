# Week 2 Goal - Implement Inference Engine LM inference backend

**Description:**
The engine can load GPT-2 124M and run single-request inference end-to-end: 
> prefill → decode → generated tokens returned. 
No batching yet, no KV cache optimization yet. One request in, tokens out.


### Task 1: LM Engine Model Loading
- **What:** 可以从 Huggingface Load GPT-2 124M 模型, 并且可以进行 forward pass, 拿到 logits 和 KV cache，shape 全部正确
- **Why:** 在做 inference 之前, 先保证能 正确 load model + forward pass.
- **Accepting Criteria:** 能成功 load GPT-2 124M, 输入一个 prompt, 输出的 logits 和 KV cache shape 都正确.
- **Estimated Effort:** 2 hr


### Task 2: Implement LM Engine 的 loop
- **What:** 实现 engine 的 inference loop, input 一个 token sequence, 先进行 prefill, 再使用 while loop 进行 decode 直到满足某个停止条件. 
- **Why:** 这是 engine 的核心功能, 先实现一个最简单的 inference loop, 确保 prefill 和 decode 的流程是通的.
- **Accepting Criteria:** 在 greedy decoding 下, 输出的 token sequence 与 用 HuggingFace 的 model.generate() 跑同一个 prompt 得到的结果一致。
- **Estimated Effort:** 4 hr



### Task 3: 把 LM Engine 中的 inference 变成 async coro, 并接入现有的 Inference Engine
- **What:** 把 LMEngine.inference() method 改成 async function, 并接入现有的 Inference Engine skeleton
- **Why:** 跑通 Inference 的 data flow.
- **Accepting Criteria:** Inference Engine 启动后, 多个User同时发送requests, InferenceEngine 可以在 async 的情况下, 同时跑 RequestReceiver.fetch() 和 LMEngine.inference(), 并且生成的 token sequence 与预期一致。
- **Estimated Effort:** 3 hr


### Task 4: End-to-end test for Inference Engine
- **What:** 写一个 end-to-end 的测试, 多个 request 按顺序进入 inference engine, 能让 LM Engine 生成这些 request 的 token sequence.
- **Why:** 验证整个 inference pipeline 是通的, 包括 request intake, inference loop.
- **Accepting Criteria:** 模拟 3 个用户, 每个用户提交
-  2 个 request, 共 6 个 request. 启动 engine 后, 6 个 request 按照顺序一个一个进入 Inference Engine, 都能正确地得到生成的 token sequence 作为输出, 并且输出的 token sequence 与预期一致。
- **Estimated Effort:** 4 hr    
