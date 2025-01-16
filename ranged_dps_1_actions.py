# ranged_dps_1_actions.py
class RangedDps1Actions:
    def do_player_action(self, player, class_name, action_type, action_name, reward):
        if action_type == "melee_attacks":
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
        elif action_type == "ranged_attacks":
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
        elif action_type == "buffs":
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
        elif action_type == "dots":
            target = self.boss
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
        elif action_type == "unique":
            if action_name.split("_")[-1] == "meteor":
                target = self.boss
                target.take_damage(25)
                reward += REWARD_HIT_BOSS
        return reward