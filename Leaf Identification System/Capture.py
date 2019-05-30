import pygame as pg
import pygame.camera
import os
import threading as th

class Capture():

    def __init__(self, parent):
        os.environ['SDL_WINDOWID'] = str(parent.embed.winfo_id())

        pg.display.init()
        pg.camera.init()

        self.size = (640,480)
        self.display = pg.display.set_mode(self.size)
        self.display.fill(pg.Color(255,255,255))

        pg.display.update()

        self.clist = pg.camera.list_cameras()#getting list of cameras, false if none

        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        print('cameras:', self.clist)

        self.cam = pg.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        self.snapshot = pg.surface.Surface(self.size, 0, self.display)

        self.runView = True

        self.event = th.Thread(target=self.eventCatcher)
        self.view = th.Thread(target=self.camView)
        self.event.start()
        self.view.start()

    def click(self):
        self.runView = False

    def reset(self):
        self.runView = True
        self.view = th.Thread(target=self.camView)
        self.view.start()
        

    def snap(self):
        img = self.cam.get_image()
        self.display.blit(img, img.get_rect())
        pg.display.update()
        pg.image.save(img, "image.jpg")
        print("Image Saved")

    def camView(self):#will be used as a seperate thread
        while self.runView:
            #print('snap ready:', self.cam.query_image())
            self.cam.get_image(self.snapshot)
            self.display.blit(self.snapshot, self.snapshot.get_rect())
            pg.display.update()
        self.snap()

    def eventCatcher(self):
        print("Event Catcher Triggered")
        closed = False
        while not closed:
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    self.cam.stop()
                    closed = True
