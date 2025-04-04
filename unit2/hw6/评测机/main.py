import datetime
import os
import re
import shutil
import subprocess
import sys
import threading
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
BG_COLOR = pygame.Color(255,255,255)

class MainGame:
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.window.fill(BG_COLOR)
        self.page = 0
        self.readyPage0 = False
        self.results = [testResult('') for _ in range(6)]
        self.groupResults = [[testResult('') for _ in range(6)] for _1 in range(7) ]
        self.mergeRect = None
        self.infor = 0
        self.downButton = None
        self.CE = 0
        self.mouseDown = 0
        self.help = 1
        self.waitCom = 0
        self.noTest = 1
        self.groupNoTest = 1
        self.groupNum = 0

        pygame.display.set_caption('昆仑评测')

    def startGame(self):
        while True:
            self.mousePos = pygame.mouse.get_pos()
            if self.page == 0 :
                self.blitStartBG()
                self.changeMouse()
            elif self.page == 1:
                pass
            elif self.page == 2:
                self.blitGroupBG()
            self.getEvent()
            pygame.display.update()

    def endGame(self):
        print("GoodBye")
        sys.exit()

    def changeMouse(self):
        if self.page == 0 and self.TestingButton.collidepoint(self.mousePos):
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
                print("down")
                self.mouseDown = 1
                self.help = 0
                if self.page==0 and self.compileButton.collidepoint(self.mousePos):
                    thread = threading.Thread(target=self.complie,args=('D:/OOTest/unit2/source',r'D:/OOTest/unit2/Tested_class'))
                    thread.start()
                elif self.page == 2 and self.compileButton.collidepoint(self.mousePos):
                    self.groupComplie()
                elif self.page==0 and self.TestingButton.collidepoint(self.mousePos):
                    self.noTest = 0
                    self.testing()
                elif self.page==2 and self.TestingButton.collidepoint(self.mousePos):
                    self.groupTesting()
                elif self.page==2 and self.LocalButton.collidepoint(self.mousePos):
                    print(1)
                    self.localTesting()
                elif self.page==0 and self.groupTestingButton.collidepoint(self.mousePos):
                    self.page = 2
                    self.window.fill((255, 254, 254))

                elif self.page == 0 and self.downButton is not None and self.downButton.collidepoint(self.mousePos):
                    self.download()
                elif self.page == 2 and  self.downButton.collidepoint(self.mousePos):
                    self.groupDownload()
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
                elif self.page > 0 and self.returnButtonRect.collidepoint(self.mousePos):
                    self.page = 0

            else:
                self.mouseDown = 0

    def blitStartBG(self):
        # self.window.fill(BG_COLOR)
        img = pygame.image.load('img/startBG.png')
        self.window.blit(img,(0,0))
        self.blitHelpButton()
        self.blitButton()
        self.blitTitle()
        self.blitResult()
        self.blitHelp()
        self.blitWaitCompile()
        self.blitWaitRun()

    def blitHelp(self):
        if self.help:
            helpImg = pygame.image.load('img/help.png')
            helpImg = pygame.transform.scale(helpImg,(600,500))
            self.window.blit(helpImg,(570,127))

    def blitButton(self):
        self.currBGImg = pygame.image.load('img/testBG.png').convert_alpha()
        self.currBGImg.set_alpha(200)
        basedLeft = 50
        basedTop = 630
        self.currBGImg = pygame.transform.scale(self.currBGImg, (200, 80))
        self.window.blit(self.currBGImg, (basedLeft, basedTop))
        self.TestingButton = self.drawButton('开始评测',basedLeft+25,basedTop+20)

        self.currBGImg = pygame.image.load('img/testBG.png').convert_alpha()
        self.currBGImg.set_alpha(200)
        basedLeft = 400
        basedTop = 630
        self.currBGImg = pygame.transform.scale(self.currBGImg, (200, 80))
        self.window.blit(self.currBGImg, (basedLeft, basedTop))
        self.groupTestingButton = self.drawButton('群测模式', basedLeft + 25, basedTop + 20)

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
            basedLeft = 780
            basedTop = 600
            self.downImg = pygame.transform.scale(self.downImg, (175, 80))
            self.window.blit(self.downImg, (basedLeft, basedTop))
            self.downButton = self.drawButton('Download', basedLeft + 25, basedTop + 20)

    def blitGroupButton(self):
        self.currBGImg = pygame.image.load('img/testBG.png').convert_alpha()
        self.currBGImg.set_alpha(200)
        basedLeft = 980
        basedTop = 0
        self.currBGImg = pygame.transform.scale(self.currBGImg, (200, 80))
        self.window.blit(self.currBGImg, (basedLeft, basedTop))
        self.TestingButton = self.drawButton('随机评测', basedLeft + 25, basedTop + 20)

        self.currBGImg = pygame.image.load('img/testBG.png').convert_alpha()
        self.currBGImg.set_alpha(200)
        basedLeft = 980
        basedTop = 100
        self.currBGImg = pygame.transform.scale(self.currBGImg, (200, 80))
        self.window.blit(self.currBGImg, (basedLeft, basedTop))
        self.LocalButton = self.drawButton('本地评测', basedLeft + 25, basedTop + 20)

        self.comImg = pygame.image.load('img/compile.png').convert_alpha()
        self.comImg.set_alpha(200)
        basedLeft = 100
        basedTop = 0
        self.comImg = pygame.transform.scale(self.comImg, (120, 80))
        self.window.blit(self.comImg, (basedLeft, basedTop))
        self.compileButton = self.drawButton('编译', basedLeft + 25, basedTop + 20)

        self.downImg = pygame.image.load('img/compile.png').convert_alpha()
        self.downImg.set_alpha(200)
        basedLeft = 980
        basedTop = 200
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

    def testing(self):
        for i in range(6):
            self.results[i].Str = ''
        threads = []

        for i in range(6):
            thread = threading.Thread(target=self.everyTest, args=(i,))
            threads.append(thread)
            thread.start()

    def everyTest(self,i):
        # 运行 dataMaking.py 并捕获输出
        result = subprocess.run(["python", "dataMaking.py"], capture_output=True, text=True,creationflags=subprocess.CREATE_NO_WINDOW)
        input = result.stdout.strip()  # 获取输出
        input_file = f"Input{i}.txt"
        with open(input_file, 'w') as f:
            f.write(input)

        Str = 'CE'
        if self.CE == 0:
            output,running = getOutput(input,r'D:\OOTest\unit2\Tested_class')
            output_file = f"Output{i}.txt"
            with open(output_file, 'w') as f:
                f.write(output)  # 直接写入getOutput返回的output内容

            if running == 0:
                Str = 'RE'
            else:
                right = check(i)
                if right == 'Accepted':
                    Str = 'AC'
                else:
                    Str = 'WA'
        self.results[i] = testResult(Str)

    def groupTesting(self):
        # for i in range(6):
        #     for j in range(self.groupNum):
        #         self.groupResults[j][i].Str = ''
        #         self.groupResults[j][i].input = ''
        #         self.groupResults[j][i].output = ''
        #         self.groupResults[j][i].answer = ''
        self.groupNoTest = 0
        threads = []
        for i in range(6):
            thread = threading.Thread(target=self.groupTestData,args=(i,))
            threads.append(thread)
            thread.start()

    def groupTestData(self,i):
        threads = []
        result = subprocess.run(
            ["python", "dataMaking.py",],
            capture_output=True, text=True,
            creationflags=subprocess.CREATE_NO_WINDOW)
        input = result.stdout.strip()  # 获取输出
        for j in range(self.groupNum):
            print(i,j)
            thread = threading.Thread(target=self.everyGroupTest, args=(i,j,input,))
            threads.append(thread)
            thread.start()

    def localTesting(self):
        print(2)
        for i in range(6):
            for j in range(self.groupNum):
                self.groupResults[j][i].Str = ''

        threads = []
        try:
            with open('D:/OOTest/unit2/localdata.txt', "r") as file:
                input = file.read()  # 读取文件的全部内容
        except FileNotFoundError:
            print("Error: localdata.txt file not found.")
            return

        for j in range(self.groupNum):
            thread = threading.Thread(target=self.everyGroupTest, args=(0,j,input,))
            threads.append(thread)
            thread.start()

    def everyGroupTest(self,i,j,input):
        # 运行 dataMaking.py 并捕获输出
        # print(input)
        self.groupResults[j][i].Str = ''

        # print(answer)
        Str = 'CE'
        pro = 0
        tempOutput = 'Compile Error'
        if self.CE == 0:
            output, running = getOutput(input,self.groupResults[j][i].path)
            output = re.sub(r'\n+$', '', output)
            tempOutput = output
            if running == 0:
                Str = 'RE'
            else:
                right = check(7*j+i)
                if right == 1:
                    Str = 'AC'
                else:
                    Str = 'WA'

        self.groupResults[j][i].Str = Str

    def blitResult(self):
        for i in range(6):
            if self.results[i].Str!='':
                x = 700 + 120 * (i % 3)
                y = 350+120*(i//3)
                self.results[i].Rect = self.drawResult(x,y,self.results[i].Str)
                if self.mergeRect == None:
                    self.mergeRect = pygame.Rect(self.results[i].Rect)
                self.mergeRect = self.mergeRect.union(self.results[i].Rect)

    def blitGroupResult(self):
        for i in range(self.groupNum):
            font = pygame.font.Font("Font/QingNiao.ttf", 32)  # 使用支持中文的字体
            button_text = font.render(self.groupResults[i][0].name, True, (255, 255, 255))  # 渲染文本
            button_rect = button_text.get_rect(topleft=(120, 110+90*i))
            self.window.blit(button_text, button_rect)
            for j in range(6):
                if self.groupResults[i][j].Str!='':
                    x = 220+100*j
                    y = 100+90*i
                    self.groupResults[i][j].Rect = (
                        self.drawGroupResult(x, y, self.groupResults[i][j].Str))

    def drawResult(self,x,y,str):
        rect_width = 100  # 框的宽度
        rect_height = 100  # 框的高度
        color = (255,255,255)
        if str == 'WA':
            color = (255, 0, 0)  # 红色
        elif str == 'RE' or str == 'CE':
            color = (128, 0, 128)  # 紫色
        elif str == 'AC':
            color = (0, 255, 0)  # 绿色

        # 绘制白色填充的正方形框
        pygame.draw.rect(self.window, color, (x, y, rect_width, rect_height))
        font_path = "Font/QingNiao.ttf"  # 替换为你的字体文件路径
        font = pygame.font.Font(font_path, 48)  # 使用支持中文的字体
        button_text = font.render(str, True, (255, 255, 255))  # 渲染文本
        button_rect = button_text.get_rect(topleft=(x+25, y+25))
        self.window.blit(button_text, button_rect)
        # 返回框的 rect 对象
        return pygame.Rect(x, y, rect_width, rect_height)

    def drawGroupResult(self, x, y, str):
        rect_width = 70  # 框的宽度
        rect_height = 70  # 框的高度
        color = (255, 255, 255)
        if str == 'WA':
            color = (255, 0, 0)  # 红色
        elif str == 'RE' or str == 'CE':
            color = (128, 0, 128)  # 紫色
        elif str == 'AC':
            color = (0, 255, 0)  # 绿色

        # 绘制白色填充的正方形框
        pygame.draw.rect(self.window, color, (x, y, rect_width, rect_height))
        font_path = "Font/QingNiao.ttf"  # 替换为你的字体文件路径
        font = pygame.font.Font(font_path, 32)  # 使用支持中文的字体
        button_text = font.render(str, True, (255, 255, 255))  # 渲染文本
        button_rect = button_text.get_rect(topleft=(x + 20, y + 15))
        self.window.blit(button_text, button_rect)
        # 返回框的 rect 对象
        return pygame.Rect(x, y, rect_width, rect_height)

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
        data_dir = r"D:\OOTest\unit2\data"
        # 获取当前时间并格式化为年月日时分秒
        current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        folder_name = os.path.join(data_dir, current_time)
        # 创建以当前时间命名的文件夹
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # 在文件夹中创建 6 个 .txt 文件
        for i  in range(6):
            file_name = os.path.join(folder_name, f"Input{i}.txt")
            copy_files_only(f'Input{i}.txt',  file_name)
            file_name = os.path.join(folder_name, f"Output{i}.txt")
            copy_files_only(f'Output{i}.txt', file_name)

        print(f"Files have been saved to {folder_name}")

    def groupDownload(self):
        print("Download")
        # 目标目录
        data_dir = r"D:\OOTest\unit2\group_data"
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
                # f.write(f"Input:\n{self.groupResults[0][i].input}\n\n")  # 写入 input 内容
                # f.write(f"Answer:\n{self.groupResults[0][i].answer}\n\n")  # 写入 answer 内容
                # cnt = 0
                # for j in range(self.groupNum):
                #     if self.groupResults[j][i].Str!='AC':
                #         cnt += 1
                #         f.write(f'{self.groupResults[j][i].name}:\n')
                #         f.write(f"Output:\n{self.groupResults[j][i].output}\n\n")  # 写入 output 内容
                # if cnt == 0:
                #     f.write(f'All Accepted!\n')
                pass
        print(f"Files have been saved to {folder_name}")

    def blitTitle(self):
        self.tltleImg = pygame.image.load('img/title.png').convert_alpha()
        self.tltleImg.set_alpha(255)
        basedLeft = 450
        basedTop = 20
        self.tltleImg = pygame.transform.scale(self.tltleImg, (300, 180))
        self.window.blit(self.tltleImg, (basedLeft, basedTop))

    def blitWaitCompile(self):
        if self.waitCom == 1 :
            font_path = "Font/YeZi.ttf"  # 替换为你的字体文件路径
            font = pygame.font.Font(font_path, 24)  # 使用支持中文的字体
            button_text = font.render('正在编译……', True, (255, 255, 255))  # 渲染文本
            button_rect = button_text.get_rect(topleft=(160 + 25, 150 + 45))
            self.window.blit(button_text, button_rect)

    def complie(self,srcPath,binPath):
        self.waitCom = 1
        # 定义源文件目录和编译后文件目录
        src_dir = srcPath  # 替换为您的Java源文件目录
        bin_dir = binPath  # 替换为您希望编译后的.class文件存放的目录

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
        compile_process = subprocess.run(compile_command, capture_output=True, text=True,creationflags=subprocess.CREATE_NO_WINDOW)
        # 检查编译是否成功
        self.waitCom = 0
        if compile_process.returncode == 0:
            # print("编译成功！")
            self.CE = 0
            return 1
        else:
            # print("编译失败：")
            print(compile_process.stderr)
            # exit(1)
            self.CE = 1
            return 0

    def groupComplie(self):
        root_dir = r'D:\OOTest\unit2\group'
        # 检查根目录是否存在
        if not os.path.exists(root_dir):
            print(f"指定的目录 {root_dir} 不存在。")
            return
        # 获取根目录下的所有子目录
        subdirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
        self.groupNum = len(subdirs)
        # 输出子目录数量和名称
        print(f"在目录 {root_dir} 下找到 {self.groupNum} 个子目录：")
        threads = []
        for i in range(self.groupNum):  # 使用索引 i 遍历
            subdir = subdirs[i]  # 通过索引获取子目录名称
            print(f"{i}. {subdir}")  # 输出序号和子目录名称
            # 在每个子目录下创建名为 name_class 的目录
            subdir_path = os.path.join(root_dir, subdir)
            new_dir_path = os.path.join(subdir_path, f"{subdir}_class")
            for j in range(6):
                self.groupResults[i][j].path = new_dir_path
                self.groupResults[i][j].name = subdir
            # 检查是否已经存在该目录，如果不存在则创建
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)
                print(f"在 {subdir_path} 下创建了目录 {subdir}_class")
            else:
                print(f"目录 {new_dir_path} 已经存在，跳过创建。")
            thread = threading.Thread(target=self.complie,args=(subdir_path,new_dir_path,))
            threads.append(thread)
            thread.start()

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
            button_rect = button_text.get_rect(topleft=(250 + 25, 600 + 65))
            self.window.blit(button_text, button_rect)

    def blitWaitGroupRun(self):
        Sum = 6*self.groupNum
        wait = Sum
        for i in range(self.groupNum):
            for j in range(6):
                if self.groupResults[i][j].Str == '':
                    wait -= 1

        if wait < (Sum) and self.groupNoTest==0 :
            font_path = "Font/YeZi.ttf"
            font = pygame.font.Font(font_path, 24)
            text = f'正在评测，请耐心等待{wait}/{Sum}……'
            button_text = font.render(text, True, (235, 255, 255))
            button_rect = button_text.get_rect(topleft=(250 + 25, + 65))
            self.window.blit(button_text, button_rect)

    def blitGroupBG(self):
        # self.window.fill((255, 254, 254))
        img = pygame.image.load('img/startBG.png')
        self.window.blit(img,(0,-80))
        self.blitReturnButton()
        self.blitGroupButton()
        self.blitGroupResult()
        self.blitWaitGroupRun()

