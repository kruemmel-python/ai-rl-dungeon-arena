# AI Reinforcement Learning Dungeon Arena

[![GitHub](https://img.shields.io/github/license/kruemmel-python/ai-rl-dungeon-arena)](https://github.com/kruemmel-python/ai-rl-dungeon-arena/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/kruemmel-python/ai-rl-dungeon-arena)](https://github.com/kruemmel-python/ai-rl-dungeon-arena/issues)

## Projektübersicht

**AI-RL-Dungeon-Arena** ist ein hochdynamisches und interaktives KI-Projekt, das die Leistungsfähigkeit von Deep Reinforcement Learning (DRL) in einer spielbasierten Umgebung demonstriert. Es simuliert Kämpfe zwischen einer Gruppe von Spielern und einem Boss-Gegner in einem voxelbasierten Dungeon.

### Funktionen
- **Spielerklassen**: Unterstützung für acht Spielerklassen (z. B. Tank, Heiler, verschiedene DPS-Typen).
- **Boss-AI**: Dynamische Boss-KI mit mehreren Phasen und Spezialfähigkeiten.
- **Deep Reinforcement Learning**: Verwendung von Double Deep Q-Learning für die Spieler- und Boss-KI.
- **Priorisierte Erfahrungsspeicherung**: Verbesserung der Trainingsstabilität und Effizienz.
- **Anpassbare Umgebung**: Konfigurierbare Parameter wie Spielfeldgröße, Anzahl der Spieler und Feinde.

## Projektstruktur

Das Projekt umfasst mehrere Module, die unterschiedliche Aspekte des Spiels abdecken:

```plaintext
ai-rl-dungeon-arena/
├── agents.py            # Deep Reinforcement Learning-Agenten
├── boss_actions.py      # Aktionen und Logik der Boss-Charaktere
├── config.py            # Globale Konfigurationsparameter
├── entities.py          # Definition der Spielfiguren (Spieler, Boss, Adds)
├── environment.py       # Umgebungslogik und Spielfluss
├── main.py              # Hauptskript für Trainings- und Testläufe
├── replay_buffer.py     # Implementierung des Replay Buffers
├── tank_actions.py      # Spezifische Tank-Aktionen
├── healer_actions.py    # Spezifische Heiler-Aktionen
└── ...                  # Weitere Aktionsdateien für Klassen
```

## Installation

1. **Projekt klonen**:
   ```bash
   git clone https://github.com/kruemmel-python/ai-rl-dungeon-arena.git
   cd ai-rl-dungeon-arena
   ```

2. **Abhängigkeiten installieren**:
   Python 3.12 oder höher ist erforderlich. Installieren Sie die erforderlichen Bibliotheken mit:
   ```bash
   pip install -r requirements.txt
   ```

3. **Optionale GPU-Unterstützung**:
   Falls Sie eine NVIDIA-GPU verwenden möchten, stellen Sie sicher, dass TensorFlow mit GPU-Unterstützung installiert ist.

## Verwendung

### Training
Das Hauptskript startet das Training der Spieler- und Boss-Agenten:
```bash
python main.py
```

### Modelle speichern und laden
- Modelle werden automatisch im Verzeichnis gespeichert und geladen (`MODEL_PATH` und `BOSS_MODEL_PATH` in `config.py`).

### Konfiguration anpassen
Ändern Sie die Parameter in der Datei `config.py`, um das Verhalten der Simulation anzupassen (z. B. Anzahl der Spieler, Spielfeldgröße, Lernrate).

## Spielerklassen und Aktionen

Jede Spielerklasse hat spezifische Aktionen und Fähigkeiten. Hier ein Überblick über die Klassen und ihre Fähigkeiten:

- **Tank**: Fokus auf Verteidigung und Schadensvermeidung.
- **Healer**: Heilung und Unterstützung der Gruppe.
- **DPS (Nah- und Fernkampf)**: Verursachen von maximalem Schaden.

### Beispiel: Tank-Fähigkeiten
```python
CLASS_ACTIONS = {
    "tank": {
        "melee_attacks": ["taunt", "shield_bash", "heavy_strike", "block", "sweep"],
        "ranged_attacks": ["chucking_shield", "shattering_throw"],
        "buffs": ["fortify", "last_stand"],
        "dots": ["rupture", "bleed"],
        "unique": "avenger_shield"
    }
}
```

## Reinforcement-Learning-Methodik

Das Projekt verwendet die folgende Architektur:

1. **Double Deep Q-Learning**: Reduziert die Überbewertung von Q-Werten und verbessert die Stabilität.
2. **Priorisierte Replay-Speicherung**: Ermöglicht das Sampling von wichtigen Erfahrungen basierend auf Fehlerprioritäten.
3. **Target-Netzwerk-Updates**: Regelmäßige Aktualisierung der Zielnetzwerke zur Stabilisierung des Lernens.

## Mitwirken
Beiträge zum Projekt sind willkommen! Bitte eröffnen Sie ein Issue oder senden Sie einen Pull-Request.

### To-Do-Liste
- Verbesserung der Aktionslogik für spezialisierte Klassen.
- Optimierung der Trainingszeit durch Hyperparameter-Tuning.
- Erweiterung der Umgebung um zusätzliche Gegner und Mechaniken.

## Lizenz
Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen finden Sie in der Datei `LICENSE`.

## Autor
**Ralf Krümmel**

- [GitHub-Profil](https://github.com/kruemmel-python)
- Kontakt: [Email](mailto:ralf.kruemmel@example.com)

---

Vielen Dank für Ihr Interesse an **AI-RL-Dungeon-Arena**! Wir freuen uns auf Ihr Feedback und Ihre Beiträge.

