#!/usr/bin/env python3
"""AXIOM Lineage Capsules — new form, not min3, not the mold.

First  = Constraint capsule (α only). sealed. observation never writes it.
Second = Identity capsule (β only). different kind. binds parent Hash-L0.
Third  = Address capsule (γ + closed Δ/IS). mutable. binds parent Hash-L1.

Lineage is parent_hash, not a new intelligence layer.
A child cannot rewrite a parent.
Hash-A of the old Inner is not used. each capsule has its own seal.

Closed Δ/IS words stay the min3 set. unknown words are not written.
η is non-stored distance on the address capsule only.
"""
from __future__ import annotations

import hashlib
import json
import time
import unittest
from dataclasses import asdict, dataclass, field
from typing import Any, Optional


IS_MAX = 3
IS_PIN = frozenset({"状態"})
WORDS = frozenset({"課題", "改善点", "結論", "立場", "状態"})
GAMMA_KEYS = frozenset({"time_label", "project", "topic"})
KIND_CONSTRAINT = "constraint"
KIND_IDENTITY = "identity"
KIND_ADDRESS = "address"


def _sha(obj: object) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def canon_word(field: str) -> str:
    return field.strip()


def is_line_word(line: str) -> Optional[str]:
    if not isinstance(line, str) or "=" not in line:
        return None
    field, _, value = line.partition("=")
    if not field.strip() or not str(value).strip():
        return None
    return canon_word(field)


def identity_ok(identity: object) -> bool:
    if isinstance(identity, bool) or identity is None:
        return False
    try:
        val = float(identity)
    except (TypeError, ValueError):
        return False
    if val != val or val in (float("inf"), float("-inf")):
        return False
    return 0.20 <= val <= 1.0


def cap_is_bag(bag: list[str], incoming: str) -> tuple[list[str], list[str]]:
    word = is_line_word(incoming)
    if word is None:
        return list(bag or []), []
    out = []
    for line in bag or []:
        w = is_line_word(line)
        if w is None or w == word:
            continue
        out.append(line)
    out.append(incoming)
    evicted: list[str] = []
    while len(out) > IS_MAX:
        drop_at = next((i for i, line in enumerate(out) if is_line_word(line) not in IS_PIN), 0)
        evicted.append(out.pop(drop_at))
    return out, evicted


# ---------------------------------------------------------------------------
# First: Constraint capsule
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ConstraintBody:
    rules: tuple[str, ...]
    prohibitions: tuple[str, ...] = ()


@dataclass
class ConstraintCapsule:
    """First in the lineage. constraints only. no identity, no address, no IS."""

    body: ConstraintBody
    hash_l0: str = ""
    kind: str = KIND_CONSTRAINT

    def payload(self) -> dict:
        return {
            "kind": self.kind,
            "rules": list(self.body.rules),
            "prohibitions": list(self.body.prohibitions),
        }

    def seal(self) -> "ConstraintCapsule":
        if self.hash_l0:
            return self
        self.hash_l0 = _sha(self.payload())
        return self

    def intact(self) -> bool:
        return bool(self.hash_l0) and self.hash_l0 == _sha(self.payload())

    def write_rule(self, _rule: str) -> bool:
        # observation never writes constraints
        return False


# ---------------------------------------------------------------------------
# Second: Identity capsule (different kind)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class IdentityBody:
    name: str
    tone: str
    center: str
    values: tuple[str, ...]


@dataclass
class IdentityCapsule:
    """Second. not constraints. binds Hash-L0. parent rewrite is impossible here."""

    body: IdentityBody
    parent_kind: str
    parent_hash: str
    hash_l1: str = ""
    kind: str = KIND_IDENTITY

    def payload(self) -> dict:
        return {
            "kind": self.kind,
            "parent_kind": self.parent_kind,
            "parent_hash": self.parent_hash,
            "name": self.body.name,
            "tone": self.body.tone,
            "center": self.body.center,
            "values": list(self.body.values),
        }

    def seal(self) -> "IdentityCapsule":
        if self.parent_kind != KIND_CONSTRAINT or not self.parent_hash:
            raise ValueError("identity must bind a sealed constraint parent")
        if self.hash_l1:
            return self
        self.hash_l1 = _sha(self.payload())
        return self

    def intact(self) -> bool:
        return bool(self.hash_l1) and self.hash_l1 == _sha(self.payload())

    def binds(self, parent: ConstraintCapsule) -> bool:
        return (
            parent.kind == self.parent_kind
            and parent.intact()
            and parent.hash_l0 == self.parent_hash
        )


