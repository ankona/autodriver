{# templates/simple.py #}

import time
import smartsim
import logging
import typing as t


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.info(f"smartsim version: {smartsim.__version__}")


class ExperimentContext:
    def __init__(self, experiment, entities, path):
        self.experiment = experiment
        self.entities = entities
        self.path = path
        self.databases = []

        for entity in self.entities:
            if isinstance(entity, smartsim.experiment.Orchestrator):
                self.databases.append(entity)


def traced(func: t.Callable):
    def _inner(*args, **kwargs):
        logger.debug(f"start:{func.__name__}")
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as ex:
            logger.exception("trace_logger caught exception in callable")
            raise
        finally:
            logger.debug(f"finish:{func.__name__}")
        return result
    
    return _inner


@traced
def build_experiment(save_to: str) -> ExperimentContext:
    exp = smartsim.Experiment("demo experiment", exp_path=save_to, launcher="local")
    
    {% if has_db %}
    db = exp.create_database(interface="lo0")
    {% endif %}

    applications = []
    {% for app in applications %}
    app_run_settings = exp.create_run_settings("{{app.rs.exe}}", "{{app.rs.arg}}")
    app = exp.create_model("{{app.name}}", app_run_settings)
    applications.append(app)
    {% endfor %}

    experiment_entities = []

    {% if has_db %}
    experiment_entities.append(db)
    {% endif %}

    {% if has_apps %}
    experiment_entities.extend(applications)
    {% endif %}

    return ExperimentContext(experiment=exp, entities=experiment_entities, path=save_to)


@traced
def run_experiment(ctx: ExperimentContext):
    exp = ctx.experiment

    exp.start(*ctx.entities, summary=False)
    
    to_stop = []

    {% if has_db %}
    to_stop.extend(ctx.databases)
    {% endif %}
    
    if to_stop:
        exp.stop(*to_stop)
    

if __name__ == "__main__":
    save_to = "/Users/chris.mcbride/code/ssdemo/output"

    ctx = build_experiment(save_to)
    run_experiment(ctx)
