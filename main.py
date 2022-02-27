from struct import pack
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
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import filedialog
import face_recognition
from PreprocessingImage import *
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
            "times new roman", 15, "bold"), bd=3, relief=RIDGE, bg="#0094cf", fg="white")
        loginbtn.place(x=110, y=300, width=120, height=35)



    def login(self):
        try: 
            if self.txtuser.get() == "" or self.txtpass.get() == "":
                messagebox.showerror("Error", "Tài khoản và mật khẩu không được để trống!")
            else:
                con = conMana.getConnection()
                cur = con.cursor()
                sql = "select * from SEC_USER where upper(USERNAME)= upper(:userName) and PASS = :passWord and status = 'ACTIVE' "
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
        self.userLogin = user
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

        btnLogout = Button(title_lblLogout, text="Đăng xuất",image = photoimage,compound = LEFT, command=self.logout, cursor="hand2", font=("Tamaho", 11, "bold"),
                         fg="#0094cf")
        btnLogout.place(x=0, y=-2, width=150, height=50)

        photo_account = PhotoImage(file = r"Image/account.png")
        # Resizing image to fit on button
        photoimage_account = photo_account.subsample(3, 3)
        btn1_1 = Button(bg_img, text="Quản lý tài khoản", command=self.accountManage, cursor="hand2", image = photoimage_account,compound = TOP,font=("Tamaho", 20, "bold"),
                        bg="white", fg="#0094cf")
        btn1_1.place(x=100, y=100, width=300, height=150)

        photo_face_detect = PhotoImage(file = r"Image/icon_face_detect.png")
        # Resizing image to fit on button
        photoimage_detect = photo_face_detect.subsample(3, 3)

        btn2_2 = Button(bg_img, text="Nhận diện", cursor="hand2",command=self.face_data,image = photoimage_detect,compound = TOP, font=("Tamaho", 20, "bold"),
                        bg="white", fg="#0094cf")
        btn2_2.place(x=520, y=100, width=300, height=150)

        photo_staff = PhotoImage(file = r"Image/staff.png")
        # Resizing image to fit on button
        photoimage_staff = photo_staff.subsample(3, 3)
        btn3_3 = Button(bg_img, text="Quản lý nhân viên", cursor="hand2", command=self.staffManage,image = photoimage_staff,compound = TOP, font=("Tamaho", 20, "bold"),
                       bg="white", fg="#0094cf")
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

    def accountManage(self):
        self.new_window=Toplevel(self.root)
        self.app=Account_Manage(self.new_window,self.userLogin)
    
    def train_data(self):
        self.new_window=Toplevel(self.root)
        #self.app=Train(self.new_window)

    def face_data(self):
        self.new_window=Toplevel(self.root)
        self.app=FaceRecognitionClass(self.new_window,model,label_encoder)  

    def staffManage(self):
        self.new_window=Toplevel(self.root)
        self.app=Staff_Manage(self.new_window,self.userLogin)
    def logout(self):
        answer = messagebox.askyesno(title='Thông báo',
            message='Bạn có chắc chắn đăng xuất ?',parent=self.root)
        if answer:
            self.new_window=Toplevel(self.root)
            self.root.destroy()
            main()
# .................exit button
    def iexit(self):
        self.iexit=tkinter.messagebox.askyesno("Face Recognition","Are you sure you want to exit this project?",parent=self.root)
        if self.iexit>0:
            self.root.destroy()
        else:
            return

