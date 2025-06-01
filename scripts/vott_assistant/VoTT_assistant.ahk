#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%

; set space as lbutton:
space::LButton

; set w as l:
w::l

; make work easer:
e::
Sleep, 300
Send, l
Sleep, 40
Send, l
Sleep, 40
return

q::
Sleep, 300
Send, l
Sleep, 40
Send, l
Sleep, 40
return

; final tag:
i::
MouseGetPos, xpos, ypos 
MouseMove, 821, 651
MouseClick
Sleep, 200
MouseMove, xpos, ypos
return

; alt final tag:
!i::
MouseGetPos, xpos, ypos 
MouseMove, 821, 651
MouseClick
Sleep, 200
MouseMove, xpos, ypos
return


; to break loops:
Esc::
BreakLoop = 1
return



; remove an object:
x::
MouseGetPos, xpos, ypos
MouseMove, 279, 61
MouseClick
Sleep, 70
MouseMove, 297, 79
MouseClick
Sleep, 30
MouseMove, xpos-5, ypos+5
MouseClick
Sleep, 70
MouseMove, xpos+22, ypos+22
MouseClick
Sleep, 30
MouseMove, xpos, ypos
return

; remove an object for 50 times:
#!x::
loop,
{
    if(BreakLoop = 1)
        {
        BreakLoop = 0
        break
        }
    Send, x
    Sleep, 250
    Send, e
    Sleep, 450

}
return


; remove an object:
z::
MouseGetPos, xpos, ypos
MouseMove, 279, 61
MouseClick
Sleep, 70
MouseMove, 297, 79
MouseClick
Sleep, 30
MouseMove, xpos+5, ypos+5
MouseClick
Sleep, 70
MouseMove, xpos-22, ypos+22
MouseClick
Sleep, 30
MouseMove, xpos, ypos
return

; remove an object for 50 times:
#!z::
loop,
{
    if(BreakLoop = 1)
        {
        BreakLoop = 0
        break
        }
    Send, z
    Sleep, 250
    Send, e
    Sleep, 450

}
return


h::
MouseMove, 900, 220
MouseClick
Sleep, 140
MouseMove, 950, 230
MouseClick
Sleep, 40
Send, e
Sleep, 450
return

#!h::
loop,
{
    if(BreakLoop = 1)
        {
        BreakLoop = 0
        break
        }

    Send, h
    Sleep, 650
}
return


#!p::
loop,
{
    if(BreakLoop = 1)
        {
        BreakLoop = 0
        break
        }

    Send, e
    Sleep, 450
    Send, d
    Sleep, 200
}
return



#!\::
MouseGetPos, xpos, ypos 
MsgBox, The cursor is at X%xpos% Y%ypos%.
return



; exit this script:
#!q::
DetectHiddenWindows, On
SetTitleMatchMode, 2
WinClose, VoTT_assistant.ahk
return
