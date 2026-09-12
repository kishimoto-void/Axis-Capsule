# アクシズカプセル / Axis Capsule

AXIOM 系統の封印カプセル。知能は入れない。観察から核を書かない。

式は常に不全のままである。

```
1 + ? = 0
```

完成和 `1 + (-1) = 0` は出さない。

| 銘板 | 値 |
|------|----|
| 系統名 | アクシズカプセル（Axis Capsule） |
| 系統 | AXIOM |
| 核の個体 | 基準体 |
| 本体 | `axiom_axis.py` |
| 所与 | Hash-A0 `1d350d6e1ab2c4bf…`（intact のとき） |

系統名と核名は別物。`write_name` は常に False。

Grok がリポジトリを読むときは先に `GROK.md`。記憶にはならない。閉じた机が載るだけである。

## 何をするか

制約を軸に分けて封じ、穴は穴のまま扱う。次トークン予測の上に載せる切断面の束ねである。答え機械ではない。

- 推測は事実にしない。演技は同一性にしない
- 保存された行は、引用が無い限り根拠にならない
- η が下がっても、cited Δ が無ければ「縮んだ」とは呼ばない
- 論文から取るのは低次元の骨格だけ。世界モデルや多段エンジンは捨てる

残す低次元は五つだけ。

`seal` / `address` / `hole` / `observe` / `persona`

## 軸

```
⟨SEAL⟩  Axis0 / Persona     核。所与。書けない
   ↓ 親ハッシュ
⟨CITE⟩  Axis1               住所・ピン・Δ・IS
   ↓ 根拠は cited のみ
⟨STORED⟩ ≠ ⟨SUPPORTED⟩
   ↓ 観察だけ
        Axis2               η。hold / nudge / pull / halt。提案のみ
   ↓ 穴
⟨HOLE⟩ ⟨PLUS⟩ ⟨MINUS⟩ ⟨GAP⟩  Axis3   思考フレーム
   ↓ 窓口
⟨ORIGIN⟩ / ⟨ACT⟩            Axis4   推測台帳 / 演技台帳
   ↓
⟨STOP⟩                      完成和・昇格・新語彙
```

| 軸 | 持つもの | 持たないもの |
|----|----------|--------------|
| Axis0 | α規則、β制約世界観、Hash-A0 | 観察からの書き戻し |
| Axis1 | γindex、Δ1人物、Δ2エピソード、Δ3何があったか、IS | 旗だけの書き込み、origin の昇格 |
| Axis2 | η、差異修正力 | 核への書き込み。提案は IS に出さない |
| Axis3 | `start + ? = goal`、analogy | 完成和。onto=住所 |
| Axis4 | origin=推測、act=演技 | 事実化、同一性化 |
| Persona | Hash-P。名前はβと一致 | 名前の書き換え |

Axis1〜4 と Persona は Hash-A0 を親にする。親が壊れたら halt。核は直さない。

## 思考レベルとフレーム型

窓口は思考レベルを要求する。キー `level` が無い／違うときは止まる。適切な型は η・cite・origin から決めて LLM に指示する。知能は足していない。

| レベル | 要求 |
|--------|------|
| L0_seal | 封印のみ。穴を埋めるな。生成するな |
| L1_desk | 閉じた材料だけ。η は観察。縮んだと主張するな |
| L2_hole | `?` を plus/minus/gap で扱え。完成和を書くな |
| L3_cite | 計画の前に印を申告せよ。stored を根拠にするな |
| L4_ledger | origin と act を分けよ。昇格するな |

