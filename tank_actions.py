# tank_actions.py
class TankActions:
    def do_player_action(self, player, class_name, action_type, action_name, reward):
        if action_type == "melee_attacks":
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
        elif action_type == "ranged_attacks":
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
        elif action_type == "buffs":
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
        elif action_type == "dots":
            target = self.boss
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
        elif action_type == "unique":
            if action_name.split("_")[-1] == "avenger_shield":
                target = self.boss
                target.take_damage(20)
                reward += REWARD_HIT_BOSS
        return reward