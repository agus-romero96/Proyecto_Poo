import wx
import wx.grid
from db import crear_registro

class CrearClientePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Crear un sizer principal con márgenes
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(wx.Colour(240, 240, 240))  # Fondo suave
        
        # Título de la sección
        titulo = wx.StaticText(self, label="Agregar Nuevo Cliente")
        titulo.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(titulo, 0, wx.ALL | wx.CENTER, 20)
        
        # Panel para el formulario
        form_panel = wx.Panel(self)
        form_sizer = wx.FlexGridSizer(rows=5, cols=2, vgap=15, hgap=10)
        
        # Campos del formulario con sus etiquetas
        campos = [
            ("Nombre:", "Ingrese el nombre del cliente"),
            ("Apellido:", "Ingrese el apellido del cliente"),
            ("Email:", "Ingrese el email del cliente"),
            ("Teléfono:", "Ingrese el teléfono del cliente")
        ]
        
        self.controles = {}
        for label, hint in campos:
            # Etiqueta
            lbl = wx.StaticText(form_panel, label=label)
            lbl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
            # Campo de texto
            txt = wx.TextCtrl(form_panel, size=(300, -1))
            txt.SetHint(hint)  # Placeholder
            txt.SetName(label.replace(":", ""))  # Nombre para accesibilidad
            
            form_sizer.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            form_sizer.Add(txt, 1, wx.EXPAND | wx.ALL, 5)
            
            self.controles[label.lower().replace(":", "")] = txt
        
        form_panel.SetSizer(form_sizer)
        main_sizer.Add(form_panel, 0, wx.ALL | wx.CENTER, 20)
        
        # Botones
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_guardar = wx.Button(self, label="&Guardar")
        self.btn_guardar.SetBackgroundColour(wx.Colour(0, 128, 0))  # Verde
        self.btn_guardar.SetForegroundColour(wx.WHITE)
        self.btn_limpiar = wx.Button(self, label="&Limpiar")
        
        button_sizer.Add(self.btn_guardar, 0, wx.ALL, 5)
        button_sizer.Add(self.btn_limpiar, 0, wx.ALL, 5)
        
        main_sizer.Add(button_sizer, 0, wx.CENTER | wx.ALL, 10)
        
        # Vincular eventos
        self.btn_guardar.Bind(wx.EVT_BUTTON, self.OnGuardar)
        self.btn_limpiar.Bind(wx.EVT_BUTTON, self.OnLimpiar)
        
        # Configurar accesibilidad
        self.SetAcceleratorTable(wx.AcceleratorTable([
            (wx.ACCEL_ALT, ord('G'), self.btn_guardar.GetId()),
            (wx.ACCEL_ALT, ord('L'), self.btn_limpiar.GetId()),
        ]))
        
        self.SetSizer(main_sizer)
    
    def OnGuardar(self, event):
        # Validar campos
        datos = {}
        for campo, control in self.controles.items():
            valor = control.GetValue().strip()
            if not valor:
                wx.MessageBox(
                    f"El campo {campo} es obligatorio",
                    "Error de validación",
                    wx.OK | wx.ICON_ERROR
                )
                control.SetFocus()
                return
            datos[campo] = valor
        
        # Guardar en la base de datos
        if crear_registro(datos):
            wx.MessageBox(
                "Cliente guardado exitosamente",
                "Éxito",
                wx.OK | wx.ICON_INFORMATION
            )
            self.OnLimpiar(None)
        else:
            wx.MessageBox(
                "Error al guardar el cliente",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
    
    def OnLimpiar(self, event):
        for control in self.controles.values():
            control.SetValue("")
        self.controles["nombre"].SetFocus()

def init_crear(parent):
    return CrearClientePanel(parent)