
class RovarTranslator:
	def translate(self,text):
		konsonanter = "bcdfghjklmnpqrstvwxz"
		self.rovartext = ""
		for bokstav in text:
			if bokstav in konsonanter:
				output = bokstav + "o" + bokstav
			else:
				output = bokstav
			self.rovartext += output
		return(self.rovartext)

rt = RovarTranslator()

text = input("Text:")

kk = rt.translate(text)

print("Translated:",kk)


