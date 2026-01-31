# 🐵 Monkey-CLI

A minimalistic typing test application for your terminal - inspired by [Monkeytype](https://monkeytype.com).

## Features

✨ **Real-time Statistics**: Track your WPM (Words Per Minute) and accuracy as you type  
🎨 **Color-Coded Feedback**: Green for correct characters, red for mistakes  
⏱️ **Timed Tests**: 30-second typing challenges  
🔄 **Restart Anytime**: Press ESC to restart, Ctrl+C to quit  
📊 **Detailed Results**: See your performance summary at the end  
📈 **Historical Tracking**: Automatic saving of all test results with statistics  
📉 **Visual Graphs**: ASCII bar charts showing WPM trends over time  
🎯 **Clean Minimal UI**: Muted color scheme for comfortable extended use  

## Installation

Clone this repository:
```bash
git clone https://github.com/arbkm22/monkey-cli.git
cd monkey-cli
```

No external dependencies needed! The application uses Python's built-in `curses` library.

### Windows Users
If you're on Windows, you'll need to install `windows-curses`:
```bash
pip install windows-curses
```

## Usage

Run the typing test:
```bash
python3 monkey_cli.py
```

Or make it executable and run directly:
```bash
chmod +x monkey_cli.py
./monkey_cli.py
```

## How to Play

1. **Start**: Press any key to begin the test
2. **Type**: Type the displayed words as accurately and quickly as possible
3. **Monitor**: Watch your real-time WPM and accuracy stats at the top
4. **Complete**: Finish the test or wait for the timer to run out
5. **Review**: Check your final statistics (automatically saved!)
6. **History**: Press H to view your typing history and progress graphs
7. **Restart**: Press ESC to try again or Ctrl+C to quit

## Keyboard Shortcuts

- **Any Key**: Start the test
- **Backspace**: Delete the last character
- **H**: View typing history (when test is complete)
- **ESC**: Restart the test or return from history view
- **Ctrl+C**: Quit the application

## Historical Data

All your test results are automatically saved to `~/.monkey-cli/history.json`. The history view shows:

- **Overall Statistics**: Total tests, average/best WPM, average/best accuracy, total characters typed
- **WPM Trend Graph**: Visual ASCII bar chart of your last 10 tests
- **Progress Tracking**: See your improvement over time

The app keeps your last 100 test results to track your progress while keeping the data file manageable.

## Customization

You can customize the test by modifying the parameters in `monkey_cli.py`:

```python
# Change duration (in seconds) and word count
test = TypingTest(stdscr, duration=60, word_count=100)
```

## Requirements

- Python 3.6+
- Terminal with color support
- Unix/Linux/macOS (native curses support) or Windows (with windows-curses)

## Screenshots

![Monkey-CLI Screenshot](https://github.com/user-attachments/assets/ca88566b-d6d4-4655-ae30-2c7f5fed1855)

The application features:
- Muted, comfortable color scheme for extended use
- Real-time WPM and accuracy display
- Color-coded text (green for correct, red for incorrect)
- Clean, distraction-free interface
- Comprehensive results screen
- Historical tracking with visual graphs
- Clean, distraction-free interface
- Comprehensive results screen

## License

MIT

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

Made with ❤️ for terminal enthusiasts
