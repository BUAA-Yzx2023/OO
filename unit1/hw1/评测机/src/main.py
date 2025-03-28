import datetime
import os
import re
import subprocess
import sys
import threading
from PIL import Image, ImageSequence
import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BG_COLOR = pygame.Color(118,194,245)

class MainGame():
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.window.fill(BG_COLOR)
        self.framesStart = []
        self.framesStart_dur = 0
        self.frame_index = 0
        self.page = 0
        self.readyPage0 = False
        self.clock = pygame.time.Clock()
        self.long = 1
        self.big = 1
        self.special = 1
        self.results = [testResult('',0) for _ in range(6)]
        self.mergeRect = None
        self.infor = 0
        self.downButton = None
        self.CE = 0
        self.mouseDown = 0
        self.help = 1
        self.waitCom = 0
        self.noTest = 1
        pygame.display.set_caption('昆仑评测')

    def startGame(self):
        while True:
            self.mousePos = pygame.mouse.get_pos()
            if self.page == 0:
                self.blitStartBG()
                self.changeMouse()
            elif self.page == 1:
                self.blitInformation(self.infor)
            self.getEvent()
            pygame.display.update()

    def endGame(self):
        print("GoodBye")
        sys.exit()

    def changeMouse(self):
        if self.page == 0 and self.TestingButton.collidepoint(self.mousePos):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.page == 0 and self.bigOption.collidepoint(self.mousePos):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.page == 0 and self.longOption.collidepoint(self.mousePos):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.page == 0 and self.specialOption.collidepoint(self.mousePos):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.page == 0 and self.helpButtonRect.collidepoint(self.mousePos):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.page == 0 and self.mergeRect is not None and  self.mergeRect.collidepoint(self.mousePos):
            for i in range(6):
                if self.results[i].Rect is not None and self.results[i].Rect.collidepoint(self.mousePos):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.page == 0 and self.compileButton.collidepoint(self.mousePos):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.page == 0 and self.downButton is not None and self.downButton.collidepoint(self.mousePos):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseDown = 1
                self.help = 0
                if self.page==0 and self.compileButton.collidepoint(self.mousePos):
                    thread = threading.Thread(target=self.complie, args=('D:/OOTest/unit1/source',))
                    thread.start()
                elif self.page==0 and self.TestingButton.collidepoint(self.mousePos):
                    self.noTest = 0
                    self.testing()
                elif self.page==0 and self.bigOption.collidepoint(self.mousePos):
                    self.big = 1-self.big
                elif self.page == 0 and self.longOption.collidepoint(self.mousePos):
                    self.long = 1 - self.long
                elif self.page == 0 and self.specialOption.collidepoint(self.mousePos):
                    self.special = 1 - self.special
                elif self.page == 0 and self.downButton is not None and self.downButton.collidepoint(self.mousePos):
                    self.download()
                elif self.page == 0 and self.helpButtonRect.collidepoint(self.mousePos):
                    self.help = 1
                elif self.page == 0 and self.mergeRect is not None and self.mergeRect.collidepoint(self.mousePos):
                    for i in range(6):
                        if self.results[i].Rect.collidepoint(self.mousePos):
                            # print("answer:  ",self.results[i].answer)
                            # print("output:  ",self.results[i].output)
                            self.window.fill((237, 204, 124))
                            self.page = 1
                            self.infor = i
                elif self.page == 1 and self.returnButtonRect.collidepoint(self.mousePos):
                    self.page = 0
            else:
                self.mouseDown = 0

    def blitStartBG(self):
        self.window.fill((175,225,252))
        self.blitHelpButton()
        self.blitButton()
        self.blitTitle()
        self.blitOption()
        self.blitResult()
        self.blitHelp()
        self.blitWaitCompile()
        self.blitWaitRun()

    def blitHelp(self):
        if self.help:
            helpImg = pygame.image.load('img/help.png')
            helpImg = pygame.transform.scale(helpImg,(500,540))
            self.window.blit(helpImg,(500,20))

    def blitButton(self):
        self.currBGImg = pygame.image.load('img/testBG.png').convert_alpha()
        self.currBGImg.set_alpha(200)
        basedLeft = 100
        basedTop = 500
        self.currBGImg = pygame.transform.scale(self.currBGImg, (200, 80))
        self.window.blit(self.currBGImg, (basedLeft, basedTop))
        self.TestingButton = self.drawButton('开始评测',basedLeft+25,basedTop+20)

        self.comImg = pygame.image.load('img/compile.png').convert_alpha()
        self.comImg.set_alpha(200)
        basedLeft = 60
        basedTop = 150
        self.comImg = pygame.transform.scale(self.comImg, (120, 80))
        self.window.blit(self.comImg, (basedLeft, basedTop))
        self.compileButton = self.drawButton('编译', basedLeft + 25, basedTop + 20)

        if self.mergeRect is not None:
            self.downImg = pygame.image.load('img/compile.png').convert_alpha()
            self.downImg.set_alpha(200)
            basedLeft = 600
            basedTop = 500
            self.downImg = pygame.transform.scale(self.downImg, (175, 80))
            self.window.blit(self.downImg, (basedLeft, basedTop))
            self.downButton = self.drawButton('Download', basedLeft + 25, basedTop + 20)

    def drawButton(self, text, x, y):
        # 加载中文字体文件
        font_path = "Font/QingNiao.ttf"  # 替换为你的字体文件路径
        font = pygame.font.Font(font_path, 36)  # 使用支持中文的字体
        button_text = font.render(text, True, (0, 0, 0))  # 渲染文本
        button_rect = button_text.get_rect(topleft=(x, y))
        if button_rect.collidepoint(self.mousePos) :
            button_text = font.render(text, True, (255, 255, 255))  # 渲染文本
        self.window.blit(button_text, button_rect)

        return button_rect

    def blitOption(self):
        self.opImg = pygame.image.load('img/option.png').convert_alpha()
        self.opImg.set_alpha(240)
        basedLeft = 0
        basedTop = 200
        self.opImg = pygame.transform.scale(self.opImg, (550, 305))
        self.window.blit(self.opImg, (basedLeft, basedTop))
        self.bigOption = self.drawOption(basedLeft+400,basedTop+115,1)
        self.longOption = self.drawOption(basedLeft+400,basedTop+167,2)
        self.specialOption = self.drawOption(basedLeft+400,basedTop+219,3)

    def drawOption(self,x,y,i):
        rect_width = 25  # 框的宽度
        rect_height = 25  # 框的高度
        # 绘制白色填充的正方形框
        pygame.draw.rect(self.window, (255, 255, 255), (x, y, rect_width, rect_height))
        condition = (i==1 and self.big==1)or(i==2 and self.long==1)or(i==3 and self.special==1)
        if condition:
            rightImg = pygame.image.load('img/right.png')
            rightImg = pygame.transform.scale(rightImg,(35,40))
            self.window.blit(rightImg,(x-9,y-11))
        # 返回框的 rect 对象
        return pygame.Rect(x, y, rect_width, rect_height)

    def testing(self):
        for i in range(6):
            self.results[i].Str = ''
        threads = []
        for i in range(6):
            thread = threading.Thread(target=self.everyTest, args=(i,))
            threads.append(thread)
            thread.start()

    def everyTest(self,i):
        long = str(self.long)
        big = str(self.big)
        # 运行 dataMaking.py 并捕获输出
        result = subprocess.run(["python", "dataMaking.py", long, big], capture_output=True, text=True,creationflags=subprocess.CREATE_NO_WINDOW)
        input = result.stdout.strip()  # 获取输出
        # print(input)
        answer = getAnswer(input)
        answer = re.sub(r'\n+$', '', answer)
        # print(answer)
        Str = 'CE'
        pro = 0
        tempOutput = 'Compile Error'
        if self.CE == 0:
            output,running = getOutput(input)
            output = re.sub(r'\n+$', '', output)
            tempOutput = output
            if running == 0:
                Str = 'RE'
            else:
                right,pro = check(answer, output)
                if right==1:
                    Str = 'AC'
                else:
                    Str = 'WA'
        self.results[i] = testResult(Str,pro)
        self.results[i].input = input
        self.results[i].output = tempOutput
        self.results[i].answer = answer

    def blitResult(self):
        for i in range(6):
            if self.results[i].Str!='':
                x = 540 + 120 * (i % 3)
                y = 250+120*(i//3)
                self.results[i].Rect = self.drawResult(x,y,self.results[i].Str,self.results[i].pro)
                if self.mergeRect==None:
                    self.mergeRect = pygame.Rect(self.results[i].Rect)
                self.mergeRect = self.mergeRect.union(self.results[i].Rect)

    def drawResult(self,x,y,str,pro):
        rect_width = 100  # 框的宽度
        rect_height = 100  # 框的高度
        color = (255,255,255)
        if str == 'WA':
            color = (255, 0, 0)  # 红色
        elif str == 'RE' or str == 'CE':
            color = (128, 0, 128)  # 紫色
        elif str == 'AC' and pro == 1:
            color = (0, 255, 0)  # 绿色
        elif str == 'AC':
            color = (255, 165, 0)  # 橙色

        # 绘制白色填充的正方形框
        pygame.draw.rect(self.window, color, (x, y, rect_width, rect_height))
        font_path = "Font/QingNiao.ttf"  # 替换为你的字体文件路径
        font = pygame.font.Font(font_path, 48)  # 使用支持中文的字体
        button_text = font.render(str, True, (255, 255, 255))  # 渲染文本
        button_rect = button_text.get_rect(topleft=(x+25, y+25))
        self.window.blit(button_text, button_rect)
        # 返回框的 rect 对象
        return pygame.Rect(x, y, rect_width, rect_height)

    def blitInformation(self,i):
        self.page = 1
        self.blitReturnButton()
        font = pygame.font.Font("Font/Arial.ttf", 72)  # 使用支持中文的字体
        button_text = font.render('Details', True, (0, 0, 0))  # 渲染文本
        button_rect = button_text.get_rect(topleft=(370, 10))
        self.window.blit(button_text, button_rect)
        self.drawWord('Input: ', 20, 150,36)
        self.drawWord(self.results[i].input, 200, 165,24)
        self.drawWord('Output: ', 20, 250,36)
        self.drawWord(self.results[i].output, 200, 265,24)
        self.drawWord('Answer: ', 20, 350, 36)
        self.drawWord(self.results[i].answer, 200, 365, 24)
        self.drawWord('r(x): ', 20, 450, 36)
        if self.results[i].pro==1:
            rx = 1
        elif self.results[i].pro>1.5:
            rx = 0
        else:
            pro = self.results[i].pro
            rx = -31.8239*(pro)**4 + 155.9038*(pro)**3 - 279.2180*(pro)**2 + 214.0743*(pro) - 57.9370
        self.drawWord(str(rx), 200, 465, 24)

    def drawWord(self,Str,x,y,size):
        Str = re.sub('\t','  ',Str)
        length = len(Str)
        font_path = "Font/Arial.ttf"  # 替换为你的字体文件路径
        font = pygame.font.Font(font_path, size)  # 使用支持中文的字体
        if length>60:
            font_path = "Font/QingNiao.ttf"  # 替换为你的字体文件路径
            font = pygame.font.Font(font_path, size)  # 使用支持中文的字体
            Str = '数据较大，请下载至本地查看'
        button_text = font.render(Str, True, (0, 0, 0))  # 渲染文本
        button_rect = button_text.get_rect(topleft=(x, y))
        self.window.blit(button_text, button_rect)

    def blitReturnButton(self):
        self.returnButton = pygame.image.load('img/return.png')
        self.returnButton = pygame.transform.scale(self.returnButton, (80, 90))
        self.window.blit(self.returnButton, (0, 0))
        self.returnButtonRect = self.returnButton.get_rect()
        if self.returnButtonRect.collidepoint(self.mousePos):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)  # 设置鼠标样式为手形
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def blitHelpButton(self):
        self.helpButton = pygame.image.load('img/light.png')
        self.helpButton = pygame.transform.scale(self.helpButton, (60, 60))
        self.window.blit(self.helpButton, (0, 0))
        self.helpButtonRect = self.helpButton.get_rect()

    def download(self):
        print("Download")
        # 目标目录
        data_dir = r"D:\OOTest\unit1\data"
        # 获取当前时间并格式化为年月日时分秒
        current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        folder_name = os.path.join(data_dir, current_time)
        # 创建以当前时间命名的文件夹
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # 在文件夹中创建 6 个 .txt 文件
        for i, result in enumerate(self.results):
            file_name = os.path.join(folder_name, f"{i}.txt")
            with open(file_name, "w", encoding="utf-8") as f:
                # 文件名格式为 index.txt
                f.write(f"Input:\n{self.results[i].input}\n\n")  # 写入 input 内容
                f.write(f"Output:\n{self.results[i].output}\n")  # 写入 output 内容
                f.write(f"Answer:\n{self.results[i].answer}\n\n")  # 写入 answer 内容
        print(f"Files have been saved to {folder_name}")

    def blitTitle(self):
        self.tltleImg = pygame.image.load('img/title.png').convert_alpha()
        self.tltleImg.set_alpha(255)
        basedLeft = 350
        basedTop = 0
        self.tltleImg = pygame.transform.scale(self.tltleImg, (300, 180))
        self.window.blit(self.tltleImg, (basedLeft, basedTop))

    def blitWaitCompile(self):
        if self.waitCom == 1 :
            font_path = "Font/YeZi.ttf"  # 替换为你的字体文件路径
            font = pygame.font.Font(font_path, 24)  # 使用支持中文的字体
            button_text = font.render('正在编译……', True, (255, 255, 255))  # 渲染文本
            button_rect = button_text.get_rect(topleft=(160 + 25, 150 + 45))
            self.window.blit(button_text, button_rect)

    def complie(self, path):
        self.waitCom = 1
        # 定义源文件目录和编译后文件目录
        src_dir = path  # 替换为您的Java源文件目录
        bin_dir = r'D:\OOTest\unit1\Tested_class'  # 替换为您希望编译后的.class文件存放的目录

        # 确保编译后的文件目录存在
        if not os.path.exists(bin_dir):
            os.makedirs(bin_dir)
        # 获取所有.java文件的路径
        # java_files = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.endswith('.java')]

        java_files = []
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith('.java'):
                    java_files.append(os.path.join(root, file))

        # 编译所有.java文件
        compile_command = ['javac', '-d', bin_dir] + java_files
        compile_process = subprocess.run(compile_command, capture_output=True, text=True,
                                         creationflags=subprocess.CREATE_NO_WINDOW)
        # 检查编译是否成功
        self.waitCom = 0
        if compile_process.returncode == 0:
            # print("编译成功！")
            self.CE = 0
            return 1
        else:
            # print("编译失败：")
            # print(compile_process.stderr)
            # exit(1)
            self.CE = 1
            return 0

    def blitWaitRun(self):
        wait = 0
        for i in range(6):
            if self.results[i].Str != '':
                wait += 1
        if wait < 6 and self.noTest==0 :
            font_path = "Font/YeZi.ttf"  # 替换为你的字体文件路径
            font = pygame.font.Font(font_path, 24)  # 使用支持中文的字体
            text = f'正在评测，请耐心等待{wait}/6……'
            button_text = font.render(text, True, (235, 255, 255))  # 渲染文本
            button_rect = button_text.get_rect(topleft=(300 + 20, 500 + 45))
            self.window.blit(button_text, button_rect)

