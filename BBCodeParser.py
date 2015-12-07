#!python3.4
# BBCodeParser 1.0
# Written by Dylan5797 [https://dylan5797.github.io]

def parse_bbcode(bc):
    tokens_found = []
    current_text = ''
    count = -1
    parsing_tag = False
    in_code = False
    code_init = False
    for x in bc:
        count += 1
        if parsing_tag:
            current_text = current_text + x
            if x == ']':
                tokens_found.append({'id':'tag', 'value':current_text})
                parsing_tag = False
                current_text = ''
                continue
            if code_init:
                in_code = True
                code_init = False
        else:
            try: n1 = bc[count]; n2 = bc[count]
            except: n1 = ''; n2 = ''
            if x[0] == '[' and (not (n1 == '[' and n2 == ']')) and (not in_code):
                tokens_found.append({'id':'text', 'value':current_text})
                current_text = '['
                parsing_tag = True
                if bc[count:count+6] == '[code]':
                    code_init = True
                continue
            elif in_code and bc[count:count+7] == '[/code]':
                tokens_found.append({'id':'text', 'value':current_text})
                current_text = '['
                parsing_tag = True
                in_code = False
                continue                
            else:
                current_text = current_text + x
    tokens_found.append({'id':'text', 'value':current_text})
    def recur(tokens, dep=0):
        output = []
        if dep > 0:
            name = tokens[0]['value'][1:-1]
        counted = 0
        skip = 0
        bump = ['']
        for x in tokens:
            bump.append(x)
        for x in tokens:
            counted = counted + 1
            bump = bump[1:]
            if skip > 0:
                skip = skip - 1
                continue
            if dep > 0 and len(bump) == len(tokens):
                continue
            if dep > 0:
                if x['value'] == '[/' + name + ']':
                    break
            if x['id'] == 'text':
                output.append(x['value'])
            else:
                re = recur(bump, dep + 1)
                skip = re[1]
                output.append({'tag':x['value'], 'value':re[0]})
        if dep > 0:
            return [output, counted - 1]
        else:
            return output
    return recur(tokens_found)
