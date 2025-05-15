import re

def parse_predict_line(line):
    # Split by arrow symbol, considering that there might be spaces around it
    parts = [p.strip() for p in re.split(r'\s*→\s*', line)]
    
    if len(parts) != 3:
        return []
    
    # Extract nonterminal from PREDICT(<nonterminal>)
    m = re.match(r"PREDICT\(([^)]+)\)", parts[0])
    if not m:
        return []
    
    nonterminal = m.group(1)
    production = parts[1]
    
    # Process lookaheads inside curly braces
    lookaheads_str = parts[2].strip()
    if lookaheads_str.startswith('{') and lookaheads_str.endswith('}'):
        # Remove curly braces and split by comma
        lookaheads_content = lookaheads_str[1:-1].strip()
        # Handle empty lookaheads case
        if not lookaheads_content:
            return []
        
        # Split by comma and clean each lookahead
        lookaheads = [re.sub(r'\s+', '', x) for x in lookaheads_content.split(',')]
        
        # Handle empty production (λ) or split by spaces
        prod_list = ['λ'] if production == 'λ' else [x for x in production.split() if x]
        
        # Create entries with specific keys that won't be duplicated
        return [((nonterminal, lookahead), prod_list) for lookahead in lookaheads if lookahead]
    
    return []

def convert_predict_table(lines):
    entries = []
    seen_keys = set()  # Track keys we've already seen
    
    for line in lines:
        line = line.strip()
        if not line or not line.startswith("PREDICT("):
            continue
            
        new_entries = parse_predict_line(line)
        for key, value in new_entries:
            if key in seen_keys:
                # If we have a duplicate key, show a warning
                print(f"Warning: Duplicate key found: {key}")
                # We skip adding this duplicate to maintain the first occurrence only
            else:
                seen_keys.add(key)
                entries.append((key, value))
    
    return entries

def format_predict_dict(entries):
    out = ["PREDICT = {"]
    last_nonterminal = None
    for (nonterminal, lookahead), prod_list in entries:
        if nonterminal != last_nonterminal:
            out.append(f"    # {nonterminal}")
            last_nonterminal = nonterminal
        prod_str = ', '.join(f"'{x}'" for x in prod_list)
        out.append(f"    ('{nonterminal}', '{lookahead}'): [{prod_str}],")
    out.append("}")
    return '\n'.join(out)

