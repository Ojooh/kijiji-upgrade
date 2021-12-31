from gui import kijijiApp
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()
    ws = kijijiApp()
    rt = ws.window_loop()
    rt.mainloop()