import streamlit as st
import itertools

# 関数定義部分（元のコードから変更なし）
def get_details(w1, w2, k=None, vict=None):
    details = ["真" if i != vict else "" for i in range(4)]
    details[2] += "真"
    if k is not None:
        details[k] += "狂"
    details[w1] += "狼"
    details[w2] += "狼"
    details_string = []
    for s in details:
        for x in s:
            details_string.append(x)
    return details_string

# 全パターンリストの作成（元のコードから変更なし）
banmen = [1, 1, 2, 1]
results = {}
for vict in range(4):
    for k in range(4):
        for w1 in range(4):
            for w2 in range(w1, 4):
                banmen[vict] -= 1
                banmen[k] += 1
                banmen[w1] += 1
                banmen[w2] += 1
                banmen_string = "-".join(list(map(str, banmen)))
                details_string = get_details(w1, w2, k, vict)
                if banmen_string not in results:
                    results[banmen_string] = [details_string]
                else:
                    results[banmen_string].append(details_string)
                banmen = [1, 1, 2, 1]
for w1 in range(4):
    for w2 in range(w1, 4):
        banmen[w1] += 1
        banmen[w2] += 1
        banmen_string = "-".join(list(map(str, banmen)))
        details_string = get_details(w1, w2)
        if banmen_string not in results:
            results[banmen_string] = [details_string]
        else:
            results[banmen_string].append(details_string)
        banmen = [1, 1, 2, 1]

# Streamlit部分の設定
st.title("人狼ゲームシミュレーション")


# forループで変数を動的に作成
col1_1, col1_2, col1_3, col1_4, col1_5 = st.columns(5)
col2_1, col2_2, col2_3, col2_4, col2_5 = st.columns(5)
col3_1, col3_2, col3_3, col3_4, col3_5 = st.columns(5)
col4_1, col4_2, col4_3, col4_4, col4_5 = st.columns(5)
col5_1, col5_2, col5_3, col5_4, col5_5 = st.columns(5)
col6_1, col6_2, col6_3, col6_4, col6_5 = st.columns(5)
col7_1, col7_2, col7_3, col7_4, col7_5 = st.columns(5)


col1 = [col1_1, col2_1, col3_1, col4_1, col5_1, col6_1, col7_1]
col2 = [col1_2, col2_2, col3_2, col4_2, col5_2, col6_2, col7_2]
col3 = [col1_3, col2_3, col3_3, col4_3, col5_3, col6_3, col7_3]
col4 = [col1_4, col2_4, col3_4, col4_4, col5_4, col6_4, col7_4]
col5 = [col1_5, col2_5, col3_5, col4_5, col5_5, col6_5, col7_5]


player_names = [col1[i].text_input(f"名前{i+1}", key=f"name_{i}") for i in range(7)]
roles = [col2[i].selectbox(
    f"配役{i+1}", ["霊能", "占い", "村人", "共有"], key=f"role_{i}"
) for i in range(7)]
fortune_teller_targets = [col3[i].selectbox(
    f"占い先{i+1}", player_names[0:i] + player_names[i+1:7], key=f"ft_target_{i}"
) if roles[i] == '占い' else None for i in range(7)]
fortune_results = [col4[i].selectbox(
    f"占い結果{i+1}", ["白", "黒"], key=f"ft_result_{i}"
) if roles[i] == '占い' else None for i in range(7)]
shared_partners = [col5[i].selectbox(
    f"共有相方{i+1}の主張", ["欠け"] + player_names[0:i] + player_names[i+1:7], key=f"shared_{i}"
) if roles[i] == '共有' else None for i in range(7)]

execute_button = st.button("実行")
#outputs = [st.empty() for _ in range(13)]

banmen = []
names = []
fortunes = []
pairs = []

def count_roles(roles):
    role_counts = {"霊能": 0, "占い": 0, "村人": 0, "共有": 0}
    for role in roles:
        role_counts[role] += 1
    return [role_counts["占い"], role_counts["霊能"], role_counts["共有"], role_counts["村人"]]

