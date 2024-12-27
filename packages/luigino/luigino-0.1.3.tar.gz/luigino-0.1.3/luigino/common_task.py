import luigi
import os
import json

class CommonLuigiTask(luigi.Task):
    """
    Ex:
    config = {
        "output_dir": "output/ababab"
    }
    luigi.build([ShelveSetTask(config = config)], 
                local_scheduler=True)

    """
    def result_key(self) -> str:
        return f"{self.__class__.__name__.lower()}"

    def output(self):
        """ 별도로 정의하지 않으면  클래스이름(소문자).json 이 결과 파일이 된다. 
        """
        file_path = os.path.join(self.output_dir(), self.result_key() + ".json")
        return luigi.LocalTarget(file_path)

    def work_file_path(self, file_name):
        file_path = os.path.join(self.config.get('output_dir'), file_name)
        return luigi.LocalTarget(file_path).path

    def write_output(self, all_info):
        with self.output().open('w') as f:
            json.dump(all_info, f, indent=4)

    def get_output_from_path(self, file_name: str) -> dict | list | None :
        path = self.work_file_path(file_name)
        with open(path,'r') as f:
            pv = json.load(f)
        return pv

    def get_previous_output(self) -> dict | list | None:
        with self.input().open('r') as f:
            pv = json.load(f)
        return pv
    
    def output_dir(self):
        return self.config.get('output_dir','')

