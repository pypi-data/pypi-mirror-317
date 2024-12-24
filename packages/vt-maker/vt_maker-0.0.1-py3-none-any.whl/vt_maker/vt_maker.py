# Copyright (c) 2024, Zhendong Peng (pzd17@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageEnhance, ImageFont


class VideoThumbnailMaker:
    def __init__(self, config):
        self.draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        self.font = ImageFont.truetype(config["font"], size=config["font_size"])

        self.text_color = config["text_color"]
        self.row = config["matrix"]["row"]
        self.col = config["matrix"]["col"]
        self.padding = config["matrix"]["padding"]
        self.background_color = config["background_color"]
        self.block_width = config["matrix"]["block_width"]
        self.width = (self.block_width + self.padding) * self.col + self.padding

        logo = Image.open(config["logo"]["path"]).convert("RGBA")
        width = int(self.block_width / 4)
        self.logo = logo.resize((width, int(logo.size[1] / logo.size[0] * width)))
        alpha = self.logo.split()[-1]
        alpha = ImageEnhance.Brightness(alpha).enhance(config["logo"]["transparency"])
        self.logo.putalpha(alpha)

    @staticmethod
    def get_metadata(filename, container, comment):
        duration = container.duration // 1000000
        video = container.streams.video[0]
        video_codec = video.codec_context.codec.name.upper()
        video_profile = video.codec_context.profile
        video_bit_rate = video.bit_rate // 1000
        video_frame = float(video.average_rate)
        audio = container.streams.audio[0]
        audio_codec = audio.codec_context.codec.name.upper()
        audio_profile = audio.codec_context.profile
        audio_bit_rate = audio.bit_rate // 1000
        audio_lang = audio.metadata.get("language", "und").title()
        return {
            "File Name": f": {os.path.basename(filename)}",
            "File Size": f": {container.size / 1024 / 1024:.2f} MB",
            "Resolution": f": {video.width}x{video.height} / {video_frame:.2f} fps",
            "Duration": f": {duration // 3600:02}:{duration % 3600 // 60:02}:{duration % 60:02}",
            "Video": f": {video_codec} ({video_profile}) :: {video_bit_rate} kb/s, {video_frame:.2f} fps",
            "Audio": f": {audio_codec} ({audio_profile}) :: {audio_bit_rate} kbps, {audio.rate} Hz, {audio.channels} channels :: {audio_lang}",
            "Comment": f": {comment}",
        }

    def create_thumbnail(self, filename, config, output_folder):
        container = av.open(filename)
        # calculate metadata box size
        metadata = VideoThumbnailMaker.get_metadata(filename, container, config["comment"])
        text = "\n".join(metadata.keys())
        left, top, right, bottom = self.draw.textbbox((10, 10), text, font=self.font)
        textbox_width = right - left + 15
        textbox_height = bottom - top + 30
        # calculate image size
        video = container.streams.video[0]
        block_height = int(self.block_width / video.width * video.height)
        height = textbox_height + (block_height + self.padding) * self.row
        # draw metadata keys
        img = Image.new("RGB", (self.width, height), self.background_color)
        ImageDraw.Draw(img).text((10, 10), text, self.text_color, font=self.font)
        # draw metadata values
        text = "\n".join(list(metadata.values()))
        ImageDraw.Draw(img).text((textbox_width, 10), text, self.text_color, font=self.font)
        # draw logo
        img.paste(self.logo, box=(img.size[0] - self.logo.size[0], 0), mask=self.logo)

        # shuffle
        if not config["shuffle"]:
            random.seed(23)
        start_frame = int(video.frames * 0.1)
        end_frame = video.frames - start_frame
        frames = sorted(random.sample(range(start_frame, end_frame), self.row * self.col))
        # draw
        for idx, frame in enumerate(frames):
            container.seek(int(frame / video.average_rate) * 1000000)
            screenshot = next(container.decode(video=0)).to_image()
            x = self.padding + (self.padding + self.block_width) * (idx % self.col)
            y = textbox_height + (self.padding + block_height) * (idx // self.col)
            screenshot = screenshot.resize((self.block_width, block_height), resample=Image.BILINEAR)
            img.paste(screenshot, box=(x, y))
            yield (idx + 1) / (self.row * self.col)
        img.save(f"{output_folder}/{Path(filename).stem}.png")
