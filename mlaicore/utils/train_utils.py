import torch as T
import os

class TrainUtils:
    def __init__(self):
        pass
    # Function to save a checkpoint
    def save_checkpoint(epoch, model, optimizer, loss, checkpoint_path):
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss
        }
        T.save(checkpoint, checkpoint_path)
        print(f"Checkpoint saved at epoch {epoch} to {checkpoint_path}")
        
    # Function to load a checkpoint
    def load_checkpoint(checkpoint_path, model, optimizer):
        if os.path.exists(checkpoint_path):
            checkpoint = T.load(checkpoint_path)
            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            start_epoch = checkpoint['epoch'] + 1
            print(f"Checkpoint loaded from {checkpoint_path}, resuming from epoch {start_epoch}")
            return start_epoch
        else:
            print(f"No checkpoint found at {checkpoint_path}, starting from scratch")
            return 0
