import os
import sys
from pathlib import Path

import cv2
from moviepy.editor import AudioClip
from moviepy.editor import AudioFileClip
from moviepy.editor import concatenate_audioclips
from moviepy.editor import VideoFileClip

sys.path.append(str(Path(__file__).parent.parent))

from architect_common import ArchitectBase
from architect_common import COVER_DISPLAY_TIME
from config import EXT_MP4
from config import EXT_PNG


class ArchitectPresentationVideoMaker(ArchitectBase):
    '''
    画像と音声ファイルからプレゼン動画を合成するアーキテクト
    sys.argv[4]: メニューから読み込むプレゼンファイルのパス一覧
    sys.argv[5]: メニューから読み込む音声ファイルのパス一覧
    '''
    def __init__(self):
        super().__init__()
        self.presentation_files = self._get_source_section(sys.argv[4])
        self.audio_files = self._get_source_section(sys.argv[5])

    def work(self):
        '''
        手順：
          1. 保存先情報の準備
          2. 画像と音声ファイルの読み込み
          3. 画像だけの仮動画を生成
          4. 画像と音声を合成して最終動画を生成
          5. 動画ファイルの保存先をメニューに追記
          6. 仮動画ファイルを削除
        '''
        super().work()

        work_file = self.output_dir / f"work_video{EXT_MP4}"
        final_file = self.output_dir / f"presentation_video{EXT_MP4}"

        image_files = {
            key: value for key, value in self.presentation_files.items()
            if Path(value).suffix.lower() == EXT_PNG}

        image_list = sorted(list(image_files.values()))
        audio_list = sorted(list(self.audio_files.values()))

        self._create_work_video(image_list, audio_list, work_file)
        self._create_final_video(audio_list, work_file, final_file)

        self._add_menu_items({"presentation_video": str(final_file)})
        work_file.unlink()

    def _create_work_video(self,
                           image_list: list,
                           audio_list: list,
                           work_file: Path):
        '''
        画像と音声ファイルから仮動画を生成
        各画像の表示時間を各読み上げ音声ファイルの長さとする
        ただし最初のカバー画像だけは固定時間とする
        手順：
          1. カバー画像の読み込み
          2. 動画クリップの初期化
          3. カバー画像の表示時間分、カバー画像を書き込み
          4. カバー画像を一覧から削除
          5. 残りの画像と音声について、音声再生時間分、画像を書き込み
          6. 動画ファイルの保存
        '''
        cover_image = cv2.imread(image_list[0])

        height, width, _ = cover_image.shape
        video = cv2.VideoWriter(str(work_file),
                                cv2.VideoWriter_fourcc(*'mp4v'),
                                1,
                                (width, height))

        for _ in range(COVER_DISPLAY_TIME):
            video.write(cover_image)

        image_list.pop(0)

        for image, audio in zip(image_list, audio_list):
            img = cv2.imread(image)
            speech = AudioFileClip(audio)
            for _ in range(round(speech.duration)):
                video.write(img)

        video.release()

    def _create_final_video(self,
                            audio_list: list,
                            work_file: Path,
                            output_file: Path):
        '''
        仮動画と音声を合成して最終動画を生成
        2024-08-29
        最終動画生成中に別の作業動画が生成されるが
        パーミッションエラーを回避するために、
        ディレクトリを変更してから動画生成を行う
        '''
        speech_files = [AudioClip(lambda t: 0, duration=COVER_DISPLAY_TIME)]
        speech_files += [AudioFileClip(value) for value in audio_list]
        final_audio = concatenate_audioclips(speech_files)

        dir_org = os.getcwd()
        os.chdir(str(self.output_dir))
        video = VideoFileClip(str(work_file))
        final_video = video.set_audio(final_audio)
        final_video.write_videofile(str(output_file),
                                    fps=24,
                                    audio_codec='aac',
                                    audio_bitrate='192k')
        os.chdir(dir_org)


def main():
    architect = ArchitectPresentationVideoMaker()
    architect.work()


if __name__ == '__main__':
    main()
