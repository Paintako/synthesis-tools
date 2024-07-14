# Mi2s Text to speech audio process tools 
## Docker
### Build
Make sure you're under the folder which contains `Dockerfile`
```sh
docker build -t syn .
```

### Run container
`
Make sure you have 'nvidia-docker' installed on your system.
We need '--gpu' option run properly in order to utilize GPU.
`

If error like: `docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]].` occurs, that means your system needs nvidia-docker to be installed.

Follow the 
[Solution](https://www.cnblogs.com/booturbo/p/16318627.html)

```sh
docker run -it --gpus all -v $PWD/app:/app --name tools syn /bin/bash
```

### Check if GPU is avaliable
Make sure you're in container and running bash.
```sh
python
>>> import torch
>>> print(torch.cuda.is_available())
True
```


## Test functions
### 1. youtube video download
```sh
python youtubeTowav.py -u [URL]
```

This command is used to download videos from youtube, and convert this video file into audio
file. You'll generate a output.wav in the `process` folder

### 2. slice audio into small chunks
```sh
fap slice-audio-v2 process process
```
This command will generate slice audio chunks in the given folder, and will mkdir a 
output dir in the given folder. 

### 3. Denoise
```sh
python denoise.py -p process/output
```
This will denoise the `output.wav` in the given folder.

### 4. ASR
```sh
python asr.py -p process/output
```

## Example
```sh
python youtubeTowav.py -u https://www.youtube.com/watch?v=AJ5anT7WHe8&t=2s&ab_channel=%E9%8C%AB%E7%89%87 
fap slice-audio-v2 process process
python denoise.py -p process/output
python asr.py -p process/output
```

Note: There's bug in `yt-dlp`, it won't automatically stop. You need to stop the process (ctrl c) by yourself.