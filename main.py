from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import re
import tkinter
from ConnectionManage import *
import hashlib
from PreprocessingImage import *
from ConnectionManage import *
from FaceRecognition import FaceRecognitionClass
conMana = ConnectionManage()

############################################# FUNCTIONS ################################################
def main():
    win = Tk()
    app = login_window(win)
    win.mainloop()
class login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập")
        app_width = 1100
        app_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)-100
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.root.resizable(False,False)
        self.bg = ImageTk.PhotoImage(file = r"Image\bgLogin.jpg")

        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, width=1100,height=700)

        frame = Frame(self.root, bg="White")
        frame.place(x=375, y=130, width=340, height=450)

        img1 = Image.open(r"Image\2.jpg")

        img1 = img1.resize((100, 100), Image.ANTIALIAS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lblimg1 = Label(image=self.photoimage1, bg="black", borderwidth=0)
        lblimg1.place(x=495, y=130, width=100, height=100)

        get_str = Label(frame, text="Đăng nhập", font=(
            "times new roman", 20, "bold"), bg="White", fg="#0094cf")
        get_str.place(x=100, y=100)

        # labels
        username_lbl = Label(frame, text="Tài khoản", font=(
            "times new roman", 15, "bold"), bg="White", fg="#0094cf")
        username_lbl.place(x=40, y=152)

        self.txtuser = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=40, y=180, width=270)

        password_lbl = Label(frame, text="Mật khẩu", font=(
            "times new roman", 15, "bold"), bg="White", fg="#0094cf")
        password_lbl.place(x=40, y=220)

        self.txtpass = ttk.Entry(frame, show="*",font=("times new roman", 15, "bold"))
        self.txtpass.place(x=40, y=250, width=270)
        # loginBuutton
        loginbtn = Button(frame, command=self.login, text="Đăng nhập", font=(
            "times new roman", 15, "bold"), bd=3, relief=RIDGE, bg="#ed1e23", fg="white")
        loginbtn.place(x=110, y=300, width=120, height=35)



    def login(self):
        try: 
            if self.txtuser.get() == "" or self.txtpass.get() == "":
                messagebox.showerror("Error", "Tài khoản và mật khẩu không được để trống!")
            else:
                con = conMana.getConnection()
                cur = con.cursor()
                sql = "select * from SEC_USER where upper(USERNAME)= upper(:userName) and PASS = :passWord and status = 1 "
                print(str(hashlib.md5(self.txtpass.get().encode('utf8')).hexdigest()))
                cur.execute(sql,userName =  self.txtuser.get(),passWord =str(hashlib.md5(self.txtpass.get().encode('utf8')).hexdigest()) )
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Tài khoản hoặc mật khẩu không đúng!")
                else:
                    self.new_window=Toplevel(self.root)
                    self.root.destroy()
                    self.app=Face_Recognition_System(row)

        except cx_Oracle.DatabaseError as e: 
            print("There is a problem with Oracle", e)
            messagebox.showerror("Error", e)
        finally:
            if con: 
                con.close()
