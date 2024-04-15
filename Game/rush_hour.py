from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time
import numpy as np
import sys
import heapq


Cars = ('X','A','B','C','D','E','F','G','I','J','K','L') # lenght = 2

Trucks = ('O','P','Q','R','S','T') # lenght = 3


class Vehicle(): # j = x // i = y
    def __init__(self,Let,i,j,horiz):
        self.l = Let #letra que representa o carro
        self.i = i
        self.j = j
        self.horiz = horiz #true se horizontal, false se vertical

class Jogo():
    def __init__(self,N,Vehicles,Goal,Prev,Cost):
        self.N = N #tamanho do tabuleiro
        self.v = Vehicles # 'X', veiculo final esta sempre em v[0]
        self.g = Goal 
        self.cost = Cost
        self.prev = Prev #tabuleiro anterior

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def load_puzzle(self,filename): #ler de ficheiro de texto o tabuleiro inicial
        fin = open(filename)
        lines = fin.readlines()
        fin.close()
        self.N = int(lines[0])
        self.g = [int(k) for k in lines[1].split()]
        for line in (lines[2::]):
            fields = line.rstrip().split()
            horiz = True
            if "v" in fields[3]:
                horiz = False
            self.v.append(Vehicle(str(fields[0]), int(fields[1]), int(fields[2]), horiz))

    def converter_em_matriz(self):
        mat = [[' ']*self.N for i in range(self.N)]
        for vehicle in self.v:
            di = 0
            dj = 0
            i = vehicle.i
            j = vehicle.j
            if vehicle.horiz == True:
                dj = 1
            else:
                di = 1
            if vehicle.l in Trucks:
                for k in range(3):
                    mat[i][j] = vehicle.l
                    i+=di
                    j+=dj
            else:
                for k in range(2):
                    mat[i][j] = vehicle.l
                    i+=di
                    j+=dj
        return mat

    def print_terminal(self): #ver o jogo no terminal
        s = ""
        mat = self.converter_em_matriz()
        for i in range(self.N):
            for j in range(self.N):
                if mat[i][j] == ' ':
                    s+="* "
                else:
                    s += "{} ".format(mat[i][j])
            s += "\n"
        print(s)
    
    def acabou_jogo(self):
        mat = self.converter_em_matriz()
        if mat[self.g[0]][self.g[1]] == 'X': #self.g guarda a posição objetivo do 'X'
            return 1
        return 0

    def criar_novo_jogo(self,letra,di,dj): 
        novo = Jogo(0,[],(),None,0)
        novo.N = self.N
        for car in self.v:
            if car.l == letra:
                novo.v.append(Vehicle(letra,car.i+di,car.j+dj,car.horiz))
            else:
                novo.v.append(Vehicle(car.l,car.i,car.j,car.horiz))
        novo.g = self.g
        novo.cost = self.cost + 1
        novo.prev = self
        return novo
    
    def jogo_string(self): #passar para str
        s = ""
        mat = self.converter_em_matriz()
        for i in range(self.N):
            for j in range(self.N):
                s += "{}".format(mat[i][j])
        return s

    def novos_carros(self): #lista com todos os tabuleiros possíveis a partir do atual
        mat = self.converter_em_matriz()
        lista = []
        for veiculo in self.v:
            i = veiculo.i
            j = veiculo.j
            l = 2
            if veiculo.l in Trucks:
                l = 3
            if veiculo.horiz == True: #horizontal
                if j-1 >= 0 and j-1 < self.N and mat[i][j-1] == ' ':
                    lista.append(self.criar_novo_jogo(veiculo.l,0,-1)) #mover para a esquerda
                if j+l >= 0 and j+l < self.N and mat[i][j+l] == ' ':
                    lista.append(self.criar_novo_jogo(veiculo.l,0,1)) #mover para a direita
            if veiculo.horiz == False: #vertical
                if i-1 >= 0 and i-1 < self.N and mat[i-1][j] == ' ':
                    lista.append(self.criar_novo_jogo(veiculo.l,-1,0)) #mover para cima
                if i+l >= 0 and i+l < self.N and mat[i+l][j] == ' ':
                    lista.append(self.criar_novo_jogo(veiculo.l,1,0)) #mover para baixo
        return lista
    

    #heurísticas
    def Manhattan_distance_heuristic(self): #distância entre a posição do carro 'X' e o objetivo
        return self.g[1] - self.v[0].j
    
    def Blocking_vehicles_heuristic(self): #veículos que estao a bloquear o carro vermelho
        grid = self.converter_em_matriz()
        blocks = 0
        for j in range(self.v[0].j+1,self.g[1]):
            if grid[self.g[0]][j] != " ":
                blocks += 1
        return blocks


    #Algoritmos de pesquisa
    def BFS(self):
        visited = set(self.jogo_string())
        queue = [self]

        while queue:
            cur = queue.pop(0)
            if cur.acabou_jogo():
                return cur
            for neighbour in cur.novos_carros():
                if neighbour.jogo_string() not in visited:
                    visited.add(neighbour.jogo_string())
                    queue.append(neighbour)

    def DFS(self):
        visited = set(self.jogo_string())
        queue = [self]

        while queue:
            cur = queue.pop(0)
            if cur.acabou_jogo():
                return cur
            for neighbour in cur.novos_carros():
                if neighbour.jogo_string() not in visited:
                    visited.add(neighbour.jogo_string())
                    queue.insert(1, neighbour)


    def A_star_manhattan(self):
        visited = set()  # Set to keep track of visited states
        queue = []  # Priority queue to store states
        heapq.heappush(queue, (0, 0, self))  # Push initial state with priority 0

        while queue:
            _, cost, current_state = heapq.heappop(queue)  # Get state with the lowest priority
            if current_state.acabou_jogo():  # Check if goal state is reached
                return current_state

            if current_state.jogo_string() not in visited:  # Check if state has been visited
                visited.add(current_state.jogo_string())  # Mark state as visited
                for neighbor in current_state.novos_carros():  # Iterate over neighbor states
                    new_cost = cost + 1  # Calculate new cost
                    priority = new_cost + neighbor.Manhattan_distance_heuristic()*5000  # Calculate priority
                    heapq.heappush(queue, (priority, new_cost, neighbor))  # Push neighbor state to queue

    def Greedy_manhattan(self): 
        visited = set()  # Set to keep track of visited states
        queue = [(0, self)]  # Priority queue to store states

        while queue:
            _, current_state = queue.pop(0)  # Get state with the lowest heuristic value
            if current_state.acabou_jogo():  # Check if goal state is reached
                return current_state

            if current_state.jogo_string() not in visited:  # Check if state has been visited
                visited.add(current_state.jogo_string())  # Mark state as visited
                for neighbour in current_state.novos_carros():  # Iterate over neighbor states
                    if neighbour.jogo_string() not in visited:
                        queue.append((neighbour.Manhattan_distance_heuristic(), neighbour))

                queue.sort(key=lambda x: x[0])  # Sort the queue based on heuristic values



    def A_star_blocking(self):
        visited = set()  # Set to keep track of visited states
        queue = [(0, self)]  # Priority queue to store states

        while queue:
            _, current_state = queue.pop(0)  # Get state with the lowest priority
            if current_state.acabou_jogo():  # Check if goal state is reached
                return current_state

            if current_state.jogo_string() not in visited:  # Check if state has been visited
                visited.add(current_state.jogo_string())  # Mark state as visited
                for neighbour in current_state.novos_carros():  # Iterate over neighbor states
                    neighbour.cost += 1  # Update the cost of the neighbor
                    if neighbour.jogo_string() not in visited:
                        queue.append((neighbour.cost + self.Blocking_vehicles_heuristic(), neighbour))

                queue.sort(key=lambda x: x[0])  # Sort the queue based on priority

    def Greedy_blocking(self):
        visited = set()  # Set to keep track of visited states
        queue = [(0, self)]  # Priority queue to store states

        while queue:
            _, current_state = queue.pop(0)  # Get state with the lowest heuristic value
            if current_state.acabou_jogo():  # Check if goal state is reached
                return current_state

            if current_state.jogo_string() not in visited:  # Check if state has been visited
                visited.add(current_state.jogo_string())  # Mark state as visited
                for neighbour in current_state.novos_carros():  # Iterate over neighbor states
                    if neighbour.jogo_string() not in visited:
                        queue.append((self.Blocking_vehicles_heuristic(), neighbour))

                queue.sort(key=lambda x: x[0])  # Sort the queue based on heuristic value



