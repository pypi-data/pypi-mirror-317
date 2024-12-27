from solovision.utils import logger as LOGGER
from solovision.utils.checks import RequirementsChecker

checker = RequirementsChecker()


def get_yolo_inferer(yolo_model):

    if 'yolox' in str(yolo_model):
        try:
            import yolox  # for linear_assignment
            assert yolox.__version__
        except (ImportError, AssertionError, AttributeError):
            checker.check_packages(('yolox==0.3.0',), cmds='--no-dependencies')
            checker.check_packages(('tabulate',))  # needed dependency
            checker.check_packages(('thop',))  # needed dependency
        from .yolox import YoloXStrategy
        return YoloXStrategy
    elif 'yolov8' in str(yolo_model):
        # ultralytics already installed when running track.py
        from .yolov8 import Yolov8Strategy
        return Yolov8Strategy

    elif 'yolov9' in str(yolo_model):
        try:
            import super_gradients  # for linear_assignment
            assert super_gradients.__version__
        except (ImportError, AssertionError, AttributeError):
            checker.check_packages(('super-gradients==3.1.3',))  # install
        from .yolov9 import Yolov9Strategy
        return Yolov9Strategy
    
    elif 'yolo_nas' in str(yolo_model):
        try:
            import super_gradients  # for linear_assignment
            assert super_gradients.__version__
        except (ImportError, AssertionError, AttributeError):
            checker.check_packages(('super-gradients==3.1.3',))  # install
        from .yolonas import YoloNASStrategy
        return YoloNASStrategy
    else:
        LOGGER.error('Failed to infer inference mode from yolo model name')
        LOGGER.error('Your model name has to contain either yolox, yolo_nas or yolov8')
        exit()
