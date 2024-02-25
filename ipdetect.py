import requests as r
import socket as s
import config
from colorama import Fore, Style

api_key , api_access =  config.run()

#main class
class ipDetect:
    #api usage
    def __init__(self, access, key) -> None:
        self.access = access
        self.api = access + key

    #rips ip into list
    def extend_ip(self, ip):
        lst = []
        temp = ""
        for chr in ip:
            if chr == ".":
                lst.append(temp)
                temp = ""
                lst.append(chr)
            else:
                temp += chr
        lst.append(temp)
        if lst.count('') > 0:
            for i in range(lst.count('')):
                lst.remove('')
            return lst
        else:
            return lst
    
    #checks if user-entered ip is valid
    def valid_ip(self, ip):
        lst = self.extend_ip(ip)
        allowed = [str(num) for num in range(0,256)] + list(".")
        check = [True for i in lst if i not in allowed]
        check2 = [True for j in lst if j.isalnum() == True]
        if len(lst) != 7 or len(check) != 0:
            return False
        elif len(check2) != 4 and False in check2:
            return False
        else:
            return ip
        
    def info_present(self, info):
        for key, value in info.items():
            if type(value) == dict:
                print(key + ":")
                for key2, value2 in value.items(): 
                    if value2 == '':
                        print(" ", key2 + ":", Fore.RED + "Not Found")
                        print(Style.RESET_ALL, end="")
                    elif value2 != False:
                        print(" ", key2 + ":", Fore.GREEN + str(value2))
                        print(Style.RESET_ALL, end="")   
                    else:
                        print(" ", key2 + ":", Fore.RED + str(value2))
                        print(Style.RESET_ALL, end="")
            else:
                if key == 'message':
                    print(Fore.RED + str(value))
                    print(Style.RESET_ALL, end="")
                elif value != False:
                    print(key + ":", Fore.GREEN + str(value))
                    print(Style.RESET_ALL, end="")
                else:
                    print(key + ":", value)

    #gets results from api   
    def output(self, ip):
        try:
            if ip == "":
                print(Fore.LIGHTRED_EX + "Missing IP address")
                print(Style.RESET_ALL, end="")
                print("usage: detect (ip)")
            else:
                self.api = self.api.replace("-",self.valid_ip(ip))
                result = r.get(self.api)
                result = result.json()
                self.info_present(result)
        except TypeError:
            print(Fore.LIGHTRED_EX + f"{ip} is not a valid IP address.")
            print(Style.RESET_ALL, end="")
        except KeyboardInterrupt:
            print("Ctrl C")
            print(Fore.GREEN + "Bye!")
            print(Style.RESET_ALL, end="")
            quit()
        except r.exceptions.JSONDecodeError:
            print(Fore.LIGHTRED_EX + "No api key is detected. Type 'key' to enter one.")
            print(Style.RESET_ALL, end="")
        except:
            print("Other Problems Occured")

    #exits the program
    def ex(self):
        print(Fore.GREEN + "Bye!")
        print(Style.RESET_ALL, end="")
        quit()

    #lists avaiable commands
    def lst_cmds(self):
        all_cmds = """
list - Lists all commands avaiable
ipshow - Shows your public and private IP address
key - Prompts you to enter api key
detect (ip) - Gives information based of given IP
exit - Exits the Program
        """
        print(all_cmds)

    def ipshow(self):
        pu_ip = r.get("https://api.ipify.org/").text
        pr_ip = s.gethostbyname(s.gethostname())
        print("Your public IP is:", Fore.GREEN + pu_ip )
        print(Style.RESET_ALL, end="")
        print("Your private IP is:", Fore.GREEN + pr_ip)
        print(Style.RESET_ALL, end="")
    
    def set_key(self):
        key = input("Enter the api key (the part after key=): ")
        self.api = self.access + key
        print(Fore.GREEN + "Updated!")
        print(Style.RESET_ALL, end="")

    
    #check if command passed in takes multiple args or not
    def clarify(self, user):
        tmp_lst = ["list", "detect", "exit", "ipshow"]
        if " " in user and user[:user.index(" ")] in tmp_lst:
            return True, user[:user.index(" ")], user[user.index(" ") + 1:]
        else:
            return False, user, None
        
    #stores all the commands
    def cmds(self):
        ac_cmds = {"list":self.lst_cmds,
                       "detect": lambda ip: self.output(ip), #lambda used to call self.output() when refered to
                        "ipshow": self.ipshow,
                        "key": self.set_key, 
                       "exit":self.ex}
        helparg_cmds = {"detect":"usage: detect (ip)"}
        while True:
            value = 0
            arg = 0
            try:
                user = input("~> ")
                value, user, arg = self.clarify(user)[0], self.clarify(user)[1], self.clarify(user)[2] #self.clarify() returns a tuple
                if value == True:
                    ac_cmds[user](arg)
                else:
                    ac_cmds[user]() #call the function in the ac_cmds dict
            except TypeError:
                print(Fore.LIGHTRED_EX + "This command requires an argument")
                print(Style.RESET_ALL, end="")
                print(helparg_cmds[user])
            except KeyError:
                print(Fore.LIGHTRED_EX + "Not a valid command")
                print(Style.RESET_ALL, end="")
            except KeyboardInterrupt:
                print("Ctrl C")
                print(Fore.GREEN + "Bye!")
                print(Style.RESET_ALL, end="")
                quit()
                
    #Displays tool banner
    def screen(self):
        banner = f"""
  _       _____       _            _   
 (_)     |  __ \     | |          | |  
  _ _ __ | |  | | ___| |_ ___  ___| |_ 
 | | '_ \| |  | |/ _ \ __/ _ \/ __| __|
 | | |_) | |__| |  __/ ||  __/ (__| |_ 
 |_| .__/|_____/ \___|\__\___|\___|\__|
   | |                                 
   |_|     

     Version 1.0 - Developed by xkingrohi           

Type{Fore.LIGHTBLUE_EX + " 'list'"}{Style.RESET_ALL} to see all commands                                                
            """
        print(banner)
        self.cmds()

    def main(self):
        self.screen()

if __name__ == "__main__":
    x = ipDetect(api_access, api_key)
    x.main()


