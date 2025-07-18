import numpy as np
import sounddevice as sd
import time

class Metronome:
    def __init__(self, bpm=100, beats_per_measure=4):
        self.bpm = bpm
        self.beats_per_measure = beats_per_measure
        self.is_running = False
        self.sample_rate = 44100
        self.beep_duration = 0.2

        self.accent_freq = 1000  # Hz
        self.beat_freq = 750     # Hz

    def _generate_beep(self, frequency):
        t = np.linspace(0, self.beep_duration, int(self.sample_rate * self.beep_duration), False)
        beep = 0.9 * np.sin(2 * np.pi * frequency * t)
        return beep.astype(np.float32)

    def _play_beat(self, beat_num):
        freq = self.accent_freq if beat_num == 1 else self.beat_freq
        beep = self._generate_beep(freq)
        sd.play(beep, samplerate=self.sample_rate)
        sd.wait()

    def start(self):
        self.is_running = True
        interval = 60.0 / self.bpm
        beat = 1

        print(f"Metronome started: {self.bpm} BPM, {self.beats_per_measure}/4")
        try:
            while self.is_running:
                print(f"Playing beat {beat}")
                self._play_beat(beat)
                time.sleep(max(0, interval - self.beep_duration))
                beat = beat + 1 if beat < self.beats_per_measure else 1
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.is_running = False
        print("Metronome stopped.")


if __name__ == "__main__":
    metronome = Metronome(bpm=100, beats_per_measure=4)
    metronome.start()
