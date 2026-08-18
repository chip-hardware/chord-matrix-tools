import json
import random
from pathlib import Path
from typing import List, Dict, Optional, Set

class SmartHarmonyGenerator:
    def __init__(self, db_path: Optional[str] = None):
        # Automatically determine the project root (go up 2 levels from src/core/)
        ROOT_DIR = Path(__file__).resolve().parent.parent.parent
        
        if db_path is None:
            db_path = ROOT_DIR / "data" / "parsed" / "chords_normalized.json"
        else:
            db_path = Path(db_path)
            
        if not db_path.exists():
            raise FileNotFoundError(f"Database not found at: {db_path}")
            
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.chords = data["chords"]
        self.progressions = data["progressions"]
        
        self.existing_chords = set(self.chords.keys())
        
        self.filtered_progressions = {}
        for chord, prog in self.progressions.items():
            filtered = [p for p in prog if p['name'] in self.existing_chords]
            if filtered:
                self.filtered_progressions[chord] = filtered
        
        self.active_chords = set(self.filtered_progressions.keys())
        
        print(f"🎵 Loaded {len(self.chords)} chords")
        print(f"🟢 Active chords (with existing transitions): {len(self.active_chords)}")
        print(f"🔗 Total filtered transitions: {sum(len(v) for v in self.filtered_progressions.values())}")
        
        total_original = sum(len(v) for v in self.progressions.values())
        total_filtered = sum(len(v) for v in self.filtered_progressions.values())
        print(f"📊 Filtered {total_original - total_filtered} dead transitions")
    
    def get_best_start_chords(self, min_transitions: int = 10) -> List[str]:
        sorted_chords = sorted(
            [(name, len(prog)) for name, prog in self.filtered_progressions.items() if len(prog) > 0],
            key=lambda x: x[1],
            reverse=True
        )
        return [name for name, count in sorted_chords if count >= min_transitions]
    
    def generate_sequence(
        self,
        start_chord: str,
        length: int = 8,
        max_tension: Optional[int] = None,
        min_tension: Optional[int] = None,
        avoid_repeats: bool = True,
        seed: Optional[int] = None
    ) -> List[str]:
        if seed is not None:
            random.seed(seed)
        
        start_chord = start_chord.lower().capitalize()
        
        if start_chord not in self.filtered_progressions:
            print(f"❌ Chord '{start_chord}' has no valid exit transitions")
            return [start_chord] if start_chord in self.existing_chords else []
        
        sequence = [start_chord]
        current = start_chord
        used = {start_chord}
        
        for _ in range(length - 1):
            options = self.filtered_progressions.get(current, [])
            
            if max_tension is not None:
                options = [opt for opt in options if self._parse_tension(opt['tension']) <= max_tension]
            
            if min_tension is not None:
                options = [opt for opt in options if self._parse_tension(opt['tension']) >= min_tension]
            
            if avoid_repeats:
                options = [opt for opt in options if opt['name'] not in used]
            
            if not options:
                break
            
            chosen = random.choice(options)
            sequence.append(chosen['name'])
            used.add(chosen['name'])
            current = chosen['name']
        
        return sequence
    
    def generate_multiple(self, start_chord: str, count: int = 5, length: int = 8, **kwargs) -> List[List[str]]:
        sequences = []
        for i in range(count):
            seq = self.generate_sequence(start_chord, length, seed=i*100+42, **kwargs)
            if seq and len(seq) >= 2:
                sequences.append(seq)
        return sequences
    
    def _parse_tension(self, tension_str: str) -> int:
        if not tension_str or not tension_str.startswith('T') or len(tension_str) < 2:
            return 0
        try:
            return int(tension_str[1])
        except ValueError:
            return 0
    
    def print_sequence(self, sequence: List[str]):
        if not sequence:
            print("❌ Sequence is empty")
            return
        print(" → ".join(sequence))

if __name__ == "__main__":
    gen = SmartHarmonyGenerator()
    print("\n🏆 TOP-10 Starting Chords:")
    best = gen.get_best_start_chords(min_transitions=5)
    for i, name in enumerate(best[:10], 1):
        print(f"  {i}. {name}: {len(gen.filtered_progressions[name])} transitions")
