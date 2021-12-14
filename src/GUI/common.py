import time
import tkinter
from tkinter.font import Font

text_pad: tkinter.Text


def write_text(output):
    """
    输出文本到已绑定文本框

    :param output: 输出内容
    :return:
    """
    global text_pad
    text_pad.config(state=tkinter.NORMAL)
    text_pad.delete('1.0', tkinter.END)
    text_pad.insert(tkinter.END, output)
    text_pad.see(tkinter.END)
    text_pad.config(state=tkinter.DISABLED)


def get_ft(size, font_type='微软雅黑', weight=tkinter.NORMAL):
    """
    生成字体

    :param size: 大小
    :param font_type: 字体
    :param weight: 字体粗细
    :return:
    """
    return Font(family=font_type, size=size, weight=weight)
