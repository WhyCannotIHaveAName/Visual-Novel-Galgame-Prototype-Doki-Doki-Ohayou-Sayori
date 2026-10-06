# Author tools ship with the game; they use replay contexts, not the live save.
default persistent.debug_enabled = False
default debug_session = False
default debug_target = "chapter1"
default debug_counter = 0
default debug_sayori = False

init python:
    import json
    with renpy.file("debug_scenes.json") as f:
        DEBUG_SCENES = json.load(f)
    DEBUG_GROUPS = ["全部", "共同篇", "Sayori", "Cordelia", "Obedience", "Monika", "小剧场", "演出预览"]
    CAST_EXPRESSIONS = {
        "sayori": ["normal", "happy", "understanding", "cry", "joke", "hug", "potato", "ice", "bbq", "surprisepink"],
        "cordelia": ["normal", "happy", "laugh", "mad", "sad"],
        "obedience": ["normal", "cute", "mean", "surprise"],
        "monika": ["normal", "happy", "touched", "angry", "book", "bike", "uncanny"],
        "leo": ["normal"], "shane": ["normal"],
    }
    def debug_scope(target, counter=0, sayori=False):
        scope = replay_scope()
        scope.update(debug_session=True, debug_target=target,
            debug_counter=counter, debug_sayori=sayori)
        return scope

    def debug_matches(row, group, query):
        return (group == "全部" or row[2] == group) and query.lower() in " ".join(row).lower()

    config.overlay_screens.append("author_shortcut")

screen author_shortcut():
    zorder 90
    if persistent.debug_enabled or debug_session:
        key "K_F6" action ShowMenu("debug_room")
    if debug_session:
        frame:
            xpos 15 ypos 15 padding (18, 10) background Solid("#102331da")
            vbox:
                spacing 5
                text "调试回看 · [current_chapter] · 隐藏计数 [monika_count]" size 21 color "#ffe6b8"
                hbox:
                    spacing 20
                    textbutton "F6 调试室" action ShowMenu("debug_room") text_size 20
                    textbutton "结束本次测试" action EndReplay(confirm=False) text_size 20

label debug_launch:
    $ monika_count = debug_counter
    $ in_sayori_route = debug_sayori
    $ monika_triggered = False
    $ horror_stage = 0
    $ horror_reset()
    jump expression debug_target

screen debug_room():
    tag menu
    default group = "全部"
    default query = ""
    default counter = 0
    default sayori_override = False
    add Solid("#142833")
    frame:
        xpos 70 ypos 45 xsize 1780 ysize 990 padding (38, 28)
        background Solid("#f8eee1")
        vbox:
            spacing 17
            hbox:
                spacing 30
                text "作者调试室" size 48 color "#243c48"
                textbutton "立绘与同屏比例" style "notebook_button" text_style "notebook_button_text" action ShowMenu("debug_portraits")
                textbutton "返回" style "notebook_button" text_style "notebook_button_text" action (ShowMenu("main_menu") if main_menu else Return())
            text "点击任意章节即可测试，无需先解锁。测试使用独立进度，不收集成就、不写入已读章节；Esc 可打开菜单结束回看。" size 24 color "#5f6869"
            hbox:
                spacing 25
                textbutton ("F6 快捷入口：开" if persistent.debug_enabled else "F6 快捷入口：关") style "notebook_button" text_style "notebook_button_text" action ToggleField(persistent, "debug_enabled")
                text "隐藏线初始计数" size 26 color "#29434e" yalign .5
                for n in range(3):
                    textbutton str(n) style "notebook_button" text_style "notebook_button_text" selected counter == n action SetScreenVariable("counter", n)
                textbutton ("Sayori 判定：开" if sayori_override else "Sayori 判定：按剧情") style "notebook_button" text_style "notebook_button_text" action ToggleScreenVariable("sayori_override")
            hbox:
                spacing 9
                for category in DEBUG_GROUPS:
                    textbutton category style "notebook_button" text_style "notebook_button_text" text_size 24 selected group == category action SetScreenVariable("group", category)
            frame:
                background Solid("#e7dccc") padding (18, 10) xfill True
                hbox:
                    spacing 20
                    text "查找章节 / 台词：" size 25 color "#324a54"
                    input value ScreenVariableInputValue("query") length 45 size 25 color "#243c48" xsize 1190
            viewport:
                ysize 568 scrollbars "vertical" mousewheel True draggable True
                vbox:
                    spacing 7
                    for target, title, category in DEBUG_SCENES:
                        if debug_matches((target, title, category), group, query):
                            textbutton (category + " · " + target + "  /  " + title):
                                style "notebook_button" text_style "notebook_button_text"
                                text_size 25 xsize 1640
                                action Replay("debug_launch", scope=debug_scope(target, counter, sayori_override), locked=False)

screen debug_portraits():
    tag menu
    default who = "sayori"
    default expression = "normal"
    default layout = 4
    default backdrop = "campus"
    add ("bg " + backdrop)
    if layout == 1:
        add (who + " " + expression) at solo
    elif layout == 2:
        add (who + " " + expression) at duo_left
        add (("monika" if who != "monika" else "sayori") + " normal") at duo_right
    else:
        for person, position in [("sayori", quartet_1), ("cordelia", quartet_2), ("obedience", quartet_3), ("monika", quartet_4)]:
            add (person + " " + (expression if person == who else "normal")) at position
    frame:
        xpos 22 ypos 18 padding (18, 10) background Solid("#142936e8")
        text "立绘检查 / 与剧情相同的站位、缩放与画布" size 25 color "#fff0dc"
    frame:
        yalign 1.0 xfill True ysize 280 padding (45, 24) background Solid("#142936f2")
        vbox:
            spacing 13
            hbox:
                spacing 12
                for person in CAST_EXPRESSIONS:
                    textbutton person style "notebook_button" text_style "notebook_button_text" text_size 24 selected who == person action [SetScreenVariable("who", person), SetScreenVariable("expression", "normal")]
                textbutton "返回调试室" style "notebook_button" text_style "notebook_button_text" text_size 24 action ShowMenu("debug_room")
            hbox:
                spacing 9
                for mood in CAST_EXPRESSIONS[who]:
                    textbutton mood style "notebook_button" text_style "notebook_button_text" text_size 21 selected expression == mood action SetScreenVariable("expression", mood)
            hbox:
                spacing 18
                for count in [1, 2, 4]:
                    textbutton (str(count) + " 人同屏") style "notebook_button" text_style "notebook_button_text" text_size 22 selected layout == count action SetScreenVariable("layout", count)
                for bgname, title in [("campus", "校园"), ("black", "深色底"), ("white", "浅色底")]:
                    textbutton title style "notebook_button" text_style "notebook_button_text" text_size 22 selected backdrop == bgname action SetScreenVariable("backdrop", bgname)

