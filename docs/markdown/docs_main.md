# Advanced Minecraft Scripting
This project aims at producing a more human readable version of Minecraft's mcfunction format. This documentation will explain the new syntax, the components of the compiler and contains a user guide to use this program to compile your project into a Minecraft datapack.

## Syntax

The AMS scripting language is based on the mcfunction syntax. The new syntax simply aims at making the code more readable and reducing duplicate code.

### The Child System

Whenever the compiler finds an line of code indented with a **tab** or a **space** it will interpret this as a child to the previous line of code with one less indent. Whenever a command is a child it's parent is simply prepended.

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

# API Reference

The ``ams_compiler.py`` is the api which handles the data. You can import it with ``import ams_compiler``.

## build_tree()

Converts file to custom data structure. See ``class node`` for tree reference

| Parameter | default | description |
|-----------|---------|-------------|
| file      | -/-     | List of strings. Each entry describes one line of the file. Produces a node-tree
| debug     | False   | Show debug information.

## compile_tree_list()

Calls ``node.compile()`` for each node in the list and bakes an output string.

| Parameter | default | description |
|-----------|---------|-------------|
| tree_list | -/-     | List of node trees.

## class node
This class is the building block of the parent-child structure.
Each node has a variable ``string`` (str) and  a variable ``children`` (list).

### \_\_init\_\_()
Called when defining new element with
```root = node("String")```

| Parameter | default | description |
|-----------|---------|-------------|
| string    | -/-     | String that defines this child.

```python
self.string = string
self.children = []
```

### add_child():

Adds child to ``children``. Accepts either string or node-object. Strings then get converted to node-object.

| Parameter | default | description |
|-----------|---------|-------------|
| child     | -/-     | String or node-object.

### to_str()
Compiles tree of element and all children into list recursively.

| Parameter | default | description |
|-----------|---------|-------------|
| n         | 1       | Length of first indent.

### compile()
Compiles tree into list of strings recursively.

**Example**
```
execute if condition
  run command1
  run command2
```
Compiled:
```
[
  "execute if condition run command1",
  "execute if condition run command2"
]
```

| Parameter | default | description |
|-----------|---------|-------------|
| parent    | ""      | Parent string to be prepended.
