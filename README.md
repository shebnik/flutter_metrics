# Flutter Metrics
This is a simple Python script to automate the process of running the [Dart Code Metrics](https://dcm.dev/) tool on a Flutter projects, which could be useful for building Regression models. It uses the links of repositories provided in `repositories.txt` file to clone the repositories and run the tool on them. The results are stored in a CSV file.

## How to use
1. Clone the repository
    ```bash
    git clone https://github.com/shebnik/dart_code_metrics.git
    ```

2. Follow the `Step 1` and `Step 3` in [DCM Quick Start Guide](https://dcm.dev/docs/quick-start/). For free license key visit [DCM Pricing](https://dcm.dev/pricing/).
3. Enter desired GitHub repositories URL's in `repositories.txt' file.
4. Run the script
    ```bash
    python3 main.py
    ```

## Output
The output is stored in a CSV file named `results.csv`. The columns are:
- URL of Repository
- SLOC - [Source Lines of Code](https://dcm.dev/docs/metrics/function/source-lines-of-code/)
- NOC - [Number of Classes](https://dcm.dev/docs/metrics/#class)
- NOM - [Number of Methods](https://dcm.dev/docs/metrics/class/number-of-methods/)
- DIT - [Depth of Inheritance Tree](https://dcm.dev/docs/metrics/class/depth-of-inheritance-tree/)
- RFC - [Response for Class](https://dcm.dev/docs/metrics/class/response-for-class/)
- CBO - [Coupling Between Object Classes](https://dcm.dev/docs/metrics/class/coupling-between-object-classes/)
- WMC - [Weighted Methods per Class](https://dcm.dev/docs/metrics/class/weighted-methods-per-class/)

## Platforms
Script tested and working only on Windows.

## Contributing

If you would like to contribute to the project, follow these steps:

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.