def button_clicked():
    ft_target_list = []
    for ft_target in fortune_teller_targets:
        if ft_target == None:
            ft_target_list.append(None)
        else:
            for i in range(7):
                if ft_target == player_names[i]:
                    ft_target_list.append(i)
            
    shared_partner_list = []
    for shared_partner in shared_partners:
        if shared_partner == None:
            shared_partner_list.append(None)
        elif shared_partner == "欠け":
            shared_partner_list.append(-1)
        else:
            for i in range(7):
                if shared_partner == player_names[i]:
                    shared_partner_list.append(i)
    
    #outputs[0].write("入力された情報:")
    #for i in range(7):
    #    name = player_names[i]
    #    role = roles[i]
    #    ft_target = fortune_teller_targets[i] if role == "占い" else "なし"
    #    fortune_result = fortune_results[i] if role == "占い" else "なし"
    #    shared_partner_claim = shared_partners[i] if role == "共有" else "なし"
    #    outputs[i+1].write(f"{name} - 役職: {role}, 占い先: {ft_target}, 共有相方主張: {shared_partner_claim}, 占い結果: {fortune_result}")

    banmen = count_roles(roles)
    #outputs[8].write(f"役職数: {banmen}")

    changed_flags = [False] * 7
    names = []
    for role_name in ["占い", "霊能", "共有", "村人"]:
        for i in range(7):
            if roles[i] == role_name:
                names.append(player_names[i])
                for j in range(7):
                    if roles[j] == "占い":
                        if ft_target_list[j] == i and changed_flags[j] == False:
                            changed_flags[j] = True
                            ft_target_list[j] = len(names) - 1
                    if roles[j] == "共有":
                        if shared_partner_list[j] == i and changed_flags[j] == False:
                            changed_flags[j] = True
                            shared_partner_list[j] = len(names) - 1

    #outputs[9].write(f"名前リスト: {names}")

    fortunes = []
    for i in range(7):
        if roles[i] == "占い":
            fortunes.append((ft_target_list[i], 0 if fortune_results[i] == "白" else 1))
    #outputs[10].write(f"占い結果リスト: {fortunes}")

    pairs = []
    for i in range(7):
        if roles[i] == "共有":
            pairs.append(shared_partner_list[i])
    #outputs[11].write(f"共有相方主張リスト: {pairs}")


    #####
    #以下、可能内訳抽出
    individual_view_list = [[],[],[],[],[],[],[]]
    utiwake_list = []

    def append_if_not_exists(lst, item):
        if item not in lst:
            lst.append(item)

    count = 0
    indi_count = 0
    banmen_string = "-".join(list(map(str, banmen)))
    try:
        patterns = results[banmen_string]
    except:
        #outputs[12].write("ありえない盤面です")
        error = st.empty()
        error.write("ありえない盤面です.")
        return -1
    for pattern in patterns:
        fortunes_list = []
        psychics_list = []
        pairs_list = []
        villagers_list = []

        for v in itertools.permutations(pattern[0:banmen[0]], banmen[0]):
            append_if_not_exists(fortunes_list, v)
        for v in itertools.permutations(pattern[banmen[0]:banmen[0]+banmen[1]], banmen[1]):
            append_if_not_exists(psychics_list, v)
        for v in itertools.permutations(pattern[banmen[0]+banmen[1]:7-banmen[3]], banmen[2]):
            append_if_not_exists(pairs_list, v)
        for v in itertools.permutations(pattern[7-banmen[3]:7], banmen[3]):
            append_if_not_exists(villagers_list, v)

        for i in fortunes_list:
            for j in psychics_list:
                for k in pairs_list:
                    for l in villagers_list:
                        tmp_pattern = []
                        for x in i: tmp_pattern.append(x)
                        for x in j: tmp_pattern.append(x)
                        for x in k: tmp_pattern.append(x)
                        for x in l: tmp_pattern.append(x)
                        try:
                            true_f = fortunes[i.index("真")]
                            if true_f[1] == 0:
                                if tmp_pattern[true_f[0]] == "狼":
                                    continue
                            else:
                                if tmp_pattern[true_f[0]] != "狼":
                                    continue
                        except:
                            pass
                        true_ps = [m for m, x in enumerate(k) if x == "真"]
                        if len(true_ps) == 1:
                            if pairs[true_ps[0]] != -1:
                                continue
                        else:
                            if pairs[true_ps[0]] != true_ps[1] + banmen[0] + banmen[1] or pairs[true_ps[1]] != true_ps[0] + banmen[0] + banmen[1]:
                                continue
                        bug_flag = 0
                        try:
                            mad = k.index("狂")
                            wolf_ps = [m for m, x in enumerate(k) if x == "狼"]
                            for m in wolf_ps:
                                if pairs[mad] == m + banmen[0] + banmen[1]:
                                    bug_flag += 1
                        except:
                            pass
                        count += 1

                        #真の場合各視点リストに追加
                        for m in range(7):
                            if tmp_pattern[m] == "真":
                                individual_view_list[m].append([names[n] + ":" + tmp_pattern[n] for n in range(7) if m != n])
                                indi_count += 1
                        #

                        utiwake_data = ""
                        utiwake_data += "[パターン" + str(count) + "] "
                        for m in range(6):
                            utiwake_data += names[m] + ":" + tmp_pattern[m] + ","
                        utiwake_data += names[6] + ":" + tmp_pattern[6]
                        if bug_flag:
                            utiwake_data += " ->狂狼同士で相方主張"

                        utiwake_list.append(utiwake_data)
    
    outputs_utiwake = [st.empty() for _ in range(len(utiwake_list))]
    for i in range(len(utiwake_list)):
        outputs_utiwake[i].write(utiwake_list[i])

    info_a = st.empty()
    info_a.write("[各視点]")

    outputs_individuals = [st.empty() for _ in range(indi_count + 7)]
    individual_index = 0

    for i in range(7):
        outputs_individuals[individual_index].write("<" + names[i] + "視点>")
        individual_index += 1
        for each_view in individual_view_list[i]:
            individual_string = ""
            for j in range(5):
                individual_string += each_view[j] + ","
            individual_string += each_view[5]
            outputs_individuals[individual_index].write(individual_string)
            individual_index += 1


if execute_button:
    button_clicked()


    #####
    
    # 追加の情報処理部分
    # (ここに必要な処理を追加してください)
