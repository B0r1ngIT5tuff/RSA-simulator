from rsa_algo import pub_keygen, priv_keygen, encrypt_m, decrypt_m
import colorama, os, json, time

# I define the colors for the CLI
colorama.init()
red = colorama.Fore.RED
cyan = colorama.Fore.CYAN
white = colorama.Fore.WHITE
blue = colorama.Fore.BLUE
green = colorama.Fore.GREEN
magenta = colorama.Fore.MAGENTA

def write_to_JSON(n,c,d):

    '''
        This function writes 'data' in the 'filename.json' file.

        Parameters: 
        - n, is a very big prime number which is the first part of the public key.
        - c, is a list containing all crypted chars of the text.
        - d, is the private key, it's used to decrypt the ecnrypted text.

        write_to_JSON(n, c, d) -> (None)
    '''

    data = {
        "Message":c,
        "Pub key":n,
        "Priv key":d
    }

    f_name = input("What's the name of the file? ")

    # It creates the crypted_messages folder if not already present
    crypted = os.listdir(os.path.curdir)
    if "crypted_messages" not in crypted:
        
        os.mkdir("crypted_messages")

        # I open 'filename.json' in write mode and I write in it 'data'.
        with open(os.path.realpath(f"crypted_messages/{f_name}" + ".json"),"w") as f:
            json.dump(data,f, indent= 4, sort_keys=True)
    else:
        with open(os.path.realpath(f"crypted_messages/{f_name}" + ".json"),"w") as f:
            json.dump(data,f, indent= 4, sort_keys=True)
    

def read_from_JSON():
    '''
        This function ask the user wihich JSON file he wants to choose, then 
        the crypted message saved in the file is read and decrypted.

        Parameters: None.

        read_from_JSON() -> (int: c, int: n ,int: d ,bool: err)

        - err, is a boolean value that indicates if the 'crypted_messages' folder contains any files.
    '''
    loop = True

    # This loop is used to visualize the cli interface to choose the desired file.
    while loop == True:
       
        os.system("clear" if os.name == "posix" else "cls")

        print(f"{red}Files:\n{white}")

        # I obtain all the JSON file names in the folder and save them in dir_json (list of names)
        dir_json = os.listdir(os.path.realpath("crypted_messages"))
        
        # If dir_json has lenght = 0, then there's no file, it will be returned the True value to the cli_menu function.
        if len(dir_json) == 0:
            print("Sorry, but there isn't any file :-(")
            time.sleep(1.5)
            return None, None, None, True
        else:
            # I print every name in dir_json.
            for j in dir_json:
                print(j, end=" ")
            print("\n")
        
            file = input(f"{blue}Choose a file (filename.json): {white}")

            # If the file is in the list, loop = False.
            if file in dir_json:
                loop = False

            # I open the selected JSON file in read mode, the content of the file is inerpreted as a 'dict' with the 'object_hook' parameter. 
            with open(os.path.realpath(f"crypted_messages/{file}"), "r") as f:
                values = json.load(f, object_hook=dict)
                c = values["Message"]
                n = values["Pub key"]
                d = values["Priv key"]

            return c, n, d, False


def cli_menu():
    '''
        This function implements the terminal interface for the program.
    '''
    # This clears every text in the cli with the 'clear' command on Unix-based systems, the 'cls' command is for Windows.
    os.system("clear" if os.name == "posix" else "cls")
    print(f"{cyan}RSA ALGORTIHM SIMULATOR{white} (made by B0r1ngIt5tuff)\n")

    print("Options:\n")
    
    print(f"{magenta}1) {white}Encrypt a message which will be saved on a JSON file.")
    print(f"{magenta}2) {white}Decrypt a messagge which was saved on a JSON file previously.")
    print(f"{magenta}3) {white}Exit.\n")

    res = int(input(f"{red}>{blue}>{green}>{white} "))

    if res == 1:

        # The first option encrypts the message and it saves the message on a JSON file.
        mex = input("Insert a message to encrypt: ")
        print(f"Encrypting the message...\n")
        exp, n_mod, phin = pub_keygen()
        d = priv_keygen(exp, phin)
        remainder = encrypt_m(mex, exp, n_mod)
        write_to_JSON(n_mod,remainder,d)
        print("Done, the crypted message was saved correctly. Take a look in the 'crypted_messages/' directory.")
        time.sleep(3)

        return True
    
    elif res == 2:
        '''
            The second option will return a list of the JSON files in 'crypted_messages',
            the user will choose from ehich file he wants to decrypt a message.
        '''
        c, n ,d ,err = read_from_JSON()

        if err == True and c == None and n == None and d == None:
            return True

        else:

            m = decrypt_m(c, d, n)
            mex = ""
            print(f"That's the original message: \n")
            
            for letter in m:
                mex += letter

            print(mex)        

            time.sleep(3)
            return True

    elif res == 3:
        return False


def main():
    loop = True
    while loop == True:
        
        loop = cli_menu()
        
if __name__ == "__main__":
    main()
