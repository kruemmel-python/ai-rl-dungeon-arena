# melee_dps_3_actions.py
class MeleeDps3Actions:
    def do_player_action(self, player, class_name, action_type, action_name, reward):
        if action_type == "melee_attacks":
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
        elif action_type == "ranged_attacks":
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
        elif action_type == "buffs":
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
        elif action_type == "dots":
            target = self.boss
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
        elif action_type == "unique":
            if action_name.split("_")[-1] == "demon_form":
                reward += 0.5
        return reward