from machine import Pin
import time

# Mapeamento dos pinos
PIN_VERMELHO = 32
PIN_AMARELO = 33
PIN_VERDE = 25
PIN_PEDESTRE = 26
PIN_BOTAO = 27

# Configuração dos componentes
led_vermelho = Pin(PIN_VERMELHO, Pin.OUT)
led_amarelo = Pin(PIN_AMARELO, Pin.OUT)
led_verde = Pin(PIN_VERDE, Pin.OUT)
led_pedestre = Pin(PIN_PEDESTRE, Pin.OUT)
botao = Pin(PIN_BOTAO, Pin.IN, Pin.PULL_UP)

# Tempos (segundos)
TEMPO_VERDE = 10
TEMPO_AMARELO = 3
TEMPO_VERMELHO_ESPERA = 1  # Tempo parado no vermelho antes de abrir pedestre
TEMPO_PEDESTRE = 6
TEMPO_PISCA_FINAL = 2

# Controle de Estado
# Estados: VERDE, AMARELO, VERMELHO, TRAVESSIA, PISCANDO
estado = "VERDE"
tempo_estado = time.ticks_ms()
pedido_pedestre = False
ultimo_pisca = 0

def setup():
    led_verde.value(1)
    led_amarelo.value(0)
    led_vermelho.value(0)
    led_pedestre.value(0)
    print("🚦 Semáforo iniciado.")

def verificar_botao():
    global pedido_pedestre
    # Se o botão for pressionado (0) e ainda não houver pedido registrado
    if botao.value() == 0 and not pedido_pedestre:
        # Pequeno debounce não bloqueante (opcional, mas aqui simplificado)
        pedido_pedestre = True
        print("🚶 Pedestre solicitou travessia!")

def trocar_estado(novo_estado):
    global estado, tempo_estado
    estado = novo_estado
    tempo_estado = time.ticks_ms()
    print(f"Mudando para: {novo_estado}")

def loop_principal():
    global pedido_pedestre, ultimo_pisca

    agora = time.ticks_ms()
    decorrido = time.ticks_diff(agora, tempo_estado)

    # 1. Leitura constante do botão (Independente do estado)
    verificar_botao()

    # 2. Máquina de Estados
    if estado == "VERDE":
        led_verde.value(1)
        led_amarelo.value(0)
        led_vermelho.value(0)
        led_pedestre.value(0)
        if decorrido >= TEMPO_VERDE * 1000:
            trocar_estado("AMARELO")

    elif estado == "AMARELO":
        led_verde.value(0)
        led_amarelo.value(1)
        if decorrido >= TEMPO_AMARELO * 1000:
            trocar_estado("VERMELHO")

    elif estado == "VERMELHO":
        led_amarelo.value(0)
        led_vermelho.value(1)
        # Se houver pedido, espera 1s e vai para travessia. Se não, volta pro verde.
        if pedido_pedestre:
            if decorrido >= TEMPO_VERMELHO_ESPERA * 1000:
                trocar_estado("TRAVESSIA")
        elif decorrido >= (TEMPO_AMARELO * 1000): # Tempo padrão se ninguém apertar
            trocar_estado("VERDE")

    elif estado == "TRAVESSIA":
        led_pedestre.value(1)
        if decorrido >= TEMPO_PEDESTRE * 1000:
            led_pedestre.value(0)
            trocar_estado("PISCANDO")

    elif estado == "PISCANDO":
        # Lógica de piscar o vermelho sem travar o código
        if time.ticks_diff(agora, ultimo_pisca) >= 250: # Pisca a cada 250ms
            led_vermelho.value(not led_vermelho.value())
            ultimo_pisca = agora
        
        if decorrido >= TEMPO_PISCA_FINAL * 1000:
            pedido_pedestre = False
            trocar_estado("VERDE")

setup()

print("Teste")

while True:
    loop_principal()
    # Sleep mínimo apenas para estabilidade do simulador (não afeta a lógica)
    time.sleep_ms(50)