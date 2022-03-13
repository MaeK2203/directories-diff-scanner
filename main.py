import pandas as pd
from pathlib import Path

csv_output_path = 'results/result.csv'


def scan_dir(path_obj: Path) -> list:
    paths = list(path_obj.glob("**/*"))

    result_paths = list()
    for path in paths:
        result_paths.append(path.resolve().relative_to(path_obj.resolve()).as_posix())

    return result_paths


def get_target_paths() -> list:
    target_dir = "targets"
    target_dirs = list(Path(target_dir).glob("*"))

    paths = list()
    for target_dir in target_dirs:
        if target_dir.is_dir():
            paths.append(target_dir)

    return paths


def scan():
    all_paths_by_target = {}
    for target_path in get_target_paths():
        all_paths_by_target[target_path] = scan_dir(target_path)

    merged_paths = list()
    for all_paths in all_paths_by_target.values():
        merged_paths += all_paths

    result_paths = list()
    for merged_path in sorted(list(set(merged_paths))):
        result_paths.append(str(merged_path))

    result_merged_paths = {"all": result_paths}

    for target_path_name in all_paths_by_target:

        diff_paths = list()
        for result_merged_path in result_merged_paths["all"]:
            if result_merged_path in all_paths_by_target[target_path_name]:
                diff_paths.append(result_merged_path)
            else:
                diff_paths.append("")

        result_merged_paths[target_path_name] = diff_paths

    pd.DataFrame(result_merged_paths).to_csv(csv_output_path)


if __name__ == '__main__':
    scan()
