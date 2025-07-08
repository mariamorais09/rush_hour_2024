**Rush Hour Game**
Rush Hour é um jogo de lógica cujo objetivo é mover o carro vermelho até à saída, localizada nas duas últimas posições da linha onde este se encontra. Para isso, será necessário deslocar os outros veículos no tabuleiro, de forma a desimpedir o caminho.

*Regras do Jogo*
- O tabuleiro é uma grelha quadrada (atualmente foram definidos apenas níveis para grelhas 6x6).
- Os veículos podem ocupar 2 ou 3 casas e estar orientados na vertical ou na horizontal.
- Veículos verticais apenas se podem mover para cima e para baixo.
- Veículos horizontais apenas se podem mover para a esquerda e para a direita.
- Nenhum veículo pode ultrapassar os limites do tabuleiro ou atravessar outros veículos.

*Funcionalidades*
- Interface textual e interface gráfica.
- Seleção de níveis com diferentes configurações e dificuldades.
- Possibilidade de ver o jogo a ser resolvido automaticamente por algoritmos de pesquisa.
- Modo de jogo manual, com a opção de pedir uma pista (hint).

*Algoritmos de Pesquisa Implementados*

Foram utilizados algoritmos de pesquisa para resolver os diferentes níveis:

Pesquisa não informada:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)

Pesquisa informada:
- A*
- Greedy Search

As pesquisas informadas utilizam duas heurísticas distintas:
- Distância de Manhattan entre o carro vermelho e a saída.
- Número de veículos que bloqueiam diretamente o caminho do carro vermelho.

*Requisitos*
- Python 3
- Bibliotecas: pygame, sys

*Como usar a interface textual*
- Aceder ao terminal, no diretório Game.
- Executar o comando: python3 rush_hour_terminal.py
  
Opções disponíveis:
- Aprender as regras do jogo.
- Jogar manualmente qualquer um dos 10 níveis disponíveis.
- Ver um algoritmo de pesquisa resolver um nível.
- Durante o jogo manual, pode pedir uma única pista premindo a tecla H.

Controlo do jogo:
- Selecione a letra correspondente ao veículo que pretende mover.
- Em seguida, escolha a direção do movimento.
- Os espaços vazios são representados por *.
- O carro vermelho é representado pela letra X.


*Como usar a interface gráfica*
- Instale a biblioteca pygame (se ainda não estiver instalada).
- No diretório Game, execute: python3 rush_hour_graphical_interface.py

No menu principal:
- Selecione "Rules" para rever as regras do jogo.
- Selecione "Play" para escolher o nível de dificuldade: Easy (nível 3), Medium (nível 6), Hard (nível 10)
- O jogo será resolvido automaticamente utilizando o algoritmo Breadth-First Search.
