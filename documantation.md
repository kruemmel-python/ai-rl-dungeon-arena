### Config Module Documentation

**Name des Moduls:** config

**Beschreibung:** Das Config-Modul enthält Konfigurationsparameter und globale Attribute, die für die Initialisierung und das Verhalten der Umgebung und Agenten verwendet werden.

### Einführung
- **Name des Moduls:** config
- **Beschreibung:** Das Config-Modul enthält Konfigurationsparameter und globale Attribute, die für die Initialisierung und das Verhalten der Umgebung und Agenten verwendet werden.

### Globale Attribute
| Name des Attributs | Datentyp | Beschreibung |
|---------------------|----------|-------------|
| WIDTH | int | Die Breite des Spielfelds. |
| HEIGHT | int | Die Höhe des Spielfelds. |
| GRID_SIZE | int | Die Größe des Rasters. |
| CELL_SIZE | int | Die Größe einer Zelle im Raster. |
| NUM_EPISODES | int | Die Anzahl der Episoden. |
| BATCH_SIZE | int | Die Größe eines Batches. |
| LEARNING_RATE | float | Die Lernrate. |
| GAMMA | float | Der Diskontfaktor. |
| EPSILON_START | float | Der Startwert für Epsilon. |
| EPSILON_MIN | float | Der minimale Wert für Epsilon. |
| EPSILON_DECAY_RATE | float | Die Abnahmerate für Epsilon. |
| TARGET_UPDATE_FREQ | int | Die Häufigkeit der Zielaktualisierung. |
| MODEL_PATH | str | Der Pfad zum Modell. |
| BOSS_MODEL_PATH | str | Der Pfad zum Boss-Modell. |
| PRIORITIZED_REPLAY_EPS | float | Der Epsilon-Wert für priorisiertes Replay. |
| MEMORY_SIZE_MAX | int | Die maximale Größe des Speichers. |
| MAX_PLAYERS | int | Die maximale Anzahl der Spieler. |
| MAX_ENEMIES | int | Die maximale Anzahl der Gegner. |
| MOVE_SPEED | int | Die Bewegungsgeschwindigkeit. |
| PLAYER_CLASSES | list | Die Liste der Spielerklassen. |
| NUM_PLAYER_CLASSES | int | Die Anzahl der Spielerklassen. |
| CLASS_ACTIONS | dict | Die Aktionen jeder Klasse. |
| ACTIONS | list | Die Liste aller Aktionen. |
| NUM_ACTIONS | int | Die Anzahl der Aktionen. |
| BOSS_ACTIONS | dict | Die Aktionen des Bosses. |
| NUM_BOSS_ACTIONS | int | Die Anzahl der Boss-Aktionen. |
| REWARD_KILL_BOSS | int | Die Belohnung für das Töten des Bosses. |
| REWARD_KILL_ADD | int | Die Belohnung für das Töten eines Adds. |
| PENALTY_PLAYER_DEATH | int | Die Strafe für den Tod eines Spielers. |
| PENALTY_BOSS_HIT_PLAYER | int | Die Strafe, wenn der Boss einen Spieler trifft. |
| REWARD_STEP | float | Die Belohnung pro Schritt. |
| REWARD_HIT_BOSS | int | Die Belohnung für das Treffen des Bosses. |
| REWARD_HEAL_PLAYER | int | Die Belohnung für das Heilen eines Spielers. |
| REWARD_MOVE_TOWARDS_BOSS | float | Die Belohnung für das Bewegen in Richtung des Bosses. |

### Entities Module Documentation

**Name des Moduls:** entities

**Beschreibung:** Das Entities-Modul enthält die Klassen für Spieler, Bosse und Adds, die in der Umgebung interagieren.

### Einführung
- **Name des Moduls:** entities
- **Beschreibung:** Das Entities-Modul enthält die Klassen für Spieler, Bosse und Adds, die in der Umgebung interagieren.

### Klassen

#### Player
- **Beschreibung:** Die Klasse Player repräsentiert einen Spieler im Spiel.
- **Attribute:**
  - **player_class** (str): Die Klasse des Spielers.
  - **x** (int): Die x-Koordinate des Spielers.
  - **y** (int): Die y-Koordinate des Spielers.
  - **max_hp** (int): Die maximale Gesundheit des Spielers.
  - **hp** (int): Die aktuelle Gesundheit des Spielers.
  - **is_dead** (bool): Gibt an, ob der Spieler tot ist.
  - **last_shot_time** (int): Die Zeit des letzten Schusses.
  - **target_boss** (bool): Gibt an, ob der Spieler den Boss angreift.
  - **recent_actions** (list): Die Liste der letzten Aktionen des Spielers.
