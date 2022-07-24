import pandas as pd
from functools import reduce
from operator import add

# データセット
d = {
    "天気":["晴","曇","曇","晴","雨"],
    "風速":["強","弱","強","弱","弱"],
    "湿度":["高","高","低","高","高"],
    "花火":["×","○","×","○","×"],
}
dft = pd.DataFrame(d)

# 値の配分を求めるラムダ式、引数はpandas.Series、戻り値は各値の個数が入った配列
# 入力sからvalue_counts()で各値の度数を取得し、辞書型のデータのループ items()を呼び出す。
# sortedは、実行毎に出力結果が変化しないように、度数の小さい順に並べ替えている。
# そして、要素がキー(k)と値(v)の文字列となった配列を生成する。
cstr = lambda s:[k+":"+str(v) for k,v in sorted(s.value_counts().items())]

# ツリーのデータ構造
tree = {
    "name": "decision tree "+dft.columns[-1]+" "+str(cstr(dft.iloc[:,-1])),
    "df": dft,
    "edges": [],
}

# 初期値の設定
open = [tree]

# ジニ不純度
zini = lambda s: reduce(add, map(lambda x: x**2, map(lambda x:(x/len(s)),s.value_counts())))

# openが空になるまで繰り返す。
while(len(open)!=0):
    n = open.pop(0)
    df_n = n["df"]

    # このノードのエントロピーが0の場合、これ以上エッジを展開できないので、このノードからの枝分かれはしない。
    if (1 - zini(df_n.iloc[:,-1])) == 0:
        continue

    attrs = {}
    # クラス属性の最後の列以外の属性をすべて調査する。
    for attr in df_n.columns[:-1]:

        attrs[attr] = {"zini":0,"dfs":[],"values":[]}

        for value in sorted(set(df_n[attr])):
            # 属性値でデータをフィルタリングする。
            df_m = df_n[df_n.loc[:,attr]==value]
            # ジニ不純度を計算し、関連するデータ、値をそれぞれ保存しておく。
            attrs[attr]["zini"] += (1 - zini(df_n.iloc[:,-1]))*df_m.shape[0]/df_n.shape[0]
            attrs[attr]["dfs"] += [df_m]
            attrs[attr]["values"] += [value]
            pass
        pass
    # クラス値を分離可能な属性が1つも無い場合は、このノードの調査を終了する。
    if len(attrs)==0:
        continue

    print(attrs)

    # 2分岐できるものの中でジニ不純度が最小になる属性を取得する。
    if len(attrs) == 1:
        continue
    else:
        attrs_copy = attrs
        while True:
            attr = min(attrs_copy,key=lambda x:attrs[x]["zini"])

            if len(attrs[attr]['values']) <= 2:
                break
            else:
                del attrs_copy[attr]

    # 分岐する属性のそれぞれの値、分岐後のデータを、ツリーとopenにそれぞれ追加する。
    for d,v in zip(attrs[attr]["dfs"],attrs[attr]["values"]):
        m = {"name":attr+"="+str(v),"edges":[],"df":d.drop(columns=attr)}
        n["edges"].append(m)
        open.append(m)
    pass

print(dft)
print('-'*30)


def tstr(tree,indent=""):

    s = indent+tree["name"]+str(cstr(tree["df"].iloc[:,-1]) if len(tree["edges"])==0 else "")+"\n"

    for e in tree["edges"]:
        s += tstr(e,indent+"  ")
        pass
    return s

print(tstr(tree))