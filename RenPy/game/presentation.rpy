# 1920 x 1080 native layout. All visible text uses the bundled Chinese font.
init offset = 10


style say_window:
    background Solid("#142936ed")
style namebox:
    background None
style say_dialogue:
    line_spacing 9
style game_menu_outer_frame:
    background None
style notify_frame:
    background Solid("#203947ed")
style notify_text:
    color "#fff2db"
style scrollbar:
    base_bar Solid("#d7c9b8")
    thumb Solid("#b8816d")
style vscrollbar:
    base_bar Solid("#d7c9b8")
    thumb Solid("#b8816d")
style bar:
    left_bar Solid("#bb8274")
    right_bar Solid("#d1c7ba")
style slider:
    base_bar Solid("#4b636f")
    thumb Solid("#e8baa2", xsize=14, ysize=38)
style choice_button:
    background Solid("#162e3beb")
    hover_background Solid("#835958f5")
    padding (36, 15)
style choice_button_text:
    color "#fff5e9"
    hover_color "#ffffff"
    size 30
style quick_button_text:
    idle_color "#c5c5c5"
    hover_color "#fff1dc"
style slot_time_text:
    color "#c7d5d9"
style slot_name_text:
    color "#e9d5c5"
style notebook_button:
    background Solid("#f5eadd")
    selected_background Solid("#dbb9a1")
    hover_background Solid("#ecd0bc")
    padding (24, 18)
style notebook_button_text:
    color "#263b44"
    hover_color "#874e4e"
    insensitive_color "#918d85"
    size 29
style notebook_text:
    color "#263b44"
    size 28

screen main_menu():
    tag menu
    add "bg campus"
    add Solid("#112a35a0")
    add "sayori happy" at Transform(xalign=0.91, yalign=1.0)
    frame:
        background Solid("#f8efe6f2")
        xpos 125 ypos 105 xsize 885 ysize 855
        padding (65, 52)
        vbox:
            spacing 20
            text "AN AUTUMN WE SHARED" color "#8e6259" size 25 kerning 5
            text "Doki Doki\nOhayou Sayori" color "#233b47" size 69 line_spacing 3
            text "早上好。今天，也一起走吧。" color "#976b61" size 31
            null height 12
            vbox:
                spacing 9
                style_prefix "notebook"
                textbutton "开始新的故事" action Start()
                textbutton "继续 · 读取存档" action ShowMenu("load")
                textbutton "回忆手册 · 结局 / 章节 / 小剧场" action ShowMenu("memories")
                textbutton "阅读设置" action ShowMenu("preferences")
                hbox:
                    spacing 14
                    textbutton "调试室" action ShowMenu("debug_room")
                    textbutton "关于作品" action ShowMenu("about")
                    textbutton "退出" action Quit(confirm=True)
    text "完整修复版 2.1  /  非官方同人作品" xpos 129 ypos 992 size 23 color "#fff6e8"

screen content_note():
    modal True
    add "bg campus"
    add Solid("#102631bb")
    frame:
        align (0.5, 0.5) xsize 1220
        padding (72, 55) background Solid("#f8efe8")
        vbox:
            spacing 28
            text "在故事开始之前" size 50 color "#233b47"
            text "这是一部包含校园日常、恋爱分支与 Meta 悬疑的同人作品。后续涉及抑郁、自伤、自杀、死亡与情绪伤害的文字描写。" color "#304754" size 33
            text "故事按原作保留。你可以随时打开菜单、保存、回退或退出；这里没有限时选择。" color "#6b6b6b" size 29
            text "隐藏线含画面异常与不安音效，可在阅读设置中选择标准、减弱或关闭恐怖演出。" color "#786c63" size 26
            text "鼠标 / 空格继续 · 滚轮向上回退 · Esc 打开菜单 · H 隐藏文字" color "#786c63" size 26
            hbox:
                spacing 25
                style_prefix "notebook"
                textbutton "开始阅读" action Return()
                textbutton "回到主菜单" action MainMenu(confirm=False)

screen ending_postcard(number):
    modal True
    $ code, title, label, note = ENDINGS[number - 1]
    add Solid("#17313bb5")
    frame:
        align (0.5, 0.5) xsize 1150
        padding (70, 60) background Solid("#f8efe5")
        vbox:
            spacing 28
            text ("调试回看 · 本次不计入收集" if debug_session else "一张新的回忆明信片") color "#a57060" size 26 kerning 4
            text "[code]  /  [title]" color "#233b47" size 58
            text note color "#5b686b" size 32
            $ completed = sum(bool(persistent.achievements.get("结局%d" % n)) for n in range(1, 10))
            text "结局收藏  [completed] / 9" color "#8c6255" size 29
            text "其他的选择还留在故事里。也可以让今天的阅读停在这里。" color "#77736b" size 26
            textbutton "收好这张明信片" style "notebook_button" text_style "notebook_button_text" action Return()

