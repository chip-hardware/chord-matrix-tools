import os

# Структура проекту (папки та порожні файли)
structure = [
    # Папки з .gitkeep
    "data/raw/.gitkeep",
    "data/parsed/.gitkeep",
    "data/generated/.gitkeep",
    
    # src/parser/
    "src/parser/__init__.py",
    "src/parser/pdf_extractor.py",
    "src/parser/chord_parser.py",
    "src/parser/glossary_parser.py",
    
    # src/core/
    "src/core/__init__.py",
    "src/core/chord_db.py",
    "src/core/generator.py",
    "src/core/filters.py",
    
    # src/export/
    "src/export/__init__.py",
    "src/export/midi_exporter.py",
    "src/export/text_exporter.py",
    
    # src/cli/
    "src/cli/__init__.py",
    "src/cli/main.py",
    
    # tests/
    "tests/__init__.py",
    "tests/test_parser.py",
    "tests/test_generator.py",
    
    # Кореневі файли
    "README.md",
    "requirements.txt",
    "run.py",
]

def create_structure():
    print("🚀 Створення структури проекту...")
    print("=" * 50)
    
    for path in structure:
        # Отримуємо папку для файлу
        dirname = os.path.dirname(path)
        
        # Створюємо папку, якщо вона є (не порожня)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        
        # Створюємо порожній файл
        with open(path, "w", encoding="utf-8") as f:
            pass  # просто створюємо порожній файл
        
        print(f"✅ {path}")
    
    print("=" * 50)
    print("🎉 Структуру створено!")
    print("""
📁 Отримана структура:
chord_matrix_project/
├── data/
│   ├── raw/
│   ├── parsed/
│   └── generated/
├── src/
│   ├── parser/
│   ├── core/
│   ├── export/
│   └── cli/
├── tests/
├── README.md
├── requirements.txt
└── run.py

Тепер можете заповнювати файли вручну.
    """)

if __name__ == "__main__":
    create_structure()