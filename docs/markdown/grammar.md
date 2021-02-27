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

* ban
* ban-ip
* defaultgamemode
* deop
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
