class Room:
	def __init__(self, room_name, description, exits):
		self.name = room_name
		self.description = description
		self.exits = exits
		self.objects = []

	def add_object(self,object):
		self.objects.append(object)

	def remove_object(self,object):
		if object in self.objects:
			self.objects.remove(object)
		else:
			print("You cannot see that here.")


class Object:
	def __init__(self,name,short_description,long_description,weight):
		self.name = name
		self.short_description = short_description
		self.long_description = long_description
		self.weight = weight
		self.objects = []

class Door:
	def __init__(self,name,short_description,long_description,weight):
		self.name = name
		self.short_description = short_description
		self.long_description = long_description
		self.weight = weight
		self.locked = True
		self.opening_items = []

	def open(self,room):
		if self.locked:
			print("It doesn't open, because it's locked.")
			return room

		else:
			print("The door opens")
			room.exits['out'] = 'goal_room'
			return room

	def lock(self,unlock_item):
		if not self.locked:
			if unlock_item in self.opening_items:
				print("You lock {} with {}.".format(self.short_description,unlock_item))
				self.locked = True
			else:
				print("The {} doesn't seem to fit in the lock.".format(unlock_item))
		else:
			print("It is already locked.")

	def unlock(self, unlock_item):
		if self.locked:
			if unlock_item in self.opening_items:
				print("You unlock {} with {}.".format(self.short_description, unlock_item))
				self.locked = False
			else:
				print("The {} doesn't seem to fit in the lock.".format(unlock_item))
		else:
			print("It isn't locked.")


# Define the world, room by room
world = {}
# room_name, description, exits
world['room1'] = Room(
    room_name="room1",
    description="You are in a corridor",
	exits={'N': 'room2'}
)
world['room2'] = Room(
    room_name='room2',
    description='You are at the north end of the corridor',
	exits={'S': 'room1','E':'room3'}
)
world['room3'] = Room(
    room_name='room3',
    description='',
	exits={'W': 'room2'}
)
world['goal_room'] = Room(
    room_name='goal_room',
    description='YAYYY, You made it!',
	exits={}
)


# Create the worlds objects
objects = {}
objects['sword1'] = Object(name='sword',
							short_description="a sword",
						   long_description ="a heavy sword with nice ornaments engraved on the blade.",
						   weight=2
							)

objects['box1'] = Object(name='box',
						 short_description='a small wooden box',
						 long_description='a wooden box that could be used to store nice things in.',
						 weight=1.0
						 )

objects['key1'] = Object(name='key',
						short_description='a golden key',
						long_description='A small key that seems to be made of gold. When looking on the key teeth, you can tell that this opens a very important door.',
						 weight=0.5
						 )

objects['key2'] = Object(name='blue key',
						short_description='a small blue key',
						long_description='a small key that seems to be used on a small lock.',
						 weight=0.5
						 )
objects['door1'] = Door(name='door',
						short_description='a wooden door.',
						long_description='This looks like the way out.',
						weight=20
						)

