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
        Генерує гармонічну послідовність
        
        Args:
            start_chord: Початковий акорд
            length: Довжина послідовності
            mood: Настрій (dark, bright, mysterious, etc.)
            tension_range: Діапазон напруги (T1-T5)
            end_chord: Фінальний акорд (якщо вказано)
            avoid_repeats: Уникати повторень
            random_seed: Seed для відтворюваності
        """
        if random_seed:
            random.seed(random_seed)
        
        sequence = [start_chord]
        current = start_chord
        
        for i in range(length - 1):
            # Отримуємо можливі наступні акорди
            options = self.db.get_next_chords(current)
            
            if not options:
                break
            
            # Фільтруємо за настроєм
            if mood:
                options = [opt for opt in options 
                          if mood.lower() in opt.get('mood', '').lower()]
            
            # Фільтруємо за напругою
            if tension_range:
                min_t, max_t = tension_range
                options = [opt for opt in options 
                          if self._tension_value(opt.get('tension')) in range(min_t, max_t + 1)]
            
            # Уникаємо повторень
            if avoid_repeats and len(sequence) > 1:
                options = [opt for opt in options 
                          if opt['name'] != sequence[-1]]
            
            # Вибираємо випадковий
            if not options:
                # Якщо немає варіантів, беремо будь-який доступний
                options = self.db.get_next_chords(current)
            
            # Вагований вибір (надаємо перевагу акордам з меншою напругою)
            selected = self._weighted_choice(options)
            current = selected['name']
            sequence.append(current)
            
            # Якщо досягли фінального акорду
            if end_chord and len(sequence) >= 2 and random.random() < 0.3:
                # Перевіряємо, чи можна перейти до end_chord
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
        """Генерує декілька послідовностей"""
        sequences = []
        for _ in range(count):
            seq = self.generate_sequence(start_chord, **kwargs)
            sequences.append(seq)
        return sequences
    
    def _tension_value(self, tension: str) -> int:
        """Перетворює T1, T2, ... на число"""
        if not tension:
            return 0
        try:
            return int(tension[1])
        except:
            return 0
    
    def _weighted_choice(self, options: List[Dict]) -> Dict:
        """Вибирає акорд з вагою на основі напруги"""
        if not options:
            return None
        
        # Чим менша напруга, тим більша вага
        weights = []
        for opt in options:
            t = self._tension_value(opt.get('tension'))
            weight = max(1, 5 - t)  # T1=5, T2=4, T3=3, T4=2, T5=1
            weights.append(weight)
        
        return random.choices(options, weights=weights, k=1)[0]