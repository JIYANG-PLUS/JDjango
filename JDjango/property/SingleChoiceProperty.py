from .SingleChoiceDialogAdapter import *

class SingleChoiceProperty(wxpg.StringProperty):
    def __init__(self, label, name=wxpg.PG_LABEL, value=''):
        wxpg.StringProperty.__init__(self, label, name, value)

        # Prepare choices
        dialog_choices = []
        dialog_choices.append("Cat")
        dialog_choices.append("Dog")
        dialog_choices.append("Gibbon")
        dialog_choices.append("Otter")

        self.dialog_choices = dialog_choices

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrlAndButton")

    def GetEditorDialog(self):
        # Set what happens on button click
        return SingleChoiceDialogAdapter(self.dialog_choices)
