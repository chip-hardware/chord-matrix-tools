import sys
from pathlib import Path
import unittest

# Add the project root to Python's search path (sys.path)
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

try:
    from src.core.harmony_generator import SmartHarmonyGenerator
except ModuleNotFoundError as e:
    print(f"❌ Critical import error! Python cannot see src modules: {e}")
    print(f"Current sys.path contains: {sys.path}")
    sys.exit(1)

class TestChordMatrixCore(unittest.TestCase):
    def test_generator_initialization(self):
        """Checks if the generator initializes successfully and sees the database"""
        try:
            gen = SmartHarmonyGenerator()
            self.assertIsNotNone(gen.chords)
            self.assertTrue(len(gen.chords) > 0)
            print("\n🟢 Database test: SUCCESS (chords_normalized.json loaded)")
        except FileNotFoundError as e:
            self.fail(f"❌ Test failed: Database file not found! {e}")

    def test_sequence_generation(self):
        """Checks if a chord progression is generated"""
        gen = SmartHarmonyGenerator()
        if gen.active_chords:
            start_chord = list(gen.active_chords)[0]
            seq = gen.generate_sequence(start_chord, length=6)
            self.assertTrue(len(seq) > 0)
            self.assertEqual(seq[0], start_chord)
            print(f"🟢 Generation test: SUCCESS (Generated progression for {start_chord})")
        else:
            print("⚠️ No active chords available for generation test.")

if __name__ == "__main__":
    print("🧪 Running core express tests (unittest)...")
    print("=" * 50)
    unittest.main()