def getOutput(input_string,binPath):
    bin_dir = binPath
    # 运行MainClass
    run_command = ['java', '-cp', bin_dir, 'TestMain']
    run_process = subprocess.run(run_command, input=input_string, capture_output=True, text=True,creationflags=subprocess.CREATE_NO_WINDOW)
    # 输出运行结果
    if run_process.returncode == 0:
        # print("程序输出：")
        return run_process.stdout,1
    else:
        # print("程序运行失败：")
        return run_process.stderr,0

def check(i):
    # 构造命令，将参数 i 传递给 check.py 脚本
    command = ["python", "check.py", str(i)]
    try:
        # 使用 subprocess.run 运行命令并捕获输出
        result = subprocess.run(command, capture_output=True, text=True, check=True,creationflags=subprocess.CREATE_NO_WINDOW)
        # 返回脚本的标准输出
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # 如果脚本运行出错，返回错误信息
        return f"Error: {e.stderr.strip()}"

def copy_source_to_target(source_path='./source', target_path='OOTest/unit2/source'):
    """
    递归复制源目录内容到目标目录
    :param source_path: 源目录路径 (默认'./source')
    :param target_path: 目标目录路径 (默认'OOTest/unit1/source')
    """
    try:
        # 检查源目录是否存在
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source directory not found: {source_path}")

        # 创建目标目录（如果不存在）
        os.makedirs(target_path, exist_ok=True)
        print(f"Target directory ready: {target_path}")

        # 递归复制内容
        for item in os.listdir(source_path):
            src = os.path.join(source_path, item)
            dst = os.path.join(target_path, item)

            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)  # Python 3.8+ 需要 dirs_exist_ok
                print(f"Copied directory: {src} -> {dst}")
            else:
                shutil.copy2(src, dst)  # 保留文件元数据
                print(f"Copied file: {src} -> {dst}")

        print("Copy operation completed successfully!")
    except Exception as e:
        print(f"Error during copy: {str(e)}")

