class RoyalScriptParser: 
    CFG = {
    '<program>': [
        ['crown', '~', '<global_dec>', '<user-defined_func>', 'castle', 'treasures', 'identifier', '(', ')', '{', '<body>', 'return', '0', '~', '}', 'reign', '~'],
    ],
    '<global_dec>': [
        ['<var_dec>', '<global_dec>'],
        ['ε'],
    ],
    '<var_dec>': [
        ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>'],
    ],
    '<dynasty>': [
        ['dynasty'],
        ['ε'],
    ],
    '<vardec_def>': [
        ['<initialization>', '<vardec_more>', '~'],
        ['[', '<array_size>', ']', '<column>', '<array_initialization>', '<array_more>', '~'],
    ],
    '<initialization>': [
        ['=', '<val>'],
        ['ε'],
    ],
    '<vardec_more>': [
        [',', 'identifier', '<initialization>', '<vardec_more>'],
        ['ε'],
    ],
    '<column>': [
        ['[', '<array_size>', ']'],
        ['ε'],
    ],
    '<array_initialization>': [
        ['=', '<array_list>'],
        ['ε'],
    ],
    '<array_list>': [
        ['{', '<array_content>', '}'],
    ],
    '<array_content>': [
        ['<array_lit>', '<lit_more>'],
        ['{', '<array_row>', '}', '<row_more>'],
    ],
    '<array_row>': [
        ['<array_lit>', '<lit_more>'],
    ],
    '<row_more>': [
        [',', '<row_more_ext>'],
        ['ε'],
    ],
    '<row_more_ext>': [
        ['{', '<array_row>', '}', '<row_more>'],
        ['identifier', '<row_more>'],
    ],
    '<lit_more>': [
        [',', '<lit_more_ext>'],
        ['ε'],
    ],
    '<lit_more_ext>': [
        ['<array_lit>', '<lit_more>'],
        ['{', '<array_row>', '}', '<row_more>'],
    ],
    '<array_more>': [
        [',', 'identifier', '[', '<array_size>', ']', '<column>', '<array_initialization>', '<array_more>'],
        ['ε'],
    ],
    '<array_lit>': [
        ['<lit4>'],
        ['identifier'],
    ],
    '<assignment_operator>': [
        ['+='],
        ['-='],
        ['*='],
        ['/='],
        ['%='],
    ],
    '<assignment_operand>': [
        ['identifier', '<id_ext>', '<more_arith>'],
        ['<lit3>', '<more_arith>'],
        ['<arithmetic_operand_2>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ],
    '<logical_exp>': [
        ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ],
    '<logical_operand>': [
        ['identifier', '<id_ext>', '<logical_operand_ext>'],
        ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['scroll_lit', '<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['rose_lit', '<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['mirror_lit', '<relational_more>'],
        ['<treasures_mirror>', '<relational_more>'],
        ['(', '<logical_operator1>', '<expression>'],
    ],
    '<expression>': [
        ['identifier', '<id_ext>', '<expression_ext_1>'],
        ['<lit3>', '<expression_ext_1>'],
        ['scroll_lit', '<expression_ext_2>'],
        ['rose_lit', '<expression_ext_2>'],
        ['mirror_lit', '<expression_ext_2>'],
        ['<treasures_mirror>', '<expression_ext_2>'],
        ['(', '<logical_operator1>', '<expression>', '<more_log>', ')', '<logical_operand_ext>'],
    ],
    '<expression_ext_1>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')'],
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', '<more_log>', ')', '<more_arith>', '<relational_more>'],
    ],
    '<expression_ext_2>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')'],
    ],
    '<logical_operand_ext>': [
        ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['ε'],
    ],
    '<logical_operator>': [
        ['&&'],
        ['||'],
    ],
    '<logical_operator1>': [
        ['!'],
        ['ε'],
    ],
    '<more_log>': [
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
        ['ε'],
    ],
    '<treasures_mirror>': [
        ['1'],
        ['0'],
    ],
    '<arithmetic_exp>': [
        ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ],
    '<arithmetic_operand_1>': [
        ['identifier', '<id_ext>'],
        ['<lit3>'],
    ],
    '<arithmetic_operand_2>': [
        ['(', '<arithmetic_exp>', ')'],
    ],
    '<arithmetic_operand>': [
        ['<arithmetic_operand_1>'],
        ['<arithmetic_operand_2>'],
    ],
    '<arithmetic_operator>': [
        ['+'],
        ['-'],
        ['/'],
        ['*'],
        ['%'],
    ],
    '<more_arith>': [
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
        ['ε'],
    ],
    '<relational_exp>': [
        ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ],
    '<relational_operand>': [
        ['identifier', '<id_ext>', '<more_arith>'],
        ['<lit3>', '<more_arith>'],
        ['scroll_lit'],
        ['rose_lit'],
        ['mirror_lit'],
        ['treasures_mirror'],
        ['(', '<expression_2>'],
    ],
    '<expression_2>': [
        ['identifier', '<id_ext>', '<expression_2_ext>'],
        ['<lit3>', '<expression_2_ext>'],
        ['scroll_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
        ['rose_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
        ['mirror_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
        ['treasures_mirror', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
        ['(', '<expression_2>', ')'],
    ],
    '<expression_2_ext>': [
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', ')', '<more_arith>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ],
    '<relational_operator>': [
        ['<'],
        ['>'],
        ['<='],
        ['>='],
        ['=='],
        ['!='],
    ],
    '<relational_more>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>'],
        ['ε'],
    ],
    '<unary>': [
        ['identifier', '<unary_operator>'],
    ],
    '<unary_operator>': [
        ['++'],
        ['--'],
    ],
    '<string_operand>': [
        ['<lit1>'],
        ['identifier', '<id_ext>'],
        ['toscroll', '(', '<conversion_value>', ')'],
    ],
    '<string_more>': [
        ['+', '<string_operand>', '<string_more>'],
        ['ε'],
    ],
    '<user-defined_func>': [
        ['spell', '<return_type>', 'identifier', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<user-defined_func>'],
        ['ε'],
    ],
    '<return_type>': [
        ['<data_type>'],
        ['chamber'],
    ],
    '<param>': [
        ['<data_type>', 'identifier', '<param_more>'],
        ['ε'],
    ],
    '<param_more>': [
        [',', '<data_type>', 'identifier', '<param_more>'],
        ['ε'],
    ],
    '<body>': [
        ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<body>'],
        ['granted', '(', '<granted_content>', '<more_granted>', ')', '~', '<body>'],
        ['identifier', '<body_1_ext>', '<body>'],
        ['spell', '<return_type>', 'identifier', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<body>'],
        ['tale', '(', '<loop_var>', '~', '<relational_exp>', '~', '<unary>', ')', '{', '<loop_body>', '}', '<body>'],
        ['cast', '(', '<condition>', ')', '{', '<body>', '}', '<elif>', '<else>', '<body>'],
        ['forever', '(', '<condition>', ')', '{', '<loop_body>', '}', '<body>'],
        ['believe', '{', '<loop_body>', '}', 'forever', '(', '<condition>', ')', '~', '<body>'],
        ['ε'],
    ],
    '<body_1_ext>': [
        ['(', '<args>', ')', '~'],
        ['<index>', '<body_1_other_ext>'],
        ['<unary_operator>', '~'],
    ],
    '<body_1_other_ext>': [
        ['=', '<val>', '~'],
        ['<assignment_operator>', '<assignment_operand>', '~'],
    ],
    '<ret_statement>': [
        ['return', '<val1>', '~'],
        ['ε'],
    ],
    '<loop_var>': [
        ['treasures', 'identifier', '=', '<loop_val>'],
        ['identifier', '<loop_init>'],
    ],
    '<loop_init>': [
        ['=', '<loop_val>'],
        ['ε'],
    ],
    '<loop_val>': [
        ['identifier'],
        ['treasures_lit'],
        ['1'],
        ['0'],
    ],
    '<loop_body>': [
        ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<loop_body>'],
        ['granted', '(', '<granted_content>', '<more_granted>', ')', '~', '<loop_body>'],
        ['identifier', '<body_1_ext>', '<loop_body>'],
        ['spell', '<return_type>', 'identifier', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<loop_body>'],
        ['tale', '(', '<loop_var>', '~', '<relational_exp>', '~', '<unary>', ')', '{', '<loop_body>', '}', '<loop_body>'],
        ['cast', '(', '<condition>', ')', '{', '<loop_body>', '<flow_control>', '}', '<elif_break>', '<else_break>', '<loop_body>'],
        ['forever', '(', '<condition>', ')', '{', '<loop_body>', '}', '<loop_body>'],
        ['believe', '{', '<loop_body>', '}', 'forever', '(', '<condition>', ')', '~', '<loop_body>'],
        ['ε'],
    ],
    '<elif_break>': [
        ['twist', '(', '<condition>', ')', '{', '<body>', '<flow_control>', '}', '<elif_break>'],
        ['ε'],
    ],
    '<else_break>': [
        ['curse', '{', '<body>', '<flow_control>', '}'],
        ['ε'],
    ],
    '<flow_control>': [
        ['break', '~'],
        ['continue', '~'],
        ['ε'],
    ],
    '<condition>': [
        ['<treasures_mirror>', '<more_log>'],
        ['identifier', '<condi_id_ext>'],
        ['!', '<logical_operand>', '<more_log>'],
        ['mirror_lit', '<relational_more>', '<more_log>'],
        ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['scroll_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['rose_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['(', '<logical_operator1>', '<expression>', '<more_log>'],
    ],
    '<condi_id_ext>': [
        ['<func_call>', '<other_id_ext>'],
        ['[', '<array_size>', ']', '<column1>', '<other_id_ext>'],
        ['<other_id_ext>'],
    ],
    '<other_id_ext>': [
        ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['ε'],
    ],
    '<elif>': [
        ['twist', '(', '<condition>', ')', '{', '<body>', '}', '<elif>'],
        ['ε'],
    ],
    '<else>': [
        ['curse', '{', '<body>', '}'],
        ['ε'],
    ],
    '<granted_content_1>': [
        ['set_precision'],
        ['identifier', '<granted_id_ext>'],
    ],
    '<granted_content_2>': [
        ['phantom'],
        ['lengthof', '(', 'identifier', '<index>', ')'],
        ['<conversion_func>', '(', '<conversion_value>', ')'],
        ['toscroll', '(', '<conversion_value>', ')', '<string_more>'],
        ['<treasures_mirror>', '<more_log>'],
        ['mirror_lit', '<relational_more>', '<more_log>'],
        ['scroll_lit', '<granted_scroll_ext>'],
        ['rose_lit', '<granted_rose_ext>'],
        ['<lit3>', '<granted_lit3_ext>'],
        ['(', '<logical_operator1>', '<granted_open_paren_ext>'],
        ['!', '<logical_operand>', '<more_log>'],
    ],
    '<granted_content>': [
        ['<granted_content_1>'],
        ['<granted_content_2>'],
    ],
    '<granted_open_paren_ext>': [
        ['identifier', '<id_ext>', '<idlit3_granted_ext>'],
        ['<lit3>', '<idlit3_granted_ext>'],
        ['scroll_lit', '<expression_ext_2>', '<more_log>', ')'],
        ['rose_lit', '<expression_ext_2>', '<more_log>', ')'],
        ['mirror_lit', '<expression_ext_2>', '<more_log>', ')'],
        ['<treasures_mirror>', '<expression_ext_2>', '<more_log>', ')'],
        ['(', '<logical_operator1>', '<granted_open_paren_ext>', ')', '<close_paren_ext>'],
    ],
    '<idlit3_granted_ext>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')', '<more_log>'],
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', ')', '<more_arith>', '<open_paren_other_ext>'],
    ],
    '<open_paren_other_ext>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
        ['ε'],
    ],
    '<close_paren_ext>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<open_paren_other_ext>'],
        ['ε'],
    ],
    '<granted_id_ext>': [
        ['<unary_operator>'],
        ['<func_call>', '<granted_other_id_ext>'],
        ['[', '<array_size>', ']', '<column1>', '<granted_other_id_ext>'],
        ['<granted_other_id_ext>'],
        ['ε'],
    ],
    '<granted_other_id_ext>': [
        ['+', '<plus_ext>'],
        ['-', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['*', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['/', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['%', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
        ['ε'],
    ],
    '<granted_other_id_ext2>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['ε'],
    ],
    '<plus_ext>': [
        ['identifier', '<id_ext>', '<plus_ext_1>'],
        ['toscroll', '(', '<conversion_value>', ')','<string_more>'],
        ['scroll_lit', '<string_more>'],
        ['rose_lit', '<string_more>'],
        ['(', '<arithmetic_exp>', ')', '<more_arith>', '<granted_other_id_ext2>'],
        ['treasures_lit', '<more_arith>', '<granted_other_id_ext2>'],
        ['1', '<more_arith>', '<granted_other_id_ext2>'],
        ['0', '<more_arith>', '<granted_other_id_ext2>'],
        ['ocean_lit', '<more_arith>', '<granted_other_id_ext2>'],
    ],
    '<plus_ext_1>': [
        ['+', '<plus_ext>'],
        ['-', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['*', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['/', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['%', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['ε'],
    ],
    '<granted_scroll_ext>': [
        ['+', '<string_operand>', '<string_more>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['ε'],
    ],
    '<granted_rose_ext>': [
        ['+', '<string_operand>', '<string_more>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['ε'],
    ],
    '<granted_lit3_ext>': [
        ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<granted_lit3_ext1>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['ε'],
    ],
    '<granted_lit3_ext1>': [
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['ε'],
    ],
    '<more_granted>': [
        [',', '<granted_content>', '<more_granted>'],
        ['ε'],
    ],
    '<data_type>': [
        ['scroll'],
        ['treasures'],
        ['mirror'],
        ['ocean'],
        ['rose'],
    ],
    '<val>': [
        ['<granted_content_2>'],
        ['identifier', '<granted_id_ext>'],
        ['<input>'],
    ],
    '<val1>': [
        ['<granted_content_2>'],
        ['identifier', '<val1_ext>'],
    ],
    '<val1_ext>': [
        ['<val1_id_ext>'],
        ['<func_call>', '<val1_id_ext>'],
        ['[', '<array_size>', ']', '<column1>', '<val1_id_ext>'],
        ['<unary_operator>'],
        ['+', '<plus_ext>'],
        ['-', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['*', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['/', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['%', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
        ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
        ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ],
    '<val1_id_ext>': [
        ['<assignment_operator>', '<assignment_operand>'],
        ['ε'],
    ],
    '<conversion_func>': [
        ['torose'],
        ['totreasures'],
        ['toocean'],
        ['tomirror'],
    ],
    '<conversion_value>': [
        ['<lit4>'],
        ['identifier', '<id_ext>'],
    ],
    '<index>': [
        ['[', '<array_size>', ']', '<column1>'],
        ['ε'],
    ],
    '<column1>': [
        ['[', '<array_size>', ']'],
        ['ε'],
    ],
    '<input>': [
        ['wish', '(', 'scroll_lit', ')'],
    ],
    '<lit1>': [
        ['scroll_lit'],
        ['rose_lit'],
    ],
    '<lit2>': [
        ['mirror_lit'],
    ],
    '<lit3>': [
        ['ocean_lit'],
        ['treasures_lit'],
        ['1'],
        ['0']
    ],
    '<lit4>': [
        ['<lit1>'],
        ['<lit2>'],
        ['<lit3>'],
    ],
    '<func_call>': [
        ['(', '<args>', ')'],
    ],
    '<args>': [
        ['<args_val>', '<args_more>'],
        ['ε'],
    ],
    '<args_val>': [
        ['identifier', '<id_ext>'],
        ['<lit4>'],
    ],
    '<args_more>': [
        [',', '<args_val>', '<args_more>'],
        ['ε'],
    ],
    '<id_ext>': [
        ['<func_call>'],
        ['[', '<array_size>', ']', '<column1>'],
        ['ε'],
    ],
    '<array_size>': [
        ['identifier'],
        ['treasures_lit'],
        ['1'],
        ['0']
    ],
}
    PREDICT = {
    # <program> 
    ('<program>', 'crown'): ['crown', '~', '<global_dec>', '<user-defined_func>', 'castle', 'treasures', 'identifier', '(', ')', '{', '<body>', 'return', '0', '~', '}', 'reign', '~'],
    # <global_dec> 
    ('<global_dec>', 'ocean'): ['<var_dec>', '<global_dec>'],
    ('<global_dec>', 'treasures'): ['<var_dec>', '<global_dec>'],
    ('<global_dec>', 'scroll'): ['<var_dec>', '<global_dec>'],
    ('<global_dec>', 'rose'): ['<var_dec>', '<global_dec>'],
    ('<global_dec>', 'dynasty'): ['<var_dec>', '<global_dec>'],
    ('<global_dec>', 'mirror'): ['<var_dec>', '<global_dec>'],
    ('<global_dec>', 'spell'): ['ε'],
    ('<global_dec>', 'castle'): ['ε'],
    # <var_dec>
    ('<var_dec>', 'ocean'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>'],
    ('<var_dec>', 'treasures'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>'],
    ('<var_dec>', 'scroll'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>'],
    ('<var_dec>', 'rose'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>'],
    ('<var_dec>', 'dynasty'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>'],
    ('<var_dec>', 'mirror'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>'],
    # <dynasty>
    ('<dynasty>', 'dynasty'): ['dynasty'],
    ('<dynasty>', 'ocean'): ['ε'],
    ('<dynasty>', 'treasures'): ['ε'],
    ('<dynasty>', 'scroll'): ['ε'],
    ('<dynasty>', 'rose'): ['ε'],
    ('<dynasty>', 'mirror'): ['ε'],
    # <vardec_def>
    ('<vardec_def>', '='): ['<initialization>', '<vardec_more>', '~'],
    ('<vardec_def>', '~'): ['<initialization>', '<vardec_more>', '~'],
    ('<vardec_def>', '['): ['[', '<array_size>', ']', '<column>', '<array_initialization>', '<array_more>', '~'],
    # <initialization>
    ('<initialization>', '='): ['=', '<val>'],
    ('<initialization>', '~'): ['ε'],
    ('<initialization>', ','): ['ε'],
    # <vardec_more>
    ('<vardec_more>', ','): [',', 'identifier', '<initialization>', '<vardec_more>'],
    ('<vardec_more>', '~'): ['ε'],
    # <column>
    ('<column>', '['): ['[', '<array_size>', ']'],
    ('<column>', '='): ['ε'],
    ('<column>', '~'): ['ε'],
    ('<column>', ','): ['ε'],
    # <array_initialization>
    ('<array_initialization>', '='): ['=', '<array_list>'],
    ('<array_initialization>', '~'): ['ε'],
    ('<array_initialization>', ','): ['ε'],
    # <array_list>
    ('<array_list>', '{'): ['{', '<array_content>', '}'],
    # <array_content>
    ('<array_content>', 'mirror_lit'): ['<array_lit>', '<lit_more>'],
    ('<array_content>', 'rose_lit'): ['<array_lit>', '<lit_more>'],
    ('<array_content>', 'scroll_lit'): ['<array_lit>', '<lit_more>'],
    ('<array_content>', 'treasures_lit'): ['<array_lit>', '<lit_more>'],
    ('<array_content>', '1'): ['<array_lit>', '<lit_more>'],
    ('<array_content>', '0'): ['<array_lit>', '<lit_more>'],
    ('<array_content>', 'identifier'): ['<array_lit>', '<lit_more>'],
    ('<array_content>', 'ocean_lit'): ['<array_lit>', '<lit_more>'],
    ('<array_content>', '{'): ['{', '<array_row>', '}', '<row_more>'],
    # <array_row>
    ('<array_row>', 'mirror_lit'): ['<array_lit>', '<lit_more>'],
    ('<array_row>', 'rose_lit'): ['<array_lit>', '<lit_more>'],
    ('<array_row>', 'scroll_lit'): ['<array_lit>', '<lit_more>'],
    ('<array_row>', 'treasures_lit'): ['<array_lit>', '<lit_more>'],
    ('<array_row>', '1'): ['<array_lit>', '<lit_more>'],
    ('<array_row>', '0'): ['<array_lit>', '<lit_more>'],
    ('<array_row>', 'identifier'): ['<array_lit>', '<lit_more>'],
    ('<array_row>', 'ocean_lit'): ['<array_lit>', '<lit_more>'],
    # <row_more>
    ('<row_more>', ','): [',', '<row_more_ext>'],
    ('<row_more>', '}'): ['ε'],
    # <row_more_ext>
    ('<row_more_ext>', '{'): ['{', '<array_row>', '}', '<row_more>'],
    ('<row_more_ext>', 'identifier'): ['identifier', '<row_more>'],
    # <lit_more>
    ('<lit_more>', ','): [',', '<lit_more_ext>'],
    ('<lit_more>', '}'): ['ε'],
    # <lit_more_ext>
    ('<lit_more_ext>', 'mirror_lit'): ['<array_lit>', '<lit_more>'],
    ('<lit_more_ext>', 'rose_lit'): ['<array_lit>', '<lit_more>'],
    ('<lit_more_ext>', 'scroll_lit'): ['<array_lit>', '<lit_more>'],
    ('<lit_more_ext>', 'treasures_lit'): ['<array_lit>', '<lit_more>'],
    ('<lit_more_ext>', '1'): ['<array_lit>', '<lit_more>'],
    ('<lit_more_ext>', '0'): ['<array_lit>', '<lit_more>'],
    ('<lit_more_ext>', 'identifier'): ['<array_lit>', '<lit_more>'],
    ('<lit_more_ext>', 'ocean_lit'): ['<array_lit>', '<lit_more>'],
    ('<lit_more_ext>', '{'): ['{', '<array_row>', '}', '<row_more>'],
    # <array_more>
    ('<array_more>', ','): [',', 'identifier', '[', '<array_size>', ']', '<column>', '<array_initialization>', '<array_more>'],
    ('<array_more>', '~'): ['ε'],
    # <array_lit>
    ('<array_lit>', 'mirror_lit'): ['<lit4>'],
    ('<array_lit>', 'rose_lit'): ['<lit4>'],
    ('<array_lit>', 'scroll_lit'): ['<lit4>'],
    ('<array_lit>', 'treasures_lit'): ['<lit4>'],
    ('<array_lit>', '1'): ['<lit4>'],
    ('<array_lit>', '0'): ['<lit4>'],
    ('<array_lit>', 'ocean_lit'): ['<lit4>'],
    ('<array_lit>', 'identifier'): ['identifier'],
    # <assignment_operator>
    ('<assignment_operator>', '+='): ['+='],
    ('<assignment_operator>', '-='): ['-='],
    ('<assignment_operator>', '*='): ['*='],
    ('<assignment_operator>', '/='): ['/='],
    ('<assignment_operator>', '%='): ['%='],
    # <assignment_operand>
    ('<assignment_operand>', 'identifier'): ['identifier', '<id_ext>', '<more_arith>'],
    ('<assignment_operand>', 'ocean_lit'): ['<lit3>', '<more_arith>'],
    ('<assignment_operand>', 'treasures_lit'): ['<lit3>', '<more_arith>'],
    ('<assignment_operand>', '1'): ['<lit3>', '<more_arith>'],
    ('<assignment_operand>', '0'): ['<lit3>', '<more_arith>'],
    ('<assignment_operand>', '('): ['<arithmetic_operand_2>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    # <logical_exp>
    ('<logical_exp>', 'mirror_lit'): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],    
    ('<logical_exp>', '0'): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<logical_exp>', 'rose_lit'): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],      
    ('<logical_exp>', '!'): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<logical_exp>', 'scroll_lit'): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],    
    ('<logical_exp>', '('): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<logical_exp>', 'treasures_lit'): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'], 
    ('<logical_exp>', 'identifier'): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],        
    ('<logical_exp>', '1'): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<logical_exp>', 'ocean_lit'): ['<logical_operator1>', '<logical_operand>', '<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],     
    # <logical_operand>
    ('<logical_operand>', 'identifier'): ['identifier', '<id_ext>', '<logical_operand_ext>'],
    ('<logical_operand>', 'ocean_lit'): ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand>', 'treasures_lit'): ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand>', 'scroll_lit'): ['scroll_lit', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand>', 'rose_lit'): ['rose_lit', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand>', 'mirror_lit'): ['mirror_lit', '<relational_more>'],
    ('<logical_operand>', '1'): ['<treasures_mirror>', '<relational_more>'],
    ('<logical_operand>', '0'): ['<treasures_mirror>', '<relational_more>'],
    ('<logical_operand>', '('): ['(', '<logical_operator1>', '<expression>'],
    # <expression>
    ('<expression>', 'identifier'): ['identifier', '<id_ext>', '<expression_ext_1>'],
    ('<expression>', 'ocean_lit'): ['<lit3>', '<expression_ext_1>'],
    ('<expression>', 'treasures_lit'): ['<lit3>', '<expression_ext_1>'],
    ('<expression>', 'scroll_lit'): ['scroll_lit', '<expression_ext_2>'],
    ('<expression>', 'rose_lit'): ['rose_lit', '<expression_ext_2>'],
    ('<expression>', 'mirror_lit'): ['mirror_lit', '<expression_ext_2>'],
    ('<expression>', '1'): ['<treasures_mirror>', '<expression_ext_2>'],
    ('<expression>', '0'): ['<treasures_mirror>', '<expression_ext_2>'],
    ('<expression>', '('): ['(', '<logical_operator1>', '<expression>', '<more_log>', ')', '<logical_operand_ext>'],
    # <expression_ext_1>
    ('<expression_ext_1>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_1>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>','<more_log>', ')', '<relational_more>'],
    ('<expression_ext_1>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_1>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_1>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_1>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_1>', '||'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')'],
    ('<expression_ext_1>', '&&'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')'],
    ('<expression_ext_1>', '/'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', '<more_log>',')', '<more_arith>', '<relational_more>'],    
    ('<expression_ext_1>', '*'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', '<more_log>',')', '<more_arith>', '<relational_more>'],    
    ('<expression_ext_1>', '-'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', '<more_log>',')', '<more_arith>', '<relational_more>'],    
    ('<expression_ext_1>', '%'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', '<more_log>',')', '<more_arith>', '<relational_more>'],    
    ('<expression_ext_1>', '+'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', '<more_log>',')', '<more_arith>', '<relational_more>'],    
    # <expression_ext_2>
    ('<expression_ext_2>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>','<more_log>', ')', '<relational_more>'],
    ('<expression_ext_2>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_2>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_2>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_2>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_2>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>',')', '<relational_more>'],
    ('<expression_ext_2>', '||'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')'],
    ('<expression_ext_2>', '&&'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')'],
    # <logical_operand_ext>
    ('<logical_operand_ext>', '>'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '/'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '*'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '!='): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '=='): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '>='): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '-'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '+'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '%'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '<='): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '<'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<logical_operand_ext>', '&&'): ['ε'],
    ('<logical_operand_ext>', '||'): ['ε'],
    ('<logical_operand_ext>', '~'): ['ε'],
    ('<logical_operand_ext>', ')'): ['ε'],
    ('<logical_operand_ext>', ','): ['ε'],
    # <logical_operator>
    ('<logical_operator>', '&&'): ['&&'],
    ('<logical_operator>', '||'): ['||'],
    # <logical_operator1>
    ('<logical_operator1>', '!'): ['!'],
    ('<logical_operator1>', 'mirror_lit'): ['ε'],
    ('<logical_operator1>', '0'): ['ε'],
    ('<logical_operator1>', 'rose_lit'): ['ε'],
    ('<logical_operator1>', 'scroll_lit'): ['ε'],
    ('<logical_operator1>', '('): ['ε'],
    ('<logical_operator1>', 'treasures_lit'): ['ε'],
    ('<logical_operator1>', 'identifier'): ['ε'],
    ('<logical_operator1>', '1'): ['ε'],
    ('<logical_operator1>', 'ocean_lit'): ['ε'],
    # <more_log>
    ('<more_log>', '||'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<more_log>', '&&'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<more_log>', ')'): ['ε'],
    ('<more_log>', ','): ['ε'],
    ('<more_log>', '~'): ['ε'],
    # <treasures_mirror>
    ('<treasures_mirror>', '1'): ['1'],
    ('<treasures_mirror>', '0'): ['0'],
    # <arithmetic_exp>
    ('<arithmetic_exp>', '('): ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<arithmetic_exp>', 'ocean_lit'): ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<arithmetic_exp>', 'treasures_lit'): ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<arithmetic_exp>', '1'): ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<arithmetic_exp>', '0'): ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<arithmetic_exp>', 'identifier'): ['<arithmetic_operand>', '<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    # <arithmetic_operand_1>
    ('<arithmetic_operand_1>', 'identifier'): ['identifier', '<id_ext>'],
    ('<arithmetic_operand_1>', 'ocean_lit'): ['<lit3>'],
    ('<arithmetic_operand_1>', 'treasures_lit'): ['<lit3>'],
    ('<arithmetic_operand_1>', '1'): ['<lit3>'],
    ('<arithmetic_operand_1>', '0'): ['<lit3>'],
    # <arithmetic_operand_2>
    ('<arithmetic_operand_2>', '('): ['(', '<arithmetic_exp>', ')'],
    # <arithmetic_operand>
    ('<arithmetic_operand>', 'ocean_lit'): ['<arithmetic_operand_1>'],
    ('<arithmetic_operand>', 'treasures_lit'): ['<arithmetic_operand_1>'],
    ('<arithmetic_operand>', '1'): ['<arithmetic_operand_1>'],
    ('<arithmetic_operand>', '0'): ['<arithmetic_operand_1>'],
    ('<arithmetic_operand>', 'identifier'): ['<arithmetic_operand_1>'],
    ('<arithmetic_operand>', '('): ['<arithmetic_operand_2>'],
    # <arithmetic_operator>
    ('<arithmetic_operator>', '+'): ['+'],
    ('<arithmetic_operator>', '-'): ['-'],
    ('<arithmetic_operator>', '/'): ['/'],
    ('<arithmetic_operator>', '*'): ['*'],
    ('<arithmetic_operator>', '%'): ['%'],
    # <more_arith>
    ('<more_arith>', '/'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<more_arith>', '*'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<more_arith>', '-'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<more_arith>', '%'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<more_arith>', '+'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>'],
    ('<more_arith>', '>'): ['ε'],
    ('<more_arith>', '&&'): ['ε'],
    ('<more_arith>', '!='): ['ε'],
    ('<more_arith>', '||'): ['ε'],
    ('<more_arith>', '=='): ['ε'],
    ('<more_arith>', '>='): ['ε'],
    ('<more_arith>', '<='): ['ε'],
    ('<more_arith>', '~'): ['ε'],
    ('<more_arith>', '<'): ['ε'],
    ('<more_arith>', ')'): ['ε'],
    ('<more_arith>', ','): ['ε'],
    # <relational_exp>
    ('<relational_exp>', 'mirror_lit'): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_exp>', 'rose_lit'): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_exp>', 'scroll_lit'): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_exp>', 'treasures_mirror'): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_exp>', '('): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_exp>', 'treasures_lit'): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_exp>', '1'): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_exp>', '0'): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_exp>', 'identifier'): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_exp>', 'ocean_lit'): ['<relational_operand>', '<relational_operator>', '<relational_operand>', '<relational_more>'],
    # <relational_operand>
    ('<relational_operand>', 'identifier'): ['identifier', '<id_ext>', '<more_arith>'],
    ('<relational_operand>', 'ocean_lit'): ['<lit3>', '<more_arith>'],
    ('<relational_operand>', 'treasures_lit'): ['<lit3>', '<more_arith>'],
    ('<relational_operand>', '1'): ['<lit3>', '<more_arith>'],
    ('<relational_operand>', '0'): ['<lit3>', '<more_arith>'],
    ('<relational_operand>', 'scroll_lit'): ['scroll_lit'],
    ('<relational_operand>', 'rose_lit'): ['rose_lit'],
    ('<relational_operand>', 'mirror_lit'): ['mirror_lit'],
    ('<relational_operand>', 'treasures_mirror'): ['treasures_mirror'],
    ('<relational_operand>', '('): ['(', '<expression_2>'],
    # <expression_2>
    ('<expression_2>', 'identifier'): ['identifier', '<id_ext>', '<expression_2_ext>'],
    ('<expression_2>', 'ocean_lit'): ['<lit3>', '<expression_2_ext>'],
    ('<expression_2>', 'treasures_lit'): ['<lit3>', '<expression_2_ext>'],
    ('<expression_2>', '1'): ['<lit3>', '<expression_2_ext>'],
    ('<expression_2>', '0'): ['<lit3>', '<expression_2_ext>'],
    ('<expression_2>', 'scroll_lit'): ['scroll_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ('<expression_2>', 'rose_lit'): ['rose_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ('<expression_2>', 'mirror_lit'): ['mirror_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ('<expression_2>', 'treasures_mirror'): ['treasures_mirror', '<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ('<expression_2>', '('): ['(', '<expression_2>', ')'],
    # <expression_2_ext>
    ('<expression_2_ext>', '/'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', ')', '<more_arith>'],
    ('<expression_2_ext>', '*'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', ')', '<more_arith>'],
    ('<expression_2_ext>', '-'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', ')', '<more_arith>'],
    ('<expression_2_ext>', '%'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', ')', '<more_arith>'],
    ('<expression_2_ext>', '+'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', ')', '<more_arith>'],
    ('<expression_2_ext>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ('<expression_2_ext>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ('<expression_2_ext>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ('<expression_2_ext>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ('<expression_2_ext>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    ('<expression_2_ext>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', ')'],
    # <relational_operator>
    ('<relational_operator>', '<'): ['<'],
    ('<relational_operator>', '>'): ['>'],
    ('<relational_operator>', '<='): ['<='],
    ('<relational_operator>', '>='): ['>='],
    ('<relational_operator>', '=='): ['=='],
    ('<relational_operator>', '!='): ['!='],
    # <relational_more>
    ('<relational_more>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_more>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_more>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_more>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_more>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_more>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>'],
    ('<relational_more>', '&&'): ['ε'],
    ('<relational_more>', '||'): ['ε'],
    ('<relational_more>', '~'): ['ε'],
    ('<relational_more>', ')'): ['ε'],
    ('<relational_more>', ','): ['ε'],
    # <unary>
    ('<unary>', 'identifier'): ['identifier', '<unary_operator>'],
    # <unary_operator>
    ('<unary_operator>', '++'): ['++'],
    ('<unary_operator>', '--'): ['--'],
    # <string_operand>
    ('<string_operand>', 'scroll_lit'): ['<lit1>'],
    ('<string_operand>', 'rose_lit'): ['<lit1>'],
    ('<string_operand>', 'identifier'): ['identifier', '<id_ext>'],
    ('<string_operand>', 'toscroll'): ['toscroll', '(', '<conversion_value>', ')'],
    # <string_more>
    ('<string_more>', '+'): ['+', '<string_operand>', '<string_more>'],
    ('<string_more>', ')'): ['ε'],
    ('<string_more>', '~'): ['ε'],
    ('<string_more>', ','): ['ε'],
    # <user-defined_func>
    ('<user-defined_func>', 'spell'): ['spell', '<return_type>', 'identifier', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<user-defined_func>'],        
    ('<user-defined_func>', 'castle'): ['ε'],
    # <return_type>
    ('<return_type>', 'ocean'): ['<data_type>'],
    ('<return_type>', 'treasures'): ['<data_type>'],
    ('<return_type>', 'scroll'): ['<data_type>'],
    ('<return_type>', 'rose'): ['<data_type>'],
    ('<return_type>', 'mirror'): ['<data_type>'],
    ('<return_type>', 'chamber'): ['chamber'],
    # <param>
    ('<param>', 'ocean'): ['<data_type>', 'identifier', '<param_more>'],
    ('<param>', 'treasures'): ['<data_type>', 'identifier', '<param_more>'],
    ('<param>', 'scroll'): ['<data_type>', 'identifier', '<param_more>'],
    ('<param>', 'rose'): ['<data_type>', 'identifier', '<param_more>'],
    ('<param>', 'mirror'): ['<data_type>', 'identifier', '<param_more>'],
    ('<param>', ')'): ['ε'],
    # <param_more>
    ('<param_more>', ','): [',', '<data_type>', 'identifier', '<param_more>'],
    ('<param_more>', ')'): ['ε'],
    # <body>
    ('<body>', 'ocean'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<body>'],
    ('<body>', 'treasures'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<body>'],
    ('<body>', 'scroll'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<body>'],
    ('<body>', 'rose'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<body>'],
    ('<body>', 'dynasty'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<body>'],
    ('<body>', 'mirror'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<body>'],
    ('<body>', 'granted'): ['granted', '(', '<granted_content>', '<more_granted>', ')', '~', '<body>'],
    ('<body>', 'identifier'): ['identifier', '<body_1_ext>', '<body>'],
    ('<body>', 'spell'): ['spell', '<return_type>', 'identifier', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<body>'],
    ('<body>', 'tale'): ['tale', '(', '<loop_var>', '~', '<relational_exp>', '~', '<unary>', ')', '{', '<loop_body>', '}', '<body>'],
    ('<body>', 'cast'): ['cast', '(', '<condition>', ')', '{', '<body>', '}', '<elif>', '<else>', '<body>'],
    ('<body>', 'forever'): ['forever', '(', '<condition>', ')', '{', '<loop_body>', '}', '<body>'],
    ('<body>', 'believe'): ['believe', '{', '<loop_body>', '}', 'forever', '(', '<condition>', ')', '~', '<body>'],
    ('<body>', 'break'): ['ε'],
    ('<body>', 'continue'): ['ε'],
    ('<body>', 'return'): ['ε'],
    ('<body>', '}'): ['ε'],
    # <body_1_ext>
    ('<body_1_ext>', '('): ['(', '<args>', ')', '~'],
    ('<body_1_ext>', '-='): ['<index>', '<body_1_other_ext>'],
    ('<body_1_ext>', '='): ['<index>', '<body_1_other_ext>'],
    ('<body_1_ext>', '['): ['<index>', '<body_1_other_ext>'],
    ('<body_1_ext>', '%='): ['<index>', '<body_1_other_ext>'],
    ('<body_1_ext>', '*='): ['<index>', '<body_1_other_ext>'],
    ('<body_1_ext>', '/='): ['<index>', '<body_1_other_ext>'],
    ('<body_1_ext>', '+='): ['<index>', '<body_1_other_ext>'],
    ('<body_1_ext>', '--'): ['<unary_operator>', '~'],
    ('<body_1_ext>', '++'): ['<unary_operator>', '~'],
    # <body_1_other_ext>
    ('<body_1_other_ext>', '='): ['=', '<val>', '~'],
    ('<body_1_other_ext>', '-='): ['<assignment_operator>', '<assignment_operand>', '~'],
    ('<body_1_other_ext>', '%='): ['<assignment_operator>', '<assignment_operand>', '~'],
    ('<body_1_other_ext>', '*='): ['<assignment_operator>', '<assignment_operand>', '~'],
    ('<body_1_other_ext>', '/='): ['<assignment_operator>', '<assignment_operand>', '~'],
    ('<body_1_other_ext>', '+='): ['<assignment_operator>', '<assignment_operand>', '~'],
    # <ret_statement>
    ('<ret_statement>', 'return'): ['return', '<val1>', '~'],
    ('<ret_statement>', '}'): ['ε'],
    # <loop_var>
    ('<loop_var>', 'treasures'): ['treasures', 'identifier', '=', '<loop_val>'],
    ('<loop_var>', 'identifier'): ['identifier', '<loop_init>'],
    # <loop_init>
    ('<loop_init>', '='): ['=', '<loop_val>'],
    ('<loop_init>', '~'): ['ε'],
    # <loop_val>
    ('<loop_val>', 'identifier'): ['identifier'],
    ('<loop_val>', 'treasures_lit'): ['treasures_lit'],
    ('<loop_val>', '1'): ['1'],
    ('<loop_val>', '0'): ['0'],
    # <loop_body>
    ('<loop_body>', 'ocean'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<loop_body>'],
    ('<loop_body>', 'treasures'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<loop_body>'],
    ('<loop_body>', 'scroll'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<loop_body>'],
    ('<loop_body>', 'rose'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<loop_body>'],
    ('<loop_body>', 'dynasty'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<loop_body>'],
    ('<loop_body>', 'mirror'): ['<dynasty>', '<data_type>', 'identifier', '<vardec_def>', '<loop_body>'],
    ('<loop_body>', 'granted'): ['granted', '(', '<granted_content>', '<more_granted>', ')', '~', '<loop_body>'],
    ('<loop_body>', 'identifier'): ['identifier', '<body_1_ext>', '<loop_body>'],
    ('<loop_body>', 'spell'): ['spell', '<return_type>', 'identifier', '(', '<param>', ')', '{', '<body>', '<ret_statement>', '}', '<loop_body>'],
    ('<loop_body>', 'tale'): ['tale', '(', '<loop_var>', '~', '<relational_exp>', '~', '<unary>', ')', '{', '<loop_body>', '}', '<loop_body>'],
    ('<loop_body>', 'cast'): ['cast', '(', '<condition>', ')', '{', '<loop_body>', '<flow_control>', '}', '<elif_break>', '<else_break>', '<loop_body>'],
    ('<loop_body>', 'forever'): ['forever', '(', '<condition>', ')', '{', '<loop_body>', '}', '<loop_body>'],
    ('<loop_body>', 'believe'): ['believe', '{', '<loop_body>', '}', 'forever', '(', '<condition>', ')', '~', '<loop_body>'],
    ('<loop_body>', 'break'): ['ε'],
    ('<loop_body>', 'continue'): ['ε'],
    ('<loop_body>', '}'): ['ε'],
    # <elif_break>
    ('<elif_break>', 'twist'): ['twist', '(', '<condition>', ')', '{', '<body>', '<flow_control>', '}', '<elif_break>'],
    ('<elif_break>', 'tale'): ['ε'],
    ('<elif_break>', 'treasures'): ['ε'],
    ('<elif_break>', 'granted'): ['ε'],
    ('<elif_break>', 'rose'): ['ε'],
    ('<elif_break>', 'forever'): ['ε'],
    ('<elif_break>', 'believe'): ['ε'],
    ('<elif_break>', 'spell'): ['ε'],
    ('<elif_break>', 'ocean'): ['ε'],
    ('<elif_break>', '}'): ['ε'],
    ('<elif_break>', 'scroll'): ['ε'],
    ('<elif_break>', 'cast'): ['ε'],
    ('<elif_break>', 'dynasty'): ['ε'],
    ('<elif_break>', 'continue'): ['ε'],
    ('<elif_break>', 'identifier'): ['ε'],
    ('<elif_break>', 'curse'): ['ε'],
    ('<elif_break>', 'break'): ['ε'],
    ('<elif_break>', 'mirror'): ['ε'],
    # <else_break>
    ('<else_break>', 'curse'): ['curse', '{', '<body>', '<flow_control>', '}'],
    ('<else_break>', 'tale'): ['ε'],
    ('<else_break>', 'treasures'): ['ε'],
    ('<else_break>', 'granted'): ['ε'],
    ('<else_break>', 'rose'): ['ε'],
    ('<else_break>', 'forever'): ['ε'],
    ('<else_break>', 'believe'): ['ε'],
    ('<else_break>', 'spell'): ['ε'],
    ('<else_break>', 'ocean'): ['ε'],
    ('<else_break>', '}'): ['ε'],
    ('<else_break>', 'cast'): ['ε'],
    ('<else_break>', 'scroll'): ['ε'],
    ('<else_break>', 'dynasty'): ['ε'],
    ('<else_break>', 'continue'): ['ε'],
    ('<else_break>', 'identifier'): ['ε'],
    ('<else_break>', 'break'): ['ε'],
    ('<else_break>', 'mirror'): ['ε'],
    # <flow_control>
    ('<flow_control>', 'break'): ['break', '~'],
    ('<flow_control>', 'continue'): ['continue', '~'],
    ('<flow_control>', '}'): ['ε'],
    # <condition>
    ('<condition>', '1'): ['<treasures_mirror>', '<more_log>'],
    ('<condition>', '0'): ['<treasures_mirror>', '<more_log>'],
    ('<condition>', 'identifier'): ['identifier', '<condi_id_ext>'],
    ('<condition>', '!'): ['!', '<logical_operand>', '<more_log>'],
    ('<condition>', 'mirror_lit'): ['mirror_lit', '<relational_more>', '<more_log>'],
    ('<condition>', 'ocean_lit'): ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<condition>', 'treasures_lit'): ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<condition>', '1'): ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<condition>', '0'): ['<lit3>', '<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<condition>', 'scroll_lit'): ['scroll_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<condition>', 'rose_lit'): ['rose_lit', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<condition>', '('): ['(', '<logical_operator1>', '<expression>', '<more_log>'],
    # <condi_id_ext>
    ('<condi_id_ext>', '('): ['<func_call>', '<other_id_ext>'],
    ('<condi_id_ext>', '['): ['[', '<array_size>', ']', '<column1>', '<other_id_ext>'],
    ('<condi_id_ext>', '>'): ['<other_id_ext>'],
    ('<condi_id_ext>', '<'): ['<other_id_ext>'],
    ('<condi_id_ext>', '/'): ['<other_id_ext>'],
    ('<condi_id_ext>', '*'): ['<other_id_ext>'],
    ('<condi_id_ext>', '=='): ['<other_id_ext>'],
    ('<condi_id_ext>', '>='): ['<other_id_ext>'],
    ('<condi_id_ext>', '-'): ['<other_id_ext>'],
    ('<condi_id_ext>', '%'): ['<other_id_ext>'],
    ('<condi_id_ext>', '+'): ['<other_id_ext>'],
    ('<condi_id_ext>', '<='): ['<other_id_ext>'],
    ('<condi_id_ext>', '!='): ['<other_id_ext>'],
    ('<condi_id_ext>', ')'): ['<other_id_ext>'],
    # <other_id_ext>
    ('<other_id_ext>', '>'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '/'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '*'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '!='): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '=='): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '>='): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '-'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '+'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '%'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '<='): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', '<'): ['<more_arith>', '<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<other_id_ext>', ')'): ['ε'],
    # <elif>
    ('<elif>', 'twist'): ['twist', '(', '<condition>', ')', '{', '<body>', '}', '<elif>'],
    ('<elif>', 'tale'): ['ε'],
    ('<elif>', 'treasures'): ['ε'],
    ('<elif>', 'granted'): ['ε'],
    ('<elif>', 'rose'): ['ε'],
    ('<elif>', 'forever'): ['ε'],
    ('<elif>', 'believe'): ['ε'],
    ('<elif>', 'spell'): ['ε'],
    ('<elif>', 'ocean'): ['ε'],
    ('<elif>', '}'): ['ε'],
    ('<elif>', 'scroll'): ['ε'],
    ('<elif>', 'cast'): ['ε'],
    ('<elif>', 'dynasty'): ['ε'],
    ('<elif>', 'continue'): ['ε'],
    ('<elif>', 'identifier'): ['ε'],
    ('<elif>', 'curse'): ['ε'],
    ('<elif>', 'return'): ['ε'],
    ('<elif>', 'break'): ['ε'],
    ('<elif>', 'mirror'): ['ε'],
    # <else>
    ('<else>', 'curse'): ['curse', '{', '<body>', '}'],
    ('<else>', 'tale'): ['ε'],
    ('<else>', 'treasures'): ['ε'],
    ('<else>', 'granted'): ['ε'],
    ('<else>', 'rose'): ['ε'],
    ('<else>', 'forever'): ['ε'],
    ('<else>', 'believe'): ['ε'],
    ('<else>', 'spell'): ['ε'],
    ('<else>', 'ocean'): ['ε'],
    ('<else>', '}'): ['ε'],
    ('<else>', 'cast'): ['ε'],
    ('<else>', 'scroll'): ['ε'],
    ('<else>', 'dynasty'): ['ε'],
    ('<else>', 'continue'): ['ε'],
    ('<else>', 'identifier'): ['ε'],
    ('<else>', 'return'): ['ε'],
    ('<else>', 'break'): ['ε'],
    ('<else>', 'mirror'): ['ε'],
    # <granted_content_1>
    ('<granted_content_1>', 'set_precision'): ['set_precision'],
    ('<granted_content_1>', 'identifier'): ['identifier', '<granted_id_ext>'],
    # <granted_content_2>
    ('<granted_content_2>', 'phantom'): ['phantom'],
    ('<granted_content_2>', 'lengthof'): ['lengthof', '(', 'identifier', '<index>', ')'],
    ('<granted_content_2>', 'torose'): ['<conversion_func>', '(', '<conversion_value>', ')'],
    ('<granted_content_2>', 'totreasures'): ['<conversion_func>', '(', '<conversion_value>', ')'],
    ('<granted_content_2>', 'toocean'): ['<conversion_func>', '(', '<conversion_value>', ')'],
    ('<granted_content_2>', 'tomirror'): ['<conversion_func>', '(', '<conversion_value>', ')'],
    ('<granted_content_2>', 'toscroll'): ['toscroll', '(', '<conversion_value>', ')', '<string_more>'],
    ('<granted_content_2>', '1'): ['<treasures_mirror>', '<more_log>'],
    ('<granted_content_2>', '0'): ['<treasures_mirror>', '<more_log>'],
    ('<granted_content_2>', 'mirror_lit'): ['mirror_lit', '<relational_more>', '<more_log>'],
    ('<granted_content_2>', 'scroll_lit'): ['scroll_lit', '<granted_scroll_ext>'],
    ('<granted_content_2>', 'rose_lit'): ['rose_lit', '<granted_rose_ext>'],
    ('<granted_content_2>', 'ocean_lit'): ['<lit3>', '<granted_lit3_ext>'],
    ('<granted_content_2>', 'treasures_lit'): ['<lit3>', '<granted_lit3_ext>'],
    ('<granted_content_2>', '('): ['(', '<logical_operator1>', '<granted_open_paren_ext>'],
    ('<granted_content_2>', '!'): ['!', '<logical_operand>', '<more_log>'],
    # <granted_content>
    ('<granted_content>', 'set_precision'): ['<granted_content_1>'],
    ('<granted_content>', 'identifier'): ['<granted_content_1>'],
    ('<granted_content>', 'mirror_lit'): ['<granted_content_2>'],
    ('<granted_content>', 'toscroll'): ['<granted_content_2>'],
    ('<granted_content>', '0'): ['<granted_content_2>'],
    ('<granted_content>', 'rose_lit'): ['<granted_content_2>'],
    ('<granted_content>', 'torose'): ['<granted_content_2>'],
    ('<granted_content>', 'totreasures'): ['<granted_content_2>'],
    ('<granted_content>', 'lengthof'): ['<granted_content_2>'],
    ('<granted_content>', 'scroll_lit'): ['<granted_content_2>'],
    ('<granted_content>', '!'): ['<granted_content_2>'],
    ('<granted_content>', 'toocean'): ['<granted_content_2>'],
    ('<granted_content>', 'tomirror'): ['<granted_content_2>'],
    ('<granted_content>', '('): ['<granted_content_2>'],
    ('<granted_content>', 'treasures_lit'): ['<granted_content_2>'],
    ('<granted_content>', '1'): ['<granted_content_2>'],
    ('<granted_content>', 'phantom'): ['<granted_content_2>'],
    ('<granted_content>', 'ocean_lit'): ['<granted_content_2>'],
    # <granted_open_paren_ext>
    ('<granted_open_paren_ext>', 'identifier'): ['identifier', '<id_ext>', '<idlit3_granted_ext>'],
    ('<granted_open_paren_ext>', 'ocean_lit'): ['<lit3>', '<idlit3_granted_ext>'],
    ('<granted_open_paren_ext>', 'treasures_lit'): ['<lit3>', '<idlit3_granted_ext>'],
    ('<granted_open_paren_ext>', 'scroll_lit'): ['scroll_lit', '<expression_ext_2>', '<more_log>', ')'],
    ('<granted_open_paren_ext>', 'rose_lit'): ['rose_lit', '<expression_ext_2>', '<more_log>', ')'],
    ('<granted_open_paren_ext>', 'mirror_lit'): ['mirror_lit', '<expression_ext_2>', '<more_log>', ')'],
    ('<granted_open_paren_ext>', '1'): ['<treasures_mirror>', '<expression_ext_2>', '<more_log>', ')'],
    ('<granted_open_paren_ext>', '0'): ['<treasures_mirror>', '<expression_ext_2>', '<more_log>', ')'],
    ('<granted_open_paren_ext>', '('): ['(', '<logical_operator1>', '<granted_open_paren_ext>', ')', '<close_paren_ext>'],
    # <idlit3_granted_ext>
    ('<idlit3_granted_ext>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>', '<more_log>'],      
    ('<idlit3_granted_ext>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>', '<more_log>'],     
    ('<idlit3_granted_ext>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>', '<more_log>'],     
    ('<idlit3_granted_ext>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>', '<more_log>'],     
    ('<idlit3_granted_ext>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>', '<more_log>'],     
    ('<idlit3_granted_ext>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>', ')', '<relational_more>', '<more_log>'],      
    ('<idlit3_granted_ext>', '||'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')', '<more_log>'],
    ('<idlit3_granted_ext>', '&&'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>', ')', '<more_log>'],
    ('<idlit3_granted_ext>', '/'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', ')', '<more_arith>', '<open_paren_other_ext>'],
    ('<idlit3_granted_ext>', '*'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', ')', '<more_arith>', '<open_paren_other_ext>'],
    ('<idlit3_granted_ext>', '-'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', ')', '<more_arith>', '<open_paren_other_ext>'],
    ('<idlit3_granted_ext>', '%'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', ')', '<more_arith>', '<open_paren_other_ext>'],
    ('<idlit3_granted_ext>', '+'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<relational_more>', ')', '<more_arith>', '<open_paren_other_ext>'],
    # <open_paren_other_ext>
    ('<open_paren_other_ext>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<open_paren_other_ext>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<open_paren_other_ext>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<open_paren_other_ext>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<open_paren_other_ext>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<open_paren_other_ext>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<open_paren_other_ext>', '||'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<open_paren_other_ext>', '&&'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<open_paren_other_ext>', ')'): ['ε'],
    ('<open_paren_other_ext>', '~'): ['ε'],
    ('<open_paren_other_ext>', ','): ['ε'],
    # <close_paren_ext>
    ('<close_paren_ext>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<close_paren_ext>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<close_paren_ext>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<close_paren_ext>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<close_paren_ext>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<close_paren_ext>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<close_paren_ext>', '||'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<close_paren_ext>', '&&'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<close_paren_ext>', '/'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<open_paren_other_ext>'],
    ('<close_paren_ext>', '*'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<open_paren_other_ext>'],
    ('<close_paren_ext>', '-'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<open_paren_other_ext>'],
    ('<close_paren_ext>', '%'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<open_paren_other_ext>'],
    ('<close_paren_ext>', '+'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<open_paren_other_ext>'],
    ('<close_paren_ext>', ')'): ['ε'],
    ('<close_paren_ext>', '~'): ['ε'],
    ('<close_paren_ext>', ','): ['ε'],
    # <granted_id_ext>
    ('<granted_id_ext>', '--'): ['<unary_operator>'],
    ('<granted_id_ext>', '++'): ['<unary_operator>'],
    ('<granted_id_ext>', '('): ['<func_call>', '<granted_other_id_ext>'],
    ('<granted_id_ext>', '['): ['[', '<array_size>', ']', '<column1>', '<granted_other_id_ext>'],
    ('<granted_id_ext>', '>'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '<'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '&&'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '/'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '*'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '||'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '=='): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '>='): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '-'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '+'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '%'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '<='): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '~'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', '!='): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', ')'): ['<granted_other_id_ext>'],
    ('<granted_id_ext>', ','): ['ε'],
    # <granted_other_id_ext>
    ('<granted_other_id_ext>', '+'): ['+', '<plus_ext>'],
    ('<granted_other_id_ext>', '-'): ['-', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<granted_other_id_ext>', '*'): ['*', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<granted_other_id_ext>', '/'): ['/', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<granted_other_id_ext>', '%'): ['%', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<granted_other_id_ext>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext>', '||'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<granted_other_id_ext>', '&&'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<granted_other_id_ext>', ')'): ['ε'],
    ('<granted_other_id_ext>', '~'): ['ε'],
    ('<granted_other_id_ext>', ','): ['ε'],
    # <granted_other_id_ext2>
    ('<granted_other_id_ext2>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext2>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext2>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext2>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext2>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext2>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_other_id_ext2>', ')'): ['ε'],
    ('<granted_other_id_ext2>', '~'): ['ε'],
    ('<granted_other_id_ext2>', ','): ['ε'],
    # <plus_ext>
    ('<plus_ext>', 'identifier'): ['identifier', '<id_ext>', '<plus_ext_1>'],
    ('<plus_ext>', 'toscroll'): ['toscroll', '(', '<conversion_value>', ')','<string_more>'],
    ('<plus_ext>', 'scroll_lit'): ['scroll_lit', '<string_more>'],
    ('<plus_ext>', 'rose_lit'): ['rose_lit', '<string_more>'],
    ('<plus_ext>', '('): ['(', '<arithmetic_exp>', ')', '<more_arith>', '<granted_other_id_ext2>'],
    ('<plus_ext>', 'treasures_lit'): ['treasures_lit', '<more_arith>', '<granted_other_id_ext2>'],
    ('<plus_ext>', '1'): ['1', '<more_arith>', '<granted_other_id_ext2>'],
    ('<plus_ext>', '0'): ['0', '<more_arith>', '<granted_other_id_ext2>'],
    ('<plus_ext>', 'ocean_lit'): ['ocean_lit', '<more_arith>', '<granted_other_id_ext2>'],
    # <plus_ext_1>
    ('<plus_ext_1>', '+'): ['+', '<plus_ext>'],
    ('<plus_ext_1>', '-'): ['-', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<plus_ext_1>', '*'): ['*', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<plus_ext_1>', '/'): ['/', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<plus_ext_1>', '%'): ['%', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<plus_ext_1>', ')'): ['ε'],
    ('<plus_ext_1>', '~'): ['ε'],
    ('<plus_ext_1>', ','): ['ε'],
    # <granted_scroll_ext>
    ('<granted_scroll_ext>', '+'): ['+', '<string_operand>', '<string_more>'],
    ('<granted_scroll_ext>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_scroll_ext>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_scroll_ext>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_scroll_ext>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_scroll_ext>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_scroll_ext>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_scroll_ext>', ','): ['ε'],
    ('<granted_scroll_ext>', ')'): ['ε'],
    ('<granted_scroll_ext>', '~'): ['ε'],
    ('<granted_scroll_ext>', ','): ['ε'],
    # <granted_rose_ext>
    ('<granted_rose_ext>', '+'): ['+', '<string_operand>', '<string_more>'],
    ('<granted_rose_ext>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_rose_ext>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_rose_ext>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_rose_ext>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_rose_ext>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_rose_ext>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_rose_ext>', ')'): ['ε'],
    ('<granted_rose_ext>', '~'): ['ε'],
    ('<granted_rose_ext>', ','): ['ε'],
    # <granted_lit3_ext>
    ('<granted_lit3_ext>', '/'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<granted_lit3_ext1>'],
    ('<granted_lit3_ext>', '*'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<granted_lit3_ext1>'],
    ('<granted_lit3_ext>', '-'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<granted_lit3_ext1>'],
    ('<granted_lit3_ext>', '%'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<granted_lit3_ext1>'],
    ('<granted_lit3_ext>', '+'): ['<arithmetic_operator>', '<arithmetic_operand>', '<more_arith>', '<granted_lit3_ext1>'],
    ('<granted_lit3_ext>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext>', ')'): ['ε'],
    ('<granted_lit3_ext>', '~'): ['ε'],
    ('<granted_lit3_ext>', ','): ['ε'],
    # <granted_lit3_ext1>
    ('<granted_lit3_ext1>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext1>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext1>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext1>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext1>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext1>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<granted_lit3_ext1>', ')'): ['ε'],
    ('<granted_lit3_ext1>', '~'): ['ε'],
    ('<granted_lit3_ext1>', ','): ['ε'],
    # <more_granted>
    ('<more_granted>', ','): [',', '<granted_content>', '<more_granted>'],
    ('<more_granted>', ')'): ['ε'],
    # <data_type>
    ('<data_type>', 'scroll'): ['scroll'],
    ('<data_type>', 'treasures'): ['treasures'],
    ('<data_type>', 'mirror'): ['mirror'],
    ('<data_type>', 'ocean'): ['ocean'],
    ('<data_type>', 'rose'): ['rose'],
    # <val>
    ('<val>', 'mirror_lit'): ['<granted_content_2>'],
    ('<val>', 'toscroll'): ['<granted_content_2>'],
    ('<val>', '0'): ['<granted_content_2>'],
    ('<val>', 'rose_lit'): ['<granted_content_2>'],
    ('<val>', 'torose'): ['<granted_content_2>'],
    ('<val>', 'totreasures'): ['<granted_content_2>'],
    ('<val>', 'lengthof'): ['<granted_content_2>'],
    ('<val>', 'scroll_lit'): ['<granted_content_2>'],
    ('<val>', '!'): ['<granted_content_2>'],
    ('<val>', 'toocean'): ['<granted_content_2>'],
    ('<val>', 'tomirror'): ['<granted_content_2>'],
    ('<val>', '('): ['<granted_content_2>'],
    ('<val>', 'treasures_lit'): ['<granted_content_2>'],
    ('<val>', '1'): ['<granted_content_2>'],
    ('<val>', 'phantom'): ['<granted_content_2>'],
    ('<val>', 'ocean_lit'): ['<granted_content_2>'],
    ('<val>', 'identifier'): ['identifier', '<granted_id_ext>'],
    ('<val>', 'wish'): ['<input>'],
    # <val1>
    ('<val1>', 'mirror_lit'): ['<granted_content_2>'],
    ('<val1>', 'toscroll'): ['<granted_content_2>'],
    ('<val1>', '0'): ['<granted_content_2>'],
    ('<val1>', 'rose_lit'): ['<granted_content_2>'],
    ('<val1>', 'torose'): ['<granted_content_2>'],
    ('<val1>', 'totreasures'): ['<granted_content_2>'],
    ('<val1>', 'lengthof'): ['<granted_content_2>'],
    ('<val1>', 'scroll_lit'): ['<granted_content_2>'],
    ('<val1>', '!'): ['<granted_content_2>'],
    ('<val1>', 'toocean'): ['<granted_content_2>'],
    ('<val1>', 'tomirror'): ['<granted_content_2>'],
    ('<val1>', '('): ['<granted_content_2>'],
    ('<val1>', 'treasures_lit'): ['<granted_content_2>'],
    ('<val1>', '1'): ['<granted_content_2>'],
    ('<val1>', 'phantom'): ['<granted_content_2>'],
    ('<val1>', 'ocean_lit'): ['<granted_content_2>'],
    ('<val1>', 'identifier'): ['identifier', '<val1_ext>'],
    # <val1_ext>
    ('<val1_ext>', '-='): ['<val1_id_ext>'],
    ('<val1_ext>', '%='): ['<val1_id_ext>'],
    ('<val1_ext>', '*='): ['<val1_id_ext>'],
    ('<val1_ext>', '~'): ['<val1_id_ext>'],
    ('<val1_ext>', '/='): ['<val1_id_ext>'],
    ('<val1_ext>', '+='): ['<val1_id_ext>'],
    ('<val1_ext>', '('): ['<func_call>', '<val1_id_ext>'],
    ('<val1_ext>', '['): ['[', '<array_size>', ']', '<column1>', '<val1_id_ext>'],
    ('<val1_ext>', '--'): ['<unary_operator>'],
    ('<val1_ext>', '++'): ['<unary_operator>'],
    ('<val1_ext>', '+'): ['+', '<plus_ext>'],
    ('<val1_ext>', '-'): ['-', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<val1_ext>', '*'): ['*', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<val1_ext>', '/'): ['/', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<val1_ext>', '%'): ['%', '<arithmetic_operand>', '<more_arith>', '<granted_other_id_ext2>'],
    ('<val1_ext>', '>'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<val1_ext>', '!='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<val1_ext>', '=='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<val1_ext>', '>='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<val1_ext>', '<='): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<val1_ext>', '<'): ['<relational_operator>', '<relational_operand>', '<relational_more>', '<more_log>'],
    ('<val1_ext>', '||'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    ('<val1_ext>', '&&'): ['<logical_operator>', '<logical_operator1>', '<logical_operand>', '<more_log>'],
    # <val1_id_ext>
    ('<val1_id_ext>', '-='): ['<assignment_operator>', '<assignment_operand>'],
    ('<val1_id_ext>', '%='): ['<assignment_operator>', '<assignment_operand>'],
    ('<val1_id_ext>', '*='): ['<assignment_operator>', '<assignment_operand>'],
    ('<val1_id_ext>', '/='): ['<assignment_operator>', '<assignment_operand>'],
    ('<val1_id_ext>', '+='): ['<assignment_operator>', '<assignment_operand>'],
    ('<val1_id_ext>', '~'): ['ε'],
    # <conversion_func>
    ('<conversion_func>', 'torose'): ['torose'],
    ('<conversion_func>', 'totreasures'): ['totreasures'],
    ('<conversion_func>', 'toocean'): ['toocean'],
    ('<conversion_func>', 'tomirror'): ['tomirror'],
    # <conversion_value>
    ('<conversion_value>', 'mirror_lit'): ['<lit4>'],
    ('<conversion_value>', 'rose_lit'): ['<lit4>'],
    ('<conversion_value>', 'scroll_lit'): ['<lit4>'],
    ('<conversion_value>', 'treasures_lit'): ['<lit4>'],
    ('<conversion_value>', '1'): ['<lit4>'],
    ('<conversion_value>', '0'): ['<lit4>'],
    ('<conversion_value>', 'ocean_lit'): ['<lit4>'],
    ('<conversion_value>', 'identifier'): ['identifier', '<id_ext>'],
    # <index>
    ('<index>', '['): ['[', '<array_size>', ']', '<column1>'],
    ('<index>', '%='): ['ε'],
    ('<index>', '-='): ['ε'],
    ('<index>', '='): ['ε'],
    ('<index>', '*='): ['ε'],
    ('<index>', ')'): ['ε'],
    ('<index>', '/='): ['ε'],
    ('<index>', '+='): ['ε'],
    # <column1>
    ('<column1>', '['): ['[', '<array_size>', ']'],
    ('<column1>', '>'): ['ε'],
    ('<column1>', '-='): ['ε'],
    ('<column1>', '='): ['ε'],
    ('<column1>', '&&'): ['ε'],
    ('<column1>', '/'): ['ε'],
    ('<column1>', '*'): ['ε'],
    ('<column1>', '!='): ['ε'],
    ('<column1>', '*='): ['ε'],
    ('<column1>', '-'): ['ε'],
    ('<column1>', '+'): ['ε'],
    ('<column1>', '<='): ['ε'],
    ('<column1>', '/='): ['ε'],
    ('<column1>', '||'): ['ε'],
    ('<column1>', '=='): ['ε'],
    ('<column1>', '>='): ['ε'],
    ('<column1>', '%='): ['ε'],
    ('<column1>', '%'): ['ε'],
    ('<column1>', ')'): ['ε'],
    ('<column1>', '~'): ['ε'],
    ('<column1>', '<'): ['ε'],
    ('<column1>', '+='): ['ε'],
    ('<column1>', ','): ['ε'],
    # <input>
    ('<input>', 'wish'): ['wish', '(', 'scroll_lit', ')'],
    # <lit1>
    ('<lit1>', 'scroll_lit'): ['scroll_lit'],
    ('<lit1>', 'rose_lit'): ['rose_lit'],
    # <lit2>
    ('<lit2>', 'mirror_lit'): ['mirror_lit'],
    # <lit3>
    ('<lit3>', 'ocean_lit'): ['ocean_lit'],
    ('<lit3>', 'treasures_lit'): ['treasures_lit'],
    ('<lit3>', '1'): ['1'],
    ('<lit3>', '0'): ['0'],
    # <lit4>
    ('<lit4>', 'scroll_lit'): ['<lit1>'],
    ('<lit4>', 'rose_lit'): ['<lit1>'],
    ('<lit4>', 'mirror_lit'): ['<lit2>'],
    ('<lit4>', 'ocean_lit'): ['<lit3>'],
    ('<lit4>', 'treasures_lit'): ['<lit3>'],
    ('<lit4>', '1'): ['<lit3>'],
    ('<lit4>', '0'): ['<lit3>'],
    # <func_call>
    ('<func_call>', '('): ['(', '<args>', ')'],
    # <args>
    ('<args>', 'mirror_lit'): ['<args_val>', '<args_more>'],
    ('<args>', 'rose_lit'): ['<args_val>', '<args_more>'],
    ('<args>', 'scroll_lit'): ['<args_val>', '<args_more>'],
    ('<args>', 'treasures_lit'): ['<args_val>', '<args_more>'],
    ('<args>', '1'): ['<args_val>', '<args_more>'],
    ('<args>', '0'): ['<args_val>', '<args_more>'],
    ('<args>', 'identifier'): ['<args_val>', '<args_more>'],
    ('<args>', 'ocean_lit'): ['<args_val>', '<args_more>'],
    ('<args>', ')'): ['ε'],
    # <args_val>
    ('<args_val>', 'identifier'): ['identifier', '<id_ext>'],
    ('<args_val>', 'mirror_lit'): ['<lit4>'],
    ('<args_val>', 'rose_lit'): ['<lit4>'],
    ('<args_val>', 'scroll_lit'): ['<lit4>'],
    ('<args_val>', 'treasures_lit'): ['<lit4>'],
    ('<args_val>', '1'): ['<lit4>'],
    ('<args_val>', '0'): ['<lit4>'],
    ('<args_val>', 'ocean_lit'): ['<lit4>'],
    # <args_more>
    ('<args_more>', ','): [',', '<args_val>', '<args_more>'],
    ('<args_more>', ')'): ['ε'],
    # <id_ext>
    ('<id_ext>', '('): ['<func_call>'],
    ('<id_ext>', '['): ['[', '<array_size>', ']', '<column1>'],
    ('<id_ext>', '>'): ['ε'],
    ('<id_ext>', '&&'): ['ε'],
    ('<id_ext>', '/'): ['ε'],
    ('<id_ext>', '*'): ['ε'],
    ('<id_ext>', '!='): ['ε'],
    ('<id_ext>', '+'): ['ε'],
    ('<id_ext>', '-'): ['ε'],
    ('<id_ext>', '<='): ['ε'],
    ('<id_ext>', '||'): ['ε'],
    ('<id_ext>', '=='): ['ε'],
    ('<id_ext>', '>='): ['ε'],
    ('<id_ext>', '%'): ['ε'],
    ('<id_ext>', ')'): ['ε'],
    ('<id_ext>', '~'): ['ε'],
    ('<id_ext>', '<'): ['ε'],
    ('<id_ext>', ','): ['ε'],
    # <array_size>
    ('<array_size>', 'identifier'): ['identifier'],
    ('<array_size>', 'treasures_lit'): ['treasures_lit'],
    ('<array_size>', '1'): ['1'],
    ('<array_size>', '0'): ['0'],
}
    
    def __init__(self, start_symbol):
        self.cfg = self.CFG
        self.predict = self.PREDICT
        self.start_symbol = start_symbol

    def parse(self, tokens):
        # Convert tokens iterator to a list for random access
        tokens = list(tokens)
        # Initialize position pointer to start of token list
        pos = 0
        # Initialize parsing stack with end marker and start symbol
        # The stack is processed from right to left (top is rightmost/last element)
        stack = ['EOF', self.start_symbol] # ['EOF', '<program>']
        # Initialize error message as None (will be set if an error occurs)
        error_message = None

        # Initialize line tracking for error reporting
        # Default to line 1 even if tokens list is empty
        last_line = 1 if tokens else 1
        # Position counter within current line
        position_in_line = 1

        # List to track all productions used during parsing (for debugging)
        entered_productions = [] 

        # Main parsing loop - continues until stack is empty
        while stack:
            # Debug output showing current state of parser
            print(f"Stack: {stack}, pos: {pos}, token: {tokens[pos].token_type if pos < len(tokens) else 'OUT_OF_BOUNDS'}")
            
            # Pop the top symbol from the stack to process it
            top = stack.pop() # '<global_dec>'

            # Skip any comment tokens before processing current symbol
            while pos < len(tokens) and tokens[pos].token_type in ('single_comment', 'multi_comment'):
                # Move to next token
                pos += 1
                # Update line position tracking if we still have tokens
                if pos < len(tokens):
                    if tokens[pos].line != last_line:  # Check if we've moved to a new line
                        last_line = tokens[pos].line   # Update line number
                        position_in_line = 1           # Reset position to beginning of line
                    else:
                        position_in_line += 1          # Increment position within current line

            # Safety check - if we've gone beyond the token list
            if pos >= len(tokens):
                error_message = f"Parser error: Position {pos} exceeded token list length {len(tokens)}"
                return False, error_message

            # Extract information from the current token for processing and error reporting
            current_token = tokens[pos]                        # Get the current token object
            current_token_type = current_token.token_type      # Extract token type for matching
            current_token_value = getattr(current_token, 'value', '')  # Get token value if available
            current_token_line = getattr(current_token, 'line', '?')   # Get line number if available

            # Use tracked position for error reporting
            current_token_pos = position_in_line

            # Case 1: If top of stack is epsilon (empty production), 
            # just continue without consuming input
            if top == 'ε': # '<gloabl_dec>' == 'ε'
                continue

            # Case 2: If top of stack matches current token type,
            # we've found a terminal match
            elif top == current_token_type: # '<gloabl_dec>' == 'castle'
                # Debug output to show matched token
                print(f"Matched token: {top} at position {pos}") # debugging
                
                # Advance to next token
                pos += 1
                # Update line position tracking if we still have tokens
                if pos < len(tokens):
                    if tokens[pos].line != last_line:  # Check if we've moved to a new line
                        last_line = tokens[pos].line   # Update line number
                        position_in_line = 1           # Reset position to beginning of line
                    else:
                        position_in_line += 1          # Increment position within current line
                            
            # Case 3: If top of stack is a non-terminal (defined in the CFG)
            elif top in self.cfg: # '<gloabl_dec>'
                # Get a list of expected tokens for this non-terminal (for error reporting)
                expected = [lookahead for (nt, lookahead) in self.predict if nt == top] # ('<gloabl_dec>', lookahead ) # 'crown'
                
                # Create a key from current non-terminal and token type to look up in predict table
                key = (top, current_token_type) # ('<gloabl_dec>', 'castle') 
                
                # If the key exists in predict table, we have a valid production
                if key in self.predict:
                    # Get the production to apply
                    production = self.predict[key] # self.predict[('<gloabl_dec>', 'castle') ] = 'ε'
                    # ['crown', '~', '<global_dec>', '<user-defined_func>', 'castle', 'treasures', 'identifier', '(', ')', '{', '<body>', 'return', '0', '~', '}', 'reign', '~'],
                    
                    # Record this production for debugging
                    entered_productions.append((top, current_token_type, production.copy()))
                    
                    # Push production symbols onto stack in reverse order
                    # (since stack processes from right to left)
                    for symbol in reversed(production):
                        if symbol != 'ε':  # Skip epsilon symbols
                            stack.append(symbol) # ['EOF', '~', .... , 'castle']
                else:
                    # If no production found, generate syntax error
                    error_message = (
                        f"Syntax Error: Unexpected input '{current_token_value}' at line {current_token_line}, position {current_token_pos}. "
                        f"Expected one of {expected}"
                    )
                    # Print debugging information showing productions applied before error
                    print("Productions entered before error:")
                    for prod in entered_productions:
                        print(f"{prod[0]} -> {prod[2]} (lookahead: {prod[1]})")
                    return False, error_message
            else:
                # Case 4: Top of stack is a terminal that doesn't match current token
                error_message = (
                    f"Syntax Error: Unexpected input '{current_token_value}' at line {current_token_line}, position {current_token_pos}. "
                    f"Expected one of ['{top}']"
                )
                # Print debugging information showing productions applied before error
                print("Productions entered before error:")
                for prod in entered_productions:
                    print(f"{prod[0]} -> {prod[2]} (lookahead: {prod[1]})")
                return False, error_message

        # After the loop ends, check the position
        print(f"Loop ended. pos: {pos}, len(tokens): {len(tokens)}")
        
        if pos == len(tokens):
            print("All productions entered during parse:") # for debug
            for prod in entered_productions:  # for debug
                print(f"{prod[0]} -> {prod[2]} (lookahead: {prod[1]})")  # for debug
            return True, None
        else:
            # Unconsumed input
            if pos < len(tokens):
                current_token = tokens[pos]
                current_token_value = getattr(current_token, 'value', '')
                current_token_line = getattr(current_token, 'line', '?')
                current_token_pos = position_in_line
                error_message = (
                    f"Syntax Error: Unexpected input '{current_token_value}' at line {current_token_line}, position {current_token_pos}. "
                    f"Expected end of input."
                )
            else:
                error_message = f"Parser error: Position {pos} exceeded token list length {len(tokens)}"
            
            print("Productions entered before error:")
            for prod in entered_productions:
                print(f"{prod[0]} -> {prod[2]} (lookahead: {prod[1]})")
            return False, error_message