- **Methoden:**
  - **__init__(player_class, x, y)**
    - **Beschreibung:** Initialisiert die Player-Klasse.
    - **Parameter:**
      - **player_class** (str): Die Klasse des Spielers.
      - **x** (int): Die x-Koordinate des Spielers.
      - **y** (int): Die y-Koordinate des Spielers.
    - **Rückgabewert:** None
  - **take_damage(damage)**
    - **Beschreibung:** Der Spieler nimmt Schaden.
    - **Parameter:**
      - **damage** (int): Der Schaden, den der Spieler nimmt.
    - **Rückgabewert:** None
  - **move(target_x, target_y)**
    - **Beschreibung:** Bewegt den Spieler zu den angegebenen Koordinaten.
    - **Parameter:**
      - **target_x** (int): Die x-Koordinate des Ziels.
      - **target_y** (int): Die y-Koordinate des Ziels.
    - **Rückgabewert:** None

#### Boss
- **Beschreibung:** Die Klasse Boss repräsentiert den Boss im Spiel.
- **Attribute:**
  - **x** (int): Die x-Koordinate des Bosses.
  - **y** (int): Die y-Koordinate des Bosses.
  - **max_hp** (int): Die maximale Gesundheit des Bosses.
  - **hp** (int): Die aktuelle Gesundheit des Bosses.
  - **is_enraged** (bool): Gibt an, ob der Boss wütend ist.
  - **enrage_timer** (int): Der Timer für die Wut des Bosses.
  - **phase** (int): Die Phase des Bosses.
  - **last_shot_time** (int): Die Zeit des letzten Schusses.
  - **target_player** (Player): Das Ziel des Bosses.
- **Methoden:**
  - **__init__(x, y)**
    - **Beschreibung:** Initialisiert die Boss-Klasse.
    - **Parameter:**
      - **x** (int): Die x-Koordinate des Bosses.
      - **y** (int): Die y-Koordinate des Bosses.
    - **Rückgabewert:** None
  - **take_damage(damage)**
    - **Beschreibung:** Der Boss nimmt Schaden.
    - **Parameter:**
      - **damage** (int): Der Schaden, den der Boss nimmt.
    - **Rückgabewert:** None
  - **check_phase()**
    - **Beschreibung:** Überprüft die Phase des Bosses.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **move(players)**
    - **Beschreibung:** Bewegt den Boss zu den angegebenen Koordinaten.
    - **Parameter:**
      - **players** (list): Die Liste der Spieler.
    - **Rückgabewert:** None
  - **get_closest_player(players)**
    - **Beschreibung:** Gibt den nächsten Spieler zurück.
    - **Parameter:**
      - **players** (list): Die Liste der Spieler.
    - **Rückgabewert:** Player

#### Add
- **Beschreibung:** Die Klasse Add repräsentiert ein Add im Spiel.
- **Attribute:**
  - **x** (int): Die x-Koordinate des Adds.
  - **y** (int): Die y-Koordinate des Adds.
  - **max_hp** (int): Die maximale Gesundheit des Adds.
  - **hp** (int): Die aktuelle Gesundheit des Adds.
  - **last_shot_time** (int): Die Zeit des letzten Schusses.
  - **target_player** (Player): Das Ziel des Adds.
- **Methoden:**
  - **__init__(x, y)**
    - **Beschreibung:** Initialisiert die Add-Klasse.
    - **Parameter:**
      - **x** (int): Die x-Koordinate des Adds.
      - **y** (int): Die y-Koordinate des Adds.
    - **Rückgabewert:** None
  - **take_damage(damage)**
    - **Beschreibung:** Das Add nimmt Schaden.
    - **Parameter:**
      - **damage** (int): Der Schaden, den das Add nimmt.
    - **Rückgabewert:** None
  - **move(players)**
    - **Beschreibung:** Bewegt das Add zu den angegebenen Koordinaten.
    - **Parameter:**
      - **players** (list): Die Liste der Spieler.
    - **Rückgabewert:** None
  - **get_closest_player(players)**
    - **Beschreibung:** Gibt den nächsten Spieler zurück.
    - **Parameter:**
      - **players** (list): Die Liste der Spieler.
    - **Rückgabewert:** Player

