import os
import json
from pathlib import Path

class FilesFinder:
    def __init__(self, path):
        self.path = Path(path)
    def by_extension(self, extension, recursive: bool = False, fullpath: bool = True):
        """
        if recursive is true , searches folders and subfolders
        """
        file_list = []
        """
        recursive is a WIP
        """
        if recursive == True:
            for roots, dirs, files in os.walk(self.path):
                # print (roots, dirs, files)
                for file in files:
                    if file.endswith(extension):
                        if not fullpath:
                            file_list.append(files)
            return file_list
        else:
            for file in os.listdir(self.path):
                if file.endswith(extension):
                    if not fullpath:
                        file_list.append(file)
                    else:
                        file_list.append(os.path.join(self.path, file))
            return file_list
 
class FilesLoader:
    def __init__(self, path):
        self.file_array = FilesFinder(path).by_extension((".jpeg",".png", ".jpg"))
        self.file_index = 0
    def increment_index(self):
        self.file_index += 1
        return self.file_array[self.file_index]
    def decrement_index(self):
        self.file_index -= 1
        return self.file_array[self.file_index]
    
class LabelsLoader:
    def __init__(self, jsonfile):
        self.json_file = json.load(open(jsonfile))
    
    def get_labels(self):
        shape = self.json_file["shapes"] 
        # print(self.json_file['imageWidth'], self.json_file['imageHeight'])
        labels = [x['label'] for x in shape]
        return labels

    def get_coords(self):
        shape = self.json_file["shapes"]
        labels = [x['label'] for x in shape]
        pts = [x['points'] for x in shape] 
        return pts, labels 