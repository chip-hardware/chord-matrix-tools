import json
from collections import Counter
from pathlib import Path

# Dynamically determine the project root (go up 3 levels from src/cli/analyze_db.py)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def analyze_database():
    # Use the normalized database for accurate analytics
    db_path = ROOT_DIR / "data" / "parsed" / "chords_normalized.json"
    
    # If normalized doesn't exist, try the base one
    if not db_path.exists():
        db_path = ROOT_DIR / "data" / "parsed" / "chords.json"
        
    if not db_path.exists():
        print(f"❌ Database not found! Please run parser first. Searched path: {db_path}")
        return

    print(f"📖 Analyzing database file: {db_path.name}")
    print("=" * 60)

    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chords = data["chords"]
    progressions = data["progressions"]

    # 1. Top chords by number of outgoing transitions
    print("\n🏆 TOP-10 Chords by outgoing transitions count:")
    print("-" * 45)
    sorted_chords = sorted(progressions.items(), key=lambda x: len(x[1]), reverse=True)
    for i, (name, prog) in enumerate(sorted_chords[:10], 1):
        print(f"  {i:2d}. {name:<10} : {len(prog)} transitions")

    # 2. Find Dead Ends
    print("\n🔍 Dead-End Chords (Have entry points, but NO exit transitions):")
    print("-" * 45)
    chord_names = set(chords.keys())
    prog_names = set(progressions.keys())
    dead_ends = chord_names - prog_names
    
    if dead_ends:
        for name in sorted(dead_ends)[:15]:  # show a bit more, up to 15
            print(f"  • {name}")
        if len(dead_ends) > 15:
            print(f"  ... and {len(dead_ends) - 15} more dead ends.")
    else:
        print("  🟢 Perfect! No dead-end chords found in this database.")

    # 3. Most popular target chords (where they go most often)
    print("\n🎯 TOP-10 Most popular target chords (Inbound traffic):")
    print("-" * 45)
    targets = []
    for prog in progressions.values():
        for p in prog:
            targets.append(p['name'])
            
    target_counts = Counter(targets)
    for i, (name, count) in enumerate(target_counts.most_common(10), 1):
        print(f"  {i:2d}. {name:<10} : targeted {count} times")
    print("=" * 60)

if __name__ == "__main__":
    analyze_database()
