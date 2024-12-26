#!/bin/bash

# Path to the Python script
SCRIPT_PATH="/lv0/test_aesthetics/procslib/scripts/infer_aesthetics.py"

# Directory containing the path files (<num>.parquet)
PATHS_DIR="/lv0/test_aesthetics/procslib/data/danbooru_path_chunks"

# Default arguments
# CHECKPOINT_PATH="/rmd/yada/checkpoints/aesthetics_cls_6k-mix_soft-firebrand-34/e9_acc0.8120.ckpt"
CHECKPOINT_PATH="/rmd/yada/checkpoints/aesthetics_cls_8.4k-mix-iter1_comic-spaceship-38/e7_acc=0.8889.ckpt"
PATH_COLUMN="local_path"
SAVE_DIR="/lv0/test_aesthetics/procslib/data/danbooru_results_8.4k_e7"

# Iterate over devices 0-7
for DEVICE in {0..7}; do
  # Select the corresponding file for each device
  PATHS_FILE="${PATHS_DIR}/${DEVICE}.parquet"

  if [ "$DEVICE" -eq 0 ]; then
    # Progress display for device 0
    echo "Running on CUDA_VISIBLE_DEVICES=$DEVICE with file $PATHS_FILE (progress shown)..."
    CUDA_VISIBLE_DEVICES=$DEVICE python $SCRIPT_PATH \
      --paths_file $PATHS_FILE \
      --checkpoint_path $CHECKPOINT_PATH \
      --path_column $PATH_COLUMN \
      --save_dir $SAVE_DIR &
  else
    # Run other devices in the background
    echo "Running on CUDA_VISIBLE_DEVICES=$DEVICE with file $PATHS_FILE..."
    CUDA_VISIBLE_DEVICES=$DEVICE python $SCRIPT_PATH \
      --paths_file $PATHS_FILE \
      --checkpoint_path $CHECKPOINT_PATH \
      --path_column $PATH_COLUMN \
      --save_dir $SAVE_DIR > "device_${DEVICE}_log.txt" 2>&1 &
  fi
done

# Wait for all background jobs to complete
wait
echo "All processes completed."
