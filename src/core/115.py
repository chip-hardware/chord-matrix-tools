import json
import random
from pathlib import Path
import datetime

# Dynamically determine the project root (go up 2 levels from src/core/)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def generate_all_sequences():
    # Load the database using the correct dynamic path
    db_path = ROOT_DIR / "data" / "parsed" / "chords_normalized.json"
    if not db_path.exists():
        raise FileNotFoundError(f"Normalized database not found at: {db_path}")
        
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    chords = data["chords"]
    progressions = data["progressions"]
    
    # Take all active chords (those that have transitions)
    active_chords = [c for c in progressions if len(progressions[c]) > 0]
    print(f"🎵 Active chords available: {len(active_chords)}")
    
    results = []
    
    # Algorithm for selecting starting chords
    for chord in sorted(active_chords)[:115]:  
        seq = [chord]
        current = chord
        used = {chord}
        
        # Progression length (6-10 chords randomly)
        length = random.randint(6, 10)
        
        for step in range(length - 1):
            options = progressions.get(current, [])
            
            # Filter repeats
            options = [opt for opt in options if opt['name'] not in used]
            
            if not options:
                break
            
            # Select a random transition
            chosen = random.choice(options)
            seq.append(chosen['name'])
            used.add(chosen['name'])
            current = chosen['name']
        
        chord_info = chords.get(chord, {})
        results.append({
            "start_chord": chord,
            "function": chord_info.get("function", "unknown"),
            "sequence": seq,
            "length": len(seq),
            "transitions": [
                {
                    "from": seq[i],
                    "to": seq[i+1],
                    "tension": next(
                        (p.get("tension", "?") for p in progressions.get(seq[i], []) 
                         if p['name'] == seq[i+1]),
                        "?"
                    )
                }
                for i in range(len(seq) - 1)
            ]
        })
    
    return results

def format_sequence(seq, with_arrows=True):
    if with_arrows:
        return " → ".join(seq)
    return ", ".join(seq)

def print_sequences(results, format_type="simple"):
    if format_type == "simple":
        print("\n" + "="*70)
        print("🎵 115 HARMONIC SEQUENCES GENERATED")
        print("="*70)
        for i, r in enumerate(results, 1):
            print(f"\n{i:3d}. {r['start_chord']} ({r['function']})")
            print(f"     → {format_sequence(r['sequence'])}")
            print(f"     [{r['length']} chords]")
            
    elif format_type == "detailed":
        print("\n" + "="*70)
        print("🔍 DETAILED PROGRESSIONS WITH TENSION")
        print("="*70)
        for i, r in enumerate(results, 1):
            print(f"\n{i:3d}. {r['start_chord']} ({r['function']})")
            print(f"     {format_sequence(r['sequence'])}")
            print(f"     [{r['length']} chords]")
            tensions = [f"{t['from']}→{t['to']}: {t['tension']}" for t in r['transitions']]
            print(f"     Tension flow: {' | '.join(tensions)}")

def save_to_file(results):
    # Dynamic paths for saving text reports
    output_main = ROOT_DIR / "data" / "generated" / "115_sequences.txt"
    output_only = ROOT_DIR / "data" / "generated" / "sequences_only.txt"
    
    output_main.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_main, "w", encoding="utf-8") as f:
        f.write(f"🎵 115 HARMONIC SEQUENCES\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Based on 'The Chord Matrix' by Aaron Spacefood\n")
        f.write("="*70 + "\n\n")
        
        for i, r in enumerate(results, 1):
            f.write(f"{i:3d}. {r['start_chord']} ({r['function']})\n")
            f.write(f"     {format_sequence(r['sequence'])}\n")
            f.write(f"     [{r['length']} chords]\n")
            tensions = [f"{t['from']}→{t['to']}: {t['tension']}" for t in r['transitions']]
            f.write(f"     Tension flow: {' | '.join(tensions)}\n\n")
            
    with open(output_only, "w", encoding="utf-8") as f:
        for r in results:
            f.write(f"{' → '.join(r['sequence'])}\n")
            
    print(f"\n💾 Saved detailed report to: {output_main}")
    print(f"📁 Saved clean sequences text to: {output_only}")

def main():
    print("🎵 GENERATING 115 SMART HARMONIC PROGRESSIONS")
    print("="*70)
    results = generate_all_sequences()
    print(f"\n✅ Total simulated pipelines: {len(results)}")
    print_sequences(results, format_type="simple")
    save_to_file(results)
    print("\n🎉 DONE! READY FOR MIDI EXPORT! 🔥")

if __name__ == "__main__":
    main()