def getAnswer(input_string):
    bin_dir = 'Answer_class'  # 替换为您希望编译后的.class文件存放的目录
    # 运行MainClass
    run_command = ['java', '-cp', bin_dir, 'MainClass']
    run_process = subprocess.run(run_command,input=input_string, capture_output=True, text=True,creationflags=subprocess.CREATE_NO_WINDOW)
    # 输出运行结果
    if run_process.returncode == 0:
        return run_process.stdout
    else:
        # print("程序运行失败：")
        return run_process.stderr

def getOutput(input_string):
    bin_dir = r'D:\OOTest\unit1\Tested_class'
    # 运行MainClass
    run_command = ['java', '-cp', bin_dir, 'MainClass']
    run_process = subprocess.run(run_command, input=input_string, capture_output=True, text=True,creationflags=subprocess.CREATE_NO_WINDOW)
    # 输出运行结果
    if run_process.returncode == 0:
        # print("程序输出：")
        return run_process.stdout,1
    else:
        # print("程序运行失败：")
        return run_process.stderr,0

def check(answer,output):
    if '(' in output or ')' in output:
        return 0,0

    lenOut = len(output)
    lenAns = len(answer)

    output = re.sub(r'\s+', '', output)
    rules = {
        r'\+\+': '+',  # 将 ++ 替换为 +
        r'\-\-': '+',  # 将 -- 替换为 +
        r'\+\-': '-',  # 将 +- 替换为 -
        r'\-\+': '-',  # 将 -+ 替换为 -
        r'\^\+': '^',  # 将 ^+ 替换为 ^
    }
    # 循环化简符号，直到没有重复符号为止
    while True:
        original_expr = output
        for pattern, replacement in rules.items():
            output = re.sub(pattern, replacement, output)
        if original_expr == output:  # 如果没有变化，说明已经化简完成
            break

    pattern = r'^([+-]?(\d+|x)([+\-*^][+-]?(\d+|x))*|(\d+|x))$'

    # # 检查是否符合格式
    if re.match(pattern, output):
        # print("合法",output)
        m = 0
    else:
        print("不合法", output)
        return 0,0

    output = getAnswer(output)
    output = re.sub(r'\s+', '', output)

    isEqual = are_polynomials_equal(answer,output)
    if (isEqual):
        pro = lenOut/lenAns
        return 1,pro
    else:
        return 0,0

