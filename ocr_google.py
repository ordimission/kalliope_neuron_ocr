from google.cloud import vision
import io

def image_text_detection_google(filename,iso_language):
    """
    This function will handle the core OCR processing of images.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(filename, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text
    return filter(lambda x: len(x) > 1, text.split('\n'))
