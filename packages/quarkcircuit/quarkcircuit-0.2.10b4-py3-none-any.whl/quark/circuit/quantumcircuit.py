# Copyright (c) 2024 XX Xiao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r""" 
This module contains the QuantumCircuit class, which offers an intuitive interface for designing, visualizing, 
and converting quantum circuits in various formats such as OpenQASM 2.0 and qlisp.
"""

import re, copy

from IPython.display import display, HTML
import numpy as np

from .utils import u3_decompose, zyz_decompose, kak_decompose
from .matrix import h_mat

def is_multiple_of_pi(n, tolerance: float = 1e-9) -> str:
    r"""
    Determines if a given number is approximately a multiple of π (pi) within a given tolerance.

    Args:
        n (float): The number to be checked.
        tolerance (float, optional): The allowable difference between the number and a multiple of π. Defaults to 1e-9.

    Returns:
        str: A string representation of the result. If the number is close to a multiple of π, 
             it returns a string in the form of "kπ" where k is a rounded multiplier (e.g., "2π" for 2 x π).
             If n is approximately 0, it returns "0.0".
             Otherwise, it returns a string representation of the number rounded to three decimal places.
    """
    result = n / np.pi
    aprox = round(result,2)
    if abs(result - aprox) < tolerance:
        if np.allclose(aprox, 0.0):
            return str(0.0)
        else:
            expression = f'{aprox}π'
            return expression
    else:
        return str(round(n,3))
    
def parse_expression(expr):
    return eval(expr, {"pi": np.pi, "np": np})

one_qubit_gates_available = {
    'id':'I', 'x':'X', 'y':'Y', 'z':'Z',
    's':'S', 'sdg':'Sdg','t':'T', 'tdg':'Tdg',
    'h':'H', 'sx':'√X','sxdg':'√Xdg',
    }
two_qubit_gates_available = {
    'cx':'●X', 'cnot':'●X', 'cy':'●Y', 'cz':'●Z', 'swap':'XX', 'iswap':'✶✶',
    }
one_qubit_parameter_gates_available = {'rx':'Rx', 'ry':'Ry', 'rz':'Rz', 'p':'P', 'u':'U','r':'R'}
two_qubit_parameter_gates_available = {'rxx':'Rxx', 'ryy':'Ryy', 'rzz':'Rzz',}
functional_gates_available = {'barrier':'░', 'measure':'M', 'reset':'|0>','delay':'Delay'}

class QuantumCircuit:
    r"""
    A class used to build and manipulate a quantum circuit.

    This class allows you to create quantum circuits with a specified number of quantum and classical bits. 
    The circuit can be customized using various quantum gates, and additional features (such as simulation support, 
    circuit summary, and more) will be added in future versions.
    
    Attributes:
        nqubits (int or None): Number of quantum bits in the circuit.
        ncbits (int or None): Number of classical bits in the circuit.
    """
    def __init__(self, *args):
        r"""
        Initialize a QuantumCircuit object.

        The constructor supports three different initialization modes:
        1. `QuantumCircuit()`: Creates a circuit with `nqubits` and `ncbits` both set to `None`.
        2. `QuantumCircuit(nqubits)`: Creates a circuit with the specified number of quantum bits (`nqubits`), 
        and classical bits (`ncbits`) set to the same value as `nqubits`.
        3. `QuantumCircuit(nqubits, ncbits)`: Creates a circuit with the specified number of quantum bits (`nqubits`) 
        and classical bits (`ncbits`).

        Args:
            *args: Variable length argument list used to specify the number of qubits and classical bits.

        Raises:
            ValueError: If more than two arguments are provided, or if the arguments are not in one of the specified valid forms.
        """
        if len(args) == 0:
            self.nqubits = None
            self.ncbits = self.nqubits
            self.qubits = []
        elif len(args) == 1:
            self.nqubits = args[0]
            self.ncbits = self.nqubits
            self.qubits = [i for i in range(self.nqubits)]
        elif len(args) == 2:
            self.nqubits = args[0]
            self.ncbits = args[1]
            self.qubits = [i for i in range(self.nqubits)]
        else:
            raise ValueError("Support only QuantumCircuit(), QuantumCircuit(nqubits) or QuantumCircuit(nqubits,ncbits).")
        
        self.from_openqasm2_str = None

        self.gates = []
        self.physical_qubits_espression = False

        self.params_value = {}

    def adjust_index(self,thres:int):
        gates = []
        for gate_info in self.gates:
            gate = gate_info[0]
            if gate in one_qubit_gates_available.keys():
                qubit = gate_info[-1] + thres
                gates.append((gate,qubit))
            elif gate in two_qubit_gates_available.keys():
                qubit1 = gate_info[1] + thres
                qubit2 = gate_info[2] + thres
                gates.append((gate,qubit1,qubit2))
            elif gate in one_qubit_parameter_gates_available.keys():
                qubit = gate_info[-1] + thres
                gates.append((gate,*gate_info[1:-1],qubit))
            elif gate in ['reset']:
                qubit = gate_info[-1] + thres
                gates.append((gate,qubit))
            elif gate in ['barrier']:
                qubits = [idx + thres for idx in gate_info[1]]
                gates.append((gate,tuple(qubits)))
            elif gate in ['measure']:
                qubits = [idx + thres for idx in gate_info[1]]
                gates.append((gate,qubits,gate_info[-1]))
        self.gates = gates   
        self.nqubits = self.nqubits + thres
        self.qubits = [idx + thres for idx in self.qubits] 

    def from_openqasm2(self,openqasm2_str: str) -> None:
        r"""
        Initializes the QuantumCircuit object based on the given OpenQASM 2.0 string.

        Args:
            openqasm2_str (str): A string representing a quantum circuit in OpenQASM 2.0 format.
        """
        assert('OPENQASM 2.0' in openqasm2_str)
        self.from_openqasm2_str = openqasm2_str
        #self.nqubits = int(re.findall(r"\d+\.?\d*", openqasm2_str.split('qreg')[1].split(';')[0])[0])
        #if 'creg' in openqasm2_str:
        #    self.ncbits = int(re.findall(r"\d+\.?\d*", openqasm2_str.split('creg')[1].split(';')[0])[0])
        #else:
        #    self.ncbits = self.nqubits
        ## update self.gates
        #self.qubits = [i for i in range(self.nqubits)]
        new_gates,qubit_used,cbit_used = self._openqasm2_to_gates()
        self.nqubits = max(qubit_used, default=0) + 1 
        self.ncbits = max(cbit_used, default=0) + 1
        self.qubits = list(qubit_used) #[i for i in range(self.nqubits)]
        self.gates = new_gates
        return self
    
    def from_qlisp(self, qlisp: list|str) -> None:
        r"""
        Initializes the QuantumCircuit object based on the given qlisp list.

        Args:
            qlisp (list): A list representing a quantum circuit in qlisp format.
        """
        if isinstance(qlisp, str):
            import ast
            qlisp = ast.literal_eval(qlisp)
        new_gates, qubit_used,cbit_used = self._qlisp_to_gates(qlisp)
        self.nqubits = max(qubit_used, default=0) + 1 
        self.ncbits = max(cbit_used, default=0) + 1
        self.qubits = list(qubit_used) #[i for i in range(self.nqubits)]
        self.gates = new_gates
        return self

    def id(self, qubit: int) -> None:
        r"""
        Add a Identity gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('id', qubit))
        else:
            raise ValueError("Qubit index out of range")

    def x(self, qubit: int) -> None:
        r"""
        Add a X gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('x', qubit))
        else:
            raise ValueError("Qubit index out of range")

    def y(self, qubit: int) -> None:
        r"""
        Add a Y gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('y', qubit))
        else:
            raise ValueError("Qubit index out of range")

    def z(self, qubit: int) -> None:
        r"""
        Add a Z gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('z', qubit))
        else:
            raise ValueError("Qubit index out of range")

    def s(self, qubit: int) -> None:
        r"""
        Add a S gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('s', qubit))
        else:
            raise ValueError("Qubit index out of range")

    def sdg(self, qubit: int) -> None:
        r"""
        Add a S dagger gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('sdg', qubit))
        else:
            raise ValueError("Qubit index out of range")

    def sx(self, qubit: int) -> None:
        r"""
        Add a Sqrt(X) gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('sx', qubit))
        else:
            raise ValueError("Qubit index out of range")
        
    def sxdg(self, qubit: int) -> None:
        r"""
        Add a Sqrt(X) dagger gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('sxdg', qubit))
        else:
            raise ValueError("Qubit index out of range")

    def t(self, qubit: int) -> None:
        r"""
        Add a T gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('t', qubit))
        else:
            raise ValueError("Qubit index out of range")

    def tdg(self, qubit: int) -> None:
        r"""Add a T dagger gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('tdg', qubit))
        else:
            raise ValueError("Qubit index out of range")
               
    def h(self, qubit: int) -> None:
        r"""
        Add a H gate.

        Args:
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('h', qubit))
        else:
            raise ValueError("Qubit index out of range")

    def swap(self, qubit1: int, qubit2: int) -> None:
        r"""
        Add a SWAP gate.

        Args:
            qubit1 (int): The first qubit to apply the gate to.
            qubit2 (int): The second qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if max(qubit1,qubit2) < self.nqubits:
            self.gates.append(('swap', qubit1,qubit2))
        else:
            raise ValueError("Qubit index out of range")
        
    def iswap(self, qubit1: int, qubit2: int) -> None:
        r"""
        Add a ISWAP gate.

        Args:
            qubit1 (int): The first qubit to apply the gate to.
            qubit2 (int): The second qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if max(qubit1, qubit2) < self.nqubits:
            self.gates.append(('iswap', qubit1,qubit2))
        else:
            raise ValueError("Qubit index out of range")
        
    def cx(self, control_qubit: int, target_qubit: int):
        r"""
        Add a CX gate.

        Args:
            control_qubit (int): The qubit used as control.
            target_qubit (int): The qubit targeted by the gate.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if max(control_qubit,target_qubit) < self.nqubits:
            self.gates.append(('cx', control_qubit,target_qubit))
        else:
            raise ValueError("Qubit index out of range")
        
    def cnot(self, control_qubit: int, target_qubit: int) -> None:
        r"""
        Add a CNOT gate.

        Args:
            control_qubit (int): The qubit used as control.
            target_qubit (int): The qubit targeted by the gate.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if max(control_qubit,target_qubit) < self.nqubits:
            self.cx(control_qubit, target_qubit)
        else:
            raise ValueError("Qubit index out of range")
                
    def cy(self, control_qubit: int, target_qubit: int) -> None:
        r"""
        Add a CY gate.

        Args:
            control_qubit (int): The qubit used as control.
            target_qubit (int): The qubit targeted by the gate.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if max(control_qubit,target_qubit) < self.nqubits:
            self.gates.append(('cy', control_qubit,target_qubit))
        else:
            raise ValueError("Qubit index out of range")
        
    def cz(self, control_qubit: int, target_qubit: int) -> None:
        r"""
        Add a CZ gate.

        Args:
            control_qubit (int): The qubit used as control.
            target_qubit (int): The qubit targeted by the gate.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if max(control_qubit,target_qubit) < self.nqubits:
            self.gates.append(('cz', control_qubit,target_qubit))
        else:
            raise ValueError("Qubit index out of range")

    def p(self, theta: float, qubit: int) -> None:
        r"""
        Add a Phase gate.

        Args:
            theta (float): The rotation angle of the gate.
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('p', theta, qubit))
            if isinstance(theta,str):
                self.params_value[theta] = theta
        else:
            raise ValueError("Qubit index out of range")
        
    def r(self, theta: float, phi:float, qubit: int) -> None:
        r"""
        Add a R gate.

        $$
        R(\theta,\phi) = e^{-i\frac{\theta}{2}(\cos{\phi x}+\sin{\phi y})} = \begin{bmatrix}
         \cos(\frac{\theta}{2})             & -i e^{-i\phi}\sin(\frac{\theta}{2}) \\
         -i e^{i\phi}\sin(\frac{\theta}{2}) & \cos(\frac{\theta}{2})      
        \end{bmatrix}
        $$

        Args:
            theta (float): The rotation angle of the gate.
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('r', theta, phi, qubit))
            if isinstance(theta,str):
                self.params_value[theta] = theta
            if isinstance(phi,str):
                self.params_value[phi] = phi
        else:
            raise ValueError("Qubit index out of range")
        
    def u(self, theta: float, phi: float, lamda: float, qubit: int) -> None:
        r"""
        Add a U3 gate.

        The U3 gate is a single-qubit gate with the following matrix representation:

        $$
        U3(\theta, \phi, \lambda) = \begin{bmatrix}
            \cos(\theta/2) & -e^{i\lambda} \sin(\theta/2) \\
            e^{i\phi} \sin(\theta/2) & e^{i(\phi + \lambda)} \cos(\theta/2)
            \end{bmatrix}
        $$

        Args:
            theta (float): The rotation angle of the gate.
            phi (float): The rotation angle of the gate.
            lamda (float): The rotation angle of the gate.
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('u', theta, phi, lamda, qubit))
            if isinstance(theta,str):
                self.params_value[theta] = theta
            if isinstance(phi,str):
                self.params_value[phi] = phi
            if isinstance(lamda,str):
                self.params_value[lamda] = lamda
        else:
            raise ValueError("Qubit index out of range")

    def rx(self, theta: float, qubit: int) -> None:
        r"""
        Add a RX gate.

        Args:
            theta (float): The rotation angle of the gate.
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('rx', theta, qubit))
            if isinstance(theta,str):
                self.params_value[theta] = theta
        else:
            raise ValueError("Qubit index out of range")
        
    def ry(self, theta: float, qubit: int) -> None:
        r"""
        Add a RY gate.

        Args:
            theta (float: The rotation angle of the gate.
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('ry', theta, qubit))
            if isinstance(theta,str):
                self.params_value[theta] = theta
        else:
            raise ValueError("Qubit index out of range")
        
    def rz(self, theta: float, qubit: int) -> None:
        r"""
        Add a RZ gate.

        Args:
            theta (float): The rotation angle of the gate.
            qubit (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('rz', theta, qubit))
            if isinstance(theta,str):
                self.params_value[theta] = theta
        else:
            raise ValueError("Qubit index out of range")
        
    def rxx(self, theta: float, qubit1: int, qubit2:int) -> None:
        r"""
        Add a RXX gate.

        $$
        Rxx(\theta) = e^{-i\frac{\theta}{2}X\otimes X} = 
        \begin{bmatrix}
         \cos(\frac{\theta}{2})  & 0 & 0 & -i\sin(\frac{\theta}{2}) \\
         0 & \cos(\frac{\theta}{2}) & -i\sin(\frac{\theta}{2}) & 0 \\
         0 & -i\sin(\frac{\theta}{2}) & \cos(\frac{\theta}{2}) & 0 \\
         -i\sin(\frac{\theta}{2}) & 0 & 0 & \cos(\frac{\theta}{2})
        \end{bmatrix}.
        $$

        Args:
            theta (float): The rotation angle of the gate.
            qubit1 (int): The qubit to apply the gate to.
            qubit2 (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if max(qubit1, qubit2) < self.nqubits:
            self.gates.append(('rxx', theta, qubit1, qubit2))
            if isinstance(theta,str):
                self.params_value[theta] = theta
        else:
            raise ValueError("Qubit index out of range")
        
    def ryy(self, theta: float, qubit1: int, qubit2:int) -> None:
        r"""
        Add a RYY gate.

        $$
        Ryy(\theta) = e^{-i\frac{\theta}{2}Y\otimes Y} = 
        \begin{bmatrix}
         \cos(\frac{\theta}{2})  & 0 & 0 & i\sin(\frac{\theta}{2}) \\
         0 & \cos(\frac{\theta}{2}) & -i\sin(\frac{\theta}{2}) & 0 \\
         0 & -i\sin(\frac{\theta}{2}) & \cos(\frac{\theta}{2}) & 0 \\
         i\sin(\frac{\theta}{2}) & 0 & 0 & \cos(\frac{\theta}{2})
        \end{bmatrix}.
        $$

        Args:
            theta (float): The rotation angle of the gate.
            qubit1 (int): The qubit to apply the gate to.
            qubit2 (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if max(qubit1, qubit2) < self.nqubits:
            self.gates.append(('ryy', theta, qubit1, qubit2))
            if isinstance(theta,str):
                self.params_value[theta] = theta
        else:
            raise ValueError("Qubit index out of range")
        
    def rzz(self, theta: float, qubit1: int, qubit2:int) -> None:
        r"""
        Add a RZZ gate.

        $$
        Rzz(\theta) = e^{-i\frac{\theta}{2}Z\otimes Z} = 
        \begin{bmatrix}
         e^{-i\frac{\theta}{2}}  & 0 & 0 & 0 \\
         0 & e^{i\frac{\theta}{2}} & 0 & 0 \\
         0 & 0 & e^{i\frac{\theta}{2}} & 0 \\
         0 & 0 & 0 & e^{-i\frac{\theta}{2}}
        \end{bmatrix}.
        $$

        Args:
            theta (float): The rotation angle of the gate.
            qubit1 (int): The qubit to apply the gate to.
            qubit2 (int): The qubit to apply the gate to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if max(qubit1, qubit2) < self.nqubits:
            self.gates.append(('rzz', theta, qubit1, qubit2))
            if isinstance(theta,str):
                self.params_value[theta] = theta
        else:
            raise ValueError("Qubit index out of range")
        
    def shallow_apply_value(self,params_dic):
        for k,v in self.params_value.items():
            self.params_value[k] = k
        for k,v in params_dic.items():
            self.params_value[k] = v

    def deep_apply_value(self,params_dic):
        for k,v in self.params_value.items():
            self.params_value[k] = k

        gates = []
        for gate_info in self.gates:
            gate = gate_info[0]
            if gate in one_qubit_parameter_gates_available.keys():
                param = gate_info[1]
                qubit = gate_info[-1]
                if param in params_dic.keys():
                    param = params_dic[param]
                    del self.params_value[gate_info[1]]
                    gate_info = (gate,param,qubit)
            gates.append(gate_info)
        self.gates = gates

    def u3_for_unitary(self, unitary: np.ndarray, qubit: int):
        r"""
        Decomposes a 2x2 unitary matrix into a U3 gate and applies it to a specified qubit.

        Args:
            unitary (np.ndarray): A 2x2 unitary matrix.
            qubit (int): The qubit to apply the gate to.
        """
        assert(unitary.shape == (2,2))
        theta,phi,lamda,phase = u3_decompose(unitary)
        self.gates.append(('u', theta, phi, lamda, qubit))

    def zyz_for_unitary(self, unitary: np.ndarray, qubit:int) -> None:
        r"""
        Decomposes a 2x2 unitary matrix into Rz-Ry-Rz gate sequence and applies it to a specified qubit.

        Args:
            unitary (np.ndarray): A 2x2 unitary matrix.
            qubit (int): The qubit to apply the gate sequence to.
        """
        assert(unitary.shape == (2,2))
        theta, phi, lamda, alpha = zyz_decompose(unitary)
        self.gates.append(('rz', lamda, qubit))
        self.gates.append(('ry', theta, qubit))
        self.gates.append(('rz', phi, qubit))

    def kak_for_unitary(self, unitary: np.ndarray, qubit1: int, qubit2: int) -> None:
        r"""
        Decomposes a 4 x 4 unitary matrix into a sequence of CZ and U3 gates using KAK decomposition and applies them to the specified qubits.

        Args:
            unitary (np.ndarray): A 4 x 4 unitary matrix.
            qubit1 (int): The first qubit to apply the gates to.
            qubit2 (int): The second qubit to apply the gates to.
        """
        assert(unitary.shape == (4,4))
        rots1, rots2 = kak_decompose(unitary)
        self.u3_for_unitary(rots1[0], qubit1)
        self.u3_for_unitary(h_mat @ rots2[0], qubit2)
        self.gates.append(('cz', qubit1, qubit2))
        self.u3_for_unitary(rots1[1], qubit1)
        self.u3_for_unitary(h_mat @ rots2[1] @ h_mat, qubit2)
        self.gates.append(('cz', qubit1, qubit2))
        self.u3_for_unitary(rots1[2], qubit1)
        self.u3_for_unitary(h_mat @ rots2[2] @ h_mat, qubit2)
        self.gates.append(('cz', qubit1, qubit2))        
        self.u3_for_unitary(rots1[3], qubit1)
        self.u3_for_unitary(rots2[3] @ h_mat, qubit2)

    def reset(self, qubit: int) -> None:
        r"""
        Add reset to qubit.

        Args:
            qubit (int): The qubit to apply the instruction to.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if qubit < self.nqubits:
            self.gates.append(('reset', qubit))
        else:
            raise ValueError("Qubit index out of range")
        
    def delay(self,duration:int|float, *qubits:tuple[int],unit='ns') ->None:
        r"""
        Adds delay to qubits, the unit is ns.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        # convert 's' 'ms' 'us' to 'ns
        if unit == 's':
            duration = duration * 1e9
        elif unit == 'ms':
            duration = duration * 1e6
        elif unit =='us':
            duration = duration * 1e3

        if not qubits: # it will add barrier for all qubits
            self.gates.append(('delay', duration, tuple(self.qubits)))
        else:
            if max(qubits) < self.nqubits:
                self.gates.append(('delay', duration, qubits))
            else:
                raise ValueError("Qubit index out of range")
        
    def barrier(self,*qubits: tuple[int]) -> None:
        r"""
        Adds barrier to qubits.

        Raises:
            ValueError: If qubit out of circuit range.
        """
        if not qubits: # it will add barrier for all qubits
            self.gates.append(('barrier', tuple(self.qubits)))
        else:
            if max(qubits) < self.nqubits:
                self.gates.append(('barrier', qubits))
            else:
                raise ValueError("Qubit index out of range")
            
    def remove_barrier(self) -> 'QuantumCircuit':
        r"""
        Remove all barrier gates from the quantum circuit.

        Returns:
            QuantumCircuit: The updated quantum circuit with all barrier gates removed.
        """
        new = []
        for gate_info in self.gates:
            gate  = gate_info[0]
            if gate != 'barrier':
                new.append(gate_info)
        self.gates = new
        return self
    
    def measure(self,qubitlst: int | list, cbitlst: int | list) -> None:
        r"""Adds measurement to qubits.

        Args:
            qubitlst (int | list): Qubit(s) to measure.
            cbitlst (int | list): Classical bit(s) to place the measure results in.
        """
        if type(qubitlst) == list:
            self.gates.append(('measure', qubitlst,cbitlst))
        else:
            self.gates.append(('measure', [qubitlst],[cbitlst]))

    def measure_all(self) -> None:
        r"""
        Adds measurement to all qubits.
        """
        qubitlst = [i for i in sorted(self.qubits)]
        cbitlst = [i for i in range(len(qubitlst))]
        #cbitlst = [i for i in range(self.ncbits)]
        self.gates.append(('measure', qubitlst,cbitlst))

    @property
    def to_latex(self) -> str:
        print('If you need this feature, please contact the developer.')    

    @property
    def to_openqasm2(self) -> str:
        r"""
        Export the quantum circuit to an OpenQASM 2 program in a string.

        Returns:
            str: An OpenQASM 2 string representing the circuit.
        """
        qasm_str = "OPENQASM 2.0;\n"
        qasm_str += "include \"qelib1.inc\";\n"
        gates0 = [gate[0] for gate in self.gates]
        if 'delay' in gates0:
            qasm_str += "opaque delay(param0) q0;\n"
        if 'r' in gates0:
            qasm_str += "gate r(param0,param1) q0 { u3(param0,param1 - pi/2,pi/2 - param1) q0; }\n"
        qasm_str += f"qreg q[{self.nqubits}];\n"
        qasm_str += f"creg c[{self.ncbits}];\n"
        for gate in self.gates:
            if gate[0] in one_qubit_gates_available.keys(): # single qubit gate 
                qasm_str += f"{gate[0]} q[{gate[1]}];\n"
            elif gate[0] in two_qubit_gates_available.keys(): # two qubit gate 
                qasm_str += f"{gate[0]} q[{gate[1]}],q[{gate[2]}];\n"
            elif gate[0] in two_qubit_parameter_gates_available.keys():
                if isinstance(gate[1],float):
                    theta = gate[1]
                elif isinstance(gate[1],str):
                    param = self.params_value[gate[1]]
                    if isinstance(param,float):
                        theta = param
                    else:
                        raise(ValueError(f'please apply value for parameter {param}')) 
                qasm_str += f"{gate[0]}({theta}) q[{gate[2]}],q[{gate[3]}];\n"                        
            elif gate[0] in one_qubit_parameter_gates_available.keys():
                if gate[0] == 'u':
                    if isinstance(gate[1],float):
                        theta = gate[1]
                    elif isinstance(gate[1],str):
                        param = self.params_value[gate[1]]
                        if isinstance(param,float):
                            theta = param
                        else:
                            raise(ValueError(f'please apply value for parameter {param}')) 
                        
                    if isinstance(gate[2],float):
                        phi = gate[2]
                    elif isinstance(gate[2],str):
                        param = self.params_value[gate[2]]
                        if isinstance(param,float):
                            phi = param
                        else:
                            raise(ValueError(f'please apply value for parameter {param}')) 
                        
                    if isinstance(gate[3],float):
                        lamda = gate[3]
                    elif isinstance(gate[3],str):
                        param = self.params_value[gate[3]]
                        if isinstance(param,float):
                            lamda = param
                        else:
                            raise(ValueError(f'please apply value for parameter {param}')) 
                        
                    qasm_str += f"{gate[0]}({theta},{phi},{lamda}) q[{gate[-1]}];\n"
                elif gate[0] == 'r':
                    if isinstance(gate[1],float):
                        theta = gate[1]
                    elif isinstance(gate[1],str):
                        param = self.params_value[gate[1]]
                        if isinstance(param,float):
                            theta = param
                        else:
                            raise(ValueError(f'please apply value for parameter {param}')) 
                        
                    if isinstance(gate[2],float):
                        phi = gate[2]
                    elif isinstance(gate[2],str):
                        param = self.params_value[gate[2]]
                        if isinstance(param,float):
                            phi = param
                        else:
                            raise(ValueError(f'please apply value for parameter {param}')) 
                        
                    qasm_str += f"{gate[0]}({theta},{phi}) q[{gate[-1]}];\n"

                else:
                    if isinstance(gate[1],float):
                        qasm_str += f"{gate[0]}({gate[1]}) q[{gate[2]}];\n"
                    elif isinstance(gate[1],str):
                        param = self.params_value[gate[1]]
                        if isinstance(param,float):
                            qasm_str += f"{gate[0]}({param}) q[{gate[2]}];\n"
                        else:
                            raise(ValueError(f'please apply value for parameter {param}')) 
            elif gate[0] in ['reset']:
                qasm_str += f"{gate[0]} q[{gate[1]}];\n"
            elif gate[0] in ['delay']:
                for qubit in gate[2]:
                    qasm_str += f"{gate[0]}({gate[1]}) q[{qubit}];\n"
            elif gate[0] in ['barrier']:
                qasm_str += f"{gate[0]} q[{gate[1][0]}]"
                for idx in gate[1][1:]:
                    qasm_str += f",q[{idx}]"
                qasm_str += ';\n'
            elif gate[0] in ['measure']:
                for idx in range(len(gate[1])):
                    qasm_str += f"{gate[0]} q[{gate[1][idx]}] -> c[{gate[2][idx]}];\n"
            else:
                raise(ValueError(f"Sorry, Quark could not find the corresponding OpenQASM 2.0 syntax for now. Please contact the developer for assistance.{gate[0]}"))
        return qasm_str.rstrip('\n')
    
    def _openqasm2_to_gates(self) -> None:
        r"""
        Parse gate information from an input OpenQASM 2.0 string, and update self.gates
        """
        new = []
        qubit_used = []
        cbit_used = []
        for line in self.from_openqasm2_str.splitlines():
            if line == '':
                continue
            gate = line.split()[0].split('(')[0]
            position = [int(num) for num in re.findall(r'\d+', line)]
            if gate in one_qubit_gates_available.keys():
                new.append((gate,position[0]))
                qubit_used.append(position[0])
            elif gate in two_qubit_gates_available.keys():
                new.append((gate,position[0],position[1]))
                qubit_used.append(position[0])
                qubit_used.append(position[1])
            elif gate in one_qubit_parameter_gates_available.keys():
                if gate == 'u':
                    params_str = re.search(r'\(([^)]+)\)', line).group(1).split(',')
                    params = [parse_expression(i) for i in params_str]
                    new.append((gate, params[0], params[1], params[2], position[-1]))
                    qubit_used.append(position[-1])
                elif gate == 'r':
                    params_str = re.search(r'\(([^)]+)\)', line).group(1).split(',')
                    params = [parse_expression(i) for i in params_str]
                    new.append((gate, params[0], params[1], position[-1]))
                    qubit_used.append(position[-1])
                else:
                    param_str = re.search(r'\(([^)]+)\)', line).group(1)
                    param = parse_expression(param_str)
                    new.append((gate, param, position[-1]))
                    qubit_used.append(position[-1])
            elif gate in two_qubit_parameter_gates_available.keys():
                param_str = re.search(r'\(([^)]+)\)', line).group(1)
                param = parse_expression(param_str)
                new.append((gate, param, position[-2], position[-1]))
                qubit_used.append(position[-2])
                qubit_used.append(position[-1])
            elif gate in ['delay']:
                param = float(re.search(r'\(([^)]+)\)', line).group(1))
                new.append((gate,param,(position[-1],)))
                qubit_used.append(position[-1])
            elif gate in ['reset']:
                new.append((gate,position[0]))
                qubit_used.append(position[0])
            elif gate in ['barrier']:
                new.append((gate, tuple(position)))
                qubit_used += list(position)
            elif gate in ['measure']:
                new.append((gate, [position[0]], [position[1]])) 
                qubit_used.append(position[0])
                cbit_used.append(position[1])
            elif gate in ['OPENQASM','include','opaque','gate','qreg','creg']:
                continue
            else:
                raise(ValueError(f"Sorry, an unrecognized OpenQASM 2.0 syntax was detected by quarkcircuit. Please contact the developer for assistance.{gate}"))
        return new,set(qubit_used),set(cbit_used)

    
    @property
    def to_qlisp(self) -> list:
        r"""Export the quantum circuit to qlisp list.

        Returns:
            list: qlisp list
        """
        qlisp = []
        for gate_info in self.gates:
            gate = gate_info[0]
            if gate in ['x', 'y', 'z', 's', 't', 'h']:
                qlisp.append((gate.upper(), 'Q'+str(gate_info[1])))
            elif gate in ['id']:
                qlisp.append(('I', 'Q'+str(gate_info[1])))
            elif gate in ['sdg','tdg']:
                qlisp.append(('-' + gate[0].upper(), 'Q'+str(gate_info[1])))
            elif gate in ['sx']:
                qlisp.append(('X/2', 'Q'+str(gate_info[1])))
            elif gate in ['sxdg']:
                qlisp.append(('-X/2', 'Q'+str(gate_info[1])))
            elif gate in ['u']:
                if isinstance(gate_info[1],float):
                    theta = gate_info[1]
                elif isinstance(gate_info[1],str):
                    param = self.params_value[gate_info[1]]
                    if isinstance(param,float):
                        theta = param
                    else:
                        raise(ValueError(f'please apply value for parameter {param}')) 
                    
                if isinstance(gate_info[2],float):
                    phi = gate_info[2]
                elif isinstance(gate_info[2],str):
                    param = self.params_value[gate_info[2]]
                    if isinstance(param,float):
                        phi = param
                    else:
                        raise(ValueError(f'please apply value for parameter {param}')) 
                    
                if isinstance(gate_info[3],float):
                    lamda = gate_info[3]
                elif isinstance(gate_info[3],str):
                    param = self.params_value[gate_info[3]]
                    if isinstance(param,float):
                        lamda = param
                    else:
                        raise(ValueError(f'please apply value for parameter {param}'))                    
                qlisp.append((('U', theta, phi, lamda),'Q'+str(gate_info[4])))
            elif gate in ['r']:
                if isinstance(gate_info[1],float):
                    theta = gate_info[1]
                elif isinstance(gate_info[1],str):
                    param = self.params_value[gate_info[1]]
                    if isinstance(param,float):
                        theta = param
                    else:
                        raise(ValueError(f'please apply value for parameter {param}')) 
                    
                if isinstance(gate_info[2],float):
                    phi = gate_info[2]
                elif isinstance(gate_info[2],str):
                    param = self.params_value[gate_info[2]]
                    if isinstance(param,float):
                        phi = param
                    else:
                        raise(ValueError(f'please apply value for parameter {param}')) 
                if abs(theta-np.pi/2) < 1e-9:
                    qlisp.append((('R', phi),'Q'+str(gate_info[3])))
                else:
                    qlisp.append((('U', theta, phi-np.pi/2, np.pi/2-phi),'Q'+str(gate_info[3])))
                    #qlisp.append((('rfUnitary', theta, phi),'Q'+str(gate_info[3])))
            elif gate in ['cx','cy', 'cz', 'swap']:
                if gate == 'cx':
                    qlisp.append(('Cnot', tuple('Q'+str(i) for i in gate_info[1:])))
                else:
                    qlisp.append((gate.upper(), tuple('Q'+str(i) for i in gate_info[1:])))
            elif gate in ['iswap']:
                qlisp.append(('iSWAP', tuple('Q'+str(i) for i in gate_info[1:])))

            elif gate in ['rx', 'ry', 'rz', 'p']:
                if isinstance(gate_info[1],float):
                    qlisp.append(((gate.capitalize(), gate_info[1]), 'Q'+str(gate_info[2])))
                elif isinstance(gate_info[1],str):
                    param = self.params_value[gate_info[1]]
                    if isinstance(param,float):
                        qlisp.append(((gate.capitalize(),param), 'Q'+str(gate_info[2])))
                    else:
                        raise(ValueError(f'please apply value for parameter {param}')) 
            elif gate in ['delay']:
                for qubit in gate_info[-1]:
                    qlisp.append(((gate.capitalize(),gate_info[1]),'Q'+str(qubit)))
            elif gate in ['reset']:
                qlisp.append((gate.capitalize(), 'Q'+str(gate_info[1])))
            elif gate in ['barrier']:
                qlisp.append((gate.capitalize(), tuple('Q'+str(i) for i in gate_info[1])))
            elif gate in ['measure']:
                for idx,cbit in enumerate(gate_info[2]):
                    qlisp.append(((gate.capitalize(), cbit), 'Q'+str(gate_info[1][idx])))
            else:
                raise(ValueError(f'Sorry, quarkcircuit could not find the corresponding qlisp syntax for now. Please contact the developer for assistance. {gate}'))
        return qlisp
    
    def _qlisp_to_gates(self, qlisp: list) -> tuple[list, list, list]:
        r"""
        Parse gate information from an input qlisp list.

        Args:
            qlisp (list): qlisp

        Returns:
            tuple[list, list, list]: A tuple containing:
                An gate information list.
                An qubit information list.
                An cbit information list.
        """
        new = []
        qubit_used = []
        cbit_used = []
        for gate_info in qlisp:
            gate = gate_info[0]
            if gate in ['X', 'Y', 'Z', 'S', 'T', 'H']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append((gate.lower(), qubit0))
            elif gate in ['Z/2']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append(('s', qubit0))
            elif gate in ['I']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append(('id', qubit0))
            elif gate in ['-S','-T']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append((gate[1].lower() + 'dg', qubit0))
            elif gate in ['-Z/2']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append(('sdg', qubit0))
            elif gate in ['X/2']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append(('sx', qubit0))
            elif gate in ['-X/2']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append(('sxdg', qubit0))
            elif gate[0] in ['u3','U']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append(('u', gate[1], gate[2], gate[3], qubit0))
            elif gate[0] in ['u1']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append(('p', gate[1], qubit0))        
            elif gate[0] in ['u2']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append(('u',np.pi/2, gate[1], gate[2],qubit0))  
            elif gate[0] in ['R']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append(('r',np.pi/2, gate[1], qubit0))  
            #elif gate[0] in ['rfUnitary']:
            #    qubit0 = int(gate_info[1].split('Q')[1])
            #    new.append(('r', gate[1], gate[2], qubit0))
            elif gate in ['Cnot']:
                qubit1 = int(gate_info[1][0].split('Q')[1])
                qubit2 = int(gate_info[1][1].split('Q')[1])
                new.append(('cx', qubit1, qubit2))
            elif gate in ['CX','CY', 'CZ', 'SWAP']:
                qubit1 = int(gate_info[1][0].split('Q')[1])
                qubit2 = int(gate_info[1][1].split('Q')[1])
                new.append((gate.lower(), qubit1, qubit2))
            elif gate in ['iSWAP']:
                qubit1 = int(gate_info[1][0].split('Q')[1])
                qubit2 = int(gate_info[1][1].split('Q')[1])
                new.append(('iswap', qubit1, qubit2))
        
            elif gate[0] in ['Rx', 'Ry', 'Rz', 'P']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append((gate[0].lower(), gate[1], qubit0))
            elif gate in ['Reset']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append((gate.lower(), qubit0))
            elif gate in ['Barrier']:
                qubitn = [int(istr.split('Q')[1]) for istr in gate_info[1]]
                new.append((gate.lower(), tuple(qubitn)))
            elif gate[0] in ['Delay']:
                qubit0 = int(gate_info[1].split('Q')[1])
                new.append((gate[0].lower(), gate[1]/1e9,(qubit0,)))
            elif gate[0] in ['Measure']:
                qubit0 = int(gate_info[1].split('Q')[1])
                cbit0 = gate[1]
                new.append((gate[0].lower(), [qubit0] ,[cbit0]))
            else:
                raise(ValueError(f'Sorry, an unrecognized qlisp syntax was detected by quarkcircuit. Please contact the developer for assistance. {gate[0]}'))

            for var in ['qubit0','qubit1','qubit2']:
                try:
                    qubit_used.append(eval(var))
                except:
                    pass
            try:
                qubit_used += qubitn
            except:
                pass
            try:
                cbit_used.append(cbit0)
            except:
                pass
        
        return new, set(qubit_used), set(cbit_used)
        
    def _initialize_gates(self) -> tuple[list, list]:
        r"""
        Initialize a blank circuit.

        Returns:
            tuple[list,list]: A tuple containing:
                - A list of fake gates element.
                - A list of fake gates element list.
        """
        nlines = 2 * self.nqubits + 1 + len(str(self.ncbits))
        gates_element = list('─ ' * self.nqubits) + ['═'] + [' '] * len(str(self.ncbits))
        gates_initial = copy.deepcopy(gates_element)
        if self.physical_qubits_espression:
            qubits_expression = 'Q'
        else:
            qubits_expression = 'q'
        for i in range(nlines):
            if i in range(0, 2 * self.nqubits, 2):
                qi = i // 2
                if len(str(qi)) == 1:
                    qn = qubits_expression + f'[{qi:<1}]  '
                elif len(str(qi)) == 2:
                    qn = qubits_expression + f'[{qi:<2}] '
                elif len(str(qi)) == 3:
                    qn = qubits_expression + f'[{qi:<3}]'
                gates_initial[i] = qn
            elif i in [2 * self.nqubits]:
                if len(str(self.ncbits)) == 1:
                    c = f'c:  {self.ncbits}/'
                elif len(str(self.ncbits)) == 2:
                    c = f'c: {self.ncbits}/'
                elif len(str(self.ncbits)) == 3:
                    c = f'c:{self.ncbits}/'
                gates_initial[i] = c
            else:
                gates_initial[i] = ' ' * 6   
        n = len(self.gates) + self.nqubits ## 
        gates_layerd = [gates_initial] + [copy.deepcopy(gates_element) for _ in range(n)]
        return gates_element,gates_layerd

    def _generate_gates_layerd_dense(self) -> list:
        r"""Assign gates to their respective layers.

        Returns:
            list: A list of dense gates element list.
        """
        # for count circuit depth
        # ignore barrier
        gates_element,gates_layerd = self._initialize_gates()
        for gate_info in self.gates:
            gate = gate_info[0]
            if gate in one_qubit_gates_available.keys():
                pos0 = gate_info[1]
                for idx in range(len(gates_layerd)-1,-1,-1):
                    if (gates_layerd[idx][2*pos0] != '─' and gates_layerd[idx][2*pos0] != '│'):
                        gates_layerd[idx+1][2*pos0] = one_qubit_gates_available[gate]
                        break
            elif gate in two_qubit_gates_available.keys():
                pos0 = min(gate_info[1],gate_info[2])
                pos1 = max(gate_info[1],gate_info[2])
                for idx in range(len(gates_layerd)-1,-1,-1):
                    if (gates_layerd[idx][2*pos0] not in ['─','│'] or
                       gates_layerd[idx][2*pos1] not in ['─','│']):
                        if pos0 == gate_info[1]: # control qubit
                            gates_layerd[idx+1][2*pos0] = two_qubit_gates_available[gate][0]
                            gates_layerd[idx+1][2*pos1] = two_qubit_gates_available[gate][-1]
                        elif pos0 == gate_info[2]:
                            gates_layerd[idx+1][2*pos0] = two_qubit_gates_available[gate][-1]
                            gates_layerd[idx+1][2*pos1] = two_qubit_gates_available[gate][0]
                        break
            elif gate in two_qubit_parameter_gates_available.keys():
                pos0 = min(gate_info[2],gate_info[3])
                pos1 = max(gate_info[2],gate_info[3])
                if isinstance(gate_info[1],float):
                    theta0_str = is_multiple_of_pi(gate_info[1])
                elif isinstance(gate_info[1],str):
                    param = self.params_value[gate_info[1]]
                    if isinstance(param,float):
                        theta0_str = is_multiple_of_pi(param)
                    elif isinstance(param,str):
                        theta0_str = param
                gate_express = two_qubit_parameter_gates_available[gate]+f'({theta0_str})'
                for idx in range(len(gates_layerd)-1,-1,-1):
                    if (gates_layerd[idx][2*pos0] not in ['─','│'] or
                       gates_layerd[idx][2*pos1] not in ['─','│']):
                        if pos0 == gate_info[2]: 
                            gates_layerd[idx+1][2*pos0] = '0'+gate_express
                            gates_layerd[idx+1][2*pos1] = '1'+gate_express
                        elif pos0 == gate_info[3]:
                            gates_layerd[idx+1][2*pos0] = '1'+gate_express
                            gates_layerd[idx+1][2*pos1] = '0'+gate_express
                        break
            elif gate in one_qubit_parameter_gates_available.keys():
                if gate == 'u':
                    if isinstance(gate_info[1],float):
                        theta0_str = is_multiple_of_pi(gate_info[1])
                    elif isinstance(gate_info[1],str):
                        param = self.params_value[gate_info[1]]
                        if isinstance(param,float):
                            theta0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            theta0_str = param
                    if isinstance(gate_info[2],float):
                        phi0_str = is_multiple_of_pi(gate_info[2])
                    elif isinstance(gate_info[2],str):
                        param = self.params_value[gate_info[2]]
                        if isinstance(param,float):
                            phi0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            phi0_str = param
                    if isinstance(gate_info[3],float):
                        lamda0_str = is_multiple_of_pi(gate_info[3])
                    elif isinstance(gate_info[3],str):
                        param = self.params_value[gate_info[3]]
                        if isinstance(param,float):
                            lamda0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            lamda0_str = param
                    pos0 = gate_info[-1]
                    for idx in range(len(gates_layerd)-1,-1,-1):
                        if (gates_layerd[idx][2*pos0] != '─' and gates_layerd[idx][2*pos0] != '│'):
                            params_str = '(' + theta0_str + ',' + phi0_str + ',' + lamda0_str + ')'
                            gates_layerd[idx+1][2*pos0] = one_qubit_parameter_gates_available[gate] + params_str
                            break      
                elif gate == 'r':      
                    if isinstance(gate_info[1],float):
                        theta0_str = is_multiple_of_pi(gate_info[1])
                    elif isinstance(gate_info[1],str):
                        param = self.params_value[gate_info[1]]
                        if isinstance(param,float):
                            theta0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            theta0_str = param
                    if isinstance(gate_info[2],float):
                        phi0_str = is_multiple_of_pi(gate_info[2])
                    elif isinstance(gate_info[2],str):
                        param = self.params_value[gate_info[2]]
                        if isinstance(param,float):
                            phi0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            phi0_str = param       
                    pos0 = gate_info[-1]
                    for idx in range(len(gates_layerd)-1,-1,-1):
                        if gates_layerd[idx][2*pos0] != '─':
                            params_str = '(' + theta0_str + ',' + phi0_str + ')'
                            gates_layerd[idx+1][2*pos0] = one_qubit_parameter_gates_available[gate] + params_str
                            self.lines_use.append(2*pos0)
                            self.lines_use.append(2*pos0 + 1)
                            break              
                else:
                    if isinstance(gate_info[1],float):
                        theta0_str = is_multiple_of_pi(gate_info[1])
                    elif isinstance(gate_info[1],str):
                        param = self.params_value[gate_info[1]]
                        if isinstance(param,float):
                            theta0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            theta0_str = param
                    pos0 = gate_info[2]
                    for idx in range(len(gates_layerd)-1,-1,-1):
                        if (gates_layerd[idx][2*pos0] != '─' and gates_layerd[idx][2*pos0] != '│'):
                            gates_layerd[idx+1][2*pos0] = one_qubit_parameter_gates_available[gate]+'('+theta0_str+')'
                            break
            elif gate in ['reset']:
                pos0 = gate_info[1]
                for idx in range(len(gates_layerd)-1,-1,-1):
                    if (gates_layerd[idx][2*pos0] != '─' and gates_layerd[idx][2*pos0] != '│'):
                        gates_layerd[idx+1][2*pos0] = functional_gates_available[gate]
                        break
            elif gate in ['delay']:
                poslst0 = gate_info[-1]
                poslst = []
                for j in poslst0:
                    if j + 1 in poslst0:
                        poslst.append(2*j)
                    else:
                        poslst.append(2*j)
                for idx in range(len(gates_layerd)-1,-1,-1):
                    e_ = [gates_layerd[idx][2*i] for i in poslst0]
                    if all(e == '─' for e in e_) is False:
                        for i in poslst:
                            gates_layerd[idx+1][i] = functional_gates_available[gate]+f'({gate_info[1]:.1e}ns)'
                        break
            elif gate in ['measure']:
                for j in range(len(gate_info[1])):
                    pos0 = gate_info[1][j]
                    pos1 = gate_info[2][j]
                    for idx in range(len(gates_layerd)-1,-1,-1):
                        if (gates_layerd[idx][2*pos0] != '─' and gates_layerd[idx][2*pos0] != '│'):
                            gates_layerd[idx+1][2*pos0] = functional_gates_available[gate]
                            break
        
        for idx in range(len(gates_layerd)-1,-1,-1):
            if gates_layerd[idx] != gates_element:
                cut = idx + 1
                break
        return gates_layerd[:cut]
    
    @property
    def depth(self) -> int:
        r"""Count QuantumCircuit depth.

        Returns:
            int: QuantumCircuit depth.
        """
        dense_gates = self._generate_gates_layerd_dense()
        return len(dense_gates)-1
    
    def _generate_gates_layerd(self) -> list:
        r"""Assign gates to their respective layers loosely.

        Returns:
            list: A list of gates element list.
        """
        self.lines_use = []
        # according plot layer distributed gates
        gates_element,gates_layerd = self._initialize_gates()
        for gate_info in self.gates:
            gate = gate_info[0]
            if gate in one_qubit_gates_available.keys():
                pos0 = gate_info[1]
                for idx in range(len(gates_layerd)-1,-1,-1):
                    if gates_layerd[idx][2*pos0] != '─':
                        gates_layerd[idx+1][2*pos0] = one_qubit_gates_available[gate]
                        self.lines_use.append(2 * pos0)
                        self.lines_use.append(2 * pos0 + 1)
                        break
            elif gate in two_qubit_gates_available.keys():
                pos0 = min(gate_info[1],gate_info[2])
                pos1 = max(gate_info[1],gate_info[2])
                for idx in range(len(gates_layerd)-1,-1,-1):
                    if gates_layerd[idx][2*pos0:2*pos1+1] != list('─ ')*(pos1-pos0)+['─']:
                        if pos0 == gate_info[1]: # control qubit
                            gates_layerd[idx+1][2*pos0] = two_qubit_gates_available[gate][0]
                            gates_layerd[idx+1][2*pos1] = two_qubit_gates_available[gate][-1]
                            self.lines_use.append(2*pos0)
                            self.lines_use.append(2*pos0 + 1)
                            self.lines_use.append(2*pos1)
                            self.lines_use.append(2*pos1 + 1)
                        elif pos0 == gate_info[2]:
                            gates_layerd[idx+1][2*pos0] = two_qubit_gates_available[gate][-1]
                            gates_layerd[idx+1][2*pos1] = two_qubit_gates_available[gate][0]
                            self.lines_use.append(2*pos0)
                            self.lines_use.append(2*pos0 + 1)
                            self.lines_use.append(2*pos1)
                            self.lines_use.append(2*pos1 + 1)
                        for i in range(2*pos0+1,2*pos1):
                            gates_layerd[idx+1][i] = '│'
                        break
            elif gate in two_qubit_parameter_gates_available.keys():
                #print(gate_info)
                pos0 = min(gate_info[2],gate_info[3])
                pos1 = max(gate_info[2],gate_info[3])
                if isinstance(gate_info[1],float):
                    theta0_str = is_multiple_of_pi(gate_info[1])
                elif isinstance(gate_info[1],str):
                    param = self.params_value[gate_info[1]]
                    if isinstance(param,float):
                        theta0_str = is_multiple_of_pi(param)
                    elif isinstance(param,str):
                        theta0_str = param
                gate_express = two_qubit_parameter_gates_available[gate]+f'({theta0_str})'
                if len(gate_express)%2 == 0:
                    gate_express += ' '
                for idx in range(len(gates_layerd)-1,-1,-1):
                    if gates_layerd[idx][2*pos0:2*pos1+1] != list('─ ')*(pos1-pos0)+['─']:
                        dif0 = (len(gate_express) - 1)//2
                        if pos0 == gate_info[2]: 
                            gates_layerd[idx+1][2*pos0] = '┌' + '─'*dif0 +'0'+'─'*dif0 + '┐'
                            gates_layerd[idx+1][2*pos1] = '└' + '─'*dif0 +'1'+'─'*dif0 + '┘'
                            self.lines_use.append(2*pos0)
                            self.lines_use.append(2*pos0 + 1)
                            self.lines_use.append(2*pos1)
                            self.lines_use.append(2*pos1 + 1)
                        elif pos0 == gate_info[3]:
                            gates_layerd[idx+1][2*pos0] = '┌' + '─'*dif0 +'1'+'─'*dif0 + '┐'
                            gates_layerd[idx+1][2*pos1] = '└' + '─'*dif0 +'0'+'─'*dif0 + '┘'
                            self.lines_use.append(2*pos0)
                            self.lines_use.append(2*pos0 + 1)
                            self.lines_use.append(2*pos1)
                            self.lines_use.append(2*pos1 + 1)
                        for i in range(2*pos0+1,2*pos1):
                            gates_layerd[idx+1][i] = '│' + ' '*len(gate_express) + '│'
                        gates_layerd[idx+1][2*pos0 + (pos1-pos0)] = '│' + gate_express + '│'

                        break
            elif gate in one_qubit_parameter_gates_available.keys():
                if gate == 'u':
                    if isinstance(gate_info[1],float):
                        theta0_str = is_multiple_of_pi(gate_info[1])
                    elif isinstance(gate_info[1],str):
                        param = self.params_value[gate_info[1]]
                        if isinstance(param,float):
                            theta0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            theta0_str = param
                    if isinstance(gate_info[2],float):
                        phi0_str = is_multiple_of_pi(gate_info[2])
                    elif isinstance(gate_info[2],str):
                        param = self.params_value[gate_info[2]]
                        if isinstance(param,float):
                            phi0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            phi0_str = param
                    if isinstance(gate_info[3],float):
                        lamda0_str = is_multiple_of_pi(gate_info[3])
                    elif isinstance(gate_info[3],str):
                        param = self.params_value[gate_info[3]]
                        if isinstance(param,float):
                            lamda0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            lamda0_str = param

                    pos0 = gate_info[-1]
                    for idx in range(len(gates_layerd)-1,-1,-1):
                        if gates_layerd[idx][2*pos0] != '─':
                            params_str = '(' + theta0_str + ',' + phi0_str + ',' + lamda0_str + ')'
                            gates_layerd[idx+1][2*pos0] = one_qubit_parameter_gates_available[gate] + params_str
                            self.lines_use.append(2*pos0)
                            self.lines_use.append(2*pos0 + 1)
                            break      
                elif gate == 'r':      
                    if isinstance(gate_info[1],float):
                        theta0_str = is_multiple_of_pi(gate_info[1])
                    elif isinstance(gate_info[1],str):
                        param = self.params_value[gate_info[1]]
                        if isinstance(param,float):
                            theta0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            theta0_str = param
                    if isinstance(gate_info[2],float):
                        phi0_str = is_multiple_of_pi(gate_info[2])
                    elif isinstance(gate_info[2],str):
                        param = self.params_value[gate_info[2]]
                        if isinstance(param,float):
                            phi0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            phi0_str = param       
                    pos0 = gate_info[-1]
                    for idx in range(len(gates_layerd)-1,-1,-1):
                        if gates_layerd[idx][2*pos0] != '─':
                            params_str = '(' + theta0_str + ',' + phi0_str + ')'
                            gates_layerd[idx+1][2*pos0] = one_qubit_parameter_gates_available[gate] + params_str
                            self.lines_use.append(2*pos0)
                            self.lines_use.append(2*pos0 + 1)
                            break    
                else:
                    if isinstance(gate_info[1],float):
                        theta0_str = is_multiple_of_pi(gate_info[1])
                    elif isinstance(gate_info[1],str):
                        param = self.params_value[gate_info[1]]
                        if isinstance(param,float):
                            theta0_str = is_multiple_of_pi(param)
                        elif isinstance(param,str):
                            theta0_str = param
                    #theta0_str = is_multiple_of_pi(gate_info[1])
                    pos0 = gate_info[2]
                    for idx in range(len(gates_layerd)-1,-1,-1):
                        if gates_layerd[idx][2*pos0] != '─':
                            gates_layerd[idx+1][2*pos0] = one_qubit_parameter_gates_available[gate]+'('+theta0_str+')'
                            self.lines_use.append(2*pos0)
                            self.lines_use.append(2*pos0 + 1)
                            break
                        
            elif gate in ['reset']:
                pos0 = gate_info[1]
                for idx in range(len(gates_layerd)-1,-1,-1):
                    if gates_layerd[idx][2*pos0] != '─':
                        gates_layerd[idx+1][2*pos0] = functional_gates_available[gate]
                        self.lines_use.append(2 * pos0)
                        self.lines_use.append(2 * pos0 + 1)
                        break
            elif gate in ['barrier']:
                poslst0 = gate_info[1]
                poslst = []
                for j in poslst0:
                    if j + 1 in poslst0:
                        poslst.append(2*j)
                        poslst.append(2*j+1)
                    else:
                        poslst.append(2*j)
                for idx in range(len(gates_layerd)-1,-1,-1):
                    e_ = [gates_layerd[idx][2*i] for i in poslst0]
                    if all(e == '─' for e in e_) is False:
                        for i in poslst:
                            gates_layerd[idx+1][i] = functional_gates_available[gate]
                        break
            elif gate in ['delay']:
                poslst0 = gate_info[-1]
                poslst = []
                for j in poslst0:
                    if j + 1 in poslst0:
                        poslst.append(2*j)
                    else:
                        poslst.append(2*j)
                for idx in range(len(gates_layerd)-1,-1,-1):
                    e_ = [gates_layerd[idx][2*i] for i in poslst0]
                    if all(e == '─' for e in e_) is False:
                        for i in poslst:
                            gates_layerd[idx+1][i] = functional_gates_available[gate]+f'({gate_info[1]:.1e}ns)'
                        break
            elif gate in ['measure']:
                for j in range(len(gate_info[1])):
                    pos0 = gate_info[1][j]
                    pos1 = gate_info[2][j]
                    for idx in range(len(gates_layerd)-1,-1,-1):
                        if gates_layerd[idx][2*pos0:] != gates_element[2*pos0:]:
                            gates_layerd[idx+1][2*pos0] = functional_gates_available[gate]
                            self.lines_use.append(2*pos0)
                            self.lines_use.append(2*pos0 + 1)
                            for i in range(2*pos0+1,2*self.nqubits,1):
                                gates_layerd[idx+1][i] = '│'
                            for i in range(2*self.nqubits+1, 2*self.nqubits+1+len(str(pos1))):
                                gates_layerd[idx+1][i] = str(pos1)[i-2*self.nqubits-1]
                            break
        for idx in range(len(gates_layerd)-1,-1,-1):
            if gates_layerd[idx] != gates_element:
                cut = idx + 1
                break
        return gates_layerd[:cut]
        
    def _format_gates_layerd(self) -> list:
        r"""Unify the width of each layer's gate strings

        Returns:
            list: A new list of gates element list.
        """
        gates_layerd = self._generate_gates_layerd()
        gates_layerd_format = [gates_layerd[0]]
        for lst in gates_layerd[1:]:
            max_length = max(len(item) for item in lst)
            if max_length == 1:
                gates_layerd_format.append(lst)
            else:
                if max_length % 2 == 0:
                    max_length += 1
                dif0 = max_length // 2
                for idx in range(len(lst)):
                    if len(lst[idx]) == 1:
                        if idx < 2 * self.nqubits:
                            if idx % 2 == 0:
                                lst[idx] = '─' * dif0 + lst[idx] + '─' * dif0
                            else:
                                lst[idx] = ' ' * dif0 + lst[idx] + ' ' * dif0
                        elif idx == 2 * self.nqubits:
                            lst[idx] = '═' * dif0 + lst[idx] + '═' * dif0
                        else:
                            lst[idx] = ' ' * dif0 + lst[idx] + ' ' * dif0
                    else:
                        dif1 = max_length - len(lst[idx])
                        if idx%2 == 0:
                            lst[idx] = lst[idx] + '─' * dif1
                        else:
                            lst[idx] = lst[idx] + ' ' * dif1
                gates_layerd_format.append(lst)
        return gates_layerd_format
    
    def _add_gates_to_lines(self, width: int = 4) -> list:
        r"""Add gates to lines.

        Args:
            width (int, optional): The width between gates. Defaults to 4.

        Returns:
            list: A list of lines.
        """
        gates_layerd_format = self._format_gates_layerd()
        nl = len(gates_layerd_format[0])
        lines1 = [str() for _ in range(nl)]
        for i in range(nl):
            for j in range(len(gates_layerd_format)):
                if i < 2 * self.nqubits:
                    if i % 2 == 0:
                        lines1[i] += gates_layerd_format[j][i] + '─' * width
                    else:
                        lines1[i] += gates_layerd_format[j][i] + ' ' * width
                elif i == 2 * self.nqubits:
                    lines1[i] += gates_layerd_format[j][i] + '═' * width
                elif i > 2 * self.nqubits:
                    lines1[i] += gates_layerd_format[j][i] + ' ' * width
        return lines1 
        
    def draw(self, width: int = 4) -> None:
        r"""
        Draw the quantum circuit.

        Args:
            width (int, optional): The width between gates. Defaults to 4.
        """
        lines1 = self._add_gates_to_lines(width) 
        fline = str()
        for line in lines1:
            fline += '\n'
            fline += line
            
        formatted_string = fline.replace("\n", "<br>").replace(" ", "&nbsp;")
        html_content = f'<div style="overflow-x: auto; white-space: nowrap; font-family: consolas;">{formatted_string}</div>'
        display(HTML(html_content))

    def draw_simply(self, width: int = 4) -> None:
        r"""
        Draw a simplified quantum circuit diagram.
        
        This method visualizes the quantum circuit by displaying only the qubits that have gates applied to them,
        omitting any qubits without active gates. The result is a cleaner, more concise circuit diagram.

        Args:
            width (int, optional): The width between gates. Defaults to 4.
        """
        lines1 = self._add_gates_to_lines(width)
        fline = str()
        for idx in range(2 * self.nqubits):
            if idx in self.lines_use:
                fline += '\n'
                fline += lines1[idx]
        for idx in range(2 * self.nqubits, len(lines1)):
            fline += '\n'
            fline += lines1[idx]
            
        formatted_string = fline.replace("\n", "<br>").replace(" ", "&nbsp;")
        html_content = f'<div style="overflow-x: auto; white-space: nowrap; font-family: consolas;">{formatted_string}</div>'
        display(HTML(html_content))

    def to_qiskitQC(self):
        from qiskit import QuantumCircuit as qiskitQC
        qc = qiskitQC(self.nqubits,self.ncbits)
        one_qubit_gates_in_qiskit = {
            'id':qc.id, 
            'x':qc.x, 
            'y':qc.y, 
            'z':qc.z,
            's':qc.s, 
            'sdg':qc.sdg,
            't':qc.t, 
            'tdg':qc.tdg,
            'h':qc.h, 
            'sx':qc.sx,
            'sxdg':qc.sxdg,
            }
        two_qubit_gates_in_qiskit = {
            'cx':qc.cx, 
            'cnot':qc.cx, 
            'cy':qc.cy, 
            'cz':qc.cz, 
            'swap':qc.swap, 
            'iswap':qc.iswap,
            }
        one_qubit_parameter_gates_in_qiskit = {
            'rx':qc.rx, 
            'ry':qc.ry, 
            'rz':qc.rz, 
            'p':qc.p, 
            'u':qc.u,
            'r':qc.r,
            }
        two_qubit_parameter_gates_in_qiskit = {
            'rxx':qc.rxx, 
            'ryy':qc.ryy, 
            'rzz':qc.rzz, 
            }
        functional_gates_in_qiskit = {
            'barrier':qc.barrier, 
            'measure':qc.measure, 
            'reset':qc.reset,
            'delay':qc.delay,
            }
        for gate_info in self.gates:
            gate = gate_info[0]
            if gate in one_qubit_gates_in_qiskit.keys():
                one_qubit_gates_in_qiskit[gate](*gate_info[1:])
            elif gate in two_qubit_gates_in_qiskit.keys():
                two_qubit_gates_in_qiskit[gate](*gate_info[1:])
            elif gate in one_qubit_parameter_gates_in_qiskit.keys():
                one_qubit_parameter_gates_in_qiskit[gate](*gate_info[1:])
            elif gate in two_qubit_parameter_gates_in_qiskit.keys():
                two_qubit_parameter_gates_in_qiskit[gate](*gate_info[1:])
            elif gate in functional_gates_in_qiskit.keys():
                if gate =='delay':
                    functional_gates_in_qiskit[gate](*gate_info[1:],unit='ns')
                else:
                    functional_gates_in_qiskit[gate](*gate_info[1:])
            else:
                raise(ValueError(f'the gate name is wrong! {gate}'))
        return qc

    def plot_with_qiskit(self):
        from qiskit.visualization import circuit_drawer
        qc = self.to_qiskitQC()
        return circuit_drawer(qc,output="mpl",idle_wires=False, style = {'backgroundcolor':'#EEEEEE','linecolor':'grey'})