import pyautogui

from .capture import screenshot
from .reconginze import template_match
import time

from .ocr import ocr2box


def Click(x,y):
    pyautogui.click(x,y)
def LClick(x,y):
    pyautogui.leftClick(x,y)
def RClick(x,y):
    pyautogui.rightClick(x,y)
def DClick(x,y):
    pyautogui.doubleClick(x,y)
def Send(text):
    pyautogui.typewrite(text)
def Press(key):
    pyautogui.press(key)
def LongClick(s):
    pyautogui.mouseDown()
    time.sleep(s)
    pyautogui.mouseUp()
def tclick(template: str) -> None:
    matching_positions, image = template_match(screenshot(), template, threshold=0.8)

    if len(matching_positions) == 0:
        raise ValueError("No matching positions found")

    # 点击第一个找到的
    pos = matching_positions[0]
    x, y = pos[0] + pos[2] / 2, pos[1] + pos[3] / 2
    pyautogui.click(x, y)
def tlclick(template: str) -> None:
    matching_positions, image = template_match(screenshot(), template, threshold=0.8)

    if len(matching_positions) == 0:
        raise ValueError("No matching positions found")

    # 点击第一个找到的
    pos = matching_positions[0]
    x, y = pos[0] + pos[2] / 2, pos[1] + pos[3] / 2
    pyautogui.leftClick(x, y)
def trcick(template: str) -> None:
    matching_positions, image = template_match(screenshot(), template, threshold=0.8)

    if len(matching_positions) == 0:
        raise ValueError("No matching positions found")

    # 点击第一个找到的
    pos = matching_positions[0]
    x, y = pos[0] + pos[2] / 2, pos[1] + pos[3] / 2
    pyautogui.rightClick(x, y)

def dclick(template: str) -> None:
    matching_positions, image = template_match(screenshot(), template, threshold=0.8)

    if len(matching_positions) == 0:
        raise ValueError("No matching positions found")

    # 点击第一个找到的
    pos = matching_positions[0]
    x, y = pos[0] + pos[2] / 2, pos[1] + pos[3] / 2
    pyautogui.doubleClick(x, y)

def Swap(pos: list[int], pos2: list[int]) -> None:
    pyautogui.moveTo(pos[0], pos[1], 0.5)
    pyautogui.dragTo(pos2[0], pos2[1], 0.5)

def tswap(template:str,direct:list[int])->None:
    matching_positions, image = template_match(screenshot(), template, threshold=0.8)
    if len(matching_positions) == 0:
        raise ValueError("No matching positions found")
    pos = matching_positions[0]
    x, y = pos[0] + pos[2] / 2, pos[1] + pos[3] / 2
    pyautogui.moveTo(x, y, 0.5)
    pyautogui.dragRel(direct[0], direct[1], 0.5)

def clicktext(text:str):
    shot = screenshot()
    data = ocr2box(shot)
    # 遍历识别到的文本
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:  # 过滤低置信度文本
            text = data['text'][i]
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]

            # 计算文本中心位置
            center_x = x + w // 2
            center_y = y + h // 2

            # 点击识别到的文字位置
            pyautogui.click(center_x, center_y)
            break
