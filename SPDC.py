# trp4fb, zy2qd, jcg6dn

"""

Created using Luther Tychonievich's gamebox.

WARNING: GAME WILL TAKE A FEW SECONDS TO DOWNLOAD ALL ASSETS FROM WEB

"""

import pygame, random, gamebox, os

CAPTION = "SOMEWHAT DEEP SPACE CHASE"
pygame.display.set_caption(CAPTION)


# memory management and permanent data storage
def createFolder():
    global big_asteroid_choices
    global mid_asteroid_choices
    global small_asteroid_choices
    os.mkdir("asteroidchase_logs")
    os.chdir("./asteroidchase_logs")
    scores = open("highscores.txt", 'x')
    scores.close()
    #force loading all the asteroid images we'll need later upfront so it doesn't download them during play
    for choice in big_asteroid_choices:
        lagKiller = gamebox.from_image(0, 0, choice)

    for choice in mid_asteroid_choices:
        lagKiller2 = gamebox.from_image(0, 0, choice)

    for choice in small_asteroid_choices:
        lagKiller3 = gamebox.from_image(0, 0, choice)
    with open("highscores.txt", 'a') as scores:
        scores.write("0\n")


def writeScore(score):
    score = str(score)
    with open("highscores.txt", 'a') as scores:
        scores.write(score + '\n')


def readScore():
    with open("highscores.txt", 'r') as scores:
        max = 0
        for line in scores:
            line = int(line)
            if line > max:
                max = int(line)
        return str(max)


# title and instruction screens
Width, Length = 800, 700
camera = gamebox.Camera(Width, Length)
imageLink = "https://virginia.box.com/shared/static/"  # used to shorten code in the future

# music
music = gamebox.load_sound(imageLink + "cb5aac92sf9r1zm9ztmb5vxu7g19s4pa")
musicplayer3 = music.play(-1)

# loading screens
splashscreen1 = gamebox.load_sprite_sheet(imageLink + "v661x3zpy4fge6wi8ubbinp3ey0r4495", 1, 16)
splashscreen1dummy = gamebox.from_color(camera.x, camera.y, 'black', 800, 700)
splashscreen2 = gamebox.load_sprite_sheet(imageLink + "g7wvy29g47qjgkrdobmiqctyuhxnjtil", 1, 16)
splashscreen2dummy = gamebox.from_color(camera.x, camera.y, 'black', 800, 700)

# conditions that control appearance of menus and other items
game_on = False
g_on = False

# used for animation of ship sprites
SHIPSHEETCOUNT = 5
positionLog = [600]
animationLog = [5]

# boundaries to keep player on the screen
leftside = gamebox.from_color(-25, 300, "black", 50, 10000)
rightside = gamebox.from_color(825, 300, "black", 50, 10000)

# creation of ship sprites
friendly_sheet = gamebox.load_sprite_sheet(imageLink + "yff7ywt1t2s6ogt6ds9gfpfbykce4as0", 1, 12)
spaceship = gamebox.from_image(600, 450, friendly_sheet[5])
spaceship.scale_by(.25)
enemy_sheet = gamebox.load_sprite_sheet(imageLink + "pc8pudop3p1vcd6i73pbsyuagj3zuk9g", 1, 12)
enemy = gamebox.from_image(600, 650, enemy_sheet[5])
enemy.scale_by(.25)

# health bar and values
h_l, h_w = 30, 16
hx, hy = 600, 50
health1 = gamebox.from_color(hx, hy, "green", h_w, h_l)
health2 = gamebox.from_color(hx + 20, hy, "green", h_w, h_l)
health3 = gamebox.from_color(hx + 40, hy, "green", h_w, h_l)
health4 = gamebox.from_color(hx + 60, hy, "green", h_w, h_l)

# laser beam and end of game message
bullet = gamebox.from_color(enemy.x, 650, "red", 3, 20)
bullet.yspeed = 10
gameOVER = gamebox.from_text(400, 350, "GAME OVER", "arial", 100, "red")

COUNTER = 0  # controls most timing based functions
ASTEROID_VELOCITYy = 16  # speed it looks like you are flying
asteroids = list()  # list of all the asteroids on the screen at any given time
score = 0
time = 0

# for the sake of variety there a number of asteroid images for the generator to choose from
big_asteroid_choices = [imageLink + "qvb610m82uo8bjh0gdz7g3kxupa1gq5y", imageLink + "pb5nc45fwngwu8lbio0zouu2zfh90rgn",
                        imageLink + "9kjry266698ygwjby27g0lbsmthh3bur"]
