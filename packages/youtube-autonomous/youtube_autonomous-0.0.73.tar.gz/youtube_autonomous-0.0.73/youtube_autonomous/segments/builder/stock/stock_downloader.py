from yta_stock_downloader import Pixabay, Pexels
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.temp import create_temp_filename


class StockDownloader:
    """
    Singleton class.

    This object simplifies the access to our Stock provider platforms.
    It uses our stock library to connecto with different stock 
    platforms directly to download the content.

    This object is used to download stock videos to build the 
    main images that are shown in the videos.

    TODO: Is this actually a singleton class (?)
    """
    __instance = None

    def __new__(cls, ignore_repeated = True):
        if not StockDownloader.__instance:
            StockDownloader.__instance = object.__new__(cls)
        
        return StockDownloader.__instance

    def __init__(self, ignore_repeated = True):
        if not hasattr(self, 'ignore_repeated'):
            self.ignore_repeated = ignore_repeated
            self.pexels_used_video_ids = []
            self.pexels_used_image_ids = []
            self.pexels_ignore_ids = []
            self.pixabay_used_video_ids = []
            self.pixabay_used_image_ids = []
            self.pixabay_ignore_ids = []

    def download_video(self, keywords: str, do_randomize: bool = False, output_filename: str = create_temp_filename('stock.mp4')):
        """
        Searches the provided 'keywords' in the different stock platforms we have 
        looking for videos. This method will download, if any video is found, a 
        video that could be the first one or a random one if 'do_randomize' is
        True.

        This method will return the locally stored filename when downloaded, or
        None if no video is found.
        """
        if not keywords:
            raise Exception('No "keywords" provided.')
        
        if not output_filename:
            output_filename = create_temp_filename('stock.mp4')

        # TODO: What about the sound?
        if do_randomize:
            try:
                downloaded_filename, video = Pexels.download_random_video(keywords, ignore_ids = self.pexels_used_video_ids, output_filename = output_filename)
            except:
                try:
                    downloaded_filename, video = Pixabay.download_random_video(keywords, ignore_ids = self.pixabay_used_video_ids, output_filename = output_filename)
                except:
                    pass
        else:
            try:
                downloaded_filename, video = Pexels.download_first_video(keywords, ignore_ids = self.pexels_used_video_ids, output_filename = output_filename)
            except:
                try:
                    downloaded_filename, video = Pixabay.download_first_video(keywords, ignore_ids = self.pixabay_used_video_ids, output_filename = output_filename)
                except:
                    pass

        if not downloaded_filename:
            return None

        if self.ignore_repeated:
            if PythonValidator.is_instance(video, 'PexelsVideo'):
                self.pexels_used_video_ids.append(video.id)
            elif PythonValidator.is_instance(video, 'PixabayVideo'):
                self.pixabay_used_video_ids.append(video.id)

        return output_filename
    