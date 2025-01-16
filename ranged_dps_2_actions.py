# ranged_dps_2_actions.py
class RangedDps2Actions:
    def do_player_action(self, player, class_name, action_type, action_name, reward):
        if action_type == "melee_attacks":
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
        elif action_type == "ranged_attacks":
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
        elif action_type == "buffs":
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
        elif action_type == "dots":
            target = self.boss
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
        elif action_type == "unique":
            if action_name.split("_")[-1] == "stampede":
                reward += 0.5
        return reward