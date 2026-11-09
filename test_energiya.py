"""5-topshiriq: qo'lda hisob va dastur natijasini taqqoslash, chegaraviy va noto'g'ri qiymat testlari.
Ishga tushirish:  python -m unittest test_energiya -v
"""
import unittest
from energiya import (NAMUNA, kun_holati, ogohlantirish_kerakmi, statistika,
                      foiz_ozgarish, tekshir_qiymat, oylik_holat)


class QoldaHisobTaqqoslash(unittest.TestCase):
    def test_qolda_hisob(self):
        # Qo'lda hisob (har bir 10 kunlik qator yig'indisi):
        # 1-10: 100.4   11-20: 102.6   21-30: 105.4   -> jami 308.4
        st = statistika(NAMUNA)
        self.assertEqual(st["jami"], 308.4)
        self.assertEqual(st["ortacha"], 10.28)      # 308.4 / 30
        self.assertEqual(st["maksimal"], 15.0)
        self.assertEqual(st["oshgan_kunlar"], 13)    # > 10
        self.assertEqual(st["ogohlantirish_kunlar"], 6)  # >= 12
        self.assertEqual(foiz_ozgarish(308.4, 300), 2.8)


class ChegaraviyHolatlar(unittest.TestCase):
    def test_1_aynan_meyor(self):            # 10.0 -> me'yorda, foiz 0
        self.assertEqual(kun_holati(10.0), "me'yorda")
        self.assertEqual(foiz_ozgarish(10.0), 0.0)

    def test_2_aynan_chegara(self):          # 12.0 -> ogohlantirish (>=)
        self.assertTrue(ogohlantirish_kerakmi(12.0))
        self.assertFalse(ogohlantirish_kerakmi(11.99))
        self.assertEqual(foiz_ozgarish(12.0), 20.0)

    def test_3_nol_sarf_va_nol_meyor(self):  # 0 sarf to'g'ri; 0 me'yor -> None
        self.assertEqual(kun_holati(0), "me'yorda")
        self.assertEqual(foiz_ozgarish(0), -100.0)
        self.assertIsNone(foiz_ozgarish(5, 0))


class NotogriQiymatlar(unittest.TestCase):
    def test_1_manfiy_qiymat(self):
        with self.assertRaises(ValueError):
            tekshir_qiymat(-3.5)

    def test_2_son_emas(self):
        with self.assertRaises(ValueError):
            statistika([9.0, "abc", 11.0])


class Qoshimcha(unittest.TestCase):
    def test_bosh_qiymatlar(self):
        st = statistika([10, None, "", 14])
        self.assertEqual((st["kunlar"], st["bosh_kunlar"], st["jami"]), (2, 2, 24.0))

    def test_wh_birligi(self):
        self.assertEqual(tekshir_qiymat(12500, "Wh"), 12.5)

    def test_birlik_xatosi(self):            # kWh o'rniga Wh yozilgan -> juda katta
        with self.assertRaises(ValueError):
            tekshir_qiymat(12500)

    def test_oylik(self):
        self.assertEqual(oylik_holat(308.4), "oylik sarf me'yordan yuqori")
        self.assertEqual(oylik_holat(360), "oylik OGOHLANTIRISH")


if __name__ == "__main__":
    unittest.main(verbosity=2)
