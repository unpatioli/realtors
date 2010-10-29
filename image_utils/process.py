def image_resize(data, output_size):
    from PIL import Image
    
    img = Image.open(data)
    
    if img.mode not in ('L', 'RGB'):
        img = img.convert('RGB')
    
    img.thumbnail(output_size, Image.ANTIALIAS)
    return img

