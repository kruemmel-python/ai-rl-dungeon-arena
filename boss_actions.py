# boss_actions.py
# Enthält die Logik für die Boss-Aktionen, z. B. do_boss_melee_action, do_boss_ranged_action, do_boss_buffs_action, do_boss_dots_action und do_boss_special_action

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
