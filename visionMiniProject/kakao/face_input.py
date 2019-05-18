import requests
import argparse
import sys
import math
import random
from collections import Counter
import searchdb
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox

photolabel, photolabel2, info_label = None, None, None
gender, age, corner = None, None, None
root = None

API_URL = "https://kapi.kakao.com/v1/vision/face/detect"  #상수 -> 대문자로 씀(값을 바꾸지 않을 것이라는 뜻)
MYAPP_KEY = "9668247f106b2c87b5121a0c57f40b4a"  #REST API 키

def file_open():# 파일을 열어서 분석하는 버튼
    global filelabel, photolabel, gender, age, corner
    filename = filedialog.askopenfilename(initialdir="C:/Users/Darkvalui/Pictures", title="choose your file",
                                          filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    img = Image.open(filename)
    resized1 = img.resize((600, 400))
    photo1 = ImageTk.PhotoImage(resized1)
    photolabel.photo1 = photo1
    photolabel.configure(image=photo1)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('image_file', type=str, nargs='?', default=filename, help='help...')
    args = parser.parse_args()
    result_json = detect_face(args.image_file)
    result = result_json['result']

    if 'faces' not in result:
        tk.messagebox.showerror("오류", "얼굴을 인식하지 못했습니다.\n다른 사진을 선택해 주세요.")
    else:
        gen = result['faces'][0]['facial_attributes']['gender']
        age = math.trunc(result['faces'][0]['facial_attributes']['age'])  # 소수점 버림

    if gen['male'] > gen['female']: gender = "남"
    elif gen['male'] < gen['female']: gender = "여"

    corner_list = ['정육', '식품', '스낵', '가전제품']
    corner = random.choice(corner_list)
    print("gender:", gender, "age:", age, "corner:", corner)

    tk.messagebox.showinfo("사진 등록 완료", "분석결과를 확인하세요.")
    result_label = tk.Label(root, text="분석결과 성별은 '" + str(gender) + "', 나이는 '" + str(age) + "' 세 입니다.",
                            font=("맑은 고딕", 35), fg="blue", bg="white")
    result_label.place(x=200, y=25)


def db_btn():
    global gender, age, corner, root
    searchdb.sqlinsert(gender, str(age), corner)
    tk.messagebox.showinfo("등록 완료", "분석결과가 DB에 등록되었습니다.")


def like_btn():  #성별, 연령으로 상품추천
    global info_label, photolabel2, best
    search_result = searchdb.sqlselect()

    corner_f1, corner_f2, corner_f3 = [], [], []
    corner_m1, corner_m2, corner_m3 = [], [], []
    for x in range(0, len(search_result)):
        if search_result[x][1] < 30:
            if search_result[x][0] == "여":
                corner_f1.append(search_result[x][2])
                cn = Counter(corner_f1)
                label_text = str("10~20대 여성이 선호하는")
            elif search_result[x][0] == "남":
                corner_m1.append(search_result[x][2])
                cn = Counter(corner_m1)
                label_text = str("10~20대 남성이 선호하는")
        elif 30 < search_result[x][1] < 50:
            if search_result[x][0] == "여":
                corner_f2.append(search_result[x][2])
                cn = Counter(corner_f2)
                label_text = str("30~40대 여성이 선호하는")
            elif search_result[x][0] == "남":
                corner_m2.append(search_result[x][2])
                cn = Counter(corner_m2)
                label_text = str("30~40대 남성이 선호하는")
        elif search_result[x][1] > 50:
            if search_result[x][0] == "여":
                corner_f3.append(search_result[x][2])
                cn = Counter(corner_f3)
                label_text = str("50대 이상 여성이 선호하는")
            elif search_result[x][0] == "남":
                corner_m3.append(search_result[x][2])
                cn = Counter(corner_m3)
                label_text = str("50대 이상 남성이 선호하는")

    mode = cn.most_common(1)
    best = mode[0][0]
    result_label = tk.Label(root, text=label_text + " " + best + "코너 상품을 추천합니다.",
                            font=("맑은 고딕", 30), fg="orange", bg="white", width=50)
    result_label.place(x=100, y=26)
    best_show()


def best_show():
    global info_label, photolabel2, best
    meat_list = ['./img/meat1.png', './img/meat2.png', './img/meat3.png']
    food_list = ['./img/food1.png', './img/food2.png', './img/food3.png']
    snack_list = ['./img/snack1.png', './img/snack2.png', './img/snack3.png']
    elec_list = ['./img/elec1.png', './img/elec2.png', './img/elec3.png']

    if best == '정육':
        img = Image.open(random.choice(meat_list))
        resized1 = img.resize((600, 400))
        photo1 = ImageTk.PhotoImage(resized1)
        photolabel2.photo1 = photo1
        photolabel2.configure(image=photo1)
        # info_label.configure(text="성별은:"+best[0]+"   나이는"+str(best[1])+"이시고   "+best[2]+ "코너를 좋아하시는군요 이 상품을 추천합니다")
    elif best == '식품':
        img = Image.open(random.choice(food_list))
        resized1 = img.resize((600, 400))
        photo1 = ImageTk.PhotoImage(resized1)
        photolabel2.photo1 = photo1
        photolabel2.configure(image=photo1)
        # info_label.configure(text="성별은:"+best[0]+"   나이는"+str(best[1])+"이시고   "+best[2]+ "코너를 좋아하시는군요 이 상품을 추천합니다")
    elif best == '스낵':
        img = Image.open(random.choice(snack_list))
        resized1 = img.resize((600, 400))
        photo1 = ImageTk.PhotoImage(resized1)
        photolabel2.photo1 = photo1
        photolabel2.configure(image=photo1)
        # info_label.configure(text="성별은:"+best[0]+"   나이는"+str(best[1])+"이시고   "+best[2]+ "코너를 좋아하시는군요 이 상품을 추천합니다")
    elif best == '가전제품':
        img = Image.open(random.choice(elec_list))
        resized1 = img.resize((600, 400))
        photo1 = ImageTk.PhotoImage(resized1)
        photolabel2.photo1 = photo1
        photolabel2.configure(image=photo1)
        # info_label.configure(text="성별은:"+best[0]+"   나이는"+str(best[1])+"이시고   "+best[2]+ "코너를 좋아하시는군요 이 상품을 추천합니다")


def detect_face(filename):
    headers = {'Authorization':'KakaoAK {}'.format(MYAPP_KEY)}  #원하는 형태로 바꿔 줌 / MYAPP_KEY가 {}안에 들어감

    #1. 카카오 접속
    try:  #네트워크 연결할 때는 예외처리 해줘야 함
        files = {'file':open(filename, 'rb')}  #원하는 형태로 바꿔줌 // 파일을 open해서 서버로 전송 // rb는 이미지
        resp = requests.post(API_URL, headers=headers, files=files)
        return resp.json()  #결과를 json으로 받아오기
    except Exception as e:
        print(str(e))
        print(type(e))  #예외 타입 출력
        sys.exit(0)  #에러 발생하면 종료


def main_ui():
    global photolabel, photolabel2, root, info_label
    root = tk.Tk()
    root.geometry("1300x650+100+50")
    root.title("상품추천시스템")
    root.resizable("false", "false")
    root.configure(bg="white")

    file = "./img/title.jpg"
    image = Image.open(file)
    resized = image.resize((600, 400))
    photo = ImageTk.PhotoImage(resized)
    photolabel = tk.Label(root, image=photo)

    file2 = "./img/like.png"
    image2 = Image.open(file2)
    resized2 = image2.resize((600, 400))
    photo2 = ImageTk.PhotoImage(resized2)
    photolabel2 = tk.Label(root, image=photo2)

    open_btn = tk.Button(root, text="사진파일 불러오기", font=("배달의민족 도현", 20), command=file_open, bg="#efc140")
    btn = tk.Button(root, text="분석결과 DB에 등록", font=("배달의민족 도현", 20), command=db_btn, bg="#efc140")
    btn2 = tk.Button(root, text="상품추천버튼", font=("배달의민족 도현", 20), command=like_btn, bg="#efc140")

    open_btn.place(x=210, y=523)
    btn.place(x=200, y=578)
    btn2.place(x=870, y=540)
    photolabel.place(x=35, y=110)
    photolabel2.place(x=660, y=110)
    root.mainloop()


if __name__ == '__main__':
    main_ui()
