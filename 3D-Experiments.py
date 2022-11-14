#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import webbrowser
import os
import numpy as np
import pybullet as p
import time
import pybullet_data

sg.theme('DarkPurple1')

path = "F:\Projects\Dovidnuk.pdf"

#! Головне вікно
def mainWin():
    col = [  [sg.Button('ЗНО з фізики', font = (20), size=(20, 2)), sg.Button("3D-моделі", size=(20, 2), font=(20))],
              [sg.Button("Тести з фізики", font = (20), size=(20, 2)), sg.Button("Довідник з фізики", font = (20), size = (20, 2))],
                [sg.Button('Задачі з фізики', font = (20), size=(20, 2))]  ]
    layout = [  [sg.Column(col , justification='center')]  ]
    window = sg.Window('Фізика', layout)
    while True:
        event, values = window.read()
        if event == 'ЗНО з фізики':
            webbrowser.open('https://zno.osvita.ua/physics/')
        elif event == "Тести з фізики":
            webbrowser.open("https://naurok.com.ua/test/fizika")
        elif event == "Довідник з фізики":
            os.system(path)
        elif event == "3D-моделі":
            models3D()
        elif event == 'Задачі з фізики':
            tasksWin()
        if event == sg.WIN_CLOSED:
            break

    window.close()


#! Задачі з фізики
data_fizik_tasks = {
    "questions" : {
        "question1" : (" Закони класичної механіки справедливі у тих інерціальних системах відліку \n відносно яких тіла рухаються зі швидкістю"),
        "question2" : (" Спеціальна теорія відносності розглядає фізичні процеси"),
        "question3" : (" Учень масою 40 кг за 0,5 хв піднявся сходами на висоту 30 м. \n Яку потужність розвинув учень"),
        "question4" : (" Під час оранки трактор долає силу опору 8 кН \n розвиваючи корисну потужність 40 кВт. З якою швидкістю рухається трактор"),
        "question5" : (" Тіло масою 6кг під дією сталої сили змінило свою швидкість на 2м/с за 10с. \n Визначте силу, яка діяла на тіло"),
        "question6" : (" Перша космічна швидкість становить"),
        "question7" : (" Період обертання можна виразити формулою"),
        "question8" : (" Обчисліть частоту обертання барабана лебідки діаметром 16см під час підйому \n вантажу зі швидкістю 49 см/с"),
        "question9" : (" Перші 5 с тіло рухалось рівномірно і прямолінійно зі швидкістю 4 м/с \n а наступні 6 с - з прискоренням 2 м/с2, напрямленим так само як і швидкість. Яке переміщення тіла за весь час руху"),
        "question10" : (" Яку ємність треба включити в коливальний контур радіостанції служби «103» \n щоб при індуктивності 50 мкГн отримати вільні коливання з частотою 10 МГц"),
    },
        "answers" : {
            "answer1" : "v набагато менша за c",
            "answer2" : "тільки в інерціальних системах відліку",
            "answer3" : "400 Вт",
            "answer4" : "5 м/с",
            "answer5" : "1.2Н",
            "answer6" : "7,9 км/с",
            "answer7" : "T= t/N",
            "answer8" : "6.125",
            "answer9" : "80м",
            "answer10" : "5 пФ",
        }
    }

def tasksWin():
    col_fizik = [[sg.Text(data_fizik_tasks['questions']["question1"], key = "quest")],
        [sg.Input(key = "answer")],
        [sg.Button('Далі', font = (20), size = (20, 3))]]
    layout_fizik = [col_fizik]
    windowTasksFizik = sg.Window("Tasks", layout_fizik, size = (600, 400))
    n = 1
    s = 0
    while True:
        event_task, values_task = windowTasksFizik.read()
        if event_task == "Далі":
            values_task[n] = windowTasksFizik["answer"].get()
            if values_task[n] == data_fizik_tasks["answers"]["answer" + str(n)]:
                s = s + 1
            windowTasksFizik["answer"].Update("")
            n = n + 1
            if n == 11:
                windowTasksFizik.close()
                layout_res = [[sg.Text("Кількість правильних відповідей: " + str(s) + "(" + str(s) + "0%)", font = (15))]]
                windowResult = sg.Window("Результати", layout_res, size = (500, 150))
                event_res = windowResult.read()
                if event_res == sg.WIN_CLOSED:
                    break
            else:
                windowTasksFizik["quest"].Update(data_fizik_tasks["questions"]["question" + str(n)])
        if event_task == sg.WIN_CLOSED:
            break
    windowTasksFizik.close()


#! Абсолютно пружний удар
def APU():
    layoutApu = [[sg.Text("Маса першого об'єкту: "), sg.Input()],
                  [sg.Text("Маса другого об'єкту: "), sg.Input()],
                  [sg.Text("Прискорення"), sg.Input()],
                  [sg.Button("Показати", size=(20, 2))]]
    windowApu = sg.Window("Параметри", layoutApu)
    while True:
        eventApu, valuesApu = windowApu.read()
        if eventApu == "Показати":
            APUpybullet(int(valuesApu[0]), int(valuesApu[1]), (10 * int(valuesApu[2])))

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
        pos1comp = round(np.array(sphere1Pos)[0])
        pos2comp = round(np.array(sphere2Pos)[0])
        if pos1comp == -1 or pos2comp == 1:
            ALPHA = 0
        p.applyExternalForce(objectUniqueId=sphere1, linkIndex=-1, forceObj=force1, posObj=sphere1Pos, flags=p.WORLD_FRAME)
        p.applyExternalForce(objectUniqueId=sphere2, linkIndex=-1, forceObj=force2, posObj=sphere2Pos, flags=p.WORLD_FRAME)
        p.stepSimulation()
        time.sleep(1./240.)

    p.disconnect()


#! 3D-моделі №1
def models3D():
    layoutModels3D = [[sg.Button("Механіка", font=(20)), sg.Button("Сила тертя", font=(20))]]
    windowModels3D = sg.Window("Вибір розділу", layoutModels3D)
    while True:
        eventModels3D, valuesModels3D = windowModels3D.read()
        if eventModels3D == "Механіка":
            layoutMechanic = [[sg.Button("Абсолютно пружний удар", font=(18)), sg.Button("Абсолютно непружний удар", font=(18))]]
            windowMechanic = sg.Window("Механіка", layoutMechanic)
            while True:
                eventMechanic, valuesMechanic = windowMechanic.read()
                if eventMechanic == "Абсолютно пружний удар":
                    APU()
        if eventModels3D == sg.WIN_CLOSED():
            break

mainWin()
