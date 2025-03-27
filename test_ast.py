import unittest
from ast_builder import *

def print_ast(node, indent=0):
    """Pretty print the AST starting from the given node with proper indentation."""
    prefix = "  " * indent
    
    if node is None:
        print(f"{prefix}None")
        return
        
    # Print the node type
    print(f"{prefix}{node.__class__.__name__}")
    
    # Handle different node types
    if isinstance(node, ProgramNode):
        print(f"{prefix}  Global Declarations:")
        for decl in node.global_declarations:
            print_ast(decl, indent + 2)
        
        print(f"{prefix}  Functions:")
        for func in node.functions:
            print_ast(func, indent + 2)
            
        print(f"{prefix}  Main Function:")
        print_ast(node.main_function, indent + 2)
        
    elif isinstance(node, VariableDeclarationNode):
        print(f"{prefix}  Type: {node.datatype}")
        print(f"{prefix}  Identifier: {node.identifier}")
        print(f"{prefix}  Value: {node.value}")
        print(f"{prefix}  Is Dynasty: {node.is_dynasty}")
        print(f"{prefix}  Scope Level: {'GLOBAL' if node.scope_level == 0 else 'LOCAL'}")
        print(f"{prefix}  Array Dimensions: {node.array_dimensions}")
        
    elif isinstance(node, VariableReassignmentNode):
        print(f"{prefix}  Identifier: {node.identifier}")
        print(f"{prefix}  Operator: {node.operator}")
        print(f"{prefix}  Expression: {node.expression}")
        
    elif isinstance(node, FunctionNode):
        print(f"{prefix}  Return Type: {node.return_type}")
        print(f"{prefix}  Identifier: {node.identifier}")
        print(f"{prefix}  Parameters: {node.parameters}")
        print(f"{prefix}  Is Global: {node.is_global}")
        print(f"{prefix}  Scope Level: {'GLOBAL' if node.scope_level == 0 else 'LOCAL'}")
        print(f"{prefix}  Return Value: {node.return_val}")
        print(f"{prefix}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
            
    elif isinstance(node, MainFunctionNode):
        print(f"{prefix}  Identifier: {node.identifier}")
        print(f"{prefix}  Return Value: {node.return_val}")
        print(f"{prefix}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
            
    elif isinstance(node, FunctionCallNode):
        print(f"{prefix}  Name: {node.name}")
        print(f"{prefix}  Arguments: {node.arguments}")
        
    elif isinstance(node, DoWhileNode):
        print(f"{prefix}  Condition: {node.condition}")
        print(f"{prefix}  Loop Body:")
        for stmt in node.loop_body:
            print_ast(stmt, indent + 2)
            
    elif isinstance(node, WhileNode):
        print(f"{prefix}  Condition: {node.condition}")
        print(f"{prefix}  Loop Body:")
        for stmt in node.loop_body:
            print_ast(stmt, indent + 2)
            
    elif isinstance(node, ForLoopNode):
        print(f"{prefix}  Loop Variable: {node.loop_var}")
        print(f"{prefix}  Loop Condition: {node.loop_exp}")
        print(f"{prefix}  Loop Update: {node.loop_unary}")
        print(f"{prefix}  Loop Body:")
        for stmt in node.loop_body:
            print_ast(stmt, indent + 2)
            
    elif isinstance(node, IfNode):
        print(f"{prefix}  Condition: {node.condition}")
        print(f"{prefix}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
            
        if node.elif_nodes:
            print(f"{prefix}  Elif Nodes:")
            for elif_node in node.elif_nodes:
                print_ast(elif_node, indent + 2)
                
        if node.else_node:
            print(f"{prefix}  Else Node:")
            print_ast(node.else_node, indent + 2)
            
    elif isinstance(node, ElifNode):
        print(f"{prefix}  Condition: {node.condition}")
        print(f"{prefix}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
            
    elif isinstance(node, ElseNode):
        print(f"{prefix}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
            
    elif isinstance(node, BreakNode):
        print(f"{prefix}  Type: {node.type}")
        
    elif isinstance(node, ContinueNode):
        print(f"{prefix}  Type: {node.type}")
        
    elif isinstance(node, ArrayAssignmentNode):
        print(f"{prefix}  Identifier: {node.identifier}")
        print(f"{prefix}  Indices: {node.indices}")
        print(f"{prefix}  Operator: {node.operator}")
        print(f"{prefix}  Expression: {node.expression}")
        
    elif isinstance(node, UnaryOperationNode):
        print(f"{prefix}  Identifier: {node.identifier}")
        print(f"{prefix}  Operator: {node.operator}")
        
    elif isinstance(node, OutputNode):
        print(f"{prefix}  Expressions: {node.expressions}")
        
    else:
        # For any other node types
        print(f"{prefix}  Attributes:")
        for attr, value in node.__dict__.items():
            print(f"{prefix}    {attr}: {value}")

# Example usage in your test case
class TestRoyalScriptASTBuilder(unittest.TestCase):
    def test_valid_program(self):
        # Example tokens for a minimal valid program
        tokens = [
            # Program start
            [("crown", "crown"), ("~", "~")],
            
            # Main function header
            [("castle", "castle"), ("treasures", "treasures"), ("identifier", "Main"), ("(", "("), (")", ")"), ("{", "{")],
            
            # If statement header: cast( identifier X == treasures lit 2 ) {
            [("cast", "cast"), ("(", "("), ("identifier", "X"), ("==", "=="), ("treasures lit", "2"), (")", ")"), ("{", "{")],
            
            # If statement body: granted( scroll lit "Complete" )~ then close if block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # First twist branch: twist( treasures lit 8 > treasures lit 5 ) {
            [("twist", "twist"), ("(", "("), ("treasures lit", "8"), (">", ">"), ("treasures lit", "5"), (")", ")"), ("{", "{")],
            
            # Twist branch body: granted( scroll lit "Complete" )~ then close twist block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # Second twist branch: twist( 1 ) {
            [("twist", "twist"), ("(", "("), ("1", "1"), (")", ")"), ("{", "{")],
            
            # Twist branch body: granted( scroll lit "Complete" )~ then close twist block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # Third twist branch: twist( ! ( treasures lit 8 > treasures lit 5 ) ) {
            [("twist", "twist"), ("(", "("), ("!", "!"), ("(", "("), ("treasures lit", "8"), (">", ">"), ("treasures lit", "5"), (")", ")"), (")", ")")],
            
            # Open block for third twist branch
            [("(", "("), (")", ")"), ("{", "{")],
            
            # Third twist branch body: granted( scroll lit "Complete" )~ then close block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # Fourth twist branch: twist( 0 ) {
            [("twist", "twist"), ("(", "("), ("0", "0"), (")", ")"), ("{", "{")],
            
            # Fourth twist branch body: granted( scroll lit "Complete" )~ then close block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # Fifth twist branch: twist( mirror lit true ) {
            [("twist", "twist"), ("(", "("), ("mirror lit", "true"), (")", ")"), ("{", "{")],
            
            # Fifth twist branch body: granted( scroll lit "Complete" )~ then close block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # Sixth twist branch: twist( mirror lit false ) {
            [("twist", "twist"), ("(", "("), ("mirror lit", "false"), (")", ")"), ("{", "{")],
            
            # Sixth twist branch body: granted( scroll lit "Complete" )~ then close block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # Seventh twist branch: twist( identifier IsTrue ) {
            [("twist", "twist"), ("(", "("), ("identifier", "IsTrue"), (")", ")"), ("{", "{")],
            
            # Seventh twist branch body: granted( scroll lit "Complete" )~ then close block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # Eighth twist branch: twist( identifier Fun ( () ) ) {
            [("twist", "twist"), ("(", "("), ("identifier", "Fun"), ("(", "("), (")", ")"), (")", ")"), ("{", "{")],
            
            # Eighth twist branch body: granted( scroll lit "Complete" )~ then close block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # Ninth twist branch: twist( identifier Arr [ 1 ] [ 0 ] ) {
            [("twist", "twist"), ("(", "("), ("identifier", "Arr"), ("[", "["), ("1", "1"), ("]", "]"),
            ("[", "["), ("0", "0"), ("]", "]"), (")", ")"), ("{", "{")],
            
            # Ninth twist branch body: granted( scroll lit "Complete" )~ then close block
            [("granted", "granted"), ("(", "("), ("scroll lit", "\"Complete\""), (")", ")"), ("~", "~"), ("}", "}")],
            
            # Return statement and close main function:
            [("return", "return"), ("0", "0"), ("~", "~"), ("}", "}")],
            
            # Program end:
            [("reign", "reign"), ("~", "~")]
        ]

        # Parse the tokens and build the AST
        builder = RoyalScriptASTBuilder(tokens)
        ast = builder.build_ast()
        
        # Print the AST structure
        print("\n=== AST Structure ===")
        print_ast(ast)
        
        # Assertions to verify the AST structure
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, ProgramNode)
        self.assertIsInstance(ast.global_declarations, list)
        # If no global declarations are provided, the list can be empty.
        self.assertGreaterEqual(len(ast.global_declarations), 0)
        self.assertIsNotNone(ast.main_function)


if __name__ == "__main__":
    unittest.main()