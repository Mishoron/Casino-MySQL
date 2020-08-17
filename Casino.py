import mysql.connector
from random import randint

mydb = mysql.connector.connect(
	host="",
	user="",
	password = "",
	database = ""
)
cursor = mydb.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS casino(
	nick VARCHAR(10),
	password VARCHAR(12),
	balance BIGINT""")
mydb.commit()

def login():
	global login
	menu = input("У вас есть учетная запись(y/n) ")
	if menu == "y":
		login = input("Ваш логин: ")
		passw = input("Ваш пароль: ")
		cursor.execute(f"SELECT nick,password FROM casino WHERE nick ='{login}' AND password='{passw}'")
		res = cursor.fetchall()
		if not res:
			print("Вы не зареганы !!!")
			reg()
		else:
			casino()
	elif menu == "n":
		reg()
	else:
		print("Бубылда тебя читать неучили !>:(>")

def reg():
	print("Зарегистрируйтесь!")
	reg = input("Придумайте логин(макс длинной 10 символов): ")
	if len(reg) > 10:
		print("Бубылда офигел тебе чо говорили!")
		return
	passw = input("Придумайте пароль(макс длинной 12 символов): ")
	if len(passw) > 12:
		print("Бубылда ну ты прикалываешься!")
		return
	cursor.execute(f"SELECT nick FROM casino WHERE nick='{reg}'")
	res = cursor.fetchall()
	if not res:
		cursor.execute(f"INSERT INTO casino VALUES('{reg}','{passw}','{100}')")
		mydb.commit()
		print("Успешно зарегистрированны!")
		print("Дальше идите и авторизуйтесь.")
	else:
		print("Такая учетная запись существует!")	
	mydb.close()

def balance():
	cursor.execute(f"SELECT balance FROM casino WHERE nick = '{login}'")
	res = cursor.fetchone()
	for i in res:
		return print(i)

def delete():
	cursor.execute(f"DELETE FROM casino WHERE nick ='{login}'")
	mydb.commit()
	mydb.close()

def money_control(dev:str,cash):
	if dev == "add":
		cursor.execute(f"SELECT balance FROM casino WHERE nick ='{login}'")
		balance = cursor.fetchone()
		for i in balance:
			cursor.execute(f"UPDATE casino SET balance ='{int(i) + int(cash)}' WHERE nick ='{login}'")
			print("Средства Успешно добавлены на ваш баланс")
			mydb.commit()
			mydb.close()
	elif dev == "remove":
		cursor.execute(f"SELECT balance FROM casino WHERE nick ='{login}'")
		balance = cursor.fetchone()
		for i in balance:
			if i <= int(cash):
				print("Вы проиграли все деньгы и были выгнаны из казино.")
				delete()
				return
			cursor.execute(f"UPDATE casino SET balance ='{int(i) - int(cash)}' WHERE nick ='{login}'")
			print("Средства Успешно списаны с баланса")
			mydb.commit()
			mydb.close()

def casino():
	print("Ваш баланс")
	balance()
	try:
		stav = input("Сумма ставки: ")
		cursor.execute(f"SELECT balance FROM casino WHERE nick='{login}'")
		res = cursor.fetchone()
		for i in res:
			if int(stav) > int(i):
				print("Вы не можете поставить больше чем у вас есть.(")
				return
			else:
				print("Ставка принята")
		
		chance = randint(1,2)
		if chance == 1:
			print(f"Вы победили!!!Ваш выигрыш:{int(stav) * 2}")
			money_control(dev = "add",cash = f"{int(stav) * 2}")
		elif chance == 2:
			print(f"Вы проиграли: {int(stav) * 2}")
			money_control(dev = "remove", cash = f"{int(stav) * 2}")
	except ValueError:
		print("Бубылда пиши цифры!!!")
		
if __name__ == '__main__':
	login()