### Environment Module Documentation

**Name des Moduls:** environment

**Beschreibung:** Das Environment-Modul enthält die Umgebungsklasse, die die Interaktionen zwischen Spielern, Bossen und Adds verwaltet.

### Einführung
- **Name des Moduls:** environment
- **Beschreibung:** Das Environment-Modul enthält die Umgebungsklasse, die die Interaktionen zwischen Spielern, Bossen und Adds verwaltet.

### Klassen

#### DungeonEnvironment
- **Beschreibung:** Die Klasse DungeonEnvironment repräsentiert die Umgebung des Spiels.
- **Attribute:**
  - **players** (list): Die Liste der Spieler.
  - **boss** (Boss): Der Boss.
  - **adds** (list): Die Liste der Adds.
  - **player_agents** (list): Die Liste der Spieler-Agenten.
  - **boss_agent** (BossAgent): Der Boss-Agent.
  - **projectiles** (list): Die Liste der Projektile.
  - **done** (bool): Gibt an, ob die Umgebung abgeschlossen ist.
  - **add_spawn_timer** (int): Der Timer für das Spawnen von Adds.
  - **add_spawn_delay** (int): Die Verzögerung für das Spawnen von Adds.
  - **game_time** (int): Die Spielzeit.
- **Methoden:**
  - **__init__()**
    - **Beschreibung:** Initialisiert die DungeonEnvironment-Klasse.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **reset()**
    - **Beschreibung:** Setzt die Umgebung zurück.
    - **Parameter:** None
    - **Rückgabewert:** np.array
  - **get_state()**
    - **Beschreibung:** Gibt den Zustand der Umgebung zurück.
    - **Parameter:** None
    - **Rückgabewert:** np.array
  - **calculate_state_size()**
    - **Beschreibung:** Berechnet die Größe des Zustands.
    - **Parameter:** None
    - **Rückgabewert:** int
  - **get_player_state_size()**
    - **Beschreibung:** Gibt die Größe des Spielerzustands zurück.
    - **Parameter:** None
    - **Rückgabewert:** int
  - **get_player_state(player)**
    - **Beschreibung:** Gibt den Zustand eines Spielers zurück.
    - **Parameter:**
      - **player** (Player): Der Spieler.
    - **Rückgabewert:** np.array
  - **get_boss_state_size()**
    - **Beschreibung:** Gibt die Größe des Bosszustands zurück.
    - **Parameter:** None
    - **Rückgabewert:** int
  - **get_boss_state()**
    - **Beschreibung:** Gibt den Zustand des Bosses zurück.
    - **Parameter:** None
    - **Rückgabewert:** np.array
  - **handle_player_actions()**
    - **Beschreibung:** Verarbeitet die Aktionen der Spieler.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **do_player_action(player, class_name, action_type, action_name, reward)**
    - **Beschreibung:** Führt eine Spieleraktion aus.
    - **Parameter:**
      - **player** (Player): Der Spieler.
      - **class_name** (str): Der Name der Klasse.
      - **action_type** (str): Der Typ der Aktion.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** float
  - **handle_boss_actions()**
    - **Beschreibung:** Verarbeitet die Aktionen des Bosses.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **update()**
    - **Beschreibung:** Aktualisiert die Umgebung.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **render()**
    - **Beschreibung:** Rendert die Umgebung.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **log_action(entity, action_name, reward)**
    - **Beschreibung:** Protokolliert eine Aktion.
    - **Parameter:**
      - **entity** (Entity): Die Entität.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** None

### Agents Module Documentation

**Name des Moduls:** agents

**Beschreibung:** Das Agents-Modul enthält die Klassen für die Agenten, die in der Umgebung interagieren.

### Einführung
- **Name des Moduls:** agents
- **Beschreibung:** Das Agents-Modul enthält die Klassen für die Agenten, die in der Umgebung interagieren.

### Klassen

#### DDQNAgent
- **Beschreibung:** Die Klasse DDQNAgent repräsentiert einen Agenten, der das DDQN-Verfahren verwendet.
- **Attribute:**
  - **state_size** (int): Die Größe des Zustands.
  - **action_size** (int): Die Größe der Aktion.
  - **memory** (PrioritizedReplayBuffer): Der Speicher für priorisiertes Replay.
  - **gamma** (float): Der Diskontfaktor.
  - **epsilon** (float): Der Epsilon-Wert.
  - **epsilon_min** (float): Der minimale Epsilon-Wert.
  - **epsilon_decay** (float): Die Abnahmerate für Epsilon.
  - **learning_rate** (float): Die Lernrate.
  - **model** (Model): Das Modell.
  - **target_model** (Model): Das Zielmodell.
  - **train_step_counter** (int): Der Zähler für die Trainingsschritte.
  - **last_reward** (float): Die letzte Belohnung.
