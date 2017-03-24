# Documentació

## APIs

### Input del director
Un fitxer amb L línies que consten de quatre nombres cada una: `t n v d `.
- `t` és el temps (en segons)
- `n` és la nota (en midi)
- `v` és la velocitat (volum)
- `d` és la durada (en segons). Totes les durades `d` han de ser múltiples del mínim entre 100 i la `d` més petita.

### Output del director i input del client (reproductor)
Un fitxer amb L línies que tenen el format següent: `(t, msg0, ,msg1, ... , msg7)`
- `t` és el temps en segons
- `msgx` és el misstage del track número `x`. Aquest missatge pot ser:
  - `0`. No passa res en aquell track
  - `255`. Note off
  - Altrament: nota en midi a reproduir


## Historial

### 2017/03/03

- Configuració de la raspberry pi
- Instal·lació Polyphone per editar i visualitzar fonts
- Consulta de la documentació de FluidSynth i el codi del Director

### 2017/03/10

- Analitzada API director
- Analitzada comunicació amb sockets
- Començada reproducció en el client

### 2017/03/17

- Feta defensa 1
- Creada i debuguejada una nova versió del client (clientPlayer.py) que rep i reprodueix les notes (part de reproducció només funciona a l'ordinador i no a la raspberry)


### 2017/03/24

- Treballant en la reproducció de música a la raspberry. Problemes amb els drivers i la reprdoducció del fluidsynth.py. Todo: instal·lar pixel a la raspberry.
