# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

screen about:

    $ version = renpy.version()

    frame:
        style_group "l"
        style "l_root"

        window:
            yoffset 70
            xfill True

            has vbox xfill True

            add "images/logo.png" xalign 0.5 yoffset -5 zoom 0.3

            null height 15

            text _("[interface.version]") xalign 0.5 style "l_link" bold True

            null height 20

            textbutton _("Preferences") xalign 0.5 action Jump("preferences")
            textbutton _("View license") xalign 0.5 action interface.OpenLicense()
            textbutton _("Documentation") xalign 0.5 action interface.OpenDocumentation()
            textbutton _("CARRY Website") xalign 0.5 action OpenURL(interface.RENPY_URL)
            if ability.can_update:
                textbutton _("Update") xalign 0.5 action Jump("update"):
                    if persistent.has_update:
                        text_color "#F96854"
                        text_hover_color Color("#F96854").tint(.8)

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label about:
    call screen about

