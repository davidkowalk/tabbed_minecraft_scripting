# Advanced Minecraft Scripting
This project aims at producing a more human readable version of Minecraft's mcfunction format. This documentation will explain the new syntax, the components of the compiler and contains a user guide to use this program to compile your project into a Minecraft datapack.

## Syntax

The AMS scripting language is based on the mcfunction syntax. The new syntax simply aims at making the code more readable and reducing duplicate code.

### The Child System

Whenever the compiler finds an line of code indented with a **tab** it will interpret this as a child to the previous line of code with one less indent. Whenever a command is a child it's parent is simply prepended.

**Example:**
```mcfunction
execute as @e[type=minecraft:villager, tag=!done]
  run data modify entity @s NoGravity set value true
  run tag @s add done
```

Parsed through the compiler this is assembled into this valid mcfunction code.

```mcfunction
execute as @e[type=minecraft:villager, tag=!done] run data modify entity @s NoGravity set value true
execute as @e[type=minecraft:villager, tag=!done] run tag @s add done
```

This can be done as many times as necessary.

**Example:**
```mcfunction
execute as @a
  if score @s dummy_scores matches 1
    run function main:func1
  if score @s dummy_scores matches 2
    if score state game_states matches 0
      run function main:func2
```
Compiles to:
```mcfunction
execute as @a if score @s dummy_scores matches 1 run function main:func1
execute as @a if score @s dummy_scores matches 2 if score state game_states matches 0 run function main:func2
```

## Usage

There are many different options to either integrate the compiler into your own application or directly use it as an application. This section will focus on the former.

### Visual Interface

Simply run ``interface.py`` with python and press "Load and Compile File". You will be prompted with a read path to select. Afterwards the program may briefly freeze but you will then be prompted with a save dialog. Select where you want to save the compiled file to and press "Save".

### Run as an import
Import the compiler into your program and run it with an input and an output path.:
```python
from interface import compile
compile(input_path, output_path)
```
