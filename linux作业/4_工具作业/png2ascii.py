#!/usr/bin/env python3
"""
PNG to ASCII Art Converter
将PNG图像转换为ASCII字符画
"""

import argparse
import sys
from PIL import Image

# ASCII字符集，从暗到亮排列
ASCII_CHARS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']

def resize_image(image, new_width=100):
    """调整图像大小"""
    width, height = image.size
    ratio = height / width / 1.65  # 1.65是字符的高宽比补偿
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))

def alpha_composite(image):
    """如果图像带透明通道，则与白色背景合并"""
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha_image = image.convert('RGBA')
        background = Image.new('RGB', alpha_image.size, (255, 255, 255))
        background.paste(alpha_image, mask=alpha_image.split()[3])
        return background
    return image.convert('RGB')

def grayify(image):
    """将图像转换为灰度图"""
    return image.convert('L')

def pixels_to_ascii(image, use_color=False):
    """将像素值转换为ASCII字符"""
    if use_color:
        image = alpha_composite(image)
        pixels = list(image.getdata())
        characters = []
        for r, g, b in pixels:
            luminance = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
            index = int(luminance / 255 * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[index]
            characters.append(f"\x1b[38;2;{r};{g};{b}m{char}")
        return characters

    gray_image = grayify(image)
    pixels = list(gray_image.getdata())
    characters = ""
    for pixel in pixels:
        index = int(pixel / 255 * (len(ASCII_CHARS) - 1))
        characters += ASCII_CHARS[index]
    return characters

def convert_to_ascii(image_path, width=100, output_file=None, color=None):
    """转换PNG图像为ASCII字符画"""
    try:
        image = Image.open(image_path)
        image = resize_image(image, width)

        color_enabled = color if color is not None else (output_file is None)
        ascii_art = pixels_to_ascii(image, use_color=color_enabled)

        ascii_art_lines = []
        for i in range(0, len(ascii_art), width):
            line = ''.join(ascii_art[i:i + width])
            if color_enabled:
                line += '\x1b[0m'
            ascii_art_lines.append(line)

        result = "\n".join(ascii_art_lines)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(result)
            print(f"已保存到: {output_file}")
        else:
            print(result)

        return True

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description='将PNG图像转换为ASCII字符画',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  p2a image.png
  p2a image.png -w 80
  p2a image.png -o output.txt
  p2a image.png -w 120 > art.txt
  p2a image.png --no-color
        ''',
        add_help=False
    )
    parser.add_argument('-h', '-?', '--help', action='help',
                        help='显示此帮助信息并退出')
    parser.add_argument('input', help='输入的PNG文件路径')
    parser.add_argument('-w', '--width', type=int, default=100, 
                        help='输出字符画的宽度 (默认: 100)')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='输出文件路径 (默认: 输出到终端)')
    parser.add_argument('--color', dest='color', action='store_true',
                        help='启用彩色输出（如果输出到终端）')
    parser.add_argument('--no-color', dest='color', action='store_false',
                        help='禁用彩色输出')
    parser.set_defaults(color=None)
    
    args = parser.parse_args()
    
    success = convert_to_ascii(args.input, args.width, args.output, args.color)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
