config = {
    "attention_dropout": 0.0,
    "bos_token_id": 151643,
    "eos_token_id": 151643,
    "hidden_act": "silu",
    "hidden_size": 5120,
    "initializer_range": 0.02,
    "intermediate_size": 27648,
    "max_position_embeddings": 131072,
    "max_window_layers": 64,
    "model_type": "qwen2",
    "num_attention_heads": 40,
    "num_hidden_layers": 64,
    "num_key_value_heads": 8,
    "rms_norm_eps": 1e-05,
    "rope_theta": 1000000.0,
    "sliding_window": 131072,
    "torch_dtype": "bfloat16",
    "transformers_version": "4.43.1",
    "vocab_size": 152064
}


# intermediate_size是FFN的中间层大小，通常是hidden_size的4倍，hidden_size是模型的隐藏层大小，num_attention_heads是多头注意力机制的头数，num_hidden_layers是模型的层数，vocab_size是词表大小
# 我们可以看到，这个模型有64层，每层有40个attention heads，每个attention head有8个key-value heads，每个head的hidden size是5120，intermediate size是27648，vocab size是152064
def calculate_total_parameters(config):
    # 计算嵌入层参数量
    embedding_params = config['vocab_size'] * config['hidden_size']
    # 计算每层的参数量
    # 前馈网络（FFN）部分
    ffn_params = 3 * (config['hidden_size'] * config['intermediate_size'])  # 三个线性层
    # 多头注意力机制部分 Q, K, V
    attention_params = 2 * config['hidden_size'] * config['hidden_size'] * config['num_key_value_heads'] / config[
        'num_attention_heads'] + config['hidden_size'] * config['hidden_size']
    # 输出投影部分O
    output_projection_params = config['hidden_size'] * config['hidden_size']  # 输出投影
    # 每层的总参数量
    layer_params = ffn_params + attention_params + output_projection_params
    # 总参数量
    total_params = embedding_params + layer_params * config['num_hidden_layers']
    return total_params / 1e9


# 总参数量
total_params = calculate_total_parameters(config)
print(f"总参数量: {total_params:.2f} B")


def calculate_prefilling_FLOPs(config):
    ## Q投影计算量
    query_projection_flops = 2 * config['prompt_token_length'] * config['hidden_size'] ** 2
    ## K,v投影计算量
    key_projection_flops = 2 * config['prompt_token_length'] * config['hidden_size'] ** 2 * config[
        'num_key_value_heads'] / config['num_attention_heads']
    value_projection_flops = 2 * config['prompt_token_length'] * config['hidden_size'] ** 2 * config[
        'num_key_value_heads'] / config['num_attention_heads']
    ## attention计算量
    # kv 在GQA的状态下，kv的存储量变小，但是计算量不变，因为K和V会有广播
    Q_K_flops = 2 * config['prompt_token_length'] ** 2 * config['hidden_size']
    A_V_flops = 2 * config['prompt_token_length'] ** 2 * config['hidden_size']
    ## 输出投影计算量
    output_projection_flops = 2 * config['prompt_token_length'] * config['hidden_size'] ** 2

    ## 前馈网络计算量
    ## swiGLu 有三次线性变换
    ffn_flops = 3 * 2 * config['prompt_token_length'] * config['hidden_size'] * config['intermediate_size']

    layer_flops = query_projection_flops + key_projection_flops + value_projection_flops + Q_K_flops + A_V_flops + output_projection_flops + ffn_flops

    total_flops = layer_flops * config['num_hidden_layers'] * config['batch_size']
    return total_flops / 1e12


calculate_prefilling_FLOPs(config)


def calculate_prefilling_FLOPs_quick(config):
    total_flops = (4 * (1 + config['num_key_value_heads'] / config['num_attention_heads']) * config[
        'prompt_token_length'] * config['hidden_size'] ** 2
                   + 4 * config['prompt_token_length'] ** 2 * config['hidden_size']
                   + 6 * config['prompt_token_length'] *
                   config['hidden_size'] * config['intermediate_size']) * config['num_hidden_layers'] * config[
                      'batch_size']
    return total_flops / 1e12


calculate_prefilling_FLOPs_quick(config)

total_prefilling_flops = calculate_prefilling_FLOPs(config)
print(f"Prefilling阶段总计算量: {total_prefilling_flops:.2f} TFLOPs")


# Decoding阶段计算量
def calculate_decoding_FLOPs_per_token(config):
    ## Q投影计算量
    query_projection_flops = 2 * config['hidden_size'] ** 2
    ## K,v投影计算量，每次计算一个token的kv
    key_projection_flops = 2 * config['hidden_size'] ** 2 * config['num_key_value_heads'] / config[
        'num_attention_heads']
    value_projection_flops = 2 * config['hidden_size'] ** 2 * config['num_key_value_heads'] / config[
        'num_attention_heads']
    ## attention计算量
    # kv cache的状态下，KV的大小的随着step的增加而增加，从初始的prompt_token_length 到最终的prompt_token_length+output_token_length
    Q_K_flops = 2 * (config['prompt_token_length'] + (1 + config['output_token_length']) / 2) * config['hidden_size']
    A_V_flops = 2 * (config['prompt_token_length'] + (1 + config['output_token_length']) / 2) * config['hidden_size']
    ## 输出投影计算量
    output_projection_flops = 2 * config['hidden_size'] ** 2
    ## 前馈网络计算量6`12
    3458## swiGLu 有三次线性变换
    ffn_flops = 3 * 2 * config['hidden_size'] * config['intermediate_size']
    layer_flops = query_projection_flops + key_projection_flops + value_projection_flops + Q_K_flops + A_V_flops + output_projection_flops + ffn_flops
    total_flops = layer_flops * config['num_hidden_layers'] * config['batch_size']
    return total_flops / 1e12


decoding_FLOPs_per_token = calculate_decoding_FLOPs_per_token(config)
print(f"平均每个token的计算量: {decoding_FLOPs_per_token:.2f} TFLOPs")
