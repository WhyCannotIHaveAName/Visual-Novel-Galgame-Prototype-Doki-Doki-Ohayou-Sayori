# Development-only native Ren'Py tests; excluded from packaged releases.
init python:
    import os
    QA_DIR = os.path.abspath(os.environ.get("OHAYOU_QA_DIR", os.path.join(config.basedir, "qa-results")))
    os.makedirs(QA_DIR, exist_ok=True)
    def qa_shot(name):
        renpy.screenshot(os.path.join(QA_DIR, name + ".png"))

testcase smoke:
    $ _test.timeout = 30.0
    pause 1.5
    $ qa_shot("title")
    "回忆手册" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("memories")
    "成就与小剧场" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("theaters")
    "已读章节" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("chapters")
    "美术手帐" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("gallery")
    "返回" pos (0.5, 0.5)
    pause 1.5
    "开始新的故事" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("content")
    "开始阅读" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("opening")
    run Jump("chapter8")
    pause 1.5
    $ qa_shot("obedience")
    run Jump("chapter83")
    pause 1.5
    $ qa_shot("leo")
    run Jump("theater1_chapter3")
    pause 1.5
    $ qa_shot("shane")
    run ShowMenu("save")
    pause 1.5
    $ qa_shot("save")
    run Return()
    run ShowMenu("preferences")
    pause 1.5
    $ qa_shot("preferences")
    run Return()
    run ShowMenu("help")
    pause 1.5
    $ qa_shot("help")
    run Return()
    run Jump("chapter1007")
    click until "Just monika"
    click
    pause 1.5
    $ qa_shot("monika-choices")
    assert renpy.get_screen("choice")
    assert len(renpy.get_screen("choice").scope["items"]) == 11
    $ qa_log("PASS UI navigation, gallery, help, save, preferences, 11-option hidden menu")
    $ renpy.quit()
