import subprocess

from _constants import TEMP_DIR


def create_envpack(env_name: str, packages: list[str], python: str) -> tuple[int, str, str]:
    python_base = python
    save_path = f"{TEMP_DIR}/{env_name}.tar.gz"
    command = ". /opt/conda/etc/profile.d/conda.sh; "
    command += f"conda create -n {env_name} --clone {python_base}; "
    if packages:
        packages = ' '.join(packages)
        command += f"conda activate {env_name}; "
        command += f"pip install {packages}; "
        command += f"conda deactivate; "
    command += f"conda pack -n {env_name} -o {save_path}; "
    command += f"conda env remove -n {env_name}"
    try:
        result = subprocess.run(command, shell=True, check=True)
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


