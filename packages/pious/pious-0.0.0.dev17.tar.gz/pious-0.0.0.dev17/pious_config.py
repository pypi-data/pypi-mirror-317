from pious.conf import pious_conf
from os import path as osp

install_dir = pious_conf.pio_install_directory
print(f"PioSOLVER Install Directory: `{install_dir}` EXISTS? {osp.exists(install_dir)}")
print(f"PioSOLVER Version          : {pious_conf.pio_version_no}")
print(f"PioSOLVER Version Type     : {pious_conf.pio_version_type}")
print(f"PioSOLVER Version Suffix   : {pious_conf.pio_version_suffix}")
pio_exec = osp.join(install_dir, pious_conf.get_pio_solver_name()) + ".exe"
print(f"PioSOLVER Executable       : {pio_exec}   EXISTS? {osp.exists(pio_exec)}")
pio_viewer = osp.join(install_dir, pious_conf.get_pio_viewer_name()) + ".exe"
print(f"PioVIEWER                  : {pio_viewer}   EXISTS? {osp.exists(pio_viewer)}")
