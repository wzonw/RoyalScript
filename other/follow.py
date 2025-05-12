follow = {
    "program" : ["$", "$"],

    "global_dec" : ["spell", "castle"],

    "var_dec" :[
        "spell", "castle", "dynasty", "scroll", "treasures",
        "mirror", "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe", "return",
        "break", "continue", ")"
   ],

    "dynasty" :["scroll", "treasures", "mirror", "ocean", "rose"],

    "vardec_def" :["dynasty", "scroll", "treasures", "mirror", "ocean", "rose"],

    "initialization" :[",", "~"],

    "vardec_more" :["~"],

    "column" :["="],

    "array_initialization" :[",", "~"],

    "array_list" :[",", "~"],

    "array_content" :["}"],

    "array_row" :["}"],

    "row_more" :["}"],

    "row_more_ext" :["}"],

    "lit_more" :["}"],

    "array_more" :["~"],

    "array_lit" :["{", ",", "}"],

    "assignment_operator" :["identifier", "ocean_lit", "treasures_lit", "("],

    "assignment_operand" :["~"],

    "logical_exp" :[")"],

    "logical_operand" :["&&", "||", ")", ",", "~"],

    "expression" :["&&", "||", ")", ",", "~"],

    "logical_operand_ext" :["&&", "||", ")", ",", "~"],

    "logical_operator" :["!", "&&", "||", ")", ",", "~"],

    "logical_operator1" :["identifier", "ocean_lit", "treasures_lit", "scroll_lit", 
                        "mirror_lit", "1", "0", "("],

    "more_log" :[")", ",", "~"],

    "treasures_mirror" :["&&", "||", ")", ",", "~"],

    "arithmetic_exp" :[")"],

    "arithmetic_operand_1" :[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "&&", "||", ")", ",", "~"
   ],

    "arithmetic_operand_2" :[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "&&", "||", ")", ",", "~"
   ],

    "arithmetic_operand" :[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "&&", "||", ")", ",", "~"
   ],

    "arithmetic_operator" :["identifier", "ocean_lit", "treasures_lit", "("],

    "more_arith" :[
        "<", ">", "<=", ">=", "==", "!=", "&&", "||", ")", ",", "~"
   ],

    "relational_exp" :[")", "~"],

    "relational_operand" :[
        "<", ">", "<=", ">=", "==", "!=", "&&", "||", ")", ",", "~"
   ],

    "expression_2" :[
        "<", ">", "<=", ">=", "==", "!=", "&&", "||", ")", ",", "~"
   ],

    "relational_operator" :[
        "identifier", "ocean_lit", "treasures_lit", "scroll_lit",
        "rose_lit", "(", "mirror_lit"
   ],

    "relational_more" :["&&", "||", ")", ",", "~"],

    "unary" :[")"],

    "unary_operator" :[",", ")", "~"],

    "string_operand" :["+", ",", ")", "~"],

    "string_more" :[",", ")", "~"],

    "user_defined_func" :[
        "castle", "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror", "ocean",
        "rose", "granted", "identifier", "spell", "tale", "cast",
        "forever", "believe"
   ],

    "return_type" :["identifier"],

    "param" :[")"],

    "param_more" :[")"],

    "body_1" :[
        "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe"
   ],

    "body_1_ext" :[
        "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe"
   ],

    "body_2" :["return", ")", "break", "continue", "}"],

    "body" :["return", ")", "break", "continue", "}"],

    "ret_statement" :["}"],

    "condi_statement" :[
        "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe"
   ],

    "for_loop" :[
        "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe"
   ],

    "loop_var" :["~"],

    "loop_init" :["~"],

    "loop_val" :["~"],

    "loop_body" :["}"],

    "if_break" :[
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe", "}"
   ],

    "elif_break" :[
        "curse", "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe", "}"
   ],

    "else_break" :[
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe", "}"
   ],

    "flow_control" :["}"],

    "do_while" :[
        "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe"
   ],

    "condition" :[")"],

    "expression_3" :[")"],

    "other_id_ext" :[")"],

    "condi_id_ext" :[")"],

    "other_id_ext_1" :[")"],

    "other_id_ext_2" :[")"],

    "mirror_init" :[")"],

    "while_statement" :[
        "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe"
   ],

    "if_statement" :[
        "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe"
   ],

    "elif_statement" :[
        "curse", "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe"
   ],

    "else_statement" :[
        "return", ")", "break", "continue", "}",
        "dynasty", "scroll", "treasures", "mirror",
        "ocean", "rose", "granted", "identifier", "spell",
        "tale", "cast", "forever", "believe"
   ],

    "output" :[
        "dynasty", "scroll", "treasures", "mirror", "ocean",
        "rose", "granted", "identifier", "spell", "tale", "cast",
        "forever", "believe", "return", ")", "break", "continue", "}"
   ],

    "granted_content_1" :[",", ")"],

    "granted_content_2" :[",", ")", "~"],

    "granted_content" :[",", ")"],

    "granted_open_paren_ext" :[",", ")", "~"],

    "granted_id_ext" :[",", ")", "~"],

    "granted_other_id_ext" :[",", ")", "~"],

    "granted_scroll_ext" :[",", ")", "~"],

    "granted_rose_ext" :[",", ")", "~"],

    "granted_lit3_ext" :[",", ")", "~"],

    "more_granted" :[")"],

    "data_type" :["identifier"],

    "val" :[",", "~"],

    "val1" :["~"],

    "val1_ext" :["~"],

    "val1_id_ext" :["~"],

    "conversion_func" :[")"],

    "conversion_value" :[")"],

    "index" :[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "&&", "||", ")", ",", "~", "+=", "-=", "*=", "/=", "%=", "=~"
   ],

    "column1" :[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "&&", "||", ")", ",", "~", "+=", "-=", "*=", "/=", "%=", "=~"
   ],

    "input" :[",", "~"],

    "lit1" :["+", ",", ")", "~", "}"],

    "lit2" :[",", "}", ")"],

    "lit3" :[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "&&", "||", ")", ",", "~", "}"
   ],

    "lit4" :[",", "}", ")"],

    "func_call" :[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "&&", "||", ")", ",", "~", "+=", "-=", "*=", "/=", "%=", "=~"
   ],

    "args" :[")"],

    "args_val" :[",", ")"],

    "args_more" :[")"],

    "array_element" :[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "&&", "||", ")", ",", "~", "+=", "-=", "*=", "/=", "%=", "=~"
   ],

    "id_ext" :[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "&&", "||", ")", ",", "~", "+=", "-=", "*=", "/=", "%=", "=~"
   ],

    "array_size" :["]"],

    "datatype" : ["treasures", "ocean", "scroll", "rose", "mirror"],
}


