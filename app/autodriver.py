import jinja2
import typing as t
from uuid import uuid4
import black


def load_autodriver_tpl() -> str:
    with open("./tpl/base.py") as tpl:
        return tpl.read()

def render_autodriver(exp_model: t.Dict[str, t.Union[str, int, bool, dict]]):
    env = jinja2.Environment(loader=jinja2.PackageLoader("autodriver"), autoescape=True)

    model_name = exp_model.get("name", str(uuid4()))
    tpl = env.get_template("driver.py")

    result = tpl.render(exp_model)

    with open(f"../output/simple_{model_name}.py", "w") as out_fp:
        result = black.format_str(result, mode=black.Mode())
        out_fp.write(result)    


if __name__ == "__main__":
    nodb_ctx: t.Dict[str, t.Union[str, int, bool]] = {
        "name": "no_db",
        "has_db": False
    }
    render_autodriver(nodb_ctx)

    db_ctx: t.Dict[str, t.Union[str, int, bool]] = {
        "name": "with_db",
        "has_db": True
    }
    render_autodriver(db_ctx)

    db_ctx: t.Dict = {
        "name": "multi_app",
        "has_db": True,
        "has_apps": True,
        "applications": [
            {
                "name": "hello-model",
                "rs": {
                    "exe": "echo",
                    "arg": "Hello, there"
                }
            },
            {
                "name": "bye-model",
                "rs": {
                    "exe": "echo",
                    "arg": "See you soon"
                }
            }
        ]
    }
    render_autodriver(db_ctx)
