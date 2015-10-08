#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as tk
"""
@author: William Gillespie
This is a calculator app that uses 7-segment displays to show the digits
"""

class Digit(object):
    def __init__(self, digit_as_string):
        """
        This init method takes a digit as a string and sets the segments to on or off
        so that the number can be displayed as a 7-segment display.  This represents the model
        of a digit in the MVC paradigm in which the digit is represented as 7 on/off switches.
        This class is used for the display of a digit and holds the on/off values for the segments
        that will be used to display the digit.
        :param digit_as_string: digit used to set the 7 segment on/off switches; type:string
        """
        self.top = True
        self.mid = True
        self.bottom = True
        self.top_left = True
        self.top_right = True
        self.bottom_left = True
        self.bottom_right = True
        if digit_as_string == '0':
            self.mid = False
        elif digit_as_string == '1':
            self.top = False
            self.mid = False
            self.bottom = False
            self.top_left = False
            self.bottom_left = False
        elif digit_as_string == '2':
            self.top_left = False
            self.bottom_right = False
        elif digit_as_string == '3':
            self.top_left = False
            self.bottom_left = False
        elif digit_as_string == '4':
            self.top = False
            self.bottom = False
            self.bottom_left = False
        elif digit_as_string == '5':
            self.top_right = False
            self.bottom_left = False
        elif digit_as_string == '6':
            self.top_right = False
        elif digit_as_string == '7':
            self.mid = False
            self.bottom = False
            self.top_left = False
            self.bottom_left = False
        elif digit_as_string == '8':
            pass
        elif digit_as_string == '9':
            self.bottom = False
            self.bottom_left = False
        elif digit_as_string == '-':
            self.top = False
            self.bottom = False
            self.top_left = False
            self.top_right = False
            self.bottom_left = False
            self.bottom_right = False
        elif digit_as_string == 'E':
            self.top_right = False
            self.bottom_right = False
# end of class Digit


