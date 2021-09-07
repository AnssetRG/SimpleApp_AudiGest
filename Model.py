import torch
import librosa
import numpy as np
from torch import nn
from torchvision import transforms, models
from PIL import Image 

class AudiGestNet(object):
    """
    Clase para la implementación y uso del modelo de Deep Learning AudiGest

    Methods
    -------
    prediction(path=None)
        Predecir la emoción de un audio y devolver la inferencia
    """
    
    #Iniciar la clase del modelo de Deep Learning
    def __init__(self) -> None:
        self.device = None
        self.model = None
        self.transform = None
        self.emotions = None

        self.device = self.set_device()
        self.transform = self.set_transformation()
        self.model = self.set_model()
        self.emotions = self.set_emotions()

    #Seleccionar procesador para realizar las operaciones, si está disponible una GPU se usará esta
    def set_device(self):
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    #Transformación de imágenes
    def set_transformation(self):
        return transforms.Compose([
            transforms.Resize(255),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225])])

    #Inicialización del modelo pre-entrenado
    def set_model(self):
        model = models.densenet121(pretrained=True)
        model.to(self.device)
        model.classifier = nn.Sequential(nn.Linear(1024,512),nn.LeakyReLU(),nn.Linear(512,8))
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
        print(emotion_predicted)
        return emotion_predicted

if __name__ == '__main__':
    hola = AudiGestNet()
    
    hola.prediction('Audios/contempt.wav')


