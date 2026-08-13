import json
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

NOTE_MAP = {
    'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63,
    'Eb': 63, 'E': 64, 'F': 65, 'F#': 66, 'Gb': 66,
    'G': 67, 'G#': 68, 'Ab': 68, 'A': 69, 'A#': 70,
    'Bb': 70, 'B': 71,
}

def chord_to_notes(chord_name, octave=4):
    root = chord_name[0]
    if len(chord_name) > 1 and chord_name[1] in '#b':
        root += chord_name[1]
    
    root_note = NOTE_MAP.get(root, 60) + (octave - 4) * 12
    
    is_minor = any(x in chord_name for x in ['min', 'm', '-'])
    is_dim = 'dim' in chord_name or '°' in chord_name
    is_aug = 'aug' in chord_name or '+' in chord_name
    is_maj7 = 'maj7' in chord_name or 'M7' in chord_name
    is_min7 = 'min7' in chord_name or 'm7' in chord_name
    is_7 = '7' in chord_name and not is_maj7 and not is_min7
    
    if is_minor:
        notes = [root_note, root_note + 3, root_note + 7]
    elif is_dim:
        notes = [root_note, root_note + 3, root_note + 6]
    elif is_aug:
        notes = [root_note, root_note + 4, root_note + 8]
    else:
        notes = [root_note, root_note + 4, root_note + 7]
    
    if is_maj7:
        notes.append(root_note + 11)
    elif is_min7 or is_7:
        notes.append(root_note + 10)
    
    return sorted(set(notes))

def export_sequence_to_midi(sequence, filename, tempo=120, duration=480):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # ВИПРАВЛЕНО: Правильне встановлення темпу в мікросекундах за допомогою mido.bpm2tempo
    microseconds_per_beat = mido.bpm2tempo(tempo)
    track.append(MetaMessage('set_tempo', tempo=microseconds_per_beat))
    
    time = 0
    for chord in sequence:
        notes = chord_to_notes(chord)
        
        for note in notes:
            track.append(Message('note_on', note=note, velocity=100, time=time))
            time = 0
        
        # Перша нота тримає тривалість (duration), інші йдуть одночасно за нею (time=0)
        first_note = True
        for note in notes:
            t = duration if first_note else 0
            track.append(Message('note_off', note=note, velocity=100, time=t))
            first_note = False
            
    mid.save(filename)
    print(f"✅ MIDI exported: {filename}")

def export_all_sequences():
    input_report = ROOT_DIR / "data" / "generated" / "115_sequences.txt"
    
    if not input_report.exists():
        print(f"❌ Text sequences file not found at: {input_report}. Generate it first.")
        return
        
    with open(input_report, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    sequences = []
    for line in lines:
        if ' → ' in line:
            seq_str = line.strip()
            if '     ' in seq_str:
                seq_str = seq_str.split('     ')[-1]
            chords = [c.strip() for c in seq_str.split(' → ')]
            if chords and len(chords) > 1:
                sequences.append(chords)
    
    print(f"🎵 Parsing found {len(sequences)} progressions. Rendering first 10 files...")
    
    midi_output_dir = ROOT_DIR / "data" / "generated" / "midi"
    midi_output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, seq in enumerate(sequences[:10], 1):
        filename = midi_output_dir / f"sequence_{i:03d}.mid"
        export_sequence_to_midi(seq, filename)
    
    print(f"\n🚀 Success! Rendered MIDI folder: {midi_output_dir}")

if __name__ == "__main__":
    export_all_sequences()
