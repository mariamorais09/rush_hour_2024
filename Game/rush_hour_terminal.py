
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import time
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
        return " "
    
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
        return blocks#print(f"Movimentos usados: ",i)


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



def reverseList(head): #reverses the order of a linked list by modifying the prev pointers of each node. After reversing the list, it returns the new head of the list.
    next = None
    while head:
        tmp = head.prev
        head.prev = next
        next = head
        head = tmp
    return next

board = Jogo(0,[],(),None,0)
##INTERFACE
contador_moves = 0
print("Welcome to the Rush Hour Game!!! What you would you like to do now?\n 0 - Learn Rules\n 1 - Play Game\n 2 - Watch the game being played by an algorithm")
o = int(input())
while (o==0):
    print("Sure! Here's how to play:\nCars are represented by letters and the empty spots where you can move such cars are represented by *.\nHorizontal cars can only move left (L) or right (R) and the vertical one's only up (U) or down (D).\nThe purpose of this game is to get the X car in the last two right spots of its line, so your job is to unblock the X path to its goal.\nYou have the chance to ask for a single hint during the game by typing H when asked what car you want to move.\n") #escrever regras
    print()
    print("Now press 1 to play the game or 2 to watch playing.")
    o = int(input())
if o==1:
    print("Let's play! Select a level of difficulty from 1 to 10, 1 being the easiest and 10 the hardest")
    l = int(input())
    match l:
        case 1:
            board.load_puzzle("l_1.txt")
            n_jogadas = 4
        case 2:
            board.load_puzzle("l_2.txt")
            n_jogadas = 7
        case 3:
            board.load_puzzle("l_3.txt")
            n_jogadas = 10
        case 4:
            board.load_puzzle("l_4.txt")
            n_jogadas = 14
        case 5:
            board.load_puzzle("l_5.txt")
            n_jogadas = 14
        case 6:
            board.load_puzzle("l_6.txt")
            n_jogadas = 16
        case 7:
            board.load_puzzle("l_7.txt")
            n_jogadas = 17
        case 8:
            board.load_puzzle("l_8.txt")
            n_jogadas = 37
        case 9:
            board.load_puzzle("l_9.txt")
            n_jogadas = 82
        case 10:
            board.load_puzzle("l_10.txt")
            n_jogadas = 81

    print("Here's your initial board! Good Luck!!\n \nDon't forget to use the hint (H) if you need to.")
    print()
    print(board.print_terminal())

    hint = False
    while (not board.acabou_jogo()):
        print("What vehicle do you want to move?\n")
        c = input()
        c = c.upper()
        print()

        if c == 'H':
            if not hint:
                hint_solution = board.BFS()  # Find the solution using BFS
                hint_solution = reverseList(hint_solution)  # Reverse the solution to get the initial move
                for _ in range(contador_moves):
                    hint_solution = hint_solution.prev
                next_move = hint_solution.prev  # The next move is the board state before the solution
                print("Here's your hint. Let's keep playing!")
                hint = True
                print()
                print(next_move.print_terminal())
                contador_moves += 1
                board = next_move
                continue
            else:
                print("You only get one hint! Sorry ...")
                continue


        print("In what direction? Left(L), Right(R), Up(U) or Down (D)")
        dir = input()
        dir = dir.upper()
        if dir == 'R':
            new = board.criar_novo_jogo(c,0,1)
        elif dir == 'L':
            new = board.criar_novo_jogo(c,0,-1)
        elif dir == 'U':
            new = board.criar_novo_jogo(c,-1,0)
        else:
            new = board.criar_novo_jogo(c,1,0)
        flag = False
        for prox in board.novos_carros():
            if prox.jogo_string() == new.jogo_string(): #Verificar se o movimento é válido se estiver em board.novos_carros(lista com todos os movimentos possíveis a partir do atual)
                new.print_terminal()
                board = new
                flag = True
                contador_moves += 1
                break
        if not flag:
            print("That move is illegal, try again.")
            print()

    if contador_moves > n_jogadas:
        print("GREAT JOB!!! You did it in", contador_moves, "moves but optimally you could have done it in", n_jogadas,".")
    else:
        print("GREAT JOB!!! You did it in", contador_moves, "moves!!")

