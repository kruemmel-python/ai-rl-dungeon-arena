################################################################################
import os
import sys
import numpy as np
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Input, LayerNormalization
from tensorflow.keras.optimizers import Adam
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", module="tensorflow")
import random
import time
import math

# Konfigurationsparameter
WIDTH, HEIGHT = 700, 700
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
NUM_EPISODES = 100
BATCH_SIZE = 128
LEARNING_RATE = 0.0001
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.05
EPSILON_DECAY_RATE = 0.0005
TARGET_UPDATE_FREQ = 100
MODEL_PATH = "mmorpg_agent.keras"
BOSS_MODEL_PATH = "boss_agent.keras"
PRIORITIZED_REPLAY_EPS = 1e-6
MEMORY_SIZE_MAX = 20000
MAX_PLAYERS = 8
MAX_ENEMIES = 10
MOVE_SPEED = 2

# Klassen und ihre Fähigkeiten
PLAYER_CLASSES = ["tank", "healer", "melee_dps_1", "melee_dps_2", "melee_dps_3", "ranged_dps_1", "ranged_dps_2", "ranged_dps_3"]
NUM_PLAYER_CLASSES = len(PLAYER_CLASSES)
CLASS_ACTIONS = {
    "tank": {
        "melee_attacks": ["taunt", "shield_bash", "heavy_strike", "block", "sweep"],
        "ranged_attacks": ["chucking_shield", "shattering_throw", "short_charge", "intimidating_roar", "defensive_throw"],
        "buffs": ["fortify", "last_stand", "resolve", "iron_skin", "vigilance"],
        "dots": ["rupture", "bleed", "pulverize", "aggravated_wound", "crippling_slash"],
        "unique": "avenger_shield"
    },
    "healer": {
        "melee_attacks": ["smite", "holy_nova", "healing_strike", "divine_touch", "mend"],
        "ranged_attacks": ["renew", "holy_fire", "prayer_of_mending", "light_burst", "radiance"],
        "buffs": ["power_word_shield", "divine_hymn", "aegis", "inspiration", "lightwell"],
        "dots": ["penance", "shadow_word_pain", "holy_smite_dot", "corrupting_touch", "blessing_of_corruption"],
        "unique": "guardian_spirit"
    },
    "melee_dps_1": {
        "melee_attacks": ["strike", "slash", "eviscerate", "backstab", "flurry"],
        "ranged_attacks": ["shuriken_toss", "throwing_knives", "fan_of_knives", "poison_dart", "shadow_step_strike"],
        "buffs": ["shadow_meld", "vanish", "adrenaline_rush", "blade_dance", "elusiveness"],
        "dots": ["poison_wound", "rupture", "bleed", "garrote", "crippling_poison"],
        "unique": "death_from_above"
    },
    "melee_dps_2": {
        "melee_attacks": ["rage_strike", "whirlwind", "execute", "furious_blow", "rampage"],
        "ranged_attacks": ["heroic_throw", "sundering_blow", "shout", "charge_throw", "enraged_leap"],
        "buffs": ["bloodlust", "berserker_rage", "battle_shout", "inner_rage", "enraged_regeneration"],
        "dots": ["rend", "deep_wounds", "mortal_wound", "bleed", "slaughter"],
        "unique": "avatar"
    },
    "melee_dps_3": {
        "melee_attacks": ["soul_rend", "demonic_slash", "chaos_nova", "fel_strike", "shadow_rush"],
        "ranged_attacks": ["fel_beam", "shadow_bolt", "immolation", "soul_fire", "demonic_empowerment"],
        "buffs": ["metamorphosis", "spectral_sight", "dark_pact", "fel_infusion", "nether_walk"],
        "dots": ["corruption", "agony", "immolate_dot", "shadow_burn", "soul_burn"],
        "unique": "demon_form"
    },
    "ranged_dps_1": {
        "melee_attacks": ["arcane_blast", "frostbolt", "fireball", "lightning_bolt", "shadow_strike"],
        "ranged_attacks": ["arcane_missiles", "icicle_lance", "inferno_blast", "chain_lightning", "shadow_pulse"],
        "buffs": ["ice_barrier", "combustion", "mana_shield", "time_warp", "evocation"],
        "dots": ["living_bomb", "ignite", "frostfire_bolt", "electrocute", "shadow_word_pain"],
        "unique": "meteor"
    },
    "ranged_dps_2": {
        "melee_attacks": ["aimed_shot", "multi_shot", "rapid_fire", "serpent_sting", "steady_shot"],
        "ranged_attacks": ["explosive_shot", "barrage", "sidewinders", "trick_shot", "piercing_shot"],
        "buffs": ["hunters_mark", "aspect_of_the_hawk", "camouflage", "trueshot", "fervor"],
        "dots": ["poison_sting", "bleed_shot", "venom_shot", "flare", "scorched_earth"],
        "unique": "stampede"
    },
    "ranged_dps_3": {
        "melee_attacks": ["starfire", "moonfire", "wrath", "solar_beam", "lunar_strike"],
        "ranged_attacks": ["starsurge", "shooting_stars", "celestial_alignment", "sunfire", "starfall"],
        "buffs": ["eclipse", "nature_swiftness", "innervate", "rejuvenation", "wild_growth"],
        "dots": ["moonfire_dot", "sunfire_dot", "swarm", "ebb_and_flow", "stellar_flare"],
        "unique": "incarnation"
    },
}

ACTIONS = []
for class_name in PLAYER_CLASSES:
    for action_type in CLASS_ACTIONS[class_name]:
        if isinstance(CLASS_ACTIONS[class_name][action_type], list):
            ACTIONS.extend([f"{class_name}_{action_type}_{action}" for action in CLASS_ACTIONS[class_name][action_type]])
        else:
            ACTIONS.append(f"{class_name}_{action_type}")

NUM_ACTIONS = len(ACTIONS)

# Boss-Fähigkeiten
BOSS_ACTIONS = {
    "melee_attacks": ["slam", "cleave", "frenzy", "bite", "smash"],
    "ranged_attacks": ["fire_breath", "shadow_bolt", "earthquake", "lightning_storm", "arcane_blast"],
    "buffs": ["enrage", "shield", "regen", "power_up", "haste"],
    "dots": ["poison_spit", "shadow_nova", "fire_dot", "bleed_dot", "frost_dot"],
    "special_abilities": ["spawn_adds", "aoe_damage", "phase_shift", "mind_control", "enrage_burst"]
}

NUM_BOSS_ACTIONS = len(BOSS_ACTIONS)
REWARD_KILL_BOSS = 100
REWARD_KILL_ADD = 10
PENALTY_PLAYER_DEATH = -25
PENALTY_BOSS_HIT_PLAYER = -2
REWARD_STEP = -0.005
REWARD_HIT_BOSS = 5
REWARD_HEAL_PLAYER = 2
REWARD_MOVE_TOWARDS_BOSS = 0.1
