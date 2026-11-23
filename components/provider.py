############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.imports.provider import *
from components.functions import getSample3,getSample4
import random

class Provider(QtCore.QRunnable):
    # Worker es el encargado de ejecutar la tarea asíncrona
    # Emitirá señales que se mapearán a la interfaz
    def __init__(self, obj):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.active = True  
        self.mgrobj = obj # Dirección de memoria del objeto MainWindow
        self.enPausa = False
        self.delay = 1

        self.connectToBal1()
        self.connectToBal2()

        self.lapse = 3000 # miliseconds
        self.makeLapse = False
        self.lapseFlag = 0
        self.initTime = 0.0
        self.endTime = 0.0
        #self.connectToBal2()
             
    @QtCore.Slot()
    def run(self):
        while self.active:
            ##print("provider running...")
            try:
                if not self.enPausa :
                    if self.makeLapse:
                        if self.lapseFlag == 0:
                            self.lapseFlag = 1
                            self.initTime = time.time()*1000
                            self.endTime = self.initTime + self.lapse
                            pass
                        if self.endTime < time.time()*1000:
                            self.lapseFlag = 0 
                            print("runnning the cycle!!!")
                            # do here all you want every 30 seconds
                            # try to reconnect to balanza 
                            #self.connectToBal1()
                            #self.connectToBal2()

                    # Todo lo recurrente aqui
                    if self.mgrobj.isCapturing():
                        #print("index balanza:",self.mgrobj.getIndexBalanza()," mode port b1=>", self.mgrobj.modeMeasureB1," mode port b2=>", self.mgrobj.modeMeasureB2)
                        if self.mgrobj.getIndexBalanza() == 1  and self.mgrobj.getViewIndex() == 2:
                            if self.mgrobj.modeMeasureB1 == 1:
                                try:
                                    weight = getSample(self.vport) #"as an string value"
                                    self.mgrobj.updateWeight(weight)
                                except Exception as e:
                                    pass
                            elif self.mgrobj.modeMeasureB1 == 2:
                                try:
                                    weight = getSample2(self.vport) #"as an string value"
                                    self.mgrobj.updateWeight(float(weight))
                                except Exception as e:
                                    #print(e)
                             
                                    pass
                            elif self.mgrobj.modeMeasureB1 == 3:
                                try:
                                    gross = getSample3(self.vport) #"as an string value"
                                    self.mgrobj.updateWeight(gross)
                                except Exception as e:
                                    #print(e)
                                
                                    pass
                            elif self.mgrobj.modeMeasureB1 == 4:
                                try:
                                    weight = getSample4(self.vport) #"as an string value"
                                    #print(weight)
                                    self.mgrobj.updateWeight(weight)
                                except Exception as e:
                                    pass
                        elif self.mgrobj.getIndexBalanza() == 2 and self.mgrobj.getViewIndex() == 2:
                            if self.mgrobj.modeMeasureB2 == 1:
                                try:
                                    weight2 = getSample(self.vport2)
                                    self.mgrobj.updateWeight(float(weight2)-self.mgrobj.weight_carucha )
                                except Exception as e:
                                    print(e)
                                    pass
                            elif self.mgrobj.modeMeasureB2 == 2:
                                try:
                                    weight2 = getSample2(self.vport2)
                                    #print(weight2)
                                    self.mgrobj.updateWeight( float(weight2)-self.mgrobj.weight_carucha )
                                except Exception as e:
                                    pass
                            elif self.mgrobj.modeMeasureB2 == 3:
                                try:
                                    gross = getSample3(self.vport2) #"as an string value"
                                    self.mgrobj.updateWeight(float(gross)-self.mgrobj.weight_carucha )
                                except Exception as e:
                                    pass
                            elif self.mgrobj.modeMeasureB2 == 4:
                                try:
                                    weight = getSample4(self.vport2) #"as an string value"
                                    self.mgrobj.updateWeight(float(weight)-self.mgrobj.weight_carucha )
                                except Exception as e:
                                    pass
                        elif self.mgrobj.getIndexBalanza2() == 4 and self.mgrobj.getViewIndex() == 3:
                            #print('you currently now at piezas  with on weight')
                            if self.mgrobj.modeMeasureB1 == 1:
                                try:
                                    weight = getSample(self.vport) #"as an string value"
                                    self.mgrobj.updateWeight(weight)
                                except Exception as e:
                                    pass
                            elif self.mgrobj.modeMeasureB1 == 2:
                                try:
                                    weight = getSample2(self.vport) #"as an string value"
                                    self.mgrobj.updateWeight(float(weight))
                                except Exception as e:
                                    pass
                            elif self.mgrobj.modeMeasureB1 == 3:
                                try:
                                    gross = getSample3(self.vport) #"as an string value"
                                    self.mgrobj.updateWeight(gross)
                                except Exception as e:
                                    pass
                            elif self.mgrobj.modeMeasureB1 == 4:
                                try:
                                    weight = getSample4(self.vport) #"as an string value"
                                    #print(weight)
                                    self.mgrobj.updateWeight(weight)
                                except Exception as e:
                                    pass
                        elif self.mgrobj.getIndexBalanza2() == 5 and self.mgrobj.getViewIndex() == 3:
                            pass
                            #print('you currently now at piezas  with off weight')
                        # All expiration process here
                    else:
                        pass
                        print("not capturing!!!")
                else:
                    # Proceso en pausa
                    pass
            except Exception as e:
                print("some error running the cycle...",e)
                #self.showNotification(ALERT_RUNNING_PROVIDER)



    def showNotification(self,textMessage):
        try:
            self.framePeso = self.mgrobj.getFramePeso()
            self.framePieza = self.mgrobj.getFramePieza()
            ##print("index:",self.mgrobj.index," fpeso:",self.framePeso," fpieza:",self.framePieza)
            if self.mgrobj.index == 2:
                self.alert = Alert(self.framePeso,"")
                self.alert.showNotification(textMessage)
            elif self.mgrobj.index == 3:
                self.alert = Alert(self.framePieza,"")
                self.alert.showNotification(textMessage)
        except Exception as e:
            pass
            #print(e)

    def setDelay(self,delay):
        self.delay = delay
        pass

    def init(self):
        self.active = True
        self.enPausa = False

    def kill(self):
        self.active = False
        self.enPausa = True
        try:
            pass
            #self.vport.close()
        except:
            pass
        try:
            pass
            #self.vport2.close()
        except:
            pass

    def setEnPausa(self,pausa):
        self.pausa = pausa
        pass 

    def setCaptura(self,captura):
        self.captura = captura  

    def getTime(self):
        #ctime = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
        ctime = datetime.datetime.today().strftime("%H:%M:%S %p")
        return ctime 
        
    # only call this method over constructor
    def connectToBal1(self):
        try:
            self.vport = self.mgrobj.vport
        except:
            #print("can't connect to balanza 1")
            pass
            #self.showNotification("El puerto de balanza 1 se encuentra conectado")
        #print("vport is open:",isPortOpen)

    # only call this method over constructor
    def connectToBal2(self):
        try:
            self.vport2 = self.mgrobj.vport2
            #print("se ha establecido el puerto 2 selccionado en mgrObj")
        except:
            #print("can't connect to balanza 2")
            pass
            #self.showNotification("No esta conectado el puerto Nro.1") 
        #print("vport2 is open:",isPortOpen)

    def getBalanza1(self):
        result = None
        try:
            result = self.vport
        except:
            pass
        return result

    def getBalanza2(self):
        result = None
        try:
            result = self.vport2
        except:
            pass
        return result

    def create_fake_weight(self):
        weight = example_weight = int( random.random()*20 )
        return weight

    def update_weight_triyin(self):
        result = False
        try:
            example_weight = str( self.create_fake_weight() ) 
            self.mgrobj.updateWeight(example_weight)
            result = True
        except:
            print('ERROR UPDATING FAKE WEIGHT!!!')
        return result