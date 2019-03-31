try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def image_text_detection_tesseract(filename,iso_language):
    """
    This function will handle the core OCR processing of images.
    """
    l = None
    if iso_language == 'fr' or iso_language.startswith('fr_'):
        l = 'fra'
    if iso_language == 'en' or iso_language.startswith('en_'):
        l = 'eng'
    if l is None:
        text = pytesseract.image_to_string(Image.open(filename))
    else:
        text = pytesseract.image_to_string(Image.open(filename), lang=l)
    # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return filter(lambda x: len(x) > 1, text.split('\n\n'))
