from fairchem.core.common.relaxation.ase_utils import OCPCalculator
from fairchem.core.models.model_registry import model_name_to_local_file
from ase.optimize import FIRE
from ase.io import read, write
from ase.constraints import FixAtoms
import ase
import numpy as np
import fairchem
import torch
import os

from fairchem.applications.cattsunami.core.autoframe import interpolate
from fairchem.applications.cattsunami.core import OCPNEB
# patch ocp to prevent using multiprocessing



def read_atoms(
    path: str
    ) -> ase.Atoms:
    '''
    ==========================================================================
    Read ase files (POSCAR, CONTCAR, *.extxyz, *.traj) via path
    Input: name of path (str)
    Output: ase.Atoms
    ==========================================================================
    '''
    adslab = read(path)

    return adslab


def setup_tags(
        atoms: ase.Atoms
    ) -> None:
    '''
    ==========================================================================
    Modified from ggu's tagging algorithm.

    Input: ase.Atoms
    Output: np.ndarray, tags about each atom with fair-chem's tagging rule
    
    Tagging rule:
    Adsorbate=2, top layer of adsorbent=1, adsorbent beneath the top layer=0
    ==========================================================================
    '''
    tags = np.ones(len(atoms))*2
    zpos = atoms.positions[:,2]
    I = np.argsort(zpos)[::-1]
    I_metal = I[atoms.numbers[I]>15]
    tags[I_metal] = 0
    surf_I = I_metal[:int(len(I_metal)/4)]
    tags[surf_I] = 1
    atoms.set_tags(tags)
    BottomHalf_surf_I = I_metal[-int(len(I_metal)/2):]
    atoms.set_constraint(FixAtoms(BottomHalf_surf_I))


def load_calculator(
    path: str,
    ) -> fairchem.core.common.relaxation.ase_utils.OCPCalculator:
    '''
    ==========================================================================
    Load OCP calculator
    Input: path
    Output: OCPCalculator
    ==========================================================================
    '''
    device = not torch.cuda.is_available()
    calc = OCPCalculator(checkpoint_path=path, 
                         cpu=device) # If you want to use gpu, then cpu=False

    return calc
   

def run_relaxation(
    adslab: ase.Atoms,
    calc: fairchem.core.common.relaxation.ase_utils.OCPCalculator,
    trajectory_path: str,
    ) -> None:
    '''
    ==========================================================================
    Run relaxtion of atoms with OCP calculator
    Save file as MLPCAR.traj
    Input: path
    Output: OCPCalculator
    ==========================================================================
    '''
    adslab.calc = calc
    opt = FIRE(adslab, trajectory=trajectory_path)
    opt.run(fmax=0.05, steps=100)


class ocp_helper:
    patch_done = False
    @classmethod
    def run_relaxation(cls,input_path,trajectory_path='relax.traj', output_path='relax_out.xsd'):
        adslab = read_atoms(path=input_path)
        setup_tags(adslab)
        checkpoint_path = model_name_to_local_file('EquiformerV2-31M-S2EF-OC20-All+MD', local_cache='./')
        calc = load_calculator(path=checkpoint_path)
        run_relaxation(adslab, calc, trajectory_path)
        write(output_path,read(trajectory_path))
        
    
    @classmethod
    def run_neb(cls,IS_path,FS_path,NIMAGES,trajectory_path='neb.traj',out_path='neb_out.xtd'):
        path = os.path.join(fairchem.__path__._path[0],'applications/cattsunami/core/ocpneb.py')
        with open(path) as f:
            s = f.read()
        if 'num_workers=2' in s:
            s = s[:s.index('num_workers=2')+12]+'0'+s[s.index('num_workers=2')+13:]
            with open(path,'w') as f:
                f.write(s)
            cls.patch_done = True
        if cls.patch_done == True:
            raise ValueError("OCPNEB has been patched. Please restart the python and rerun.")
        
        IS = read(IS_path)
        FS = read(FS_path)
        
        # change PBC
        pbc = np.array([[0,0,0], [-1, -1, -1], [-1, -1, 0], [-1, -1, 1], [-1, 0, -1],
               [-1, 0, 1], [-1, 1, -1], [-1, 1, 0], [-1, 1, 1], [0, -1, -1], [0, -1, 0],
               [0, -1, 1], [0, 0, -1], [0, 0, 1], [0, 1, -1], [0, 1, 0], [0, 1, 1],
               [1, -1, -1], [1, -1, 0], [1, -1, 1], [1, 0, -1], [1, 0, 0], [1, 0, 1],
               [1, 1, -1], [1, 1, 0],[1, 1, 1],[-1, 0, 0]])
        
        pos1c = IS.get_positions()
        pos2s = FS.get_scaled_positions()
        pos2s = pos2s[None,:,:]+pbc[:,None,:]
        pos2c = np.dot(pos2s,FS.cell)
        pbcdists = np.linalg.norm(pos1c[None,:,:]-pos2c,axis=2)
        mindisti = np.argmin(pbcdists,axis=0)
        pos2cmin = []
        for i,j in enumerate(mindisti):
            pos2cmin.append(pos2c[j,i,:])
        pos2cmin = np.array(pos2cmin)
        FS.set_positions(pos2cmin)
        
        setup_tags(IS)
        setup_tags(FS)
        
        frame_set = interpolate(IS,FS,NIMAGES)
        
        
        ### Settings
        fmax = 0.05 # [eV / ang]
        delta_fmax_climb = 0.4 # this means that when the fmax is below 0.45 eV/Ang climbing image will be turned on
        #cpu = False # set to False if you have a GPU
        cpu = not torch.cuda.is_available()
        
        
        # NOTE: Change the checkpoint path to locally downloaded files as needed
        checkpoint_path = model_name_to_local_file('EquiformerV2-31M-S2EF-OC20-All+MD', local_cache='./')
        
        
        neb = OCPNEB(
                frame_set,
                checkpoint_path=checkpoint_path,
                k=1,
                batch_size=8, # If you get a memory error, try reducing this to 4
                cpu = cpu,
                )
        
        optimizer = FIRE(
                    neb,
                    trajectory=trajectory_path,
                    )
        
        neb.climb = True
        conv = optimizer.run(fmax=fmax+delta_fmax_climb, steps=600)
        if conv:
           neb.climb = True
           conv = optimizer.run(fmax=fmax, steps=300)
        
        nframes = len(frame_set)
        optimized_neb = read(trajectory_path, ":")[-1*nframes:]
        optimized_neb[0] =read(IS_path)
        optimized_neb[-1] = read(FS_path)
        #s = f"{'img':3s} {'Energy [eV]':>18s}   {'Max Force [eV/ang]':>18s}\n"
        s = f"{'img':3s} {'Energy [eV]':>18s}\n"
        for i, atoms in enumerate(optimized_neb):
            eng = atoms.get_potential_energy()
            #maxforce = np.max(np.linalg.norm(atoms.get_forces(),axis=1))
            #s += f"{i:3d} {eng:+18.6f}   {maxforce:18.6f}\n"
            s += f"{i:3d} {eng:+18.6f}\n"
        print(s)
        write(out_path,optimized_neb)
        



