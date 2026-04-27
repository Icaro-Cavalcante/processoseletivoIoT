# 🎛️ Projeto de IoT - Processo Seletivo PNAAT

**Nome:** Icaro Cavalcante de Carvalho Pinheiro  
**E-mail:** icarodev06@gmail.com  
**Data da entrega:** 26/04/2026

## 📚 Resumo do Projeto

> O objetivo deste projeto é desenvolver um sistema de controle de tráfego (semáforo) inteligente e interativo, demonstrando os conhecimentos em sistemas embarcados com MicroPython. O sistema embarcado simula o funcionamento de um cruzamento, controlando o fluxo de veículos com um ciclo de Verde -> Amarelo -> Vermelho, e prioriza a travessia de pedestres por meio de um botão de solicitação. Ele oferece um ciclo normal para carros, que se repete indefinidamente. Quando um pedestre deseja atravessar, ele pode apertar um botão e o sistema sinaliza, aguardando o ciclo atual terminar, exibindo um sinal específico (LED verde) para a travessia com segurança. Essa é a principal interação do usuário com o sistema simulado.

## 🏗️ Arquitetura do Sistema Embarcado
A lógica do sistema se baseia em uma máquina de estados finitos (Finite State Machine - FSM) implementada no main.py. O programa alterna entre os estados "VERDE", "AMARELO" e "VERMELHO" de acordo com temporizadores e um pedido externo (botão).

O fluxo do programa é estruturado em um loop principal, onde o estado atual controla as ações sobre os componentes de hardware (LEDs). O diagrama pode ser visualizado no diagrama abaixo:

<img width="1468" height="724" alt="image" src="https://github.com/user-attachments/assets/1cfd7c5b-caf4-4c7b-88cf-f2d343f12758" />


## 🧑‍💻 Como funciona
Ao iniciar, o sistema executa a função setup() e configura todos os LEDs, além de inicializar o temporizador time.ticks_ms(). Uma decisão de projeto importante foi o uso da comunicação serial como uma ferramenta de interface homem-máquina. As ações do sistema são exibidas no console com print(), mostrando a mudança de estado (🟢 Verde - Siga), o pedido de travessia e a contagem regressiva, permitindo o acompanhamento das ações do semáforo. A resposta do CI confirma que a mensagem '🚦 Semáforo iniciado. Modo NORMAL.' foi exibida corretamente, validando essa comunicação.

## 💡 Componentes Utilizados na Simulação
Os seguintes componentes foram definidos no arquivo `diagram.json` para compor o circuito virtual da simulação：

*   **Placa Microcontroladora:** `board-esp32-devkit-c-v4`, que serve como o cérebro do sistema.
*   **LEDs (Saídas Visuais):** Quatro LEDs são usados para sinalização: o LED Vermelho (GPIO 32), o LED Amarelo (GPIO 33), o LED Verde (GPIO 25) para os carros, e um LED Verde adicional (GPIO 26) para pedestres.
*   **Botão (Entrada de Usuário):** Um botão de pressão (`wokwi-pushbutton`), conectado ao pino GPIO 27 com uma configuração de pull-up interno. Quando pressionado, ele sinaliza um pedido de travessia.
*   **Resistores:** Quatro resistores de 220Ω (GPIOs identificados por `r_red`, `r_yellow`, `r_green`, `r_ped`) são usados para limitar a corrente que passa por cada LED, prevenindo danos.
*   **Monitor Serial:** O componente `$serialMonitor` é utilizado para exibir as mensagens de status do sistema.

## 🧰 Decisões Técnicas Relevantes
A implementação do código `main.py` reflete as seguintes decisões técnicas:

*   **Organização do Código:** O código foi estruturado com funções dedicadas para cada tarefa (`setup()`, `verificar_botao()`, `piscar_led_vermelho()` e `loop_principal()`). Essa modularização facilita a leitura, manutenção e depuração.
*   **Uso de Máquina de Estados:** A escolha por uma *FSM* em vez de uma sequência linear de `time.sleep()` evita o bloqueio do sistema. Enquanto o semáforo está no estado `"VERDE"`, o programa continua verificando o botão (`verificar_botao()`) em paralelo, garantindo que um pedido de pedestre seja detectado a qualquer momento.
*   **Temporização Assíncrona:** A função usou `time.ticks_ms()` e `time.ticks_diff()` para controlar a duração de cada estado de forma não-bloqueante, ao invés de `time.sleep()`. Essa abordagem evita travar completamente o programa enquanto ele aguarda uma mudança de estado, sendo uma prática comum em sistemas embarcados para manter a responsividade.
*   **Tratamento do Botão (Debounce):** Foi implementada uma lógica de *debounce* simples com `time.sleep_ms(50)` na função `verificar_botao()`. Isso elimina leituras falsas causadas pelo ruído mecânico do botão, garantindo que um único toque seja registrado uma única vez.

## 📊 Resultados Obtidos
O sistema final atendeu aos requisitos propostos. O funcionamento correto foi validado localmente na plataforma **Wokwi** e, crucialmente, por meio do **GitHub Actions**. O sistema imprime no console a mensagem `'🚦 Semáforo iniciado. Modo NORMAL.'`, que foi configurada como critério de sucesso no CI. O log de execução mostra:

*   `🚦 Semáforo iniciado. Modo NORMAL.`
*   `Verde para carros por 10 segundos.`
*   `Teste`

Com base nesses resultados, o sistema **funciona corretamente** dentro do simulador.

Todos os requisitos descritos foram atendidos conforme o esperado. O comportamento observado na simulação do Wokwi demonstrou que o sistema executa o ciclo de um semáforo real e gerencia corretamente a interação com o usuário, um passo fundamental para a integração em um sistema maior.

## 🗣️ Comentários Adicionais
Durante o desenvolvimento, um dos maiores desafios foi configurar o ambiente de integração contínua (CI) para que o GitHub Actions validasse a simulação do Wokwi sem erros relacionados ao firmware (arquivos .bin). Superar essas dificuldades técnicas exigiu pesquisa (uso do vfs-merge) e testes, mas no final, a configuração aprovada no CI demonstra sua robustez.

Com mais tempo, futuras melhorias seriam implementar uma lógica de controle mais abrangente com múltiplos botões e semáforos para veículos em direções opostas, e exibir o status do sistema em um display de LCD ou OLED para uma interface mais rica.

Este projeto consolidou os aprendizados em MicroPython, máquinas de estado e integração de hardware simulado com CI, habilidades fundamentais para o desenvolvimento de produtos robustos em IoT.


## 🔍 Link para o repositório original do desafio
[Repositório base PNAT](https://github.com/pnaat/processoseletivoIoT)
