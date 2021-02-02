import tkinter as tk
import matrix as m
from string import ascii_uppercase
from tkinter import messagebox as mb


class MatrixViewer:

    def __init__(self, n_mat=2):
        self.n_mat = n_mat
        self.matrices = [m.Matrix([[0, 0, 0], [0, 0, 0]]) for i in range(self.n_mat)]  # list holding the matrices
        self.matrix_res = None  # results matrix

        # define main window
        self.win = tk.Tk()
        self.win.title("Matrix Operations Visualizer")
        self.win.resizable(True, True)

        # define frames
        self.frame_top = tk.Frame(self.win)
        self.frames_shapes = [tk.LabelFrame(self.win, text="Shape " + ascii_uppercase[i], labelanchor="n")
                              for i in range(self.n_mat)]  # list of frames holding shape setters for each matrix
        self.frames_mat = [tk.LabelFrame(self.win, text="Matrix " + ascii_uppercase[i], labelanchor="n")
                           for i in range(self.n_mat)]  # list of frames holding input field grid for each matrix
        self.frame_res = tk.LabelFrame(self.win, text="Result", labelanchor="n")  # frame holding display grid for results matrix
        self.frame_buttons = tk.Frame(self.win)  # frame holding action buttons for each matrix operation

        # pack frames
        self.frame_top.pack(side=tk.TOP)
        for i in range(self.n_mat):
            self.frames_shapes[i].pack(side=tk.LEFT)
        self.frame_buttons.pack(side=tk.BOTTOM)
        for i in range(self.n_mat):
            self.frames_mat[i].pack(side=tk.LEFT)
        self.frame_res.pack(side=tk.LEFT)

        # fill top frame
        instructions_txt = "Supported Matrix operations:\n" \
                           "-  addition (+)\n" \
                           "- multiplication (*)\n" \
                           "- elementwise multiplication, or Hadamard product (@)\n" \
                           "- scalar multiplication (A*n)\n" \
                           "- transposition (~)\n\n" \
                           "Instructions:\n" \
                           "Set matrix shapes (left-hand) and select operation (bottom).\n" \
                           "Operations incompatible with selected shapes will be deactivated.\n" \
                           "For scalar multiplication, set one of the two matrices to shape 1x1.\n"
        tk.Label(self.frame_top, text=instructions_txt, justify=tk.LEFT).pack(anchor="w")

        # create action buttons in bottom frame; each button bound to method for given operation
        self.but_add = tk.Button(self.frame_buttons, text="A+B", command=self.addition)  # matrix addition
        self.but_mult = tk.Button(self.frame_buttons, text="A*B", command=self.mult)  # matrix multiplication
        self.but_mult_had = tk.Button(self.frame_buttons, text="A@B", command=self.mult_had)  # hadamard multiplication
        self.but_mult_scal = tk.Button(self.frame_buttons, text="A*n", command=self.mult_scal)  # scalar multiplication
        self.but_transp = tk.Button(self.frame_buttons, text="~A", command=self.transp)  # matrix transposition

        # pack action buttons in bottom frame
        self.but_add.pack(side=tk.LEFT, padx=5, pady=5)
        self.but_mult.pack(side=tk.LEFT, padx=5, pady=5)
        self.but_mult_had.pack(side=tk.LEFT, padx=5, pady=5)
        self.but_mult_scal.pack(side=tk.LEFT, padx=5, pady=5)
        self.but_transp.pack(side=tk.LEFT, padx=5, pady=5)

        # define headers for spin boxes for rows for each matrix
        self.spin_rows_heads = [tk.Label(self.frames_shapes[i], text="rows").grid(row=0, column=i * 2)
                                for i in range(self.n_mat)]
        # define headers for spin boxes for cols for each matrix
        self.spin_cols_heads = [tk.Label(self.frames_shapes[i], text="cols").grid(row=0, column=i * 2 + 1)
                                for i in range(self.n_mat)]

        # define text labels of spin boxes for rows for each matrix
        self.spin_rows_txt = [tk.IntVar() for i in range(self.n_mat)]
        # define text labels of spin boxes for cols for each matrix
        self.spin_cols_txt = [tk.IntVar() for i in range(self.n_mat)]

        # assign shapes of pre-defined matrices to spin box text labels for each matrix
        for i in range(self.n_mat):
            self.spin_rows_txt[i].set(self.matrices[i].n_rows)
            self.spin_cols_txt[i].set(self.matrices[i].n_cols)

            # define row spin boxes for each matrix, bind them to method resize_matrix_grid(), place spin boxes in grid
            tk.Spinbox(self.frames_shapes[i], from_=1, to=20, width=3, state="readonly", textvariable=self.spin_rows_txt[i],
                       command=lambda i=i:self.resize_matrix_grid(id_mat=i, new_size=self.spin_rows_txt[i].get(), what="rows")).grid(row=1, column=2*i)
            # lambda i=i: needed to pass iteration variable i as argument to resize_matrix_grid(); without this callback,
            # only the last iteration value of i will be passed to lambda function

            # define col spin boxes for each matrix, bind them to method resize_matrix_grid(), place spin boxes in grid
            tk.Spinbox(self.frames_shapes[i], from_=1, to=20, width=3, state="readonly", textvariable=self.spin_cols_txt[i],
                       command=lambda i=i: self.resize_matrix_grid(id_mat=i, new_size=self.spin_cols_txt[i].get(), what="cols")).grid(row=1, column=2*i+1)

            # in each matrix frame, create empty cells according to size of pre-defined matrices
            self.create_cells(frame=self.frames_mat[i], n_rows=self.matrices[i].n_rows, n_cols=self.matrices[i].n_cols)
        self.check_button_states()
        self.win.mainloop()

    # definition of required functions
    def create_cells(self, frame, n_rows, n_cols, items=None, head=""):
        '''
        Populates selected frame with entry cells according to shape of specified matrix.
        :param frame (tk.Frame or tk.LabelFrame): frame in which entry cells are to be placed.
        :param n_rows: number of rows
        :param n_cols: number of columns
        :param items: Optional: nested list of matrix items. Used for display of resulting Matrix object. Default is None
        :param head: Optional: string indicating subheading of frame. Default is ""
        :return: None
        '''
        # get current widgets in frame and destroy them
        for widget in frame.winfo_children():
            widget.destroy()
        # define and place optional heading within frame
        heading = tk.Label(frame, text=head)
        heading.grid(row=0, columnspan=n_cols, sticky="n")

        # Create & place entry cells according to matrix shape. If items are passed, cells are read-only and non-empty.
        for r in range(n_rows):
            for c in range(n_cols):
                if items:
                    cell_value = tk.StringVar()
                    cell_value.set(items[r][c])
                    state = "readonly"
                    bg = "grey"
                else:
                    cell_value = None
                    state = "normal"
                    bg = "white"
                cell = tk.Entry(frame, width=5, textvariable=cell_value, state=state, bg=bg)
                cell.grid(row=r+1, column=c)

    def resize_matrix_grid(self, id_mat, new_size, what="rows"):
        '''
        Sets shape of Matrix object and changes shape of corresponding entry grid. Method bound to spin boxes for number of rows
        and columns in given matrix frame.
        :param id_mat: ID of matrix frame to be resized
        :param new_size: New number of columns/rows, to which matrix frame will be resized.
        :param what: Specifies whether :param new_size refers to 'rows' or 'cols'.
        :return: Nothing. Calls method crate_cells() and check_button_states().
        '''
        new_size = int(new_size)
        # set selected dimension of given Matrix object to new value
        if what == "rows":
            self.matrices[id_mat].n_rows = new_size
        elif what == "cols":
            self.matrices[id_mat].n_cols = new_size
        # place empty matrix of given shape in .matrix attribute of given Matrix object
        self.matrices[id_mat].matrix = self.matrices[id_mat].initialise_empty(self.matrices[id_mat].n_rows, self.matrices[id_mat].n_cols)
        # set shape of given Matrix object to new value
        self.matrices[id_mat].shape = (self.matrices[id_mat].n_rows, self.matrices[id_mat].n_cols)
        # for given matrix, create entry fields according to selected shape
        self.create_cells(frame=self.frames_mat[id_mat], n_rows=self.matrices[id_mat].n_rows, n_cols=self.matrices[id_mat].n_cols)
        self.check_button_states() # check button states to prohibit operations incompatible with given matrix shapes

    def check_button_states(self):
        '''
        Helper function enabling/disabling action buttons, depending of shapes of Matrices. Disabling
        action buttons prevents invalid matrix operations (e.g. addition of two matrices of different shapes).
        :return: None. Simply calls checking function for each operation operation button.
        '''
        self.check_button_addition_had()
        self.check_button_mul()
        self.check_button_mul_scal()

    def check_button_addition_had(self):
        '''
        Disables action button for matrix addition and hadamard multiplication if shapes of matrices are not equal.
        :return: None. Disables action button if invalid state is detected.
        '''
        if self.matrices[0].shape == self.matrices[1].shape:
            self.but_add['state'] = tk.NORMAL
            self.but_mult_had['state'] = tk.NORMAL
        else:
            self.but_add['state'] = tk.DISABLED
            self.but_mult_had['state'] = tk.DISABLED

    def check_button_mul(self):
        '''
        Disables action button for matrix multiplication if number of columns of Matrix X is not equal to number of rows
        of Matrix B.
        :return: None. Disables action button if invalid state is detected.
        '''
        if self.matrices[0].n_cols == self.matrices[1].n_rows:
            self.but_mult['state'] = tk.NORMAL
        else:
            self.but_mult['state'] = tk.DISABLED

    def check_button_mul_scal(self):
        '''
        Disables action button for scalar multiplication if none/both of the matrices are scalars (1x1 matrices).
        :return: None. Disables action button if invalid state is detected.
        '''
        shapes = [self.matrices[i].shape for i in range(self.n_mat)]
        if (any(shape == (1,1) for shape in shapes) and
            any(shape != (1,1) for shape in shapes)):
            self.but_mult_scal['state'] = tk.NORMAL
        else:
            self.but_mult_scal['state'] = tk.DISABLED

    def addition(self):
        '''
        Performs matrix addition, writes result to results matrix, and creates output cells in results frame.
        :return: None.
        '''
        self.grid2matrix()
        self.matrix_res = self.matrices[0] + self.matrices[1]
        self.create_cells(self.frame_res, self.matrix_res.n_rows, self.matrix_res.n_cols, self.matrix_res.items, "A+B")

    def mult(self):
        '''
        Performs matrix multiplication, writes result to results matrix, and creates output cells in results frame.
        :return: None.
        '''
        self.grid2matrix()
        self.matrix_res = self.matrices[0] * self.matrices[1]
        self.create_cells(self.frame_res, self.matrix_res.n_rows, self.matrix_res.n_cols, self.matrix_res.items, "A*B")

    def mult_had(self):
        '''
        Performs element-wise matrix multiplication (Hadamard product), writes result to results matrix, and creates
        output cells in results frame.
        :return: None.
        '''
        self.grid2matrix()
        self.matrix_res = self.matrices[0] @ self.matrices[1]
        self.create_cells(self.frame_res, self.matrix_res.n_rows, self.matrix_res.n_cols, self.matrix_res.items, "A@B")

    def mult_scal(self):
        '''
        Performs scalar multiplication, writes result to results matrix, and creates output cells in results frame.
        :return: None.
        '''
        self.grid2matrix()
        a = self.matrices[0].items[0][0] if self.matrices[0].shape == (1,1) else self.matrices[0]
        b = self.matrices[1].items[0][0] if self.matrices[1].shape == (1,1) else self.matrices[1]
        self.matrix_res = a * b
        self.create_cells(self.frame_res, self.matrix_res.n_rows, self.matrix_res.n_cols, self.matrix_res.items, "A@B")

    def transp(self):
        '''
        Performs matrix transposition, writes result to results matrix, and creates output cells in results frame.
        :return: None.
        '''
        self.grid2matrix(mat_ids = [0])
        self.matrix_res = ~self.matrices[0]
        self.create_cells(self.frame_res, self.matrix_res.n_rows, self.matrix_res.n_cols, self.matrix_res.items, "~A")

    def cells2list(self, frame):
        '''
        Converts inputs from visual matrix (= grid of entry cells) into a nested list of matrix items.
        :param frame: Frame containing the entry cells to be converted into nested list.
        :return: Nested list: each list item corresponds to a matrix row
        '''
        # get shape of entry grid from frame attributes
        n_rows = frame.grid_size()[1] - 1  # -1 because first row of frame holds heading
        n_cols = frame.grid_size()[0]
        # get all entry widgets of given frame
        input_cells = frame.winfo_children()[1:]  # ignore first frame child, which holds the heading
        values = [int(cell.get()) for cell in input_cells]
        values_nested = [values[i:i+n_cols] for i in range(0, n_rows * n_cols, n_cols)]
        return values_nested

    def grid2matrix(self, mat_ids=range(2)):
        '''
        Writes input items in visual matrix (= grid of entry cells) to Matrix objects. Writing operation to Matrix object
        uses overloaded method __setitem__ of Matrix class.
        :param mat_ids: List of IDs indicating the matrices to be processed. Defaults to [0,1]
        :return: None
        '''
        frames = [self.frames_mat[i] for i in mat_ids]  # get selected frames using the supplied matrix IDs
        try:
            input_values = [self.cells2list(frame) for frame in frames]  # retrieve values inputted by user into cells
            for i in mat_ids:
                for r in range(self.matrices[i].n_rows):
                    for c in range(self.matrices[i].n_cols):
                        self.matrices[i][r, c] = input_values[i][r][c]  # update matrix items of given Matrix object
        except ValueError:  # raise error in dialog box if input cells of given matrix contain empty fields
            mb.showinfo("Empty Matrix Fields Error", "Computation impossible on Matrices with empty fields.")
