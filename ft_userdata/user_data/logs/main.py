import time
import discord
from discord import Embed
from discord.ext import tasks

"""import keyboard  # using module keyboard

def temps(temps):
    debut = time.time()
    while(temps >= (time.time()-debut)):
        sortie()
        #print((time.time()-debut))

def sortie():
    if keyboard.is_pressed('q'):
        print('\n=========================================\n          Sortie d\'urgence\n=========================================\n')
        quit()
"""

client = discord.Client()

def recherche_message():
        message = {"sell": [], "buy": []}
        with open('freqtrade.log', 'r') as f:
                for line in f:
                        if "Sending rpc message" in line:
                                #cas sell
                                if "'type': sell" in line:
                                        txt = triage1(line)         #sort le dictionnaire
                                        sortie = ecriture(txt,"sell")      #sort s'il existe ou pas
                                        if sortie:
                                                message["sell"].append(txt) #enregistre dans la liste sell pour l'afficher
                                #cas buy               
                                elif "'type': buy" in line:
                                        txt = triage1(line) 
                                        sortie = ecriture(txt,"buy")     
                                        if sortie:
                                                message["buy"].append(txt)       
        return message


def triage1(line):
        #initialisation des variable 
        dictio_txt = ""
        t1 = False
        t2 = False
        t3 = False
        #permet de prendre que le dictionnaire et non le texte entier
        for i in line:
                if(t1 and t2 and t3):
                        if(i!=" "):
                                dictio_txt += i

                elif i == ":" and t1 == False:
                        t1 = True
                elif i == ":" and t2 == False:
                        t2 = True
                elif i == ":" and t3 == False:
                        t3 = True
        return dictio_txt




def trier(txt,type): 
        _id = ""
        crypto = ""
        achat = ""
        vente = ""
        ratio = ""
        heure_achat= []
        heure_vente= []
        #         SELL                               BUY

        #1  ==> 'type'                             'trade_id'  <------ 
        #2  ==> 'trade_id'           <------       'type' 
        #3  ==> 'exchange'                         'buy_tag'
        #4  ==> 'pair' ex:'ETH/USDT  <------       'exchange'
        #5  ==> 'gain'                             'pair'      <------ 
        #6  ==> 'limit'                            'limit'
        #7  ==> 'order_type'                       'open_rate'  <------
        #8  ==> 'amount'                           'order_type'
        #9  ==> 'open_rate'          <------       'stake_amount'
        #10 ==> 'close_rate'         <------       'stake_currency'
        #11 ==> 'current_rate'                     'fiat_currency'
        #12 ==> 'profit_amount'      <------       'amount'      
        #13 ==> 'profit_ratio'                     'open_date'  <------
        #14 ==> 'buy_tag'                          'current_rate'
        #15 ==> 'sell_reason' 
        #16 ==> 'open_date'          <------
        #17 ==> 'close_date'         <------
        #18 ==> 'stake_currency'
        #19 ==> 'fiat_currency'
        nbr = 0
        noter = False

        heure = False
        heure_nombre = False
        nbr_heure = 0
        #apres une nbr de virgule
        #0 ===> annees
        #1 ===> mois
        #2 ===> jours
        #3 ===> heures
        #4 ===> minutes
        #5 ===> secondes
        year = ""
        month = ""
        day = ""
        hour = ""
        minute = ""
        seconde = ""
        for i in txt:
                if i == ":":
                        nbr += 1
                        noter = True
                elif noter == True and (i != "," or heure == True):

                        if (nbr == 2 and type == "sell") or (nbr == 1 and type == "buy"):
                                _id += i
                        elif (nbr == 4 and type == "sell") or (nbr == 5 and type == "buy"):
                                crypto += i
                        elif (nbr == 9 and type == "sell") or (nbr == 7 and type == "buy"):
                                achat += i
                        elif (nbr == 10 and type == "sell"):
                                vente += i
                        elif (nbr == 12 and type == "sell"):
                                ratio += i
                        elif (nbr == 16 and type == "sell") or (nbr == 13 and type == "buy"):
                                heure = True
                                if (i == "("):
                                        heure_nombre = True
                                elif (i == ")"):
                                        heure_nombre = False
                                        heure = False
                                elif (i == ","):
                                        nbr_heure += 1
                                
                                elif(heure_nombre):
                                        if nbr_heure == 0:
                                                year +=i
                                        elif nbr_heure == 1:
                                                month +=i
                                        elif nbr_heure == 2:
                                                day +=i
                                        elif nbr_heure == 3:
                                                hour +=i
                                        elif nbr_heure == 4:
                                                minute +=i
                                        elif nbr_heure == 5:
                                                seconde +=i


                        elif nbr == 17:
                                heure = True
                                if (i == "("):
                                        heure_nombre = True
                                        heure_achat.append(day+"/"+month+"/"+year)
                                        heure_achat.append(hour+"h"+minute+":"+seconde)
                                        year = ""
                                        month = ""
                                        day = ""
                                        hour = ""
                                        minute = ""
                                        seconde = ""
                                        nbr_heure = 0
                                elif (i == ")"):
                                        heure_nombre = False
                                elif (i == ","):
                                        nbr_heure += 1
                                
                                elif(heure_nombre):
                                        if nbr_heure == 0:
                                                year +=i
                                        elif nbr_heure == 1:
                                                month +=i
                                        elif nbr_heure == 2:
                                                day +=i
                                        elif nbr_heure == 3:
                                                hour +=i
                                        elif nbr_heure == 4:
                                                minute +=i
                                        elif nbr_heure == 5:
                                                seconde +=i
                                heure_vente += i
                        elif (nbr == 13 and type == "buy"):
                                break
                
                else:
                        noter = False
        
        

        if type == "buy":
                heure_achat.append(day+"/"+month+"/"+year)
                heure_achat.append(hour+"h"+minute+":"+seconde)
                return _id,crypto,achat,heure_achat

        elif type == "sell":
                heure_vente.append(day+"/"+month+"/"+year)
                heure_vente.append(hour+"h"+minute+":"+seconde)
                return _id,crypto,achat,vente,ratio,heure_achat,heure_vente

        return 'what!!!'


