import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from logic import Cell 
from random import randint

board = [[Cell(x,y) for y in range(9)] for x in range(9)]
bombx = [randint(0,8) for x in range(11)]
bomby = [randint(0,8) for x in range(11)]
for i in range(11):
    board[bombx[i]][bomby[i]].make_bomb()

# Creating the main menu window
class MainMenu:
    def __init__(self):
        self.main_menu = tk.Tk()
        self.main_menu.title("Main Menu")
        self.main_menu.resizable(False, False)
        self.main_menu.iconbitmap("game.ico")

        # Components called here
        self.create_widgets()

        # Window size
        win_width = 500
        win_height = 350

        # Adjust window location to mid screen
        screen_width = self.main_menu.winfo_screenwidth()
        screen_height = self.main_menu.winfo_screenheight()

        x = int((screen_width / 2) - (win_width / 2))
        y = int((screen_height / 2) - (win_height / 2))

        self.main_menu.geometry(f"{win_width}x{win_height}+{x}+{y}")

    # Start button action
    def start_handler(self):
        self.main_menu.destroy()
        game = Game()
        game.game_window.focus_force()

    # Exit button action
    def exit_handler(self):
        self.main_menu.destroy()

    # Creating window components
    def create_widgets(self):
        global photo

        main_frame = tk.LabelFrame(self.main_menu)
        main_frame.pack(expand=True)

        image = Image.open('title.png')
        resized = image.resize((450, 70), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized)

        image_label = tk.Label(main_frame, image=photo)
        image_label.grid(column=0, row=0, padx=3, pady=5, columnspan=2)

        self.label = tk.Label(main_frame, font=('OpenSans', 18, "bold"), fg='green', text="WELCOME!")
        self.label.grid(column=0, row=1, columnspan=2, padx=18, pady=10)

        self.game = tk.Label(main_frame, font=('OpenSans', 10, "italic", "bold"), fg='purple',
                             text="All you have to do is play MINESWEEPER!\n"
                                  "The board is 9x9 and there are 10 mines.\n\n"
                                  "If you left click on a mine you will loose!\n"
                                  "if you manage to mark all 10 mines with right click you will win!\n"
                                  "After selecting all 10, click check button to see if you won.\n")

        self.game.grid(column=0, row=2, columnspan=2,  padx=18, pady=10)

        # Creating button style
        s = ttk.Style()
        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))

        self.start_game = ttk.Button(main_frame, style='my.TButton', text="Start Game",
                                     command=self.start_handler)
        self.start_game.grid(column=0, row=4, padx=10, pady=10, sticky=tk.E)

        self.exit_button = ttk.Button(main_frame, style='my.TButton', text="Exit Game",
                                      command=self.exit_handler)
        self.exit_button.grid(column=1, row=4, padx=10, pady=10, sticky=tk.W)

