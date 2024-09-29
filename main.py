import os
from dart_metrics_analyzer import DartMetricsAnalyzer

def main():
    analyzer = DartMetricsAnalyzer("repositories.txt", os.getcwd())
    results = analyzer.run_analysis()
    analyzer.write_results_to_csv(results)

if __name__ == "__main__":
    main()