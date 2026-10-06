# 游戏入口。剧情在 story.rpy；系统在 systems.rpy；界面在 presentation.rpy。
label splashscreen:
    return

label start:
    $ debug_session = False
    $ horror_stage = 0
    $ horror_reset()
    call screen content_note
    $ monika_count = 0
    $ in_sayori_route = False
    $ monika_triggered = False
    jump chapter1

label ending_card(number):
    $ horror_stage = 0
    $ horror_reset()
    stop music fadeout 1.0
    scene bg campus with fade
    call screen ending_postcard(number)
    $ renpy.end_replay()
    return
