# from __future__ import print_function
# import cv2 as cv
import numpy as np

folder_number = np.arange(1,2)
for numbers  in folder_number:

    print("folder number: ", numbers)


    #from __future__ import print_function
    import scipy.io.wavfile as wavfile
    import numpy as np
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip as exr
    import os
    num = numbers
    #num = int(input('please input folder number: '))
    import subprocess
    dir = os.path.join('/media/icv/The Boss/split','split{}'.format(num))
    os.chdir(dir)

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dir):
        for file in f:
            if '.mp4' in file:
                files.append(file)

    for f in files:
        f = f.rstrip('mp4')
        print(f)
        aud_sep = subprocess.Popen("ffmpeg -i {}mp4 -vn -codec:a libmp3lame {}1.mp3".format(f, f),shell=True)
        aud_sep.communicate()

        while True:
            try:
                open(f+'1.mp3')
                break
            except:
                continue
        denoise = subprocess.Popen('sox {} -n trim 1 1 noiseprof| sox {} {} noisered'.format(f+'1.mp3',f+'1.mp3',f+'2.mp3'),shell=True)
        denoise.communicate()
        while True:
            try:
                open(f+'2.mp3')
                break
            except:
                continue
        normalise = subprocess.Popen('sox {}2.mp3 {}3.mp3 norm'.format(f,f),shell=True)
        normalise.communicate()
        while True:
            try:
                open(f+'3.mp3')
                break
            except:
                continue
        mp3_to_wav = subprocess.Popen('ffmpeg -i {}3.mp3 {}wav'.format(f,f),shell=True)
        mp3_to_wav.communicate()
        while True:
            try:
                open(f+'wav')
                break
            except:
                continue

        fs_rate, signal = wavfile.read(f+'wav')
        l_audio = len(signal.shape)
        if l_audio == 2:
            signal = signal.sum(axis=1) / 2
        N = signal.shape[0]
        secs = N / float(fs_rate)
        Ts = 1.0 / fs_rate
        signal = np.array(signal)
        last_peak = np.argwhere(signal > 10000)[-1]
        t = np.arange(0, secs, Ts)
        time = float(t[last_peak])
        time = time+1.4
        exr(f+'mp4',time,float(t[-1]),'/media/icv/nash/Niyi/major_trim{}/'.format(num) +f+'mp4')