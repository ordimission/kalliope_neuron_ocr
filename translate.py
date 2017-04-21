import logging

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
from googletranslate import translator
from googletranslate import constants

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Translate(NeuronModule):
    def __init__(self, **kwargs):
        # we don't need the TTS cache for this neuron
        cache = kwargs.get('cache', None)
        if cache is None:
            cache = False
            kwargs["cache"] = cache
        super(Translate, self).__init__(**kwargs)

        self.message = None

        # get parameters form the neuron
        self.lang_out = kwargs.get('lang_out', None)
        self.lang_in = kwargs.get('lang_in', 'auto')
        self.sentence = kwargs.get('sentence', None)

        if self._is_parameters_ok():
            result = translator.translate(self.sentence, dest=self.lang_out, src=self.lang_in).text
            lang_detect = translator.detect(self.sentence).lang

            self.message = {
                "result": result,
                "lang_in": lang_detect,
                "lang_out": self.lang_out
            }

            logger.debug("Translate returned message: %s" % str(self.message))
            self.say(self.message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: InvalidParameterException
        """

        if self.lang_in != 'auto':
            self.lang_in = self.__lang_is_ok(self.lang_in)

        if self.lang_in is None:
            raise InvalidParameterException("Translate needs a lang_in")

        self.lang_out = self.__lang_is_ok(self.lang_out)

        if self.lang_out is None:
            raise InvalidParameterException("Translate needs a lang_out")

        if self.sentence is None:
            raise InvalidParameterException("Translate needs a sentence")

        return True

    @staticmethod
    def __lang_is_ok(lang):
        lang = lang.lower()

        if lang in constants.LANGUAGES:
            return lang

        lang_translate = translator.translate(lang, dest='en', src='auto').text
        try:
            lang_id = constants.LANGUAGES.items()[constants.LANGUAGES.values().index(lang_translate.lower())][0]
            return lang_id
        except KeyError:
            pass
        return None
