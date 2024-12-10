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
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Email", "email"),
            ("Teléfono", "teléfono")
        ]
        
        self.controles = {}
        for etiqueta, campo_id in campos:
            # Etiqueta
            lbl = wx.StaticText(form_panel, label=f"{etiqueta}:")
            lbl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            # Campo de texto
            txt = wx.TextCtrl(form_panel, size=(300, -1))
            txt.SetHint(f"Ingrese el {etiqueta.lower()}")

            form_sizer.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            form_sizer.Add(txt, 1, wx.EXPAND | wx.ALL, 5)

            # Guardar el control con la clave correcta
            self.controles[campo_id] = txt
        
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
        # Imprimir para debug
        print("Contenido de self.controles:", self.controles.keys())
        # Mapeo directo de las claves que existen en self.controles
        for campo, control in self.controles.items():
            valor = control.GetValue().strip()
            # Imprimir para debug
            print(f"Campo original: '{campo}', Valor: '{valor}'")
            if not valor:
                wx.MessageBox(
                    f"El campo {campo} es obligatorio",
                    "Error de validación",
                    wx.OK | wx.ICON_ERROR
                )
                control.SetFocus()
                return
            # Limpiar el nombre del campo
            campo_limpio = campo.lower().replace(':', '').replace('é', 'e')
            datos[campo_limpio] = valor
        # Imprimir para debug
        print("Datos finales a guardar:", datos)
        # Verificar que tenemos todas las claves necesarias
        campos_requeridos = ['nombre', 'apellido', 'email', 'telefono']
        for campo in campos_requeridos:
            if campo not in datos:
                wx.MessageBox(
                    f"Error: Falta el campo {campo}",
                    "Error de validación",
                    wx.OK | wx.ICON_ERROR
                )
                return

        # Intentar guardar en la base de datos
        if crear_registro(datos):
            wx.MessageBox(
                "Cliente guardado exitosamente",
                "Éxito",
                wx.OK | wx.ICON_INFORMATION
            )
            self.OnLimpiar(None)
            self.GetParent().DestroyChildren()
            self.GetParent().GetParent().Centre()
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