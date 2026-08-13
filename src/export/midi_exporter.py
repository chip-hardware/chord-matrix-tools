import mido
from mido import MidiFile, MidiTrack, Message
from typing import List, Dict
import random

class MIDIExporter:
    def __init__(self):
        self.note_map = {
            'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63,
            'Eb': 63, 'E': 64, 'F': 65, 'F#': 66, 'Gb': 66,
            'G': 67, 'G#': 68, 'Ab': 68, 'A': 69, 'A#': 70,
            'Bb': 70, 'B': 71
        }
    
    def export_sequence(
        self,
        sequence: List[str],
        filename: str,
        tempo: int = 120,
        chord_duration: int = 480,
        octave: int = 4
    ):
        """Експортує послідовність акордів у MIDI"""
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        
        # Tempo
        tempo_micro = int(60000000 / tempo)
        track.append(mido.MetaMessage('set_tempo', tempo=tempo_micro))
        
        time = 0
        for chord_name in sequence:
            notes = self._chord_to_notes(chord_name, octave)
            
            # Note On
            for note in notes:
                track.append(Message('note_on', note=note, velocity=100, time=time))
                time = 0
            
            # Note Off після тривалості
            for note in notes:
                track.append(Message('note_off', note=note, velocity=100, time=chord_duration))
                time = 0
        
        mid.save(filename)
    
    def _chord_to_notes(self, chord_name: str, octave: int) -> List[int]:
        """Перетворює назву акорду на ноти"""
        # Спрощена реалізація
        root = chord_name[0]
        if len(chord_name) > 1 and chord_name[1] in '#b':
            root += chord_name[1]
        
        root_note = self.note_map.get(root, 60) + (octave - 4) * 12
        
        # Основна тріада
        if 'm' in chord_name or 'min' in chord_name:
            notes = [root_note, root_note + 3, root_note + 7]  # minor
        else:
            notes = [root_note, root_note + 4, root_note + 7]  # major
        
        # 7-і акорди
        if '7' in chord_name and 'maj7' not in chord_name:
            notes.append(root_note + 10)  # 7
        elif 'maj7' in chord_name:
            notes.append(root_note + 11)  # maj7
        
        return sorted(set(notes))