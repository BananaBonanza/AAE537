import tkinter as tk
import numpy as np

## ATMOSPHERIC MODEL ##
class atmosphere:
    def __init__(self, val, valGiven = 0,units = "SI"):
        #Convert from US to SI
        if units != "SI" and valGiven == 0:
            val = val / 3.281
        if units != "SI" and valGiven == 1:
            val = val * 0.04788
        #0 implies the given value is an altitude
        #1 implies the given value is a pressure
        if valGiven == 0:
            self.h = val
        elif valGiven == 1:
            self.P = val
        else:
            print("Not a valid 'valGiven' parameter.")
    def hCalc(self):
        if self.h < 11000:
            self.T = 15.04 - 0.00649*self.h
            self.P = 101.29 * ((self.T + 273.1)/228.08)**(5.256)
        elif self.h < 25000:
            self.T = -56.46
            self.P = 22.65 * np.exp(1.73 - 0.000157*self.h)
        elif self.h > 24999:
            self.T = -131.21 + 0.00299*self.h
            self.P = 2.488 * ((self.T + 273.1)/216.6)**(-11.388)
        self.rho = self.P / (0.2869 * (self.T + 273.1))
    def PCalc(self):
        if self.P > 22.632:
            self.T = (288.08*(self.P/101.29)**(1/5.256))-273.1
            self.h = (self.T - 15.04)/(-0.00649)
        elif self.P > 0.1113586:
            self.T = -56.46
            self.h = (1.73 - np.log((self.P/22.65)))/(0.000157)
        else:
            self.T = (216.6*(self.P/2.488)**(1/(-11.388)))-273.1
            self.h = (self.T + 131.21)/0.00299
        self.rho = self.P / (0.2869 * (self.T + 273.1))


##########################
##       UI Methods     ##
##########################

fields = ('Altitude', 'Dynamic Pressure',
          'Bypass Ratio','Compressor Pressure Ratio',
          'Heat Capacity Cp', 'Ratio of Specific Heats',
          'Enthalpy of Combustion Hb', 'Mass Flow' ,'Burner Total Temp',
          'Afterburner Total Temp','Efficiency - Compressor',
          'Efficiency - Burner','Efficiency - Turbine',
          'Efficiency - Afterburner','Efficiency - Nozzle'
          )
def run_analysis(entries):
    #Altitude
    alt = float(entries['Altitude'].get())
    #Dymanic Pressure
    q = float(entries['Dynamic Pressure'].get())
    #Bypass
    beta = float(entries['Bypass Ratio'].get())
    #CPR
    CPR = float(entries['Compressor Pressure Ratio'].get())
    #Cp
    Cp = float(entries['Heat Capacity Cp'].get())
    #gamma
    gamma = float(entries['Ratio of Specific Heats'].get())
    #Hb
    Hb = float(entries['Enthalpy of Combustion Hb'].get())
    #mDot
    mDot = float(entries['Mass Flow'].get())
    #Tt4
    Tt4 = float(entries['Burner Total Temp'].get())
    #Tt7
    Tt7 = float(entries['Afterburner Total Temp'].get())
    #nc
    nc = float(entries['Efficiency - Compressor'].get())
    #nb
    nb = float(entries['Efficiency - Burner'].get())
    #nt
    nt = float(entries['Efficiency - Turbine'].get())
    #nab
    nab = float(entries['Efficiency - Afterburner'].get())
    #nn
    nn = float(entries['Efficiency - Nozzle'].get())
    #####################
    ##   Evaluation    ##
    #####################
    #Run the atmospheric model
    atmos = atmosphere(alt, units='US')
    atmos.hCalc()
    M0 = m.sqrt((2*q)/(gamma*atmos.P))
    print(M0)
    res.configure(text = "Result: " + str(Cp))

def makeform(root, fields):
    entries = {}
    for field in fields:
        print(field)
        row = tk.Frame(root)
        lab = tk.Label(row, width=22, text=field+": ", anchor='e')
        ent = tk.Entry(row)
        ent.insert(0, "0")
        out = tk.Entry(row)
        row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.LEFT, 
                 expand=tk.YES, 
                 fill=tk.X)
        entries[field] = ent
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Turbojet Analysis")
    ents = makeform(root, fields)
    res = tk.Label(root)
    b1 = tk.Button(root, text='Perform Analysis',
           command=(lambda e=ents: run_analysis(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    res.pack(side=tk.RIGHT)
    root.mainloop()
    root.destroy()