screen memories():
    tag menu
    default tab = "endings"
    default hints = False
    add "bg campus"
    add Solid("#102a37dc")
    frame:
        xpos 110 ypos 70 xsize 1700 ysize 935
        padding (48, 38) background Solid("#faf2e8")
        vbox:
            spacing 23
            hbox:
                xfill True
                text "我们的回忆手册" size 53 color "#243c48"
                textbutton "返回" xalign 1.0 style "notebook_button" text_style "notebook_button_text" action (ShowMenu("main_menu") if main_menu else Return())
            hbox:
                spacing 15
                style_prefix "notebook"
                textbutton "结局明信片" action SetScreenVariable("tab", "endings")
                textbutton "已读章节" action SetScreenVariable("tab", "chapters")
                textbutton "成就与小剧场" action SetScreenVariable("tab", "theaters")
                textbutton "美术手帐" action SetScreenVariable("tab", "art")
            viewport:
                ysize 680
                scrollbars "vertical" mousewheel True draggable True
                if tab == "endings":
                    vbox:
                        spacing 14
                        text "只有抵达过的结局，才会写下名字。点击已解锁明信片可以回看。" style "notebook_text"
                        for index, (code, title, label, note) in enumerate(ENDINGS):
                            $ unlocked = persistent.achievements.get("结局%d" % (index + 1), False)
                            textbutton ("%s  /  %s  —  %s" % (code, title, note) if unlocked else "%02d  /  尚未抵达" % (index + 1)):
                                style "notebook_button" text_style "notebook_button_text"
                                xsize 1520
                                action Replay(label, scope=replay_scope(), locked=not unlocked)
                elif tab == "chapters":
                    vbox:
                        spacing 12
                        text "回看使用独立进度，可收集新成就；不改写原存档。隐藏线计数从零开始。" style "notebook_text"
                        for label, title, route, unused in BOOKMARKS:
                            $ unlocked = label in persistent.read_chapters
                            textbutton ("%s · %s" % (title, route) if unlocked else "尚未读到的章节"):
                                style "notebook_button" text_style "notebook_button_text"
                                xsize 1520
                                action Replay(label, scope=replay_scope(), locked=not unlocked)
                elif tab == "theaters":
                    vbox:
                        spacing 20
                        textbutton ("收起路线提示" if hints else "显示轻度路线提示") style "notebook_button" text_style "notebook_button_text" action ToggleScreenVariable("hints")
                        for key, title, names, side, label in GROUPS:
                            $ done = group_progress(names)
                            $ total = len(names)
                            $ unlocked = done == total
                            frame:
                                background Solid("#e9e1d6") padding (25, 20) xsize 1520
                                vbox:
                                    spacing 10
                                    text "[title]  ·  [done] / [total]" size 34 color "#2b424b"
                                    bar value done range total xsize 1420 ysize 10
                                    if hints:
                                        text HINTS[key] color "#775c52" size 26
                                    text "  /  ".join(n + (" ✓" if persistent.achievements.get(n) else " ·") for n in names) color "#68716e" size 24 xsize 1400
                                    textbutton ("阅读小剧场 · " + side if unlocked else "收集本组全部成就，解锁小剧场"):
                                        style "notebook_button" text_style "notebook_button_text"
                                        action Replay(label, scope=replay_scope(), locked=not unlocked)
                else:
                    vbox:
                        spacing 18
                        text "那些我们一起走过的地方 / 新增场景画集" style "notebook_text"
                        for name, caption in [("campus", "秋日校园"), ("lab", "工程实验室"), ("cafe", "灯光下的餐桌"), ("studio", "同频的广播室"), ("river", "江风与渡口"), ("station", "出发的早晨"), ("clinic", "校医院的阳光"), ("park", "奇妙夜"), ("roof", "寒夜天台"), ("lake", "思源湖畔"), ("library", "图书馆里的话"), ("office", "学生会办公室"), ("city", "弄堂口的灯"), ("bbq", "三只烤红薯"), ("classroom", "课堂的日光"), ("dormday", "寝室的早晨"), ("dormnight", "深夜未眠")]:
                            text caption color "#42616a" size 31
                            add ("bg " + name) xysize (1400, 788)
