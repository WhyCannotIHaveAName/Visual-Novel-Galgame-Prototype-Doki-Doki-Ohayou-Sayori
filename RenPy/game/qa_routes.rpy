# Native engine integration tests. This file is excluded from player builds.
default qa_case = {}
default qa_expected = 0
default qa_found = 0
default qa_count = 0
default qa_visited = []

init python:
    def qa_tick():
        if renpy.get_screen("choice"):
            screen = renpy.get_screen("choice")
            items = screen.scope["items"]
            index = qa_case.get(current_chapter, 0)
            return renpy.run(items[index].action)
        elif renpy.get_screen("ending_postcard"):
            number = renpy.get_screen("ending_postcard").scope["number"]
            assert persistent.achievements.get("结局%d" % number), "Ending not registered"
            store.qa_found = number
            return True
        elif renpy.get_screen("say"):
            if current_chapter not in qa_visited:
                qa_visited.append(current_chapter)
            store.qa_count += 1
            renpy.end_interaction(True)

    def qa_log(message):
        path = os.path.join(QA_DIR, "runtime-checks.txt")
        with open(path, "a", encoding="utf-8") as f:
            f.write(message + "\n")

screen qa_driver():
    timer .01 repeat True action Function(qa_tick)

label qa_suite:
    $ preferences.text_cps = 0
    $ preferences.transitions = 0
    $ preferences.music_volume = 0
    $ persistent.achievements = {}
    $ persistent.read_chapters = []
    $ qa_visited = []
    $ qa_count = 0
    $ qa_log("BEGIN native complete-playthrough suite")
    python:
        qa_cases = [
            (1, {"chapter3":0,"chapter12":0,"chapter30":0,"chapter37":1,"chapter40":0}),
            (2, {"chapter3":1,"chapter12":1,"chapter30":0,"chapter37":1,"chapter40":1}),
            (3, {"chapter3":2,"chapter12":3,"chapter30":0,"chapter37":0,"chapter38":0}),
            (4, {"chapter30":1,"chapter67":0}),
            (5, {"chapter30":1,"chapter67":1}),
            (6, {"chapter30":1,"chapter67":2}),
            (7, {"chapter30":2,"chapter88":0}),
            (8, {"chapter30":2,"chapter88":1}),
            (9, {"chapter19":1,"chapter26":1,"chapter30":1,"chapter66":1}),
            (9, {"chapter3":0,"chapter12":2,"chapter30":0,"chapter31":1,"chapter37":2}),
            (9, {"chapter30":0,"chapter31":2,"chapter38":1}),
            (9, {"chapter19":1,"chapter26":1,"chapter30":2,"chapter88":1,"chapter99":1}),
        ]
    while qa_cases:
        $ qa_expected, qa_case = qa_cases.pop(0)
        $ qa_found = 0
        $ monika_count = 0
        $ in_sayori_route = False
        $ monika_triggered = False
        show screen qa_driver
        call chapter1
        hide screen qa_driver
        $ assert qa_found == qa_expected, (qa_found, qa_expected)
        $ qa_log("PASS full route -> ending %d; menu choices %r" % (qa_expected, qa_case))
    $ assert all(check_achievement_group(g[0]) for g in GROUPS), persistent.achievements
    $ qa_log("PASS all 39 achievements earned by playing; all five theaters unlocked")
    $ qa_sides = ["theater1", "theater2", "theater3", "theater4", "theater5"]
    while qa_sides:
        $ qa_side = qa_sides.pop(0)
        show screen qa_driver
        call expression qa_side
        hide screen qa_driver
        $ qa_log("PASS complete side story -> " + qa_side)
    $ qa_log("PASS %d rendered dialogue interactions across %d chapters" % (qa_count, len(qa_visited)))
    $ monika_count = 2
    $ persistent.qa_loaded = False
    show screen qa_driver
    "存档恢复检查。"
    $ renpy.save("qa-proof")
    if not persistent.qa_loaded:
        $ persistent.qa_loaded = True
        $ renpy.save_persistent()
        $ monika_count = 99
        $ renpy.load("qa-proof")
    $ assert monika_count == 2
    $ qa_log("PASS native save/load restores route counter")
    $ renpy.unlink_save("qa-proof")
    hide screen qa_driver
    $ monika_count = 77
    $ current_chapter = "qa-parent"
    $ renpy.game.call_replay("qa_replay_target", scope=replay_scope())
    $ assert monika_count == 77 and current_chapter == "qa-parent"
    $ qa_log("PASS ending replay returns and preserves parent route state")
    $ persistent.qa_completed = True
    $ renpy.save_persistent()
    $ qa_log("ALL PASS")
    $ renpy.quit()

label qa_replay_target:
    $ assert monika_count == 0 and not in_sayori_route
    show screen qa_driver
    jump chapter50

testcase routes:
    $ _test.timeout = 900.0
    pause .5
    run Start("qa_suite")
    pause 900.0

testcase persistence:
    pause 1.0
    assert persistent.qa_completed
    assert all(check_achievement_group(g[0]) for g in GROUPS)
    $ qa_log("PASS new engine process retained all achievements and theater unlocks")
    $ renpy.quit()

testcase entry:
    $ _test.timeout = 30.0
    pause 1.0
    $ qa_shot("title")
    run Start()
    pause 1.5
    $ qa_shot("content")
    "开始阅读" pos (0.5, 0.5)
    pause 1.5
    $ qa_shot("opening")
    run Jump("chapter8")
    pause 1.5
    $ qa_shot("obedience")
    run ShowMenu("preferences")
    pause 1.5
    $ qa_shot("preferences")
    run Return()
    run ShowMenu("save")
    pause 1.5
    $ qa_shot("save")
    $ renpy.quit()
