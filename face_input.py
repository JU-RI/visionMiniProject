import requests
import argparse  #serialize와 같은 역할 // 이미지를 원하는 파라미터 형태로
import sys
import math
import random
from kakao import searchdb
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog




photolabel = None
info_label = None
gender = None
age = None
corner = None
root = None

API_URL = "https://kapi.kakao.com/v1/vision/face/detect"  #상수 -> 대문자로 씀(값을 바꾸지 않을 것이라는 뜻)
MYAPP_KEY = "b0ae685600b37988ffc8c4f7e1b4c8d2"  #REST API 키


def file_open():# 파일을 열어서 분석하는 버튼
    global filelabel, photolabel, gender, age, corner
    try:
        filename = filedialog.askopenfilename(initialdir="C:/Users/Darkvalui/Pictures", title="choose your file",

                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        img = Image.open(filename)
        resized1 = img.resize((650, 400))
        photo1 = ImageTk.PhotoImage(resized1)
        photolabel.photo1 = photo1
        photolabel.configure(image=photo1)

        parser = argparse.ArgumentParser(description='Mosaic faces...')  # parser 생성

        parser.add_argument('image_file', type=str, nargs='?', default= filename, help='help...')

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

    except:
        pass

def db_btn():
    global gender, age, corner, root
    searchdb.sqlinsert(gender,str(age),corner)

def like_btn():
    global info_label
    searchdb.sqlselect()
    info_label.configure(text=searchdb.record[0])

def detect_face(filename):
    headers = {'Authorization':'KakaoAK {}'.format(MYAPP_KEY)}  #원하는 형태로 바꿔 줌 / MYAPP_KEY가 {}안에 들어감

    #1. 카카오 접속
    try:  #네트워크 연결할 때는 예외처리 해줘야 함
        files = {'file':open(filename, 'rb')}  #원하는 형태로 바꿔줌 // 파일을 open해서 서버로 전송 // rb는 이미지
        resp = requests.post(API_URL, headers=headers, files=files)

        #2. 접속 상태 확인
        print(resp)  #서버랑 연결이 잘 됐을 때 응답코드: [200]
        print("kakao 접속 성공")
        resp.raise_for_status()  #응답코드가 200이 아닐 경우 에러 발동

        # 3. 이미지 분석 결과 json 받아오기
        return resp.json()  #결과를 json으로 받아오기

    except Exception as e:
        print(str(e))
        print(type(e))  #예외 타입 출력
        sys.exit(0)  #에러 발생하면 종료


def main_ui():
    global photolabel , root

    root = tk.Tk()
    root.geometry("1450x600")
    root.resizable("false","false")
    root.configure(bg="white")

    file = "./img/title.jpg"
    image = Image.open(file)
    resized = image.resize((650, 400))
    photo = ImageTk.PhotoImage(resized)

    photolabel = tk.Label(root, image=photo)

    file2 = "./img/like.png"
    image2 = Image.open(file2)
    resized2 = image2.resize((650, 400))
    photo2 = ImageTk.PhotoImage(resized2)

    photolabel2 = tk.Label(root, image=photo2)


    info_label = tk.Label(root, text="테스트")


    open_btn = tk.Button(root, text="사진파일 불러오기" ,command=file_open)
    btn = tk.Button(root, text="사진 DB에 등록", command=db_btn)
    btn2 = tk.Button(root, text="상품추천버튼", command=like_btn)


    open_btn.place(x=345, y=470)
    btn.place(x=350,y=500)
    btn2.place(x=1020,y=500)
    photolabel.place(x=75,y=50)
    photolabel2.place(x=735 ,y=50)
    info_label.place(x=1040,y=470)
    root.mainloop()


if __name__ == '__main__':
    main_ui()
