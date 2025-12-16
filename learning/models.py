from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Расширенная модель пользователя с ролями"""
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('teacher', 'Преподаватель'),
        ('student', 'Студент'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name='Роль'
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    @property
    def is_teacher(self):
        return self.role == 'teacher' or self.is_admin
    
    @property
    def is_student(self):
        return self.role == 'student'


class Section(models.Model):
    """Раздел курса"""
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name='Владелец'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    
    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Material(models.Model):
    """Материал раздела"""
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name='Раздел'
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Содержание')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    
    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.section.title} - {self.title}"


class Test(models.Model):
    """Тест для материала"""
    material = models.OneToOneField(
        Material,
        on_delete=models.CASCADE,
        related_name='test',
        verbose_name='Материал'
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    passing_score = models.IntegerField(
        default=60,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Проходной балл (%)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.material.title} - {self.title}"


class Question(models.Model):
    """Вопрос теста"""
    QUESTION_TYPES = [
        ('single', 'Один правильный ответ'),
        ('multiple', 'Несколько правильных ответов'),
    ]
    
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Тест'
    )
    text = models.TextField(verbose_name='Текст вопроса')
    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default='single',
        verbose_name='Тип вопроса'
    )
    order = models.IntegerField(default=0, verbose_name='Порядок')
    points = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Баллы'
    )
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.test.title} - {self.text[:50]}"


class Answer(models.Model):
    """Вариант ответа на вопрос"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    text = models.TextField(verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question.text[:30]} - {self.text[:30]}"


class TestResult(models.Model):
    """Результат прохождения теста"""
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Тест'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='test_results',
        verbose_name='Пользователь'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Балл (%)'
    )
    is_passed = models.BooleanField(default=False, verbose_name='Пройден')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата прохождения')
    
    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'
        ordering = ['-completed_at']
        unique_together = [['test', 'user']]
    
    def __str__(self):
        return f"{self.user.username} - {self.test.title} ({self.score}%)"


class UserAnswer(models.Model):
    """Ответ пользователя на вопрос"""
    test_result = models.ForeignKey(
        TestResult,
        on_delete=models.CASCADE,
        related_name='user_answers',
        verbose_name='Результат теста'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос'
    )
    selected_answers = models.ManyToManyField(
        Answer,
        verbose_name='Выбранные ответы'
    )
    
    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
        unique_together = [['test_result', 'question']]
    
    def __str__(self):
        return f"{self.test_result.user.username} - {self.question.text[:30]}"
