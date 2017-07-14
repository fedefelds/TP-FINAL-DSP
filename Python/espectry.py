# import matplotlib.pyplot as plt
# import librosa
# import numpy as np
# filename='/Users/Fede/Desktop/stew.mp3'
import librosa
import numpy as np
import matplotlib.pyplot as plt
filename='/Users/Fede/Documents/Github/TP-FINAL-DSP/Informe/reiss_punch_rev.wav'

# cargar audio
y, sr = librosa.load(filename)

# extraer silencios al principio y final
y,index=librosa.effects.trim(y, top_db=60, ref=np.amax, frame_length=2048, hop_length=50)

# normalizar
valor_max=np.max(y)
y=y/valor_max

D = librosa.stft(y,win_length=300)
print(D.shape)
# librosa.display.specshow(librosa.amplitude_to_db(D,ref=np.max),y_axis='log', x_axis='time')
# plt.title('Power spectrogram')
# plt.colorbar(format='%+2.0f dB')
# plt.tight_layout()
# plt.show()
