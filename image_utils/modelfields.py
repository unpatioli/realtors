from django.db import models

class ResizedImageField(models.ImageField):
    def __init__(self, dimensions, **kwargs):
        self.dimensions = dimensions
        super(ResizedImageField, self).__init__(**kwargs)
        
    def save_form_data(self, instance, data, name=None):
        import os
        import hashlib
        from StringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
        
        from image_utils.process import image_resize
        
        if data and isinstance(data, UploadedFile):
            image = image_resize(data, self.dimensions)
            new_image = StringIO()
            image.save(new_image, 'JPEG', quality=85)
            if not name:
                name = hashlib.md5(new_image.getvalue()).hexdigest()
            full_name = "%s.jpg" % name
            data = SimpleUploadedFile(full_name, new_image.getvalue(), data.content_type)
            
            # Remove previous image
            try:
                previous = getattr(instance, self.name).path
                if os.path.isfile(previous):
                    os.remove(previous)
            except (AttributeError, ValueError):
                pass
        super(ResizedImageField, self).save_form_data(instance, data)
    

