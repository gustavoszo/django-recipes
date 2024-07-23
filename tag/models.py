from django.db import models
from django.utils.text import slugify
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Campos para a relação genérica

    # COMENTARIO Representa o model que vai ser encaixado aqui
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # COMENTATIO Representa o id do obj do model descrito acima
    # object_id = models.CharField(max_length=255)
    # COMENTARIO Um campo que representa a relação genérica que conhece os dois campos acima
    # content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            count = Tag.objects.filter(name=self.name).count()
            if count != 0:
                slug = f'{slugify(self.name)}-{count}' 
            else:
                slug = slugify(self.name)
            self.slug = slug

        return super().save(*args, **kwargs)
