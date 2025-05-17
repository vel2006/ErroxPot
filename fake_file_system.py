import hashlib
import json
import os
class FakeFileSystemError(Exception):
    def __init__(self, message):
        super().__init__(message)
class FileSystem():
    """
        Add \'.__init__()\' to see information about the \'FileSystem()\' object and its methods.
    """
    def add_directory(self, target_directory:str, higher_directories:list):
        """
            \'add_directory\' is a method for adding a logical directory to the current fake file system
            This is used when creating a new blank directory, below is an explination of the arguments:

            \"target_directory\";
                Name of the directory to add, this has to be a string and will be the logical name of the directory for the file system.
                A \'/\' is added to the name of the directory, so PLEASE ommit the forward slash \'/\'
            
            \"higher_directories\";
                A list of keys (precursing directories) that will lead to the new directory in the file system
            
            Below is an example of how to call this function:

            obj.add_directory(\"new_folder\", ["/", "home/", "that1ethicalhacker/", "Desktop/"])
        """
        path = self.FILES[higher_directories[0]]
        directories = higher_directories[1:]
        for key in directories:
            path = path[key]
        print(f"directory {target_directory} has last one as: {higher_directories[-1]}")
        path[f"{target_directory}"] = {
            "..":higher_directories[-1],
            ".":target_directory
            }
    def add_file(self, file_name:str, file_data:list, higher_directories:list):
        """
            \'add_file\' is a method for adding a logical file to the current fake file system
            This is used when adding a file to the fake file system and including it\'s data
            Below is an explination of the arguments:

            \"file_name\";
                Name of the file to add, this has to be a string and will be the logical name for the file
            
            \"file_data\";
                A list of the file\'s data, below is an explination of how to format the list:
                    [10000, "C:\\Users\\Public\\Destop\\file.txt"]
                       ^                        ^
                       |                        |
                       |                        |- Path to the file in the host computer\'s file system
                       |
                       |- Size of the file in bytes
            
            \"higher_directories\";
                A list of keys (precursing directories) that will lead to the new directory in the file system
            
            Below is an example of how to call this function:
            
            obj.add_file(\"file.txt\", [1000, \"C:\\Users\\that1ethicalhacker\\Desktop\\file.txt\"], ["/", "home/", "that1ethicalhacker/", "Desktop/"])
        """
        path = self.FILES[higher_directories[0]]
        higher_directories = higher_directories[1:]
        for key in higher_directories:
            path = path[key]
        path[file_name] = file_data
    def get_file_data(self, file_name:str, path_to_file:list):
        """
            \'get_file_data\' is a method for getting the information stored about a logical file

            Below is an explination of arguments:

            \"file_name\";
                The wanted file\'s name, must be the same as what is stored in the fake file systm

            \"path_to_file\";
                A list of keys (precursing directories) that will lead to the new directory in the fake file system
            
            Below is an example of how to call this function:
            
            data = obj.get_file_data("file.txt", ["/", "home/", "that1ethicalhacker/", "Desktop/"])
        """
        return self.FILES[path_to_file][file_name]
    def add_directory_to_file_system(self, target_directory:str, item_fake_path:str):
        """
            WARNING: THIS FUNCTION IS NOT DESIGNED TO BE DIRECTLY CALLED VIA ANY API INTERFACE, IT IS TO RUN WITHIN THE \'__init__\' FUNCTION

            \'dive_into_directory\' is a method for scraping files and directories inside of a provided directory

            This version is designed to work with the fake file system that \'FileSystem\'s \'__init__\' creates. If the \'__init__\' has not been ran, this method will encounter an error and likely crash.

            For usage, follow the arguments below:

                \"target_directory\";
                    The directory to search / scrape. This argument has to be a folder\'s full path, or the method will enounter an error and likely crash.

                \"item_fake_path\";
                    The fake path to the passed directory for the \'target_directory\' argument. This is the path that the user will be shown instead of the file\'s actual path.
            
            Example usage:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                system.dive_into_directory(\"C:\\Users\\<user>\\Documents\\FakeFiles\\fake_logs\", \'logs\\')
        """
        if os.path.exists(target_directory) and os.path.isdir(target_directory):
            print(f"[i] Starting conversion of directory: \'{target_directory}\'")
            directorys = []
            with os.scandir(target_directory) as entries:
                for item in entries:
                    if item.is_file():
                        self.add_file(item.name, [item.stat().st_size, item.path], item_fake_path)
                    elif item.is_dir():
                        self.add_directory(item.name, item_fake_path)
                        directorys.append([item.path, [item_fake_path, item.name]])
                entries.close()
            while True:
                if len(directorys) != 0:
                    to_remove = []
                    for entry in directorys:
                        with os.scandir(entry[0]) as entries:
                            for item in entries:
                                if item.is_file():
                                    self.add_file(item.name, [item.stat().st_size, item.path], entry[1])
                                elif item.is_dir():
                                    self.add_directory(item.name, entry[-1])
                                    fake_path = entry[1]
                                    fake_path.append(item.name)
                                    directorys.append([item.path, fake_path])
                            entries.close()
                        to_remove.append(entry)
                    for entry in to_remove:
                        directorys.remove(entry)
                else:
                    break
        print("[i] All directories and files loaded!")
    def save_file_system(self):
        """
            \'save_file_system\' will work to save the current FILES variable for later usage or for backing up the current system.

            It takes no arguments, and returns nothing due to it simply saving the data to files.
            If an error is encountered, a FakeFileSystemError is raised
        """
        file_system = json.dumps(self.FILES)
        with open("saved_output.filesys", "w") as file_handle:
            file_handle.write(file_system)
            file_handle.close()
        with open("saved_output_hash.filesys", "w") as file_handle:
            hasher = hashlib.sha256()
            hasher.update(bytes(file_system, 'utf-8'))
            file_handle.write(f"{hasher.hexdigest()}")
            file_handle.close()
    def load_saved_file_system(self, file_system_path:str, file_system_hash_path:str):
        """
            WARNING: THIS FUNCTION IS NOT DESIGNED TO BE DIRECTLY CALLED VIA ANY API INTERFACE, IT IS TO RUN WITHIN THE \'__init__\' FUNCTION

            \'load_saved_file_system\' will work by loading the requested file system into the current FileSystem object

            Below is an explination of it\'s arguments:

                \"file_system_path\";
                    Path to the file holding the saved file system file, by default it is called \'saved_output.filesys\'
                
                \"file_system_hash_path\";
                    Path to the file holding the saved file system file\'s hash, by default it is called \'saved_output_hash.filesys\'
                    This is crutial to ensure that tampering with the file system by an idiot Junior dev does not go wrong, and if someone wants to mess with your honeypot they would have to overwrite the saved hash and saved file system
        """
        hash = ""
        with open(file_system_hash_path, 'r') as file_handle:
            hash = file_handle.read()
            file_handle.close()
        with open(file_system_path, 'r') as file_handle:
            file_system = json.load(file_handle)
            file_handle.close()
        hasher = hashlib.sha256()
        hasher.update(bytes(json.dumps(file_system), 'utf-8'))
        if hasher.hexdigest() != hash:
            raise FakeFileSystemError("[!] CRITICAL ERROR: SAVED FILE SYSTEM DOES NOT MATCH LOADED FILE SYSTEM HASH!")
        else:
            self.FILES = file_system
            print("[i] Loaded saved file system with no issues!")
    def __init__(self, custom_file_system:str, uploaded_file_directory:str, log_file_directory:str, saved_file_system:str=None, saved_file_hash:str=None):
        """
            \'FileSystem\' is an object that holds information about a fake file system used in honeypots and other cases.

            Below is an explination of each argument:

                \"custom_file_system\";
                    Path to a directory holding the real files and directoies to be used inside of the fake file system

                \"uploaded_file_directory\";
                    Path to a directory which will hold uploaded files from the honey-pot, it is suggested that this is an isolated directory or drive
                
                \"log_file_directory\";
                    Path to a directory which will hold log files containing information about events within the fake file system
                
                \"saved_file_system\";
                    Path to a file holding a system which was created by a \'FileSystem\' object\'s \"save_file_systen\" function
                
                \"saved_file_hash\";
                    Path to a file holding the hash for the saved file system \'saved_file_system\' argument

            \'FileSystem\' (can and will likely have) a very slow \'start\' due to it loading the entire file system if not using a saved file system

            Here is an example of it being used with using a saved file system:

                file_system = FileSystem(None, None, None, \"C:\\Program Files\\ErroxPot\\fake_system\\custom_system.filesys\", \"C:\\Program Files\\ErroxPot\\fake_system\\system_hash.filesys\")
            
            Here is an example of it being used without using a saved file system:

                file_ystem = FileSystem(\"C:\\Program Files\\ErroxPot\\fake_system\", \"C:\\Program Files\\Sandbox\", \"C:\\Program Files\\ErroxPot\\Logs\", None, None)
        """
        if saved_file_system is None:
            if os.path.exists(custom_file_system) and os.path.exists(custom_file_system):
                if os.path.exists(uploaded_file_directory) and os.path.isdir(uploaded_file_directory):
                    if os.path.exists(log_file_directory) and os.path.isdir(log_file_directory):
                        self.PATH_TO_FAKE_FILES = custom_file_system
                        self.PATH_TO_SAVE_FILES = uploaded_file_directory
                        self.CWD = ["/"]
                        self.FILES = {
                            "/":{}
                            }
                        self.add_directory_to_file_system(custom_file_system, "/")
                    else:
                        raise FakeFileSystemError("Proveded Path to Directory \'log_file_directory\' Is Not A Directory")
                else:
                    raise FakeFileSystemError("Provided Path to Directory \'uploaded_file_directory\' Is Not A Directory.")
            else:
                raise FakeFileSystemError("Provided Path to Directory \'custom_file_system\' Is Not A Directory.")
        else:
            if os.path.exists(saved_file_system) and os.path.isfile(saved_file_system):
                if os.path.exists(saved_file_hash) and os.path.isfile(saved_file_hash):
                    self.load_saved_file_system(saved_file_system)
                else:
                    raise FakeFileSystemError("Privided Path to \'saved_file_hash\' Is Not A Vaild File")
            else:
                raise FakeFileSystemError("Provided Path to \'saved_file_system\' Is Not A Vaid File")
    def get_current_directory(self):
        """
            \'get_current_directory\' is very simple and simply returns the CWD class variable
        """
        return self.CWD
    def change_current_directory(self, new_directory:str):
        """
            \'change_current_directory\' will change the current fake file system depth to reflect the simulated space within the file system.

            Below is an explination of it\'s arguments:

                \"new_directory\";
                    The directory that will become the new current directory. Must be within the current directory, to go back one use \'..\'
        """
        if new_directory == ".." and self.CWD[-1] != "/":
            self.CWD = self.CWD[:-2]
        path = self.FILES[self.CWD[0]]
        for i in self.CWD[1:]:
            path = path[i]
        if new_directory not in path.keys():
            return "Doesnt exist."
        self.CWD.append(new_directory)
    def list_current_directory_all(self) -> dict:
        """
            \'list_current_directory_all\' will list every bit of information about each file and directory within the current fake directory.

            It takes no arguments but returns a dictionary
        """
        path = self.FILES[self.CWD[0]]
        higher_directories = self.CWD[1:]
        for key in higher_directories:
            path = path[key]
        return path
    def list_current_directory_items(self) -> dict:
        """
            \'list_current_directory_items\' will list only the name of each file and directory within the current fake directory.

            This function is very similar to \'list_current_directory_all\' except for the increase in call time due to filtering the output

            It takes no arguments but returns a dictionary.
        """
        path = self.FILES[self.CWD[0]]
        higher_directories = self.CWD[1:]
        for key in higher_directories:
            path = path[key]
        items = []
        for item in path.keys():
            items.append(item)
        return items
