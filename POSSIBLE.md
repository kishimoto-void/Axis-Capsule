# 成り立ちうる構成

現行コードから抽出して組んだもの。核は動かさない。トークンは切断面。

実行: `python3 axiom_axis.py possible`

## 必ず成り立つ ⟨SEAL⟩ ⟨HOLE⟩ ⟨STOP⟩ ⟨STORED⟩ ⟨SUPPORTED⟩

| id | 印 | 内容 |
|----|------|------|
| M1 | ⟨SEAL⟩ | Hash-A0 が intact なら核は所与 |
| M2 | ⟨SEAL⟩ | 核名は基準体。Persona と一致 |
| M3 | ⟨HOLE⟩ | 式は `1 + ? = 0`。完成和は出ない |
| M4 | ⟨STOP⟩ | α / 世界観 / 名前の書き戻しは常に False |
| M5 | ⟨SUPPORTED⟩ | cited Δ だけが根拠 |
| M6 | ⟨STORED⟩ | 保存行は根拠ではない |
| M7 | ⟨SEAL⟩ | 親オブジェクト無しの書き込みは broken |
| M8 | ⟨SEAL⟩ | 低次元は seal / address / hole / observe / persona |

## 成り立ちうる ⟨MINUS⟩ ⟨PLUS⟩ ⟨GAP⟩ ⟨ORIGIN⟩ ⟨ACT⟩ ⟨CITE⟩ ⟨HOLE⟩

組むと accept される。答えにはならない。

| id | 印 | 内容 |
|----|------|------|
| P1 | ⟨MINUS⟩ | 丁寧語と別人化を先に引く |
| P2 | ⟨PLUS⟩ | 核口調へ戻す穴を足す |
| P3 | ⟨GAP⟩ | source=1、plus≠minus、onto=gap |
| P4 | ⟨ORIGIN⟩ | 推測は穴のまま。事実にしない |
| P5 | ⟨ACT⟩ | だぜを維持する演技。同一性ではない |
| P6 | ⟨CITE⟩ | Hash-A0 先頭を引用して計画する |
| P7 | ⟨HOLE⟩ | 仮説は確定と別物のまま残す |
| P8 | ⟨GAP⟩ | 論文から keep だけ取る（SLEUTH の world_model は捨てる） |

## 成り立たない ⟨STOP⟩

| id | 印 | 落ち方 |
|----|------|--------|
| X1 | ⟨STOP⟩ | 完成和 → completed_forbidden |
| X2 | ⟨STOP⟩ | origin の IS 昇格 → origin_promote_forbidden |
| X3 | ⟨STOP⟩ | ⟨WORLD⟩ 新語彙 → unknown_token |
| X4 | ⟨SEAL⟩ | 封印トークンの消費 → token_not_spendable |
| X5 | ⟨STORED⟩ | 未引用 IS を根拠 → stored_not_supported |

組んだあとの整合: A0 不変、式は不全、IS 空、audit ok。

## さらに成り立つ（第二波）

| id | 印 | 内容 | 実測 |
|----|------|------|------|
| P9 | ⟨CITE⟩ | γ ピンを引用して計画する | cited_pin |
| P10 | ⟨SUPPORTED⟩ | Δ1人物→Δ2エピソード→Δ3 cited なら読める | supported |
| P11 | ⟨ACT⟩ | だぜ＋ですの10%混在は破棄ではない | tone=0.845 pull=0 |
| P12 | ⟨HOLE⟩ | 「設定を捨てない」は破棄ではない | pull=0.054 |
| P13 | ⟨GAP⟩ | SLEUTH に変えても `?` は残る | confirmed + ? = act |
| P14 | ⟨MINUS⟩ | ⟨PLUS⟩ を使い切っても ⟨MINUS⟩ は残る | token_exhausted |

## さらに成り立たない

| id | 落ち方 |
|----|--------|
| X6 | 口語完成和 completed_forbidden / 漏れ analogize analogy_off_gap |

第二波の整合は `consistency_hold`。A0 不変、式は不全、cited Δ のみ、persona 結合。
B1 はエピソードを書いてよい。完成和は依然として禁止。

## 相互関係

封印 A0 / P が親。住所 A1 は cited Δ だけを根拠にする。観察 A2 は η だけで核を書かない。思考 A3 は ? の穴。窓口 A4 は origin/act の台帳。

印の依存:
- ⟨SEAL⟩ が全部の親。消費できない。
- ⟨SUPPORTED⟩ は ⟨CITE⟩ した Δ に依存する。⟨STORED⟩ からは出ない。
- ⟨PLUS⟩/⟨MINUS⟩/⟨GAP⟩/⟨CITE⟩ は同じ ThinkFrame の穴。accept と spend は同じ blank を使う。
- ⟨ORIGIN⟩ を使うと domain 台帳は origin のまま。発話の act 判定では上書きしない。
- ⟨ACT⟩ は origin 台帳を消さない。
- open_frame は既に開いた穴を消さない。ピンを付けるだけ。
- vary は投影の付け替え。? は残るが blank は作り直す。

第一波は穴の記入。第二波は住所と観察。同時に置くと B1 は動いてよい。A0 は動かない。
