from logging import LogBasicData
import threading
import os
import re
class FakeFileSystemError(Exception):
    def __init__(self, message):
        super().__init__(message)
class FileSystem():
    """
        Add \'.__init__()\' to see information about the \'FileSystem()\' object and its methods.
    """
    def dive_into_directory(self, target_directory:str, item_fake_path:str):
        """
            \'dive_into_directory\' is a method for scraping files and directories inside of a provided directory, it is ran by the \'__init__\' method for a \'FileSystem\' object. Is not designed to be called externally.

            This version is designed to work with the fake file system that \'FileSystem\'s \'__init__\' creates. If the \'__init__\' has not been ran, this method will encounter an error and likely crash.

            For usage, follow the arguments below:

                target_directory:str = The directory to search / scrape. This argument has to be a folder\'s full path, or the method will enounter an error and likely crash.

                item_fake_path:str = The fake path to the passed directory for the \'target_directory\' argument. This is the path that the user will be shown instead of the file\'s actual path.
            
            Example usage:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                system.dive_into_directory(\"C:\\Users\\<user>\\Documents\\FakeFiles\\fake_logs\", \'/logs\')
        """
        items = os.listdir(target_directory)
        threads = []
        # Example of how files works: self.FILES[f"{item_fake_path}/{item}"] = (os.path.join(target_directory, item), 'directory', item)
    def __init__(self, path_to_fake_file_directory:str, path_to_save_uploaded_files:str, path_to_save_logs:str):
        """
            \'FileSystem\' is an object that holds information about a fake file system used in honeypots and other cases.

            It takes two arguments, those being the path to files that will be used in the honeypot, and the path to where uploaded files will be held.

            It is designed that both passed arguments have to be directories, and will return an error if they are not.

            \'FileSystem\' (can have) a very slow \'start\' due to it calling \'dive_into_directory\' for the passed directory holding files for the honeypot (For more information of how \'dive_into_directory\' works, check it\'s description) so it is not advised to create a new object due to a new user or new connection.

            Here is an example of it being used:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
        """
        if os.path.exists(path_to_fake_file_directory):
            if os.path.isdir(path_to_fake_file_directory):
                if os.path.isdir(path_to_save_uploaded_files):
                    self.PATH_TO_FAKE_FILES = path_to_fake_file_directory
                    self.PATH_TO_SAVE_FILES = path_to_save_uploaded_files
                    self.PROCESS_LIMIT = 10
                    self.PROCESSES = []
                    self.THREAD_LIMIT = 20
                    self.THREADS = []
                    self.THREAD_LOCK = threading.Lock()
                    self.CWD = "/"
                    files = os.listdir(self.PATH_TO_FAKE_FILES)
                    self.LOGING_ERROR = LogBasicData(path_to_save_logs, "log_instance_", 10)
                    self.FILES = {}
                    for item in files:
                        if os.path.isdir(os.path.join(self.PATH_TO_FAKE_FILES, item)):
                            self.FILES[item] = (os.path.join(self.PATH_TO_FAKE_FILES, item), 'directory')
                            if len(self.THREADS) < self.THREAD_LIMIT:
                                thread_handle = threading.Thread(target=self.dive_into_directory, args=(os.path.join(self.PATH_TO_FAKE_FILES, item), f"/{item}"))
                                self.THREADS.append(thread_handle)
                            else:
                                for process in self.PROCESSES:
                                    try:
                                        if process.is_alive():
                                            pass
                                        else:
                                            process.join()
                                    except Exception:
                                        pass
                                    finally:
                                        pass
                                for thread in self.THREADS:
                                    try:
                                        if thread.is_alive():
                                            pass
                                        else:
                                            thread.join()
                                    except Exception:
                                        pass
                                    finally:
                                        pass
                                process_handle = multiprocessing.Process(target=self.dive_into_directory, args=(os.path.join(self.PATH_TO_FAKE_FILES, item), f"/{item}"))
                                self.PROCESSES.append(process_handle)
                        else:
                            try:
                                with open(os.path.join(self.PATH_TO_FAKE_FILES, item), 'rb') as file:
                                    file_contents = file.read()
                                    self.FILES[f"/{item}"] = (os.path.join(self.PATH_TO_FAKE_FILES, item), file_contents)
                                    file.close()
                            except Exception as error:
                                print(f"Error with reading file {os.path.join(self.PATH_TO_FAKE_FILES, item)}, returned with error: {error}")
                                print("Excluding from FakeFileSystem.")
                else:
                    raise FakeFileSystemError("Provided Path to Directory Holding Uploaded Files Is Not Directory.")
            else:
                raise FakeFileSystemError("Provided Path to Directory Holding Fake Files Is Not Directory.")
        else:
            raise FakeFileSystemError("Provided Path to Directory Holding Files For Fake Filesystem Does Not Exist.")
    def get_fake_working_directory(self):
        """
            \'get_fake_working_directory\' takes no arguments, and simply returns the current fake directory that is currently in use by the client.

            It is designed in such a way that you have to call it from a \'FileSystem\' object as shown below:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                client_current_directory = system.get_fake_working_directory()
        """
        return self.CWD
    def change_fake_working_directory(self, new_fake_working_directory:str):
        """
            \'change_fake_working_directory\' takes one argument, that being the path to change the client\'s fake directory into.

            It doesnt return a value if succeded, however, in the event that \'change_fake_working_directory\' failes it will return a \'FakeFileSystemError\' claiming that the directory passed was not found or is a file.
            This is due to how it works under the hood, instead of making a call to a real file, it instead checks for the wanted fake file inside of a dictionary that holds all of the current fake files / directories along with their data.

            It is designed in such a way that you have to call it from a \'FileSystem\' object as shown below:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                system.change_fake_working_directory(\'/logs\')
        """
        if new_fake_working_directory in self.FILES and self.FILES[new_fake_working_directory][1] == 'directory':
            self.CWD = new_fake_working_directory
        else:
            return FakeFileSystemError(f"Directory {new_fake_working_directory} was not found or is a file.")
    def upload_file(self, new_file_name:str, new_file_path:str, new_file_data:bytes):
        """
            \'upload_file\' takes three arguments, those being the name of the new file, the file\'s path in the fake file system this was called from, and the data inside of the file in bytes

            It returns either True or a \'FakeFileSystem\' error, the error will describe the issue in simple terms

            It is designed in such a way that you have to call if from a \'FileSystem\' object as shown below:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                system.upload_file(\'uploaded_file.txt\', \'/uploads\', b\'This is a file\\nI think\')
        """
        if new_file_name in self.FILES.keys():
            return FakeFileSystemError(f"File {new_file_name} already exists.")
        try:
            with open(os.path.join(self.PATH_TO_SAVE_FILES, new_file_name), 'wb') as file:
                file.write(new_file_data)
                file.close()
            self.FILES[new_file_path] = (os.path.join(self.PATH_TO_SAVE_FILES), new_file_data, new_file_name)
            return True
        except Exception as error:
            self.LOGING_ERROR.log_data(f"\'upload_file\' encountered error; {error}")
            return FakeFileSystemError(f"\'upload_file\' encountered error; \"{error}\"")
        finally:
            pass
        return True
    def remove_file(self, target_file_path:str):
        """
            \'remove_file\' takes one argument, that being the full path of the file to be removed.

            It checks the full path provided to see if the file exists and removes it if found.

            It retuns either True or a \'FakeFileSystem\' error, the error will describe the issue in simple terms

            It is designed in such a way that you have to call it from a \'FakeFileSystem\' object as shown below:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                system.remove_file(\'/uploads/uploaded_file.txt\')
        """
        if target_file_path not in self.FILES.keys():
            return FakeFileSystemError(f"File {target_file_path} does not exist.")
        try:
            self.FILES.pop(target_file_path)
        except Exception as error:
            self.LOGING_ERROR.log_data(f"\'upload_file\' encountered error; {error}")
            return FakeFileSystemError(f"\'remove_file\' encountered error; \"{error}\"")
        finally:
            pass
        return True
    def get_file_contents(self, file_path:str):
        """
            \'get_file_contents\' takes one argument, that being the path to a requested file inside of the fake file system.

            It returns the contents of the passed file in byte format (b\"this is\\ndata\\n\\tinside of a file\\n\")

            It is designed in such a way that you have to call it from a \'FileSystem\' object as shown below:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                example_file_contents = system.get_file_contents(\'example_file.txt\')
        """
        if file_path in self.FILES.keys() and self.FILES[file_path] != 'directory':
            return self.FILES[file_path][1]
        else:
            return FakeFileSystemError(f"File {file_path} does not exist or is directory.")
    def get_file_data(self, file_path:str):
        """
            \'get_file_data\' takes one argument, that being the path to a requested file inside of the fake file system.

            It returns the data held inside of a dictionary containing all data about each file in the fake file system created with \'FileSystem\'.

            It is designed in such a way that you have to call it from a \'FileSystem\' object as shown below:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                example_file_contents = system.get_file_data(\'example_file.txt\')
        """
        if file_path in self.FILES.keys() and self.FILES[file_path] != 'directory':
            return self.FILES[file_path]
        else:
            return FakeFileSystemError(f"File {file_path} does not exist or is directory.")
    def get_files_in_current_directory(self):
        """
            \'get_files_in_current_directory\' takes no arguments, it simply works off of the data held inside of the \'FileSystem\' object it is called from.

            It returns a list of the files inside of the client\'s current fake working directory (which can be found by using \'get_fake_working_directory\')

            It is designed in such a way that you have to call it from a \'FileSystem\' object as shown below:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                files_in_fake_directory = system.get_files_in_fake_working_directory()
        """
        files = []
        for item in self.FILES.keys():
            if self.CWD in item:
                files.append(item)
        return files
    def get_all_files(self):
        """
            \'get_all_files\' takes no arguments, it simply works off of the data held inside of the \'FileSystem\' object it is called from.

            It returns a tuple of all fake file paths within this object\'s instance, for more data on each file use \'get_file_contents\' and \'get_file_data\'.

            It is designed in such a way that you have to call it from a \'FileSystem\' object as shown below:

                system = FileSystem(\"C:\\Users\\<user>\\Documents\\FakeFiles\", \"C:\\Users\\<user>\\Documents\\UploadedFiles\")
                all_fake_files_directory = system.get_all_files()
        """
        return tuple(self.FILES.keys())
