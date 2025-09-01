
import json, re
import streamlit as st
from pathlib import Path
from mock_apis import initiate_payment, confirm_payment, update_policy, send_email, schedule_callback
from nlu import detect_intent, extract_time

page_bg = """
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364); /* blue gradient */
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🧠 GenAI Policy Payment Reminder")

data_path = Path(__file__).parent / "data" / "customers.json"
customers = json.loads(Path(data_path).read_text())["customers"]
names = [f'{c["name"]} (ID: {c["customerId"]})' for c in customers]
choice = st.selectbox("Select a mock customer:", names, index=0)
customer = customers[names.index(choice)]

if "history" not in st.session_state:
    st.session_state.history = []

def bot_say(txt): st.session_state.history.append(("bot", txt))
def user_say(txt): st.session_state.history.append(("user", txt))

def list_policies(cust):
    if len(cust["policies"]) == 1:
        p = cust["policies"][0]
        return f'Your payment of ₹{p["amountDue"]} for Policy {p["policyNumber"]} is due. Pay now or later?'
    else:
        lines = ["You have pending policies:"]
        for p in cust["policies"]:
            lines.append(f'- {p["policyNumber"]} ₹{p["amountDue"]} due.')
        lines.append("Reply with policy number like POL12345.")
        return "\n".join(lines)

if st.button("Start Conversation"):
    st.session_state.history = []
    bot_say(f'Hello {customer["name"]}, this is a reminder about your policy payments.')
    bot_say(list_policies(customer))

prompt = st.chat_input("Type your reply…")
if prompt:
    user_say(prompt)
    intent = detect_intent(prompt)
    selected = None
    m = re.findall(r"(POL\d{5})", prompt.upper())
    if m:
        for p in customer["policies"]:
            if p["policyNumber"] == m[0]:
                selected = p
    if selected: st.session_state.selected_policy = selected
    selected = st.session_state.get("selected_policy", None) or (customer["policies"][0] if len(customer["policies"])==1 else None)

    if intent == "CHOOSE_POLICY":
        bot_say(f"Proceeding with policy {selected['policyNumber']}. Pay now or later?")
    elif intent == "PAY_NOW":
        if not selected:
            bot_say("Please mention a policy number.")
        else:
            resp = initiate_payment(customer["customerId"], selected["policyNumber"], selected["amountDue"])
            bot_say(f"Payment link: {resp['paymentLink']}")
            conf = confirm_payment(resp["paymentId"], selected["policyNumber"])
            if conf["status"] == "SUCCESS":
                update_policy(customer["customerId"], selected["policyNumber"], "Paid")
                send_email(customer["email"], f"Policy {selected['policyNumber']}", "Document sent.", f"{selected['policyNumber']}.pdf")
                bot_say(f"Payment confirmed. Document emailed to {customer['email']}.")
            else:
                bot_say("Payment failed. Try again later.")
    elif intent == "PAY_LATER":
        iso_time = extract_time(prompt)
        resp = schedule_callback(customer["customerId"], selected["policyNumber"], iso_time)
        if resp["status"] == "Scheduled":
            bot_say(f"Callback scheduled for {iso_time}.")
    elif intent == "NOT_INTERESTED":
        bot_say("Okay, will not remind again. Thank you!")
    else:
        bot_say("Sorry, I didn’t get that. Pay now, later, or mention a policy number.")

for role, msg in st.session_state.history:
    with st.chat_message("assistant" if role=="bot" else "user"):
        st.markdown(msg)
