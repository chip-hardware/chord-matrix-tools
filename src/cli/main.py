import click
import json
from pathlib import Path
# Імпортуємо ваш робочий генератор з ядра системи
from src.core.harmony_generator import SmartHarmonyGenerator
from src.export.export import export_sequence_to_midi

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

@click.group()
def cli():
    """🎵 Chord Matrix - Advanced Harmonic Progression CLI Tool"""
    pass

@cli.command()
@click.option('--start', '-s', required=True, help='Starting root chord (e.g., Cmin)')
@click.option('--length', '-l', default=8, help='Progression length (number of chords)')
@click.option('--tension', '-t', help='Filter transitions by tension level (T1-T5)')
@click.option('--count', '-c', default=5, help='Number of sequence variations to output')
@click.option('--export-midi', '-e', help='Base file name to export sequences to MIDI')
def generate(start, length, tension, count, export_midi):
    """Generates procedural harmonic progressions using the matrix database."""
    try:
        gen = SmartHarmonyGenerator()
    except FileNotFoundError as e:
        click.echo(f"❌ {e}")
        return
    
    # Визначаємо рівень напруги, якщо він заданий
    max_t = None
    if tension and tension.startswith('T'):
        try:
            max_t = int(tension[1])
        except ValueError:
            pass

    sequences = gen.generate_multiple(
        start_chord=start,
        length=length,
        max_tension=max_t,
        count=count
    )
    
    click.echo(f"\n🎵 Generated {len(sequences)} harmonic progressions:\n")
    for i, seq in enumerate(sequences, 1):
        click.echo(f"{i:2d}. {' → '.join(seq)}")
    
    if export_midi and sequences:
        midi_dir = ROOT_DIR / "data" / "generated" / "midi"
        midi_dir.mkdir(parents=True, exist_ok=True)
        
        for i, seq in enumerate(sequences):
            filename = midi_dir / f"{export_midi}_{i+1}.mid"
            export_sequence_to_midi(seq, filename)
        click.echo(f"\n🚀 Successfully exported {len(sequences)} MIDI files to: data/generated/midi/")

@cli.command()
@click.argument('chord')
def info(chord):
    """Shows full architectural database info for a single chord."""
    db_path = ROOT_DIR / "data" / "parsed" / "chords_normalized.json"
    if not db_path.exists():
        click.echo("❌ Database not found. Run the parser pipeline first.")
        return
        
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    chords = data.get("chords", {})
    progressions = data.get("progressions", {})
    
    # Нормалізуємо введення
    chord_key = chord.lower().capitalize()
    
    if chord_key in chords:
        info_data = chords[chord_key]
        click.echo(f"\n🎵 Chord: {chord_key}")
        click.echo(f"  • Harmonic Function : {info_data.get('function', 'unknown').upper()}")
        click.echo(f"  • Book Origin Page  : Page {info_data.get('page', 'unknown')}")
        click.echo(f"  • Description       : {info_data.get('description', 'No description available')}")
        
        next_chords = progressions.get(chord_key, [])
        if next_chords:
            click.echo("\n🔗 Available Transitions:")
            for nc in next_chords[:8]:  # Показуємо перші 8 переходів
                click.echo(f"    → {nc['name']:<8} [Tension: {nc.get('tension', '?')}]")
    else:
        click.echo(f"❌ Chord '{chord}' not found in the parsed database matrix.")

if __name__ == '__main__':
    cli()
