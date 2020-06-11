# Advanced Minecraft Scripting
This project aims at producing a more human readable version of Minecraft's mcfunction format. This documentation will explain the new syntax, the components of the compiler and contains a user guide to use this program to compile your project into a Minecraft datapack.

## Syntax

The AMS scripting language is based on the mcfunction syntax. The new syntax simply aims at making the code more readable and reducing duplicate code.

### The Child System

Whenever the compiler finds an line of code indented with a **tab** it will interpret this as a child to the previous line of code with one less indent.

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

This can be done as many times as necessary. Whenever a command is a child it's parent is simply prepended.

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
