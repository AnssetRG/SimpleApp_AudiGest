import cv2
import numpy as np
import os
import threading

from psbody.mesh import Mesh
from subprocess import call

import torch
from utils.rendering.rendering import render_mesh_helper

class ModelRender:
    def __init__(self, config: dict):
        self.template_mesh = Mesh(filename=config['files']['face'])
        self.set_up()
    
    def set_up(self, device=None, feature_tensor=None, emotion_tensor=None, subject_tensor=None, audio_path=None, out_folder=None, video_path=None):
        self.device = device
        self.feature_tensor = feature_tensor
        self.emotion_tensor = emotion_tensor
        self.subject_tensor = subject_tensor
        self.audio_path = audio_path
        self.out_folder = out_folder
        self.video_path = video_path

    def render_sequences(self, model, landmarks: torch.tensor = None, run_in_parallel=True,):
        if run_in_parallel:
            thread = threading.Thread(target=self._render_helper, args=(model, landmarks))
            thread.start()
            thread.join()
        else:
            self._render_helper(model, landmarks)

    def _render_helper(self, model, landmarks: torch.tensor = None):
            if not os.path.exists(self.out_folder):
                os.makedirs(self.out_folder)

            video_fname = f'{self.video_path}.wmv'
            temp_video_fname = f'{self.video_path}_tmp.wmv'
            self._render_sequences_helper(model, video_fname, temp_video_fname, landmarks)

    def _render_sequences_helper(self, model, video_fname, temp_video_fname, base_target):
        num_frames = self.feature_tensor.shape[1]

        if int(cv2.__version__[0]) < 3:
            print('cv2 < 3')
            writer = cv2.VideoWriter(temp_video_fname, cv2.cv.CV_FOURCC(*'wmv2'), 30, (800, 800), True)
        else:
            print('cv2 >= 3')
            writer = cv2.VideoWriter(temp_video_fname, cv2.VideoWriter_fourcc(*'wmv2'), 30, (800, 800), True)

        model= model.to(self.device)
        model.eval()

        with torch.no_grad():
            feature_tensor = self.feature_tensor.to(self.device)

            emotion_tensor = self.emotion_tensor.to(self.device)

            subject_tensor = self.subject_tensor.to(self.device)

            base_target = base_target.to(self.device)

            reconstructed = model(feature_tensor, emotion_tensor, subject_tensor, base_target)
            reconstructed = reconstructed.squeeze(dim=0)
            reconstructed = reconstructed.cpu().numpy()

            reconstructed = self.scale_face(reconstructed)

            for i_frame in range(num_frames):
                pred_img = render_mesh_helper(Mesh(reconstructed[i_frame], self.template_mesh.f))
                writer.write(pred_img)
            writer.release()

        cmd = (f'ffmpeg -i {self.audio_path} -i {temp_video_fname} -codec copy -ac 2 -channel_layout stereo {video_fname}').split()
        call(cmd)
        #mp4_name = f'{video_fname.split(".")[0]}.mp4'
        #cmd = (f'ffmpeg -i {video_fname} -c:v libx264 -crf 23 -c:a aac -q:a 100 {mp4_name}').split()
        #call(cmd)
        self.set_up()
        if os.path.exists(temp_video_fname):
            os.remove(temp_video_fname)
    
    def MSE(self, array_1: np.array = None, array_2: np.array = None):
        return (np.square(array_1 - array_2)).mean()
    
    def scale_face(self, reconstructed):
        reconstructed[:,:,0] *= 1.6
        reconstructed[:,:,1] *= 0.9
        reconstructed[:,:,2] *= 1.6
        return reconstructed