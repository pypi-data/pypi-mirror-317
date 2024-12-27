import wmi
import win32com.client

#Function to get processor details
def get_processor_details():
    processor_details = []
    str_computer = "."
    obj_wmi_service = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    obj_swbem_services = obj_wmi_service.ConnectServer(str_computer, "root\cimv2")
    col_items = obj_swbem_services.ExecQuery("SELECT * FROM Win32_Processor")
    for obj_item in col_items:
        processor = {
            'name': obj_item.Name,
            'description': obj_item.description,
            'DeviceID': obj_item.DeviceID,
            'manufacturer': obj_item.Manufacturer,
            'processorID': obj_item.processorID,
            'systemName': obj_item.SystemName
        }
        processor_details.append(processor)
    return processor_details

#Function to get motherboard details
def get_motherboard_details():
    motherboard_details = []
    str_computer = "."
    obj_wmi_service = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    obj_swbem_services = obj_wmi_service.ConnectServer(str_computer, "root\cimv2")
    col_items = obj_swbem_services.ExecQuery("SELECT * FROM Win32_BaseBoard")
    for obj_item in col_items:
        main_board = {
            'name': obj_item.Name,
            'description': obj_item.Description,
            'manufacturer': obj_item.Manufacturer,
            'model': obj_item.Model,
            'product': obj_item.Product,
            'serialNumber': obj_item.SerialNumber,
            'version': obj_item.Version
        }
        motherboard_details.append(main_board)
    return motherboard_details

#Function to get VGA devices
def get_gpu_details():
    gpu_details = []
    computer = wmi.WMI()
    gpu_info = computer.Win32_VideoController()
    for eachitem in gpu_info:
        each_gpu = {
            'name': eachitem.Name,
            'adapterRAM': eachitem.AdapterRAM,
            'description': eachitem.description,
            'pnpDeviceID': eachitem.PNPDeviceID,
            'systemName': eachitem.SystemName
        }
        gpu_details.append(each_gpu)
    return gpu_details

#Function to get monitor details
def get_monitor_details():
    monitor_details = []
    obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)
    displays = [x for x in obj if 'Monitor' in str(x)]
    for item in displays:
        if item.PNPClass == "Monitor":
            each_monitor = {
                'name': item.Caption,
                'manufacturer': item.Manufacturer,
                'hardwareID': item.HardwareID[0],
                'description': item.Description,
                'systemName':item.SystemName
            }
            monitor_details.append(each_monitor)
    return monitor_details

#Function to get cd_drive details
def get_cd_drive_details():
    cd_drive_details = []
    obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)
    cd_drive = [x for x in obj if 'CDROM' in str(x)]
    for item in cd_drive:
        each_cd_drive = {
            'name': item.Name,
            'description': item.Description,
            'hardwareID': item.HardwareID[0],
            'pnpDeviceID': item.pnpDeviceID,
            'manufacturer': item.Manufacturer,
            'systemName': item.systemName
        }
        cd_drive_details.append(each_cd_drive)
    return cd_drive_details

#Function to get mouse details
def get_mouse_details():
    mouse_details = []
    obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)
    mouse = [x for x in obj if 'Mouse' in str(x)]
    for item in mouse:
        each_mouse = {
            'name': item.Caption,
            'manufacturer': item.Manufacturer,
            'hardwareID': item.HardwareID[0],
            'description': item.Description,
            'systemName':item.SystemName
        }
        mouse_details.append(each_mouse)
    return mouse_details

#Fuction to get speaker details
def get_speaker_details():
    speaker_details = []
    obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)
    speakers = [x for x in obj if 'Speakers' in str(x)]
    for item in speakers:
        each_speaker = {
            'name': item.Caption,
            'manufacturer': item.Manufacturer,
            'hardwareID': item.HardwareID[0],
            'description': item.Description,
            'systemName':item.SystemName
        }
        speaker_details.append(each_speaker)
    return speaker_details

#Function to get keyboard details
def get_keyboard_details():
    keyboard_details = []
    obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)
    keyboard = [x for x in obj if 'Keyboard' in str(x)]
    for item in keyboard:
        each_keyboard = {
            'name': item.Caption,
            'manufacturer': item.Manufacturer,
            'hardwareID': item.HardwareID[0],
            'description': item.Description,
            'systemName':item.SystemName
        }
        keyboard_details.append(each_keyboard)
    return keyboard_details

#Function to get Hard Disk details
def get_hard_disk_details():
    hard_disk_details = []
    str_computer = "."
    obj_wmi_service = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    obj_swbem_services = obj_wmi_service.ConnectServer(str_computer, "root\cimv2")
    col_items = obj_swbem_services.ExecQuery("SELECT * FROM Win32_DiskDrive")
    for obj_item in col_items:
        each_hard_disk = {
            'name': obj_item.Name,
            'manufacturer': obj_item.Manufacturer,
            'deviceID': obj_item.DeviceID,
            'description': obj_item.Description,
            'pnpDeviceID': obj_item.PNPDeviceID,
            'size': obj_item.Size
        }
        hard_disk_details.append(each_hard_disk)
    return hard_disk_details

#Get RAM details
def get_ram_details():
    ram_details = []
    str_computer = "."
    obj_wmi_service = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    obj_swbem_services = obj_wmi_service.ConnectServer(str_computer, "root\cimv2")
    col_items = obj_swbem_services.ExecQuery("SELECT * FROM Win32_PhysicalMemory")
    for obj_item in col_items:
        each_ram = {
            'name': obj_item.Name,
            'manufacturer': obj_item.manufacturer,
            'description': obj_item.description,
            'serialNumber': obj_item.SerialNumber,
            'capaity': obj_item.capacity
        }
        ram_details.append(each_ram)
    return ram_details
