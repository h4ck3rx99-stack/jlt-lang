# ☕ Just Like That (`.jlt`)

<div align="center">

```
  ____. __   ___________ 
 |    ||  |  \__    ___/ 
 |    ||  |    |    |    
 /\__|    ||  |___ |    |    
 \________||______/|____|    
```

### *A Programming Language Crafted in Bangalorean English* 🚀

*"Swalpa adjust maadi, code will run pakka boss!"*

[![Language: JLT](https://img.shields.io/badge/Language-.jlt-orange.svg)](#)
[![Bangalore: 100%](https://img.shields.io/badge/Bengaluru-100%25-green.svg)](#)
[![Vibe: Filter Coffee](https://img.shields.io/badge/Filter%20Coffee-Active-brown.svg)](#)

</div>

---

## 🌆 What is `.jlt`?

**Just Like That (`.jlt`)** is a friendly, expressive, and fun programming language built around **Bangalore English** (the unique blend of English, conversational idioms, techie slang, and Kanglish spoken across Namma Bengaluru — from Koramangala to Malleshwaram).

Instead of boring old `print()`, you say:
```jlt
tell_ra_macha("Namaskara Bengaluru!");
```

Instead of dry `if / else`, you write:
```jlt
suppose (traffic_level > 80) {
    tell_ra_macha("Silk Board is jammed solid da, take Metro!");
} otherwise {
    tell_ra_macha("Road is khali, drive smoothly boss!");
}
```

---

## 🚀 Quick Start

### 1. Installation & Setup
Run directly with Python 3.8+:
```bash
# Clone or navigate to the directory
cd "c:/X Drive/JLT"

# Install locally in editable mode (optional)
pip install -e .
```

### 2. Run a `.jlt` Script
```bash
# Run any .jlt file directly
python -m jlt run examples/01_hello_world.jlt

# Or if installed via pip:
jlt run examples/06_bengaluru_techie_day.jlt
```

### 3. Interactive Bangalore REPL
```bash
python -m jlt repl
```
```text
╔═════════════════════════════════════════════════════════════════════════════╗
║          ☕  JUST LIKE THAT (.jlt) - BANGALORE ENGLISH REPL  ☕             ║
║                                                                             ║
║   "Swalpa adjust maadi, code will run pakka boss!"                         ║
║   Type 'exit', 'pack_up_macha', or 'saaku' to leave the session.            ║
║   Sample: let_us_say x = 10; tell_ra_macha("Total: " + str(x * 2));         ║
╚═════════════════════════════════════════════════════════════════════════════╝

jlt (bengaluru) >>> let_us_say coffee = 25;
jlt (bengaluru) >>> tell_ra_macha("Filter coffee bill: Rs. " + str(coffee));
➜ Filter coffee bill: Rs. 25
```

### 4. Transpile `.jlt` to Python
Want to compile your `.jlt` code into readable Python 3?
```bash
python -m jlt transpile examples/04_cafe_billing.jlt -o out.py
```

### 5. Check Syntax
```bash
python -m jlt check examples/02_silk_board_traffic.jlt
# ✅ Pakka! 'examples/02_silk_board_traffic.jlt' syntax is 100% valid Bangalore English code!
```

---

## 📖 Language Cheat Sheet & Syntax

### 🏷️ 1. Variables & Constants
| Concept | JLT Syntax | Description |
| :--- | :--- | :--- |
| **Variables** | `let_us_say x = 10;`<br>`macha name = "Rahul";`<br>`boss salary = 80000;`<br>`put food = "CTR Dosa";` | Declare dynamic variables |
| **Constants** | `pakka company = "Indiranagar Tech";`<br>`fixed_boss pi = 3.14;` | Value cannot be modified once set |
| **Reassignment** | `x = 20;` or `x += 5;` | Updates variable value |

---

### 🖨️ 2. Output & Input
| Concept | JLT Syntax | Example |
| :--- | :--- | :--- |
| **Print / Output** | `tell_ra_macha(...)`<br>`tell_da(...)`<br>`shout(...)` | `tell_ra_macha("Dosa is ready!");` |
| **User Input** | `ask_macha("prompt")`<br>`ask_da("prompt")` | `let_us_say area = ask_macha("Which area?: ");` |

---

### 🔀 3. Conditionals
Use `suppose`, `or_suppose`, and `otherwise`:
```jlt
let_us_say auto_meter = 120;

suppose (auto_meter > 100) {
    tell_ra_macha("What boss, meter is running too fast!");
} or_suppose (auto_meter == 30) {
    tell_ra_macha("Minimum fare only, very good!");
} otherwise {
    tell_ra_macha("Normal meter rate, paid smoothly.");
}
```

---

### 🔁 4. Loops & Iteration
#### While Loop (`as_long_as`):
```jlt
let_us_say battery = 30;
as_long_as (battery > 0) {
    tell_ra_macha("Coding in Third Wave Coffee...");
    battery -= 10;
}
```

#### Range Loop (`count_from`):
```jlt
count_from cup = 1 to 3 {
    tell_ra_macha("Enjoying Filter Coffee cup #" + str(cup));
}
```

#### For-Each Loop (`for_each`):
```jlt
for_each spot in ["CTR", "Corner House", "Vidyarthi Bhavan"] {
    tell_ra_macha("Must visit hangout: " + spot);
}
```

#### Loop Controls:
- **Break**: `pack_up_macha;` or `saaku_boss;`
- **Continue**: `adjust_and_go;` or `skip_da;`

---

### ⚙️ 5. Functions (`do_one_thing`, `give_back`)
```jlt
do_one_thing calculate_dosa_bill(count, extra_butter) {
    let_us_say rate = 80;
    let_us_say total = count * rate;
    
    suppose (extra_butter same_to_same pakka) {
        total += 20;
    }
    
    give_back total;
}

let_us_say my_bill = calculate_dosa_bill(3, pakka);
tell_ra_macha("Total Breakfast Bill: Rs. " + str(my_bill));
```

---

### 🛡️ 6. Error Handling (`adjust_and_try`, `what_ra_error`, `in_the_end`)
```jlt
adjust_and_try {
    let_us_say result = 100 / 0;
} what_ra_error (err) {
    tell_ra_macha("Ayyo! Calculation stuck at Silk Board: " + err);
} in_the_end {
    tell_ra_macha("Adjusted and recovered smoothly!");
}
```

---

### ⚖️ 7. Operators & Bangalore Logic

| Category | Keywords / Symbols | Meaning |
| :--- | :--- | :--- |
| **Booleans** | `pakka`, `correct_only`, `true_da` | `True` |
| | `bogus`, `wrong_only`, `fake_news` | `False` |
| **Null** | `khali`, `nothing_da`, `empty_scene` | `None / null` |
| **Equality** | `same_to_same`, `ditto`, `==` | Equal |
| | `different_only`, `not_same`, `!=` | Not Equal |
| **Comparison** | `more_than` (`>`), `less_than` (`<`) | Greater / Less |
| | `atleast` (`>=`), `atmost` (`<=`) | Min / Max |
| **Logical** | `and_also` (`&&`), `or_else` (`\|\|`) | AND / OR |
| | `opposite` (`!`), `ulta` | NOT |
| **Arithmetic** | `+`, `-`, `*`, `/`, `%`, `^` | Math ops |

---

### ☕ 8. Built-in Bangalore Standard Library

- `filter_coffee_boost()`: Returns a burst of instant caffeine motivation.
- `silk_board_jam(seconds)`: Simulates traffic delay with status alerts.
- `auto_fare(distance_km, is_night)`: Calculates Bangalore Auto Rickshaw meter fare (with 1.5x night multiplier).
- `bengaluru_weather()`: Instant Bangalore weather report.
- `len(obj)`, `str(obj)`, `num(obj)`, `bool(obj)`: Type conversions.
- `push(list, item)`, `pop(list)`: List manipulation.
- `keys(dict)`, `values(dict)`: Dictionary inspection.

---

## 📁 Examples Included

Explore the `examples/` directory for ready-to-run programs:

1. **`01_hello_world.jlt`**: Hello world, Bangalore variable declarations, and strings.
2. **`02_silk_board_traffic.jlt`**: Silk board conditionals and decision trees.
3. **`03_filter_coffee_loops.jlt`**: While loops, for-each loops, and range counters.
4. **`04_cafe_billing.jlt`**: Functions with parameter passing and discount logic.
5. **`05_auto_rickshaw_meter.jlt`**: Safe try/catch error handling and zero-division recovery.
6. **`06_bengaluru_techie_day.jlt`**: Full day in the life of a Bangalore startup engineer.

---

## 🧪 Running Tests

```powershell
pytest tests/ -v
```

---

## 💛 Made with Love in Bengaluru

*Swalpa code maadi, swalpa filter coffee kudi!* ☕✨