# Creating the game window
class Game:
    def __init__(self):
        self.game_window = tk.Tk()
        self.game_window.title("Game")
        self.game_window.resizable(False, False)
        self.game_window.iconbitmap("game.ico")

        # Components called here
        self.create_widgets()

        win_width = 200
        win_height = 280

        screen_width = self.game_window.winfo_screenwidth()
        screen_height = self.game_window.winfo_screenheight()

        x = int((screen_width / 2) - (win_width / 2))
        y = int((screen_height / 2) - (win_height / 2))

        self.game_window.geometry(f"{win_width}x{win_height}+{x}+{y}")

    def loose_handler(self):
        self.game_window.destroy()
        loose = GameOver()
        loose.game_over.focus_force()

    # Check button action
    def check_handler(self):
        won = True
        for i in range(10):
            if board[bombx[i]][bomby[i]].f == False:
                won = False
        if won:
            self.game_window.destroy()
            wellDone = WellDone()
            wellDone.wellDone_window.focus_force()

    def cal_env(self, board, L, i, j):
        if len(board) > i+1 and L[i+1][j].cget("text") == '    ':
            board[i+1][j].calculate_val(board) 
            if board[i+1][j].val != -1:
                L[i+1][j].config(text=" "+str(board[i+1][j].val)+" ")
            if board[i+1][j].val == 0:    
                self.cal_env(board, L, i+1, j)

        if i-1 >= 0 and L[i-1][j].cget("text") == '    ':
            board[i-1][j].calculate_val(board) 
            if board[i-1][j].val != -1:
                L[i-1][j].config(text=" "+str(board[i-1][j].val)+" ")
            if board[i-1][j].val == 0:
                self.cal_env(board, L, i-1, j)

        if len(board) > j+1 and L[i][j+1].cget("text") == '    ': 
            board[i][j+1].calculate_val(board)
            if board[i][j+1].val != -1:
                L[i][j+1].config(text=" "+str(board[i][j+1].val)+" ")
            if board[i][j+1].val== 0:
                self.cal_env(board, L, i, j+1)
                
        if j-1 >= 0 and L[i][j-1].cget("text") == '    ': 
            board[i][j-1].calculate_val(board)         
            if board[i][j-1].val != -1:
                L[i][j-1].config(text=" "+str(board[i][j-1].val)+" ")
            if board[i][j-1].val== 0:
                self.cal_env(board, L, i, j-1)

        if i-1 >= 0 and j-1 >= 0 and L[i-1][j-1].cget("text") == '    ':
            board[i-1][j-1].calculate_val(board)          
            if board[i-1][j-1].val != -1:
                L[i-1][j-1].config(text=" "+str(board[i-1][j-1].val)+" ")
            if board[i-1][j-1].val==0:
                self.cal_env(board, L, i-1, j-1)

        if j-1 >= 0 and len(board) > i+1 and L[i+1][j-1].cget("text") == '    ':
            board[i+1][j-1].calculate_val(board)       
            if board[i+1][j-1].val != -1:
                L[i+1][j-1].config(text=" "+str(board[i+1][j-1].val)+" ")        
            if board[i+1][j-1].val==0:
                self.cal_env(board, L, i+1, j-1)
                
        if len(board) > i+1 and len(board) > j+1 and L[i+1][j+1].cget("text") == '    ':
            board[i+1][j+1].calculate_val(board)          
            if board[i+1][j+1].val != -1:
                L[i+1][j+1].config(text=" "+str(board[i+1][j+1].val)+" ")                
            if board[i+1][j+1].val==0:
                self.cal_env(board, L, i+1, j+1)
                
        if i-1 >= 0 and len(board) > j+1 and L[i-1][j+1].cget("text") == '    ':
            board[i-1][j+1].calculate_val(board)
            if board[i-1][j+1].val != -1:
                L[i-1][j+1].config(text=" "+str(board[i-1][j+1].val)+" ")
            if board[i-1][j+1].val==0:
                self.cal_env(board, L, i-1, j+1)

    def on_click(self,i,j,event,L):
        if event.num == 1:
            if board[i][j].val == -1:
                # Loose condition
                # self.loose_handler()
                pass
            else:
                board[i][j].calculate_val(board)
                event.widget.config(text=" "+str(board[i][j].val)+" ")
                if board[i][j].val == 0:
                    self.cal_env(board, L, i, j)
    

        if event.num == 3:
            if board[i][j].f == False:
                color = "red"
                event.widget.config(bg=color)
                board[i][j].f = True
            else:
                color = "white"
                event.widget.config(bg=color)
                board[i][j].f = False


    # Creating window components
    def create_widgets(self):
        main_frame = tk.LabelFrame(self.game_window)
        main_frame.pack(expand=True)

        # Creating button style
        s = ttk.Style()
        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))
        L = [[tk.Label() for y in range(9)] for x in range(9)]
        
        for i,row in enumerate(board):
            for j,column in enumerate(row):
                
                L[i][j] = tk.Label(main_frame,text='    ',bg='white', borderwidth=3, relief="ridge")
                L[i][j].grid(row=i,column=j)
                L[i][j].bind('<Button-1>',lambda e,i=i,j=j: self.on_click(i,j,e,L))
                L[i][j].bind('<Button-3>',lambda e,i=i,j=j: self.on_click(i,j,e,L))

        self.check_button = ttk.Button(main_frame, style='my.TButton', text="Check",
                                     command=self.check_handler)
        self.check_button.grid(column=0, row=10, columnspan=10, padx=10, pady=10)

