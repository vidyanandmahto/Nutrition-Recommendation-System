# 🍎 Food Nutrition Clustering System using K-Means

## 📌 Project Overview

This project applies the **K-Means Clustering** algorithm to group foods with similar nutritional characteristics. By analyzing nutrients such as calories, protein, carbohydrates, fat, iron, and vitamin C, the model identifies meaningful food clusters that can be used in nutrition recommendation systems, diet planning applications, and health analytics.

The project demonstrates the complete Machine Learning workflow, including data preprocessing, feature scaling, optimal cluster selection, model training, evaluation, visualization, and interpretation.

---

## 📂 Dataset Information

- **Dataset:** Food Nutrition Dataset
- **Total Records:** 205
- **Total Features:** 9
- **Data Type:** Numerical + Categorical
- **Source:** USDA FoodData Central API

### Features

| Feature | Description |
|----------|-------------|
| food_name | Name of the food item |
| category | Food category |
| calories | Calories per 100g |
| protein | Protein (g) |
| carbs | Carbohydrates (g) |
| fat | Fat (g) |
| iron | Iron (mg) |
| vitamin_c | Vitamin C (mg) |

---

# 🎯 Problem Statement

Different foods contain different nutritional values. Instead of manually categorizing foods, Machine Learning can automatically identify groups of nutritionally similar foods.

This project clusters foods into different nutritional groups using K-Means Clustering, making it useful for:

- Nutrition Recommendation Systems
- Diet Planning
- Health Monitoring
- Food Analytics
- Fitness Applications

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

---

# 📊 Machine Learning Workflow

1. Import Libraries
2. Load Dataset
3. Data Exploration
4. Data Cleaning
5. Handle Missing Values
6. Remove Duplicate Records
7. Feature Selection
8. Feature Scaling using StandardScaler
9. Elbow Method
10. Silhouette Score
11. K-Means Clustering
12. Cluster Visualization
13. Cluster Analysis
14. Save Clustered Dataset

---

# 📈 Data Visualization

The project includes:

- Elbow Method Graph
- Cluster Scatter Plot
- Pair Plot
- Cluster-wise Nutritional Analysis

---

# 🤖 Machine Learning Algorithm

## K-Means Clustering

K-Means is an unsupervised machine learning algorithm that groups similar data points into clusters based on feature similarity.

### Steps

- Initialize cluster centroids
- Assign data points to the nearest centroid
- Update centroids
- Repeat until convergence

---

# 📏 Model Evaluation

The optimal number of clusters was determined using:

- Elbow Method
- Silhouette Score

---

# 📁 Project Structure

```
Food-Nutrition-Clustering-System/
│
├── dataset/
│   └── Food_Nutrition_Dataset.csv
│
├── notebook/
│   └── Food_Nutrition_Clustering.ipynb
│
├── output/
│   ├── Food_Nutrition_Clustered.csv
│   ├── elbow_plot.png
│   ├── scatter_plot.png
│   └── pair_plot.png
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Food-Nutrition-Clustering-System.git
```

Go to the project directory

```bash
cd Food-Nutrition-Clustering-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the notebook

```bash
jupyter notebook
```

---

# 📌 Results

- Successfully clustered food items based on nutritional values.
- Identified similar foods using unsupervised learning.
- Visualized clusters using scatter plots.
- Evaluated clustering performance using Elbow Method and Silhouette Score.

---

# 📚 Future Improvements

- Build a Nutrition Recommendation Web App
- Deploy using Flask or Streamlit
- Add PCA for better visualization
- Integrate Deep Learning-based Recommendation Systems
- Use larger nutrition datasets
- Deploy the model on cloud platforms

---

# 👨‍💻 Author

**Vidyanand Mahto**

Engineering Student | Data Science Enthusiast | Machine Learning Learner

---

## ⭐ If you found this project useful, consider giving it a star!