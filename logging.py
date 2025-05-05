import time
import os

class LogFTPDataError(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)

class LogBasicDataError(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)

class LogBasicData():
    """
        \'LogBasicData\' is a class for logging data in a single directory.
        
        It is designed to create log files based on the name for the log file(s), it will create new files when the log limit has been hit.

        For more information about what this class needs when called, check \'LogBasicData.__init__()\'

        Here is an example of how to use \'LogBasicData\':

            log_object = LogBasicData()
    """
    def __init__(self, folder_to_log_files:str, log_file_name:str, log_limit:int=0):
        """
            \'LogBasicData\' takes three arguments. Those are described below:
            
                folder_to_log_files:str = The path for log files to be held inside of.

                log_file_name:str = The name for log files, the format goes as follows; f\'{log_file_name}_{log_file_count}\' where the \'log_file_count\' is the number for a log file.

                log_limit:int = The amount of logs per file, if it is set to 0 or not declared, a new log file will be created every day, instead of after a certain amount of logs
        """
        if os.path.exists(folder_to_log_files):
            if os.path.isdir(folder_to_log_files):
                self.LOG_DIRECTORY = folder_to_log_files
                self.LOG_FILE_NAME = log_file_name
                self.LOG_LIMIT = log_limit
                self.LOG_FILE_COUNT = 0
                self.WRITTEN_LOGS = 0
                self.CURRENT_LOG_FILE = f"{self.LOG_FILE_NAME}_{self.LOG_FILE_COUNT}"
            else:
                LogBasicDataError(f"Passed path for \'folder_to_log_files\': \'{folder_to_log_files}\' is not a directory.")
        else:
            raise LogBasicDataError(f"Passed path for \'folder_to_log_files\': \'{folder_to_log_files}\' does not exist.")
    
    def check_for_log_file_change(self):
        """
            \'check_for_log_file_change\' takes no arguments. It is not something that needs to be called directly.

            It returns True or False depending on if the log limit has been hit or passed.
        """
        if self.WRITTEN_LOGS >= self.LOG_LIMIT:
            return True
        return False

    def change_log_file(self):
        """
            \'change_log_file\' takes no arguments. It is not something that needs to be called directly.

            It changes the log file to have the new \'log_file_count\' added to the current name for log files.
        """
        self.LOG_FILE_COUNT = self.LOG_FILE_COUNT + 1
        self.CURRENT_LOG_FILE = f"{self.LOG_FILE_NAME}_{self.LOG_FILE_COUNT}"

    def change_log_folder(self, new_log_folder:str):
        if os.path.exists(new_log_folder):
            if os.path.isdir(new_log_folder):
                self.LOG_DIRECTORY = new_log_folder
            else:
                raise LogBasicDataError(f"Passed path for \'new_log_folder\': \'{folder_to_log_files}\' is not a directory.")
        else:
           raise LogBasicDataError(f"Passed path for \'new_log_folder\': \'{folder_to_log_files}\' is not a directory.")

    def log_data(self, data_to_log:str):
        if self.check_for_log_file_change():
            self.change_log_file()
        try:
            with open(os.path.join(self.LOG_DIRECTORY, self.CURRENT_LOG_FILE), 'a') as file:
                file.write(f"Loged data {time.strftime('%H:%M:%S-%m%d%y', time.localtime(time.time()))}: {data_to_log}\n")
                file.close()
            self.WRITTEN_LOGS + 1
        except Exception as error:
            raise LogBasicDataError(f"log_data raised error \'{error}\' when writing \'{data_to_log}\' to log file \'{self.CURRENT_LOG_FILE}\'")
        finally:
            pass

