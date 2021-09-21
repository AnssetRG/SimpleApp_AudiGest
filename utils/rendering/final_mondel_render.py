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

    def render_sequences(self, model, device, melspectrogram_tensor, mfcc_tensor, audio_path, out_folder, run_in_parallel=True):
        if run_in_parallel:
            thread = threading.Thread(target=self._render_helper, args=(model, device, melspectrogram_tensor, mfcc_tensor, audio_path, out_folder))
            thread.start()
            thread.join()
        else:
            self._render_helper(model, device, melspectrogram_tensor, mfcc_tensor, audio_path, out_folder)

    def _render_helper(self, model, device, melspectrogram_tensor, mfcc_tensor, audio_path, out_folder):
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)

            audio_name = audio_path.split("/")[-1].split(".")[0]
            video_fname = os.path.join(out_folder, f'{audio_name}.mp4')
            temp_video_fname = os.path.join(out_folder, f'{audio_name}_tmp.mp4')
            self._render_sequences_helper(model, device, video_fname, temp_video_fname, audio_path, melspectrogram_tensor, mfcc_tensor)

    def _render_sequences_helper(self, model, device, video_fname, temp_video_fname, audio_path, melspec, mfcc):
        def add_image_text(img, text):
            img = img.copy()
            font = cv2.FONT_HERSHEY_SIMPLEX
            textsize = cv2.getTextSize(text, font, 1, 2)[0]
            textX = (img.shape[1] - textsize[0]) // 2
            textY = textsize[1] + 50
            return cv2.putText(img, '%s' % (text), (textX, textY), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        num_frames = melspec.shape[0]

        # tmp_video_file = tempfile.NamedTemporaryFile('w', suffix='.mp4', dir=os.path.dirname(video_fname))
        if int(cv2.__version__[0]) < 3:
            print('cv2 < 3')
            writer = cv2.VideoWriter(temp_video_fname, cv2.cv.CV_FOURCC(*'mp4v'), 30, (800, 800), True)
        else:
            print('cv2 >= 3')
            writer = cv2.VideoWriter(temp_video_fname, cv2.VideoWriter_fourcc(*'mp4v'), 30, (800, 800), True)

        model= model.to(device)
        model.eval()
        hidden = None

        with torch.no_grad():
            # melspec = melspec.unsqueeze(1)
            melspec = melspec.to(device)

            # mfcc = mfcc.permute(0, 2, 1)
            mfcc = mfcc.to(device)

            reconstructed, _ = model(melspec, mfcc, hidden)
            reconstructed = reconstructed.cpu().numpy()

            center = np.mean(reconstructed[0], axis=0)

            for i_frame in range(num_frames):
                pred_img = render_mesh_helper(Mesh(reconstructed[i_frame], self.template_mesh.f), center)
                pred_img = add_image_text(pred_img, 'Prediction')
                writer.write(pred_img)
            writer.release()

        cmd = (f'ffmpeg -i {audio_path} -i {temp_video_fname} -vcodec h264 -ac 2 -channel_layout stereo -pix_fmt yuv420p {video_fname}').split()
        call(cmd)