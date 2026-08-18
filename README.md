# Chord Matrix Tools 🎵

A Python toolkit to automate harmonic progression generation based on the musical concepts from the book **"The Chord Matrix"** by Aaron Spacefood.

---

### ⚠️ Legal Disclaimer
This repository contains **only programmatic code**. It **DOES NOT** contain the original book text, images, or PDF files to prevent copyright issues.

---

### 🚀 Quick Start (How to run)

1. **Install dependencies** (run once):
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the main controller menu**:
   ```bash
   python run.py
   ```

3. **Standard Pipeline Execution Order** inside the menu:
   * **Press 1** — Normalize raw chords database *(fixes flat notations and typos)*.
   * **Press 2** — Extend transitions from basic triads to 7th chords.
   * **Press 4** — Generate smart harmonic sequences.
   * **Press 5** — Export generated sequences into playable MIDI files.

---

### 📁 Where to find the output files?

All results are automatically generated in the `data/generated/` directory:

* 📄 `data/generated/115_sequences.txt` — Detailed text report showing chord progressions and calculated tension levels.
* 📝 `data/generated/sequences_only.txt` — Clean text list of chord chains separated by arrows (`→`) for quick copy-pasting.
* 🎹 `data/generated/midi/` — Rendered `.mid` files. Drag and drop them directly onto any virtual instrument track in your DAW *(Ableton, FL Studio, Logic, etc.)*.

---

### 📊 Database Setup Guide (For manual edits)

If you need to update the source data, the system expects `data/parsed/chords_normalized.json` to follow this strict structure:

```json
{
  "chords": {
    "Cmin": { 
      "function": "tonic", 
      "page": 42, 
      "description": "Dark and tense" 
    }
  },
  "progressions": {
    "Cmin": [
      { 
        "name": "G7", 
        "tension": "T3", 
        "page": 43 
      }
    ]
  }
}
```

---

### 🧪 Running Tests

To check if the project paths and imports are functioning correctly without launching the main menu, run:

```bash
python tests/test_generator.py
```
