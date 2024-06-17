// Copyright (c) 2024, Maria Rose Xavier and contributors
// For license information, please see license.txt

frappe.ui.form.on("Petty Cash Management", {
	refresh: function(frm) {
        // Filter active employees
        frm.set_query('employee', function() {
            return {
                filters: {
                    status: 'Active'
                }
            };
        });

        // Filter cash accounting ledger
        frm.set_query('cash_accounting_ledger', function() {
            return {
                filters: {
                    account_type: 'Cash'
                }
            };
        });

        // Filter expense accounting ledger in child table
        frm.fields_dict['expenses'].grid.get_field('expense_accounting_ledger').get_query = function() {
            return {
                filters: {
                    account_type: 'Expense Account'
                }
            };
        };
        
        if(frm.doc.docstatus ===1 && frm.doc.status !== 'Closed' && frm.doc.status !== 'On Hold') {
            frm.add_custom_button(__('Journal Entry'),
            function() {
                frappe.model.open_mapped_doc({
                    method: "cash_management.cash_management.doctype.petty_cash_management.petty_cash_management.create_journal_entry",
                    frm:frm,
                });
                
                
            }, __("Create"));
            
        }
    }
});
