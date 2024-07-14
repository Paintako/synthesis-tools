import os
import argparse
from DeepFilterNet.DeepFilterNet.df.enhance import enhance, init_df, load_audio, save_audio
from tqdm import tqdm
import librosa
import soundfile as sf

def parse_paths():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='path of the audio file to be denoised')
    args = parser.parse_args()
    if not args.path:
        raise Exception('Please enter the path of the audio file to be denoised')
    return args.path

def denoise(audio_path):
    # Load default model
    model, df_state, _, _ = init_df()

    for file in tqdm(os.listdir(audio_path), desc="Processing audio files"):
        if not file.endswith(".wav"):
            continue
        file = audio_path + '/' + file
        # Load audio
        try:
            audio, _ = load_audio(file, sr=df_state.sr())
        except Exception as e:
            os.system(f'rm {file}')
            os.system(f'rm {file.replace(".wav", ".txt")}')
            print(f'Error loading {file}: {e}')
            continue
        # Denoise the audio
        enhanced = enhance(model, df_state, audio)
        # Save for listening
        save_audio(file, enhanced, df_state.sr())
        # change sample rate if needed

    print(f'Denoising {audio_path} finished')


def trim_silence(audio_path):
    for file in tqdm(os.listdir(audio_path), desc="Processing audio files"):
        if not file.endswith(".wav"):
            continue
        file = audio_path + '/' + file
        # Load audio
        y, sr = librosa.load(file, sr=48000)

        # trim silent edges
        yt, index = librosa.effects.trim(y, top_db=20, frame_length=2048, hop_length=512)

        print(f'original length: {len(y)}, trimmed length: {len(yt)}')
        # save
        sf.write(file, yt, sr, 'PCM_16')

if __name__ == "__main__":
    path = parse_paths()
    denoise(path)
        

    


