# Custom App -Cash Management

Cash Management App Overview

The Cash Management app is designed to streamline the management of petty cash expenses. It comprises two main DocTypes:

Petty Cash Management (Parent DocType)
Petty Cash Expense (Child DocType)

After submitting a Petty Cash Management document, a custom "Create" button appears, allowing the user to generate a Journal Entry with pre-filled fields. This simplifies the process of recording transactions. Features

Efficiently manage petty cash transactions.
Automatically generate journal entries from petty cash data.
User-friendly interface with automated field filling.

Installation Prerequisites

Frappe framework
ERPNext
mariadb

Steps

Create a New Custom App:

bash

bench new-app cash_management

Install the App to Your Site:

bash

bench --site your-site-name install-app cash_management

Run Bench Migrations:

bash

bench --site your-site-name migrate

Start the Bench:

bash

bench start

Usage

Create a Petty Cash Management Document:
    Navigate to the Petty Cash Management module.
    Fill in the required fields such as company, posting_date, and other relevant details.
    Add items to the Petty Cash Expense child table.

Submit the Document:
    After completing the entries, submit the Petty Cash Management document.

Generate a Journal Entry:
    Upon submission, a custom "Create" button will appear.
    Click the "Create" button and select "Create Journal Entry".
    You will be redirected to the Journal Entry page with fields automatically filled.
    Review the details, then click "Save" and "Submit" to finalize the journal entry.

