import json
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import random

class ChordDatabase:
    def __init__(self, data_path: str = None):
        self.chords = {}
        self.progressions = defaultdict(list)
        self.tonalities = {}
        
        if data_path:
            self.load(data_path)
    
    def load(self, data_path: str):
        """Loads the database from JSON"""
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.chords = data.get('chords', {})
            self.progressions = data.get('progressions', defaultdict(list))
            self.tonalities = data.get('tonalities', {})
    
    def save(self, data_path: str):
        """Saves the database to JSON"""
        data = {
            'chords': self.chords,
            'progressions': dict(self.progressions),
            'tonalities': self.tonalities
        }
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_chord(self, name: str) -> Optional[Dict]:
        """Retrieves chord information"""
        return self.chords.get(name)
    
    def get_next_chords(self, chord_name: str) -> List[Dict]:
        """Retrieves all possible next chords"""
        return self.progressions.get(chord_name, [])
    
    def get_next_by_criteria(self, chord_name: str, **criteria) -> List[Dict]:
        """Retrieves next chords by criteria"""
        options = self.get_next_chords(chord_name)
        filtered = options
        
        for key, value in criteria.items():
            if key == 'mood':
                filtered = [opt for opt in filtered 
                           if value.lower() in opt.get('mood', '').lower()]
            elif key == 'tension':
                filtered = [opt for opt in filtered 
                           if opt.get('tension') == value]
            elif key == 'function':
                filtered = [opt for opt in filtered 
                           if opt.get('function') == value]
            elif key == 'max_tension':
                t_value = int(value[1]) if value.startswith('T') else None
                if t_value:
                    filtered = [opt for opt in filtered 
                               if int(opt.get('tension', 'T0')[1]) <= t_value]
        
        return filtered
