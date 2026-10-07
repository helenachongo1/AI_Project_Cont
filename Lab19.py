import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, lti, bode


'''def analyze_z_transfer_function(num, den):
    system=TransferFunction(num, den)
    
    zeros = system.zeros
    poles = system.poles
    print("Zeros:",zeros)
    print("Poles:",poles)
    
    #Srability analysis
    stable = all(np.abs(pole)<1 for pole in poles)
    print("Stability:", "Stable" if stable else "Unstable")
    
    #Casuality analysis
    casual = all(num[i] == 0 for i in range(len(num)-1) if num[i+1] == 0)
    print("Casuality:", "Causal" if casual else "Non-Casual")
    
    #Time Invariance analysis
    time_invariant = True 
    print("Time Invariance:", "Time Invariant" if time_invariant else "Time Variant")
    
    [w,mag,phase] = bode(system)
    
    plt.figure(figsize=(12,8))
    plt.subplot(2,1,1)
    plt.semilogx(w, mag)
    plt.title('Bode Magnitude Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Magnitude [dB]')
    plt.grid()
    plt.subplot(2, 1, 2)
    plt.semilogx(w, phase)
    plt.title('Bode Phase Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Phase [degrees]')
    plt.grid()
    plt.tight_layout()
    plt.show()
    

num = [1,0.5]
den = [1,-1.5,0.5]
analyze_z_transfer_function(num, den)'''

'''def analyze_z_transfer_function(num, den):
    system=TransferFunction(num, den)
    
    zeros = system.zeros
    poles = system.poles
    print("Zeros:",zeros)
    print("Poles:",poles)
    
    #Srability analysis
    stable = all(np.abs(pole)<1 for pole in poles)
    print("Stability:", "Stable" if stable else "Unstable")
    
    #Casuality analysis
    casual = all(num[i] == 0 for i in range(len(num)-1) if num[i+1] == 0)
    print("Casuality:", "Causal" if casual else "Non-Casual")
    
    #Time Invariance analysis
    time_invariant = True 
    print("Time Invariance:", "Time Invariant" if time_invariant else "Time Variant")
    
    [w,mag,phase] = bode(system)
    
    plt.figure(figsize=(12,8))
    plt.subplot(2,1,1)
    plt.semilogx(w, mag)
    plt.title('Bode Magnitude Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Magnitude [dB]')
    plt.grid()
    plt.subplot(2, 1, 2)
    plt.semilogx(w, phase)
    plt.title('Bode Phase Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Phase [degrees]')
    plt.grid()
    plt.tight_layout()
    plt.show()
    

num = [1,-1]
den = [1,-0.5]
analyze_z_transfer_function(num, den)'''

'''def analyze_z_transfer_function(num, den):
    system=TransferFunction(num, den)
    
    zeros = system.zeros
    poles = system.poles
    print("Zeros:",zeros)
    print("Poles:",poles)
    
    #Srability analysis
    stable = all(np.abs(pole)<1 for pole in poles)
    print("Stability:", "Stable" if stable else "Unstable")
    
    #Casuality analysis
    casual = all(num[i] == 0 for i in range(len(num)-1) if num[i+1] == 0)
    print("Casuality:", "Causal" if casual else "Non-Casual")
    
    #Time Invariance analysis
    time_invariant = True 
    print("Time Invariance:", "Time Invariant" if time_invariant else "Time Variant")
    
    [w,mag,phase] = bode(system)
    
    plt.figure(figsize=(12,8))
    plt.subplot(2,1,1)
    plt.semilogx(w, mag)
    plt.title('Bode Magnitude Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Magnitude [dB]')
    plt.grid()
    plt.subplot(2, 1, 2)
    plt.semilogx(w, phase)
    plt.title('Bode Phase Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Phase [degrees]')
    plt.grid()
    plt.tight_layout()
    plt.show()
    

num = [0.5]
den = [1,-0.8]
analyze_z_transfer_function(num, den)'''

#Q1
def analyze_z_transfer_function(num, den):
    system=TransferFunction(num, den)
    
    zeros = system.zeros
    poles = system.poles
    print("Zeros:",zeros)
    print("Poles:",poles)
    
    #Srability analysis
    stable = all(np.abs(pole)<1 for pole in poles)
    print("Stability:", "Stable" if stable else "Unstable")
    
    #Casuality analysis
    casual = all(num[i] == 0 for i in range(len(num)-1) if num[i+1] == 0)
    print("Casuality:", "Causal" if casual else "Non-Casual")
    
    #Time Invariance analysis
    time_invariant = True 
    print("Time Invariance:", "Time Invariant" if time_invariant else "Time Variant")
    
    [w,mag,phase] = bode(system)
    
    plt.figure(figsize=(12,8))
    plt.subplot(2,1,1)
    plt.semilogx(w, mag)
    plt.title('Bode Magnitude Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Magnitude [dB]')
    plt.grid()
    plt.subplot(2, 1, 2)
    plt.semilogx(w, phase)
    plt.title('Bode Phase Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Phase [degrees]')
    plt.grid()
    plt.tight_layout()
    plt.show()
    

num = [1]
den = [1,-1]
analyze_z_transfer_function(num, den)


#Q2
'''def analyze_z_transfer_function(num, den):
    system=TransferFunction(num, den)
    
    zeros = system.zeros
    poles = system.poles
    print("Zeros:",zeros)
    print("Poles:",poles)
    
    #Srability analysis
    stable = all(np.abs(pole)<1 for pole in poles)
    print("Stability:", "Stable" if stable else "Unstable")
    
    #Casuality analysis
    casual = all(num[i] == 0 for i in range(len(num)-1) if num[i+1] == 0)
    print("Casuality:", "Causal" if casual else "Non-Casual")
    
    #Time Invariance analysis
    time_invariant = True 
    print("Time Invariance:", "Time Invariant" if time_invariant else "Time Variant")
    
    [w,mag,phase] = bode(system)
    
    plt.figure(figsize=(12,8))
    plt.subplot(2,1,1)
    plt.semilogx(w, mag)
    plt.title('Bode Magnitude Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Magnitude [dB]')
    plt.grid()
    plt.subplot(2, 1, 2)
    plt.semilogx(w, phase)
    plt.title('Bode Phase Plot')
    plt.xlabel('Frequency [rad/s]')
    plt.ylabel('Phase [degrees]')
    plt.grid()
    plt.tight_layout()
    plt.show()
    

num = [0.5,-0.8,0.315]
den = [1,-1,0.24]
analyze_z_transfer_function(num, den)'''
    
    