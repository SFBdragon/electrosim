from raylibpy import *
from math import *
import random


t = 0
fps = 60
dt = 1/60

width = 1280
height = 720
screen_center = Vector2(width/2,height/2)

class Particle:
    def __init__(self, pos, vel, mass, charge):
        self.pos = pos + screen_center
        self.vel = vel
        self.mass = mass
        self.charge = charge
        self.radius = sqrt(mass) * 20

e = 1
me = 0.2
mp = 2


def main():
    ps = [
        Particle(Vector2( 100, -300), Vector2(50,300),   me, -e), # electron
        Particle(Vector2( -200, -300), Vector2(-200,200),   me, -e), # electron
        Particle(Vector2( 400, 300), Vector2(0,-500),   me, -e), # electron
        Particle(Vector2( 200,  50), Vector2(100,0),   mp, e),    # proton
        Particle(Vector2(-100, -100), Vector2(-40,0), 4*mp, e*2),      # alpha
    ]

    init_window(width, height, "Electric Interaction Sim")

    set_target_fps(fps/2)

    view = True

    while not window_should_close():

        for i in range(len(ps)):
            f = Vector2()
            for j in range(len(ps)):
                if i != j:
                    s = ps[j].pos - ps[i].pos
                    f += 9e6 * ps[i].charge * ps[j].charge / max(s.length**3, 0.0001) * -s
                    
            ps[i].vel += f / ps[i].mass * dt
            ps[i].pos += ps[i].vel * dt

        if is_key_pressed(KEY_SPACE):
            view = not view

        if is_key_pressed(KEY_R):
            for part in ps:
                part.pos = Vector2((random.random() - 0.5) * 700, (random.random() - 0.5) * 700) + screen_center
                part.vel = Vector2((random.random() - 0.5) * 700, (random.random() - 0.5) * 700)

        begin_drawing()
        clear_background(RAYWHITE)

        draw_text("Press Space To Switch View, R to Reset", 0, 0, 30, Color(0,0,0,100))

        for part in ps:
            intens = part.charge / e * 50
            color = Color(intens, 0, 0, 255) if part.charge > 0 else Color(0, 0, intens, 255)
            draw_circle_v(part.pos, part.radius, color)

        if view:
            freq = 40
            for x in range(freq, width - freq//2, freq):
                for y in range(freq, width - freq//2, freq):
                    p = Vector2(x, y)
                    f = Vector2()
                    for j in range(len(ps)):
                        s = ps[j].pos - Vector2(x,y)
                        if s.length < part.radius:
                            break
                        f += ps[j].charge / max(s.length**3, 0.0001) * -s
                    else:
                        fm = f.length
                        f = f * 100000

                        draw_color = Color(min(f.length, 255), 200, 0, 255)
                        draw_line_v(p, p + f, draw_color)
                        draw_circle_v(p + f, 2, draw_color)
        else:
            for part in ps:
                if part.charge < 0:
                    continue
                for x in [-1, -0.5, 0, 0.5, 1]:
                    for y in [-1, -0.5, 0, 0.5, 1]:
                        if x == 0 and y == 0:
                            continue

                        ff = 1 if part.charge > 0 else -1
                        p = part.pos + Vector2(x, y).normalize() * (part.radius+0.1)
                        cont = True
                        i = 0

                        while cont:# and 0 < p.x < width and 0 < p.y < height:
                            f = Vector2()
                            for party in ps:
                                s = party.pos - p
                                if s.length < party.radius:
                                    cont = False
                                f += party.charge / max(s.length**3, 0.000000001) * -s
                            
                            np = p + f.normalize() * 10 * ff
                            draw_line_v(p, np, Color(0,0,0,255))
                            p = np

                            i += 1
                            if i > 100:
                                break
                

        end_drawing()

    close_window()

if __name__ == '__main__':
    main()

