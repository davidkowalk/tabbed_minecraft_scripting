execute as @a[scores = {kills=1..}] run clear @s 
# if statement
execute as @a[scores = {kills=1..}] if score game_states matches 1 run function combat:give_loot
execute as @a[scores = {kills=1..}] if score game_states matches 1 run say @s made a kill
execute as @a[scores = {kills=1..}] run scoreboard players set @s kills 1
say ticking