- **Methoden:**
  - **__init__(state_size, action_size)**
    - **Beschreibung:** Initialisiert die DDQNAgent-Klasse.
    - **Parameter:**
      - **state_size** (int): Die Größe des Zustands.
      - **action_size** (int): Die Größe der Aktion.
    - **Rückgabewert:** None
  - **on_done()**
    - **Beschreibung:** Wird aufgerufen, wenn der Agent fertig ist.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **_build_model()**
    - **Beschreibung:** Erstellt das Modell.
    - **Parameter:** None
    - **Rückgabewert:** Model
  - **update_target_model()**
    - **Beschreibung:** Aktualisiert das Zielmodell.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **remember(state, action, reward, next_state, done, error)**
    - **Beschreibung:** Speichert eine Erfahrung im Speicher.
    - **Parameter:**
      - **state** (np.array): Der Zustand.
      - **action** (int): Die Aktion.
      - **reward** (float): Die Belohnung.
      - **next_state** (np.array): Der nächste Zustand.
      - **done** (bool): Gibt an, ob die Episode abgeschlossen ist.
      - **error** (float): Der Fehler.
    - **Rückgabewert:** None
  - **act(state)**
    - **Beschreibung:** Wählt eine Aktion basierend auf dem Zustand.
    - **Parameter:**
      - **state** (np.array): Der Zustand.
    - **Rückgabewert:** int
  - **train_step(state, action, reward, next_state, done)**
    - **Beschreibung:** Führt einen Trainingsschritt durch.
    - **Parameter:**
      - **state** (np.array): Der Zustand.
      - **action** (int): Die Aktion.
      - **reward** (float): Die Belohnung.
      - **next_state** (np.array): Der nächste Zustand.
      - **done** (bool): Gibt an, ob die Episode abgeschlossen ist.
    - **Rückgabewert:** None
  - **load(name)**
    - **Beschreibung:** Lädt die Gewichte des Modells.
    - **Parameter:**
      - **name** (str): Der Name der Datei.
    - **Rückgabewert:** None
  - **save(name)**
    - **Beschreibung:** Speichert die Gewichte des Modells.
    - **Parameter:**
      - **name** (str): Der Name der Datei.
    - **Rückgabewert:** None

#### BossAgent
- **Beschreibung:** Die Klasse BossAgent repräsentiert einen Boss-Agenten, der das DDQN-Verfahren verwendet.
- **Attribute:**
  - **state_size** (int): Die Größe des Zustands.
  - **action_size** (int): Die Größe der Aktion.
  - **memory** (PrioritizedReplayBuffer): Der Speicher für priorisiertes Replay.
  - **gamma** (float): Der Diskontfaktor.
  - **epsilon** (float): Der Epsilon-Wert.
  - **epsilon_min** (float): Der minimale Epsilon-Wert.
  - **epsilon_decay** (float): Die Abnahmerate für Epsilon.
  - **learning_rate** (float): Die Lernrate.
  - **model** (Model): Das Modell.
  - **target_model** (Model): Das Zielmodell.
  - **train_step_counter** (int): Der Zähler für die Trainingsschritte.
  - **last_reward** (float): Die letzte Belohnung.