class Staff_Manage:
    state_form = 'DEFAULT'
    def __init__(self,root,user):
        self.userLogin = user[1]
        self.var_id=StringVar()
        self.var_fullName=StringVar()
        self.var_position=StringVar()
        self.var_gender=StringVar()
        self.var_idCard=StringVar()
        self.var_doi=StringVar()
        self.var_dop=StringVar()
        self.var_dob=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_status=StringVar()
        self.var_folderPath = StringVar()
        self.var_idSearch=StringVar()
        self.var_fullNameSearch=StringVar()
        self.var_positionSearch=StringVar()
        self.var_statusSearch=StringVar()
        self.root = root
        app_width = 1880
        app_height = 1000
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2) -30
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.root.resizable(False,False)
        self.root.title("Quản lý nhân viên")
        self.root.configure(background='#0094cf')
        frameMain = Frame(self.root, bg="#fff",highlightbackground="black",highlightthickness=1)
        frameMain.place(relx=0.006, rely=0.015, relwidth=0.984, relheight=0.88)
        frameHeader = Frame(frameMain, bg="#fff",highlightbackground="black",highlightthickness=1)
        frameHeader.place(relx=0, rely=0, relwidth=1, relheight=0.06)
        title_lbl=Label(frameHeader,text="Quản lý nhân viên",font=("Calibri",30,"bold"),bg="white",fg="#0094cf")
        title_lbl.place(x=0, y=0,relwidth=1,height=50)
        frame1 = LabelFrame(frameMain, bg="#fff",bd=2,relief=RIDGE,text="Thông tin nhân viên",font=("Calibri",14,"bold"))
        frame1.place(x=10, y=60, width=900,height=700)

        frame2 = LabelFrame(frameMain, bg="#fff",bd=2,relief=RIDGE,text="Danh sách nhân viên",font=("Calibri",14,"bold"))
        frame2.place(x=935, y=60, width=900,height=700)

        lblId = Label(frame1, text="Mã nhân viên : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblId.place(x=30, y=20)
        self.txtId = Entry(frame1,textvariable=self.var_id,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtId.place(x=160, y=20)
        self.txtId.configure(state='disabled')

        lblFullName = Label(frame1, text="Tên nhân viên : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblFullName.place(x=470, y=20)
        self.txtFullName = Entry(frame1,textvariable=self.var_fullName,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtFullName.place(x=600, y=20)
        self.txtFullName.configure(state='disabled')

        lblPosition = Label(frame1, text="Chức vụ : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblPosition.place(x=30, y=70)
        self.cboPosition = ttk.Combobox(frame1,textvariable=self.var_position,font=("Calibri",11,"bold"),state="readonly",width=32)
        self.cboPosition.place(x=160, y=70)
        self.cboPosition["values"]=("Giám đốc","Trưởng phòng","Nhân viên")
        self.cboPosition.current(0)
        self.cboPosition.configure(state='disabled')

        lblGender = Label(frame1, text="Giới tính : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblGender.place(x=470, y=70)
        self.cboGender = ttk.Combobox(frame1,textvariable=self.var_gender,font=("Calibri",11,"bold"),state="readonly",width=32)
        self.cboGender.place(x=600, y=70)
        self.cboGender["values"]=("Nam","Nữ")
        self.cboGender.current(0)
        self.cboGender.configure(state='disabled')

        lblCmnd = Label(frame1, text="Số CMND : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblCmnd.place(x=30, y=120)
        self.txtCmnd = Entry(frame1,textvariable=self.var_idCard,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtCmnd.place(x=160, y=120)
        self.txtCmnd.configure(state='disabled')

        lblDateOfIssue = Label(frame1, text="Ngày cấp : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblDateOfIssue.place(x=470, y=120)
        self.calDateOfIssue = DateEntry(frame1,textvariable=self.var_doi, width=37,locale='en_US', date_pattern='dd/mm/y',
         background='darkblue', foreground='white', borderwidth=2)
        self.calDateOfIssue.place(x=600, y=120)
        self.calDateOfIssue.configure(state='disabled')

        lblPlaceOfIssue = Label(frame1, text="Nơi cấp : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblPlaceOfIssue.place(x=30, y=170)
        self.txtPlaceOfIssue = Entry(frame1,textvariable=self.var_dop,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtPlaceOfIssue.place(x=160, y=170)
        self.txtPlaceOfIssue.configure(state='disabled')

        lblStatus = Label(frame1, text="Trạng thái : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblStatus.place(x=470, y=170)
        self.cboStatus = ttk.Combobox(frame1,textvariable=self.var_status,font=("Calibri",11,"bold"),state="readonly",width=32)
        self.cboStatus.place(x=600, y=170)
        self.cboStatus["values"]=("ACTIVE","INACTIVE")
        self.cboStatus.current(0)
        self.cboStatus.configure(state='disabled')

        lblDateOfBirth = Label(frame1, text="Ngày sinh : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblDateOfBirth.place(x=30, y=220)
        self.calDateOfBirth = DateEntry(frame1,textvariable=self.var_dob, width=37,locale='en_US', date_pattern='dd/mm/y',
         background='darkblue', foreground='white', borderwidth=2)
        self.calDateOfBirth.place(x=160, y=220)
        self.calDateOfBirth.configure(state='disabled')

        lblPhone = Label(frame1, text="Số điện thoại : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblPhone.place(x=470, y=220)
        self.txtPhone = Entry(frame1,textvariable=self.var_phone,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtPhone.place(x=600, y=220)
        self.txtPhone.configure(state='disabled')

        lblAddress = Label(frame1, text="Địa chỉ : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold '))
        lblAddress.place(x=30, y=270)
        self.txtAddress = Entry(frame1,textvariable=self.var_address,width=85 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtAddress.place(x=160, y=270)
        self.txtAddress.configure(state='disabled')

        lblFolderPath = Label(frame1, text="Thư mục ảnh : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold '))
        lblFolderPath.place(x=30, y=320)
        self.txtFolderPath = Entry(frame1,textvariable=self.var_folderPath,width=85 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtFolderPath.place(x=160, y=320)
        self.txtFolderPath.configure(state='disabled')

        table_frame=Frame(frame2,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=5,y=150,width=880,height=500)
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL) 
        self.staff_table=ttk.Treeview(table_frame,column=("staffId","fullName","gender","idCard","idIssuedDate","idIssuedPlace","birthDay",
        "address","phone","position","status"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.staff_table.xview)
        scroll_y.config(command=self.staff_table.yview)
        self.staff_table.heading("staffId",text="Mã nhân viên")
        self.staff_table.heading("fullName",text="Tên nhân viên")
        self.staff_table.heading("gender",text="Giới tính")
        self.staff_table.heading("idCard",text="Số CMND")
        self.staff_table.heading("idIssuedDate",text="Ngày cấp")
        self.staff_table.heading("idIssuedPlace",text="Nơi cấp")
        self.staff_table.heading("birthDay",text="Ngày sinh")
        self.staff_table.heading("address",text="Địa chỉ")
        self.staff_table.heading("phone",text="Số điện thoại")
        self.staff_table.heading("position",text="Chức vụ")
        self.staff_table.heading("status",text="Trạng thái")
        self.staff_table["show"]="headings"

        self.staff_table.column("staffId",width=100)
        self.staff_table.column("fullName",width=200)
        self.staff_table.column("gender",width=100)
        self.staff_table.column("idCard",width=100)
        self.staff_table.column("idIssuedDate",width=150)
        self.staff_table.column("idIssuedPlace",width=200)
        self.staff_table.column("birthDay",width=150)
        self.staff_table.column("address",width=300)
        self.staff_table.column("phone",width=100)
        self.staff_table.column("position",width=100)
        self.staff_table.column("status",width=100)
        self.staff_table.pack(fill=BOTH,expand=1)

        self.staff_table.bind("<ButtonRelease>",self.get_cursor)
        
        self.fetch_data()
        self.btnSave = Button(frame1, text="Lưu", command=self.saveData  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnReject = Button(frame1, text="Bỏ qua", command=self.reject  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnChooseFolder = Button(frame1, text="Browser", command=self.selectFolder  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnGetImage = Button(frame1, text="Chụp ảnh", command=self.getImage  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnTranning = Button(frame1, text="Tranning ảnh", command=self.tranningImage  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))


        self.btnAdd = Button(frame1, text="Thêm", command=self.add  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnAdd.place(x=230, y=370)
        self.btnUpdate = Button(frame1, text="Sửa", command=self.update  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnUpdate.place(x=380, y=370)
        self.btnDelete = Button(frame1, text="Xóa", command=self.delete  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnDelete.place(x=530, y=370)

        lblIdSearch = Label(frame2, text="Mã nhân viên : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblIdSearch.place(x=30, y=20)
        self.txtIdSearch = Entry(frame2,textvariable=self.var_idSearch,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtIdSearch.place(x=160, y=20)

        lblFullNameSearch = Label(frame2, text="Tên nhân viên : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblFullNameSearch.place(x=470, y=20)
        self.txtFullNameSearch = Entry(frame2,textvariable=self.var_fullNameSearch,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtFullNameSearch.place(x=600, y=20)

        lblPositionSearch = Label(frame2, text="Chức vụ : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblPositionSearch.place(x=30, y=70)
        self.cboPositionSearch = ttk.Combobox(frame2,textvariable=self.var_positionSearch,font=("Calibri",11,"bold"),state="readonly",width=32)
        self.cboPositionSearch.place(x=160, y=70)
        self.cboPositionSearch["values"]=("Tất cả","Giám đốc","Trưởng phòng","Nhân viên")
        self.cboPositionSearch.current(0)

        lblStatusSearch = Label(frame2, text="Trạng thái : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblStatusSearch.place(x=470, y=70)
        self.cboStatusSearch = ttk.Combobox(frame2,textvariable=self.var_statusSearch,font=("Calibri",11,"bold"),state="readonly",width=32)
        self.cboStatusSearch.place(x=600, y=70)
        self.cboStatusSearch["values"]=("Tất cả","ACTIVE","INACTIVE")
        self.cboStatusSearch.current(0)

        self.btnSearch = Button(frame2, text="Tìm kiếm", command=self.search  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnSearch.place(x=600, y=100)
    def fetch_data(self):
        try: 
            con = conMana.getConnection()
            cur = con.cursor()
            sql = "select * from STAFF where status <> 'DELETE' order by CREATE_DATE desc "
            cur.execute(sql )
            data = cur.fetchall()
            if len(data)!=0:
                self.staff_table.delete(*self.staff_table.get_children())
                for i in data:
                    self.staff_table.insert("",END,values=i)
        except cx_Oracle.DatabaseError as e: 
            print("There is a problem with Oracle", e)
        finally:
            if con: 
                con.close()
    def get_cursor(self,event=""):
        cursor_focus=self.staff_table.focus()
        content=self.staff_table.item(cursor_focus)
        data=content["values"]
        if(data != None):
            self.var_id.set(data[0]),
            self.var_fullName.set(data[1]),
            self.var_gender.set(data[2]),
            self.var_idCard.set(data[3]),
            self.var_doi.set(datetime.strptime(data[4][0:10], '%Y-%m-%d').strftime("%d/%m/%Y")),
            self.var_dop.set(data[5]),
            self.var_dob.set(datetime.strptime(data[6][0:10], '%Y-%m-%d').strftime("%d/%m/%Y")),
            self.var_address.set(data[7]),
            self.var_phone.set(data[8]),
            self.var_position.set(data[9]), 
            self.var_status.set(data[10])
            self.btnChooseFolder.place(x=230, y=420)
            self.btnGetImage.place(x=380, y=420)
            self.btnTranning.place(x=530, y=420)
        else :
            self.btnChooseFolder.place_forget()
            self.btnGetImage.place_forget()
            self.btnTranning.place_forget()
    def search(self):
        try: 
            con = conMana.getConnection()
            cur = con.cursor()
            sql = "select * from STAFF where   ( TRIM(:staffId) IS NULL   OR staff_id LIKE '%'  ||:staffId || '%' ) and ( TRIM(:fullName) IS NULL   OR upper(FULL_NAME) LIKE '%'  ||upper(:fullName) || '%' ) and (:position = 'Tất cả' or position = :position)  and (:status = 'Tất cả' or status = :status) order by CREATE_DATE desc "
            cur.execute(sql,staffId = self.var_idSearch.get(),fullName = self.var_fullNameSearch.get(),position = self.var_positionSearch.get(),status = self.var_statusSearch.get() )
            data = cur.fetchall()
            self.staff_table.delete(*self.staff_table.get_children())
            if len(data)!=0:
                for i in data:
                    self.staff_table.insert("",END,values=i)
        except cx_Oracle.DatabaseError as e: 
            print("There is a problem with Oracle", e)
        finally:
            if con: 
                con.close()
    def add(self):
        self.btnAdd.place_forget()
        self.btnUpdate.place_forget()
        self.btnDelete.place_forget()
        self.btnSave.place(x=300, y=370)
        self.btnReject.place(x=450, y=370)
        self.btnChooseFolder.place_forget()
        self.btnGetImage.place_forget()
        self.btnTranning.place_forget()
        self.stateField('normal','readonly')
        id = self.getNewId()
        self.txtId.configure(state='normal')
        self.txtId.delete(0,"end")
        self.txtId.insert(0,str(id))
        self.txtId.configure(state='disabled')
        global state_form
        state_form = 'ADD'
        self.clearData()
    def update(self):
        if(self.txtId.get() == None or self.txtId.get() == ''):
            messagebox.showerror("Thông báo","Bạn chưa chọn bản ghi nào!",parent=self.root)
            return
        self.btnAdd.place_forget()
        self.btnUpdate.place_forget()
        self.btnDelete.place_forget()
        self.btnSave.place(x=300, y=370)
        self.btnReject.place(x=450, y=370)
        self.btnChooseFolder.place_forget()
        self.btnGetImage.place_forget()
        self.btnTranning.place_forget()
        self.stateField('normal','readonly')
        global state_form
        state_form = 'UPDATE'
        self.txtFolderPath.configure(state='normal')
        self.txtFolderPath.delete(0,"end")
        self.txtFolderPath.insert(0,str(''))
        self.txtFolderPath.configure(state='disabled')
    def delete(self):
        if(self.txtId.get() == None or self.txtId.get() == ''):
            messagebox.showerror("Thông báo","Bạn chưa chọn bản ghi nào!",parent=self.root)
            return
        answer = messagebox.askyesno(title='Thông báo',
                    message='Bạn có chắc chắn muốn xóa nhân viên '+self.txtId.get() +' ?',parent=self.root)
        if answer:
            try: 
                con = conMana.getConnection()
                cur = con.cursor()
                sql = "UPDATE staff SET STATUS = 'DELETE',DELETE_DATE = sysdate,DELETE_USER = :deleteUser where STAFF_ID = :staffId "
                cur.execute(sql , staffId = int(self.var_id.get()),
                                    deleteUser=self.userLogin
                                    )
                con.commit()
                self.fetch_data()
                messagebox.showinfo("Thông báo","Xóa nhân viên "+self.var_id.get()+' thành công!',parent=self.root)
                self.resetForm()
                self.txtId.configure(state='normal')
                self.txtId.delete(0,"end")
                self.txtId.insert(0,str(''))
                self.txtId.configure(state='disabled')
                self.txtFullName.configure(state='normal')
                self.txtFullName.delete(0,"end")
                self.txtFullName.insert(0,str(''))
                self.txtFullName.configure(state='disabled')
                self.cboPosition.configure(state='normal')
                self.cboPosition.current(0)
                self.cboPosition.configure(state='disabled')
                self.cboGender.configure(state='normal')
                self.cboGender.current(0)
                self.cboGender.configure(state='disabled')
                self.txtCmnd.configure(state='normal')
                self.txtCmnd.delete(0,"end")
                self.txtCmnd.insert(0,str(''))
                self.txtCmnd.configure(state='disabled')
                self.txtPlaceOfIssue.configure(state='normal')
                self.txtPlaceOfIssue.delete(0,"end")
                self.txtPlaceOfIssue.insert(0,str(''))
                self.txtPlaceOfIssue.configure(state='disabled')
                self.cboStatus.configure(state='normal')
                self.cboStatus.current(0)
                self.cboStatus.configure(state='disabled')
                self.txtPhone.configure(state='normal')
                self.txtPhone.delete(0,"end")
                self.txtPhone.insert(0,str(''))
                self.txtPhone.configure(state='disabled')
                self.txtAddress.configure(state='normal')
                self.txtAddress.delete(0,"end")
                self.txtAddress.insert(0,str(''))
                self.txtAddress.configure(state='disabled')
                self.txtFolderPath.configure(state='normal')
                self.txtFolderPath.delete(0,"end")
                self.txtFolderPath.insert(0,str(''))
                self.txtFolderPath.configure(state='disabled')
            except cx_Oracle.DatabaseError as e: 
                messagebox.showerror("Thông báo","Đã lỗi: "+str(e),parent=self.root)
            finally:
                if con: 
                    con.close()
    def reject(self):
        self.btnSave.place_forget()
        self.btnReject.place_forget()
        self.btnAdd.place(x=230, y=370)
        self.btnUpdate.place(x=380, y=370)
        self.btnDelete.place(x=530, y=370)
        self.btnChooseFolder.place_forget()
        self.btnGetImage.place_forget()
        self.btnTranning.place_forget()
        self.clearData()
        self.stateField('disabled','disabled')
        global state_form
        state_form = 'DEFAULT'
    def resetForm(self):
        self.btnSave.place_forget()
        self.btnReject.place_forget()
        self.btnAdd.place(x=230, y=370)
        self.btnUpdate.place(x=380, y=370)
        self.btnDelete.place(x=530, y=370)
        self.btnChooseFolder.place_forget()
        self.btnGetImage.place_forget()
        self.btnTranning.place_forget()
        self.txtId.configure(state='normal')
        self.txtId.delete(0,"end")
        self.txtId.insert(0,str(''))
        self.txtId.configure(state='disabled')
        self.txtFullName.delete(0,"end")
        self.txtFullName.insert(0,str(''))
        self.cboPosition.current(0)
        self.cboGender.current(0)
        self.txtCmnd.delete(0,"end")
        self.txtCmnd.insert(0,str(''))
        self.txtPlaceOfIssue.delete(0,"end")
        self.txtPlaceOfIssue.insert(0,str(''))
        self.cboStatus.current(0)
        self.txtPhone.delete(0,"end")
        self.txtPhone.insert(0,str(''))
        self.txtAddress.delete(0,"end")
        self.txtAddress.insert(0,str(''))
        self.txtFolderPath.delete(0,"end")
        self.txtFolderPath.insert(0,str(''))
        self.stateField('disabled','disabled')
        global state_form
        state_form = 'DEFAULT'
    def stateField(self,status,statusCombobox):
        self.txtFullName.configure(state=status)
        self.cboPosition.configure(state=statusCombobox)
        self.cboGender.configure(state=statusCombobox)
        self.txtCmnd.configure(state=status)
        self.calDateOfIssue.configure(state=status)
        self.txtPlaceOfIssue.configure(state=status)
        self.cboStatus.configure(state=statusCombobox)
        self.calDateOfBirth.configure(state=status)
        self.txtPhone.configure(state=status)
        self.txtAddress.configure(state=status)
    def getNewId(self) :
        try: 
            con = conMana.getConnection()
            cur = con.cursor()
            sql = "select STAFF_SEQ.nextval from dual"
            cur.execute(sql )
            row = cur.fetchone()
        except cx_Oracle.DatabaseError as e: 
            print("There is a problem with Oracle", e)
        finally:
            if con: 
                con.close()
        return row[0]
    def clearData(self) :
        if(state_form != 'UPDATE'):
            self.txtId.configure(state='normal')
            self.txtId.delete(0,"end")
            self.txtId.insert(0,str(''))
            self.txtId.configure(state='disabled')
            self.txtFullName.delete(0,"end")
            self.txtFullName.insert(0,str(''))
            self.cboPosition.current(0)
            self.cboGender.current(0)
            self.txtCmnd.delete(0,"end")
            self.txtCmnd.insert(0,str(''))
            self.txtPlaceOfIssue.delete(0,"end")
            self.txtPlaceOfIssue.insert(0,str(''))
            self.cboStatus.current(0)
            self.txtPhone.delete(0,"end")
            self.txtPhone.insert(0,str(''))
            self.txtAddress.delete(0,"end")
            self.txtAddress.insert(0,str(''))
            self.txtFolderPath.delete(0,"end")
            self.txtFolderPath.insert(0,str(''))
    def saveData(self) :
        if(self.validForm() == 'FAILD'):
            return
        if(state_form == 'ADD'):
            try: 
                con = conMana.getConnection()
                cur = con.cursor()
                sql = "insert into staff(STAFF_ID,FULL_NAME,GENDER,ID_CARD,ID_ISSUED_DATE,ID_ISSUED_PLACE,BIRTHDAY,ADDRESS,PHONE,POSITION,STATUS,CREATE_DATE,CREATE_USER,UPDATE_DATE,UPDATE_USER,DELETE_DATE,DELETE_USER) values(:staffId,:fullName,:gender,:idCard,to_date(:doi,'dd/MM/yyyy'),:dop,to_date(:dob,'dd/MM/yyyy') ,:address,:phone,:position,:status,sysdate,:createUser,null,null,null,null)"
                cur.execute(sql , staffId = int(self.var_id.get()),
                                    fullName=self.var_fullName.get(),
                                    gender=self.var_gender.get(),
                                    idCard=self.var_idCard.get(),
                                    doi=self.var_doi.get(),
                                    dop=self.var_dop.get(),
                                    dob=self.var_dob.get(),
                                    address=self.var_address.get(),
                                    phone=self.var_phone.get(),
                                    position=self.var_position.get(),
                                    status=self.var_status.get(),
                                    createUser=self.userLogin
                                    )
                con.commit()
                self.fetch_data()
                messagebox.showinfo("Thông báo","Thêm nhân viên "+self.var_id.get()+' thành công!',parent=self.root)
                self.resetForm()
            except cx_Oracle.DatabaseError as e: 
                messagebox.showerror("Thông báo","Đã lỗi: "+str(e),parent=self.root)
            finally:
                if con: 
                    con.close()
        else :
            try: 
                con = conMana.getConnection()
                cur = con.cursor()
                sql = "UPDATE staff SET FULL_NAME =:fullName,GENDER = :gender,ID_CARD = :idCard,ID_ISSUED_DATE = to_date(:doi,'dd/MM/yyyy'),ID_ISSUED_PLACE = :dop,BIRTHDAY = to_date(:dob,'dd/MM/yyyy'),ADDRESS = :address,PHONE = :phone,POSITION = :position,STATUS = :status,UPDATE_DATE = sysdate,UPDATE_USER = :updateUser where STAFF_ID = :staffId "
                cur.execute(sql , staffId = int(self.var_id.get()),
                                    fullName=self.var_fullName.get(),
                                    gender=self.var_gender.get(),
                                    idCard=self.var_idCard.get(),
                                    doi=self.var_doi.get(),
                                    dop=self.var_dop.get(),
                                    dob=self.var_dob.get(),
                                    address=self.var_address.get(),
                                    phone=self.var_phone.get(),
                                    position=self.var_position.get(),
                                    status=self.var_status.get(),
                                    updateUser=self.userLogin
                                    )
                con.commit()
                self.fetch_data()
                messagebox.showinfo("Thông báo","Cập nhật nhân viên "+self.var_id.get()+' thành công!',parent=self.root)
                self.resetForm()
            except cx_Oracle.DatabaseError as e: 
                messagebox.showerror("Thông báo","Đã lỗi: "+str(e),parent=self.root)
            finally:
                if con: 
                    con.close()
            
    def validForm(self):
        if(self.var_fullName.get() == None or self.var_fullName.get() == ''):
            messagebox.showerror("Thông báo","Không được để trống họ tên nhân viên!",parent=self.root)
            return 'FAILD'
        if(self.var_idCard.get() == None or self.var_idCard.get() == ''):
            messagebox.showerror("Thông báo","Không được để trống số CMND nhân viên!",parent=self.root)
            return 'FAILD'
        if(self.var_dop.get() == None or self.var_dop.get() == ''):
            messagebox.showerror("Thông báo","Không được để trống nơi cấp nhân viên!",parent=self.root)
            return 'FAILD'
        if(self.var_phone.get() == None or self.var_phone.get() == ''):
            messagebox.showerror("Thông báo","Không được để trống số điện thoại nhân viên!",parent=self.root)
            return 'FAILD'
        if(self.var_address.get() == None or self.var_address.get() == ''):
            messagebox.showerror("Thông báo","Không được để trống địa chỉ nhân viên!",parent=self.root)
            return 'FAILD'
        return 'SUCCESS'
    def selectFolder(self):
        filename = filedialog.askdirectory(parent=self.root)
        self.var_folderPath.set(filename)
    def getImage(self):
        cap = cv2.VideoCapture(0)
        count = 0
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        print('Start Capture Image ........ - >>>')
        while True:  
            ret, frame = cap.read()
            face_locations = face_recognition.face_locations(frame)
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top-20), (right, bottom+5), (0,255,0), 2)
            if not os.path.exists('TrainingImage'+'_'+dt_string+'/'+self.var_id.get()+'-'+self.var_fullName.get()):
                    os.makedirs('TrainingImage'+'_'+dt_string+'/'+self.var_id.get()+'-'+self.var_fullName.get())
            count +=1
            if(len(face_locations) > 0):
                print('TrainingImage'+'_'+dt_string+'/'+self.var_id.get()+'-'+self.var_fullName.get()+'/'+self.var_id.get()+'_'+str(count) + '.jpg')
                cv2.imwrite('TrainingImage'+'_'+dt_string+'/'+self.var_id.get()+'-'+self.var_fullName.get()+'/'+self.var_id.get()+'_'+str(count) + '.jpg',frame[top-20:bottom+5, left:right])
            cv2.imshow('Image' ,frame)
            cv2.waitKey(1)
            if(count>200):
                self.txtFolderPath.configure(state='normal')
                self.txtFolderPath.delete(0,"end")
                self.txtFolderPath.insert(0,str('TrainingImage'+'_'+dt_string))
                self.txtFolderPath.configure(state='disabled')               
                break
        print('End Capture Image ........< --')
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Thông báo","Chụp ảnh nhân viên "+self.var_id.get()+' thành công!',parent=self.root)
    def tranningImage(self):
        if(self.var_folderPath.get() == None or self.var_folderPath.get() == ''):
            messagebox.showerror("Thông báo","Bạn chưa chọn thư mục để trainning!",parent=self.root)
        '''tiền xử lý dữ liệu rồi lưu thành 1 file npz để thuận tiện cho việc train và update model'''
        pre = PreprocessingFaceImg()
        #load folder train,thay ten model muon train
        link = self.var_folderPath.get()
        X_train, labels = pre.ManyFaceFeatures(link)
        X_train = X_train.T
        #update model
        x_train_new = []
        if os.path.isfile('image_train_success/image_train_success.npz'):
            print("Start Update model-->")
            data = np.load('image_train_success/image_train_success.npz')
            x_data, x_data_label = data['arr_0'], data['arr_1']
            np.concatenate((x_data, X_train))
            x_train_new = np.vstack((np.array(x_data), np.array(X_train)))
            x_label_new = np.append(x_data_label,labels)
            print("Update model success-->")
        else:
            x_train_new = X_train
            x_label_new = labels
        #luu model update
        np.savez_compressed('image_train_success/image_train_success.npz', x_train_new, x_label_new)
        global model
        global label_encoder
        print("Start--->")
        MAndP = ModelAndPrediction()
        label_encoder = LabelEncoder()
        data = np.load('image_train_success/image_train_success.npz')
        x_train, x_label = data['arr_0'], data['arr_1']
        x_label = label_encoder.fit_transform(x_label)
        model = MAndP.BuiltModel(x_train, x_label)
        print("Start End--->")
        messagebox.showinfo("Thông báo","Trainning ảnh nhân viên "+self.var_id.get()+' thành công!',parent=self.root)
        print("----> Train image success")
class Account_Manage:
    global state_form
    state_form = 'DEFAULT'
    def __init__(self,root,user):
        self.userLogin = user[1]
        self.var_userName = StringVar()
        self.var_fullName = StringVar()
        self.var_passWord = StringVar()
        self.var_rePassWord = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_position = StringVar()
        self.var_status = StringVar()

        self.var_userNameSearch=StringVar()
        self.var_fullNameSearch=StringVar()
        self.var_positionSearch=StringVar()
        self.var_statusSearch=StringVar()
        self.root = root
        app_width = 1880
        app_height = 1000
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2) -30
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.root.resizable(False,False)
        self.root.title("Quản lý tài khoản")
        self.root.configure(background='#0094cf')
        frameMain = Frame(self.root, bg="#fff",highlightbackground="black",highlightthickness=1)
        frameMain.place(relx=0.006, rely=0.015, relwidth=0.984, relheight=0.88)
        frameHeader = Frame(frameMain, bg="#fff",highlightbackground="black",highlightthickness=1)
        frameHeader.place(relx=0, rely=0, relwidth=1, relheight=0.06)
        title_lbl=Label(frameHeader,text="Quản lý tài khoản",font=("Calibri",30,"bold"),bg="white",fg="#0094cf")
        title_lbl.place(x=0, y=0,relwidth=1,height=50)
        frame1 = LabelFrame(frameMain, bg="#fff",bd=2,relief=RIDGE,text="Thông tin tài khoản",font=("Calibri",14,"bold"))
        frame1.place(x=10, y=60, width=900,height=700)

        frame2 = LabelFrame(frameMain, bg="#fff",bd=2,relief=RIDGE,text="Danh sách tài khoản",font=("Calibri",14,"bold"))
        frame2.place(x=935, y=60, width=900,height=700)

        lblId = Label(frame1, text="Tài khoản : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblId.place(x=30, y=20)
        self.txtUsername = Entry(frame1,textvariable=self.var_userName,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtUsername.place(x=160, y=20)
        self.txtUsername.configure(state='disabled')

        lblFullName = Label(frame1, text="Tên nhân viên : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblFullName.place(x=470, y=20)
        self.txtFullName = Entry(frame1,textvariable=self.var_fullName,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtFullName.place(x=600, y=20)
        self.txtFullName.configure(state='disabled')

        lblPassword = Label(frame1, text="Mật khẩu : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblPassword.place(x=30, y=70)
        self.txtPassword = Entry(frame1,show="*",textvariable=self.var_passWord,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtPassword.place(x=160, y=70)
        self.txtPassword.configure(state='disabled')

        lblRePassword = Label(frame1, text="Nhập lại mật khẩu : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblRePassword.place(x=470, y=70)
        self.txtRePassword = Entry(frame1,show="*",textvariable=self.var_rePassWord,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtRePassword.place(x=600, y=70)
        self.txtRePassword.configure(state='disabled')

        lblEmail= Label(frame1, text="Email : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblEmail.place(x=30, y=120)
        self.txtEmail = Entry(frame1,textvariable=self.var_email,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtEmail.place(x=160, y=120)
        self.txtEmail.configure(state='disabled')

        lblPhone= Label(frame1, text="Số điện thoại : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblPhone.place(x=470, y=120)
        self.txtPhone = Entry(frame1,textvariable=self.var_phone,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtPhone.place(x=600, y=120)
        self.txtPhone.configure(state='disabled')

        lblPosition= Label(frame1, text="Loại tài khoản : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblPosition.place(x=30, y=170)
        self.cboPosition = ttk.Combobox(frame1,textvariable=self.var_position,font=("Calibri",11,"bold"),state="readonly",width=32)
        self.cboPosition.place(x=160, y=170)
        self.cboPosition["values"]=("Quản trị","Nhân viên")
        self.cboPosition.current(0)
        self.cboPosition.configure(state='disabled')

        lblStatus = Label(frame1, text="Trạng thái : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblStatus.place(x=470, y=170)
        self.cboStatus = ttk.Combobox(frame1,textvariable=self.var_status,font=("Calibri",11,"bold"),state="readonly",width=32)
        self.cboStatus.place(x=600, y=170)
        self.cboStatus["values"]=("ACTIVE","INACTIVE")
        self.cboStatus.current(0)
        self.cboStatus.configure(state='disabled')

        table_frame=Frame(frame2,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=5,y=150,width=880,height=500)
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL) 
        self.account_table=ttk.Treeview(table_frame,column=("username","fullName","email","phone","position","status"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.account_table.xview)
        scroll_y.config(command=self.account_table.yview)
        self.account_table.heading("username",text="Tài khoản")
        self.account_table.heading("fullName",text="Tên nhân viên")
        self.account_table.heading("email",text="Email")
        self.account_table.heading("phone",text="Số điện thoại")
        self.account_table.heading("position",text="Loại tài khoản")
        self.account_table.heading("status",text="Trạng thái")
        self.account_table["show"]="headings"

        self.account_table.column("username",width=150)
        self.account_table.column("fullName",width=200)
        self.account_table.column("email",width=200)
        self.account_table.column("phone",width=100)
        self.account_table.column("position",width=130)
        self.account_table.column("status",width=100)
        self.account_table.pack(fill=BOTH,expand=1)

        self.account_table.bind("<ButtonRelease>",self.get_cursor)
        
        self.fetch_data()
        self.btnSave = Button(frame1, text="Lưu", command=self.saveData  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnReject = Button(frame1, text="Bỏ qua", command=self.reject  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))

        self.btnAdd = Button(frame1, text="Thêm", command=self.add  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnAdd.place(x=230, y=220)
        self.btnUpdate = Button(frame1, text="Sửa", command=self.update  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnUpdate.place(x=380, y=220)
        self.btnDelete = Button(frame1, text="Xóa", command=self.delete  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnDelete.place(x=530, y=220)

        lblUserNameSearch = Label(frame2, text="Tài khoản : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblUserNameSearch.place(x=30, y=20)
        self.txtUsermameSearch = Entry(frame2,textvariable=self.var_userNameSearch,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtUsermameSearch.place(x=160, y=20)

        lblFullNameSearch = Label(frame2, text="Tên tài khoản : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblFullNameSearch.place(x=470, y=20)
        self.txtFullNameSearch = Entry(frame2,textvariable=self.var_fullNameSearch,width=30 ,fg="black",font=('times', 11, ' bold '),borderwidth=2, relief="ridge")
        self.txtFullNameSearch.place(x=600, y=20)

        lblPositionSearch = Label(frame2, text="Loại tài khoản : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblPositionSearch.place(x=30, y=70)
        self.cboPositionSearch = ttk.Combobox(frame2,textvariable=self.var_positionSearch,font=("Calibri",11,"bold"),state="readonly",width=32)
        self.cboPositionSearch.place(x=160, y=70)
        self.cboPositionSearch["values"]=("Tất cả","Quản trị","Nhân viên")
        self.cboPositionSearch.current(0)

        lblStatusSearch = Label(frame2, text="Trạng thái : " ,fg="black", bg="#fff" ,font=('Calibri', 11, ' bold ') )
        lblStatusSearch.place(x=470, y=70)
        self.cboStatusSearch = ttk.Combobox(frame2,textvariable=self.var_statusSearch,font=("Calibri",11,"bold"),state="readonly",width=32)
        self.cboStatusSearch.place(x=600, y=70)
        self.cboStatusSearch["values"]=("Tất cả","ACTIVE","INACTIVE")
        self.cboStatusSearch.current(0)

        self.btnSearch = Button(frame2, text="Tìm kiếm", command=self.search  ,fg="#fff"  ,bg="#0094cf"  ,width=10  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.btnSearch.place(x=600, y=100)
    def fetch_data(self):
        try: 
            con = conMana.getConnection()
            cur = con.cursor()
            sql = "select USERNAME,FULLNAME,EMAIL,PHONE,POSITION,STATUS from SEC_USER where status <> 'DELETE' order by CREATE_TIME desc "
            cur.execute(sql )
            data = cur.fetchall()
            if len(data)!=0:
                self.account_table.delete(*self.account_table.get_children())
                for i in data:
                    self.account_table.insert("",END,values=i)
        except cx_Oracle.DatabaseError as e: 
            print("There is a problem with Oracle", e)
        finally:
            if con: 
                con.close()
    def get_cursor(self,event=""):
        cursor_focus=self.account_table.focus()
        content=self.account_table.item(cursor_focus)
        data=content["values"]
        if(data != None):
            self.var_userName.set(data[0]),
            self.var_fullName.set(data[1]),
            self.var_email.set(data[2]),
            self.var_phone.set(data[3]),
            self.var_position.set(data[4]),
            self.var_status.set(data[5]),
    def search(self):
        try: 
            con = conMana.getConnection()
            cur = con.cursor()
            sql = "select USERNAME,FULLNAME,EMAIL,PHONE,POSITION,STATUS from SEC_USER where   ( TRIM(:userName) IS NULL   OR upper(username) LIKE '%'  ||upper(:userName) || '%' ) and ( TRIM(:fullName) IS NULL   OR upper(FULLNAME) LIKE '%'  ||upper(:fullName) || '%' ) and (:position = 'Tất cả' or position = :position)  and (:status = 'Tất cả' or status = :status) order by CREATE_TIME desc "
            cur.execute(sql,userName = self.var_userNameSearch.get(),fullName = self.var_fullNameSearch.get(),position = self.var_positionSearch.get(),status = self.var_statusSearch.get() )
            data = cur.fetchall()
            self.account_table.delete(*self.account_table.get_children())
            if len(data)!=0:
                for i in data:
                    self.account_table.insert("",END,values=i)
        except cx_Oracle.DatabaseError as e: 
            print("There is a problem with Oracle", e)
        finally:
            if con: 
                con.close()
    def add(self):
        self.btnAdd.place_forget()
        self.btnUpdate.place_forget()
        self.btnDelete.place_forget()
        self.btnSave.place(x=300, y=220)
        self.btnReject.place(x=450, y=220)
        self.stateField('normal','readonly')
        global state_form
        state_form = 'ADD'
        self.clearData()
        self.txtUsername.configure(state='normal')
    def update(self):
        if(self.txtUsername.get() == None or self.txtUsername.get() == ''):
            messagebox.showerror("Thông báo","Bạn chưa chọn bản ghi nào!",parent=self.root)
            return
        self.btnAdd.place_forget()
        self.btnUpdate.place_forget()
        self.btnDelete.place_forget()
        self.btnSave.place(x=300, y=220)
        self.btnReject.place(x=450, y=220)
        self.stateField('normal','readonly')
        global state_form
        state_form = 'UPDATE'
    def delete(self):
        if(self.txtUsername.get() == None or self.txtUsername.get() == ''):
            messagebox.showerror("Thông báo","Bạn chưa chọn bản ghi nào!",parent=self.root)
            return
        answer = messagebox.askyesno(title='Thông báo',
                    message='Bạn có chắc chắn muốn xóa tài khoản '+self.txtUsername.get() +' ?',parent=self.root)
        if answer:
            try: 
                con = conMana.getConnection()
                cur = con.cursor()
                sql = "UPDATE SEC_USER SET STATUS = 'DELETE',DELETE_TIME = sysdate,DELETE_USER = :deleteUser where upper(username) = upper(:username) "
                cur.execute(sql , staffId = int(self.var_id.get()),
                                    deleteUser=self.userLogin
                                    )
                con.commit()
                self.fetch_data()
                messagebox.showinfo("Thông báo","Xóa tài khoản "+self.var_userName.get()+' thành công!',parent=self.root)
                self.resetForm()
                self.txtUsername.configure(state='normal')
                self.txtUsername.delete(0,"end")
                self.txtUsername.insert(0,str(''))
                self.txtUsername.configure(state='disabled')
                self.txtFullName.configure(state='normal')
                self.txtFullName.delete(0,"end")
                self.txtFullName.insert(0,str(''))
                self.txtFullName.configure(state='disabled')
                self.txtEmail.configure(state='normal')
                self.txtEmail.delete(0,"end")
                self.txtEmail.insert(0,str(''))
                self.txtEmail.configure(state='disabled')
                self.txtPhone.configure(state='normal')
                self.txtPhone.delete(0,"end")
                self.txtPhone.insert(0,str(''))
                self.txtPhone.configure(state='disabled')
                self.cboPosition.configure(state='normal')
                self.cboPosition.current(0)
                self.cboPosition.configure(state='disabled')
                self.cboStatus.configure(state='normal')
                self.cboStatus.current(0)
                self.cboStatus.configure(state='disabled')
            except cx_Oracle.DatabaseError as e: 
                messagebox.showerror("Thông báo","Đã lỗi: "+str(e),parent=self.root)
            finally:
                if con: 
                    con.close()
    def reject(self):
        self.btnSave.place_forget()
        self.btnReject.place_forget()
        self.btnAdd.place(x=230, y=220)
        self.btnUpdate.place(x=380, y=220)
        self.btnDelete.place(x=530, y=220)
        self.clearData()
        self.stateField('disabled','disabled')
        global state_form
        state_form = 'DEFAULT'
    def resetForm(self) :
        self.btnSave.place_forget()
        self.btnReject.place_forget()
        self.btnAdd.place(x=230, y=220)
        self.btnUpdate.place(x=380, y=220)
        self.btnDelete.place(x=530, y=220)
        self.txtUsername.configure(state='normal')
        self.txtUsername.delete(0,"end")
        self.txtUsername.insert(0,str(''))
        self.txtUsername.configure(state='disabled')
        self.txtFullName.delete(0,"end")
        self.txtFullName.insert(0,str(''))
        self.txtPassword.delete(0,"end")
        self.txtPassword.insert(0,str(''))
        self.txtRePassword.delete(0,"end")
        self.txtRePassword.insert(0,str(''))
        self.txtEmail.delete(0,"end")
        self.txtEmail.insert(0,str(''))
        self.txtPhone.delete(0,"end")
        self.txtPhone.insert(0,str(''))
        self.cboPosition.current(0)
        self.cboStatus.current(0)
        self.stateField('disabled','disabled')
        global state_form
        state_form = 'DEFAULT'
    def stateField(self,status,statusCombobox):
        if(state_form == 'ADD'):           
            self.txtUsername.configure(state='normal')
        else:
            self.txtUsername.configure(state='disabled')
        self.txtFullName.configure(state=status)
        self.txtPassword.configure(state=status)
        self.txtRePassword.configure(state=status)
        self.txtEmail.configure(state=status)
        self.txtPhone.configure(state=status)
        self.cboPosition.configure(state=statusCombobox)
        self.cboStatus.configure(state=statusCombobox)
    def clearData(self) :
        if(state_form !='UPDATE'):
            self.txtUsername.configure(state='normal')
            self.txtUsername.delete(0,"end")
            self.txtUsername.insert(0,str(''))
            self.txtUsername.configure(state='disabled')
            self.txtFullName.delete(0,"end")
            self.txtFullName.insert(0,str(''))
            self.txtPassword.delete(0,"end")
            self.txtPassword.insert(0,str(''))
            self.txtRePassword.delete(0,"end")
            self.txtRePassword.insert(0,str(''))
            self.txtEmail.delete(0,"end")
            self.txtEmail.insert(0,str(''))
            self.txtPhone.delete(0,"end")
            self.txtPhone.insert(0,str(''))
            self.cboPosition.current(0)
            self.cboStatus.current(0)
    def saveData(self) :
        if(self.validForm() == 'FAILD'):
            return
        if(state_form == 'ADD'):
            try: 
                con = conMana.getConnection()
                cur = con.cursor()
                sql = "insert into SEC_USER(USER_ID,USERNAME,FULLNAME,EMAIL,PASS,CREATE_TIME,LAST_LOGIN,PHONE,RETRY,STATUS,POSITION,CREATE_USER,UPDATE_USER,DELETE_TIME,DELETE_USER,UPDATE_TIME) values(SEC_USER_SEQ.nextval,:username,:fullName,:email,:password,sysdate,null,:phone,null,:status,:position,:createUser,null,null,null,null)"
                cur.execute(sql , username = self.var_userName.get(),
                                    fullName=self.var_fullName.get(),
                                    email=self.var_email.get(),
                                    password=str(hashlib.md5(self.var_passWord.get().encode('utf8')).hexdigest()),
                                    phone=self.var_phone.get(),
                                    status=self.var_status.get(),
                                    position=self.var_position.get(),
                                    createUser=self.userLogin
                                    )
                con.commit()
                self.fetch_data()
                messagebox.showinfo("Thông báo","Thêm tài khoản "+self.var_userName.get()+' thành công!',parent=self.root)
                self.resetForm()
            except cx_Oracle.DatabaseError as e: 
                messagebox.showerror("Thông báo","Đã lỗi: "+str(e),parent=self.root)
            finally:
                if con: 
                    con.close()
        else :
            try: 
                con = conMana.getConnection()
                cur = con.cursor()
                sql = "UPDATE SEC_USER SET FULLNAME =:fullName,EMAIL = :email,PHONE = :phone,POSITION = :position,STATUS = :status,UPDATE_TIME = sysdate,UPDATE_USER = :updateUser where upper(USERNAME) = upper(:username) "
                cur.execute(sql , username = self.var_userName.get(),
                                    fullName=self.var_fullName.get(),
                                    email=self.var_email.get(),
                                    phone=self.var_phone.get(),
                                    status=self.var_status.get(),
                                    position=self.var_position.get(),
                                    updateUser=self.userLogin
                                    )
                if(self.var_passWord.get() != None and self.var_passWord.get() != ''):
                    cur = con.cursor()
                    sql = "update SEC_USER set pass = :password where upper(USERNAME) = upper(:username)"
                    cur.execute(sql , username = self.var_userName.get(),
                                    password=str(hashlib.md5(self.var_passWord.get().encode('utf8')).hexdigest())
                                    )
                con.commit()
                self.fetch_data()
                messagebox.showinfo("Thông báo","Cập nhật tài khoản "+self.var_userName.get()+' thành công!',parent=self.root)
                self.resetForm()
            except cx_Oracle.DatabaseError as e: 
                messagebox.showerror("Thông báo","Đã lỗi: "+str(e),parent=self.root)
            finally:
                if con: 
                    con.close()
            
    def validForm(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(self.var_userName.get() == None or self.var_userName.get() == ''):
            messagebox.showerror("Thông báo","Không được để trống tài khoản!",parent=self.root)
            return 'FAILD'
        if(state_form == 'ADD'):
            if(self.validUserName() == 'FAILD'):
                messagebox.showerror("Thông báo","Tài khoản đã tồn tại!",parent=self.root)
                return 'FAILD'
        if(self.var_fullName.get() == None or self.var_fullName.get() == ''):
            messagebox.showerror("Thông báo","Không được để trống họ tên nhân viên!",parent=self.root)
            return 'FAILD'
        if(state_form == 'ADD'):
            if(self.var_passWord.get() == None or self.var_passWord.get() == ''):
                messagebox.showerror("Thông báo","Không được để trống mật khẩu!",parent=self.root)
                return 'FAILD'
            if(self.var_rePassWord.get() == None or self.var_rePassWord.get() == ''):
                messagebox.showerror("Thông báo","Mời nhập lại mật khẩu!",parent=self.root)
                return 'FAILD'
            if(self.var_rePassWord.get() != self.var_passWord.get()):
                messagebox.showerror("Thông báo","Mật khẩu bạn nhập lại không đúng!",parent=self.root)
                return 'FAILD'
        if(state_form == 'UPDATE'):
            if((self.var_passWord.get() == None or self.var_passWord.get() == '') and (self.var_rePassWord.get() != None and self.var_rePassWord.get() != '')):
                messagebox.showerror("Thông báo","Mời nhập lại mật khẩu!",parent=self.root)
                return 'FAILD'
            if((self.var_passWord.get() != None and self.var_passWord.get() != '') and (self.var_rePassWord.get() == None or self.var_rePassWord.get() == '')):
                messagebox.showerror("Thông báo","Không được để trống mật khẩu!",parent=self.root)
                return 'FAILD' 
            if((self.var_passWord.get() != None and self.var_passWord.get() != '') and (self.var_rePassWord.get() != None and self.var_rePassWord.get() != '')):
                if(self.var_rePassWord.get() != self.var_passWord.get()):
                    messagebox.showerror("Thông báo","Mật khẩu bạn nhập lại không đúng!",parent=self.root)
                    return 'FAILD'
        if(self.var_email.get() == None or self.var_email.get() == ''):
            messagebox.showerror("Thông báo","Không được để trống email!",parent=self.root)
            return 'FAILD'
        if(re.fullmatch(regex, self.var_email.get())):
            print("Valid Email")
        else:
            messagebox.showerror("Thông báo","Email không đúng định dạng!",parent=self.root)
            return 'FAILD'
        if(self.var_phone.get() == None or self.var_phone.get() == ''):
            messagebox.showerror("Thông báo","Không được để trống số điện thoại nhân viên!",parent=self.root)
            return 'FAILD'
        return 'SUCCESS'
    def validUserName(self):
        try: 
            con = conMana.getConnection()
            cur = con.cursor()
            sql = "select count(*) from sec_user where upper(username) = upper(:username) "
            cur.execute(sql ,username = self.var_userName.get())
            row = cur.fetchone()
            if(row[0] != 0):
                return 'FAILD'
        except cx_Oracle.DatabaseError as e: 
            print("There is a problem with Oracle", e)
        finally:
            if con: 
                con.close()
        return 'SUCCESS'
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
    print("Start End--->")
    main()
                