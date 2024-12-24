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

import argparse

import yaml
from tqdm import tqdm

from vt_maker import VideoThumbnailMaker


def main():
    parser = argparse.ArgumentParser(description="Make thumbnails (caps, previews) of video file.")
    parser.add_argument("--video", required=True, help="video file")
    parser.add_argument("--config", default="config.yml", help="config yaml file")
    parser.add_argument("--output_folder", default=".", help="thumbnail output folder")
    args = parser.parse_args()

    config = yaml.safe_load(open(args.config, encoding="utf-8"))
    maker = VideoThumbnailMaker(config)
    with tqdm(total=100) as pbar:
        for progress in maker.create_thumbnail(args.video, config, args.output_folder):
            pbar.update(int(progress * 100) - pbar.n)


if __name__ == "__main__":
    main()
