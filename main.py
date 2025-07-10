from metronome import Metronome

if __name__ == "__main__":
    bpm = int(input("Enter BPM: "))
    beats = int(input("Enter beats per measure (e.g., 4): "))
    met = Metronome(bpm=bpm, beats_per_measure=beats)
    met.start()