def reverseList(head):
    next = None
    i = 1
    while head:
        tmp = head.prev
        head.prev = next
        next = head
        head = tmp
        i += 1
    return next


s1 = Jogo(0,[],(),None,0)  # Initialize the Jogo object

def easy_load():
    global selected_mode
    selected_mode = "easy"
    s1.load_puzzle("l_3.txt")
    final1 = s1.BFS()
    return main(final1)

def medium_load():
    global selected_mode
    selected_mode = "medium"
    s1.load_puzzle("l_6.txt")
    final2 = s1.BFS()
    return main(final2)

def hard_load():
    global selected_mode
    selected_mode = "hard"
    s1.load_puzzle("l_10.txt")
    final3 = s1.BFS()
    return main(final3)

BLACK = (0,0,0)
WHITE = (237,230,242)
RED = (223,41,53)
BLUE = (58,70,226)
GREEN = (127,182,50)
PINK = (245,100,169)
BLUE2 = (174,184,254)
PINK2 = (255,153,255)
YELLOW = (245,200,0)
ORANGE = (245,138,7)
BROWN = (76,35,10)
PURPLE = (129,41,134)
GREY = (100,100,100)
GREY1 = (200,200,200)
GREY2 = (150,150,75)
TEAL = (0, 128, 128)
CYAN = (0, 255, 255)
LIME_GREEN = (50, 205, 50)
TURQUOISE = (64, 224, 208)
GOLD = (255, 215, 0)
MAGENTA = (255, 0, 255)
SALMON = (250, 128, 114)

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 720

