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
The module contains some functions for generating random circuits or classical ansatzes.
"""
import numpy as np
import copy
from .quantumcircuit import (QuantumCircuit,
                             one_qubit_gates_available,
                             two_qubit_gates_available,
                             one_qubit_parameter_gates_available,
                             functional_gates_available,
                             )

def generate_ghz_state(nqubits: int) -> 'QuantumCircuit':
    r"""
    Produce a GHZ state on n qubits.

    Args:
        nqubits (int): The number of qubits. Must be >= 2.

    Returns:
        QuantumCircuit: A quantum circuit representing the GHZ state.
    """
    cir =  QuantumCircuit(nqubits)
    cir.h(0)
    for i in range(1,nqubits):
        cir.cx(0,i)
    return cir

def generate_random_circuit(nqubits: int, ncycle: int, seed: int = 2024, function_gates: bool = True) -> 'QuantumCircuit':
    r"""
    Generate random quantum circuits, mainly for testing.

    Args:
        nqubits (int): The number of qubits.
        ncycle (int): The number of quantum circuit layers.
        seed (int, optional): Random seed. Defaults to 2024.
        function_gates (bool, optional): Whether it contains functional gates. Defaults to True.

    Returns:
        QuantumCircuit: A random quantum circuit.
    """
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(nqubits)
    # print('ncycle: {}, nqubit: {}'.format(ncycle, nqubits))
    two_qubit_gates_available_qiskit = copy.deepcopy(two_qubit_gates_available)
    two_qubit_gates_available_qiskit.pop('iswap')
    for _ in range(ncycle):
        for qubit in range(nqubits):
            if function_gates:
                gate_type = rng.choice(['single', 'parametric', 'two','barrier','measure','reset'])
            else:
                gate_type = rng.choice(['single', 'parametric', 'two'])
            if gate_type == 'single':
                gate = rng.choice(list(one_qubit_gates_available.keys()))
                getattr(qc, gate)(qubit)
            elif gate_type == 'two' and nqubits > 1:
                gate = rng.choice(list(two_qubit_gates_available_qiskit.keys()))
                target_qubit = rng.choice([q for q in range(nqubits) if q != qubit])
                getattr(qc, gate)(qubit, target_qubit)
            elif gate_type == 'parametric':
                gate = rng.choice(list(one_qubit_parameter_gates_available.keys()))
                if gate == 'u':
                    theta = rng.uniform(-1,1)*np.pi 
                    phi = rng.uniform(-1,1)*np.pi 
                    lamda = rng.uniform(-1,1)*np.pi 
                    getattr(qc, gate)(theta,phi,lamda,qubit)
                elif gate == 'r':
                    theta = rng.uniform(-1,1)*np.pi 
                    phi = rng.uniform(-1,1)*np.pi 
                    getattr(qc, gate)(theta,phi,qubit)                    
                else:
                    theta = rng.uniform(-1,1)*np.pi  
                    getattr(qc, gate)(theta, qubit)
            elif gate_type == 'barrier':
                for idx in range(qubit+1):
                    getattr(qc, 'barrier')(idx)
            elif gate_type == 'measure':
                getattr(qc, 'measure')(qubit,qubit)
            elif gate_type == 'reset':
                getattr(qc, 'reset')(qubit)
    return qc

def quarkQC(nqubits):
    """Plot all gates supported by QuarkCircuit on a single circuit.

    Args:
        nqubits (int): The number of qubits.

    Returns:
        QuantumCircuit: A qunatum circuit.
    """
    qc = QuantumCircuit(nqubits,nqubits)
    one_qubit_gates_in_quark = {
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
    two_qubit_gates_in_quark = {
        'cx':qc.cx, 
        'cnot':qc.cx, 
        'cy':qc.cy, 
        'cz':qc.cz, 
        'swap':qc.swap, 
        'iswap':qc.iswap,
        }
    one_qubit_parameter_gates_in_quark = {
        'rx':qc.rx, 
        'ry':qc.ry, 
        'rz':qc.rz, 
        'p':qc.p, 
        'u':qc.u,
        'r':qc.r,
        }
    two_qubit_parameter_gates_in_quark = {
        'rxx':qc.rxx, 
        'ryy':qc.ryy, 
        'rzz':qc.rzz, 
        }
    functional_gates_in_quark = {
    'barrier':qc.barrier, 
        'measure':qc.measure, 
        'reset':qc.reset,
        'delay':qc.delay,
        }

    for  gate in one_qubit_gates_in_quark.keys():
        qubit = np.random.choice(range(nqubits))
        one_qubit_gates_in_quark[gate](qubit)
    qc.barrier()
    for gate in two_qubit_gates_in_quark.keys():
        qubit1,qubit2  = np.random.choice(range(nqubits),2,replace=False)
        two_qubit_gates_in_quark[gate](qubit1,qubit2)
    qc.barrier()
    for gate in one_qubit_parameter_gates_in_quark.keys():
        qubit = np.random.choice(range(nqubits))
        if gate == 'u':
            theta,phi,lamda = np.random.uniform(-1,1,3)*np.pi
            one_qubit_parameter_gates_in_quark[gate](theta,phi,lamda,qubit)
        elif gate == 'r':
            theta,phi = np.random.uniform(-1,1,2)*np.pi
            one_qubit_parameter_gates_in_quark[gate](theta,phi,qubit)
        else:
            theta = np.random.uniform(-1,1,1)[0]*np.pi
            one_qubit_parameter_gates_in_quark[gate](theta,qubit)
    qc.barrier()
    for gate in two_qubit_parameter_gates_in_quark.keys():
        qubit1,qubit2  = np.random.choice(range(nqubits),2,replace=False)
        theta = np.random.uniform(-1,1,1)[0]*np.pi
        two_qubit_parameter_gates_in_quark[gate](theta,qubit1,qubit2)
    qc.barrier()
    qc.delay(9e-9)
    qc.measure_all()
    return qc

def quarkQC_params(nqubits):
    """Plot all parameterized gates supported by QuarkCircuit on a single circuit.

    Args:
        nqubits (int): The number of qubits.

    Returns:
        QuantumCircuit: A qunatum circuit.
    """
    qc = QuantumCircuit(nqubits,nqubits)
    one_qubit_parameter_gates_in_quark = {
        'rx':qc.rx, 
        'ry':qc.ry, 
        'rz':qc.rz, 
        'p':qc.p, 
        'u':qc.u,
        'r':qc.r,
        }
    params = ['a'+str(i) for i in range(nqubits)]
    for gate in one_qubit_parameter_gates_in_quark.keys():
        qubit = np.random.choice(range(nqubits))
        if gate == 'u':
            theta,phi,lamda = np.random.choice(params,3)
            one_qubit_parameter_gates_in_quark[gate](theta,phi,lamda,qubit)
        elif gate == 'r':
            theta,phi = np.random.choice(params,2)
            one_qubit_parameter_gates_in_quark[gate](theta,phi,qubit)
        else:
            theta = np.random.choice(params)
            one_qubit_parameter_gates_in_quark[gate](theta,qubit)
    qc.barrier()
    qc.measure_all()
    return qc