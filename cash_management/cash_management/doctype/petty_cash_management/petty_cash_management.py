import frappe
from frappe.utils import flt
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PettyCashManagement(Document):
    pass

@frappe.whitelist()
def create_journal_entry(source_name, target_doc=None, skip_item_mapping=False):

    def update_item(source, target, source_parent):
        target.debit_in_account_currency = flt(source.amount)
        target.cost_center = source_parent.cost_center
        target.party_type = "Supplier"
        target.party = source.supplier
        target.voucher_type = "Journal Entry"
        target.user_remark = source.remark

    mapper = {
        "Petty Cash Management": {
            "doctype": "Journal Entry",
            "field_map": {
                "company": "company",
                "posting_date": "posting_date"
            },
            "validation": {"docstatus": ["=", 1]}
        },
    }

    if not skip_item_mapping:
        mapper["Petty Cash Expense"] = {
            "doctype": "Journal Entry Account",
            "field_map": {
                "amount": "debit_in_account_currency",
            },
            "postprocess": update_item,
        }

    try:
        # Verify if the source document exists
        source_doc = frappe.get_doc("Petty Cash Management", source_name)
        frappe.log_error(message=f"Source document found: {source_doc.name}", title="Debug Log")

        # Check the number of rows in the relevant child table (Petty Cash Expense)
        if len(source_doc.get("expenses")) == 1:
            frappe.log_error(message="Only one row found in Petty Cash Expense", title="Debug Log")
            # Handle the case where there is only one row in the Petty Cash Expense table
            expense = source_doc.expenses[0]
            target_doc = frappe.new_doc("Journal Entry")
            target_doc.company = source_doc.company
            target_doc.posting_date = source_doc.posting_date

            # Add debit entry
            target_doc.append("accounts", {
                "account": expense.expense_accounting_ledger,
                "debit_in_account_currency": flt(expense.amount),
                "user_remark": expense.remark
            })

            # Add credit entry
            target_doc.append("accounts", {
                "account": source_doc.cash_accounting_ledger,
                "credit_in_account_currency": flt(expense.amount),
                "party_type": "Supplier",
                "party": expense.supplier,
                "user_remark": expense.remark
            })
        else:
            # Perform the mapping as usual
            target_doc = get_mapped_doc("Petty Cash Management", source_name, mapper, target_doc)
            frappe.log_error(message=f"Journal Entry created successfully for source_name: {source_name}", title="Debug Log")

        return target_doc

    except frappe.DoesNotExistError:
        frappe.throw(f"Petty Cash Management document with name {source_name} not found")
    except Exception as e:
        frappe.log_error(message=str(e), title="Error in create_journal_entry")
        frappe.throw(f"An error occurred while creating the Journal Entry: {str(e)}")
