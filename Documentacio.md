# Documentació

## Instruccions d'ús
Tots els arxius a executar es troben al directori `Code`.
1. Obrir una terminal en un ordinador que pugui fer multicast a la xarxa i executar `./bot.py`.
2. Connectar-se amb ssh a cadascuna de les raspberries (`ssh pi@10.5.3.128` per exemple). Si la raspberry no està actualitzada, executar `./configure.sh`.
3. En cada raspberry pi, executar `./setSoundDevice.py` i després `python3 clientPlayer.py -t tracks_a_reproduir_en_aquest_dispositiu` (per exemple, per reproduir els tracks 3 i 4 farem `python3 clientPlayer.py -t 3,4`.

## Historial

### 2017/03/03

- Configuració de la raspberry pi
- Instal·lació Polyphone per editar i visualitzar fonts
- Consulta de la documentació de FluidSynth i el codi del Director

### 2017/03/10

- Analitzada API director
- Analitzada comunicació amb sockets
- Començada reproducció en el client

### 2017/03/17: defensa 1

- Feta defensa 1
- Creada i debuguejada una nova versió del client (clientPlayer.py) que rep i reprodueix les notes (part de reproducció només funciona a l'ordinador i no a la raspberry)


### 2017/03/24

- Treballant en la reproducció de música a la raspberry. Problemes amb els drivers i la reprdoducció del fluidsynth.py. Todo: instal·lar pixel a la raspberry.


### 2017/03/31

- Instal·lat pixel a la raspberry pi i solucionat el problema amb la reproducció de so a la raspberry. *Ja funciona!* Ara només faltaria tenir més raspberries, amb targetes SD i altaveus i ja tindríem una orquestra.
- Creat el bot de Telegram.
- Modularització de la classe director.


### 2017/04/21

- Instruccions d'ús
- ...

### 2017/04/28: defensa 2

- Feta defensa 2: primera prova amb més d'un altaveu amb èxit :D

### 2017/05/05

- Creació d'un script per canviar l'output per defecte d'audio per tal de poder reproduir la música per la tarjeta de so USB.
- Definició protocol de comunicació director -- músic amb format JSON.

### 2017/05/12

- Primera versió del bot de Telegram: enviament d'imatges.
- Implementat el protocol de comunicació amb JSON.
- Troballa de llibreria que passa de MIDI a JSON. Es deixaran d'usar els fitxers `txt` de les pistes.

### 2017/05/19

- El bot ja es baixa arxius midi.
- Reproducció de midi també funciona (falta optimitzar).
- Pel proper dia, falta ajuntar els dos punts anteriors i ja ho tindrem.
- Comença la redacció de la memòria.

### 2017/05/26

- Units els codis del bot i el director.
- Actualitzat l'arxiu de configuració per instal·lar les llibreries de telegram.
- Redacció de la memòria i la presentació final.

### 20117/06/02: defensa final

- Presentació final del treball

## APIs

### Input del director
Un fitxer amb L línies que consten de quatre nombres cada una: `t n v d `.
- `t` és el temps (en segons)
- `n` és la nota (en midi)
- `v` és la velocitat (volum)
- `d` és la durada (en segons). Totes les durades `d` han de ser múltiples del mínim entre 100 i la `d` més petita.

### Output del director i input del client/músic (obsolet)
Un fitxer amb L línies que tenen el format següent: `(t, msg0, ,msg1, ... , msg7)`
- `t` és el temps en segons
- `msgx` és el misstage del track número `x`. Aquest missatge pot ser:
  - `0`. No passa res en aquell track
  - `255`. Note off
  - Altrament: nota en midi a reproduir
  
### Comunicació en JSON

En aquest nou protocol les dades s'envien de la següent manera,
hi ha les variables `in`, `out` i `tracks`. Que contenen

 - `in`: Objecte amb `numero_canal` i `notes_entren`.
 - `out`: Objecte amb `numero_canal` i `notes_paren`.
 - `tracks`: Nombre de pistes que hi ha en total

```JSON
{
  "in": {
    "1": [1, 2, 3],
    "3": [4, 5, 6]
  },
  "out": {
    "1": [4, 5],
    "2": [1, 2]
  },
  "tracks": 8
}
```
