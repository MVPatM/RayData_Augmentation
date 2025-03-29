import copy
from collections import deque
from ray.data._internal.logical.interfaces import LogicalOperator, LogicalPlan, Rule
from ray.data._internal.logical.operators.map_operator import (
    _get_udf_name,
    AbstractUDFMap
)

class TestLogicalRule(Rule):
    def apply(self, plan: LogicalPlan) -> LogicalPlan:
        optimized_dag: LogicalOperator = self._apply(plan.dag)
        return LogicalPlan(dag=optimized_dag)
    
    #Assume that apply to simCLR pipeline
    def _apply(self, op: LogicalOperator) -> LogicalOperator:
        operators = []
        udf_op = []
        
        crop_func = ("album_RandomCrop",
                     "album_CenterCrop",
                     "album_Crop",
                     "album_CropNonEmptyMaskIfExists",
                     "album_RandomSizedCrop",
                     "album_RandomResizedCrop",
                     "album_RandomCropNearBBox",
                     "album_RandomSizedBBoxSafeCrop",
                     "album_CropAndPad",
                     "album_RandomCropFromBorders",
                     "album_BBoxSafeRandomCrop")
        
        resize_func = ("album_RandomScale",
                       "album_LongestMaxSize",
                       "album_SmallestMaxSize",
                       "album_Resize")
        
        grayscale_func = ("album_ToGray")
        
        crop_op = []
        resize_op = []
        grayscale_op = []
        
        # Post-order traversal.
        nodes = deque()
        for node in op.post_order_iter():
            nodes.append(node)
        
        while len(nodes) > 0:
            current_op = nodes.pop()
            
            if not isinstance(current_op, AbstractUDFMap):
                operators.append(copy.copy(current_op))
            else:
                if _get_udf_name(current_op._fn) in crop_func:
                    crop_op.append(copy.copy(current_op))
                elif _get_udf_name(current_op._fn) in resize_func:
                    resize_op.append(copy.copy(current_op))
                elif _get_udf_name(current_op._fn) in grayscale_func:
                    grayscale_op.append(copy.copy(current_op))
                else:
                    udf_op.append(copy.copy(current_op))
        
        op = operators[0]
        op._input_dependencies = []
        
        for resize in resize_op:
            resize._input_dependencies = [op]
            op._output_dependencies = [resize]
            op = resize
        
        for crop in crop_op:
            crop._input_dependencies = [op]
            op._output_dependencies = [crop]
            op = crop
            
        for grayscale in grayscale_op:
            grayscale._input_dependencies = [op]
            op._output_dependencies = [grayscale]
            op = grayscale
            
        for udf in udf_op:
            udf._input_dependencies = [op]
            op._output_dependencies = [udf]
            op = udf
        
        for i in range(1, len(operators)):
            operators[i]._input_dependencies = [op]
            op = operators[i]
            op._output_dependencies = [operators[i]]
        
        op._output_dependencies = []
        return op        