elif o==2:
    print("Select a level of difficulty from 1 to 10, 1 being the easiest and 10 the hardest.")
    l = int(input())
    match l:
        case 1:
            board.load_puzzle("l_1.txt")
            n_jogadas = 4
        case 2:
            board.load_puzzle("l_2.txt")
            n_jogadas = 7
        case 3:
            board.load_puzzle("l_3.txt")
            n_jogadas = 10
        case 4:
            board.load_puzzle("l_4.txt")
            n_jogadas = 14
        case 5:
            board.load_puzzle("l_5.txt")
            n_jogadas = 14
        case 6:
            board.load_puzzle("l_6.txt")
            n_jogadas = 16
        case 7:
            board.load_puzzle("l_7.txt")
            n_jogadas = 17
        case 8:
            board.load_puzzle("l_8.txt")
            n_jogadas = 37
        case 9:
            board.load_puzzle("l_9.txt")
            n_jogadas = 82
        case 10:
            board.load_puzzle("l_10.txt")
            n_jogadas = 81
    print()
    print("Now select one of these algorithms to play this level:\n 1 - Breadth-First Search\n 2 - Depth-First Search\n 3 - A* with manhattan distance heuristic\n 4 - Greedy Search with manhattan distance heuristic\n 5 - A* with blocking vehicles heuristic\n 6 - Greedy Search with blocking vehicles heuristic")
    a = int(input())
    moves =0
    print()
    match a:
        case 1:
            a = time.time()
            sol = board.BFS()
            sol = reverseList(sol)
            b = time.time()
            while sol.prev:
                mat = sol.converter_em_matriz()
                print(sol.print_terminal())
                moves +=1
                print()
                sol = sol.prev
            print(sol.print_terminal())
            print("Time used: " , b-a)
            print("Number of moves: ", moves)
            
        case 2:
            a = time.time()
            sol = board.DFS()
            sol = reverseList(sol)
            b = time.time()
            while sol.prev:
                mat = sol.converter_em_matriz()
                print(sol.print_terminal())
                moves +=1
                print()
                sol = sol.prev
            print(sol.print_terminal())
            print("Time used: " , b-a)
            print("Number of moves: ", moves)
        case 3:
            a = time.time()
            sol = board.A_star_manhattan()
            sol = reverseList(sol)
            b = time.time()
            while sol.prev:
                mat = sol.converter_em_matriz()
                print(sol.print_terminal())
                moves += 1
                print()
                sol = sol.prev
            print(sol.print_terminal())
            print("Time used: " , b-a)
            print("Number of moves: ", moves)
        case 4:
            a = time.time()
            sol = board.Greedy_manhattan()
            sol = reverseList(sol)
            b = time.time()
            while sol.prev:
                mat = sol.converter_em_matriz()
                print(sol.print_terminal())
                moves += 1
                print()
                sol = sol.prev
            print(sol.print_terminal())
            print("Time used: " , b-a)
            print("Number of moves: ", moves)
        case 5:
            a = time.time()
            sol = board.A_star_blocking()
            sol = reverseList(sol)
            b = time.time()
            while sol.prev:
                mat = sol.converter_em_matriz()
                print(sol.print_terminal())
                moves +=1
                print()
                sol = sol.prev
            print(sol.print_terminal())
            print("Time used: " , b-a)
            print("Number of moves: ", moves)
        case 6:
            a = time.time()
            sol = board.Greedy_blocking()
            sol = reverseList(sol)
            b = time.time()
            while sol.prev:
                mat = sol.converter_em_matriz()
                print(sol.print_terminal())
                moves += 1
                print()
                sol = sol.prev
            print(sol.print_terminal())
            print("Time used: " , b-a)
            print("Number of moves: ", moves)
