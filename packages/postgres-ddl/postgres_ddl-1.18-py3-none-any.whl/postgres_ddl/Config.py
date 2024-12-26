#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config():
    Indent = " " * 2
    NL = chr(10)
    FunctionParamSign = ":="
    ShowSequenceGrantsInTable = False
    ShowUserMappings = True
    FolderFunction = "functions"
    FolderTrigger  = "triggers"

    @staticmethod
    def Parse(json):
        Config.Indent = " " * (json.get("indent") or 2)
        Config.NL = json.get("new_line") or chr(10)
        Config.FunctionParamSign = json.get("fnc_param_sign") or ":="

        settings = json.get("settings") or {}
        Config.ShowSequenceGrantsInTable = (settings.get("show_sequence_grants_in_table") is True)
        Config.ShowUserMappings = (settings.get("show_user_mappings") is not False)
        Config.FolderFunction = settings.get("folder_functions") or "functions"
        Config.FolderTrigger  = settings.get("folder_triggers")  or "triggers"
