# **PMTK: Project Management Toolkit**

PMTK (Project Management Toolkit) is a Python library designed to simplify and automate project management tasks. The library provides tools for creating, analyzing, and exporting network diagrams used in project management methodologies such as Critical Path Method (CPM).

---

## **Features**

- **Network Diagram Generation**: Create a network diagram with detailed activity information, including start/end times, durations, and slack values.
- **Critical Path Analysis**: Automatically identify and extract critical path activities (activities with zero slack).
- **Excel Export**: Export the network diagram to a formatted Excel file for visualization and reporting.
- **Support for Multiple Levels of Precedence**: Handles multiple levels of precedence relationships between project activities.

---

## **Installation**

You can install PMTK from PyPI using `pip`:

```bash
pip install pmtk
```

---

## **Usage**

### **1. Initialize a Network Diagram**

The `NetworkDiagram` class processes your project activities and calculates critical path information. You need to provide a Pandas DataFrame with the following columns:

- **`Activity`**: Main activities.
- **`Duration`**: Duration of the main activities.
- **`Activity.1`, `Duration.1`**: First level of precedence activities.
- **`Activity.2`, `Duration.2`**: Second level of precedence activities.
- **`Activity.3`, `Duration.3`**: Third level of precedence activities.

Example:

```python
import pandas as pd
from pmtk import NetworkDiagram

# Example DataFrame
data = {
    'Activity': ['A', 'B'],
    'Duration': [5, 3],
    'Activity.1': ['C', 'D'],
    'Duration.1': [4, 2],
    'Activity.2': ['E', 'F'],
    'Duration.2': [3, 6],
    'Activity.3': ['G', 'H'],
    'Duration.3': [2, 1]
}
df = pd.DataFrame(data)

# Initialize and calculate the network diagram
nd = NetworkDiagram(df)
network_diagram = nd.get_network_diagram()
critical_path = nd.get_critical_path()

# Print the results
print("Network Diagram:")
print(network_diagram)
print("\nCritical Path:")
print(critical_path)
```

---

### **2. Export Network Diagram to Excel**

The `NetworkDiagramExporter` class allows you to export the network diagram to a visually formatted Excel file.

Example:

```python
from pmtk import NetworkDiagramExporter

# Initialize the exporter with the NetworkDiagram object
exporter = NetworkDiagramExporter(network_diagram=nd, filename="network_diagram.xlsx")

# Export to Excel
exporter.export()

print("Network diagram exported to 'network_diagram.xlsx'")
```

---

## **Requirements**

- Python 3.6 or higher
- Pandas
- XlsxWriter (for Excel export)

---

## **Contributing**

We welcome contributions! If you have ideas, improvements, or bug fixes, please submit a pull request or open an issue.

---

## **License**

This project is licensed under the MIT License.

---

## **Contact**

For any questions or feedback, please reach out to the author:

- **Author**: Yasayah Nadeem Khokhar
- **Email**: [yasayahnadeem22@gmail.com](mailto:yasayahnadeem22@gmail.com)
- **GitHub**: [https://github.com/Yasayah-Nadeem-Khokhar/pmtk](https://github.com/Yasayah-Nadeem-Khokhar/pmtk)

--- 

This README provides a comprehensive overview of your library, including installation instructions, usage examples, and contact information. Let me know if you'd like any modifications!