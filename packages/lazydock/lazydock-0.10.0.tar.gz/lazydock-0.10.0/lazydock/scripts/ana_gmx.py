import argparse
import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

from mbapy_lite.base import put_err, put_log
from mbapy_lite.file import get_paths_with_extension, opts_file
from pymol import cmd
from tqdm import tqdm

from lazydock.gmx.run import Gromacs
from lazydock.scripts._script_utils_ import Command, clean_path
from lazydock.utils import uuid4


class simple(Command):
    HELP = """
    simple analysis for GROMACS simulation
    0. gmx_mpi trjconv -s md.tpr -f md.xtc -o md_center.xtc -pbc mol -center
    
    1. gmx_mpi rms -s md.tpr -f md_center.xtc -o rmsd.xvg -tu ns 
    2. gmx_mpi rmsf -s md.tpr -f md_center.xtc -o rmsf.xvg
    3. gmx_mpi gyrate -s md.tpr -f md_center.xtc -o gyrate.xvg
    4. gmx_mpi hbond -s md.tpr -f md_center.xtc -num -dt 10
    
    5. gmx_mpi sasa -s md.tpr -f md_center.xtc -o sasa_total.xvg -or sasa_res.xvg -tu ns 
    6. gmx_mpi covar -s md.tpr -f md_center.xtc -o eigenval.xvg -tu ns 
    """
    def __init__(self, args, printf=print):
        super().__init__(args, printf)
        
    @staticmethod
    def make_args(args: argparse.ArgumentParser):
        args.add_argument('-d', '--dir', type=str,
                          help='directory to store the prepared files')
        args.add_argument('-n', '--main-name', type = str,
                          help='main name in each sub-directory, such as md.tpr.')           
        return args
        
    @staticmethod
    def trjconv(gmx: Gromacs, main_name: str, center_group: str = '1', **kwargs):
        gmx.run_command_with_expect('trjconv', s=f'{main_name}.tpr', f=f'{main_name}.xtc', o=f'{main_name}_center.xtc', pbc='mol', center=True,
                                    expect_actions=[{'Select a group:': f'{center_group}\r'}, {'Select a group:': '0\r'}], **kwargs)
        
    @staticmethod
    def rms(gmx: Gromacs, main_name: str, group: str = '4', **kwargs):
        gmx.run_command_with_expect('rms', s=f'{main_name}.tpr', f=f'{main_name}_center.xtc', o=f'rmsd.xvg', tu='ns',
                                    expect_actions=[{'Select a group:': f'{group}\r'}, {'Select a group:': f'{group}\r'}], **kwargs)
        os.system(f'cd "{gmx.working_dir}" && dit xvg_show -f rmsd.xvg -o rmsd.png -smv')
        
    @staticmethod
    def rmsf(gmx: Gromacs, main_name: str, group: str = '4', res: bool = True, **kwargs):
        gmx.run_command_with_expect('rmsf', s=f'{main_name}.tpr', f=f'{main_name}_center.xtc', o=f'rmsf.xvg', res=res,
                                    expect_actions=[{'Select a group:': f'{group}\r'}], **kwargs)
        os.system(f'cd "{gmx.working_dir}" && dit xvg_show -f rmsf.xvg -o rmsf.png -smv')
        
    @staticmethod
    def gyrate(gmx: Gromacs, main_name: str, group: str = '4', **kwargs):
        gmx.run_command_with_expect('gyrate', s=f'{main_name}.tpr', f=f'{main_name}_center.xtc', o=f'gyrate.xvg',
                                    expect_actions=[{'Select a group:': f'{group}\r'}], **kwargs)
        os.system(f'cd "{gmx.working_dir}" && dit xvg_show -f gyrate.xvg -o gyrate.png -smv')
        
    @staticmethod
    def hbond(gmx: Gromacs, main_name: str, group: str = '1', dt=10, **kwargs):
        gmx.run_command_with_expect('hbond', s=f'{main_name}.tpr', f=f'{main_name}_center.xtc',
                                    num=f'{main_name}_hbond_num.xvg', dist=f'{main_name}_hbond_dist.xvg',
                                    expect_actions=[{'Select a group:': f'{group}\r'}, {'Select a group:': f'{group}\r'}], **kwargs)
        for ty in ['num', 'dist']:
            os.system(f'cd "{gmx.working_dir}" && dit xvg_show -f {main_name}_hbond_{ty}.xvg -o hbond_{ty}.png -smv')
        
    @staticmethod
    def sasa(gmx: Gromacs, main_name: str, group: str = '1', **kwargs):
        gmx.run_command_with_expect('sasa or sasa_res.xvg', s=f'{main_name}.tpr', f=f'{main_name}_center.xtc',
                                    o=f'sasa_total.xvg', odg=f'sasa_dg.xvg', tv='sasa_tv.xvg', tu='ns',
                                    expect_actions=[{'Select a group:': f'{group}\r'}], **kwargs)
        for ty in ['total', 'res', 'dg', 'tv']:
            os.system(f'cd "{gmx.working_dir}" && dit xvg_show -f sasa_{ty}.xvg -o sasa_{ty}.png -smv')
        
    @staticmethod
    def covar(gmx: Gromacs, main_name: str, xmax: str = 10, **kwargs):
        gmx.run_command_with_expect('covar', s=f'{main_name}.tpr', f=f'{main_name}_center.xtc', o=f'eigenval.xvg', tu='ns',
                                    expect_actions=[{'Select a group:': '1\r'}], **kwargs)
        os.system(f'cd "{gmx.working_dir}" && dit xvg_show -f eigenval.xvg -o eigenval.png -xmin 0 -xmax {xmax}')
        
    def main_process(self):
        # get complex paths
        if os.path.isdir(self.args.dir):
            complexs_path = get_paths_with_extension(self.args.dir, [], name_substr=self.args.main_name)
        else:
            put_err(f'dir argument should be a directory: {self.args.dir}, exit.', _exit=True)
        put_log(f'get {len(complexs_path)} task(s)')
        # process each complex
        for complex_path in tqdm(complexs_path, total=len(complexs_path)):
            complex_path = Path(complex_path).resolve()
            gmx = Gromacs(working_dir=str(complex_path.parent))
            # perform trjconv
            self.trjconv(gmx, main_name=complex_path.stem, center_group='1')
            # perform analysis
            self.rms(gmx, main_name=complex_path.stem, group='4')
            self.rmsf(gmx, main_name=complex_path.stem, group='4')
            self.gyrate(gmx, main_name=complex_path.stem, group='4')
            self.hbond(gmx, main_name=complex_path.stem, group='1')
            self.sasa(gmx, main_name=complex_path.stem, group='1')
            self.covar(gmx, main_name=complex_path.stem, xmax=10)


_str2func = {
    'simple': simple,
}


def main(sys_args: List[str] = None):
    args_paser = argparse.ArgumentParser(description = 'tools for GROMACS analysis.')
    subparsers = args_paser.add_subparsers(title='subcommands', dest='sub_command')

    simple_args = simple.make_args(subparsers.add_parser('simple', description=simple.HELP))

    args = args_paser.parse_args(sys_args)
    if args.sub_command in _str2func:
        _str2func[args.sub_command](args).excute()


if __name__ == '__main__':
    main()