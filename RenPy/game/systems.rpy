# Systems are kept separate from the author's dialogue.
default persistent.achievements = {}
default persistent.read_chapters = []
default persistent.signal_effects = True
default monika_count = 0
default in_sayori_route = False
default monika_triggered = False
default current_chapter = ""

init python:
    import json

    with renpy.file("bookmarks.json") as bookmark_file:
        BOOKMARKS = json.load(bookmark_file)

    GROUPS = [
        ("hug", "抱抱能量", ["拥抱%d" % i for i in range(1, 16)], "有朋自远方来", "theater1"),
        ("school", "学在脚大", ["脚大%d" % i for i in range(1, 8)], "假装游刃有余的一天", "theater2"),
        ("ending", "九种答案", ["结局%d" % i for i in range(1, 10)], "孤独的守望", "theater3"),
        ("possibility", "另一种可能", ["另一种可能%d" % i for i in range(1, 3)], "殊途同归", "theater4"),
        ("duck", "丑小鸭也有春天", ["丑小鸭%d" % i for i in range(1, 7)], "奇妙夜", "theater5"),
    ]
    ENDINGS = [
        ("S-1", "八点之后", "chapter42", "有些告别，没有说出口。"),
        ("S-2", "早晨的牛肉汤", "chapter45", "在可以触碰的地方，继续同行。"),
        ("S-3", "阳光照进来了", "chapter50", "即使世界是假的，此刻也可以是真的。"),
        ("C-1", "没有寄出的信", "chapter68", "那张纸，留下了没有答完的问题。"),
        ("C-2", "凝望东方", "chapter69", "有些距离，无法用一句道歉消除。"),
        ("C-3", "直到苍穹尽头", "chapter70", "不是奇迹，是依然在身边。"),
        ("O-2 / S-4", "弄堂口的灯", "chapter90", "一个不是悲剧的悲剧。"),
        ("O-1", "渡口与彼岸", "chapter100", "冬天的江风里，我们重新认识彼此。"),
        ("M", "Sayo-nara", "chapter999", "向屏幕的另一侧，道一声再见。"),
    ]
    HINTS = {
        "hug": "不同路线都有拥抱的瞬间；分岔前存档，或从已读章节回看。",
        "school": "留意共同篇、文学社与广播站的校园生活。",
        "ending": "三个社团通往不同线路。看似乱码的选项，也会被记住。",
        "possibility": "在文学社之后，聆听两种关于真实的回答。",
        "duck": "从第一次同行开始，试着了解 Obedience 的选择。",
    }

    def grant_achievement(name):
        if debug_session:
            return
        if persistent.achievements is None:
            persistent.achievements = {}
        if not persistent.achievements.get(name, False):
            persistent.achievements[name] = True
            renpy.save_persistent()
            renpy.notify("收进回忆手册 · " + name)

    def check_achievement_group(key):
        return any(key == k and all(persistent.achievements.get(n, False) for n in names)
                   for k, title, names, side, label in GROUPS)

    def group_progress(names):
        return sum(bool(persistent.achievements.get(n, False)) for n in names)

    def enter_chapter(label):
        store.current_chapter = label
        horror_reset()
        store.horror_stage = 2 if label in ("chapter999", "chapter1000", "chapter1001", "chapter1007") else (1 if monika_count and label != "chapter1009" else 0)
        if not debug_session and label not in persistent.read_chapters:
            persistent.read_chapters.append(label)
            renpy.save_persistent()
        if label.startswith("chapter100") and label != "chapter100":
            track = "audio/afterimage.wav"
        elif label in ("chapter999", "chapter42", "chapter45", "chapter46", "chapter47", "chapter64", "chapter65", "chapter66", "chapter67", "chapter68", "chapter69", "chapter90", "theater5_chapter4", "theater5_chapter5"):
            track = "audio/blue_hour.wav"
        else:
            track = "audio/ohayou.wav"
        if renpy.music.get_playing() != track:
            renpy.music.play(track, fadeout=1.0, fadein=1.5)

    def replay_scope():
        # A replay gets its own rollback-aware state; it never borrows route flags.
        return {"monika_count": 0, "in_sayori_route": False,
                "monika_triggered": False, "current_chapter": "", "horror_stage": 0, "debug_session": False}


define config.main_menu_music = "audio/ohayou.wav"
default preferences.music_volume = 0.35

transform solo:
    xalign 0.5 yalign 1.0
transform duo_left:
    xalign 0.22 yalign 1.0
transform duo_right:
    xalign 0.78 yalign 1.0
transform trio_left:
    xalign 0.04 yalign 1.0
transform trio_right:
    xalign 0.96 yalign 1.0
transform quartet_1:
    xalign 0.0 yalign 1.0
transform quartet_2:
    xalign 0.33 yalign 1.0
transform quartet_3:
    xalign 0.67 yalign 1.0
transform quartet_4:
    xalign 1.0 yalign 1.0

# A deliberate, brief in-game signal interruption. No desktop or file tricks.
screen signal_disturbance():
    zorder 80
    if persistent.signal_effects:
        add Solid("#10254cdd")
        for row in range(0, 1080, 18):
            add Solid("#72b9e011") ypos row ysize 3
        text "SIGNAL LOST\n\n鑾Ξ鍗" align (0.5, 0.45) size 66 color "#d5efff"

translate None strings:
    old "Start"
    new "开始新的故事"
    old "Load"
    new "读取存档"
    old "Save"
    new "保存进度"
    old "Preferences"
    new "阅读设置"
    old "About"
    new "关于作品"
    old "Help"
    new "操作说明"
    old "Quit"
    new "退出游戏"
    old "Return"
    new "返回"
    old "History"
    new "对话历史"
    old "Main Menu"
    new "主菜单"
    old "End Replay"
    new "结束回看"
    old "Back"
    new "回退"
    old "Skip"
    new "快进"
    old "Auto"
    new "自动"
    old "Q.Save"
    new "快存"
    old "Q.Load"
    new "快读"
    old "Prefs"
    new "设置"

    old "Display"
    new "显示"
    old "Window"
    new "窗口"
    old "Fullscreen"
    new "全屏"
    old "Unseen Text"
    new "未读文本"
    old "After Choices"
    new "选择后继续快进"
    old "Transitions"
    new "转场"
    old "Text Speed"
    new "文字速度"
    old "Auto-Forward Time"
    new "自动阅读间隔"
    old "Music Volume"
    new "音乐音量"
    old "Sound Volume"
    new "音效音量"
    old "Mute All"
    new "全部静音"
    old "Yes"
    new "是"
    old "No"
    new "否"
    old "empty slot"
    new "空存档位"
