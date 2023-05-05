import time
import smartsim
import logging
import typing as t
from deco import traced


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.info(f"smartsim version: {smartsim.__version__}")


@traced
def run_experiment(i: int):
    save_to = "/Users/chris.mcbride/code/ssdemo/output"

    exp = smartsim.Experiment("demo experiment", exp_path=save_to, launcher="local")
    db = exp.create_database(interface="lo0")

    hello_rs = exp.create_run_settings("echo", "Hello, Chris!")
    hello_model = exp.create_model("hello-model", hello_rs)

    goodbye_rs = exp.create_run_settings("echo", "Goodby, Chris!")
    goodbye_model = exp.create_model("goodbye-model", goodbye_rs)

    experiment_entities = [
        db,
        hello_model,
        goodbye_model,
    ]

    exp.start(*experiment_entities, summary=False)
    time.sleep(5)
    exp.stop(db)


if __name__ == "__main__":
    run_experiment(123)
