import comtypes.client
import ctypes

ETABSModel = None

def ETABS():
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        return ctypes.windll.user32.MessageBoxW(0, "Connection with ETABS successful", "CEINT-SOFTWARE", 64)
        return ETABSModel
    except:
        pass