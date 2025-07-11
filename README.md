# 🔔 GitHub Actions Webhook Tracker

This project is a **GitHub Webhook Integration System** built with Flask and MongoDB, designed to track and display events from a connected GitHub repository in real-time.

It captures three key GitHub actions:
- ✅ `Push`
- ✅ `Pull Request`
- ✅ `Merge`

These events are received via a webhook endpoint, stored in MongoDB, and displayed in a clean, minimalistic frontend that auto-updates every 15 seconds.

---

## 🚀 Demo

![UI Screenshot](screenshot.png) <!-- Add a screenshot of your final UI here -->

Live site: [https://your-render-url.onrender.com](https://your-render-url.onrender.com)

---

## 📦 Repositories Used

- **action-repo** → The GitHub repo where push/pull/merge triggers happen.
- **webhook-repo** → This repo. Hosts the Flask app + MongoDB backend + UI.

---

## 🧠 Tech Stack

- **Backend:** Python (Flask), MongoDB (Atlas)
- **Frontend:** HTML, TailwindCSS, JavaScript (Axios)
- **Deployment:** Render.com
- **Webhook:** GitHub → `/webhook` endpoint

---


