from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from functools import partial

from lights_out_q_solver import LightsOutQSolver

class GUI(App):

    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        self.title = "Quantum Lights Out!"
        self.lights = [0 for i in range(9)]

    def build(self):
        # Main layout
        main_layout = BoxLayout(orientation='horizontal', spacing=10, padding=10)

        # Left section - 3x3 grid of buttons
        lights_out_grid = GridLayout(cols=3, spacing=2)
        self.lights_out_grid_buttons = []
        left_layout = BoxLayout(orientation='vertical', spacing=5)

        for i in range(9):
                button = Button(on_press=partial(self.on_button_press, i), background_color=(0.5,0.5,0.5,1))
                self.lights_out_grid_buttons.append(button)
                lights_out_grid.add_widget(button)

        label = Label(text="Solve Lights Out With Grevor!", size_hint_y=None, height=100)
        left_layout.add_widget(label)
        left_layout.add_widget(lights_out_grid)

        # Right section - two buttons
        right_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_x=None, width=200)
        reset_btn = Button(text='Reset', on_press=self.on_reset,size_hint_y=None, height=50)
        solve_btn = Button(text='Solve', on_press=self.solve, size_hint_y=None, height=50, background_color=(0.8, 0.5, 0.5, 1))
        label = Label(text="Solution", size_hint_y=None, height=50)
        
        solution_grid = GridLayout(cols=3)
        self.solution_grid_btns = []

        for i in range(9):
                button = Button(size_hint_y=None, height=50, background_color=(0.5,0.5,0.5,1))
                self.solution_grid_btns.append(button)
                solution_grid.add_widget(button)

        right_layout.add_widget(reset_btn)
        right_layout.add_widget(solve_btn)
        right_layout.add_widget(label)
        right_layout.add_widget(solution_grid)

        # Add left and right sections to the main layout
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        return main_layout

    def on_reset(self, instance):
        self.lights = [0 for i in range(9)]

        for j in range(9):
            self.lights_out_grid_buttons[j].background_color = (0.5, 0.5, 0.5, 1.0)
            self.solution_grid_btns[j].background_color = (0.5, 0.5, 0.5, 1.0)
    
    def on_button_press(self,i, instance):
        if self.lights[i]:
            instance.background_color = (0.5, 0.5, 0.5, 1.0)
            self.lights[i] = 0
        else:
            instance.background_color = (0.9,0.9,0,1)
            self.lights[i] = 1
        


    def solve(self, instance):
        solver = LightsOutQSolver(3)
        solution = solver.run_algorithm(self.lights)
        print(solution)
        for i in range(len(solution)):
            if solution[i]:
                self.solution_grid_btns[i].background_color = (1, 0, 0, 1.0)
            else:
                self.solution_grid_btns[i].background_color = (0.5, 0.5, 0.5, 1.0)