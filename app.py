from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
import os

app = Flask(__name__)

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), r"C:\Users\Lenovo\Desktop\Data Science Training\ML\unsupervised_ML\project\Nutrition recommendation system\Data\Food_Nutrition_Dataset.csv")

FEATURES = ["calories", "protein", "carbs", "fat", "iron", "vitamin_c"]
ENGINEERED_FEATURES = FEATURES + [
    "protein_per_cal", "carb_per_cal", "fat_per_cal", "micronutrient_score"
]

CLUSTER_LABELS = {
    0: "High-Calorie Dense Foods",
    1: "Vitamin-Rich Foods",
    2: "High-Protein Dense Foods",
    3: "Balanced Light Foods",
}

CLUSTER_ICONS = {0: "🔥", 1: "🥦", 2: "💪", 3: "⚖️"}
CLUSTER_DESC = {
    0: "Energy-dense foods high in calories and fats. Great for bulking or high-activity days.",
    1: "Low-fat foods packed with Vitamin C and micronutrients. Perfect for immunity & health.",
    2: "Protein-rich foods that support muscle growth and recovery.",
    3: "Low-calorie, well-rounded foods ideal for weight management and everyday eating.",
}

GOAL_MAP = {
    "weight_loss":  {"label": "Weight Loss",   "icon": "⚖️",  "cluster": None, "sort": "calories",  "asc": True},
    "muscle_gain":  {"label": "Muscle Gain",   "icon": "💪",  "cluster": None, "sort": "protein",   "asc": False},
    "vitamin_rich": {"label": "Vitamin Rich",  "icon": "🥦",  "cluster": 1,    "sort": None,        "asc": None},
    "balanced":     {"label": "Balanced",      "icon": "🍱",  "cluster": 3,    "sort": None,        "asc": None},
    "high_protein": {"label": "High Protein",  "icon": "🥩",  "cluster": 2,    "sort": None,        "asc": None},
    "high_energy":  {"label": "High Energy",   "icon": "🔥",  "cluster": 0,    "sort": None,        "asc": None},
}

# ─────────────────────────────────────────
# LOAD & TRAIN  (once at startup)
# ─────────────────────────────────────────
def build_model():
    df = pd.read_csv(r"C:\Users\Lenovo\Desktop\Data Science Training\ML\unsupervised_ML\project\Nutrition recommendation system\Data-clean_tool\Food_Nutrition_Clustered_Enhanced.csv")
    df = df.drop_duplicates()
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    df["protein_per_cal"]     = df["protein"]  / (df["calories"] + 1)
    df["carb_per_cal"]        = df["carbs"]    / (df["calories"] + 1)
    df["fat_per_cal"]         = df["fat"]      / (df["calories"] + 1)
    df["micronutrient_score"] = df["iron"] * 2 + df["vitamin_c"] * 0.1

    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(df[ENGINEERED_FEATURES])

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=20, max_iter=500)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    return df, scaler, kmeans

DF, SCALER, MODEL = build_model()
CATEGORIES = sorted(DF["category"].unique().tolist())

# ─────────────────────────────────────────
# RECOMMENDATION LOGIC
# ─────────────────────────────────────────
def get_recommendations(goal, max_calories=None, min_protein=None,
                        exclude_categories=None, top_n=10):
    filtered = DF.copy()
    if max_calories:
        filtered = filtered[filtered["calories"] <= float(max_calories)]
    if min_protein:
        filtered = filtered[filtered["protein"] >= float(min_protein)]
    if exclude_categories:
        filtered = filtered[~filtered["category"].isin(exclude_categories)]

    cfg = GOAL_MAP[goal]

    # Dynamic sort-based goals
    if cfg["sort"]:
        result = (filtered.nsmallest(top_n, cfg["sort"]) if cfg["asc"]
                  else filtered.nlargest(top_n, cfg["sort"]))
    else:
        # Cluster-based: rank by centroid distance
        target = cfg["cluster"]
        cluster_foods = filtered[filtered["Cluster"] == target].copy()
        if cluster_foods.empty:
            return []
        centroid = MODEL.cluster_centers_[target]
        eng = cluster_foods[FEATURES].assign(
            protein_per_cal    = cluster_foods["protein"] / (cluster_foods["calories"] + 1),
            carb_per_cal       = cluster_foods["carbs"]   / (cluster_foods["calories"] + 1),
            fat_per_cal        = cluster_foods["fat"]     / (cluster_foods["calories"] + 1),
            micronutrient_score= cluster_foods["iron"] * 2 + cluster_foods["vitamin_c"] * 0.1,
        )[ENGINEERED_FEATURES]
        dists = np.linalg.norm(SCALER.transform(eng) - centroid, axis=1)
        cluster_foods["dist"] = dists
        result = cluster_foods.nsmallest(top_n, "dist")

    records = []
    for _, row in result.iterrows():
        records.append({
            "food_name": row["food_name"],
            "category":  row["category"],
            "calories":  round(row["calories"], 1),
            "protein":   round(row["protein"],  1),
            "carbs":     round(row["carbs"],    1),
            "fat":       round(row["fat"],      1),
            "iron":      round(row["iron"],     2),
            "vitamin_c": round(row["vitamin_c"],1),
            "cluster":   int(row["Cluster"]),
            "cluster_label": CLUSTER_LABELS[int(row["Cluster"])],
        })
    return records


