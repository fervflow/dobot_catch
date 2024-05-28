import pydobot
from serial.tools import list_ports

# Dobot limits
INNER_RADIUS, OUTER_RADIUS = 100, 290
X_LIMIT = (-50, OUTER_RADIUS)
Y_LIMIT = (-OUTER_RADIUS, OUTER_RADIUS)
Z_LIMIT = (-30, 130)

def is_reachable(x, y, z):
    return (
        X_LIMIT[0] <= x <= X_LIMIT[1] and 
        Y_LIMIT[0] <= y <= Y_LIMIT[1] and
        Z_LIMIT[0] <= z <= Z_LIMIT[1] and
        INNER_RADIUS**2 <= (x**2 + y**2) <= OUTER_RADIUS**2
    )

# Dobot initialization
available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

dobot = pydobot.Dobot(port=port, verbose=False)

(x, y, z, r, j1, j2, j3, j4) = dobot.pose()
print('START POSITION')
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

# Agarrar objecto desde Origen a Destino
def agarrar_objeto(origin, destiny):
    if not is_reachable(origin[0], origin[1], Z_LIMIT[1]):
        print('ORIGIN CORDS UNREACHABLE')
    elif not is_reachable(destiny[0], destiny[1], Z_LIMIT[0]):
        print('DESTINY CORDS UNREACHABLE')
    else: # False=abierto; True=cerrado
        # Abrir garra y llevar al origen (cubo)
        dobot.grip(False)
        dobot.move_to(origin[0], origin[1], 120, r, wait=True)
        dobot.move_to(origin[0], origin[1], -30, r, wait=True)
        
        # Cerrar garra y elevar brazo
        dobot.grip(True)
        dobot.wait(500)
        dobot.move_to(origin[0], origin[1], 120, r, wait=True)

        # Llevar al destino, abrir garra y elevar brazo
        dobot.move_to(destiny[0], destiny[1], 120, r, wait=True)
        dobot.move_to(destiny[0], destiny[1], -30, r, wait=True)
        dobot.grip(False)
        dobot.wait(500)
        dobot.move_to(destiny[0], destiny[1], 120, r, wait=True)


# Coordenadas
coords = [
    (220, 100), # Origen (x, y) // cubo
    (240, -250) # Destino (x, y) // caja
]

# MAIN
agarrar_objeto(coords[0], coords[1])
    
dobot.close()
