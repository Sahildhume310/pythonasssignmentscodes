import psutil
import sys
import os
import time
import schedule
import smtplib
from email.message import EmailMessage


# ----------------------------------------------------------
# Function : Create Log File
# ----------------------------------------------------------

def CreateLog(FolderName):

    Border = "-" * 60

    # Check folder exists or not
    if os.path.exists(FolderName):

        if not os.path.isdir(FolderName):
            print("Unable to create folder")
            return None

    else:
        os.mkdir(FolderName)
        print("Directory created successfully")

    # Create log file name with timestamp
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    FileName = os.path.join(
        FolderName,
        "System_Surveillance_%s.log" % timestamp
    )

    print("Log file created :", FileName)

    # Open file
    fobj = open(FileName, "w")

    # ----------------------------------------------------------
    # Header
    # ----------------------------------------------------------

    fobj.write(Border + "\n")
    fobj.write("----------- Platform Surveillance System -----------\n")
    fobj.write("Log created at : " + time.ctime() + "\n")
    fobj.write(Border + "\n\n")

    # ----------------------------------------------------------
    # CPU Usage
    # ----------------------------------------------------------

    fobj.write("CPU Usage : %s %%\n" % psutil.cpu_percent())

    # ----------------------------------------------------------
    # RAM Usage
    # ----------------------------------------------------------

    mem = psutil.virtual_memory()

    fobj.write("RAM Usage : %s %%\n" % mem.percent)

    # ----------------------------------------------------------
    # Disk Usage
    # ----------------------------------------------------------

    fobj.write("\nDisk Usage Report\n")
    fobj.write(Border + "\n")

    for part in psutil.disk_partitions():

        try:
            usage = psutil.disk_usage(part.mountpoint)

            fobj.write(
                "%s -> %s %% used\n"
                % (part.mountpoint, usage.percent)
            )

        except:
            pass

    # ----------------------------------------------------------
    # Network Usage
    # ----------------------------------------------------------

    net = psutil.net_io_counters()

    fobj.write("\nNetwork Usage Report\n")

    fobj.write(
        "Sent : %.2f MB\n"
        % (net.bytes_sent / (1024 * 1024))
    )

    fobj.write(
        "Received : %.2f MB\n"
        % (net.bytes_recv / (1024 * 1024))
    )

    fobj.write(Border + "\n")

    # ----------------------------------------------------------
    # Process Information
    # ----------------------------------------------------------

    Data = ProcessScan()

    for info in Data:

        fobj.write("PID : %s\n" % info.get("pid"))
        fobj.write("Name : %s\n" % info.get("name"))
        fobj.write("UserName : %s\n" % info.get("username"))
        fobj.write("Threads : %s\n" % info.get("thread"))
        fobj.write("Status : %s\n" % info.get("status"))
        fobj.write("Start Time : %s\n" % info.get("create_time"))

        fobj.write(
            "CPU %% : %.2f\n"
            % info.get("cpu_percent")
        )

        fobj.write(
            "Memory %% : %.2f\n"
            % info.get("memory_percent")
        )

        fobj.write(
            "Open Files : %s\n"
            % info.get("open_files")
        )

        fobj.write(
            "RSS RAM : %.2f MB\n"
            % info.get("rss_mb", 0)
        )

        fobj.write(
            "VMS Memory : %.2f MB\n"
            % info.get("vms_mb", 0)
        )

        fobj.write(Border + "\n")

    # ----------------------------------------------------------
    # Top 10 Memory Processes
    # ----------------------------------------------------------

    fobj.write("\nTop 10 Memory Consuming Processes\n")
    fobj.write(Border + "\n")

    top10 = GetTop10Processes()

    for i in range(len(top10)):

        proc = top10[i]

        rank = i + 1

        fobj.write(
            f"Rank : {rank} | PID : {proc.get('pid')}\n"
        )

        fobj.write(
            "RSS : %.2f MB | VMS : %.2f MB | Memory %% : %.2f%%\n"
            % (
                proc.get("rss_mb", 0),
                proc.get("vms_mb", 0),
                proc.get("memory_percent", 0)
            )
        )

        fobj.write(Border + "\n")

    # ----------------------------------------------------------
    # End Section
    # ----------------------------------------------------------

    fobj.write("\n")
    fobj.write(Border + "\n")
    fobj.write("--------------- End Of Log File -------------------\n")
    fobj.write(Border + "\n")

    fobj.close()

    return FileName


# ----------------------------------------------------------
# Function : Scan Processes
# ----------------------------------------------------------

def ProcessScan():

    listprocesses = []

    # Warmup CPU calculation
    for proc in psutil.process_iter():

        try:
            proc.cpu_percent()

        except:
            pass

    time.sleep(0.2)

    # Actual process scan
    for proc in psutil.process_iter():

        try:

            info = proc.as_dict(
                attrs=[
                    "pid",
                    "name",
                    "username",
                    "status",
                    "create_time"
                ]
            )

            # Format create time
            try:

                info["create_time"] = time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.localtime(info["create_time"])
                )

            except:
                info["create_time"] = "NA"

            # Open files
            try:

                open_files_list = proc.open_files()

                open_file_count = len(open_files_list)

            except psutil.AccessDenied:
                open_file_count = "Access Denied"

            except psutil.NoSuchProcess:
                open_file_count = "Process Ended"

            except psutil.ZombieProcess:
                open_file_count = "NA"

            info["open_files"] = open_file_count

            # CPU %
            info["cpu_percent"] = proc.cpu_percent(None)

            # Memory %
            info["memory_percent"] = proc.memory_percent()

            # Threads
            info["thread"] = proc.num_threads()

            # Memory info
            mem_info = proc.memory_info()

            info["rss_mb"] = mem_info.rss / (1024 * 1024)

            info["vms_mb"] = mem_info.vms / (1024 * 1024)

            listprocesses.append(info)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            pass

    return listprocesses


