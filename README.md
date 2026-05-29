# Azw Forza Bot

Bot de automação pra Forza Horizon com interface gráfica. Tem dois modos: um que farma corridas no piloto automático, e outro que executa a sequência de compra de carro na loja. Roda em segundo plano, você ativa e desativa com uma tecla.

---

## O que tem aqui

**Bot de Corrida** — Fica esperando a tela inicial da corrida aparecer, confirma, acelera até o final, detecta a chegada e reinicia o ciclo sozinho. Você só precisa deixar rodando.

**Bot de Compra** — Executa a sequência para comprar repetidamente um carro específico.

---

## Como usar cada script

**Bot de Corrida** — Acesse a corrida que quer farmar(testada apenas na corrida de destruir objetos) codigo da corrida 890 169 683, inicie o bot na tela inicial onde tem a opção "Iniciar evento de corrida".

**Bot de Compra** — Abra o menu, vá na aba campanha, diário de coleção, entre na aba da direita(Mestre da Exploração), coleção de carros, procure pelo carro que você deseja, entre nele com enter e ative o script. ***IMPORTANTE:*** Você precisa ter adquirido o carro pelo menos uma vez.

## Requisitos

- Python 3.10+
- Forza Horizon 6

Instale as dependências:

```bash
pip install pyautogui pydirectinput keyboard pygetwindow customtkinter
```

---

## Primeiros passos

### Rodando pela interface

```bash
python gui.py
```

A janela vai abrir. Selecione o script no dropdown, ajuste a hotkey se quiser (padrão: **F8**), e clique em **INICIAR**. A mesma hotkey que ativa também desativa.

> Rode sempre como **administrador** — sem isso, o `pydirectinput` pode não conseguir enviar inputs pro jogo dependendo da versão.

---

## Bot de Corrida — como configurar

Esse bot usa reconhecimento de imagem pra saber em que ponto da corrida você está. Antes de usar pela primeira vez, você precisa criar duas imagens de referência.

### Criando as imagens de referência

**1. `images/initial.png` — tela inicial da corrida**

Essa imagem é usada pra o bot saber quando a corrida está pronta pra começar. O ponto ideal é capturar **antes de você confirmar a corrida**, quando ainda aparece a tela com nome da corrida/mapa.

- Tire um print da tela enquanto estiver nessa tela de seleção
- Recorte uma parte pequena e específica — o nome da corrida, um ícone fixo, qualquer coisa que não mude entre as runs
- Salve como `images/initial.png`

**2. `images/finish_screen.png` — tela de chegada/vitória**

Essa imagem avisa o bot que a corrida terminou.

- Termine uma corrida manualmente uma vez pra ver a tela de resultado
- Tire um print e recorte algum elemento fixo que aparece só nessa tela (placar, ícone de vitória, etc.)
- Salve como `images/finish_screen.png`

> **Dica importante:** Use imagens pequenas e bem específicas. Quanto mais genérica a imagem, maior a chance de falso positivo. Evite áreas que tenham animações, cronômetros ou qualquer coisa que muda na tela.

---

## Trocando a hotkey

Na interface tem um campo mostrando a hotkey atual. Clica em **Alterar**, pressiona a tecla que quer usar, e pronto. Vale tanto pra ativar quanto pra desativar o bot. A configuração fica salva enquanto o programa estiver aberto.

---

## Gerando o executável

Se quiser usar em outro PC sem precisar instalar Python:

**1. Instale o PyInstaller:**
```bash
pip install pyinstaller
```

**2. Rode o build:**
```bash
python build.py
```

O `.exe` vai aparecer em `dist/Azw Forza Bot.exe`. Ele já pede permissão de administrador automaticamente ao abrir, então não precisa fazer nada extra.

> Ao distribuir o executável, lembre de incluir a pasta `images/` com as duas imagens de referência no mesmo diretório que o `.exe`.

---

## Problemas comuns

**O bot não detecta as imagens**
Isso geralmente acontece quando a resolução ou escala do jogo é diferente da usada na hora de capturar as imagens. Recapture com o jogo no mesmo modo (janela/fullscreen) e mesma resolução.

**Inputs não funcionam no jogo**
Rode como administrador. Alguns jogos ignoram inputs simulados sem privilégio elevado.

**O F8 não para o bot imediatamente**
O bot checa a flag de parada a cada 0.1s. Em momentos de sleep mais longo (ex: aguardando reinício da corrida), pode demorar até o próximo ciclo de checagem — o que é no máximo alguns décimos de segundo.

**Falso positivo na detecção**
Diminua o parâmetro `confidence` nos arquivos `bot_forza.py` se não estiver detectando, ou aumente se estiver detectando coisas erradas. O valor padrão é `0.5` pra tela inicial e `0.6` pra chegada.

---

*by Azw*
