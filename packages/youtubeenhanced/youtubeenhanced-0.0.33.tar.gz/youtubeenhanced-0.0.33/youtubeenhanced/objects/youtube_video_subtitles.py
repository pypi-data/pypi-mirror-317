"""
Here comes some peculiarities you should know 
about these subtitles related to Youtube videos.

The first point is that some of the subtitles
types are based on whole sentences and not word
by word, so you cannot obtain the time moment in
which each word is said. For the ones that work
word by word, yes, you can. 

The second point is that the durations that are
shown most of the time are based on the time the
subtitle is shown in the video. This, of course,
doesn't mean that the word or the sentence is 
said during that time. Also, the first line of
subtitles is sometimes shown with a second line,
so the first line duration will show the duration
of the first and second row together, as it is 
shown during all that time.

As we are using the subtitles to know about what
and when they say something in a video, that
duration is not useful for us. By the way, they
use to put the time moment in which a word starts
being said, so we can use that 'start_time' as a
valid one, and use the one of the next word as the
'end_time' of the previous one. 

We are processing the files and obtaining an almost
raw array of 'elements' containing the subtitles
extracted from each file, but then we have to do a
post-process to obtain the elements transformed for
our specific purpose so we can work with them.
"""
from youtubeenhanced.enums import Subtitles
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.file.reader import FileReader
from datetime import timedelta

import xml.etree.ElementTree as ET
import re


class YoutubeVideoSubtitleElement:
    """
    Class that represents one subtitle element
    of a Youtube video. This element is usually
    a single word.

    Attention: the 'duration' time represents
    the time the element is shown as subtitle,
    not the time the element is spoken in the
    video.
    """
    text: str = None
    """
    The text of this subtitle line.
    """
    start_time: int = None
    """
    The start time moment (in ms) of this subtitle
    line in the corresponding video.
    """
    duration: int = None
    """
    The time this subtitle line is shown in the
    corresponding video. This is not the amount of
    time the element is being spoken in the video.
    """

    @property
    def end_time(self):
        """
        The end time (in ms) based on the sum of the
        'start_time' and the 'duration'.
        """
        return round(self.start_time + self.duration, 3)

    def __init__(self, text: str, start_time: int, duration: int):
        self.text = text
        self.start_time = start_time
        self.duration = duration

    def __str__(self):
        return f'[{self.start_time} - {self.end_time}]   {self.text}'

