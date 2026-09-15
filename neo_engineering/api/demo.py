"""UI-triggered demo utilities.

Lets an administrator load the full demo dataset and create a customer
test user from the Engineering Dashboard — no terminal required.
Both endpoints are restricted to System Manager.
"""

import frappe
from frappe import _

DEMO_USER_EMAIL = "customer.demo@neoengineering.test"
DEMO_USER_ROLES = [
    "Engineering Management", "Project Manager", "Design Lead",
    "Technical Manager", "Supervision Manager",
    # standard-module read/work access for the demo walkthrough
    "Projects User", "Sales User", "Purchase User", "Accounts User",
    "Support Team",
]


@frappe.whitelist()
def demo_status():
    frappe.only_for("System Manager", message=True)
    from neo_engineering.setup.demo import PROJECTS
    names = [p[0] for p in PROJECTS]
    loaded = frappe.db.count("Project", {"project_name": ("in", names)})
    return {
        "demo_projects": loaded,
        "total_expected": len(names),
        "demo_user_exists": bool(frappe.db.exists("User", DEMO_USER_EMAIL)),
        "demo_user_email": DEMO_USER_EMAIL,
    }


@frappe.whitelist()
def load_demo_data():
    frappe.only_for("System Manager", message=True)
    from neo_engineering.setup.demo import make_demo_data
    make_demo_data()
    status = demo_status()
    frappe.msgprint(_("Demo data loaded: {0} demo project(s) with the full "
        "record chain, masters, and dashboard history.").format(
        status["demo_projects"]), indicator="green",
        title=_("Demo ready"))
    return status


@frappe.whitelist()
def delete_demo_data():
    frappe.only_for("System Manager", message=True)
    from neo_engineering.setup.demo import delete_demo_data as _delete
    _delete()
    return demo_status()


@frappe.whitelist()
def create_demo_user(password=None):
    """Create (or refresh) the customer test user and return credentials.
    The password is shown ONCE to the administrator — advise the customer
    to change it, and disable this user after the evaluation."""
    frappe.only_for("System Manager", message=True)
    password = password or frappe.generate_hash(length=10) + "!a1"

    if frappe.db.exists("User", DEMO_USER_EMAIL):
        user = frappe.get_doc("User", DEMO_USER_EMAIL)
        user.enabled = 1
    else:
        user = frappe.get_doc({
            "doctype": "User", "email": DEMO_USER_EMAIL,
            "first_name": "Customer Demo", "last_name": "| عميل تجريبي",
            "send_welcome_email": 0, "user_type": "System User",
            "language": "en",
        })
    user.new_password = password
    existing = {r.role for r in (user.get("roles") or [])}
    for role in DEMO_USER_ROLES:
        if role not in existing and frappe.db.exists("Role", role):
            user.append("roles", {"role": role})
    user.flags.ignore_permissions = True
    user.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "email": DEMO_USER_EMAIL,
        "password": password,
        "note": _("Share these credentials with the customer. The user can "
                  "switch to Arabic from My Settings → Language. Disable this "
                  "user after the evaluation (User list → disable)."),
    }