def predict_food(calories, protein, carbs, fat, iron, vitamin_c):
    new = pd.DataFrame([{
        "calories": calories, "protein": protein, "carbs": carbs,
        "fat": fat, "iron": iron, "vitamin_c": vitamin_c
    }])
    new["protein_per_cal"]     = new["protein"]  / (new["calories"] + 1)
    new["carb_per_cal"]        = new["carbs"]    / (new["calories"] + 1)
    new["fat_per_cal"]         = new["fat"]      / (new["calories"] + 1)
    new["micronutrient_score"] = new["iron"] * 2 + new["vitamin_c"] * 0.1

    scaled  = SCALER.transform(new[ENGINEERED_FEATURES])
    cluster = int(MODEL.predict(scaled)[0])

    # Top 5 similar foods
    similar_df = DF[DF["Cluster"] == cluster].copy()
    centroid   = MODEL.cluster_centers_[cluster]
    eng = similar_df[FEATURES].assign(
        protein_per_cal    = similar_df["protein"] / (similar_df["calories"] + 1),
        carb_per_cal       = similar_df["carbs"]   / (similar_df["calories"] + 1),
        fat_per_cal        = similar_df["fat"]     / (similar_df["calories"] + 1),
        micronutrient_score= similar_df["iron"] * 2 + similar_df["vitamin_c"] * 0.1,
    )[ENGINEERED_FEATURES]
    similar_df["dist"] = np.linalg.norm(SCALER.transform(eng) - scaled, axis=1)
    top5 = similar_df.nsmallest(5, "dist")[["food_name", "category"] + FEATURES]

    return {
        "cluster":       cluster,
        "cluster_label": CLUSTER_LABELS[cluster],
        "cluster_icon":  CLUSTER_ICONS[cluster],
        "cluster_desc":  CLUSTER_DESC[cluster],
        "similar": [
            {"food_name": r["food_name"], "category": r["category"],
             "calories": round(r["calories"],1), "protein": round(r["protein"],1)}
            for _, r in top5.iterrows()
        ]
    }


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────
@app.route("/")
def index():
    stats = {
        "total_foods": len(DF),
        "total_categories": DF["category"].nunique(),
        "cluster_counts": {
            CLUSTER_LABELS[c]: int(n)
            for c, n in DF["Cluster"].value_counts().sort_index().items()
        }
    }
    return render_template("index.html", stats=stats, goals=GOAL_MAP,
                           categories=CATEGORIES)


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    # GET — pre-select goal from query string (e.g. clicked from home page)
    if request.method == "GET":
        goal     = request.args.get("goal", "balanced")
        max_cal  = request.args.get("max_calories") or None
        min_prot = request.args.get("min_protein") or None
        top_n    = int(request.args.get("top_n", 10))
        excl     = request.args.getlist("exclude_categories")
    else:
        goal     = request.form.get("goal", "balanced")
        max_cal  = request.form.get("max_calories") or None
        min_prot = request.form.get("min_protein") or None
        top_n    = int(request.form.get("top_n", 10))
        excl     = request.form.getlist("exclude_categories")

    # Always run recommendation so results show immediately
    results   = get_recommendations(goal, max_cal, min_prot, excl, top_n)
    goal_info = GOAL_MAP[goal]
    return render_template("results.html", results=results,
                           goal=goal, goal_info=goal_info,
                           max_calories=max_cal, min_protein=min_prot,
                           top_n=top_n, categories=CATEGORIES,
                           goals=GOAL_MAP, exclude_categories=excl)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    result = None
    if request.method == "POST":
        try:
            result = predict_food(
                float(request.form["calories"]),
                float(request.form["protein"]),
                float(request.form["carbs"]),
                float(request.form["fat"]),
                float(request.form["iron"]),
                float(request.form["vitamin_c"]),
            )
        except Exception as e:
            result = {"error": str(e)}
    return render_template("predict.html", result=result, goals=GOAL_MAP)


@app.route("/explore")
def explore():
    cluster_filter = request.args.get("cluster", "all")
    category_filter = request.args.get("category", "all")
    search = request.args.get("search", "").strip().lower()

    data = DF.copy()
    if cluster_filter != "all":
        data = data[data["Cluster"] == int(cluster_filter)]
    if category_filter != "all":
        data = data[data["category"] == category_filter]
    if search:
        data = data[data["food_name"].str.lower().str.contains(search)]

    foods = []
    for _, row in data.iterrows():
        foods.append({
            "food_name":     row["food_name"],
            "category":      row["category"],
            "calories":      round(row["calories"], 1),
            "protein":       round(row["protein"],  1),
            "carbs":         round(row["carbs"],    1),
            "fat":           round(row["fat"],      1),
            "iron":          round(row["iron"],     2),
            "vitamin_c":     round(row["vitamin_c"],1),
            "cluster":       int(row["Cluster"]),
            "cluster_label": CLUSTER_LABELS[int(row["Cluster"])],
            "cluster_icon":  CLUSTER_ICONS[int(row["Cluster"])],
        })

    return render_template("explore.html", foods=foods,
                           cluster_labels=CLUSTER_LABELS,
                           cluster_icons=CLUSTER_ICONS,
                           categories=CATEGORIES,
                           goals=GOAL_MAP,
                           selected_cluster=cluster_filter,
                           selected_category=category_filter,
                           search=search)


if __name__ == "__main__":
    app.run(debug=True)
