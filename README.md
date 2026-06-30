# 🥗 NutriAI — Nutrition Recommendation System

An unsupervised machine learning web application that clusters foods by nutritional profile and recommends them based on your health goals.

Built with **KMeans Clustering** + **Flask** + **HTML/CSS**.

---

## 🚀 Live Demo

> Run locally by following the setup instructions below.

---

## 📸 Screenshots

| Home | Recommend | Predict | Explore |
|------|-----------|---------|---------|
| Cluster overview & health goals | Filter by goal, calories, protein | Enter nutrients → get cluster | Search & browse all 205 foods |

---

## 🧠 How It Works

1. **Data** — 205 foods across 61 categories with 6 nutritional features: `calories`, `protein`, `carbs`, `fat`, `iron`, `vitamin_c`
2. **Feature Engineering** — 4 derived ratio features added: `protein_per_cal`, `carb_per_cal`, `fat_per_cal`, `micronutrient_score`
3. **Scaling** — `RobustScaler` used to handle outliers better than StandardScaler
4. **Clustering** — KMeans (k=4) trained using 3 evaluation metrics: Silhouette Score, Davies–Bouldin Index, Calinski–Harabász Index
5. **Recommendation** — Foods ranked by distance to cluster centroid for most representative results

### 🔵 The 4 Food Clusters

| Cluster | Label | Description |
|---------|-------|-------------|
| 0 | 🔥 High-Calorie Dense | Energy-dense foods high in calories and fats |
| 1 | 🥦 Vitamin-Rich | Low-fat, high Vitamin C and micronutrient foods |
| 2 | 💪 High-Protein Dense | Protein-packed foods for muscle support |
| 3 | ⚖️ Balanced Light | Low-calorie, well-rounded everyday foods |

---

## ✨ Features

- **🏠 Home** — Cluster overview, stats, and quick goal shortcuts
- **🍽️ Recommend** — Filter by health goal, max calories, min protein, and exclude categories
- **🔬 Predict** — Enter any food's nutrients and classify it into a cluster with similar food suggestions
- **🔎 Explore** — Searchable, filterable table of all 205 foods with cluster labels

### 6 Health Goals Supported
| Goal | Logic |
|------|-------|
| ⚖️ Weight Loss | Lowest calorie foods across all clusters |
| 💪 Muscle Gain | Highest protein foods across all clusters |
| 🥦 Vitamin Rich | Closest foods to Cluster 1 centroid |
| 🍱 Balanced | Closest foods to Cluster 3 centroid |
| 🥩 High Protein | Closest foods to Cluster 2 centroid |
| 🔥 High Energy | Closest foods to Cluster 0 centroid |

---

## 🗂️ Project Structure

```
NUTRITION RECOMMENDATION SYSTEM/
│
├── Data/
│   ├── Food_Nutrition_Dataset.csv        # Original dataset
│   └── Food_Nutrition_Clustered.csv      # Dataset with cluster labels
│
├── Data-clean-tool/
│   ├── Food_Nutrition_...                # Data cleaning scripts
│   └── Nutrition_Reco...                 # EDA & exploration notebooks
│
├── Model/                                # Saved model artifacts
│
├── static/
│   ├── css/
│   │   └── style.css                     # Dark theme responsive CSS
│   └── js/
│       └── main.js                       # Animations, live search, quick-fill
│
├── templates/
│   ├── base.html                         # Shared navbar, footer, layout
│   ├── index.html                        # Home page
│   ├── results.html                      # Recommendations page
│   ├── predict.html                      # Predict cluster page
│   └── explore.html                      # Browse all foods page
│
├── app.py                                # Flask app — routes & ML logic
├── requirements.txt                      # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/nutrition-recommendation-system.git
cd nutrition-recommendation-system
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

---

## 📦 Dependencies

```
flask>=3.0.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
```

---

## 📊 Dataset

- **Source:** Food Nutrition Dataset (CSV)
- **Size:** 205 foods, 8 columns
- **Features:** `food_name`, `category`, `calories`, `protein`, `carbs`, `fat`, `iron`, `vitamin_c`
- **Missing values:** Filled with column median
- **Duplicates:** Removed before training

---

## 🤖 ML Details

| Parameter | Value |
|-----------|-------|
| Algorithm | KMeans |
| Clusters (k) | 4 |
| Scaler | RobustScaler |
| Features | 10 (6 raw + 4 engineered) |
| `n_init` | 20 |
| `max_iter` | 500 |
| `random_state` | 42 |

### Evaluation Metrics (k=4)
| Metric | Score |
|--------|-------|
| Silhouette Score | 0.3071 |
| Davies–Bouldin Index | 1.2978 |
| Calinski–Harabász | 62.13 |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| ML | scikit-learn, pandas, numpy |
| Frontend | HTML5, CSS3, Vanilla JS |
| Fonts | Google Fonts (Inter) |
| Theme | Custom dark theme |

---

## 🙋 Author

**Your Name**
- GitHub: https://github.com/vidyanandmahto
- LinkedIn: https://www.linkedin.com/in/vidyanand-mahto-b9a283301/

---

## 📄 License

This project is licensed under the MIT License

---

> ⭐ If you found this project helpful, please consider giving it a star!