#! /bin/bash

task=$1
name=$2
device=$3
seed=$4
echo 'export CUDA_VISIBLE_DEVICES=0; python dynalang/train.py \
  --run.script train \
  --logdir ~/logdir/homegrid/test \
  --use_wandb True \
  --task test \
  --envs.amount 1 \
  --seed 0003 \
  --encoder.mlp_keys token$ \
  --decoder.mlp_keys token$ \
  --decoder.vector_dist onehot \
  --batch_size 16 \
  --batch_length 256 \
  --run.train_ratio 32 \
  "$@"'

export CUDA_VISIBLE_DEVICES=0; python dynalang/train.py \
  --run.script train \
  --logdir ~/logdir/homegrid/test \
  --use_wandb True \
  --task test \
  --envs.amount 1 \
  --seed 0003 \
  --encoder.mlp_keys token$ \
  --decoder.mlp_keys token$ \
  --decoder.vector_dist onehot \
  --batch_size 16 \
  --batch_length 256 \
  --run.train_ratio 32 \
  "$@"