- **Methoden:**
  - **__init__(state_size, action_size)**
    - **Beschreibung:** Initialisiert die BossAgent-Klasse.
    - **Parameter:**
      - **state_size** (int): Die Größe des Zustands.
      - **action_size** (int): Die Größe der Aktion.
    - **Rückgabewert:** None
  - **on_done()**
    - **Beschreibung:** Wird aufgerufen, wenn der Agent fertig ist.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **_build_model()**
    - **Beschreibung:** Erstellt das Modell.
    - **Parameter:** None
    - **Rückgabewert:** Model
  - **update_target_model()**
    - **Beschreibung:** Aktualisiert das Zielmodell.
    - **Parameter:** None
    - **Rückgabewert:** None
  - **remember(state, action, reward, next_state, done, error)**
    - **Beschreibung:** Speichert eine Erfahrung im Speicher.
    - **Parameter:**
      - **state** (np.array): Der Zustand.
      - **action** (int): Die Aktion.
      - **reward** (float): Die Belohnung.
      - **next_state** (np.array): Der nächste Zustand.
      - **done** (bool): Gibt an, ob die Episode abgeschlossen ist.
      - **error** (float): Der Fehler.
    - **Rückgabewert:** None
  - **act(state)**
    - **Beschreibung:** Wählt eine Aktion basierend auf dem Zustand.
    - **Parameter:**
      - **state** (np.array): Der Zustand.
    - **Rückgabewert:** int
  - **train_step(state, action, reward, next_state, done)**
    - **Beschreibung:** Führt einen Trainingsschritt durch.
    - **Parameter:**
      - **state** (np.array): Der Zustand.
      - **action** (int): Die Aktion.
      - **reward** (float): Die Belohnung.
      - **next_state** (np.array): Der nächste Zustand.
      - **done** (bool): Gibt an, ob die Episode abgeschlossen ist.
    - **Rückgabewert:** None
  - **load(name)**
    - **Beschreibung:** Lädt die Gewichte des Modells.
    - **Parameter:**
      - **name** (str): Der Name der Datei.
    - **Rückgabewert:** None
  - **save(name)**
    - **Beschreibung:** Speichert die Gewichte des Modells.
    - **Parameter:**
      - **name** (str): Der Name der Datei.
    - **Rückgabewert:** None

### Replay Buffer Module Documentation

**Name des Moduls:** replay_buffer

**Beschreibung:** Das Replay Buffer-Modul enthält die Klassen für den priorisierten Replay-Buffer.

### Einführung
- **Name des Moduls:** replay_buffer
- **Beschreibung:** Das Replay Buffer-Modul enthält die Klassen für den priorisierten Replay-Buffer.

### Klassen

#### SumTree
- **Beschreibung:** Die Klasse SumTree repräsentiert einen Summenbaum, der für den priorisierten Replay-Buffer verwendet wird.
- **Attribute:**
  - **capacity** (int): Die Kapazität des Baums.
  - **tree** (np.array): Der Baum.
  - **data** (np.array): Die Daten.
  - **n_entries** (int): Die Anzahl der Einträge.
  - **next_leaf_index** (int): Der Index des nächsten Blatts.
- **Methoden:**
  - **__init__(capacity)**
    - **Beschreibung:** Initialisiert die SumTree-Klasse.
    - **Parameter:**
      - **capacity** (int): Die Kapazität des Baums.
    - **Rückgabewert:** None
  - **_propagate(index, change)**
    - **Beschreibung:** Verbreitet die Änderung im Baum.
    - **Parameter:**
      - **index** (int): Der Index.
      - **change** (float): Die Änderung.
    - **Rückgabewert:** None
  - **_retrieve(index, s)**
    - **Beschreibung:** Ruft den Wert im Baum ab.
    - **Parameter:**
      - **index** (int): Der Index.
      - **s** (float): Der Wert.
    - **Rückgabewert:** int
  - **add(priority, data)**
    - **Beschreibung:** Fügt eine Priorität und Daten zum Baum hinzu.
    - **Parameter:**
      - **priority** (float): Die Priorität.
      - **data** (object): Die Daten.
    - **Rückgabewert:** None
  - **update(index, priority)**
    - **Beschreibung:** Aktualisiert die Priorität eines Blatts.
    - **Parameter:**
      - **index** (int): Der Index.
      - **priority** (float): Die Priorität.
    - **Rückgabewert:** None
  - **get_leaf(s)**
    - **Beschreibung:** Gibt das Blatt mit der gegebenen Priorität zurück.
    - **Parameter:**
      - **s** (float): Die Priorität.
    - **Rückgabewert:** tuple
  - **total_priority()**
    - **Beschreibung:** Gibt die Gesamtpriorität des Baums zurück.
    - **Parameter:** None
    - **Rückgabewert:** float

#### PrioritizedReplayBuffer
- **Beschreibung:** Die Klasse PrioritizedReplayBuffer repräsentiert einen priorisierten Replay-Buffer.
- **Attribute:**
  - **tree** (SumTree): Der Summenbaum.
  - **capacity** (int): Die Kapazität des Buffers.
  - **alpha** (float): Der Alpha-Wert.
  - **beta_start** (float): Der Startwert für Beta.
  - **beta** (float): Der Beta-Wert.
  - **beta_frames** (int): Die Anzahl der Frames für Beta.
  - **frame** (int): Der aktuelle Frame.
