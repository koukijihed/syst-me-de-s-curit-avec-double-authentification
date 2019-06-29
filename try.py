  import face_recognition  
	import cv2  
	import numpy as np  
	import time  
	import pickle  
	import sys  
	import os  
	from gpiozero import LED  
	green = LED(21)  
	red = LED(16)  
	yellow = LED(20)  
	i= 0  
	name = ''  
	import yagmail  
	yag = yagmail.SMTP("willsmithplaysfootball@gmail.com","2019ocvmagic")  
	contents = ['Hello ',  
	            'You can find a file attached.', name+'image.jpg']  
	from mfrc522 import SimpleMFRC522  
	reader = SimpleMFRC522()  
	video_capture = cv2.VideoCapture(0)  
	timefirst = time.time()  
  with open('faces.pkl', 'rb') as f:  
	    Anouar_face_encoding, Souhail_face_encoding, Jihed_face_encoding, known_face_encodings, known_face_names= pickle.load(f)  
	      
	face_locations = []  
	face_encodings = []  
	face_names = []  
	process_this_frame = True  
	timeexcuted = time.time() - timefirst  
	print(timeexcuted)  
	  
	while True:  
	    ret, frame = video_capture.read()  
	  
	    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  
	  
	    rgb_small_frame = small_frame[:, :, ::-1]  
	  
	    if process_this_frame:  
	        face_locations = face_recognition.face_locations(rgb_small_frame)  
	        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)  
	  
	        face_names = []  
	        for face_encoding in face_encodings:  
	            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)  
              name = "Unknown"  
	            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)  
	            best_match_index = np.argmin(face_distances)  
	            if matches[best_match_index]:  
	                name = known_face_names[best_match_index]  
	            face_names.append(name)  
	    process_this_frame = not process_this_frame  
	  
	    for (top, right, bottom, left), name in zip(face_locations, face_names):  
	        top *= 4  
	        right *= 4  
	        bottom *= 4  
	        left *= 4  
	        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  
	        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)  
	        font = cv2.FONT_HERSHEY_DUPLEX  
	        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)  
	    cv2.imshow('Video', frame)  
	    yellow.on()  
	    if name !="Unknown" and name != "":  
	        id, text = reader.read()  
	        print(name)  
	        if name == text[0:len(name)]:  
	            yellow.off()  
	            red.off()  
	            green.on()  
	            output = open('./log/log_'+name+'.txt','a+')  
	            output.write(name+"*"+time.strftime("%b/%d/%Y")+"*"+time.strftime("%H:%M:%S")+"\n")  
	            print(name+" accessed "+time.strftime("%b/%d/%Y || %H:%M:%S"))  
	            name=""  
	            output.close()  
	            time.sleep(2)  
	            green.off()  
	    elif name == "Unknown":  
	        red.on()  
	        green.off()  
	        yellow.off()  
	    else:  
	        yellow.off()  
	        green.off()  
	        red.off()  
	  
	    if cv2.waitKey(1) & 0xFF == ord('q'):  
	        break  
	video_capture.release()  
	cv2.destroyAllWindows()
