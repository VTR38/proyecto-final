import pygame
import sys
import heapq
from collections import defaultdict

# Inicializa pygame
pygame.init()

# Configuración de la ventana
screen_width = 1500
screen_height = 1020
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulación de Sistema de Taxis")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PASTEL_GREEN = (108, 178, 95)
PASTEL_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Taxi color
CYAN = (0, 255, 255)  # Passenger location color
MAGENTA = (255, 0, 255)  # Passenger destination color

# Variables de control
running = True

# Rectángulo del botón de reset
reset_button_rect = pygame.Rect(screen_width - 120, 20, 100, 50)
start_button_rect = pygame.Rect(screen_width - 120, 80, 100, 50)

# Fuentes
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        """Agrega una arista bidireccional con su peso."""
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

    def dijkstra(self, start, goal):
        """Implementación del algoritmo de Dijkstra para encontrar el camino más corto."""
        queue, seen = [(0, start, ())], set()
        while queue:
            (cost, v1, path) = heapq.heappop(queue)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                if v1 == goal:
                    return (cost, self._flatten(path))

                for v2 in self.edges[v1]:
                    if v2 not in seen:
                        heapq.heappush(queue, (cost + self.weights[(v1, v2)], v2, path))
        return float("inf"), []

    def _flatten(self, path):
        """Aplana el camino devuelto por Dijkstra."""
        result = []
        while path:
            result.append(path[0])
            path = path[1]
        result.reverse()
        return result

class Taxi:
    def __init__(self, location):
        """Inicializa un taxi en una ubicación específica."""
        self.location = location
        self.destination = None
        self.path = []
        self.traveling = False
        self.total_cost = 0
        self.current_cost = 0
        self.traveled_paths = []
        self.passenger = None
        self.step_counter = 0
        self.steps_per_move = 10  # Cambia este valor para ajustar la velocidad del taxi

    def move(self):
        """Mueve el taxi a lo largo del camino hacia su destino."""
        if self.path:
            self.step_counter += 1
            if self.step_counter >= self.steps_per_move:
                self.step_counter = 0
                next_location = self.path.pop(0)
                self.traveled_paths.append((self.location, next_location))
                self.current_cost += city_graph.weights[(self.location, next_location)]
                self.location = next_location
                if not self.path:
                    if self.location == self.passenger.location:
                        cost, path = city_graph.dijkstra(self.location, self.passenger.destination)
                        if path:
                            self.path = path[1:]  # Omitir el nodo inicial
                    else:
                        self.traveling = False
                        self.destination = None
                        self.total_cost += self.current_cost
                        self.current_cost = 0
                        self.passenger = None

class Passenger:
    def __init__(self, location, destination):
        """Inicializa un pasajero con una ubicación y destino."""
        self.location = location
        self.destination = destination

# Crear el grafo de la ciudad
city_graph = Graph()

# Definir nodos y aristas (calles)
nodes = [
    (70, 70), (230, 70), (430, 70), (510, 70), (590, 70), (670, 70), (750, 70), (980,70), #1 fila
    (70, 130), (150, 130),(230, 130), (310,130), (390,130), (430, 130), (750, 130), (790, 130), (890, 130), (1020, 130),#2 fila
    (390, 230), (430, 230),(510, 230), (590, 230), (670, 230), (750, 230), (790,230), #3 fila
    (70, 330), (150,330),(230, 330), (310,330), (390, 330), (470, 330), (590, 330), (670, 330), (750, 330), (790,330), (890, 330), (980,330),(1100,330), #4 fila
    (470, 390), (510, 390), (590, 390), (670, 390), #5 fila
    (70,490), (1090,430),#6 fila
    (150,550), (230,550), (310,550), (390,550),(470,550), (510,550), (670,550), (750,550), (860,550), (980,550), (1090,550), (1200,550),#7 fila
    (230,630), #8 fila
    (270,680), (510,680), (590,680), (670,680), (1000,680), (1200,680), #9 fila
    (350,780), (670,780), (890,780), #10 fila
    (400,880), (670,880), (770,880), #11 fila
    (500,980), (670,980)
]

