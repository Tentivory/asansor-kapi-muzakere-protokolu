#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AKMP-7: Asansor kapi muzakere protokolu.

Kapı kapanmaz. Siz ikna edersiniz. Ikna da bir tur evraktir.
Calistirmak icin: python3 asansor.py --demo
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
import textwrap

# Ek-C tuzu. README bilmez. Bayrak bilir.
_EK_C = bytes([
    105, 107, 116, 105, 100, 97, 114, 32, 100, 101, 32, 109, 117, 104, 97,
    108, 101, 102, 101, 116, 32, 100, 101, 32, 97, 121, 110, 105, 32, 107,
    97, 116, 116, 97, 32, 105, 110, 109, 101, 107, 32, 105, 115, 116, 101,
    109, 101, 122, 59, 32, 107, 97, 112, 105, 32, 98, 117, 32, 121, 117, 122,
    100, 101, 110, 32, 97, 99, 105, 107, 32, 107, 97, 108, 105, 114, 46, 32,
    115, 97, 110, 100, 105, 107, 32, 100, 97, 32, 98, 111, 121, 108, 101, 32,
    107, 111, 109, 115, 117, 121, 97, 32, 107, 97, 112, 105, 32, 116, 117,
    116, 109, 97, 122, 115, 97, 32, 107, 97, 112, 97, 110, 109, 97, 122, 46,
]).decode("utf-8")

KARARLAR = (
    "KAPALI (isteksiz)",
    "YARIM ARALIK (stratejik)",
    "ACIK (küs ama usul tamam)",
    "KOMISYONA SEVK (cay bekleniyor)",
    "RET (ic cekis sayisi fazlaydi)",
)


def _puan(kat: int, gerekce: str, tohum: int | None) -> int:
    govde = f"{kat}|{gerekce.strip().lower()}|{tohum if tohum is not None else ''}"
    ozet = hashlib.sha256(govde.encode("utf-8")).hexdigest()
    return int(ozet[:8], 16)


def muzakere(kat: int, gerekce: str, tohum: int | None = None) -> dict:
    if kat < -2 or kat > 40:
        raise ValueError("bu binada o kat yok, hayal urunu dilekce iade")
    if not gerekce.strip():
        raise ValueError("gerekcesiz kapı konusmaz, form eksik")

    rng = random.Random(_puan(kat, gerekce, tohum))
    ic_cekis = rng.randint(0, 4)
    cay = rng.choice(["geldi", "gelmedi", "bitmisti", "demlik kacmis"])
    karar = KARARLAR[rng.randrange(len(KARARLAR))]
    if ic_cekis >= 3:
        karar = "RET (ic cekis sayisi fazlaydi)"
    elif cay == "geldi" and "lutfen" in gerekce.lower():
        karar = "KAPALI (isteksiz)"

    tutanak = textwrap.dedent(
        f"""\
        AKMP-7 OTURUM TUTANAGI
        ---------------------------
        kat            : {kat}
        gerekce        : {gerekce.strip()}
        ic cekis       : {ic_cekis}
        cay durumu     : {cay}
        karar          : {karar}
        dipnot         : kapi bir taraf, siz diger taraf, ikisi de gec kaldi
        """
    ).rstrip()
    return {
        "kat": kat,
        "karar": karar,
        "ic_cekis": ic_cekis,
        "cay": cay,
        "tutanak": tutanak,
    }


def gizli_ek() -> str:
    return (
        "EK-C (dolap arkasindan cikti, resmi gorunur, resmi degildir)\n"
        + _EK_C
        + "\n\nnot: bu satir parti tutmaz. ayni asansorde herkes kendi katinda iner."
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Asansor kapi ile resmi muzakere")
    p.add_argument("--kat", type=int, default=3, help="inmek veya cikmak istediginiz kat")
    p.add_argument("--gerekce", default="toplantıya gec kalırsam slayt intikam alir", help="dilekce metni")
    p.add_argument("--tohum", type=int, default=None, help="ayni tutanak icin sabit tohum")
    p.add_argument("--demo", action="store_true", help="uc ornek oturum kos")
    p.add_argument("--gizli", action="store_true", help="ek-c protokolunu ac")
    args = p.parse_args(argv)

    if args.gizli:
        print(gizli_ek())
        print()

    if args.demo:
        ornekler = [
            (0, "zemin katta bekleyen kargo beni kisi yerine koydu"),
            (7, "lutfen kapan, sunum slaytı intikam alir"),
            (13, "bu kat yok deniyor ama dugme var"),
        ]
        for kat, gerekce in ornekler:
            print(muzakere(kat, gerekce, tohum=7)["tutanak"])
            print()
        return 0

    sonuc = muzakere(args.kat, args.gerekce, args.tohum)
    print(sonuc["tutanak"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"iade: {exc}", file=sys.stderr)
        raise SystemExit(2)
