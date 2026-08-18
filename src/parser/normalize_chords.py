import json
import re
from pathlib import Path

# Define the global project root (go up 2 levels from src/parser/)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def fix_flat_notation(name: str) -> str:
    return re.sub(r'([A-G])B([0-9A-Z]|$)', r'\1b\2', name)

def parse_chord_name(name: str) -> tuple:
    name = fix_flat_notation(name.upper().strip())
    name = re.sub(r'[^\w#b]', '', name)
    
    root_match = re.match(r'^([A-G][#b]?)', name)
    if not root_match:
        return None, None
    
    root = root_match.group(1)
    rest = name[len(root):]
    quality = 'maj'
    
    if rest.startswith('MIN7') or rest.startswith('M7') and rest.startswith('MIN'): quality = 'min7'
    elif rest.startswith('MIN'): quality = 'min'
    elif rest.startswith('DIM7'): quality = 'dim7'
    elif rest.startswith('DIM'): quality = 'dim'
    elif rest.startswith('AUG7'): quality = 'aug7'
    elif rest.startswith('AUG'): quality = 'aug'
    elif rest.startswith('MAJ7'): quality = 'maj7'
    elif rest.startswith('7'): quality = '7'
    elif rest.startswith('SUS'): quality = 'sus'
    elif rest.startswith('ADD'): quality = 'add'
    
    return root, quality

def normalize_chord_name(name: str, existing_chords: set) -> str:
    name = fix_flat_notation(name)
    root, quality = parse_chord_name(name)
    if not root:
        return name
    
    alt_map = {'A#': 'Bb', 'Bb': 'A#', 'C#': 'Db', 'Db': 'C#', 'D#': 'Eb', 'Eb': 'D#', 'F#': 'Gb', 'Gb': 'F#', 'G#': 'Ab', 'Ab': 'G#'}
    roots_to_try = [root]
    if root in alt_map:
        roots_to_try.append(alt_map[root])
    
    possible_names = []
    for r in roots_to_try:
        if quality == 'maj': possible_names.extend([r, f"{r}maj"])
        elif quality in ['min', 'dim', 'aug', '7', 'maj7', 'min7', 'dim7', 'aug7']: possible_names.append(f"{r}{quality}")
        else: possible_names.append(r)
    
    for p in possible_names:
        if p in existing_chords:
            return p
    return possible_names[0] if possible_names else name

def main():
    input_path = ROOT_DIR / "data" / "parsed" / "chords.json"
    output_path = ROOT_DIR / "data" / "parsed" / "chords_normalized.json"
    
    if not input_path.exists():
        print(f"❌ Base chords database not found at: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chords = data["chords"]
    progressions = data["progressions"]
    existing_chords = set(chords.keys())

    chord_mapping = {}
    all_targets = set()
    for prog in progressions.values():
        for p in prog:
            all_targets.add(p['name'])

    for target in sorted(all_targets):
        chord_mapping[target] = normalize_chord_name(target, existing_chords)

    new_progressions = {}
    for chord, prog in progressions.items():
        new_prog = []
        for p in prog:
            target = p['name']
            mapped = chord_mapping.get(target, target)
            if mapped in existing_chords:
                new_prog.append({
                    "name": mapped,
                    "tension": p.get("tension", ""),
                    "description": p.get("description", ""),
                    "page": p.get("page", 0)
                })
        if new_prog:
            new_progressions[chord] = new_prog

    normalized_data = {
        "chords": chords,
        "progressions": new_progressions,
        "total_chords": len(chords),
        "total_transitions": sum(len(v) for v in new_progressions.values())
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(normalized_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Normalization completed! Saved to {output_path}")

if __name__ == "__main__":
    main()
