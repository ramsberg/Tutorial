#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import boto3
import os,sys
import pprint
import cv2

from PIL import Image, ImageDraw, ImageFont

def capture_image():
	camera = cv2.VideoCapture(0)
	print("Press 'q' to snap picture.")
	cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
	cv2.moveWindow('frame', 20, 20)
	cv2.resizeWindow('frame', 640, 480)
	while(True):
		ret, frame = camera.read()
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

		cv2.imshow('frame', rgb)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			out = cv2.imwrite('capture.jpg', frame)
			break
	camera.release()
	cv2.destroyAllWindows()


def draw_box(image, person, rleft, rtop, rwidth, rheight):
	# Get a sketchable object of the image
	drawing = ImageDraw.Draw(image)

	# Translate bounding box fractions to real image coordinates
	image_size_x, image_size_y = image.size
	ileft = int(image_size_x * rleft)  # left
	itop = int(image_size_y * rtop)  # upper
	iright = int(ileft + image_size_x * rwidth)  # right == left + width
	ibottom = int(itop + image_size_y * rheight)  # bottom == upper + height
	# Draw lines for the box on the image
	drawing.line((ileft, itop) + (iright, itop), 'yellow', width=2)
	drawing.line((iright, itop) + (iright, ibottom), 'yellow', width=2)
	drawing.line((iright, ibottom) + (ileft, ibottom), 'yellow', width=2)
	drawing.line((ileft, ibottom) + (ileft, itop), 'yellow', width=2)
	font = ImageFont.truetype("/Users/oller/Downloads/SimpleCV-master/SimpleCV/fonts/ubuntu/ubuntu.ttf", 18)
	drawing.text((ileft, itop - 20), str(person), 'yellow', font=font)
	# Return the image
	return image


def main(argument="detect_faces"):
	capture_image()
	image_file_path = "capture.jpg"
	#  image_file_path = os.path.join("/Users/oller/Pictures/", sys.argv[1])
	with open(image_file_path, 'rb') as image_handle:
		image_b_bytes = image_handle.read()
	im = Image.open(image_file_path)

	client = boto3.client('rekognition', region_name='us-east-1')
	if argument == "faces":
		response = client.detect_faces(Image={'Bytes': image_b_bytes}, Attributes=['ALL'])

		print("I see {n_pers} persons.".format(n_pers=len(response['FaceDetails'])))
		person = 0
		for face in response['FaceDetails']:
			#  pprint.pprint(face)
			Top = face['BoundingBox']['Top']
			Left = face['BoundingBox']['Left']
			Height = face['BoundingBox']['Height']
			Width = face['BoundingBox']['Width']
			im = draw_box(im, person, Left, Top, Width, Height)
			msg = "Person {person} is a {gender} between {min_age} and {max_age} who is {emot}".format(person=person,
						gender=face['Gender']['Value'], emot=face['Emotions'][0]['Type'].lower(),
						min_age=face['AgeRange']['Low'], max_age=face['AgeRange']['High'])
			if face['Smile']['Value']:
				msg += " and is smiling."
			else:
				msg += " and isn't smiling."
			if face['Eyeglasses']['Value'] or face['Sunglasses']['Value']:
				msg += " The {gender} is wearing glasses".format(gender=face['Gender']['Value'].lower())
			else:
				msg += " The {gender} isn't wearing glasses".format(gender=face['Gender']['Value'].lower())
			if face['Mustache']['Value']:
				msg += " and has a mustache."
			else:
				msg += "."
			print(msg)
			person += 1
		im.show()
	elif argument == "celebs":
		response = client.recognize_celebrities(Image={'Bytes': image_b_bytes})
		#  pprint.pprint(response)
		print("Length list:",len(response['CelebrityFaces']))
		if len(response['CelebrityFaces']):
			person = 0
			print("I see {n_celebs} celebrities in the image.".format(n_celebs=len(response['CelebrityFaces'])))
			for celeb in response['CelebrityFaces']:
				face = celeb['Face']
				Top = face['BoundingBox']['Top']
				Left = face['BoundingBox']['Left']
				Height = face['BoundingBox']['Height']
				Width = face['BoundingBox']['Width']
				im = draw_box(im, celeb['Name'], Left, Top, Width, Height)
				print("Celeb {c_number}: {c_name}. {certanty}% sure.".format(c_number=person, c_name=celeb['Name'], certanty=celeb['MatchConfidence']))
				person += 1
		else:
			print("No celebrities found here. Move along!")
		if len(response['UnrecognizedFaces']):
			person = 0
			print("I see {n_unknown} unknown persons in the image.".format(n_unknown=len(response['UnrecognizedFaces'])))
			for unknown in response['UnrecognizedFaces']:
				Top = unknown['BoundingBox']['Top']
				Left = unknown['BoundingBox']['Left']
				Height = unknown['BoundingBox']['Height']
				Width = unknown['BoundingBox']['Width']
				im = draw_box(im, str(person), Left, Top, Width, Height)
				person += 1
		im.show()

if __name__ == "__main__":
	main(sys.argv[1])

