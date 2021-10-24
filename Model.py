from librosa.feature.spectral import mfcc
import torch
import torch.nn.functional as F
from utils.model.AudiGest import AudiGest
from utils.audio import AudioFeatureExtractor
from utils.config_creator import get_config
from utils.rendering.model_render import ModelRender
import os
import numpy as np
from datetime import datetime

class AudiGestNet(object):
    """
    Class with initialze AudiGest net and uses for inference
    """
    
    #Iniciar la clase del modelo de Deep Learning
    def __init__(self) -> None:
        self.device = self.set_device()
        self.config = get_config()
        self.model = self.set_model()

        self.n_fft = int(self.config['audio']['window_len'] * self.config['audio']['sample_rate'])
        self.hop_len = int(self.config['audio']['sample_interval'] * self.config['audio']['sample_rate'])
        self.feature_extractor = AudioFeatureExtractor(self.config['audio'])

    def set_device(self):
        """
        Select CUDA if GPU is available, otherwise cpu
        """
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def set_model(self):
        """
        Initialize AudiGest net and load weights
        """
        model = AudiGest(self.config)
        model.to(self.device)
        model.load(20)
        return model

    def inference(self, audio_path: str ="", face_obj: str = None, face_landmarks: str = None):
        """
        Inference function
        Args:
            audio_path: String containing the file path from the audio selected in the application.
        """
        melspectrogram, mfccs, base_target = self.process_audio(audio_path=audio_path, landmarks_path=face_landmarks)

        current_date_time = datetime.now()

        audio_name = audio_path.split("/")[-1].split(".")[0]
        video_fname = os.path.join("Videos", f'{audio_name}_{current_date_time.date()}_{current_date_time.hour}_{current_date_time.minute}_{current_date_time.second}')


        #Set up configuration and dataset
        renderer = ModelRender(config=self.config)
        #Render the video and save from data
        renderer.render_sequences(self.model,self.device, melspectrogram, mfccs,audio_path, "Videos", video_path=video_fname, landmarks=base_target)
        video_fname = f'{video_fname}.wmv'
        return video_fname

    def process_audio(self, audio_path:str = "", landmarks_path: str = None):
        """
        Load and audio from an string path into a torch tensor. Then, it is used for extracting the melspectrogram and mfcc of the audio according Config parameters.

        Args:
            audio_path: String containing the file path from the audio selected in the application.

        Returns:
            Audio Melspectrogram sliced tensor [n_frames, 1, 128, 30] and MFCC framed tensor [n_frames, 20, 30]
        """

        _, mfcc = self.feature_extractor.get_melspec_and_mfccs(audio_path=audio_path,use_delta=True)
        mfcc_list = self.feature_extractor.process_framed_mfcc(mfcc, use_delta=True)

        n_frames = mfcc_list.shape[0]

        #melspec = melspec.repeat(n_frames,1,1)
        #melspec = melspec.unsqueeze(1)
        melspec = torch.tensor(3)
        melspec = melspec.repeat(n_frames)
        melspec = F.one_hot(melspec,8)

        torch_mfcc = torch.from_numpy(mfcc_list).type(torch.float32)
        torch_mfcc = torch_mfcc.permute(0, 2, 1)

        base_target = np.load(landmarks_path)
        base_target = torch.from_numpy(base_target).type(torch.float32)
        base_target = base_target.repeat(n_frames, 1, 1)

        #raise Exception("STOP >:v")

        return melspec,torch_mfcc,base_target