# Definir las aristas entre nodos con sus pesos
edges = [
    (0,1,56), (0,8,28), # Nodo 0
    (1,2,68),  (1, 10,25), # Nodo 1
    (2,3,28),(2,13,28),# Nodo 2
    (3,4,25),(3,20,58),# Nodo 3
    (4,5,30), (4,21,59), # Nodo 4
    (5,6,28), (5,22,59), # Nodo 5
    (6,7,56), (6,14,26), # Nodo 6
    (7,17,27), # Nodo 7

    (8,9,58), (8,25,56), # Nodo 8
    (9,10,27), (9,26,57), # Nodo 9
    (10, 11, 28), (10, 27, 58),  # Nodo 10
    (11, 12, 24), (11, 28, 54) , # Nodo 11
    (12, 13, 12), (12, 18, 27),  # Nodo 12
    (13, 19, 30),  # Nodo 13
    (14,15,11), (14,23,30), # Nodo 14
    (15,16,25), (15,24,32), # Nodo 15
    (16,17,27), (16,35,53), # Nodo 16

    (17,37,24), # Nodo 17
    (18,19,12), (18,29,26),# Nodo 18
    (19,20,27), # Nodo 19
    (20, 21,28),  # Nodo 20
    (21,22,27), (21,31,25), # Nodo 21
    (22,23,29), # Nodo 22
    (23,24,13),# Nodo 23
    (24,34,23), # Nodo 24

    (25,26,28),(25,42,51), # Nodo 25
    (26,27,27), (26,44,65), # Nodo 26
    (27, 28, 28), (27, 45, 75),  # Nodo 27
    (28, 29, 26), (28, 46, 73),  # Nodo 28
    (29, 30, 25), (29, 47, 76),  # Nodo 29
    (30, 31, 42), (30,38,30), # Nodo 30
    (31, 32, 27), # Nodo 31
    (32,33,27), (32,41,27), # Nodo 32
    (33,34,14), (33,51,73), # Nodo 33
    (34,35,14), # Nodo 34
    (35,36,13), # Nodo 35
    (36,37,27), (36,53,74), # Nodo 36
    (37,55,71), # Nodo 37

    (38,39,23), (38,48,43), # Nodo 38
    (39,40,28), (39,49,42), # Nodo 39
    (40,41,25), (40,59,71), # Nodo 40
    (41,50,46), # Nodo 41

    (42,44,25), # Nodo 42
    (43,54,31), # Nodo 43
    (44,56,37), # Nodo 44
    (45,46,10), (45,56,22), # Nodo 45
    (46,47,26), # Nodo 46
    (47,48,27), # Nodo 47
    (48,49,20), # Nodo 48
    (49,58,29), # Nodo 49
    (50,51,32), (50,60,24), # Nodo 50
    (51,52,28), # Nodo 51
    (52,53,23), # Nodo 52
    (53,54,29), # Nodo 53
    (54,55,24), # Nodo 54
    (55,62,20), # Nodo 55
    (56,57,20), # Nodo 56
    (57,58,80), (57,63,34),# Nodo 57
    (58,59,25), # Nodo 58
    (59,60,30), # Nodo 59
    (60,61,82), (60,64,29),# Nodo 60
    (61,62,50), (61,65,34), # Nodo 61

    (63,64,112), (63,66,40), # Nodo 63
    (64,65,61), (64,67,24), # Nodo 64
    (65,68,37), # Nodo 65
    (66,69,27), (66,67,87), # Nodo 66
    (67,68,33), (67,70,30), # Nodo 67
    (68,70,44), # Nodo 68
    (69,70,68), # Nodo 69
]

# Agregar las aristas al grafo
for edge in edges:
    city_graph.add_edge(*edge)

