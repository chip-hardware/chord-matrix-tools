import sys
from pathlib import Path
import unittest

# Додаємо корінь проєкту в лінії пошуку Python (sys.path)
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

try:
    from src.core.harmony_generator import SmartHarmonyGenerator
except ModuleNotFoundError as e:
    print(f"❌ Критична помилка імпорту! Python не бачить модулі src: {e}")
    print(f"Поточний sys.path містить: {sys.path}")
    sys.exit(1)

class TestChordMatrixCore(unittest.TestCase):
    def test_generator_initialization(self):
        """Перевіряє, чи успішно ініціалізується генератор та чи бачить базу даних"""
        try:
            gen = SmartHarmonyGenerator()
            self.assertIsNotNone(gen.chords)
            self.assertTrue(len(gen.chords) > 0)
            print("\n🟢 Тест бази даних: УСПІШНО (База chords_normalized.json завантажена)")
        except FileNotFoundError as e:
            self.fail(f"❌ Тест провалено: Файл бази даних не знайдено! {e}")

    def test_sequence_generation(self):
        """Перевіряє, чи генерується ланцюжок акордів"""
        gen = SmartHarmonyGenerator()
        if gen.active_chords:
            start_chord = list(gen.active_chords)[0]
            seq = gen.generate_sequence(start_chord, length=6)
            self.assertTrue(len(seq) > 0)
            self.assertEqual(seq[0], start_chord)
            print(f"🟢 Тест генерації: УСПІШНО (Згенеровано ланцюжок для {start_chord})")
        else:
            print("⚠️ Немає активних акордів для тесту генерації.")

if __name__ == "__main__":
    print("🧪 Запуск експрес-тестів ядра (unittest)...")
    print("=" * 50)
    unittest.main()
