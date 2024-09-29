from django.db import models

class MyModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Section(models.Model):
    title = models.CharField(max_length=100)

class Story(models.Model):
    headline = models.CharField(max_length=200)
    tease = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)