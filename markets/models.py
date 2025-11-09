from django.db import models
from django.utils import timezone
from livebazar.models import Costumer


class Product(models.Model):
    CATEGORIES = [
        ("meva", "Meva-sabzavotlar"),
        ("gosht", "Go‘sht va parranda mahsulotlari"),
        ("sut", "Sut va sut mahsulotlari"),
        ("non", "Non va un mahsulotlari"),
        ("ichimlik", "Ichimliklar"),
        ("shakar", "Shakar va shirinliklar"),
        ("ziravor", "Oziq-ovqat ziravorlari"),
        ("uy", "Uy-ro‘zg‘or buyumlari"),
        ("texnika", "Maishiy texnika"),
        ("kiyim", "Kiyim-kechak"),
        ("gozallik", "Go‘zallik va parvarish vositalari"),
        ("qurilish", "Qurilish mollari"),
        ("avto", "Avto ehtiyot qismlar"),
        ("elektronika", "Elektronika"),
        ("hayvon", "Hayvonlar uchun mahsulotlar"),
    ]

    seller = models.ForeignKey(Costumer, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150, verbose_name="Mahsulot nomi")
    description = models.TextField(verbose_name="Mahsulot tavsifi")
    category = models.CharField(max_length=50, choices=CATEGORIES, verbose_name="Kategoriya")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi (so‘mda)")
    discount = models.PositiveIntegerField(default=0, verbose_name="Chegirma (%)")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Mavjud soni")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Rasm")
    location = models.CharField(max_length=100, verbose_name="Joylashuv (masalan: Samarqand bozor)")
    is_available = models.BooleanField(default=True, verbose_name="Sotuvda bormi?")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price} so'm"

    @property
    def final_price(self):
        """Chegirmadan keyingi narxni hisoblaydi"""
        if self.discount > 0:
            return round(self.price - (self.price * self.discount / 100), 2)
        return self.price
