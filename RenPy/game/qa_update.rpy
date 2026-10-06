# Excluded from player builds. Real replay contexts and rendered screen checks.
label qa_debug_probe:
    $ assert debug_session and monika_count == 2 and in_sayori_route
    $ enter_chapter("qa-never-collect")
    $ grant_achievement("qa-never-collect")
    $ assert "qa-never-collect" not in persistent.achievements
    $ assert "qa-never-collect" not in persistent.read_chapters
    $ monika_count = 100
    $ horror_stage = 2
    show screen horror_burst("portrait")
    $ renpy.end_replay()
    return

label qa_fx_launch:
    show screen qa_driver
    jump debug_launch

label qa_update_suite:
    $ preferences.text_cps = 0
    $ preferences.music_volume = 0
    $ preferences.set_volume("sfx", 0)
    $ persistent.achievements = {"keep-me": True}
    $ persistent.read_chapters = ["keep-me"]
    $ monika_count = 77
    $ current_chapter = "qa-parent"
    $ horror_stage = 0
    $ renpy.game.call_replay("debug_launch", scope=debug_scope("qa_debug_probe", 2, True))
    $ assert not debug_session and monika_count == 77 and current_chapter == "qa-parent" and horror_stage == 0
    $ assert not renpy.get_screen("horror_burst")
    $ assert persistent.achievements == {"keep-me": True} and persistent.read_chapters == ["keep-me"]
    $ qa_log("PASS debug replay preserves parent state and all persistent collection data")
    $ qa_effects = ["debug_fx_signal", "debug_fx_rupture", "debug_fx_stare", "debug_fx_false_end"]
    $ qa_levels = [2, 1, 0]
    while qa_levels:
        $ qa_level = qa_levels.pop(0)
        $ set_horror_level(qa_level)
        $ qa_fx_queue = list(qa_effects)
        while qa_fx_queue:
            $ qa_fx = qa_fx_queue.pop(0)
            show screen qa_driver
            $ renpy.game.call_replay("qa_fx_launch", scope=debug_scope(qa_fx))
            hide screen qa_driver
            $ assert not renpy.get_screen("horror_burst")
            $ assert not debug_session and monika_count == 77
        $ qa_log("PASS all four effect previews at intensity %d" % qa_level)
    $ assert persistent.achievements == {"keep-me": True} and persistent.read_chapters == ["keep-me"]
    $ set_horror_level(2)
    scene bg hollow
    show monika normal at solo
    show screen horror_burst("fracture")
    $ renpy.pause(1.5)
    $ qa_shot("fx-fracture")
    show screen horror_burst("mirror")
    $ renpy.pause(1.5)
    $ qa_shot("fx-mirror")
    show screen horror_burst("portrait")
    $ renpy.pause(1.5)
    $ qa_shot("fx-portrait")
    $ horror_reset()
    $ qa_log("PASS update 2.1 screenshots and effect rendering")
    $ renpy.quit()

testcase update21:
    $ _test.timeout = 120.0
    pause 1.5
    "调试室" pos (0.5, 0.5)
    pause 1.5
    assert renpy.get_screen("debug_room")
    $ qa_shot("debug-room")
    "立绘与同屏比例" pos (0.5, 0.5)
    pause 1.5
    assert renpy.get_screen("debug_portraits")
    $ qa_shot("cast-four")
    "2 人同屏" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("cast-two")
    "返回调试室" pos (0.5, 0.5)
    pause 1.0
    "Monika" pos (0.5, 0.5)
    pause 1.0
    $ qa_shot("debug-monika-list")
    "chapter1007" pos (0.5, 0.5)
    pause 1.5
    assert debug_session and current_chapter == "chapter1007"
    $ qa_shot("debug-scene")
    "结束本次测试" pos (0.5, 0.5)
    pause 1.5
    assert renpy.get_screen("debug_room")
    "返回" pos (0.5, 0.5)
    run Start("qa_update_suite")
    pause 120.0

testcase portraits:
    pause 1.5
    "调试室" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("debug-room")
    "立绘与同屏比例" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("cast-four")
    "2 人同屏" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("cast-two")
    "obedience" pos (0.5, 0.5)
    "1 人同屏" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("cast-obedience")
    $ renpy.quit()

testcase shortcut:
    $ _test.timeout = 20.0
    $ persistent.debug_enabled = True
    run Start("chapter1")
    pause 1.0
    type F6
    pause 1.0
    assert renpy.get_screen("debug_room")
    type "chapter1007"
    pause 1.0
    assert renpy.get_screen("debug_room").scope["query"] == "chapter1007"
    "Monika · chapter1007" pos (0.5, 0.5)
    pause 1.0
    assert debug_session and current_chapter == "chapter1007"
    "结束本次测试" pos (0.5, 0.5)
    pause 1.0
    $ qa_shot("shortcut-return")
    assert renpy.get_screen("debug_room")
    "返回" pos (0.5, 0.5)
    pause 1.0
    assert not debug_session and current_chapter == "chapter1"
    $ qa_log("PASS F6, live search, direct scene replay, return to parent chapter")
    $ renpy.quit()
