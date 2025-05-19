CUDA_VISIBLE_DEVICES=0 \
swift deploy \
    --adapters qwen2.5_hot_mus_sft \
    --infer_backend vllm \
    --temperature 0 \
    --max_new_tokens 16384 \
    --port 8005 \
