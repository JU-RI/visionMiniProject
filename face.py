import requests
import argparse
import sys
import math
import random
from collections import Counter

API_URL = "https://kapi.kakao.com/v1/vision/face/detect"
MYAPP_KEY = "9668247f106b2c87b5121a0c57f40b4a"

def detect_face(filename):
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}
    try:
        files = {'file': open(filename, 'rb')}
        resp = requests.post(API_URL, headers=headers, files=files)
        # print(resp)  #접속 상태 확인
        resp.raise_for_status()
        return resp.json()  #이미지 분석 결과 json 받아오기
    except Exception as e:
        print(str(e))
        sys.exit(0)



if __name__ == '__main__':
    # 카카오에 접속해서 얼굴에 대한 정보 받아오기
    parser = argparse.ArgumentParser(description='Mosaic faces...')  #parser 생성
    parser.add_argument('image_file', type=str, nargs='?', default='./img/yy1.jpg', help='help...')
    args = parser.parse_args()
    result_json = detect_face(args.image_file)
    result = result_json['result']

    gen = result['faces'][0]['facial_attributes']['gender']
    age = math.trunc(result['faces'][0]['facial_attributes']['age'])  # 소수점 버림

    if gen['male'] > gen['female']:
        gender = "남"
    elif gen['male'] < gen['female']:
        gender = "여"

    corner_list = ['정육', '식품', '스낵', '가전제품']
    corner = random.choice(corner_list)
    print("gender:", gender, "age:", age, "corner:", corner)

    #DB에 저장

    corner_f1, corner_f2, corner_f3 = [], [], []
    corner_m1, corner_m2, corner_m3 = [], [], []

    #db에서 정보를 불러와서  / person_id로 추천
    #db불러오기
    person_corner = []  #id select문으로 corner값만 가져오기
    best = person.corner.most_common(1)
    print("당신은", best, "를 선호하시는 군요!")

    

    #db에서 정보를 불러와서  / 성별,연령으로 추천
    for x in corner:
        if age < 30:
            if gender == "여":
                corner_f1.append(x)
                cn = Counter(corner_f1)
            elif gender == "남":
                corner_m1.append(x)
                cn = Counter(corner_m1)
        elif 30 < age < 50:
            if gender == "여":
                corner_f2.append(x)
                cn = Counter(corner_f2)
            elif gender == "남":
                corner_m2.append(x)
                cn = Counter(corner_m2)
        elif age > 50:
            if gender == "여":
                corner_f3.append(x)
                cn = Counter(corner_f3)
            elif gender == "남":
                corner_m3.append(x)
                cn = Counter(corner_m3)

    print(cn)
    mode = cn.most_common(1)
    print(mode)
    best = mode[0][0]
    print("당신은", best, "를 선호하시는 군요!")

    meat_list = ['meat1.png', 'meat2.png', 'meat3.png']
    food_list = ['food1.png', 'food2.png', 'food3.png']
    snack_list = ['snack1.png', 'snack2.png', 'snack3.png']
    elec_list = ['elec1.png', 'elec2.png', 'elec3.png']

    if best == 'meat':
        for rec_img in meat_list:
            photo = PhotoImage(file=rec_img)
            label = Label(w, image=photo)
            label.pack()
    elif best == 'food'
        for rec_img in food_list:
            photo = PhotoImage(file=rec_img)
            label = Label(w, image=photo)
            label.pack()
    elif best == 'snack':
        for rec_img in snack_list:
            photo = PhotoImage(file=rec_img)
            label = Label(w, image=photo)
            label.pack()
    elif best == 'elec':
        for rec_img in elec_list:
            photo = PhotoImage(file=rec_img)
            label = Label(w, image=photo)
            label.pack()

    print("상품을 추천합니다.")