def copy_files_only(source_path, target_path):
    """
    将指定的源文件复制到目标路径。
    如果目标路径是一个目录，文件将被复制到该目录中，保持原文件名。
    如果目标路径是一个文件路径，文件将被直接复制到该路径。

    :param source_path: 源文件路径
    :param target_path: 目标路径（可以是目录或文件路径）
    """
    # 确保源文件存在
    if not os.path.exists(source_path):
        print(f"错误：源文件 '{source_path}' 不存在。")
        return

    # 确保源路径是一个文件
    if not os.path.isfile(source_path):
        print(f"错误：'{source_path}' 不是一个有效的文件。")
        return

    # 如果目标路径是一个目录
    if os.path.isdir(target_path):
        # 构造目标文件路径（保持原文件名）
        target_file_path = os.path.join(target_path, os.path.basename(source_path))
    else:
        # 目标路径是一个文件路径
        target_file_path = target_path

    # 确保目标目录存在，如果不存在则创建
    target_dir = os.path.dirname(target_file_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"目标目录 '{target_dir}' 已创建。")

    # 复制文件
    try:
        shutil.copy2(source_path, target_file_path)
        print(f"文件 '{source_path}' 已成功复制到 '{target_file_path}'。")
    except Exception as e:
        print(f"复制文件时发生错误：{e}")

def init():
    print("Initializing directories...")
    # 定义目标路径
    base_dir = r"D:\OOTest"
    unit2_dir = os.path.join(base_dir, "unit2")
    source_dir = os.path.join(unit2_dir, "source")
    data_dir = os.path.join(unit2_dir, "data")
    class_dir = os.path.join(unit2_dir, "Tested_class")

    # 检查并创建 OOTest 目录
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Directory created: {base_dir}")
    else:
        print(f"Directory already exists: {base_dir}")
    # 检查并创建 OOTest/unit1 目录
    if not os.path.exists(unit2_dir):
        os.makedirs(unit2_dir)
        print(f"Directory created: {unit2_dir}")
    else:
        print(f"Directory already exists: {unit2_dir}")

        # 检查并创建 OOTest/unit1/source 目录
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        print(f"Directory created: {source_dir}")
    else:
        print(f"Directory already exists: {source_dir}")
    copy_source_to_target('./source', source_dir)

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
    def __init__(self,Str):
        self.Str = Str
        self.name = None
        self.path = None
        self.Rect = None

os.chdir(os.path.dirname(__file__))
init()
MainGame().startGame()
