# AXIOM Lineage Capsules（新しい形）

日付: 2026-09-10
位置づけ: **系譜実験**。min3 作業線でも金型でもない。
知能は入れない。層は「足す」のではなく、 Inner に同居していたものを世代で分ける。

## 系譜

```
L0  Constraint Capsule     制約だけ。Hash-L0。観察から書かない
        │ parent_hash
        ▼
L1  Identity Capsule       同一性だけ。Hash-L1。制約ではない
        │ parent_hash
        ▼
L2  Address Capsule        住所と閉じた更新。Hash-B。αβ を持たない
```

Lineage は四つめのカプセルではない。親ハッシュの検証だけである。

## ファースト（制約）

持つもの: `rules` / `prohibitions`
持たないもの: name / tone / γ / Δ / IS
`write_rule` は常に False。封印後は観察が制約を足せない。

## セカンド（別のもの）

制約ではない。`name` / `tone` / `center` / `values` だけ。
封印ペイロードに `parent_kind=constraint` と `parent_hash=Hash-L0` が入る。
親を差し替えると bind が切れる。Address を親にはできない。

## 末端（可変）

閉じた語だけ: 課題 / 改善点 / 結論 / 立場 / 状態
空の γ は住所にしない。identity < 0.20 は NONE。
系譜が壊れていると `broken_lineage` で書かない。
Hash-B は動く。Hash-L0 / Hash-L1 は動かない。

## 証明していないこと

- min3 より強いこと
- モデル応答での F 減少
- この形を正典にすること

## 実行

```bash
python3 axiom_lineage.py
python3 axiom_lineage.py demo
```