def ecriture(line,type):
        t1 = False
        t2 = False 
        id_txt = ""
        for i in line:
                if(t1 and t2 and type == "sell") or (t1 and type == "buy"):
                        if(i!=","):
                                id_txt += i
                        else:
                                break

                elif i == ":" and t1 == False:
                        t1 = True
                elif i == ":" and t2 == False:
                        t2 = True
        #print("id_txt", id_txt)
        faire = True
        liste = []
        with open(type+'.txt', 'r') as f:
                for line in f:
                        liste.append(line)
                        #print(line)
                        if id_txt+"\n" == line:
                                faire = False

        if faire:
                with open(type+'.txt', 'w+') as f:   # create a new file or truncates it
                        for i in liste:
                                f.write(i)
                        
                        f.write(id_txt+"\n")
        return faire
                

class Fretrade(discord.Client):
        async def on_ready(self):
                print("Le bot est prêt")
                self.my_background_task.start()

        @tasks.loop(seconds=600)  # task runs every 60 seconds
        async def my_background_task(self):
                channel = self.get_channel(955496908435103837)

                liste = recherche_message()
                 
                if liste["sell"]:
                        for i in liste["sell"]:
                                _id,crypto,achat,vente,ratio,heure_achat,heure_vente = trier(i,"sell")
                                embed = discord.Embed(title="💵  SELL  💵 \n\n🗓 "+heure_vente[0]+"\n "+heure_vente[1],colour = 0x52c72e)

                                retStr = str("""\n Quantité vente : """+vente+"""\n""")
                                embed.add_field(name="🪙 "+crypto,value=retStr)

                                retStr = str("""\n👉 Id : """+_id+"""\n""")
                                embed.add_field(name="📈Ratio : "+ratio,value=retStr)

                                retStr = str("""\n_by Luc\n""")
                                embed.add_field(name="🗓 Heure d'achat : "+heure_achat[0]+"\n                   "+heure_achat[1],value=retStr)

                                await channel.send(embed=embed)
                if liste["buy"]:
                        for i in liste["buy"]:
                                _id,crypto,achat,heure_achat = trier(i,"buy")
                                embed = discord.Embed(title="💰  BUY  💰\n\n🗓 "+heure_achat[0]+"\n "+heure_achat[1],colour = 0x2f11ec)

                                retStr = str("""\n Quantité achat : """+achat+"""\n""")
                                embed.add_field(name="🪙 "+crypto,value=retStr)

                                retStr = str("""\n_by Luc\n""")
                                embed.add_field(name=str("""\n👉 Id : """+_id+"""\n"""),value=retStr)

                                await channel.send(embed=embed)  
                


        
        async def on_message(self, message):
                if message.author.id == self.user.id:
                        return

                if message.content.startswith("ping") or message.content.startswith("Ping"):
                        #print(message)
                        await message.channel.send("pong 🏓")

                elif message.content.endswith("quoi") or message.content.endswith("Quoi") or message.content.endswith("Quoi!") or message.content.endswith("quoi!") or message.content.endswith("quoi.") or message.content.endswith("Quoi."):
                        await message.channel.send("FEUR  🪒")

                

if __name__ == "__main__":
        bot = Fretrade()
        
        bot.run("OTU1NDk0MTEzNzgyOTUyMDA3.YjifPA.V_IQxTxHTmIIwuxDEKTfg8N_FVA")
        
        
        


