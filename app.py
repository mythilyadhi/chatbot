from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import sqlite3
import random

app = Flask(__name__)

mybot = ChatBot("PizzaBot",storage_adapter="chatterbot.storage.SQLStorageAdapter")

training_data_quesans = open('ques_ans.txt').read().splitlines()

training_data = training_data_quesans

trainer = ListTrainer(mybot)
trainer.train(training_data)

db=sqlite3.connect('db1.sqlite3')
cursor = db.cursor()
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='orders' ''')
if cursor.fetchone()[0]==0 :
    cursor.execute('''CREATE TABLE orders(id INTEGER PRIMARY KEY,name TEXT, phone TEXT, address TEXT,pizzalist TEXT,total INTEGER)''')
db.commit()

flag = 0
@app.route("/")
def home():
    return render_template("index.html")
p_name=''
total=0
@app.route("/get")
def get_bot_response():
    with sqlite3.connect("db1.sqlite3") as db:
        global flag
        global p_name
        global total
        cursor = db.cursor()
        userText = request.args.get('msg')
        if(userText=='Italian Pizza' or userText == 'Greek Pizza' or userText=='Sarda Pizza' or userText=='Tonno Pizza'):
            if(p_name == '' ):
                if (userText == 'Italian Pizza'):
                    total += 150
                elif (userText== 'Greek Pizza'):
                    total += 200
                elif (userText== 'Sarda Pizza'):
                    total += 250
                elif (userText== 'Tonno Pizza'):
                    total += 300
                p_name=userText
            else:
                if (userText == 'Italian Pizza'):
                    total += 150
                elif (userText== 'Greek Pizza'):
                    total += 200
                elif (userText== 'Sarda Pizza'):
                    total += 250
                elif (userText== 'Tonno Pizza'):
                    total += 300
                p_name = p_name + ',' +userText
        if(flag == 1):
            ind = userText.index(',')
            name = userText[:ind]
            temp = userText[ind + 1:]
            ind = temp.index(',')
            phone = temp[:ind]
            address = temp[ind + 1:]
            cursor.execute('''INSERT INTO orders(name, phone, address,pizzalist,total) VALUES(?,?,?,?,?)''',(name, phone, address, p_name,total))
            cursor.execute('''SELECT * FROM orders WHERE phone=(?)''',(phone,))
            rows=cursor.fetchall()
            db.commit()
            flag = 0
            p_name=''
            total=0
            return 'Order Id: '+str(rows[0][0])+' \t Ordered Items: '+str(rows[0][4]) +'.' +'  Bill amount:'+str(rows[0][5])
        elif(flag==2):
            myid=int(userText)
            cursor.execute(''' SELECT count(id) FROM orders WHERE id=(?) ''',(myid,))
            if cursor.fetchone()[0] == 0:
                flag=0
                db.commit()
                return 'Kindly make an order with us'
            status = ["Your order is already out for delivery","Your order is being prepared"]
            index = [0,1]
            flag=0
            db.commit()
            return status[random.choice(index)]

        else:
            res = str(mybot.get_response(userText))
            if(res=='Kindly, enter your name, phone number, and the delivery address in the same format'):
                flag=1
            elif(res=='Please enter your order id'):
                flag=2
            return res

if __name__ == "__main__":
    app.run()

