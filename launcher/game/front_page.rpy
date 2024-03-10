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

define PROJECT_ADJUSTMENT = ui.adjustment()

init python:

    import datetime

    # Used for testing.
    def Relaunch():
        renpy.quit(relaunch=True)

screen front_page:

    frame:
        alt ""

        style_group "l"
        style "l_root"

        has hbox

        # Projects list section - on left.

        frame:
            style "l_projects"
            xmaximum 300
            right_margin 2

            top_padding 20
            bottom_padding 13

            side "t c b":

                window style "l_label":

                    has hbox:
                        xfill True

                    text _("PROJECTS:") style "l_label_text" size 36 yoffset 10

                side "c r":

                    viewport:
                        yadjustment PROJECT_ADJUSTMENT
                        mousewheel True
                        use front_page_project_list

                    vbar:
                        style "l_vscrollbar"
                        adjustment PROJECT_ADJUSTMENT

                vbox:
                    add HALF_SPACER
                    add HALF_SPACER

                    vbox:
                        xfill True

                        textbutton _("Create New Project"):
                            xoffset 20
                            action Jump("new_project")
                        textbutton _("Launch!"):
                            xoffset 20
                            text_size 30
                            action project.Launch()

        # Project section - on right.

        if project.current is not None:
            use front_page_project
    imagebutton:
        idle im.MatrixColor(renpy.easy.displayable("images/logo.png"), im.matrix.brightness(-0.7))
        hover im.MatrixColor(renpy.easy.displayable("images/logo.png"), im.matrix.brightness(0.0))
        at resize_logo
        action Jump("about") xalign 0.9 yalign 0.8

# This is used by front_page to display the list of known projects on the screen.
screen front_page_project_list:
    timer 0.3 action Function(project.Rescan()) repeat True

    $ projects = project.manager.projects
    $ templates = project.manager.templates

    vbox:
        xoffset 10

        if templates and persistent.show_templates:

            for p in templates:

                textbutton _("[p.name!q] (template)"):
                    action project.Select(p)
                    alt _("Select project [text].")
                    style "l_list"

            null height 12

        if projects:

            for p in projects:

                textbutton "[p.name!q]":
                    action project.Select(p)
                    alternate project.Launch()
                    alt _("Select project [text].")
                    style "l_list"

# This is used for the right side of the screen, which is where the project-specific
# buttons are.
screen front_page_project:

    $ p = project.current

    window yoffset 63 xoffset -7:

        has vbox

        frame style "l_label":
            has hbox xfill True

        frame style "l_indent":
            has vbox

            textbutton "Open project directory" action OpenDirectory(os.path.join(p.path, "."), absolute=True)

        add SPACER

        grid 2 1:
            xfill True
            spacing HALF_INDENT

            frame style "l_indent":
                has vbox

                textbutton _("Navigate Script") action Jump("navigation")
                textbutton _("Check Script (Lint)") action Call("lint")

                if project.current.exists("game/gui.rpy"):
                    textbutton _("Change/Update GUI") action Jump("change_gui")
                else:
                    textbutton _("Change Theme") action Jump("choose_theme")


                textbutton _("Delete Persistent") action Jump("rmpersistent")
                textbutton _("Force Recompile") action Jump("force_recompile")

                # textbutton "Relaunch" action Relaunch

            frame style "l_indent":
                has vbox

                if ability.can_distribute:
                    textbutton _("Build Distributions") action Jump("build_distributions")

                textbutton _("Android") action Jump("android")
                textbutton _("iOS") action Jump("ios")
                textbutton _("Web") + " " + _("(Beta)") action Jump("web")
                textbutton _("Generate Translations") action Jump("translate")
                textbutton _("Extract Dialogue") action Jump("extract_dialogue")

label main_menu:
    return

label start:
    $ dmgcheck()

    jump expression renpy.session.pop("launcher_start_label", "before_front_page")

default persistent.has_chosen_language = False
default persistent.has_update = False

label before_front_page:

    if (not persistent.has_chosen_language) or ("RENPY_CHOOSE_LANGUAGE" in os.environ):

        if (_preferences.language is None) or ("RENPY_CHOOSE_LANGUAGE" in os.environ):
            call choose_language

        $ persistent.has_chosen_language = True

    call editor_check

label post_editor_check:
label front_page:

    if persistent.daily_update_check and ((not persistent.last_update_check) or (datetime.date.today() > persistent.last_update_check)):
        python hide:
            persistent.last_update_check = datetime.date.today()
            renpy.invoke_in_thread(fetch_update_channels)

    call screen front_page
    jump front_page


label lint:
    python hide:

        interface.processing(_("Checking script for potential problems..."))
        lint_fn = project.current.temp_filename("lint.txt")

        persistent.lint_options.discard("--orphan-tl") # compat
        persistent.lint_options.discard("--builtins-parameters") # compat
        persistent.lint_options.discard("--words-char-count") # compat

        project.current.launch([ 'lint', lint_fn, ] + list(persistent.lint_options), wait=True)

        e = renpy.editor.editor
        e.begin(True)
        e.open(lint_fn)
        e.end()

    return

label rmpersistent:

    python hide:
        interface.processing(_("Deleting persistent data..."))
        project.current.launch([ 'rmpersistent' ], wait=True)

    jump front_page

label force_recompile:

    python hide:
        interface.processing(_("Recompiling all rpy files into rpyc files..."))
        project.current.launch([ 'compile' ], wait=True)

    jump front_page
