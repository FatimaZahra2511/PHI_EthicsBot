
# EthicsBot — Operationalizing Luciano Floridi’s *The Ethics of Information* (21st Century)

EthicsBot is an AI agent that provides **ethical guidance for AI, digital systems, and data-driven design**, grounded *exclusively* in Luciano Floridi’s 21st-century philosophical framework: **Information Ethics**.

Unlike generic chatbots, EthicsBot does **not invent answers** and does **not hallucinate**.  
Instead, it retrieves structured knowledge from a dataset manually built from Floridi’s book:

 *Luciano Floridi — The Ethics of Information* (2013)

---

##  What EthicsBot can do
EthicsBot answers questions such as:

> *Is it ethical for an AI system to collect personal data without consent?*  
> *Can an AI be responsible for harm even if it has no intentions?*

For each question, EthicsBot provides:

| Output | Description |
|--------|-------------|
| **Theme** | Philosophical category (e.g., consent, identity, governance) |
| **Claim** | Paraphrased insight from Floridi |
| **Direct Quote** | Short citation from the book |
| **Page Reference** | Page number(s) for verification |
| **Design Guideline** | Practical advice for AI / UX / data engineers |
| **Page Snapshot** | Preview of the cited page from the book |

---

##  Project Goal
To **turn philosophical theory into actionable design ethics** for developers, engineers, and policymakers.

EthicsBot shows that philosophy is not abstract — it can directly inform **responsible AI development**.

---

##  Architecture
- **Python**
- **Streamlit UI**
- **TF-IDF + Cosine similarity** retrieval
- **Custom dataset built from Floridi’s book**
- **Local search only — NO external AI models / NO internet needed**

##  Live Deployment

The AI agent is deployed on Streamlit Cloud and can be used directly:

 **https://phiethicsbot-dvb8sjpreozlck4y54537x.streamlit.app/**

No installation required — open the link and ask any ethical question related to AI, data, and digital systems.

 Features in the live demo:
- Grounded answers with philosophical themes
- Direct quotes from Floridi’s *The Ethics of Information*
- Page references + book page snapshot
- Design guidelines for engineers
- Export of all Q&A pairs from the session