- **Methoden:**
  - **__init__(capacity, alpha, beta_start, beta_frames)**
    - **Beschreibung:** Initialisiert die PrioritizedReplayBuffer-Klasse.
    - **Parameter:**
      - **capacity** (int): Die Kapazität des Buffers.
      - **alpha** (float): Der Alpha-Wert.
      - **beta_start** (float): Der Startwert für Beta.
      - **beta_frames** (int): Die Anzahl der Frames für Beta.
    - **Rückgabewert:** None
  - **add(state, action, reward, next_state, done, error)**
    - **Beschreibung:** Fügt eine Erfahrung zum Buffer hinzu.
    - **Parameter:**
      - **state** (np.array): Der Zustand.
      - **action** (int): Die Aktion.
      - **reward** (float): Die Belohnung.
      - **next_state** (np.array): Der nächste Zustand.
      - **done** (bool): Gibt an, ob die Episode abgeschlossen ist.
      - **error** (float): Der Fehler.
    - **Rückgabewert:** None
  - **_get_priority(error)**
    - **Beschreibung:** Gibt die Priorität basierend auf dem Fehler zurück.
    - **Parameter:**
      - **error** (float): Der Fehler.
    - **Rückgabewert:** float
  - **sample(batch_size)**
    - **Beschreibung:** Gibt eine Stichprobe aus dem Buffer zurück.
    - **Parameter:**
      - **batch_size** (int): Die Größe des Batches.
    - **Rückgabewert:** tuple
  - **batch_update(tree_idxs, errors)**
    - **Beschreibung:** Aktualisiert die Prioritäten im Baum.
    - **Parameter:**
      - **tree_idxs** (list): Die Indizes der Blätter.
      - **errors** (list): Die Fehler.
    - **Rückgabewert:** None

### Boss Actions Module Documentation

**Name des Moduls:** boss_actions

**Beschreibung:** Das Boss Actions-Modul enthält die Logik für die Boss-Aktionen.

### Einführung
- **Name des Moduls:** boss_actions
- **Beschreibung:** Das Boss Actions-Modul enthält die Logik für die Boss-Aktionen.

### Funktionen

#### do_boss_melee_action(self, reward)
- **Beschreibung:** Führt eine Nahkampfaktion des Bosses aus.
- **Parameter:**
  - **self** (DungeonEnvironment): Die Umgebung.
  - **reward** (float): Die Belohnung.
- **Rückgabewert:** float

#### do_boss_ranged_action(self, reward)
- **Beschreibung:** Führt eine Fernkampfaktion des Bosses aus.
- **Parameter:**
  - **self** (DungeonEnvironment): Die Umgebung.
  - **reward** (float): Die Belohnung.
- **Rückgabewert:** float

#### do_boss_buffs_action(self, reward)
- **Beschreibung:** Führt eine Buff-Aktion des Bosses aus.
- **Parameter:**
  - **self** (DungeonEnvironment): Die Umgebung.
  - **reward** (float): Die Belohnung.
- **Rückgabewert:** float

#### do_boss_dots_action(self, reward)
- **Beschreibung:** Führt eine DOT-Aktion des Bosses aus.
- **Parameter:**
  - **self** (DungeonEnvironment): Die Umgebung.
  - **reward** (float): Die Belohnung.
- **Rückgabewert:** float

#### do_boss_special_action(self, reward)
- **Beschreibung:** Führt eine spezielle Aktion des Bosses aus.
- **Parameter:**
  - **self** (DungeonEnvironment): Die Umgebung.
  - **reward** (float): Die Belohnung.
- **Rückgabewert:** float

### Main Module Documentation

**Name des Moduls:** main

**Beschreibung:** Das Main-Modul erstellt die Umgebung und startet den Trainingsloop. Es beinhaltet das Laden und Speichern der Modelle.

### Einführung
- **Name des Moduls:** main
- **Beschreibung:** Das Main-Modul erstellt die Umgebung und startet den Trainingsloop. Es beinhaltet das Laden und Speichern der Modelle.

### Beispiele

