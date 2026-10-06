# In-game psychological horror, with explicit presentation levels.
default persistent.horror_intensity = 2
default horror_stage = 0

init python:
    renpy.music.register_channel("signal", mixer="sfx", loop=False)
    def horror_level():
        return persistent.horror_intensity if persistent.signal_effects else 0

    def set_horror_level(level):
        persistent.horror_intensity = level
        persistent.signal_effects = level > 0
        renpy.music.stop(channel="signal", fadeout=.15)
        renpy.save_persistent()

    def horror_reset():
        renpy.hide_screen("horror_burst")
        renpy.music.stop(channel="signal", fadeout=.2)

    def horror_sound(name):
        level = horror_level()
        if level:
            renpy.music.play("audio/fx_" + name + ".wav", channel="signal",
                relative_volume=.65 if level == 2 else .25)

    config.overlay_screens.append("horror_ambience")

transform signal_drift:
    xoffset 0
    pause .38
    xoffset 13
    pause .11
    xoffset -9
    pause .28
    xoffset 0
    pause 1.6
    repeat

transform signal_echo:
    alpha .08
    linear 1.7 alpha .24
    linear 2.3 alpha .08
    repeat

transform ghost_left:
    xalign .16 yalign 1.0 alpha .5
    matrixcolor TintMatrix("#739caa")

screen horror_ambience():
    zorder 12
    if horror_level() and horror_stage and not main_menu:
        add Solid("#02061055") xpos 0 xsize 45 ysize 765
        add Solid("#02061055") xpos 1875 xsize 45 ysize 765
        if horror_level() == 2:
            for y in (86, 238, 415, 602, 743):
                add Solid("#9f315b13") ypos y ysize 2 xsize 1920 at signal_drift
        if horror_stage >= 2:
            text "SIGNAL // 03  ·  她还在这里" xpos 1480 ypos 65 size 20 color "#b68c9c88" at signal_echo

screen horror_burst(kind="signal", amount=1):
    zorder 75
    if horror_level():
        if kind == "signal":
            add Solid("#07192799")
            if horror_level() == 2:
                add "monika uncanny" at Transform(xalign=.87, yalign=1.0, alpha=.27)
            text ("选择已记录。" if amount == 1 else "你也听见了，对吗？") align (.5, .43) size 58 color "#d6e6e9"
        elif kind == "fracture":
            add Solid("#06102ae8")
            text "连接已断开" xpos 220 ypos 170 size 78 color "#c5d7f0"
            text "Error  /  CHARACTER CHANNEL MISMATCH" xpos 224 ypos 277 size 28 color "#7494b6"
            text ":)" xpos 1570 ypos 110 size 180 color "#ca8ca2" at Transform(rotate=90)
            text "你还在这里。" align (.5, .72) size 45 color "#e2b7ba"
        elif kind == "sun":
            add "bg hollow"
            add Solid("#09051c77")
            text "没有你的名字。" align (.5, .77) size 52 color "#d5b9ca"
        elif kind == "mirror":
            add Solid("#060912e8")
            add "sayori cry" at Transform(xalign=.04, yalign=1.0, alpha=.58, matrixcolor=TintMatrix("#72b4bd"))
            add "cordelia sad" at Transform(xalign=.5, yalign=1.0, alpha=.55, matrixcolor=TintMatrix("#a95686"))
            add "obedience surprise" at Transform(xalign=.96, yalign=1.0, alpha=.58, matrixcolor=TintMatrix("#6b929e"))
            if horror_level() == 2:
                add Transform(Crop((145, 180, 410, 115), "monika uncanny"), xysize=(1470, 240), alpha=.66) xpos 210 ypos 285 at signal_drift
            text "S A Y O R I     /     ???     /     O B E D I E N C E" align (.5, .79) size 28 color "#e5b2bf"
        elif kind == "portrait":
            add Solid("#100918d9")
            add "monika uncanny" at Transform(xalign=.5, yalign=.45, zoom=1.42)
            text "看着我。" xpos 1320 ypos 380 size 80 color "#b0798e"
        elif kind == "end":
            add Solid("#03040a")
            text "END" align (.5, .43) size 140 kerning 36 color "#c5bdc8"
            text "……谁说结束了？" align (.5, .66) size 37 color "#9d6a80" at signal_echo
        if horror_level() == 2 and kind != "end":
            for row in range(14, 1060, 39):
                add Solid("#7fa6b314") ypos row ysize 3 xsize 1920
            for y, width, x in [(120, 570, 0), (330, 970, 950), (510, 300, 230), (810, 1100, 110)]:
                add Solid("#52113945") xpos x ypos y xsize width ysize 18 at signal_drift

label horror_signal(amount=1):
    if horror_level():
        $ horror_sound("signal")
        show screen horror_burst("signal", amount)
        $ renpy.pause(.65 if amount == 1 else 1.0)
        hide screen horror_burst
        $ renpy.music.stop(channel="signal", fadeout=.2)
    return

label horror_cut(kind="fracture", duration=1.3):
    if horror_level():
        $ horror_sound("low" if kind in ("portrait", "sun", "end") else "fracture")
        show screen horror_burst(kind)
        $ renpy.pause(duration)
        hide screen horror_burst
        $ renpy.music.stop(channel="signal", fadeout=.2)
    return

label debug_fx_signal:
    scene bg classroom
    show sayori normal at solo
    "接下来预览第 1 次、第 2 次隐藏选项的异常信号。"
    call horror_signal(1)
    call horror_signal(2)
    "预览结束。"
    $ renpy.end_replay()
    return

label debug_fx_rupture:
    scene bg hollow
    "接下来预览连接断裂、黑色太阳和人物残像。"
    call horror_cut("fracture", 2.0)
    call horror_cut("sun", 2.0)
    call horror_cut("mirror", 2.5)
    "预览结束。"
    $ renpy.end_replay()
    return

label debug_fx_stare:
    scene bg hollow
    show monika normal at solo
    monika "你有没有发现，我一直没有移开视线？"
    call horror_cut("portrait", 2.2)
    "预览结束。"
    $ renpy.end_replay()
    return

label debug_fx_false_end:
    scene bg black
    "接下来预览假结束画面。"
    call horror_cut("end", 3.0)
    monika "还没有结束哦。"
    $ renpy.end_replay()
    return
