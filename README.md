# 🎛️ Projeto de IoT - Processo Seletivo PNAAT

**Nome:** Icaro Cavalcante de Carvalho Pinheiro  
**E-mail:** icarodev06@gmail.com  

## 📚 Resumo do Projeto

> O objetivo deste projeto é o desenvolvimento de um Semáforo Inteligente para controle de tráfego veicular e de pedestres. O sistema simula um cruzamento urbano onde o fluxo de carros é interrompido sob demanda por um botão de travessia. O usuário interage pressionando o botão de pedestre, o que sinaliza ao controlador a necessidade de transição para a fase de segurança, respeitando tempos mínimos de verde para os veículos.

## 🏗️ Arquitetura do Sistema Embarcado
O projeto utiliza uma **Máquina de Estados Finita (FSM)** para gerenciar as transições de sinalização de forma determinística e segura. 
*   **Fluxo Principal:** O código roda em um loop infinito que monitora constantemente as entradas (botão) enquanto verifica o tempo decorrido no estado atual.
*   **Temporização Não-Bloqueante:** Em vez de utilizar `time.sleep()`, o sistema utiliza `time.ticks_ms()` para calcular intervalos. Isso garante que o microcontrolador nunca fique ocioso e possa responder a eventos (como o pressionamento do botão) a qualquer momento.
*   **Estrutura de Estados:**
    *   `VERDE`: Fluxo veicular liberado.
    *   `AMARELO`: Transição de atenção.
    *   `VERMELHO`: Pare veicular e preparo para pedestres.
    *   `TRAVESSIA`: Sinal verde para pedestres.
    *   `PISCANDO`: Alerta final de travessia antes do retorno ao verde veicular.
 

## 📜 Diagrama

<img width="839" height="620" alt="image" src="https://github.com/user-attachments/assets/0922cf07-d65a-4256-bc90-98d7cd0f80a7" />


## 💡 Componentes Utilizados na Simulação
*   **Placa:** ESP32 DevKit V4 (Padrão para aplicações IoT e embarcados).
*   **LEDs Veiculares (Vermelho, Amarelo, Verde):** Indicadores do estado de tráfego de carros.
*   **LED Pedestre (Verde):** Indicador de travessia segura para o usuário.
*   **Pushbutton:** Entrada digital configurada com *Pull-up* interno para disparar a solicitação de travessia.
*   **Resistores (220Ω):** Proteção dos periféricos contra sobrecorrente.

## 🧰 Decisões Técnicas Relevantes
A implementação do código `main.py` reflete as seguintes decisões técnicas:

*   **Organização do Código:** O código foi estruturado com funções dedicadas para cada tarefa (`setup()`, `verificar_botao()`e `loop_principal()`). Essa modularização facilita a leitura, manutenção e depuração.
*   **Uso de Máquina de Estados:** A escolha por uma *FSM* em vez de uma sequência linear de `time.sleep()` evita o bloqueio do sistema. A função verificar_botao() é executada de forma assíncrona ao fluxo de temporização em todos os estados do ciclo. Isso garante que uma solicitação de travessia nunca seja perdida, independentemente de o semáforo estar na fase verde, amarela ou vermelha, elevando a confiabilidade do sistema e a experiência do usuário.
*   **Temporização Assíncrona:** A função usou `time.ticks_ms()` e `time.ticks_diff()` para controlar a duração de cada estado de forma não-bloqueante, ao invés de `time.sleep()`. Essa abordagem evita travar completamente o programa enquanto ele aguarda uma mudança de estado, sendo uma prática comum em sistemas embarcados para manter a responsividade.
*   **Tratamento do Botão (Debounce):** Foi implementada uma lógica de *debounce* simples com `time.sleep_ms(50)` na função `verificar_botao()`. Isso elimina leituras falsas causadas pelo ruído mecânico do botão, garantindo que um único toque seja registrado uma única vez.

## 📊 Resultados Obtidos
O sistema final atendeu aos requisitos propostos. O funcionamento correto foi validado localmente na plataforma **Wokwi** e, crucialmente, por meio do **GitHub Actions**. O log de execução mostra:

*   `🚦 Semáforo iniciado.`
*   `Teste`

Com base nesses resultados, o sistema **funciona corretamente** dentro do simulador.

Todos os requisitos descritos foram atendidos conforme o esperado. O comportamento observado na simulação do Wokwi demonstrou que o sistema executa o ciclo de um semáforo real e gerencia corretamente a interação com o usuário, um passo fundamental para a integração em um sistema maior.

## 🗣️ Comentários Adicionais
Durante o desenvolvimento, um dos maiores desafios foi configurar o ambiente de integração contínua (CI) para que o GitHub Actions validasse a simulação do Wokwi sem erros relacionados ao firmware (arquivos .bin). No final, a configuração aprovada no CI demonstra sua robustez.


Este projeto consolidou os aprendizados em MicroPython, máquinas de estado e integração de hardware simulado com CI, habilidades fundamentais para o desenvolvimento de produtos robustos em IoT.


## 🔍 Link para o repositório original do desafio
[Repositório base PNAT](https://github.com/pnaat/processoseletivoIoT)
