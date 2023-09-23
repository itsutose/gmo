import os
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess

class MyPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MyPythonService'
    _svc_display_name_ = 'My Python Service'
    _svc_description_ = 'This is a Python service that runs test_gmo_orderbooks_copy.py'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        # Locate Python executable and script
        python_exe = "C:/Users/yamaguchi/anaconda3/envs/stock/python.exe"  # Adjust the path to your Anaconda python.exe
        script_path = "H:/マイドライブ/pytest/virtual_currency/gmo/public_API/test_gmo_orderbooks_copy2.py"  # Adjust the path to your script

        while self.is_alive:
            # Run your script
            process = subprocess.Popen([python_exe, script_path], shell=True)
            process.wait()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyPythonService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyPythonService)