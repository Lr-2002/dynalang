#! /bin/bash

task=$1
name=$2
device=$3
seed=$4

shift
shift
shift
shift

export CUDA_VISIBLE_DEVICES=$device; python dynalang/train.py \
  --run.script debug \
  --logdir ~/logdir/homegrid/$name \
  --use_wandb False\
  --task $task \
  --envs.amount 1 \
  --seed $seed \
  --encoder.mlp_keys token$ \
  --decoder.mlp_keys token$ \
  --decoder.vector_dist onehot \
  --batch_size 4 \
  --batch_length 32 \
  --run.train_ratio 8 \
  "$@"
