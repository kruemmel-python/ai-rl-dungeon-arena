# ranged_dps_3_actions.py
class RangedDps3Actions:
    def do_player_action(self, player, class_name, action_type, action_name, reward):
        if action_type == "melee_attacks":
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
            if action_name.split("_")[-1] == "incarnation":
                reward += 0.5
        return reward