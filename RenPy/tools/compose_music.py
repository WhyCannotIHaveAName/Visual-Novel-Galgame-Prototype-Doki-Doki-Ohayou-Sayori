from pathlib import Path
import numpy as np
import wave

out = Path(__file__).resolve().parents[1] / 'game/audio'
out.mkdir(parents=True, exist_ok=True)
rate = 22050

def make(name, chords, melody, bpm, tone):
    beat = 60 / bpm
    length = beat * 64
    audio = np.zeros((int(length * rate), 2), dtype=np.float64)
    def note(midi, start, duration, volume, pan=0.0, pad=False):
        size = int(duration * rate)
        t = np.arange(size) / rate
        freq = 440 * 2 ** ((midi - 69) / 12)
        if pad:
            env = np.minimum(t / .5, 1) * np.minimum((duration - t) / .8, 1)
            y = (np.sin(2*np.pi*freq*t) + .12*np.sin(2*np.pi*freq*2*t)) * env
        else:
            env = (1-np.exp(-t*100)) * np.exp(-t / tone) * np.minimum((duration-t)/.1,1)
            y = (np.sin(2*np.pi*freq*t) + .22*np.sin(2*np.pi*freq*2*t)*np.exp(-t*3) + .09*np.sin(2*np.pi*freq*3*t)*np.exp(-t*5)) * env
        pos = int(start*rate)
        n = min(size,len(audio)-pos)
        if n<=0:return
        audio[pos:pos+n,0] += y[:n]*volume*(1-pan*.4)
        audio[pos:pos+n,1] += y[:n]*volume*(1+pan*.4)
    for bar in range(16):
        chord=chords[bar%len(chords)]
        start=bar*4*beat
        for n in chord:note(n-12,start,4*beat,.019,pad=True)
        for step,idx in enumerate([0,1,2,1,0,2,1,2]):note(chord[idx],start+step*.5*beat,2*beat,.055,-.35)
        for step in range(4):
            n=melody[(bar*4+step)%len(melody)]
            if n:note(n,start+step*beat,2.7*beat,.09,.3)
    # A quiet room reflection, with enough decay and no clipping.
    dry=audio.copy()
    for delay,gain in [(.19,.12),(.37,.07),(.58,.04)]:
        shift=int(delay*rate);audio[shift:]+=dry[:-shift]*gain
    fade=int(rate*.65); audio[:fade]*=np.linspace(0,1,fade)[:,None]; audio[-fade:]*=np.linspace(1,0,fade)[:,None]
    audio=np.clip(audio,-.85,.85)
    with wave.open(str(out/(name+'.wav')),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(rate);f.writeframes((audio*32767).astype('<i2').tobytes())
    print(name,round(length,1),'seconds; peak',round(float(np.max(np.abs(audio))),3))

make('ohayou',[(60,64,67),(57,60,64),(53,57,60),(55,59,62)], [76,0,74,72,71,72,0,67,69,72,76,74,71,0,69,67],84,1.1)
make('blue_hour',[(57,60,64),(53,57,60),(50,53,57),(52,55,59)], [72,0,71,0,69,0,64,0,65,0,69,67,64,0,0,0],66,1.8)
make('afterimage',[(60,64,71),(56,60,63),(57,60,64),(55,59,66)], [83,0,0,76,0,75,0,0,81,0,76,0,78,0,0,0],72,2.0)