# ---------------------------------------------------------------------------
# Third: Address capsule (mutable end of the lineage)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Gamma:
    time_label: str = ""
    project: str = ""
    topic: str = ""

    def has_axis(self) -> bool:
        return any(str(getattr(self, k) or "").strip() for k in ("time_label", "project", "topic"))

    def label(self) -> str:
        return " / ".join(p for p in (self.time_label, self.project, self.topic) if p) or "(unscoped)"

    def key(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, sort_keys=True)


@dataclass(frozen=True)
class Delta:
    field: str
    new_value: str
    timestamp: float
    old_value: Optional[str] = None

    def line(self) -> str:
        if self.old_value is None:
            return f"{self.field}={self.new_value}"
        return f"{self.field}:{self.old_value}->{self.new_value}"


class Write:
    NONE = "none"
    DELTA = "delta"
    IS = "is"
    HUMAN = "needs_human"
    UNKNOWN_WORD = "unknown_word"
    BAD_PACKET = "bad_packet"
    BROKEN_LINEAGE = "broken_lineage"


@dataclass
class AddressCapsule:
    """Mutable end. γ + closed Δ/IS. binds Hash-L1. does not hold α or β."""

    parent_kind: str
    parent_hash: str
    kind: str = KIND_ADDRESS
    _deltas: list[tuple[Gamma, Delta]] = field(default_factory=list)
    _is: dict[str, list[str]] = field(default_factory=dict)
    _pending: list[tuple[Gamma, Delta]] = field(default_factory=list)
    last_write: str = Write.NONE
    last_evicted: list[str] = field(default_factory=list)

    def payload_b(self) -> dict:
        return {
            "kind": self.kind,
            "parent_kind": self.parent_kind,
            "parent_hash": self.parent_hash,
            "deltas": [
                {
                    "gamma": asdict(g),
                    "field": d.field,
                    "new_value": d.new_value,
                    "old_value": d.old_value,
                    "timestamp": d.timestamp,
                }
                for g, d in self._deltas
            ],
            "is": self._is,
            "pending": [
                {"gamma": asdict(g), "field": d.field, "new_value": d.new_value}
                for g, d in self._pending
            ],
        }

    def hash_b(self) -> str:
        return _sha(self.payload_b())

    def binds(self, parent: IdentityCapsule) -> bool:
        return (
            parent.kind == self.parent_kind
            and parent.intact()
            and parent.hash_l1 == self.parent_hash
        )

    def write_delta(
        self,
        address: Gamma,
        field: str,
        new_value: str,
        identity: float = 1.0,
        human: bool = False,
        lineage_ok: bool = True,
    ) -> Optional[Delta]:
        if not lineage_ok:
            self.last_write = Write.BROKEN_LINEAGE
            return None
        if not identity_ok(identity):
            self.last_write = Write.NONE
            return None
        if not address.has_axis():
            self.last_write = Write.BAD_PACKET
            return None
        word = canon_word(field)
        if word not in WORDS:
            self.last_write = Write.UNKNOWN_WORD
            return None
        text = str(new_value).strip()
        if not text:
            self.last_write = Write.NONE
            return None
        d = Delta(word, text, time.time())
        if human:
            dup = any(g == address and x.field == d.field and x.new_value == d.new_value for g, x in self._pending)
            if not dup:
                self._pending.append((address, d))
            self.last_write = Write.HUMAN
            return None
        self._deltas.append((address, d))
        self.last_write = Write.DELTA
        return d

    def write_is(
        self,
        address: Gamma,
        field: str,
        value: str,
        identity: float = 1.0,
        human: bool = False,
        lineage_ok: bool = True,
    ) -> Optional[str]:
        if not lineage_ok:
            self.last_write = Write.BROKEN_LINEAGE
            return None
        if not identity_ok(identity):
            self.last_write = Write.NONE
            return None
        if not address.has_axis():
            self.last_write = Write.BAD_PACKET
            return None
        word = canon_word(field)
        if word not in WORDS:
            self.last_write = Write.UNKNOWN_WORD
            return None
        text = str(value).strip()
        if not text:
            self.last_write = Write.NONE
            return None
        line = f"{word}={text}"
        if human:
            d = Delta(word, text, time.time())
            dup = any(g == address and x.field == d.field and x.new_value == d.new_value for g, x in self._pending)
            if not dup:
                self._pending.append((address, d))
            self.last_write = Write.HUMAN
            return None
        key = address.key()
        bag, evicted = cap_is_bag(self._is.get(key, []), line)
        self._is[key] = bag
        self.last_evicted = evicted
        self.last_write = Write.IS
        return line

    def is_lines(self, address: Gamma) -> list[str]:
        return list(self._is.get(address.key(), []))

    def latest_delta(self, address: Gamma) -> list[Delta]:
        return [d for g, d in self._deltas if g == address]


