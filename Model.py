import torch
from utils.model.AudiGest import AudiGest
from utils.audio import get_mfcc_transform, get_signal_mono, get_sliced_melspectrogram, process_framed_mfcc
from utils.config_creator import get_config
from utils.rendering.final_mondel_render import ModelRender
import os

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
        self.mfcc_transformation = get_mfcc_transform(self.config['audio']['sample_rate'], self.config['audio']['n_mfcc'], n_fft=self.n_fft, hop_len=self.hop_len)

    def set_device(self):
        """
        Select CUDA if GPU is available, otherwise cpu
        """
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def set_model(self):
        """
        Initialize AudiGest net and load weights
        """
        print(type(self.config))
        model = AudiGest(self.config)
        model.to(self.device)
        model.load(20)
        return model

    def inference(self, audio_path: str ="", face_landmarks: torch.Tensor = None):
        """
        Inference function
        Args:
            audio_path: String containing the file path from the audio selected in the application.
        """

        melspectrogram, mfccs = self.process_audio(audio_path=audio_path)

        audio_name = audio_path.split("/")[-1].split(".")[0]
        print(audio_name)
        temp_video_fname = os.path.join("Videos", f'{audio_name}.mp4')


        #Set up configuration and dataset
        renderer = ModelRender(config=self.config)
        #Render the video and save from data
        renderer.render_sequences(self.model,self.device, melspectrogram, mfccs,audio_path, "Videos")

        return temp_video_fname

    def process_audio(self, audio_path:str = ""):
        """
        Load and audio from an string path into a torch tensor. Then, it is used for extracting the melspectrogram and mfcc of the audio according Config parameters.

        Args:
            audio_path: String containing the file path from the audio selected in the application.

        Returns:
            Audio Melspectrogram sliced tensor [n_frames, 1, 128, 30] and MFCC framed tensor [n_frames, 20, 30]
        """
        signal = get_signal_mono(audio_path=audio_path, config=self.config['audio'])

        melspec = get_sliced_melspectrogram(signal, config=self.config['audio'], n_fft=self.n_fft, hop_len=self.hop_len)
        mfcc_list = process_framed_mfcc(signal, config=self.config['audio'], mfcc_transform=self.mfcc_transformation)

        n_frames = len(mfcc_list)

        melspec = melspec.repeat(n_frames,1,1)
        melspec = melspec.unsqueeze(1)

        torch_mfcc = torch.stack(mfcc_list)
        torch_mfcc = torch_mfcc.permute(0, 2, 1)
        return melspec,torch_mfcc
