from pathlib import Path
import json

class DataBase:
    def __init__(self,store_path:Path) -> None:
        if store_path.exists() and not store_path.is_dir():
            raise ValueError('provide a directory')
        if not store_path.exists():
            store_path.mkdir()
        self.store_path: Path = store_path


    def create(self,file_name:str,content:str) -> bool:
        if self.find_by_pattern(file_name):
            return False
        
        with open(self.store_path / file_name ,'w') as f:
            _ = f.write(content)
    
        return True

    def delete(self,file_name:str) -> bool:
        file = self.find_by_pattern(file_name)
        if not file :
            return False
        file[0].unlink()
        return True

    def read(self,file_name:str):
        file = self.find_by_pattern(file_name)
        if not file:
            return
        with open(file[0],'r') as f:
            data = f.read()
        return data

    def find_by_pattern(self,pattern:str) -> list[Path]:
        return list(self.store_path.glob(pattern))

    def exist(self,file_name:str) -> bool:
        return True if self.find_by_pattern(file_name) else False


