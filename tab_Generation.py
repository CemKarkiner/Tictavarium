from DB_operations import connect_to_mongo, get_all_notes_by_pdf
import os

NOTE_TO_MIDI = {
    "C": 0, "C#": 1, "D": 2, "D#": 3,
    "E": 4, "F": 5, "F#": 6, "G": 7,
    "G#": 8, "A": 9, "A#": 10, "B": 11
}

GUITAR_TUNING = {
    "E": 40,  # E2
    "A": 45,
    "D": 50,
    "G": 55,
    "B": 59,
    "e": 64   # E4
}

def note_name_to_midi(note_name):
    note_name = note_name.strip().upper()
    # Örnek: C5, C#5, D5
    if len(note_name) < 2:
        raise ValueError(f"Geçersiz nota adı: {note_name}")

    # Eğer ikinci karakter '#' ise, nota iki karakterli, aksi halde tek karakter
    if note_name[1] == '#':
        note = note_name[:2]
        octave_part = note_name[2:]
    else:
        note = note_name[0]
        octave_part = note_name[1:]

    if note not in NOTE_TO_MIDI:
        raise ValueError(f"Tanımsız nota: {note}")

    if not octave_part.isdigit():
        raise ValueError(f"Geçersiz oktav: {octave_part} in note {note_name}")

    octave = int(octave_part)
    return (octave + 1) * 12 + NOTE_TO_MIDI[note]


def midi_to_string_and_fret(midi_note):
    possibilities = []
    for string, base_midi in GUITAR_TUNING.items():
        fret = midi_note - base_midi
        if 0 <= fret <= 24:
            possibilities.append((string, fret))
    return possibilities[0] if possibilities else (None, None)

def convert_notes_to_tab(notes_data):
    tab_output = {s: s + "|" for s in ["e", "B", "G", "D", "A", "E"]}

    for note_obj in notes_data:
        note_name = note_obj.get("note", "").strip().upper()
        duration = int(note_obj.get("duration", "12"))

        if note_name in ["REST", "SILENCE", "PAUSE"]:
            for s in tab_output:
                tab_output[s] += "-" * duration
            continue

        try:
            midi = note_name_to_midi(note_name)
            string, fret = midi_to_string_and_fret(midi)
        except ValueError as e:
            print(f"Hatalı nota atlandı: {note_name} ({e})")
            for s in tab_output:
                tab_output[s] += "-" * duration
            continue

        for s in tab_output:
            if s == string:
                tab_output[s] += f"-{fret}-".ljust(duration, "-")
            else:
                tab_output[s] += "-" * duration

    return "\n".join(tab_output.values())


def generate_tab_for_pdf(source_pdf, output_dir="tabs_output"):
    collection = connect_to_mongo()
    notes_data = get_all_notes_by_pdf(source_pdf, collection)

    if not notes_data:
        print(f"{source_pdf} için nota bulunamadı.")
        return

    tab_content = convert_notes_to_tab(notes_data)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{source_pdf}Tab.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tab_content)

    print(f"TAB dosyası oluşturuldu: {output_path}")

if __name__ == "__main__":
    generate_tab_for_pdf("GuitarLick_AMinorPentatonic")
