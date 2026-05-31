import pandas as pd

pre = pd.read_csv("surveys/pre_raw.csv", skiprows=[1])
post = pd.read_csv("surveys/post_raw.csv", skiprows=[1])

FIRST = "RecipientFirstName"
LAST = "RecipientLastName"

for df in [pre, post]:
    df[FIRST] = df[FIRST].str.strip()
    df[LAST] = df[LAST].str.strip()

def get_name(list, index):
    first = ""
    last = ""

    if pd.notna(list[FIRST][index]):
        first = list[FIRST][i].strip()
        
    if pd.notna(list[LAST][index]):
        last = list[LAST][i].strip() 

    name = first + " " + last
    return name

index = {}
for i in range(len(pre)):
    name = get_name(pre, i)
    index[name] = i

matched = {}
unmatched_post = []
unmatched_pre = []

# unmatched post
for i in range(len(post)):
    name = get_name(post, i)
    if name in index:
        matched[name] = (index[name], i)
    else:
        unmatched_post.append(i)

# unmatched pre
for i in range(len(pre)):
    name = get_name(pre, i)
    if name not in matched:
        unmatched_pre.append(i)

# print matched pairs
for name, (pre_i, post_i) in matched.items():
    print(pre[pre_i:pre_i+1])
    print(post[post_i:post_i+1])
    print("\n")
 
# print unmatched
print("------ Unmatched Pre ------")
for i in unmatched_pre:
    print(pre[i:i+1])
 
print("\n------ Unmatched Post ------")
for i in unmatched_post:
    print(post[i:i+1])

# save CSV
rows = []
for name, (pre_i, post_i) in matched.items():
    rows.append(pre[pre_i:pre_i+1])
    rows.append(post[post_i:post_i+1])
    rows.append(pd.DataFrame([{}]))

rows.append(pd.DataFrame([{}]))
for i in unmatched_pre:
    rows.append(pre[i:i+1])

rows.append(pd.DataFrame([{}]))
for i in unmatched_post:
    rows.append(post[i:i+1])

pd.concat(rows).to_csv("pair_output.csv", index=False)
