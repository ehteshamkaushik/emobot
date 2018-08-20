from tkinter import *
import pyaudio
import wave
from os import path
import speech_recognition as sr
import soundfile as sf
import math
import numpy as np
import librosa
import Stimuli.Speech as sp
from aubio import source
from aubio import pitch as pt
import Domains.AbstractDomain as abd
import Domains.AffectiveDomain as afd
import Domains.Perception as pc
import Domains.GenerateEmotion as ge

root = Tk()

global button1, button2, button3, button4, lable1, no_of_words, \
    lable_duration, lable_intensity, lable_pitch, lable_rate, lable_signal_energy, lable_volume, lable_emotion

p = pyaudio.PyAudio()
frames = []
WIDTH = 2
CHANNELS = 2
RATE = 44100
CHUNK = 8192
FORMAT = pyaudio.paInt16
speech = sp.Speech()


def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return in_data, pyaudio.paContinue


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback,
                start=False)


def start():
    print("Recording Started")
    stream.start_stream()
    button1.config(state=DISABLED)
    button2.config(state=NORMAL)


def stop():
    print("Recording Finished")
    button1.config(state=NORMAL)
    button2.config(state=DISABLED)
    stream.stop_stream()
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    frames.clear()


def recognize():
    global no_of_words
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "output.wav")
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`

        sentence = r.recognize_google(audio)
        no_of_words = sentence.count(' ') + 1
        print("No of Words in a sentcence : ", no_of_words)
        # print("Google Speech Recognition thinks you said " + sentence)
        lable1.config(text=sentence)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        no_of_words = 1
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def calculate_volume(data1, data2):
    cnt = 0
    d = 0
    for i in range(0, len(data1)):
        if data1[i] > 0.02:
            cnt += 1
            d += data1[i]

    avg1 = d/cnt

    cnt = 0
    d = 0
    for i in range(0, len(data2)):
        if data2[i] > 0.02:
            cnt += 1
            d += data1[i]

    avg2 = d / cnt
    avg = (avg1+avg2)/2
    return avg


def detect_pitch():
    filename = 'output.wav'

    downsample = 1
    samplerate = 44100 // downsample
    if len(sys.argv) > 2: samplerate = int(sys.argv[2])

    win_s = 4096 // downsample  # fft size
    hop_s = 512 // downsample  # hop size

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 1

    pitch_o = pt("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)
    average = 62.2
    pitches = []
    confidences = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        # pitch = int(round(pitch))
        confidence = pitch_o.get_confidence()
        # if confidence < 0.8: pitch = 0.
        # print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))

        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    pitches1 = []
    for i in pitches:
        if i != 0:
            pitches1.append(i)

    return np.asarray(pitches1).mean()

def stEnergy(frame):
    """Computes signal energy of frame"""
    return np.sum(frame ** 2) / np.float64(len(frame))


def calculate():
    global no_of_words
    data, samplerate = sf.read('output.wav')
    speech.signal_energy = normalize(0.0001, 0.06, 0.001, 0.01, stEnergy(data))
    print("Signal Energy:", speech.signal_energy)
    lable_signal_energy.config(text="Signal Energy : "+str(speech.signal_energy))
    data1 = []
    data2 = []

    for i in range(0, len(data)):
        if abs(data[i][0]) >= 0.75:
            # print(data[i])
            data[i] = 0
            # print("Removing noise")
            # print(data[i])
        data1.append(data[i][0])
        data2.append(data[i][1])

    peak1 = max(data1)
    peak2 = max(data2)
    maxpeak = max(peak1, peak2)
    ratio = (maxpeak*maxpeak)/(.01*.01)
    intensity = 10 * math.log(ratio, 10)
    speech.intensity = normalize(15, 40, 25, 35, intensity)
    print("Intensity : ", speech.intensity)
    lable_intensity.config(text="Intensity : "+str(intensity))

    zeroSamples = 0
    start = False
    lastSample = None
    cuttingSamples = 0
    for i in range(0, len(data1)):
        if abs(data[i][0]) <= 0.02:
            if start:
                zeroSamples+=1
            else:
                cuttingSamples += 1
        elif not start:
            start = True
        else:
            lastSample = zeroSamples

    cuttingSamples += zeroSamples - lastSample
    zeroSamples = lastSample
    activeSamples = len(data1) - cuttingSamples
    # print("Total dur: ", cuttingSamples/samplerate)
    dur = activeSamples/samplerate
    # print("No of ActiveSamples: ", activeSamples)
    # print("No of dur: ", dur)

    avg = calculate_volume(data1, data2)
    speech.volume = normalize(0.01, 0.15, 0.05, 0.09, avg)
    print("volume : ", speech.volume)
    lable_volume.config(text="volume : " + str(avg))
    zerotime = zeroSamples/samplerate
    averageDuration = zerotime/no_of_words
    speech.duration = normalize(0.2, 1.3, 0.4, 0.8, averageDuration)
    print("Duration : ", speech.duration)
    lable_duration.config(text="Duration : "+str(averageDuration))
    speech.average_pitch = normalize(55, 85, 68, 72, detect_pitch())
    print("Average Pitch : ", speech.average_pitch)
    lable_pitch.config(text="Average Pitch : " + str(speech.average_pitch))

    wpm = no_of_words*60/dur
    speech.rate = normalize(20, 140, 60, 100, wpm)
    print("Rate in WPM : ", speech.rate)
    lable_rate.config(text="Rate in WPM : " + str(wpm))
    abstract_domain = abd.AbstractDomain()
    affective_domain = afd.AffectiveDomain()
    perception = pc.Perception(speech)
    generate = ge.GenerateEmotion()
    perception.calculate()
    generate.calculateEmotions()
    print(affective_domain)
    lable_emotion.config(text=str(affective_domain))
    print(abstract_domain)


def normalize(minval, maxval, avgminval, avgmaxval, val):
    minValue = minval
    maxValue = maxval
    avgmin = avgminval
    avgmax = avgmaxval
    avgvalue = (avgmin + avgmax)/2
    value = val
    if value >= avgvalue:
        stepsize = 1/(maxValue - avgvalue)
        retval = (0 + (value - avgvalue)*stepsize)
        return retval
    else:
        stepsize = 1/(avgvalue - minValue)
        retval = (0 - (avgvalue - value) * stepsize)
        return retval


button1 = Button(root, text="Start Recording",command=start)
button2 = Button(root, text="Stop Recording", command=stop)
button3 = Button(root, text="Recognize Audio", command=recognize)
button4 = Button(root, text="Calculate", command=calculate)
lable1 = Label(root, text="Click Recognize to see text")
lable_signal_energy = Label(root, text="Signal Energy")
lable_intensity = Label(root, text="Intensity")
lable_volume = Label(root, text="Volume")
lable_duration = Label(root, text="Duration")
lable_rate = Label(root, text="Rate in Wpm")
lable_pitch = Label(root, text="Pitch")
lable_emotion = Label(root, text="Emotion")


button1.pack()
button2.pack()
button3.pack()
button4.pack()
lable1.pack()
lable_duration.pack()
lable_signal_energy.pack()
lable_volume.pack()
lable_rate.pack()
lable_pitch.pack()
lable_intensity.pack()
lable_emotion.pack()
root.mainloop()
