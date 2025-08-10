# Title

## Team 

1. Banyar Saw Thit
2. Bui Tran Doan
3. Hein Htet Aung
4. Zwe Nanda
---
## Team Roles
1. Banyar Saw Thit (Backend Engineering)
2. Bui Tran Doan (Product Owner)
3. Hein Htet Aung (Frontend Engineering)
4. Zwe Nanda (UI/UX designer)
---
## Project overview
This project is a Django-based Restaurant Management System designed to help restaurants streamline their daily operations. It includes features for managing menus, orders, inventory, staff, and sales reporting. By providing an integrated dashboard and role-based access, the system improves efficiency, reduces manual errors, and enhances decision-making for managers and staff. The solution is tailored for small to medium-sized restaurants aiming for an all-in-one management tool.

---
## Project goals
The main goal of this project is to develop a user-friendly and efficient platform for managing restaurant operations. We aim to provide managers with tools for real-time monitoring of sales, inventory, and staff performance while giving staff an easy way to manage orders and menu updates. The system should be secure, scalable, and adaptable to different restaurant workflows. Ultimately, it should save time, improve accuracy, and support better customer service.

---
## Checklist / TODOs:
* Update the following during each weekly prac session.
* GitHub entry timestamp is BEFORE iteration-1.
* User stories are correct and complete (see textbook p.39).
* Must have more user stories than can fit into iterations 1 and 2 — to practice prioritizing.

---

## Iteration 1 [duration 4 weeks], 10/06/2025 – 07/07/2025

* Goal is to have 2 iterations during a trimester of teaching.  
* Update the following during each week prac session  
* During pracs, you may experiment with using other GitHub ways of tracking changes, e.g. via pull requests

1. [Add menu items](./user_stories/user_story_01_add_menu_items.md), priority High, 2 days  
2. [Store customer orders](./user_stories/user_story_02_store_customer_orders.md), priority High, 3 days  
3. [Store inventory data](./user_stories/user_story_03_store_inventory_data.md), priority High, 3 days  
4. [System Architecture & UI Sketching](./user_stories/task_system_architecture_ui.md), priority Medium, 1 day  

**Total:** 9 days

---

### Iteration 2 [duration 4 weeks], 15/07/2025 – 11/08/2025

* Goal is to have 2 iterations during a trimester of teaching.  

1. [Manage staff access & info](./user_stories/user_story_04_manage_staff_access.md), priority High, 3 days  
2. [Store labor/staff data](./user_stories/user_story_05_store_labor_data.md), priority High, 3 days  
3. [Dashboard overview](./user_stories/user_story_06_dashboard_overview.md), priority High, 1 day  

**Total:** 7 days

---

### Not enough time/developers:

1. [CI/CD pipeline setup](./user_stories/task_cicd_pipeline.md), priority Medium, 2 days  
2. [Write authentication unit tests](./user_stories/task_auth_unit_tests.md), priority Low, 2 days  

**Total:** 4 days

# Actual iterations
1. [Iteration-1](./iteration_1.md)
2. [Iteration-2](./iteration_2.md)

---

## Installation Instructions

Follow the steps below to set up the project locally:
1. Clone the Repository
<pre>git clone https://github.com/your-repo-name.git
cd your-repo-name</pre>
2. Create and Activate a Virtual Environment

On Windows:

 <pre> python -m venv venv  </pre> 

On macOS/Linux:

<pre>source venv/bin/activate</pre>

3. Install Required Dependencies

<pre>pip install -r requirements.txt</pre>


4. Set Up the Database

Run migrations to create database tables:
<pre>python manage.py makemigrations</pre>
<pre>python manage.py migrate</pre>

5. Create a Superuser (Admin)
<pre>python manage.py createsuperuser</pre>


Follow the prompts to set username, email, and password.
6. Run the Development Server
<pre>python manage.py runserver</pre>


Access the app at http://127.0.0.1:8000/

