# 🧠 GenAI Policy Payment Reminder Assistant

This is a prototype project for a **GenAI-powered automated policy payment reminder assistant**, built as part of an interview case study.

The assistant can:
- Remind customers about pending insurance policy payments.  
- Handle **Pay Now**, **Pay Later**, and **Not Interested** flows.  
- Demonstrate integration with mocked APIs (Payment, Confirmation, Policy Portal Update, Email, Scheduler).  

⚡ The goal: **Show working prototype + approach**, not production-ready code.

---

## 🚀 Demo Features

✅ **Chat-style UI** using Streamlit  
✅ **Mock Customers & Policies** (JSON data)  
✅ **Intents supported**:  
   - *Pay Now* → generates payment link, simulates confirmation, updates policy, emails document  
   - *Pay Later* → schedules a reminder callback (mocked)  
   - *Not Interested* → closes politely  
✅ **Multiple Policies** → user can pick which one to pay (e.g., `POL12345`)  
✅ **Architecture Diagram** included (`architecture.png`)  

---

## 📂 Project Structure

