import comtypes.client
import pandas as pd
import ctypes
import sys
import math

# OBTIENE LOS DESPLAZAMIENTOS DE LOS CENTROS DE MASAS
def StoryDisp(Caso_Carga:str):
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        locks = type(bool)
        locks = ETABSModel.GetModelIsLocked()

        if locks == False:
            ctypes.windll.user32.MessageBoxW(0, "Ejecute análisis para poder usar esta función", "CEINT-SOFTWARE", 16)
            ETABSModel = None
            ETABSObject = None
            sys.exit()

        TableVersion = 0
        FieldsKeysIncluded = []     # Cabeceras de la Tabla / Table Headers
        NumberRecords = 0           # Número de Filas de la Tabla / Number Rows of Table
        TableData = []              # Array que contiene toda la información de la Tabla / Array containing all information of Table
        FieldKeyList = []
        GroupName = None

        [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForDisplayArray("Point Bays", FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

        cont = 1

        CM_Label = [] # labels o Etiquetas de los Puntos de los Centros de Masas
        CM_Unique = [] # Nombres Unicos de los puntos en los Centros de Masas

        Name = None
        NumberNames = 0
        MyName = []

        [NumberNames, MyName, ret] = ETABSModel.Story.GetNameList(NumberNames, MyName)

        piso = 0

        # --------------------------------------------------------------------
        # AGRUPACIÓN DE LOS PUNTOS DE LOS CM EN LABELS Y UNIQUE NAMES
        #---------------------------------------------------------------------
        for i in range(0, NumberRecords):
            if TableData[cont] == "Yes":
                CM_Label.append(TableData[cont - 1])
                [Name, ret] = ETABSModel.PointObj.GetNameFromLabel(TableData[cont - 1], MyName[piso], Name)        
                CM_Unique.append(Name)        
                piso += 1
            cont += len(FieldsKeysIncluded)

        
        forceUnits = 0 ; lengthUnits = 0 ; temperatureUnits = 0
        [forceUnits, lengthUnits, temperatureUnits, ret] = ETABSModel.GetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
        ETABSModel.SetPresentUnits_2(6, 6, 2) # Unidades Tonf, m, C

        Obj = []
        Elm = []
        U1 = [] ; U2 = [] ; U3 = [] ; R1 = [] ; R2 = [] ; R3 = []
        NumberResults = 0
        LoadCase = []
        StepType = []
        StepNum = []

        Desp_Ux = []
        Desp_Uy = []

        Point_U = []
        D_X = []
        D_Y = []
        Story_Point = []
        
        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput(Caso_Carga)
        for i in range(0, len(CM_Unique)):
            [NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3, ret] = ETABSModel.Results.JointDispl(CM_Unique[i], 0, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)
            Desp_Ux = [] ; Desp_Uy = []
            for j in range(0, len(U1)):
                Desp_Ux.append(U1[j])
                Desp_Uy.append(U2[j])
            D_X.append(max(Desp_Ux))
            D_Y.append(max(Desp_Uy))
            Point_U.append(CM_Unique[i])
            Story_Point.append(MyName[i])

        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)

        ETABSModel = None
        ETABSObject = None

        import pandas as pd

        Data_Desp = {"Punto" : Point_U , "Piso" : Story_Point, "Desp.-X" : D_X, "Desp.-Y" : D_Y}
        Tabla_Desp = pd.DataFrame(Data_Desp)

        return Tabla_Desp
    
    except:
        pass

# 1 -> Sistema Regular || 2 -> Sistema Irregular
# R -> Factor de Reducción Sísmica según Norma
# 1-> Concreto || 2 -> Acero || 3-> Albañilería || 4 -> Madera || 5 -> Muros de Ductilidad Limitada

# CALCULA LAS DERIVAS DE PISO PARA UN CASO DE CARGA ESPECÍFICO
def StoryDrift(Caso_Carga:str, sistema:int, R:float, Material:int):
    try:

        if sistema < 1 or sistema > 2:
            ctypes.windll.user32.MessageBoxW(0, "Índice del Sistema Estructural Erróneo:" + "\n" + "1 -> Sistema Regular" + "\n" + "2 -> Sistema Irregular", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Material < 1 or Material > 5:
            ctypes.windll.user32.MessageBoxW(0, "Índice del material Erróneo:" + "\n" + "1 -> Concreto" + "\n" + "2 -> Acero" + "\n" + "3 -> Albañilería" + "\n" + "5 -> Muros de Ductilidad Limitada", "CEINT-SOFTWARE", 16)
            sys.exit()

        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        locks = type(bool)
        locks = ETABSModel.GetModelIsLocked()

        if locks == False:
            ctypes.windll.user32.MessageBoxW(0, "Ejecute análisis para poder usar esta función", "CEINT-SOFTWARE", 16)
            ETABSModel = None
            ETABSObject = None
            sys.exit()

        TableVersion = 0
        FieldsKeysIncluded = []     # Cabeceras de la Tabla / Table Headers
        NumberRecords = 0           # Número de Filas de la Tabla / Number Rows of Table
        TableData = []              # Array que contiene toda la información de la Tabla / Array containing all information of Table
        FieldKeyList = []
        GroupName = None

        [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForDisplayArray("Point Bays", FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

        cont = 1

        CM_Label = [] # labels o Etiquetas de los Puntos de los Centros de Masas
        CM_Unique = [] # Nombres Unicos de los puntos en los Centros de Masas
        Altura_Pisos = [] # Altura de todos los pisos

        Name = None
        NumberNames = 0
        MyName = []
        Height = 0

        [NumberNames, MyName, ret] = ETABSModel.Story.GetNameList(NumberNames, MyName)
        
        piso = 0

        # --------------------------------------------------------------------
        # AGRUPACIÓN DE LOS PUNTOS DE LOS CM EN LABELS Y UNIQUE NAMES
        #---------------------------------------------------------------------

        forceUnits = 0 ; lengthUnits = 0 ; temperatureUnits = 0
        [forceUnits, lengthUnits, temperatureUnits, ret] = ETABSModel.GetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
        ETABSModel.SetPresentUnits_2(6, 6, 2) # Unidades Tonf, m, C

        for i in range(0, NumberRecords):
            if TableData[cont] == "Yes":
                CM_Label.append(TableData[cont - 1])
                [Name, ret] = ETABSModel.PointObj.GetNameFromLabel(TableData[cont - 1], MyName[piso], Name)
                [Height, ret] = ETABSModel.Story.GetHeight(MyName[piso], Height)       
                CM_Unique.append(Name)
                Altura_Pisos.append(Height)
                piso += 1
            cont += len(FieldsKeysIncluded)
     

        Obj = []
        Elm = []
        U1 = [] ; U2 = [] ; U3 = [] ; R1 = [] ; R2 = [] ; R3 = []
        NumberResults = 0
        LoadCase = []
        StepType = []
        StepNum = []

        Desp_Ux = []
        Desp_Uy = []

        Point_U = []
        D_X = []
        D_Y = []
        Story_Point = []

        Deriva_Elast_X = []
        Deriva_Elast_Y = []
        Deriva_Inelast_X = []
        Deriva_Inelast_Y = []
        Desp_Rel_X = []
        Desp_Rel_Y = []
        Deriva_Limite = []

        factor = 0
        limite = 0

        if sistema == 1:
            factor = 0.75 * R
        else:
            factor = 0.85 * R
        
        if Material == 1:
            limite = 0.007
        elif Material == 2:
            limite = 0.010
        elif Material == 3:
            limite = 0.005
        elif Material == 4:
            limite = 0.010
        elif Material == 5:
            limite = 0.005

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput(Caso_Carga)
        for i in range(0, len(CM_Unique)):
            [NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3, ret] = ETABSModel.Results.JointDispl(CM_Unique[i], 0, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)
            Desp_Ux = [] ; Desp_Uy = []
            for j in range(0, len(U1)):
                Desp_Ux.append(U1[j])
                Desp_Uy.append(U2[j])
            D_X.append(max(Desp_Ux))
            D_Y.append(max(Desp_Uy))
            Point_U.append(CM_Unique[i])
            Story_Point.append(MyName[i])
            Deriva_Limite.append(limite)

            if len(D_X) > 1:
                Desp_Rel_X.append(D_X[len(D_X)-2] - D_X[len(D_X)-1])
                Desp_Rel_Y.append(D_Y[len(D_Y)-2] - D_Y[len(D_Y)-1])
                Deriva_Elast_X.append((D_X[len(D_X)-2] - D_X[len(D_X)-1]) / Altura_Pisos[i])
                Deriva_Elast_Y.append((D_Y[len(D_Y)-2] - D_Y[len(D_Y)-1]) / Altura_Pisos[i])
                Deriva_Inelast_X.append(factor * (D_X[len(D_X)-2] - D_X[len(D_X)-1]) / Altura_Pisos[i])
                Deriva_Inelast_Y.append(factor * (D_Y[len(D_Y)-2] - D_Y[len(D_Y)-1]) / Altura_Pisos[i])

        Desp_Rel_X.append(D_X[len(D_X)-1])
        Desp_Rel_Y.append(D_Y[len(D_Y)-1])
        Deriva_Elast_X.append(D_X[len(D_X)-1] / Altura_Pisos[len(D_X)-1])
        Deriva_Elast_Y.append(D_Y[len(D_Y)-1] / Altura_Pisos[len(D_X)-1])
        Deriva_Inelast_X.append(factor * D_X[len(D_X)-1] / Altura_Pisos[len(D_X)-1])
        Deriva_Inelast_Y.append(factor * D_Y[len(D_Y)-1] / Altura_Pisos[len(D_X)-1])
        
        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)

        ETABSModel = None
        ETABSObject = None
     
        import pandas as pd

        Data_Deriva = {"Punto" : Point_U , "Piso" : Story_Point, "Desp.-X" : D_X, "Desp.-Y" : D_Y, "Desp. Rel.-X" : Desp_Rel_X, "Desp. Rel.-Y" : Desp_Rel_Y,
                     "Der. Elást.-X" : Deriva_Elast_X, "Der. Elást.-Y" : Deriva_Elast_Y, "Der. Inelást.-X" : Deriva_Inelast_X, "Der. Inelást.-Y" : Deriva_Inelast_Y,
                     "Limite" : Deriva_Limite}
        Tabla_Deriva = pd.DataFrame(Data_Deriva)

        return Tabla_Deriva
    
    except:
        pass

# DEFINE EL SISMO ESTÁTICO
def SeismoUserCoef(NameLoad:str, DirLoad:tuple, Ecc:float, RangeStory:tuple, C:float, k:float):
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        ETABSModel.SetModelIsLocked(False)
        
        # Definición de Patrón de Carga Sísmica Estática
        ETABSModel.LoadPatterns.Add(NameLoad, 5)

        NumFatalErrors = 0 ; NumErrorMsgs = 0 ; NumWarnMsgs = 0 ; NumInfoMsgs = 0
        ImportLog = None        # Información del resultado de la Importación de Datos a la Tabla
        TableVersion = 1
        FieldsKeysIncluded = [] # Contiene las Cabeceras de la Tabla
        NumberRecords = 0       # Número de Filas que tiene la Tabla
        TableData = []          # Contenido de la Tabla
        GroupName = None

        [TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForEditingArray("Load Pattern Definitions - Auto Seismic - User Coefficient", GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
        
        FieldsKeysIncluded = ["Name", "IsAuto", "XDir", "XDirPlusE", "XDirMinusE", "YDir", "YDirPlusE", "YDirMinusE", 
                      "EccRatio", "TopStory", "BotStory", "OverStory", "OverDiaph", "OverEcc", "C", "K"]
        
        if len(TableData) > 1:
            Table_Old = []

            for i in range(0, len(TableData), len(FieldsKeysIncluded)):
                if TableData[i] != NameLoad:
                    for j in range(i, i+len(FieldsKeysIncluded)):
                        Table_Old.append(TableData[j])

            #for j in range(0, len(TableData)):
            #    Table_Old.append(TableData[j])
            New_Data = [NameLoad, "No", DirLoad[0], DirLoad[1], DirLoad[2], DirLoad[3], DirLoad[4], DirLoad[5], str(Ecc), RangeStory[0], RangeStory[1], None, None, None, str(C), str(k)]
            TableData = Table_Old + New_Data
        else:
            TableData = [NameLoad, "No", DirLoad[0], DirLoad[1], DirLoad[2], DirLoad[3], DirLoad[4], DirLoad[5], str(Ecc), RangeStory[0], RangeStory[1], None, None, None, str(C), str(k)]

        NumberRecords = int(len(TableData) / len(FieldsKeysIncluded))
        [FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.SetTableForEditingArray("Load Pattern Definitions - Auto Seismic - User Coefficient", TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
        [NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog, ret] = ETABSModel.DatabaseTables.ApplyEditedTables(True, NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

        ETABSModel = None
        ETABSObject = None

        return print("Carga Sismica \"" + NameLoad + "\" creada con éxito")

    except:
        return print("La Carga \"" + NameLoad + "\" no pudo crearse")

# DEFINE CASOS DE CARGA SÍSMICA QUE INCORPORAN UN ESPECTRO DE DISEÑO
def SeismoAMRE(LoadName:str, Dir:str, NameFunc:str, SF:float):

    # Dir --> U1, U2, U3, R1, R2, R3
    # Indicar el Nombre de la Función Espectral
    # SF --> es el factor de escala

    try:

        Direcciones = ["U1", "U2", "U3", "R1", "R2", "R3"]
        con = 0

        for i in range(0, len(Direcciones)):
            if Direcciones[i] == Dir:
                break
            con += 1

        if con == 6:
            ctypes.windll.user32.MessageBoxW(0, "La Dirección del Sismo indicada no corresponde.", "CEINT-SOFTWARE", 16)
            sys.exit()

        if SF == 0:
            ctypes.windll.user32.MessageBoxW(0, "El Factor de Escala no puede ser cero", "CEINT-SOFTWARE", 16)
            sys.exit()

        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        NumberNames = 0
        MyName = []
        FuncType = 0
        AddType = 0

        [NumberNames, MyName, ret] = ETABSModel.Func.GetNameList(NumberNames, MyName)

        Espectros = []
        for i in range(0, NumberNames):
            [FuncType, AddType, ret] = ETABSModel.Func.GetTypeOAPI(MyName[i], FuncType, AddType)
            if FuncType == 1:
                Espectros.append(MyName[i])

        con = 0
        for i in range(0, len(Espectros)):
            if Espectros[i] == NameFunc:
                break

        if con == len(Espectros):
            ctypes.windll.user32.MessageBoxW(0, "El nombre de la Función Espectral no existe en su modelo en ETABS", "CEINT-SOFTWARE", 16)
            ETABSModel = None
            ETABSObject = None
            sys.exit()

        
        forceUnits = 0 ; lengthUnits = 0 ; temperatureUnits = 0
        [forceUnits, lengthUnits, temperatureUnits, ret] = ETABSModel.GetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
        ETABSModel.SetPresentUnits_2(6, 6, 2) # Unidades Tonf, m, C

        ETABSModel.LoadCases.ResponseSpectrum.SetCase(LoadName)
        ETABSModel.LoadCases.ResponseSpectrum.SetLoads(LoadName, 1, [Dir], [NameFunc], [SF], ["Global"], [0])
        ETABSModel.LoadCases.ResponseSpectrum.SetModalCase(LoadName, "Modal")
        ETABSModel.LoadCases.ResponseSpectrum.SetEccentricity(LoadName, 0.05)

        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)

        ETABSModel = None
        ETABSObject = None

        return 1

    except:
        return 0

# OBTIENE EL FACTOR K DE DISTRIBUCIÓN DE FUERZA ESTÁTICA EN ALTURA
def kFactor(k_x:float, k_y:float):

    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        locks = type(bool)
        locks = ETABSModel.GetModelIsLocked()

        if locks == False:
            ctypes.windll.user32.MessageBoxW(0, "Ejecute análisis para poder usar esta función", "CEINT-SOFTWARE", 16)
            ETABSModel = None
            ETABSObject = None
            sys.exit()

        NumberResults = 0
        LoadCase = [] ; StepType = [] ; StepNum = [] ; Period = [] ; Ux = [] ; Uy = [] ; Uz = [] ; SumUx = [] ; SumUy = [] ; SumUz = [] ; Rx = [] ; Ry = [] ; Rz = [] ; SumRx = [] ; SumRy = [] ; SumRz = []

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput("Modal")
        [NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz, ret] = ETABSModel.Results.ModalParticipatingMassRatios(NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz)

        for i in range(0, NumberResults):

            if round(max(Ux), 5) == round(Ux[i], 5):

                if Period[i] <= 0.5:
                    k_x = 1
                else:
                    k_x = min(0.75 + 0.5 * Period[i], 2)
                
                break

        for i in range(0, NumberResults):

            if round(max(Uy), 5) == round(Uy[i], 5):

                if Period[i] <= 0.5:
                    k_y = 1
                else:
                    k_y = min(0.75 + 0.5 * Period[i], 2)
                
                break
                
        ETABSModel = None
        ETABSObject = None

        return k_x, k_y
    
    except:
        pass

# OBTIENE EL FACTOR DE ZONA SÍSMICA ASIGNADA
def ZFactor(Zona:int, Z:float):

    try:

        if Zona < 1 or Zona > 4:
            ctypes.windll.user32.MessageBoxW(0, "Índice de Zona Sísmica Errónea", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Zona == 1:
            Z = 0.1
        elif Zona == 2:
            Z = 0.25
        elif Zona == 3:
            Z = 0.35
        elif Zona == 4:
            Z = 0.45

        return Z
    
    except:
        pass

# OBTIENE EL FACTOR DE USO
def UFactor(Uso:int, U:float):

    try:

        if Uso < 1 or Uso > 3:
            ctypes.windll.user32.MessageBoxW(0, "índice de Uso Erróneo", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Uso == 1:
            U = 1.5
        elif Uso == 2:
            U = 1.3
        elif Uso == 3:
            U = 1

        return U
    
    except:
        pass

# OBTIENE EL FACTOR DE AMPLIFICACIÓN DINÁMICA, C
def CFactor(C_x:float, C_y:float, TP:float, TL:float):

    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        locks = type(bool)
        locks = ETABSModel.GetModelIsLocked()

        if locks == False:
            ctypes.windll.user32.MessageBoxW(0, "Ejecute análisis para poder usar esta función", "CEINT-SOFTWARE", 16)
            ETABSModel = None
            ETABSObject = None
            sys.exit()

        NumberResults = 0
        LoadCase = [] ; StepType = [] ; StepNum = [] ; Period = [] ; Ux = [] ; Uy = [] ; Uz = [] ; SumUx = [] ; SumUy = [] ; SumUz = [] ; Rx = [] ; Ry = [] ; Rz = [] ; SumRx = [] ; SumRy = [] ; SumRz = []

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput("Modal")
        [NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz, ret] = ETABSModel.Results.ModalParticipatingMassRatios(NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz)

        for i in range(0, NumberResults):
            if round(max(Ux), 5) == round(Ux[i], 5):
                T_x = Period[i]
                if T_x <= TP:
                    C_x = 2.5        
                else:
                    if TP < T_x and T_x <= TL:
                        C_x = 2.5 * TP / T_x
                    else:
                        C_x = 2.5 * TP * TL / pow(T_x, 2)
                break

        for i in range(0, NumberResults):
            if round(max(Uy), 5) == round(Uy[i], 5):
                T_y = Period[i]
                if T_y <= TP:
                    C_y = 2.5        
                else:
                    if TP < T_y and T_y <= TL:
                        C_y = 2.5 * TP / T_y
                    else:
                        C_y = 2.5 * TP * TL / pow(T_y, 2)
                break

        ETABSModel = None
        ETABSObject = None

        return C_x, C_y

    except:
        pass

# OBTIENE EL FACTOR DE SUELO
def SFactor(Zona:int, Suelo:int, S:float, TP:float, TL:float):

    try:

        if Zona < 1 or Zona > 4:
            ctypes.windll.user32.MessageBoxW(0, "Índice de Zona Sísmica Errónea", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Suelo < 0 or Suelo > 4:
            ctypes.windll.user32.MessageBoxW(0, "índice de Suelo no corresponde", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Suelo == 0:
            S = 0.8
            TP = 0.3
            TL = 3
        elif Suelo == 1:
            S = 1
            TP = 0.4
            TL = 2.5
        elif Suelo == 2:
            if Zona == 1:
                S = 1.6
            elif Zona == 2:
                S = 1.2
            elif Zona == 3:
                S = 1.15
            elif Zona == 4:
                S = 1.05
            TP = 0.6
            TL = 2
        elif Suelo == 3:
            if Zona == 1:
                S = 2
            elif Zona == 2:
                S = 1.4
            elif Zona == 3:
                S = 1.2
            elif Zona == 4:
                S = 1.1
            TP = 1
            TL = 1.6

        return S, TP, TL
    
    except:
        pass

# GENERA UN ARREGLO DE BARRAS PERSONALIZADO SEGÚN EL USUARIO
def BarCustom(NameBars:tuple, Diameter:tuple, Area:tuple):
        try:
            ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
            ETABSModel = ETABSObject.SapModel

            ETABSModel.SetModelIsLocked(False)

            NumFatalErrors = 0 ; NumErrorMsgs = 0 ; NumWarnMsgs = 0 ; NumInfoMsgs = 0
            ImportLog = None        # Información del resultado de la Importación de Datos a la Tabla
            TableVersion = 1
            FieldsKeysIncluded = [] # Contiene las Cabeceras de la Tabla
            NumberRecords = 0       # Número de Filas que tiene la Tabla
            TableData = []          # Contenido de la Tabla
            GroupName = None

            [TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForEditingArray("Reinforcing Bar Sizes", GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

            FieldsKeysIncluded = ["Name", "Diameter", "Area", "GUID"] # Cabeceras de la Tabla

            TableData = []
            
            for i in range(0, len(NameBars)):
                TableData.append(NameBars[i])
                TableData.append(str(Diameter[i]))
                TableData.append(str(Area[i]))
                TableData.append("GDSAGDSAFDASFAGEE")

            NumberRecords = int(len(TableData) / len(FieldsKeysIncluded))
            [FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.SetTableForEditingArray("Reinforcing Bar Sizes", TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
            [NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog, ret] = ETABSModel.DatabaseTables.ApplyEditedTables(True, NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

            ETABSModel = None
            ETABSObject = None

            return print("Personalización de barras exitosa")
        
        except:
            return print("La personalización no se realizó")
    
# PERMITE OBTENER EL SISTEMA ESTRUCTURAL DEL EDIFICIO SEGÚN CLASIFICACIÓN DE LA E.030
def SistemaEstructural(LoadName:str, Direccion:int, StoryName:str, resultado:str, Tabla:pd.DataFrame):
    
    try:

        if LoadName == None:
            ctypes.windll.user32.MessageBoxW(0, "El nombre de la carga no puede ser vacío", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Direccion < 1 or Direccion > 2:
            ctypes.windll.user32.MessageBoxW(0, "índice de Dirección Incorrecto", "CEINT-SOFTWARE", 16)
            sys.exit()

        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        locks = type(bool)
        locks = ETABSModel.GetModelIsLocked()

        if locks == False:
            ctypes.windll.user32.MessageBoxW(0, "Ejecute análisis para poder usar esta función", "CEINT-SOFTWARE", 16)
            ETABSModel = None
            ETABSObject = None
            sys.exit()

        ETABSModel.PierLabel.SetPier("Muros")
        ETABSModel.PierLabel.SetPier("Columnas")

        NumberNames = 0
        MyName = [] ; MyLabel = [] ; MyStory = []

        [NumberNames, MyName, ret] = ETABSModel.Story.GetNameList(NumberNames, MyName)

        con = 0

        for i in range(0, NumberNames):
            if MyName[i] == StoryName:
                Piso_1 = MyName[i]
                break
            con += 1

        if con == NumberNames:
            ctypes.windll.user32.MessageBoxW(0, "El Nombre del Piso no existe", "CEINT-SOFTWARE", 16)
            ETABSModel = None
            ETABSObject = None
            sys.exit()

        
        [NumberNames, MyName, MyLabel, MyStory, ret] = ETABSModel.AreaObj.GetLabelNameList(NumberNames, MyName, MyLabel, MyStory)

        for i in range(0, NumberNames):
            if MyLabel[i][0 : 1] == "W" and MyStory[i] == Piso_1:
                ETABSModel.AreaObj.SetPier(MyName[i], "Muros")


        LabelFr = None
        Story = None

        [NumberNames, MyName, ret] = ETABSModel.FrameObj.GetNameListOnStory(Piso_1, NumberNames, MyName)

        for i in range(0, NumberNames-1):

            [LabelFr, Story, ret] = ETABSModel.FrameObj.GetLabelFromName(MyName[i], LabelFr, Story)
    
            if LabelFr[0 : 1] == "C":
                ETABSModel.FrameObj.SetPier(MyName[i], "Columnas")
            LabelFr = None

        
        NumberStories = 0
        StoryName = []
        AxisAngle_Wall = []
        AxisAngle_Col = []
        NumAreaObjs = []
        NumLineObjs = []
        WidthBot = []
        ThicknessBot = []
        WidthTop = []
        ThicknessTop = []
        MatProp = []
        CGBotX = []
        CGBotY = []
        CGBotZ = []
        CGTopX = []
        CGTopY = []
        CGTopZ = []
        
        forceUnits = 0 ; lengthUnits = 0 ; temperatureUnits = 0
        [forceUnits, lengthUnits, temperatureUnits, ret] = ETABSModel.GetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
        ETABSModel.SetPresentUnits_2(6, 6, 2) # Unidades Tonf, m, C

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput(LoadName)

        NumberResults = 0
        StoryName = []
        PierName = []
        LoadCase = []
        Location = []
        P = []
        V2 = []
        V3 = []
        T = []
        M2 = []
        M3 = []

        [NumberResults, StoryName, PierName, LoadCase, Location, P, V2, V3, T, M2, M3, ret] = ETABSModel.Results.PierForce(NumberResults, StoryName, PierName, LoadCase, Location, P, V2, V3, T, M2, M3)

        [NumberStories, StoryName, AxisAngle_Wall, NumAreaObjs, NumLineObjs, WidthBot, ThicknessBot, WidthTop, ThicknessTop, MatProp, CGBotX, CGBotY, CGBotZ, CGTopX, CGTopY, CGTopZ, ret] = ETABSModel.PierLabel.GetSectionProperties ("Muros", NumberStories, StoryName, AxisAngle_Wall, NumAreaObjs, NumLineObjs, WidthBot, ThicknessBot, WidthTop, ThicknessTop, MatProp, CGBotX, CGBotY, CGBotZ, CGTopX, CGTopY, CGTopZ)
        [NumberStories, StoryName, AxisAngle_Col, NumAreaObjs, NumLineObjs, WidthBot, ThicknessBot, WidthTop, ThicknessTop, MatProp, CGBotX, CGBotY, CGBotZ, CGTopX, CGTopY, CGTopZ, ret] = ETABSModel.PierLabel.GetSectionProperties ("Columnas", NumberStories, StoryName, AxisAngle_Col, NumAreaObjs, NumLineObjs, WidthBot, ThicknessBot, WidthTop, ThicknessTop, MatProp, CGBotX, CGBotY, CGBotZ, CGTopX, CGTopY, CGTopZ)
        
        V_muro = 0
        V_column = 0

        for i in range(0, NumberResults):
            if PierName[i] == "Muros":
                if Direccion == 1:
                    V_muro = abs(V2[i] * math.cos(math.pi * AxisAngle_Wall[0] / 180) + V3[i] * math.sin(math.pi * AxisAngle_Wall[0] / 180))
                else:
                     V_muro = abs(V3[i] * math.cos(math.pi * AxisAngle_Wall[0] / 180) - V2[i] * math.sin(math.pi * AxisAngle_Wall[0] / 180))
            elif PierName[i] == "Columnas":
                if Direccion == 1:
                    V_column = abs(V2[i] * math.cos(math.pi * AxisAngle_Col[0] / 180) + V3[i] * math.sin(math.pi * AxisAngle_Col[0] / 180))
                else:
                     V_column = abs(V3[i] * math.cos(math.pi * AxisAngle_Col[0] / 180) - V2[i] * math.sin(math.pi * AxisAngle_Col[0] / 180))


        V_total = V_muro + V_column


        Ratio_Muro = V_muro / V_total
        Ratio_Column = V_column / V_total

        resultado = None
        #print("V_muro: " + str(round(Ratio_Muro, 4)))
        #print("V_columna: " + str(round(Ratio_Column, 4)))
        #print("------------------------------------")
        if round(Ratio_Column, 4) >= 0.8:
            resultado = "El Sistema es de Pórticos"
            #print("El sistema es de Pórticos")
        elif round(Ratio_Muro, 4) >= 0.7:
            resultado = "El Sistema es de Muros Estructurales"
            #print("El sistema es de Muros Estructurales")
        elif round(Ratio_Muro) >= 0.2 and round(Ratio_Muro) < 0.7:
            resultado = "El Sistema es Dual"
            #print("El sistema es Dual")

        Ratios_Shear = [Ratio_Muro, Ratio_Column, 1.0]
        Shears = [V_muro, V_column, V_total]

        Data_Table = {"Cortante" : ["Muros", "Columnas", "Total"], "Valor" : Shears, "Porcentaje" : Ratios_Shear}
        Tabla = pd.DataFrame(Data_Table)
        Tabla

        #print("Unidades: Tonf, m, C")

        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)

        ETABSModel.PierLabel.Delete("Muros")
        ETABSModel.PierLabel.Delete("Columnas")

        ETABSModel = None
        ETABSObject = None

        return resultado, Tabla

    except:
        pass
    
# GENERA EL FACTOR ZUCS/R DEL ARTÍCULO 28.2.1 DE LA NTE E.030
def ZUCSR(Zona:int, Uso:int, Suelo:int, R_x:float, R_y:float, ZUCSR_X:float, ZUCSR_Y:float, Tabla:pd.DataFrame):

    # Zona -> 1 = Z1 | 2 = Z2 | 3 = Z3 | 4 = Z4
    # Uso -> 1 = Esencial | 2 = Importante | 3 = Comun
    # Suelo -> 0 = So | 1 = S1 | 2 = S2 | 3 = S3

    try:

        if Zona < 1 or Zona > 4:
            ctypes.windll.user32.MessageBoxW(0, "Índice de Zona Sísmica Errónea", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Uso < 1 or Uso > 3:
            ctypes.windll.user32.MessageBoxW(0, "índice de Uso Erróneo", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Suelo < 0 or Suelo > 4:
            ctypes.windll.user32.MessageBoxW(0, "índice de Suelo no corresponde", "CEINT-SOFTWARE", 16)
            sys.exit()

        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        locks = type(bool)
        locks = ETABSModel.GetModelIsLocked()

        if locks == False:
            ctypes.windll.user32.MessageBoxW(0, "Ejecute análisis para poder usar esta función", "CEINT-SOFTWARE", 16)
            ETABSModel = None
            ETABSObject = None
            sys.exit()

        NumberResults = 0
        LoadCase = [] ; StepType = [] ; StepNum = [] ; Period = [] ; Ux = [] ; Uy = [] ; Uz = [] ; SumUx = [] ; SumUy = [] ; SumUz = [] ; Rx = [] ; Ry = [] ; Rz = [] ; SumRx = [] ; SumRy = [] ; SumRz = []

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput("Modal")
        [NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz, ret] = ETABSModel.Results.ModalParticipatingMassRatios(NumberResults, LoadCase, StepType, StepNum, Period, Ux, Uy, Uz, SumUx, SumUy, SumUz, Rx, Ry, Rz, SumRx, SumRy, SumRz)

        Z = 0 ; U = 0 ; C_x = 0 ; C_y = 0 ; S = 0 ; TP = 0 ; TL = 0
        
        if Zona == 1:
            Z = 0.1
        elif Zona == 2:
            Z = 0.25
        elif Zona == 3:
            Z = 0.35
        elif Zona == 4:
            Z = 0.45


        if Suelo == 0:
            S = 0.8
            TP = 0.3
            TL = 3
        elif Suelo == 1:
            S = 1
            TP = 0.4
            TL = 2.5
        elif Suelo == 2:
            if Zona == 1:
                S = 1.6
            elif Zona == 2:
                S = 1.2
            elif Zona == 3:
                S = 1.15
            elif Zona == 4:
                S = 1.05
            TP = 0.6
            TL = 2
        elif Suelo == 3:
            if Zona == 1:
                S = 2
            elif Zona == 2:
                S = 1.4
            elif Zona == 3:
                S = 1.2
            elif Zona == 4:
                S = 1.1
            TP = 1
            TL = 1.6

        if Uso == 1:
            U = 1.5
        elif Uso == 2:
            U = 1.3
        elif Uso == 3:
            U = 1

        C_x = 0
        C_y = 0

        for i in range(0, NumberResults):
            if round(max(Ux), 5) == round(Ux[i], 5):
                T_x = Period[i]
                if T_x <= TP:
                    C_x = 2.5        
                else:
                    if TP < T_x and T_x <= TL:
                        C_x = 2.5 * TP / T_x
                    else:
                        C_x = 2.5 * TP * TL / pow(T_x, 2)
                break

        for i in range(0, NumberResults):
            if round(max(Uy), 5) == round(Uy[i], 5):
                T_y = Period[i]
                if T_y <= TP:
                    C_y = 2.5        
                else:
                    if TP < T_y and T_y <= TL:
                        C_y = 2.5 * TP / T_y
                    else:
                        C_y = 2.5 * TP * TL / pow(T_y, 2)
                break

        ZUCSR_X = Z * U * C_x * S / R_x
        ZUCSR_Y = Z * U * C_y * S / R_y

        #print("Z: " + str(Z))
        #print("U: " + str(U))
        #print("Cy: " + str(C_y))
        #print("S: " + str(S))
        #print("Rx: " + str(R_x))
        #print("Ry: " + str(R_y))
        #print("ZUCS/Rx: " + str(ZUCSR_X))
        #print("ZUCS/Ry: " + str(ZUCSR_Y))

        Dir_X = [Z, U, C_x, S, R_x, round(ZUCSR_X, 6)]
        Dir_Y = [Z, U, C_y, S, R_y, round(ZUCSR_Y, 6)]

        Data_Table = {"Parámetro" : ["Zona Sísmica, Z", "Categoría de Uso, U", "Factor de Amplificación Sísmica, C", "Factor de Sitio o Suelo, S", "Coeficiente de Reducción, R", "Coficiente de Cortante Basal, ZUCS/R"],
                      "Dirección X" : Dir_X, "Dirección Y" : Dir_Y}
        Tabla = pd.DataFrame(Data_Table)
        Tabla

        ETABSModel = None
        ETABSObject = None

        return ZUCSR_X, ZUCSR_Y, Tabla

    except:
        pass

# DEFINE MATERIAL DE CONCRETO SEGÚN NTE E.060
def MatConcrete(MaterialName:str, fc:float):

    try:

        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        ETABSModel.SetModelIsLocked(False)

        forceUnits = 0 ; lengthUnits = 0 ; temperatureUnits = 0
        [forceUnits, lengthUnits, temperatureUnits, ret] = ETABSModel.GetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
        ETABSModel.SetPresentUnits_2(5, 5, 2) # Unidades Kgf, cm, C

        ETABSModel.PropMaterial.SetMaterial(MaterialName, 2)
        ETABSModel.PropMaterial.SetOConcrete(MaterialName, fc, False, 0, 2, 4, 2 * fc / (15100 * pow(fc, 0.5)), 0.005)
        ETABSModel.PropMaterial.SetMPIsotropic(MaterialName, 15100 * pow(fc, 0.5), 0.15, 0.0000055)
        ETABSModel.SetPresentUnits(8) # Kgf-m-C
        ETABSModel.PropMaterial.SetWeightAndMass(MaterialName, 1, 2400)

        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)

        ETABSModel = None
        ETABSObject = None
    except:
        pass

# CALCULA Y EXPORTA ESPECTROS DE SISMO VERTICAL
def EspectroVertical(Name:str, Zona:int, Uso:int, Suelo:int, R:float):

    try:        

        Z = 0 ; U = 0 ; S = 0 ; TP = 0 ; TL = 0

        if Zona < 1 or Zona > 4:
            ctypes.windll.user32.MessageBoxW(0, "Índice de Zona Sísmica Errónea", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Uso < 1 or Uso > 3:
            ctypes.windll.user32.MessageBoxW(0, "índice de Uso Erróneo", "CEINT-SOFTWARE", 16)
            sys.exit()

        if Suelo < 0 or Suelo > 4:
            ctypes.windll.user32.MessageBoxW(0, "índice de Suelo no corresponde", "CEINT-SOFTWARE", 16)
            sys.exit()
        
        [S, TP, TL] = SFactor(Zona, Suelo, S, TP, TL)
        
        Z = ZFactor(Zona, Z)

        U = UFactor(Uso, U)
        
        T = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.16, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5, 5.25, 5.5, 5.75, 6, 6.25, 6.5, 6.75, 7, 7.25, 7.5, 7.75, 8, 8.5, 9, 9.5, 10]
        Sa = [] ; C = 0 ; C_factor = []
        
        for i in range(0, len(T)):
            
            if T[i] <= 0.2 * float(TP):
                C = 1 + 7.5 * T[i] / float(TP)
                C_factor.append(1 + 7.5 * T[i] / TP)                
            elif 0.2 * float(TP) < T[i] and T[i] <= float(TP):
                C = 2.5
                C_factor.append(2.5)                
            elif float(TP) < T[i] and T[i] <= float(TL):
                C = 2.5 * float(TP) / T[i]
                C_factor.append(2.5 * float(TP) / T[i])                
            elif T[i] > float(TL):
                C = 2.5 * float(TP) * float(TL) / pow(T[i], 2)
                C_factor.append(2.5 * float(TP) * float(TL) / pow(T[i], 2))
                
            
            Sa.append(float(Z) * float(U) * float(S) * C / float(R))

        
        Data_Tabla = {"Periodo" : T, "C" : C_factor, "Sa" : Sa}
        Tabla_Sa = pd.DataFrame(Data_Tabla)

        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        TableVersion = 0
        FieldsKeysIncluded = []
        NumberRecords = 0
        TableData = []
        FieldKeyList = []
        GroupName = None

        [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForDisplayArray("Functions - Response Spectrum - User Defined", FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

        DataList = []

        for i in range(0, len(TableData), len(FieldsKeysIncluded)):
            if TableData[i] != Name:
                for j in range(i, i+len(FieldsKeysIncluded)):
                    DataList.append(TableData[j])

            
        DataList.append(Name)
        DataList.append(str(T[0]))
        DataList.append(str(Sa[0]))
        DataList.append("0.05")
        DataList.append("fdsafdsafdsafdsafsafa")

        for i in range(1, len(Sa)):
            DataList.append(Name)
            DataList.append(str(T[i]))
            DataList.append(str(Sa[i]))
            DataList.append(None)
            DataList.append(None)

        NumFatalErrors = 0 ; NumErrorMsgs = 0 ; NumWarnMsgs = 0 ; NumInfoMsgs = 0
        ImportLog = None

        [TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForEditingArray("Functions - Response Spectrum - User Defined", GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
        TableData = tuple(DataList)
        NumberRecords = int(len(TableData) / len(FieldsKeysIncluded))
        [FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.SetTableForEditingArray("Functions - Response Spectrum - User Defined", TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
        [NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog, ret] = ETABSModel.DatabaseTables.ApplyEditedTables(True, NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

        ETABSModel = None
        ETABSObject = None

        return Tabla_Sa

    except:
        pass


def MatAlbaE070():
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        # COLOCAR AQUÍ TU CÓDIGO

        ETABSModel = None
        ETABSObject = None
    except:
        pass

def IrregularidadAltura():
    try:
        1
    except:
        pass

def IrregularidadPlanta():
    try:
        1
    except:
        pass