class Face_Recognition_System:
    def __init__(self,user):
        winMain = Tk()
        self.root = winMain
        app_width = 1450
        app_height = 720
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)-100
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.root.resizable(False,False)
        self.root.title("Hệ thống chấm công")

        # second image

        img4 = Image.open(r"Image/bg.png")

        img4 = img4.resize((1450, 720), Image.ANTIALIAS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        bg_img = Label(self.root, image=self.photoimg4)
        bg_img.place(x=0, y=0, width=1450, height=720)

        title_lblEmpty = Label(bg_img, text="",
                          font=("Algerian", 30, "bold"), fg="#0094cf")
        title_lblEmpty.place(x=0, y=0, width=260, height=50)

        title_lbl = Label(bg_img, text="HỆ THỐNG CHẤM CÔNG",
                          font=("Algerian", 30, "bold"), fg="#0094cf")
        title_lbl.place(x=240, y=0, width=1000, height=50)

        title_lblUser = Label(bg_img, text="Username : "+user[1],
                          font=("Tamaho", 11, "bold"), fg="black")
        title_lblUser.place(x=1000, y=0, width=300, height=50)

        title_lblLogout = Label(bg_img, text="Username : "+user[1],
                          font=("Tamaho", 11, "bold"), fg="black")
        title_lblLogout.place(x=1300, y=0, width=150, height=50)   

        photo = PhotoImage(file = r"Image/icon-logout.png")
        # Resizing image to fit on button
        photoimage = photo.subsample(3, 3)

        btnLogout = Button(title_lblLogout, text="Đăng xuất",image = photoimage,compound = LEFT, command=self.student_details, cursor="hand2", font=("Tamaho", 11, "bold"),
                         fg="black")
        btnLogout.place(x=0, y=-2, width=150, height=50)
        btn1_1 = Button(bg_img, text="Student Details", command=self.student_details, cursor="hand2", font=("Algerian", 20, "bold"),
                        bg="darkblue", fg="white")
        btn1_1.place(x=100, y=100, width=300, height=150)

        photo_face_detect = PhotoImage(file = r"Image/icon_face_detect.png")
        # Resizing image to fit on button
        photoimage_detect = photo_face_detect.subsample(3, 3)

        btn2_2 = Button(bg_img, text="Nhận diện", cursor="hand2",command=self.face_data,image = photoimage_detect,compound = TOP, font=("Tamaho", 20, "bold"),
                        bg="white", fg="#0094cf")
        btn2_2.place(x=520, y=100, width=300, height=150)

        btn3_3 = Button(bg_img, text="Attendance", cursor="hand2", command=self.attendance_data, font=("Algerian", 20, "bold"),
                        bg="darkblue", fg="white")
        btn3_3.place(x=980, y=100, width=300, height=150)

        btn5_5 = Button(bg_img, text="Train Data", cursor="hand2",command=self.train_data, font=("Algerian", 20, "bold"),
                        bg="darkblue", fg="white")
        btn5_5.place(x=100, y=350, width=300, height=150)

        btn6_6 = Button(bg_img, text="Photos", cursor="hand2",command=self.open_img, font=("Algerian", 20, "bold"),
                        bg="darkblue", fg="white")
        btn6_6.place(x=520, y=350, width=300, height=150)

        btn8_8 = Button(bg_img, text="Exit",command=self.iexit,cursor="hand2", font=("Algerian", 20, "bold"),
                        bg="darkblue", fg="white")
        btn8_8.place(x=980, y=350, width=300, height=150)
        winMain.mainloop()

    def open_img(self):
        os.startfile("data")
    def command(self):
        print("hi")
    # =================================== Functions =========================================

    def student_details(self):
        self.new_window = Toplevel(self.root)
        #self.app = Student(self.new_window)
    
    def train_data(self):
        self.new_window=Toplevel(self.root)
        #self.app=Train(self.new_window)

    def face_data(self):
        self.new_window=Toplevel(self.root)
        self.app=FaceRecognitionClass(self.new_window,model,label_encoder)  

    def attendance_data(self):
        self.new_window=Toplevel(self.root)
        #self.app=Attendance(self.new_window)  

# .................exit button
    def iexit(self):
        self.iexit=tkinter.messagebox.askyesno("Face Recognition","Are you sure you want to exit this project?",parent=self.root)
        if self.iexit>0:
            self.root.destroy()
        else:
            return


if __name__ == "__main__":
    global model
    global label_encoder
    print("Start--->")
    MAndP = ModelAndPrediction()
    label_encoder = LabelEncoder()
    data = np.load('image_train_success/image_train_success.npz')
    x_train, x_label = data['arr_0'], data['arr_1']
    x_label = label_encoder.fit_transform(x_label)
    model = MAndP.BuiltModel(x_train, x_label)
    global key
    key = ''
    print("Start End--->")
    main()
                