from django.db import models
from django.utils import timezone

class Recipe(models.Model):
    delicacy = models.CharField(max_length=50, help_text='Enter a name of the delicacy')
    introduction = models.CharField(max_length=1000, help_text='Enter a brief description of the recipe')
    photo = models.ForeignKey('Recipe_Photo', on_delete=models.SET_NULL, null=True, blank=True)
    DELICACY_TYPE_CHOICES = (
        ('a', '開胃菜(appetizer)'),
        ('m', '主餐(main course)'),
        ('sf', '主食(staple food)'),
        ('s', '副菜(side)'),
        ('d', '甜點(dessert)'),
        ('b', '飲品(beverages)'),
    )
    delicacy_type = models.CharField(max_length=5, choices=DELICACY_TYPE_CHOICES, default='a', blank=False)
    
    CATEGORY_CHOICES=(
        ('m','葷(meat)'),
        ('v','純素(vegan)'),
        ('o','蛋奶素(ovo-lacto vegetarian)'),
        ('f','五辛素(Five pungent spices vegan)'),
    )
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='m', blank=False)
    cooking_time = models.PositiveIntegerField(null=True, blank=True)
    servings = models.PositiveIntegerField(default=1)
    reference = models.CharField(max_length=1000, null=True, blank=True)
    memo_text = models.CharField(max_length=100, null=True, blank=True)
    storage_method = models.CharField(max_length=100, null=True, blank=True)
    is_public = models.BooleanField(default=False)  ## False: 食譜為未公開的，除了建立者以外的人無法檢視
    is_draft = models.BooleanField(default=True)  ## True: 食譜為草稿
    upload_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f'<{self.pk}> {self.delicacy}: {self.introduction} / upload_date: {self.upload_date}'

    def delete(self, *args, **kwargs):
        if self.photo:
            self.photo.delete()
        super().delete(*args, **kwargs)

    def get_nutrition_facts(self):
        return self.nutrition_facts_set.all()

    def get_steps(self):
        return self.step_set.all().order_by('step')

    def get_used_ingredients(self):
        return self.used_ingredient_set.all()

class Recipe_Photo(models.Model):
    photo = models.ImageField(upload_to='recipes/delicacy_photos', null=True, blank=True)
    upload_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'<{self.pk}> {self.photo} upload_date: {self.upload_date}'
    
    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)

class Step_Photo(models.Model):
    photo = models.ImageField(upload_to='steps/photos', null=True, blank=True)
    upload_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'<{self.pk}> {self.photo} upload_date: {self.upload_date}'
    
    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)

class Step(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, null=True, blank=True)
    step = models.PositiveSmallIntegerField(default=1)
    photo = models.ForeignKey('Step_Photo', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    notes = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'<{self.pk}> ({self.recipe.pk} {self.recipe.delicacy}) step {self.step}: {self.description} notes:{self.notes} photo:{self.photo}'
    
    def delete(self, *args, **kwargs):
        if self.photo:
            self.photo.delete()
        super().delete(*args, **kwargs)
