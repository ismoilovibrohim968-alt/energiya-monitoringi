"""4-VARIANT. Energiya monitoringi — elektr sarfini tahlil qilish moduli.

Boshlang'ich shartlar:
    - kunlik sarf kWh da beriladi;
    - me'yor = 10 kWh/kun;
    - davr = 30 kun;
    - ogohlantirish chegarasi me'yordan 20% yuqori (10 * 1.2 = 12 kWh).
"""

MEYOR = 10.0                                   # kWh/kun
DAVR = 30                                      # kun
OGOHLANTIRISH_FOIZI = 20                       # %
OGOHLANTIRISH_CHEGARASI = MEYOR * (1 + OGOHLANTIRISH_FOIZI / 100)   # 12.0 kWh
MAKS_REAL_SARF = 200.0                         # kWh/kun — xonadon uchun mantiqiy yuqori chegara


# ---------------------------------------------------------------------------
# Yordamchi: qiymatni tekshirish (birlik, bo'sh qiymat, noto'g'ri tur)
# ---------------------------------------------------------------------------
def tekshir_qiymat(qiymat, birlik="kWh"):
    """Bitta kunlik qiymatni tekshiradi va float qaytaradi.

    None yoki bo'sh satr -> None (bo'sh qiymat, keyin tashlab yuboriladi).
    Wh birligida berilsa -> kWh ga o'tkaziladi.
    Manfiy, son bo'lmagan yoki haddan katta qiymat -> ValueError.
    """
    if qiymat is None or (isinstance(qiymat, str) and qiymat.strip() == ""):
        return None
    if isinstance(qiymat, bool):
        raise ValueError(f"Mantiqiy qiymat sarf bo'la olmaydi: {qiymat!r}")
    try:
        son = float(qiymat)
    except (TypeError, ValueError):
        raise ValueError(f"Son emas: {qiymat!r}")
    if son != son:                              # NaN tekshiruvi
        return None

    if birlik == "Wh":
        son = son / 1000
    elif birlik != "kWh":
        raise ValueError(f"Noma'lum birlik: {birlik!r} (faqat 'kWh' yoki 'Wh')")

    if son < 0:
        raise ValueError(f"Sarf manfiy bo'lishi mumkin emas: {son}")
    if son > MAKS_REAL_SARF:
        raise ValueError(f"Sarf mantiqan juda katta: {son} kWh (birlikni tekshiring)")
    return son


# ---------------------------------------------------------------------------
# 1-topshiriq: kunlik va oylik sarf, me'yordan oshishni aniqlash
# ---------------------------------------------------------------------------
def kun_holati(sarf):
    """Bitta kun holatini zanjirli taqqoslash va and/or bilan aniqlaydi."""
    if 0 <= sarf <= MEYOR:                                  # zanjirli ifoda
        return "me'yorda"
    elif MEYOR < sarf < OGOHLANTIRISH_CHEGARASI:            # zanjirli ifoda
        return "me'yordan biroz yuqori"
    elif sarf >= OGOHLANTIRISH_CHEGARASI:
        return "OGOHLANTIRISH"
    return "noma'lum"


def meyordan_oshdimi(sarf):
    return sarf > MEYOR and sarf >= 0


def ogohlantirish_kerakmi(sarf):
    # >= ishlatiladi: aynan 12.0 kWh ham ogohlantirish
    return sarf >= OGOHLANTIRISH_CHEGARASI


def oylik_holat(oylik_sarf, kunlar=DAVR):
    oylik_meyor = MEYOR * kunlar
    oylik_chegara = OGOHLANTIRISH_CHEGARASI * kunlar
    if oylik_sarf <= oylik_meyor:
        return "oylik sarf me'yorda"
    elif oylik_meyor < oylik_sarf < oylik_chegara:
        return "oylik sarf me'yordan yuqori"
    return "oylik OGOHLANTIRISH"


# ---------------------------------------------------------------------------
# 2-topshiriq: 30 kunlik ro'yxat statistikasi
# ---------------------------------------------------------------------------
def tozalash(sarflar, birlik="kWh"):
    """Ro'yxatni tekshiradi: bo'sh qiymatlarni tashlaydi, noto'g'rilarida xato beradi."""
    if not isinstance(sarflar, (list, tuple)):
        raise TypeError("Sarflar ro'yxat (list/tuple) bo'lishi kerak")
    toza = []
    for q in sarflar:
        v = tekshir_qiymat(q, birlik)
        if v is not None:
            toza.append(v)
    return toza


def statistika(sarflar, birlik="kWh"):
    """Jami, o'rtacha, maksimal, me'yordan oshgan va ogohlantirish kunlarini qaytaradi."""
    toza = tozalash(sarflar, birlik)
    bosh_kunlar = len(sarflar) - len(toza)
    if not toza:
        return {"kunlar": 0, "bosh_kunlar": bosh_kunlar, "jami": 0.0,
                "ortacha": None, "maksimal": None, "oshgan_kunlar": 0,
                "ogohlantirish_kunlar": 0}
    jami = sum(toza)
    return {
        "kunlar": len(toza),
        "bosh_kunlar": bosh_kunlar,
        "jami": round(jami, 2),
        "ortacha": round(jami / len(toza), 2),
        "maksimal": max(toza),
        "oshgan_kunlar": sum(1 for s in toza if s > MEYOR),
        "ogohlantirish_kunlar": sum(1 for s in toza if s >= OGOHLANTIRISH_CHEGARASI),
    }


# ---------------------------------------------------------------------------
# 4-topshiriq: me'yorga nisbatan foiz o'zgarish (nolga bo'lishdan himoya)
# ---------------------------------------------------------------------------
def foiz_ozgarish(sarf, meyor=MEYOR):
    """((sarf - meyor) / meyor) * 100. Meyor 0 bo'lsa None qaytaradi."""
    if meyor == 0:
        return None                     # nolga bo'lish bartaraf etildi
    return round(((sarf - meyor) / meyor) * 100, 2)


# ---------------------------------------------------------------------------
# Namuna ma'lumotlar (30 kun) va hisobot
# ---------------------------------------------------------------------------
NAMUNA = [
    8.5, 9.2, 10.0, 11.4, 12.0, 7.8, 9.9, 13.5, 10.1, 8.0,
    9.5, 11.9, 12.6, 10.0, 6.4, 9.0, 14.2, 10.5, 8.8, 9.7,
    11.0, 12.1, 7.5, 9.3, 10.0, 15.0, 8.9, 9.6, 11.8, 10.2,
]


if __name__ == "__main__":
    print("Kun | Sarf  | Holat                  | Foiz o'zgarish")
    print("-" * 58)
    for i, s in enumerate(NAMUNA, 1):
        print(f"{i:>3} | {s:>5} | {kun_holati(s):<22} | {foiz_ozgarish(s):+.1f}%")
    st = statistika(NAMUNA)
    print("\n30 kunlik statistika:")
    for k, v in st.items():
        print(f"  {k}: {v}")
    print(" ", oylik_holat(st["jami"]))
    print(f"  Oylik foiz o'zgarish: {foiz_ozgarish(st['jami'], MEYOR * DAVR):+.2f}%")