class YoutubeVideoSubtitles:
    """
    Class to represent a Youtube video subtitles,
    contaning all the subtitle lines.

    These subtitles are modified and processed by
    our system to accomplish our objective. We 
    don't want to handle subtitles as they are, we
    want to be able to know what is being said in
    the video to be able to identify the topics, 
    the most interesting things, etc. Our aim is to
    recognize what (and when) is being said in the
    video to be able to enhance it later by our
    software.
    """
    filename: str = None
    """
    The source file name used to obtain the subtitles.
    """
    elements: list[YoutubeVideoSubtitleElement] = None
    """
    The list of all the youtube video subtitles file
    elements processed.
    """
    processed_elements: list[YoutubeVideoSubtitleElement] = None
    """
    The list of all the youtube video subtitles file 
    elements that have been processed and post 
    processed to be able to handle them for our specific
    purpose.
    """

    @property
    def processed_text(self):
        """
        A concatenation of all the words once they have been
        processed. This is useful to extract the topics, the
        key ideas that are being said, etc. This can be sent
        to an AI assistant to analyze it and.

        This is a text formed by joining all the processed
        elements texts (after .strip() is applied), so the
        word index (based on blank space separations) will be
        the same index as in 'processed_elements' attribute.
        """
        return ' '.join([processed_element.text.strip() for processed_element in self.processed_elements])

    def __init__(self, filename: str):
        """
        Parse the provided 'filename' youtube video 
        subtitles file, processes it and detects all
        the subtitle elements.
        """
        if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
            raise Exception('The provided "filename" is not a valid string or filename.')
        
        file_extension = get_file_extension(filename)

        if file_extension not in Subtitles.get_all_values():
            raise Exception(f'The provided "filename" has an extension that is not accepted by our system. Try one of these: {Subtitles.get_all_values_as_str()}')
        
        if file_extension == Subtitles.TYPE_SRV1.value:
            elements = _parse_srv1_file(filename)

            processed_elements = elements.copy()
        elif file_extension == Subtitles.TYPE_SRV2.value:
            elements = _parse_srv2_file(filename)

            processed_elements = elements.copy()
            # We first remove empty elements
            processed_elements = [processed_element for processed_element in processed_elements if processed_element.text]

            # Then we adjust durations for our purpose
            for i in range(1, len(processed_elements)):
                processed_elements[i - 1].duration = processed_elements[i].start_time - processed_elements[i - 1].start_time
        elif file_extension == Subtitles.TYPE_SRV3.value:
            elements = _parse_srv3_file(filename)

            # The duration is not clear for each word in
            # the subtitles. There is a paragraph duration
            # and the 'start_time' for each word, so we
            # will use the next word 'start_time' as the
            # end of the previous one
            processed_elements = elements.copy()
            for i in range(1, len(processed_elements)):
                processed_elements[i - 1].duration = processed_elements[i].start_time - processed_elements[i - 1].start_time
        elif file_extension == Subtitles.TYPE_JSON3.value:
            elements = _parse_json3_file(filename)

            processed_elements = elements.copy()
            for i in range(1, len(processed_elements)):
                processed_elements[i - 1].duration = processed_elements[i].start_time - processed_elements[i - 1].start_time
        elif file_extension == Subtitles.TYPE_TTML.value:
            elements = _parse_ttml_file(filename)

            processed_elements = elements.copy()
        elif file_extension == Subtitles.TYPE_VTT.value:
            elements = _parse_vtt_file(filename)

            processed_elements = elements.copy()
            # When showing the subtitles, the previous
            # sentence is also shown in the upper part
            # of the subtitles, but it has been said
            # previously, so we should remove them to
            # be able to analyze the text correctly.
            for i in range(1, len(processed_elements)):
                processed_elements[i].text = processed_elements[i].text.replace(processed_elements[i - 1].text, '')

        self.filename = filename
        self.elements = elements
        self.processed_elements = processed_elements

    def __str__(self):
        return '\n'.join([element.__str__() for element in self.processed_elements])

__all__ = [
    'YoutubeVideoSubtitleElement',
    'YoutubeVideoSubtitles'
]
        
def _time_to_ms(time_str):
    return int(timedelta(hours = int(time_str[:2]), minutes = int(time_str[3:5]), seconds = int(time_str[6:8]), milliseconds = int(time_str[9:])).total_seconds() * 1000)

def _parse_srv1_file(filename: str):
    if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
        raise Exception('The provided "filename" is not a valid string or filename.')
    
    tree_root = ET.parse(filename).getroot()

    subtitles = [
        YoutubeVideoSubtitleElement(
            text = text_element.text.strip() if text_element.text else '',
            start_time = round(float(text_element.get('start', 0)), 3),
            duration = round(float(text_element.get('dur', 0)), 3)
        ) for text_element in tree_root.findall('.//text')
    ]

    return subtitles

def _parse_srv2_file(filename: str):
    """
    This format handles the subtitles word by word so
    we can handle those words individually, and we can
    also know the specific time moment for each word.

    TODO: Exaplein this maybe in the Enum so we can 
    know in code how each subtitle is.
    """
    if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
        raise Exception('The provided "filename" is not a valid string or filename.')
    
    tree_root = ET.parse(filename).getroot()

    subtitles = [
        YoutubeVideoSubtitleElement(
            text = text_element.text.strip() if text_element.text else '',
            start_time = int(text_element.get('t', 0)),
            duration = int(text_element.get('d', 0))
        ) for text_element in tree_root.findall('.//text')
    ]
    
    return subtitles

