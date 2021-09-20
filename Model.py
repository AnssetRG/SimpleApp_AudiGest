from librosa.feature.spectral import mfcc
import torch
import librosa
import numpy as np
from torch import nn
from torch._C import device
from torchvision import transforms, models
from PIL import Image 
import AudiGestModel as AudiGest
from utils import get_mfcc_transform, get_signal_mono, get_sliced_melspectrogram, process_framed_mfcc

class AudiGestNet(object):
    """
    Class with initialze AudiGest net and uses for inference
    """
    
    #Iniciar la clase del modelo de Deep Learning
    def __init__(self) -> None:
        self.device = self.set_device()
        self.emotions = self.set_emotions()
        self.model = self.set_model()
        self.transform = self.set_transformation()
        self.config = self.create_default_config()

        print(type(self.config))

        self.n_fft = int(self.config['audio']['window_len'] * self.config['audio']['sample_rate'])
        self.hop_len = int(self.config['audio']['sample_interval'] * self.config['audio']['sample_rate'])
        self.mfcc_transformation = get_mfcc_transform(self.config['audio']['sample_rate'], self.config['audio']['n_mfcc'], n_fft=self.n_fft, hop_len=self.hop_len)

    def set_device(self):
        """
        Select CUDA if GPU is available, otherwise cpu
        """
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def set_transformation(self):
        return transforms.Compose([
            transforms.Resize(255),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225])])
    
    def create_default_config(self):
        """
        Create a dictionary for configurations
        """
        config = {
            'audio': {
                'use_clean': True,
                'sample_rate': 16000,
                'max_samples': 16000,
                'sample_interval': 1 / 30,
                'window_len': 0.025,
                'n_mfcc': 20,
                'fps': 30
            },
            'model': {
                'lstm': {
                    'hidden_dim': 16,
                    'num_layers': 1,
                },
                'fc': {
                    'in_feat': 576,
                    'hidden_1': 256,
                    'hidden_2': 128,
                    'hidden_3': 256,
                    'hidden_4': 512,
                    'drop': 0.5
                },
                'vertex_num': 468
            }
        }

        return config

    def set_model(self):
        """
        Initialize AudiGest net and load weights
        """
        model = models.densenet121(pretrained=True)
        #model = AudiGest(self.config, self.device)
        model.to(self.device)
        model.classifier = nn.Sequential(nn.Linear(1024,512),nn.LeakyReLU(),nn.Linear(512,8))
        #TO DO: Load AudiGest Net weights
        model.load_state_dict(torch.load('SER_densenet121.pt'))
        return model

    #Labels o categorías de predicción
    def set_emotions(self):
        emotions=['angry', 'contempt', 'disgusted', 'fear', 'happy', 'neutral', 'sad', 'surprised']
        return emotions

    #Función de Inferencia/Predicción
    def prediction(self, path = ""):
        """Carga el audio desde una dirección del ordenador (path) e infiere la emoción predominante.

        Parameters
        ----------
        path : str
            Ruta del audio wav a cargar
        """
        y, sr = librosa.load(path)
        S_full, phase = librosa.magphase(librosa.stft(y))
        img=np.stack((S_full,)*3, axis=-1)
        PIL_image = Image.fromarray((img*255).astype(np.uint8))
        image=self.transform(PIL_image)
        image = image.to(self.device)
        image = image.unsqueeze_(0)
        self.model.to(self.device)
        predicted_label=np.argmax(self.model(image).detach().cpu())
        emotion_predicted = str(self.emotions[predicted_label.numpy()])        
        return emotion_predicted

    def inference(self, audio_path: str ="", face_landmarks: torch = None):
        """
        Inference function
        Args:
            audio_path: String containing the file path from the audio selected in the application.
        """

        melspectrogram, mfccs = self.process_audio(audio_path=audio_path)

        melspectrogram.to(self.device)
        mfccs.to(self.device)
        self.model.to(self.device)

        hidden = None

        #model -> [n_frames,468,3]
        predicted_landmarks, _ = self.model(melspectrogram,mfccs, hidden)

        #TO DO: llamar la función de animación

    def process_audio(self, audio_path:str = ""):
        """
        Load and audio from an string path into a torch tensor. Then, it is used for extracting the melspectrogram and mfcc of the audio according Config parameters.

        Args:
            audio_path: String containing the file path from the audio selected in the application.

        Returns:
            Audio Melspectrogram sliced tensor [n_frames, 128, 30] and MFCC framed tensor [n_frames, 20, 30]
        """
        signal = get_signal_mono(audio_path=audio_path, config=self.config)

        melspec = get_sliced_melspectrogram(signal, config=self.config, n_fft=self.n_fft, hop_len=self.hop_len)
        mfcc_list = process_framed_mfcc(signal, config=self.config, mfcc_transform=self.config)

        n_frames = len(mfcc_list)

        melspec = melspec.repeat(n_frames,1,1)
        melspec = melspec.unsqueeze(1)

        torch_mfcc = nn.FloatTensor(mfcc_list)
        torch_mfcc = torch_mfcc.permute(0, 2, 1)
        return melspec,torch_mfcc
