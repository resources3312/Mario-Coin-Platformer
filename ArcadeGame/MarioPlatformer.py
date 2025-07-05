import arcade



class Platformer(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title):
        super().__init__(screen_width, screen_height, screen_title)
        
        # Объявляем константы игры
        self.PLAYER_SPEED = 7 # Константа хранящая значение скорости игрока
        self.PLAYER_JUMP = 15 # Константа хранящая значение высоты прыжка игрока
        self.PLAYER_SCALING = 0.9 # Константа хранящая масштаб игрока по отношению к тайлу

        
        self.TILE_SCALING = 1.0 # Константа хранящая значение гравитации внутри уровня
        self.COIN_SCALING = 0.5 # Константа для хранения значения масштаба монеты по отношению к тайлу 
        self.GRAVITY = 1 # Константа содержащая значение гравитации
        
        self.score = 0 # Атрибут служащий для хранения текущего счета игрока 
        
        self.tilemap = None # Атрибут, инициализированный для хранения объекта карты уровня
        self.scene = None # Атрибут для хранения объекта сцены 'Scene'
        self.player = None # Атрибут для хранения объекта спрайта игрока
        self.ground_list = None # Атрибут служащий для хранения спрайтов из слоя ground
        self.coins_list = None # Атрибут для хранения спрайтов из слоя coins
        self.player_layer = None # Атрибут объявленный для хранения объектного слоя Player
        self.physics_engine = None # Атрибут для храния объекта физического движка
        
        arcade.set_background_color(arcade.csscolor.SKY_BLUE) # Устаавливаем SKY_BLUE в качестве фонового цвета уровня
        
        self.coin_sound = arcade.load_sound("res/sounds/coin_sound.ogg") # Атрибут для хранения звука взятия монеты
    
    def setup(self) -> None:
        self.tilemap = arcade.load_tilemap("res/maps/map.tmx", self.TILE_SCALING, {
            "ground": {"use_spatial_hash": True},
            "coins": {"use_spatial_hash": True}
        }) # Инициализируем атрибут для хранения карты уровня

        self.scene = arcade.Scene.from_tilemap(self.tilemap) # Присваиваем объект Scene атрибуту scene

        self.player = arcade.Sprite("res/images/player.png", self.PLAYER_SCALING) # Присваиваем атрибуту player объект Sprite
        
        self.player_layer = self.tilemap.object_lists["Player"] # Присваиваем атрибуту player_layer объектный слой

        self.player.center_x = self.player_layer[0].shape[0] # Устанавливаем начальную позицию игрока по оси X
        self.player.center_y = self.player_layer[0].shape[1] # Устанавливаем начальную позицию игрока по оси Y

        self.scene.add_sprite("Player", self.player) # Добавляем спрайт игрока в сцену
        
        self.ground_list = self.tilemap.sprite_lists["ground"] # Присваиваем слой ground атрибуту ground_list
        self.coins_list = self.tilemap.sprite_lists["coins"] # Присваиваем слой coins атрибуту coins_list

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, walls=self.ground_list, gravity_constant=self.GRAVITY) # Присваиваем атрибуту physics_engine объект физического движка 
    
    def on_draw(self) -> None:
        if len(self.coins_list) == 0: # Проверяем список спрайтов монет на наличие элементов
            self.clear()
            win_text = arcade.Text("WIN", 300, 300, arcade.csscolor.GOLD, 150) # Инициализируем атрибут хранящий надпись о победе игрока 
            win_text.draw() # Отображаем надпись о победе игрока

        else: # В случае наличия спрайтов в списке coins_list продолжаем отрисовку сцены и счета
            self.clear() # Очищаем экран приложения
            self.scene.draw() # Производим отрисовку сцены
            
            text = arcade.Text(f"Score: {self.score}", 15, 600, arcade.csscolor.GOLD, 25) # Инициализируем атрибут хранящий данные о счете игрока
            text.draw() # Отображаем текущий счет игрока

    

    def on_update(self, delta_time) -> None:
        self.physics_engine.update() # Запускаем цикл работы физического движка
        
        for coin in arcade.check_for_collision_with_list(self.player, self.coins_list):
            coin.remove_from_sprite_lists() # Удаляем спрайт монеты если он соприкоснулся с игроком
            self.score += 1 # Прибавляем единицу к счету игрока
            arcade.play_sound(self.coin_sound) # Воспроизводим звук взятие монеты

    def on_key_press(self, key, modifiers) -> None:
        match key:
            case arcade.key.UP:
                if self.physics_engine.can_jump(): # Проверяем, может ли игрок совершить прыжок в данный момент
                    self.player.change_y = self.PLAYER_JUMP # Устанавливаем новую позицию игрока по оси Y
            
            case arcade.key.RIGHT:
                self.player.change_x = self.PLAYER_SPEED # Устанавливаем новую позицию игрока по оси X
            
            case arcade.key.LEFT:
                self.player.change_x = -self.PLAYER_SPEED # Устанавливаем новую позицию игрока по оси X
    
    def on_key_release(self, key, modifiers) -> None:
        if key == arcade.key.LEFT or key == arcade.key.RIGHT: 
            self.player.change_x = 0 # Устанавливаем нулевое приращение позиции по оси X, если игрок отпустил нажатую клавишу



def main() -> None:
    platformer = Platformer(960, 640, "Mario platformer") # Инициализируем класс игры
    platformer.setup() # Конфигурируем игру с помощью метода setup()
    arcade.run() # Запускаем игру

if __name__ == '__main__': main()
