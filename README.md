# Energiya monitoringi — elektr sarfini tahlil qilish (4-variant)

Kunlik elektr energiyasi sarfini (kWh) me'yor bilan solishtiruvchi Python moduli.

**Boshlang'ich shartlar:** me'yor = 10 kWh/kun, davr = 30 kun, ogohlantirish chegarasi me'yordan 20% yuqori (12 kWh).

## Fayllar

| Fayl | Tavsif |
|---|---|
| `energiya.py` | Asosiy modul: kun holati, 30 kunlik statistika, foiz o'zgarish, qiymatlarni tekshirish |
| `test_energiya.py` | `unittest` testlari: qo'lda hisob bilan taqqoslash, chegaraviy holatlar, noto'g'ri qiymatlar |

## Ishga tushirish

```bash
python energiya.py                     # 30 kunlik hisobot
python -m unittest test_energiya -v    # testlar
```

## Topshiriqlar

1. **Kunlik va oylik sarf** — `kun_holati()`, `oylik_holat()`; `>=`, `<=`, `and` va zanjirli ifodalar (`0 <= sarf <= MEYOR`).
2. **30 kunlik statistika** — `statistika()`: jami, o'rtacha, maksimal, me'yordan oshgan va ogohlantirish kunlari.
3. **Model uchun prompt** — pastda.
4. **Foiz o'zgarish** — `foiz_ozgarish()`: `((sarf - meyor) / meyor) * 100`, me'yor 0 bo'lsa `None` (nolga bo'linmaydi).
5. **Testlar** — qo'lda hisob va dastur natijasi taqqoslangan, 3 ta chegaraviy va 2 ta noto'g'ri qiymat testi.

## Natijalar (namuna ma'lumotlar)

| Ko'rsatkich | Qiymat |
|---|---|
| Jami | 308.4 kWh |
| O'rtacha | 10.28 kWh/kun |
| Maksimal | 15.0 kWh |
| Me'yordan oshgan kunlar | 13 |
| Ogohlantirish kunlari (≥12 kWh) | 6 |
| Oylik o'zgarish | +2.8% (me'yordan yuqori) |

## Test hujjati

| № | Turi | Kirish | Kutilgan natija |
|---|---|---|---|
| 1 | Chegaraviy | 10.0 | "me'yorda", 0% |
| 2 | Chegaraviy | 12.0 / 11.99 | ogohlantirish bor / yo'q, +20% |
| 3 | Chegaraviy | sarf 0; me'yor 0 | −100%; `None` |
| 4 | Noto'g'ri | −3.5 | `ValueError` |
| 5 | Noto'g'ri | "abc" | `ValueError` |

## Prompt (3-topshiriq)

> Sen tajribali Python dasturchisisan. Elektr energiyasi sarfini tahlil qiluvchi modul yoz.
> Kirish: 30 kunlik sarflar ro'yxati (float). Me'yor 10 kWh/kun, ogohlantirish chegarasi me'yordan 20% yuqori (12 kWh).
> 1. Jami, o'rtacha, maksimal, me'yordan oshgan va ogohlantirish kunlari sonini hisobla.
> 2. Birliklarni tekshir: kWh bo'lishi shart, `birlik="Wh"` bo'lsa o'tkaz; kuniga 200 kWh dan katta qiymat — birlik xatosi.
> 3. Bo'sh qiymatlarni (`None`, `""`, NaN) tashlab yubor va sonini qaytar; bo'sh ro'yxatda xato bermasin.
> 4. Manfiy, son bo'lmagan va `bool` qiymatlar uchun aniq xabarli `ValueError` chiqar.
> 5. Foiz o'zgarishni nolga bo'lishdan himoyalab hisobla.
> 6. `unittest` bilan kamida 3 ta chegaraviy va 2 ta noto'g'ri qiymat testini yoz, kutilgan natijalarni izohla.
