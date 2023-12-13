MODEL_FLAGS="--image_size 256 --num_channels 128 --class_cond False --num_res_blocks 2 --num_heads 1 --learn_sigma True --use_scale_shift_norm False --attention_resolutions 16"
DIFFUSION_FLAGS="--diffusion_steps 1000 --noise_schedule linear --rescale_learned_sigmas False --rescale_timesteps False"
TRAIN_FLAGS="--lr 1e-4 --batch_size 10 --num_images 50"
CRACK_DIR="/home/neelesh/crackdiff/datasets/crack500_2/train"

CUDA_AVAILABLE_DEVICES=0,1 python scripts/segmentation_train.py --data_dir ./data/training/ $TRAIN_FLAGS $MODEL_FLAGS $DIFFUSION_FLAGS