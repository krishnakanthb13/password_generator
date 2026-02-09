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