#### Beispiel: Hauptfunktion
```python
if __name__ == "__main__":
    env = DungeonEnvironment()
    player_agent_count = len(env.player_agents)
    boss_agent = env.boss_agent
    try:
        for agent in env.player_agents:
            agent.load(MODEL_PATH + ".weights.h5")
        boss_agent.load(BOSS_MODEL_PATH + ".weights.h5")
        print("Models loaded.")
    except:
        print("No existing model found, starting from scratch")

    for episode in range(NUM_EPISODES):
        state = env.reset()
        done = False
        total_reward = 0
        start_time = time.time()
        while not done:
            env.update()
            total_reward = 0
            for agent in env.player_agents:
                total_reward += agent.last_reward
            if env.done:
                break
        end_time = time.time()
        episode_time = end_time - start_time
        print(f"Episode: {episode + 1}/{NUM_EPISODES}, Total Reward: {total_reward:.2f}, Time: {episode_time:.2f} sec")
        if (episode + 1) % 25 == 0:
            for agent in env.player_agents:
                agent.save(MODEL_PATH + ".weights.h5")
            boss_agent.save(BOSS_MODEL_PATH + ".weights.h5")
            print("Models saved.")
    for agent in env.player_agents:
        agent.save(MODEL_PATH + ".weights.h5")
    boss_agent.save(BOSS_MODEL_PATH + ".weights.h5")
    print("Training complete, models saved.")
```

### Tank Actions Module Documentation

**Name des Moduls:** tank_actions

**Beschreibung:** Das Tank Actions-Modul enthält die Logik für die Aktionen der Tank-Klasse.

### Einführung
- **Name des Moduls:** tank_actions
- **Beschreibung:** Das Tank Actions-Modul enthält die Logik für die Aktionen der Tank-Klasse.

### Klassen

#### TankActions
- **Beschreibung:** Die Klasse TankActions repräsentiert die Aktionen der Tank-Klasse.
- **Methoden:**
  - **do_player_action(player, class_name, action_type, action_name, reward)**
    - **Beschreibung:** Führt eine Spieleraktion aus.
    - **Parameter:**
      - **player** (Player): Der Spieler.
      - **class_name** (str): Der Name der Klasse.
      - **action_type** (str): Der Typ der Aktion.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** float

### Healer Actions Module Documentation

**Name des Moduls:** healer_actions

**Beschreibung:** Das Healer Actions-Modul enthält die Logik für die Aktionen der Healer-Klasse.

### Einführung
- **Name des Moduls:** healer_actions
- **Beschreibung:** Das Healer Actions-Modul enthält die Logik für die Aktionen der Healer-Klasse.

### Klassen

#### HealerActions
- **Beschreibung:** Die Klasse HealerActions repräsentiert die Aktionen der Healer-Klasse.
- **Methoden:**
  - **do_player_action(player, class_name, action_type, action_name, reward)**
    - **Beschreibung:** Führt eine Spieleraktion aus.
    - **Parameter:**
      - **player** (Player): Der Spieler.
      - **class_name** (str): Der Name der Klasse.
      - **action_type** (str): Der Typ der Aktion.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** float

### Melee DPS 1 Actions Module Documentation

**Name des Moduls:** melee_dps_1_actions

**Beschreibung:** Das Melee DPS 1 Actions-Modul enthält die Logik für die Aktionen der Melee DPS 1-Klasse.

### Einführung
- **Name des Moduls:** melee_dps_1_actions
- **Beschreibung:** Das Melee DPS 1 Actions-Modul enthält die Logik für die Aktionen der Melee DPS 1-Klasse.

### Klassen

#### MeleeDps1Actions
- **Beschreibung:** Die Klasse MeleeDps1Actions repräsentiert die Aktionen der Melee DPS 1-Klasse.
- **Methoden:**
  - **do_player_action(player, class_name, action_type, action_name, reward)**
    - **Beschreibung:** Führt eine Spieleraktion aus.
    - **Parameter:**
      - **player** (Player): Der Spieler.
      - **class_name** (str): Der Name der Klasse.
      - **action_type** (str): Der Typ der Aktion.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** float

### Melee DPS 2 Actions Module Documentation

**Name des Moduls:** melee_dps_2_actions

**Beschreibung:** Das Melee DPS 2 Actions-Modul enthält die Logik für die Aktionen der Melee DPS 2-Klasse.

### Einführung
- **Name des Moduls:** melee_dps_2_actions
- **Beschreibung:** Das Melee DPS 2 Actions-Modul enthält die Logik für die Aktionen der Melee DPS 2-Klasse.

### Klassen

