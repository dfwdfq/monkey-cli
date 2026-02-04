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

## Requirements

- Python 3.6+
- Terminal with color support
- Linux(don't care of non-Linux)

## Screenshots(Not mine)

![Monkey-CLI Screenshot](https://github.com/user-attachments/assets/ca88566b-d6d4-4655-ae30-2c7f5fed1855)

The application features:
- Muted, comfortable color scheme for extended use
- Real-time WPM and accuracy display
- Color-coded text (green for correct, red for incorrect)
- Clean, distraction-free interface
- Comprehensive results screen
- Historical tracking with visual graphs
