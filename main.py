import pygame
import time
from random import randint

pygame.init()
online = True
pygame.display.set_mode((800, 600))
n = 0
g = 0
queue = []  # cписок


def add2q(amount):
    for i in range(amount):
        queue.append(Client(n, randint(100, 500)))


def done():
    queue.pop(0)


def gone(client_index):
    global g
    queue.pop(client_index)
    g += 1


class Client:
    def __init__(self, time_arrive, max_wait_time=10, name='Basilio'):
        self.time_arrive = time_arrive
        self.max_wait_time = max_wait_time
        self.name = name
        self.in_progress = False

    def __str__(self):
        prefix = ''
        if self.in_progress:
            prefix = '*'
        return prefix + '(a:' + str(round(self.time_arrive/10, 2)) +\
               ', w:' + str(round(-n + self.time_arrive + self.max_wait_time, 2)) + ')'


processing = 0

while online:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            online = False
    if randint(0, 100) > 97:
        add2q(randint(1, 5))
    for i in range(len(queue) - 1, -1, -1):
        if queue[i].max_wait_time < (n - queue[i].time_arrive) and not queue[i].in_progress:
            gone(i)
    if processing > 0:
        processing -= 1
        if processing == 0:
            done()
    elif len(queue) > 0:
        queue[0].in_progress = True
        processing = randint(10, 15)
    time.sleep(0.1)
    n += 1
    if n % 10 == 0:
        print(n // 10, end='  ')
        print(g, end='  ')
        if len(queue) > 0:
            print(len(queue), end='  ')
            for i in range(len(queue)):
                print(queue[i], end=',')
        print('')
pygame.quit()

# % - остаток от деления
# // - целая часть от деления
# / - деление

# 0. все не именованные константы вынести в переменные