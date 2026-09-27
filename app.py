"""Local explorer; Snowflake-backed pages are introduced in later solutions."""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parent / "data" / "generated"

st.set_page_config(page_title="Agentic Enterprise | Foundation", layout="wide")
st.title("The Agentic Enterprise: foundation")
st.caption("Fictional accounts and deterministic synthetic data · Solution 00")

if not (DATA / "accounts.csv").exists():
    st.info("Generate the dataset first: uv run generate-demo-data")
    st.stop()

accounts = pd.read_csv(DATA / "accounts.csv")
opportunities = pd.read_csv(DATA / "opportunities.csv")
invoices = pd.read_csv(DATA / "invoices.csv")
shipments = pd.read_csv(DATA / "shipments.csv")

chosen = st.selectbox("Account", accounts["account_name"])
account = accounts.loc[accounts["account_name"] == chosen].iloc[0]
aid = account["account_id"]
opp = opportunities.loc[opportunities["account_id"] == aid]
inv = invoices.loc[invoices["account_id"] == aid]
ship = shipments.loc[shipments["account_id"] == aid]

pipeline = int(opp.loc[opp["stage"] != "Closed Won", "amount_usd"].sum())
ar = int((inv["amount_usd"] - inv["paid_amount_usd"]).sum())
late = int((ship["status"] == "Late").sum())
c1, c2, c3 = st.columns(3)
c1.metric("Open pipeline", f"${pipeline:,.0f}")
c2.metric("Outstanding AR", f"${ar:,.0f}")
c3.metric("Late shipments", late)

st.subheader("Business relationships")
st.write(f"**{chosen}** is owned by sales rep `{account['sales_rep_id']}`. "
         "Opportunities, invoices, and shipments link to this Account through `account_id`.")
tabs = st.tabs(["Opportunities", "Invoices", "Shipments", "Ontology"])
for tab, frame in zip(tabs[:3], [opp, inv, ship]):
    with tab:
        st.dataframe(frame.drop(columns="account_id"), hide_index=True, use_container_width=True)
with tabs[3]:
    st.code((Path(__file__).parent / "ontology" / "entities.yaml").read_text(), language="yaml")
