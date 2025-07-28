# PgZero-Crawler

<img width="810" height="585" alt="image" src="https://github.com/user-attachments/assets/75048edc-9a35-4813-a7e0-d33b1b030c9e" />


# Dungeon Crawler - Roguelike Game

Um jogo roguelike desenvolvido em Python utilizando a biblioteca PgZero, com visão de cima para baixo, movimento suave entre células e animações de sprites

## Requisitos

- Python 3.6+
- PgZero (`pip install pgzero`)

## Como Jogar

### Instalação e Execução

Rode o comando:

pgzrun main.py


### Controles

- **WASD** ou **Setas do teclado**: Mover o herói
- **Mouse**: Navegar pelos menus
- **Espaço**: Retornar ao menu principal (tela de game over)

### Objetivo

- Explore a masmorra evitando os inimigos
- Mantenha-se vivo o máximo de tempo possível
- Cada colisão com inimigo causa 20 de dano
- Vida inicial: 100 pontos

## Características do Jogo

### Menu Principal

- **Start Game**: Inicia uma nova partida
- **Sound: ON/OFF**: Liga/desliga sons e música
- **Exit**: Sair do jogo

### Mecânicas de Jogo

- **Movimento suave**: Transições animadas entre células do grid
- **Sistema de vida**: HUD mostrando a vida atual do jogador
- **IA dos inimigos**: Patrulhamento inteligente em território limitado
- **Detecção de colisão**: Sistema preciso de colisão entre personagens
- **Animações**: Sprites animados para movimento e estado idle

### Inimigos

- **6 tipos diferentes**: Skeleton, Orc, Goblin
- **Patrulhamento**: Cada inimigo patrulha uma área de 3 células de raio
- **Movimento aleatório**: IA com intervalos variáveis de movimento
- **Animação**: Estados visuais diferentes para movimento e parado

## Arquitetura do Código

### Classes Principais

#### `SpriteAnimator`

- Gerencia animações de sprites com múltiplos frames
- Controla timing e ciclos de animação

#### `Character` (Classe Base)

- Sistema de movimento suave entre células do grid
- Animações para estados idle e movimento
- Coordenadas de grid e mundo
- Velocidade de movimento configurável

#### `Player`

- Herói controlado pelo jogador
- Sistema de vida
- Estados de vivo/morto

#### `Enemy`

- IA de patrulhamento
- Área de patrulha definida
- Movimento aleatório inteligente
- Múltiplos tipos visuais

#### `Game`

- Controle principal do jogo
- Gerenciamento de estados (Menu, Jogando, Game Over)
- Sistema de input
- Renderização
- Lógica de jogo

### Arquivos

```
projeto/
├── main.py         
└── README.md        
```

## Recursos Técnicos

### Sistema de Grid

- Grid 800x600 pixels
- Paredes e chão com renderização diferenciada

### Animação

- Sistema de frames múltiplos
- Animações separadas para idle e movimento
- Timing configurável por animação
- Efeitos visuais para feedback de movimento

### Estados do Jogo

- **MENU**: Tela inicial com opções
- **PLAYING**: Jogo ativo
- **GAME_OVER**: Tela de fim de jogo

### Sistema de Som

- Controle de habilitação/desabilitação
- Preparado para música de fundo e efeitos sonoros

## Configurações

### Personalizações Possíveis

- Velocidade de movimento dos personagens
- Número de inimigos
- Tamanho da área de patrulha
- Intervalos de movimento da IA
- Dano por colisão
- Vida inicial do jogador

## Tratamento de Erros

- Verificação de limites do grid
- Detecção de colisão com paredes
- Validação de posições válidas
