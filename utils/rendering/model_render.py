import cv2
import numpy as np
import os
import tempfile
import threading

from psbody.mesh import Mesh
from scipy.io import wavfile
from subprocess import call

import torch
from utils.rendering.rendering import render_mesh_helper

class ModelRender:
    def __init__(self, config: dict):
        self.template_mesh = Mesh(filename=config['files']['face'])
        #self.template_mesh = None

    def render_sequences(self, model, device, feature_tensor, emotion_tensor, subject_tensor, audio_path, out_folder, run_in_parallel=True, video_path:str = None, landmarks: torch.tensor = None):
        #self.template_mesh = Mesh(filename=face_path)
        if run_in_parallel:
            thread = threading.Thread(target=self._render_helper, args=(model, device, feature_tensor, emotion_tensor, subject_tensor, audio_path, out_folder, landmarks, video_path))
            thread.start()
            thread.join()
        else:
            self._render_helper(model, device, feature_tensor, emotion_tensor, subject_tensor, audio_path, out_folder, landmarks, video_path)

    def _render_helper(self, model, device, feature_tensor, emotion_tensor, subject_tensor, audio_path, out_folder, landmarks: torch.tensor = None,  video_path:str = None):
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)

            video_fname = f'{video_path}.wmv'
            temp_video_fname = f'{video_path}_tmp.wmv'
            self._render_sequences_helper(model, device, video_fname, temp_video_fname, audio_path, feature_tensor, emotion_tensor, subject_tensor, landmarks)

    def _render_sequences_helper(self, model, device, video_fname, temp_video_fname, audio_path, feature_tensor, emotion_tensor, subject_tensor, base_target):
        def add_image_text(img, text):
            img = img.copy()
            font = cv2.FONT_HERSHEY_SIMPLEX
            textsize = cv2.getTextSize(text, font, 1, 2)[0]
            textX = (img.shape[1] - textsize[0]) // 2
            textY = textsize[1] + 50
            return cv2.putText(img, '%s' % (text), (textX, textY), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        num_frames = feature_tensor.shape[1]

        # tmp_video_file = tempfile.NamedTemporaryFile('w', suffix='.mp4', dir=os.path.dirname(video_fname))
        if int(cv2.__version__[0]) < 3:
            print('cv2 < 3')
            writer = cv2.VideoWriter(temp_video_fname, cv2.cv.CV_FOURCC(*'wmv2'), 30, (800, 800), True)
        else:
            print('cv2 >= 3')
            writer = cv2.VideoWriter(temp_video_fname, cv2.VideoWriter_fourcc(*'wmv2'), 30, (800, 800), True)

        model= model.to(device)
        model.eval()

        with torch.no_grad():
            # melspec = melspec.unsqueeze(1)
            feature_tensor = feature_tensor.to(device)

            # mfcc = mfcc.permute(0, 2, 1)
            emotion_tensor = emotion_tensor.to(device)

            subject_tensor = subject_tensor.to(device)

            base_target = base_target.to(device)

            reconstructed = model(feature_tensor, emotion_tensor, subject_tensor, base_target)
            reconstructed = reconstructed.squeeze(dim=0)
            reconstructed = reconstructed.cpu().numpy()

            reconstructed = self.scale_face(reconstructed)

            center = np.mean(reconstructed[0], axis=0)

            #noise = np.random.uniform(-0.001,0.001,reconstructed.shape)
            #reconstructed = reconstructed + noise

            for i_frame in range(num_frames):
                pred_img = render_mesh_helper(Mesh(reconstructed[i_frame], self.template_mesh.f))
                pred_img = add_image_text(pred_img, 'Prediction')
                writer.write(pred_img)
            writer.release()

        cmd = (f'ffmpeg -i {audio_path} -i {temp_video_fname} -codec copy -ac 2 -channel_layout stereo {video_fname}').split()
        call(cmd)
    
    def MSE(self, array_1: np.array = None, array_2: np.array = None):
        return (np.square(array_1 - array_2)).mean()
    
    def scale_face(self, reconstructed):
        reconstructed[:,:,0] *= 1.6
        #reconstructed[:,:,1] *= 0.9
        reconstructed[:,:,2] *= 1.6
        return reconstructed