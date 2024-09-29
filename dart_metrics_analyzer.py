import os
import subprocess
import csv
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class MetricsResult:
    url: str
    sloc: int = 0
    noc: int = 0
    nom: int = 0
    dit: int = 0
    rfc: int = 0
    cbo: int = 0
    wmc: int = 0


class DartMetricsAnalyzer:
    def __init__(self, repositories_file: str, results_dir: str):
        self.repositories = self.load_repositories(repositories_file)
        self.results_dir = results_dir
        self.repo_dir = os.path.join(results_dir, "repositories")
        self.dcm_analysis_options = self.get_dcm_analysis_options()

    @staticmethod
    def load_repositories(file_path: str) -> List[str]:
        with open(file_path, "r") as f:
            return f.read().splitlines()

    @staticmethod
    def get_dcm_analysis_options() -> str:
        return """
        dart_code_metrics:
            metrics:
                source-lines-of-code: 0
                cyclomatic-complexity: 0
                coupling-between-object-classes: 0
                depth-of-inheritance-tree: 0
                number-of-methods: 0
                response-for-class: 0
                number-of-external-imports: 0
                weighted-methods-per-class: 0
        """

    def prepare_directory(self) -> None:
        os.makedirs(self.repo_dir, exist_ok=True)
        os.chdir(self.repo_dir)

    def clone_repository(self, repo: str, path: str) -> bool:
        try:
            subprocess.run(
                f"git clone {repo} {path}",
                shell=True,                
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository {repo}: {e}")
            return False

    def find_pubspec_yaml(self, path: str) -> str:
        if os.path.exists(os.path.join(path, "pubspec.yaml")):
            return path
        for subdir, _, files in os.walk(path):
            if "pubspec.yaml" in files:
                return subdir
        return path

    def write_analysis_options(self, path: str) -> None:
        with open(os.path.join(path, "analysis_options.yaml"), "w") as f:
            f.write(self.dcm_analysis_options)

    def run_dart_code_metrics(self, path: str) -> str:
        result = subprocess.run(
            "dcm calculate-metrics . -c --report-all",
            shell=True,
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.decode()

    def parse_metrics(self, output: str) -> Dict[str, int]:
        metrics = {
            "sloc": 0,
            "noc": 0,
            "nom": 0,
            "dit": 0,
            "rfc": 0,
            "cbo": 0,
            "wmc": 0,
        }
        for line in output.split("\n"):
            if "SLOC" in line:
                metrics["sloc"] = int(line.split("sum: ")[1])
            elif "Scanned classes:" in line:
                metrics["noc"] = int(line.split("Scanned classes: ")[1])
            elif "number of methods" in line:
                metrics["nom"] += int(
                    line.split("methods")[1].split(": ")[1].split(" ")[0]
                )
            elif "depth of inheritance tree" in line:
                metrics["dit"] += int(
                    line.split("tree")[1].split(": ")[1].split(" ")[0]
                )
            elif "response for a class" in line:
                metrics["rfc"] += int(
                    line.split("class")[1].split(": ")[1].split(" ")[0]
                )
            elif "coupling between object classes" in line:
                metrics["cbo"] += int(
                    line.split("classes")[1].split(": ")[1].split(" ")[0]
                )
            elif "weighted methods per class" in line:
                metrics["wmc"] += int(line.split("class")[1].split(": ")[1])
        return metrics

    def analyze_repository(self, repo: str, index: int) -> MetricsResult:
        path = os.path.join(self.repo_dir, str(index))
        result = MetricsResult(url=repo)

        if not os.path.exists(path) and not self.clone_repository(repo, path):
            return result

        path = self.find_pubspec_yaml(path)
        self.write_analysis_options(path)

        output = self.run_dart_code_metrics(path)
        metrics = self.parse_metrics(output)

        return MetricsResult(url=repo, **metrics)

    def run_analysis(self) -> List[MetricsResult]:
        self.prepare_directory()
        results = []

        for i, repo in enumerate(self.repositories, 1):
            result = self.analyze_repository(repo, i)
            print(
                f"\n{i}/{len(self.repositories)}: {repo} - SLOC: {result.sloc}, NOC: {result.noc}, NOM: {result.nom}, DIT: {result.dit}, RFC: {result.rfc}, CBO: {result.cbo}, WMC: {result.wmc}\n"
            )
            results.append(result)
            subprocess.run(f"rmdir /s /q {self.repo_dir}\\{i}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)            
        
        subprocess.run(f"rmdir /s /q {self.repo_dir}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
        return results

    def write_results_to_csv(self, results: List[MetricsResult]) -> None:
        headers = [
            "URL",
            "SLOC (Source Lines of Code)",
            "NOC (Number of Classes)",
            "NOM (Number of Methods)",
            "DIT (Depth of Inheritance Tree)",
            "RFC (Response for Class)",
            "CBO (Coupling Between Object Classes)",
            "WMC (Weighted Methods per Class)",
        ]

        with open(os.path.join(self.results_dir, "results.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for result in results:
                writer.writerow(
                    [
                        result.url,
                        result.sloc,
                        result.noc,
                        result.nom,
                        result.dit,
                        result.rfc,
                        result.cbo,
                        result.wmc,
                    ]
                )
