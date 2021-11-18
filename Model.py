import torch
import torch.nn.functional as F
from utils.model.SequenceRegressor import SequenceRegressor
from utils.audio import AudioFeatureExtractor
from utils.config_creator import get_config
from utils.rendering.model_render import ModelRender
import os
import numpy as np
from datetime import datetime
from random import randint

class AudiGestNet(object):
    """
    Class with initialze AudiGest net and uses for inference
    """
    
    #Iniciar la clase del modelo de Deep Learning
    def __init__(self) -> None:
        self.device = self.set_device()
        self.config = get_config()
        self.model = self.set_model()
        self.feature_extractor = AudioFeatureExtractor(self.config['audio'])
        self.renderer = ModelRender(config=self.config)

    def set_device(self):
        """
        Select CUDA if GPU is available, otherwise cpu
        """
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def set_model(self):
        """
        Initialize AudiGest net and load weights
        """
        model = SequenceRegressor(self.config,self.device)
        model.load(300)
        return model

    def inference(self, audio_path: str ="", face_landmarks: str = None):
        """
        Inference function
        Args:
            audio_path: String containing the file path from the audio selected in the application.
            face_landmarks: String containing the path of landmarks npy file
        """
        feature, emotion, subject, base_target = self.process_data(audio_path=audio_path,landmarks_path=face_landmarks)
        
        current_date_time = datetime.now()

        audio_name = audio_path.split("/")[-1].split(".")[0]
        video_fname = os.path.join("Videos", f'{audio_name}_{current_date_time.date()}_{current_date_time.hour}_{current_date_time.minute}_{current_date_time.second}')
        video_fname = os.path.join("Videos",audio_name)
        self.renderer.set_up(self.device,feature,emotion,subject,audio_path,"Videos",video_fname)

        self.renderer.render_sequences(self.model, base_target)
        video_fname = f'{video_fname}.wmv'
        return video_fname
    
    def process_data(self, audio_path:str = "", landmarks_path: str = None):
        subject = F.one_hot(torch.Tensor([randint(0,3)]).type(torch.int64), 4)
        emotion = F.one_hot(torch.Tensor([randint(0,7)]).type(torch.int64), 8)

        _, mfccs, melspec = self.feature_extractor.get_melspec_and_mfccs(audio_path=audio_path, use_delta=True)

        feature = melspec if self.config['model']['feature'] == "melspec" else mfccs
        feature = torch.from_numpy(feature).type(torch.float32)
        feature = feature.unsqueeze(dim=0)
        feature = feature.permute(0, 2, 1)

        base_target = np.load(landmarks_path)
        base_target = torch.from_numpy(base_target).type(torch.float32)
        base_target = base_target.repeat(feature.shape[1], 1, 1)
        base_target = base_target.unsqueeze(dim=0)

        return feature, emotion, subject, base_target
