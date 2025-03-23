import subprocess


subprocess.run(["python3", "load_model.py"], check=True)
subprocess.run(["python3", "query_response.py"], check=True)