mid_asteroid_choices = [imageLink + "iqnkbi2umx29hvdjfpgu4lpru8r8z7cp", imageLink + "h5e2yhnanmi6m619f0y3lybixqc24qtz",
                        imageLink + "598kqah7zogfi7rvq1ggveux3ymo0fm0"]
small_asteroid_choices = [imageLink + "wxmqfziwd0r5y8rscx3afo21r1u2qmvl",
                          imageLink + "1sjm8by3tpaiuemuvh68o3odvhqjryj8",
                          imageLink + "xk63c7d6t9m3cau3qztuahdeqmz3e80w"]

def starry_background():  # creates the randomly generated background
    if COUNTER % 5 == 0:  # approx 1/6 sec
        numstars = random.randint(0, 7)  # number of stars to generate for a row each 1/6 sec
        for i in range(numstars):
            stars.append(gamebox.from_color(random.randint(5, Width - 5), 0, "white", 3, 3))
    for star in stars:
        # move the star down the window by increasing y.
        star.y += 4
        if star.y > Length:
            stars.remove(star)

        camera.draw(star)

def healthbar():  # draws the health status bar
    camera.draw(health1)
    camera.draw(health2)
    camera.draw(health3)
    camera.draw(health4)

done = True

try:
    os.chdir("./asteroidchase_logs")
except:  # if the dir doesn't exist, it creates it.
    createFolder()

def asteroidGenerate():  # asteroid generation function
    global ASTEROID_VELOCITYy
    if COUNTER % (60) == 0:
        asteroidcount = random.randint(1, 3)  # determines how many asteroids will spawn on this row
        bigmediumsmall = random.randint(0, 2)  # determines if a big, small, or medium asteroid will be created
        if bigmediumsmall == 0:
            for i in range(asteroidcount):
                randX = random.randint(5, Width - 5)  # random position
                image_choice = small_asteroid_choices[
                    random.randint(0, 2)]  # random image from within that asteroid's size category
                randRot = random.randint(0, 270)  # random rotation
                astbox = gamebox.from_image(randX, -400, image_choice)
                randSize = random.uniform(2, 5)  # random real number between 2 and 5 to scale by
                astbox.rotate(randRot)
                astbox.scale_by(randSize)
                asteroids.append(astbox)
        elif bigmediumsmall == 1:
            for i in range(asteroidcount):
                randX = random.randint(5, Width - 5)
                image_choice = mid_asteroid_choices[random.randint(0, 2)]
                randRot = random.randint(0, 270)
                astbox = gamebox.from_image(randX, -400, image_choice)
                randSize = random.uniform(2, 5)
                astbox.rotate(randRot)
                astbox.scale_by(randSize)
                asteroids.append(astbox)
        else:
            for i in range(asteroidcount):
                randX = random.randint(5, Width - 5)
                image_choice = big_asteroid_choices[random.randint(0, 2)]
                randRot = random.randint(0, 270)
                astbox = gamebox.from_image(randX, -400, image_choice)
                randSize = random.uniform(2, 5)
                astbox.rotate(randRot)
                astbox.scale_by(randSize)
                asteroids.append(astbox)

    for astbox in asteroids:
        astbox.speedy = ASTEROID_VELOCITYy
        if astbox.y > 3000:
            asteroids.remove(astbox)  # saving memory
        if bullet.top_touches(astbox):
            asteroids.remove(astbox)
            bullet.y = -20
        if spaceship.touches(astbox, -15,
                             -15):  # collisions with some overlap to help with near misses in the dangers of the asteroid belt
            asteroids.remove(astbox)
            if health1.x == hx:
                health1.x = 1000
            elif health2.x == hx + 20:
                health2.x = 1020
            elif health3.x == hx + 40:
                health3.x = 1040
            elif health4.x == hx + 60:
                health4.x = 1060

        astbox.move_speed()
        camera.draw(astbox)

def enemyAI():
    # player and enemy are held 200 pixels apart. The ticks it takes for the asteroids to get travel that distance is = 200/ASTEROID_VELOCITYy
    global ASTEROID_VELOCITYy
    global animationLog
    delay = 200 // ASTEROID_VELOCITYy
    global positionLog  # create a log of the player's position so that the enemy can match it
    global COUNTER
    if COUNTER > delay + 1:  # once the game has been running for the time it takes an asteroid to travel from the player to the enemy...
        enemy.x = positionLog[len(
            positionLog) - delay]  # move the enemy to where the player was when it safely dodged the asteroid a few ticks earlier
        enemy.image = enemy_sheet[animationLog[
            len(animationLog) - delay]]  # match the banking position the player's ship had when it was moving
    if len(positionLog) > delay + 1:
        del positionLog[0]  # memory preservation
        del animationLog[0]
    else:
        pass

