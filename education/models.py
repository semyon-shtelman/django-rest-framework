from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField()
    preview = models.ImageField(upload_to='course/previews/', blank=True, null=True, verbose_name='Превью курса')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField()
    preview = models.ImageField(upload_to='lesson/previews/', blank=True, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