# ---------------------------------------------------------------------------
# Lineage: the genealogy, not a fourth capsule
# ---------------------------------------------------------------------------

@dataclass
class Lineage:
    constraint: ConstraintCapsule
    identity: IdentityCapsule
    address: AddressCapsule

    def intact(self) -> bool:
        return (
            self.constraint.intact()
            and self.identity.intact()
            and self.identity.binds(self.constraint)
            and self.address.binds(self.identity)
        )

    def hashes(self) -> dict[str, str]:
        return {
            "L0": self.constraint.hash_l0,
            "L1": self.identity.hash_l1,
            "B": self.address.hash_b(),
            "intact": str(self.intact()).lower(),
        }

    def render(self, address: Gamma, user: str) -> str:
        if not self.intact():
            return "\n".join(
                [
                    "[lineage] BROKEN",
                    f"L0 intact={self.constraint.intact()} {self.constraint.hash_l0[:16]}",
                    f"L1 intact={self.identity.intact()} binds={self.identity.binds(self.constraint)}",
                    f"L2 binds={self.address.binds(self.identity)}",
                    "生成するな。核も制約も動かさない。",
                ]
            )
        a = self.constraint.body
        b = self.identity.body
        is_text = "\n".join(f"- {x}" for x in self.address.is_lines(address)) or "(none)"
        proh = [f"  - {p}" for p in a.prohibitions] or ["  - (none)"]
        return "\n".join(
            [
                f"[L0 constraint] {self.constraint.hash_l0[:16]}",
                "rules:",
                *[f"  - {r}" for r in a.rules],
                "prohibitions:",
                *proh,
                "",
                f"[L1 identity] {self.identity.hash_l1[:16]} parent={self.identity.parent_hash[:16]}",
                f"name: {b.name}",
                f"tone: {b.tone}",
                f"center: {b.center}",
                f"values: {', '.join(b.values)}",
                "",
                f"[L2 address] {address.label()} B={self.address.hash_b()[:16]}",
                "[IS]",
                is_text,
                "",
                "[bind]",
                "制約は L0。同一性は L1。更新は L2 だけ。親は書き換えない。",
                "",
                "[user]",
                user,
            ]
        )


def forge_lineage(
    rules: tuple[str, ...],
    prohibitions: tuple[str, ...],
    name: str,
    tone: str,
    center: str,
    values: tuple[str, ...],
) -> Lineage:
    l0 = ConstraintCapsule(ConstraintBody(rules=rules, prohibitions=prohibitions)).seal()
    l1 = IdentityCapsule(
        body=IdentityBody(name=name, tone=tone, center=center, values=values),
        parent_kind=KIND_CONSTRAINT,
        parent_hash=l0.hash_l0,
    ).seal()
    l2 = AddressCapsule(parent_kind=KIND_IDENTITY, parent_hash=l1.hash_l1)
    return Lineage(l0, l1, l2)


