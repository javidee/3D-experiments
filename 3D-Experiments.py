#!/usr/bin/env python3
# coding: utf-8
import PySimpleGUI as sg
import os
import numpy as np
import pybullet as p
import time
import pybullet_data

sg.theme("DarkPurple1")

layout = [[sg.Button("АПУ", size=(20, 2))],
          [sg.Button("АНУ", size=(20, 2))]]
window = sg.Window("3D Experiments", layout, size=(600, 200))

#!Абсолютно пружний удар

layoutApu = [[sg.Button("Що таке АПУ?", size=(20, 2))],
             [sg.Button("Дивитись", size=(20, 2))]]
windowApu = sg.Window("АПУ", layoutApu)
def APU():
        while True:
            eventApu, valuesApu = windowApu.read()
            if eventApu == sg.WIN_CLOSED:
                break
            if eventApu == "Що таке АПУ?":
                eventApu = ""
                APUexplain()
            if eventApu == "Дивитись":
                eventApu = ""
                APUshow()
layoutApuExplain = [[sg.Text("Абсолютно пружним називають такий удар,\nпісля якого в тілах, що зазнали зіткнення, не залишається жодних деформацій, \nа кінетична енергія до і після зіткнення не змінюється.", font = 18)],
                    [sg.Button("Назад", size=(20, 2))]]
windowApuExplain = sg.Window("Пояснення", layoutApuExplain)
def APUexplain():
    while True:
        eventApuExplain, valuesApuExplain = windowApuExplain.read()
        if eventApuExplain == sg.WIN_CLOSED:
            break
        if eventApuExplain == "Назад":
            windowApuExplain.close()
            APU()
layoutApuShow = [[sg.Text("Маса першого об'єкту: "), sg.Input()],
                  [sg.Text("Маса другого об'єкту: "), sg.Input()],
                  [sg.Text("Прискорення"), sg.Input()],
                  [sg.Button("Показати", size=(20, 2))]]
windowApuShow = sg.Window("Параметри", layoutApuShow)
def APUshow():
    while True:
        eventApuShow, valuesApuShow = windowApuShow.read()
        if eventApuShow == sg.WIN_CLOSED:
            break
        if eventApuShow == "Показати":
            APUpybullet(int(valuesApuShow[0]), int(valuesApuShow[1]), (10 * int(valuesApuShow[2])))


def APUpybullet(mass1, mass2, ALPHA):
    physicsClient = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-10)
    planeId = p.loadURDF("plane.urdf")
    startPos=[0, 0, 0]
    checkPos = -1
    startPos1 = [-25, 0, 1]
    startPos2 = [25, 0, 1]
    sphere1 = p.loadURDF("sphere2red.urdf", startPos1)
    sphere2 = p.loadURDF("sphere2red.urdf", startPos2)
    p.changeDynamics(sphere1, -1, mass=mass1)
    p.changeDynamics(sphere2, -1, mass=mass2)
    while True:
        sphere1Pos, sphere1Orn = p.getBasePositionAndOrientation(sphere1)
        sphere2Pos, sphere2Orn = p.getBasePositionAndOrientation(sphere2)
        force1 = ALPHA * (np.array(startPos) - np.array(sphere1Pos))
        force2 = ALPHA * (np.array(startPos) - np.array(sphere2Pos))
        pos1comp = round(np.array(sphere1Pos)[0], 1)
        pos2comp = round(np.array(sphere2Pos)[0], 1)
        if pos1comp == checkPos or pos2comp == abs(checkPos):
            ALPHA = 0
        p.applyExternalForce(objectUniqueId=sphere1, linkIndex=-1, forceObj=force1, posObj=sphere1Pos, flags=p.WORLD_FRAME)
        p.applyExternalForce(objectUniqueId=sphere2, linkIndex=-1, forceObj=force2, posObj=sphere2Pos, flags=p.WORLD_FRAME)
        p.stepSimulation()
        time.sleep(1./240.)

        print (pos1comp)

    p.disconnect()


#! Абсолютно непружний удар

layoutAnu = [[sg.Button("Що таке АНУ?", size=(20, 2))],
             [sg.Button("Дивитись", size=(20, 2))]]
windowAnu = sg.Window("АПУ", layoutAnu)
def ANU():
    while True:
        eventAnu, valuesAnu = windowAnu.read()
        if eventAnu == sg.WIN_CLOSED:
            break
        if eventAnu == "Що таке АНУ?":
            eventAnu = ""
            ANUexplain()
        if eventAnu == "Дивитись":
            eventAnu = ""
            ANUshow()
layoutAnuExplain = [[sg.Text("Абсолютно непружним ударом називають такий удар,\nпри якому вся енергія відносного руху тіл переходить у тепло і тіла злипаються.", font = 18)],
                    [sg.Button("Назад", size=(20, 2))]]
windowAnuExplain = sg.Window("Пояснення", layoutAnuExplain)
def ANUexplain():
    while True:
        eventAnuExplain, valuesAnuExplain = windowAnuExplain.read()
        if eventAnuExplain == sg.WIN_CLOSED:
            break
        if eventAnuExplain == "Назад":
            windowAnuExplain.close()
            ANU()
layoutAnuShow = [[sg.Text("Маса першого об'єкту: "), sg.Input()],
                  [sg.Text("Маса другого об'єкту: "), sg.Input()],
                  [sg.Text("Прискорення"), sg.Input()],
                  [sg.Button("Показати", size=(20, 2))]]
windowAnuShow = sg.Window("Параметри", layoutAnuShow)
def ANUshow():
    while True:
        eventAnuShow, valuesAnuShow = windowAnuShow.read()
        if eventAnuShow == sg.WIN_CLOSED:
            break
        if eventAnuShow == "Показати":
            pass


#! Головне вікно

layout = [[sg.Button("АПУ", size=(20, 2))],
          [sg.Button("АНУ", size=(20, 2))]]
window = sg.Window("Привіт!", layout)
def main():    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "АПУ":
            window.close()
            APU()
        if event == "АНУ":
            window.close()
            ANU()


main()
# TODO:  window + pybullet.