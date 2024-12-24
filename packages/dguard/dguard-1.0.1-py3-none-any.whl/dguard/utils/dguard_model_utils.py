# coding = utf-8
# @Time    : 2024-05-21  09:02:30
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Dguard Model.

import base64
import getpass
import os
import subprocess
import tarfile
import uuid

import torch
import torchaudio
import yaml
from cryptography.fernet import Fernet

from dguard.interface.models_info import model_info as MI
from dguard.process.processor import FBank_kaldi
from dguard.speaker.models.speaker_model import get_speaker_model
from dguard.utils import logger
from dguard.utils.config import yaml_config_loader
from dguard.utils.wespeaker_checkpoint import load_checkpoint

ALL_MODELS = list(MI.keys())
DGUARD_MODEL_PATH = os.getenv("DGUARD_MODEL_PATH", None)
if DGUARD_MODEL_PATH is None:
    DGUARD_MODEL_PATH = os.path.expanduser("~/.dguard")
    print(f"DGUARD_MODEL_PATH is not set, using default path: {DGUARD_MODEL_PATH}")
    print("Please put ALL your model files in this directory.")
os.makedirs(DGUARD_MODEL_PATH, exist_ok=True)


def remove_file(file_path):
    if os.path.exists(file_path):
        subprocess.run(f"rm -rf {file_path}", shell=True)


def wget_download(url, out):
    cmd = f"wget '{url}' -O {out}"
    subprocess.run(cmd, shell=True)


def download_or_load(url, model_name=None, ext=".tar"):
    if url.startswith("http"):
        filename = os.path.basename(url)
        filename = filename.split("=")[-1]
        ckpt_path = f"{DGUARD_MODEL_PATH}/{filename}"
        if os.path.exists(ckpt_path):
            return ckpt_path
        else:
            logger.info(
                f"Model not found, downloading from {url} -> {DGUARD_MODEL_PATH}"
            )
        wget_download(url, out=os.path.join(DGUARD_MODEL_PATH, filename))
    else:
        ckpt_path = url
    if not os.path.exists(ckpt_path):
        if ext == ".yaml":
            ckpt_path = ckpt_path.replace("_lm", "")
            if not os.path.exists(ckpt_path):
                raise FileNotFoundError(
                    f"Dguard Error: Model file {ckpt_path} not found and it is not a valid URL."
                )
            else:
                return ckpt_path
        raise FileNotFoundError(
            f"Dguard Error: Model file {ckpt_path} not found and it is not a valid URL."
        )
    return ckpt_path


def untar_and_find_pt_yaml_file(tar_path, model_name):
    extract_dist_path = os.path.join(DGUARD_MODEL_PATH, model_name)
    if not os.path.exists(extract_dist_path):
        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(extract_dist_path)
        logger.info(f"Extracted {tar_path} to {extract_dist_path}")
    pt_path = None
    yaml_path = None
    for root, dirs, files in os.walk(extract_dist_path):
        for file in files:
            if file.startswith("."):
                continue
            if file.endswith(".pt"):
                pt_path = os.path.join(root, file)
            if file.endswith(".yaml"):
                yaml_path = os.path.join(root, file)
    if pt_path is None or yaml_path is None:
        raise FileNotFoundError(
            f"Dguard Error: Cannot find pt or yaml file in {DGUARD_MODEL_PATH}."
        )
    return pt_path, yaml_path