def draw_graph():
    """Dibuja los nodos y aristas del grafo en la pantalla."""
    for (x, y) in nodes:
        pygame.draw.circle(screen, WHITE, (x, y), 10)
    for from_node, to_node, weight in edges:
        pygame.draw.line(screen, WHITE, nodes[from_node], nodes[to_node], 2)
        mid_point = ((nodes[from_node][0] + nodes[to_node][0]) // 2, (nodes[from_node][1] + nodes[to_node][1]) // 2)
        text = small_font.render(str(weight), True, WHITE)
        screen.blit(text, mid_point)

taxi_image = pygame.image.load("C:/Users/vreyes/Downloads/taxi.png")
taxi_image = pygame.transform.scale(taxi_image, (50, 50))
passenger_image = pygame.image.load("C:/Users/vreyes/Downloads/pasajero.png")
passenger_image = pygame.transform.scale(passenger_image, (30, 30))
destination_image = pygame.image.load("C:/Users/vreyes/Downloads/destino.png")
destination_image = pygame.transform.scale(destination_image, (30, 30))

def draw_taxis(taxis):
    """Dibuja todos los taxis en sus ubicaciones actuales."""
    for taxi in taxis:
        screen.blit(taxi_image, (nodes[taxi.location][0] - taxi_image.get_width() // 2, nodes[taxi.location][1] - taxi_image.get_height() // 2))
        if not taxi.traveling and taxi.total_cost > 0:
            text = small_font.render(f"Cost: {taxi.total_cost}", True, WHITE)
            screen.blit(text, (10, 10 + 20 * taxis.index(taxi)))

def draw_passengers(passengers):
    """Dibuja todos los pasajeros y sus destinos en la pantalla."""
    for passenger in passengers:
        screen.blit(passenger_image, (nodes[passenger.location][0] - passenger_image.get_width() // 2, nodes[passenger.location][1] - passenger_image.get_height() // 2))
        screen.blit(destination_image, (nodes[passenger.destination][0] - destination_image.get_width() // 2, nodes[passenger.destination][1] - destination_image.get_height() // 2))

def draw_reset_button():
    """Dibuja el botón de reset en la pantalla."""
    pygame.draw.rect(screen, PASTEL_BLUE, reset_button_rect)
    text = font.render("Reset", True, BLACK)
    screen.blit(text, (reset_button_rect.x + 10, reset_button_rect.y + 10))

def draw_start_button():
    """Dibuja el botón de inicio en la pantalla."""
    pygame.draw.rect(screen, PASTEL_BLUE, start_button_rect)
    text = font.render("Start", True, BLACK)
    screen.blit(text, (start_button_rect.x + 10, start_button_rect.y + 10))

def draw_taxi_path(taxi):
    """Dibuja el camino que sigue un taxi hacia su destino."""
    if taxi.path:
        path_points = [nodes[taxi.location]] + [nodes[point] for point in taxi.path]
        pygame.draw.lines(screen, BLACK, False, path_points, 2)

def draw_taxi_traveled_paths(taxi):
    """Dibuja las rutas recorridas por un taxi en la pantalla."""
    for from_node, to_node in taxi.traveled_paths:
        pygame.draw.line(screen, BLACK, nodes[from_node], nodes[to_node], 2)

# Inicialización de taxis y pasajeros
taxis = [Taxi(0)]
passengers = []
selected_location = None
selecting_passenger = False
start_simulation = False

while running:
    screen.fill(PASTEL_GREEN)
    draw_graph()
    draw_taxis(taxis)
    draw_passengers(passengers)
    draw_reset_button()
    draw_start_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if reset_button_rect.collidepoint(mouse_pos):
                # Resetea las selecciones y el estado del viaje
                taxis = [Taxi(0)]
                passengers = []
                selected_location = None
                selecting_passenger = False
                start_simulation = False
            elif start_button_rect.collidepoint(mouse_pos):
                start_simulation = True
            else:
                for i, (x, y) in enumerate(nodes):
                    if (mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2 < 100:
                        if not selecting_passenger:
                            selected_location = i
                            selecting_passenger = True
                        else:
                            passengers.append(Passenger(selected_location, i))
                            selected_location = None
                            selecting_passenger = False

    if start_simulation:
        for taxi in taxis:
            if not taxi.traveling and passengers:
                passenger = passengers.pop(0)
                cost, path = city_graph.dijkstra(taxi.location, passenger.location)
                if path:
                    taxi.path = path[1:]  # Omitir el nodo inicial
                    taxi.traveling = True
                    taxi.destination = passenger.destination
                    taxi.passenger = passenger
                    taxi.total_cost = 0

    for taxi in taxis:
        if taxi.traveling:
            draw_taxi_path(taxi)
            taxi.move()

        draw_taxi_traveled_paths(taxi)

    pygame.display.flip()
    pygame.time.Clock().tick(40)

pygame.quit()
sys.exit()
