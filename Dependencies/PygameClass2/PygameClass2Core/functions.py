import pygame, time, math, sys, random
pygame.init()

def dirToRad(dir):
    return (2*dir*math.pi)/360

def radToDir(rad):
    return (rad*360)/(2*math.pi)

def secondsToFormat(s):
    t = {"h":3600, "m":60, "s":1}
    for i in t:
        f = s//t[i]
        s -=  f * t[i]
        t[i] = f
    return "{}:{}:{}".format(*list(["0"+str(i) if len(str(i)) < 2 else i for i in t.values()]))