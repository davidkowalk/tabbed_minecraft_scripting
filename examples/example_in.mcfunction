execute as @a[scores = {kills=1..}]
	run clear @s
	
	# if statement
	if score game_states matches 1
		run function combat:give_loot
		run say @s made a kill

	run scoreboard players set @s kills 1

say ticking
