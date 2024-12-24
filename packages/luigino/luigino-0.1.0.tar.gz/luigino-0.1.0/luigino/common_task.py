import luigi
import os
import json

class CommonLuigiTask(luigi.Task):
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
        return self.config.get('output_dir')

