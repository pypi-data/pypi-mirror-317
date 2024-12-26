#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 15:53
# @Author  : 兵
# @email    : 1747193328@qq.com
import os
import subprocess

import numpy as np
from ase.calculators.vasp import Vasp
from ase.io import read as ase_read
from ase.io import write as ase_write
from NepTrain import Config
def write_to_xyz(vaspxml_path, save_path, Config_type, append=True):

    atoms_list = []
    atoms = ase_read(vaspxml_path, index=":")
    index = 1
    for atom in atoms:
        xx, yy, zz, yz, xz, xy = -atom.calc.results['stress'] * atom.get_volume()  # *160.21766
        atom.info['virial'] = np.array([(xx, xy, xz), (xy, yy, yz), (xz, yz, zz)])

        atom.calc.results['energy'] = atom.calc.results['free_energy']

        atom.info['Config_type'] = Config_type + str(index)
        atom.info['Weight'] = 1.0
        del atom.calc.results['stress']
        del atom.calc.results['free_energy']
        atoms_list.append(atom)
        index += 1

    ase_write(save_path, atoms_list, format='extxyz', append=append)
    return atoms_list
class VaspInput(Vasp):


    def __init__(self,*args,**kwargs):

        super(VaspInput,self).__init__(*args,**kwargs)
        self.input_params["setups"] = {"base": "recommended"}
        self.input_params["pp"] = ''

        os.environ[self.VASP_PP_PATH] = os.path.expanduser(Config.get("environ", "potcar_path"))


        # self.converged
    def _run(self, command=None, out=None, directory=None):
        """Method to explicitly execute VASP"""
        if command is None:
            command = self.command
        if directory is None:
            directory = self.directory

        errorcode = subprocess.call(command,
                                    shell=True,
                                    stdout=out,
                                    stderr=out,
                                    cwd=directory)

        return errorcode
if __name__ == '__main__':
    vasp=VaspInput()




    atoms=ase_read("./POSCAR",format='vasp')
    vasp.read_incar("./INCAR")
    vasp.calculate(atoms,('energy'))
    print(vasp.results)
    print(vasp.atoms.info)
    print(atoms.calc.results)