# Chainsaw
## Install
### `chainsaw` dependencies

* `python3-pyo`
* `python3-liblo`
* `jackd2`

#### `midi_chainsaw` dependencies

* `mididings`

### `chainsaw`

    git clone https://framagit.org/groolot-association/chainsaw.git
    cd chainsaw
    make all

#### Debian like

    sudo dpkg -i ./chainsaw_x.y_all.deb

#### With `pip`

    pip3 install ./chainsaw-x.y-py3-none-any.whl

## Credits
### Lead developers
 * Grégory David <dev@groolot.net>
 * Jean-Emmanuel Doucet <jean-emmanuel.doucet@groolot.net>

### Framework

 * Olivier Bélanger (Pyo: https://github.com/belangeo/pyo)

## Diagrams
### Audio pipeline
![Instrument audio pipeline](documentation/pipeline.png)

### UML Class diagram
![Global UML class diagram](documentation/UML_class_diagram.png)
