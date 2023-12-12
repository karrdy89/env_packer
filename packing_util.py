import subprocess
from typing import Optional

from _constants import TEMP_DIR


def create_envpack(env_name: str, packages: list[str], python_version: Optional[str] = "3.11") -> tuple[int, str, str]:
    python_base = "python" + python_version
    packages = ' '.join(packages)
    save_path = f"{TEMP_DIR}/{env_name}.tar.gz"
    try:
        subprocess.run(f"conda create -n {env_name} --clone {python_base};"
                       f"conda activate {env_name};"
                       f"pip install {packages};"
                       f"conda deactivate;"
                       f"conda pack -n {env_name} -o {save_path};"
                       f"conda env remove -n {env_name}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        subprocess.run(f"conda deactivate", shell=True, check=False)
        subprocess.run(f"conda env remove -n {env_name}", shell=True, check=False)
        return -1, e.__str__(), save_path
    except Exception as e:
        subprocess.run(f"conda deactivate", shell=True, check=False)
        subprocess.run(f"conda env remove -n {env_name}", shell=True, check=False)
        return -2, e.__str__(), save_path
    else:
        return 0, '', save_path