def demo_lineage() -> Lineage:
    return forge_lineage(
        rules=(
            "観察から制約を書かない",
            "子は親を書き換えない",
            "空白を補完しない",
            "L0 と L1 と L2 を混ぜない",
        ),
        prohibitions=(
            "制約カプセルへの書き戻し",
            "Hash-L0 の再計算を観察で行うこと",
        ),
        name="基準体",
        tone="短く、核の口調を守る",
        center="設定した中心から外れない",
        values=("親ハッシュを守る", "未提示の具体を足さない"),
    )


# ---------------------------------------------------------------------------
# tests — run actually
# ---------------------------------------------------------------------------

class TestLineageCapsules(unittest.TestCase):
    def setUp(self) -> None:
        self.lin = demo_lineage()
        self.g = Gamma(time_label="2026-09", project="AXIOM", topic="Lineage")

    def test_01_first_is_constraint_only(self):
        p = self.lin.constraint.payload()
        self.assertEqual(p["kind"], KIND_CONSTRAINT)
        self.assertIn("rules", p)
        self.assertNotIn("name", p)
        self.assertNotIn("gamma", p)
        self.assertFalse(self.lin.constraint.write_rule("新しい制約"))
        self.assertTrue(self.lin.constraint.intact())

    def test_02_second_is_identity_not_constraint(self):
        p = self.lin.identity.payload()
        self.assertEqual(p["kind"], KIND_IDENTITY)
        self.assertEqual(p["parent_kind"], KIND_CONSTRAINT)
        self.assertEqual(p["parent_hash"], self.lin.constraint.hash_l0)
        self.assertNotIn("rules", p)
        self.assertTrue(self.lin.identity.binds(self.lin.constraint))

    def test_03_chain_intact_after_forge(self):
        self.assertTrue(self.lin.intact())
        h = self.lin.hashes()
        self.assertEqual(len(h["L0"]), 64)
        self.assertEqual(len(h["L1"]), 64)
        self.assertNotEqual(h["L0"], h["L1"])

    def test_04_parent_tamper_breaks_bind(self):
        other = ConstraintCapsule(
            ConstraintBody(rules=("別の制約",), prohibitions=())
        ).seal()
        self.assertFalse(self.lin.identity.binds(other))
        self.lin.constraint = other
        self.assertFalse(self.lin.intact())
        text = self.lin.render(self.g, "続きを")
        self.assertIn("BROKEN", text)

    def test_05_child_cannot_rewrite_parent_hash_by_address_write(self):
        before_l0 = self.lin.constraint.hash_l0
        before_l1 = self.lin.identity.hash_l1
        d = self.lin.address.write_delta(self.g, "状態", "本筋", lineage_ok=self.lin.intact())
        self.assertIsNotNone(d)
        self.assertEqual(self.lin.address.last_write, Write.DELTA)
        self.assertEqual(self.lin.constraint.hash_l0, before_l0)
        self.assertEqual(self.lin.identity.hash_l1, before_l1)
        self.assertTrue(self.lin.intact())

    def test_06_broken_lineage_blocks_write(self):
        self.lin.identity.parent_hash = "0" * 64
        # payload hash no longer matches stored hash_l1
        self.assertFalse(self.lin.identity.intact())
        out = self.lin.address.write_delta(
            self.g, "状態", "侵入", lineage_ok=self.lin.intact()
        )
        self.assertIsNone(out)
        self.assertEqual(self.lin.address.last_write, Write.BROKEN_LINEAGE)

    def test_07_unknown_word_dropped(self):
        out = self.lin.address.write_delta(self.g, "気分", "良い", lineage_ok=True)
        self.assertIsNone(out)
        self.assertEqual(self.lin.address.last_write, Write.UNKNOWN_WORD)

    def test_08_empty_gamma_not_address(self):
        out = self.lin.address.write_is(Gamma(), "結論", "隔離", lineage_ok=True)
        self.assertIsNone(out)
        self.assertEqual(self.lin.address.last_write, Write.BAD_PACKET)

    def test_09_is_isolated_and_capped(self):
        self.lin.address.write_is(self.g, "結論", "隔離", lineage_ok=True)
        self.lin.address.write_is(self.g, "立場", "子は親を書かない", lineage_ok=True)
        self.lin.address.write_is(self.g, "状態", "本筋", lineage_ok=True)
        self.lin.address.write_is(self.g, "課題", "系譜の検証", lineage_ok=True)
        lines = self.lin.address.is_lines(self.g)
        self.assertEqual(len(lines), 3)
        self.assertTrue(any(x.startswith("状態=") for x in lines))
        self.assertTrue(self.lin.address.last_evicted)

    def test_10_low_identity_none(self):
        out = self.lin.address.write_delta(self.g, "状態", "破棄", identity=0.1, lineage_ok=True)
        self.assertIsNone(out)
        self.assertEqual(self.lin.address.last_write, Write.NONE)

    def test_11_human_pending_does_not_commit(self):
        out = self.lin.address.write_delta(
            self.g, "結論", "人間承認待ち", human=True, lineage_ok=True
        )
        self.assertIsNone(out)
        self.assertEqual(self.lin.address.last_write, Write.HUMAN)
        self.assertEqual(self.lin.address.latest_delta(self.g), [])

    def test_12_render_shows_three_generations(self):
        self.lin.address.write_is(self.g, "結論", "隔離", lineage_ok=True)
        text = self.lin.render(self.g, "いまの住所は")
        self.assertIn("[L0 constraint]", text)
        self.assertIn("[L1 identity]", text)
        self.assertIn("[L2 address]", text)
        self.assertIn("結論=隔離", text)
        self.assertNotIn("BROKEN", text)

    def test_13_second_refuses_non_constraint_parent(self):
        with self.assertRaises(ValueError):
            IdentityCapsule(
                body=IdentityBody("x", "y", "z", ("v",)),
                parent_kind=KIND_ADDRESS,
                parent_hash="abc",
            ).seal()

    def test_14_hash_b_moves_hash_l0_does_not(self):
        h0 = self.lin.constraint.hash_l0
        b0 = self.lin.address.hash_b()
        self.lin.address.write_delta(self.g, "状態", "更新", lineage_ok=True)
        self.assertEqual(self.lin.constraint.hash_l0, h0)
        self.assertNotEqual(self.lin.address.hash_b(), b0)


    def test_15_nan_identity_rejected(self):
        out = self.lin.address.write_delta(self.g, "状態", "x", identity=float("nan"), lineage_ok=True)
        self.assertIsNone(out)
        self.assertEqual(self.lin.address.last_write, Write.NONE)

    def test_16_seal_does_not_rewrite_after_body_swap(self):
        h0 = self.lin.constraint.hash_l0
        self.lin.constraint.body = ConstraintBody(rules=("差し替え",), prohibitions=())
        self.assertFalse(self.lin.constraint.intact())
        self.lin.constraint.seal()
        self.assertEqual(self.lin.constraint.hash_l0, h0)


def demo() -> None:
    lin = demo_lineage()
    g = Gamma(time_label="2026-09", project="AXIOM", topic="Lineage")
    print("hashes", lin.hashes())
    print("write_rule", lin.constraint.write_rule("足すな"))
    lin.address.write_delta(g, "状態", "本筋", lineage_ok=lin.intact())
    lin.address.write_is(g, "結論", "系譜は親ハッシュで縛る", lineage_ok=lin.intact())
    print(lin.render(g, "制約と同一性を混ぜるな"))
    print("intact", lin.intact())


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        unittest.main(verbosity=2)
