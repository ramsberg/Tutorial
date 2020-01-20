from adventure_caller_data import world,objects
import random

move_commands =['N','S','E','W','out']
quit_commands =['quit','die']
take_commands =['take','get','grab','pickup']
drop_commands =['drop']
look_commands =['look']
inventory_commands = ['i','inventory','inv','backpack']

all_commands = move_commands+quit_commands+take_commands+drop_commands+look_commands+inventory_commands


unnessecary_words = ('on','at','to','the')

def split_command(command):
	command_list = command.split(" ")
	pure_command_list = list(set(command_list) - set(unnessecary_words))
	print(command_list)
	print(pure_command_list)
	return pure_command_list

class Player:
	global maze_completed
	def __init__(self,name, start_position):
		self.level = 1
		self.health = self.level * 10
		self.inventory = []
		self.name = name
		self.room = start_position
		self.can_move = True

	def show_inventory(self):
		print("You are currently carrying:")
		for item in self.inventory:
			print(item.short_description)

	def calculate_weight(self):
		total_weight = 0
		for item in self.inventory:
			total_weight += item.weight
		if total_weight > 10:
			self.can_move = False
		else:
			self.can_move = True
		return total_weight

	def take(self,itemname):
		found = False
		for room_item in player.room.objects:
			if room_item.name == itemname:
				found = True
				self.inventory.append(room_item)
				print("You put {} in your backpack.".format(room_item.name))
				self.room.remove_object(room_item)
				self.calculate_weight()
				return
		if not found:
			print("I cannot find that here")


	def drop(self,itemname):
		found = False
		for item in self.inventory:
			if item.name == itemname:
				found = True
				self.inventory.remove(item)
				print("You drop {}.".format(item.name))
				self.room.add_object(item)
				return
		if not found:
			print("You don't have {} in your backpack.".format(item))

	def health(self):
		return self._health

	def move(self, direction):
		if self.can_move:
			if direction not in self.room.exits:
				print("Cannot move in that direction!")
				return
			new_room_name = self.room.exits[direction]
	#		print('moving to', new_room_name)
			self.room = world[new_room_name]
			if self.room.name == 'goal_room':
				maze_completed = True
		else:
			print("You can't move, you are maybe carrying too much?")


def hide_things():
	room_list = []
	for room in world.keys():
		room_list.append(room)

	world[random.choice(room_list)].add_object(objects['key1'])
	#world[random.choice(room_list)].add_object(objects['key2'])
	#world[random.choice(room_list)].add_object(objects['sword1'])
	world[random.choice(room_list)].add_object(objects['door1'])
	objects['door1'].opening_items.append('key1')


player = Player("balgor", world['room1'])
hide_things()
maze_completed = False
while not maze_completed:
	print(player.room.description)
	exits = ", ".join(player.room.exits.keys())
	print("From here you can move:", exits)
	command = input("Command: ")
	command_list = split_command(command)
	if len(command)==0:
		continue
	elif command in move_commands:
		player.move(command)
	elif command in quit_commands:
		break
	elif command.split()[0] == 'look':
		if command.find(" ") != -1:
			rest = command[command.find(" ")+1:]
			if rest.split()[0] == 'at':
				item_of_interest = rest[rest.find(" ")+1:]
				for room_item in player.room.objects:
					if item_of_interest == room_item.name:
						print(room_item.short_description,room_item.long_description)
		if len(player.room.objects):
			print("Here you can see:")
			for object in player.room.objects:
				print(object.short_description)
		else:
			print("You see nothing special here.")
	elif command.split()[0] in take_commands:
		item = command[command.find(" ")+1:]
		player.take(item)
	elif command.split()[0] in drop_commands:
		itemname = command[command.find(" ")+1:]
		player.drop(itemname)
	elif command in inventory_commands:
		player.show_inventory()
	elif command.split()[0] == 'open':
		if command.find(" ") != -1:
			item_of_interest = command[command.find(" ")+1:]
			target_found = False
			for object in player.room.objects:
				if item_of_interest == object.name:
					target_found = True
					new_room = object.open(player.room)
					player.room = new_room
					break
			if not target_found:
				print("I don't know what you want to open.")
	elif command.split()[0] == 'unlock':
		if command.find(" ") != -1:
			item_of_interest = command[command.find(" ")+1:]
			target_found = False
			for object in player.room.objects:
				if item_of_interest == object.name:
					target_found = True
					player.room = object.open(player.room)
					break
	else:
		print("Invalid command")
