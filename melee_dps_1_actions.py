# melee_dps_1_actions.py
class MeleeDps1Actions:
    def do_player_action(self, player, class_name, action_type, action_name, reward):
        if action_type == "melee_attacks":
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
        elif action_type == "ranged_attacks":
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
        elif action_type == "buffs":
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
        elif action_type == "dots":
            target = self.boss
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
        elif action_type == "unique":
            if action_name.split("_")[-1] == "death_from_above":
                target = self.boss
                target.take_damage(25)
                reward += REWARD_HIT_BOSS
        return reward