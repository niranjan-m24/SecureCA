import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="SecureCA | Client Intelligence", page_icon="🔎", layout="wide")

st.title("🔎 SecureCA")
st.caption("Unified Client Intelligence — prototype for academic demonstration")
st.info("Demo only: the included records are synthetic. Alerts indicate items for review, not confirmed errors, fraud, or tax non-compliance.")

# Demo data
clients_demo = pd.DataFrame([
    {"client_id": "C001", "client_name": "ABC Traders", "business_type": "Trading", "financial_year": "2026-27"},
    {"client_id": "C002", "client_name": "Sunrise Foods", "business_type": "Food processing", "financial_year": "2026-27"},
    {"client_id": "C003", "client_name": "Pioneer Services", "business_type": "Services", "financial_year": "2026-27"},
])
accounting_demo = pd.DataFrame([
    {"client_id": "C001", "reference": "PUR-101", "date": "2026-10-05", "record_type": "Purchase", "party": "Shree Suppliers", "amount": 50000},
    {"client_id": "C001", "reference": "PUR-102", "date": "2026-10-08", "record_type": "Purchase", "party": "Metro Distributors", "amount": 24000},
    {"client_id": "C001", "reference": "SAL-201", "date": "2026-10-12", "record_type": "Sales", "party": "Retail Customer A", "amount": 125000},
    {"client_id": "C002", "reference": "PUR-301", "date": "2026-10-10", "record_type": "Purchase", "party": "Fresh Inputs Ltd", "amount": 55000},
    {"client_id": "C002", "reference": "SAL-401", "date": "2026-10-15", "record_type": "Sales", "party": "Local Retailer", "amount": 98000},
    {"client_id": "C003", "reference": "SAL-501", "date": "2026-10-18", "record_type": "Sales", "party": "Client Z", "amount": 76000},
])
support_demo = pd.DataFrame([
    {"client_id": "C001", "reference": "PUR-101", "date": "2026-10-05", "party": "Shree Suppliers", "amount": 55000, "document_name": "invoice_101.pdf"},
    {"client_id": "C001", "reference": "PUR-102", "date": "2026-10-08", "party": "Metro Distributors", "amount": 24000, "document_name": "invoice_102.pdf"},
    {"client_id": "C002", "reference": "PUR-301", "date": "2026-10-10", "party": "Fresh Inputs Ltd", "amount": 55000, "document_name": "invoice_301.pdf"},
])
tasks_demo = pd.DataFrame([
    {"client_id": "C001", "task": "October bank reconciliation", "due_date": "2026-11-30", "status": "Pending"},
    {"client_id": "C001", "task": "Collect purchase invoice PUR-101", "due_date": "2026-11-28", "status": "Pending"},
    {"client_id": "C002", "task": "Review monthly GST summary", "due_date": "2026-11-29", "status": "In progress"},
    {"client_id": "C003", "task": "Confirm sales ledger", "due_date": "2026-12-02", "status": "Completed"},
])
reg_demo = pd.DataFrame([
    {"topic": "Income-tax update", "published_date": "Replace with verified date", "effective_date": "Verify applicability", "summary": "Demo placeholder: add a verified amendment summary here.", "official_source": "https://www.incometax.gov.in/"},
    {"topic": "GST update", "published_date": "Replace with verified date", "effective_date": "Verify applicability", "summary": "Demo placeholder: add a verified GST notification summary here.", "official_source": "https://www.gst.gov.in/"},
])

def load_csv(uploaded, fallback, label):
    if uploaded is None:
        return fallback.copy()
    try:
        df = pd.read_csv(uploaded)
        st.sidebar.success(f"{label} loaded")
        return df
    except Exception as e:
        st.sidebar.error(f"Could not read {label}: {e}")
        return fallback.copy()

st.sidebar.header("Data sources")
st.sidebar.write("Upload CSV files to replace the synthetic demo datasets. Keep the required column names.")
clients_file = st.sidebar.file_uploader("Clients CSV", type=["csv"], key="clients")
accounting_file = st.sidebar.file_uploader("Accounting records CSV", type=["csv"], key="accounting")
support_file = st.sidebar.file_uploader("Supporting records CSV", type=["csv"], key="support")
tasks_file = st.sidebar.file_uploader("Tasks CSV", type=["csv"], key="tasks")
reg_file = st.sidebar.file_uploader("Regulatory updates CSV", type=["csv"], key="reg")

clients = load_csv(clients_file, clients_demo, "Clients")
accounting = load_csv(accounting_file, accounting_demo, "Accounting records")
support = load_csv(support_file, support_demo, "Supporting records")
tasks = load_csv(tasks_file, tasks_demo, "Tasks")
regulations = load_csv(reg_file, reg_demo, "Regulatory updates")

required = {
    "Clients": (clients, ["client_id", "client_name"]),
    "Accounting records": (accounting, ["client_id", "reference", "amount"]),
    "Supporting records": (support, ["client_id", "reference", "amount"]),
    "Tasks": (tasks, ["client_id", "task", "status"]),
}
bad = []
for name, (df, cols) in required.items():
    missing = [c for c in cols if c not in df.columns]
    if missing:
        bad.append(f"{name}: missing columns {', '.join(missing)}")
