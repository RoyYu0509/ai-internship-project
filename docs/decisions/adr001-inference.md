# ADR-001: Inference Engine 的设计

**Date**: [04-15-2026] | **Status**: Proposed

## Context
1. Inference 用 HuggingFace 中的 model() Forward Pass 来做.
2. 整个 Inference Flow 的 Structure

## Decision
### Inference Engine 在接收到 request 之后怎么跑 inference?
**✨ Final Decision**
使用 HuggingFace 的 `model(input, kv_cache)` 来进行 inference. 好处是: 我们可以手动控制 input 是什么, 然后 output 是什么.

```
outputs = model(
    input_ids=input_ids,          # shape: [batch_size, seq_len]
    past_key_values=past_kv,      # 上一步存的 KV cache，第一次是 None
    use_cache=True,               # 让它返回 KV cache
)

logits = outputs.logits           # shape: [batch_size, seq_len, vocab_size]
new_kv = outputs.past_key_values  # 传给下一步用
```

**Alternatives**
> 1. 用 HuggingFace 的 model.generate() 来做 inference.
**问题:** 它不暴露中间状态（KV cache、per-step logits），导致你无法在 Week 3/4 实现 continuous batching 和 paged KV cache。这才是 rejection reason.
**好处**: 代码量少、不需要手动管理 KV cache、不需要自己写 stopping logic、HuggingFace 已经帮你处理了 edge case.


## Inference Data Flow 的设计
**✨ Final Decision**
1. Prefill Step: 
   a. Input: TokenizedData Class
   b. 调用 model(input_ids, past_key_values=None) -> new_token_logits, new_kv
   c. 用 greedy sampling 从 new_token_logits 生成 new_token.
   d. 更新 request 的 status 从 WAITING → PREFILLING. (因为我们是从 LM Engine 的 waiting_queue 里拿到 request 的, 所以最开始的 status 是 WAITING)
   e. Output: new_token 和 new_kv

2. Decoding Step:
   a. Input: 上一步的 new_token 和 new_kv
   b. 更新 request 的 status 从 PREFILLING → DECODING. 
   c. WHILE: 调用 model(new_token, past_key_values=new_kv) -> logits, new_kv, 用 greedy sampling 从 new_token_logits 生成 new_token.
   d. 当达到最大长度 或 生成<EOS>时: Break Decoding WHILE loop.
   e. 更新 request 的 status 从 DECODING → DONE. 
   f. Output: new_token_sequence

3. KV Cache 只保留现在正在 running 的 request 的 KV Cache. 跑完一个 request 的时候, 就丢掉它的 KV Cache.
4. 生成 new_token 的时候, 用 greedy sampling, 也就是选概率最高的 token 作为 new_token, 因为这样是 deterministic的, 方便对比我们自己控制的 inference 和 model.generate() 是一致的.
5. Generating Stopping Criteria: 达到最大长度 或 生成<EOS> token.


## Consequences
1. 现在的 Inference Engine 可以处理 单个 request 的 prefill -> decoding 的完整流程, KV Cache 用完就丢, 不需要存储.
