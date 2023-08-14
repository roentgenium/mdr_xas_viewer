import pathlib, shutil, json

from util import load_9809_format

class XasDatum():
    def __init__(self, fname):
        self.metadata = None
        self.rawdata = None
        self.filepath = fname
        self.energy = []
        self.mu = []
        self.from_file(fname)
        try:
            self.name = self.metadata["sample"][0]["chemical_formula"]
        except KeyError:
            self.name = "Unknown"

    def guess_file_format(self, fname):
        try:
            with open(fname, encoding="utf-8") as f:
                try:
                    if "9809" in f.readline():
                        return "9809"
                    else:
                        return "unknown"
                except UnicodeDecodeError:
                    print(f"Fail to load {fname}")
        except IOError:
            print(f"Fail to load {fname}")

    def from_file(self, fname):
        # Unzip a zip file
        dir_name = pathlib.Path(fname).stem
        shutil.unpack_archive(fname, dir_name)

        # Load metadata
        fname2 = pathlib.Path(dir_name + "/" + "metadata.all.json" )
        with open(fname2, encoding = 'utf-8') as f:
            self.metadata = json.load(f)

        # Find rawdata files
        self.rawdata = self.metadata["local"]["xafs_filename_list"]
        fname3 = self.rawdata[0].replace("(", "_").replace(")", "_")

        # Guess file format
        type = self.guess_file_format(dir_name + "/" + fname3)
        if type == "9809":
            load_9809_format(self, dir_name + "/" + fname3)

    def toList(self) -> list:
        return [self.name, self]
    
    @classmethod    
    def toHeaderList(cls) -> list[str]:
        return ["Name", "Data"]