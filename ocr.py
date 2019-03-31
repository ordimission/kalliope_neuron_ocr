import logging
from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
from ocr_google import image_text_detection_google
from ocr_tesseract import image_text_detection_tesseract

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
                result = image_text_detection_tesseract(self.image_path, self.lang)
            if self.engine == 'google':
                result = image_text_detection_google(self.image_path, self.lang)
            self.message = {
                "result": result
            }

            logger.info("Ocr returned message: %s" % str(self.message))
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


