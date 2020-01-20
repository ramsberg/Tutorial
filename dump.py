print(len(rest))
if len(rest):
	print("Looking.at?")
	if rest.split()[0] == 'at':
		print("Looking.at?-yes")
		print(rest.find(" ") + 1)
		item_of_interest = rest[rest.find(" ") + 1:]
		for object in player.room.objects:
			if item_of_interest == object.name:
				print(object.long_description)
else: