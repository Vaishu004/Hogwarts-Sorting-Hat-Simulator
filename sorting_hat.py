import cv2
import pyttsx3
from time import sleep
from PIL import Image
import numpy as np
import pygame

pygame.init()
pygame.mixer.init()

try :
    pygame.mixer.music.load('harry_potter_theme.mp3')
    pygame.mixer.music.play(-1)
except :
    print("Couldn't find music file. Continue without music !")

house_mapping = {
    'a' : 'Gryffindor',
    'b' : 'Hufflepuff',
    'c' : 'Ravenclaw',
    'd' : 'Slytherin'
}

def quiz() :
    print("Welcome to Hogwarts !! The Sorting Ceremony will begin soon !")

    answers = {
        'Q1': input("Q1: What quality do you value most? (a) Bravery (b) Loyalty (c) Intelligence (d) Ambition: "),
        'Q2': input("Q2: Which activity would you enjoy the most? (a) Exploring a forbidden forest (b) Helping a friend with a tough project (c) Solving a difficult puzzle (d) Leading a team to victory: "),
        'Q3': input("Q3: If you found a lost magical artifact, what would you do? (a) Study it to understand its power (b) Return it to its rightful owner (c) Use it to help others (d) Keep it hidden for personal use: "),
        'Q4': input("Q4: Choose a magical creature you feel connected to: (a) Phoenix (b) Badger (c) Eagle (d) Snake: "),
        'Q5': input("Q5: What would you do if you were insulted? (a) Stand up and defend yourself (b) Try to resolve it peacefully (c) Ignore it and prove yourself through success (d) Plan a clever comeback later: "),
        'Q6': input("Q6: Your favorite class at Hogwarts would be: (a) Defense Against the Dark Arts (b) Herbology (c) Charms (d) Potions: "),
        'Q7': input("Q7: Pick a motto: (a) 'Courage above all.' (b) 'Work hard, stay humble.' (c) 'Knowledge is power.' (d) 'Victory by any means.': "),
        'Q8': input("Q8: Which word describes you best? (a) Bold (b) Kind (c) Wise (d) Strategic: ")
    }
    return answers

def sort_house(answers) :
    house_scores = {'Gryffindor' : 0, 'Hufflepuff' : 0, 'Ravenclaw' : 0, 'Slytherin' : 0}

    for answer in answers.values() :
        house = house_mapping.get(answer.lower(), None)
        if house :
            house_scores[house] += 1

    sorted_house = max(house_scores, key=house_scores.get)
    return sorted_house

engine = pyttsx3.init()

def overlay_transparent(background, overlay, x, y):
    if overlay.shape[2] < 4:
        return background

    h, w = overlay.shape[:2]

    if y + h > background.shape[0] or x + w > background.shape[1]:
        return background  # Avoid out-of-bounds error

    overlay_img = overlay[:, :, :3]
    mask = overlay[:, :, 3:] / 255.0

    roi = background[y:y+h, x:x+w]
    blended = (1 - mask) * roi + mask * overlay_img
    background[y:y+h, x:x+w] = blended.astype(np.uint8)

    return background


def detect_face_and_sorting_hat(answers) :
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    hat_image = cv2.imread('sorting_hat_img.png', cv2.IMREAD_UNCHANGED)
    #hat_resized = cv2.resize(hat_image, (208,172))
    house_name = None 

    while True :
        ret, frame = cap.read()

        if not ret :
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

        for (x, y, w, h) in faces:
    
            hat_width = w
            hat_height = int(hat_image.shape[0] * (hat_width / hat_image.shape[1]))
            hat_resized = cv2.resize(hat_image, (hat_width, hat_height))

            y1 = max(0, y - hat_height)
            y2 = y
            x1 = x
            x2 = x + w

            hat_resized = hat_resized[(hat_resized.shape[0] - (y2 - y1)):, :]

            if y2 - y1 == hat_resized.shape[0] and x2 - x1 == hat_resized.shape[1]:
                frame = overlay_transparent(frame, hat_resized, x1, y1)


            break


        cv2.imshow('Sorting Hat Simulator', frame)

        if house_name :
            announce_house(house_name)
            break

        if cv2.waitKey(1) & 0xFF == ord('q') :
            house_name = sort_house(answers)

    cap.release()
    cv2.destroyAllWindows()

def announce_house(house_name) :
    print("Sorting Complete ! Welcome to !!", {house_name})
    engine.say(f"Sorting Complete ! Welcome to {house_name} !!")
    engine.runAndWait()

def main() :
    answers = quiz()
    house = sort_house(answers)

    print("Sorting you into {house}...")
    detect_face_and_sorting_hat(answers)
    sleep(3)

    #announce_house(house)

if __name__ == "__main__" :
    main()
    

