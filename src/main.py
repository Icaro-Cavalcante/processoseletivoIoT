from machine import Pin
import time

# Mapeamento dos pinos (conforme diagrama)
PIN_VERMELHO = 32
PIN_AMARELO = 33
PIN_VERDE = 25
PIN_PEDESTRE = 26
PIN_BOTAO = 27

# Configuração dos LEDs como saída
led_vermelho = Pin(PIN_VERMELHO, Pin.OUT)
led_amarelo = Pin(PIN_AMARELO, Pin.OUT)
led_verde = Pin(PIN_VERDE, Pin.OUT)
led_pedestre = Pin(PIN_PEDESTRE, Pin.OUT)

# Botão de pedestre com pull-up interno (pressionado = 0)
botao = Pin(PIN_BOTAO, Pin.IN, Pin.PULL_UP)

# Variáveis de controle
pedido_pedestre = False
estado = "VERDE"
tempo_estado = 0

# Tempos em segundos
TEMPO_VERDE = 10
TEMPO_AMARELO = 3
TEMPO_VERMELHO = 3
TEMPO_PEDESTRE = 6
TEMPO_PISCA_VERMELHO = 2

def setup():
    global tempo_estado
    led_verde.value(1)
    led_amarelo.value(0)
    led_vermelho.value(0)
    led_pedestre.value(0)
    tempo_estado = time.ticks_ms()
    print("🚦 Semáforo iniciado. Modo NORMAL.")
    print("Verde para carros por", TEMPO_VERDE, "segundos.")

def verificar_botao():
    global pedido_pedestre
    if botao.value() == 0:  # pressionado
        time.sleep_ms(50)   # debounce
        if botao.value() == 0 and not pedido_pedestre:
            pedido_pedestre = True
            print("🚶 Pedestre solicitou travessia!")

def piscar_led_vermelho(tempo_total):
    """Pisca o LED vermelho dos carros rapidamente antes de liberar pedestre."""
    fim = time.ticks_ms() + tempo_total * 1000
    while time.ticks_ms() < fim:
        led_vermelho.value(1)
        time.sleep_ms(200)
        led_vermelho.value(0)
        time.sleep_ms(200)
    led_vermelho.value(0)

def loop_principal():
    global estado, pedido_pedestre, tempo_estado
    agora = time.ticks_ms()
    decorrido = time.ticks_diff(agora, tempo_estado)

    if estado == "VERDE":
        if decorrido >= TEMPO_VERDE * 1000:
            # Se houver pedido de pedestre, vai para amarelo e depois vermelho especial
            led_verde.value(0)
            led_amarelo.value(1)
            estado = "AMARELO"
            tempo_estado = time.ticks_ms()
            print("🟡 Amarelo - atenção")
        else:
            # Durante o verde, verifica botão
            verificar_botao()

    elif estado == "AMARELO":
        if decorrido >= TEMPO_AMARELO * 1000:
            led_amarelo.value(0)
            led_vermelho.value(1)
            estado = "VERMELHO"
            tempo_estado = time.ticks_ms()
            print("🔴 Vermelho - pare")

    elif estado == "VERMELHO":
        # Se tiver pedido de pedestre, faz a travessia
        if pedido_pedestre:
            # Aguarda um pouco no vermelho (opcional) e libera pedestre
            if decorrido >= 1000:  # pelo menos 1 segundo de vermelho
                print("✅ Sinal verde para pedestres!")
                led_pedestre.value(1)
                time.sleep(TEMPO_PEDESTRE)
                led_pedestre.value(0)
                print("⚠️ Sinal vermelho para pedestres - termine a travessia")
                # Pisca o LED vermelho dos carros por 2 segundos
                piscar_led_vermelho(TEMPO_PISCA_VERMELHO)
                # Reseta pedido e volta para verde
                pedido_pedestre = False
                led_vermelho.value(0)
                led_verde.value(1)
                estado = "VERDE"
                tempo_estado = time.ticks_ms()
                print("🟢 Verde liberado para carros novamente")
        else:
            # Se não houver pedestre, após TEMPO_VERMELHO volta ao verde
            if decorrido >= TEMPO_VERMELHO * 1000:
                led_vermelho.value(0)
                led_verde.value(1)
                estado = "VERDE"
                tempo_estado = time.ticks_ms()
                print("🟢 Verde para carros")

# Inicialização
setup()

# Loop principal
while True:
    loop_principal()
    time.sleep_ms(50)  # pequena pausa para evitar sobrecarga
    