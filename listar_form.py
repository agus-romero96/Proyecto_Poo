import wx
import wx.grid
from db import obtener_registros

class ListarClientesPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        
        # Título
        titulo = wx.StaticText(self, label="Listado de Clientes")
        titulo.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(titulo, 0, wx.ALL | wx.CENTER, 20)
        
        # Barra de búsqueda
        search_panel = wx.Panel(self)
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        search_label = wx.StaticText(search_panel, label="Buscar:")
        self.search_ctrl = wx.SearchCtrl(search_panel, size=(200, -1))
        self.search_ctrl.SetHint("Buscar por nombre o email")
        self.search_ctrl.SetName("Campo de búsqueda")
        
        search_sizer.Add(search_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        search_sizer.Add(self.search_ctrl, 1, wx.EXPAND)
        search_panel.SetSizer(search_sizer)
        
        main_sizer.Add(search_panel, 0, wx.ALL | wx.EXPAND, 10)
        
        # Grid para mostrar los datos
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, 4)
        
        # Configurar columnas
        columnas = ["Nombre", "Apellido", "Email", "Teléfono"]
        for idx, col in enumerate(columnas):
            self.grid.SetColLabelValue(idx, col)
            self.grid.SetColSize(idx, 200)
        
        self.grid.SetRowLabelSize(40)
        self.grid.EnableEditing(False)
        
        # Estilos del grid
        self.grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        self.grid.SetLabelFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        main_sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 10)
        
        # Botones de acción
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_actualizar = wx.Button(self, label="&Actualizar Lista")
        self.btn_exportar = wx.Button(self, label="&Exportar a CSV")
        
        button_sizer.Add(self.btn_actualizar, 0, wx.ALL, 5)
        button_sizer.Add(self.btn_exportar, 0, wx.ALL, 5)
        
        main_sizer.Add(button_sizer, 0, wx.CENTER | wx.ALL, 10)
        
        # Vincular eventos
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.OnActualizar)
        self.btn_exportar.Bind(wx.EVT_BUTTON, self.OnExportar)
        self.search_ctrl.Bind(wx.EVT_TEXT, self.OnBuscar)
        
        # Configurar accesibilidad
        self.SetAcceleratorTable(wx.AcceleratorTable([
            (wx.ACCEL_ALT, ord('A'), self.btn_actualizar.GetId()),
            (wx.ACCEL_ALT, ord('E'), self.btn_exportar.GetId()),
        ]))
        
        self.SetSizer(main_sizer)
        self.CargarDatos()
    
    def CargarDatos(self):
        registros = obtener_registros()
        self.grid.ClearGrid()
        
        # Ajustar el número de filas
        actual_rows = self.grid.GetNumberRows()
        if actual_rows < len(registros):
            self.grid.AppendRows(len(registros) - actual_rows)
        elif actual_rows > len(registros):
            self.grid.DeleteRows(0, actual_rows - len(registros))
        
        # Llenar datos
        for row, registro in enumerate(registros):
            for col, valor in enumerate(registro[1:]):  # Ignorar el ID
                self.grid.SetCellValue(row, col, str(valor))
                
        self.grid.AutoSizeColumns()
    
    def OnActualizar(self, event):
        self.CargarDatos()
        wx.MessageBox(
            "Lista actualizada",
            "Información",
            wx.OK | wx.ICON_INFORMATION
        )
    
    def OnExportar(self, event):
        # Implementar exportación a CSV
        wx.MessageBox(
            "Función de exportación en desarrollo",
            "Información",
            wx.OK | wx.ICON_INFORMATION
        )
    
    def OnBuscar(self, event):
        busqueda = self.search_ctrl.GetValue().lower()
        for row in range(self.grid.GetNumberRows()):
            coincide = False
            for col in range(self.grid.GetNumberCols()):
                if busqueda in self.grid.GetCellValue(row, col).lower():
                    coincide = True
                    break
            self.grid.ShowRow(row, coincide)

def init_listar(parent):
    return ListarClientesPanel(parent)