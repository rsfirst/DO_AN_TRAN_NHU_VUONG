############################################# IMPORTING ################################################
from pickle import FALSE, TRUE
import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
from matplotlib.pyplot import text
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
from datetime import datetime
import time
from PreprocessingImage import *
from ConnectionManage import *
from Model.Staff import *
import traceback
conMana = ConnectionManage()
pre = PreprocessingFaceImg()
ds_factor = 1
###########################################################################################
class FaceRecognitionClass:
    def __init__(self,root,modelValue,label_encoderValue):
        global model
        global label_encoder
        model = modelValue
        label_encoder = label_encoderValue
        self.root=root
        app_width = 1880
        app_height = 1000
        global isCloseCamera
        isCloseCamera = 'OPEN'
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2) -30
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.root.resizable(False,False)
        self.root.title("Hệ thống chấm công")
        ######################################## GUI FRONT-END ###########################################
        self.root.configure(background='#0094cf')
        self.frameMain = tk.Frame(self.root, bg="#fff",highlightbackground="black",highlightthickness=1)
        self.frameMain.place(relx=0.006, rely=0.015, relwidth=0.984, relheight=0.88)
        self.frameHeader = tk.Frame(self.frameMain, bg="#fff",highlightbackground="black",highlightthickness=1)
        self.frameHeader.place(relx=0, rely=0, relwidth=1, relheight=0.06)
        self.title_lbl=tk.Label(self.frameHeader,text="Hệ thống chấm công",font=("Calibri",30,"bold"),bg="white",fg="#0094cf")
        self.title_lbl.place(x=0, y=0,relwidth=1,height=50)
        self.frame1 = tk.LabelFrame(self.frameMain, bg="#fff",bd=2,relief=tk.RIDGE,text="Màn hình nhận diện",font=("Calibri",14,"bold"))
        self.frame1.place(relx=0.15, rely=0.065, relwidth=0.354, relheight=0.7)

        self.frame2 = tk.LabelFrame(self.frameMain, bg="#fff",bd=2,relief=tk.RIDGE,text="Chấm công thành công",font=("Calibri",14,"bold"))
        self.frame2.place(relx=0.55, rely=0.065, relwidth=0.28, relheight=0.7)

        self.img_unknow=Image.open(r"Image\unkownImage.jpg")
        self.img_unknow = self.img_unknow.resize((217, 217),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(self.img_unknow)
        self.imageCapture =  tk.Label(self.frame2,bg="#efefef",borderwidth=2, relief="ridge",image=self.photoimg)
        self.imageCapture.grid(row=0, column=0)
        self.imageCapture.place(x=160, y=10,width=217,height=217)
        self.lbl = tk.Label(self.frame2, text="Mã nhân viên : " ,fg="black", bg="#fff" ,font=('Calibri', 14, ' bold ') )
        self.lbl.place(x=30, y=270)
        self.txt = tk.Entry(self.frame2,width=32 ,fg="black",font=('times', 14, ' bold '),borderwidth=2, relief="ridge")
        self.txt.place(x=160, y=270)
        #txt.config(state='disabled')

        self.lbl2 = tk.Label(self.frame2, text="Tên nhân viên : ",fg="black", bg="#fff" ,font=('Calibri', 14, ' bold ') )
        self.lbl2.place(x=30, y=310)
        self.txt2 = tk.Entry(self.frame2,width=32 ,fg="black",font=('times', 14, ' bold '),borderwidth=2, relief="ridge")
        self.txt2.place(x=160, y=310)
        #txt2.config(state='disabled')

        self.lbl3 = tk.Label(self.frame2, text="Thời gian : ",fg="black", bg="#fff" ,font=('Calibri', 14, ' bold ') )
        self.lbl3.place(x=30, y=350)
        self.txt3 = tk.Entry(self.frame2,width=32 ,fg="black",font=('times', 14, ' bold '),borderwidth=2, relief="ridge")
        self.txt3.place(x=160, y=350)
        #txt3.config(state='disabled')

        self.lbl4 = tk.Label(self.frame2, text="Chức vụ : ",fg="black", bg="#fff" ,font=('Calibri', 14, ' bold ') )
        self.lbl4.place(x=30, y=390)
        self.txt4 = tk.Entry(self.frame2,width=32 ,fg="black",font=('times', 14, ' bold '),borderwidth=2, relief="ridge")
        self.txt4.place(x=160, y=390)
        #txt4.config(state='disabled')

        self.labelOption =  tk.Label(self.frame1,bg="#fff",borderwidth=2, relief="ridge")
        self.labelOption.grid(row=0, column=0)
        self.labelOption.place(x=10, y=10,relwidth=0.97,height=50)

        self.labelChamCong =  tk.Label(self.labelOption, text="Chọn loại Chấm công : ",fg="black", bg="#fff" ,font=('Calibri', 14, ' bold ') )
        self.labelChamCong.grid(row=0, column=0)
        self.labelChamCong.place(x=10, y=5,width=200,height=40)
        self.type_combo=ttk.Combobox(self.labelOption,font=("Calibri",13,"bold"),state="readonly",width=18)
        self.type_combo["values"]=("Vào","Ra")
        self.type_combo.current(0)
        self.type_combo.grid(row=0,column=1,padx=2,pady=10,sticky=tk.W)
        self.type_combo.place(x=205, y=10,width=200,height=30)
        self.video =  tk.Label(self.frame1,bg="#efefef",borderwidth=2, relief="ridge")
        self.video.grid(row=0, column=0)
        self.video.place(x=10, y=80,relwidth=0.97,relheight=0.76)


        ###################### BUTTONS ##################################

        self.openCameraBtn = tk.Button(self.frameMain, text="Mở camera", command=self.TrackImages  ,fg="#fff"  ,bg="#0094cf"  ,width=20  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.openCameraBtn.place(relx=0.19,y=740)
        self.closeCameraBtn = tk.Button(self.frameMain, text="Đóng camera", command=self.closeCamera  ,fg="#fff"  ,bg="#0094cf"  ,width=20  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
        self.closeCameraBtn.place(relx=0.33,y=740)
        self.closeCameraBtn.config(state='disabled')

    def fillInfo(self,staff : Staff,imageAttendance : str):
        self.txt.configure(state='normal')
        self.txt.delete(0,"end")
        self.txt.insert(0,str(staff.getStaffId()))
        self.txt.configure(state='disabled')
        self.txt2.configure(state='normal')
        self.txt2.delete(0,"end")
        self.txt2.insert(0,str(staff.getFullName()))
        self.txt2.configure(state='disabled')
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.txt3.configure(state='normal')
        self.txt3.delete(0,"end")
        self.txt3.insert(0,str(dt_string))
        self.txt3.configure(state='disabled')
        self.txt4.configure(state='normal')
        self.txt4.delete(0,"end")
        self.txt4.insert(0,str(staff.getDeptId()))
        self.txt4.configure(state='disabled')
        print(imageAttendance)
        img_Capture=Image.open(imageAttendance)
        img_Capture = img_Capture.resize((217, 217),Image.ANTIALIAS)
        imgCaptureTk = ImageTk.PhotoImage(image = img_Capture)
        self.imageCapture.imgtk = imgCaptureTk
        self.imageCapture.configure(image=imgCaptureTk)
        self.frame2.update()
    def TrackImages(self):
        self.openCameraBtn.config(state='disabled')
        self.closeCameraBtn.config(state='active')
        cap = cv2.VideoCapture(0)
        self.type_combo.config(state='disabled')
        type = 1
        if self.type_combo.get() == "Vào":
            type = 1
        else:
            type = 2
        while True:
            ret, frame = cap.read()
            feature, boxs = pre.FaceFeatures(frame)
            try:
                if len(boxs) == 0:
                    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image = img)
                    self.video.imgtk = imgtk
                    self.video.configure(image=imgtk)
                    print("length 0")
                    self.frame2.update()
                else:
                    id = 'Unknown'
                    fullName = 'Unknown'
                    for box,feature in zip(boxs, feature): 
                        feature = feature.reshape(-1, 3780) 
                        result = model.predict(feature) # du doan dac trung truyen vao so voi anh train
                        name = label_encoder.inverse_transform(result)
                        yhat_prob = model.predict_proba(feature)
                        # get name
                        class_index = result[0]
                        class_probability = yhat_prob[0,class_index] * 100 
                        x1, y1, x2, y2 = box
                        cv2.rectangle(frame, (y2, x1), (y1, x2), (255,255,255), 1)
                        namePre = name[0]
                        fullName = 'Unknown'
                        if(class_probability<30 or namePre == 'Unknown'):
                            namePre = 'Unknown'
                            fullName = 'Unknown'
                            id = 'Unknown'
                        else:
                            id = namePre.split('-')[0]
                            fullName = namePre.split('-')[1]
                        cv2.putText(frame, 'MNV: '+id,(y2, x1-55), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1) #viet text
                        cv2.putText(frame, 'Ho ten: '+fullName,(y2, x1-30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1) #viet text
                        cv2.putText(frame, 'Accuracy: '+str(round(class_probability, 3))+'%',(y2, x1-7), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1) #viet text
                    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2image)
                    imgtk = ImageTk.PhotoImage(image = img)
                    self.video.imgtk = imgtk
                    self.video.configure(image=imgtk)
                    if namePre != 'Unknow':
                        staff = self.getInfoUser(int(namePre.split('-')[0]),type)
                        if staff == None:
                            print("Khonng co nhan vien hoac nhan vien da điểm danh")
                            self.frame2.update()
                        else :
                            nowTime = datetime.now()
                            timeAttendance = nowTime.strftime("%d%m%Y")
                            image = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
                            if not os.path.exists('image_attendance'+'/'+timeAttendance):
                                os.makedirs('image_attendance'+'/'+timeAttendance)
                            if(len(box) > 0):
                                timeImage = datetime.now().strftime("%d%m%Y%H%M%S")
                                if not os.path.exists('image_attendance'+'/'+str(timeAttendance)+'/'+str(staff.getStaffId())+'_'+str(timeImage)+ '.jpg'):     
                                    cv2.imwrite('image_attendance'+'/'+timeAttendance+'/'+str(staff.getStaffId())+'_'+str(timeImage)+ '.jpg',image[x1:x2, y2:y1])  
                                    self.insertAttendance(staff,'image_attendance'+'/'+timeAttendance+'/'+str(staff.getStaffId())+'_'+str(timeImage)+ '.jpg',type)
                                    self.fillInfo(staff,'image_attendance'+'/'+timeAttendance+'/'+str(staff.getStaffId())+'_'+str(timeImage)+ '.jpg')
            except Exception:
                traceback.print_exc()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image = img)
                self.video.imgtk = imgtk
                self.video.configure(image=imgtk)

                self.frame2.update()
                continue
            if isCloseCamera=='CLOSE':
                break
        self.restartValue()
        cap.release() # giai phong du lieu video
        cv2.waitKey()
        cv2.destroyAllWindows() # giai phong du lieu anh
    def closeCamera(self):
        global isCloseCamera
        isCloseCamera = 'CLOSE'
    def restartValue(self):
        global isCloseCamera
        isCloseCamera = 'OPEN'
        img_camera=Image.open(r"Image\cammera.jpg")
        img_camera = img_camera.resize((639, 481),Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image = img_camera)
        self.video.imgtk = imgtk
        self.video.configure(image=imgtk)
        self.img_unknow=Image.open(r"Image\unkownImage.jpg")
        self.img_unknow = self.img_unknow.resize((217, 217),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(self.img_unknow)
        self.imageCapture =  tk.Label(self.frame2,bg="#efefef",borderwidth=2, relief="ridge",image=self.photoimg)
        self.imageCapture.grid(row=0, column=0)
        self.imageCapture.place(x=160, y=10,width=217,height=217)
        self.txt.configure(state='normal')
        self.txt.delete(0,"end")
        self.txt.insert(0,str(''))
        self.txt.configure(state='disabled')
        self.txt2.configure(state='normal')
        self.txt2.delete(0,"end")
        self.txt2.insert(0,str(''))
        self.txt2.configure(state='disabled')
        self.txt3.configure(state='normal')
        self.txt3.delete(0,"end")
        self.txt3.insert(0,str(''))
        self.txt3.configure(state='disabled')
        self.txt4.configure(state='normal')
        self.txt4.delete(0,"end")
        self.txt4.insert(0,str(''))
        self.txt4.configure(state='disabled')
        self.closeCameraBtn.config(state='disabled')
        self.openCameraBtn.config(state='active')
        self.type_combo.config(state='readonly')
        self.frame2.update()
    def getInfoUser(self,id,type):
        try: 
            staff = None
            con = conMana.getConnection()
            cur = con.cursor()
            sql = "select * from STAFF where staff_id= :staff_id and status = 'ACTIVE' and staff_id not in (select STAFF_ID from attendance where  attendance_type = :attendanceType and ATTENDANCE_DATE >TRUNC(SYSDATE) AND ATTENDANCE_DATE< TRUNC(SYSDATE+1))"
            cur.execute(sql,staff_id =  int(id),attendanceType =type )
            res = cur.fetchall()
            for row in res:
                staff = Staff()
                staff.setStaffId(row[0])
                staff.setFullName(row[1])
                staff.setGender(row[2])
                staff.setIdCard(row[3])
                staff.setIdIssuedDate(row[4])
                staff.setIdIssuedPlace(row[5])
                staff.setBirthDay(row[6])
                staff.setAddress(row[7])
                staff.setPhone(row[8])
                staff.setDeptId(row[9])
                staff.setStatus(row[10])
                staff.setCreateDate(row[11])
                staff.setCreateUser(row[12])
                staff.setUpdateDate(row[13])
                staff.setUpdateUser(row[14])
                staff.setDeleteDate(row[15])
                staff.setDeleteUser(row[16])
        except cx_Oracle.DatabaseError as e: 
            print("There is a problem with Oracle", e)
        finally:
            if con: 
                con.close()
        return staff
    def insertAttendance(self,staff :Staff,imgAttendance : str,type :int):
        con = conMana.getConnection()
        rows = [ (staff.getStaffId(), staff.getFullName(),staff.getDeptId(),1,type,imgAttendance ) ]
        curInsert = con.cursor()
        curInsert.executemany("insert into attendance(ATTENDANCE_ID,STAFF_ID,FULL_NAME,DEPT_ID,ATTENDANCE_DATE,ATTENDANCE_STATUS,attendance_type,ATTENDANCE_IMAGE) values (ATTENDANCE_seq.nextval, :1,:2,:3,sysdate,:4,:5,:6)", rows)
        con.commit()
if __name__=="__main__":
    root=Tk()
    obj=FaceRecognitionClass(root)
    root.mainloop()
##################### END ######################################

####################################################################################################
