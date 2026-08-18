import os
import sys
import subprocess
from pathlib import Path

# Define the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent

def print_menu():
    print("\n" + "="*50)
    print("      CHORD MATRIX TOOLS - CLI MENU      ")
    print("="*50)
    print("1. [Parser] Normalize Raw Chords (Fix flats/enharmonics)")
    print("2. [Parser] Add Septachords Extensions")
    print("3. [Core]   Analyze Database Analytics & Dead Ends")
    print("4. [Core]   Generate 115 Harmonic Sequences")
    print("5. [Export] Export Generated Sequences to MIDI")
    print("6. Exit")
    print("="*50)

def run_script(script_path):
    try:
        script_abs_path = ROOT_DIR / script_path
        if not script_abs_path.exists():
            print(f"\n❌ [Error] Script not found at: {script_path}")
            return
            
        script_dir = script_abs_path.parent
        script_name = script_abs_path.name
        
        # Run the script in its own directory to prevent relative path breakage
        subprocess.run([sys.executable, script_name], cwd=script_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ [Error] Script failure: {e}")
    except Exception as e:
        print(f"\n❌ [Error] Unexpected issue: {e}")

def main():
    while True:
        print_menu()
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            print("\n[Running] Normalizing chords data...")
            run_script("src/parser/normalize_chords.py")
        elif choice == '2':
            print("\n[Running] Extending triads to 7th chords...")
            run_script("src/parser/add_sept.py")
        elif choice == '3':
            print("\n[Running] Analyzing chord transitions graph...")
            run_script("src/cli/analyze_db.py")
        elif choice == '4':
            print("\n[Running] Simulating 115 smart sequences...")
            run_script("src/core/115.py")
        elif choice == '5':
            print("\n[Running] Converting text chains to MIDI files...")
            run_script("src/export/export.py")
        elif choice == '6':
            print("\nThank you for using Chord Matrix Tools. Goodbye! 🎵")
            break
        else:
            print("\n[Invalid] Please select a number between 1 and 6.")

if __name__ == "__main__":
    main()
