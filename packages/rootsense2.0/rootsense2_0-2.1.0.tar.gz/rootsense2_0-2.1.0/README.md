Here is the updated README for your project: 

```markdown
# rootsense2.0

A multithreading application for system monitoring, resource analysis, and predictive insights. This package integrates multiple functionalities for efficient resource management and includes Streamlit-based visualizations.

## Features

- **osinfo**: Collects and displays system information.
- **predict**: Trains predictive models for system resource usage.
- **root**: Performs root cause analysis based on system logs.
- **ticket**: Manages and analyzes tickets for system issues.
- **threads**: Combines all functionalities with multithreading for simultaneous execution.
- **chart**: Provides interactive charts using Streamlit.
- **report**: Generates detailed reports using Streamlit.

## Installation

1. Install Python (>=3.6).
2. Install the package via pip:

```bash
pip install rootsense2
```

## Usage

### Run All Functionalities

To execute all modules with multithreading:

```bash
python -m rootsense2.threads
```

### Streamlit Applications

To run Streamlit apps separately:

```bash
streamlit run src/rootsense2/chart.py
streamlit run src/rootsense2/report.py
```

### Individual Modules

Each module can be run independently:

```bash
python -m rootsense2.osinfo
python -m rootsense2.predict
python -m rootsense2.root
python -m rootsense2.ticket
```

## Dependencies

The following main Python libraries are required:

- `pymongo`
- `streamlit`
- `scipy`
- `sklearn`
- `pandas`
- `numpy`
- `logging`

Install dependencies automatically during package installation or manually using:

```bash
pip install -r requirements.txt
```

## Project Structure

```
rootsense2/
├── src/
│   ├── rootsense2/
│   │   ├── __init__.py
│   │   ├── threads.py
│   │   ├── osinfo.py
│   │   ├── predict.py
│   │   ├── root.py
│   │   ├── ticket.py
│   │   ├── chart.py
│   │   ├── report.py
├── README.md
├── LICENSE
├── setup.py
├── requirements.txt
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for enhancements or bug fixes.

## Support

For any questions or issues, please contact [yarnalkaramey@gmail.com](mailto:yarnalkaramey@gmail.com).
```

This README provides a complete overview of the project, including its structure, usage, and installation. Let me know if you'd like to adjust anything further!