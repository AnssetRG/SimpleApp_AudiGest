import librosa
import torch
import torch.nn.functional as F
import torchaudio
import torchaudio.transforms as T
import os


def get_mfcc_transform(sr: int, n_fcc: int, n_fft: int, hop_len: int) -> T.MFCC:
    return T.MFCC(
        sample_rate=sr,
        n_mfcc=n_fcc,
        melkwargs={
            'n_fft': n_fft,
            'hop_length': hop_len
        }
    )

def _convert_to_mono(signal: torch.Tensor) -> torch.Tensor:
    """
        Convert audio from STEREO to MONO

        Args:
            signal: Tensor of the audio signal to check.

        Returns:
            Tensor of the MONO audio
    """
    if signal.shape[0] > 1:
        signal = torch.mean(signal, dim=0, keepdim=True)
    return signal

def _check_for_resample(signal: torch.Tensor, original_sr: int, target_sample_rate: int) -> torch.Tensor:
    """
        Resample signal to standar Hz (sample rate)

        Args:
            signal: Tensor of the audio signal to check.
            original_sr: Int of the audio Sample Rate
            target_sample_rate: Int of the standar Sample rate

        Returns:
            Tensor of the audio resampled
    """
    if original_sr != target_sample_rate:
        resampler = T.Resample(original_sr, target_sample_rate)
        signal = resampler(signal)
    return signal

def get_signal_mono(audio_path: str, config: dict) -> torch.Tensor:
    """
        Load audio from a path to be resampled and converted to MONO

        Args:
            audio_path: String of path of the audio file
            config: Dictionary of the configuration for resample

        Returns:
            Tensor of the audio signal
    """
    signal, sr = torchaudio.load(audio_path)
    signal = _check_for_resample(signal, sr, config['sample_rate'])
    return _convert_to_mono(signal)

def get_sliced_melspectrogram(mono_signal: torch.Tensor, config: dict, n_fft: int, hop_len: int) -> torch.Tensor:
    """
        Represent the audio signal as Melspectrogram

        Args:
            mono_signal: Tensor of the audio signal to check.
            config: Int of the audio Sample Rate
            n_fft: Int of number of Fast Fourrier Transformations of the Melspectrogram transformation
            hop_len: int of the Hop Lenght of the windows in the Melspectrogram transformation

        Returns:
            Tensor of audio Melspectrogram
    """
    signal_len = mono_signal.shape[1]
    if signal_len > config['max_samples']:
        mono_signal = mono_signal[:, :config['max_samples']]
    elif signal_len < config['max_samples']:
        pad_samples = config['max_samples'] - signal_len
        right_pad = (0, pad_samples)
        mono_signal = F.pad(mono_signal, right_pad)

    melspec = librosa.feature.melspectrogram(mono_signal.numpy()[0], config['sample_rate'],
                                            n_fft=n_fft, hop_length=hop_len)

    return torch.from_numpy(melspec)

def compute_mfcc(mono_signal: torch.Tensor, mfcc_transform: T.MFCC = None) -> torch.Tensor:
    mono_signal = torch.flatten(mono_signal)

    if mfcc_transform is not None:
        return mfcc_transform(mono_signal)
    else:
        raise AttributeError('MFCC transformation function is None')

def process_framed_mfcc(mono_signal: torch.Tensor, config: dict, mfcc_transform: T.MFCC = None) -> 'list[torch.Tensor]':
    """
        Extract the Mel Frequency Cepstral Coefficents of the audio

        Args:
            mono_signal: Tensor of the audio signal to check.
            config: Int of the audio Sample Rate
            n_fft: Int of number of Fast Fourrier Transformations of the Melspectrogram transformation
            hop_len: int of the Hop Lenght of the windows in the Melspectrogram transformation

        Returns:
            Tensor of audio Melspectrogram
    """
    mfcc = compute_mfcc(mono_signal, mfcc_transform=mfcc_transform)
    mean, std = torch.mean(mfcc, dim=0), torch.std(mfcc, dim=0)
    mfcc = (mfcc - mean) / std

    frame_size = int(config['fps'] / 2)
    pad_left = torch.zeros(config['n_mfcc'], frame_size)
    pad_right = torch.zeros(config['n_mfcc'], frame_size)
    mfcc = torch.column_stack((pad_left, mfcc, pad_right))

    seq_len = mfcc.shape[1]
    input_list = []
    for i in range(frame_size, seq_len - frame_size):
        input_list.append(mfcc[:, i - frame_size:i + frame_size])

    return input_list

def _check_file_exists(file_name: str) -> str:
    data_dir = 'processed_data'
    file_path = os.path.join(data_dir, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise ValueError('{} does not exists'.format(file_path))

    return file_path

def load_torch(file_name: str) -> torch.Tensor:
    """
        Load pytorch serialized data from processed_data directory.

        Args:
            file_name: String containing the file path from 'processed_data' directory.

        Raises:
            ValueError: If the file does not exists.

        Returns:
            The tensor in serialized file.
    """
    file_path = _check_file_exists(file_name)

    return torch.load(file_path)