<div align="center">

<img src="assets/college-of-computer.png" alt="Qassim University — College of Computer" width="520"/>

# CS471 — Django Projects

### Library Management Web Application
**Qassim University · College of Computer · CS471 (Web Application Development)**

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="Django" src="https://img.shields.io/badge/Django-6.0.2-092E20?logo=django&logoColor=white">
  <img alt="SQLite" src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white">
  <img alt="HTML5" src="https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white">
  <img alt="CSS3" src="https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-Academic-blue">
</p>

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Data Model](#-data-model)
- [Applications](#-applications)
- [Getting Started](#-getting-started)
- [Running the App](#-running-the-app)
- [Routes / URL Map](#-routes--url-map)
- [Labs Walkthrough](#-labs-walkthrough)
  - [Lab 8 — Querying the ORM](#lab-8--querying-the-orm)
  - [Lab 9 — Relationships, Aggregation & CRUD](#lab-9--relationships-aggregation--crud)
- [Database Seeding](#-database-seeding)
- [Notes & Known Caveats](#-notes--known-caveats)
- [Author & Acknowledgements](#-author--acknowledgements)

---

## 🧭 Overview

This repository contains the Django coursework for **CS471 (Web Application Development)** at **Qassim University, College of Computer**. The project is a single Django project named **`libraryproject`** that implements a small **library management** web application and the practical exercises from **Lab 8** and **Lab 9**.

The work demonstrates a full slice of modern Django development: defining relational models, querying them with the ORM (filters, `Q` objects, aggregation and annotations across relationships), building full CRUD flows in two different styles (manual request handling vs. Django `ModelForm`), template inheritance with shared layout/includes, static asset management, and Qassim University branding (custom favicon and stylesheet). Sample content and inline code comments are written in **Arabic**.

---

## ✨ Features

- **Relational data model** — `Book`, `Publisher`, and `Author` with one‑to‑many (`Publisher → Book`) and many‑to‑many (`Book ↔ Author`) relationships, plus a `Student`/`Address` pair carried over from an earlier lab.
- **ORM query demonstrations** — simple filters, chained `filter()`/`exclude()`, complex `Q` expressions using `&`, `|`, and `~`, ordering, and aggregation with `Count`, `Sum`, `Avg`, `Max`, and `Min`.
- **Cross‑relationship annotations** — per‑publisher statistics (total stock, average/min/max price, oldest publication date, conditional book counts) computed via `annotate()`.
- **Full CRUD on books, two ways** — a **manual** approach that reads `request.POST` directly, and a **`ModelForm`** approach (`BookForm`) with built‑in validation.
- **Search** — filter an in‑memory book list by title and/or author from a search form.
- **Templating** — a shared `base.html` layout with reusable header/footer includes and per‑page blocks.
- **Static assets** — custom CSS, book cover images, and the Qassim University favicon.
- **Django Admin** — enabled at `/admin/` for managing data through the built‑in interface.

---

## 🛠 Tech Stack

| Layer        | Technology                                   |
|--------------|----------------------------------------------|
| Language     | Python 3.10+                                 |
| Framework    | Django 6.0.2                                 |
| Database     | SQLite (`db.sqlite3`)                        |
| Frontend     | Django Templates, HTML5, CSS, Font Awesome 4.7 |
| Tooling      | Django ORM, `ModelForm`, virtual environment |

---

## 📁 Project Structure

```
DjangoProjects/
└── libraryproject/                # Django project root (run manage.py here)
    ├── manage.py                  # Django CLI entry point
    ├── db.sqlite3                 # SQLite database (development)
    ├── libraryproject/            # Project configuration package
    │   ├── settings.py            # Installed apps, templates, static, DB
    │   ├── urls.py                # Root URLConf (admin + books)
    │   ├── wsgi.py / asgi.py      # WSGI / ASGI entry points
    │   └── __init__.py
    └── apps/                      # Reusable apps package
        ├── bookmodule/            # Core app: models, ORM demos, CRUD, search
        │   ├── models.py          # Address, Student, Publisher, Author, Book
        │   ├── views.py           # Lab 8 & 9 views + CRUD + search + seeding
        │   ├── urls.py            # Namespaced "books.*" routes
        │   ├── forms.py           # BookForm (ModelForm)
        │   ├── admin.py
        │   └── migrations/        # 0001_initial → 0003 (schema evolution)
        ├── usermodule/            # Scaffolded app (placeholder for user features)
        ├── templates/
        │   ├── layouts/base.html  # Base layout (QU favicon + styles)
        │   ├── includes/          # header.html, footer.html
        │   └── bookmodule/        # Page + per‑task templates
        └── static/                # main.css, styles.css, book images, qu-icon.png
```

> **Note:** In the GitHub repo the project files may sit at the top level rather than under a `DjangoProjects/` wrapper. Either way, the directory that contains `manage.py` is your working directory.

---

## 🗃 Data Model

Defined in `apps/bookmodule/models.py`:

| Model       | Key Fields                                                   | Relationships                                                  |
|-------------|--------------------------------------------------------------|----------------------------------------------------------------|
| `Address`   | `city`                                                       | Referenced by `Student`                                        |
| `Student`   | `name`, `age`                                                | `address` → `Address` (ForeignKey)                             |
| `Publisher` | `name`, `location`                                           | Referenced by `Book`                                           |
| `Author`    | `name`, `DOB`                                                | Linked to `Book` (ManyToMany)                                  |
| `Book`      | `title`, `price`, `quantity`, `pubdate`, `rating`            | `publisher` → `Publisher` (FK, `SET_NULL`); `authors` → `Author` (M2M) |

**Relationship summary**

- One `Publisher` can have many `Book`s; deleting a publisher sets the book's `publisher` to `NULL`.
- A `Book` can have many `Author`s, and an `Author` can write many `Book`s (many‑to‑many).
- A `Student` belongs to one `Address`; deleting an address cascades to its students.

---

## 🧩 Applications

**`bookmodule`** — the heart of the project. It owns all models, the URL map (every route is namespaced `books.*`), the views for both lab sessions, the CRUD flows, search, and the database‑seeding endpoints.

**`usermodule`** — a scaffolded Django app reserved for user‑related functionality. Its `models.py` and `views.py` are currently placeholders, leaving room for future authentication or profile features.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10+**
- `pip` and (recommended) the `venv` module

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/9llmy/CS471_DjangoProjects.git
cd CS471_DjangoProjects          # then cd into the folder containing manage.py

# 2. Create and activate a virtual environment
python -m venv djangoenv
# Windows
djangoenv\Scripts\activate
# macOS / Linux
source djangoenv/bin/activate

# 3. Install Django
pip install "Django>=6.0,<6.1"

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. (Optional) Create an admin account for /admin/
python manage.py createsuperuser
```

---

## ▶ Running the App

```bash
python manage.py runserver
```

Open your browser at:

- **App (book module):** http://127.0.0.1:8000/books/
- **Admin panel:** http://127.0.0.1:8000/admin/

---

## 🗺 Routes / URL Map

All book‑module routes are mounted under the `/books/` prefix (see `libraryproject/urls.py` → `apps.bookmodule.urls`).

| Path                                  | View               | Purpose                                       |
|---------------------------------------|--------------------|-----------------------------------------------|
| `/books/`                             | `index`            | Home page                                     |
| `/books/list_books/`                  | `list_books`       | Static book list                              |
| `/books/<int:bookId>/`                | `viewbook`         | Single book page                              |
| `/books/aboutus/`                     | `aboutus`          | About page                                    |
| `/books/search/`                      | `search`           | Search by title / author                      |
| `/books/html5/links/`                 | `links`            | HTML5 links demo                              |
| `/books/html5/text/formatting/`       | `formatting`       | HTML5 text‑formatting demo                    |
| `/books/html5/listing/`               | `listing`          | HTML5 lists demo                              |
| `/books/html5/tables/`                | `tables`           | HTML5 tables demo                             |
| `/books/init-db/`                     | `init_db`          | Seed sample books *(legacy schema — see caveats)* |
| `/books/init-students/`               | `init_students`    | Seed sample students & cities                 |
| `/books/init-lab9/`                   | `init_lab9`        | Seed Lab 9 publishers, authors & books        |
| `/books/simple/query/`                | `simple_query`     | Simple ORM filter                             |
| `/books/complex/query/`               | `complex_query`    | Chained ORM filters                           |
| `/books/lab8/task1/`                  | `task1`            | `Q` filter: price ≤ 80                         |
| `/books/lab8/task2/`                  | `task2`            | Combined `Q` with `&` and `|`                  |
| `/books/lab8/task3/`                  | `task3`            | Negated conditions with `~`                    |
| `/books/lab8/task4/`                  | `task4`            | Order books by title                           |
| `/books/lab8/task5/`                  | `task5`            | Library‑wide aggregate statistics              |
| `/books/lab8/task7/`                  | `task7`            | Student count per city (`annotate`)            |
| `/books/lab9/task1/`                  | `task1_lab9`       | Each book's share of total stock (%)           |
| `/books/lab9/task2/`                  | `task2_lab9`       | Total stock per publisher                      |
| `/books/lab9/task3/`                  | `task3_lab9`       | Oldest publication date per publisher          |
| `/books/lab9/task4/`                  | `task4_lab9`       | Avg / min / max price per publisher            |
| `/books/lab9/task5/`                  | `task5_lab9`       | Count of books rated ≥ 4 per publisher         |
| `/books/lab9/task6/`                  | `task6_lab9`       | Conditional book count per publisher           |
| `/books/lab9_part1/listbooks/`        | `listbooks`        | List books (CRUD)                              |
| `/books/lab9_part1/addbook/`          | `addbook`          | Add book — manual                              |
| `/books/lab9_part1/editbook/<id>/`    | `editbook`         | Edit book — manual                             |
| `/books/lab9_part1/deletebook/<id>/`  | `deletebook`       | Delete book                                    |
| `/books/lab9_part2/addbook/`          | `addbook_part2`    | Add book — `ModelForm`                          |
| `/books/lab9_part2/editbook/<id>/`    | `editbook_part2`   | Edit book — `ModelForm`                          |

---

## 📚 Labs Walkthrough

### Lab 8 — Querying the ORM

This lab focuses on **reading** data with the Django ORM.

- **`simple_query`** — returns books whose title contains a keyword (`title__icontains`).
- **`complex_query`** — chains several conditions (`filter`/`exclude`) to narrow results.
- **`task1`** — uses a `Q` object to fetch books priced at 80 or less.
- **`task2`** — combines conditions with `&` (AND) and `|` (OR) inside `Q`.
- **`task3`** — negates conditions with `~` (NOT).
- **`task4`** — orders all books alphabetically by title (`order_by`).
- **`task5`** — computes library‑wide aggregates: total count, total/average/max/min price.
- **`task7`** — annotates each city with the number of students living there (`Count`).

### Lab 9 — Relationships, Aggregation & CRUD

This lab introduces **relationships**, **cross‑table aggregation**, and **writing** data.

- **`task1_lab9`** — calculates each book's percentage share of the library's total stock.
- **`task2_lab9`** — sums `quantity` of related books per publisher (`Sum('book__quantity')`).
- **`task3_lab9`** — finds the oldest publication date per publisher (`Min('book__pubdate')`).
- **`task4_lab9`** — computes average, minimum, and maximum book price per publisher.
- **`task5_lab9`** — counts books rated 4 or higher for each publisher.
- **`task6_lab9`** — counts books per publisher under combined price/quantity conditions.

**CRUD — Part 1 (manual):** `listbooks`, `addbook`, `editbook`, and `deletebook` handle create/read/update/delete by reading `request.POST` fields directly and redirecting back to the list.

**CRUD — Part 2 (`ModelForm`):** `addbook_part2` and `editbook_part2` use `BookForm` (a `ModelForm` bound to `Book`) so Django generates and validates the form automatically — `form.save()` persists the record in a single call.

---

## 🌱 Database Seeding

Three helper endpoints populate sample data so the query pages have something to display:

- **`/books/init-students/`** — creates two cities (الرياض، القصيم) and five students linked to them.
- **`/books/init-lab9/`** — creates two publishers (دار القلم، دار المنهاج), two authors (ابن قيم الجوزية، الذهبي), and two books wired up with publisher and author relationships.
- **`/books/init-db/`** — seeds books using an older schema *(see caveats below)*.

Visit a seeding URL once, then browse the corresponding query pages.

---

## ⚠ Notes & Known Caveats

- The database is **SQLite** and intended for **development / coursework only**. `settings.py` ships with `DEBUG = True` and a development `SECRET_KEY` — do not deploy as‑is.
- Some **early Lab 8 endpoints** (`init_db`, `simple_query`, the lab8 `task` views) reference an **older `Book` schema** that used `author` and `edition` fields. The current model (after migration `0003`) uses `publisher`, `authors` (M2M), `pubdate`, `rating`, and `quantity`. If you call those legacy endpoints they may error against the current schema — use **`/books/init-lab9/`** for seeding and the **Lab 9** pages to see the relational features working end‑to‑end. Aligning the legacy views with the current model is a good cleanup task.
- Several templates and all seeded sample data are in **Arabic**.
- If you commit a local virtual environment folder (e.g. `djangoenv/`), consider adding it to `.gitignore` to keep the repository lean.

---

## 👤 Author & Acknowledgements

**9llmy** — Qassim University, College of Computer · CS471
GitHub: [@9llmy](https://github.com/9llmy)

<div align="center">

<img src="assets/college-of-computer.png" alt="Qassim University — College of Computer" width="360"/>

> 📖 Academic coursework submitted for the **CS471 — Web Application Development** course.

</div>