# ----------------------------------------------------------
# Function : Get Top 10 Processes
# ----------------------------------------------------------

def GetTop10Processes():

    Data = ProcessScan()

    sorted_Data = sorted(
        Data,
        key=lambda x: x.get("memory_percent", 0),
        reverse=True
    )

    return sorted_Data[:10]


# ----------------------------------------------------------
# Function : Email Summary
# ----------------------------------------------------------

def GetEmailSummary():

    Data = ProcessScan()

    total = len(Data)

    sorted_cpu = sorted(
        Data,
        key=lambda x: x.get("cpu_percent", 0),
        reverse=True
    )

    top_cpu = sorted_cpu[0]

    sorted_mem = sorted(
        Data,
        key=lambda x: x.get("memory_percent", 0),
        reverse=True
    )

    top_mem = sorted_mem[0]

    sorted_thread = sorted(
        Data,
        key=lambda x: x.get("thread", 0),
        reverse=True
    )

    top_thread = sorted_thread[0]

    valid = []

    for p in Data:

        if isinstance(p.get("open_files"), int):
            valid.append(p)

    sorted_files = sorted(
        valid,
        key=lambda x: x.get("open_files", 0),
        reverse=True
    )

    top_openfiles = sorted_files[0] if valid else None

    summary = "System Summary\n\n"

    summary += "Total Processes : %s\n" % total

    summary += (
        "Top CPU : %s -> %s %%\n"
        % (
            top_cpu.get("name"),
            top_cpu.get("cpu_percent")
        )
    )

    summary += (
        "Top Memory : %s -> %s %%\n"
        % (
            top_mem.get("name"),
            top_mem.get("memory_percent")
        )
    )

    summary += (
        "Top Thread : %s -> %s threads\n"
        % (
            top_thread.get("name"),
            top_thread.get("thread")
        )
    )

    if top_openfiles:

        summary += (
            "Top Files : %s -> %s files\n"
            % (
                top_openfiles.get("name"),
                top_openfiles.get("open_files")
            )
        )

    return summary


# ----------------------------------------------------------
# Function : Send Mail
# ----------------------------------------------------------

def Marvellous_send_mail(
    sender,
    app_password,
    receiver,
    subject,
    body,
    attachment_path
):

    msg = EmailMessage()

    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.set_content(body)

    # Attachment
    with open(attachment_path, "rb") as Efobj:

        file_data = Efobj.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="octet-stream",
        filename=os.path.basename(attachment_path)
    )

    # SMTP connection
    smtp = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    )

    smtp.login(sender, app_password)

    smtp.send_message(msg)

    smtp.quit()

    print("Mail sent successfully")


# ----------------------------------------------------------
# Function : Send Email Periodically
# ----------------------------------------------------------

def SendEmailPerodically(Foldername, receiver):

    log_file = CreateLog(Foldername)

    summary = GetEmailSummary()

    sender_email = "YOUR_EMAIL@gmail.com"

    app_password = "YOUR_APP_PASSWORD"

    subject = "System Report - " + time.ctime()

    Marvellous_send_mail(
        sender_email,
        app_password,
        receiver,
        subject,
        summary,
        log_file
    )


# ----------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------

def main():

    Border = "-" * 60

    print(Border)
    print("----------- Platform Surveillance System -----------")
    print(Border)

    # ----------------------------------------------------------
    # HELP
    # ----------------------------------------------------------

    if len(sys.argv) == 2:

        if sys.argv[1] in ["--h", "--H"]:

            print("This script is used to : ")
            print("1 : Create Automatic Logs")
            print("2 : Execute Periodically")
            print("3 : Send Mail with Log")
            print("4 : Monitor Processes")
            print("5 : Monitor CPU")
            print("6 : Monitor RAM")
            print("7 : Monitor Disk Usage")

        elif sys.argv[1] in ["--u", "--U"]:

            print("Usage :")
            print(
                "python ScriptName.py TimeInterval FolderName"
            )

            print(
                "python ScriptName.py TimeInterval FolderName ReceiverEmail"
            )

        else:

            print("Invalid option")
            print("Use --h or --u")

    # ----------------------------------------------------------
    # AUTO LOGGING
    # ----------------------------------------------------------

    elif len(sys.argv) == 3:

        interval = int(sys.argv[1])

        folder = sys.argv[2]

        schedule.every(interval).minutes.do(
            CreateLog,
            folder
        )

        print("Automation Started")
        print("Folder :", folder)
        print("Interval :", interval, "minutes")

        print("Press Ctrl + C To Stop")

        while True:

            schedule.run_pending()

            time.sleep(1)

    # ----------------------------------------------------------
    # EMAIL AUTOMATION
    # ----------------------------------------------------------

    elif len(sys.argv) == 4:

        interval = int(sys.argv[1])

        folder = sys.argv[2]

        receiver = sys.argv[3]

        schedule.every(interval).minutes.do(
            SendEmailPerodically,
            folder,
            receiver
        )

        print("Email Reporting Started")

        print("Folder :", folder)

        print("Receiver :", receiver)

        print("Interval :", interval, "minutes")

        print("Press Ctrl + C To Stop")

        while True:

            schedule.run_pending()

            time.sleep(1)

    else:

        print("Invalid Number of Arguments")

        print("Use --h or --u")

    print(Border)
    print("--------------- Thank You ----------------")
    print(Border)


# ----------------------------------------------------------
# START PROGRAM
# ----------------------------------------------------------

if __name__ == "__main__":
    main()