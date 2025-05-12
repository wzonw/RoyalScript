import unittest
from ast_builder import *

def print_ast(node, indent=0):
    """Return a pretty-printed string of the AST starting from the given node."""
    prefix = "  " * indent
    lines = []

    if node is None:
        lines.append(f"{prefix}None")
        return "\n".join(lines)
        
    # Node type and line/position info
    node_info = f"{prefix}{node.__class__.__name__}"
    if hasattr(node, 'line') and hasattr(node, 'position'):
        node_info += f" (Line: {node.line}, Position: {node.position})"
    lines.append(node_info)
    
    # Handle different node types
    if isinstance(node, ProgramNode):
        lines.append(f"{prefix}  Global Declarations:")
        for decl in node.global_declarations:
            lines.append(print_ast(decl, indent + 2))
        lines.append(f"{prefix}  Functions:")
        for func in node.functions:
            lines.append(print_ast(func, indent + 2))
        lines.append(f"{prefix}  Main Function:")
        lines.append(print_ast(node.main_function, indent + 2))
        
    elif isinstance(node, VariableDeclarationNode):
        lines.append(f"{prefix}  Type: {node.datatype}")
        lines.append(f"{prefix}  Identifier: {node.identifier}")
        lines.append(f"{prefix}  Value: {node.value}")
        lines.append(f"{prefix}  Is Dynasty: {node.is_dynasty}")
        lines.append(f"{prefix}  Scope Level: {'GLOBAL' if node.scope_level == 0 else 'LOCAL'}")
        lines.append(f"{prefix}  Array Dimensions: {node.array_dimensions}")
        
    elif isinstance(node, VariableReassignmentNode):
        lines.append(f"{prefix}  Identifier: {node.identifier}")
        lines.append(f"{prefix}  Operator: {node.operator}")
        lines.append(f"{prefix}  Expression: {node.expression}")
        
    elif isinstance(node, FunctionNode):
        lines.append(f"{prefix}  Return Type: {node.return_type}")
        lines.append(f"{prefix}  Identifier: {node.identifier}")
        lines.append(f"{prefix}  Parameters: {node.parameters}")
        lines.append(f"{prefix}  Is Global: {node.is_global}")
        lines.append(f"{prefix}  Scope Level: {'GLOBAL' if node.scope_level == 0 else 'LOCAL'}")
        lines.append(f"{prefix}  Return Value: {node.return_val}")
        lines.append(f"{prefix}  Body:")
        for stmt in node.body:
            lines.append(print_ast(stmt, indent + 2))
            
    elif isinstance(node, MainFunctionNode):
        lines.append(f"{prefix}  Identifier: {node.identifier}")
        lines.append(f"{prefix}  Return Value: {node.return_val}")
        lines.append(f"{prefix}  Body:")
        for stmt in node.body:
            lines.append(print_ast(stmt, indent + 2))
            
    elif isinstance(node, FunctionCallNode):
        lines.append(f"{prefix}  Name: {node.name}")
        lines.append(f"{prefix}  Arguments: {node.arguments}")
        
    elif isinstance(node, DoWhileNode):
        lines.append(f"{prefix}  Condition: {node.condition}")
        lines.append(f"{prefix}  Loop Body:")
        for stmt in node.loop_body:
            lines.append(print_ast(stmt, indent + 2))
            
    elif isinstance(node, WhileNode):
        lines.append(f"{prefix}  Condition: {node.condition}")
        lines.append(f"{prefix}  Loop Body:")
        for stmt in node.loop_body:
            lines.append(print_ast(stmt, indent + 2))
            
    elif isinstance(node, ForLoopNode):
        lines.append(f"{prefix}  Loop Variable: {node.loop_var}")
        lines.append(f"{prefix}  Loop Condition: {node.loop_exp}")
        lines.append(f"{prefix}  Loop Update: {node.loop_unary}")
        lines.append(f"{prefix}  Loop Body:")
        for stmt in node.loop_body:
            lines.append(print_ast(stmt, indent + 2))
            
    elif isinstance(node, IfNode):
        lines.append(f"{prefix}  Condition: {node.condition}")
        lines.append(f"{prefix}  Body:")
        for stmt in node.body:
            lines.append(print_ast(stmt, indent + 2))
        if node.elif_nodes:
            lines.append(f"{prefix}  Elif Nodes:")
            for elif_node in node.elif_nodes:
                lines.append(print_ast(elif_node, indent + 2))
        if node.else_node:
            lines.append(f"{prefix}  Else Node:")
            lines.append(print_ast(node.else_node, indent + 2))
            
    elif isinstance(node, ElifNode):
        lines.append(f"{prefix}  Condition: {node.condition}")
        lines.append(f"{prefix}  Body:")
        for stmt in node.body:
            lines.append(print_ast(stmt, indent + 2))
            
    elif isinstance(node, ElseNode):
        lines.append(f"{prefix}  Body:")
        for stmt in node.body:
            lines.append(print_ast(stmt, indent + 2))
            
    elif isinstance(node, BreakNode):
        lines.append(f"{prefix}  Type: {node.type}")
        
    elif isinstance(node, ContinueNode):
        lines.append(f"{prefix}  Type: {node.type}")
        
    elif isinstance(node, ArrayAssignmentNode):
        lines.append(f"{prefix}  Identifier: {node.identifier}")
        lines.append(f"{prefix}  Indices: {node.indices}")
        lines.append(f"{prefix}  Operator: {node.operator}")
        lines.append(f"{prefix}  Expression: {node.expression}")
        
    elif isinstance(node, UnaryOperationNode):
        lines.append(f"{prefix}  Identifier: {node.identifier}")
        lines.append(f"{prefix}  Operator: {node.operator}")
        
    elif isinstance(node, OutputNode):
        lines.append(f"{prefix}  Expressions: {node.expressions}")
        
    else:
        # For any other node types
        lines.append(f"{prefix}  Attributes:")
        for attr, value in node.__dict__.items():
            if attr not in ['line', 'position']:
                lines.append(f"{prefix}    {attr}: {value}")

    return "\n".join(lines)