def split_polynomial(polynomial):
    """
    按照 + 和 - 分割多项式，提取每一项。
    """
    # 替换减号为 "+-"，以便统一处理
    polynomial = polynomial.replace('-', '+-')
    # 分割多项式
    terms = polynomial.split('+')
    # 去除空项
    terms = [term for term in terms if term.strip()]
    return terms

def parse_term(term):
    # 默认系数为1，指数为1
    coefficient = 1
    exponent = 1
    if 'x' not in term:
        # 常数项
        coefficient = term
        exponent = 0
    else:
        # 包含 x 的项
        if '^' in term:
            # 有指数
            base, exp = term.split('x^')
            base = base.replace('*', '')
            if base == '':
                coefficient = 1
            elif base == '-':
                coefficient = -1
            else:
                coefficient = int(base)
            exponent = int(exp)
        else:
            # 没有指数
            term = term.replace('x','')
            term = term.replace('*', '')
            if term=='':
                coefficient = 1
            elif term == '-':
                coefficient = -1
            else:
                coefficient = int(term)
            exponent = 1

    return coefficient, exponent

def polynomial_to_dict(polynomial):
    terms = split_polynomial(polynomial)
    poly_dict = {}
    for term in terms:
        coefficient, exponent = parse_term(term)
        poly_dict[exponent] = coefficient
    return poly_dict

