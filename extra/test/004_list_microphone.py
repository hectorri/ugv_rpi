import speech_recognition as sr
import pyaudio
#for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #print(f'{index}, {name}')

print("\nPyaudio:")
p = pyaudio.PyAudio()
for ii in range(p.get_device_count()):
      print(p.get_device_info_by_index(ii).get('name'))