#!/bin/bash
day=$1
osascript -e "                              \
        tell application \"System Events\" to   \
            tell every desktop to               \
                set picture to \"/Users/zhangguodong/Pictures/BingWallpaper/$day\""
des=${day:0:10}
osascript -e "display notification \"$des\" with title \"BingWallpaper\""
