import copy
from collections import deque
from ray.data._internal.logical.interfaces import LogicalOperator, LogicalPlan, Rule
from ray.data._internal.logical.operators.map_operator import (
    _get_udf_name,
    AbstractUDFMap
)


class PushdownFloatRule(Rule):
    def apply(self, plan: LogicalPlan) -> LogicalPlan:
        optimized_dag: LogicalOperator = self._apply(plan.dag)
        return LogicalPlan(dag=optimized_dag)
    
    #Assume that apply to simCLR pipeline
    def _apply(self, op: LogicalOperator) -> LogicalOperator:
        nodes = deque()
        float_ops = []
        tmp_op = None
        
        float_func = ("album_ToFloat", )
        jitter_func = ("album_ColorJitter", )
        blur_func = ("album_GaussianBlur",
                     "album_Blur",
                     "album_AdvancedBlur",
                     "album_MedianBlur",
                     "album_ZoomBlur",
                     "album_MotionBlur")
    
        for node in op.post_order_iter():
            nodes.appendleft(node)
            
        while len(nodes) > 0:
            current_op = nodes.pop()
            
            if (tmp_op == None) and isinstance(current_op, AbstractUDFMap) and (_get_udf_name(current_op._fn) in jitter_func + blur_func):
                tmp_op = current_op
            
            if isinstance(current_op, AbstractUDFMap) and (_get_udf_name(current_op._fn) in float_func):
                current_op._input_dependencies[0]._output_dependencies = current_op._output_dependencies
                if current_op._output_dependencies:
                    current_op._output_dependencies[0]._input_dependencies = current_op._input_dependencies
    
                float_ops.append(copy.copy(current_op))
                next_ops = current_op.output_dependencies
                
                while next_ops[0].output_dependencies:
                    if (tmp_op == None) and isinstance(current_op, AbstractUDFMap) and (_get_udf_name(next_ops[0]._fn) in jitter_func + blur_func):
                        tmp_op = copy.copy(tmp_op)
                        
                    if isinstance(current_op, AbstractUDFMap) and (_get_udf_name(next_ops[0]._fn) in float_func):
                        next_ops[0]._input_dependencies[0]._output_dependencies = next_ops[0]._output_dependencies
                        if next_ops[0]._output_dependencies:
                            next_ops[0]._output_dependencies[0]._input_dependencies = next_ops[0]._input_dependencies
                            
                        float_ops.append(copy.copy(current_op))
                    
                    next_ops = next_ops[0].output_dependencies
                break
        
        if float_ops:
            float_ops[0]._input_dependencies = tmp_op.input_dependencies
            float_ops[0]._output_dependencies = [tmp_op]
            tmp_op.input_dependencies[0]._output_dependencies = [float_ops[0]]
            tmp_op._input_dependencies = [float_ops[0]]
                
        return op
