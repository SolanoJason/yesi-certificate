from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField("Curso", max_length=150)
    duration = models.IntegerField("Duración (meses)")
    hours = models.IntegerField("Horas totales")
    image = models.ImageField("Imagen", upload_to="courses", blank=True, null=True, max_length=255)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self) -> str:
        return f"{self.name}: {self.duration} meses"
