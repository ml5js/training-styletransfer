#! /bin/bash

python style.py --style images/matildeperez.jpg \
  --checkpoint-dir checkpoints/ \
  --test images/violetaparra.jpg \
  --test-dir tests/ \
  --content-weight 1.5e1 \
  --checkpoint-iterations 1000 \
  --batch-size 20