#### MeleeDps2Actions
- **Beschreibung:** Die Klasse MeleeDps2Actions repräsentiert die Aktionen der Melee DPS 2-Klasse.
- **Methoden:**
  - **do_player_action(player, class_name, action_type, action_name, reward)**
    - **Beschreibung:** Führt eine Spieleraktion aus.
    - **Parameter:**
      - **player** (Player): Der Spieler.
      - **class_name** (str): Der Name der Klasse.
      - **action_type** (str): Der Typ der Aktion.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** float

### Melee DPS 3 Actions Module Documentation

**Name des Moduls:** melee_dps_3_actions

**Beschreibung:** Das Melee DPS 3 Actions-Modul enthält die Logik für die Aktionen der Melee DPS 3-Klasse.

### Einführung
- **Name des Moduls:** melee_dps_3_actions
- **Beschreibung:** Das Melee DPS 3 Actions-Modul enthält die Logik für die Aktionen der Melee DPS 3-Klasse.

### Klassen

#### MeleeDps3Actions
- **Beschreibung:** Die Klasse MeleeDps3Actions repräsentiert die Aktionen der Melee DPS 3-Klasse.
- **Methoden:**
  - **do_player_action(player, class_name, action_type, action_name, reward)**
    - **Beschreibung:** Führt eine Spieleraktion aus.
    - **Parameter:**
      - **player** (Player): Der Spieler.
      - **class_name** (str): Der Name der Klasse.
      - **action_type** (str): Der Typ der Aktion.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** float

### Ranged DPS 1 Actions Module Documentation

**Name des Moduls:** ranged_dps_1_actions

**Beschreibung:** Das Ranged DPS 1 Actions-Modul enthält die Logik für die Aktionen der Ranged DPS 1-Klasse.

### Einführung
- **Name des Moduls:** ranged_dps_1_actions
- **Beschreibung:** Das Ranged DPS 1 Actions-Modul enthält die Logik für die Aktionen der Ranged DPS 1-Klasse.

### Klassen

#### RangedDps1Actions
- **Beschreibung:** Die Klasse RangedDps1Actions repräsentiert die Aktionen der Ranged DPS 1-Klasse.
- **Methoden:**
  - **do_player_action(player, class_name, action_type, action_name, reward)**
    - **Beschreibung:** Führt eine Spieleraktion aus.
    - **Parameter:**
      - **player** (Player): Der Spieler.
      - **class_name** (str): Der Name der Klasse.
      - **action_type** (str): Der Typ der Aktion.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** float

### Ranged DPS 2 Actions Module Documentation

**Name des Moduls:** ranged_dps_2_actions

**Beschreibung:** Das Ranged DPS 2 Actions-Modul enthält die Logik für die Aktionen der Ranged DPS 2-Klasse.

### Einführung
- **Name des Moduls:** ranged_dps_2_actions
- **Beschreibung:** Das Ranged DPS 2 Actions-Modul enthält die Logik für die Aktionen der Ranged DPS 2-Klasse.

### Klassen

#### RangedDps2Actions
- **Beschreibung:** Die Klasse RangedDps2Actions repräsentiert die Aktionen der Ranged DPS 2-Klasse.
- **Methoden:**
  - **do_player_action(player, class_name, action_type, action_name, reward)**
    - **Beschreibung:** Führt eine Spieleraktion aus.
    - **Parameter:**
      - **player** (Player): Der Spieler.
      - **class_name** (str): Der Name der Klasse.
      - **action_type** (str): Der Typ der Aktion.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** float

### Ranged DPS 3 Actions Module Documentation

**Name des Moduls:** ranged_dps_3_actions

**Beschreibung:** Das Ranged DPS 3 Actions-Modul enthält die Logik für die Aktionen der Ranged DPS 3-Klasse.

### Einführung
- **Name des Moduls:** ranged_dps_3_actions
- **Beschreibung:** Das Ranged DPS 3 Actions-Modul enthält die Logik für die Aktionen der Ranged DPS 3-Klasse.

### Klassen

#### RangedDps3Actions
- **Beschreibung:** Die Klasse RangedDps3Actions repräsentiert die Aktionen der Ranged DPS 3-Klasse.
- **Methoden:**
  - **do_player_action(player, class_name, action_type, action_name, reward)**
    - **Beschreibung:** Führt eine Spieleraktion aus.
    - **Parameter:**
      - **player** (Player): Der Spieler.
      - **class_name** (str): Der Name der Klasse.
      - **action_type** (str): Der Typ der Aktion.
      - **action_name** (str): Der Name der Aktion.
      - **reward** (float): Die Belohnung.
    - **Rückgabewert:** float
