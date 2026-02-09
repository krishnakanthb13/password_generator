# Custom Wordlists

Place custom wordlist files here for use with the passphrase generator.

## Usage

```bash
python main.py phrase --wordlist data/wordlists/my_words.txt
```

## Format

- One word per line
- UTF-8 encoding
- Words should be 3+ characters
- Lines starting with # are treated as comments

## Example

```
apple
banana
cherry
dragon
elephant
```

## Included Wordlists

The passphrase generator includes a built-in EFF Large Wordlist (1600+ words) by default.
Custom wordlists override this default when specified.

### Themed Lists

| Filename | Count | Description | Example |
| :--- | :--- | :--- | :--- |
| `animals.txt` | 109 | Animals (land, sea, air) | `Lion-Eagle-Shark-Wolf` |
| `biology.txt` | 181 | Biological terms & anatomy | `Cell-Gene-DNA-Life` |
| `fruits.txt` | 50 | Common fruits | `Mango-Kiwi-Grape-Fig` |
| `ideas.txt` | 92 | Abstract concepts & values | `Truth-Honor-Hope-Time` |
| `linux.txt` | 79 | Linux commands & distros | `Bash-Vim-Sudo-Apt` |
| `mac.txt` | 70 | macOS applications | `Finder-Safari-Xcode` |
| `math.txt` | 138 | Math terms & functions | `Sum-Ratio-Pi-Graph` |
| `negative.txt` | 132 | Negative/Intense words | `Storm-Fear-Pain-Loss` |
| `objects.txt` | 111 | Common household items | `Lamp-Chair-Book-Pen` |
| `pc.txt` | 74 | PC hardware components | `Cpu-Gpu-Ram-Ssd` |
| `positive.txt` | 131 | Positive & uplifting words | `Happy-Joy-Hope-Love` |
| `values.txt` | 88 | Core personal values | `Loyalty-Growth-Faith` |
| `windows.txt` | 69 | Windows apps & tools | `Notepad-Edge-Cmd` |

### Themed Generation Example

```bash
# Generate a "jungle" passphrase
python main.py phrase -w 4 --wordlist data/wordlists/animals.txt --capitalize
>> Tiger-Parrot-Monkey-Snake
```
