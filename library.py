import datetime
import MySQLdb
import time
from datetime import date
db=MySQLdb.connect('localhost','root','********','library')
c=db.cursor()
from Tkinter import *
import tkMessageBox
t=Tk()
def registration():
    def insert():
        sql="insert into login(user_name,password)values('%s','%s')"%(u.get(),p.get())
        try:
            c.execute(sql)
            db.commit()
        except Exception,e:
            print e
            tkMessageBox.showinfo(message="User_Name already exist")
            db.rollback()
        u.delete(0,END)
        p.delete(0,END)
        
    t1=Tk()
    Label(t1,text="REGISTRATION",relief=RAISED,padx=20).grid(column=1)
    Label(t1,text="USER_NAME",relief=RAISED).grid(row=1)
    Label(t1,text="PASSWORD",relief=RAISED).grid(row=2)
    u=Entry(t1)
    u.grid(row=1,column=1)
    p=Entry(t1)
    p.grid(row=2,column=1)
    s=Button(t1,text="SUBMIT",bg="blue",command=insert)
    s.grid(row=3,column=1)



    
def login():


    sql="select password from login where user_name=('%s')"%(str(un.get()))
    try:
        c.execute(sql)
        result=c.fetchone()
        d=str(result[0])
            
        if d==str(pwd.get()) and str(un.get())=='r':
            t2=Tk()
            
            def book():
                
                sql="insert into book(author,name,price,category,monthly_fee,fine,id,availablity)values('%s','%s','%d','%s','%d','%d','%d','%s')"%(athr.get(),name.get(),int(price.get()),cgry.get(),int(mfee.get()),int(fine.get()),int(i.get()),avlb.get())
                try:
                    c.execute(sql)
                    db.commit()
                    
                except Exception,e:
                    print e
                    db.rollback()
                athr.delete(0,END)
                name.delete(0,END)
                price.delete(0,END)
                cgry.delete(0,END)
                mfee.delete(0,END)
                fine.delete(0,END)
                i.delete(0,END)
                avlb.delete(0,END)
                db.commit()
                
            
            def rtrn():
                try:
                    c.execute("select curdate()")
                    date=c.fetchone()
                    
                    c.execute("select issued_date from report where id=%d"%(int(ir.get())))
                    d1=c.fetchone()
                    
                    dd=datetime.datetime.strptime(str(d1[0]),"%Y-%m-%d")
                    d2=dd+datetime.timedelta(days=29)
                    d3=datetime.datetime.strptime(str(d2),"%Y-%m-%d %H:%M:%S")
                    d4=d3.date()
                    
                   
                    
                    if date[0]>d4:
                        n=date[0]-d4
                        
                        c.execute("select monthly_fee,fine from book where id='%d'"%(int(ir.get())))
                        f=c.fetchall()
                        for i in f:
                            
                            c.execute("update report set fee=%d+%d"%(i[0],(i[1]*n)))
                            db.commit()
                
                    
                    else:
                        try:
                            print date[0]
                            print ir.get()
                            c.execute("update report set return_date='%s' where id='%d'"%(str(date[0]),int(ir.get())))
                            db.commit()
                            c.execute("select * from report where id='%d'"%(int(ir.get())))
                            result=c.fetchall()
                            for i in result:
                                c.execute("insert into records(id,name,issued_date,return_date,fee)values('%d','%s','%s','%s','%d')"%(i[0],i[1],i[2],i[3],i[4]))
                            db.commit()
                        except Exception,e:
                            print e
                            db.rollback()
                    c.execute("update book set availablity='%s' where id='%d'"%("Available",int(ir.get())))
                    c.execute("delete from temp where id='%d'"%(int(ir.get())))
                    c.execute("delete from report where id=%d"%(int(ir.get())))
                    db.commit()

                except Exception,e:
                    print e
                    db.rollback()
                ir.delete(0,END)
            Label(t2,text="ADMIN PANEL",relief=RAISED,bg="red",padx=50).grid(column=1)
            Label(t2,text="Author",relief=RAISED).grid(row=1)
            Label(t2,text="Name",relief=RAISED).grid(row=2)
            Label(t2,text="Price",relief=RAISED).grid(row=3)
            Label(t2,text="Category",relief=RAISED).grid(row=4)
            Label(t2,text="Monthly_fee",relief=RAISED).grid(row=5)
            Label(t2,text="Fine",relief=RAISED).grid(row=6)
            Label(t2,text="Id",relief=RAISED).grid(row=7)
            Label(t2,text="Availablity",relief=RAISED).grid(row=8)
            athr=Entry(t2)
            name=Entry(t2)
            price=Entry(t2)
            cgry=Entry(t2)
            mfee=Entry(t2)
            fine=Entry(t2)
            i=Entry(t2)
            avlb=Entry(t2)
            athr.grid(row=1,column=1)
            name.grid(row=2,column=1)
            price.grid(row=3,column=1)
            cgry.grid(row=4,column=1)
            mfee.grid(row=5,column=1)
            fine.grid(row=6,column=1)
            i.grid(row=7,column=1)
            avlb.grid(row=8,column=1)
            sbmt=Button(t2,text="submit",relief=RAISED,command=book)
            sbmt.grid(row=9,column=1)
            l1=Listbox(t2,selectmode=MULTIPLE)
            l1.grid(row=10,column=1)
            
            try:
                c.execute("select * from temp")
                result=c.fetchall()
                for i in result:
                    d="name='%s',id='%d'"%(i[0],i[1])
                    l1.insert(1,d)
                db.commit()
            except Exception,e:
                print e
                db.rollback()
            
            Label(t2,text="FOR RETURN",relief=RAISED,padx=10).grid(row=14,column=1)
            Label(t2,text="Id",relief=RAISED).grid(row=15)
            ir=Entry(t2)
            ir.grid(row=15,column=1)
            rb=Button(t2,text="RETURN",relief=RAISED,command=rtrn)
            rb.grid(row=16,column=1)
        elif(result[0]==pwd.get()):
            def ctgry():
                t3=Tk()
                l2=Listbox(t3,selectmode=MULTIPLE)
                l2.grid()
                try:
                    c.execute("select * from book where category='%s'"%(e1.get()))
                    result=c.fetchall()
                    for i in result:
                        d=i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]
                        l2.insert(1,d)
                    db.commit()
                except Exception,e:
                    print e
                    db.rollback()
            def temp():
                try:
                    c.execute("select monthly_fee from book where id=%d"%(int(e2.get())))
                    result=c.fetchone()
                    
                    c.execute("update book set availablity='%s' where id='%d'"%("Issued",int(e2.get())))
                    c.execute("insert into temp(user_name,id)values('%s','%d')"%(un.get(),int(e2.get())))
                    c.execute("insert into report(id,name,issued_date,fee)values('%d','%s','%s','%d')"%(int(e2.get()),un.get(),date[0],result[0]))
                    
                    db.commit()
                except Exception,e:
                    tkMessageBox.showinfo(message=e)
                    db.rollback()
                    e2.delete(0,END)
                

            t2=Tk()
            Label(t2,text="WELCOME TO LIBRARY",relief=RAISED,bg="red",padx=20).grid(column=1)
            l1=Listbox(t2,selectmode=MULTIPLE,width=50)
            l1.grid(row=1,column=1)
            Label(t2,text="Category",padx=50).grid(row=5)
            e1=Entry(t2)
            e1.grid(row=5,column=1)
            s=Button(t2,text="Search",relief=RAISED,command=ctgry)
            s.grid(row=5,column=2)
            try:
                c.execute("select * from book")
                result=c.fetchall()
                db.commit()
                for i in result:
                    d="Author='%s',Name='%s',Price='%s',Category='%s',mfee='%d',Fine='%d',Id='%d',Availablity='%s'"%(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
                    l1.insert(1,d)
            except Exception,e:
                print e
                db.rollback()
            Label(t2,text="Select Your Book",relief=RAISED,padx=50).grid(row=6,column=1)
            Label(t2,text="Book Id",relief=RAISED).grid(row=7)
            e2=Entry(t2)
            e2.grid(row=7,column=1)
            b1=Button(t2,text="Ok",relief=RAISED,command=temp)
            b1.grid(row=7,column=2)
            try:
                c.execute("select current_date()")
                date=c.fetchone()
                if e2.get():
                    
                    c.execute("select issued_date from report where id=%d"%(int(e2.get())))
                    d1=c.fetchone()
                    print d1[0]
                    dd=datetime.datetime.strptime(str(d1[0]),"%Y-%m-%d")
                


                    d2=dd+datetime.timedelta(days=29)
                    d3=datetime.datetime.strptime(str(d2),"%Y-%m-%d %H:%M:%S")
                    d4=d3.date()
                    print d4
                
                    if d4==date[0]:
                        tkMessageBox.showinfo(message="last date")
                    elif date[0]>d4:
                        tkMessageBox.showinfo(message="date expired")
                db.commit()
            except Exception,e:
                print e
                db.rollback()
        else:
            tkMessageBox.showinfo(message="invalid user_name or password")
        
    except Exception,e:
        print e
        db.rollback()
Label(t,text="WELCOME TO THE LIBRARY",relief=RAISED,bg="red",fg="black",padx=20).grid(column=1)
Label(t,text="USER_NAME",relief=RAISED).grid(row=1)
Label(t,text="PASSWORD",relief=RAISED).grid(row=2)
un=Entry(t)
un.grid(row=1,column=1)
pwd=Entry(t)
pwd.grid(row=2,column=1)
lg=Button(t,text="LOGIN",relief=RAISED,command=login)
lg.grid(row=3,column=1)
Label(t,text="for new users").grid(row=4)
si=Button(text="SIGNUP",relief=RAISED,command=registration)
si.grid(row=4,column=1)
t.mainloop()
