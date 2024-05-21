# Run on a single GPU
deepspeed --num_gpus 1 mii-example.py

# Run on multiple GPUs
deepspeed --num_gpus 2 mii-example.py