from youtube_autonomous.segments.enhancement.edition_manual.enums import EditionManualTermContext
from youtube_autonomous.segments.enums import ShortcodeStart
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.experimental.elements.enhancement import Enhancement
from yta_general_utils.text.finder import TextFinder, TextFinderMode
from typing import Union
from copy import copy


class EditionManualTerm:
    """
    A term of the edition manual terms book that is used to look
    for matches in the segments text in order to enhance the video
    or audio content.

    See: https://www.notion.so/Diccionarios-de-mejora-155efcba8f0d44e0890b178effb3be84?pvs=4
    """
    _term: str = None
    """
    The text of the term.
    """
    _mode: TextFinderMode = None
    """
    The mode in which the term must be searched.
    """
    _context: EditionManualTermContext = None
    """
    The context in which the term must be applied.

    This means, if this term is for a 'sport' context
    or similar, can only be used in that context.
    """
    _enhancements: list[Enhancement, dict] = None
    """
    The list of enhancements that must be applied when
    the term is found.
    """

    @property
    def term(self):
        # TODO: Explain the term
        return self._term
    
    @term.setter
    def term(self, term: str):
        if not term:
            raise Exception('no "term" provided.')
        
        if not isinstance(term, str):
            raise Exception('The "term" parameter provided is not a string.')
        
        self._term = term

    @property
    def mode(self):
        # TODO: Explain the term
        return self._mode
        
    @mode.setter
    def mode(self, mode: Union[TextFinderMode, str]):
        TextFinderMode.to_enum(mode)

        self._mode = mode

    @property
    def context(self):
        # TODO: Explain the term
        return self._context
    
    @context.setter
    def context(self, context: Union[EditionManualTermContext, str]):
        EditionManualTermContext.to_enum(context)

        self._context = context

    @property
    def enhancements(self):
        return self._enhancements
    
    @enhancements.setter
    def enhancements(self, enhancements: list[Enhancement, dict]):
        # TODO: Make some checkings and improvements
        if not enhancements:
            enhancements = []

        # These enhancements should have been validated before when
        # the EditionManual is accepted, so now we consider them as
        # valids

        # Here 'enhancements' are only dicts

        # # We turn dicts to EnhancementElement if necessary
        # obj_enhancements = []
        # for enhancement in enhancements:
        #     if not isinstance(enhancement, EnhancementElement) and not issubclass(enhancement.__class__, EnhancementElement):
        #         obj_enhancements.append(EnhancementElement.get_class_from_type(enhancement['type'])(enhancement['type'], EnhancementElementStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD, EnhancementElementDuration.SHORTCODE_CONTENT, enhancement['keywords'], enhancement.get('url', ''), enhancement.get('filename', ''), enhancement['mode']))
        #     else:
        #         obj_enhancements.append(enhancement)

        self._enhancements = enhancements

    def __init__(self, term: str, mode: str, context: str, enhancements: list[dict]):
        self.term = term
        self.mode = mode
        self.context = context
        self.enhancements = enhancements

    @staticmethod
    def init_from_dict(dict: dict):
        """
        Validates the provided 'dict' that must be a 'key:dict' pair 
        containing the term and its structure. It will raise an 
        Exception if something is wrong or will return a
        EditionManualTerm if everything is ok.
        """
        ElementParameterValidator.validate_edition_manual_term(dict)

        term, dict = dict
        
        return EditionManualTerm(term, dict['mode'], dict['context'], dict['enhancements'])
    
    def search(self, transcription: list[dict]):
        """
        Searches the term in the provided 'transcription' text and, if
        found, returns the corresponding Enhancements with the processed
        duration (if it is possible to process it).

        This method returns the list of enhancement elements that should
        be applied, according to the provided 'transcription', as dict
        elements.
        """
        ElementParameterValidator.validate_transcription_parameter(transcription)

        # TODO: 'transcription' must be the list of words
        # with their 'start' and 'end'

        text = ' '.join(transcription_word['text'] for transcription_word in transcription)
        term = self.term

        enhancements_found = []
        terms_found = TextFinder.find_in_text(term, text, mode = self.mode)
        for term_found in terms_found:
            match_first_word_index = term_found[0]
            match_last_word_index = term_found[1]

            for term_enhancement in self.enhancements:
                enhancement_found = copy(term_enhancement)
                # If only one term, we cannot use this strategy below so we 
                # use another strategy
                if enhancement_found['start'] == ShortcodeStart.END_OF_FIRST_SHORTCODE_CONTENT_WORD.value and match_first_word_index == match_last_word_index:
                    enhancement_found['start'] = ShortcodeStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD.value

                # Here we need to transform string 'start' and 'duration'
                # into their real numeric values
                start = None
                duration = None

                if enhancement_found['start'] == ShortcodeStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD.value:
                    start = transcription[match_first_word_index]['start']
                    duration = transcription[match_last_word_index]['end'] - start
                elif enhancement_found['start'] == ShortcodeStart.MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD.value:
                    start = (transcription[match_first_word_index]['start'] + transcription[match_first_word_index]['end']) / 2
                    duration = (transcription[match_last_word_index]['start'] + transcription[match_last_word_index]['end']) / 2 - start
                elif enhancement_found['start'] == ShortcodeStart.END_OF_FIRST_SHORTCODE_CONTENT_WORD.value:
                    start = transcription[match_first_word_index]['end']
                    duration = start - transcription[match_last_word_index]['start']

                if start is None or duration is None:
                    raise Exception('Something went wrong when applying a EditionManualTerm.')

                enhancement_found['start'] = start
                enhancement_found['duration'] = duration
                
                # TODO: Should I turn this into a Enhancement object (?)
                # It is a dict right here
                enhancements_found.append(enhancement_found)

        return enhancements_found


"""
"Lionel Messi": {
    "mode": "exact",
    "context": "generic",
    "enhancements": [
        {
            "type": "sticker",
            "keywords": "lionel messi portrait",
            "url": "",
            "filename": "",
            "mode": "overlay"
        }
    ]
}
"""