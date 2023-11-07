
from analysis_modules.params_monitor import SysLog
from basic_operation.basic_io_operation import IoMethods
from analysis_modules.params_monitor import OutputParams

class ImageCreation:
    def __init__(self, output_params: OutputParams):
        self.log = SysLog()
        self.output_path = output_params.output_path

    def error_if_not_required(self, value, need_list, param_name):
        if value not in need_list:
            raise AttributeError("parameter {a} must be one of these values: "
                                 "{b}").format(a=param_name, b=str(need_list))

    @SysLog().calculate_cost_time("<store fig>")
    def store_fig(self, fig, output_file: str, output_path: str=None):
        extension = IoMethods.get_file_extension(output_file)
        output_type_list = ['.jpeg','.png','.webp','.svg','.pdf','.eps']
        self.error_if_not_required(extension, output_type_list, "output_file's extension")
        if output_path is not None:
            self.output_path = output_path
        IoMethods.mkdir_if_no_dir(self.output_path)
        full_output_path = IoMethods.join_path(self.output_path, output_file)

        fig.write_image(full_output_path)
        self.log.show_log(f'[IMAGE OUTPUT] image is stored as: {full_output_path}')
        return