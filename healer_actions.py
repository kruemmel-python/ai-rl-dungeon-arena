# healer_actions.py
class HealerActions:
    def do_player_action(self, player, class_name, action_type, action_name, reward):
        if action_type == "melee_attacks":
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
        elif action_type == "ranged_attacks":
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
        elif action_type == "buffs":
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
        elif action_type == "dots":
            target = self.boss
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
        elif action_type == "unique":
            if action_name.split("_")[-1] == "guardian_spirit":
                player.hp += 20
                reward += REWARD_HEAL_PLAYER
        return reward