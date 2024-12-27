# from .detector import ObjectDetection
from .models.Detectron2.detectron2_model import Detectron2
from .models.DETR.detr import DETR
from .models.DETR_CLIP.detr_clip import DETRCLIP
from .models.GroundingDINO.groundingdino import GroundingDINO
from .models.kosmos2.kosmos2 import Kosmos2
from .models.owlvit.owlvit import OWLVit
from .models.rtdetr.rtdetr import RTDETR
from .models.sam2.sam2 import SAM2
from .models.YOLO.YOLOv5.yolov5 import YOLOv5
from .models.YOLO.YOLOv6.yolov6 import YOLOv6
from .models.YOLO.YOLOv7.yolov7 import YOLOv7
from .models.YOLO.YOLOv8.yolov8 import YOLOv8
from .models.YOLO.YOLOv10.yolov10 import YOLOv10
from .models.YOLO.YOLOv11.yolov11 import YOLOv11
from .models.YOLO.YOLOX.yolox import YOLOX
