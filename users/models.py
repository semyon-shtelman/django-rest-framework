from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Course, Lesson

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватарка')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    PAYMENT_CASH = 'cash'
    PAYMENT_TRANSFER = 'transfer'

    PAYMENT_CHOICES = [
        (PAYMENT_CASH, 'наличные'),
        (PAYMENT_TRANSFER, 'перевод')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Оплаты',
    )
    date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name='payments',
        verbose_name='курс',
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        related_name='payments',
        verbose_name='урок',
        null=True,
        blank=True
    )
    amount = models.IntegerField()
    method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default=PAYMENT_TRANSFER,
        verbose_name='Способ оплаты'
    )

    def __str__(self):
        return f'{self.user.username} - {self.course if self.course else self.lesson}- {self.amount}'

    def clean(self):
        if self.course and self.lesson:
            raise ValueError('Нельзя оплатить одновременно курс и урок')
        if not self.course and not self.lesson:
            raise ValueError('Должен быть указан либо курс, либо урок')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'