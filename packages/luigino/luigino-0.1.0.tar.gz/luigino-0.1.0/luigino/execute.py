import os
import shutil
from celery import states
from celery.exceptions import Ignore
from .common_task import CommonLuigiTask
import luigi
import json

def execute_task(celery_app, task_class: CommonLuigiTask, jsonstr_config: str):
    """Execute a luigi task and handle the success and error cases."""
    try:
        config = json.loads(jsonstr_config)
        task_instance = task_class(config=config)
        success = luigi.build([task_instance], local_scheduler=True)

        if not success:
            errlog_path = os.path.join(config.get('output_dir'), 'error.log')
            with open(errlog_path, 'r') as f:
                errlog = f.read()
            raise ValueError(errlog)

        message = "task completed"
        with task_instance.output().open('r') as f:
            data = json.load(f).get(task_instance.result_key(), {}) if success else {}

        return {
            "success": success,
            "detail": message,
            "data": data
        }

    except Exception as e:
        celery_app.update_state(state=states.FAILURE, meta={
            "exc_type": type(e).__name__,
            "exc_message": str(e)
        })
        raise Ignore()

    finally:
        if os.getenv('PRESERVE_OUTPUT', 'False').lower() != 'true':
            shutil.rmtree(config.get('output_dir'))
