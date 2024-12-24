import os
# try:
#     from colorama import Fore, init
# except ImportError:
#     import subprocess
#     import sys
#     print("colorama is not installed. Installing...")
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
#     from colorama import Fore, init  # Спробуємо імпортувати знову після встановлення
from colorama import Fore, init
init()

#e

class DATABASE:
    def __init__(self, db_file):
        self.logS = "NONE"
        self.fileType = db_file.split('.')[1]
        self.fileName = db_file.split('.')[0]

    def LogType(self, Type):
        if Type == "BASE" or Type == "COLORFUL" or Type == "NONE":
            self.logS = Type
        else:
            raise Exception(Fore.RED + f"logS type cannot be: '{Fore.RESET}{Fore.BLUE}{Type}{Fore.RESET}{Fore.RED}'. Only '{Fore.RESET}BASE{Fore.RESET}{Fore.RED}', '{Fore.RESET}{Fore.YELLOW}COLORFUL{Fore.RESET}{Fore.RED}' or '{Fore.RESET}{Fore.LIGHTBLACK_EX}NONE{Fore.RESET}{Fore.RED}'") 
            #print(Fore.RED + f"logS state cannot be: '{Fore.RESET}{Fore.BLUE}{State}{Fore.RESET}{Fore.RED}'. Only '{Fore.RESET}BASE{Fore.RESET}{Fore.RED}', '{Fore.RESET}{Fore.YELLOW}COLORFUL{Fore.RESET}{Fore.RED}' or '{Fore.RESET}{Fore.LIGHTBLACK_EX}NONE{Fore.RESET}{Fore.RED}'") 
            

    def CreateDatabase(self):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, self.fileName)
        
        if os.path.exists(f"{self.fileName}.{self.fileType}"):
            if self.logS == 'BASE':
                print(f"Database: '{self.fileName}' exists")
            elif self.logS == 'COLORFUL':
                print(Fore.GREEN + f"Database: '{Fore.RESET}{Fore.BLUE}{self.fileName}{Fore.RESET}{Fore.GREEN}' exists")
            return file_path
        else:
            f = open(f"{self.fileName}.{self.fileType}", "x")
            if self.logS == 'BASE':
                print(f"Database: {self.fileName} was created")
                return file_path
            elif self.logS == 'COLORFUL':
                print(Fore.GREEN + f"Database: '{Fore.RESET}{Fore.BLUE}{self.fileName}{Fore.RESET}{Fore.GREEN}' was created")
                return file_path
            else:
                return file_path
            



    def WriteDatabase(self, information, cell):

        if os.path.exists(f"{self.fileName}.{self.fileType}"):

            information_str = list(map(str,information))
            index = 0
            with open(f"{self.fileName}.{self.fileType}", "r") as f:
                lines = f.readlines()
            with open(f"{self.fileName}.{self.fileType}", "w") as f:

                if self.logS == 'BASE':
                    print(Fore.RESET + f"Database file '{self.fileName}.{self.fileType}' Writing...")
                elif self.logS == 'COLORFUL':
                    print(Fore.RED + f"Database file '{self.fileName}.{self.fileType}' Writing... {Fore.RESET}")

                lines = [line for line in lines if not line.startswith(str(cell))]

                for cs in information_str:
                    lines.append(f"{str(cell)}|{index}|{cs}|{str(cell)}|{index}\n")
                    index += 1
                f.writelines(lines)
                index = 0
                
        else:
            self.CreateDatabase()
            self.WriteDatabase(information,  cell)





    def ReadDatabase(self, cell, index=None):
        ret = []
        if os.path.exists(f"{self.fileName}.{self.fileType}"):
            try:
                with open(f"{self.fileName}.{self.fileType}", "r") as f:
                    lines = f.readlines()
            except FileNotFoundError:
                lines = []

            if index == None or index == 'ALL':
                for line in lines:
                    indexes = line.split('|')
                    if indexes[0] == str(cell):
                        ret.append(indexes[2]) 
                return ret
            else:
                for line in lines:
                    indexes = line.split('|')
                    if indexes[0] == str(cell):
                        if indexes[1] == str(index):
                            return indexes[2]
            if self.logS == 'BASE':
                print(Fore.RESET + f"Database file '{self.fileName}.{self.fileType}' Reading...")
            elif self.logS == 'COLORFUL':
                print(Fore.RED + f"Database file '{self.fileName}.{self.fileType}' Reading... {Fore.RESET}")
        

        else:
            return 'DB was not found!'







    def DeleteDatabase(self):
        DATABASE_PATH = f"{self.fileName}.{self.fileType}"

        if os.path.exists(DATABASE_PATH): 
            try:
                os.remove(DATABASE_PATH)
                if self.logS == 'BASE':
                    print(Fore.RESET + f"Deleting database >> {self.fileName}")
                elif self.logS == 'COLORFUL':
                    print(Fore.RED + f"Deleting database >> {self.fileName}{Fore.RESET}")

            except OSError as e:
                print(f"Error: {e.strerror}")
        else:

            if self.logS == 'BASE':
                print(Fore.RESET + f"Database file '{self.fileName}.{self.fileType}' was not found!")
            elif self.logS == 'COLORFUL':
                print(Fore.RED + f"Database file '{self.fileName}.{self.fileType}' was not found! {Fore.RESET}")

    
    def RenameDatabase(self, newFileName):

        if os.path.exists(f"{self.fileName}.{self.fileType}"):
            if not os.path.exists(f"{newFileName}.{self.fileType}"):

                if self.logS == 'BASE':
                    print(Fore.RESET + f"Database file '{self.fileName}.{self.fileType}' Renaming!!!")
                elif self.logS == 'COLORFUL':
                    print(Fore.RED + f"Database file '{Fore.GREEN}{self.fileName}.{self.fileType}{Fore.RED}' Renaming!!! {Fore.RESET}")

                open(f"{newFileName}.{self.fileType}", "x")
                f = open(f"{self.fileName}.{self.fileType}", "r")
                with open(f"{newFileName}.{self.fileType}", "w") as dt2:
                    dt2.writelines(f)

                if self.logS == 'BASE':
                    print(Fore.RESET + f"Database file '{self.fileName}.{self.fileType}' Renaming completed!!! New name >> {newFileName}.{self.fileType}")
                elif self.logS == 'COLORFUL':
                    print(Fore.RED + f"Database file '{Fore.GREEN}{self.fileName}.{self.fileType}{Fore.RED}' Renaming completed!!! New name >> {Fore.GREEN}{newFileName}.{self.fileType}{Fore.RESET}")

                f.close()
                DATABASE_PATH = f"{self.fileName}.{self.fileType}"
                os.remove(DATABASE_PATH)
            
            else:
                if self.logS == 'BASE':
                    print(Fore.RESET + f"Database file >> '{newFileName}.{self.fileType}' exists. Deleting...")
                elif self.logS == 'COLORFUL':
                    print(Fore.RED + f"Database file >> '{Fore.GREEN}{newFileName}.{self.fileType}{Fore.RED}' exists. Deleting... {Fore.RESET}")

                DATABASE_PATH = f"{newFileName}.{self.fileType}"
                os.remove(DATABASE_PATH)
                self.RenameDatabase(self.fileName, newFileName)
            self.fileName = newFileName
        else:
            if self.logS == 'BASE':
                print(Fore.RESET + f"Database file >> '{self.fileName}.{self.fileType}' does not exist.")
            elif self.logS == 'COLORFUL':
                print(Fore.RED + f"Database file >> '{Fore.GREEN}{self.fileName}.{self.fileType}{Fore.RED}' does not exist. {Fore.RESET}")


    # def Change_File_Type(self, fileName, NewfileType):#
        
    #     if NewfileType != self.fileType:
    #         if fileName != "":
                
    #             old_file_path = f"{fileName}.{self.fileType}"
    #             new_file_path = f"{fileName}.{NewfileType}"

    #             if os.path.exists(old_file_path):
    #                 if self.logS == 'BASE':
    #                     print(Fore.RESET + f"Database file '{old_file_path}' Renaming!!!")
    #                 elif self.logS == 'COLORFUL':
    #                     print(Fore.RED + f"Database file '{Fore.GREEN}{old_file_path}{Fore.RED}' Renaming!!! {Fore.RESET}")


    #                 with open(old_file_path, "r") as f:
    #                     content = f.read()
    #                 with open(new_file_path, "w") as new_file:
    #                     new_file.write(content)


    #                 os.remove(old_file_path)
    #                 self.fileType = NewfileType
                 

    #                 if self.logS == 'BASE':
    #                     print(Fore.RESET + f"Database file '{old_file_path}' Renaming complete!!! New name >> {new_file_path}")
    #                 elif self.logS == 'COLORFUL':
    #                     print(Fore.RED + f"Database file '{Fore.GREEN}{old_file_path}{Fore.RED}' Renaming complete!!! New name >> {Fore.GREEN}{new_file_path}{Fore.RESET}")

                    
    #             else:
    #                 if self.logS == 'BASE':
    #                     print(Fore.RESET + "The original file does not exist")
    #                 elif self.logS == 'COLORFUL':
    #                     print(Fore.BLUE + "The original file does not exist")
    #         else:
    #             self.fileType = NewfileType
    #             if self.logS == 'BASE':
    #                 print(Fore.RESET + "The File is reseted")
    #             elif self.logS == 'COLORFUL':
    #                 print(Fore.BLUE + "The File is reseted")
    #     else:
    #         if self.logS == 'BASE':
    #             print(Fore.RESET + "The file type is already the same")
    #         elif self.logS == 'COLORFUL':
    #             print(Fore.BLUE + "The file type is already the same")