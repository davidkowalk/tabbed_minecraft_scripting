# AMS Best Practice Proposals

ABPP is meant as a documentation of general best practices to optimize readabillity and run time performance.

## 1. Indentation vs. Functions

Even though AMS makes repeated beginnings of lines extremely easy this is not always optimal for runtime performance.

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
