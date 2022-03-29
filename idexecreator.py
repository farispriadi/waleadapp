import argparse
from config import ABOUT
import datetime
import docker
import os
import pathlib
import subprocess

parser = argparse.ArgumentParser(description='IdExeCreator Help')
parser.add_argument('--project', action='store', type=str, default="",
                    help="project path, fill it if current directory is not project folder (using absolute path)")
parser.add_argument('--platform', action='store', type=str, default="windows",
                    help="platform , option 'windows' by default or 'linux'")
parser.add_argument('--iss', action='store', type=str, default="innosetup.iss",
                    help="Inno setup script (use relative path)")
parser.add_argument('--spec', action='store', type=str, default="pyinstaller.spec",
                    help="PyInstaller Specification (use relative path)")

args = parser.parse_args()


if __name__ == "__main__":
    out =""
    checking = True
    if str(args.project) != "":
        project = str(args.project)
        workdir = subprocess.run(["cd", project], capture_output=True, text=True)
        out = "change dir to {}".format(project)
        print(out)
    source_dir = str(os.getcwd())
    project = str(os.getcwd()).split()[-1]

    # check requirements
    if not any(filename =="requirements.txt" for filename in os.listdir(".")):
        print("No requirements file")
        checking =False
    else:
        print("requirements file : OK")

    # check spec file
    if not any(filename.endswith(".spec") for filename in os.listdir(".")):
        print("No .spec pyinstaller file")
        checking =False
        spec_file = ""
    else:
        print("spec file file : OK")
        spec_file = str(args.spec)

    if args.platform not in ["windows", "linux"]:
        print("choose between windows and linux")
        checking =False
    
    platform = args.platform
    output_dir = source_dir+"/dist/{}/{}/Output".format(platform,project)

    # check iss file
    iss_file = args.iss
    iss_path = pathlib.Path(source_dir+"/"+iss_file)
    if iss_path.exists():
        print("iss file OK")
    else:
        print("iss file not exist")
        checking = False


    if checking:
        client_docker = docker.from_env()
        out = out +"\n\n\n# PyInstaller\n"
        print("this", out)
        # run pyiinstaller docker in root project 
        # pyinstaller = subprocess.run(["docker", "run", "-v", "'$(pwd):/src/'", "cdrx/pyinstaller-windows"], shell=True,capture_output=True, text=True)
        # out = out+pyinstaller.stdout.strip()
        client_docker.containers.run("cdrx/pyinstaller-windows","{}".format(spec_file),volumes=["{}:/src/".format(source_dir)])


        #copy iss file
        iss_file_setup = subprocess.run(["cp", "{}/{}".format(source_dir,iss_file), "${}/dist/{}/{}/".format(source_dir,platform,project)],shell=True, capture_output=True, text=True)
        print("cwd ", os.getcwd())

        # run innosetup docker in root project
        # innosetup = subprocess.run(["docker", "run", "--rm -i -v", "'$(pwd)/dist/{}:/work/'".format(platform)," amake/innosetup {}".format(iss_file)],shell=True, capture_output=True, text=True)
        # out = out +"\n\n\n# Inno Setup\n" 
        # out= out+innosetup.stdout.strip()
        client_docker.containers.run("amake/innosetup", "{}".format(iss_file),auto_remove=True, volumes=["{}/dist/{}:/work/".format(source_dir,platform)])

        with open('log.txt','w') as f:
            f.write("Log Building Python to Exe Setup using Docker, PyInstaller and Inno Setup\n")
            f.write("Date : {} \n".format(str(datetime.datetime.now())))
            f.write("Name : {} \n".format(ABOUT['app_name']))
            f.write("Version : {} \n".format(ABOUT['version']))
            f.write("Author : {} \n".format(ABOUT['author']))
            f.write("#######################################\n")
            f.write(out)

        print("check output folder in {}".format(output_dir))
