from youtubeenhanced.enums import Subtitles, Language, Quality
from youtubeenhanced.objects.youtube_video_subtitles import YoutubeVideoSubtitles
from yta_multimedia.experimental.text.gemini_ai import GeminiAI
from yta_general_utils.downloader.utils import download_file
from yta_general_utils.file.remover import FileRemover
from yta_general_utils.programming.parameter_validator import NumberValidator
from yta_general_utils.temp import create_temp_filename
from yt_dlp import YoutubeDL
from random import uniform as random_uniform
from typing import Union


class YoutubeVideo:
    """
    An object that represents a Youtube video with all its data and 
    metadata. It just needs the url to load all the information.
    """
    url: str = None
    """
    The video url to watch it. Something like 
    'https://www.youtube.com/watch?v=tVV7ijh01jo'. This url includes
    the id in the string.
    """
    id: str = None
    """
    The video id (that is the one contained in the url 'watch?v={id}')
    """
    # TODO: Explain all parameters, please
    _main_ideas: list[str] = None
    """
    The main ideas of the video extracted from the
    subtitles using AI.
    """
    _summary: str = None
    """
    A summary of the video built from the subtitles
    using AI.
    """

    @property
    def is_available(self):
        """
        Return True if the video is available (and able to 
        get the information and download it) or False if 
        not (if there is no duration attribute set).
        """
        # TODO: I'm not sure that this works as I want, but...
        return self.duration is not None
    
    @property
    def main_ideas(self):
        """
        Uses the subtitles (if available) to know what
        is being said and builds a collection with the
        most important ideas extracted from those
        subtitles based on AI..
        """
        if self._main_ideas is None:
            self._load_ideas_and_summary()
            
        return self._main_ideas
    
    @property
    def summary(self):
        """
        Uses the subtitles (if available) to know what
        is being said and builds a summary of the video
        using AI based on those subtitles.
        """
        if self._summary is None:
            self._load_ideas_and_summary()

        return self._summary

    def __init__(self, url):
        # TODO: Make this work not only with 'url' but with id only
        self.url = url

        ydl_opts = {
            #'listformats': True,
            'format': 'bestaudio/best',
            #'outtmpl': '%(title)s.%(ext)s', # You can change the PATH as you want
            #'download_archive': 'downloaded.txt',
            'noplaylist': True,   
            'quiet': True,
            'no_warnings': True,
            # 'postprocessors': [{
            #     'key': 'FFmpegExtractAudio',
            #     'preferredcodec': 'mp3',
            #     'preferredquality': '192',
            # }],
            #'progress_hooks': [hook]
        }
        self.youtubedl = YoutubeDL(ydl_opts)

        self.__load_data()

        #self.youtubedl.download([url])
        #print(self.video_formats)
        #print(self.audio_formats)
        #print(self.get_best_quality_audio_format(LANGUAGE_SPANISH))
        #print(self.get_best_quality_video_format())

    def __load_data(self):
        """
        Makes a request and loads the data for the specific Youtube video. This will refresh
        url links expiration time.
        """
        # Urls have expiration token, so I do the 'get_data' here to force, with this method
        # to get the data again if outdated, but using only one 'youtubedl' service loaded
        # on __init__ method.
        self.data = self.youtubedl.extract_info(self.url, download = False)

        self.__get_id()
        self.__get_thumbnail()
        self.__get_duration()
        self.__get_description()
        self.__get_views_count()
        self.__get_likes_count()
        self.__get_comments_count()
        self.__get_heatmap()
        self.__get_key_moment()
        self.__get_attribution()
        self.__get_all_subtitles()
        self.__get_all_automatic_subtitles()
        self.__get_all_formats()

        self.__get_video_formats()
        self.__get_audio_formats()

    def __get_id(self):
        self.id = self.data['id']

    def __get_thumbnail(self):
        self.thumbnail = self.data['thumbnail']

    def __get_duration(self):
        self.duration = self.data['duration']

    def __get_description(self):
        self.description = self.data['description']

    def __get_views_count(self):
        self.views = self.data['view_count']

    def __get_likes_count(self):
        self.likes = self.data.get('like_count')

    def __get_comments_count(self):
        self.comments = self.data['comment_count']

    def __get_heatmap(self):
        self.heatmap = self.data['heatmap']

    def __get_key_moment(self):
        """
        This method gets the key moment from description, that is written in a
        specific way so we can read it to our own benefit. This key moment is
        set manually to let our system know in which video second happens the
        most interesting thing of the video. 
        """
        # Read from self.description
        self.key_moment = 0
        if '@@@@@@@@@@' in self.description:
            try:
                # We wrap the key moment in an specific way
                self.key_moment = float(self.description.split('@@@@@@@@@@')[1].strip().split('=')[1])
            except:
                pass

        return self.key_moment

    def __get_attribution(self):
        """
        This method gets the song attribution from description, that is written in
        a specific way so we can read it. This attribution is to know which songs
        we have used in the video so we can add them in our final video, as the
        attribution, when uploaded.

        TODO: We must standarize the way this must be written
        to be read by the method in any project or channel.
        """
        self.attribution = ''
        if 'Attribution is just below' in self.description:
            try:
                self.attribution = self.description.split('Attribution is just below')[1]
            except:
                pass

        return self.attribution

    def get_hottest_moments(self, moments_number, ordered_by_time = False):
        """
        Returns the 'moments_number' hottest moments of the video based on the 'heatmap'
        if existing. If it doesn't exist, it just return None as it can not be calculated.

        This method is calculated on-demand to avoid useless calculations if it won't be
        used.

        If 'ordered_by_time' is True, it will return those X moments but ordered from
        begin to end of the video.

        Each element returned has 'start', 'end' and 'score' (but 'score' is only for internal
        use so you can ignore it).

        This moments are not given always by Youtube. When given, they represent the moments
        that people have played the most of the time. Those hot moments are intervals of time.
        That is the graph you can see when mouse hover the Youtube player timeline.
        """
        if not self.heatmap:
            return None
        
        hottest_moments = [{
            'start': -1,
            'end': -1,
            'score': -1,   
        }]

        for heatmap_moment in self.heatmap:
            # 'start_time', 'end_time' and 'value' (score)
            for index, hot_moment in enumerate(hottest_moments):
                if heatmap_moment['value'] > hot_moment['score']:
                    # TODO: What about moments that collide?
                    hottest_moments.insert(index, {
                        'start': heatmap_moment['start_time'],
                        'end': heatmap_moment['end_time'],
                        'score': heatmap_moment['value']
                    })

                        # If we have more moments than the limit, we remove the last (the less viewed)
                    if len(hottest_moments) > moments_number:
                        hottest_moments.pop()
                    break
            
        if ordered_by_time:
            hottest_moments_ordered_by_time = [{
                'start': 99999999999,
                'end': 99999999999,
                'score': -1,  
            }]

            for hot_moment in hottest_moments:
                for index, moment in enumerate(hottest_moments_ordered_by_time):
                    if hot_moment['start'] < moment['start']:
                        hottest_moments_ordered_by_time.insert(index, hot_moment)
                        break

            # We remove the additional moment that we used in the comparison
            if len(hottest_moments_ordered_by_time) > moments_number:
                hottest_moments_ordered_by_time.pop()

            hottest_moments = hottest_moments_ordered_by_time

        return hottest_moments

    def get_scenes(self, scenes_number, scene_duration):
        """
        Returns 'scenes_number' scenes of 'scene_duration' that are from the video. Each
        of those scenes has 'start' and 'end' attributes to be able to subclip the clip.

        Imagine a video of 10 minutes, and we want 5 ('scenes_number') scenes. We will 
        first crop the video in 5 different scenes of 2 minutes each one. Then, we will
        get only 'scene_duration' seconds of each of those scenes.

        # TODO: This method could be improved by applying some logic strategy to the
        scenes extraction. We could obtain, for each scene, the main event based on
        video analysis, and extract those main scenes. We also could apply one method
        we have in another module that is able to detect the scene changes based on
        high level of pixels change between frames.
        """
        scene_fragment_duration = self.duration / scenes_number
        scenes = []
        for i in range(scenes_number):
            # We calculate the center for our scene
            scene_segment_start = (i * scene_fragment_duration) + (scene_duration / 2)
            scene_segment_end = (scene_segment_start + scene_fragment_duration) - (scene_duration / 2)

            # Generate a random between our valid limits for each segment
            start = random_uniform(scene_segment_start, scene_segment_end)
            scenes.append({
                'start': start,
                'end': start + scene_duration
            })

        return scenes

    def get_hottest_scenes(self, scenes_number: int, scene_duration: float):
        """
        Returns 'scenes_number' scenes of 'scene_duration' that are from the
        video by using the hot moments as scenes (if available). This method
        will raise an Exception if the heatmap is not available, so please
        ensure it is available before calling this method.

        This method returns an array containing elements with 'start' and
        'end' attributes.
        """
        if not NumberValidator.is_positive_number(scenes_number, do_include_zero = False):
            raise Exception('The provided "scenes_number" parameter is not a valid and positive number.')
        
        if not NumberValidator.is_positive_number(scene_duration, do_include_zero = False):
            raise Exception('The provided "scene_duration" parameter is not a valid and positive number.')

        if not self.heatmap:
            raise Exception('Sorry, there is no heatmap available in the provided YoutubeVideo so we cannot obtain the hottest scenes.')
        
        hottest_moments = self.get_hottest_moments(scenes_number, True)
        duration = scene_duration * scenes_number

        # Turn hottest_moments into scenes
        scenes = []
        accumulated_duration = 0
        for index, hot_moment in enumerate(hottest_moments):
            hot_moment_duration = hot_moment['end'] - hot_moment['start']
            start = hot_moment['start'] + (hot_moment_duration / 2) - (scene_duration / 2)

            # Our scene duration can be longer than the hot moment duration 
            # so we need a larger scene encapsulating that hot moment and 
            # this could happend at the begining of the video
            if start < 0:
                start = 0

            end = start + scene_duration

            if end > self.duration:
                end = self.duration
                # TODO: What about our scene group that is longer than the video
                # so we could end with a negative start... Check this please
                start = end - scene_duration

            accumulated_duration += (end - start)

            # We will make sure the set of calculations 'duration' is equal to 
            # the expected one
            if index == (len(hottest_moments) - 1):
                if accumulated_duration > duration:
                    end = end - (accumulated_duration - duration)
                if duration > accumulated_duration:
                    end = end + (duration - accumulated_duration)

            scenes.append({
                'start': start,
                'end': end
            })

        return scenes
    
    def __get_all_subtitles(self):
        self.subtitles = self.data['subtitles']
    
    def get_subtitles(self, language: Language = Language.DEFAULT, format: Subtitles = Subtitles.TYPE_JSON3):
        """
        Return the url of the subtitles file found by the
        provided 'language' and 'format', or None if not
        found.
        """
        language = Language.to_enum(language)
        format = Subtitles.to_enum(format)
        
        if self.subtitles:
            if language == Language.DEFAULT:
                language = list(self.subtitles.keys())[0]

            if language.value in self.subtitles:
                for type in self.subtitles[language.value]:
                    if type['ext'] == format.value:
                        type['language'] = language.value
                        return type

        return None
    
    def download_subtitles(self, language: Language = Language.DEFAULT, format: Subtitles = Subtitles.TYPE_JSON3, output_filename: Union[str, None] = None):
        """
        Download the subtitles, if existing, with the provided
        "language" and "format", or raises an Exception if not
        found. This method returns the final 'output_filename'
        used in the download.
        """
        language = Language.to_enum(language)
        format = Subtitles.to_enum(format)

        subtitles = self.get_subtitles(language, format)

        if not subtitles:
            raise Exception('No subtitles found with the provided "language" and "format".')
        
        if not output_filename:
            output_filename = create_temp_filename(f'subtitles.{format.value}')

        # TODO: Use the custom extension replace class
        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]
        output_filename += '.' + format.value
        
        download_file(subtitles['url'], output_filename)

        return output_filename
    
    def __get_all_automatic_subtitles(self):
        self.automatic_subtitles = self.data['automatic_captions']

    def get_automatic_subtitles(self, language: Language = Language.DEFAULT, format: Subtitles = Subtitles.TYPE_JSON3):
        """
        Returns the automatic subtitles for the provided 'language' and 'format'.

        This method returns None if not found.
        """
        if not language or not format:
            return None
        
        language = language.value
        format = format.value

        if self.automatic_subtitles:
            if language == Language.DEFAULT.value:
                language = list(self.automatic_subtitles.keys())[0]

            if language in self.automatic_subtitles:
                for type in self.automatic_subtitles[language]:
                    if type['ext'] == format:
                        type['language'] = language
                        return type

        return None
    
    def download_automatic_subtitles(self, language: Language = Language.DEFAULT, format: Subtitles = Subtitles.TYPE_JSON3, output_filename: Union[str, None] = None):
        """
        Download the automatic subtitles, if existing, with the
        provided "language" and "format", or raises an Exception
        if not found. This method returns the final
        'output_filename' used in the download.
        """
        language = Language.to_enum(language)
        format = Subtitles.to_enum(format)

        automatic_subtitles = self.get_automatic_subtitles(language, format)

        if not automatic_subtitles:
            raise Exception('No automatic subtitles found with the provided "language" and "format".')

        if not output_filename:
            output_filename = create_temp_filename(f'subtitles.{format.value}')

        # TODO: Use the custom extension replace class
        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]
        output_filename += '.' + format.value
        
        download_file(automatic_subtitles['url'], output_filename)

        return output_filename
    
    # TODO: Maybe get_spanish_subtitles, get_english_subtitles?

    def __get_all_formats(self):
        self.formats = self.data['formats']
    
    def __get_video_formats(self):
        self.video_formats = {}
        for format in self.formats:
            if format['aspect_ratio'] and 'format_note' in format and format['format_note'] != 'storyboard' and format['format_note'] != 'Premium':
                # We customize the format preserving only interesting fields
                self.video_formats[str(format['height'])] = {
                    'format_id': format['format_id'],
                    'url': format['url'],
                    'quality': format['quality'],
                    'width': format['width'],
                    'height': format['height'],
                    'extension': format['ext'],
                    'video_extension': format['video_ext'], # Yes, redundant
                    'fps': format['fps'],
                    'aspect_ratio': format['aspect_ratio'],
                    'vbr': format['vbr'],
                }

    def get_best_quality_video_format(self):
        """
        Returns the best quality video format.
        """
        if len(self.video_formats.keys()) == 0:
            return None
    
        return self.video_formats[sorted(self.video_formats.keys(), key = float, reverse = True)[0]]
    
    def get_video_format(self, quality: Quality = Quality.DEFAULT):
        """
        Returns the video format of the provided 'quality' that is the height we usually associate
        with the video quality (1080 is for 1080p that is 1920x1080).

        If you provide 1080 as 'quality' parameter you will receive the video format of that 
        height, if existing, or None if not.
        """
        if not self.video_formats or len(self.video_formats.keys()) == 0:
            return None
        
        if quality == Quality.DEFAULT:
            quality = sorted(self.video_formats.keys(), key = float, reverse = True)[0]
        else:
            quality = quality.value

        quality = str(quality)
        
        if not quality in self.video_formats:
            # TODO: Here we have a problem. Not all videos in Youtube are 16:9, so 
            # our resolutions (widths) are not always 1920, 2160, etc... (even when
            # Youtube video player shows 2160 it could be other resolution). This
            # happens with this video (https://www.youtube.com/watch?v=UF3AOpkccjs).
            #
            # We also have 'aspect_ratio' field in our self.video_formats, so we can
            # work with it. A video format is like this below:
            #
            # '676': {'format_id': '247', 'url': '[omitted]', 'quality': 8.0, 
            # 'width': 1280, 'height': 676, 'extension': 'webm', 
            # 'video_extension': 'webm', 'fps': 25, 'aspect_ratio': 1.89, 'vbr': 114.113}
            return None
        
        return self.video_formats[quality]

    def download(self, quality: Quality = Quality.DEFAULT, output_filename: Union[str, None] = None):
        """
        Downloads the video in the provided 'quality' quality if existing and stores it
        locally as 'output_filename' with the video format extension, so any extension 
        provided will be ignored.

        This method returns the real output filename that has been downloaded.
        """
        quality = Quality.to_enum(quality)

        video_format = self.get_video_format(quality)

        if not video_format:
            raise Exception('No video found for the provided "quality".')
        
        if not output_filename:
            output_filename = create_temp_filename('video.mp4')

        # TODO: Use the custom extension replace class
        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]
        output_filename += '.' + video_format['video_extension']

        try:
            # I remove the file because youtube-dl will detect it as downloaded and pass
            FileRemover.delete_file(output_filename)
        except:
            pass
        
        # I use the youtubedl download method because it is faster than others
        self.youtubedl = YoutubeDL({
            'outtmpl': output_filename,
            'format': video_format['format_id']
        })
        self.youtubedl.download(self.url)

        return output_filename

    def __get_audio_formats(self):
        self.audio_formats = {}
        for format in self.formats:
            if 'width' in format and not format['width'] and 'height' in format and not format['height']:
                # We first check the language
                if not format['language'] in self.audio_formats:
                    self.audio_formats[format['language']] = {}

                # We customize the format preserving only interesting fields
                self.audio_formats[format['language']][str(format['abr'])] = {
                    'format_id': format['format_id'],
                    'url': format['url'],
                    'quality': format['quality'],
                    'language': format['language'], # Yes, redundant
                    'extension': format['ext'],
                    'audio_extension': format['audio_ext'], # Yes, redundant
                    'abr': format['abr'],
                }

    def get_best_quality_audio_format(self, language: Language = Language.DEFAULT):
        """
        Returns the highest audio (based on quality) available that is for the provided
        'language' language. If 'language' is None, the first language is provided.
        """
        # No audios detected
        if len(self.audio_formats.keys()) == 0:
            return None
        
        language = Language.to_enum(language)

        if language != Language.DEFAULT:
            language = language.value
            # Specific audio requested
            if len(self.audio_formats[language].keys()) == 0:
                return None
        
            if not language in self.audio_formats:
                return None
        else:
            # Default audio is just the first one: simple
            language = list(self.audio_formats.keys())[0]
        
        return self.audio_formats[language][sorted(self.audio_formats[language].keys(), key = float, reverse = True)[0]]

    def download_audio(self, language: Language = Language.DEFAULT, output_filename: Union[str, None] = None):
        """
        Downloads the best audio available for the provided 'language' and stores it locally
        as 'output_filename' with the audio format extension, so any extension provided will
        be ignored.

        This method returns the real output filename that has been downloaded.
        """
        language = Language.to_enum(language)

        audio_format = self.get_best_quality_audio_format(language)

        if not audio_format:
            raise Exception('No audio found for the provided "language".')
        
        if not output_filename:
            output_filename = create_temp_filename('audio.mp3')

        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]
        output_filename += '.' + audio_format['audio_extension']

        try:
            # I remove the file because youtube-dl will detect it as downloaded and pass
            FileRemover.delete_file(output_filename)
        except:
            pass
        
        # I use the youtubedl download method because it is faster than others
        self.youtubedl = YoutubeDL({
            'outtmpl': output_filename,
            'format': audio_format['format_id']
        })
        self.youtubedl.download(self.url)

        return output_filename

    def download_with_audio(self, quality: Quality = Quality.FULL_HD, language: Language = Language.DEFAULT, output_filename: Union[str, None] = 'video.mp4'):
        """
        Downloads the video in the provided 'quality' and with the best quality audio found
        for the provided 'language'.
        """
        quality = Quality.to_enum(quality)
        language = Language.to_enum(language)

        video = self.get_video_format(quality)
        audio = self.get_best_quality_audio_format(language)

        if not video or not audio:
            raise Exception('No video or audio found for the provided "quality" and/or "language".')
        
        if not output_filename:
            output_filename = create_temp_filename('video.mp4')

        if '.' in output_filename:
            output_filename = output_filename.split('.')[0]

        # I will merge them, so I don't need another extension that the merged one
        merged_file_extension = 'mp4'
        output_filename += '.' + merged_file_extension

        try:
            # I remove the file (if existing) because youtube-dl will detect it as
            # previsouly downloaded and will not download it again
            FileRemover.delete_file(output_filename)
        except:
            pass

        # Thank you boss: https://gist.github.com/khalid32/129cdd43d7347601a6515eeb6e1bc2da
        self.youtubedl = YoutubeDL({
            'outtmpl': output_filename,
            'format': video['format_id'] + '+' + audio['format_id'],
            'merge_output_format': merged_file_extension
        })
        self.youtubedl.download(self.url)

        return output_filename
    
    def _load_ideas_and_summary(self):
        """
        Uses the subtitles (if available) to know what
        is being said and builds a summary of the video
        using AI based on those subtitles.
        """
        # We don't want to be loaded again
        if self._main_ideas is not None and self._summary is not None:
            return True
        
        subtitles_filename = self.download_automatic_subtitles(language = Language.SPANISH, format = Subtitles.TYPE_JSON3)
        subtitles = YoutubeVideoSubtitles(subtitles_filename)

        gemini_response = GeminiAI().ask(f'Quiero que actúes como un profesional en la interpretación de subtítulos de vídeos de Youtube, siendo capaz de extraer las ideas principales del vídeo, y de hacer un resumen de unas 100 palabras de las ideas más importantes que se hablan en el vídeo. Quiero que, como respuesta, me devuelvas todo en una lista no enumerada, donde lo último es el párrafo resumen del vídeo, y todas las líneas anteriores son las ideas principales. Estos son los subtítulos del vídeo: {subtitles.processed_text}')

        def handle_gemini_response(gemini_response):
            """
            Handle a Gemini response to a custom prompt in
            which I provided the video subtitles to obtain
            the main ideas and a summary. This response has
            an specific structure that we handle here.

            Here below is an example:

            * Idea 1

            * Idea 2


            Resumen: El vídeo propone cinco maneras para adolescentes de generar ingresos desde casa: creando miniaturas para Instagram, editando vídeos para diversas plataformas, creando un canal de YouTube, gestionando una cuenta de Instagram y utilizando TikTok.  Se enfatiza la importancia de construir un portfolio, la calidad del contenido y la creación de una comunidad en cada plataforma.  Se recomiendan herramientas gratuitas y se anima a comenzar con una sola opción, aprendiendo y expandiendo gradualmente las habilidades y la presencia online.

            """
            lines = gemini_response.splitlines()
            non_empty_lines = [line.strip() for line in lines if line.strip() != ""]
            idea_lines = [line.replace('*', '') for line in non_empty_lines if line.startswith('*')]
            idea_lines = []
            summary = ''
            for line in lines:
                if line.strip() != "":
                    if line.startswith('*'):
                        idea_lines.append(line.replace('*', '').strip())
                    else:
                        summary = line.replace('Resumen:', '').strip()

            return idea_lines, summary
        
        ideas, summary = handle_gemini_response(gemini_response)

        self._main_ideas = ideas
        self._summary = summary
        

