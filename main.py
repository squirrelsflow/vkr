import pygame
import time
from random import randint

pygame.init()
online = True
surface = pygame.display.set_mode((800, 600))
n = 0
game_speed = 100
min_ready_wait_time = 100  # минимальная граница выбора рандомного времени готовности ждать в очереди
max_ready_wait_time = 500  # максимальная граница выбора рандомного времени готовности ждать в очереди

prob_come = 3  # вероятность, что человек придёт
min_people_came_to_queue = 1  # минимальная граница выбора рандомного количества человек в очереди
max_people_came_to_queue = 5  # максимальная граница выбора рандомного количества человек в очереди
min_time_of_processing = 10  # минимальное время обслуживания одного клиента
max_time_of_processing = 15  # минимальное время обслуживания одного клиента


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
        return prefix + '(a:' + str(round(self.time_arrive / 10, 2)) + \
               ', w:' + str(round(-n + self.time_arrive + self.max_wait_time, 2)) + ')'


class Queue:
    def __init__(self, prob_come):
        self.d = 0
        self.g = 0
        self.processing = 0
        self.queue = []  # список
        self.prob_come = prob_come

    def add2q(self, amount):
        for i in range(amount):
            self.queue.append(Client(n, randint(min_ready_wait_time, max_ready_wait_time)))

    def done(self):
        self.queue.pop(0)
        self.d += 1

    def gone(self, client_index):
        self.queue.pop(client_index)
        self.g += 1

    def __len__(self):
        return len(self.queue)

    def turn(self):
        if randint(0, 100) < prob_come:
            self.add2q(randint(min_people_came_to_queue, max_people_came_to_queue))
        for i in range(len(self) - 1, -1, -1):
            if self.queue[i].max_wait_time < (n - self.queue[i].time_arrive) and not self.queue[i].in_progress:
                self.gone(i)
        if self.processing > 0:
            self.processing -= 1
            if self.processing == 0:
                self.done()
        elif len(self) > 0:
            self.queue[0].in_progress = True
            self.processing = randint(min_time_of_processing, max_time_of_processing)


queue = Queue(prob_come)

while online:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            online = False
    queue.turn()
    surface.fill((0, 0, 0))
    pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(20, 20, len(queue) * 10, 20))
    pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(20, 60, queue.d, 20))
    pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(20, 100, queue.g, 20))
    pygame.display.flip()
    time.sleep(1/game_speed)
    n += 1
    if n % game_speed == 0:
        print(n // game_speed, end='  ')
        print(queue.g, end='  ')
        if len(queue) > 0:
            print(len(queue), end='  ')
            for i in range(len(queue)):
                print(queue.queue[i], end=',')
        print('')
pygame.quit()

# % - остаток от деления
# // - целая часть от деления
# / - деление
