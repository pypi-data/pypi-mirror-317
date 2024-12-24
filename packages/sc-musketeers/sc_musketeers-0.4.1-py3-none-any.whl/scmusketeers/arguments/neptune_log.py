import neptune
from neptune.utils import stringify_unsupported


def start_neptune_log(workflow):
    print(f"Use Neptune.ai log : {workflow.run_file.log_neptune}")
    if workflow.run_file.log_neptune:
        print(f"Use Neptune project name = {workflow.run_file.neptune_name}")
        if workflow.run_file.neptune_name == "benchmark":
            workflow.run = neptune.init_run(
                project="becavin-lab/benchmark",
                api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJiMmRkMWRjNS03ZGUwLTQ1MzQtYTViOS0yNTQ3MThlY2Q5NzUifQ==",
            )
        elif workflow.run_file.neptune_name == "sc-musketeers":
            workflow.run_neptune = neptune.init_run(
                project="becavin-lab/sc-musketeers",
                api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI1Zjg5NGJkNC00ZmRkLTQ2NjctODhmYy0zZDAzYzM5ZTgxOTAifQ==",
            )
        else:
            print("No neptune_name was provided !!!")

        workflow.run_neptune["parameters/model"] = "scMusketeers"
        for par, val in workflow.run_file.__dict__.items():
            if par in dir(workflow):
                workflow.run_neptune[f"parameters/{par}"] = (
                    stringify_unsupported(getattr(workflow, par))
                )
            # elif par in dir(workflow.ae_param):
            #    workflow.run_neptune[f"parameters/{par}"] = stringify_unsupported(getattr(workflow.ae_param, par))
        if (
            workflow.hp_params
        ):  # Overwrites the defaults arguments contained in the runfile
            for par, val in workflow.hp_params.items():
                workflow.run_neptune[f"parameters/{par}"] = (
                    stringify_unsupported(val)
                )


def add_custom_log(workflow, name, value):
    workflow.run_neptune[f"parameters/{name}"] = stringify_unsupported(value)


def stop_neptune_log(workflow):
    if workflow.run_file.log_neptune:
        workflow.run_neptune.stop()
