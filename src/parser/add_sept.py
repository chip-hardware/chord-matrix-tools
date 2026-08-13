import json
from pathlib import Path

# Динамічно визначаємо корінь проєкту (на 2 рівні вгору від src/parser/)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def extend_triads_to_sevenths():
    db_path = ROOT_DIR / "data" / "parsed" / "chords_normalized.json"
    backup_path = db_path.with_suffix(".json.bak")
    
    if not db_path.exists():
        print(f"❌ Database not found at: {db_path}. Please run normalization first.")
        return

    # Створюємо резервну копію перед мутацією
    import shutil
    shutil.copy(str(db_path), str(backup_path))
    print(f"✅ Created a safe database backup at: {backup_path.name}")

    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chords = data["chords"]
    progressions = data["progressions"]

    # Явний маппінг: тризвук -> його септакорди
    chord_family = {}
    for chord in chords.keys():
        if not any(chord.endswith(x) for x in ['7', 'maj7', 'min7', 'dim7']):
            chord_family[chord] = {
                'maj7': f"{chord}maj7" if f"{chord}maj7" in chords else None,
                'min7': f"{chord}min7" if f"{chord}min7" in chords else None,
                '7': f"{chord}7" if f"{chord}7" in chords else None,
                'dim7': f"{chord}dim7" if f"{chord}dim7" in chords else None,
            }

    print(f"📊 Found {len(chord_family)} chord families.")

    added = 0
    for triad, family in chord_family.items():
        if triad not in progressions or len(progressions[triad]) == 0:
            continue
        
        for quality, seventh in family.items():
            if seventh and seventh in chords:
                if seventh not in progressions or len(progressions[seventh]) == 0:
                    progressions[seventh] = []
                
                for p in progressions[triad]:
                    if p['name'] not in [x['name'] for x in progressions[seventh]]:
                        progressions[seventh].append({
                            "name": p['name'],
                            "tension": p.get("tension", "T1 5"),
                            "description": f"from {seventh} (inherited from {triad})",
                            "page": p.get("page", 0)
                        })
                        added += 1

    print(f"✅ Injected {added} transitions for 7th chords.")

    data["progressions"] = progressions
    data["total_transitions"] = sum(len(v) for v in progressions.values())

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 Database successfully updated and written to {db_path.name}!")

if __name__ == "__main__":
    extend_triads_to_sevenths()
