import re
import json
from pathlib import Path
from typing import Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class ChordParser:
    def __init__(self):
        self.chords = {}
        self.progressions = {}
    
    def clean_text(self, text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()
    
    def extract_chord_name(self, text: str) -> Optional[str]:
        patterns = [
            r'([A-G][#b]?)\s+(MAJ|MIN|DIM|AUG|MAJOR|MINOR)',
            r'([A-G][#b]?)(MAJ|MIN|DIM|AUG|maj|min|dim|aug)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                root = match.group(1)
                quality = match.group(2).lower()
                if quality in ['maj', 'major']: return f"{root}maj"
                elif quality in ['min', 'minor']: return f"{root}min"
                elif quality in ['dim', 'aug']: return f"{root}{quality}"
        return None
    
    def parse_page(self, content: str, page_num: int) -> Dict:
        result = {"page": page_num, "function": None, "tonic": None, "description": None, "next_chords": []}
        
        func_match = re.search(r'^(TONIC|SUBDOMINANT|DOMINANT|SUPER-TONIC|SUPERTONIC|MEDIANT|SUBMEDIANT|SUB-TONIC|SUBTONIC|LEADING-TONE)', content, re.MULTILINE | re.IGNORECASE)
        if func_match:
            result["function"] = func_match.group(1).upper()
        
        result["tonic"] = self.extract_chord_name(content)
        
        func_desc_match = re.search(r'FUNCTION:\s*([^.]+\.)', content, re.IGNORECASE)
        if func_desc_match:
            result["description"] = re.sub(r'[lI|]+', '', func_desc_match.group(1)).strip()
        
        next_pattern = r'([A-G][#b]?(?:MAJ|MIN|DIM|AUG|M|m|7|M7|m7|maj7|min7)?)\s+.*?T([1-5])\s+([0-9])\s+(\d{1,4})'
        for match in re.finditer(next_pattern, content, re.IGNORECASE):
            chord_name = match.group(1).upper()
            if chord_name and len(chord_name) <= 10:
                result["next_chords"].append({
                    "name": chord_name,
                    "description": "",
                    "tension": f"T{match.group(2)}{match.group(3)}",
                    "page": int(match.group(4))
                })
        
        if not result["next_chords"]:
            simple_pattern = r'([A-G][#b]?(?:MAJ|MIN|DIM|AUG|M|m|7|M7|m7|maj7|min7)?)\s+T([1-5])\s+([0-9])\s+(\d{1,4})'
            for match in re.finditer(simple_pattern, content, re.IGNORECASE):
                chord_name = match.group(1).upper()
                if chord_name and len(chord_name) <= 10:
                    result["next_chords"].append({
                        "name": chord_name,
                        "description": "",
                        "tension": f"T{match.group(2)}{match.group(3)}",
                        "page": int(match.group(4))
                    })
        return result

def main():
    input_file = ROOT_DIR / "data" / "raw" / "extracted_text.txt"
    output_file = ROOT_DIR / "data" / "parsed" / "chords.json"
    
    if not input_file.exists():
        print(f"❌ Source raw file not found at: {input_file}")
        return
    
    print(f"📖 Loading text from: {input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    page_pattern = r"--- PAGE (\d+) ---\n(.*?)(?=\n--- PAGE \d+ ---|\Z)"
    parser = ChordParser()
    all_chords, all_progressions = {}, {}
    processed, failed = 0, 0
    
    for match in re.finditer(page_pattern, text, re.DOTALL):
        page_num = int(match.group(1))
        content = match.group(2)
        
        if "FUNCTION:" in content and "NEXT CHORD" in content:
            try:
                result = parser.parse_page(content, page_num)
                if result["tonic"] and result["function"]:
                    chord_name = result["tonic"]
                    if chord_name not in all_chords:
                        all_chords[chord_name] = {"page": page_num, "function": result["function"], "description": result["description"] or ""}
                    
                    if result["next_chords"]:
                        if chord_name not in all_progressions: all_progressions[chord_name] = []
                        existing_names = {p['name'] for p in all_progressions[chord_name]}
                        for p in result["next_chords"]:
                            if p['name'] not in existing_names:
                                all_progressions[chord_name].append(p)
                                existing_names.add(p['name'])
                    processed += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output = {"chords": all_chords, "progressions": all_progressions, "total_chords": len(all_chords), "successful_pages": processed, "failed_pages": failed}
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"🎉 Parsing finalized! Saved to {output_file}")

if __name__ == "__main__":
    main()
