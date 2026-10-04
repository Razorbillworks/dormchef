# 🍳 DormChef: Midnight Pantry Rescue

An offline-first, local culinary assistant built specifically for college hostel living. It solves a late-night problem for my roommate, **Abhishek**: turning random room snacks and pantry scraps into realistic, high-protein meals using only a kettle or sandwich toaster.

Built for the **[Hacktoberfest 2026: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)** Weekend DEV Challenge.

---

## 📸 Interface & Live Generation

![DormChef Interface](screenshot-ui.png)
*Configuring pantry items, selecting appliances, and defining macro goals.*

![DormChef Recipe Output](screenshot-recipe.png)
*Real-time token streaming recipe with built-in appliance safety rules.*

---

## 🎯 The Motivation: Why Abhishek Needed This

Abhishek is an engineering student and gym regular who tracks his daily protein intake. In our hostel, dinner closes early, and after late-night study sessions, food options are bleak. Ordering takeout is either too expensive or terrible for nutrition, leaving him with whatever items are in our cupboard (eggs, bread, oats, peanut butter).

Our cooking setup is strictly limited:
- An electric kettle
- A dual-plate sandwich press / toaster

Most online recipe apps assume an oven, a 4-burner stovetop, and whole groceries. Standard cloud LLMs frequently give dangerous suggestions—like telling someone to crack raw eggs or fry butter directly onto exposed electric kettle coils, which burns out the appliance and causes hostel inspection fines. 

DormChef acts as a guardrailed assistant that translates room scraps into edible food while adhering strictly to dorm hardware limitations.

---

## 💡 Why Open Innovation Matters Here

- **Hostel Wi-Fi Independence:** Campus Wi-Fi in our block frequently drops or throttles past midnight. Because DormChef runs locally via Ollama, it functions 100% offline.
- **Zero Cost for Students:** College students cannot justify $20/month proprietary AI subscriptions or pay-per-token API fees to cook midnight eggs. Open-weight models level the playing field.
- **Edge Sovereignty & Custom Guardrails:** Running Google's Gemma 2 (2B) locally allows fine-grained system steering. We strictly forbid bare-coil kettle frying (enforcing water-bath poaching or mug steeping) and require sandwich press lining to avoid burnt-on messes.

---

## 🛠️️ Architecture & Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Foundation Model** | `Google Gemma 2 (2B)` | Open-weight edge reasoning model |
| **Inference Engine** | `Ollama` | Local background inference runtime |
| **Frontend UI** | `Streamlit` | Editorial slip layout with live token streaming |
| **Development** | `GitHub Copilot` | Scaffolding regex allergen filtering and UI logic |

### Prize Categories Entered
- **Best Use of Gemma** ($200 Featured Category): Running Google's open-weight Gemma 2 locally on consumer hardware.
- **Best Use of GitHub Copilot** ($100 Partner Category): Used to scaffold boilerplate, regex parsers, and Streamlit components.

---

## ⚙️ Local Setup Guide

### 1. Prerequisites
- [Ollama installed](https://ollama.com/)
- Python 3.10+

### 2. Pull the Open-Weight Model
Run this in your terminal:
```bash
ollama run gemma2:2b
