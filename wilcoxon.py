# Wilcoxon matched-pairs signed-rank test

from scipy.stats import wilcoxon
import pandas as pd

pair = pd.read_csv("surveys/pair_agree.csv")
pair = pair[pair["ResponseId"].notna()]
pre = []
post = []

for i, row in pair.iterrows():
    if i % 2 == 0:
        pre.append(row)
    else:
        post.append(row)

pre = pd.DataFrame(pre)
post = pd.DataFrame(post)

like_qs = [
    "Q23_1","Q23_2","Q23_3","Q23_4","Q23_5","Q23_6","Q23_7","Q23_8","Q25_1","Q25_2","Q25_3"
]

con_qs = [
    "Q24_1.1","Q24_2.1","Q24_3.1","Q24_4"
]

qs = like_qs + con_qs

# map scales to numeric
likert_map = {
    "Strongly disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly agree": 5
}

confidence_map = {
    "Not at all confident": 1,
    "Slightly confident": 2,
    "Somewhat confident": 3,
    "Fairly confident": 4,
    "Completely confident": 5
}

for q in like_qs:
    pre[q] = pre[q].map(likert_map)
    post[q] = post[q].map(likert_map)

for q in con_qs:
    pre[q] = pre[q].map(confidence_map)
    post[q] = post[q].map(confidence_map)

results = []

# wilcoxon
for q in qs:
    paired = pd.DataFrame({
        "pre": pre[q].values,
        "post": post[q].values
    }).dropna() # drops empty rows

    stat, p = wilcoxon(paired["pre"], paired["post"])

    results.append({
        "Question": q,
        "W statistic": stat,
        "p-value": p,
        "N": len(paired) # sample size
    })

results_df = pd.DataFrame(results)

print(results_df)

# results_df.to_csv("wilcoxon_results.csv", index=False) # save to csv