# Example usage:
if __name__ == "__main__":
    # You can paste your input text here as a multi-line string
    input_text = """
PREDICT(<program>) → crown ~ <global_dec> <user-defined_func> castle treasures id_lit ( ) { <body> return 0 ~ } reign ~ → {crown}
PREDICT(<global_dec>) → <var_dec> <global_dec> → {rose, ocean, treasures, dynasty, scroll, mirror}
PREDICT(<global_dec>) → λ → {spell, castle}
PREDICT(<var_dec>) → <dynasty> <data_type> id_lit <vardec_def> → {rose, ocean, treasures, dynasty, scroll, mirror}
PREDICT(<dynasty>) → dynasty → {dynasty}
PREDICT(<dynasty>) → λ → {treasures, rose, ocean, mirror, scroll}
PREDICT(<vardec_def>) → <initialization> <vardec_more> ~ → {,, =, ~}
PREDICT(<vardec_def>) → [ <array_size> ] <column> <array_initialization> <array_more> ~ → {[}
PREDICT(<initialization>) → = <val> → {=}
PREDICT(<initialization>) → λ → {,, ~}
PREDICT(<vardec_more>) → , id_lit <initialization> <vardec_more> → {,}
PREDICT(<vardec_more>) → λ → {~}
PREDICT(<column>) → [ <array_size> ] → {[}
PREDICT(<column>) → λ → {,, =, ~}
PREDICT(<array_initialization>) → = <array_list> → {=}
PREDICT(<array_initialization>) → λ → {,, ~}
PREDICT(<array_list>) → { <array_content> } → {{}
PREDICT(<array_content>) → <array_lit> <lit_more> → {scroll_lit, mirror_lit, treasures_lit, rose_lit, ocean_lit, id_lit}
PREDICT(<array_content>) → { <array_row> } <row_more> → {{}
PREDICT(<array_row>) → <array_lit> <lit_more> → {scroll_lit, mirror_lit, treasures_lit, rose_lit, ocean_lit, id_lit}
PREDICT(<row_more>) → , <row_more_ext> → {,}
PREDICT(<row_more>) → λ → {}}
PREDICT(<row_more_ext>) → { <array_row> } <row_more> → {{}
PREDICT(<row_more_ext>) → id_lit <row_more> → {id_lit}
PREDICT(<lit_more>) → , <lit_more_ext> → {,}
PREDICT(<lit_more>) → λ → {}}
PREDICT(<lit_more_ext>) → <array_lit> <lit_more> → {scroll_lit, mirror_lit, treasures_lit, rose_lit, ocean_lit, id_lit}
PREDICT(<lit_more_ext>) → { <array_row> } <row_more> → {{}
PREDICT(<array_more>) → , id_lit [ <array_size> ] <column> <array_initialization> <array_more> → {,}
PREDICT(<array_more>) → λ → {~}
PREDICT(<array_lit>) → <lit4> → {scroll_lit, mirror_lit, treasures_lit, rose_lit, ocean_lit}
PREDICT(<array_lit>) → id_lit → {id_lit}
PREDICT(<assignment_operator>) → += → {+=}
PREDICT(<assignment_operator>) → -= → {-=}
PREDICT(<assignment_operator>) → *= → {*=}
PREDICT(<assignment_operator>) → /= → {/=}
PREDICT(<assignment_operator>) → %= → {%=}
PREDICT(<assignment_operand>) → id_lit <id_ext> <more_arith> → {id_lit}
PREDICT(<assignment_operand>) → <lit3> <more_arith> → {treasures_lit, ocean_lit}
PREDICT(<assignment_operand>) → <arithmetic_operand_2> <arithmetic_operator> <arithmetic_operand> <more_arith> → {(}
PREDICT(<logical_exp>) → <logical_operator1> <logical_operand> <logical_operator> <logical_operator1> <logical_operand> <more_log> → {scroll_lit, 1, !, mirror_lit, treasures_lit, rose_lit, ocean_lit, (, 0, id_lit}
PREDICT(<logical_operand>) → id_lit <id_ext> <logical_operand_ext> → {id_lit}
PREDICT(<logical_operand>) → <lit3> <more_arith> <relational_operator> <relational_operand> <relational_more> → {treasures_lit, ocean_lit}
PREDICT(<logical_operand>) → scroll_lit <relational_operator> <relational_operand> <relational_more> → {scroll_lit}
PREDICT(<logical_operand>) → rose_lit <relational_operator> <relational_operand> <relational_more> → {rose_lit}
PREDICT(<logical_operand>) → mirror_lit <relational_more> → {mirror_lit}
PREDICT(<logical_operand>) → <treasures_mirror> <relational_more> → {1, 0}
PREDICT(<logical_operand>) → ( <logical_operator1> <expression> → {(}
PREDICT(<expression>) → id_lit <id_ext> <expression_ext_1> → {id_lit}
PREDICT(<expression>) → <lit3> <expression_ext_1> → {treasures_lit, ocean_lit}
PREDICT(<expression>) → scroll_lit <expression_ext_2> → {scroll_lit}
PREDICT(<expression>) → rose_lit <expression_ext_2> → {rose_lit}
PREDICT(<expression>) → mirror_lit <expression_ext_2> → {mirror_lit}
PREDICT(<expression>) → <treasures_mirror> <expression_ext_2> → {1, 0}
PREDICT(<expression>) → ( <logical_operator1> <expression> <more_log> ) <logical_operand_ext> → {(}
PREDICT(<expression_ext_1>) → <relational_operator> <relational_operand> <relational_more> ) <relational_more> → {<=, <, >=, !=, >, ==}
PREDICT(<expression_ext_1>) → <logical_operator> <logical_operator1> <logical_operand> <more_log> ) → {&&, ||}
PREDICT(<expression_ext_1>) → <arithmetic_operator> <arithmetic_operand> <more_arith> <relational_more> ) <more_arith> <relational_more> → {-, %, *, /, +}
PREDICT(<expression_ext_2>) → <relational_operator> <relational_operand> <relational_more> ) <relational_more> → {<=, <, >=, !=, >, ==}
PREDICT(<expression_ext_2>) → <logical_operator> <logical_operator1> <logical_operand> <more_log> ) → {&&, ||}
PREDICT(<logical_operand_ext>) → <more_arith> <relational_operator> <relational_operand> <relational_more> → {-, <=, /, <, >=, %, !=, >, ==, *, +}
PREDICT(<logical_operand_ext>) → λ → {), &&, ~, ||, ,}
PREDICT(<logical_operator>) → && → {&&}
PREDICT(<logical_operator>) → || → {||}
PREDICT(<logical_operator1>) → ! → {!}
PREDICT(<logical_operator1>) → λ → {scroll_lit, 1, mirror_lit, treasures_lit, rose_lit, ocean_lit, (, 0, id_lit}
PREDICT(<more_log>) → <logical_operator> <logical_operator1> <logical_operand> <more_log> → {&&, ||}
PREDICT(<more_log>) → λ → {,, ), ~}
PREDICT(<treasures_mirror>) → 1 → {1}
PREDICT(<treasures_mirror>) → 0 → {0}
PREDICT(<arithmetic_exp>) → <arithmetic_operand> <arithmetic_operator> <arithmetic_operand> <more_arith> → {id_lit, treasures_lit, ocean_lit, (}
PREDICT(<arithmetic_operand_1>) → id_lit <id_ext> → {id_lit}
PREDICT(<arithmetic_operand_1>) → <lit3> → {treasures_lit, ocean_lit}
PREDICT(<arithmetic_operand_2>) → ( <arithmetic_exp> ) → {(}
PREDICT(<arithmetic_operand>) → <arithmetic_operand_1> → {id_lit, treasures_lit, ocean_lit}
PREDICT(<arithmetic_operand>) → <arithmetic_operand_2> → {(}
PREDICT(<arithmetic_operator>) → + → {+}
PREDICT(<arithmetic_operator>) → - → {-}
PREDICT(<arithmetic_operator>) → / → {/}
PREDICT(<arithmetic_operator>) → * → {*}
PREDICT(<arithmetic_operator>) → % → {%}
PREDICT(<more_arith>) → <arithmetic_operator> <arithmetic_operand> <more_arith> → {-, %, *, /, +}
PREDICT(<more_arith>) → λ → {<=, ~, <, >=, !=, >, ,, ==, ), &&, ||}
PREDICT(<relational_exp>) → <relational_operand> <relational_operator> <relational_operand> <relational_more> → {scroll_lit, mirror_lit, treasures_lit, rose_lit, ocean_lit, (, id_lit, treasures_mirror}
PREDICT(<relational_operand>) → id_lit <id_ext> <more_arith> → {id_lit}
PREDICT(<relational_operand>) → <lit3> <more_arith> → {treasures_lit, ocean_lit}
PREDICT(<relational_operand>) → scroll_lit → {scroll_lit}
PREDICT(<relational_operand>) → rose_lit → {rose_lit}
PREDICT(<relational_operand>) → mirror_lit → {mirror_lit}
PREDICT(<relational_operand>) → treasures_mirror → {treasures_mirror}
PREDICT(<relational_operand>) → ( <expression_2> → {(}
PREDICT(<expression_2>) → id_lit <id_ext> <expression_2_ext> → {id_lit}
PREDICT(<expression_2>) → <lit3> <expression_2_ext> → {treasures_lit, ocean_lit}
PREDICT(<expression_2>) → scroll_lit <relational_operator> <relational_operand> <relational_more> ) → {scroll_lit}
PREDICT(<expression_2>) → rose_lit <relational_operator> <relational_operand> <relational_more> ) → {rose_lit}
PREDICT(<expression_2>) → mirror_lit <relational_operator> <relational_operand> <relational_more> ) → {mirror_lit}
PREDICT(<expression_2>) → treasures_mirror <relational_operator> <relational_operand> <relational_more> ) → {treasures_mirror}
PREDICT(<expression_2>) → ( <expression_2> ) → {(}
PREDICT(<expression_2_ext>) → <arithmetic_operator> <arithmetic_operand> <more_arith> ) <more_arith> → {-, %, *, /, +}
PREDICT(<expression_2_ext>) → <relational_operator> <relational_operand> <relational_more> ) → {<=, <, >=, !=, >, ==}
PREDICT(<relational_operator>) → < → {<}
PREDICT(<relational_operator>) → > → {>}
PREDICT(<relational_operator>) → <= → {<=}
PREDICT(<relational_operator>) → >= → {>=}
PREDICT(<relational_operator>) → == → {==}
PREDICT(<relational_operator>) → != → {!=}
PREDICT(<relational_more>) → <relational_operator> <relational_operand> <relational_more> → {<=, <, >=, !=, >, ==}
PREDICT(<relational_more>) → λ → {), &&, ~, ||, ,}
PREDICT(<unary>) → id_lit <unary_operator> → {id_lit}
PREDICT(<unary_operator>) → ++ → {++}
PREDICT(<unary_operator>) → -- → {--}
PREDICT(<string_operand>) → <lit1> → {scroll_lit, rose_lit}
PREDICT(<string_operand>) → id_lit <id_ext> → {id_lit}
PREDICT(<string_operand>) → toscroll ( <conversion_value> ) → {toscroll}
PREDICT(<string_more>) → + <string_operand> <string_more> → {+}
PREDICT(<string_more>) → λ → {,, ), ~}
PREDICT(<user-defined_func>) → spell <return_type> id_lit ( <param> ) { <body> <ret_statement> } <user-defined_func> → {spell}
PREDICT(<user-defined_func>) → λ → {castle}
PREDICT(<return_type>) → <data_type> → {rose, ocean, treasures, scroll, mirror}
PREDICT(<return_type>) → chamber → {chamber}
PREDICT(<param>) → <data_type> id_lit <param_more> → {rose, ocean, treasures, scroll, mirror}
PREDICT(<param>) → λ → {)}
PREDICT(<param_more>) → , <data_type> id_lit <param_more> → {,}
PREDICT(<param_more>) → λ → {)}
PREDICT(<body>) → <dynasty> <data_type> id_lit <vardec_def> <body> → {rose, ocean, treasures, dynasty, scroll, mirror}
PREDICT(<body>) → granted ( <granted_content> <more_granted> ) ~ <body> → {granted}
PREDICT(<body>) → id_lit <body_1_ext> <body> → {id_lit}
PREDICT(<body>) → spell <return_type> id_lit ( <param> ) { <body> <ret_statement> } <body> → {spell}
PREDICT(<body>) → tale ( <loop_var> ~ <relational_exp> ~ <unary> ) { <loop_body> } <body> → {tale}
PREDICT(<body>) → cast ( <condition> ) { <body> } <elif> <else> <body> → {cast}
PREDICT(<body>) → forever ( <condition> ) { <loop_body> } <body> → {forever}
PREDICT(<body>) → believe { <loop_body> } forever ( <condition> ) ~ <body> → {believe}
PREDICT(<body>) → λ → {return, continue, break, }}
PREDICT(<body_1_ext>) → ( <args> ) ~ → {(}
PREDICT(<body_1_ext>) → <index> <body_1_other_ext> → {*=, %=, /=, =, +=, [, -=}
PREDICT(<body_1_ext>) → <unary_operator> ~ → {++, --}
PREDICT(<body_1_other_ext>) → = <val> ~ → {=}
PREDICT(<body_1_other_ext>) → <assignment_operator> <assignment_operand> ~ → {*=, %=, /=, +=, -=}
PREDICT(<ret_statement>) → return <val1> ~ → {return}
PREDICT(<ret_statement>) → λ → {}}
PREDICT(<loop_var>) → treasures id_lit = <loop_val> → {treasures}
PREDICT(<loop_var>) → id_lit <loop_init> → {id_lit}
PREDICT(<loop_init>) → = <loop_val> → {=}
PREDICT(<loop_init>) → λ → {~}
PREDICT(<loop_val>) → id_lit → {id_lit}
PREDICT(<loop_val>) → treasures_lit → {treasures_lit}
PREDICT(<loop_body>) → <dynasty> <data_type> id_lit <vardec_def> <loop_body> → {rose, ocean, treasures, dynasty, scroll, mirror}
PREDICT(<loop_body>) → granted ( <granted_content> <more_granted> ) ~ <loop_body> → {granted}
PREDICT(<loop_body>) → id_lit <body_1_ext> <loop_body> → {id_lit}
PREDICT(<loop_body>) → spell <return_type> id_lit ( <param> ) { <body> <ret_statement> } <loop_body> → {spell}
PREDICT(<loop_body>) → tale ( <loop_var> ~ <relational_exp> ~ <unary> ) { <loop_body> } <loop_body> → {tale}
PREDICT(<loop_body>) → cast ( <condition> ) { <loop_body> <flow_control> } <elif_break> <else_break> <loop_body> → {cast}
PREDICT(<loop_body>) → forever ( <condition> ) { <loop_body> } <loop_body> → {forever}
PREDICT(<loop_body>) → believe { <loop_body> } forever ( <condition> ) ~ <loop_body> → {believe}
PREDICT(<loop_body>) → λ → {continue, break, }}
PREDICT(<elif_break>) → twist( <condition> ) { <body> <flow_control> } <elif_break> → {twist(}
PREDICT(<elif_break>) → λ → {spell, granted, ocean, dynasty, scroll, }, tale, mirror, forever, rose, treasures, curse, break, cast, id_lit, continue, believe}        
PREDICT(<else_break>) → curse { <body> <flow_control> } → {curse}
PREDICT(<else_break>) → λ → {spell, granted, ocean, dynasty, scroll, }, tale, mirror, forever, rose, treasures, break, cast, id_lit, continue, believe}
PREDICT(<flow_control>) → break ~ → {break}
PREDICT(<flow_control>) → continue ~ → {continue}
PREDICT(<flow_control>) → λ → {}}
PREDICT(<condition>) → <treasures_mirror> <more_log> → {1, 0}
PREDICT(<condition>) → id_lit <condi_id_ext> → {id_lit}
PREDICT(<condition>) → ! <logical_operand> <more_log> → {!}
PREDICT(<condition>) → mirror_lit <relational_more> <more_log> → {mirror_lit}
PREDICT(<condition>) → <lit3> <more_arith> <relational_operator> <relational_operand> <relational_more> <more_log> → {treasures_lit, ocean_lit}
PREDICT(<condition>) → scroll_lit <relational_operator> <relational_operand> <relational_more> <more_log> → {scroll_lit}
PREDICT(<condition>) → rose_lit <relational_operator> <relational_operand> <relational_more> <more_log> → {rose_lit}
PREDICT(<condition>) → ( <logical_operator1> <expression> <more_log> → {(}
PREDICT(<condi_id_ext>) → <func_call> <other_id_ext> → {(}
PREDICT(<condi_id_ext>) → [ <array_size> ] <column1> <other_id_ext> → {[}
PREDICT(<condi_id_ext>) → <other_id_ext> → {-, <=, <, >=, %, !=, >, *, ==, ), /, +}
PREDICT(<other_id_ext>) → <more_arith> <relational_operator> <relational_operand> <relational_more> <more_log> → {-, <=, /, <, >=, %, !=, >, ==, *, +}
PREDICT(<other_id_ext>) → λ → {)}
PREDICT(<elif>) → twist( <condition> ) { <body> } <elif> → {twist(}
PREDICT(<elif>) → λ → {spell, granted, ocean, dynasty, scroll, }, tale, mirror, forever, rose, treasures, curse, break, cast, id_lit, return, continue, believe}      
PREDICT(<else>) → curse { <body> } → {curse}
PREDICT(<else>) → λ → {spell, granted, ocean, dynasty, scroll, }, tale, mirror, forever, rose, treasures, break, cast, id_lit, return, continue, believe}
PREDICT(<granted_content_1>) → set_precision → {set_precision}
PREDICT(<granted_content_1>) → id_lit <granted_id_ext> → {id_lit}
PREDICT(<granted_content_2>) → phantom → {phantom}
PREDICT(<granted_content_2>) → lengthof ( id_lit <index> ) → {lengthof}
PREDICT(<granted_content_2>) → <conversion_func> ( <conversion_value> ) → {torose, tomirror, totreasures, toocean}
PREDICT(<granted_content_2>) → toscroll ( <conversion_value> ) <string_more> → {toscroll}
PREDICT(<granted_content_2>) → <treasures_mirror> <more_log> → {1, 0}
PREDICT(<granted_content_2>) → mirror_lit <relational_more> <more_log> → {mirror_lit}
PREDICT(<granted_content_2>) → scroll_lit <granted_scroll_ext> → {scroll_lit}
PREDICT(<granted_content_2>) → rose_lit <granted_rose_ext> → {rose_lit}
PREDICT(<granted_content_2>) → <lit3> <granted_lit3_ext> → {treasures_lit, ocean_lit}
PREDICT(<granted_content_2>) → ( <logical_operator1> <granted_open_paren_ext> → {(}
PREDICT(<granted_content_2>) → ! <logical_operand> <more_log> → {!}
PREDICT(<granted_content>) → <granted_content_1> → {id_lit, set_precision}
PREDICT(<granted_content>) → <granted_content_2> → {1, scroll_lit, !, mirror_lit, treasures_lit, toscroll, rose_lit, phantom, ocean_lit, (, tomirror, 0, torose, totreasures, lengthof, toocean}
PREDICT(<granted_open_paren_ext>) → id_lit <id_ext> <idlit3_granted_ext> → {id_lit}
PREDICT(<granted_open_paren_ext>) → <lit3> <idlit3_granted_ext> → {treasures_lit, ocean_lit}
PREDICT(<granted_open_paren_ext>) → scroll_lit <expression_ext_2> <more_log> ) → {scroll_lit}
PREDICT(<granted_open_paren_ext>) → rose_lit <expression_ext_2> <more_log> ) → {rose_lit}
PREDICT(<granted_open_paren_ext>) → mirror_lit <expression_ext_2> <more_log> ) → {mirror_lit}
PREDICT(<granted_open_paren_ext>) → <treasures_mirror> <expression_ext_2> <more_log> ) → {1, 0}
PREDICT(<granted_open_paren_ext>) → ( <logical_operator1> <granted_open_paren_ext> ) <close_paren_ext> → {(}
PREDICT(<idlit3_granted_ext>) → <relational_operator> <relational_operand> <relational_more> <more_log> ) <relational_more> <more_log> → {<=, <, >=, !=, >, ==}       
PREDICT(<idlit3_granted_ext>) → <logical_operator> <logical_operator1> <logical_operand> <more_log> ) <more_log> → {&&, ||}
PREDICT(<idlit3_granted_ext>) → <arithmetic_operator> <arithmetic_operand> <more_arith> <relational_more> ) <more_arith> <open_paren_other_ext> → {-, %, *, /, +}     
PREDICT(<open_paren_other_ext>) → <relational_operator> <relational_operand> <relational_more> <more_log> → {<=, <, >=, !=, >, ==}
PREDICT(<open_paren_other_ext>) → <logical_operator> <logical_operator1> <logical_operand> <more_log> → {&&, ||}
PREDICT(<open_paren_other_ext>) → λ → {,, ), ~}
PREDICT(<close_paren_ext>) → <relational_operator> <relational_operand> <relational_more> <more_log> → {<=, <, >=, !=, >, ==}
PREDICT(<close_paren_ext>) → <logical_operator> <logical_operator1> <logical_operand> <more_log> → {&&, ||}
PREDICT(<close_paren_ext>) → <arithmetic_operator> <arithmetic_operand> <more_arith> <open_paren_other_ext> → {-, %, *, /, +}
PREDICT(<close_paren_ext>) → λ → {,, ), ~}
PREDICT(<granted_id_ext>) → <unary_operator> → {++, --}
PREDICT(<granted_id_ext>) → <func_call> <granted_other_id_ext> → {(}
PREDICT(<granted_id_ext>) → [ <array_size> ] <column1> <granted_other_id_ext> → {[}
PREDICT(<granted_id_ext>) → <granted_other_id_ext> → {-, <=, ~, <, >=, %, !=, >, *, ,, ==, ), &&, ||, /, +}
PREDICT(<granted_other_id_ext>) → + <plus_ext> → {+}
PREDICT(<granted_other_id_ext>) → - <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {-}
PREDICT(<granted_other_id_ext>) → * <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {*}
PREDICT(<granted_other_id_ext>) → / <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {/}
PREDICT(<granted_other_id_ext>) → % <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {%}
PREDICT(<granted_other_id_ext>) → <relational_operator> <relational_operand> <relational_more> <more_log> → {<=, <, >=, !=, >, ==}
PREDICT(<granted_other_id_ext>) → <logical_operator> <logical_operator1> <logical_operand> <more_log> → {&&, ||}
PREDICT(<granted_other_id_ext>) → λ → {,, ), ~}
PREDICT(<granted_other_id_ext2>) → <relational_operator> <relational_operand> <relational_more> <more_log> → {<=, <, >=, !=, >, ==}
PREDICT(<granted_other_id_ext2>) → λ → {,, ), ~}
PREDICT(<plus_ext>) → id_lit <plus_ext_1> → {id_lit}
PREDICT(<plus_ext>) → toscroll <string_more> → {toscroll}
PREDICT(<plus_ext>) → scroll_lit <string_more> → {scroll_lit}
PREDICT(<plus_ext>) → rose_lit <string_more> → {rose_lit}
PREDICT(<plus_ext>) → ( <arithmetic_exp> ) <more_arith> <granted_other_id_ext2> → {(}
PREDICT(<plus_ext>) → treasures_lit <more_arith> <granted_other_id_ext2> → {treasures_lit}
PREDICT(<plus_ext>) → ocean_lit <more_arith> <granted_other_id_ext2> → {ocean_lit}
PREDICT(<plus_ext_1>) → + <plus_ext> → {+}
PREDICT(<plus_ext_1>) → - <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {-}
PREDICT(<plus_ext_1>) → * <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {*}
PREDICT(<plus_ext_1>) → / <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {/}
PREDICT(<plus_ext_1>) → % <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {%}
PREDICT(<plus_ext_1>) → λ → {,, ), ~}
PREDICT(<granted_scroll_ext>) → + <string_operand> <string_more> → {+}
PREDICT(<granted_scroll_ext>) → <relational_operator> <relational_operand> <relational_more> <more_log> → {<=, <, >=, !=, >, ==}
PREDICT(<granted_scroll_ext>) → λ → {,, ), ~}
PREDICT(<granted_rose_ext>) → + <string_operand> <string_more> → {+}
PREDICT(<granted_rose_ext>) → <relational_operator> <relational_operand> <relational_more> <more_log> → {<=, <, >=, !=, >, ==}
PREDICT(<granted_rose_ext>) → λ → {,, ), ~}
PREDICT(<granted_lit3_ext>) → <arithmetic_operator> <arithmetic_operand> <more_arith> <granted_lit3_ext1> → {-, %, *, /, +}
PREDICT(<granted_lit3_ext>) → <relational_operator> <relational_operand> <relational_more> <more_log> → {<=, <, >=, !=, >, ==}
PREDICT(<granted_lit3_ext>) → λ → {,, ), ~}
PREDICT(<granted_lit3_ext1>) → <relational_operator> <relational_operand> <relational_more> <more_log> → {<=, <, >=, !=, >, ==}
PREDICT(<granted_lit3_ext1>) → λ → {,, ), ~}
PREDICT(<more_granted>) → , <granted_content> <more_granted> → {,}
PREDICT(<more_granted>) → λ → {)}
PREDICT(<data_type>) → scroll → {scroll}
PREDICT(<data_type>) → treasures → {treasures}
PREDICT(<data_type>) → mirror → {mirror}
PREDICT(<data_type>) → ocean → {ocean}
PREDICT(<data_type>) → rose → {rose}
PREDICT(<val>) → <granted_content_2> → {1, scroll_lit, !, mirror_lit, treasures_lit, toscroll, rose_lit, phantom, ocean_lit, (, tomirror, 0, torose, totreasures, lengthof, toocean}
PREDICT(<val>) → id_lit <granted_id_ext> → {id_lit}
PREDICT(<val>) → <input> → {wish}
PREDICT(<val1>) → <granted_content_2> → {1, scroll_lit, !, mirror_lit, treasures_lit, toscroll, rose_lit, phantom, ocean_lit, (, tomirror, 0, torose, totreasures, lengthof, toocean}
PREDICT(<val1>) → id_lit <val1_ext> → {id_lit}
PREDICT(<val1_ext>) → <val1_id_ext> → {~, *=, %=, /=, +=, -=}
PREDICT(<val1_ext>) → <func_call> <val1_id_ext> → {(}
PREDICT(<val1_ext>) → [ <array_size> ] <column1> <val1_id_ext> → {[}
PREDICT(<val1_ext>) → <unary_operator> → {++, --}
PREDICT(<val1_ext>) → + <plus_ext> → {+}
PREDICT(<val1_ext>) → - <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {-}
PREDICT(<val1_ext>) → * <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {*}
PREDICT(<val1_ext>) → / <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {/}
PREDICT(<val1_ext>) → % <arithmetic_operand> <more_arith> <granted_other_id_ext2> → {%}
PREDICT(<val1_ext>) → <relational_operator> <relational_operand> <relational_more> <more_log> → {<=, <, >=, !=, >, ==}
PREDICT(<val1_ext>) → <logical_operator> <logical_operator1> <logical_operand> <more_log> → {&&, ||}
PREDICT(<val1_id_ext>) → <assignment_operator> <assignment_operand> → {*=, %=, /=, +=, -=}
PREDICT(<val1_id_ext>) → λ → {~}
PREDICT(<conversion_func>) → torose → {torose}
PREDICT(<conversion_func>) → totreasures → {totreasures}
PREDICT(<conversion_func>) → toocean → {toocean}
PREDICT(<conversion_func>) → tomirror → {tomirror}
PREDICT(<conversion_value>) → <lit4> → {scroll_lit, mirror_lit, treasures_lit, rose_lit, ocean_lit}
PREDICT(<conversion_value>) → id_lit <id_ext> → {id_lit}
PREDICT(<index>) → [ <array_size> ] <column1> → {[}
PREDICT(<index>) → λ → {+=, ), -=, *=, %=, /=, =}
PREDICT(<column1>) → [ <array_size> ] → {[}
PREDICT(<column1>) → λ → {-, *=, !=, %, /=, &&, ||, <=, ~, <, >=, %=, ,, =, >, *, ==, ), +=, /, -=, +}
PREDICT(<input>) → wish ( scroll_lit ) → {wish}
PREDICT(<lit1>) → scroll_lit → {scroll_lit}
PREDICT(<lit1>) → rose_lit → {rose_lit}
PREDICT(<lit2>) → mirror_lit → {mirror_lit}
PREDICT(<lit3>) → ocean_lit → {ocean_lit}
PREDICT(<lit3>) → treasures_lit → {treasures_lit}
PREDICT(<lit4>) → <lit1> → {scroll_lit, rose_lit}
PREDICT(<lit4>) → <lit2> → {mirror_lit}
PREDICT(<lit4>) → <lit3> → {treasures_lit, ocean_lit}
PREDICT(<func_call>) → ( <args> ) → {(}
PREDICT(<args>) → <args_val> <args_more> → {scroll_lit, mirror_lit, treasures_lit, rose_lit, ocean_lit, id_lit}
PREDICT(<args>) → λ → {)}
PREDICT(<args_val>) → id_lit <id_ext> → {id_lit}
PREDICT(<args_val>) → <lit4> → {scroll_lit, mirror_lit, treasures_lit, rose_lit, ocean_lit}
PREDICT(<args_more>) → , <args_val> <args_more> → {,}
PREDICT(<args_more>) → λ → {)}
PREDICT(<id_ext>) → <func_call> → {(}
PREDICT(<id_ext>) → [ <array_size> ] <column1> → {[}
PREDICT(<id_ext>) → λ → {-, /, %, !=, &&, ||, <=, ~, <, >=, >, ,, ==, ), *, +}
PREDICT(<array_size>) → id_lit → {id_lit}
PREDICT(<array_size>) → positive_treasures_lit → {positive_treasures_lit}
"""  
    
    lines = input_text.strip().split('\n')
    entries = convert_predict_table(lines)
    output = format_predict_dict(entries)
    print(output)