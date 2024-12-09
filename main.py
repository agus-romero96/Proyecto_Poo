import wx  # Reemplazamos tkinter por wx
from crear_form import init_crear
from listar_form import init_listar
from db import crear_tabla

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Gestión de clientes", size=(800, 600))
        
        # Crear tabla en la base de datos
        crear_tabla()
        
        # Crear el panel principal
        self.panel = wx.Panel(self)
        
        # Crear barra de menú
        barra_menu = wx.MenuBar()
        
        # Menú Archivo
        menu_archivo = wx.Menu()
        menu_archivo.Append(wx.ID_NEW, "Nuevo Archivo")
        menu_archivo.Append(wx.ID_ANY, "Nueva Ventana")
        menu_archivo.AppendSeparator()
        menu_archivo.Append(wx.ID_CLOSE, "Cerrar Ventana")
        salir = menu_archivo.Append(wx.ID_EXIT, "Salir")
        
        # Menú Gestión
        menu_gestion = wx.Menu()
        agregar_cliente = menu_gestion.Append(wx.ID_ANY, "Agregar cliente")
        listar_clientes = menu_gestion.Append(wx.ID_ANY, "Listado de clientes")
        
        # Agregar menús a la barra
        barra_menu.Append(menu_archivo, "Archivo")
        barra_menu.Append(menu_gestion, "Gestión Cliente")
        barra_menu.Append(wx.Menu(), "Edición")
        barra_menu.Append(wx.Menu(), "Selección")
        barra_menu.Append(wx.Menu(), "Vista")
        
        # Establecer la barra de menú
        self.SetMenuBar(barra_menu)
        
        # Vincular eventos
        self.Bind(wx.EVT_MENU, self.OnSalir, salir)
        self.Bind(wx.EVT_MENU, self.OnAgregarCliente, agregar_cliente)
        self.Bind(wx.EVT_MENU, self.OnListarClientes, listar_clientes)
        
        self.Centre()
        self.Show()
    
    def OnSalir(self, event):
        self.Close()
    
    def OnAgregarCliente(self, event):
        self.limpiar_panel()
        init_crear(self.panel)
        
    def OnListarClientes(self, event):
        self.limpiar_panel()
        init_listar(self.panel)
    
    def limpiar_panel(self):
        self.panel.DestroyChildren()

def main():
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()

if __name__ == '__main__':
    main()