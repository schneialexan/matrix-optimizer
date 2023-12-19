<div align="center">
<h1 align="center">
<img src="https://cdn.icon-icons.com/icons2/1223/PNG/512/1492617364-13-setting-configure-repair-support-optimization-google_83447.png" width="250" />
<br></h1>
<h3>DAViS - Dashboard für EVA Matrix Optimierung</h3>
<h3>◦ Developed with the software and tools below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/SciPy-8CAAE6.svg?style=flat-square&logo=SciPy&logoColor=white" alt="SciPy" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat-square&logo=pandas&logoColor=white" alt="pandas" />
<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat-square&logo=NumPy&logoColor=white" alt="NumPy" />
<img src="https://img.shields.io/badge/Dash-008DE4.svg?style=flat-square&logo=Dash&logoColor=white" alt="Dash" />
</p>
</div>

---

## 📖 Table of Contents
- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [📂 repository Structure](#-repository-structure)
- [⚙️ Modules](#modules)
- [🚀 Getting Started](#-getting-started)
    - [🔧 Installation](#-installation)
    - [🤖 Running ](#-running-)
    - [🧪 Tests](#-tests)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview

This is a project made by Alexandru Schneider while studying (BSc Computational and Data Science) at the FHGR in Chur (Switzerland). The goal was to optimize the EVA Matrix, which is needed to make an empirical aggregation approach for cities.

---

## 📦 Features

In the first page you input a file which NEEDS to contain:

- only numbers
- column with name 'year'
- column with name 'bfs_nummer'

This then makes the necessary yearly numpy arrays, which then are used to optimize the Matrix on the second page.

---


## 📂 Repository Structure

```sh
└── /
    ├── helpers/
    │   ├── helpers.py
    │   └── sideBar.py
    ├── main.py
    ├── optimizers/
    │   ├── cvxpy_minimizer.py
    │   ├── scipy_minimizer.py
    │   └── sgd_minimizer.py
    ├── pages/
    │   ├── data_selector.py
    │   └── matrix_optimizer.py
    └── requirements.txt

```

---


## ⚙️ Modules

<details closed><summary>Root</summary>

| File                               | Summary       |
| ---                                | ---           |
| [main.py]({file_path})             | Dash App is here|
| [requirements.txt]({file_path})    | All Python Modules Required |
| [helpers.py]({file_path})          | Helper functions for conversion and simulation |
| [sideBar.py]({file_path})          | Sidebar HTML Code and logo |
| [cvxpy_minimizer.py]({file_path})  | The optimization code with the CVXPY library |
| [scipy_minimizer.py]({file_path})  | The optimization code with the SCIPY library |
| [sgd_minimizer.py]({file_path})    | The optimization code with my own SGD |
| [data_selector.py]({file_path})    | The First Page when starting the website |
| [matrix_optimizer.py]({file_path}) | The Second Page, where the optimization loop is|

</details>

---

## 🚀 Getting Started

***Dependencies***

Please ensure you have the following dependencies installed on your system:

`- ℹ️ at least Python 3.9`

`- ℹ️ This was run on a Windows Environment`


### 🔧 Installation

1. Clone the  repository:
```sh
git clone git@github.com:schneialexan/matrix-optimizer.git
```

2. Change to the project directory:
```sh
cd matrix-optimizer
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🤖 Running 

```sh
python main.py
```

### 🧪 Tests
```sh
pytest
```

---


## 🛣 Project Roadmap

> - [X] `ℹ️  Task 1: SGD Algorithmus`
> - [X] `ℹ️  Task 2: Scipy Optimize`
> - [X] `ℹ️  Task 3: Constraints Brainstorming`
> - [X] `ℹ️  Task 4: Constraint Implementing (Max-Change)`
> - [X] `ℹ️  Task 5: Constraint Implementing (Lock-Indices)`
> - [X] `ℹ️  Task 6: Implementing CVXPY`
> - [X] `ℹ️  Task 7: Polishing GUI`
> - [X] `ℹ️  Task 7: Delpoyment: https://matrix-optimizer-production.up.railway.app/`


---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/local//blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/local//discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/local//issues)**: Submit bugs found or log feature requests for LOCAL.

#### *Contributing Guidelines*

<details closed>
<summary>Click to expand</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone <your-forked-repo-url>
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear and concise message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

## 📄 License


This project is protected under the [MIT-LICENCE](https://github.com/schneialexan/matrix-optimizer/blob/main/LICENSE) License. For more details, refer to the [LICENSE](https://github.com/schneialexan/matrix-optimizer/blob/main/LICENSE) file.

---

## 👏 Acknowledgments

- DAViS Team (Alexander van Schie & Marco Schmid)
- Ansprechperson (Heiko Rölke) (Ebenfalls im DAViS Team)

[**Return**](#Top)

---

