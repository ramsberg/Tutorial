
konsonanter = "bcdfghjklmnpqrstvwxz"

text = input("Text:")

rovartext= ""

for bokstav in text:
	if bokstav in konsonanter:
		output = bokstav+"o"+bokstav
	else:
		output = bokstav
	rovartext += output

print(rovartext)
