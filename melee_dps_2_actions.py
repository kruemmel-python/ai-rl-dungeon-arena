# melee_dps_2_actions.py
class MeleeDps2Actions:
    def do_player_action(self, player, class_name, action_type, action_name, reward):
        if action_type == "melee_attacks":
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
        elif action_type == "ranged_attacks":
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
        elif action_type == "buffs":
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
        elif action_type == "dots":
            target = self.boss
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
        elif action_type == "unique":
            if action_name.split("_")[-1] == "avatar":
                reward += 0.4
        return reward