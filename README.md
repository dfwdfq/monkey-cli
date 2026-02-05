# Monkey-CLI
Monkeytype clone for terminal. De-vibecoded fork.


## Installation

Clone this repository:
```bash
git clone https://github.com/arbkm22/monkey-cli.git
cd monkey-cli
```

No external dependencies needed! The application uses Python's built-in `curses` library.



## Usage
### run with default settings
```bash
chmod +x monkey_cli.py
./monkey_cli.py
```
### run with custom duration(in seconds)
```bash
./monkey_cli.py -d 15
```

or

```bash
./monkey_cli.py --duration 15
```


### run with custom words count
```bash
./monkey_cli -w 10
``

or

```bash
./monkey_cli.py --word-count 15
```

### configure with 2 possible arguments
```bash
./monkey_cli.py -w 10 -d 15
```


### see history
```bash
./monkey_cli.py -H
```