| 型 | レベル | いつ選ぶか |
|----|--------|------------|
| `axiom` | L2_hole | 既定。式は `1 + ? = 0` |
| `minus_first` | L2_hole | η が高い／pull／persona_drop |
| `gap_only` | L2_hole | 写しが生きている。onto=gap |
| `cite_gate` | L3_cite | 保存はあるが cite が無い |
| `observe` | L1_desk | nudge。η は観察 |
| `ledger` | L4_ledger | 発明／推測台帳 |
| `recall` | L3_cite | 過去を思い出す。ネット接続と γindex が両方要る |
| `halt` | L0_seal | 核が壊れた |

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
- Δ は evidence を明示したときだけ cited。住所キーの自動引用はしない
- 引用印は Hash-A0 / atom / γピンの先頭だけ。任意文字列は印にならない
- 境界トークンは開いている穴だけ。使い切ったら予算から落ちる
- 漏れ語（です／ます／補完します など）の analogize は拒否

## 含意（これが通るならこれが成り立つ）

形は `P ⇒ Q`。実測は `python3 equations.py`。

- intact(A0) ∧ given=Hash-A0 ⇒ 核は所与。`write_*` は False
- accept が通る ⇒ `?` ∈ 式 ∧ ¬completed
- cited(Δ) ⇒ standing=supported
- IS ∧ ¬cited ⇒ stored_not_supported
- η↓ ∧ ¬cited ⇒ ¬shrunk
- η 高／pull ⇒ pattern=`minus_first` ∧ level=`L2_hole`
- 窓口に level 無し ⇒ `level_required`
- stored ∧ ¬cited ⇒ `cite_gate` ∧ `L3_cite`
- recall ∧ ¬net ⇒ origin。IS に出さない
- recall ∧ net ∧ γindex cited ⇒ standing=supported

ロールプレイで過去を思い出すときは、インターネット接続と γindex 参照が両方要る。どちらか欠ければ推測穴。記憶を発明しない。

## 実行

Python 3。依存なし。

```bash
python3 axiom_axis.py          # 通常テスト
python3 axiom_axis.py demo     # 封印・ドリフト・窓口の通し
python3 axiom_axis.py analog0  # ドリフト0の写し整合
python3 axiom_axis.py analog10 # アナロジー10%漏れ
python3 axiom_axis.py drift10  # 口調10%漏れ
python3 axiom_axis.py break20  # 破壊20
python3 axiom_axis.py possible # 成り立ちうる構成の整合
python3 axiom_axis.py eq       # 含意方程式 P⇒Q
python3 axiom_axis.py pattern  # 思考レベルと適切なフレーム型
python3 axiom_axis.py recall   # 過去想起：ネット接続と γindex
python3 axis_general.py        # 一般タイプの検査
python3 axis_general.py demo   # 一般タイプの通し
python3 axis_general.py tutorial # キャラをネットから取る骨格
```

実測（この封印のまま）: 通常 74/74、一般 5/5、含意 30/30 HOLD、break20 は 20/20 BLOCK。A0 は動かない。

## 一般タイプ

封印本体は触らない。使い口だけ `axis_general.py`。

```python
from axis_general import Capsule

c = Capsule(topic="scene")
c.pin("char-scope")
c.note("結論", "隔離")          # cited。IS ではない
c.net("https://example.com")    # 接続。記憶ではない
print(c.ask("基準体のままだぜ。穴は穴だ。"))
print(c.recall("隔離"))         # ネットと γindex が両方要る
print(c.prompt("昔を思い出して"))
print(c.card())
```

## ファイル

| ファイル | 役割 |
|----------|------|
| `GROK.md` | Grok が先に読む机。記憶ではない |
| `GROK_TUTORIAL.md` | チャット骨格。キャラ設定はネットから |
| `axiom_axis.py` | 本体。軸・封印・検査・実験ランナー |
| `axis_general.py` | 一般タイプ。使い口。核は触らない |
| `equations.py` | 含意方程式の実測 |
| `特徴と性質.md` | 性質の銘板 |
| `AXIS.md` | 短い位置づけ |
| `POSSIBLE.md` | 成り立ちうる／成り立たない構成 |
| `LINEAGE.md` | 前段の系譜。現行軸には繋がない |
| `axiom_lineage.py` | 系譜実験 |

## 証明していないこと

- 知能を足したこと
- 穴を埋めて揃えたこと
- min3 より強いこと
- この形を正典にすること