def are_polynomials_equal(answer, output):
    answer_dict = polynomial_to_dict(answer)
    output_dict = polynomial_to_dict(output)
    return answer_dict == output_dict

def init():
    print("Initializing directories...")
    # 定义目标路径
    base_dir = r"D:\OOTest"
    unit1_dir = os.path.join(base_dir, "unit1")
    source_dir = os.path.join(unit1_dir, "source")
    data_dir = os.path.join(unit1_dir, "data")
    class_dir = os.path.join(unit1_dir, "Tested_class")

    # 检查并创建 OOTest 目录
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Directory created: {base_dir}")
    else:
        print(f"Directory already exists: {base_dir}")
    # 检查并创建 OOTest/unit1 目录
    if not os.path.exists(unit1_dir):
        os.makedirs(unit1_dir)
        print(f"Directory created: {unit1_dir}")
    else:
        print(f"Directory already exists: {unit1_dir}")

        # 检查并创建 OOTest/unit1/source 目录
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        print(f"Directory created: {source_dir}")
    else:
        print(f"Directory already exists: {source_dir}")

        # 检查并创建 OOTest/unit1/data 目录
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Directory created: {data_dir}")
    else:
        print(f"Directory already exists: {data_dir}")

    if not os.path.exists(class_dir):
        os.makedirs(class_dir)
        print(f"Directory created: {class_dir}")
    else:
        print(f"Directory already exists: {class_dir}")

class testResult:
    def __init__(self,Str,pro):
        self.Str = Str
        self.pro = pro
        self.Rect = None
        self.input = None
        self.answer = None
        self.output = None



os.chdir(os.path.dirname(__file__))
init()
MainGame().startGame()
