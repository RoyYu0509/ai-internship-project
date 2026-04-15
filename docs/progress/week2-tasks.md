# Week 2 Goal - Implement LM Engine inference backend

**Description:**
The engine can load GPT-2 124M and run single-request inference end-to-end: 
> prefill → decode → generated tokens returned. 
No batching yet, no KV cache optimization yet. One request in, tokens out.


### Task 1: LM Engine Model Loading
- **What:** 可以从 Huggingface Load GPT-2 124M 模型, 并且可以进行 forward pass, 拿到 logits 和 KV cache，shape 全部正确
- **Why:** 在做 inference 之前, 先保证能 正确 load model + forward pass.
- **Accepting Criteria:** 能成功 load GPT-2 124M, 输入一个 prompt, 输出的 logits 和 KV cache shape 都正确.
- **Estimated Effort:** 2 hr

### Task 2: Implement Inference loop
- **What:** 实现 engine 的 inference loop, input 一个 token sequence, 先进行 prefill, 再使用 while loop 进行 decode 直到满足某个停止条件. 
- **Why:** 这是 engine 的核心功能, 先实现一个最简单的 inference loop, 确保 prefill 和 decode 的流程是通的.
- **Accepting Criteria:** 在 fixed random seed 下, 输入一个 prompt, 能得到一个确定的 token sequence 作为输出. 输出的 token sequence 与 用 HuggingFace 的 model.generate() 跑同一个 prompt 得到的结果一致。
- **Estimated Effort:** 4 hr

### Task 3: 把 Inference Engine 接入现有的 LM Engine
- **What:** 把上面实现的 inference loop 接入现有的 LM Engine skeleton, 让 Inference Engine 能从 waiting_queue 里拿 request 来跑 inference, 并把结果存回 request 里.
- **Why:** 跑通 Inference 的 data flow.
- **Accepting Criteria:** LM Engine 启动后, Inference Engine 能够从 waiting_queue 中 一个一个 request 拿出来跑 inference, 并且生成的 token sequence 与预期一致。
- **Estimated Effort:** 3 hr
  
### Task 4: End-to-end test for Inference Engine
- **What:** 写一个 end-to-end 的测试, 多个 request 按顺序进入 inference engine, 最后都能正确地得到生成的 token sequence 作为输出.
- **Why:** 验证整个 inference pipeline 是通的, 包括 request intake, inference loop.
- **Accepting Criteria:** 模拟 3 个用户, 每个用户提交 2 个 request, 共 6 个 request. 启动 engine 后, 6 个 request 按照顺序一个一个进入 Inference Engine, 都能正确地得到生成的 token sequence 作为输出, 并且输出的 token sequence 与预期一致。
- **Estimated Effort:** 4 hr    
