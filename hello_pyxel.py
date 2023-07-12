import pyxel as PX

class App:
    def __init__(self):
        PX.init(160,120, title="HelloWorld",display_scale=2)
        PX.image(0).load(0, 0, "assets/pyxel_logo_38x16.png")
        PX.run(self.update, self.draw)

    def update(self):
        if PX.btnp(PX.KEY_Q):PX.quit() # q key to quit

    def draw(self):
        PX.cls(0)
        color=PX.frame_count % 16
        PX.text(55, 41, "Hello World, Pyxel!", color)
        PX.blt(61, 66, 0, 0, 0, 38, 16)
App()