# Creating the game over window
class GameOver:
    def __init__(self):
        self.game_over = tk.Tk()
        self.game_over.title("Game Over!")
        self.game_over.resizable(False, False)
        self.game_over.iconbitmap("game.ico")

        # Components called here
        self.create_widgets()

        win_width = 500
        win_height = 350

        screen_width = self.game_over.winfo_screenwidth()
        screen_height = self.game_over.winfo_screenheight()

        x = int((screen_width / 2) - (win_width / 2))
        y = int((screen_height / 2) - (win_height / 2))

        self.game_over.geometry(f"{win_width}x{win_height}+{x}+{y}")

    # Menu button action
    def mainMenu_handler(self):
        self.game_over.destroy()
        mainMenu = MainMenu()
        mainMenu.main_menu.focus_force()

    # Exit button action
    def exit_handler(self):
        self.game_over.destroy()

    # Creating window components
    def create_widgets(self):
        global photo

        main_frame = tk.LabelFrame(self.game_over)
        main_frame.pack(expand=True)

        image = Image.open('loose.png')
        resized = image.resize((450, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized)

        image_label = tk.Label(main_frame, image=photo)
        image_label.grid(column=0, row=0, padx=3, pady=5, columnspan=2)

        self.loose_label = tk.Label(main_frame, font=('Times', 20, "bold"), fg='purple', text="GAME OVER!")
        self.loose_label.grid(column=0, row=1, padx=18, columnspan=2, pady=10)

        s = ttk.Style()
        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))

        self.main_menu_button = ttk.Button(main_frame, style='my.TButton', text="Main Menu",
                                           command=self.mainMenu_handler)
        self.main_menu_button.grid(column=0, row=2, padx=10, pady=10, sticky=tk.E)

        self.exit_button = ttk.Button(main_frame, style='my.TButton', text="Exit Game",
                                      command=self.exit_handler)
        self.exit_button.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)


# Creating the well done window
class WellDone:
    def __init__(self):
        self.wellDone_window = tk.Tk()
        self.wellDone_window.title("Well Done!")
        self.wellDone_window.resizable(False, False)
        self.wellDone_window.iconbitmap("game.ico")

        # Components called here
        self.create_widgets()

        win_width = 500
        win_height = 350

        screen_width = self.wellDone_window.winfo_screenwidth()
        screen_height = self.wellDone_window.winfo_screenheight()

        x = int((screen_width / 2) - (win_width / 2))
        y = int((screen_height / 2) - (win_height / 2))

        self.wellDone_window.geometry(f"{win_width}x{win_height}+{x}+{y}")

    # Menu button action
    def mainMenu_handler(self):
        self.wellDone_window.destroy()
        mainMenu = MainMenu()
        mainMenu.main_menu.focus_force()

    # Exit button action
    def exit_handler(self):
        self.wellDone_window.destroy()

    # Creating window components
    def create_widgets(self):
        global photo

        main_frame = tk.LabelFrame(self.wellDone_window)
        main_frame.pack(expand=True)

        image = Image.open('win.png')
        resized = image.resize((450, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized)

        image_label = tk.Label(main_frame, image=photo)
        image_label.grid(column=0, row=0, padx=3, pady=5, columnspan=2)

        self.win_label = tk.Label(main_frame, font=('Times', 20, "bold"), fg='orange', text="WELL DONE!")
        self.win_label.grid(column=0, row=1, padx=18, columnspan=2, pady=10)

        s = ttk.Style()
        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))

        self.main_menu_button = ttk.Button(main_frame, style='my.TButton', text="Main Menu",
                                           command=self.mainMenu_handler)
        self.main_menu_button.grid(column=0, row=2, padx=10, pady=10, sticky=tk.E)

        self.exit_button = ttk.Button(main_frame, style='my.TButton', text="Exit Game",
                                      command=self.exit_handler)
        self.exit_button.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)


# Starting the GUI app
app = MainMenu()
app.main_menu.mainloop()