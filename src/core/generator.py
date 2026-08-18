import random
from typing import List, Dict, Optional, Tuple
from .chord_db import ChordDatabase

class HarmonyGenerator:
    def __init__(self, db: ChordDatabase):
        self.db = db
        self.sequence = []
    
    def generate_sequence(
        self,
        start_chord: str,
        length: int = 8,
        mood: Optional[str] = None,
        tension_range: Optional[Tuple[int, int]] = None,
        end_chord: Optional[str] = None,
        avoid_repeats: bool = True,
        random_seed: Optional[int] = None
    ) -> List[str]:
        """
        Generates a harmonic progression
        
        Args:
            start_chord: Starting chord
            length: Length of the progression
            mood: Mood (dark, bright, mysterious, etc.)
            tension_range: Tension range (T1-T5)
            end_chord: Final chord (if specified)
            avoid_repeats: Avoid repetitions
            random_seed: Seed for reproducibility
        """
        if random_seed:
            random.seed(random_seed)
        
        sequence = [start_chord]
        current = start_chord
        
        for i in range(length - 1):
            # Get possible next chords
            options = self.db.get_next_chords(current)
            
            if not options:
                break
            
            # Filter by mood
            if mood:
                options = [opt for opt in options 
                          if mood.lower() in opt.get('mood', '').lower()]
            
            # Filter by tension
            if tension_range:
                min_t, max_t = tension_range
                options = [opt for opt in options 
                          if self._tension_value(opt.get('tension')) in range(min_t, max_t + 1)]
            
            # Avoid repeats
            if avoid_repeats and len(sequence) > 1:
                options = [opt for opt in options 
                          if opt['name'] != sequence[-1]]
            
            # Select randomly
            if not options:
                # If no options, take any available
                options = self.db.get_next_chords(current)
            
            # Weighted selection (prefer chords with lower tension)
            selected = self._weighted_choice(options)
            current = selected['name']
            sequence.append(current)
            
            # If we reached the final chord
            if end_chord and len(sequence) >= 2 and random.random() < 0.3:
                # Check if we can transition to end_chord
                possible = self.db.get_next_chords(current)
                if any(opt['name'] == end_chord for opt in possible):
                    sequence.append(end_chord)
                    break
        
        return sequence
    
    def generate_multiple(
        self,
        start_chord: str,
        count: int = 10,
        **kwargs
    ) -> List[List[str]]:
        """Generates multiple progressions"""
        sequences = []
        for _ in range(count):
            seq = self.generate_sequence(start_chord, **kwargs)
            sequences.append(seq)
        return sequences
    
    def _tension_value(self, tension: str) -> int:
        """Converts T1, T2, ... to a number"""
        if not tension:
            return 0
        try:
            return int(tension[1])
        except:
            return 0
    
    def _weighted_choice(self, options: List[Dict]) -> Dict:
        """Selects a chord with weight based on tension"""
        if not options:
            return None
        
        # Lower tension = higher weight
        weights = []
        for opt in options:
            t = self._tension_value(opt.get('tension'))
            weight = max(1, 5 - t)  # T1=5, T2=4, T3=3, T4=2, T5=1
            weights.append(weight)
        
        return random.choices(options, weights=weights, k=1)[0]
