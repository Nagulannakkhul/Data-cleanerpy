# 🚀 Data Cleaner App

A modern, user-friendly GUI application for cleaning and preprocessing CSV and Excel datasets. Built using Python, Pandas, and CustomTkinter with AI-powered features.

---

## 📌 Features

### 📂 Data Upload

* Load CSV or Excel (.xlsx) files
* View dataset information (rows, columns)
* Quick preview of uploaded data

---

### 🧹 Data Cleaning Options

* Remove duplicate rows
* Remove empty rows / rows with empty cells
* Strip whitespace from text columns
* Remove special characters
* Fix inconsistent text (case formatting)
* Remove negative values
* Fix invalid dates
* Apply IQR-based outlier removal
* Fill missing values (median/mode)
* Auto-convert data types
* Overbound cleaning (min/max filtering)
* 🔥 Remove highly correlated columns

---

### 🤖 AI-Based Cleaning

* Analyze dataset using AI
* Suggest cleaning steps
* Apply automatic smart cleaning

---

### 📊 Data Quality Report

* Data Quality Score (0–100)
* Missing values (%)
* Duplicate rows (%)
* Outliers detection
* Invalid data detection
* 🔥 Highly correlated columns report

---

### 💾 Data Export

* Save cleaned data as:

  * CSV
  * Excel
  * JSON

---

### 🎨 User Interface

* Step-by-step wizard (Upload → Clean → Report → Save)
* Responsive layout
* Modern dark theme UI
* Interactive buttons and feedback

---

## ⚙️ Installation

### ✅ Prerequisites

* Python 3.8 or higher
* Tkinter (comes with Python)
* Internet connection (for AI features)

---

### 🛠️ Setup

1. Clone the repository:

```bash
git clone https://github.com/Nagulannakkhul/data-cleaning-project.git
cd data-cleaning-project
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the application:

```bash
python main.py
```

---

### 🔄 Workflow

1. **Upload**

   * Select CSV / Excel dataset

2. **Clean**

   * Choose cleaning options
   * Apply manual or AI cleaning

3. **Report**

   * View data quality score
   * Analyze issues and correlations

4. **Save**

   * Export cleaned dataset

---

## 📦 Requirements

* pandas >= 2.0.0
* numpy >= 1.20.0
* customtkinter >= 5.0.0
* openpyxl >= 3.0.0
* google-generativeai (for AI features)

---

## 📁 Project Structure

```
data-cleaning-project/
├── main.py
├── data_cleaner.py
├── llm_cleaner.py
├── utils.py
├── requirements.txt
├── components/
│   └── step_indicator.py
└── pages/
    ├── upload_page.py
    ├── clean_page.py
    ├── save_page.py
    └── report_page.py
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes

   ```bash
   git commit -m "Add new feature"
   ```
4. Push to GitHub

   ```bash
   git push origin feature/your-feature
   ```
5. Create a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgments

* CustomTkinter for modern UI
* Pandas & NumPy for data processing
* AI APIs for intelligent data analysis

---

## 👨‍💻 Author

**Nagulan Nakkhul**
GitHub: https://github.com/Nagulannakkhul