first = {
    "program":["crown"],
    "global_dec":["dynasty", "scroll", "treasures", "mirror", "ocean", "rose", ],
    "var_dec":["dynasty", "scroll", "treasures", "mirror", "ocean", "rose"],
    "dynasty":["dynasty", ],
    "vardec_def":["=", "[", ],
    "initialization":["=", ],
    "vardec_more":[",", ],
    "column":["[", ],
    "array_initialization":["="],
    "array_list":["{"],
    "array_content":["scroll_lit", "rose_lit", "mirror_lit", "ocean_lit", "treasures_lit", "identifier", "{"],
    "array_row":["scroll_lit", "rose_lit", "mirror_lit", "ocean_lit", "treasures_lit", "identifier"],
    "row_more":[",", ],
    "row_more_ext":["{", "identifier"],
    "lit_more":[",", ],
    "array_more":[",", ],
    "array_lit":["scroll_lit", "rose_lit", "mirror_lit", "ocean_lit", "treasures_lit", "identifier"],
    "assignment_operator":["+=", "-=", "*=", "/=", "%="],
    "assignment_operand":["identifier", "ocean_lit", "treasures_lit", "("],
    "logical_exp":["identifier", "ocean_lit", "treasures_lit", "scroll_lit", "mirror_lit", "1", "0", "(", "!"],
    "logical_operand":["identifier", "ocean_lit", "treasures_lit", "scroll_lit", "mirror_lit", "1", "0", "("],
    "expression":["identifier", "ocean_lit", "treasures_lit", "scroll_lit", "rose_lit", "(", "1", "0", "!"],
    "logical_operand_ext":["+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=", ],
    "logical_operator":["&&", "||"],
    "logical_operator1":["!", ],
    "more_log":["&&", "||", ],
    "treasures_mirror":["1", "0"],
    "arithmetic_exp":["identifier", "ocean_lit", "treasures_lit", "("],
    "arithmetic_operand_1":["identifier", "ocean_lit", "treasures_lit"],
    "arithmetic_operand_2":["("],
    "arithmetic_operand":["identifier", "ocean_lit", "treasures_lit", "("],
    "arithmetic_operator":["+", "-", "/", "*", "%"],
    "more_arith":["+", "-", "/", "*", "%", ],
    "relational_exp":["identifier", "ocean_lit", "treasures_lit", "scroll_lit", "rose_lit", "(", "mirror_lit"],
    "relational_operand":["identifier", "ocean_lit", "treasures_lit", "scroll_lit", "rose_lit", "(", "mirror_lit", "treasures_lit"],
    "expression_2":["identifier", "ocean_lit", "treasures_lit", "(", "scroll_lit", "rose_lit"],
    "relational_operator":["<", ">", "<=", ">=", "==", "!="],
    "relational_more":["<", ">", "<=", ">=", "==", "!=", ],
    "unary":["identifier"],
    "unary_operator":["++", "--"],
    "string_operand":["scroll_lit", "rose_lit", "identifier", "toscroll"],
    "string_more":["+", ],
    "user-defined_func":["spell", ],
    "return_type":["scroll", "treasures", "mirror", "ocean", "rose", "chamber"],
    "param":["scroll", "treasures", "mirror", "ocean", "rose", ],
    "param_more":[",", ],
    "body_1":["dynasty", "scroll", "treasures", "mirror", "ocean", "rose", "granted", "identifier", "spell", "tale", ],
    "body_1_ext":["(", "=", "++", "--", "[", ],
    "body_2":["cast", "forever", "believe"],
    "body":["dynasty", "scroll", "treasures", "mirror", "ocean", "rose", "granted", "identifier", "spell", "tale", "cast", "forever", "believe", ],
    "ret_statement":["return", ],
    "condi_statement":["cast", "forever", "believe"],
    "for_loop":["tale"],
    "loop_var":["treasures", "identifier"],
    "loop_init":["=", ],
    "loop_val":["identifier", "treasures_lit"],
    "loop_body":["dynasty", "scroll", "treasures", "mirror", "ocean", "rose", "granted", "identifier", "spell", "tale", "cast", "forever", "believe", ],
    "if_break":["cast"],
    "elif_break":["twist", ],
    "else_break":["curse", ],
    "flow_control":["break", "continue", ],
    "do_while":["believe"],
    "condition":["identifier", "!", "mirror_lit", "ocean_lit", "treasures_lit", "scroll_lit", "rose_lit", "(", ],
    "expression_3":["identifier", "ocean_lit", "treasures_lit", "scroll_lit", "mirror_lit", "1", "0", "(", "!"],
    "condi_id_ext":["==", "!=", "(", "[", "+", "-", "/", "*", "%", ],
    "other_id_ext":["+", "-", "/", "*", "%", "&&", "||", ],
    "other_id_ext_1":["+", "-", "/", "*", "%", ],
    "other_id_ext_2":["&&", "||", ],
    "mirror_init":["==", "!=", ],
    "while":["forever"],
    "if":["cast"],
    "elif":["twist", ],
    "else":["curse", ],
    "output":["granted"],
    "granted_content_1":["set_precision", "identifier"],
    "granted_content_2":[
        "phantom", "torose", "totreasures", "toocean", "tomirror", "toscroll",
        "1", "0", "mirror_lit", "scroll_lit", "rose_lit", "ocean_lit",
        "treasures_lit", "lengthof", "(", "!", 
    ],
    "granted_content":[
        "set_precision", "identifier", "phantom", "torose", "totreasures", "toocean",
        "tomirror", "toscroll", "1", "0", "mirror_lit", "scroll_lit",
        "rose_lit", "ocean_lit", "treasures_lit", "(", "!", 
    ],
    "granted_open_paren_ext":[
        "identifier", "ocean_lit", "treasures_lit", "(", "scroll_lit",
        "rose_lit", "1", "0", "!"
    ],
    "granted_id_ext":["++", "--", "(", "[", ],
    "granted_other_id_ext":["+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=", ],
    "granted_scroll_ext":["+", "<", ">", "<=", ">=", "==", "!="],
    "granted_rose_ext":["+", "<", ">", "<=", ">=", "==", "!=", ],
    "granted_lit3_ext":["+", "-", "/", "*", "%", ],
    "more_granted":[",", ],
    "data_type":["scroll", "treasures", "mirror", "ocean", "rose"],
    "val":[
        "phantom", "torose", "totreasures", "toocean", "tomirror", "toscroll",
        "1", "0", "mirror_lit", "scroll_lit", "rose_lit", "ocean_lit",
        "treasures_lit", "(", "!", "identifier", "wish", 
    ],
    "val1":[
        "phantom", "torose", "totreasures", "toocean", "tomirror", "toscroll",
        "1", "0", "mirror_lit", "scroll_lit", "rose_lit", "ocean_lit",
        "treasures_lit", "(", "!", "identifier"
    ],
    "val1_ext":[
        "(", "[", "++", "--", "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "+=", "-=", "*=", "/=", "%=", "=", 
    ],
    "val1_id_ext":[
        "+", "-", "/", "*", "%", "<", ">", "<=", ">=", "==", "!=",
        "+=", "-=", "*=", "/=", "%=", "=", 
    ],
    "conversion_func":["torose", "totreasures", "toocean", "tomirror"],
    "conversion_value":["scroll_lit", "rose_lit", "mirror_lit", "ocean_lit", "treasures_lit", "identifier"],
    "index":["[", ],
    "column1":["["],
    "input":["wish"],
    "lit1":["scroll_lit", "rose_lit"],
    "lit2":["mirror_lit"],
    "lit3":["ocean_lit", "treasures_lit"],
    "lit4":["scroll_lit", "rose_lit", "mirror_lit", "ocean_lit", "treasures_lit"],
    "func_call":["("],
    "args":["identifier", "scroll_lit", "rose_lit", "mirror_lit", "ocean_lit", "treasures_lit", ],
    "args_val":["identifier", "scroll_lit", "rose_lit", "mirror_lit", "ocean_lit", "treasures_lit"],
    "args_more":[",", ],
    "array_element":["[", ],
    "id_ext":["(", "[", ],
    "array_size":["identifier", "positive_treasures_lit", "0"]
}
