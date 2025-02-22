from pathlib import Path
def check_dataFolder() :
    folderPath = Path("data")

    if folderPath.is_dir() :
        return
    else:
        folderPath.mkdir(parents=True, exist_ok=True) 

        for filename in ["colleges.csv", "programs.csv", "students.csv"]:
            (folderPath / filename).touch()

check_dataFolder()