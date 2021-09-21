import os
import torch
from torch.utils.data import dataset

from utils.model.AudiGest import AudiGest
from utils.model.MEADdataset import MEADDataset

from utils.config_creator import get_config
from utils.rendering.model_render import ModelRender
from utils.files.save import save_numpy


def get_last_epoch() -> int:
    checkpoints_dir = os.path.join('processed_data', 'training')
    if not os.path.exists(checkpoints_dir):
        os.makedirs(checkpoints_dir)
        print(f'No checkpoint detected.')
        return -1

    checkpoints = [int(file.split('.')[0].replace('AG_', ''))
                    for file in os.listdir(checkpoints_dir)]

    if len(checkpoints) < 1:
        print(f'No checkpoint detected.')
        return -1

    last_checkpoint = max(checkpoints)
    print(f'Detected last checkpoint at epoch {last_checkpoint}.')
    return last_checkpoint

def mse(predicted: torch.tensor, target: torch.tensor) -> float:
    return torch.square(predicted - target).mean().item()


def make_inference(model: AudiGest, device: torch.device, melspec: torch.Tensor, mfcc: torch.Tensor) -> torch.tensor:
    model = model.to(device)
    model.eval()
    hidden = None

    with torch.no_grad():
        melspec = melspec.unsqueeze(1)
        melspec = melspec.to(device)

        mfcc = mfcc.permute(0, 2, 1)
        mfcc = mfcc.to(device)

        reconstructed, _ = model(melspec, mfcc, hidden)
        return reconstructed


def main():
    config = get_config()

    #Define root and data of dataset (training or testing)
    test_data = MEADDataset(train=False, config=config)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using {device}')

    #Set up AudiGest neural network
    model = AudiGest(config)
    #Obtain last epoch of training
    last_epoch = get_last_epoch()
    #Load last epoch on AudiGest network
    model.load(last_epoch)

    #Set up configuration and dataset
    renderer = ModelRender(config=config, dataset=test_data)
    #Render the video and save from data
    renderer.render_sequences(model, device, 'output/videos')

    # melspec, mfcc, target, _, _, _ = test_data.get_sequence(0)
    # print('melspec:', melspec.shape)
    # print('mfcc:', mfcc.shape)
    # print('target:', target.shape)

    # reconstructed = make_inference(model, device, melspec, mfcc)
    # reconstructed = reconstructed.cpu()
    # print('reconstructed:', reconstructed.shape)
    # print('mse:', mse(reconstructed, target))
    
    # npy_face = reconstructed.numpy()
    # save_numpy(npy_face, 'test.npy')


if __name__ == '__main__':
    main()