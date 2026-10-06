from pathlib import Path
import numpy as np
import wave
g=Path(__file__).resolve().parents[1]/"game"
# Original synthesis: envelopes prevent clicks; restrained peak levels.
sr=44100;rng=np.random.default_rng(21)
for name,seconds in [('signal',1.1),('fracture',2.2),('low',2.4)]:
 t=np.arange(int(seconds*sr))/sr
 env=np.minimum(t/.08,1)*np.minimum((seconds-t)/.4,1)
 if name=='low': v=np.sin(2*np.pi*(52*t+5*t*t))*.2+np.sin(2*np.pi*81*t)*.09
 elif name=='signal': v=np.sin(2*np.pi*(440*t-110*t*t))*.07+rng.normal(0,.07,len(t))*np.sin(2*np.pi*8*t)**8
 else: v=np.sin(2*np.pi*(90*t+17*t*t))*.15+rng.normal(0,.045,len(t))*(.5+.5*np.sin(2*np.pi*7*t))
 data=(np.clip(v*env,-.55,.55)*32767).astype('<i2')
 with wave.open(str(g/'audio'/f'fx_{name}.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(data.tobytes())
