from qiskit import *
import math

class LightsOutQSolver:
    def __init__(self, n) -> None:
        self._n = n
        self._switch = QuantumRegister(self._n**2, "switch")
        self._bulb = QuantumRegister(self._n**2, "bulb")
        self._output = QuantumRegister(1, "output")
        self._result = ClassicalRegister(self._n**2, "result")
        self._qc = QuantumCircuit(self._switch, self._bulb, self._output, self._result)
    
    def _initalize(self,lights)->None:
        ## mapping the initial bulb state to the given inital lights state
        for idx, light in enumerate(lights):
            if light:
                self._qc.x(self._bulb[idx])
        #initializating |S>
        self._qc.h(self._switch)
        ## initialize the state of the output qubit for phase kickback
        self._qc.x(self._output)
        self._qc.h(self._output)

    def _switch_flip(self)->None:
        for i in range(self._n**2):
            #performing the cnot gate on current position
            self._qc.cx(self._switch[i],self._bulb[i])
            
            #which bulbs to perform the switch on horizontally 
            if i%self._n==0:
                self._qc.cx(self._switch[i],self._bulb[i+1])
            elif (i+1)%self._n == 0:
                self._qc.cx(self._switch[i],self._bulb[i-1])
            else:
                self._qc.cx(self._switch[i],self._bulb[i+1])
                self._qc.cx(self._switch[i],self._bulb[i-1])
            #which bulbs to perform the switch oself.n vertically 
            if i//self._n==0:        
                self._qc.cx(self._switch[i],self._bulb[i+self._n])
            elif i//self._n == self._n-1:
                self._qc.cx(self._switch[i],self._bulb[i-self._n])
            else:
                self._qc.cx(self._switch[i],self._bulb[i-self._n])
                self._qc.cx(self._switch[i],self._bulb[i+self._n])

    @property 
    def iterations(self)->int:
        N = 2**(self._n**2)
        return int(math.pi/4 * math.sqrt(N)) 


    def _perform_iterations(self)->None:
        for i in range(self.iterations):
            self._switch_flip()

            # checking for the winner-state
            self._qc.x(self._bulb)                  #flipping the bulbs
            self._qc.mct(self._bulb, self._output)        #if all bulbs are on the output qubit will be flipped based on the action of tofflie gate
            #resetting (uncomputing)
            self._qc.x(self._bulb)          
            self._switch_flip()
            # diffuser
            self._qc.h(self._switch)
            self._qc.x(self._switch)
            self._qc.h(self._switch[-1])
            self._qc.mct(self._switch[0:-1], self._switch[-1])
            self._qc.h(self._switch[-1])
            self._qc.x(self._switch)
            self._qc.h(self._switch)
    
       

    def run_algorithm(self, lights)->list:
        self._initalize(lights)
        self._perform_iterations()
        # Measure:
        self._qc.reverse_bits()
        self._qc.measure(self._switch, self._result)

        sim = Aer.get_backend('qasm_simulator')
        job = execute(self._qc, backend=sim, shots=1000)
        result = job.result()
        count = result.get_counts()

        max_label = max(count, key=count.get)[::-1]
        actions = list(map(lambda x: int(x), list(max_label)))

        return actions
        