import subprocess, platform

from rich.console import Console
from rich.progress import Progress, BarColumn, SpinnerColumn

from cbuild.compilers.instance import CompilerInstance

class GCCCompiler(CompilerInstance):
    def __init__(self, flags:list=[], outtypes:list=[]):
        super().__init__("MinGW", "gcc", flags, ["exe", "dll"])

    def compile(self, console:Console, defines:list, sources:list[str], includes:list[str], outdir:str) -> list[str]:
        ofiles = []
        with Progress(SpinnerColumn(), "[progress.description]{task.description}", BarColumn(), transient=True) as progress:
            for source in progress.track(sources, description="Compiling source files..."):
                sourcefile = [s for s in source.split("\\") if s.endswith(".c")][0].replace(".c", ".o")
                ofile = f"{outdir.removesuffix("\\")}\\ofiles\\{sourcefile}"
                definestr = " ".join([f"-D{define.strip()}" for define in defines])
                includestr = " ".join([f"-I{include.strip()}" for include in includes])
                command = f"{self.prefix} {definestr} {includestr} -c {source} -o {ofile}"
                try:
                    subprocess.run(command, check=True)
                    ofiles.append(ofile)
                except FileNotFoundError as e:
                    return None
                except subprocess.CalledProcessError as e:
                    return None
        return ofiles
    
    def link(self, outname: str, output: str, libraries: dict[str, str], objects: list[str], outdir: str) -> bool | Exception:
        platform_name = platform.system().lower()
        
        # Object files to link
        ofilestr = " ".join([*map(str.strip, objects)])
        libstr: str = " ".join([f"-l{lib.strip()}" for lib in libraries])
        libdirstr: str = " ".join([f"-L{libraries[lib].strip()}" for lib in libraries if libraries[lib]])

        # output is a dynamic library (dll, dylib, or so)
        if output in ["dll", "dylib", "so"]:
            if platform_name == "darwin":
                command = f"{self.prefix} -dynamiclib {ofilestr} {libstr} {libdirstr} -o {outdir}/{outname}.dylib"
            elif platform_name == "windows":
                command = f"{self.prefix} -shared {ofilestr} {libstr} {libdirstr} -o {outdir}\\{outname}.dll"
            else:
                command = f"{self.prefix} -shared {ofilestr} {libstr} {libdirstr} -o {outdir}/{outname}.so"
        # output is an executable
        else:
            command = f"{self.prefix} {ofilestr} {libstr} {libdirstr} -o {outdir}/{outname}"

        try:
            subprocess.run(command, check=True)
            return True
        except FileNotFoundError as e:
            return e
        except subprocess.CalledProcessError as e:
            return e
