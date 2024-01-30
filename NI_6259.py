import nidaqmx
import numpy as np
import time
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

class NI_6259:
    ''' Leitura de dados do NI-6259.

    Parameters:
    ----------
    channel_ADC : str - Canal de leitura do ADC.
    channel_DC : str - Canal de leitura do DC.
    pre_time : float - Tempo de pre-leitura.
    pos_time : float - Tempo de pos-leitura.
    path : str - Diretorio de salvamento dos dados.

    Example:
    --------
    >>> NI_6259(
    ...     channel_ADC = "Dev1/ai0",
    ...     channel_DC = "Dev1/ai0",
    ...     pre_time = 0.2,
    ...     pos_time = 15 * 60,
    ...     path = "C:/Users/vinic/OneDrive/Desktop/Digital_Twin/Batuta/NI-DAQ_6259/NI_6259.py",
    ...     )
    '''

    def __init__(
            self, 
            channel_ADC = "Dev1/ai0",
            channel_DC = "Dev1/ai0",
            pre_time = 0.2,
            pos_time = 15 * 60,
            path = "C:/Users/vinic/OneDrive/Desktop/Digital_Twin/Batuta/NI-DAQ_6259/NI_6259.py",
            ):
        
        self.channel_ADC = channel_ADC
        self.channel_DC = channel_DC
        self.pre_time = pre_time
        self.pos_time = pos_time
        self.path = Path(f"{path} / coleta.txt")

        if not self.path.exists():
            self.path.mkdir()

        self.run()
        
    def readDC(self):
        nidaqmx.task.ai_channels.add_ai_voltage_chan(self.channel_DC)
        return nidaqmx.task.read()

    def readADC(self):
        nidaqmx.task.ai_channels.add_ai_voltage_chan(self.channel_ADC)
        return nidaqmx.task.read()
    
    def run(self):
        _flag_trigger = False

        while _flag_trigger is False:
            # leituras
            last_readADC = readADC()
            readDC = readDC()

            time.sleep(self.pre_time)
        
            # trigger ativado
            if readDC == 0: 
                _flag_trigger = True
        
        # Salva ultimo dado
        file = open(self.path, "w")
        file.write(f"{last_readADC} \n")
        file.close()

        _flag_trigger = False

        # Faz a leitura enquanto o trigger estiver ativo
        while _flag_trigger is False:
            readADC = readADC()
            file = open(self.path, "w")
            file.write(f"{readADC} \n")
            file.close()
            
            # trigger desativado
            if readDC() == 1:
                _flag_trigger = True

            time.sleep(self.pos_time)

        self.stop() # Finaliza processo

    def stop(self):
        self.task.stop()
        self.task.close()

    def load(self):
        data = np.loadtxt(self.path)
        return data
    
    def plot(self):
        data = self.load()
        fig = go.Figure(data=go.Scatter(x=np.arange(len(data)), y=data))
        fig.show()

