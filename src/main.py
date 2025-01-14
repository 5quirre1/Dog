from tkinter import *
import pygame
import random
import pyttsx3
import threading
import os

message_label = None
engine = pyttsx3.init()
exploded = False

def dog_click_message(event):
    global message_label
    if message_label:
        message_label.destroy()
    messages = [
        "Woof", "eggs", "greg", "save me", "I'm gay",
        '''
It starts with one, one thing, I don't know why
It doesn't even matter how hard you try
Keep that in mind, I designed this rhyme to explain in due time
All I know, time is a valuable thing
Watch it fly by as the pendulum swings
Watch it count down to the end of the day, the clock ticks life away
It's so unreal, didn't look out below
Watch the time go right out the window
Tryna hold on, d-didn't even know
I wasted it all just to watch you go
I kept everything inside and even though I tried, it all fell apart
What it meant to me will eventually be a memory of a time when
I tried so hard and got so far
But in the end, it doesn't even matter
I had to fall to lose it all
But in the end, it doesn't even matter
One thing, I don't know why
It doesn't even matter how hard you try
Keep that in mind, I designed this rhyme
To remind myself how I tried so hard
In spite of the way you were mockin' me
Actin' like I was part of your property
Rememberin' all the times you fought with me
I'm surprised it got so far
Things aren't the way they were before
You wouldn't even recognize me anymore
Not that you knew me back then, but it all comes back to me in the end
You kept everything inside and even though I tried, it all fell apart
What it meant to me will eventually be a memory of a time when
I tried so hard and got so far
But in the end, it doesn't even matter
I had to fall to lose it all
But in the end, it doesn't even matter
I've put my trust in you
Pushed as far as I can go
For all this, there's only one thing you should know
I've put my trust in you
Pushed as far as I can go
For all this, there's only one thing you should know
I tried so hard and got so far
But in the end, it doesn't even matter
I had to fall to lose it all
But in the end, it doesn't even matter
'''
    ]
    #in the end
    message = random.choice(messages)
    message_label = Label(root, text=message, bg="white", font=("Arial", 12))
    message_label.place(x=dog.dog_label.winfo_x(), y=dog.dog_label.winfo_y() - 20)

    threading.Thread(target=lambda: (engine.stop(), engine.say(message), engine.runAndWait()), daemon=True).start()

    message_label.after(3000, message_label.destroy)

class Dog:
    def __init__(self, root):
        self.root = root
        self.dog_photo = PhotoImage(file=os.path.join("src", "stuff", "stupid_egg_dog.png"))
        self.dog_photo = self.dog_photo.subsample(2, 2)
        self.dog_label = Label(root, image=self.dog_photo)
        self.dog_label.image = self.dog_photo
        self.dog_label.place(x=200, y=180)

        self.bg_music = os.path.join("src", "stuff", "main.mp3")
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.Sound(self.bg_music)
        self.music.set_volume(0.2)
        self.music.play(-1)

        self.walk_sound = os.path.join("src", "stuff", "mr-krabs-walking.mp3")
        self.walk_sound = pygame.mixer.Sound(self.walk_sound)
        self.walk_sound_playing = False
        self.moving = False
        self.speed = 5

    def move_dog(self, key):
        global message_label
        if message_label:
            message_label.destroy()
        if not exploded:
            if key == "Up":
                new_y = self.dog_label.winfo_y() - self.speed
                if new_y < 0:
                    new_y = self.root.winfo_height() - self.dog_label.winfo_height()
                self.dog_label.place(x=self.dog_label.winfo_x(), y=new_y)
            elif key == "Down":
                new_y = self.dog_label.winfo_y() + self.speed
                if new_y > self.root.winfo_height() - self.dog_label.winfo_height():
                    new_y = 0
                self.dog_label.place(x=self.dog_label.winfo_x(), y=new_y)
            elif key == "Left":
                new_x = self.dog_label.winfo_x() - self.speed
                if new_x < 0:
                    new_x = self.root.winfo_width() - self.dog_label.winfo_width()
                self.dog_label.place(x=new_x, y=self.dog_label.winfo_y())
            elif key == "Right":
                new_x = self.dog_label.winfo_x() + self.speed
                if new_x > self.root.winfo_width() - self.dog_label.winfo_width():
                    new_x = 0
                self.dog_label.place(x=new_x, y=self.dog_label.winfo_y())

    def start_walking_sound(self):
        if not self.walk_sound_playing:
            self.walk_sound.play(-1)
            self.walk_sound_playing = True

    def stop_walking_sound(self):
        if self.walk_sound_playing:
            self.walk_sound.stop()
            self.walk_sound_playing = False

    def explode_dog(self):
        global exploded
        if not exploded:
            exploded = True
            self.music.stop()

            explosion_message = "I'm going to explode now"
            threading.Thread(target=lambda: (engine.stop(), engine.say(explosion_message), engine.runAndWait()), daemon=True).start()

            explosion_image = PhotoImage(file=os.path.join("src", "stuff", "explosion.png"))
            explosion_image = explosion_image.subsample(2, 2)
            explosion_label = Label(self.root, image=explosion_image)
            explosion_label.image = explosion_image
            explosion_label.place(x=self.dog_label.winfo_x(), y=self.dog_label.winfo_y())

            explosion_sound = pygame.mixer.Sound(os.path.join("src", "stuff", "loud-explosion.mp3"))
            explosion_sound.play()

            self.root.after(2000, root.destroy)

root = Tk()
root.configure(bg="teal")
root.geometry("1000x700")
root.title("dog")

icon_path = os.path.join("src", "stuff", "stupid_egg_dog.ico")
root.iconbitmap(os.path.abspath(icon_path))

dog = Dog(root)

keys_pressed = set()

def key_press(event):
    if exploded:
        root.destroy()
    if event.keysym.upper() == "E":
        dog.explode_dog()
    if event.keysym in ["Up", "Down", "Left", "Right"] and not exploded:
        keys_pressed.add(event.keysym)
        if not dog.moving:
            dog.moving = True
            dog.start_walking_sound()
            move_dog()

def key_release(event):
    if event.keysym in ["Up", "Down", "Left", "Right"]:
        keys_pressed.discard(event.keysym)
        if not keys_pressed:
            dog.moving = False
            dog.stop_walking_sound()

def move_dog():
    if dog.moving and not exploded:
        for key in list(keys_pressed):
            dog.move_dog(key)
        root.after(50, move_dog)

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)
dog.dog_label.bind("<Button-1>", dog_click_message)
root.mainloop()