class LogFTPData():
    """
        LogFTPData is a class for logging data, wow.
        
        But in all reality, its nothing too great, having few methods that can be used.
        
        While designed for Windows using the \'C:\\Program Files\\Errox_FTP-Pot\\logs\\\' directory for logs
        
        Housing the \'check_time\', \'change_loging_level\', \'change_log_file\', \'log_data\' and basic constructor methods, LogFTPData is 100% autonomous, needing only a directory to place the logs into (and being called inside of a script (duh))

        For information on how to use \'LogFTPData()\' read the description of \'LogFTPData.__init__()\'.
    """

    def check_time(self, last_day:int):
        """
            \'check_time\' checks the current date in the form of numeric day to see if it\'s a new day, in which case it will call \'change_log_file\' after creating the new log file.

            The reason that this method exists, is so that one file isnt too large, and instead you can archive data day by day for not only ease of categorization, but also for less demand of YOUR computer when opening a log file.
        """
        while True:
            day = int(time.strftime('%d', time.localtime(time.time())))
            if day != self.CURRENT_LOG_DAY:
                new_log_file_path = f"C:\\Program Files\\Errox_FTP-Pot\\logs\\log-{time.strftime('%H:%M:%S-%m%d%y', time.localtime(time.time()))}.log"
                with open(new_log_file_path, 'w') as new_log_file:
                    new_log_file.write("\n")
                    new_log_file.close()
                    return day
                self.change_log_file(new_log_file_path)
            else:
                time.sleep(60)

    def change_loging_level(self, new_logging_level:int):
        """
            \'change_loging_level\' is a method used after \'LogFTPData\' is held inside of a variable, it is completely un-needed for most usecases.

            It works by changing the logging level for the LogFTPData object, it takes an int in the form of 1, 2, or 3, with each having an increase amount of logging.

            Below are what each \'level\' does:

                1) Only logs downloads, its useful to see who is accessing what and only that.

                2) Logs uploads and downloads, is the default setting if none is present when creating the LogFTPData object

                3) Logs connections, disconnections, and every action inside of the client session, its useful if you want to track everything like BigBrother

            If an invalid number is passed into this method, then the previous value will be used.
        """
        match new_logging_level:
            case self.LOGING_LEVEL:
                pass
            case 1:
                self.LOGING_LEVEL = 1
            case 2:
                self.LOGING_LEVEL = 2
            case 3:
                self.LOGING_LEVEL = 3
            case _:
                pass

    def change_log_file(self, new_log_file:str):
        """
            \'chanle_log_file\' is very simple, all it does is change the current self.LOG_FILE_PATH value.

            It is designed to be ran after \'LogFTPData\' so you can change the log file, keep in mind that when \'check_time\' is called, it will revert the naming scheme and path to default. If you want to avoid this, use this  method in base \'logging\' instead of the \'LogFTPData\' object.
        """
        if os.path.exists(os.path.dirname(new_log_file)):
            self.LOG_FILE_PATH = new_log_file

    def log_data(self, ip_to_log:str, port_to_log:int, type_of_command:dict, if_command_succeeded:bool):
        """
            \'log_data\' is used to open and write the data passed into the current log file. This method IS NOT TO BE CALLED DIRECTTLY OUTSIDE OF \'Errox_FTP(S)-Pot\', in which case you wish to call this method directly, swap from using the \'LogFTPData\' class object and instead use the method in base \'logging\'

            It writes in the sceme \'{current time}: {ip address to log}@{port to log} sent {type of command} with value of {command return value} that returned a {}\'

            The arguments are described below:

                ip_to_log:str = the ip address of client

                port_to_log:int = the port address that the client is using to connect through

                type_of_command:dict = the command and it\'s type, it has to be in this spesific format; {[\'type\']: type_of_command, [\'sucess\']: if_command_succeeded}

                if_command_succeeded:bool = true of false value of if the command worked on the honeypot and was a valid command / did the command work?
        """
        with open(self.LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"{time.time()}: {ip_to_log}@{port_to_log} sent a {type_of_command['type']} with with value of {type_of_command['sucess']} that returned a {if_command_succeeded}\n")
            log_file.close()

    def __init__(self, set_log_level:int=1):
        """
            \'LogFTPData\' is a method used to construct the object for all of the following methods inside of this object:
                \'check_time\', \'change_loging_level\', \'change_log_file\' and \'log_data\'.
            
            \'LogFTPData\' also takes one argument, that being \'set_log_level\' which is defaulted to 2, but if you want to know more about the logging levels, read the description of \'change_loging_level\'

            Basic coverage of each method and use case:
                
                \'check_time\' is a forever loop and designed to be used inside of a seperate thread or seperate process and will automatically call \'change_log_file\' using the default naming scheme.

                \'change_loging_level\' is designed to be called so that more or less data is storred inside of log files

                \'change_log_file\' is designed to automatically change the log file as to save device recources when opening a log file

                \'log_data\' is one of two methods for this object to call constantly, it simply adds data to the log file in a spesific way
        """
        self.LOG_FILE_PATH = f"C:\\Program Files\\Errox_FTP-Pot\\logs\\log-{time.strftime('%H:%M:%S-%m%d%y', time.localtime(time.time()))}.log"
        match set_log_level:
            case 1:
                self.LOGING_LEVEL = 1
            case 2:
                self.LOGING_LEVEL = 2
            case 3:
                self.LOGING_LEVEL = 3
            case _:
                self.LOGING_LEVEL = 2
