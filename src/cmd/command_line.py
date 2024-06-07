import subprocess

class DirectCommandLine:

    @staticmethod
    def popen(shell=True, **kwargs):
        command_execute =""
        for key, value in kwargs.items():
            command_execute += str(value) + ' '

        result_command = subprocess.Popen(command_execute, shell=shell,
                                  stdout=subprocess.PIPE)

        return result_command.communicate()[0]

    @staticmethod
    def call(shell=True, **kwargs):
        command_execute =""
        for key, value in kwargs.items():
            command_execute += str(value) + ' '

        subprocess.call(command_execute, shell=shell)
