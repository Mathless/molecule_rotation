# Thisfile_path=Noneython script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Graph:
    def __int__(self):
        self.graph = {}
        self.coords = {}

def parse_molecule_json(file_path: str) -> Graph:
    """Returns a Graph class representing the graph
    :param file_path: abs or rel path to file
    """




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    molecule_file_name = "Conformer3D_CID_2244.json"
    parse_molecule_json("./molecules"+molecule_file_name)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