if bad:
    st.error("Some uploaded files do not match the required format:\n\n" + "\n".join(f"- {x}" for x in bad))
    st.stop()

for df in (accounting, support):
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
for df in (accounting, support):
    if "reference" in df.columns:
        df["reference"] = df["reference"].astype(str).str.strip()
    df["client_id"] = df["client_id"].astype(str).str.strip()

clients["client_id"] = clients["client_id"].astype(str).str.strip()
client_lookup = clients.set_index("client_id")["client_name"].to_dict()

tab1, tab2, tab3, tab4 = st.tabs(["Client 360°", "Reconciliation", "Regulatory Intelligence", "Data Explorer"])

with tab1:
    st.subheader("Client 360° view")
    selected_id = st.selectbox(
        "Select client",
        options=clients["client_id"].tolist(),
        format_func=lambda x: f"{x} — {client_lookup.get(x, 'Unknown client')}"
    )
    client_row = clients[clients["client_id"] == selected_id].iloc[0]
    a = accounting[accounting["client_id"] == selected_id].copy()
    s = support[support["client_id"] == selected_id].copy()
    t = tasks[tasks["client_id"] == selected_id].copy()
    st.markdown(f"### {client_row.get('client_name', selected_id)}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accounting records", len(a))
    c2.metric("Supporting records", len(s))
    c3.metric("Open tasks", int((~t["status"].astype(str).str.lower().isin(["completed", "closed", "done"])).sum()))
    c4.metric("Accounting value", f"₹{a['amount'].fillna(0).sum():,.0f}")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Accounting records")
        st.dataframe(a, use_container_width=True, hide_index=True)
    with right:
        st.markdown("#### Tasks and follow-ups")
        st.dataframe(t, use_container_width=True, hide_index=True)
    st.caption("A real implementation would connect permitted sources and apply access controls; this prototype uses CSV imports.")

with tab2:
    st.subheader("Cross-source reconciliation")
    st.write("Matches records by client ID and reference number, then compares amounts. Unmatched records and differences require human review.")
    keys = ["client_id", "reference"]
    a = accounting.copy()
    s = support.copy()
    merged = a.merge(s, on=keys, how="outer", suffixes=("_accounting", "_support"), indicator=True)
    merged["accounting_amount"] = merged.get("amount_accounting")
    merged["supporting_amount"] = merged.get("amount_support")
    merged["difference"] = merged["accounting_amount"] - merged["supporting_amount"]
    def status(row):
        if row["_merge"] == "left_only":
            return "No supporting record matched"
        if row["_merge"] == "right_only":
            return "No accounting record matched"
        if pd.isna(row["accounting_amount"]) or pd.isna(row["supporting_amount"]):
            return "Amount missing"
        if abs(row["difference"]) > 0.01:
            return "Amount mismatch — review"
        return "Matched"
    merged["review_status"] = merged.apply(status, axis=1)
    display_cols = [c for c in ["client_id", "reference", "party_accounting", "document_name", "accounting_amount", "supporting_amount", "difference", "review_status"] if c in merged.columns]
    alerts = merged[merged["review_status"] != "Matched"].copy()
    m1, m2, m3 = st.columns(3)
    m1.metric("Records compared", len(merged))
    m2.metric("Need review", len(alerts))
    m3.metric("Matched", int((merged["review_status"] == "Matched").sum()))
    st.dataframe(merged[display_cols], use_container_width=True, hide_index=True)
    if len(alerts):
        st.warning(f"{len(alerts)} item(s) need review. A difference is not proof of an error or misconduct.")
        st.download_button("Download review queue CSV", alerts[display_cols].to_csv(index=False).encode("utf-8"), "secureca_review_queue.csv", "text/csv")

with tab3:
    st.subheader("Regulatory Intelligence")
    st.write("Prototype for tracking verified official updates and presenting a simple summary with a source link.")
    st.warning("The bundled entries are placeholders, not current legal advice. Replace them with verified notifications before presenting regulatory conclusions.")
    if "official_source" in regulations.columns:
        for _, r in regulations.iterrows():
            with st.container(border=True):
                st.markdown(f"**{r.get('topic', 'Regulatory update')}**")
                st.write(f"Published: {r.get('published_date', 'Not specified')}  |  Effective: {r.get('effective_date', 'Verify applicability')}")
                st.write(r.get("summary", "No summary supplied."))
                url = str(r.get("official_source", "")).strip()
                if url.startswith("https://"):
                    st.link_button("Open official source", url)
    else:
        st.error("Regulatory updates CSV must include an official_source column.")

with tab4:
    st.subheader("Imported data explorer")
    choice = st.selectbox("Choose dataset", ["Clients", "Accounting", "Supporting records", "Tasks", "Regulatory updates"])
    data_map = {"Clients": clients, "Accounting": accounting, "Supporting records": support, "Tasks": tasks, "Regulatory updates": regulations}
    st.dataframe(data_map[choice], use_container_width=True, hide_index=True)
    st.download_button("Download selected dataset as CSV", data_map[choice].to_csv(index=False).encode("utf-8"), f"{choice.lower().replace(' ', '_')}.csv", "text/csv")

st.divider()
st.caption("SecureCA academic MVP • Synthetic sample data • Not tax, accounting, or legal advice")
