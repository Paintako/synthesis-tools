import whisper
import os
import tqdm
import re
import argparse

def contains_non_chinese_characters(s):
    # 匹配任何非中文字符（包括英文字母）
    english_letter_pattern = re.compile(r'[A-Za-z]')
    
    # 搜索字符串中是否包含英文字母
    match = english_letter_pattern.search(s)
    
    return match is not None


def remove_punctuation(text):
    # 使用正則表達式匹配所有標點符號
    return re.sub(r'[^\w\s]', '', text)


def asr(wav_file: os.path.abspath, model) -> str:
    audio = whisper.load_audio(wav_file)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)
    language = max(probs, key=probs.get)
    options = whisper.DecodingOptions(language='zh')
    result = whisper.decode(model, mel, options)
    return result.text

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, required=True, help='path to the audio file')
    return parser.parse_args()

if __name__ == "__main__":
    args = args_parser()
    base_dir = args.p
    bad_dir = "./bad"
    if not os.path.exists(bad_dir):
        os.mkdir(bad_dir)
    model = whisper.load_model("medium")
    total_files = len(os.listdir(base_dir)) 
    with tqdm.tqdm(total=total_files, desc="Processing WAV files", ncols=100, unit='file') as pbar:
        for f in os.listdir(base_dir):
            if not f.endswith('.wav'):
                continue
            wav_file = os.path.join(base_dir, f)
            text = asr(wav_file, model)
            with open(wav_file.replace('.wav', '.txt'), 'w') as text_file:
                text_file.write(text)
            pbar.update(1)