ticks = 0

def tick(keys):
    global time
    global game_on
    global g_on
    global score
    global win
    global ticks
    global animationLog
    global done
    ticks += 1
    camera.clear('black')
    starry_background()
    if game_on == False:
        splashscreen1dummy.image = splashscreen1[(ticks // 3) % len(splashscreen1)]
        camera.draw(splashscreen1dummy)
        camera.display()
        if pygame.K_SPACE in keys:
            camera.clear('black')
            game_on = True
    elif game_on:
        splashscreen2dummy.image = splashscreen2[(ticks // 3) % len(splashscreen2)]
        camera.draw(splashscreen2dummy)
        camera.display()
        if pygame.K_UP in keys:
            g_on = True
            game_on = None

    if g_on:
        global COUNTER
        global SHIPSHEETCOUNT
        if done:
            time += 1
        else:
            time = 0
        COUNTER += 1
        camera.clear("black")
        starry_background()
        camera.draw(leftside)
        camera.draw(rightside)
        if spaceship.touches(rightside) or spaceship.touches(leftside):  # keeping the player on the screen
            spaceship.move_to_stop_overlapping(leftside)
            spaceship.move_to_stop_overlapping(rightside)

        if done:
            asteroidGenerate()

        healthbar()
        if time % 50 == 0 and done == True:
            score += 10

        score_box = gamebox.from_text(100, 60, "Score: " + str(score), "arial", 24, "white")
        camera.draw(score_box)
        seconds = str(int((time / ticks_per_second))).zfill(3)
        time_box = gamebox.from_text(100, 30, "Time: " + seconds, "arial", 24, "white")
        camera.draw(time_box)
        # end of timer change
        # banking animation
        if COUNTER % 15 == 0:  # keeps the frame rate a bit lower so the animation is slightly more visible; still tough with motion blur
            if SHIPSHEETCOUNT > 5:
                SHIPSHEETCOUNT -= 1  # the ship drifts back towards the no turn position over time unless you tell it not to.
            elif SHIPSHEETCOUNT < 5:
                SHIPSHEETCOUNT += 1
            if pygame.K_RIGHT in keys:
                if SHIPSHEETCOUNT > 5:
                    SHIPSHEETCOUNT += 2  # bank right
            if pygame.K_LEFT in keys:
                if SHIPSHEETCOUNT < 5:
                    SHIPSHEETCOUNT -= 2  # bank left
        if pygame.K_RIGHT in keys:
            spaceship.x += 15  # movement
        if pygame.K_LEFT in keys:
            spaceship.x -= 15
            spaceship.image = friendly_sheet[SHIPSHEETCOUNT]
        animationLog.append(SHIPSHEETCOUNT)  # allows enemy to know where to go and how to turn
        positionLog.append(spaceship.x)
        camera.draw(spaceship)
        enemyAI()  # he's coming for you
        if done:
            camera.draw(enemy)
            if (bullet.y <= -10 or spaceship.x == enemy.x) and time >= 30:
                if COUNTER % 40 == 0:  # bullet delay
                    bullet.y = enemy.y
                    bullet.x = enemy.x
                    camera.draw(bullet)
        if time >= 30:
            bullet.y = bullet.y - bullet.yspeed
            camera.draw(bullet)
        camera.display()
        if bullet.top_touches(spaceship) or bullet.touches(spaceship):
            bullet.y = -20
            if health1.x == hx:
                health1.x = 1000
            elif health2.x == hx + 20:
                health2.x = 1020
            elif health3.x == hx + 40:
                health3.x = 1040
            elif health4.x == hx + 60:
                health4.x = 1060

        if health4.x == 1060:
            writeScore(score)  # logs the result of your game to your hard drive
            high_score = readScore()  # finds max score in the text file that was created.
            high_score = gamebox.from_text(Width / 2, Length - 2 * Length / 3, "High Score: " + high_score, "arial", 35,
                                           "Yellow")
            current_score = gamebox.from_text(Width / 2, Length - Length / 3, "Score: " + str(score), "arial", 40,
                                              "Yellow")
            camera.draw(current_score)
            camera.draw(high_score)
            camera.draw(gameOVER)
            gamebox.pause()
    camera.display()

stars = []
ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)

'''

Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live. -Martin Golding

'''