def main(final):
    global SCREEN, CLOCK
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    running = True
    resul = reverseList(final)
    while running:
        MAT = resul.converter_em_matriz()
        drawGrid(MAT)
        time.sleep(0.25)
        if resul.prev:
            MAT = resul.converter_em_matriz()
            resul = resul.prev
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False       
        pygame.display.update()

# Map characters to integers
vehicle_to_color_index = {
    ' ': -1, 'X': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4,
    'E': 5, 'F': 6, 'G': 7, 'I': 8, 'J': 9, 'K': 10,
    'K': 11, 'L': 12, 'O': 13, 'P': 14, 'Q': 15, 'R': 16,
    'S': 17, 'T': 18
}

# Adjust colorConvert to handle more cases
def colorConvert(i):
    match i:
        case -1:
            return WHITE
        case 0:
            return RED
        case 1:
            return BLUE
        case 2:
            return YELLOW
        case 3:
            return GREEN
        case 4:
            return MAGENTA
        case 5:
            return PINK
        case 6:
            return GOLD
        case 7:
            return ORANGE
        case 8:
            return BROWN
        case 9:
            return BLUE2
        case 10:
            return GREY
        case 11:
            return GREY1
        case 12:
            return GREY2
        case 13:
            return PURPLE
        case 14:
            return LIME_GREEN
        case 15:
            return TURQUOISE
        case 16:
            return PINK2
        case 17:
            return TEAL
        case 18:
            return SALMON

def drawGrid(MAT):
    blockSize = 120
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            vehicle = MAT[y//blockSize][x//blockSize]
            color_index = vehicle_to_color_index.get(vehicle, -1)  # Use default -1 for unknown vehicles
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, colorConvert(color_index), rect, 200)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
