from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date


class Client(models.Model):
    full_name = models.CharField(
        max_length=200,
        verbose_name='Полное имя'
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Телефон'
    )
    registration_date = models.DateField(
        default=date.today,
        verbose_name='Дата регистрации'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.full_name

    def clean(self):
        # full_name не пустое
        if not self.full_name or self.full_name.strip() == '':
            raise ValidationError({'full_name': 'Полное имя не может быть пустым.'})

        # email — формат (проверяется EmailField, но добавим кастомную проверку)
        if '@' not in self.email:
            raise ValidationError({'email': 'Введите корректный email.'})
        if '.' not in self.email.split('@')[-1]:
            raise ValidationError({'email': 'Введите корректный email с доменом.'})

        # уникальность email уже есть unique=True

        # phone — если указан, должен быть уникальным (уже unique=True, но с null=True)

        # registration_date — не в будущем
        if self.registration_date and self.registration_date > timezone.now().date():
            raise ValidationError({'registration_date': 'Дата регистрации не может быть в будущем.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)