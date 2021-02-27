# Grammar

This file documents the grammar of the commands supported by the interpreter. The interpreter is designed specifically for the Java-version of minecraft.

## List of active minecraft commands

|  Comands  | Status  | Action
|-----------|---------|-------
| attribute | Planned | Queries, adds, removes or sets an entity attribute.
| bossbar   | Planned | Creates and modifies bossbars in the backend
| clear     | Planned | Clears items from player inventory.
| data      | Planned | Gets, merges, modifies and removes block entity, entity or storage NBT data.
| effect    | Planned | Add or remove status effects to entity.
| enchant   | Planned | Adds an enchantment to a player's selected item.
| execute   | Planned | The big one. Executes other commands.
| function  | Planned | Calls another function.
| gamemode  | Planned | Sets a players gamemode.
| give      | Planned | Gives an item to a player if there is space in the players inventory
| kill      | Planned | Delete entity object.
| list      | Planned | Lists players one the server
| say       | Planned | Prints a message in the console with the senders name
| scoreboard| Planned | Manages scoreboard objectives and players.
| stop      | Planned | Exits the interpreter
| summon    | Planned | Summons any entity. (players included in the interpreter)
| tag       | Planned | Controls entity tags
| team      | Planned | Adds or removes players from teams
| teleport  | Planned | Changes the coordinates of an entity. Alias: `tp`
| tellraw   | Planned | Displays JSON messages in the console.
| title     | Planned | Displays JSON message in the console.



## List of ignored commands

These commands will be read by the interpreter but will do nothing. This list may be modified in the future

* clone
* fill
* setblock
* datapack
* debug
* difficulty
* experience/xp
* forceload
* gamerule
* particle
* playsound
* schedule
* seed
* setblock
* spawnpoint
* stopsound
* teammsg/tm
* tell
* time
* weather
* worldborder

## List of commands that will not be implemented

These commands will throw a warning in the console when encountered, as if they were invalid comands. This list may be modified in the future and some may be moved to ignored commands.
I decided that these commands are used too infrequently as to implement them.

* ?
* advancement
* ban
* ban-ip
* defaultgamemode
* deop
* help
* kick
* locate
* locatebiome
* loot
* me
* msg
* op
* pardon
* pardon-ip
* publish
* save-all
* save-off
* save-on
* setidletimeout
* setworldspawn
* spectate
* spreadplayers
* whitelist

## Grammar

This section lays out the grammar of all commands in the active or ignored command list.

---
### Active commands

#### attribute

```
attribute <target> <attribute> (
  get [<scale>] |
  base get [<scale>] |
  base set <value> |
  modifier add <uuid> <name> <value> (add|multiply|multiply_base) |
  modifier remove <uuid> |
  modifier value get <uuid> [<scale>]
)
```

#### bossbar

```
bossbar (
  add <id> <name> |
  get <id> (max|players|value|visible) |
  list |
  remove <id> |
  set <id> (
    color (blue|green|pink|purple|red|white|yellow) |
    max <max> |
    name <name> |
    players [<target>] |
    style (notched_6|notched_10|notched_12|notched_20|progress) |
    value <value> |
    visible <visible>
    )
  )
```

#### clear

```
clear [<targets>] [<item>] [<maxCount>]
```

#### data

```
data (
  get ( block <targetPos> | entity <target> | storage <target>) [<path>] [<scale>] |
  merge (block <targetPos> | entity <target> | storage <target>) <nbt> |
  modify (block <targetPos> | entity <target> | storage <target>) <targetPath> (
    append (from (block <sourcePos> | entity <source> | storage <source>) [<sourcePath>] | value <value>) |
    insert <index> (from (block <sourcePos>|entity <source>|storage <source>) [<sourcePath>] | value <value>) |
    merge (from (block <sourcePos> | entity <source> | storage <source>) [<sourcePath>] | value <value>) |
    prepend (from (block <sourcePos>|entity <source>|storage <source>) [<sourcePath>] | value <value>) |
    set (from (block <sourcePos>|entity <source>|storage <source>) [<sourcePath>] | value <value>) |
    remove (block <targetPos>|entity <target>|storage <target>) <path>
  )
)
```

#### effect

```
effect (
  clear [<targets>] [<effect>] |
  give <targets> <effect> [<seconds>] [<amplifier>] [<hideParticles>]
  )
```

#### enchant

```
enchant <targets> <enchantment> [<level>]
```

#### execute

I'm procrastinating on this one.

#### function

```
function <name>
```

#### gamemode

```
gamemode (adventure|creative|spectator|survival) [<target>]
```

#### give

```
give <target> <item> [<count>]
```

#### kill

```
kill [<targets>]
```

#### list

```
list
```

#### say

```
say <message>
```

#### scoreboard

```
scoreboard (
  objective (
    add <objective> <criterion> [<displayName>] |
    list |
    modify <objective> (displayname <displayName> | rendertype (hearts|integer)) |
    remove <objective>
    setdisplay <slot> [<objective>])|
  player (
    add <targets> <objective> <score> |
    enable <targets> <objective> |
    get <target> <objective> |
    list [<target>] |
    operation <targets> <targetObjective> <operation> <source> <sourceObjective> |
    remove <targets> <objective> <score> |
    reset <targets> [<objective>] |
    set <targets> <objective> <score>
    )
  )
```

#### stop

```
stop
```

#### summon

```
summon <entity> [<pos>] [<nbt>]
```

#### tag

```
tag <targets> (
  add <name> |
  list |
  remove <name> |
  )
```

#### team

```
team (
  add <team> [<displayName>] |
  empty <team> |
  join <team> [<members>] |
  leave <members> |
  list [<team>] |
  modify <team> <option> <value> |
  remove <team>
  )
```

#### teleport

```
(teleport | tp) (
  <targets> <destination> |
  <targets> <location> [<rotation>] |
  <targets> <location> facing <facingLocation> |
  <targets> <location> facing entity <facingEntity> [<facingAnchor>]
  )
```

#### tellraw

```
tellraw <targets> <message>
```

#### title

```
title <target> (
  (clear | reset) |
  (title|subtitle|actionbar) <title> |
  times <fadeIn> <stay> <fadeOut>
  )
```


---
### Ignored commands

#### advancement
#### ban
#### ban-ip
#### defaultgamemode
#### deop
#### kick
#### locate
#### locatebiome
#### loot
#### me
#### msg
#### op
#### pardon
#### pardon-ip
#### publish
#### save-all
#### save-off
#### save-on
#### setidletimeout
#### setworldspawn
#### spectate
#### spreadplayers
#### whitelist
---
