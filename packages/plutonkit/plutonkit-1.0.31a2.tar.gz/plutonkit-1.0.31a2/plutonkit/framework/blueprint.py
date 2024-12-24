import os
import sys

from yaml import Loader, load

from plutonkit.config import PROJECT_COMMAND_FILE, PROJECT_DETAILS_FILE
from plutonkit.helper.command import clean_command_split, pip_run_command
from plutonkit.helper.environment import setEnvironmentVariable
from plutonkit.helper.filesystem import (
    create_yaml_file, generate_project_folder_cwd, write_file_content,
)
from plutonkit.helper.template import convert_shortcode
from plutonkit.management.filesystem.BlueprintFileSchema import (
    BlueprintFileSchema,
)
from plutonkit.management.logic.ConditionSplit import ConditionSplit
from plutonkit.management.request.ArchitectureRequest import (
    ArchitectureRequest,
)
from plutonkit.management.terminal.inquiry_terminal import InquiryTerminal


class FrameworkBluePrint:
    def __init__(self, path) -> None:
        self.path = path
        self.folder_name = ""
        self.directory = os.getcwd()
        self.arch_req = None

    def set_folder_name(self, name):
        self.folder_name = name

    def execute_clone_project(self,ans_ref):
        self.arch_req = ArchitectureRequest(self.path, self.directory)
        if self.arch_req.isValidReq is False:
            print(self.arch_req.errorMessage)
            self.arch_req.clearRepoFolder()
            sys.exit(0)
        try:
            generate_project_folder_cwd(self.folder_name)
            content = load(str(self.arch_req.getValidReq), Loader=Loader)
            self._bootloader_project(content,ans_ref)

        except Exception as e:
            print(e)
            print("Invalid details to proceed in creating new project")
            sys.exit(0)

    def execute_create_project(self):
        self.arch_req = ArchitectureRequest(self.path, self.directory)
        if self.arch_req.isValidReq is False:
            print(self.arch_req.errorMessage)
            self.arch_req.clearRepoFolder()
            sys.exit(0)
        try:
            generate_project_folder_cwd(self.folder_name)
            content = load(str(self.arch_req.getValidReq), Loader=Loader)

            choices = content.get("choices", [])

            inquiry_terminal = InquiryTerminal(choices)
            inquiry_terminal.execute()

            while inquiry_terminal.is_continue():

                if inquiry_terminal.is_terminate():
                    self._bootloader_project(content,inquiry_terminal.get_answer())
                    break

        except Exception as e:
            print(e)
            print("Invalid details to proceed in creating new project")
            self.arch_req.clearRepoFolder()
            sys.exit(0)

    def _bootloader_project(self, content, args):
        files = content.get("files", [])
        script = content.get("script", {})
        bootscript = content.get("bootscript", [])
        env = content.get("env",{})
        setEnvironmentVariable(env)
        terminal_answer = args
        terminal_answer["folder_name"] = self.folder_name

        self._files(files, terminal_answer)
        self._boot_command(bootscript, terminal_answer)
        os.chdir(self.directory)
        create_yaml_file(
            self.folder_name,
            PROJECT_DETAILS_FILE,
            {"name": self.folder_name, "blueprint": self.path, "default_choices": terminal_answer},
            )
        create_yaml_file(
            self.folder_name, PROJECT_COMMAND_FILE, {"script": self._script_template(script,terminal_answer), "env": env}
            )
        self.arch_req.clearRepoFolder()
        print("Congrats!! your first project has been generated")

    def _script_template(self,configs,args):
        for value in configs:
            commands = configs[value]['command']
            for key_com,val_com in enumerate(commands):
                commands[key_com] = convert_shortcode(val_com, args)
        return configs

    def _files(self, values, args):

        files_check: list[BlueprintFileSchema] = []
        default_item = values.get("default", [])

        for value in default_item:

            for file1 in self.arch_req.getBlob(value):
                files_check.append(BlueprintFileSchema(file1, args))

        optional_item = values.get("optional", [])
        for value in optional_item:

            cond_valid = ConditionSplit(value.get("condition"), args)

            if "dependent" in value and cond_valid.validCond():
                for s_value in value["dependent"]:
                    for file1 in self.arch_req.getBlob(s_value):

                        files_check.append(BlueprintFileSchema(file1, args))

        for value in files_check:
            if value.isObjFile():
                data = self.arch_req.getFiles(value.value["file"])
                if data["is_valid"]:
                    for save_file in value.get_save_files():
                        write_file_content(
                            self.directory, self.folder_name, save_file, data["content"], args
                        )
                else:
                    print(f"error in downloading the file {value.value['file']}")

    def _boot_command(self, values, args):

        path = os.path.join(self.directory, self.folder_name)

        is_exec_running = len(values)>0
        while is_exec_running:
            chdir = os.path.join(path,convert_shortcode(values[0].get("chdir",""), args))
            command = values[0].get("command", "")
            condition = values[0].get("condition", "")
            str_convert = convert_shortcode(command, args)

            is_valid = False
            if condition == "":
                is_valid = True
            else:
                cond_valid = ConditionSplit(condition, args)
                is_valid = cond_valid.validCond()

            if is_valid:
                os.chdir(chdir)
                try:
                    pip_run_command(clean_command_split(str_convert))
                except Exception as E:
                    print(E)
            values.pop(0)
            is_exec_running = len(values)>0
