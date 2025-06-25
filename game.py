import pyxel

# 定数
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_INTERVAL, START_SCENE, PLAY_SCENE

# クラス
from entities import Item, Bullet, Explosion, Heart
from enemy import Enemy
from enemy_type import get_enemy_type_by_stage


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="mokoゲーム")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        self.current_scene = START_SCENE

        pyxel.run(self.update, self.draw)

    def reset_play_scene(self):
        self.player_x = SCREEN_WIDTH / 2
        self.player_y = SCREEN_HEIGHT * 4 / 5
        self.hp = 3
        self.score = 0
        self.items = []
        self.bullets = []
        self.shot_interval = 5
        self.shot_timer = 0
        self.explosions = []
        self.hearts = []
        self.enemies = []
        self.item_collision = False
        self.shot = False
        self.enemy_collision = False
        self.heart_collision = False
        self.item_timer = 0
        self.item_timer_max = 300
        self.heart_timer = 0
        self.collision_timer = 0
        self.stage = 1
        self.stage_timer = 0
        self.stage_duration = 1800


    def update_start_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE


    def update_play_scene(self):
        #ステージのカウント
        self.stage_timer += 1
        if self.stage_timer > self.stage_duration:
            self.stage += 1
            self.stage_timer = 0

        #無敵時間のカウント
        if self.collision_timer > 0:
            self.collision_timer -= 1
        else:
            self.enemy_collision = False

        if self.hp == 0:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.current_scene = START_SCENE
            return

        #ミクの移動
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH - 15:
            self.player_x += 2
        elif pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 0:
            self.player_x -= 2

        #敵の追加
        if pyxel.frame_count % ENEMY_INTERVAL == 0:
            enemy_type = get_enemy_type_by_stage(self.stage)
            self.enemies.append(Enemy(pyxel.rndi(0, SCREEN_WIDTH - 8), 0, enemy_type))

        #敵の移動
        for enemy in self.enemies.copy():
            enemy.update()

            #当たり判定
            if (enemy.x < self.player_x + 7 < enemy.x + 15 and
                enemy.y < self.player_y + 8 < enemy.y + 16
                ):

                if self.enemy_collision == False:
                    self.hp -= 1
                    self.enemy_collision = True
                    self.collision_timer = 30
                    pyxel.play(0, 1) 
                    self.explosions.append(Explosion(enemy.x + 8, enemy.y + 8))
                    self.enemies.remove(enemy)
                

            #画面外に出た敵の削除
            if enemy.y >= SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.score += 50


        #ハートの追加
        if pyxel.frame_count % ENEMY_INTERVAL == 0:
            if pyxel.rndi(0,100) == 0:
                self.hearts.append(Heart(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))

        if self.heart_timer > 0:
            self.heart_timer -= 1

        #ハートの移動
        for heart in self.hearts.copy():
            heart.update()

            #当たり判定
            if (heart.x < self.player_x + 7 < heart.x + 8 and
                heart.y < self.player_y + 8 < heart.y + 8
                ):

                if self.hp < 3:
                    self.hp += 1
                    pyxel.play(0, 0) 
                    self.hearts.remove(heart)
                    self.heart_timer = 8
                    
            #画面外に出たハートの削除
            if heart.y >= SCREEN_HEIGHT:
                self.hearts.remove(heart)
                
        #強化アイテムの追加
        if pyxel.frame_count % ENEMY_INTERVAL == 0:
            if pyxel.rndi(0,150) == 0:
                self.items.append(Item(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))

        if self.item_timer > 0:
            self.item_timer -= 1

        #強化アイテムの移動
        for item in self.items.copy():
            item.update()

            #当たり判定
            if (item.x < self.player_x + 7 < item.x + 16 and
                item.y < self.player_y + 8 < item.y + 16
                ):
                pyxel.play(0, 0) 
                self.shot = True
                self.items.remove(item)
                self.item_timer = self.item_timer_max
                    
            #画面外に出た強化アイテムの削除
            if item.y >= SCREEN_HEIGHT:
                self.items.remove(item)

        #弾を撃つ
        if self.shot and pyxel.btn(pyxel.KEY_SPACE):
            if pyxel.frame_count % 2 < 1:
               pyxel.play(0, 3)
               self.bullets.append(Bullet(self.player_x + 7, self.player_y))

        #弾の追加
        for bullet in self.bullets.copy():
            bullet.update()
        #画面外に出た時の処理
            if bullet.y < 0:
                self.bullets.remove(bullet)
            
        #弾の当たり判定
            for enemy in self.enemies.copy(): 
                if (enemy.x - 2 < bullet.x < enemy.x + 17 and
                    enemy.y - 2 < bullet.y < enemy.y + 18
                    ):
                    self.enemies.remove(enemy)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    pyxel.play(0, 2)
                    self.explosions.append(Explosion(enemy.x + 8, enemy.y + 8))
                    self.score += 200
                    break

        #強化時間
        if self.item_timer <= 0:
            self.shot = False

        #敵撃破のエフェクト
        for explosion in self.explosions.copy():
            explosion.update()
            if explosion.timer <= 0:
                self.explosions.remove(explosion)



    def draw_start_scene(self):
        pyxel.cls(pyxel.COLOR_GREEN)
        pyxel.text(SCREEN_WIDTH / 2 - 25, SCREEN_HEIGHT / 2,
                   "Enter to Start", pyxel.COLOR_PINK)

    
    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        pyxel.rect(0, SCREEN_HEIGHT * 9 / 10, SCREEN_WIDTH, 
                   SCREEN_HEIGHT * 1 / 5
                   , pyxel.COLOR_BROWN)
        
        #ステージ切り替え
        pyxel.text(165, 5, f"Stage: {self.stage}", pyxel.COLOR_WHITE)

        #強化アイテム
        for item in self.items:
            item.draw()
        #強化時間
        if self.shot:
            bar_x = 19.75
            bar_y = 72
            bar_w = 162.25
            bar_h = 5

            current_w = int(bar_w * self.item_timer / self.item_timer_max)
            #バー
            pyxel.rect(bar_x, bar_y, bar_w, bar_h, pyxel.COLOR_GRAY)
            pyxel.rect(bar_x, bar_y, current_w, bar_h, pyxel.COLOR_RED)

            # 小数第2位までの残り時間（秒）を計算
            remaining_sec = self.item_timer / 30
            time_str = f"{remaining_sec:.2f}"  # 小数第2位まで

            # 数字の表示
            text_x = bar_x + (bar_w - len(time_str) * 4) // 2
            text_y = bar_y + 6
            pyxel.text(text_x, text_y, time_str, pyxel.COLOR_WHITE)

        #弾
        for bullet in self.bullets:
            bullet.draw()

        #爆発
        for explosion in self.explosions:
            explosion.draw()


        #ハート
        for heart in self.hearts:
            heart.draw()

        #敵
        for enemy in self.enemies:
            enemy.draw()

        #GAMEOVER画面
        if self.hp == 0:
            pyxel.blt(self.player_x, self.player_y, 0, 
                      16, 0, 16, 16, pyxel.COLOR_BLACK)
            pyxel.text(SCREEN_WIDTH / 2 - 19, SCREEN_HEIGHT / 2 - 10,
                       "GAME OVER", pyxel.COLOR_YELLOW)
            pyxel.text(SCREEN_WIDTH / 2 - 32, SCREEN_HEIGHT / 2 + 2,
                       f"Final Score:{self.score}", pyxel.COLOR_YELLOW)
            pyxel.text(SCREEN_WIDTH / 2 - 29, SCREEN_HEIGHT / 2 + 15,
                       "Retry to Enter", pyxel.COLOR_YELLOW)
            
            return
        
        #ミク
        if not self.enemy_collision or pyxel.frame_count % 6 < 3:
            pyxel.blt(self.player_x, self.player_y, 0, 
                      16, 0, 16, 16, pyxel.COLOR_BLACK)

        #HP表示
        for hp_x in range(self.hp):
            pyxel.blt(hp_x * 10 + 5, 5, 0, 
                      32, 0, 8, 16, pyxel.COLOR_RED)
        #HPの消えるエフェクト    
        if 28 < self.collision_timer < 30:
            pyxel.blt(hp_x * 10 + 15, 5, 0, 
                      48, 0, 7, 16, pyxel.COLOR_BLACK)
        if 26 < self.collision_timer <= 28:
            pyxel.blt(hp_x * 10 + 15, 5, 0, 
                      40, 0, 8, 16, pyxel.COLOR_BLACK)
        #HP回復エフェクト    
        if 0 < self.heart_timer < 2 or 4 < self.heart_timer < 6:
            pyxel.blt(hp_x * 10 + 5, 5, 0, 
                      65, 0, 8, 8, pyxel.COLOR_BLACK)
        if 2 <= self.heart_timer < 4 or 6 <= self.heart_timer < 8:
            pyxel.blt(hp_x * 10 + 5, 5, 0, 
                      65, 0, 8, 8, pyxel.COLOR_BLACK)


        #スコア表示
        pyxel.text(5, 23, f"SCORE:{self.score}", pyxel.COLOR_WHITE)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()


        if self.current_scene == PLAY_SCENE:
            self.update_play_scene()
        elif self.current_scene == START_SCENE:
            self.update_start_scene()
        

    def draw(self):
        if self.current_scene == PLAY_SCENE:
            self.draw_play_scene()
        elif self.current_scene == START_SCENE:
            self.draw_start_scene()


App()