class Calculator(tk.Frame):
    def __init__(self, parent):
        """
        This method initializes the Calculator Frame.  It sets and declares global variables
        used in the program and calls init_ui().
        :param parent: root frame of the application.  Type: Frame
        """
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.input1 = []  # list of strings that represent the string of digits that the user enters
        self.input2 = []  # same kind of list but for the second input
        self.result = []  # same kind of list but for the result of a calculation
        self.operator = None  # the current operator that the user clicked, type: string, e.g. '+'
        self.resultHasBeenCalculated = False  # type: boolean

        # lists for displaying the digits
        self.input1_digits = []  # list of Digit objects that hold the hold on/off values for display
        self.input2_digits = []  # list of Digits for second input to be displayed
        self.result_digits = []  # list of Digits for the result to be displayed

        self.topFrame = None  # top Frame that holds number inputs
        self.midFrame = None  # middle Frame that holds number inputs
        self.bottomFrame = None  # bottom Frame that holds number inputs

        self.topDisplays = []  # list of canvas objects on which the digits will be drawn
        self.midDisplays = []  # same kind of list but placed in midFrame
        self.bottomDisplays = []  # same kind of list but placed in bottomFrame

        self.init_ui()  # initializes the user interface

    def init_ui(self):
        """
        initializes the user interface by adding all of the buttons and canvases to their
        respective frames.
        """
        self.parent.title("Calculator")

        # sets up the row and column grids for the buttons
        for colNumber in range(0, 3, 1):
            self.columnconfigure(colNumber, pad=3)

        for rowNumber in range(0, 4, 1):
            self.rowconfigure(0, pad=3)

        button_list = [
            'C', '+/-', '%', '÷',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', 'Enter'
        ]

        # creates the and adds all of the buttons to the display
        r = 3
        c = 0
        for label in button_list:
            cmd = lambda key=label: self.click(key)
            button = tk.Button(self, text=label, width=5, font=("Helvetica", 48), command=cmd)
            if label == '0' or label == 'Enter':
                button.grid(row=r, column=c, columnspan=2)
                c += 2
            else:
                button.grid(row=r, column=c)
                c += 1
            if c > 3:
                c = 0
                r += 1
        self.pack()

        # start of code for the digit display
        # this code creates the Frames for the canvases and puts the canvases in the Frames

        self.topFrame = tk.Frame(self)
        self.update()
        window_width = self.winfo_width()
        display_width = window_width / 12
        display_height = self.winfo_height() / 5

        self.topFrame.grid(row=0, column=0, rowspan=1, columnspan=4, sticky=tk.W + tk.E + tk.N + tk.S)
        for i in range(1, 12, 1):
            display = tk.Canvas(self.topFrame, width=display_width, height=display_height, background='lightgreen')
            display.pack(side=tk.LEFT, fill=tk.X)
            self.topDisplays.append(display)

        self.midFrame = tk.Frame(self)
        self.midFrame.grid(row=1, column=0, rowspan=1, columnspan=4, sticky=tk.W + tk.E + tk.N + tk.S)
        for i in range(1, 12, 1):
            display = tk.Canvas(self.midFrame, width=display_width, height=display_height, background='lightblue')
            display.pack(side=tk.LEFT, fill=tk.X)
            self.midDisplays.append(display)

        self.bottomFrame = tk.Frame(self)
        self.bottomFrame.grid(row=2, column=0, rowspan=1, columnspan=4, sticky=tk.W + tk.E + tk.N + tk.S)
        for i in range(1, 12, 1):
            display = tk.Canvas(self.bottomFrame, width=display_width, height=display_height, background='#DEABEE')
            display.pack(side=tk.LEFT, fill=tk.X)
            self.bottomDisplays.append(display)
    # end of init_ui() method

    def click(self, key):
        """
        This method is executed when the user clicks a button in the UI.  It updates the
        UI depending on whether the user clicked a digit, operator, or the Clear button.
        :param key: the button the user clicked.  It could be a number, operator, or C.
                    key's type: string.  e.g. '7', '*', or 'C'
        """
        if key.isdigit():  # if the button clicked was a digit
            if self.resultHasBeenCalculated:  # if the result has been calculated and we click
                self.input1 = []              # a button, we reset everything and clear canvases
                self.input2 = []
                self.result = []
                self.input1_digits = []
                self.input2_digits = []
                self.result_digits = []
                self.clearCanvasRow(self.topDisplays)
                self.clearCanvasRow(self.midDisplays)
                self.clearCanvasRow(self.bottomDisplays)

                # updates Frames so that canvases erase their contents
                self.topFrame.update()
                self.midFrame.update()
                self.bottomFrame.update()

                self.resultHasBeenCalculated = False  # set to true for the new calculation
            if self.operator is None:  # if it is none, we are dealing w/ first input
                number = self.input1
                number_list = self.input1_digits
            else:  # otherwise we are dealing w/ second input
                number = self.input2
                number_list = self.input2_digits
            # end of code to determine which calculator state we are in (i.e. first input,
                # second input, or input of an operator)
            can_append = False
            if len(number) and number[0] == '-':
                if len(number) <= 10:
                    can_append = True
            elif len(number) <= 9:  # if the number is <= 9 digits, its still short enough to add to
                can_append = True

            if can_append:
                number.append(key)  # appends the key (i.e. the number) to the list of strings
                                    # that represent the input number
                number_list.append(Digit(key))  # appends the digit (my Digit class) to the list
                                                # of digits that represent the number input
                self.drawDigits(number_list, self.bottomDisplays)  # draws digits using the list of Digits
        elif key == '+' or key == '-' or key == '*' or key == '%' or key == '÷':  # if key is an operator
            if self.result == ['E']:  # if the result E (overflow), we cannot do a calculation
                return          # so we just return and do nothing
            if self.operator:
                return
            elif len(self.input1) > 0 and len(self.input2) > 0:  # if both inputs are present,
                self.operator = key                              # that means we are using the
                self.input1 = self.result                        # previous result as input1
                self.input1_digits = self.result_digits              # for the new calculation.

                # in the following code, we clear the canvases and redraw the previous
                # result in the midDisplays so we can use the previous result as the first input
                # in the new calculation
                self.input2 = []
                self.input2_digits = []
                self.result = []
                self.result_digits = []
                self.clearCanvasRow(self.topDisplays)
                self.clearCanvasRow(self.midDisplays)
                self.clearCanvasRow(self.bottomDisplays)
                self.drawDigits(self.input1_digits, self.midDisplays)

                self.topFrame.update()
                self.midFrame.update()
                self.bottomFrame.update()

                self.resultHasBeenCalculated = False  # new calculation has begun, so we set to false
            elif len(self.input1) > 0:  # if there is only one input, the user is starting a
                                        # fresh calculation and is not using the previous
                                        # result as the input to a new calculation
                self.operator = key
                self.drawDigits(self.input1_digits, self.midDisplays)  # push input1 to mid display
                self.clearCanvasRow(self.bottomDisplays)  # clear bottom display to make way for input2

                self.midFrame.update()  # update frames to force a drawing and erasing
                self.bottomFrame.update()

        elif key == 'Enter':  # if user wants the initiate the calculation
            if self.result == ['E']:  # if there was a previous error, we cannot calculate anything
                return                # so we just do nothing
            if self.operator and self.input1 and self.input2:  # if there is an operator, we can calculate!!!
                self.calculate(self.input1, self.input2, self.operator)  # places result of calculation in self.result
                self.drawDigits(self.input1_digits, self.topDisplays)  # draw input1 on top row
                self.drawDigits(self.input2_digits, self.midDisplays)  # draw input2 on mid row
                self.drawDigits(self.result_digits, self.bottomDisplays)  # draw result on bottom row

                # update frames to force a draw and erase of the new/old digits
                self.topFrame.update()
                self.midFrame.update()
                self.bottomFrame.update()

                self.operator = None  # once there is a calculation, operator is net to None
                self.resultHasBeenCalculated = True  # sets it to true for a new calculation
        elif key == '+/-':
            # if these conditions are true we cannot apply the sign toggling
            if len(self.input1) == 0:  # if there is no input 1
                return
            elif len(self.input2) == 0 and self.operator is not None:  # if no input 2
                return
            elif self.result and self.result[-1] == 'E':  # if prev calculation resulted in Error
                return

            def toggle_minus(number_as_list, number_as_list_of_digits):
                """

                :param number_as_list: represents list of the numbers, Type: list of strings
                :param number_as_list_of_digits: list of digits (7 segment digits), Type: list of Digit class
                :return:
                """
                if number_as_list[0] == '-':  # there is a minus
                    number_as_list.remove(number_as_list[0])
                    number_as_list_of_digits.remove(number_as_list_of_digits[0])
                    index_at_which_to_erase_canvas = len(self.bottomDisplays) - len(number_as_list) - 1
                    canvas_to_delete = self.bottomDisplays[index_at_which_to_erase_canvas]
                    canvas_to_delete.delete(tk.ALL)
                    canvas_to_delete.update()
                else:  # there is no minus
                    number_as_list.insert(0, '-')
                    minus_digit = Digit('-')
                    number_as_list_of_digits.insert(0, minus_digit)
                    index_at_which_to_insert_minus_sign = len(self.bottomDisplays) - len(number_as_list)
                    canvas_to_draw_on = self.bottomDisplays[index_at_which_to_insert_minus_sign]
                    self.drawDigitOnCanvas(minus_digit, canvas_to_draw_on)
                    canvas_to_draw_on.update()
            # toggles minus depending on which canvas it must select
            if len(self.input1_digits) and self.operator is None and self.resultHasBeenCalculated is False:  # toggling bottom row
                toggle_minus(self.input1, self.input1_digits)
            elif len(self.input1) and len(self.input2) and self.resultHasBeenCalculated is False:
                toggle_minus(self.input2, self.input2_digits)
            else:  # toggle result's sign
                toggle_minus(self.result, self.result_digits)
        elif key == 'C':  # if the user wants to clear the calculator,
            self.nukeCalculator()  # we reset the calculator and clear all the canvases
            self.topFrame.update()
            self.midFrame.update()
            self.bottomFrame.update()

    def calculate(self, input1, input2, operator):
        """

        :param input1: Type: list of strings (strings are numeric)
        :param input2: Type: list of strings (strings are numeric)
        :param operator: the operators +, -, ÷, *, and %
        :return:
        """
        # turn into numbers for calculation
        in1_string = "".join(input1)
        in1 = int(in1_string)
        in2_string = "".join(input2)
        in2 = int(in2_string)

        if operator == '+':
            temp_result = in1 + in2
        elif operator == '-':
            temp_result = in1 - in2
        elif operator == '*':
            temp_result = in1 * in2
        elif operator == '÷':
            if self.input2[-1] == '0':
                self.result = ['E']
                self.result_digits.append(Digit('E'))
                return
            temp_result = in1 / in2
            temp_result = int(temp_result)
        elif operator == '%':
            if self.input2[-1] == '0':
                self.result = ['E']
                self.result_digits.append(Digit('E'))
                return
            temp_result = in1 % in2
            # end of code to determine which arithmetic operation it was
        temp_result = str(temp_result)
        temp_result = list(temp_result)
        if len(temp_result) > 10:  # if the result is too big
            self.result = ['E']
            self.result_digits.append(Digit('E'))
        else:
            self.result = temp_result
            for i in temp_result:
                self.result_digits.append(Digit(i))

    def drawDigits(self, number_list, canvas_row):
        """
        draws the digits on a row of canvases
        :param number_list: Type: list of numeric strings
        :param canvas_row: Type: list of canvases
        """
        for display in canvas_row:
            display.delete(tk.ALL)
        digits_reversed = number_list[::-1]  # creates a reverse of the list (I know its witchcraft, right?)
        displays = reversed(canvas_row)
        for digit in digits_reversed:
            self.drawDigitOnCanvas(digit, next(displays))

    def drawDigitOnCanvas(self, digit, canvas):
        """
        Draws a single digit on a single canvas according to the on/off switches
        /boolean variables in the Digit object
        :param digit: Type: Digit
        :param canvas: Type: canvas
        """
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        mid = int(height / 2)
        if digit.top:
            y = 0 + 8
            canvas.create_line(0, y, width, y, fill="black", width=10)
        if digit.mid:
            y = int(height / 2)
            canvas.create_line(0, y, width, y, fill="black", width=10)
        if digit.bottom:
            y = height - 8
            canvas.create_line(0, y, width, y, fill="black", width=10)
        if digit.top_left:
            x = 8
            y1 = 0
            y2 = mid
            canvas.create_line(x, y1, x, y2, fill="black", width=10)
        if digit.top_right:
            x = width - 8
            y1 = 0
            y2 = mid
            canvas.create_line(x, y1, x, y2, fill="black", width=10)
        if digit.bottom_left:
            x = 8
            y1 = mid
            y2 = height
            canvas.create_line(x, y1, x, y2, fill="black", width=10)
        if digit.bottom_right:
            x = width - 8
            y1 = mid
            y2 = height
            canvas.create_line(x, y1, x, y2, fill="black", width=10)
        canvas.update()

    def clearCanvasRow(self, canvas_row):
        """
        Erases all of the Digits on a canvas row; update() must be called sometime afterward
        :param canvas_row:
        """
        for display in canvas_row:
            display.delete(tk.ALL)

    def nukeCalculator(self):
        """
        resets the calculator app
        """
        self.input1 = []
        self.input1_digits = []
        self.input2 = []
        self.input2_digits = []
        self.result = []
        self.result_digits = []
        self.clearCanvasRow(self.topDisplays)
        self.clearCanvasRow(self.midDisplays)
        self.clearCanvasRow(self.bottomDisplays)
        self.resultHasBeenCalculated = False


def main():
    # gets the app up and running
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()


if __name__ == '__main__':
    main()