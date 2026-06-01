from scipy.stats import kendalltau
import pandas as pd
import itertools

pre = pd.read_csv("surveys/pre.csv", skiprows=[1,2])
post = pd.read_csv("surveys/post.csv", skiprows=[1,2])

# likert questions
like_qs = [
    "Q23_1","Q23_2","Q23_3","Q23_4","Q23_5","Q23_6","Q23_7","Q23_8","Q25_1","Q25_2","Q25_3"
]

# confidence questions
con_qs = [ 
    "Q24_1","Q24_2","Q24_3","Q24_4"
] 

q11_qs = [
    "Q11_1", "Q11_2", "Q11_3", "Q11_4", "Q11_5", "Q11_6", "Q11_7"
]

pre_qs = like_qs + con_qs 
post_qs = like_qs + con_qs + q11_qs

# remove incomplete rows
pre = pre.dropna(subset=pre_qs)
post = post.dropna(subset=post_qs)

# map scales to numeric
likert_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
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

for q in q11_qs:
    post[q] = post[q].map(likert_map)

pre_results = []
post_results = []

# kendall - pre
for q1, q2 in itertools.combinations(pre_qs, 2): # unique combinations without duplicates

    paired_pre = pd.DataFrame({
        "x": pre[q1],
        "y": pre[q2]
    }).dropna() # drop empty row

    tau, p = kendalltau(paired_pre["x"], paired_pre["y"])

    pre_results.append({
        "Question 1": q1,
        "Question 2": q2,
        "Tau-b": tau,
        "p-value": p,
        "N": len(paired_pre)
    })

results_pre = pd.DataFrame(pre_results)

print("PRE")
print(results_pre)
print("-------------------------\n")

# kendall - post
for q1, q2 in itertools.combinations(post_qs, 2): # unique combinations without duplicates

    paired_post = pd.DataFrame({
        "x": post[q1],
        "y": post[q2]
    }).dropna() # drop empty row

    tau, p = kendalltau(paired_post["x"], paired_post["y"])

    post_results.append({
        "Question 1": q1,
        "Question 2": q2,
        "Tau-b": tau,
        "p-value": p,
        "N": len(paired_post)
    })

results_post = pd.DataFrame(post_results)

print("POST")
print(results_post)

# export to csv
results_pre.to_csv("kendall_pre.csv", index=False)
results_post.to_csv("kendall_post.csv", index=False)
