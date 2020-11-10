# TMS Best Practice Proposals

TBPP is meant as a documentation of general best practices to optimize readabillity and run time performance.

## 1. Indentation vs. Functions

Even though TMS makes repeated beginnings of lines extremely easy this is not always optimal for runtime performance.

**When should you create a new function?**

Commands should be grouped into a new function when find a given selector multiple times. Instead of finding this selector n times you can find the selector once and make the selected entity execute a function.

For example:

```mcfunction
execute as @e[tag=team_blue] run
  replaceitem entity @s armor.head minecraft:leather_helmet
  replaceitem entity @s armor.chest minecraft:leather_chestplate
```

This will compile into the following code:

```mcfunction
execute as @e[tag=team_blue] run replaceitem entity @s armor.head minecraft:leather_helmet
execute as @e[tag=team_blue] run replaceitem entity @s armor.chest minecraft:leather_chestplate
```

As you can see in this example Brigadier would need to find any entity with the tag `team_blue` two times and then execute a command on them. Instead you should write a function file:

```mcfunction
replaceitem entity @s armor.head minecraft:leather_helmet
replaceitem entity @s armor.chest minecraft:leather_chestplate
```

and then run this function using:

```mcfunction
execute as @e[tag=team_blue] run function namespace:function
```

**When should you use indents?**

Indents should be used when creating different variations of a command. For example:

```mcfunction
execute if
  score @s objective matches 1 run function if:option1
  score @s objective matches 2 run function if:option2
  score @s objective matches 3 run
    say @s -> Option 3
    tp @s ~ ~ ~ ~ ~180
```

This produces four completely unique lines of code, none of which could be outsourced into a secondary file for performance.


## 2. Conditional blocks

A block of code indented below a condition will test the condition for every line of the code.

Suppose a code block like this:

```mcfunction
execute if score Score GameScores matches 1
  run scoreboard players set Score GameScores 0
  run function lobby:reset
  run function effect:reset
```

In this scenario the functions `lobby:reset` and `effect:reset` will never be called, since the condition can not be satisfied. Instead the modification of `Score` should either be moved to the end of the code-block or the three lines should be moved into a wrapper function which calls all three. This will also improve performance, since the condition is only tested once.

## Constant Naming Convention

To avoid conflicts with existing expressions in your code, constants defined in the config-file should be prepended with either `var_` or `const_`. Example

```json
{
  "ifiles": [],
  "ofiles": [],
  "define": {
    "const_location_1": "x y z",
    "const_location_2": "x y z"
  }
}
```

where in the mcfunction source file you may then use these constants as a replacement for the values you defined:

```mcfunction
setbloc
  const_location_1 air
  const_location_2 redstone_block
