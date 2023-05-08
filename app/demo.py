import typing as t
import autodriver as autod


def demo_no_db():
        ctx: t.Dict[str, t.Union[str, int, bool]] = {
            "name": "no_db",
            "has_db": False
        }
        autod.render_autodriver(ctx)


def demo_has_db():
    ctx: t.Dict[str, t.Union[str, int, bool]] = {
        "name": "with_db",
        "has_db": True
    }
    autod.render_autodriver(ctx)


def demo_multiple_apps():
    ctx: t.Dict = {
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
    autod.render_autodriver(ctx)


if __name__ == "__main__":
    demo_no_db()
    demo_has_db()
    demo_multiple_apps()
