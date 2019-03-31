import logging
from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
from google.cloud import vision
import io
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Ocr(NeuronModule):
    def __init__(self, **kwargs):
        # we don't need the TTS cache for this neuron
        cache = kwargs.get('cache', None)
        if cache is None:
            cache = False
            kwargs["cache"] = cache
        super(Ocr, self).__init__(**kwargs)

        self.message = None

        # get parameters form the neuron
        self.image_path = kwargs.get('image_path', None)
        self.engine = kwargs.get('engine', 'tesseract')
        self.lang = kwargs.get('lang', None)

        if self._is_parameters_ok():
            result = "";
            if self.engine == 'tesseract':
                result = self.image_text_detection_tesseract()
            if self.engine == 'google':
                result = self.image_text_detection_google()
            self.message = {
                "result": result
            }
            #logger.info("Ocr returned message: %s" % self.message)
            self.say(self.message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: InvalidParameterException
        """

        if self.image_path is None:
            raise InvalidParameterException("Ocr needs an image path")

        return True

    def image_text_detection_google(self):
        """
        This function will handle the core OCR processing of images.
        """
        client = vision.ImageAnnotatorClient()

        with io.open(self.image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.document_text_detection(image=image)
        text = response.full_text_annotation.text
        #return filter(lambda x: len(x) > 1, text.split('\n'))
        return text

    def image_text_detection_tesseract(self):
        """
        This function will handle the core OCR processing of images.
        """
        l = None
        if self.lang == 'fr' or self.lang.startswith('fr_'):
            l = 'fra'
        if self.lang  == 'en' or self.lang.startswith('en_'):
            l = 'eng'
        if l is None:
            text = pytesseract.image_to_string(Image.open(self.image_path))
        else:
            text = pytesseract.image_to_string(Image.open(self.image_path), lang=l)
        # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
        #return filter(lambda x: len(x) > 1, text.split('\n\n')).join('\n')
        return text
