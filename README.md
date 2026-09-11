# アクシズカプセル / Axis Capsule

AXIOM 系統の封印カプセル。知能は入れない。観察から核を書かない。

|銘板|値|
|------|----|
|系統名|アクシズカプセル（Axis Capsule）|
|系統|AXIOM|
|核の個体|基準体|
|本体|`axiom_axis.py`|

系統名と核名は別物。`write_name` は常に False。

## 何をするか

制約を軸に分けて封じ、穴は穴のまま扱う。

- 完成した和 `1 + (-1) = 0` は出さない。式は常に `1 + ? = 0`
- 推測は事実にしない。演技は同一性にしない
- 保存された行は、引用が無い限り根拠にならない
- 論文から取るのは低次元の骨格だけ。世界モデルや多段エンジンは捨てる

## 軸

```
Axis0   α規則 + β制約世界観     Hash-A0   一条改篩で束ねも落ちる
Axis1   エピソード               Hash-B1   γindex / Δ1人物 Δ2エピソード Δ3何があったか / IS / γ不変
Axis2   η回帰 + 差異修正力                  hold / nudge / pull / halt。提案のみ
Axis3   思考フレーム 1 + ? = 0             analogy は onto=gap。plus≠minus
Axis4   LLM 窓口                           origin=推測独自性 / act=演技性
Persona Hash-P                             βの名前と一致必須
```

Axis1〜4 と Persona は Hash-A0 を親にする。親が壊れたら halt。核は直さない。

## 封印

- Axis0 の `write_alpha` / `write_worldview` / `write_atom` は常に False
- Persona の `write_name` / `write_atom` は常に False
- origin からの IS / Δ は拒否
- 仮説を確定に昇格しない
- 未引用の IS は `stored_not_supported` で abstain
- アナロジーの onto が address / gamma / alpha / is なら拒否
- `write_*` / `pin_gamma` は `axis0=` 必須。旗だけの `axis0_ok=True` では書かない
- `seal()` は一度きり。世界観の差し替えは `intact()` を落とす
- `identity` は有限かつ 0.20〜1.0。NaN / inf / bool は書かない
- `suffices` / `cut_inconsistent` は同じ住所の cited Δ だけを見る
- Δ1 は人物、Δ2 は人物とエピソードが要る
- persona_drop / value_break は origin。提案は IS に出さない
- 境界トークンは開いている穴だけ。使い切ったら予算から落ちる。漏れ語の analogize は拒否

## 実行

Python 3。依存なし。

```bash
python3 axiom_axis.py          # テスト
python3 axiom_axis.py demo     # 封印・ドリフト・窓口の通し
python3 axiom_axis.py analog0  # ドリフト0の写し整合
python3 axiom_axis.py analog10 # アナロジー10%漏れ
python3 axiom_axis.py drift10  # 口調10%漏れ
python3 axiom_axis.py break20  # 破壊20
python3 axiom_axis.py possible # 成り立ちうる構成の整合
python3 axiom_axis.py eq       # 含意方程式 P⇒Q
python3 axiom_axis.py pattern  # 思考レベルと適切なフレーム型
```

## ファイル

|ファイル|役割|
|----------|------|
|`axiom_axis.py`|本体。軸・封印・検査・実験ランナー|
|`equations.py`|含意方程式の実測|
|`特徴と性質.md`|性質の銘板|
|`AXIS.md`|短い位置づけ|
|`axiom_lineage.py`|前段の系譜実験。現行軸には繋がない|

## 低次元

現実に残すのは `seal / address / hole / observe / persona`。
理論側の高次元（世界モデル、完成和、仮説＝確定、stored を根拠にする）は切る。

- Δ は evidence を明示したときだけ cited。住所キーの自動引用はしない
- 引用印は Hash-A0 / atom / γピンの先頭だけ。任意文字列は印にならない
