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
    
    #assume to appy to simCLR pipeline
    def _apply(self, op: LogicalOperator) -> LogicalOperator:
        import albumentations as A
        operators = []
        isSet = False
        
        # Post-order traversal.
        nodes = deque()
        for node in op.post_order_iter():
            nodes.append(node)
        
        while len(nodes) > 0:
            current_op = nodes.pop()
            if not isinstance(current_op, AbstractUDFMap):
                for insert_op in operators:
                    insert_op._input_dependencies = [current_op]
                    insert_op._ouput_dependencies = current_op.input_dependencies
                    if len(current_op.output_dependencies) > 0:
                        current_op.output_dependencies[0]._input_dependencies = [insert_op]
                    current_op._output_dependencies = [insert_op]
                    current_op = insert_op
                    
                if not isSet:
                    op = current_op
                break
            
            if _get_udf_name(current_op._fn) == "album_randomcrop":
                operators.append(copy.copy(current_op))
                if len(current_op.input_dependencies) > 0:
                    current_op.input_dependencies[0]._output_dependencies = current_op.output_dependencies
                if len(current_op.output_dependencies) > 0:
                    current_op.output_dependencies[0]._input_dependencies = current_op.input_dependencies
            elif not isSet:
                op = current_op
                isSet = True
            
        return op        
