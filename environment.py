################################################################################
import numpy as np
import random
import math
from config import WIDTH, HEIGHT, GRID_SIZE, CELL_SIZE, MOVE_SPEED, MAX_PLAYERS, MAX_ENEMIES, PLAYER_CLASSES, NUM_PLAYER_CLASSES, ACTIONS, NUM_ACTIONS, BOSS_ACTIONS, NUM_BOSS_ACTIONS, REWARD_KILL_BOSS, REWARD_KILL_ADD, PENALTY_PLAYER_DEATH, PENALTY_BOSS_HIT_PLAYER, REWARD_STEP, REWARD_HIT_BOSS, REWARD_HEAL_PLAYER, REWARD_MOVE_TOWARDS_BOSS
from entities import Player, Boss, Add
from agents import DDQNAgent, BossAgent

# Umgebungsklasse
class DungeonEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        print("Resetting environment")
        self.players = []
        self.boss = Boss(WIDTH // 2, HEIGHT // 4)
        self.adds = []
        self.player_agents = []
        self.boss_agent = None
        self.projectiles = []
        self.done = False
        self.add_spawn_timer = 0
        self.add_spawn_delay = 200
        self.game_time = 0

        for i, class_name in enumerate(PLAYER_CLASSES):
            x = (i + 1) * (WIDTH // (len(PLAYER_CLASSES) + 1))
            y = HEIGHT - CELL_SIZE
            player = Player(class_name, x, y)
            self.players.append(player)
            player_agent = DDQNAgent(self.get_player_state_size(), NUM_ACTIONS)
            self.player_agents.append(player_agent)

        self.boss = Boss(WIDTH // 2, HEIGHT // 4)
        print(f"Boss initialized at ({self.boss.x}, {self.boss.y})")
        self.boss_agent = BossAgent(self.get_boss_state_size(), len(BOSS_ACTIONS))
        self.done = False
        return self.get_state()

    def get_state(self):
        state = []
        state.append(self.game_time / 200)
        state.append(self.boss.hp / self.boss.max_hp)
        state.append(self.boss.phase / 3)
        state.append(len(self.adds) / MAX_ENEMIES)
        player_features = []
        for player in self.players:
            player_features.extend([
                player.x / WIDTH,
                player.y / HEIGHT,
                PLAYER_CLASSES.index(player.player_class) / (len(PLAYER_CLASSES) - 1),
                player.hp / player.max_hp,
                int(player.is_dead)
            ])
        while len(player_features) < MAX_PLAYERS * 5:
            player_features.append(0)
        state.extend(player_features)

        add_features = []
        for add in self.adds:
            add_features.extend([
                add.x / WIDTH,
                add.y / HEIGHT,
                add.hp / add.max_hp,
            ])
        while len(add_features) < MAX_ENEMIES * 3:
            add_features.append(0)
        state.extend(add_features)
        return np.array(state, dtype=np.float32)

    def calculate_state_size(self):
        state_size = 4
        state_size += MAX_PLAYERS * 5
        state_size += MAX_ENEMIES * 3
        return state_size

    def get_player_state_size(self):
        state_size = 3
        state_size += 1
        state_size += 2
        state_size += 1
        state_size += MAX_PLAYERS * 3
        state_size += MAX_ENEMIES * 3
        return state_size

    def get_player_state(self, player):
        state = []
        state.append(self.game_time / 200)
        state.append(self.boss.hp / self.boss.max_hp)
        state.append(self.boss.phase / 3)
        state.append(int(player.is_dead))
        state.append(player.x / WIDTH)
        state.append(player.y / HEIGHT)
        state.append(player.hp / player.max_hp)
        player_features = []
        for p in self.players:
            if p != player:
                player_features.extend([
                    p.x / WIDTH,
                    p.y / HEIGHT,
                    p.hp / p.max_hp
                ])
        while len(player_features) < MAX_PLAYERS * 3:
            player_features.append(0)
        state.extend(player_features)
        add_features = []
        for add in self.adds:
            add_features.extend([
                add.x / WIDTH,
                add.y / HEIGHT,
                add.hp / add.max_hp,
            ])
        while len(add_features) < MAX_ENEMIES * 3:
            add_features.append(0)
        state.extend(add_features)
        return np.array(state, dtype=np.float32)

    def get_boss_state_size(self):
        state_size = 4
        state_size += MAX_PLAYERS * 3
        return state_size

    def get_boss_state(self):
        state = []
        state.append(self.game_time / 200)
        state.append(self.boss.hp / self.boss.max_hp)
        state.append(self.boss.phase / 3)
        state.append(len(self.adds) / MAX_ENEMIES)
        player_features = []
        for player in self.players:
            player_features.extend([
                player.x / WIDTH,
                player.y / HEIGHT,
                player.hp / player.max_hp
            ])
        while len(player_features) < MAX_PLAYERS * 3:
            player_features.append(0)
        state.extend(player_features)
        return np.array(state, dtype=np.float32)

    def handle_player_actions(self):
        for player, agent in zip(self.players, self.player_agents):
            player_state = self.get_player_state(player)
            action_index = agent.act(player_state)
            action_name = ACTIONS[action_index]

            class_name = action_name.split("_")[0]
            action_type = action_name.split("_")[1]
            reward = REWARD_STEP
            if player.is_dead:
                reward -= 5
            if player.player_class != class_name:
                reward -= 1
            if not player.is_dead:
                distance_to_boss_before = math.sqrt((player.x - self.boss.x)**2 + (player.y - self.boss.y)**2)
                target_x = self.boss.x if player.target_boss else player.x
                target_y = self.boss.y if player.target_boss else player.y
                player.move(target_x, target_y)
                distance_to_boss_after = math.sqrt((player.x - self.boss.x)**2 + (player.y - self.boss.y)**2)
                if distance_to_boss_after < distance_to_boss_before:
                    reward += REWARD_MOVE_TOWARDS_BOSS
                reward = self.do_player_action(player, class_name, action_type, action_name, reward)
                next_player_state = self.get_player_state(player)
                agent.remember(player_state, action_index, reward, next_player_state, self.done, 0)
                agent.train_step(player_state, action_index, reward, next_player_state, self.done)

                # Log the action
                self.log_action(player, action_name, reward)

    def do_player_action(self, player, class_name, action_type, action_name, reward):
        if action_type == "melee_attacks":
            if player.player_class == "tank":
                target = self.boss
                if action_name.split("_")[-1] == "taunt":
                    reward += 3
                    print("Tank taunt")
                elif action_name.split("_")[-1] == "shield_bash":
                    target.take_damage(25)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "heavy_strike":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "block":
                    reward += 2
                elif action_name.split("_")[-1] == "sweep":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
            if player.player_class == "healer":
                if action_name.split("_")[-1] == "smite":
                    target = self.boss
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "holy_nova":
                    for p in self.players:
                        p.hp += 5
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                        reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "healing_strike":
                    for p in self.players:
                        p.hp += 5
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "divine_touch":
                    player.hp += 20
                    if player.hp > player.max_hp:
                        player.hp = player.max_hp
                    if player.hp / player.max_hp < 0.25:
                        reward += 4
                    elif player.hp / player.max_hp < 0.5:
                        reward += 2
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "mend":
                    player.hp += 15
                    if player.hp > player.max_hp:
                        player.hp = player.max_hp
                    reward += REWARD_HEAL_PLAYER
            elif player.player_class == "melee_dps_1":
                target = self.boss
                if action_name.split("_")[-1] == "strike":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "slash":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "eviscerate":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "backstab":
                    target.take_damage(20)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "flurry":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "melee_dps_2":
                target = self.boss
                if action_name.split("_")[-1] == "rage_strike":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "whirlwind":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "execute":
                    target.take_damage(20)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "furious_blow":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "rampage":
                    target.take_damage(25)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "melee_dps_3":
                target = self.boss
                if action_name.split("_")[-1] == "soul_rend":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "demonic_slash":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "chaos_nova":
                    target.take_damage(20)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "fel_strike":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shadow_rush":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "ranged_dps_1":
                target = self.boss
                if action_name.split("_")[-1] == "arcane_blast":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "frostbolt":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "fireball":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "lightning_bolt":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shadow_strike":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "ranged_dps_2":
                target = self.boss
                if action_name.split("_")[-1] == "aimed_shot":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "multi_shot":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "rapid_fire":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "serpent_sting":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "steady_shot":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "ranged_dps_3":
                target = self.boss
                if action_name.split("_")[-1] == "starfire":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "moonfire":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "wrath":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "solar_beam":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "lunar_strike":
                    target.take_damage(20)
                    reward += REWARD_HIT_BOSS
        elif action_type == "ranged_attacks":
            if player.player_class == "tank":
                target = self.boss
                if action_name.split("_")[-1] == "chucking_shield":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shattering_throw":
                    target.take_damage(20)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "short_charge":
                    player.move(target.x, target.y)
                    reward += 1
                elif action_name.split("_")[-1] == "intimidating_roar":
                    reward += 0.3
                elif action_name.split("_")[-1] == "defensive_throw":
                    reward += 0.3
            if player.player_class == "healer":
                target = self.boss
                if action_name.split("_")[-1] == "renew":
                    for p in self.players:
                        p.hp += 1
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "holy_fire":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "prayer_of_mending":
                    for p in self.players:
                        p.hp += 2
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "light_burst":
                    for p in self.players:
                        p.hp += 5
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "radiance":
                    for p in self.players:
                        p.hp += 7
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
            elif player.player_class == "melee_dps_1":
                target = self.boss
                if action_name.split("_")[-1] == "shuriken_toss":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "throwing_knives":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "fan_of_knives":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "poison_dart":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shadow_step_strike":
                    player.move(target.x, target.y)
                    reward += 1
            elif player.player_class == "melee_dps_2":
                target = self.boss
                if action_name.split("_")[-1] == "heroic_throw":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "sundering_blow":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shout":
                    reward += 0.2
                elif action_name.split("_")[-1] == "charge_throw":
                    player.move(target.x, target.y)
                    reward += 1
                elif action_name.split("_")[-1] == "enraged_leap":
                    player.move(target.x, target.y)
                    reward += 1
            elif player.player_class == "melee_dps_3":
                target = self.boss
                if action_name.split("_")[-1] == "fel_beam":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shadow_bolt":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "immolation":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "soul_fire":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "demonic_empowerment":
                    reward += 0.2
            elif player.player_class == "ranged_dps_1":
                target = self.boss
                if action_name.split("_")[-1] == "arcane_missiles":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "icicle_lance":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "inferno_blast":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "chain_lightning":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shadow_pulse":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "ranged_dps_2":
                target = self.boss
                if action_name.split("_")[-1] == "explosive_shot":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "barrage":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "sidewinders":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "trick_shot":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "piercing_shot":
                    target.take_damage(20)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "ranged_dps_3":
                target = self.boss
                if action_name.split("_")[-1] == "starsurge":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shooting_stars":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "celestial_alignment":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "sunfire":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "starfall":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
        elif action_type == "buffs":
            if player.player_class == "tank":
                if action_name.split("_")[-1] == "fortify":
                    player.hp += 10
                    reward += 0.5
                elif action_name.split("_")[-1] == "last_stand":
                    player.hp += 20
                    reward += 0.8
                elif action_name.split("_")[-1] == "resolve":
                    player.hp += 10
                    reward += 0.5
                elif action_name.split("_")[-1] == "iron_skin":
                    player.hp += 5
                    reward += 0.3
                elif action_name.split("_")[-1] == "vigilance":
                    reward += 0.2
            elif player.player_class == "healer":
                if action_name.split("_")[-1] == "power_word_shield":
                    player.hp += 10
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "divine_hymn":
                    for p in self.players:
                        p.hp += 10
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "aegis":
                    for p in self.players:
                        p.hp += 5
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "inspiration":
                    for p in self.players:
                        p.hp += 2
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "lightwell":
                    for p in self.players:
                        p.hp += 8
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
            elif player.player_class == "melee_dps_1":
                if action_name.split("_")[-1] == "shadow_meld":
                    reward += 0.3
                elif action_name.split("_")[-1] == "vanish":
                    reward += 0.4
                elif action_name.split("_")[-1] == "adrenaline_rush":
                    reward += 0.3
                elif action_name.split("_")[-1] == "blade_dance":
                    reward += 0.2
                elif action_name.split("_")[-1] == "elusiveness":
                    reward += 0.2
            elif player.player_class == "melee_dps_2":
                if action_name.split("_")[-1] == "bloodlust":
                    reward += 0.5
                elif action_name.split("_")[-1] == "berserker_rage":
                    reward += 0.4
                elif action_name.split("_")[-1] == "battle_shout":
                    reward += 0.3
                elif action_name.split("_")[-1] == "inner_rage":
                    reward += 0.3
                elif action_name.split("_")[-1] == "enraged_regeneration":
                    player.hp += 10
                    if player.hp > player.max_hp:
                        player.hp = player.max_hp
                    reward += 0.5
            elif player.player_class == "melee_dps_3":
                if action_name.split("_")[-1] == "metamorphosis":
                    reward += 0.5
                elif action_name.split("_")[-1] == "spectral_sight":
                    reward += 0.2
                elif action_name.split("_")[-1] == "dark_pact":
                    player.hp += 10
                    reward += 0.5
                elif action_name.split("_")[-1] == "fel_infusion":
                    reward += 0.3
                elif action_name.split("_")[-1] == "nether_walk":
                    reward += 0.3
            elif player.player_class == "ranged_dps_1":
                if action_name.split("_")[-1] == "ice_barrier":
                    player.hp += 5
                    reward += 0.3
                elif action_name.split("_")[-1] == "combustion":
                    reward += 0.4
                elif action_name.split("_")[-1] == "mana_shield":
                    player.hp += 10
                    reward += 0.5
                elif action_name.split("_")[-1] == "time_warp":
                    reward += 0.4
                elif action_name.split("_")[-1] == "evocation":
                    player.hp += 20
                    reward += 0.8
            elif player.player_class == "ranged_dps_2":
                if action_name.split("_")[-1] == "hunters_mark":
                    reward += 0.1
                elif action_name.split("_")[-1] == "aspect_of_the_hawk":
                    reward += 0.2
                elif action_name.split("_")[-1] == "camouflage":
                    reward += 0.3
                elif action_name.split("_")[-1] == "trueshot":
                    reward += 0.4
                elif action_name.split("_")[-1] == "fervor":
                    reward += 0.3
            elif player.player_class == "ranged_dps_3":
                if action_name.split("_")[-1] == "eclipse":
                    reward += 0.3
                elif action_name.split("_")[-1] == "nature_swiftness":
                    reward += 0.4
                elif action_name.split("_")[-1] == "innervate":
                    reward += 0.5
                elif action_name.split("_")[-1] == "rejuvenation":
                    for p in self.players:
                        p.hp += 2
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
                elif action_name.split("_")[-1] == "wild_growth":
                    for p in self.players:
                        p.hp += 5
                        if p.hp > p.max_hp:
                            p.hp = p.max_hp
                    reward += REWARD_HEAL_PLAYER
        elif action_type == "dots":
            target = self.boss
            if player.player_class == "tank":
                if action_name.split("_")[-1] == "rupture":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "bleed":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "pulverize":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "aggravated_wound":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "crippling_slash":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
            if player.player_class == "healer":
                if action_name.split("_")[-1] == "penance":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shadow_word_pain":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "holy_smite_dot":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "corrupting_touch":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "blessing_of_corruption":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "melee_dps_1":
                if action_name.split("_")[-1] == "poison_wound":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "rupture":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "bleed":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "garrote":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "crippling_poison":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "melee_dps_2":
                if action_name.split("_")[-1] == "rend":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "deep_wounds":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "mortal_wound":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "bleed":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "slaughter":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "melee_dps_3":
                if action_name.split("_")[-1] == "corruption":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "agony":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "immolate_dot":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shadow_burn":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "soul_burn":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "ranged_dps_1":
                if action_name.split("_")[-1] == "living_bomb":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "ignite":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "frostfire_bolt":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "electrocute":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "shadow_word_pain":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "ranged_dps_2":
                if action_name.split("_")[-1] == "poison_sting":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "bleed_shot":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "venom_shot":
                    target.take_damage(12)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "flare":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "scorched_earth":
                    target.take_damage(15)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "ranged_dps_3":
                if action_name.split("_")[-1] == "moonfire_dot":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "sunfire_dot":
                    target.take_damage(8)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "swarm":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "ebb_and_flow":
                    target.take_damage(10)
                    reward += REWARD_HIT_BOSS
                elif action_name.split("_")[-1] == "stellar_flare":
                    target.take_damage(18)
                    reward += REWARD_HIT_BOSS
        elif action_type == "unique":
            if player.player_class == "tank":
                if action_name.split("_")[-1] == "avenger_shield":
                    target = self.boss
                    target.take_damage(20)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "healer":
                if action_name.split("_")[-1] == "guardian_spirit":
                    player.hp += 20
                    reward += REWARD_HEAL_PLAYER
            elif player.player_class == "melee_dps_1":
                if action_name.split("_")[-1] == "death_from_above":
                    target = self.boss
                    target.take_damage(25)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "melee_dps_2":
                if action_name.split("_")[-1] == "avatar":
                    reward += 0.4
            elif player.player_class == "melee_dps_3":
                if action_name.split("_")[-1] == "demon_form":
                    reward += 0.5
            elif player.player_class == "ranged_dps_1":
                if action_name.split("_")[-1] == "meteor":
                    target = self.boss
                    target.take_damage(25)
                    reward += REWARD_HIT_BOSS
            elif player.player_class == "ranged_dps_2":
                if action_name.split("_")[-1] == "stampede":
                    reward += 0.5
            elif player.player_class == "ranged_dps_3":
                if action_name.split("_")[-1] == "incarnation":
                    reward += 0.5
        return reward

    def handle_boss_actions(self):
        boss_state = self.get_boss_state()
        action_index = self.boss_agent.act(boss_state)
        action_name = list(BOSS_ACTIONS.keys())[action_index]
        reward = REWARD_STEP

        if action_name == "melee_attacks":
            reward = self.do_boss_melee_action(reward)
        elif action_name == "ranged_attacks":
            reward = self.do_boss_ranged_action(reward)
        elif action_name == "buffs":
            reward = self.do_boss_buffs_action(reward)
        elif action_name == "dots":
            reward = self.do_boss_dots_action(reward)
        elif action_name == "special_abilities":
            reward = self.do_boss_special_action(reward)

        next_boss_state = self.get_boss_state()
        self.boss_agent.remember(boss_state, action_index, reward, next_boss_state, self.done, 0)
        self.boss_agent.train_step(boss_state, action_index, reward, next_boss_state, self.done)

        # Log the action
        self.log_action(self.boss, action_name, reward)

    def do_boss_melee_action(self, reward):
        if self.boss.target_player:
            if random.random() < 0.5:
                if self.boss.is_enraged:
                    damage = 20
                else:
                    damage = 10
                self.boss.target_player.take_damage(damage)
                reward += PENALTY_BOSS_HIT_PLAYER
                if self.boss.target_player.is_dead:
                    reward += PENALTY_PLAYER_DEATH
        return reward

    def do_boss_ranged_action(self, reward):
        if random.random() < 0.4:
            for player in self.players:
                if not player.is_dead:
                    player.take_damage(10)
                    reward += PENALTY_BOSS_HIT_PLAYER / 2
                    if player.is_dead:
                        reward += PENALTY_PLAYER_DEATH / 2
        return reward

    def do_boss_buffs_action(self, reward):
        if random.random() < 0.3:
            if not self.boss.is_enraged:
                self.boss.is_enraged = True
                self.boss.enrage_timer = 100
                print("Boss ist Enraged!")
                reward += 1
            else:
                self.boss.enrage_timer = 100
                reward -= 0.2
        if random.random() < 0.4:
            self.boss.hp += 10
            if self.boss.hp > self.boss.max_hp:
                self.boss.hp = self.boss.max_hp
            reward += 0.2
        return reward

    def do_boss_dots_action(self, reward):
        if random.random() < 0.6:
            for player in self.players:
                if not player.is_dead:
                    player.take_damage(5)
                    reward += PENALTY_BOSS_HIT_PLAYER / 4
                    if player.is_dead:
                        reward += PENALTY_PLAYER_DEATH / 4
        return reward

    def do_boss_special_action(self, reward):
        if random.random() < 0.3 and len(self.adds) < MAX_ENEMIES:
            add_x = random.randint(0, WIDTH)
            add_y = random.randint(0, HEIGHT)
            add = Add(add_x, add_y)
            self.adds.append(add)
            reward += 1
        if random.random() < 0.2:
            for player in self.players:
                if not player.is_dead:
                    player.take_damage(15)
                    reward += PENALTY_BOSS_HIT_PLAYER / 3
                    if player.is_dead:
                        reward += PENALTY_PLAYER_DEATH / 3
        if self.boss.phase == 3 and random.random() < 0.2 and not self.boss.is_enraged:
            self.boss.is_enraged = True
            self.boss.enrage_timer = 100
            print("Boss ist Enraged!")
            reward += 2
        if random.random() < 0.1:
            if self.players:
                target_player = random.choice(self.players)
                target_player.target_boss = False
                reward -= 0.5
        return reward

    def update(self):
        self.game_time += 1
        self.boss.check_phase()
        self.boss.move(self.players)

        for add in self.adds:
            add.move(self.players)

        if self.boss.is_enraged:
            self.boss.enrage_timer -= 1
            if self.boss.enrage_timer <= 0:
                self.boss.is_enraged = False
                print("Boss ist nicht mehr Enraged!")

        self.handle_player_actions()
        self.handle_boss_actions()

        if self.add_spawn_timer <= 0 and len(self.adds) < MAX_ENEMIES:
            add_x = random.randint(0, WIDTH)
            add_y = random.randint(0, HEIGHT)
            add = Add(add_x, add_y)
            self.adds.append(add)
            self.add_spawn_timer = self.add_spawn_delay
        else:
            self.add_spawn_timer -= 1

        for add in self.adds:
            if add.hp <= 0:
                self.adds.remove(add)
                for agent in self.player_agents:
                    agent.last_reward += REWARD_KILL_ADD
                break

        if self.boss.hp <= 0:
            self.done = True
            for agent in self.player_agents:
                agent.last_reward += REWARD_KILL_BOSS
            print("Boss wurde besiegt!")

        if all(player.is_dead for player in self.players):
            self.done = True
            print("Alle Spieler sind tot!")

        if self.done:
            for agent in self.player_agents:
                agent.on_done()

    def render(self):
        pass

    def log_action(self, entity, action_name, reward):
        log_message = f"{entity.player_class if isinstance(entity, Player) else 'Boss'} performed {action_name} with reward {reward}"
        print(log_message)
        with open("combat_log.txt", "a") as file:
            file.write(log_message + "\n")
