# NickGen

A simple nickname generator that runs in the terminal.

It can produce random nonsensical combinations as well as meaningful nicknames derived from real names.

---

## Setup

```bash
pip install -r dependencies.txt
```

## Usage

```bash
# default — generates a random nickname
py main.py

# generate 5 at once
py main.py -c 5

# meaningful nicknames from real names
py main.py -v

# generate a full name and suggest a matching nickname
py main.py -n

# options can be combined
py main.py -v -c 10 -m 16
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-c`, `--count` | Number of nicknames to generate | 1 |
| `-m`, `--max-length` | Max character length (including @) | 14 |
| `-v`, `--anlamli` | Generate meaningful nicknames | off |
| `-n`, `--name` | Generate a full name with a matching nickname | off |

## Modes

**Random (default)** — Produces pronounceable syllable patterns, fully random letters, or alphanumeric mixes.

**Meaningful (`-v`)** — Picks from real name databases provided by `nicknames` and `names`, appends 3 random digits.

**Name & Nickname (`-n`)** — Generates a random first-last name pair and suggests a fitting nickname for it.

## Dependencies

- [nicknames](https://pypi.org/project/nicknames/) — Name-to-nickname mapping dataset
- [names](https://pypi.org/project/names/) — Random name generator

## License

Personal use.