def load_wav(
    wav_file, sr, channel=0, wavform_normalize=False, saveto=None, start_time=None
):
    if hasattr(wav_file, "filename"):
        wav_file = wav_file.filename
    my_uuid = str(uuid.uuid1())
    os.makedirs(f"{DGUARD_MODEL_PATH}/tmp", exist_ok=True)
    if saveto:
        tmp_wav_file = saveto
    else:
        tmp_wav_file = f"{DGUARD_MODEL_PATH}/tmp/{my_uuid}.wav"
    try:
        cmd = f"ffmpeg -i {wav_file} -acodec pcm_s16le -ar {sr} -map_metadata -1 -map_channel 0.0.{channel} -y {tmp_wav_file} > /dev/null 2>&1"
        subprocess.run(cmd, shell=True)
        pcm, sr = torchaudio.load(tmp_wav_file, normalize=wavform_normalize)
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(f"FFmpeg command failed: {cmd}")
        logger.error("Check if ffmpeg is installed and in PATH.")
        logger.error(f"Also check if the input file dose not have channel #{channel}.")
        raise e

    if start_time:
        if start_time * sr > pcm.shape[1]:
            raise ValueError(
                f"start_time {start_time} is greater than the duration of the audio file"
            )
        else:
            pcm = pcm[:, int(start_time * sr) :]

    # rm tmp file
    if not saveto:
        subprocess.run(f"rm -rf {tmp_wav_file}", shell=True)
    return pcm, sr


def parse_config_or_kwargs(config_file, key=None, **kwargs):
    """parse_config_or_kwargs

    :param config_file: Config file that has parameters, yaml format
    :param **kwargs: Other alternative parameters or overwrites for config
    """
    if key is not None:
        with open(config_file, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = Fernet(key).decrypt(encrypted_data)
        # print(decrypted_data)
        yaml_config = yaml.load(decrypted_data, Loader=yaml.FullLoader)
        # print(yaml_config)
    else:
        with open(config_file) as con_read:
            yaml_config = yaml.load(con_read, Loader=yaml.FullLoader)
    # values from config file are all possible params
    help_str = "Valid Parameters are:\n"
    help_str += "\n".join(list(yaml_config.keys()))
    return dict(yaml_config, **kwargs)


def load_model_tiny_model(
    loader,
    pt_path,
    yaml_path,
    strict,
    device,
    sample_rate,
    feat_dim,
    feature_extractor,
    key=None,
):
    if loader == "3dspeaker":
        # TODO: Will be deprecated in the future!!!
        config = yaml_config_loader(yaml_path)
        embedding_model = build("embedding_model", config)
        embedding_model.load_state_dict(
            torch.load(pt_path, map_location="cpu"), strict=strict
        )
        embedding_model.eval()
        embedding_size = config["model"]["embed_dim"]
        if feature_extractor:
            feature_extractor = build("feature_extractor", config)
        else:
            feature_extractor = None
    elif loader == "wespeaker":
        if "encry" in pt_path:
            if key is None:
                # ask user input password
                key = getpass.getpass(":) Welcom ! Please input the key: \n")
                key = key + "a" * (32 - len(key)) if len(key) < 32 else key[:32]
                key = key.encode()
                assert len(key) == 32, "The key must be 32 bytes long"
                key = base64.urlsafe_b64encode(key)
            configs = yaml.load(yaml_path, Loader=yaml.FullLoader)
            configs = parse_config_or_kwargs(configs, key=key)
            embedding_model = get_speaker_model(configs["model"])(
                **configs["model_args"]
            )
        else:
            configs = yaml.load(yaml_path, Loader=yaml.FullLoader)
            configs = parse_config_or_kwargs(configs)
            embedding_model = get_speaker_model(configs["model"])(
                **configs["model_args"]
            )
        # feat_dim = configs['model']["feat_dim"]

        if "encry" in pt_path:
            load_checkpoint(embedding_model, pt_path, encrypt=True, key=key)
        else:
            load_checkpoint(embedding_model, pt_path)
        embedding_model.eval()
        if feature_extractor:
            feature_extractor = FBank_kaldi(
                n_mels=feat_dim, sample_rate=sample_rate, cmn=True
            )
        else:
            feature_extractor = None
    else:
        raise NotImplementedError(f"Loader {loader} not implemented.")
    embedding_model = embedding_model.to(device)
    return embedding_model, feature_extractor, key
