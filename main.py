import json
import os
import sys
import time
from PIL import Image
import colorama
import keyboard
from rich.console import Console
from rich.text import Text as RichText
colorama.init()

def save_file(key,valve,path="save.json"):
    try:
        with open(path,"r",encoding="utf-8") as f:
            save = json.loads(f.read())
    except:save={}
    save[key]=valve
    with open(path,"w",encoding="utf-8") as f:
        f.write(json.dumps(save))

def get_file(key,path="save.json"):
    try:
        with open(path,"r",encoding="utf-8") as f:
            save = json.loads(f.read())
        return save.get(key)
    except: return None


def gradient_text(text,color,end="\n",step=10):
    print(colorama.Fore.RESET,end="")
    for _ in text:
        color[0] -= step
        color[1] -= step
        color[2] -= step
    for i,sim in enumerate(text):
        Console(soft_wrap=True).print(RichText(sim), style=f"rgb({color[0]+i*step},{color[1]+i*step},{color[2]+i*step})", end="")
    print(end=end)

def draw_image(file_path="pizza.jpg",size=10):
    img = Image.open(file_path)
    for colon in range(size):
        for row in range(size):
            color=img.getpixel((img.size[0]//size*row, img.size[0]//size*colon))
            for _ in range(2):Console(soft_wrap=True).print(RichText("█"), style=f"rgb({color[0]},{color[1]},{color[2]})",end="")
        print()
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
class Item():
    def __init__(self,name,description,age,ingredients,price,sale,sale_description,id):
        self.name = name
        self.description = description
        self.age = age
        self.ingredients = ingredients
        self.price=price
        self.sale=sale
        self.sale_description=sale_description
        self.id=id
    def add_compound(self,*add):
        for ing in add:
            self.ingredients.append(ing)

    def remove_compound(self,*rem):
        for ing in rem:
            self.ingredients.remove(ing)

class ShopList():
    def __init__(self):
        self.decoded_json=[]
        self.items=[]
    def update_list(self,json_list=[]):
        self.decoded_json = json_list
        self.items=[]
        for data in self.decoded_json:
            self.items.append(Item(
                data["name"],
                data["description"],
                data["+18"],
                data["ingredients"],
                data["price"],
                data["sale"],
                data["sale_description"],
                data["id"],
            ))
        return self.items

class Shop():
    def __init__(self,json_list,save_file,user):
        self.save_file=save_file
        self.decoded_json=json.loads(json_list)
        self.shop_list=ShopList()
        self.shop_list.update_list(self.decoded_json["items"])
        self.name = self.decoded_json["name"]
        self.description = self.decoded_json["description"]
        self.user=user

    def draw_garbage(self):
        os.system("cls")
        text_in_image = [f"{colorama.Fore.RED + self.name + colorama.Fore.RESET}"] + f"{self.description}".split("\n")
        # img = Image.open("pizza.jpg")

        # size=len(self.description)//8
        size = len(text_in_image)
        for colon in range(size):
            for row in range(size):
                pass
            # color = img.getpixel((img.size[0] // size * row, img.size[0] // size * colon))
            # for _ in range(2): Console(soft_wrap=True).print(RichText("█"),
            #                                                style=f"rgb({color[0]},{color[1]},{color[2]})", end="")
            if len(text_in_image) > colon: print(text_in_image[colon], end="")
            print()
        # print(colorama.Fore.RED+f"{(len(self.description)//2 - len(self.name)//2 -3) * '-'} {self.name} {(len(self.description)//2 - len(self.name)//2 -3) * '-'}")
        # print(f"{colorama.Fore.GREEN+self.description}")
        for i, item in enumerate(self.shop_list.items):
            if self.in_garbage(item.id)!=0:
                print(colorama.Fore.YELLOW + "●", item.name,
                      (colorama.Back.RED + colorama.Fore.BLACK + "(+18)" + colorama.Back.RESET) * int(item.age),
                      (colorama.Back.YELLOW + colorama.Fore.BLACK + f"СКИДКА {item.sale}%" + colorama.Back.RESET) * int(
                          item.sale != 0),
                      colorama.Fore.RED + f"{self.in_garbage(item.id)} в корзине" * int(self.in_garbage(item.id) != 0),
                      end=" "
                      )
                if self.liked(item.id):
                    gradient_text("Лайкнуто", color=[255, 255, 94])
                else:
                    print()

        print(colorama.Fore.GREEN+"Денег на карте:", self.user.wallet.money_card)
        print("Денег наличкой:", self.user.wallet.cash)

    def draw_menu(self,select=0):



        os.system("cls")
        text_in_image=[f"{colorama.Fore.RED+self.name+colorama.Fore.RESET}"]+f"{self.description}".split("\n")
        #img = Image.open("pizza.jpg")

        #size=len(self.description)//8
        size=len(text_in_image)
        for colon in range(size):
            for row in range(size):
                pass
               # color = img.getpixel((img.size[0] // size * row, img.size[0] // size * colon))
                #for _ in range(2): Console(soft_wrap=True).print(RichText("█"),
                 #                                                style=f"rgb({color[0]},{color[1]},{color[2]})", end="")
            if len(text_in_image)>colon: print(text_in_image[colon],end="")
            print()
        #print(colorama.Fore.RED+f"{(len(self.description)//2 - len(self.name)//2 -3) * '-'} {self.name} {(len(self.description)//2 - len(self.name)//2 -3) * '-'}")
        #print(f"{colorama.Fore.GREEN+self.description}")
        for i,item in enumerate(self.shop_list.items):
            if i==select:print()
            print(colorama.Fore.YELLOW + "●", item.name,
                  (colorama.Back.RED + colorama.Fore.BLACK + "(+18)" + colorama.Back.RESET) * int(item.age),(colorama.Back.YELLOW + colorama.Fore.BLACK + f"СКИДКА {item.sale}%" + colorama.Back.RESET) * int(
                        item.sale != 0),
                        colorama.Fore.RED + f"{self.in_garbage(item.id)} в корзине" * int(self.in_garbage(item.id) != 0),end=" "
                  )
            if self.liked(item.id): gradient_text("Лайкнуто",color=[255,255,94])
            else:print()
            if i == select:
                print(colorama.Fore.YELLOW + "├──> ", item.description,
                      (colorama.Back.YELLOW + colorama.Fore.BLACK + f"СКИДКА {item.sale}%" + colorama.Back.RESET) * int(
                          item.sale != 0))
                if item.sale != 0:print(colorama.Fore.YELLOW + "├──> ",
                      (colorama.Back.YELLOW + colorama.Fore.BLACK + item.sale_description + colorama.Back.RESET) * int(
                          item.sale != 0))
                print(colorama.Fore.YELLOW + "├──> ","Ингредиенты:",
                      (colorama.Back.RESET + colorama.Fore.RED + ", ".join(item.ingredients) + colorama.Back.RESET))
                print(colorama.Fore.YELLOW + "└──> ", "Цена:",
                      (colorama.Back.RESET + colorama.Fore.RESET+(colorama.Back.YELLOW + colorama.Fore.BLACK)*int(item.sale !=0) + str(item.price-(item.price//100*item.sale))+"р"

                       + colorama.Back.RESET))
                if i == select: print()

    def in_garbage(self,id):
        i=0
        garbage = get_file("garbage", self.save_file)
        if garbage == None: garbage = []
        for id_item in garbage:
            if id == id_item:i+=1
        return i

    def liked(self,id):
        i=0
        liked = get_file("likes", self.save_file)
        if liked == None: liked = []
        for id_item in liked:

            if id == id_item:
                return True
        return False
    def payment(self):
        os.system("cls")
        text_in_image = [f"{colorama.Fore.RED + self.name + colorama.Fore.RESET}"] + f"{self.description}".split("\n")

        size = len(text_in_image)
        for colon in range(size):
            for row in range(size):
                pass
            # color = img.getpixel((img.size[0] // size * row, img.size[0] // size * colon))
            # for _ in range(2): Console(soft_wrap=True).print(RichText("█"),
            #                                                style=f"rgb({color[0]},{color[1]},{color[2]})", end="")
            if len(text_in_image) > colon: print(text_in_image[colon], end="")
            print()
        full_price=0
        age_need_allow=False
        have_any_item=False
        for i, item in enumerate(self.shop_list.items):
            if self.in_garbage(item.id)!=0:
                have_any_item=True
                if item.age:age_need_allow=True
                print(colorama.Fore.YELLOW + "●", item.name,
                      (colorama.Back.RED + colorama.Fore.BLACK + "(+18)" + colorama.Back.RESET) * int(item.age),
                      (colorama.Back.YELLOW + colorama.Fore.BLACK + f"СКИДКА {item.sale}%" + colorama.Back.RESET) * int(
                          item.sale != 0),
                      colorama.Fore.RED + f"{self.in_garbage(item.id)} в корзине" * int(self.in_garbage(item.id) != 0),
                      end=" "
                      )
                full_price = full_price + self.in_garbage(item.id)*(item.price-(item.price//100*item.sale))
                print(colorama.Fore.RESET+str( self.in_garbage(item.id)*(item.price-(item.price//100*item.sale)))+"р")
        print()
        print(colorama.Fore.GREEN + "Итог:", full_price)
        if age_need_allow and self.user.age<18:
            print(colorama.Fore.GREEN + "В вашем заказе есть товары которые нельзя продавать с эти возрастом!")
            return False
        if not have_any_item:
            print(colorama.Fore.GREEN + "В вашем заказе нет товаров!")
            return False
        print(colorama.Fore.GREEN+"Итог:",full_price)
        print(colorama.Fore.GREEN+"< Наличка | Безнал >")
        while True:
            if keyboard.is_pressed('left'):
                time.sleep(0.5)
                print("Денег у вас есть:",self.user.wallet.cash)
                while True:
                    try:
                        send_to_payment=float(input("Сколько вы даёте рублей?: "))
                        break
                    except:print()
                if send_to_payment<full_price:print("Вы недоплатили.")
                else:

                    try:
                        self.user.wallet.edit_cash(-full_price)
                        print("Сдача:", send_to_payment - full_price)
                        print("Спасибо за заказ,", self.user.name + "!")
                    except Exception as e:
                        print("Ошибка при оплате:", e)
                break
            if keyboard.is_pressed('right'):
                time.sleep(0.5)
                print("Денег у вас есть:", self.user.wallet.money_card)
                try:
                    self.user.wallet.edit_money_card(-full_price)
                    print("Спасибо за заказ,",self.user.name+"!")
                except Exception as e:
                    print("Ошибка при оплате:", e)
                break

    def menu_loop(self):
        select=0
        self.draw_menu(select)
        while True:

            if keyboard.is_pressed('up'):
                select-=1
                if select<0:select=0
                self.draw_menu(select)
                time.sleep(0.5)

            if keyboard.is_pressed('down'):
                select+=1
                if select >= len(self.shop_list.items): select = len(self.shop_list.items)-1
                self.draw_menu(select)
                time.sleep(0.5)

            if keyboard.is_pressed('enter'):
                garbage=get_file("garbage",self.save_file)
                if garbage==None:garbage=[]
                garbage.append(self.shop_list.items[select].id)
                save_file("garbage",garbage, self.save_file)
                self.draw_menu(select)
                time.sleep(0.5)

            if keyboard.is_pressed('backspace'):
                garbage=get_file("garbage",self.save_file)
                if garbage==None:garbage=[]
                if self.shop_list.items[select].id in garbage:garbage.remove(self.shop_list.items[select].id)
                save_file("garbage",garbage, self.save_file)
                self.draw_menu(select)
                time.sleep(0.5)
            if keyboard.is_pressed('right'):
                likes=get_file("likes",self.save_file)
                if likes==None:likes=[]
                if self.liked(self.shop_list.items[select].id):likes.remove(self.shop_list.items[select].id)
                else: likes.append(self.shop_list.items[select].id)
                save_file("likes",likes, self.save_file)
                self.draw_menu(select)
                time.sleep(0.5)
            if keyboard.is_pressed('left'):
                self.draw_garbage()
                time.sleep(0.5)
                while True:
                    if keyboard.is_pressed('left'):
                        break
                    if keyboard.is_pressed('enter'):
                        self.payment()
                        time.sleep(5)
                        break
                self.draw_menu()
                time.sleep(0.5)

class Wallet():
    def __init__(self,money_card,cash,save_file="save.json",save_load=True):
        self.money_card=money_card
        self.cash=cash
        self.save_file = save_file
        self.save_load=save_load
        if save_load:self.load()
    def edit_cash(self,count):
        if (self.cash + count)<0:
            raise ValueError("There is no money to pay")
        else:self.cash+=count
        if self.save_load:self.save()

    def edit_money_card(self,count):
        if (self.money_card + count)<0:
            raise ValueError("There is no money to pay")
        else:self.money_card+=count
        if self.save_load:self.save()

    def save(self):
        save_file("money_card",self.money_card,self.save_file)
        save_file("cash", self.cash, self.save_file)

    def load(self):
        if get_file("money_card",self.save_file)!=None:self.money_card=get_file("money_card",self.save_file)
        if get_file("cash",self.save_file)!=None:self.cash=get_file("cash", self.save_file)


class User():
    def __init__(self,name=None,age=None,wallet=Wallet(10000,10000),save_file="save.json",save_load=True):
        self.save_file = save_file
        if save_load:self.load()
        if get_file("name",self.save_file)==None:
            while True:
                try:
                    self.name=input("Ваше имя: ")
                    self.age=int(input("Ваш возраст: "))
                    break
                except:print()
            if save_load: self.save()
        self.wallet=wallet

    def save(self):
        save_file("name",self.name,self.save_file)
        save_file("age", self.age, self.save_file)

    def load(self):
        if get_file("name",self.save_file)!=None:self.name=get_file("name",self.save_file)
        if get_file("age",self.save_file)!=None:self.age=get_file("age", self.save_file)


if __name__=="__main__":
    shop_file="shop.json"
    if len(sys.argv)==2:
        shop_file=sys.argv[1]
    shop=Shop(read_file(shop_file),"save.json",User(None,None,Wallet(10000,10000,save_load=True)))
    shop.menu_loop()