def _parse_srv3_file(filename: str):
    if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
        raise Exception('The provided "filename" is not a valid string or filename.')
    
    tree_root = ET.parse(filename).getroot()

    subtitles = []
    for paragraph in tree_root.findall('.//p'):
        paragraph_start_time = int(paragraph.attrib['t'])
        duration = int(paragraph.attrib['d'])
        
        for word in paragraph.findall('s'):
            # Words with no 't' are the first ones and
            # its start_time is the paragraph start_time
            # and the ones with 't', that 't' is the 
            # 'start_time' relative to the paragraph
            relative_word_start_time = int(word.attrib['t']) if 't' in word.attrib else 0
            text = word.text

            subtitles.append(
                YoutubeVideoSubtitleElement(
                    text = text,
                    start_time = paragraph_start_time + relative_word_start_time,
                    # This duration will be changed it later in
                    # post-processing based on the next word
                    # 'start_time'
                    duration = duration
                )
            )

    return subtitles

def _parse_json3_file(filename: str):
    if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
        raise Exception('The provided "filename" is not a valid string or filename.')

    json_data = FileReader.read_json(filename)

    subtitles = []
    for paragraph in json_data.get('events', []):
        paragraph_start_time = paragraph.get('tStartMs', 0)
        paragraph_duration = paragraph.get('dDurationMs', 0)
        for word in paragraph.get('segs', []):
            relative_word_start_time = int(word['tOffsetMs']) if 'tOffsetMs' in word else 0
            text = word['utf8']
            # We drop any '\n' word as we don't care
            if text == '\n':
                continue

            subtitles.append(
                YoutubeVideoSubtitleElement(
                    text = text,
                    start_time = paragraph_start_time + relative_word_start_time,
                    # TODO: This must be updated in the post-processing
                    duration = paragraph_duration
                )
            )

    return subtitles

def _parse_vtt_file(filename: str):
    # TODO: We need to fix an error with the processing
    # that ends generating an empty line followed by a
    # line without blank spaces. Both of them should not
    # be there, but they are (see Notion for more info)
    if not PythonValidator.is_string(filename) or not FileValidator.is_file(filename):
        raise Exception('The provided "filename" is not a valid string or filename.')
    
    content = FileReader.read(filename)

    def clean_text_tags(text: str):
        return re.sub(r'<[^>]+>', '', text).strip()
        #return re.sub(r'<.*?>', '', text).strip()
    
    # We remove the first 3 header lines
    content = '\n'.join(content.splitlines()[3:])
    
    # Remove comments, empty lines or headers and a
    # text we don't want nor need
    content = content.strip()
    content = content.replace(' align:start position:0%', '')

    # Split the content in blocks according to time line
    subtitle_blocks = re.split(r'\n(?=\d{2}:\d{2}:\d{2}\.\d{3})', content)
    
    subtitles = []
    for block in subtitle_blocks:
        lines = block.splitlines()

        # First row is time
        time_range = lines[0].split(' --> ')
        start_time_str = time_range[0].strip()
        end_time_str = time_range[1].strip()

        start_time = _time_to_ms(start_time_str)
        end_time = _time_to_ms(end_time_str)
        duration = end_time - start_time
        
        # Next rows are the text
        text_segments = [line.strip() for line in lines[1:]]

        # Clean tags and unify
        full_text = ' '.join([clean_text_tags(text) for text in text_segments])

        # The sentences with duration 10 are the ones 
        # that contain the new sentence that is said
        # in the video, so those texts are the ones we
        # must keep for our purpose.
        if duration == 10:
            subtitles[-1] = YoutubeVideoSubtitleElement(full_text, subtitles[-1].start_time, subtitles[-1].duration + 10)
        else:
            subtitles.append(YoutubeVideoSubtitleElement(full_text, start_time, duration))
    
    return subtitles

def _parse_ttml_file(filename: str):
    tree_root = ET.parse(filename).getroot()

    # This is the namespace used in this kind of file
    namespace = {'tt': 'http://www.w3.org/ns/ttml'}

    # Look for paragraphs containing it
    subtitles = []
    for p in tree_root.findall('.//tt:body//tt:div//tt:p', namespace):
        start_time_str = p.get('begin')
        end_time_str = p.get('end')
        
        if start_time_str and end_time_str:
            start_time = _time_to_ms(start_time_str)
            end_time = _time_to_ms(end_time_str)
            duration = end_time - start_time

            text = ''.join(p.itertext()).strip()

            # Guardamos el subtítulo como un objeto
            subtitles.append(YoutubeVideoSubtitleElement(text, start_time, duration))
    
    return subtitles