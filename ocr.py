import logging

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
from google.cloud import vision

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
        self.image_uri = kwargs.get('image_uri', None)

        if self._is_parameters_ok():
            result = "";
            client = vision.ImageAnnotatorClient()

            with io.open(path, 'rb') as image_file:
                content = image_uri.read()

            image = vision.types.Image(content=content)

            response = client.document_text_detection(image=image)

            for page in response.full_text_annotation.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            word_text = ''.join([
                                symbol.text for symbol in word.symbols
                            ])
                            result.append(word_text)
            self.message = {
                "result": result
            }

            logger.debug("Ocr returned message: %s" % str(self.message))
            self.say(self.message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: InvalidParameterException
        """

        if self.image_uri is None:
            raise InvalidParameterException("Ocr needs an image_uri")

        return True


