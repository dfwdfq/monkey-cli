# Monkey-CLI Visual Examples

## Screenshot

Here's what the Monkey-CLI application looks like with the new features:

![Monkey-CLI Screenshot](https://github.com/user-attachments/assets/ca88566b-d6d4-4655-ae30-2c7f5fed1855)

The screenshot shows three states:
1. **Active Typing Test** - Updated with muted colors (gray instead of bright cyan/yellow) for comfortable extended use, showing real-time stats and color-coded text
2. **Test Complete** - Results screen with option to view history (Press H)
3. **History View** - NEW! Shows overall statistics and a visual WPM trend graph using ASCII bar charts

---

## 1. Starting Screen
```
================================================================================
                   🐵 MONKEY-CLI - Terminal Typing Test
              Duration: 30s | Press any key to start...
────────────────────────────────────────────────────────────────────────────────

the quick brown fox jumps over the lazy dog and runs through the
field with great speed and agility in the morning sunshine while
chasing butterflies across the meadow

                        ESC: Restart | Ctrl+C: Quit
================================================================================
```

## 2. During Typing (Colors indicated by annotations)
```
================================================================================
                   🐵 MONKEY-CLI - Terminal Typing Test
                Time: 12.5s | WPM: 48 | Accuracy: 97.3%
────────────────────────────────────────────────────────────────────────────────

[GREEN: the quick brown fox jumps over][RED: t][UNDERLINE: h][GRAY: e lazy dog and runs through the
field with great speed and agility in the morning sunshine while
chasing butterflies across the meadow]

                        ESC: Restart | Ctrl+C: Quit
================================================================================

Legend:
[GREEN] = Correctly typed characters
[RED] = Incorrectly typed characters  
[UNDERLINE] = Current cursor position
[GRAY] = Not yet typed
```

## 3. Test Complete - Results Screen
```
================================================================================
                           🎉 Test Complete!

                            WPM: 52.34
                          Accuracy: 96.50%
                      Correct Characters: 193
                     Incorrect Characters: 7
                       Total Characters: 200

              Press ESC to restart or Ctrl+C to quit
================================================================================
```

## 4. Color Scheme

The application uses terminal colors for visual feedback:
- **Green**: Correctly typed characters
- **Red**: Incorrectly typed characters (typos)
- **White/Gray**: Characters not yet typed
- **Yellow**: Statistics header (WPM, Accuracy, Timer)
- **Cyan**: Title and success messages
- **Underline**: Current cursor position

## 5. Key Features Demonstrated

### Real-time Feedback
As you type, each character is immediately color-coded:
- Correct → Green
- Incorrect → Red
- This helps you identify mistakes instantly

### Live Statistics
The header updates in real-time showing:
- **Time**: Countdown timer (30 seconds by default)
- **WPM**: Words per minute (calculated as chars/5/minutes)
- **Accuracy**: Percentage of correct characters

### Results Summary
After the test completes (time runs out or text is finished):
- Final WPM score
- Final accuracy percentage
- Total characters typed
- Breakdown of correct vs incorrect

### Controls
- **Any key**: Start the test
- **Backspace**: Delete last character
- **ESC**: Restart the test
- **Ctrl+C**: Quit the application
